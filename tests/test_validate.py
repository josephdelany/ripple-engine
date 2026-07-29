"""
test_validate.py -- the validation framework proves itself.

Small, hand-verifiable tests over src/validate.py. Each expected value is worked out BY
HAND in the comment, so the test documents the maths, not just asserts it. numpy-only path
is exercised too (the erf/normal fallbacks used when scipy is absent in CI).
Run:  python3 -m pytest -q tests/test_validate.py
"""

import numpy as np

import validate as V


# v1 -- Benjamini-Hochberg. p = [0.001, 0.5, 0.5, 0.5, 0.5], q = 0.05, m = 5.
# BH line q*k/m = 0.01, 0.02, 0.03, 0.04, 0.05. Sorted p_(1)=0.001 <= 0.01 (pass);
# p_(2)=0.5 > 0.02 (fail) -> largest passing rank is 1, so ONLY the smallest survives.
# q-value of the smallest = p*m/rank = 0.001*5/1 = 0.005.
def test_v1_bh_fdr_one_survivor():
    r = V.bh_fdr([0.001, 0.5, 0.5, 0.5, 0.5], q=0.05)
    assert r["n_survive"] == 1
    assert r["survive"][0] is True and not any(r["survive"][1:])
    assert abs(r["qvalues"][0] - 0.005) < 1e-6


# v2 -- Bonferroni. p = [0.01, 0.2], m = 2 -> adjusted [0.02, 0.4]. At alpha 0.05 only the
# first survives (0.02 < 0.05; 0.4 > 0.05).
def test_v2_bonferroni():
    r = V.bonferroni([0.01, 0.2], alpha=0.05)
    assert r["adjusted"] == [0.02, 0.4]
    assert r["survive"] == [True, False]
    assert r["n_survive"] == 1


# v3 -- Wilson CI at k=50, n=100. p = 0.5, z = 1.96. By hand:
# half = 1.96*sqrt(0.25/100 + 1.96^2/(4*100^2)) / (1 + 1.96^2/100)
#      = 1.96*sqrt(0.0025 + 0.000096) / 1.0384 = 1.96*0.050956/1.0384 = 0.0962.
# So the interval is ~[0.404, 0.596], centred on 0.5.
def test_v3_wilson_ci():
    r = V.wilson_ci(50, 100)
    assert r["p"] == 0.5
    assert abs(r["lo"] - 0.404) < 0.005
    assert abs(r["hi"] - 0.596) < 0.005


# v4 -- bootstrap CI of a constant sample is degenerate: every resample of [5,5,5,5] has
# mean 5, so lo = hi = stat = 5 exactly.
def test_v4_bootstrap_ci_constant():
    r = V.bootstrap_ci([5.0, 5.0, 5.0, 5.0], n_boot=200)
    assert r["stat"] == 5.0 and r["lo"] == 5.0 and r["hi"] == 5.0


# v5 -- CPCV splits over n=12 with 6 folds, 2 test folds: C(6,2) = 15 paths. With embargo 0,
# train and test are disjoint and together cover all 12 rows; test size is 4 (two folds of 2).
def test_v5_cpcv_splits_disjoint_and_complete():
    splits = list(V.cpcv_splits(12, k_folds=6, k_test=2, embargo=0))
    assert len(splits) == 15
    for train, test in splits:
        assert len(test) == 4
        assert set(train).isdisjoint(set(test))
        assert set(train) | set(test) == set(range(12))    # embargo 0 -> complete cover


# v5b -- with an embargo the band around the test block is PURGED from train, so train no
# longer covers everything (some rows are dropped to prevent leakage).
def test_v5b_cpcv_embargo_purges():
    train, test = next(V.cpcv_splits(12, k_folds=6, k_test=2, embargo=2))
    assert set(train).isdisjoint(set(test))
    assert len(set(train) | set(test)) < 12                # purged rows are excluded


# v6 -- PBO on a matrix with a genuinely best config in every row. Column 0 = 1.0 everywhere,
# the other two columns = 0.0. The in-sample best is always column 0, and out-of-sample it
# still beats the others, so it NEVER lands below the OOS median: PBO = 0.
def test_v6_pbo_real_signal_is_zero():
    perf = np.zeros((16, 3))
    perf[:, 0] = 1.0
    r = V.pbo_cscv(perf, S=8)
    assert r["ok"] and r["pbo"] == 0.0


# v7 -- Diebold-Mariano when forecaster A has a consistently lower loss (with variation).
# d = loss_a - loss_b is negative on average, so the test says A is better and the stat is
# negative.
def test_v7_diebold_mariano_A_better():
    loss_a = [0.1, 0.3, 0.1, 0.3, 0.1, 0.3]
    loss_b = [0.4, 0.5, 0.35, 0.55, 0.4, 0.5]
    r = V.diebold_mariano(loss_a, loss_b, h=1)
    assert r["ok"] and r["better"] == "A" and r["dm_stat"] < 0


# v7b -- identical loss series -> zero difference variance -> DM is degenerate, reported
# honestly (not a spurious "significant" result).
def test_v7b_diebold_mariano_degenerate():
    r = V.diebold_mariano([0.2, 0.2, 0.2, 0.2], [0.2, 0.2, 0.2, 0.2])
    assert r["ok"] is False


# v8 -- directional permutation p. mags = [1,1,1,10,10,10] with states = [0,0,0,1,1,1] put
# every big move in the high-state bucket (amp = 10-1 = 9, the maximum). Only 1 of the
# C(6,3)=20 label arrangements reproduces that, so p ~ 1/20 = 0.05.
def test_v8_permutation_p_strong_signal():
    r = V.permutation_p([1, 1, 1, 10, 10, 10], [0, 0, 0, 1, 1, 1], sign=+1, n_perm=5000)
    assert abs(r["obs"] - 9.0) < 1e-9
    assert r["p"] < 0.10


# v9 -- cluster bootstrap of the same strong signal recovers obs = 9.0 and almost always
# points the predicted way (share_positive near 1).
def test_v9_cluster_bootstrap_amp():
    r = V.cluster_bootstrap_amp([1, 1, 1, 10, 10, 10], [0, 0, 0, 1, 1, 1], sign=+1, n_boot=2000)
    assert abs(r["obs"] - 9.0) < 1e-9 and r["n"] == 6
    assert r["share_positive"] >= 0.9


# v10 -- the numpy normal-CDF fallback is accurate regardless of scipy: N(0)=0.5 and
# N(1.96)=0.975 to ~3 decimals. (Guards the CI/DM code paths when scipy is absent.)
def test_v10_normal_cdf_fallback():
    assert abs(V._ncdf(0.0) - 0.5) < 1e-6
    assert abs(V._ncdf(1.96) - 0.975) < 2e-3
