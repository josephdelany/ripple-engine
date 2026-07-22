"""
derive_signals.py -- the DERIVED LAYER. Raw data -> discriminating signals.

WHY THIS EXISTS:
Raw price tells you almost nothing. "Brent is $88" doesn't let you deviate from a
base rate. But "positioning is at the 12th percentile of its 5-year range while
price sits at the 88th" is a discriminating signal -- a reason to disagree with
consensus and be right.

Two properties make this layer valuable:
  1. It is DETERMINISTIC. Arithmetic on receipted inputs. There is no model in the
     loop that can invent anything. The analytical content lives BELOW the layer
     where an LLM writes prose, which is where fabrication happens.
  2. Each signal has a PRE-REGISTERED MECHANISM, declared before we look at what it
     says. Computing fifty metrics and hunting for the pretty one is p-hacking.

Derived signals are written back into the SAME observations table with a
'derived.' prefix -- no new tables, full provenance.

Run:  python3 src/derive_signals.py
"""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"

LOOKBACK = 1260   # ~5 years of trading days for z-scores/percentiles
MIN_OBS = 252     # need ~1 year before a z-score means anything

# Each signal: (id, name, unit, mechanism -- WHY it should matter, declared up front)
MECHANISMS = {
    "derived.brent_wti_spread": (
        "Brent-WTI Spread", "USD/bbl",
        "US logistics/export bottlenecks widen the spread; a widening gap signals "
        "American crude trapped inland rather than a global supply story."),
    "derived.brent_wti_spread_z": (
        "Brent-WTI Spread (z-score, 5y)", "sigma",
        "Normalised so 'wide' is measured against its own history, not eyeballed."),
    "derived.curve_2s10s": (
        "2s10s Treasury Curve", "percentage points",
        "Macro regime. An inverted curve signals a demand-destruction backdrop that "
        "dampens supply-shock pass-through."),
    "derived.usd_z": (
        "Broad Dollar (z-score, 5y)", "sigma",
        "Oil is priced in dollars. A strong dollar mechanically dampens commodity "
        "price moves and tightens global financial conditions."),
    "derived.vix_pct": (
        "VIX percentile (5y)", "percentile",
        "Stress regime. Shocks transmit harder and faster when volatility is already "
        "elevated and risk appetite is thin."),
    "derived.brent_vol20": (
        "Brent realised volatility (20d, annualised)", "percent",
        "The market's current sensitivity. High prevailing vol means a given shock "
        "produces a larger absolute move."),
    "derived.cot_pct": (
        "Managed-money net-long percentile (5y)", "percentile",
        "H3 (pre-registered): crowded speculative positioning is fragile; "
        "extremes of net-long amplify shocks via forced unwinds."),
}


def load_wide(conn):
    """Pull every series into one date-indexed table (one column per series)."""
    df = pd.read_sql(
        "SELECT series_id, obs_date, value FROM observations "
        "WHERE series_id NOT LIKE 'derived.%'", conn)
    df["obs_date"] = pd.to_datetime(df["obs_date"])
    wide = df.pivot_table(index="obs_date", columns="series_id", values="value")
    return wide.sort_index()


def zscore(s):
    """How many standard deviations from its own 5-year normal."""
    m = s.rolling(LOOKBACK, min_periods=MIN_OBS).mean()
    sd = s.rolling(LOOKBACK, min_periods=MIN_OBS).std()
    return (s - m) / sd


def percentile(s):
    """Where it sits in its own 5-year distribution (0-100)."""
    return s.rolling(LOOKBACK, min_periods=MIN_OBS).rank(pct=True) * 100


def build_signals(w):
    """Compute every derived signal. Each line maps to a declared mechanism above."""
    out = pd.DataFrame(index=w.index)
    brent = w.get("fred.DCOILBRENTEU")
    wti = w.get("fred.DCOILWTICO")

    if brent is not None and wti is not None:
        spread = brent - wti
        out["derived.brent_wti_spread"] = spread
        out["derived.brent_wti_spread_z"] = zscore(spread)

    if "fred.DGS10" in w and "fred.DGS2" in w:
        out["derived.curve_2s10s"] = w["fred.DGS10"] - w["fred.DGS2"]

    if "fred.DTWEXBGS" in w:
        out["derived.usd_z"] = zscore(w["fred.DTWEXBGS"])

    if "fred.VIXCLS" in w:
        out["derived.vix_pct"] = percentile(w["fred.VIXCLS"])

    if brent is not None:
        # realised volatility: std of daily log returns, annualised
        r = np.log(brent).diff()
        out["derived.brent_vol20"] = r.rolling(20).std() * np.sqrt(252) * 100

    if "cftc.mm_net_wti" in w:
        # Weekly series on a daily index: forward-fill so each day carries the
        # latest known Tuesday reading (that IS the point-in-time value).
        # Percentile lookback is 260 weekly obs ~= 5 years.
        cot = w["cftc.mm_net_wti"].ffill()
        out["derived.cot_pct"] = (
            w["cftc.mm_net_wti"].dropna()
            .rolling(260, min_periods=52).rank(pct=True).mul(100)
            .reindex(w.index).ffill()
        )

    return out


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    wide = load_wide(conn)
    signals = build_signals(wide)

    cur.execute("INSERT OR IGNORE INTO entities VALUES (?,?,?,?)",
                ("derived.signals", "derived", "Derived Signals",
                 "Deterministic metrics computed from receipted inputs"))

    for sid in signals.columns:
        name, unit, mechanism = MECHANISMS[sid]
        cur.execute(
            "INSERT OR REPLACE INTO series VALUES (?,?,?,?,?,?,?,?)",
            (sid, name, "derived.signals", unit, "daily", "derived (this repo)",
             "src/derive_signals.py", mechanism))
        col = signals[sid].dropna()
        payload = [(sid, d.strftime("%Y-%m-%d"), float(v), d.strftime("%Y-%m-%d"), now)
                   for d, v in col.items()]
        cur.executemany("INSERT OR REPLACE INTO observations VALUES (?,?,?,?,?)", payload)
        print(f"{name:<44} {len(payload):>7,} obs")

    conn.commit()

    # --- Current state of the system: what the signals say RIGHT NOW ---
    print("\n" + "=" * 68)
    print("CURRENT STATE OF THE SYSTEM (latest available reading)")
    print("=" * 68)
    for sid in signals.columns:
        col = signals[sid].dropna()
        if col.empty:
            continue
        name = MECHANISMS[sid][0]
        print(f"  {name:<44} {col.iloc[-1]:>8.2f}   ({col.index[-1].date()})")
    print("\nThese are the MODULATORS. A shock landing today lands into this state.")
    conn.close()


if __name__ == "__main__":
    main()
