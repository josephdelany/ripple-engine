"""
event_study.py -- THE RIPPLE. The analytical core of the engine.

WHAT AN EVENT STUDY DOES (the method, in plain English):
You want to know "how much did oil move because of this event?" But oil moves
every day for a thousand reasons. So you:
  1. Look at a quiet period BEFORE the event (the "estimation window") and work
     out what a NORMAL day's return looks like for this asset.
  2. Look at the days around the event (the "event window") and compute how much
     each day's return DIFFERS from normal. That difference is the ABNORMAL RETURN.
  3. Add those abnormal returns up across the window. That running total is the
     CUMULATIVE ABNORMAL RETURN (CAR) -- the size and shape of the ripple.
  4. Average the CAR across all events of the same type to get the typical ripple
     for, say, a chokepoint disruption.

This is the standard method from MacKinlay (1997), "Event Studies in Economics
and Finance." We use the simplest normal-return model (constant mean return),
which is the appropriate choice for a commodity with no obvious market index.

Run:  python3 src/event_study.py
"""

import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
SERIES_ID = "fred.DCOILBRENTEU"   # Brent = the global benchmark

# --- Window parameters. Declare these BEFORE looking at results (pre-registration). ---
EST_START, EST_END = 130, 11   # estimation window: t-130 to t-11 (quiet period)
PRE, POST = 5, 20              # event window: t-5 to t+20
HORIZONS = [1, 5, 10, 20]      # report the ripple at these day-counts


def load_returns(conn):
    """Load the price series and convert it to daily log returns."""
    df = pd.read_sql(
        "SELECT obs_date, value FROM observations WHERE series_id = ? ORDER BY obs_date",
        conn, params=[SERIES_ID],
    )
    df["obs_date"] = pd.to_datetime(df["obs_date"])
    s = df.set_index("obs_date")["value"].sort_index()
    # log returns add up cleanly over time, which is why event studies use them
    return np.log(s).diff().dropna()


def car_for_event(ret, event_date):
    """Compute the CAR path for one event. Returns None if there isn't enough data."""
    dates = ret.index
    # Events can fall on weekends/holidays -> use the FIRST TRADING DAY on or after.
    pos = dates.searchsorted(pd.Timestamp(event_date))
    if pos >= len(dates):
        return None
    if pos - EST_START < 0 or pos + POST >= len(dates):
        return None  # not enough history or future data around this event

    # 1. What does a normal day look like? (mean return over the quiet window)
    mu = ret.iloc[pos - EST_START: pos - EST_END].mean()
    # 2. Abnormal return = actual minus normal, across the event window
    window = ret.iloc[pos - PRE: pos + POST + 1]
    abnormal = window - mu
    # 3. Cumulate -> the ripple
    return abnormal.cumsum().to_numpy()


def main():
    conn = sqlite3.connect(DB)
    ret = load_returns(conn)
    events = pd.read_sql(
        "SELECT event_id, event_date, type, title FROM events ORDER BY event_date", conn
    )
    conn.close()

    rel_days = np.arange(-PRE, POST + 1)
    results, skipped = {}, []

    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["event_date"])
        if car is None:
            skipped.append(f"{ev['event_id']} (outside price history)")
            continue
        results.setdefault(ev["type"], []).append((ev["event_id"], car))

    if not results:
        print("No events could be analysed. Check that events fall inside the price history.")
        return

    print(f"Price series: {len(ret):,} daily returns, "
          f"{ret.index.min().date()} to {ret.index.max().date()}")
    print(f"Estimation window: t-{EST_START} to t-{EST_END} | "
          f"Event window: t-{PRE} to t+{POST}\n")
    if skipped:
        print("Skipped:", "; ".join(skipped), "\n")

    print(f"{'event type':<24}{'n':>3}  " + "".join(f"CAR+{h:<7}" for h in HORIZONS) + "t-stat(+20)")
    print("-" * 78)

    for etype, items in sorted(results.items()):
        paths = np.vstack([c for _, c in items])
        mean_path = paths.mean(axis=0)
        n = len(items)
        row = f"{etype:<24}{n:>3}  "
        for h in HORIZONS:
            idx = PRE + h                      # position of t+h in the window
            row += f"{mean_path[idx]*100:>+6.1f}%  "
        # crude significance check on the +20 day CAR across events
        final = paths[:, PRE + 20]
        t = final.mean() / (final.std(ddof=1) / np.sqrt(n)) if n > 1 and final.std(ddof=1) > 0 else np.nan
        row += f"{t:>+7.2f}" if np.isfinite(t) else "     n/a"
        print(row)

    print("\nCAR = cumulative abnormal return (log), i.e. the move beyond normal.")
    print("|t| > ~2 is the rough significance threshold -- but with a small n,")
    print("treat these as INDICATIVE, not conclusive. Report the uncertainty honestly.")

    # --- The ripple chart ---
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for etype, items in sorted(results.items()):
        paths = np.vstack([c for _, c in items])
        ax.plot(rel_days, paths.mean(axis=0) * 100, linewidth=2,
                label=f"{etype} (n={len(items)})")
    ax.axvline(0, color="black", linewidth=1, linestyle="--", alpha=0.6)
    ax.axhline(0, color="grey", linewidth=0.8)
    ax.set_title("The Ripple: average cumulative abnormal return in Brent, by event type")
    ax.set_xlabel("trading days relative to event (0 = event day)")
    ax.set_ylabel("cumulative abnormal return (%)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    out = ROOT / "data" / "ripple.png"
    fig.savefig(out, dpi=130, bbox_inches="tight")
    print(f"\nSaved ripple chart to {out}")


if __name__ == "__main__":
    main()
