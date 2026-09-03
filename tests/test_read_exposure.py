"""EXPOSURE_REGISTRATION §4 as tests: read(exposure) -> distribution.

Written against hand-built cases, not the live blocks — six sessions are filling those and a test
asserting today's n would be flaky tomorrow and "fixed" by editing the number. The live corpus is
checked for invariants only.

The load-bearing test in this file is `test_a_missing_field_never_matches_as_a_zero`. Everything
else is schema; that one is the defect this session keeps meeting.
"""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import read_exposure as R  # noqa: E402


def case(**kw):
    base = {"event_id": "c1", "date": "2015-01-05", "asset_type": "refinery",
            "capacity_nameplate_kbd": 400, "capacity_affected_kbd": 200,
            "days_to_partial_restore": 5, "days_to_full_restore": 30,
            "_block": "T", "_status": "PARTIAL", "_hard_failures": []}
    base.update(kw)
    return base


def many(n, **kw):
    return [case(event_id=f"c{i}", **kw) for i in range(n)]


# ------------------------------------------------------------------ THE ONE THAT MATTERS

def test_a_missing_field_never_matches_as_a_zero():
    """`ies90` used max(default=0) and published 18 events as 'no escalation' when the truth was
    'no answer'. Here the same defect would be a query with 5,700 kb/d affected scoring a perfect
    magnitude match against a case whose capacity is simply unrecorded."""
    q = {"asset_type": "refinery", "capacity_affected_kbd": 5700, "capacity_nameplate_kbd": 7000}
    absent = case(capacity_affected_kbd="unknown")
    score, used, skipped = R.compare(q, absent)
    assert "capacity_affected_kbd" not in used, "a missing capacity was compared"
    assert "capacity_affected_kbd" in skipped and "case" in skipped["capacity_affected_kbd"]
    # and it must not be treated as 0 either, which would be a MAXIMALLY DISTANT match rather than
    # a skipped one -- both are wrong, and the difference is visible only in `fields_not_compared`
    zeroed = case(capacity_affected_kbd=0)
    s_absent, _, _ = R.compare(q, absent)
    s_zero, used_zero, _ = R.compare(q, zeroed)
    assert "capacity_affected_kbd" in used_zero, "a measured 0 must be compared, not skipped"
    assert s_absent != s_zero, "an absent capacity scored the same as a measured zero"


def test_a_measured_zero_is_compared_and_scores_as_the_value_it_is():
    """A foiled attack took 0 kb/d offline. That is a finding, not a gap."""
    assert R._mag_close(0, 0) == 1.0            # two zeros are the same event shape
    assert R._mag_close(0, 500) == 0.0          # zero against a real loss is maximally different
    assert R._num(0) == 0.0 and R._num("unknown") is None


def test_a_case_with_nothing_comparable_is_not_a_match():
    q = {"asset_type": "refinery", "capacity_affected_kbd": 100}
    blind = case(capacity_affected_kbd="unknown", capacity_nameplate_kbd="unknown")
    score, used, skipped = R.compare(q, blind)
    assert score is None and not used


def test_affected_share_needs_both_halves_on_both_sides():
    assert R.affected_share({"capacity_affected_kbd": 100, "capacity_nameplate_kbd": 400}) == 0.25
    for bad in ({"capacity_affected_kbd": 100}, {"capacity_nameplate_kbd": 400},
                {"capacity_affected_kbd": 100, "capacity_nameplate_kbd": 0},
                {"capacity_affected_kbd": 100, "capacity_nameplate_kbd": "unknown"}):
        assert R.affected_share(bad) is None


# ------------------------------------------------------------------ §4 no adequate precedent

def test_S4_fewer_than_five_comparable_cases_is_a_first_class_state():
    q = {"asset_type": "refinery", "capacity_affected_kbd": 200}
    r = R.read(q, cases=many(4), prices={})
    assert r["state"] == "no_adequate_precedent"
    assert r["n"] == 4 and "5" in r["reason"]
    assert r["cases_found"] and "what_would_change_it" in r
    assert "duration" not in r and "price" not in r, "a below-threshold read must not emit distributions"


def test_S4_five_comparable_cases_is_enough():
    r = R.read({"asset_type": "refinery", "capacity_affected_kbd": 200}, cases=many(5), prices={})
    assert r["state"] == "ok" and r["n"] == 5 and r["reference_class"]


def test_S4_the_threshold_is_not_met_by_widening_the_search():
    """A chokepoint query must not be answered with refinery cases just to reach five."""
    r = R.read({"asset_type": "chokepoint", "capacity_affected_kbd": 200}, cases=many(20), prices={})
    assert r["state"] == "no_adequate_precedent" and r["n"] == 0
    assert any("asset_type" in k for k in r["retrieval"]["excluded"])


# ------------------------------------------------------------------ §4 never a probability

def test_S4_the_output_never_expresses_a_probability():
    r = R.read({"asset_type": "refinery", "capacity_affected_kbd": 200}, cases=many(6), prices={})
    assert "not_a_probability" in r, "the read must carry the §4 disclaimer"
    # scan everything EXCEPT the disclaimer itself -- it necessarily contains the word it forbids
    stripped = {k: v for k, v in r.items() if k != "not_a_probability"}
    blob = json.dumps(stripped).lower()
    for banned in ("probability", "probabilit", "likelihood", "odds of", "chance of", "p(", "pct_chance"):
        assert banned not in blob, f"the read expressed {banned!r} outside the disclaimer"
    # and every share is explicitly a share OF A STATED n, not a rate in the abstract
    for d in r["duration"].values():
        for cat in d["categories"].values():
            assert set(cat) == {"n", "share_of_n"}, "a category reported something other than n and share_of_n"


