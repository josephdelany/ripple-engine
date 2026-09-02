"""
inference.py -- PATH Step 8 / protocol §6: is the skill real?

Pure numpy (the repo deliberately carries no scipy). Each piece is checked against a textbook
value in tests/test_walk.py.

  t_cdf(x, df)                Student-t CDF via the regularized incomplete beta function
                              (continued fraction, Numerical Recipes 6.4); matches the t-table.
  dm_test(loss_a, loss_b, h)  Diebold-Mariano (1995) with Newey-West HAC variance (Bartlett, h-1 lags)
                              and the Harvey-Leybourne-Newbold (1997) small-sample correction,
                              p from t_{T-1}. Negative statistic = A better.
  stationary_bootstrap(...)   Politis-Romano (1994) stationary block bootstrap indices.
  bootstrap_ci(...)           percentile interval of any statistic under the stationary bootstrap.
  spa(...)                    White (2000) Reality Check and Hansen (2005) SPA p-values for
                              "does the best of M models beat the benchmark?"
  bh_fdr(pvals, q)            Benjamini-Hochberg step-up.
  permutation_p(obs, null)    rank of the observed statistic in its permutation null.
  power_mds(...)              simulation-based minimum detectable mean differential at 80% power.
"""
from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------- Student t via incomplete beta

def _betacf(a, b, x, max_iter=300, eps=3e-14):
    fpmin = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > fpmin else fpmin)
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d; d = 1.0 / (d if abs(d) > fpmin else fpmin)
        c = 1.0 + aa / c; c = c if abs(c) > fpmin else fpmin
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d; d = 1.0 / (d if abs(d) > fpmin else fpmin)
        c = 1.0 + aa / c; c = c if abs(c) > fpmin else fpmin
        de = d * c
        h *= de
        if abs(de - 1.0) < eps:
            break
    return h


def _lgamma(z):
    return float(np.math.lgamma(z)) if hasattr(np, "math") else __import__("math").lgamma(z)


def betainc(a, b, x):
    """Regularized incomplete beta I_x(a, b)."""
    import math
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1.0 - x)
    bt = math.exp(lbeta)
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def t_cdf(x, df):
    x = float(x); df = float(df)
    if df <= 0:
        raise ValueError("df must be positive")
    ib = betainc(df / 2.0, 0.5, df / (df + x * x))
    return 1.0 - 0.5 * ib if x >= 0 else 0.5 * ib


def norm_cdf(x):
    import math
    return 0.5 * (1.0 + math.erf(float(x) / math.sqrt(2.0)))


# ---------------------------------------------------------------- Diebold-Mariano with HLN + HAC

def newey_west_var(d, lag):
    """HAC long-run variance estimate of the mean of d with a Bartlett kernel and `lag` lags."""
    d = np.asarray(d, float)
    T = len(d)
    dc = d - d.mean()
    v = float(np.mean(dc * dc))
    for j in range(1, int(lag) + 1):
        if j >= T:
            break
        g = float(np.mean(dc[j:] * dc[:-j]))
        v += 2.0 * (1.0 - j / (lag + 1.0)) * g
    return max(v, 0.0)


def dm_test(loss_a, loss_b, h=1, lag=None):
    """Equal predictive accuracy of A vs B on per-read losses. d = loss_a - loss_b (negative: A better).
    HAC with `lag` lags (default h-1), HLN correction, two-sided p from t_{T-1}."""
    a = np.asarray(loss_a, float); b = np.asarray(loss_b, float)
    keep = np.isfinite(a) & np.isfinite(b)
    d = (a - b)[keep]
    T = len(d)
    if T < 3:
        return {"ok": False, "reason": "need >= 3 paired losses", "n": T}
    lag = int(h - 1 if lag is None else lag)
    dbar = float(d.mean())
    lrv = newey_west_var(d, lag)
    if lrv <= 0:
        return {"ok": False, "reason": "degenerate (zero variance) loss difference", "n": T, "mean_diff": dbar}
    dm = dbar / np.sqrt(lrv / T)
    hln = np.sqrt((T + 1 - 2 * h + h * (h - 1) / T) / T)
    dm_star = float(dm * hln)
    p = 2.0 * (1.0 - t_cdf(abs(dm_star), T - 1))
    return {"ok": True, "n": T, "h": h, "lag": lag, "mean_diff": dbar, "dm": float(dm), "dm_hln": dm_star,
            "p_value": float(p), "better": "A" if dbar < 0 else ("B" if dbar > 0 else "tie")}


# ---------------------------------------------------------------- stationary block bootstrap

def stationary_bootstrap(n, mean_block, rng, size=None):
    """Politis-Romano indices: geometric block lengths with mean `mean_block`, wrapping circularly."""
    size = size or n
    p = 1.0 / max(float(mean_block), 1.0)
    idx = np.empty(size, dtype=int)
    i = 0
    while i < size:
        start = int(rng.integers(0, n))
        L = int(rng.geometric(p))
        for j in range(L):
            if i >= size:
                break
            idx[i] = (start + j) % n
            i += 1
    return idx


