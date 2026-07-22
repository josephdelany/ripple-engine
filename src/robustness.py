"""
robustness.py -- do the H1-H3 conditioning findings survive honest scrutiny?

THE PROBLEM THIS SOLVES:
Event studies assume events are INDEPENDENT. But March-April 2020 has three
"events" inside five weeks (OPEC collapse, COVID declaration, record cut) whose
measurement windows overlap heavily. That's one episode measured three times.
If all three sit in the same state bucket, they inflate the conditioning result.

THE TESTS (standard robustness practice), run for EACH registered variable:
  1. BASELINE      - all 20 events, as before (this is the RAW split).
  2. CLUSTERED     - events whose windows overlap are collapsed into one cluster
                     (keep the FIRST event of each cluster; the cluster's ripple
                     is measured once, from its first shock). THIS is the row the
                     pre-registered decision rule is applied to.
  3. NO-OUTLIER    - clustered, minus any event with an extreme measurement
                     environment (Brent vol > 100% annualised -- the negative-price
                     chaos of April 2020 makes CAR meaningless there anyway).

THE REGISTERED HYPOTHESES (directions fixed in BRIEF_SKELETON.md §4, before
results). Each is a high-vs-low split of |CAR+20| at the variable's own median;
"amplification" is (high bucket mean) - (low bucket mean), in percentage points:
  H1 VIX (vix_pct):     high stress amplifies      -> predicted amp POSITIVE
  H2 inventories (inv_sigma): tight (LOW sigma) amplifies -> predicted amp NEGATIVE
  H3 positioning (cot_pct):   crowded (HIGH net-long %) amplifies -> predicted POSITIVE

DECISION RULE (BRIEF_SKELETON.md §4, fixed before computation):
  a hypothesis HOLDS if the CLUSTERED amplification exceeds +5pp IN THE PREDICTED
  DIRECTION; otherwise it FAILS. Reported exactly as computed.

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
HOLD_THRESHOLD = 5.0  # pp; clustered amplification must clear this to "hold"

# The three pre-registered hypotheses. `sign` maps the raw (high-low) amplification
# onto the PREDICTED direction: +1 = high bucket predicted bigger, -1 = low bigger.
# These directions come straight from the H1-H3 statements, declared before results.
REGISTERED = [
    ("H1", "derived.vix_pct",   "vix",       +1, "high VIX (stress) amplifies"),
    ("H2", "derived.inv_sigma", "inv_sigma", -1, "tight inventories (LOW sigma) amplify"),
    ("H3", "derived.cot_pct",   "cot",       +1, "crowded net-long (HIGH percentile) amplifies"),
]


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


def split(df, col):
    """High-vs-low median split of |CAR+20|. Returns a dict, or None if too thin."""
    v = df[df[col].notna()]
    if len(v) < 4:
        return None
    med = v[col].median()
    hi, lo = v[v[col] >= med], v[v[col] < med]
    if not len(hi) or not len(lo):
        return None
    return {
        "n": len(v),
        "hi_mean": hi["abs_car"].mean() * 100, "n_hi": len(hi),
        "lo_mean": lo["abs_car"].mean() * 100, "n_lo": len(lo),
        "amp": (hi["abs_car"].mean() - lo["abs_car"].mean()) * 100,  # raw high-low
    }


def print_row(label, res):
    """One line of the survival table for a single test row."""
    if res is None:
        print(f"  {label:<26} not enough events")
        return
    print(f"  {label:<26} n={res['n']:>2}   "
          f"high |CAR+20|={res['hi_mean']:5.1f}% (n={res['n_hi']})   "
          f"low={res['lo_mean']:5.1f}% (n={res['n_lo']})   "
          f"amplification {res['amp']:+.1f} pp")


def main():
    conn = sqlite3.connect(DB)
    ret = load_returns(conn)
    signals = build_signals(load_wide(conn))
    events = pd.read_sql("SELECT event_id, event_date AS date, type FROM events "
                         "ORDER BY event_date", conn)
    conn.close()

    # State of each registered variable at t-1 (last reading BEFORE the event).
    rows = []
    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["date"])
        if car is None:
            continue
        cutoff = pd.Timestamp(ev["date"]) - pd.Timedelta(days=1)
        row = {"event_id": ev["event_id"], "date": ev["date"],
               "abs_car": abs(car[PRE + 20])}
        for _, sid, key, _, _ in REGISTERED:
            s = signals[sid].dropna() if sid in signals else pd.Series(dtype=float)
            row[key] = s.asof(cutoff) if len(s) else np.nan
        vol = signals["derived.brent_vol20"].dropna().asof(cutoff) \
            if "derived.brent_vol20" in signals else np.nan
        row["brent_vol"] = vol
        rows.append(row)
    df = assign_clusters(pd.DataFrame(rows))

    # Show what got clustered, so nothing happens silently.
    print("=" * 90)
    print("CLUSTERS (events measured inside the same window = one episode)")
    print("=" * 90)
    for cid, grp in df.groupby("cluster"):
        if len(grp) > 1:
            print(f"  cluster {cid}: {', '.join(grp['event_id'])}   -> keeping first only")
    if df.groupby("cluster").size().max() == 1:
        print("  (no overlapping events)")

    clustered = df.groupby("cluster").first().reset_index()
    no_outlier = clustered[clustered["brent_vol"] < VOL_OUTLIER]
    dropped = clustered[clustered["brent_vol"] >= VOL_OUTLIER]
    if len(dropped):
        print(f"\n  outlier dropped in test 3: "
              f"{', '.join(dropped['event_id'])} (Brent vol > {VOL_OUTLIER:.0f}%)")

    # --- The survival table, run for all three registered variables ---
    verdicts = []
    for hid, sid, key, sign, desc in REGISTERED:
        print("\n" + "=" * 90)
        print(f"{hid}: DOES {desc.upper()} SURVIVE?   (split on {sid})")
        print("=" * 90)
        base = split(df, key)
        clus = split(clustered, key)
        noout = split(no_outlier, key)
        print_row("1. baseline (all events)", base)
        print_row("2. clustered", clus)
        print_row("3. clustered, no outlier", noout)

        # Decision rule: clustered amplification, IN THE PREDICTED DIRECTION.
        if clus is None:
            verdicts.append(f"{hid} FAILS (too few events with a reading to test)")
        else:
            directional = sign * clus["amp"]   # flip so 'predicted bigger' is positive
            holds = directional > HOLD_THRESHOLD
            arrow = "high>low" if sign > 0 else "low>high"
            print(f"  -> predicted direction: {arrow}; clustered directional "
                  f"amplification {directional:+.1f} pp "
                  f"(threshold +{HOLD_THRESHOLD:.0f} pp)")
            verdicts.append(f"{hid} {'HOLDS' if holds else 'FAILS'} "
                            f"(clustered {directional:+.1f} pp in predicted direction)")

    print("\nHow to read this: down each variable's three rows, if the amplification "
          "stays large and\nin the predicted direction, the finding survives its own "
          "best rebuttals. If it shrinks or\nflips when the 2020 cluster collapses, it "
          "was that episode all along -- also reportable.")

    # --- The registered verdict (decision rule applied deterministically) ---
    print("\n" + "#" * 90)
    print("REGISTERED VERDICT (BRIEF_SKELETON.md §4 rule: +5pp clustered, predicted direction)")
    print("#" * 90)
    for v in verdicts:
        print("  " + v)


if __name__ == "__main__":
    main()
