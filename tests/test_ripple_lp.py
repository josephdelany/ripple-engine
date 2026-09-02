"""The ripple ESTIMATOR (src/ripple_lp.py), which produces every number in data/ripple/.

Section ids in the test names are RIPPLE_REGISTRATION.md sections. These are the checks that
would catch a silent corruption of all 932 rows: an off-by-one in the window alignment, a wrong
standard error, a placebo shortcut that does not equal the regression it stands in for, a
Benjamini-Hochberg that stops at the first non-rejection, a cluster window that is not the
registered one, or a verdict that does not require what Amendment B says it requires.

The standard errors are checked against statsmodels, not against numbers I typed in.
"""
import numpy as np
import pytest

import ripple_lp as RL

sm = pytest.importorskip("statsmodels.api", reason="statsmodels needed to check HC1/HAC")


def test_r_2_1_shift_alignment_is_exact_in_both_directions():
    a = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    fwd = RL.shift(a, 1)                       # shift(a,1)[t] = a[t-1]
    assert np.isnan(fwd[0]) and fwd[1] == 0.0 and fwd[4] == 3.0
    back = RL.shift(a, -2)                     # shift(a,-h)[t] = a[t+h]
    assert back[0] == 2.0 and back[2] == 4.0 and np.isnan(back[3]) and np.isnan(back[4])
    assert np.array_equal(RL.shift(a, 0), a)


def test_r_2_1_lp_design_builds_exactly_the_registered_regression():
    """dep = y[t+h] - y[t-1]; column 1 is the shock; then p+1 own lags of dy (lag augmentation)."""
    y = np.arange(20, dtype=float) ** 1.5
    S = np.zeros(20); S[[5, 11]] = 1.0
    p, h = 2, 3
    X, dep, mask = RL.lp_design(y, S, h, p, ctrls=[])
    for t in range(1, 20 - h):
        assert dep[t] == pytest.approx(y[t + h] - y[t - 1]), t
    assert np.array_equal(X[:, 1], S)                       # the shock is column 1, untouched
    assert X.shape[1] == 2 + (p + 1)                        # const + shock + p+1 lags, no controls
    dy = y - RL.shift(y, 1)
    for l in range(1, p + 2):
        col, want = X[:, l + 1], RL.shift(dy, l)          # column l+1 is the l-th own lag of dy
        fin = np.isfinite(want)
        assert np.allclose(col[fin], want[fin]), l
    assert not mask[:p + 2].any()                           # rows without a full lag block are dropped


def test_r_2_4_hc1_and_newey_west_match_statsmodels_at_every_bandwidth():
    """The primary (EHW/HC1) and diagnostic (Newey-West, bandwidth = h) covariances are the
    registered inference. Checked against statsmodels rather than a remembered formula."""
    rng = np.random.default_rng(0)
    n = 400
    X = np.column_stack([np.ones(n), rng.normal(size=n), rng.normal(size=n)])
    y = X @ np.array([1.0, 2.0, -0.5]) + rng.normal(size=n) * (1 + 0.5 * np.abs(X[:, 1]))
    for L in (0, 5, 20):
        mine = RL.ols(X, y, L=L)
        hc1 = sm.OLS(y, X).fit(cov_type="HC1")
        hac = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": L, "use_correction": False})
        assert np.allclose(mine["b"], hc1.params)
        assert np.allclose(mine["se_hc"], hc1.bse, atol=1e-12), L
        assert np.allclose(mine["se_nw"], hac.bse, atol=1e-12), L


