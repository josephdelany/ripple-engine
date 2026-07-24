"""
fetch_series.py -- the ingestion ADAPTER that makes the engine multi-variable.

This is the depth upgrade. Until now the database held one thing: price.
Price alone can only tell you THAT oil moved. To know WHY a ripple was big or
small, you need the state of the system around it -- inventories, the dollar,
rates, volatility. Those are the MODULATORS.

Note what this script does NOT do: it does not add a single table. Six new data
series drop straight into the existing `series` + `observations` schema. That is
the architecture working as designed -- new data = new rows, never new structure.

Every series below is free and keyless from FRED.

Run:  python3 src/fetch_series.py
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

# (fred_id, entity_id, human name, unit, frequency, why it matters)
CATALOG = [
    ("WCESTUS1",  "commodity.wti",   "US Crude Oil Stocks",        "thousand bbl", "weekly",
     "Physical buffer. Thin inventories amplify any supply shock."),
    ("DHHNGSP",   "commodity.natgas","Henry Hub Natural Gas Spot", "USD/MMBtu",    "daily",
     "Energy complex co-movement; gas often reacts to the same shocks."),
    ("DTWEXBGS",  "macro.usd",       "Broad US Dollar Index",      "index",        "daily",
     "Oil is priced in dollars. A strong dollar dampens commodity moves."),
    ("DGS10",     "macro.rates",     "10-Year Treasury Yield",     "percent",      "daily",
     "Macro regime + the risk-free backdrop shocks land against."),
    ("DGS2",      "macro.rates",     "2-Year Treasury Yield",      "percent",      "daily",
     "With the 10Y gives the 2s10s curve -- a regime signal."),
    ("DGS5",      "macro.rates",     "5-Year Treasury Yield",      "percent",      "daily",
     "The belly of the curve -- a cross-asset reaction target (TASK_BRIEF_10)."),
    ("VIXCLS",    "macro.vol",       "CBOE Volatility Index",      "index",        "daily",
     "Risk appetite. Shocks transmit harder when volatility is already elevated."),
    ("GASREGW",   "commodity.gasoline", "US Regular Retail Gasoline", "USD/gallon", "weekly",
     "Pass-through to the pump: does an oil shock reach retail gasoline? (TASK_BRIEF_11)"),
]

ENTITIES = [
    ("commodity.natgas", "commodity", "Natural Gas",        "Henry Hub benchmark"),
    ("macro.usd",        "macro",     "US Dollar",          "Broad trade-weighted index"),
    ("macro.rates",      "macro",     "US Treasury Yields", "Risk-free curve"),
    ("macro.vol",        "macro",     "Equity Volatility",  "VIX"),
    ("commodity.gasoline","commodity", "Retail Gasoline",   "US regular retail, weekly"),
]


def fetch(sid):
    """Download one FRED series as a tidy (date, value) table."""
    r = requests.get(FRED.format(sid=sid), timeout=30)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")  # "." -> missing
    return df.dropna()


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO entities VALUES (?,?,?,?)", ENTITIES)

    for sid, entity, name, unit, freq, why in CATALOG:
        series_id = f"fred.{sid}"
        print(f"Downloading {name} ({sid}) ...")
        try:
            df = fetch(sid)
        except Exception as e:
            print(f"  ! failed: {e}")
            continue

        cur.execute(
            "INSERT OR REPLACE INTO series VALUES (?,?,?,?,?,?,?,?)",
            (series_id, name, entity, unit, freq, "FRED",
             f"https://fred.stlouisfed.org/series/{sid}", why),
        )
        payload = [
            (series_id, d.strftime("%Y-%m-%d"), float(v), d.strftime("%Y-%m-%d"), now)
            for d, v in zip(df["date"], df["value"])
        ]
        cur.executemany("INSERT OR IGNORE INTO observations VALUES (?,?,?,?,?)", payload)
        print(f"  {len(payload):,} rows, {df['date'].min().date()} to {df['date'].max().date()}")

    conn.commit()

    print("\nThe database now holds these series:")
    rows = cur.execute(
        "SELECT s.series_id, s.name, s.frequency, COUNT(o.value) "
        "FROM series s LEFT JOIN observations o ON o.series_id = s.series_id "
        "GROUP BY s.series_id ORDER BY s.series_id"
    ).fetchall()
    for sid, name, freq, n in rows:
        print(f"  {sid:<24} {name:<28} {freq:<8} {n:>8,} obs")
    total = cur.execute("SELECT COUNT(*) FROM observations").fetchone()[0]
    print(f"\nTotal observations: {total:,}  (no new tables were needed)")
    conn.close()


if __name__ == "__main__":
    main()