def bootstrap_ci(stat_fn, n, n_boot=2000, mean_block=3.0, seed=19900802, ci=0.95):
    """Percentile CI of stat_fn(indices) under the stationary bootstrap over positions 0..n-1."""
    rng = np.random.default_rng(seed)
    obs = stat_fn(np.arange(n))
    boots = []
    for _ in range(n_boot):
        idx = stationary_bootstrap(n, mean_block, rng)
        v = stat_fn(idx)
        if v is not None and np.isfinite(v):
            boots.append(v)
    if not boots:
        return {"estimate": obs, "lo": None, "hi": None, "n_boot": 0}
    lo, hi = np.percentile(boots, [100 * (1 - ci) / 2, 100 * (1 - (1 - ci) / 2)])
    return {"estimate": float(obs) if obs is not None else None, "lo": float(lo), "hi": float(hi),
            "n_boot": len(boots), "mean_block": mean_block}


# ---------------------------------------------------------------- Reality Check / SPA

def spa(d, n_boot=1000, mean_block=3.0, seed=19900802):
    """d: T x M matrix of (benchmark loss - model loss); positive = model beats benchmark.
    Null: no model beats the benchmark (max_k E d_k <= 0).
    Returns White's RC p-value and Hansen's consistent SPA p-value, plus the best model index."""
    d = np.asarray(d, float)
    if d.ndim == 1:
        d = d[:, None]
    T, M = d.shape
    dbar = d.mean(axis=0)
    omega2 = np.array([newey_west_var(d[:, k], max(int(mean_block) - 1, 0)) for k in range(M)])
    omega = np.sqrt(np.maximum(omega2, 1e-300))
    stat = float(np.max(np.sqrt(T) * dbar / omega))
    # Hansen's recentering: keep the mean for models that are "not too bad" (consistent p-value)
    thresh = -omega * np.sqrt(2.0 * np.log(np.log(max(T, 3))) / T)
    mu_c = np.where(dbar >= thresh, 0.0, dbar)          # subtract dbar only where dbar < thresh -> centred at 0 there
    rng = np.random.default_rng(seed)
    rc_hits = spa_hits = 0
    for _ in range(n_boot):
        idx = stationary_bootstrap(T, mean_block, rng)
        db = d[idx].mean(axis=0)
        rc_stat = np.max(np.sqrt(T) * (db - dbar) / omega)            # White: recentre every model at 0
        spa_stat = np.max(np.sqrt(T) * (db - dbar + mu_c) / omega)    # Hansen: poor models keep their (negative) mean
        rc_hits += rc_stat >= stat
        spa_hits += spa_stat >= stat
    return {"n_models": M, "T": T, "stat": stat, "best_model": int(np.argmax(dbar)), "best_mean_gain": float(dbar.max()),
            "p_rc": float((rc_hits + 1) / (n_boot + 1)), "p_spa": float((spa_hits + 1) / (n_boot + 1)), "n_boot": n_boot}


# ---------------------------------------------------------------- multiplicity, permutation, power

def bh_fdr(pvals, q=0.05):
    p = np.asarray(pvals, float)
    m = len(p)
    if m == 0:
        return {"survive": [], "qvalues": [], "q": q}
    order = np.argsort(p)
    ranks = np.arange(1, m + 1)
    adj = np.minimum.accumulate((p[order] * m / ranks)[::-1])[::-1]
    qv = np.empty(m); qv[order] = np.clip(adj, 0, 1)
    return {"survive": [bool(v <= q) for v in qv], "qvalues": [float(v) for v in qv], "q": q}


def permutation_p(observed, null):
    null = np.asarray(null, float)
    return float((np.sum(null >= observed) + 1) / (len(null) + 1))


def power_mds(sd, n, lag=0, alpha=0.05, target=0.80, n_sims=400, seed=19900802, grid=None):
    """Minimum detectable mean loss differential (in score units) at `target` power for a DM test
    on n reads with differential sd `sd`, by simulation (iid normal differentials; stated)."""
    if n < 5 or not sd or sd <= 0:
        return {"n": n, "mds": None, "note": "n < 5 or no variance: power not estimable"}
    rng = np.random.default_rng(seed)
    grid = grid if grid is not None else sd * np.array([0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.75, 1.0, 1.5, 2.0])
    out = []
    for delta in grid:
        rej = 0
        for _ in range(n_sims):
            d = rng.normal(delta, sd, n)
            r = dm_test(d, np.zeros(n), h=1, lag=lag)
            rej += bool(r.get("ok") and r["p_value"] < alpha)
        pw = rej / n_sims
        out.append((float(delta), pw))
        if pw >= target:
            return {"n": n, "sd": float(sd), "mds": float(delta), "power_at_mds": pw, "curve": out, "n_sims": n_sims}
    return {"n": n, "sd": float(sd), "mds": None, "curve": out, "note": "not reached on the grid", "n_sims": n_sims}
