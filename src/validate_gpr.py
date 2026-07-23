"""
validate_gpr.py -- does our hand-built event list line up with GPR? (read-only)

THE QUESTION (FRONTIER_AUDIT F4 -- selection bias):
We picked 42 events by hand. A referee will ask: did you cherry-pick the ones you
already knew moved oil, and ignore comparably-geopolitical events that didn't?
An honest check is to hold each event up against an EXTERNAL, peer-reviewed
salience measure -- the GPR index -- that knows nothing about oil. If our events
sit at high GPR, our selection tracks real geopolitical salience. If some sit at
low GPR, that is a flag to discuss openly, not hide.

WHAT THIS COMPUTES, per event (nothing is split, conditioned, or predicted):
  * GPRD on the event date, and its full-history percentile (where that day's GPR
    ranks against every GPR day since 1985).
  * The PEAK GPRD within +/-3 calendar days of the event, and ITS percentile --
    the headline salience number, because geopolitical news often peaks a day or
    two around the event date.

Output: data/gpr_validation.txt (sorted high-salience first) + a summary: the
median peak-GPR percentile across the 42 events, and the events whose peak still
sits below the 50th percentile (the selection-bias candidates to discuss).

THIS IS DATA VALIDATION, NOT ANALYSIS. It does NOT condition CARs on GPR. That
step is blocked until Joe registers an H4 hypothesis (direction + rationale)
before looking at any result -- the same pre-registration discipline as H1-H3.

Run:  python3 src/validate_gpr.py
"""

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "gpr_validation.txt"

WINDOW_DAYS = 3   # +/- calendar days around the event for the peak GPR


def _ord(x):
    """93 -> '93rd', 57 -> '57th' -- so the summary reads naturally."""
    n = int(round(x))
    suffix = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def main():
    conn = sqlite3.connect(DB)
    gpr = pd.read_sql(
        "SELECT obs_date, value FROM observations WHERE series_id = 'gpr.GPRD' "
        "ORDER BY obs_date", conn)
    events = pd.read_sql(
        "SELECT event_id, event_date, type FROM events ORDER BY event_date", conn)
    conn.close()

    if gpr.empty:
        print("STOP: no gpr.GPRD data in the database. Run src/fetch_gpr.py first.")
        return

    gpr["obs_date"] = pd.to_datetime(gpr["obs_date"])
    s = gpr.set_index("obs_date")["value"].sort_index()
    all_vals = s.to_numpy()

    def percentile(v):
        """Full-history percentile: share of all GPR days at or below v."""
        if v is None or np.isnan(v):
            return np.nan
        return float((all_vals <= v).mean() * 100)

    rows = []
    for _, ev in events.iterrows():
        d = pd.Timestamp(ev["event_date"])
        on_date = s.asof(d)                                    # value on/just before
        win = s[(s.index >= d - pd.Timedelta(days=WINDOW_DAYS)) &
                (s.index <= d + pd.Timedelta(days=WINDOW_DAYS))]
        peak = float(win.max()) if len(win) else np.nan
        rows.append({
            "event_id": ev["event_id"], "date": ev["event_date"], "type": ev["type"],
            "gprd_on": None if pd.isna(on_date) else float(on_date),
            "pct_on": percentile(None if pd.isna(on_date) else float(on_date)),
            "gprd_peak": peak, "pct_peak": percentile(peak),
        })
    df = pd.DataFrame(rows).sort_values("pct_peak", ascending=False)

    lines = []
    w = lines.append
    w("=" * 92)
    w("GPR EVENT-LIST VALIDATION -- do our 42 events line up with the field-standard "
      "salience measure?")
    w("=" * 92)
    w(f"GPR history: {s.index.min().date()} to {s.index.max().date()}  "
      f"({len(s):,} daily obs).  Percentiles are full-history.")
    w(f"'peak' = highest GPRD within +/-{WINDOW_DAYS} days of the event.  "
      f"Sorted by peak percentile (most salient first).")
    w("-" * 92)
    w(f"{'event_id':<32}{'date':<12}{'GPRD':>8}{'pctile':>8}   "
      f"{'peak':>8}{'pk pctile':>10}")
    w("-" * 92)
    for _, r in df.iterrows():
        w(f"{r['event_id'][:31]:<32}{r['date']:<12}"
          f"{r['gprd_on']:>8.1f}{r['pct_on']:>7.0f}%   "
          f"{r['gprd_peak']:>8.1f}{r['pct_peak']:>9.0f}%")
    w("-" * 92)

    # --- Summary ---
    med_peak = df["pct_peak"].median()
    med_on = df["pct_on"].median()
    below = df[df["pct_peak"] < 50].sort_values("pct_peak")
    w("")
    w("SUMMARY")
    w(f"  events validated:                 {len(df)}")
    w(f"  median peak-GPR percentile:       {_ord(med_peak)}   "
      f"(median on-date percentile: {_ord(med_on)})")
    w(f"  events below the 50th percentile (peak): {len(below)}")
    if len(below):
        w("  -> selection-bias candidates to discuss (F4): even their +/-3d GPR peak "
          "ranks below the median GPR day.")
        for _, r in below.iterrows():
            w(f"       {_ord(r['pct_peak']):>5}  {r['event_id']:<32} ({r['date']}, "
              f"{r['type']})")
    else:
        w("  -> every event's +/-3d GPR peak sits at or above the median GPR day: "
          "the hand-built list tracks external salience.")
    w("")
    w("NOTE: this is validation only. Conditioning blocked pending registered H4 (Joe).")

    text = "\n".join(lines)
    OUT.write_text(text + "\n")
    print(text)
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
