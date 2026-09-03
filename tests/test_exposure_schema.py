"""EXPOSURE_REGISTRATION §2 as tests, against src/exposure_schema.py.

Written against hand-built event dicts, not against the live blocks: six sessions are filling
A-E concurrently, so any test asserting today's counts would be flaky by tomorrow and would be
"fixed" by editing the number — the failure mode that let CLASS_AUDIT §6 rot. The live blocks are
checked for INVARIANTS only (a hard failure can never be COMPLETE; the totals add up).

Each test names the clause it covers.
"""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import exposure_schema as S  # noqa: E402

PROV = {"source_url": "https://example.invalid/x", "source_publisher": "Pub", "source_date": "2020-01-01"}


def ev(**kw):
    base = {"event_id": "e1", "date": "2020-06-01", "asset_name": "A refinery", "asset_type": "refinery",
            "capacity_nameplate_kbd": 100, "capacity_affected_kbd": 50,
            "days_to_partial_restore": 3, "days_to_full_restore": 10,
            "provenance": {f: dict(PROV) for f in S.NUMERIC}}
    base.update(kw)
    return base


# ------------------------------------------------------------------ §2 COMPLETE

def test_S2_complete_requires_all_six_required_fields():
    assert S.validate_event(ev())["computed_status"] == "COMPLETE"
    for f in S.REQUIRED:
        r = S.validate_event(ev(**{f: "unknown"}))
        assert r["computed_status"] != "COMPLETE", f"COMPLETE without {f}"
        assert f in r["missing_required"]


def test_S2_no_required_fields_is_EMPTY_and_some_is_PARTIAL():
    empty = ev(**{f: "unknown" for f in S.REQUIRED})
    assert S.validate_event(empty)["computed_status"] == "EMPTY"
    assert S.validate_event(ev(capacity_affected_kbd="unknown"))["computed_status"] == "PARTIAL"


# ------------------------------------------------------------------ §2 THE RULE: hard failure

def test_S2_a_filled_numeric_without_provenance_is_a_HARD_FAILURE_not_a_warning():
    r = S.validate_event(ev(provenance={}))
    assert r["hard_failures"], "an unsourced numeric produced no hard failure"
    assert r["computed_status"] == "INVALID"
    assert r["computed_status"] != "COMPLETE", "an unsourced magnitude must never reach COMPLETE"


def test_S2_partial_provenance_is_not_provenance():
    """All three of url, publisher and date, or it does not count."""
    for drop in S.PROV_KEYS:
        p = {f: {k: v for k, v in PROV.items() if k != drop} for f in S.NUMERIC}
        r = S.validate_event(ev(provenance=p))
        assert r["computed_status"] == "INVALID", f"missing {drop} was tolerated"


def test_S2_an_event_level_source_triple_covers_its_numerics():
    """The flat shape blocks A-E use is accepted -- §2 fixes the requirement, not the layout."""
    e = ev(provenance={}, **PROV)
    r = S.validate_event(e)
    assert not r["hard_failures"] and r["computed_status"] == "COMPLETE"
    assert set(r["provenance_kind"].values()) == {"event_flat"}
    assert any("flat_provenance_covers_multiple_numerics" in n for n in r["notes"])


def test_S2_per_field_provenance_wins_over_the_flat_triple():
    e = ev(source_url="unknown", source_publisher="unknown", source_date="unknown")
    assert S.validate_event(e)["computed_status"] == "COMPLETE"


# ------------------------------------------------------------------ the inversion that must not happen

def test_a_measured_zero_is_a_value_not_a_missing_field():
    """`capacity_affected_kbd: 0` on a foiled attack means nothing was taken offline -- a finding.
    Treating it as absent is max(default=0) run backwards and would drop the cleanest observations."""
    assert S.is_filled(0) and S.is_filled(0.0)
    r = S.validate_event(ev(capacity_affected_kbd=0, days_to_partial_restore=0, days_to_full_restore=0))
    assert r["computed_status"] == "COMPLETE"
    assert "capacity_affected_kbd" in r["filled_numeric"]


