"""
scoring.py -- PATH Step 8 / protocol §3: strictly proper scoring rules, in closed form.

A proper score cannot be gamed: the best expected score comes only from reporting honest
probabilities (Gneiting & Raftery 2007). Every function here is pure numpy and is checked
against a closed-form value in tests/test_walk.py.

  brier(probs, realized)          multi-category Brier over the IES-90 levels: sum_l (p_l - 1[l = realized])^2, in [0, 2]
  rps(probs, realized)            ranked probability score over the ORDINAL levels (Epstein 1969; Murphy 1971):
                                  sum_{k=0}^{K-2} (F_k - O_k)^2 with F, O the cumulative forecast / outcome; in
                                  [0, K-1 = 3]; strictly proper; a miss by two levels costs more than a miss by one
  brier_binary(p, y)              the DEAL flag: (p - y)^2
  log_score(probs, realized)      -ln p_realized after the registered floor (read.LOG_FLOOR)
  crps(values, y, weights)        CRPS of a (weighted) empirical distribution:
                                  E|X - y| - 1/2 E|X - X'|   (Gneiting & Raftery eq. 21)
  pinball(values, y, tau, w)      quantile (pinball) loss at level tau on the weighted quantile
  pit(values, y, weights)         probability integral transform: F(y) with half mass on ties
  sign_correct(values, y, w)      sign of the weighted median agrees with sign of y
  murphy(probs, outcomes, bins)   Murphy (1973) decomposition of the binary Brier score:
                                  Brier = reliability - resolution + uncertainty
  skill(s_engine, s_ref)          1 - S_engine / S_reference (> 0: beats the reference)

DIAGNOSTIC, NOT REGISTERED (protocol §3 registers Brier and CRPS; the registered scores drive every
gate). An empirical distribution built from m analogs carries sampling noise that the population
distribution does not; its expected CRPS exceeds the population CRPS by E|X-X'|/(2m), and its
expected Brier exceeds the population Brier by sum_b p_b(1-p_b)/m. Climatology pools ~10x more atoms
than an item (k = 5..12), so under the NULL the registered skill of the engine vs climatology is
negative -- by sample size alone. The walk publishes the size-corrected ("fair", Ferro 2014 QJRMS)
scores beside the registered ones so the size of that bias is visible; it does not gate on them:
  crps_fair(values, y, weights)   E|X-y| - 1/2 * sum_{i!=j} w_i w_j |x_i-x_j| / (1 - sum_i w_i^2)
                                  (uniform weights: Ferro's m/(m-1) correction; one atom: |x-y|)
  brier_fair(labels, realized, w) sum_b [(p_b - 1[b])^2 - c * p_b (1-p_b)],  c = sum w^2 / (1 - sum w^2)
                                  (uniform weights: Ferro's p(1-p)/(m-1) correction; one atom: Brier)
  rps_fair(labels, realized, w)   the same correction on each cumulative term: sum_k [(F_k - O_k)^2 - c F_k (1-F_k)]
"""
from __future__ import annotations

import numpy as np

LEVELS = ("0", "1", "2", "3")          # IES-90 ordinal levels (OUTCOME_MAPPING.md Amendment 1); order matters for rps
LOG_FLOOR = 0.01


def _w(values, weights):
    v = np.asarray(values, float)
    if weights is None:
        w = np.full(len(v), 1.0 / len(v))
    else:
        w = np.asarray(weights, float)
        w = w / w.sum()
    return v, w


def brier(probs: dict, realized: str, branches=LEVELS) -> float:
    return float(sum((float(probs.get(b, 0.0)) - (1.0 if b == realized else 0.0)) ** 2 for b in branches))


def brier_binary(p, y) -> float:
    return float((float(p) - float(y)) ** 2)


def rps(probs: dict, realized: str, levels=LEVELS) -> float:
    """Ranked probability score over ordered categories: sum over the K-1 cumulative thresholds of the
    squared difference between cumulative forecast and cumulative outcome (Epstein 1969)."""
    p = np.array([float(probs.get(l, 0.0)) for l in levels])
    o = np.array([1.0 if l == realized else 0.0 for l in levels])
    F, O = np.cumsum(p)[:-1], np.cumsum(o)[:-1]
    return float(np.sum((F - O) ** 2))


def floor_probs(probs: dict, floor=LOG_FLOOR, branches=LEVELS) -> dict:
    f = {b: max(float(probs.get(b, 0.0)), floor) for b in branches}
    z = sum(f.values())
    return {b: f[b] / z for b in branches}


def log_score(probs: dict, realized: str, floor=LOG_FLOOR, branches=LEVELS) -> float:
    return float(-np.log(floor_probs(probs, floor, branches)[realized]))


