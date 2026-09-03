"""
tests/test_grid_power.py -- GRID_STUDY_REGISTRATION.md Part II.

Every test name carries the clause it covers. The estimators are tested against closed-form values on
synthetic series; the published file is tested for internal consistency with the rules it claims to apply.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from engine.grid import power_arithmetic as PA      # noqa: E402

PUBLISHED = PA.OUT
published_only = pytest.mark.skipif(not PUBLISHED.exists(), reason="power_arithmetic.json not yet computed")


# ---------------------------------------------------------------- §2.2 design effects on the time axis

def test_2_2_bartlett_deff_is_about_one_for_an_iid_series():
    rng = np.random.default_rng(0)
    d = [PA.bartlett_deff(rng.normal(size=4000), lag=5) for _ in range(8)]
    assert 0.85 < float(np.mean(d)) < 1.15, d


def test_2_2_bartlett_deff_recovers_the_closed_form_of_an_MA_overlap_process():
    """Overlapping h-period sums sampled every period are an MA(h-1) with rho_k = 1 - k/h. At h = 4 and a
    Bartlett lag of 3 the closed form is 1 + 2*sum_k (1-k/4)*(1-k/4) = 1 + 2(0.5625+0.25+0.0625) = 2.75."""
    rng = np.random.default_rng(1)
    e = rng.normal(size=200_000)
    x = np.convolve(e, np.ones(4), mode="valid")            # 4-period overlapping sums
    got = PA.bartlett_deff(x, lag=3)
    assert got == pytest.approx(2.75, abs=0.08), got


def test_2_2_random_walk_overlap_benchmark_is_the_closed_form():
    """rho_k = max(0, 1 - k*s/h): at spacing 1 and h = 4 with lag 3 this is the same 2.75."""
    assert PA.rw_overlap_deff(1, 4, 3) == pytest.approx(2.75, abs=1e-9)
    assert PA.rw_overlap_deff(21, 20, 1) == pytest.approx(1.0)      # month-end grid, h = 20: no overlap


def test_2_2_bootstrap_deff_agrees_with_bartlett_on_the_same_overlap_process():
    rng = np.random.default_rng(2)
    x = np.convolve(rng.normal(size=6000), np.ones(4), mode="valid")
    b = PA.bartlett_deff(x, lag=3)
    s = PA.bootstrap_deff(x, mean_block=4.0, n_boot=400, seed=7)
    assert 0.5 < s / b < 2.0, (b, s)


def test_2_2_tiebreak_publishes_both_and_uses_the_larger_when_they_disagree():
    """The registered rule: > 1.5x apart -> both published, the LARGER used. Never the smaller."""
    rng = np.random.default_rng(3)
    x = np.convolve(rng.normal(size=3000), np.ones(8), mode="valid")
    blk = PA.deff_block(x, mean_block=1.0, lag=7, label="probe")     # a deliberately mismatched mean_block
    assert blk["deff_bartlett"] > 0 and blk["deff_bootstrap_ratio"] > 0
    if blk["tiebreak_fired"]:
        assert blk["deff_used"] == max(blk["deff_bartlett"], blk["deff_bootstrap_ratio"])
    else:
        assert blk["deff_used"] == blk["deff_bootstrap_ratio"]
    assert blk["deff_used"] >= min(blk["deff_bartlett"], blk["deff_bootstrap_ratio"])


# ---------------------------------------------------------------- §2.3 / §2.4 effective width

def test_2_3_eff_width_is_M_for_orthogonal_columns_and_1_for_perfectly_correlated_ones():
    assert PA.eff_width(np.eye(6)) == pytest.approx(6.0)
    assert PA.eff_width(np.ones((6, 6))) == pytest.approx(1.0)


def test_2_3_eff_width_matches_the_closed_form_for_equicorrelated_columns():
    """M_eff = M / (1 + (M-1) rho) when every off-diagonal correlation is rho."""
    for m, rho in ((6, 0.5), (5, 0.2), (30, 0.9)):
        c = np.full((m, m), rho); np.fill_diagonal(c, 1.0)
        assert PA.eff_width(c) == pytest.approx(m / (1 + (m - 1) * rho), rel=1e-9)


def test_2_4_random_walk_horizon_correlation_is_sqrt_min_over_max():
    c = PA.rw_horizon_corr((5, 10, 20, 40, 60))
    assert c[0, 0] == pytest.approx(1.0)
    assert c[0, 2] == pytest.approx(np.sqrt(5 / 20))
    assert c[1, 4] == pytest.approx(np.sqrt(10 / 60))
    assert np.allclose(c, c.T)
    assert 1.0 < PA.eff_width(c) < 5.0        # five nested horizons are worth strictly fewer than five


# ---------------------------------------------------------------- §2.5 the dyad panel

def test_2_5_a_grid_date_whose_window_passes_the_coverage_end_is_nan_never_zero():
    """The ies90 rule, inherited: no covering source is `no_independent_outcome`, never a 0."""
    import pandas as pd
    spells = pd.DataFrame([("2-20", pd.Timestamp("1990-01-01"), pd.Timestamp("1990-06-01"), 2, "mid")],
                          columns=["dyad", "lo", "hi", "level", "src"])
    # the window is (t, t+90], so a grid date is covered only if t+90 days is still inside the source
    grid = pd.DatetimeIndex(["1990-03-30", "2014-06-30", "2014-10-31", "2020-01-31"])
    lvl, dyads, covered = PA.dyad_panel(spells, grid, "2014-12-31")
    assert covered.tolist() == [True, True, False, False], "t + 90 days must be inside the coverage end"
    assert lvl[0, 0] == 2.0                    # the spell intersects the (t, t+90] window
    assert lvl[1, 0] == 0.0                    # covered, nothing recorded -> 0 is asserted
    assert np.isnan(lvl[2, 0]) and np.isnan(lvl[3, 0])     # past the coverage end -> NaN, not 0


def test_2_5_two_way_cluster_deff_exceeds_iid_when_whole_dates_move_together():
    rng = np.random.default_rng(4)
    T, D = 200, 40
    common = rng.normal(size=(T, 1))                       # a date-level common shock
    X = common + 0.2 * rng.normal(size=(T, D))
    covered = np.ones(T, bool)
    tw = PA.two_way_cluster_deff(X, covered)
    assert tw["deff_two_way"] > 5.0, tw                     # strong date clustering must show up
    Xi = rng.normal(size=(T, D))
    assert PA.two_way_cluster_deff(Xi, covered)["deff_two_way"] < 5.0


# ---------------------------------------------------------------- the published file

@published_only
def test_2_8_the_published_file_reports_the_joint_number_and_labels_the_product_as_a_diagnostic():
    o = json.loads(PUBLISHED.read_text())
    for kind in ("month_end", "week_end"):
        j = o["price_panel"][kind]["joint"]
        assert "n_eff" in j and "naive_product" in j
        assert "DIAGNOSTIC ONLY" in j["rule"]
        assert j["n_eff"] < j["n_nominal"], "a nominal count may never be reported as an effective one"
        assert j["realisation_ratio"] < 1.0


@published_only
def test_2_2_published_deff_used_obeys_the_tiebreak_everywhere():
    o = json.loads(PUBLISHED.read_text())
    blocks = []
    for kind in ("month_end", "week_end"):
        blocks += list(o["price_panel"][kind]["deff_per_cell"].values())
        blocks.append(o["price_panel"][kind]["time"])
        for w in o["escalation_panel"][kind].values():
            blocks.append(w["time"])
    for b in blocks:
        lo, hi = sorted((b["deff_bartlett"], b["deff_bootstrap_ratio"]))
        pre = hi if b["tiebreak_fired"] else b["deff_bootstrap_ratio"]
        # a measured design effect below 1 is a finite-sample artefact and is floored at 1, so that n_eff
        # can never exceed n_nominal; the floor is recorded when it fires
        assert b["deff_used"] == pytest.approx(max(pre, PA.DEFF_FLOOR), abs=1e-3)
        assert b["deff_used"] >= PA.DEFF_FLOOR - 1e-9
        assert b.get("deff_floored_at_1") is (pre < PA.DEFF_FLOOR)


@published_only
def test_2_5_published_escalation_n_eff_applies_the_two_way_tiebreak_and_never_the_smaller_deff():
    o = json.loads(PUBLISHED.read_text())
    for kind in ("month_end", "week_end"):
        for w in o["escalation_panel"][kind].values():
            sep, two = w["deff_separable_TxD"], w["deff_two_way"]
            want = max(sep, two) if w["tiebreak_fired"] else sep
            assert w["deff_used"] == pytest.approx(want, abs=1e-2)   # published rounded to 3 dp
            assert w["n_eff"] == pytest.approx(w["n_nominal_cells"] / w["deff_used"], rel=1e-3)
            if w["tiebreak_fired"]:
                assert w["n_eff"] <= w["n_eff_separable_TxD_before_tiebreak"], "the tiebreak may only lower n_eff"


@published_only
def test_2_5_published_escalation_states_that_its_n_eff_is_a_ceiling():
    """The level panel is overwhelmingly zeros; both a forecaster and its climatology get those right."""
    o = json.loads(PUBLISHED.read_text())
    for kind in ("month_end", "week_end"):
        for w in o["escalation_panel"][kind].values():
            assert w["share_level_0"] > 0.9
            assert "UPPER BOUND" in w["informative_share_warning"]


@published_only
def test_2_7_published_decisions_follow_the_registered_drop_rule_mechanically():
    o = json.loads(PUBLISHED.read_text())
    for kind in ("month_end", "week_end"):
        for name, r in o["multipliers"][kind].items():
            R = r.get("R"); add = r.get("delta_n_eff", r.get("delta_n_eff_vs_event"))
            if R is None or add is None:
                continue
            if add < PA.MIN_TIER_N or R < PA.DROP_RATIO:
                assert r["decision"].startswith("DROP"), (name, R, add, r["decision"])
            elif R < PA.MARGINAL_RATIO:
                assert "MARGINAL" in r["decision"]
            else:
                assert r["decision"].startswith("KEEP") and "MARGINAL" not in r["decision"]


@published_only
def test_2_9_the_power_verdict_uses_the_measured_noise_ratio_not_an_invented_one():
    o = json.loads(PUBLISHED.read_text())
    eb = o["event_triggered_baseline"]
    for task in ("G", "P"):
        assert 0.1 < eb[task]["sd_over_ref"] < 2.0
        assert eb[task]["n_eff"] <= eb[task]["n_nominal"]
    for kind in ("month_end", "week_end"):
        v = o["verdicts"][kind]
        for task in ("G", "P"):
            assert v["power_input"][task]["sd_over_ref"] == pytest.approx(eb[task]["sd_over_ref"])
        assert v["mds_skill_price_at_n_eff"] < 0.127, "the grid must beat the event-triggered MDS or say so"


@published_only
def test_0_2_the_arithmetic_never_writes_to_the_event_triggered_tree():
    """GRID_STUDY_REGISTRATION §0.2: the grid study reads data/walk_forward/** and never writes there."""
    src = (ROOT / "src" / "engine" / "grid" / "power_arithmetic.py").read_text()
    assert "walk_forward" in src, "the baseline is read from the sealed run"
    for bad in ('walk_forward" / "summary.json").write', "wf / \"summary.json\").write", ".jsonl\").open(\"w"):
        assert bad not in src
    assert str(PA.OUT).endswith("data/grid/power_arithmetic.json")


@published_only
def test_2_2_no_published_n_eff_exceeds_its_own_nominal_count():
    """The defect the floor fixes: an unclamped design effect below 1 reported MORE effective observations
    than there were cells. 1,784 from 1,440, in one case. Publishing that as information is indefensible."""
    o = json.loads(PUBLISHED.read_text())
    for kind in ("month_end", "week_end"):
        j = o["price_panel"][kind]["joint"]
        assert j["n_eff"] <= j["n_nominal"]
        assert o["price_panel"][kind]["time"]["T_eff"] <= o["price_panel"][kind]["time"]["n"] + 1e-6
        for w in o["escalation_panel"][kind].values():
            assert w["n_eff"] <= w["n_nominal_cells"] + 1e-6
        for m in o["multipliers"][kind].values():
            if m.get("R") is not None:
                assert m["R"] <= 1.0 + 1e-9, "a realisation ratio above 1 means n_eff beat n_nominal"
