"""
cc2_robustness.py -- R6: CC2 outlier-drop + seasonality (red-team attacks 13, 14).

THE EDGE UNDER FIRE
-------------------
CC2 (supply events -> gasoline crack, signed CAR+10) is the value-chain edge the
cross-chain battery called VALIDATED: +2.96 $/bbl, CI [0.99, 5.21], perm p=0.003.
Two attacks, both CONCEDED:

  #13 Outlier-driven. The n=37 episode CARs have signs all over the place
      (-6.85 ... +10.97, +16.64, and a lone +29.01 for hormuz_closure_2026, ~10x
      the median). Nearly half are negative against the predicted "+". The CI
      lower bound is only +0.99; drop the two post-registration monsters
      (hormuz_closure_2026, venezuela_blackout_2019) and it likely crosses zero.

  #14 No seasonality control. The gasoline crack has a strong summer-driving-season
      signature; a 1987-2026 study with a constant-mean model does not remove it.

WHAT THIS COMPUTES
------------------
Reuses the EXACT CC2 machinery from cross_chain.py (same _value_returns / _signed_car
/ cluster / _one_sample), so the baseline reproduces, then re-runs CC2 under:

  * drop hormuz_closure_2026
  * drop venezuela_blackout_2019
  * drop BOTH (the reviewer's ask)
  * month-of-year seasonally-adjusted crack (see METHOD), full sample
  * seasonally-adjusted AND both outliers dropped  (the strictest cut)

SEASONAL-ADJUSTMENT METHOD (documented)
---------------------------------------
The crack "return" is the daily change of the gasoline-crack spread ($/bbl). Build a
month-of-year climatology: the mean daily change within each calendar month over the
whole series (12 numbers). Subtract each day's calendar-month mean from that day's
change -> a deseasonalised daily-change series with the average seasonal drift
removed. Recompute the constant-mean signed CAR+10 on the deseasonalised series. This
strips the summer-driving-season drift that the +10d window would otherwise pick up.
Caveat (stated): the climatology is estimated full-sample, so it is a fixed CALENDAR
adjustment, not point-in-time price information -- standard for de-seasonalising, but
noted as a mild in-sample use of the calendar.

DECISION (pre-stated, matches the brief): if the outlier-drop CI crosses zero, CC2
DOWNGRADES from validated to SUGGESTIVE in the portfolio and packs.

ADDITIVE LENS: reads the DB, writes data/cc2_seasonal.json. Registered record untouched.
Run:  python3 src/cc2_robustness.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from cross_chain import (_value_returns, _signed_car, _one_sample, SUPPLY_TYPES,
                         POST_D, SEED)
from robustness import assign_clusters

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
JSON = ROOT / "data" / "cc2_seasonal.json"
CRACK = "derived.gasoline_crack"
DROP_HORMUZ = "hormuz_closure_2026"
DROP_VENEZUELA = "venezuela_blackout_2019"


def _deseasonalise(ret):
    """Subtract the month-of-year mean daily change (full-sample climatology) from each day.
    ret is a date-indexed Series of daily crack changes ($/bbl)."""
    monthly_mean = ret.groupby(ret.index.month).transform("mean")
    return ret - monthly_mean


def _cc2_episodes(conn, ret, events, drop_ids=()):
    """The CC2 episode CARs on a given (possibly deseasonalised) crack-return series, excluding
    any event_ids in drop_ids. Same event set, same clustering, same first-per-cluster as CC2."""
    ev = events[events["type"].isin(SUPPLY_TYPES)].copy()
    rows = []
    for r in ev.itertuples():
        if r.event_id in drop_ids:
            continue
        c = _signed_car(ret, r.event_date, POST_D)
        if c is not None:
            rows.append({"event_id": r.event_id, "date": pd.Timestamp(str(r.event_date)), "car": c})
    if len(rows) < 6:
        return None
    df = assign_clusters(pd.DataFrame(rows)).groupby("cluster").first().reset_index()
    return df


def _variant(conn, ret, events, drop_ids=()):
    df = _cc2_episodes(conn, ret, events, drop_ids)
    if df is None:
        return {"ok": False, "reason": "too few episodes"}
    r = _one_sample(df["car"].to_numpy(float), sign=+1)
    r["n_episodes"] = int(len(df))
    return r


def run():
    conn = sqlite3.connect(DB)
    events = pd.read_sql("SELECT event_id, event_date, type FROM events ORDER BY event_date", conn)
    ret_raw = _value_returns(conn, CRACK, "diff")
    ret_des = _deseasonalise(ret_raw)
    conn.close()

    baseline = _variant(conn, ret_raw, events)                                   # reproduce CC2
    drop_hormuz = _variant(conn, ret_raw, events, {DROP_HORMUZ})
    drop_venez = _variant(conn, ret_raw, events, {DROP_VENEZUELA})
    drop_both = _variant(conn, ret_raw, events, {DROP_HORMUZ, DROP_VENEZUELA})
    seasonal = _variant(conn, ret_des, events)
    seasonal_drop_both = _variant(conn, ret_des, events, {DROP_HORMUZ, DROP_VENEZUELA})

    def crosses_zero(v):
        return not (v.get("ok") and v.get("ci_excludes_zero_in_dir"))

    # The verdict: any of the reviewer's cuts (outlier-drop or seasonal) crossing zero downgrades CC2.
    downgrade = any(crosses_zero(v) for v in (drop_both, seasonal, seasonal_drop_both))

    out = {
        "lens": "R6_cc2_outlier_seasonal",
        "attacks": [13, 14],
        "edge": "CC2_supply_gasoline_crack",
        "spec": "supply events (chokepoint_disruption U infrastructure_attack) -> gasoline crack, "
                "signed constant-mean CAR+10 ($/bbl), cluster-first, one-sample directional test.",
        "seasonal_method": "month-of-year climatology: subtract each calendar month's mean daily "
                           "crack change (full-sample) from that day's change; recompute CAR on the "
                           "deseasonalised series. Fixed calendar adjustment (noted: full-sample).",
        "baseline_reproduces_cc2": baseline,
        "outlier_drop": {
            "ex_hormuz_2026": drop_hormuz,
            "ex_venezuela_2019": drop_venez,
            "ex_both": drop_both,
        },
        "seasonally_adjusted": seasonal,
        "seasonally_adjusted_ex_both_outliers": seasonal_drop_both,
        "ci_crosses_zero": {
            "ex_both_outliers": crosses_zero(drop_both),
            "seasonal": crosses_zero(seasonal),
            "seasonal_ex_both": crosses_zero(seasonal_drop_both),
        },
        "downgrade_to_suggestive": bool(downgrade),
        "verdict": (
            "CC2 DOWNGRADES to SUGGESTIVE: at least one of {drop-both-outliers, seasonally-adjusted, "
            "seasonal+drop-both} has a 95% CI that includes zero, so the edge is not robust to the "
            "two post-registration outliers and/or the summer-driving seasonality."
            if downgrade else
            "CC2 HOLDS: the CI still excludes zero after dropping both named outliers AND after "
            "month-of-year seasonal adjustment. The edge is not outlier- or season-driven."),
        "corpus_note": "additive lens; frozen registered record untouched.",
    }
    JSON.write_text(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    r = run()
    print(json.dumps(r, indent=2))
