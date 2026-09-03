"""
power_arithmetic.py -- GRID_STUDY_REGISTRATION.md Part II (2026-09-03): the effective-n arithmetic,
computed under the method registered in commit 7afcb2c BEFORE this file existed.

The question this answers is NOT "does the grid design work". It is "how much does each of the four
multipliers actually buy, in units of power, before anything is built". Nothing here computes a forecast,
a score or a skill. It computes:

  §2.6  availability   -- how many rows each multiplier can actually supply, given what is loaded
  §2.2  DEFF_time      -- serial dependence, Bartlett closed form AND the registered block-bootstrap ratio
  §2.3  M_eff          -- effective number of independent targets, M^2 / sum_ij rho_ij
  §2.4  H_eff          -- effective number of independent horizons, with the random-walk benchmark
                          corr(r_h1, r_h2) = sqrt(min/max) computed in closed form beside it
  §2.5  dyad panel     -- two-way (dyad x date) clustering, against the coverage wall
  §2.8  the JOINT n_eff on the stacked matrix, with the product of separate factors published ONLY as
                          `naive_product` beside it -- a nominal multiplier is never a power multiplier
  §2.7  R_m and the pre-declared drop decision for each multiplier
  §2.9  the two threshold verdicts: is the study worth building, and is training legitimate

Proxy, and the direction of its error, both registered in §2.3 before the numbers: score differentials do
not exist until the study is built, so dependence is estimated on the h-horizon log returns (P) and on the
IES level panel (G). A score differential carries the forecast's own target-specific error on top of the
outcome, so rho_d <= rho_proxy is EXPECTED and the numbers here are therefore expected to be a FLOOR on
M_eff / H_eff. That is an argument, not a proof; the realised values are recomputed on the first run of the
study and published beside these, and these are never retro-fitted.

Run:  python3 src/engine/grid/power_arithmetic.py
"""
from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from engine import inference as INF       # noqa: E402
import walk as W                          # noqa: E402

DB = ROOT / "data" / "oil.db"
OUT_DIR = ROOT / "data" / "grid"
OUT = OUT_DIR / "power_arithmetic.json"

# --- the registered constants this study inherits (WALK_FORWARD_PROTOCOL.md; GRID_STUDY_REGISTRATION §0.2)
CLUSTER_DAYS = W.REGISTERED["cluster_days"]          # 35
N_BOOT = W.REGISTERED["n_boot"]                      # 2000
SEED = W.REGISTERED["seeds"]["bootstrap_and_spa"]    # 19900802
MIN_TIER_N = W.REGISTERED["min_tier_n"]              # 30

# --- this study's registered grid (§1.2) and multipliers
GRID_START = "1987-01-01"
HORIZONS = (5, 10, 20, 40, 60)                       # multiplier 3, trading days
TARGETS = {                                          # multiplier 2
    "brent": "fred.DCOILBRENTEU", "wti": "fred.DCOILWTICO",
    "diesel_crack": "derived.diesel_crack", "gasoline_crack": "derived.gasoline_crack",
    "henry_hub": "fred.DHHNGSP", "propane": "fred.DPROPANEMBTX",
}
MARKET_FIELDS = {                                    # the engine's market block (similarity.MARKET_SERIES)
    "vix_pct": "derived.vix_pct", "ovx_pct": "derived.ovx_pct", "brent_vol20": "derived.brent_vol20",
    "inv_sigma": "derived.inv_sigma", "cot_pct": "derived.cot_pct", "curve_2s10s": "derived.curve_2s10s",
    "usd_z": "derived.usd_z", "credit_stress": "derived.credit_stress", "real_rate": "derived.real_rate",
    "gpr": "gpr.GPRD", "conflict_intensity_pct": "derived.conflict_intensity_pct",
    "diesel_crack": "derived.diesel_crack", "brent_wti_spread_z": "derived.brent_wti_spread_z",
}
RELEASE_LAGS = {"cot_pct": 3, "inv_sigma": 5}        # Amendment G, calendar days
IES_WINDOW = 90                                      # calendar days, (t, t+90]
DROP_RATIO = 0.10                                    # §2.7
MARGINAL_RATIO = 0.33                                # §2.7
DEFF_TIEBREAK = 1.5                                  # §2.2
UNITS_PER_PARAMETER = 20                             # §2.9


# ================================================================ data

def load_series(conn, series_ids):
    q = f"""select series_id, obs_date, value from observations
            where series_id in ({','.join('?' * len(series_ids))}) and value is not null"""
    d = pd.read_sql(q, conn, params=list(series_ids))
    d["obs_date"] = pd.to_datetime(d["obs_date"])
    return {k: g.set_index("obs_date")["value"].sort_index() for k, g in d.groupby("series_id")}