def test_r_2_2_planted_response_peaks_at_the_horizon_it_was_planted_at():
    """A response planted entirely 5 days after the shock must show up at h=5 and not before.
    The recovered size is BELOW the planted 2.0 because neighbouring windows overlap the jump
    (rows t..t+5 all contain it), which is a property of local projections, not an error --
    so the shape is asserted, not a magnitude that would be wrong."""
    rng = np.random.default_rng(7)
    T = 3000
    dy = rng.normal(size=T) * 0.05
    ev = np.arange(200, T - 100, 37)
    S = np.zeros(T); S[ev] = 1.0
    dy[ev + 5] += 2.0
    y = np.cumsum(dy)
    irf = {r["h"]: r for r in RL.run_lp(y, S, [0, 2, 5, 10], RL.P_DAILY, [])}
    assert irf[5]["beta"] > 10 * irf[5]["se_ehw"]                 # unmistakably present at h=5
    assert abs(irf[0]["beta"]) < 0.2 and abs(irf[2]["beta"]) < 0.5  # not before it
    assert irf[5]["beta"] > irf[2]["beta"] and irf[5]["beta"] > irf[10]["beta"]
    assert irf[5]["ehw_covers_zero"] is False and irf[5]["n_events"] == len(ev)


def test_r_2_5_placebo_shortcut_equals_the_full_regression_coefficient():
    """The placebo draws thousands of coefficients via Frisch-Waugh-Lovell instead of refitting.
    If that shortcut does not equal the real regression's coefficient, every placebo percentile
    in the study is wrong."""
    rng = np.random.default_rng(3)
    n = 500
    Z = np.column_stack([np.ones(n), rng.normal(size=n), rng.normal(size=n)])
    rows = np.sort(rng.choice(n, size=40, replace=False))
    S = np.zeros(n); S[rows] = 1.0
    yy = Z @ np.array([0.3, 1.0, -2.0]) + 1.5 * S + rng.normal(size=n)
    full = np.linalg.lstsq(np.column_stack([Z, S]), yy, rcond=None)[0][-1]
    ZtZinv = np.linalg.pinv(Z.T @ Z)
    ytil = yy - Z @ (ZtZinv @ (Z.T @ yy))
    assert RL.fwl_beta(Z, ZtZinv, ytil, rows) == pytest.approx(float(full), rel=1e-9)


def test_r_2_9_benjamini_hochberg_takes_the_largest_k_not_the_first_failure():
    """BH rejects everything up to the LARGEST k with p_(k) <= k/m*q. A version that stopped at
    the first failure would reject 1 of these 5 instead of all 5."""
    p = [0.001, 0.09, 0.09, 0.09, 0.09]          # thresholds .02 .04 .06 .08 .10 -> k=5 passes
    assert RL.bh_flags(p, q=0.10) == [True] * 5
    assert RL.bh_flags([0.5, 0.6, 0.7], q=0.10) == [False] * 3
    flags = RL.bh_flags([0.001, None, 0.9], q=0.10)   # None is not a test and is never rejected
    assert flags[0] is True and flags[1] is False and flags[2] is False


def test_amendment_a_cluster_window_is_35_calendar_days_chained():
    import pandas as pd
    assert RL.CLUSTER_DAYS == 35
    import robustness
    assert RL.CLUSTER_DAYS == robustness.CLUSTER_DAYS      # the registration defers to the code
    d = ["2020-01-01", "2020-02-01", "2020-03-10", "2020-03-11"]
    keep = RL.cluster_first_dates([pd.Timestamp(x) for x in d])
    assert [str(k.date()) for k in keep] == ["2020-01-01", "2020-03-10"]


def test_amendment_b_verdict_requires_band_placebo_and_newey_west_together():
    head = {"beta": 3.0, "ehw_covers_zero": False, "nw_covers_zero": False}
    beyond = {"beyond_state": True}
    assert RL.verdict(head, beyond, 20) == ("TRANSMITTING", False)
    assert RL.verdict(head, {"beyond_state": False}, 20) == ("NULL", False)   # placebo required
    fragile = {"beta": 3.0, "ehw_covers_zero": False, "nw_covers_zero": True}
    assert RL.verdict(fragile, beyond, 20) == ("NULL", True)                  # NW disagrees -> fragile
    assert RL.verdict(head, beyond, 14)[0] == "INSUFFICIENT"                  # below MIN_N = 15
    assert RL.MIN_N == 15
