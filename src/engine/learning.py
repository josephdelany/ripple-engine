"""
learning.py -- PATH Step 8 / protocol §5: the learning loop.

The engine may adjust itself ONLY by re-weighting a finite, registered menu of weightings
(data/walk_forward/menu.json), using the exponentially-weighted average forecaster -- Hedge
(Cesa-Bianchi & Lugosi 2006, Thm 2.2). After each outcome is known, and only then, each menu
item's cumulative sealed loss L_i grows; the engine's forecast at the next read is the mixture
sum_i w_i f_i with w_i proportional to exp(-eta * L_i).

Regret bound (losses in [0,1]): sum_t <w_t, l_t> - min_i L_i,T <= ln(N)/eta + eta*T/8.
The mixture forecast's loss is <= <w_t, l_t> for every convex proper score (Brier, log, CRPS are
convex in the forecast), so the bound holds for the mixture itself. tests/test_walk.py checks it
on a toy sequence.

Registered: ETA = 0.25 (~ sqrt(8 ln 12 / 300) for the expected ~300 reads per tier).
"""
from __future__ import annotations

import numpy as np

ETA = 0.25


class Hedge:
    def __init__(self, n, eta=ETA):
        self.n = int(n)
        self.eta = float(eta)
        self.L = np.zeros(self.n)
        self.T = 0

    def weights(self):
        z = -self.eta * (self.L - self.L.min())     # shift for numerical stability; weights are invariant to it
        w = np.exp(z)
        return w / w.sum()

    def update(self, losses):
        l = np.asarray(losses, float)
        if np.any(~np.isfinite(l)):
            raise ValueError("losses must be finite")
        if np.any(l < 0) or np.any(l > 1):
            raise ValueError("Hedge losses must lie in [0, 1] (scale them first)")
        self.L += l
        self.T += 1

    def state(self):
        return {"weights": [round(float(x), 6) for x in self.weights()],
                "cum_loss": [round(float(x), 6) for x in self.L], "n_updates": self.T, "eta": self.eta}


def regret_bound(n, eta, T):
    return float(np.log(n) / eta + eta * T / 8.0)


def run_hedge(loss_matrix, eta=ETA):
    """Replay Hedge over a T x N matrix of expert losses in [0,1]. Returns (hedge_losses per step,
    weights per step, regret, bound). Weights at step t depend only on losses before t."""
    L = np.asarray(loss_matrix, float)
    T, N = L.shape
    h = Hedge(N, eta)
    hl, W = [], []
    for t in range(T):
        w = h.weights()
        W.append(w.copy()); hl.append(float(w @ L[t]))
        h.update(L[t])
    regret = float(np.sum(hl) - L.sum(axis=0).min())
    return np.asarray(hl), np.asarray(W), regret, regret_bound(N, eta, T)