def crps(values, y, weights=None) -> float:
    """CRPS of the empirical distribution with atoms `values` (weights optional) at realization y.

    E|X - X'| is computed in O(n log n) on the sorted atoms rather than from the n x n pairwise
    matrix: with v sorted ascending, W_i = sum_{j<i} w_j and S_i = sum_{j<i} w_j v_j,
        E|X - X'| = 2 * sum_i w_i * (v_i * W_i - S_i).
    (The pairwise form needs n^2 floats -- 13 GB at n = 40,000 -- and stalled the closed-form test.)"""
    v, w = _w(values, weights)
    order = np.argsort(v, kind="stable")
    v, w = v[order], w[order]
    term1 = float(np.sum(w * np.abs(v - y)))
    cw = np.cumsum(w) - w                 # weight strictly below each atom
    cs = np.cumsum(w * v) - w * v         # weighted sum strictly below each atom
    term2 = 2.0 * float(np.sum(w * (v * cw - cs)))
    return term1 - 0.5 * term2


def crps_fair(values, y, weights=None) -> float:
    """Size-corrected CRPS (diagnostic; see the module docstring). Unbiased for the population CRPS
    when the atoms are exchangeable draws from the forecast distribution (Ferro 2014)."""
    v, w = _w(values, weights)
    sw2 = float(np.sum(w * w))
    if len(v) < 2 or sw2 >= 1.0 - 1e-12:
        return float(np.sum(w * np.abs(v - y)))          # a single atom: no spread to correct
    std = crps(v, y, w)
    term2 = 2.0 * (float(np.sum(w * np.abs(v - y))) - std)   # = sum_{i,j} w_i w_j |x_i - x_j| (diagonal is 0)
    return float(np.sum(w * np.abs(v - y)) - 0.5 * term2 / (1.0 - sw2))


def brier_fair(labels, realized: str, weights=None, branches=LEVELS) -> float:
    """Size-corrected multi-category Brier (diagnostic; see the module docstring). labels: one branch
    label per atom (analog); weights optional. Returns the registered Brier when only one atom."""
    labels = list(labels)
    if not labels:
        raise ValueError("brier_fair needs at least one atom")
    w = np.full(len(labels), 1.0 / len(labels)) if weights is None else np.asarray(weights, float)
    w = w / w.sum()
    p = {b: float(np.sum(w * np.array([1.0 if l == b else 0.0 for l in labels]))) for b in branches}
    sw2 = float(np.sum(w * w))
    if len(labels) < 2 or sw2 >= 1.0 - 1e-12:
        return brier(p, realized, branches)
    c = sw2 / (1.0 - sw2)
    return float(sum((p[b] - (1.0 if b == realized else 0.0)) ** 2 - c * p[b] * (1.0 - p[b]) for b in branches))


def rps_fair(labels, realized: str, weights=None, levels=LEVELS) -> float:
    """Size-corrected RPS (diagnostic): each cumulative term is a binary Brier on F_k, corrected as brier_fair."""
    labels = list(labels)
    if not labels:
        raise ValueError("rps_fair needs at least one atom")
    w = np.full(len(labels), 1.0 / len(labels)) if weights is None else np.asarray(weights, float)
    w = w / w.sum()
    p = {l: float(np.sum(w * np.array([1.0 if x == l else 0.0 for x in labels]))) for l in levels}
    sw2 = float(np.sum(w * w))
    if len(labels) < 2 or sw2 >= 1.0 - 1e-12:
        return rps(p, realized, levels)
    c = sw2 / (1.0 - sw2)
    F = np.cumsum([p[l] for l in levels])[:-1]
    O = np.cumsum([1.0 if l == realized else 0.0 for l in levels])[:-1]
    return float(np.sum((F - O) ** 2 - c * F * (1.0 - F)))


def weighted_quantile(values, tau, weights=None) -> float:
    v, w = _w(values, weights)
    order = np.argsort(v)
    v, w = v[order], w[order]
    cum = np.cumsum(w)
    i = int(np.searchsorted(cum, tau, side="left"))
    return float(v[min(i, len(v) - 1)])


def pinball(values, y, tau, weights=None) -> float:
    q = weighted_quantile(values, tau, weights)
    return float(tau * (y - q)) if y >= q else float((1.0 - tau) * (q - y))


def pit(values, y, weights=None) -> float:
    v, w = _w(values, weights)
    return float(np.sum(w * (v < y)) + 0.5 * np.sum(w * (v == y)))


def sign_correct(values, y, weights=None):
    if y == 0:
        return None
    return bool(np.sign(weighted_quantile(values, 0.5, weights)) == np.sign(y))


