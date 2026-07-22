"""
conditioned_study.py -- THE CONDITIONED RIPPLE. The analytical core.

THE QUESTION THIS ANSWERS:
A plain event study says "conflict shocks move oil +28% on average." That's an
average across all history, and averages hide the thing that matters. The real
question an analyst is paid to answer is:

    "Does the SAME shock hit harder when the system is already fragile?"

So for every event we measure the STATE of the system on the day BEFORE it
(volatility regime, energy vol, logistics spread, dollar, curve), then compare
the ripple across states. That turns:

    "conflict -> +28%"
into
    "conflict -> +40% when volatility was already elevated, +12% when it was calm"

That is a conditioned forecast, and it is the difference between a statistic and
an insight.

PRE-REGISTERED DESIGN (declared before looking at any result):
  - State is measured at t-1, the last reading BEFORE the event. Never after.
    (Measuring state after the event would leak the outcome into the predictor.)
  - Split rule: high vs low = above/below the median of that signal's own history.
  - We report event-level detail, because with a small sample the honest
    presentation is the raw table, not a confident average.

Run:  python3 src/conditioned_study.py
"""

import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Reuse the tested logic instead of duplicating it (modularity).
from derive_signals import load_wide, build_signals
from event_study import load_returns, car_for_event, PRE, POST

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"

# The state variables that condition a ripple, with why each should matter.
STATE_VARS = {
    "derived.vix_pct":            "VIX %ile",   # H1
    "derived.cot_pct":            "COT %ile",   # H3
    "derived.brent_vol20":        "Brent vol",
    "derived.brent_wti_spread_z": "B-W z",
    "derived.usd_z":              "USD z",
    "derived.curve_2s10s":        "2s10s",
}
# The variable we split on for the conditional comparison.
SPLIT_ON = "derived.brent_vol20"


def main():
    conn = sqlite3.connect(DB)
    ret = load_returns(conn)
    signals = build_signals(load_wide(conn))
    events = pd.read_sql(
        "SELECT event_id, event_date, type, title, severity, surprise "
        "FROM events ORDER BY event_date", conn)
    conn.close()

    rows = []
    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["event_date"])
        if car is None:
            continue
        # State on the day BEFORE the event -- no lookahead.
        cutoff = pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1)
        state = {}
        for sid in STATE_VARS:
            if sid in signals:
                s = signals[sid].dropna()
                state[sid] = s.asof(cutoff) if len(s) else np.nan
            else:
                state[sid] = np.nan
        rows.append({
            "event_id": ev["event_id"], "date": ev["event_date"], "type": ev["type"],
            "severity": ev["severity"], "surprise": ev["surprise"],
            "car5": car[PRE + 5], "car20": car[PRE + 20],
            "abs_car20": abs(car[PRE + 20]),   # magnitude, for pooling across types
            "path": car, **state,
        })

    if not rows:
        print("No analysable events.")
        return
    df = pd.DataFrame(rows)

    # --- 1. Event-level detail (the honest presentation at small n) ---
    print("=" * 100)
    print("EVENT-LEVEL DETAIL -- the ripple, and the state of the system the day before")
    print("=" * 100)
    hdr = f"{'event':<28}{'date':<12}{'CAR+5':>8}{'CAR+20':>8}   "
    hdr += "".join(f"{lbl:>11}" for lbl in STATE_VARS.values())
    print(hdr)
    print("-" * 100)
    for _, r in df.iterrows():
        line = f"{r['event_id'][:27]:<28}{r['date']:<12}{r['car5']*100:>+7.1f}%{r['car20']*100:>+7.1f}%   "
        for sid in STATE_VARS:
            v = r[sid]
            line += f"{v:>11.2f}" if pd.notna(v) else f"{'n/a':>11}"
        print(line)

    # --- 2. The conditional comparison, on MAGNITUDE ---
    # WHY MAGNITUDE: pooling signed returns across opposite-signed event types
    # (OPEC decisions push price DOWN, conflicts push it UP) measures nothing but
    # the mix of types in each bucket. |CAR| asks the right question: "was the
    # ripple BIGGER in this state?" -- which is what conditioning is actually about.
    def compare(col, label):
        v = df[df[col].notna()]
        if len(v) < 2:
            print(f"\n  {label}: not enough events with a reading.")
            return
        med = v[col].median()
        hi, lo = v[v[col] >= med], v[v[col] < med]
        print(f"\n  Split on {label} at median {med:.2f}")
        for name, grp in [("high", hi), ("low ", lo)]:
            if len(grp):
                print(f"    {name}  n={len(grp)}   mean |CAR+20| = "
                      f"{grp['abs_car20'].mean()*100:>5.1f}%")
        if len(hi) and len(lo):
            amp = (hi["abs_car20"].mean() - lo["abs_car20"].mean()) * 100
            print(f"    amplification: {amp:+.1f} pp")

    print("\n" + "=" * 100)
    print("CONDITIONED RIPPLE -- ripple MAGNITUDE by pre-event state")
    print("=" * 100)
    for col, label in [(SPLIT_ON, STATE_VARS[SPLIT_ON]),
                       ("derived.vix_pct", "VIX %ile"),
                       ("surprise", "surprise (1-5)")]:
        if col in df.columns:
            compare(col, label)

    valid = df[df[SPLIT_ON].notna()]

    print("\n" + "!" * 100)
    print(f"HONESTY CHECK: n = {len(df)} events. This is FAR too few to conclude "
          f"anything.\nThe machinery is correct and will sharpen with every sourced "
          f"event you add.\nReport these as illustrative, never as findings.")
    print("!" * 100)

    # --- 3. Chart: ripple paths coloured by pre-event state ---
    if len(valid) >= 2:
        med = valid[SPLIT_ON].median()
        rel = np.arange(-PRE, POST + 1)
        fig, ax = plt.subplots(figsize=(10, 5.5))
        for _, r in valid.iterrows():
            fragile = r[SPLIT_ON] >= med
            ax.plot(rel, r["path"] * 100, linewidth=1.8,
                    color="#D85A30" if fragile else "#378ADD", alpha=0.85,
                    label="_nolegend_")
        ax.plot([], [], color="#D85A30", linewidth=2, label="elevated volatility at t-1")
        ax.plot([], [], color="#378ADD", linewidth=2, label="calm at t-1")
        ax.axvline(0, color="black", linestyle="--", linewidth=1, alpha=0.6)
        ax.axhline(0, color="grey", linewidth=0.8)
        ax.set_title("Conditioned ripple: same shocks, different starting states")
        ax.set_xlabel("trading days relative to event")
        ax.set_ylabel("cumulative abnormal return (%)")
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3)
        out = ROOT / "data" / "conditioned_ripple.png"
        fig.savefig(out, dpi=130, bbox_inches="tight")
        print(f"\nSaved chart to {out}")


if __name__ == "__main__":
    main()
