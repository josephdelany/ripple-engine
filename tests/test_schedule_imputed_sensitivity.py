import inspect
from pathlib import Path

import numpy as np
import pytest

import schedule_imputed_sensitivity as S


def test_admission_rule_is_closed_world_and_has_no_outcome_input():
    assert list(inspect.signature(S.admission_reason).parameters) == ["row", "event_date"]
    good = ("e", "cinc", "1990-01-01", 1.0, None, "country.x", "1991-01-01",
            "2026-01-01", 0, "COW National Material Capabilities v7.0 (NMC-70-abridged.csv)")
    assert S.admission_reason(good, "1992-01-01") == "admitted"
    assert S.admission_reason(good, "1990-12-31") == "vintage_after_event"
    assert S.admission_reason((*good[:9], "invented source"), "1992-01-01") == "source_not_allowlisted"
    assert S.admission_reason((good[0], "wti_daily", *good[2:]), "1992-01-01") == "field_not_allowlisted"


def test_retrospective_and_situation_rows_can_never_enter():
    source = "COW National Material Capabilities v7.0 (NMC-70-abridged.csv)"
    base = ("e", "cinc", "1990-01-01", 1.0, None, "country.x", "1991-01-01", "2026-01-01", 0, source)
    assert S.admission_reason((*base[:8], 1, source), "2000-01-01") == "retrospective"
    assert S.admission_reason((*base[:5], "situation", *base[6:]), "2000-01-01") == "entity_is_situation"


def test_allowlists_exactly_match_frozen_registration_text():
    text = S.REGISTRATION.read_text(encoding="utf-8")
    for field in S.FIELD_BLOCKS:
        assert f"`{field}`" in text
    for source in S.ALLOWED_SOURCES:
        assert f"`{source}`" in text
    assert "wti_daily" not in S.FIELD_BLOCKS
    assert "opec_decision_dated" not in S.FIELD_BLOCKS


def test_bundle_admission_is_fail_closed_and_only_allowlisted(tmp_path):
    conn = S.connect_bundle(S.BUNDLE)
    try:
        vectors, metadata, receipt = S.admitted_panel(conn)
    finally:
        conn.close()
    assert receipt["n_rows"] == 11_089
    assert receipt["n_admitted"] > 0
    assert sum(receipt["first_exclusion_reason_counts"].values()) == receipt["n_rows"]
    assert receipt["first_exclusion_reason_counts"]["field_not_allowlisted"] > 0
    assert receipt["overlapping_exclusion_rule_counts"]["source_not_allowlisted"] > 0
    for event in vectors.values():
        assert all(key.removeprefix("panel:") in S.FIELD_BLOCKS for key in event)
    for event in metadata.values():
        assert all(meta["block"] != "market" for meta in event.values())


def test_one_nonmarket_field_augments_combined_arm_but_not_standalone_diagnostic():
    target = {"panel:polity2": 5.0}
    candidate = {"panel:polity2": 2.0}
    meta = {"panel:polity2": {"kind": "num", "block": "actors"}}
    history = [(f"19{i:02d}-01-01", {"panel:polity2": float(i)}) for i in range(40)]
    detail = S.nonmarket_distance(target, candidate, history, "2000-01-01", meta, meta)
    assert detail is not None
    assert detail["n_fields"] == 1
    assert detail["blocks"].keys() == {"actors"}
    assert detail["n_fields"] < S.MIN_FIELDS


def test_prepare_preserves_all_frozen_support_without_reading_scores(monkeypatch):
    original = S.load_jsonl
    def guarded(path):
        assert Path(path) != S.SCORES, "design preparation opened realized target outcomes"
        return original(path)
    monkeypatch.setattr(S, "load_jsonl", guarded)
    designs, admission = S.prepare_designs()
    reads = original(S.READS)
    assert len(designs) == len(reads) == 264
    for design, read in zip(designs, reads):
        assert design["event_id"] == read["event_id"]
        assert design["date"] == read["date"]
        assert design["candidate_ids"] == read["candidate_ids"]
        assert len(design["distances"]["availability_state"]) == len(read["candidate_ids"])
        assert design["atoms_sha256"] == S.hashlib.sha256(
            S.canonical(read["forecasts"]["20"]["abnormal_atoms"]).encode()
        ).hexdigest()
    assert admission["pairwise_block_combination_counts"]


def test_every_primary_arm_hits_the_same_registered_effective_size():
    designs, _ = S.prepare_designs()
    for design in designs:
        target = design["common_target_effective_n"]
        for name in ("market_matched", "availability_state_matched", "event_class_matched"):
            assert S.effective_n(design["weights"][name]) == pytest.approx(target, abs=S.TOL)


def test_nonmarket_diagnostic_is_explicitly_restricted_and_never_changes_primary_support():
    designs, admission = S.prepare_designs()
    defined = [d for d in designs if d["nonmarket_only_diagnostic"] is not None]
    assert len(defined) == admission["nonmarket_only_defined_on_all_candidates_dates"]
    assert len(defined) <= len(designs) == 264
    for design in defined:
        diagnostic = design["nonmarket_only_diagnostic"]
        assert len(diagnostic["distances"]) == len(design["candidate_ids"])
        assert len(diagnostic["weights_tau_0_25"]) == len(design["candidate_ids"])
        assert sum(diagnostic["weights_tau_0_25"]) == pytest.approx(1.0)


def test_scoring_math_on_synthetic_data_only(monkeypatch):
    designs = [{
        "event_id": "e", "date": "2000-01-01", "read_hash": "h", "candidate_ids": ["a", "b"],
        "atoms_sha256": S.hashlib.sha256(S.canonical([-1.0, 2.0]).encode()).hexdigest(),
        "weights": {
            "market_matched": [0.5, 0.5], "availability_state_matched": [0.75, 0.25],
            "event_class_matched": [0.25, 0.75],
        },
    }]
    reads = [{"event_id": "e", "date": "2000-01-01", "hash": "h", "candidate_ids": ["a", "b"],
              "forecasts": {"20": {"abnormal_atoms": [-1.0, 2.0]}}}]
    scores = [{"event_id": "e", "date": "2000-01-01", "read_hash": "h", "outcome": 0.0}]
    monkeypatch.setattr(S, "load_jsonl", lambda path: reads if Path(path).name == "reads.jsonl" else scores)
    monkeypatch.setattr(S, "paired_block", lambda a, b, dates, n: {
        "n": len(a), "mean_diff": float(np.mean(a-b)), "ci95": [-1, 1],
        "dm": {"p_value": 0.5}, "n_boot": n,
    })
    rows, summary = S.score_designs(designs, n_boot=3)
    assert len(rows) == 1
    assert set(summary["primary"]) == {
        "availability_state_minus_market_matched",
        "availability_state_minus_event_class_matched",
    }
    assert all(x["dm_p_holm"] == 1.0 for x in summary["primary"].values())


def test_publication_remains_blocked_by_the_recorded_user_ruling():
    assert S.IMPLEMENTATION_COMMIT == "9265ec5a5d4779ccc81a6fbcb2ecc8335b771c03"
    assert S.PUBLICATION_AUTHORIZED is False
    with pytest.raises(RuntimeError, match="not authorized"):
        S.publish(out_dir=Path("unused"))