def test_S4_every_distribution_carries_its_own_n():
    cases = many(6)
    cases[0]["days_to_full_restore"] = "unknown"
    r = R.read({"asset_type": "refinery", "capacity_affected_kbd": 200}, cases=cases, prices={})
    for f, d in r["duration"].items():
        assert d["n_matches"] == r["n"]
        assert d["n_numeric"] <= d["n_matches"], f
        assert sum(v["n"] for v in d["categories"].values()) + d["n_numeric"] == d["n_matches"], f


# ------------------------------------------------------------------ durations are outcomes, not numbers

def test_ongoing_and_never_are_counted_as_outcomes_not_folded_into_the_days():
    cases = many(6)
    cases[0]["days_to_full_restore"] = "ongoing"
    cases[1]["days_to_full_restore"] = "never"
    r = R.read({"asset_type": "refinery", "capacity_affected_kbd": 200}, cases=cases, prices={})
    d = r["duration"]["days_to_full_restore"]
    assert d["categories"]["ongoing"]["n"] == 1 and d["categories"]["never"]["n"] == 1
    assert d["n_numeric"] == 4, "a permanent closure was folded into the numeric durations"


# ------------------------------------------------------------------ the match must explain itself

def test_the_read_states_which_fields_drove_the_match():
    cases = many(6, capacity_nameplate_kbd="unknown")
    r = R.read({"asset_type": "refinery", "capacity_affected_kbd": 200,
                "capacity_nameplate_kbd": 400}, cases=cases, prices={})
    drv = r["fields_that_drove_the_match"]
    assert "capacity_affected_kbd" in drv
    assert "capacity_nameplate_kbd" not in drv, "a field missing on every case was reported as driving"
    assert all(m["fields_not_compared"] for m in r["matches"])


def test_geography_alone_is_not_exposure_similarity():
    cases = many(8, capacity_affected_kbd="unknown", capacity_nameplate_kbd="unknown",
                 country_iso3="SAU")
    r = R.read({"asset_type": "refinery", "country_iso3": "SAU"}, cases=cases, prices={})
    assert r["state"] == "no_adequate_precedent"
    assert any("geography is not exposure" in k for k in r["retrieval"]["excluded"])


def test_an_INVALID_case_is_never_used_as_evidence():
    """§2 hard failure = a numeric with no provenance. Matching on it imports an unsourced magnitude."""
    cases = many(6)
    for c in cases[:3]:
        c["_status"] = "INVALID"
    r = R.read({"asset_type": "refinery", "capacity_affected_kbd": 200}, cases=cases, prices={})
    assert r["n"] == 3 and r["state"] == "no_adequate_precedent"
    assert any("INVALID" in k for k in r["retrieval"]["excluded"])


def test_a_case_with_no_asset_type_is_not_asserted_to_match():
    cases = many(8, asset_type="unknown")
    r = R.read({"asset_type": "refinery", "capacity_affected_kbd": 200}, cases=cases, prices={})
    assert r["state"] == "no_adequate_precedent"
    assert any("no asset_type" in k for k in r["retrieval"]["excluded"])


# ------------------------------------------------------------------ price side

def test_an_unparseable_event_date_yields_no_price_not_a_default_one():
    import pandas as pd
    s = pd.Series([100.0, 101.0, 102.0], index=pd.to_datetime(["2020-01-02", "2020-01-03", "2020-01-06"]))
    assert R.forward_change(s, "unknown", 1) is None
    assert R.forward_change(s, None, 1) is None
    assert R.forward_change(s, "2020-01-02", 1) == pytest.approx(1.0)
    assert R.forward_change(s, "2020-01-02", 99) is None, "a window off the end must be None, not 0"


def test_the_reference_class_is_named_from_the_matches_not_the_query():
    cases = many(6, capacity_affected_kbd=50)
    r = R.read({"asset_type": "refinery", "capacity_affected_kbd": 9999}, cases=cases, prices={})
    assert "50" in r["reference_class"] and "9999" not in r["reference_class"]


# ------------------------------------------------------------------ the live corpus: invariants only

def test_live_the_two_worked_reads_are_committed_and_self_consistent():
    for stem in ("abqaiq_2019_heldout", "ras_tanura_scenario"):
        p = R.OUT_DIR / f"{stem}.json"
        if not p.exists():
            pytest.skip("run python3 src/read_exposure.py first")
        r = json.loads(p.read_text())
        assert r["state"] in ("ok", "no_adequate_precedent")
        if r["state"] == "ok":
            assert r["n"] >= R.MIN_CASES and len(r["matches"]) == r["n"]
        else:
            assert r["n"] < R.MIN_CASES
        assert (R.OUT_DIR / f"{stem}.md").exists()


def test_live_the_held_out_read_excluded_its_own_case():
    p = R.OUT_DIR / "abqaiq_2019_heldout.json"
    if not p.exists():
        pytest.skip("run python3 src/read_exposure.py first")
    r = json.loads(p.read_text())
    ids = [m["event_id"] for m in r.get("matches", [])] + [c["event_id"] for c in r.get("cases_found", [])]
    assert "abqaiq_attack_2019" not in ids, "the held-out case answered its own question"
    assert r["held_out"]["event_id"] == "abqaiq_attack_2019"
