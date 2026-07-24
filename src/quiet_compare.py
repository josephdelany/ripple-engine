"""
quiet_compare.py -- do high-alarm / no-supply-channel shocks move oil? (the
                    threat-inflation control, FRONTIER_AUDIT F4)

THE QUESTION:
A referee asks whether our 42-event corpus is cherry-picked -- did we only keep
shocks we already knew moved oil? The honest test is a CONTROL GROUP: events that
generated enormous geopolitical alarm but had no channel to actually disrupt
crude (a nuclear test, an airstrike between non-producers, a domestic riot). If
those "quiet" shocks move oil about as much as our corpus, our selection is
suspect. If they move it far less, then oil reacts to supply channels, not to
alarm as such -- which is also the evidence base for the threat-inflation point.

This is DESCRIPTIVE / EXPLORATORY. It runs the SAME event-study machinery
(imported, not re-implemented) on the quiet set and reports the |CAR+20|
distribution against the clustered main corpus, with a two-sided permutation p on
the difference. No verdicts; the numbers speak for themselves.

Fujairah caveat: the Fujairah tanker sabotage (2019-05-12) sits 32 days before the
in-corpus Gulf of Oman attacks (2019-06-13), so its +20 window is contaminated by
that shock. Its numbers are reported, but it is EXCLUDED from the pooled
comparison, and we say so.

Run:  python3 src/quiet_compare.py
"""

import re
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

# Import only -- same CAR math, clustering, seed, and the cross-asset return builder.
from event_study import car_for_event, PRE
from robustness import assign_clusters
from cross_asset import asset_returns
from inference import PERMUTATION_SEED, N_PERM
import load_quiet

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "quiet_comparison.txt"

BRENT = "fred.DCOILBRENTEU"
FIVE_YR = "fred.DGS5"
FUJAIRAH_ID = "fujairah_sabotage_2019"   # excluded from the pool (window overlap)

# Descriptive report -- verdict/confirmatory words are not allowed.
BANNED = ("confirms", "confirm", "verdict", "holds", "fails", "proves", "proven")


def two_sample_perm_p(quiet_abs, main_abs, seed=PERMUTATION_SEED, n=N_PERM):
    """Two-sided permutation p on the difference in mean |CAR+20| between the two
    groups: pool the values, shuffle the group labels, and count how often the
    absolute mean-difference is at least as large as observed. Seeded -> identical
    across runs."""
    a, b = np.asarray(quiet_abs, float), np.asarray(main_abs, float)
    obs = abs(b.mean() - a.mean())
    pool = np.concatenate([a, b])
    na = len(a)
    rng = np.random.default_rng(seed)
    count = 0
    for _ in range(n):
        perm = rng.permutation(pool)
        if abs(perm[na:].mean() - perm[:na].mean()) >= obs:
            count += 1
    return count / n, obs


def car_pair(returns, date, scale):
    """CAR+5 and CAR+20 for one event on one return series (None if too little data)."""
    car = car_for_event(returns, date)
    if car is None:
        return None, None
    return car[PRE + 5] * scale, car[PRE + 20] * scale


def _enforce(text):
    hits = [w for w in BANNED if re.search(rf"\b{w}\b", text, re.IGNORECASE)]
    if hits:
        raise SystemExit(f"LANGUAGE CHECK FAILED: quiet report contains verdict/"
                         f"confirmatory words {hits}. Fix the template.")


