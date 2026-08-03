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
    "derived.inv_sigma": (
        "Inventory deviation from seasonal norm (5y)", "sigma",
        "H2 (pre-registered): thin physical buffers cannot absorb supply risk, "
        "so price must; crude stocks below their seasonal norm (negative sigma) "
        "amplify shock transmission."),
    "derived.be_level": (
        "10Y inflation breakeven percentile (5y)", "percentile",
        "Inflation-expectations regime (pre-registered conditioner for the "
        "yields-inflation-regime hypothesis in the edge battery). When breakevens "
        "sit high in their own 5y range the market reads an oil shock as "
        "inflationary and passes it into nominal yields; when low/anchored the same "
        "shock reads growth-negative (flight-to-quality). So the |yield move| a "
        "shock produces should be larger when this sits high."),
    "derived.credit_stress": (
        "HY credit stress percentile (5y)", "percentile",
        "Credit-cycle regime (WS-S amendment). Built from the HYG high-yield ETF's "
        "drawdown from its trailing-252d high (keyless, 2007+), ranked in its own 5y "
        "range -- high = credit already stressed. Un-caps the credit hypothesis the "
        "battery had to exclude (the keyless HY spread was capped at ~3y). A shock "
        "should ripple harder into HY credit when credit is already stressed."),
    "derived.ovx_pct": (
        "Oil implied-vol (OVX) percentile (5y)", "percentile",
        "Oil-specific risk regime (WS-S amendment). Percentile of OVX, the oil VIX "
        "(keyless, 2007+). Distinct from equity VIX: measures how much oil-risk the "
        "options market is ALREADY pricing. A shock into an already-fearful oil "
        "market may transmit differently than into a complacent one."),
    "derived.real_rate": (
        "10Y real yield (TIPS) percentile (5y)", "percentile",
        "Real-rate regime (WS-S amendment). Percentile of the 10Y TIPS real yield "
        "(keyless, 2003+). Gold and haven assets are real-rate assets -- they should "
        "ripple harder when real rates are LOW (the apt conditioner for gold that "
        "generic VIX-stress was not)."),
    "derived.diesel_crack": (
        "Diesel/heating-oil crack (distillate margin)", "USD/bbl",
        "Value-chain transmission (V1). The refiner's distillate margin: NY Harbor "
        "heating-oil/diesel (x42 gal->bbl) minus WTI crude. The crack IS the crude->fuel "
        "transmission channel -- a widening margin means product tightness is outrunning "
        "crude, i.e. the shock is passing THROUGH to the distillate that moves the real "
        "economy (trucking, farming, heating), not staying in crude. Point-in-time: "
        "same-day prices, no lookahead."),
    "derived.gasoline_crack": (
        "Gasoline crack (consumer-fuel margin)", "USD/bbl",
        "Value-chain transmission (V1). US Gulf Coast wholesale gasoline (x42 gal->bbl) "
        "minus WTI crude -- the crude->pump margin. Distinct from the diesel crack: "
        "gasoline is the consumer/driving-season channel, distillate the industrial one. "
        "Widening = the shock is reaching motor fuel. Point-in-time: same-day prices."),
    "derived.conflict_intensity_pct": (
        "Background conflict intensity (UCDP fatalities) percentile (5y)", "percentile",
        "Verified-conflict regime (UCDP amendment 2026-07-30). Percentile of global "
        "UCDP monthly fatalities (gold-standard vetted data, 1989+) in its own 5y range. "
        "Pre-registered conditioner: a shock landing when background conflict is already "
        "intense may ripple harder into safe-haven assets (gold). POINT-IN-TIME: monthly "
        "data forward-filled to daily, read at t-1 -> sees the last COMPLETED month, never "
        "the current one (no lookahead)."),
}


def load_wide(conn):
    """Pull every SIGNAL-INPUT series into one date-indexed table (one col each).

    CRITICAL: we must NOT let a calendar-daily series (one that carries values on
    weekends too, like the GPR index) into this table. The rolling windows below
    assume a TRADING-DAY index -- LOOKBACK=1260 means '5 years of trading days',
    and rolling(20) volatility needs 20 consecutive trading days. If weekend rows
    leak in, every column gets weekend NaNs: rolling(20) then never sees 20
    non-NaN in a row (brent_vol20 goes all-NaN) and the 1260-row lookbacks shrink
    to ~3.4 calendar-years. So exclude derived.* (outputs) and gpr.* (a
    calendar-daily external measure that is read directly elsewhere, never a
    signal input here)."""
    df = pd.read_sql(
        "SELECT series_id, obs_date, value FROM observations "
        "WHERE series_id NOT LIKE 'derived.%' AND series_id NOT LIKE 'gpr.%'", conn)
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


