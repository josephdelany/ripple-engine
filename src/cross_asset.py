"""
cross_asset.py -- the EDGES layer: the same 42 shocks, measured beyond oil.

WHY THIS EXISTS (FRONTIER_AUDIT F7):
Everything so far measured one market: oil. But a geopolitical shock ripples
through the whole complex -- natural gas, the dollar, Treasury yields. Measuring
those together is the first step from an "oil engine" to a general reaction
engine, and it is the honest external-validity check: if a shock that moved oil
also moved gas and yields in sensible directions, the signal is real; if oil
moved alone, be suspicious.

WHAT IT DOES:
For each event and each target asset it runs the SAME constant-mean event study
as the oil study (imported from event_study.py -- not re-implemented), over the
same windows (estimation t-130..t-11, event t-5..t+20). The only difference is
the unit of "return":
  * PRICE assets (oil, gas, the dollar index): daily LOG returns -> CAR in %.
  * YIELD assets (5Y, 10Y Treasuries): daily CHANGES in the level, in BASIS
    POINTS (1 percentage point = 100 bps) -> CAR in bps. A yield is already a
    rate, so a log return would be meaningless; the change in the rate is the move.
Every number below is labelled with its unit, because mixing % and bps silently
is exactly how a cross-asset table lies.

THIS IS A MEASUREMENT LAYER -- DESCRIPTIVE ONLY. No hypotheses, no verdicts, no
amplifiers. Conditioning any of these ripples on market state would need a future
REGISTERED hypothesis (Joe's gate); nothing here does that.

Writes one row per (event, asset) into the `edges` table (finally earning its
place) and a human propagation map to data/cross_asset_results.txt.

Run:  python3 src/cross_asset.py
"""

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

# Import only -- the CAR math and clustering come from the tested modules.
from event_study import car_for_event, PRE, POST
from robustness import assign_clusters
from load_events import VALID_TYPES

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "cross_asset_results.txt"

# The target markets. 'price' -> log returns, % ; 'yield' -> level change, bps.
ASSETS = [
    {"series": "fred.DCOILBRENTEU", "label": "Brent oil",  "entity": "commodity.brent",
     "kind": "price", "unit": "%"},
    {"series": "fred.DHHNGSP",      "label": "HH natgas",  "entity": "commodity.natgas",
     "kind": "price", "unit": "%"},
    {"series": "fred.DTWEXBGS",     "label": "Broad USD",  "entity": "macro.usd",
     "kind": "price", "unit": "%"},
    {"series": "fred.DGS5",         "label": "5Y yield",   "entity": "macro.rates",
     "kind": "yield", "unit": "bps"},
    {"series": "fred.DGS10",        "label": "10Y yield",  "entity": "macro.rates",
     "kind": "yield", "unit": "bps"},
    # Downstream energy-spine nodes (Step 1): the refined-fuel channel and the macro/inflation
    # channel a crude shock propagates INTO -- the nodes the propagation network connects to.
    {"series": "fred.DHOILNYH",     "label": "Heating oil",  "entity": "commodity.diesel",
     "kind": "price", "unit": "%"},
    {"series": "fred.T5YIE",        "label": "5Y breakeven", "entity": "macro.inflation",
     "kind": "yield", "unit": "bps"},
    {"series": "fred.T10YIE",       "label": "10Y breakeven", "entity": "macro.inflation",
     "kind": "yield", "unit": "bps"},
    # Gasoline is WEEKLY -- measured on a weekly clock (+1/+2/+4 WEEKS), never
    # pretended to be daily. Its car5/car20 slots hold +1 week / +4 weeks.
    {"series": "fred.GASREGW",      "label": "Gasoline",   "entity": "commodity.gasoline",
     "kind": "weekly", "unit": "%"},
]

# Trading days the CAR+20 accumulates over (t-5..t+20 inclusive) -- recorded as
# provenance in each edge row (daily assets only).
N_DAYS = PRE + POST + 1