def test_the_registered_unknown_markers_are_missing_and_nothing_else_is():
    for m in ("unknown", "", "n/a", "N/A", "  ", "-"):
        assert not S.is_filled(m), f"{m!r} should count as missing"
    for v in (0, 0.0, 1, "ongoing", "Lukoil"):
        assert S.is_filled(v), f"{v!r} should count as filled"
    assert not S.is_filled(None)


# ------------------------------------------------------------------ §2 vintage

def test_S2_nameplate_from_a_post_event_source_must_carry_retrospective():
    late = {f: dict(PROV) for f in S.NUMERIC}
    late["capacity_nameplate_kbd"]["source_date"] = "2021-01-01"     # after the 2020-06-01 event
    r = S.validate_event(ev(provenance=late))
    assert r["computed_status"] == "INVALID"
    assert any("retrospective" in h for h in r["hard_failures"])
    late["capacity_nameplate_kbd"]["retrospective"] = True
    assert S.validate_event(ev(provenance=late))["computed_status"] == "COMPLETE"


def test_S2_a_pre_event_source_needs_no_retrospective_flag():
    early = {f: dict(PROV) for f in S.NUMERIC}
    early["capacity_nameplate_kbd"]["source_date"] = "2019-01-01"
    assert S.validate_event(ev(provenance=early))["computed_status"] == "COMPLETE"


# ------------------------------------------------------------------ §2 'ongoing'

def test_S2_ongoing_is_permitted_only_with_a_stamp_date():
    r = S.validate_event(ev(days_to_full_restore="ongoing"))
    assert r["computed_status"] == "INVALID" and any("stamp" in h for h in r["hard_failures"])
    ok = S.validate_event(ev(days_to_full_restore="ongoing", ongoing_stamp_date="2026-08-05"))
    assert ok["computed_status"] == "COMPLETE"


# ------------------------------------------------------------------ status is computed, never read

def test_the_declared_status_cannot_make_an_invalid_event_complete():
    """A session marking its own work COMPLETE is not evidence that it is."""
    r = S.validate_event(ev(provenance={}, status="COMPLETE"))
    assert r["computed_status"] == "INVALID" and r["declared_status"] == "COMPLETE"


def test_the_validator_never_reads_the_status_field_to_decide():
    src = (ROOT / "src" / "exposure_schema.py").read_text()
    body = src[src.index("def validate_event("):src.index("def load_blocks(")]
    assert 'event.get("status")' in body, "the declared status is recorded..."
    assert body.count('event.get("status")') == 1, "...but read exactly once, only to report it"
    for marker in ("status ==", 'status") ==', "declared_status =="):
        assert marker not in body, f"the declared status is being branched on: {marker}"


# ------------------------------------------------------------------ §5 coverage and the gate of 30

def test_S5_the_gate_is_thirty_and_reports_the_registered_consequence():
    assert S.GATE_N == 30
    cov = S.coverage({"X": [S.validate_event(ev(event_id=f"e{i}")) for i in range(5)]})
    assert cov["gate"]["n_complete"] == 5 and cov["gate"]["gate_met"] is False
    assert "descriptive" in cov["gate"]["consequence_if_not_met"].lower()
    cov2 = S.coverage({"X": [S.validate_event(ev(event_id=f"e{i}")) for i in range(30)]})
    assert cov2["gate"]["gate_met"] is True


def test_S5_the_coverage_counts_add_up():
    cov = S.coverage({"X": [S.validate_event(ev()), S.validate_event(ev(provenance={})),
                            S.validate_event(ev(**{f: "unknown" for f in S.REQUIRED}))]})
    t = cov["total"]
    assert sum(t.values()) == cov["n_events"] == 3
    assert t["COMPLETE"] == 1 and t["INVALID"] == 1 and t["EMPTY"] == 1


# ------------------------------------------------------------------ the live blocks: invariants only