def seasonal_sigma(s):
    """Deviation from the SEASONAL norm, in standard deviations.

    Inventories are hugely seasonal -- stocks always build in spring and draw in
    summer -- so a plain z-score would just measure the calendar. Instead we
    compare each weekly reading to the SAME week-of-year over the trailing 5
    years: mean and std of the five prior occurrences of that week (shift(1) so
    the current reading never contaminates its own norm -- point-in-time, no
    lookahead). Negative = tighter (lower stocks) than normal for the season.
    """
    s = s.dropna()
    woy = s.index.isocalendar().week.to_numpy()
    df = pd.DataFrame({"val": s.to_numpy(), "woy": woy}, index=s.index)
    grp = df.groupby("woy")["val"]
    # rolling(5) over the same-week history, then shift so it uses the PRIOR
    # five years only; need >=3 to say anything about a seasonal band.
    mean = grp.transform(lambda x: x.rolling(5, min_periods=3).mean().shift(1))
    std = grp.transform(lambda x: x.rolling(5, min_periods=3).std().shift(1))
    return (df["val"] - mean) / std


def build_signals(w):
    """Compute every derived signal. Each line maps to a declared mechanism above."""
    out = pd.DataFrame(index=w.index)
    brent = w.get("fred.DCOILBRENTEU")
    wti = w.get("fred.DCOILWTICO")

    if brent is not None and wti is not None:
        # Compute on the spread's OWN trading-day index (dates where BOTH prices exist), then reindex
        # back to the wide frame. If we computed on the wide union, weekend/holiday rows injected by
        # newer calendar-daily feeds (portwatch/predmkt/wiki) would leave NaN gaps that stall the
        # rolling z-score's tail -- the bug that silently froze this signal ~5 days behind Brent.
        spread = (brent - wti).dropna()
        out["derived.brent_wti_spread"] = spread.reindex(w.index)
        out["derived.brent_wti_spread_z"] = zscore(spread).reindex(w.index)

    if "fred.DGS10" in w and "fred.DGS2" in w:
        out["derived.curve_2s10s"] = w["fred.DGS10"] - w["fred.DGS2"]

    if "fred.DTWEXBGS" in w:
        out["derived.usd_z"] = zscore(w["fred.DTWEXBGS"])

    if "fred.VIXCLS" in w:
        out["derived.vix_pct"] = percentile(w["fred.VIXCLS"])

    if brent is not None:
        # realised volatility: std of daily log returns, annualised -- computed on Brent's OWN
        # trading-day index (dropna) so weekend NaNs from other feeds can't stall the rolling tail,
        # then reindexed back to the wide frame.
        b = brent.dropna()
        r = np.log(b).diff()
        out["derived.brent_vol20"] = (r.rolling(20).std() * np.sqrt(252) * 100).reindex(w.index)

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

    if "eia.crude_stocks_xspr" in w:
        # Weekly stock level on a daily index: compute the seasonal sigma on the
        # native weekly observations, then forward-fill so each day carries the
        # latest known reading -- exactly the ffill discipline cot_pct uses.
        out["derived.inv_sigma"] = (
            seasonal_sigma(w["eia.crude_stocks_xspr"])
            .reindex(w.index).ffill()
        )

    if "fred.T10YIE" in w:
        # 10Y inflation breakeven, ranked in its own 5y range -> the inflation-regime
        # conditioner for the edge battery (keyless FRED, daily from 2003).
        out["derived.be_level"] = percentile(w["fred.T10YIE"])

    if "yf.hyg" in w:
        # Credit-cycle stress from the HYG high-yield ETF: drawdown from the trailing-252d high
        # (own trading-day index, then reindex), ranked in its own 5y range. High = credit stressed.
        hyg = w["yf.hyg"].dropna()
        dd = hyg / hyg.rolling(252, min_periods=126).max() - 1.0     # <= 0
        out["derived.credit_stress"] = percentile(-dd).reindex(w.index)

    if "fred.OVXCLS" in w:
        out["derived.ovx_pct"] = percentile(w["fred.OVXCLS"])        # oil implied-vol regime

    if "fred.DFII10" in w:
        out["derived.real_rate"] = percentile(w["fred.DFII10"])      # real-rate regime (low = haven-supportive)

    # Value-chain cracks (V1): refined-product margin = product ($/gal x42 -> $/bbl) - WTI ($/bbl).
    # Computed on each pair's OWN trading-day index (dropna), then reindexed -- the brent_wti_spread
    # discipline, so weekend NaNs from calendar-daily feeds can't stall the tail. A level, not a
    # rolling stat, so no lookback needed.
    GAL_PER_BBL = 42.0
    if wti is not None and "fred.DHOILNYH" in w:
        diesel_bbl = (w["fred.DHOILNYH"] * GAL_PER_BBL - wti).dropna()
        out["derived.diesel_crack"] = diesel_bbl.reindex(w.index)
    if wti is not None and "fred.DGASUSGULF" in w:
        gaso_bbl = (w["fred.DGASUSGULF"] * GAL_PER_BBL - wti).dropna()
        out["derived.gasoline_crack"] = gaso_bbl.reindex(w.index)

    if "ucdp.fat_global" in w:
        # UCDP is monthly: rank each month's fatalities in its own 5y (~60-month) window, then forward-
        # fill so each day carries the latest COMPLETED month's percentile. t-1 reads the prior month
        # (point-in-time: a shock's day never sees its own month's not-yet-complete total).
        u = w["ucdp.fat_global"].dropna()
        pct = u.rolling(60, min_periods=12).rank(pct=True).mul(100)
        out["derived.conflict_intensity_pct"] = pct.reindex(w.index).ffill()

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