def trading_calendar(series):
    """The daily tier's trading days: the union of the two crude spot series' observation dates."""
    idx = series["fred.DCOILBRENTEU"].index.union(series["fred.DCOILWTICO"].index)
    return pd.DatetimeIndex(sorted(idx[idx >= pd.Timestamp(GRID_START)]))


def grid_dates(cal, kind):
    """§1.2: the last trading day of each month / of each week. Not filtered by whether anything happened."""
    key = cal.to_period("M") if kind == "month_end" else cal.to_period("W")
    return pd.DatetimeIndex(pd.Series(cal, index=key).groupby(level=0).last().values)


# ================================================================ §2.2 design effects

def bartlett_deff(x, lag):
    """DEFF = 1 + 2 * sum_{k=1..L} (1 - k/(L+1)) * rho_k   (Newey-West / Bartlett kernel)."""
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 5 or lag < 1:
        return 1.0
    x = x - x.mean()
    v0 = float(x @ x) / n
    if v0 <= 0:
        return 1.0
    s = 1.0
    for k in range(1, min(lag, n - 2) + 1):
        rk = float(x[k:] @ x[:-k]) / (n * v0)
        s += 2.0 * (1.0 - k / (lag + 1.0)) * rk
    return float(max(s, 1e-6))


def bootstrap_deff(x, mean_block, n_boot=N_BOOT, seed=SEED):
    """The REGISTERED estimator: var of the mean under the stationary block bootstrap (Politis-Romano, the
    tier's measured mean block) divided by its var under an i.i.d. bootstrap at the same n and seed."""
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 5:
        return 1.0
    rng_b = np.random.default_rng(seed)
    rng_i = np.random.default_rng(seed)
    blk = np.array([x[INF.stationary_bootstrap(n, mean_block, rng_b)].mean() for _ in range(n_boot)])
    iid = np.array([x[rng_i.integers(0, n, n)].mean() for _ in range(n_boot)])
    vi = float(iid.var())
    return float(blk.var() / vi) if vi > 0 else 1.0


def deff_block(x, mean_block, lag, label):
    """§2.2's two estimators with the registered tie-break: disagree by > 1.5x -> publish both, use the larger."""
    b = bartlett_deff(x, lag)
    s = bootstrap_deff(x, mean_block)
    ratio = max(b, s) / max(min(b, s), 1e-9)
    used = max(b, s) if ratio > DEFF_TIEBREAK else s
    return {"series": label, "n": int(np.sum(~np.isnan(np.asarray(x, float)))),
            "deff_bartlett": round(b, 4), "deff_bootstrap_ratio": round(s, 4),
            "disagreement": round(ratio, 3), "tiebreak_fired": bool(ratio > DEFF_TIEBREAK),
            "deff_used": round(float(used), 4),
            "rule": "§2.2: both published; if they differ by more than 1.5x the LARGER is used everywhere"}


def rw_overlap_deff(spacing_td, h, lag):
    """Diagnostic benchmark, the analogue of §2.4's registered random-walk benchmark on the time axis: for
    h-day returns sampled every `spacing` trading days, a random walk gives rho_k = max(0, 1 - k*s/h)."""
    rho = [max(0.0, 1.0 - k * spacing_td / h) for k in range(1, lag + 1)]
    return float(1.0 + 2.0 * sum((1.0 - k / (lag + 1.0)) * r for k, r in enumerate(rho, 1)))


# ================================================================ §2.3 / §2.4 cross-sectional effective width

def eff_width(corr):
    """M_eff = M^2 / sum_ij rho_ij -- the effective number of independent columns."""
    c = np.asarray(corr, float)
    m = c.shape[0]
    s = float(np.nansum(c))
    return float(m * m / s) if s > 0 else float(m)


def rw_horizon_corr(hs):
    """§2.4 REGISTERED benchmark: under a random walk, corr(r_{t,h1}, r_{t,h2}) = sqrt(min/max)."""
    return np.array([[np.sqrt(min(a, b) / max(a, b)) for b in hs] for a in hs])


# ================================================================ §2.6 availability

def horizon_returns(series, cal, grid, target_ids, horizons):
    """r_{t,h} = log(P_{t+h td} / P_t) on the grid, per target and horizon. NaN where either end is missing."""
    pos = pd.Series(np.arange(len(cal)), index=cal)
    out = {}
    for name, sid in target_ids.items():
        s = series.get(sid)
        if s is None:
            continue
        on_cal = s.reindex(cal)                       # no fill: a missing print is missing, not carried
        for h in horizons:
            gi = pos.reindex(grid).to_numpy()
            ok = (gi + h) < len(cal)
            v0 = np.full(len(grid), np.nan); v1 = np.full(len(grid), np.nan)
            v0[ok] = on_cal.to_numpy()[gi[ok].astype(int)]
            v1[ok] = on_cal.to_numpy()[(gi[ok] + h).astype(int)]
            with np.errstate(divide="ignore", invalid="ignore"):
                out[(name, h)] = pd.Series(np.log(v1 / v0), index=grid)
    return out