def main():
    conn = sqlite3.connect(DB)
    load_quiet.load(conn)                                  # ensure the quiet table exists

    brent_ret = asset_returns(conn, BRENT, "price")        # log returns
    dgs5_ret = asset_returns(conn, FIVE_YR, "yield")       # daily change, bps

    quiet = pd.read_sql("SELECT event_id, event_date FROM quiet_events "
                        "ORDER BY event_date", conn)
    events = pd.read_sql("SELECT event_id, event_date AS date FROM events "
                         "ORDER BY event_date", conn)
    conn.close()

    # --- Per quiet event: Brent (%) and 5Y (bps) reactions ---
    q_rows = []
    for _, ev in quiet.iterrows():
        b5, b20 = car_pair(brent_ret, ev["event_date"], 100)   # log -> %
        y5, y20 = car_pair(dgs5_ret, ev["event_date"], 1)      # already bps
        q_rows.append({"event_id": ev["event_id"], "date": ev["event_date"],
                       "brent5": b5, "brent20": b20, "y5": y5, "y20": y20})
    qdf = pd.DataFrame(q_rows)

    # --- Main corpus |CAR+20| (Brent), clustered like robustness.py ---
    m_rows = []
    for _, ev in events.iterrows():
        car = car_for_event(brent_ret, ev["date"])
        if car is None:
            continue
        m_rows.append({"event_id": ev["event_id"], "date": ev["date"],
                       "abs20": abs(car[PRE + 20]) * 100})
    mdf = assign_clusters(pd.DataFrame(m_rows))
    main_clustered = mdf.groupby("cluster").first().reset_index()
    main_abs = main_clustered["abs20"].dropna().to_numpy()

    # --- Quiet pool: |CAR+20| Brent, EXCLUDING Fujairah (window overlap) ---
    pool = qdf[(qdf["event_id"] != FUJAIRAH_ID) & qdf["brent20"].notna()].copy()
    quiet_abs = pool["brent20"].abs().to_numpy()

    p, obs = two_sample_perm_p(quiet_abs, main_abs)

    # ---------------------------------------------------------------- report
    lines = []
    w = lines.append
    w("=" * 92)
    w("QUIET-SET COMPARISON -- do high-alarm / NO-supply-channel shocks move oil?")
    w("(DESCRIPTIVE / EXPLORATORY -- no verdicts; the numbers speak)")
    w("=" * 92)
    w("The quiet set: geopolitically alarming events with no channel to disrupt "
      "crude supply. Same event-study")
    w("machinery, windows and clustering as the main corpus. Units: Brent in % "
      "(log-return CAR), 5Y in bps.")
    w("")
    w("PER-EVENT REACTIONS (quiet set)")
    w(f"  {'event_id':<34}{'date':<12}{'Brent+5':>9}{'Brent+20':>10}{'5Y+5':>8}{'5Y+20':>8}")
    w("  " + "-" * 80)
    for _, r in qdf.iterrows():
        b5 = "  n/a" if pd.isna(r["brent5"]) else f"{r['brent5']:+.1f}%"
        b20 = "  n/a" if pd.isna(r["brent20"]) else f"{r['brent20']:+.1f}%"
        y5 = " n/a" if pd.isna(r["y5"]) else f"{r['y5']:+.0f}bp"
        y20 = " n/a" if pd.isna(r["y20"]) else f"{r['y20']:+.0f}bp"
        flag = "  <- FLAGGED (overlaps Gulf of Oman; excluded from pool)" \
            if r["event_id"] == FUJAIRAH_ID else ""
        w(f"  {r['event_id']:<34}{r['date']:<12}{b5:>9}{b20:>10}{y5:>8}{y20:>8}{flag}")
    w("")

    # --- The comparison ---
    w("=" * 92)
    w("|CAR+20| DISTRIBUTION -- quiet set (Fujairah excluded) vs clustered main corpus")
    w("=" * 92)
    w(f"  quiet set        n={len(quiet_abs):<2}  mean |CAR+20| = {quiet_abs.mean():5.1f}%   "
      f"median = {np.median(quiet_abs):5.1f}%   [{quiet_abs.min():.1f}% .. {quiet_abs.max():.1f}%]")
    w(f"  main corpus      n={len(main_abs):<2}  mean |CAR+20| = {main_abs.mean():5.1f}%   "
      f"median = {np.median(main_abs):5.1f}%   [{main_abs.min():.1f}% .. {main_abs.max():.1f}%]")
    w(f"  difference in means (main - quiet): {obs:+.1f} pp")
    w(f"  two-sided permutation p (seed={PERMUTATION_SEED}, N={N_PERM:,}): {p:.4f}")
    w("")
    w(f"  Fujairah reported above but EXCLUDED from this pool: its +20 window "
      f"overlaps the in-corpus")
    w(f"  Gulf of Oman attacks (2019-06-13, 32 days later), which would contaminate "
      f"its |CAR+20|.")
    w("")
    w("  Read (descriptive): a large positive difference with a small p is consistent "
      "with oil reacting to")
    w("  supply channels rather than to alarm as such; a small difference would be "
      "consistent with the")
    w("  corpus being alarm-selected. Exploratory only -- this raises the question, "
      "it does not settle it.")

    text = "\n".join(lines)
    _enforce(text)
    OUT.write_text(text + "\n")
    print(text)
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