# Weekly gasoline event study: a constant-mean model on WEEKLY returns.
EST_WEEKS = 26           # ~ the weekly equivalent of the daily t-130..t-11 window
GAP_WEEKS = 1            # small gap before the event (mirrors the daily t-11 gap)
WEEKLY_HORIZONS = (1, 2, 4)   # weeks after the last weekly reading before the event

SMALL_N_ANECDOTE = 3   # shout at or below this, same as the scenario playbook


def asset_returns(conn, series_id, kind):
    """Build the daily 'return' series for one asset, in its natural unit.
    Returns None if the series is absent."""
    df = pd.read_sql(
        "SELECT obs_date, value FROM observations WHERE series_id = ? ORDER BY obs_date",
        conn, params=[series_id])
    if df.empty:
        return None
    df["obs_date"] = pd.to_datetime(df["obs_date"])
    s = df.set_index("obs_date")["value"].sort_index().dropna()
    if kind in ("price", "weekly"):
        # log returns; for a weekly series the consecutive diff IS the weekly return
        return np.log(s).diff().dropna()
    return s.diff().dropna() * 100                  # yield change in basis points


def weekly_car(returns, event_date):
    """Weekly constant-mean CAR at +1/+2/+4 WEEKS from the last weekly reading
    before the event. This is a WEEKLY clock -- do not read the horizons as days.
    Returns {1: %, 2: %, 4: %} (log-return CAR) or None if too little weekly history."""
    dates = returns.index
    start = dates.searchsorted(pd.Timestamp(event_date))   # first weekly return on/after event
    max_h = max(WEEKLY_HORIZONS)
    if start - GAP_WEEKS - EST_WEEKS < 0 or start + max_h > len(dates):
        return None
    mu = returns.iloc[start - GAP_WEEKS - EST_WEEKS: start - GAP_WEEKS].mean()
    cum = (returns.iloc[start: start + max_h] - mu).cumsum().to_numpy()
    return {h: float(cum[h - 1]) * 100 for h in WEEKLY_HORIZONS}


def build_table(conn):
    """One row per event, with CAR+5/+20 (in DISPLAY units) for every asset.
    NaN where an asset lacks enough history around that event (reported honestly)."""
    events = pd.read_sql(
        "SELECT event_id, event_date AS date, type FROM events ORDER BY event_date", conn)
    returns = {a["series"]: asset_returns(conn, a["series"], a["kind"]) for a in ASSETS}

    rows = []
    for _, ev in events.iterrows():
        row = {"event_id": ev["event_id"], "date": ev["date"], "type": ev["type"]}
        for a in ASSETS:
            ret = returns[a["series"]]
            if a["kind"] == "weekly":                       # gasoline: weekly clock
                wc = weekly_car(ret, ev["date"]) if ret is not None else None
                row[f"{a['series']}_car5"] = np.nan if wc is None else wc[1]   # +1 week
                row[f"{a['series']}_car20"] = np.nan if wc is None else wc[4]  # +4 weeks
                row[f"{a['series']}_car2w"] = np.nan if wc is None else wc[2]  # +2 weeks
                continue
            car = car_for_event(ret, ev["date"]) if ret is not None else None
            if car is None:
                row[f"{a['series']}_car5"] = np.nan
                row[f"{a['series']}_car20"] = np.nan
            else:
                scale = 100 if a["kind"] == "price" else 1   # log->%, bps already scaled
                row[f"{a['series']}_car5"] = car[PRE + 5] * scale
                row[f"{a['series']}_car20"] = car[PRE + 20] * scale
        rows.append(row)
    return assign_clusters(pd.DataFrame(rows))     # adds a 'cluster' column


# ----------------------------------------------------------------- edges table