def market_knowability(series, grid):
    """§1.2 / Amendment G: how many of the market block's fields have an observation dated < t - lag(field)."""
    cnt = np.zeros(len(grid), int)
    per_field = {}
    g = grid.to_numpy()
    for f, sid in MARKET_FIELDS.items():
        s = series.get(sid)
        if s is None:
            per_field[f] = 0
            continue
        cut = g - np.timedelta64(RELEASE_LAGS.get(f, 0), "D")
        idx = np.searchsorted(s.index.to_numpy(), cut, side="left")     # obs strictly before the cutoff
        has = idx > 0
        cnt += has.astype(int)
        per_field[f] = int(has.sum())
    return cnt, per_field


# ================================================================ §2.5 the dyad-date escalation panel

def load_dyad_spells():
    """Dispute / crisis spells with a dyad and dated endpoints, from the files in the tree. PROVISIONAL, and
    said so: the study's panel is built by src/state/ies90.py under its registered rules (dyadic precedence,
    littoral map, source tie order). This reconstruction exists only to measure the DEPENDENCE STRUCTURE and
    the coverage of a dyad-date panel, which are properties of the spells, not of the tie-breaking."""
    raw = ROOT / "data" / "state" / "raw"
    spells = []
    mid = pd.read_csv(raw / "cow_mid" / "dyadic_mid_4.03.csv", low_memory=False)
    hostlev = {1: 0, 2: 1, 3: 1, 4: 2, 5: 3}          # ies90.HOSTLEV_TO_LEVEL
    for r in mid.itertuples():
        try:
            lo = pd.Timestamp(year=int(r.strtyr), month=max(int(r.strtmnth), 1), day=max(int(r.strtday), 1))
            hi = pd.Timestamp(year=int(r.endyear), month=max(int(r.endmnth), 1), day=max(int(r.endday), 1))
        except (ValueError, TypeError):
            continue
        if pd.isna(lo) or pd.isna(hi) or hi < lo:
            continue
        a, b = sorted((int(r.statea), int(r.stateb)))
        spells.append((f"{a}-{b}", lo, hi, hostlev.get(int(r.hihost), 0), "mid"))
    icb = pd.read_csv(raw / "icb" / "icb_dyads_v16.csv", low_memory=False)
    for r in icb.itertuples():
        y = getattr(r, "year", None)
        if y is None or pd.isna(y):
            continue
        a, b = sorted((int(r.statea), int(r.stateb)))
        lo = pd.Timestamp(year=int(y), month=1, day=1); hi = pd.Timestamp(year=int(y), month=12, day=31)
        spells.append((f"{a}-{b}", lo, hi, 2, "icb"))   # ICB dyad file is year-resolution: level held at 2
    return pd.DataFrame(spells, columns=["dyad", "lo", "hi", "level", "src"])


def dyad_panel(spells, grid, cover_end):
    """Level per (dyad, grid date) over (t, t+90]: the max level of any spell of that dyad intersecting the
    window. A grid date after the source's coverage end is NOT covered and is NaN, never 0."""
    dyads = sorted(spells.dyad.unique())
    di = {d: i for i, d in enumerate(dyads)}
    T, D = len(grid), len(dyads)
    lvl = np.zeros((T, D))
    g0 = grid.to_numpy()
    g1 = g0 + np.timedelta64(IES_WINDOW, "D")
    for r in spells.itertuples():
        j = di[r.dyad]
        hit = (np.datetime64(r.lo) <= g1) & (np.datetime64(r.hi) > g0)
        if hit.any():
            lvl[hit, j] = np.maximum(lvl[hit, j], r.level)
    covered = np.asarray((grid + pd.Timedelta(days=IES_WINDOW)) <= pd.Timestamp(cover_end), bool)
    lvl[~covered, :] = np.nan
    return lvl, dyads, covered


