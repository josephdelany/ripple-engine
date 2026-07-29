"""
local_projections.py -- Tier-2 upgrade of H1: the ripple IRF + hierarchical pooling (Step 6).

The registered H1 is a single median-split number (+5pp). This is its Jordà-style local-projection
form: the ripple MAGNITUDE regressed on the continuous pre-event VIX-stress state, at each horizon,
so you see the impulse-response shape (h = 1,5,10,20 trading days) with bootstrap confidence bands
-- and, crucially, run BOTH raw and STANDARDIZED (each event's |CAR| divided by its own estimation-
window sigma), because the standardized version is the volatility-clustering defeater. If the VIX
coefficient survives standardization, the amplification is transmission, not just turbulent times.

Also: HIERARCHICAL (partial) POOLING across the 7 event types -- per-type amplification shrunk
toward the grand mean by sample size, so small-N types borrow strength instead of showing noisy
extremes.

This is a post-registration METHOD lens (like inference.py), not a new hypothesis or a changed
verdict. Clustered (de-overlapped) sample. numpy-only (OLS via lstsq, bootstrap CIs). Deterministic.

Run:  python3 src/local_projections.py
"""

import json
import sqlite3
from math import sqrt
from pathlib import Path

import numpy as np
import pandas as pd

from event_study import load_returns, car_for_event, PRE
from derive_signals import load_wide, build_signals
from robustness import assign_clusters
from inference import sigma_for_event

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "local_projections.json"

VIX = "derived.vix_pct"
HORIZONS = [1, 5, 10, 20]
N_BOOT = 5000
SEED = 19900802


def _frame(conn):
    ret = load_returns(conn)
    signals = build_signals(load_wide(conn))
    events = pd.read_sql("SELECT event_id, event_date, type FROM events ORDER BY event_date", conn)
    rows = []
    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["event_date"])
        if car is None:
            continue
        sigma = sigma_for_event(ret, ev["event_date"])
        cutoff = pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1)
        s = signals[VIX].dropna() if VIX in signals else pd.Series(dtype=float)
        vix = s.asof(cutoff) if len(s) else np.nan
        row = {"event_id": ev["event_id"], "date": ev["event_date"], "type": ev["type"],
               "vix": vix, "sigma": sigma}
        for h in HORIZONS:
            row[f"abs_car{h}"] = abs(car[PRE + h]) * 100.0                 # pp
            if sigma:
                row[f"std_car{h}"] = abs(car[PRE + h]) / (sigma * sqrt(PRE + h + 1))
        rows.append(row)
    df = assign_clusters(pd.DataFrame(rows))
    return df.groupby("cluster").first().reset_index()


