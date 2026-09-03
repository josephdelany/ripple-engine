"""
price_walk.py -- GRID_STUDY_REGISTRATION.md Part III + Amendment 1 (2026-09-03): the grid study's PRICE arm.

The unit is a DATE, not an event. At every month-end grid date t the engine reads the world state, retrieves
the k most similar prior grid dates whose own outcome had already closed by t, and issues the empirical
distribution of the returns that followed them, for six targets and five horizons.

Registered before this file existed: Part III (commit 48e1e9b) and its Amendment 1 (commit c949565), which
fixed the four block set, the 175-candidate search grid, k, tau, the burn-in and the eligibility rule.

What this arm is for, in one line: the event-triggered walk scores 253 reads and never sees a third of the
days the market moved; this scores every month-end and therefore sees all of them.

  registered scores      CRPS (gate), pinball 10/50/90, PIT           -- protocol §3, unchanged
  baselines              grid-climatology, no-change, random analogs, the FROZEN equal-weight engine
  the fitted model       four block weights + one metric scale, selected by expanding-origin nested CV
                         on reads whose outcome closed by t -- published against the frozen one EITHER WAY

Run:  python3 src/engine/grid/price_walk.py [--fast]
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from engine import scoring as SC          # noqa: E402
from engine import inference as INF       # noqa: E402
from engine.grid import power_arithmetic as PA   # noqa: E402
import walk as W                          # noqa: E402

OUT_DIR = ROOT / "data" / "grid" / "price"

# ----------------------------------------------------------------- registered (Part III + Amendment 1)
BLOCKS = {
    "physical": ["inv_sigma", "diesel_crack", "brent_wti_spread_z"],
    "market": ["brent_vol20", "vix_pct", "cot_pct", "ovx_pct"],
    "macro": ["curve_2s10s", "real_rate", "usd_z", "credit_stress"],
    "geopolitical": ["gpr", "conflict_intensity_pct"],
}
BLOCK_NAMES = tuple(BLOCKS)
K = 12                                   # Amendment 1: k nearest eligible grid dates
TAU_GRID = (0.25, 0.5, 1.0, 2.0, 4.0)    # Amendment 1: the metric scale
W_STEP = 0.25                            # Amendment 1: simplex step
BURN_IN = 60                             # Amendment 1: closed prior grid dates before a read is scored
FROZEN_W = np.array([0.25, 0.25, 0.25, 0.25])
FROZEN_TAU = 1.0
SEED = W.REGISTERED["seeds"]["bootstrap_and_spa"]
N_BOOT = W.REGISTERED["n_boot"]
N_SPA = W.REGISTERED["n_spa_boot"]
CLUSTER_DAYS = W.REGISTERED["cluster_days"]
HORIZONS = PA.HORIZONS
TARGETS = PA.TARGETS


def simplex_grid(n=4, step=W_STEP):
    """Amendment 1: block weights on the simplex in steps of 0.25 -- 35 vectors for four blocks."""
    m = int(round(1 / step))
    out = []
    for c in product(range(m + 1), repeat=n):
        if sum(c) == m:
            out.append(np.array(c, float) * step)
    return out


CANDIDATES = [(w, t) for w in simplex_grid() for t in TAU_GRID]


# ----------------------------------------------------------------- the panel

# ---------------------------------------------------------------- Amendment 2: the abnormal-return target

EST_WINDOW = 250          # trading days in the estimation window
EST_GAP = 21              # trading days between the estimation window and the read (20-day horizon + 1)
EST_MIN = 100             # minimum usable observations, else the read is dropped and counted
FACTOR = {"diesel_crack": "brent", "gasoline_crack": "brent"}      # market model; all others constant-mean


def abnormal_returns(series, cal, grid, gi, R_raw):
    """Amendment 2 (A2.1). AR(t,h) = raw(t,h) - h*alpha - beta*factor(t,h), with alpha and beta estimated by
    OLS on DAILY log returns over the 250 trading days ending EST_GAP days before the read -- so the read's
    own horizon can never enter its own benchmark. Constant-mean (beta = 0) for crude and gas; market model
    on Brent for the cracks. Returns the AR array and the count of reads dropped for a short window."""
    # TARGETS here is PA.TARGETS: a flat {name: series_id} map of STRINGS, not specs.
    lvl, dropped = {}, 0
    for name, sid in TARGETS.items():
        s_ = series.get(sid)
        if s_ is not None:
            with np.errstate(divide="ignore", invalid="ignore"):
                lvl[name] = np.log(s_.reindex(cal).to_numpy(float))
    T, A, H = R_raw.shape
    AR = np.full_like(R_raw, np.nan)
    diag = {}
    for ai, name in enumerate(TARGETS):
        if name not in lvl:
            continue
        y = lvl[name]
        f = lvl.get(FACTOR.get(name)) if FACTOR.get(name) in lvl else None
        dy = np.diff(y, prepend=np.nan)
        df_ = np.diff(f, prepend=np.nan) if f is not None else None
        n_ok = 0
        for ti, g0 in enumerate(gi):
            e1 = g0 - EST_GAP
            e0 = e1 - EST_WINDOW
            if e0 < 1:
                dropped += 1; continue
            ry = dy[e0:e1]
            if df_ is None:
                m = np.isfinite(ry)
                if m.sum() < EST_MIN:
                    dropped += 1; continue
                alpha, beta = float(ry[m].mean()), 0.0
            else:
                rf = df_[e0:e1]
                m = np.isfinite(ry) & np.isfinite(rf)
                if m.sum() < EST_MIN:
                    dropped += 1; continue
                X = np.column_stack([np.ones(m.sum()), rf[m]])
                b_, *_ = np.linalg.lstsq(X, ry[m], rcond=None)
                alpha, beta = float(b_[0]), float(b_[1])
            n_ok += 1
            for hi, h in enumerate(HORIZONS):
                raw = R_raw[ti, ai, hi]
                if not np.isfinite(raw):
                    continue
                exp_ = 100.0 * h * alpha
                if df_ is not None:
                    fi = list(TARGETS).index(FACTOR[name])
                    fr = R_raw[ti, fi, hi]
                    if not np.isfinite(fr):
                        continue
                    exp_ += beta * fr
                AR[ti, ai, hi] = raw - exp_
        diag[name] = {"model": ("market_model_on_" + FACTOR[name]) if df_ is not None else "constant_mean",
                      "reads_with_a_model": n_ok}
    return AR, dropped, diag


def build_panel():
    """Grid dates, the point-in-time state matrix and the return matrix. All from the loaded DB."""
    conn = sqlite3.connect(PA.DB)
    fields = [f for b in BLOCKS.values() for f in b]
    ids = sorted(set(list(TARGETS.values()) + [PA.MARKET_FIELDS[f] for f in fields]))
    series = PA.load_series(conn, ids)
    cal = PA.trading_calendar(series)
    grid = PA.grid_dates(cal, "month_end")
    gi = pd.Series(np.arange(len(cal)), index=cal).reindex(grid).to_numpy().astype(int)

    # raw state at t: each field's last observation strictly before t - lag(field)  (Amendment G)
    S = np.full((len(grid), len(fields)), np.nan)
    g = grid.to_numpy()
    for j, f in enumerate(fields):
        s = series.get(PA.MARKET_FIELDS[f])
        if s is None:
            continue
        cut = g - np.timedelta64(PA.RELEASE_LAGS.get(f, 0), "D")
        idx = np.searchsorted(s.index.to_numpy(), cut, side="left") - 1
        ok = idx >= 0
        S[ok, j] = s.to_numpy()[idx[ok]]

    # returns: r[t, a, h] = log(P_{t+h} / P_t)
    R = np.full((len(grid), len(TARGETS), len(HORIZONS)), np.nan)
    for ai, (name, sid) in enumerate(TARGETS.items()):
        s = series.get(sid)
        if s is None:
            continue
        on = s.reindex(cal).to_numpy()
        for hi, h in enumerate(HORIZONS):
            ok = (gi + h) < len(cal)
            v0 = np.where(ok, on[np.clip(gi, 0, len(cal) - 1)], np.nan)
            v1 = np.where(ok, on[np.clip(gi + h, 0, len(cal) - 1)], np.nan)
            with np.errstate(divide="ignore", invalid="ignore"):
                R[:, ai, hi] = np.log(v1 / v0)
    return grid, gi, fields, S, R, series, cal


def block_distances(S, fields):
    """Per-block mean squared difference on the POINT-IN-TIME standardisation (Amendment 1).

    D[b][i, j] = mean over the fields of block b known at BOTH i and j of (z_i - z_j)^2, with z computed
    from grid dates strictly before i -- both endpoints on i's stats, so they share a scale."""
    T, F = S.shape
    known = ~np.isnan(S)
    mu = np.full((T, F), np.nan); sd = np.full((T, F), np.nan)
    for i in range(T):
        past = S[:i]
        with np.errstate(invalid="ignore"):
            m = np.nanmean(past, axis=0) if i else np.full(F, np.nan)
            s = np.nanstd(past, axis=0) if i > 1 else np.full(F, np.nan)
        mu[i], sd[i] = m, np.where((s > 0) & np.isfinite(s), s, np.nan)
    D = {b: np.full((T, T), np.nan) for b in BLOCK_NAMES}
    cols = {b: [fields.index(f) for f in fs] for b, fs in BLOCKS.items()}
    for i in range(T):
        z_i = (S[i] - mu[i]) / sd[i]                       # 1 x F, standardised on i's stats
        Z = (S - mu[i]) / sd[i]                            # T x F, the same stats for every candidate
        both = known[i] & known & np.isfinite(Z) & np.isfinite(z_i)
        diff2 = (Z - z_i) ** 2
        for b in BLOCK_NAMES:
            c = cols[b]
            m = both[:, c]
            n = m.sum(axis=1)
            with np.errstate(invalid="ignore"):
                s = np.where(m, diff2[:, c], 0.0).sum(axis=1)
            D[b][i] = np.where(n > 0, s / np.maximum(n, 1), np.nan)
    return D