def two_way_cluster_deff(X, covered):
    """§2.5: DEFF from a two-way cluster on dyad and on date (Cameron-Gelbach-Miller), relative to i.i.d.

    Var(mean) under two-way clustering = [ sum over date-clusters + sum over dyad-clusters
    - sum over (date,dyad) cells ] of the products of centred residuals, divided by N^2."""
    Z = X[covered]
    if Z.size == 0:
        return None
    m = np.nanmean(Z)
    R = Z - m
    ok = ~np.isnan(R)
    R = np.where(ok, R, 0.0)
    N = int(ok.sum())
    if N < 10:
        return None
    v_iid = float((R ** 2).sum()) / (N ** 2)
    v_date = float((R.sum(axis=1) ** 2).sum()) / (N ** 2)
    v_dyad = float((R.sum(axis=0) ** 2).sum()) / (N ** 2)
    v_cell = float((R ** 2).sum()) / (N ** 2)
    v_two = v_date + v_dyad - v_cell
    return {"n_cells": N, "var_iid": v_iid, "var_two_way": v_two,
            "deff_two_way": round(float(v_two / v_iid), 4) if v_iid > 0 else None,
            "rule": "Cameron-Gelbach-Miller two-way cluster on (date, dyad), relative to i.i.d."}



SEALED_DIFF = {}          # task -> (differential series, reference mean), the measured input to §2.9


def event_triggered_effective_n():
    """A like-for-like baseline. Comparing a grid n_eff against an event-triggered NOMINAL count would
    flatter the grid; this computes the published run's own effective n on the same definition, from the
    sealed score differentials (engine minus climatology Brier for G, CRPS for P)."""
    wf = ROOT / "data" / "walk_forward"
    summary = json.loads((wf / "summary.json").read_text())
    rid = summary["run_id"]
    rows = [json.loads(l) for l in (wf / "scores.jsonl").open() if l.strip()]
    rows = [r for r in rows if r["run_id"] == rid and r["tier"] == "daily" and r.get("burn_in_ok")]
    rows.sort(key=lambda r: (r["date"], r["event_id"]))
    out = {}
    for task, key in (("G", "brier"), ("P", "crps")):
        d, dates = [], []
        for r in rows:
            e = (r["scores"].get("engine") or {}).get(task)
            c = (r["scores"].get("climatology") or {}).get(task)
            if e and c and e.get(key) is not None and c.get(key) is not None:
                d.append(e[key] - c[key]); dates.append(r["date"])
        if len(d) < 30:
            continue
        mb = W._mean_block(dates, CLUSTER_DAYS); lag = max(int(round(mb)) - 1, 0)
        blk = deff_block(np.array(d), mb, lag, f"event_triggered|{task}")
        ref = float(np.mean([(r["scores"]["climatology"] or {})[task][key] for r in rows
                             if (r["scores"].get("climatology") or {}).get(task)
                             and (r["scores"]["climatology"][task] or {}).get(key) is not None]))
        SEALED_DIFF[task] = (np.array(d, float), ref)
        out[task] = {"n_nominal": len(d), "mean_block": round(mb, 2), "hac_lag": lag,
                     **blk, "n_eff": round(len(d) / blk["deff_used"], 1),
                     "reference_mean": round(ref, 5), "sd_diff": round(float(np.std(d, ddof=1)), 5),
                     "sd_over_ref": round(float(np.std(d, ddof=1)) / ref, 4)}
    out["note"] = ("computed on the SEALED differentials of run " + rid + " by the same estimator as the "
                   "grid panels, so the comparison is like for like and not nominal against effective")
    return out


# ================================================================ the report

