"""
recalibrate.py -- WALK_FORWARD_PROTOCOL.md Amendment C (2026-09-02): walk-forward recalibration (menu item M13).

Per IES level l a monotone map g_l is fitted on the frozen mixture's EARLIER reads whose branch window had
closed by the read date (the walk's closed-by-t rule) and applied to the frozen mixture's probability of l;
the four mapped probabilities are renormalized. Let n be the number of closed reads with a label:
  n < 40                          identity (M13 = the frozen mixture)
  n >= 40, level with >= 40 hits  isotonic regression (pool-adjacent-violators on (p, 1[level = l]),
                                  evaluated by linear interpolation between block centres, clamped to [0,1])
  n >= 40, otherwise              Platt scaling sigma(a * logit(p) + b), maximum likelihood by Newton's
                                  method on p clipped to [0.01, 0.99]
Pure numpy; every piece is checked in tests/test_walk.py (closed forms) and tests/test_walk_recalibration.py.
"""
from __future__ import annotations

import math

import numpy as np

LEVELS = ("0", "1", "2", "3")
MIN_N = 40          # C.2: identity until this many closed reads
MIN_POS = 40        # C.2: isotonic needs this many positives for the level; otherwise Platt
CLIP = 0.01


def pav(x, y):
    """Isotonic regression (non-decreasing) of y on x by pool-adjacent-violators.
    Returns (block_x_mean, block_fitted) arrays sorted by x."""
    order = np.argsort(x, kind="stable")
    xs, ys = np.asarray(x, float)[order], np.asarray(y, float)[order]
    # blocks: [sum_y, count, sum_x]
    blocks = []
    for xi, yi in zip(xs, ys):
        blocks.append([yi, 1, xi])
        while len(blocks) >= 2 and blocks[-2][0] / blocks[-2][1] > blocks[-1][0] / blocks[-1][1]:
            b = blocks.pop()
            blocks[-1][0] += b[0]; blocks[-1][1] += b[1]; blocks[-1][2] += b[2]
    bx = np.array([b[2] / b[1] for b in blocks]); by = np.array([b[0] / b[1] for b in blocks])
    return bx, by


def isotonic_map(x, y):
    bx, by = pav(x, y)
    if len(bx) == 1:
        v = float(by[0])
        return lambda p: np.full_like(np.asarray(p, float), v)
    return lambda p: np.clip(np.interp(np.asarray(p, float), bx, by), 0.0, 1.0)


def _logit(p):
    p = np.clip(np.asarray(p, float), CLIP, 1 - CLIP)
    return np.log(p / (1 - p))


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500.0, 500.0)))


def platt_fit(p, y, iters=50, ridge=1e-3):
    """Maximum-likelihood a, b of sigma(a * logit(p) + b) by Newton's method with a small ridge (1e-3 on a and b,
    stated) so separable or one-class samples give a finite map instead of a diverging one. Returns (a, b, converged)."""
    z = _logit(p); y = np.asarray(y, float)
    a, b = 1.0, 0.0
    for _ in range(iters):
        s = _sigmoid(a * z + b)
        g = np.array([np.sum((s - y) * z) + ridge * a, np.sum(s - y) + ridge * b])
        w = s * (1 - s)
        H = np.array([[np.sum(w * z * z) + ridge, np.sum(w * z)], [np.sum(w * z), np.sum(w) + ridge]])
        try:
            step = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            return 1.0, 0.0, False
        a, b = a - step[0], b - step[1]
        if not (np.isfinite(a) and np.isfinite(b)):
            return 1.0, 0.0, False
        if np.max(np.abs(step)) < 1e-9:
            break
    return float(a), float(b), True


def platt_map(a, b):
    return lambda p: _sigmoid(a * _logit(p) + b)


class Recalibrator:
    """fit(probs, labels): probs = list of level->probability dicts (the frozen mixture at closed reads),
    labels = their realized levels. apply(probs) -> recalibrated dict (renormalized)."""

    def __init__(self, min_n=MIN_N, min_pos=MIN_POS, levels=LEVELS):
        self.min_n, self.min_pos, self.levels = min_n, min_pos, levels
        self.maps, self.mode, self.n = {}, {l: "identity" for l in levels}, 0

    def fit(self, probs, labels):
        self.n = len(labels)
        self.maps, self.mode = {}, {l: "identity" for l in self.levels}
        if self.n < self.min_n:
            return self
        for l in self.levels:
            x = np.array([float(p.get(l, 0.0)) for p in probs]); y = np.array([1.0 if lab == l else 0.0 for lab in labels])
            if int(y.sum()) >= self.min_pos:
                self.maps[l], self.mode[l] = isotonic_map(x, y), "isotonic"
            else:
                a, b, ok = platt_fit(x, y)
                if ok:
                    self.maps[l], self.mode[l] = platt_map(a, b), "platt"
        return self

    def apply(self, probs):
        if probs is None:
            return None
        if not self.maps:                       # identity: the frozen mixture, untouched (no renormalization noise)
            return dict(probs)
        out = {}
        for l in self.levels:
            p = float(probs.get(l, 0.0))
            out[l] = float(self.maps[l](p)) if l in self.maps else p
        z = sum(out.values())
        return {l: (v / z if z > 0 else float(probs.get(l, 0.0))) for l, v in out.items()}

    def state(self):
        return {"n_fit": self.n, "mode": dict(self.mode)}


def fit_apply_arrays(P, y, p, min_n=MIN_N, min_pos=MIN_POS):
    """The same rule on arrays, for the replays (Amendment C.4): P n x K probabilities of the closed reads,
    y their realized level indices, p the K-vector to recalibrate. Returns the recalibrated K-vector."""
    P = np.asarray(P, float); y = np.asarray(y); p = np.asarray(p, float)
    n, K = P.shape
    out = p.copy()
    if n < min_n:
        return out
    for l in range(K):
        yl = (y == l).astype(float)
        if int(yl.sum()) >= min_pos:
            out[l] = float(isotonic_map(P[:, l], yl)(p[l]))
        else:
            a, b, ok = platt_fit(P[:, l], yl)
            if ok:
                out[l] = float(platt_map(a, b)(p[l]))
    z = out.sum()
    return out / z if z > 0 else p
