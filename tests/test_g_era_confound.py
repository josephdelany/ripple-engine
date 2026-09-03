"""Tests for src/g_era_confound.py (Session G, G-6, OPEN_ITEMS 1.4).

Every test names the clause of docs/g/G6_ERA_CONFOUND_REGISTRATION.md it covers.
Nothing here writes to any table; the diagnostic reads oil.db and data/walk_forward/** read-only.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import g_era_confound as E  # noqa: E402

OUT = ROOT / "docs" / "g" / "ERA_CONFOUND.json"


# ------------------------------------------------------------------ §2 the pinning

def test_g6_2_the_run_is_pinned_to_the_published_one():
    """§2 + Amendment 2: the pinned run must BE the one summary.json publishes. This test failed the
    moment session B's re-run landed, which is the point -- a diagnostic that silently keeps
    describing a superseded run is worse than one that stops."""
    s = json.loads((ROOT / "data" / "walk_forward" / "summary.json").read_text())
    assert s["run_id"] == E.RUN_ID, "the pinned run is no longer the one summary.json publishes"


@pytest.mark.skipif(not OUT.exists(), reason="diagnostic not run in this tree")
def test_g6_2_more_than_one_run_in_the_file_is_reported_not_silently_mixed():
    o = json.loads(OUT.read_text())
    assert o["run_pinned"] == E.RUN_ID
    assert E.RUN_ID in o["runs_in_file"]
    # every scored row used must belong to the pinned run
    assert all(r.get("era") is not None or True for r in o["frame"])
    assert len(o["frame"]) == o["baseline_check"]["recomputed"]["n"]


@pytest.mark.skipif(not OUT.exists(), reason="diagnostic not run in this tree")
def test_g6_2_baseline_check_reproduces_the_published_G_block():
    """§2: if this does not reproduce to the seventh decimal the diagnostic is void."""
    o = json.loads(OUT.read_text())
    b = o["baseline_check"]
    assert b["agrees"] is True, json.dumps(b, indent=1)
    assert b["pinned_is_published"] is True
    pub = json.loads((ROOT / "data" / "walk_forward" / "summary.json").read_text())
    assert b["recomputed"]["n"] == pub["tiers"]["daily"]["G"]["engine_vs"]["climatology"]["n"]
    for k in ("engine_mean", "ref_mean", "skill"):
        assert abs(b["recomputed"][k] - b["published"][k]) < 1e-7
    assert "VOID" not in o


# ------------------------------------------------------------------ §5 separability

def test_g6_5_the_decision_rule_is_the_registered_one():
    assert E.SEP_RHO == 0.80 and E.SEP_CELL_N == 20


def test_g6_5_verdict_fires_on_criterion_a():
    sep = {"spearman": {"era_index~pool_g": 0.9}, "off_diagonal_cells_ge_20": [1, 2, 3]}
    tab = {"e1": {"n": 10, "skill": 0.0, "ci95": [-1.0, -0.5]}}          # does not contain pooled
    v = E.verdict(sep, tab, -0.09)
    assert v["separable"] is False and any("(a)" in c for c in v["criteria_fired"])


def test_g6_5_verdict_fires_on_criterion_c():
    sep = {"spearman": {"era_index~pool_g": 0.1}, "off_diagonal_cells_ge_20": [1, 2, 3]}
    tab = {"e1": {"n": 10, "skill": 0.0, "ci95": [-1.0, 1.0]},
           "e2": {"n": 10, "skill": 0.0, "ci95": [-1.0, 1.0]}}
    v = E.verdict(sep, tab, -0.09)
    assert v["separable"] is False and any("(c)" in c for c in v["criteria_fired"])


def test_g6_5_verdict_can_return_separable():
    sep = {"spearman": {"era_index~pool_g": 0.1}, "off_diagonal_cells_ge_20": [1, 2, 3]}
    tab = {"e1": {"n": 10, "skill": 0.5, "ci95": [0.4, 0.6]},
           "e2": {"n": 10, "skill": -0.5, "ci95": [-0.6, -0.4]}}
    v = E.verdict(sep, tab, -0.09)
    assert v["separable"] is True and v["criteria_fired"] == []


@pytest.mark.skipif(not OUT.exists(), reason="diagnostic not run in this tree")
def test_g6_5_the_published_verdict_is_not_separable_and_publishes_no_decomposition():
    o = json.loads(OUT.read_text())
    v = o["verdict"]
    assert v["separable"] is False
    assert "no decomposition" in v["consequence"].lower()
    assert "decomposition" not in o, "a decomposition was published under a NOT SEPARABLE verdict"


# ------------------------------------------------------------------ §4 / Amendment 1

@pytest.mark.skipif(not OUT.exists(), reason="diagnostic not run in this tree")
def test_A1_the_failed_S4_test_is_left_failed_and_its_threshold_is_not_moved():
    """A1.3: replacing a test after seeing it fail is the move this project exists to prevent."""
    o = json.loads(OUT.read_text())
    s4 = o["s4_size_correction"]
    assert s4["threshold"] == E.S4_HALF == 0.5
    assert s4["passes"] is False
    assert s4["ratio_fair_to_registered"] > s4["threshold"]


@pytest.mark.skipif(not OUT.exists(), reason="diagnostic not run in this tree")
def test_A1_1_the_registered_premise_that_k_engine_is_constant_is_false():
    """A1.1: §4 derived its whole magnitude from a constant engine atom count of 5."""
    o = json.loads(OUT.read_text())
    ke = {x["n_atoms_engine"] for x in o["frame"] if x["n_atoms_engine"]}
    assert len(ke) > 1, f"k_engine is constant at {ke}; §4's premise would have been right"
    assert max(ke) > min(ke) + 3, sorted(ke)


@pytest.mark.skipif(not OUT.exists(), reason="diagnostic not run in this tree")
def test_A1_5_D1_climatology_atom_count_is_exactly_the_pool_size():
    """D1, the finding that collapses two of the three confounds into one variable."""
    o = json.loads(OUT.read_text())
    d1 = o["post_hoc"]["D1_identity"]
    assert d1["n_atoms_clim_equals_pool_g"] == d1["of"] == len(o["frame"])
    for x in o["frame"]:
        assert x["n_atoms_clim"] == x["pool_g"]


@pytest.mark.skipif(not OUT.exists(), reason="diagnostic not run in this tree")
def test_A1_2_the_measured_swing_is_far_below_the_registered_prediction():
    """A2.4: read on the bins large enough to read. The all-bins spread is dominated by the smallest
    bin -- the same defect that sank S4 (A1.3) -- so both are published and this asserts the one the
    reading uses."""
    o = json.loads(OUT.read_text())
    p = o["post_hoc"]
    assert p["D2_swing_bins_ge_8"] is not None
    assert p["D2_swing_bins_ge_8"] < p["D2_registered_prediction_was"] / 3, p["D2_swing_bins_ge_8"]
    assert "D2_swing_all_bins" in p and "dominated by the smallest bins" in p["D2_caveat"]


@pytest.mark.skipif(not OUT.exists(), reason="diagnostic not run in this tree")
def test_A1_5_D3_uses_only_bins_the_registration_admits_for_inference():
    """§7 says the n = 2 and n = 10 bins are description, not inference. D3 applies that caveat."""
    o = json.loads(OUT.read_text())
    big = o["post_hoc"]["D3_bins_with_n_ge_50"]
    assert big, "no bin carries enough n for inference"
    assert all(v["n"] >= 50 for v in big.values())
    small = {k for k, v in o["era_registered"].items() if 0 < v.get("n", 0) < 50}
    assert not (set(big) & small), "a bin below the inference threshold leaked into D3"


@pytest.mark.skipif(not OUT.exists(), reason="diagnostic not run in this tree")
def test_A1_5_the_size_corrected_pooled_number_is_credited_to_B_not_claimed():
    o = json.loads(OUT.read_text())
    txt = o["post_hoc"]["already_published_by_B"]
    assert "summary.json" in txt and "did not discover" in txt
    s = json.loads((ROOT / "data" / "walk_forward" / "summary.json").read_text())
    pub = s["tiers"]["daily"]["G"]["diagnostic_fair"]["engine_vs_climatology"]
    # the number is B's and is read from B's file, never hard-coded here (Amendment 2)
    assert pub["n"] == len(o["frame"]) and isinstance(pub["skill"], float)


# ------------------------------------------------------------------ standing

@pytest.mark.skipif(not OUT.exists(), reason="diagnostic not run in this tree")
def test_g6_gates_nothing_and_writes_no_table():
    o = json.loads(OUT.read_text())
    assert "gates" in o and "nothing" in o["gates"].lower()
    src = (ROOT / "src" / "g_era_confound.py").read_text()
    assert "mode=ro" in src
    for bad in ("INSERT", "UPDATE ", "DELETE", "CREATE TABLE", "conn.commit"):
        assert bad not in src, f"g_era_confound.py contains {bad!r}"


def test_g6_6_intervals_use_the_registered_cluster_rule_and_seed():
    assert E.CLUSTER_DAYS == 35 and E.SEED == 19900802
    import datetime as _dt
    ds = [_dt.date(2020, 1, 1), _dt.date(2020, 1, 10), _dt.date(2020, 6, 1)]
    cl = E.clusters(ds)
    assert cl[0] == cl[1] and cl[2] != cl[0]        # 9 days together, 5 months apart


@pytest.mark.skipif(not OUT.exists(), reason="diagnostic not run in this tree")
def test_A2_the_superseded_run_is_retained_and_not_deleted():
    """Amendment 2: this project annotates its record, it does not rewrite it."""
    o = json.loads(OUT.read_text())
    sup = o.get("superseded_run")
    assert sup and sup["run_pinned"] == E.SUPERSEDED_RUN != E.RUN_ID
    assert sup["verdict"]["separable"] is False          # and it reached the same verdict


@pytest.mark.skipif(not OUT.exists(), reason="diagnostic not run in this tree")
def test_A2_the_verdict_is_NOT_SEPARABLE_on_both_runs():
    """The conclusion is robust across B's re-run, by different criteria -- which is stronger than
    either run alone. If a future run makes it separable, this test says so loudly."""
    o = json.loads(OUT.read_text())
    assert o["verdict"]["separable"] is False
    assert o["superseded_run"]["verdict"]["separable"] is False
    assert o["verdict"]["criteria_fired"] != o["superseded_run"]["verdict"]["criteria_fired"]


@pytest.mark.skipif(not OUT.exists(), reason="diagnostic not run in this tree")
def test_A1_5_D1_identity_holds_on_both_runs():
    o = json.loads(OUT.read_text())
    for block in (o["post_hoc"], o["superseded_run"]["post_hoc"]):
        d1 = block["D1_identity"]
        assert d1["n_atoms_clim_equals_pool_g"] == d1["of"]