def ensure_edge_columns(conn):
    """Add the cross-asset measurement columns to `edges` if they aren't there
    yet -- the same ALTER TABLE migration pattern init_db.py uses. The original
    Chain-Library columns are left intact for future use."""
    have = {r[1] for r in conn.execute("PRAGMA table_info(edges)")}
    for col, coltype in [("event_id", "TEXT"), ("target_series", "TEXT"),
                         ("car5", "REAL"), ("car20", "REAL"),
                         ("units", "TEXT"), ("n_days", "INTEGER")]:
        if col not in have:
            conn.execute(f"ALTER TABLE edges ADD COLUMN {col} {coltype}")


def populate_edges(conn, table):
    """One edge row per (event, asset) with a real reaction. Replaces prior
    cross-asset rows (target_series NOT NULL); never touches Chain-Library rows."""
    ensure_edge_columns(conn)
    conn.execute("DELETE FROM edges WHERE target_series IS NOT NULL")
    written = 0
    for _, r in table.iterrows():
        for a in ASSETS:
            c5, c20 = r[f"{a['series']}_car5"], r[f"{a['series']}_car20"]
            if pd.isna(c20):
                continue
            weekly = a["kind"] == "weekly"
            conn.execute(
                "INSERT INTO edges (to_entity, mechanism, event_id, target_series, "
                "car5, car20, units, n_days) VALUES (?,?,?,?,?,?,?,?)",
                (a["entity"], "cross-asset event-study reaction (descriptive)",
                 r["event_id"], a["series"], round(float(c5), 2), round(float(c20), 2),
                 "% (WEEKLY: car5=+1wk, car20=+4wk)" if weekly else a["unit"],
                 max(WEEKLY_HORIZONS) if weekly else N_DAYS))
            written += 1
    conn.commit()
    return written


# ------------------------------------------------------------- propagation map

def propagation_summary(table):
    """Clustered mean reaction per event type x asset (same clustering as
    robustness.py: collapse events within the window, keep the first)."""
    clustered = table.groupby("cluster").first().reset_index()
    types = [t for t in sorted(VALID_TYPES)
             if (clustered["type"] == t).any()]
    summary = {}
    for t in types:
        grp = clustered[clustered["type"] == t]
        cells = {}
        for a in ASSETS:
            c5 = grp[f"{a['series']}_car5"].dropna()
            c20 = grp[f"{a['series']}_car20"].dropna()
            cells[a["series"]] = {
                "car5": round(float(c5.mean()), 1) if len(c5) else None,
                "car20": round(float(c20.mean()), 1) if len(c20) else None,
                "n": int(len(c20)),
            }
        summary[t] = {"n_type": int(len(grp)), "cells": cells}
    return summary


def _cell(v, unit):
    return "   n/a " if v is None else f"{v:+6.1f}{unit}"