def compute():
    conn = sqlite3.connect(DB)
    need = list(TARGETS.values()) + list(MARKET_FIELDS.values())
    series = load_series(conn, sorted(set(need)))
    cal = trading_calendar(series)
    out = {
        "registration": "GRID_STUDY_REGISTRATION.md Part II (2026-09-03), registered in commit 7afcb2c "
                        "before this module existed",
        "what_this_is_not": "no forecast, no score, no skill is computed here; this is the pre-build "
                            "arithmetic of how much each multiplier buys in units of power",
        "computed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "registered": {"cluster_days": CLUSTER_DAYS, "n_boot": N_BOOT, "seed": SEED,
                       "min_tier_n": MIN_TIER_N, "horizons": list(HORIZONS),
                       "targets": TARGETS, "drop_ratio": DROP_RATIO, "marginal_ratio": MARGINAL_RATIO,
                       "deff_tiebreak": DEFF_TIEBREAK, "units_per_parameter": UNITS_PER_PARAMETER},
        "calendar": {"trading_days": len(cal), "first": str(cal[0].date()), "last": str(cal[-1].date())},
        "grids": {}, "price_panel": {}, "escalation_panel": {}, "multipliers": {}, "verdicts": {},
    }

    for kind in ("month_end", "week_end"):
        grid = grid_dates(cal, kind)
        spacing = float(np.mean(np.diff(pd.Series(np.arange(len(cal)), index=cal).reindex(grid).to_numpy())))
        out["grids"][kind] = {"n_dates": len(grid), "first": str(grid[0].date()), "last": str(grid[-1].date()),
                              "mean_spacing_trading_days": round(spacing, 2)}

    # ---------------------------------------------------------------- the price panel, on both grids
    for kind in ("month_end", "week_end"):
        grid = grid_dates(cal, kind)
        spacing = float(np.mean(np.diff(pd.Series(np.arange(len(cal)), index=cal).reindex(grid).to_numpy())))
        R = horizon_returns(series, cal, grid, TARGETS, HORIZONS)
        cnt, per_field = market_knowability(series, grid)
        mb = W._mean_block([str(d.date()) for d in grid], CLUSTER_DAYS)
        lag = max(int(round(mb)) - 1, 0)

        avail = {f"{a}|h{h}": int(np.sum(~np.isnan(v.to_numpy()))) for (a, h), v in R.items()}
        # §2.2 per cell, and the random-walk overlap benchmark beside it
        per_cell = {}
        for (a, h), v in R.items():
            x = v.to_numpy()
            if np.sum(~np.isnan(x)) < 30:
                continue
            d = deff_block(x, mb, lag, f"{a}|h{h}")
            d["benchmark_random_walk_overlap"] = round(rw_overlap_deff(spacing, h, lag), 4)
            per_cell[f"{a}|h{h}"] = d

        cols = [(a, h) for a in TARGETS for h in HORIZONS if (a, h) in R]
        X = pd.DataFrame({f"{a}|h{h}": R[(a, h)] for a, h in cols})
        corr = X.corr(min_periods=60)
        C = corr.shape[0]
        c_eff = eff_width(corr.to_numpy())

        # targets alone (averaged over horizons) and horizons alone (averaged over targets), for naive_product
        m_effs, h_effs = [], []
        for h in HORIZONS:
            sub = corr.loc[[f"{a}|h{h}" for a in TARGETS if f"{a}|h{h}" in corr.index],
                           [f"{a}|h{h}" for a in TARGETS if f"{a}|h{h}" in corr.index]]
            if len(sub) > 1:
                m_effs.append(eff_width(sub.to_numpy()))
        for a in TARGETS:
            sub = corr.loc[[f"{a}|h{h}" for h in HORIZONS if f"{a}|h{h}" in corr.index],
                           [f"{a}|h{h}" for h in HORIZONS if f"{a}|h{h}" in corr.index]]
            if len(sub) > 1:
                h_effs.append(eff_width(sub.to_numpy()))
        m_eff = float(np.mean(m_effs)) if m_effs else 1.0
        h_eff = float(np.mean(h_effs)) if h_effs else 1.0
        h_eff_rw = eff_width(rw_horizon_corr(HORIZONS))

        # §2.8 the JOINT number, on the stacked matrix: row mean over cells, then the time design effect
        y = np.nanmean(X.to_numpy(), axis=1)
        t_ok = int(np.sum(~np.isnan(y)))
        d_time = deff_block(y, mb, lag, f"{kind}|stacked_row_mean")
        d_time["benchmark_random_walk_overlap_h20"] = round(rw_overlap_deff(spacing, 20, lag), 4)
        t_eff = t_ok / d_time["deff_used"]
        n_nom = int(sum(avail.values()))
        n_eff_joint = t_eff * c_eff
        naive = t_eff * m_eff * h_eff

        out["price_panel"][kind] = {
            "n_grid_dates": len(grid), "mean_spacing_trading_days": round(spacing, 2),
            "market_block_knowable": {
                "fields": len(MARKET_FIELDS),
                "dates_with_ge_k_fields": {str(k): int(np.sum(cnt >= k)) for k in (1, 5, 8, 10, 13)},
                "per_field_dates": per_field,
                "note": "Amendment G's release lags applied; an observation dated d is visible at t only "
                        "if d + lag < t. No minimum field count is imposed here -- none is registered.",
            },
            "availability": avail, "n_nominal_cells": n_nom,
            "deff_per_cell": per_cell,
            "cross_section": {"n_columns": C, "C_eff_joint": round(c_eff, 3),
                              "M_eff_targets_mean_over_horizons": round(m_eff, 3),
                              "H_eff_horizons_mean_over_targets": round(h_eff, 3),
                              "H_eff_random_walk_benchmark": round(h_eff_rw, 3),
                              "note": "M_eff = M^2 / sum_ij rho_ij on h-horizon log returns (§2.3's "
                                      "registered proxy; expected to be a FLOOR on the score-differential "
                                      "value). The random-walk benchmark is corr = sqrt(min/max) (§2.4)."},
            "time": {"n_grid_dates_scored": t_ok, "mean_block": round(mb, 2), "hac_lag": lag, **d_time,
                     "T_eff": round(t_eff, 2)},
            "joint": {"n_nominal": n_nom, "n_eff": round(n_eff_joint, 1),
                      "realisation_ratio": round(n_eff_joint / n_nom, 4) if n_nom else None,
                      "naive_product": round(naive, 1),
                      "naive_over_joint": round(naive / n_eff_joint, 3) if n_eff_joint else None,
                      "rule": "§2.8: n_eff computed on the stacked matrix as T_eff x C_eff. naive_product "
                              "= T_eff x M_eff x H_eff is a DIAGNOSTIC ONLY -- a nominal multiplier is "
                              "never reported as a power multiplier."},
            "correlations": {"brent_wti_h20": round(float(corr.loc["brent|h20", "wti|h20"]), 4)
                             if "brent|h20" in corr.index and "wti|h20" in corr.index else None,
                             "mean_offdiag": round(float((corr.to_numpy().sum() - C) / (C * C - C)), 4)},
        }

    # ---------------------------------------------------------------- the escalation panel (§2.5)
    spells = load_dyad_spells()
    for kind in ("month_end", "week_end"):
        grid = grid_dates(cal, kind)
        mb = W._mean_block([str(d.date()) for d in grid], CLUSTER_DAYS)
        lag = max(int(round(mb)) - 1, 0)
        blocks = {}
        # Three variants. The third is added on session G's probe (data/grid/PROBE.md, commit b31a24e),
        # which established -- against ies90.py's own rules, not by inference -- that MID, MIDI and COW War
        # are the ONLY sources recording which SIDE a state was on, that they stop covering the grid at
        # 2014-10-02, and that after that every non-zero dyad-date cell is an artefact: ICB records crisis
        # ACTORS not sides, so on a mechanically-supplied pair allies read as adversaries (GBR|USA at IES 3
        # from one Syria crisis), and GED is a location death count replicated across every dyad containing
        # that country. `sided_only_2014` is therefore the only variant whose non-zero mass rests on evidence
        # that the two states were on opposite sides.
        for wall_name, wall, srcs in (("mid_family_2014", "2014-12-31", None),
                                      ("icb_2021", "2021-12-31", None),
                                      ("sided_only_2014", "2014-10-02", ("mid",))):
            sp = spells if srcs is None else spells[spells.src.isin(srcs)]
            lvl, dyads, covered = dyad_panel(sp, grid, wall)
            n_cells = int(covered.sum() * len(dyads))
            varying = [j for j in range(len(dyads)) if np.nanstd(lvl[covered, j]) > 0]
            Xv = lvl[np.ix_(covered, varying)] if varying else np.zeros((int(covered.sum()), 0))
            corr = pd.DataFrame(Xv).corr(min_periods=30).to_numpy() if Xv.shape[1] > 1 else np.ones((1, 1))
            d_eff = eff_width(np.nan_to_num(corr, nan=0.0)) if Xv.shape[1] > 1 else float(Xv.shape[1])
            y = np.nanmean(Xv, axis=1) if Xv.shape[1] else np.zeros(int(covered.sum()))
            d_time = deff_block(y, mb, lag, f"{kind}|{wall_name}|dyad_row_mean")
            t_eff = int(covered.sum()) / d_time["deff_used"]
            tw = two_way_cluster_deff(lvl, covered)
            # §2.5's tie-break, applied and not merely reported: the T_eff x D_eff construction implies a
            # design effect of n_cells / (T_eff x D_eff); the two-way cluster gives another. If they differ
            # by more than 1.5x, both are published and the LARGER is used -- which lowers n_eff.
            deff_sep = n_cells / max(t_eff * d_eff, 1e-9)
            deff_two = (tw or {}).get("deff_two_way")
            fired = bool(deff_two and max(deff_sep, deff_two) / max(min(deff_sep, deff_two), 1e-9) > DEFF_TIEBREAK)
            deff_used = max(deff_sep, deff_two) if fired else deff_sep
            n_eff = n_cells / deff_used if deff_used else 0.0
            marg = {str(int(k)): int(v) for k, v in
                    zip(*np.unique(lvl[covered][~np.isnan(lvl[covered])], return_counts=True))}
            n_obs = sum(marg.values()) or 1
            blocks[wall_name] = {
                "coverage_end": wall, "n_grid_dates_covered": int(covered.sum()),
                "n_dyads": len(dyads), "n_dyads_with_any_variation": len(varying),
                "n_nominal_cells": n_cells,
                "level_marginal": marg,
                "share_level_0": round(marg.get("0", 0) / n_obs, 5),
                "informative_cells": n_obs - marg.get("0", 0),
                "informative_share_warning":
                    "the level panel is " + str(round(100 * marg.get("0", 0) / n_obs, 2)) + " % zeros. A "
                    "forecaster and its climatology both get those cells right, so they carry no power to "
                    "DISCRIMINATE between them. §2.3 registers that the direction of the proxy's error must "
                    "be stated in advance: for the price panel the return proxy is expected to FLOOR M_eff; "
                    "for this panel the level proxy is an UPPER BOUND on discriminating information, and the "
                    "n_eff below should be read as a ceiling, not an estimate.",
                "D_eff": round(float(d_eff), 3), "time": {**d_time, "T_eff": round(t_eff, 2)},
                "two_way_cluster": tw,
                "deff_separable_TxD": round(float(deff_sep), 3),
                "deff_two_way": deff_two, "tiebreak_fired": fired, "deff_used": round(float(deff_used), 3),
                "n_eff": round(float(n_eff), 1),
                "n_eff_separable_TxD_before_tiebreak": round(float(t_eff * d_eff), 1),
                "realisation_ratio": round(float(n_eff) / n_cells, 5) if n_cells else None,
                "sources": list(srcs) if srcs else "mid+icb",
                "sided_evidence": bool(srcs),
                "cross_session": ("session G's probe (data/grid/PROBE.md, commit b31a24e) found that after "
                                  "2014 every non-zero dyad-date cell is an artefact -- ICB records crisis "
                                  "ACTORS not sides, so allies read as adversaries on a mechanically supplied "
                                  "pair, and GED is a location count replicated across every dyad containing "
                                  "that country. Only the sided_only_2014 variant is free of that. The other "
                                  "two are retained as published, and are contaminated."),
                "note": "the panel is PROVISIONAL: reconstructed from MID and ICB dyad spells to measure "
                        "dependence and coverage. The study's labels are built by src/state/ies90.py under "
                        "its registered rules. A grid date whose window extends past the source's coverage "
                        "end is NOT covered and is NaN, never 0.",
            }
        out["escalation_panel"][kind] = blocks

    out["event_triggered_baseline"] = event_triggered_effective_n()
    out["sources"] = {
        "dyadic_mid_4.03_rows": int(len(pd.read_csv(ROOT / "data/state/raw/cow_mid/dyadic_mid_4.03.csv",
                                                    low_memory=False))),
        "icb_dyads_v16_rows": int(len(pd.read_csv(ROOT / "data/state/raw/icb/icb_dyads_v16.csv",
                                                  low_memory=False, encoding="latin-1"))),
        "spells_used": int(len(spells)), "dyads_in_spells": int(spells.dyad.nunique()),
        "brief_claimed_mid_rows": 59076,
        "note": "GRID_STUDY_REGISTRATION §2.5: the brief's 59,076 figure does not match the file in the "
                "tree. The registration uses the real count and states the discrepancy.",
    }
    return out


