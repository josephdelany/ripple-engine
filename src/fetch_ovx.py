"""
fetch_ovx.py -- the market's IMPLIED oil volatility (OVX), keyless (Pillar 1).

OVX is the CBOE Crude Oil Volatility Index -- options-implied expected 30-day Brent/WTI vol.
It is the cleanest single instrument for "what the market has PRICED" about oil turbulence, which
is exactly the counterpart the gap engine needs (market-as-null). Free & keyless from FRED
(OVXCLS), daily back to 2007. New data = new rows in the existing observations table.

Run:  python3 src/fetch_ovx.py
"""

import io
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=OVXCLS"


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    r = requests.get(FRED, timeout=30)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df.columns = ["date", "value"]
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna()

    conn = sqlite3.connect(DB)
    conn.execute("INSERT OR IGNORE INTO entities VALUES (?,?,?,?)",
                 ("macro.oil_vol", "macro", "Oil Implied Volatility", "CBOE OVX"))
    conn.execute("INSERT OR REPLACE INTO series VALUES (?,?,?,?,?,?,?,?)",
                 ("fred.OVXCLS", "CBOE Crude Oil Volatility Index (OVX)", "macro.oil_vol",
                  "index", "daily", "FRED", "https://fred.stlouisfed.org/series/OVXCLS",
                  "Options-implied 30-day oil volatility -- what the market has PRICED (the gap's null)."))
    payload = [("fred.OVXCLS", d, float(v), d, now) for d, v in zip(df["date"], df["value"])]
    conn.executemany("INSERT OR IGNORE INTO observations VALUES (?,?,?,?,?)", payload)
    conn.commit()
    n = conn.execute("SELECT COUNT(*) FROM observations WHERE series_id='fred.OVXCLS'").fetchone()[0]
    conn.close()
    print(f"fetch_ovx -- OVX loaded: {len(payload):,} rows fetched, {n:,} in DB, "
          f"{df['date'].min()} .. {df['date'].max()}")


if __name__ == "__main__":
    main()