def murphy(probs, outcomes, bins=5) -> dict:
    """Murphy (1973) decomposition for a binary event. probs: forecast probabilities; outcomes: 0/1.
    Brier = reliability - resolution + uncertainty (exact identity over the binning)."""
    p = np.asarray(probs, float); o = np.asarray(outcomes, float)
    n = len(p)
    if n == 0:
        return {"n": 0}
    obar = o.mean()
    edges = np.linspace(0, 1, bins + 1)
    idx = np.clip(np.digitize(p, edges[1:-1], right=True), 0, bins - 1)
    rel = res = 0.0
    diagram = []
    for k in range(bins):
        m = idx == k
        nk = int(m.sum())
        if nk == 0:
            continue
        pk, ok = p[m].mean(), o[m].mean()
        rel += nk * (pk - ok) ** 2
        res += nk * (ok - obar) ** 2
        diagram.append({"bin": [round(float(edges[k]), 2), round(float(edges[k + 1]), 2)], "n": nk,
                        "forecast_mean": round(float(pk), 4), "observed_freq": round(float(ok), 4)})
    unc = obar * (1 - obar)
    bs = float(np.mean((p - o) ** 2))
    # Murphy's identity is exact only when every forecast in a bin takes the bin's mean value. For
    # continuous forecasts binned afterwards the exact identity (Stephenson, Coelho & Jolliffe 2008) is
    #   Brier = REL - RES + UNC + WBV - WBC
    # with WBV the within-bin variance of the forecasts and WBC twice the within-bin covariance of
    # forecast and outcome. Both are published; identity_gap is the residual of the EXACT identity.
    wbv = wbc = 0.0
    for k in range(bins):
        m = idx == k
        if m.sum() == 0:
            continue
        dp = p[m] - p[m].mean()
        wbv += float(np.sum(dp * dp))
        wbc += 2.0 * float(np.sum(dp * (o[m] - o[m].mean())))
    return {"n": n, "brier": round(bs, 5), "reliability": round(rel / n, 5), "resolution": round(res / n, 5),
            "uncertainty": round(float(unc), 5), "base_rate": round(float(obar), 4), "diagram": diagram,
            "within_bin_variance": round(wbv / n, 6), "within_bin_covariance": round(wbc / n, 6),
            "murphy_gap": round(bs - (rel / n - res / n + unc), 8),
            "identity_gap": round(bs - (rel / n - res / n + unc + wbv / n - wbc / n), 8)}


def skill(s_engine, s_ref):
    if s_ref is None or s_engine is None or s_ref == 0:
        return None
    return float(1.0 - s_engine / s_ref)


def mixture_g(dists, weights, branches=LEVELS):
    """Weighted average of branch-rate dicts (items with no distribution are dropped, weights renormalized)."""
    pairs = [(d, w) for d, w in zip(dists, weights) if d]
    if not pairs:
        return None
    z = sum(w for _, w in pairs)
    if z <= 0:
        return None
    return {b: float(sum(w * float(d.get(b, 0.0)) for d, w in pairs) / z) for b in branches}


def mixture_p(value_lists, weights, id_lists=None):
    """Weighted ensemble from several analog value lists: each list's atoms share its item weight.
    With id_lists, an analog that several items retrieved is ONE atom carrying the sum of its weights
    (the registered CRPS is unchanged by merging; the effective sample size in crps_fair is not).
    Returns (values, weights) or (values, weights, ids) when id_lists is given; (None, None) if empty."""
    if id_lists is None:
        vals, ws = [], []
        for vl, w in zip(value_lists, weights):
            if vl and w > 0:
                vals.extend(vl); ws.extend([w / len(vl)] * len(vl))
        return (vals, ws) if vals else (None, None)
    merged = {}
    for vl, il, w in zip(value_lists, id_lists, weights):
        if vl and w > 0:
            for v, i in zip(vl, il):
                cur = merged.get(i)
                merged[i] = (v, (cur[1] if cur else 0.0) + w / len(vl))
    if not merged:
        return None, None, None
    ids = list(merged)
    return [merged[i][0] for i in ids], [merged[i][1] for i in ids], ids


def mixture_atoms(id_lists, label_lists, weights):
    """Merged (ids, labels, weights) of the branch-label atoms behind a G mixture -- the evidence
    behind mixture_g, one atom per analog, weight = sum over the items that retrieved it."""
    merged = {}
    for il, ll, w in zip(id_lists, label_lists, weights):
        if il and w > 0:
            for i, l in zip(il, ll):
                merged[i] = (l, merged.get(i, (l, 0.0))[1] + w / len(il))
    if not merged:
        return [], [], []
    ids = list(merged)
    return ids, [merged[i][0] for i in ids], [merged[i][1] for i in ids]