def _ols_slope(x, y):
    """Slope of y ~ x (with intercept) via least squares."""
    X = np.column_stack([np.ones_like(x), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(beta[1])


def _slope_ci(x, y, n_boot=N_BOOT, seed=SEED):
    """Bootstrap 95% CI for the OLS slope by resampling (x,y) pairs."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    keep = np.isfinite(x) & np.isfinite(y)
    x, y = x[keep], y[keep]
    n = len(x)
    if n < 8:
        return None
    obs = _ols_slope(x, y)
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        if np.std(x[idx]) < 1e-9:
            continue
        boot.append(_ols_slope(x[idx], y[idx]))
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return {"slope": round(obs, 4), "lo": round(float(lo), 4), "hi": round(float(hi), 4),
            "n": n, "excludes_zero": bool(lo > 0 or hi < 0)}


def hierarchical_pool(df, col="abs_car20"):
    """Per-type amplification (high-VIX minus low-VIX mean |CAR20|), partial-pooled toward the
    grand mean by sample size: shrunk_t = w*a_t + (1-w)*grand, w = n_t/(n_t+k). Small-N types
    borrow strength instead of showing noisy extremes."""
    v = df[df["vix"].notna() & df[col].notna()]
    med = v["vix"].median()
    per, amps, ns = {}, [], []
    for t, g in v.groupby("type"):
        hi, lo = g[g["vix"] >= med][col], g[g["vix"] < med][col]
        if len(hi) and len(lo):
            a = float(hi.mean() - lo.mean())
            per[t] = {"n": int(len(g)), "raw_amp_pp": round(a, 2)}
            amps.append(a); ns.append(len(g))
    if not per:
        return {}
    grand = float(np.average(amps, weights=ns))
    k = float(np.median(ns))                          # shrinkage constant = median group size
    for t in per:
        n = per[t]["n"]; w = n / (n + k)
        per[t]["pooled_amp_pp"] = round(w * per[t]["raw_amp_pp"] + (1 - w) * grand, 2)
    return {"grand_mean_pp": round(grand, 2), "shrinkage_k": round(k, 1), "by_type": per}


def run():
    conn = sqlite3.connect(DB)
    df = _frame(conn)
    conn.close()
    vix = df["vix"].to_numpy(float)
    vixz = (vix - np.nanmean(vix)) / np.nanstd(vix)          # standardized stress (per 1 sd)

    irf = []
    for h in HORIZONS:
        raw = _slope_ci(vixz, df[f"abs_car{h}"].to_numpy(float))
        std = _slope_ci(vixz, df[f"std_car{h}"].to_numpy(float)) if f"std_car{h}" in df else None
        irf.append({"horizon": h, "raw_pp_per_sd": raw, "standardized_per_sd": std})

    h20 = next(x for x in irf if x["horizon"] == 20)
    raw_ok = bool(h20["raw_pp_per_sd"] and h20["raw_pp_per_sd"]["excludes_zero"]
                  and h20["raw_pp_per_sd"]["slope"] > 0)
    std_ok = bool(h20["standardized_per_sd"] and h20["standardized_per_sd"]["excludes_zero"]
                  and h20["standardized_per_sd"]["slope"] > 0)
    report = {
        "what": "Jordà-style local-projection IRF of ripple magnitude on VIX-stress state, per "
                "horizon, raw and standardized (vol-clustering defeater); + hierarchical pooling.",
        "sample": "clustered (de-overlapped)", "n": int(len(df)),
        "note": "Post-registration method lens; does not change the registered +5pp verdict.",
        "irf": irf,
        "pooling": hierarchical_pool(df),
        "h20_raw_amplifies_ci_excludes_zero": raw_ok,
        "h20_survives_standardization": std_ok,
        "verdict": (
            "H1 corroborated as an IRF: the VIX-stress coefficient on |CAR+20| is positive with a "
            "bootstrap CI excluding zero"
            + (", AND it survives standardization (transmission, not just volatility clustering)."
               if std_ok else
               ", BUT it weakens/loses significance once standardized -- at this N the standardized "
               "effect is suggestive, not conclusive (same caveat inference.py flagged for H1).")
            if raw_ok else
            "The continuous VIX-magnitude slope's CI does not clearly exclude zero at h=20 here."),
    }
    OUT.write_text(json.dumps(report, indent=2))
    return report


def main():
    r = run()
    print("=" * 78)
    print("LOCAL PROJECTIONS -- ripple magnitude IRF on VIX stress (clustered)")
    print("=" * 78)
    print(f"  n={r['n']} episodes.  slope = pp of |CAR| per +1 sd of VIX %ile")
    print(f"  {'h':>3}  {'raw slope [95% CI]':<28}{'standardized [95% CI]':<28}")
    for x in r["irf"]:
        rw, st = x["raw_pp_per_sd"], x["standardized_per_sd"]
        rs = f"{rw['slope']:+.2f} [{rw['lo']:+.2f},{rw['hi']:+.2f}]" if rw else "n/a"
        ss = f"{st['slope']:+.3f} [{st['lo']:+.3f},{st['hi']:+.3f}]" if st else "n/a"
        star = " *" if rw and rw["excludes_zero"] else ""
        print(f"  {x['horizon']:>3}  {rs:<28}{ss:<28}{star}")
    p = r.get("pooling", {})
    if p:
        print(f"\n  Hierarchical pooling (amp per type at +20, shrunk toward grand "
              f"{p['grand_mean_pp']}pp, k={p['shrinkage_k']}):")
        for t, s in sorted(p["by_type"].items(), key=lambda kv: -kv[1]["n"]):
            print(f"    {t:<24} n={s['n']:<3} raw {s['raw_amp_pp']:+.1f}pp -> "
                  f"pooled {s['pooled_amp_pp']:+.1f}pp")
    print(f"\n  {r['verdict']}")


if __name__ == "__main__":
    main()