def combined(D, w):
    """sqrt of the weighted mean over the blocks that are defined for a pair; a missing block's weight is
    redistributed over the rest (Amendment 1) and the pair is dropped only if no block is defined."""
    num = np.zeros_like(D[BLOCK_NAMES[0]])
    den = np.zeros_like(num)
    for wi, b in zip(w, BLOCK_NAMES):
        if wi == 0:
            continue
        ok = np.isfinite(D[b])
        num += np.where(ok, D[b] * wi, 0.0)
        den += np.where(ok, wi, 0.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        out = np.sqrt(np.where(den > 0, num / den, np.nan))
    return out


# ----------------------------------------------------------------- forecasts and scores

def eligible_mask(T, gi, h):
    """Analog u is eligible at t iff u's own outcome closed by t: u + h trading days <= t (Amendment 1)."""
    close = gi + h
    return (close[None, :] <= gi[:, None]) & ~np.eye(T, dtype=bool)


def crps_grid(dist, R, elig, ai, hi, k=K, tau=1.0):
    """CRPS of the k-nearest-analog forecast at every grid date, for one target and horizon."""
    T = dist.shape[0]
    y = R[:, ai, hi]
    out = np.full(T, np.nan)
    n_at = np.zeros(T, int)
    for t in range(T):
        m = elig[t] & np.isfinite(dist[t]) & np.isfinite(R[:, ai, hi])
        if m.sum() < BURN_IN or not np.isfinite(y[t]):
            continue
        idx = np.flatnonzero(m)
        d = dist[t, idx]
        sel = idx[np.argsort(d, kind="stable")[:k]]
        wts = np.exp(-dist[t, sel] / tau)
        if not np.isfinite(wts).all() or wts.sum() <= 0:
            wts = np.ones(len(sel))
        out[t] = SC.crps(R[sel, ai, hi], y[t], wts)
        n_at[t] = len(sel)
    return out, n_at


def baseline_scores(R, elig, gi):
    """Grid-climatology, no-change and random analogs -- all point-in-time (§1.3, §3.3)."""
    T, A, H = R.shape
    clim = np.full((T, A, H), np.nan)
    noch = np.full_like(clim, np.nan)
    rand = np.full_like(clim, np.nan)
    for ai in range(A):
        for hi in range(H):
            y = R[:, ai, hi]
            for t in range(T):
                m = elig[t] & np.isfinite(y)
                if m.sum() < BURN_IN or not np.isfinite(y[t]):
                    continue
                pool = y[m]
                clim[t, ai, hi] = SC.crps(pool, y[t])
                noch[t, ai, hi] = SC.crps(np.array([0.0]), y[t])
                rng = np.random.default_rng(SEED + t * 1000 + ai * 10 + hi)
                draws = [SC.crps(rng.choice(pool, size=min(K, len(pool)), replace=False), y[t])
                         for _ in range(25)]
                rand[t, ai, hi] = float(np.mean(draws))
    return clim, noch, rand


def crps_all(D, R, gi, cand):
    """CRPS of one registered candidate at every (grid date, target, horizon) on the supplied target array."""
    w, tau = cand
    T, A, H = R.shape
    out = np.full((T, A, H), np.nan)
    dist = combined(D, w)
    masks = {h: eligible_mask(T, gi, h) for h in HORIZONS}
    for hi, h in enumerate(HORIZONS):
        for ai in range(A):
            out[:, ai, hi], _ = crps_grid(dist, R, masks[h], ai, hi, tau=tau)
    return out, dist


def candidate_scores(D, R, gi, cands, quiet=False):
    """CRPS of every registered candidate at every (grid date, target, horizon).

    This is the object the nested CV needs: candidate c's score at u is a legitimate point-in-time score,
    because c's forecast at u used only analogs closed by u. The inner-fold criterion at outer read t is
    then the cumulative sum over the u whose outcome closed by t -- exact, not an approximation."""
    T = R.shape[0]
    A, H = len(TARGETS), len(HORIZONS)
    out = np.full((len(cands), T, A, H), np.nan)
    masks = {h: eligible_mask(T, gi, h) for h in HORIZONS}
    for ci, (w, tau) in enumerate(cands):
        dist = combined(D, w)
        for hi, h in enumerate(HORIZONS):
            for ai in range(A):
                out[ci, :, ai, hi], _ = crps_grid(dist, R, masks[h], ai, hi, tau=tau)
        if not quiet and ci % 25 == 0:
            print(f"  candidate {ci + 1}/{len(cands)}", flush=True)
    return out


def nested_cv(cand_crps, gi, cands):
    """Amendment 1: at outer read t, select the candidate minimising cumulative CRPS over the reads whose
    outcome closed by t. Inner folds are strictly before the outer read, with no exception."""
    C, T, A, H = cand_crps.shape
    pooled = np.nanmean(cand_crps.reshape(C, T, A * H), axis=2)          # C x T
    chosen = np.full(T, -1, int)
    n_inner = np.zeros(T, int)
    maxh = max(HORIZONS)
    for t in range(T):
        closed = np.flatnonzero((gi + maxh) <= gi[t])
        closed = closed[closed < t]
        n_inner[t] = len(closed)
        if len(closed) < BURN_IN:
            continue                       # no fit until the inner set exists; the read is unscored
        cum = np.nansum(pooled[:, closed], axis=1)
        valid = np.isfinite(cum) & (np.sum(np.isfinite(pooled[:, closed]), axis=1) > 0)
        chosen[t] = int(np.argmin(np.where(valid, cum, np.inf)))
    return chosen, n_inner


def full_diagnostics(dist_by_t, R, gi, taus_by_t, chosen_mask):
    """§3.2's registered companions to the gate score, computed only for the forecasters that are published
    (not for all 175 candidates): the Ferro size-corrected CRPS -- whose bias runs AGAINST a k-atom engine
    and FOR a large-pool climatology (Amendment E.3) -- plus pinball at 10/50/90 and the PIT."""
    T, A, H = R.shape
    out = {k: np.full((T, A, H), np.nan) for k in ("crps", "crps_fair", "pin10", "pin50", "pin90", "pit")}
    masks = {h: eligible_mask(T, gi, h) for h in HORIZONS}
    for hi, h in enumerate(HORIZONS):
        elig = masks[h]
        for t in range(T):
            if not chosen_mask[t]:
                continue
            dist, tau = dist_by_t[t], taus_by_t[t]
            for ai in range(A):
                y = R[t, ai, hi]
                m = elig[t] & np.isfinite(dist[t]) & np.isfinite(R[:, ai, hi])
                if m.sum() < BURN_IN or not np.isfinite(y):
                    continue
                idx = np.flatnonzero(m)
                sel = idx[np.argsort(dist[t, idx], kind="stable")[:K]]
                v = R[sel, ai, hi]
                w = np.exp(-dist[t, sel] / tau)
                if not np.isfinite(w).all() or w.sum() <= 0:
                    w = np.ones(len(sel))
                out["crps"][t, ai, hi] = SC.crps(v, y, w)
                out["crps_fair"][t, ai, hi] = SC.crps_fair(v, y, w)
                for tau_q, key in ((0.10, "pin10"), (0.50, "pin50"), (0.90, "pin90")):
                    out[key][t, ai, hi] = SC.pinball(v, y, tau_q, w)
                out["pit"][t, ai, hi] = SC.pit(v, y, w)
    return out


def climatology_diagnostics(R, gi):
    """The same companions for grid-climatology, whose pool is large -- so its fair CRPS is close to its
    registered one, which is exactly the asymmetry Amendment E.3 names."""
    T, A, H = R.shape
    out = {k: np.full((T, A, H), np.nan) for k in ("crps", "crps_fair", "pit")}
    for hi, h in enumerate(HORIZONS):
        elig = eligible_mask(T, gi, h)
        for ai in range(A):
            y = R[:, ai, hi]
            for t in range(T):
                m = elig[t] & np.isfinite(y)
                if m.sum() < BURN_IN or not np.isfinite(y[t]):
                    continue
                pool = y[m]
                out["crps"][t, ai, hi] = SC.crps(pool, y[t])
                out["crps_fair"][t, ai, hi] = SC.crps_fair(pool, y[t])
                out["pit"][t, ai, hi] = SC.pit(pool, y[t])
    return out


def _hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()


# ----------------------------------------------------------------- the run

def run(fast=False):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    run_id = "grid_price_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    grid, gi, fields, S, R, series, cal = build_panel()
    T = len(grid)
    print(f"grid {T} month-ends {grid[0].date()}..{grid[-1].date()}; {len(fields)} fields", flush=True)
    D = block_distances(S, fields)
    cands = CANDIDATES[:15] if fast else CANDIDATES
    n_boot, n_spa = (200, 200) if fast else (N_BOOT, N_SPA)

    AR, n_dropped, ar_diag = abnormal_returns(series, cal, grid, gi, R)
    print(f"abnormal-return target built: {n_dropped} read-target cells dropped for a short estimation window",
          flush=True)
    print(f"scoring {len(cands)} registered candidates ...", flush=True)
    cand_crps = candidate_scores(D, R, gi, cands)
    chosen, n_inner = nested_cv(cand_crps, gi, cands)

    frozen_ci = min(range(len(cands)),
                    key=lambda i: (np.abs(cands[i][0] - FROZEN_W).sum(), abs(cands[i][1] - FROZEN_TAU)))
    frozen = cand_crps[frozen_ci]
    fitted = np.full_like(frozen, np.nan)
    for t in range(T):
        if chosen[t] >= 0:
            fitted[t] = cand_crps[chosen[t], t]

    # every baseline pool obeys the same closing rule as the engine's analogs, per horizon
    clim = np.full_like(frozen, np.nan); noch = np.full_like(frozen, np.nan); rand = np.full_like(frozen, np.nan)
    for hi, h in enumerate(HORIZONS):
        m = eligible_mask(T, gi, h)
        c1, n1, r1 = baseline_scores(R[:, :, [hi]], m, gi)
        clim[:, :, hi] = c1[:, :, 0]; noch[:, :, hi] = n1[:, :, 0]; rand[:, :, hi] = r1[:, :, 0]

    # §3.2's registered companions, on the published forecasters only
    dist_fit = [combined(D, cands[chosen[t]][0]) if chosen[t] >= 0 else None for t in range(T)]
    tau_fit = [cands[chosen[t]][1] if chosen[t] >= 0 else 1.0 for t in range(T)]
    mask_fit = np.array([c >= 0 for c in chosen])
    dist_frz = combined(D, cands[frozen_ci][0])
    diag_fit = full_diagnostics([d if d is not None else dist_frz for d in dist_fit], R, gi, tau_fit, mask_fit)
    diag_frz = full_diagnostics([dist_frz] * T, R, gi, [cands[frozen_ci][1]] * T, np.ones(T, bool))
    diag_clim = climatology_diagnostics(R, gi)

    dates = [str(d.date()) for d in grid]
    mb = W._mean_block(dates, CLUSTER_DAYS); lag = max(int(round(mb)) - 1, 0)

    def per_date(x, y):
        """Reduce a T x ... score array to one value per grid date over the cells finite in BOTH.

        THE CORRECTION THAT MATTERS. The first cut of this module flattened T x A x H to one long vector
        and resampled it with a block length measured in DATES. Adjacent entries in that flat vector are
        different targets at the same date -- Brent and WTI 20-day returns correlate 0.906 -- so a block of
        two in flattened index space is not a block in time, and the interval was computed as though there
        were 10,857 quasi-independent observations where §2.8's own arithmetic says there are 1,979. Every
        interval and every p-value in this file now resamples WHOLE GRID DATES, all their cells moving
        together, which is the same joint construction §2.8 registered for counting -- applied to inference."""
        m = np.isfinite(x) & np.isfinite(y)
        xr = np.where(m, x, np.nan).reshape(x.shape[0], -1)
        yr = np.where(m, y, np.nan).reshape(y.shape[0], -1)
        with np.errstate(invalid="ignore"):
            a_ = np.nanmean(xr, axis=1); b_ = np.nanmean(yr, axis=1)
        ok = np.isfinite(a_) & np.isfinite(b_)
        return a_[ok], b_[ok], int(m.sum())

    def block(a, b, label):
        x, y, n_cells = per_date(a, b)
        if len(x) < 30:
            return {"n_dates": int(len(x)), "n_cells": n_cells, "skill": None, "ref": label}
        ci = INF.bootstrap_ci(lambda ix: None if y[ix].mean() == 0 else 1 - x[ix].mean() / y[ix].mean(),
                              len(x), n_boot=n_boot, mean_block=mb)
        dm = INF.dm_test(x, y, h=1, lag=lag)
        return {"n_dates": int(len(x)), "n_cells": n_cells, "mean": float(x.mean()),
                "ref_mean": float(y.mean()), "skill": ci["estimate"], "ci95": [ci["lo"], ci["hi"]],
                "dm_hln": dm.get("dm_hln"), "dm_p": dm.get("p_value"), "ref": label, "score": "crps",
                "unit_of_dependence": "grid date -- all cells of a date resample together (§2.8 applied "
                                      "to inference; n_cells is printed but is NOT the inferential n)"}

    refs = {"grid_climatology": clim, "no_change": noch, "random_analogs": rand, "frozen": frozen}
    summary = {
        "study": "GRID_STUDY_REGISTRATION.md Part III + Amendment 1 (2026-09-03)",
        "unit": "date",
        "estimand": "given the world state on date t, the distribution of the h-day return -- NOT the "
                    "event-triggered estimand; no number in data/walk_forward/** is re-judged (§0.2)",
        "run_id": run_id, "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "registered": {"blocks": BLOCKS, "k": K, "tau_grid": list(TAU_GRID), "w_step": W_STEP,
                       "burn_in": BURN_IN, "candidates": len(cands), "horizons": list(HORIZONS),
                       "targets": list(TARGETS), "seed": SEED, "n_boot": n_boot, "n_spa": n_spa,
                       "frozen": {"w": FROZEN_W.tolist(), "tau": FROZEN_TAU},
                       "grid": "month_end (Part III §3.1: primary because its design effect is 1.02)"},
        "panel": {"n_grid_dates": T, "first": dates[0], "last": dates[-1],
                  "n_scored_cells": int(np.isfinite(fitted).sum()),
                  "n_nominal_cells": int(np.isfinite(R).sum()),
                  "mean_block": round(mb, 2), "hac_lag": lag},
        "fitted_vs": {k: block(fitted, v, k) for k, v in refs.items()},
        "frozen_vs": {k: block(frozen, v, k) for k, v in refs.items() if k != "frozen"},
        "the_comparison": block(fitted, frozen, "frozen"),
    }

    summary["diagnostic_fair"] = {
        "what": "Ferro size-corrected CRPS (Amendment A.5 / E.3, inherited by §0.2 and required by §3.2). "
                "A k = 12 atom forecast is charged E|X-X'|/(2k) that a large climatology pool is not, so "
                "the correction can only RAISE the engine's measured standing against climatology. It is a "
                "diagnostic and it gates nothing: the registered CRPS decides.",
        "means": {"fitted": float(np.nanmean(diag_fit["crps"])), "fitted_fair": float(np.nanmean(diag_fit["crps_fair"])),
                  "frozen": float(np.nanmean(diag_frz["crps"])), "frozen_fair": float(np.nanmean(diag_frz["crps_fair"])),
                  "climatology": float(np.nanmean(diag_clim["crps"])), "climatology_fair": float(np.nanmean(diag_clim["crps_fair"]))},
        "fitted_vs_climatology_registered": block(diag_fit["crps"], diag_clim["crps"], "grid_climatology"),
        "fitted_vs_climatology_fair": block(diag_fit["crps_fair"], diag_clim["crps_fair"], "grid_climatology_fair"),
        "frozen_vs_climatology_fair": block(diag_frz["crps_fair"], diag_clim["crps_fair"], "grid_climatology_fair"),
    }
    pit = diag_fit["pit"][np.isfinite(diag_fit["pit"])]
    pit_c = diag_clim["pit"][np.isfinite(diag_clim["pit"])]
    summary["calibration"] = {
        "pinball": {k: float(np.nanmean(diag_fit[k])) for k in ("pin10", "pin50", "pin90")},
        "pit_hist_fitted": np.histogram(pit, bins=10, range=(0, 1))[0].tolist(),
        "pit_hist_climatology": np.histogram(pit_c, bins=10, range=(0, 1))[0].tolist(),
        "pit_n": int(len(pit)),
        "note": "a calibrated forecast has a flat PIT; §3 registers the histogram, not a test statistic",
    }

    # §3.2 inherits §6 unchanged, which includes the multiplicity guards. The first cut omitted them.
    fam = ["fitted", "frozen", "random_analogs", "no_change"]
    arrs = {"fitted": fitted, "frozen": frozen, "random_analogs": rand, "no_change": noch}
    base_d, _, _ = per_date(clim, clim)
    cols = []
    for nm in fam:
        a_, b_, _ = per_date(arrs[nm], clim)
        cols.append(b_ - a_)                      # benchmark minus model: positive means the model wins
    L = min(len(c) for c in cols)
    dmat = np.column_stack([c[:L] for c in cols])
    spa = INF.spa(dmat, n_boot=n_spa, mean_block=mb)
    spa["best_model"] = fam[spa["best_model"]]; spa["models"] = fam
    spa["benchmark"] = "grid_climatology"
    spa["note"] = ("§6 / Part III §3.2: with four models compared against one benchmark, the best of them is "
                   "tested against the null that NONE beats it. Computed on per-date differentials, the same "
                   "unit of dependence as every interval in this file.")
    summary["spa"] = spa

    # per target and per horizon, with H_eff attached wherever horizons are pooled (Part III §3.2)
    summary["per_target"] = {a: block(fitted[:, ai][:, None, :], clim[:, ai][:, None, :], "grid_climatology")
                             for ai, a in enumerate(TARGETS)}
    summary["per_horizon"] = {f"h{h}": block(fitted[:, :, hi][:, :, None], clim[:, :, hi][:, :, None], "grid_climatology")
                              for hi, h in enumerate(HORIZONS)}
    summary["pooling_disclosure"] = {
        "H_eff": 1.547, "H_eff_random_walk_benchmark": 1.550, "R_horizons": 0.137,
        "C_eff_joint": 4.255, "n_eff_joint": 1979.1,
        "rule": "Part III §3.2: five horizons are worth about one and a half, and this pairing is mandatory "
                "beside every pooled-horizon number. n_nominal is never reported as n_eff.",
    }
    # the fitted trajectory (§3.7.3: a fitted model whose weights swing is a different object)
    traj = [{"date": dates[t], "n_inner": int(n_inner[t]),
             "w": (cands[chosen[t]][0].tolist() if chosen[t] >= 0 else None),
             "tau": (cands[chosen[t]][1] if chosen[t] >= 0 else None)} for t in range(T)]
    picked = [tuple(x["w"]) + (x["tau"],) for x in traj if x["w"]]
    summary["training"] = {
        "fitted_parameters": 5, "required_effective_units": 100, "available_inner_effective": 989.5,
        "legitimate": True, "n_reads_with_a_fit": len(picked),
        "distinct_selections": len(set(picked)),
        "modal_selection": (max(set(picked), key=picked.count) if picked else None),
        "modal_share": (round(picked.count(max(set(picked), key=picked.count)) / len(picked), 3)
                        if picked else None),
        "blocks": BLOCK_NAMES,
        "note": "§3.7.3 registered that the weight trajectory is published: a fitted model whose weights "
                "swing across folds is a different object from one whose weights converge.",
    }
    # BH-FDR across every DM p-value this file reports (§6)
    fdr_names, fdr_p = [], []
    for grp in ("fitted_vs", "frozen_vs"):
        for k, v in summary.get(grp, {}).items():
            if v.get("dm_p") is not None:
                fdr_names.append(f"{grp}:{k}"); fdr_p.append(v["dm_p"])
    if summary["the_comparison"].get("dm_p") is not None:
        fdr_names.append("the_comparison:fitted_vs_frozen"); fdr_p.append(summary["the_comparison"]["dm_p"])
    for grp in ("per_target", "per_horizon"):
        for k, v in summary.get(grp, {}).items():
            if v.get("dm_p") is not None:
                fdr_names.append(f"{grp}:{k}"); fdr_p.append(v["dm_p"])
    if fdr_p:
        summary["fdr"] = {"names": fdr_names, "p": fdr_p, "bh": INF.bh_fdr(fdr_p, q=0.05),
                          "note": "§6: Benjamini-Hochberg across the family this file reports. A comparison "
                                  "that does not survive is not a finding."}
    (OUT_DIR / "training.json").write_text(json.dumps(traj, indent=1))
    # ---- Amendment 2: the SAME engine, analogs, baselines and inference on the abnormal-return target
    print("re-scoring the identical design on the abnormal-return target ...", flush=True)
    frozen_ar, _ = crps_all(D, AR, gi, cands[frozen_ci])
    fitted_ar = np.full_like(frozen_ar, np.nan)
    by_c = {}
    for t in range(T):
        ci_ = chosen[t]
        if ci_ < 0:
            continue
        if ci_ not in by_c:
            by_c[ci_], _ = crps_all(D, AR, gi, cands[ci_])
        fitted_ar[t] = by_c[ci_][t]
    clim_ar = np.full_like(frozen_ar, np.nan); noch_ar = np.full_like(frozen_ar, np.nan)
    rand_ar = np.full_like(frozen_ar, np.nan)
    for hi, h in enumerate(HORIZONS):
        m_ = eligible_mask(T, gi, h)
        c1, n1, r1 = baseline_scores(AR[:, :, [hi]], m_, gi)
        clim_ar[:, :, hi] = c1[:, :, 0]; noch_ar[:, :, hi] = n1[:, :, 0]; rand_ar[:, :, hi] = r1[:, :, 0]
    refs_ar = {"grid_climatology": clim_ar, "no_change": noch_ar, "random_analogs": rand_ar, "frozen": frozen_ar}
    summary["abnormal_return_target"] = {
        "amendment": "GRID_STUDY_REGISTRATION.md Part III Amendment 2 (2026-09-03), answering "
                     "docs/audit/01_TIER1_design_defects.md A1",
        "model": ar_diag, "estimation_window_td": EST_WINDOW, "gap_td": EST_GAP, "min_obs": EST_MIN,
        "n_cells_dropped_short_window": int(n_dropped),
        "n_scored_cells": int(np.isfinite(fitted_ar).sum()),
        "fitted_vs": {k: block(fitted_ar, v, k) for k, v in refs_ar.items()},
        "the_comparison": block(fitted_ar, frozen_ar, "frozen"),
        "per_target": {a: block(fitted_ar[:, ai][:, None, :], clim_ar[:, ai][:, None, :], "grid_climatology")
                       for ai, a in enumerate(TARGETS)},
        "note": "identical engine, analogs, baselines, cluster structure and inference; ONLY the target "
                "changed. Any movement is attributable to the target definition and to nothing else.",
    }
    # §6's multiplicity guards on the ABNORMAL arm too. Omitting them here while requiring them on the raw
    # arm would be exactly the double standard this project exists to prevent.
    fam_ar = ["fitted", "frozen", "random_analogs", "no_change"]
    arrs_ar = {"fitted": fitted_ar, "frozen": frozen_ar, "random_analogs": rand_ar, "no_change": noch_ar}
    cols_ar = []
    for nm in fam_ar:
        a_, b_, _ = per_date(arrs_ar[nm], clim_ar)
        cols_ar.append(b_ - a_)
    L_ar = min(len(c) for c in cols_ar)
    spa_ar = INF.spa(np.column_stack([c[:L_ar] for c in cols_ar]), n_boot=n_spa, mean_block=mb)
    spa_ar["best_model"] = fam_ar[spa_ar["best_model"]]; spa_ar["models"] = fam_ar
    spa_ar["benchmark"] = "grid_climatology_abnormal"
    summary["abnormal_return_target"]["spa"] = spa_ar
    nm_ar, p_ar = [], []
    for k, v in summary["abnormal_return_target"]["fitted_vs"].items():
        if v.get("dm_p") is not None:
            nm_ar.append(f"fitted_vs:{k}"); p_ar.append(v["dm_p"])
    for k, v in summary["abnormal_return_target"]["per_target"].items():
        if v.get("dm_p") is not None:
            nm_ar.append(f"per_target:{k}"); p_ar.append(v["dm_p"])
    if p_ar:
        summary["abnormal_return_target"]["fdr"] = {
            "names": nm_ar, "p": p_ar, "bh": INF.bh_fdr(p_ar, q=0.05),
            "note": "§6 BH-FDR across the abnormal arm's own family. A comparison that does not survive is "
                    "not a finding, on this arm exactly as on the raw one."}
    summary["determinism"] = {"content_digest": _hash([summary["registered"], dates,
                                                       np.nan_to_num(fitted, nan=-999).round(6).tolist()])}
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, indent=1, default=str))
    np.savez_compressed(OUT_DIR / "scores.npz", fitted=fitted, frozen=frozen, clim=clim,
                        noch=noch, rand=rand, chosen=chosen, fitted_ar=fitted_ar,
                        frozen_ar=frozen_ar, clim_ar=clim_ar, noch_ar=noch_ar, rand_ar=rand_ar)
    return summary


def main():
    s = run(fast="--fast" in sys.argv)
    print(json.dumps({k: s[k] for k in ("panel", "the_comparison", "fitted_vs", "frozen_vs", "training",
                                        "pooling_disclosure")}, indent=1, default=str))


if __name__ == "__main__":
    main()
