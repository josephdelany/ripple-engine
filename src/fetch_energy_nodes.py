"""
fetch_energy_nodes.py -- add the downstream energy-spine nodes, keyless (Step 1).

The propagation network needs nodes to connect. These extend the spine PAST crude, into the two
channels analysts actually care about downstream of an oil shock:
  - Heating oil / diesel (DHOILNYH) -- the refined-fuel / logistics-cost channel (a supply-chain node).
  - 5Y & 10Y inflation breakevens (T5YIE, T10YIE) -- the macro channel (does the shock reprice
    inflation expectations? the rates analyst's node).
All keyless from FRED (verified). New data = new rows in observations; no schema change.
(Note: a clean keyless European gas / TTF series was NOT available on FRED -- an honest coverage
gap; Henry Hub gas is already in the corpus as the gas node.)

Run:  python3 src/fetch_energy_nodes.py
"""

import io
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"

# (fred_id, entity_id, name, unit, why)
CATALOG = [
    ("DHOILNYH", "commodity.diesel", "No.2 Heating Oil / Diesel (NY Harbor)", "USD/gal",
     "Refined-fuel / logistics-cost node: does a crude shock pass through to distillate?"),
    ("T5YIE", "macro.inflation", "5-Year Breakeven Inflation", "percent",
     "Macro node: does the shock reprice 5Y inflation expectations?"),
    ("T10YIE", "macro.inflation", "10-Year Breakeven Inflation", "percent",
     "Macro node: 10Y inflation expectations -- the rates channel of an energy shock."),
    ("DFII10", "macro.rates", "10-Year TIPS Real Yield", "percent",
     "Real-rate regime conditioner (keyless, 2003+): gold/haven assets ripple harder when real "
     "rates are low. Used to build derived.real_rate for the edge battery."),
]
ENTITIES = [
    ("commodity.diesel", "commodity", "Diesel / Heating Oil", "NY Harbor No.2 distillate"),
    ("macro.inflation", "macro", "Inflation Expectations", "TIPS breakeven inflation"),
    ("macro.rates", "macro", "Real Rates", "TIPS real yields"),
]


def _fetch(sid):
    r = requests.get(FRED.format(sid=sid), timeout=30)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df.columns = ["date", "value"]
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna()


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn = sqlite3.connect(DB)
    conn.executemany("INSERT OR IGNORE INTO entities VALUES (?,?,?,?)", ENTITIES)
    for sid, entity, name, unit, why in CATALOG:
        series_id = f"fred.{sid}"
        try:
            df = _fetch(sid)
        except Exception as e:
            print(f"  ! {sid} failed: {e}"); continue
        conn.execute("INSERT OR REPLACE INTO series VALUES (?,?,?,?,?,?,?,?)",
                     (series_id, name, entity, unit, "daily", "FRED",
                      f"https://fred.stlouisfed.org/series/{sid}", why))
        payload = [(series_id, d, float(v), d, now) for d, v in zip(df["date"], df["value"])]
        conn.executemany("INSERT OR IGNORE INTO observations VALUES (?,?,?,?,?)", payload)
        print(f"  {series_id:<16} {len(payload):>6,} rows  {df['date'].min()} .. {df['date'].max()}")
    conn.commit()
    conn.close()
    print("energy-spine nodes loaded (keyless).")


if __name__ == "__main__":
    main()
