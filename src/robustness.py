"""
robustness.py -- does the VIX finding survive honest scrutiny?

THE PROBLEM THIS SOLVES:
Event studies assume events are INDEPENDENT. But March-April 2020 has three
"events" inside five weeks (OPEC collapse, COVID declaration, record cut) whose
measurement windows overlap heavily. That's one episode measured three times.
If all three sit in the high-VIX bucket, they inflate the conditioning result.

THE TESTS (standard robustness practice):
  1. BASELINE      - all 20 events, as before.
  2. CLUSTERED     - events whose windows overlap are collapsed into one cluster
                     (keep the FIRST event of each cluster; the cluster's ripple
                     is measured once, from its first shock).
  3. NO-OUTLIER    - clustered, minus any event with an extreme measurement
                     environment (Brent vol > 100% annualised -- the negative-price
                     chaos of April 2020 makes CAR meaningless there anyway).

If the VIX amplification holds in all three rows, it's likely real.
If it dies when the 2020 cluster collapses, it was an artifact. Either answer
is a legitimate finding -- and you report whichever one the data gives.

Run:  python3 src/robustness.py
"""

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from derive_signals import load_wide, build_signals
from event_study import load_returns, car_for_event, PRE, POST

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"

# Two events overlap if they're within this many CALENDAR days
# (the event window spans about 25 trading days ~= 35 calendar days).
CLUSTER_DAYS = 35
VOL_OUTLIER = 100.0   # Brent vol (annualised %) above this = broken environment


def assign_clusters(df):
    """Group events whose windows overlap. Returns df with a cluster id."""
    df = df.sort_values("date").reset_index(drop=True)
    cluster, last_date, cid = [], None, 0
    for d in pd.to_datetime(df["date"]):
        if last_date is not None and (d - last_date).days <= CLUSTER_DAYS:
            cluster.append(cid)          # same cluster as previous event
        else:
            cid += 1
            cluster.append(cid)
        last_date = d
    df["cluster"] = cluster
    return df


def vix_split(df, label):
    """The conditioning test: ripple magnitude, high-VIX vs low-VIX."""
    v = df[df["vix"].notna()]
    if len(v) < 4:
        print(f"  {label:<26} not enough events")
        return
    med = v["vix"].median()
    hi, lo = v[v["vix"] >= med], v[v["vix"] < med]
    amp = (hi["abs_car"].mean() - lo["abs_car"].mean()) * 100
    print(f"  {label:<26} n={len(v):>2}   "
          f"high |CAR+20|={hi['abs_car'].mean()*100:5.1f}% (n={len(hi)})   "
          f"low={lo['abs_car'].mean()*100:5.1f}% (n={len(lo)})   "
          f"amplification {amp:+.1f} pp")


def main():
    conn = sqlite3.connect(DB)
    ret = load_returns(conn)
    signals = build_signals(load_wide(conn))
    events = pd.read_sql("SELECT event_id, event_date AS date, type FROM events "
                         "ORDER BY event_date", conn)
    conn.close()

    rows = []
    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["date"])
        if car is None:
            continue
        cutoff = pd.Timestamp(ev["date"]) - pd.Timedelta(days=1)
        vix = signals["derived.vix_pct"].dropna().asof(cutoff) \
            if "derived.vix_pct" in signals else np.nan
        vol = signals["derived.brent_vol20"].dropna().asof(cutoff) \
            if "derived.brent_vol20" in signals else np.nan
        rows.append({"event_id": ev["event_id"], "date": ev["date"],
                     "abs_car": abs(car[PRE + 20]), "vix": vix, "brent_vol": vol})
    df = assign_clusters(pd.DataFrame(rows))

    # Show what got clustered, so nothing happens silently.
    print("=" * 90)
    print("CLUSTERS (events measured inside the same window = one episode)")
    print("=" * 90)
    for cid, grp in df.groupby("cluster"):
        if len(grp) > 1:
            names = ", ".join(grp["event_id"])
            print(f"  cluster {cid}: {names}   -> keeping first only")
    if df.groupby("cluster").size().max() == 1:
        print("  (no overlapping events)")

    clustered = df.groupby("cluster").first().reset_index()
    no_outlier = clustered[clustered["brent_vol"] < VOL_OUTLIER]
    dropped = clustered[clustered["brent_vol"] >= VOL_OUTLIER]
    if len(dropped):
        print(f"\n  outlier dropped in test 3: "
              f"{', '.join(dropped['event_id'])} (Brent vol > {VOL_OUTLIER:.0f}%)")

    print("\n" + "=" * 90)
    print("DOES THE VIX CONDITIONING SURVIVE?")
    print("=" * 90)
    vix_split(df, "1. baseline (all events)")
    vix_split(clustered, "2. clustered")
    vix_split(no_outlier, "3. clustered, no outlier")

    print("\nHow to read this: if the amplification stays large and positive down "
          "all three rows,\nthe finding survives its own best rebuttals. If it "
          "shrinks toward zero, it was the\n2020 episode all along -- also worth "
          "knowing, and also reportable.")


if __name__ == "__main__":
    main()