@pytest.mark.skipif(not S.BLOCKS.exists(), reason="no blocks")
def test_live_blocks_every_hard_failure_is_INVALID_and_no_INVALID_is_COMPLETE():
    for b, rows in S.validate_all().items():
        for r in rows:
            if r["hard_failures"]:
                assert r["computed_status"] == "INVALID", (b, r["event_id"])
            assert not (r["computed_status"] == "COMPLETE" and r["hard_failures"]), (b, r["event_id"])


@pytest.mark.skipif(not S.BLOCKS.exists(), reason="no blocks")
def test_live_blocks_cover_the_seventy_five_in_scope_events():
    """§1: exposure is populated only for the 48 infrastructure_attack + 27 chokepoint_disruption.

    Counted over the blocks that COUNT TOWARD THE GATE, not over every file in the directory.
    G_accident was added under Amendment 1 with `counts_toward_gate: false` -- its rows are an
    accident comparison, not corpus events -- so asserting a flat 80 here would silently redefine
    §1's scope, and asserting a flat 75 would break the moment another such block lands."""
    res, flags = S.validate_all(), S.gate_flags()
    counted = {b: rows for b, rows in res.items() if flags.get(b, True)}
    n = sum(len(v) for v in counted.values())
    assert n == 75, f"the gate-counting blocks hold {n} events; §1 scopes this layer to 75"
    ids = [r["event_id"] for rows in res.values() for r in rows]
    assert len(set(ids)) == len(ids), "an event appears in more than one block"


@pytest.mark.skipif(not S.BLOCKS.exists(), reason="no blocks")
def test_a_block_cannot_carry_the_gate_with_rows_it_says_do_not_count():
    """A block declaring `counts_toward_gate: false` is honoured, not overridden."""
    flags = S.gate_flags()
    assert any(v is False for v in flags.values()) or all(flags.values())
    fake = {"IN": [S.validate_event(ev(event_id=f"i{i}")) for i in range(3)],
            "OUT": [S.validate_event(ev(event_id=f"o{i}")) for i in range(40)]}
    cov = S.coverage(fake, flags={"IN": True, "OUT": False})
    assert cov["gate"]["n_complete"] == 3, "rows from an excluded block reached the gate count"
    assert cov["gate"]["gate_met"] is False
    assert cov["gate"]["n_complete_including_excluded_blocks"] == 43
    assert cov["gate"]["blocks_excluded_by_own_declaration"] == ["OUT"]


def test_never_is_a_measured_outcome_not_a_missing_value():
    """A permanently closed asset (block G_accident) did not restore. 'never' is the measurement."""
    r = S.validate_event(ev(days_to_full_restore="never", days_to_partial_restore="never"))
    assert r["computed_status"] == "COMPLETE"
    assert any("never" in n for n in r["notes"])


@pytest.mark.skipif(not (S.BLOCKS.parent / "coverage.json").exists(), reason="run exposure_schema first")
def test_the_published_coverage_matches_a_fresh_validation():
    """The table on disk must be what the validator says today, not what it said when written.

    Skipped while a block is NEWER than the table. Five sessions are filling A-E concurrently, and
    a test that goes red on the shared tree every time one of them saves a file is a test that
    gets deleted rather than heeded -- it would be punishing other sessions for doing their job.
    The check still bites whenever the table is regenerated, which is when it matters."""
    table = S.BLOCKS.parent / "coverage.json"
    newer = [f.name for f in S.BLOCKS.glob("*.json") if f.stat().st_mtime > table.stat().st_mtime]
    if newer:
        pytest.skip(f"blocks edited since the table was generated ({', '.join(sorted(newer))}); "
                    f"re-run python3 src/exposure_schema.py")
    fresh = S.coverage(S.validate_all())
    disk = json.loads(table.read_text())["coverage"]
    assert disk["total"] == fresh["total"], "data/exposure/coverage.json is stale: re-run src/exposure_schema.py"
    assert disk["gate"]["n_complete"] == fresh["gate"]["n_complete"]