def decide(out):
    """§2.7's drop rule and §2.9's two thresholds, applied mechanically to the computed numbers."""
    eb = out.get("event_triggered_baseline", {})
    event_n = {"G": (eb.get("G") or {}).get("n_eff", 150), "P": (eb.get("P") or {}).get("n_eff", 253)}
    dec = {}
    for kind in ("month_end", "week_end"):
        p = out["price_panel"][kind]
        g = out["escalation_panel"][kind]["mid_family_2014"]
        g21 = out["escalation_panel"][kind]["icb_2021"]
        rows = {}
        # multiplier 1 (grid): one target, one horizon, against the event-triggered P baseline
        base = p["deff_per_cell"].get("brent|h20")
        m1_eff = p["time"]["n_grid_dates_scored"] / base["deff_used"] if base else None
        rows["1_grid"] = {"n_nominal": p["n_grid_dates"], "n_eff": round(m1_eff, 1) if m1_eff else None,
                          "R": round(m1_eff / p["n_grid_dates"], 4) if m1_eff else None,
                          "vs_event_triggered_P_effective": event_n["P"],
                          "delta_n_eff_vs_event": round(m1_eff - event_n["P"], 1) if m1_eff else None}
        # multiplier 2 (targets): the joint C_eff against the horizons-only width
        c = p["cross_section"]
        m2_nom = len(TARGETS) - 1
        m2_eff = c["M_eff_targets_mean_over_horizons"] - 1.0
        rows["2_targets"] = {"n_nominal_added_per_cell": m2_nom, "n_eff_added_per_cell": round(m2_eff, 3),
                             "R": round(m2_eff / m2_nom, 4),
                             "delta_n_eff": round(m1_eff * m2_eff, 1) if m1_eff else None}
        m3_nom = len(HORIZONS) - 1
        m3_eff = c["H_eff_horizons_mean_over_targets"] - 1.0
        rows["3_horizons"] = {"n_nominal_added_per_cell": m3_nom, "n_eff_added_per_cell": round(m3_eff, 3),
                              "R": round(m3_eff / m3_nom, 4),
                              "random_walk_benchmark_H_eff": c["H_eff_random_walk_benchmark"],
                              "delta_n_eff": round(m1_eff * m3_eff, 1) if m1_eff else None}
        rows["4_dyad_date"] = {"n_nominal": g["n_nominal_cells"], "n_eff": g["n_eff"],
                               "R": g["realisation_ratio"],
                               "vs_event_triggered_G_effective": event_n["G"],
                               "delta_n_eff_vs_event": round(g["n_eff"] - event_n["G"], 1),
                               "coverage_2021_variant": {"n_eff": g21["n_eff"], "R": g21["realisation_ratio"]}}
        for k, r in rows.items():
            R = r.get("R")
            add = r.get("delta_n_eff", r.get("delta_n_eff_vs_event"))
            if R is None or add is None:
                r["decision"] = "UNDECIDED -- not computable"; continue
            if add < MIN_TIER_N:
                r["decision"] = f"DROP -- adds {add} effective units, below the registered min_tier_n {MIN_TIER_N}"
            elif R < DROP_RATIO:
                r["decision"] = f"DROP -- realisation ratio {R} below the registered {DROP_RATIO}"
            elif R < MARGINAL_RATIO:
                r["decision"] = f"KEEP, REPORTED AS MARGINAL -- realisation ratio {R}"
            else:
                r["decision"] = f"KEEP -- realisation ratio {R}"
        dec[kind] = rows
    return dec


