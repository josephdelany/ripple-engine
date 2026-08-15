"""
sar_lens.py -- R1: the STANDARDIZED headline (Boehmer-Musumeci-Poulsen 1991).

WHY THIS EXISTS (red-team attack #1, CONCEDED)
----------------------------------------------
The headline H1 amplification was computed on |CAR| -- the raw cumulative abnormal
return magnitude, from a constant-mean model. |CAR| is a *volatility* quantity: a
20-day move is bigger, in absolute terms, whenever the market is more volatile.
VIX *is* a volatility index. So splitting |CAR| by VIX and finding the high-VIX
side bigger can be almost mechanical -- "high vol periods have bigger moves in
everything" -- rather than evidence that shocks genuinely ripple *harder*.

The field's standard fix (BMP 1991) is to STANDARDIZE each event's abnormal return
by *its own* estimation-window volatility before comparing. A big move in a
high-vol regime gets divided by that regime's big sigma, so it no longer counts as
"large" just because the backdrop was noisy. If the amplification survives on the
standardized number (SCAR), it is a real amplification. If it collapses, the
original headline was vol-clustering -- and we say so.

WHAT IT COMPUTES
----------------
For each Brent event that clears the same window guards as the frozen study:
  CAR_i     = constant-mean cumulative abnormal return at t+HORIZON (event_study)
  sigma_i   = SD of daily returns in the SAME estimation window (t-130..t-11)
  L         = number of days cumulated into CAR (= PRE + HORIZON + 1)
  SCAR_i    = CAR_i / (sigma_i * sqrt(L))          # BMP standardized CAR (unitless)
  |SCAR_i|  = the standardized magnitude that replaces |CAR_i| in the H1 split

Then the SAME gate as the frozen study: cluster to episodes, median-split the VIX
state read at t-1, amplification = mean(|SCAR| high) - mean(|SCAR| low), with the
cluster-bootstrap 95% CI and the 10k-permutation p. The raw |CAR| amplification is
recomputed alongside as the SECONDARY, clearly-labelled "unstandardized" line.

This is an ADDITIVE lens: it reads the DB and writes data/h1_sar.json. It does not
touch the frozen registered record.

Run:  python3 src/sar_lens.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from cross_asset import asset_returns, ASSETS
from event_study import car_for_event, PRE, POST, EST_START, EST_END
from robustness import assign_clusters
import research
import validate

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"

# H1 configuration -- Brent oil, VIX-percentile state, "high" amplifies, +20d horizon.
STATE_SID = "derived.vix_pct"
ASSET_SERIES = "fred.DCOILBRENTEU"
SIGN_STR = "high"
HORIZON = 20


def _sigma_for_event(ret, event_date):
    """SD of daily returns in the estimation window (t-130..t-11) -- the same quiet window the
    constant-mean model uses for mu. Returns None if the event lacks enough surrounding history
    (identical guard to event_study.car_for_event, so exactly the same events qualify)."""
    dates = ret.index
    pos = dates.searchsorted(pd.Timestamp(event_date))
    if pos >= len(dates) or pos - EST_START < 0 or pos + POST >= len(dates):
        return None
    est = ret.iloc[pos - EST_START: pos - EST_END]
    sd = float(est.std(ddof=1))
    return sd if sd > 0 else None


def _mags(conn, events, horizon, standardized):
    """Per-event magnitude at t+horizon. standardized=False -> |CAR| (%, the original headline
    metric). standardized=True -> |SCAR| = |CAR| / (sigma * sqrt(L)), the BMP number (unitless)."""
    asset = research._asset(ASSET_SERIES)
    ret = asset_returns(conn, asset["series"], asset["kind"])
    if ret is None:
        return {}
    L = PRE + horizon + 1                     # days cumulated into CAR[PRE+horizon]
    out = {}
    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["event_date"])
        if car is None or PRE + horizon >= len(car):
            continue
        car_h = float(car[PRE + horizon])     # signed CAR in return units (fraction)
        if standardized:
            sigma = _sigma_for_event(ret, ev["event_date"])
            if sigma is None:
                continue                      # no valid standardizer -> drop (smaller, honest sample)
            out[ev["event_id"]] = abs(car_h / (sigma * np.sqrt(L)))
        else:
            out[ev["event_id"]] = abs(car_h) * 100.0   # % -- matches _car_mags for price assets
    return out


def _episodes(conn, events, mags):
    """Reproduce run_test's episode construction: attach the VIX state at t-1, require >=12 usable
    events, cluster (35-day de-dup), keep the first per cluster -> (mags, states) episode arrays."""
    state = research._state_series(conn, STATE_SID)
    rows = []
    for _, ev in events.iterrows():
        if ev["event_id"] not in mags:
            continue
        v = state.asof(pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1))   # t-1, no lookahead
        if pd.notna(v):
            rows.append({"event_id": ev["event_id"], "date": ev["event_date"],
                         "mag": mags[ev["event_id"]], "state": float(v)})
    if len(rows) < 12:
        return None, None
    df = assign_clusters(pd.DataFrame(rows))
    clustered = df.groupby("cluster").first().reset_index()
    return clustered["mag"].to_numpy(float), clustered["state"].to_numpy(float)


def _gate(m, s):
    """The frozen gate: cluster-bootstrap amp + 95% CI, 10k-permutation p. sign=+1 (high amplifies)."""
    boot = validate.cluster_bootstrap_amp(m, s, sign=+1)
    perm = validate.permutation_p(m, s, sign=+1)
    excl0 = bool(boot["lo"] is not None and (boot["lo"] > 0 or boot["hi"] < 0))
    return {"amp": boot["obs"], "ci95": [boot["lo"], boot["hi"]], "perm_p": perm["p"],
            "ci_excludes_zero": excl0, "n_episodes": int(len(m))}


def run():
    conn = sqlite3.connect(DB)
    events = research._events(conn)

    raw = _mags(conn, events, HORIZON, standardized=False)
    sar = _mags(conn, events, HORIZON, standardized=True)
    m_raw, s_raw = _episodes(conn, events, raw)
    m_sar, s_sar = _episodes(conn, events, sar)
    conn.close()

    if m_sar is None:
        raise SystemExit("SAR lens: too few usable episodes -- cannot compute.")

    res_raw = _gate(m_raw, s_raw)
    res_sar = _gate(m_sar, s_sar)

    out = {
        "lens": "R1_SAR_headline",
        "attack": 1,
        "statement": "H1 amplification under BMP-standardized abnormal returns (each event's CAR "
                     "divided by its own estimation-window sigma * sqrt(L)).",
        "config": {"state": STATE_SID, "asset": ASSET_SERIES, "sign": SIGN_STR, "horizon": HORIZON,
                   "L_days_cumulated": PRE + HORIZON + 1,
                   "estimation_window": f"t-{EST_START}..t-{EST_END}"},
        "headline_sar": {
            "metric": "|SCAR+20| high-minus-low amplification (unitless, sigmas)",
            "amp": res_sar["amp"], "ci95": res_sar["ci95"], "perm_p": res_sar["perm_p"],
            "ci_excludes_zero": res_sar["ci_excludes_zero"], "n_episodes": res_sar["n_episodes"],
        },
        "secondary_raw_unstandardized": {
            "metric": "|CAR+20| high-minus-low amplification (pp) -- SUBJECT TO VOL-CLUSTERING",
            "amp": res_raw["amp"], "ci95": res_raw["ci95"], "perm_p": res_raw["perm_p"],
            "ci_excludes_zero": res_raw["ci_excludes_zero"], "n_episodes": res_raw["n_episodes"],
        },
        "verdict": ("SAR CI excludes zero -> amplification survives standardization"
                    if res_sar["ci_excludes_zero"] else
                    "SAR CI includes zero -> amplification does NOT survive standardization "
                    "(original headline was vol-clustering)"),
        "corpus_note": "current post-sweep corpus; additive lens, frozen record untouched.",
    }
    (ROOT / "data" / "h1_sar.json").write_text(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    r = run()
    print(json.dumps(r, indent=2))