def write_results(table, summary):
    L = []
    w = L.append
    n_events = int(table["event_id"].nunique())
    w("=" * 100)
    w(f"CROSS-ASSET PROPAGATION MAP -- the {n_events} registered shocks measured "
      f"beyond oil (DESCRIPTIVE, no verdicts)")
    w("=" * 100)
    w("Same constant-mean event study and windows as the oil study; clustered "
      "(overlapping events collapsed, first kept).")
    w("Units: PRICE assets (Brent, natgas, USD) in % (log-return CAR); YIELD assets "
      "(5Y, 10Y) in bps (CAR of daily level changes).")
    w("GASOLINE is WEEKLY, on its own clock: its CAR+5 column = +1 WEEK and its "
      "CAR+20 column = +4 WEEKS (in %). Not daily -- see the gasoline appendix for "
      "+1/+2/+4 weeks.")
    w("Coverage note: natgas begins 1997, the broad-dollar index 2006, weekly "
      "retail gasoline 1990 -- earlier events show n/a, honestly.")
    w("")

    hdr = f"  {'event type':<24}{'n':>3}  " + "".join(
        f"{a['label']:>12}" for a in ASSETS)
    for horizon in ("car20", "car5"):
        w(f"CLUSTERED MEAN {'CAR+20' if horizon == 'car20' else 'CAR+5'} "
          f"by event type x asset:")
        w(hdr)
        w("  " + "-" * (29 + 12 * len(ASSETS)))
        for t, info in summary.items():
            line = f"  {t:<24}{info['n_type']:>3}  "
            for a in ASSETS:
                cell = info["cells"][a["series"]][horizon]
                line += f"{_cell(cell, a['unit']):>12}"
            w(line)
        w("")
    # honest small-n reminder, computed
    small = sorted({t for t, info in summary.items() if info["n_type"] <= SMALL_N_ANECDOTE})
    if small:
        w(f"SMALL-n WARNING: event types with n<= {SMALL_N_ANECDOTE} clustered "
          f"episodes are ANECDOTE, NOT STATISTICS: {', '.join(small)}")
        w("")

    # --- Gasoline pass-through appendix (weekly clock: +1 / +2 / +4 weeks) ---
    w("=" * 100)
    w("GASOLINE PASS-THROUGH TO THE PUMP -- clustered mean retail-gasoline CAR by "
      "event type (WEEKLY, %)")
    w("=" * 100)
    gclust = table.groupby("cluster").first().reset_index()
    w(f"  {'event type':<24}{'n':>3}{'+1 week':>10}{'+2 weeks':>10}{'+4 weeks':>10}")
    w("  " + "-" * 57)
    for t in [x for x in sorted(VALID_TYPES) if (gclust['type'] == x).any()]:
        grp = gclust[gclust["type"] == t]
        c1, c2, c4 = (grp["fred.GASREGW_car5"].dropna(),
                      grp["fred.GASREGW_car2w"].dropna(),
                      grp["fred.GASREGW_car20"].dropna())
        if len(c4):
            w(f"  {t:<24}{len(c4):>3}{c1.mean():>+9.1f}%{c2.mean():>+9.1f}%{c4.mean():>+9.1f}%")
        else:
            w(f"  {t:<24}{0:>3}{'n/a':>10}{'n/a':>10}{'n/a':>10}")
    w("")

    # --- September 11 appendix: the flight-to-safety canary ---
    w("=" * 100)
    w("APPENDIX -- September 11, 2001 (flight-to-safety canary: assets should "
      "react in DIFFERENT directions)")
    w("=" * 100)
    row = table[table["event_id"] == "september_11_attacks_2001"]
    if row.empty:
        w("  september_11_attacks_2001 not found in the event set.")
    else:
        r = row.iloc[0]
        w(f"  {'asset':<14}{'CAR+5':>12}{'CAR+20':>12}   unit")
        w("  " + "-" * 52)
        for a in ASSETS:
            c5, c20 = r[f"{a['series']}_car5"], r[f"{a['series']}_car20"]
            c5s = "n/a" if pd.isna(c5) else f"{c5:+.1f}"
            c20s = "n/a" if pd.isna(c20) else f"{c20:+.1f}"
            w(f"  {a['label']:<14}{c5s:>12}{c20s:>12}   {a['unit']}")
        w("")
        w("  Read (descriptive): a genuine flight-to-safety shows up as yields "
          "FALLING (negative bps) while")
        w("  oil and equities-linked assets move the other way -- the assets "
          "parting company is the signal.")
    w("")
    w("DESCRIPTIVE MEASUREMENT ONLY. Conditioning any of these reactions on "
      "market state would require a")
    w("future REGISTERED hypothesis (Joe's gate). Nothing here is a verdict.")

    OUT.write_text("\n".join(L) + "\n")
    return "\n".join(L)


def main():
    conn = sqlite3.connect(DB)
    table = build_table(conn)
    n_edges = populate_edges(conn, table)
    conn.close()
    summary = propagation_summary(table)
    text = write_results(table, summary)
    print(text)
    print(f"\nWrote {OUT}  |  populated {n_edges} edge rows (one per event x asset).")


if __name__ == "__main__":
    main()
