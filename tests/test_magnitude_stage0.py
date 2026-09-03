"""MAGNITUDE_REGISTRATION.md section 3 -- the Stage 0 kill-test that gates the study.

The point of these is that the decision rule was quantified and committed BEFORE the estimator ran
(de70b04, with no stage0.json in the tree), that the four specifications differ only in the
regressor and not in the sample, and that the one positive band on a physical quantity is recorded
with the diagnostic that disqualifies a causal reading of it."""
import json
from pathlib import Path

import numpy as np
import pytest

import ripple_lp as R
import magnitude_stage0 as S0

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "magnitude" / "stage0.json"


@pytest.fixture(scope="module")
def payload():
    if not OUT.exists():
        pytest.skip("run src/magnitude_stage0.py first")
    return json.loads(OUT.read_text())


def test_s3_the_shared_subsample_is_what_stage0_contributes(payload):
    """v2 section 4.1 compared Kaenzig to the OPEC dummy on DIFFERENT samples. Stage 0's whole job
    is that A, B, C and D see the same days."""
    it = payload["intersection"]
    assert it["n_days"] == len(it["dates"]) == len(it["surprise"])
    assert it["n_days"] >= R.MIN_N
    for outcome in ("price", "quantity"):
        ns = {payload[outcome]["specs"][s]["n_nonzero"]
              for s in ("A_dummy", "B_magnitude", "D_severity_ordinal")}
        assert len(ns) == 1, f"{outcome}: specs do not share a sample: {ns}"


def test_s3_the_decision_rule_bar_was_fixed_before_the_estimates_existed():
    """The registration wrote '>>' without quantifying it; the quantification lives in the module
    docstring and in beats(), committed at de70b04 with no result file in the tree."""
    src = (ROOT / "src" / "magnitude_stage0.py").read_text()
    assert "B BEATS A  iff" in src
    assert "def beats(" in src
    # the rule must not consult anything but the two headline dicts
    fn = src[src.index("def beats("):src.index("def main(")]
    for leak in ["json.load", "stage0.json", "open("]:
        assert leak not in fn


def test_s3_beats_implements_exactly_the_stated_bar():
    hi = {"beta": 2.0, "se_ehw": 0.6, "z_ehw": 3.3, "ehw_covers_zero": False}
    lo = {"beta": 1.0, "se_ehw": 1.0, "z_ehw": 1.0, "ehw_covers_zero": True}
    weak = {"beta": 2.0, "se_ehw": 0.9, "z_ehw": 2.2, "ehw_covers_zero": False}
    assert S0.beats(hi, lo)[0] is True                 # B excludes zero, A does not
    assert S0.beats(weak, weak)[0] is False            # both exclude zero, |z_B| < 2|z_A|
    assert S0.beats(lo, hi)[0] is False


def test_s3_price_arm_magnitude_beats_the_dummy_and_the_dummy_dies_in_spec_c(payload):
    d = payload["decision"]["price"]
    assert d["B_beats_A"] is True
    assert d["C_dummy_indistinguishable_from_zero"] is True
    c = payload["price"]["specs"]["C_both"]
    assert c["dummy"]["ehw_covers_zero"] is True
    assert c["magnitude"]["ehw_covers_zero"] is False


def test_s5_the_free_ordinal_baseline_does_not_beat_the_measured_surprise(payload):
    """Section 5: 'a magnitude series that cannot beat an ordinal severity code is not worth
    building'. The converse also matters -- severity must not quietly be good enough."""
    assert payload["decision"]["price"]["B_beats_D_severity_baseline"] is True
    d = payload["price"]["specs"]["D_severity_ordinal"]["headline"]
    assert d["ehw_covers_zero"] is True


def test_s3_quantity_arm_magnitude_does_not_beat_the_dummy(payload):
    assert payload["decision"]["quantity"]["B_beats_A"] is False
    b = payload["quantity"]["specs"]["B_magnitude"]["headline"]
    assert b["ehw_covers_zero"] is True


def test_s3_the_registered_outcome_is_one_of_the_three_written_in_advance(payload):
    allowed = {"MAGNITUDE IS THE BINDING CONSTRAINT",
               "MAGNITUDE IS NOT THE BINDING CONSTRAINT",
               "MAGNITUDE IS BELIEF, NOT BARRELS"}
    assert payload["decision"]["stage0"]["outcome"] in allowed


def test_s3_stage0_returns_belief_not_barrels(payload):
    """The result, asserted so that a later change to it is a visible failure."""
    assert payload["decision"]["stage0"]["outcome"] == "MAGNITUDE IS BELIEF, NOT BARRELS"


def test_s3_the_one_positive_quantity_band_is_recorded_with_its_anticipation_diagnostic(payload):
    """The dummy's h=0 hit clears the state-matched placebo, so the thing that disqualifies a causal
    reading is the pre-trend, and it must travel with the number."""
    s = payload["quantity_dummy_scrutiny"]
    assert s["mean_dlog_into_prior_month_pct"] < 0 < s["mean_dlog_into_event_month_pct"]
    assert abs(s["mean_dlog_into_event_month_pct"]) > abs(s["mean_dlog_all_months_pct"])
    assert s["placebo_at_headline"] is not None
    assert "not identified" in s["reading"]


def test_s3_the_quantity_dummy_effect_exists_only_at_the_contemporaneous_horizon(payload):
    irf = {x["h"]: x for x in payload["quantity"]["specs"]["A_dummy"]["irf"] if x.get("beta") is not None}
    assert irf[0]["ehw_covers_zero"] is False
    for h in (1, 2, 3, 6, 9, 12):
        assert irf[h]["ehw_covers_zero"] is True, h


def test_s3_expectations_are_scored_in_the_registered_vocabulary(payload):
    e = payload["expectations"]
    assert e["E-2"]["score"] == "CONSISTENT"
    assert e["E-1"]["price_mechanism"] == "CONSISTENT"
    assert "PARTLY CONSISTENT" in e["E-1"]["score"]


def test_s7_min_n_for_a_continuous_regressor_is_the_nonzero_count(payload):
    """Section 7: with a continuous magnitude the effective sample is not a count, so the rule is
    the number of events with a non-zero, non-missing magnitude, reported on every row."""
    for outcome in ("price", "quantity"):
        for s in ("A_dummy", "B_magnitude", "D_severity_ordinal"):
            sp = payload[outcome]["specs"][s]
            assert sp["n_nonzero"] >= R.MIN_N
            assert sp["meets_min_n"] is True
            assert "max_single_event_variance_share" in sp["variance_concentration"]


def test_s3_estimator_is_imported_not_reimplemented():
    src = (ROOT / "src" / "magnitude_stage0.py").read_text()
    assert "import ripple_lp as R" in src and "import ripple_physical as PH" in src
    for fn in ["def run_lp(", "def placebo(", "def cluster_first_dates(", "def build_daily("]:
        assert fn not in src, f"{fn} is re-implemented; it must come from ripple_lp"
    assert "R.ols(" in src          # lp_two is a design, not a new estimator


def test_s14_stage0_does_not_start_stage1():
    """Section 14: nothing here builds a magnitude series for any other class."""
    src = (ROOT / "src" / "magnitude_stage0.py").read_text()
    for cls in ["sanctions", "chokepoint_disruption", "infrastructure_attack", "conflict_escalation"]:
        assert f'"{cls}"' not in src, cls