def thresholds(out):
    """§2.9: is the study worth building, and is training legitimate, at the computed joint n_eff."""
    res = {}
    for kind in ("month_end", "week_end"):
        p = out["price_panel"][kind]; g = out["escalation_panel"][kind]["mid_family_2014"]
        n_p = int(round(p["joint"]["n_eff"])); n_g = int(round(g["n_eff"]))
        # §2.9: the protocol's own power estimator, fed the MEASURED noise-to-reference ratio of the sealed
        # run rather than an invented one -- MDS in skill units is 2.8 * sd(d) / (sqrt(n) * ref_mean), so the
        # ratio sd(d)/ref_mean is the whole input and it is a fact about this engine, not an assumption.
        # Dependence is already folded into n_eff, so the series is passed as i.i.d. at that n.
        eb = out.get("event_triggered_baseline", {})
        mds = {}
        for task, n_here in (("P", n_p), ("G", n_g)):
            sealed = SEALED_DIFF.get(task)
            if sealed is None:
                mds[task] = None; continue
            d, ref = sealed
            pw = INF.power_block(d, 1.0, 0, ref_mean=ref, n_list=[max(n_here, 5)],
                                 target_skill=0.05, n_sims=300)
            mds[task] = pw["by_n"][str(max(n_here, 5))]["mds_skill"]
        mds_p, mds_g = mds.get("P"), mds.get("G")
        build = (mds_p is not None and mds_p <= 0.05) or (mds_g is not None and mds_g <= 0.05)
        n_par = 6            # 5 block weights + 1 metric scale, the parameter count Part III will fit
        need = UNITS_PER_PARAMETER * n_par
        inner = min(n_p, n_g) * 0.5      # an inner training set is at most half an outer fold's history
        res[kind] = {
            "n_eff_price": n_p, "mds_skill_price_at_n_eff": mds_p,
            "n_eff_escalation": n_g, "mds_skill_escalation_at_n_eff": mds_g,
            "power_input": {t: {"sd_over_ref": round(float(np.std(SEALED_DIFF[t][0], ddof=1) / SEALED_DIFF[t][1]), 4),
                                "reference_mean": round(SEALED_DIFF[t][1], 5)}
                            for t in SEALED_DIFF},
            "escalation_panel_is_dropped_by_2_7":
                out["multipliers"][kind]["4_dyad_date"]["decision"].startswith("DROP")
                if out.get("multipliers") else None,
            "build_the_study": bool(build),
            "build_rule": "§2.9: built iff the registered power estimator detects Brier skill +0.05 at 80 % "
                          "power for at least one panel at the computed joint n_eff",
            "training": {"fitted_parameters": n_par, "effective_units_required": need,
                         "effective_units_available_inner": round(inner, 1),
                         "legitimate": bool(inner >= need),
                         "rule": f"§2.9: the fit runs only if each inner training set carries >= "
                                 f"{UNITS_PER_PARAMETER} effective units per fitted parameter; otherwise the "
                                 f"fit is NOT run, the frozen registered-weight engine stands, and that is "
                                 f"published as a result about the design"},
        }
    return res


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = compute()
    out["multipliers"] = decide(out)
    out["verdicts"] = thresholds(out)
    OUT.write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({"grids": out["grids"], "sources": out["sources"],
                      "multipliers": out["multipliers"], "verdicts": out["verdicts"]}, indent=1))


if __name__ == "__main__":
    main()
