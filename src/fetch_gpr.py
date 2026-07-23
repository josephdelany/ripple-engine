"""
fetch_gpr.py -- the Geopolitical Risk (GPR) index, an EXTERNAL salience yardstick.

WHAT GPR IS (and why we want it):
The GPR index (Caldara & Iacoviello, 2022, American Economic Review) counts the
share of major-newspaper articles each day that discuss adverse geopolitical
events -- wars, terror, tension, military build-ups. It is the field-standard,
peer-reviewed measure of "how much geopolitical risk was in the air." We load it
for ONE reason in this brief: to independently check our hand-built event list.
If our 42 events line up with GPR spikes, our selection isn't just our own
judgement; if some events sit at low GPR, that is an honest selection-bias flag
to discuss (FRONTIER_AUDIT F4). No conditioning is done here -- data only.

DATA SOURCE (public file, no key):
The daily series, straight from the authors' site:
  https://www.matteoiacoviello.com/gpr_files/data_gpr_daily_recent.xls
It carries the daily headline GPRD plus the GPRD_ACT (realised acts) and
GPRD_THREAT (threats) sub-indices, dated back to 1985. We load all three.

POINT-IN-TIME: GPR is revised as the text corpus and method are updated, so we
stamp every row's as_of with the FETCH date (not the observation date) and keep a
single latest vintage (each fetch replaces the series). That way the stored data
is honestly labelled "this is the vintage we pulled on <date>."

If the download fails or the file's columns aren't what we expect, this STOPS and
says so -- it never scrapes an alternative or hand-enters numbers.

Run:  python3 src/fetch_gpr.py
"""

import io
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"

GPR_URL = "https://www.matteoiacoviello.com/gpr_files/data_gpr_daily_recent.xls"
SOURCE = "Caldara & Iacoviello, Geopolitical Risk index (matteoiacoviello.com)"

# The GPR entity these series hang off (a macro measure, not a priceable asset).
ENTITY = ("macro.geopolitics", "macro", "Geopolitical Risk",
          "Caldara-Iacoviello GPR: newspaper-based geopolitical risk index")

# (column in the file, series_id, human name). Headline first, then sub-indices.
SERIES_DEFS = [
    ("GPRD",        "gpr.GPRD",        "Geopolitical Risk Index (daily, headline)"),
    ("GPRD_ACT",    "gpr.GPRD_ACT",    "Geopolitical Risk Index (daily, realised acts)"),
    ("GPRD_THREAT", "gpr.GPRD_THREAT", "Geopolitical Risk Index (daily, threats)"),
]
# Columns we require to be present; a mismatch means STOP, not improvise.
REQUIRED_COLS = {"date", "GPRD", "GPRD_ACT", "GPRD_THREAT"}


def main():
    fetch_date = datetime.now(timezone.utc).date().isoformat()          # as_of (vintage)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")      # retrieved_at

    # 1. Download the daily file.
    try:
        r = requests.get(GPR_URL, headers={"User-Agent": "ripple-engine"}, timeout=90)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"STOP: could not download GPR daily file ({type(e).__name__}: {e}).")
        print(f"URL: {GPR_URL}  -- do not scrape an alternative; tell Joe.")
        return

    # 2. Parse and VALIDATE the format before touching the database.
    try:
        df = pd.read_excel(io.BytesIO(r.content))
    except Exception as e:
        print(f"STOP: GPR file could not be parsed as Excel ({type(e).__name__}: {e}).")
        return
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        print(f"STOP: GPR file format changed -- missing expected columns {missing}.")
        print(f"Found: {list(df.columns)}. Not guessing; tell Joe.")
        return
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # 3. Register the entity + the three series.
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO entities VALUES (?,?,?,?)", ENTITY)

    total = 0
    for col, series_id, name in SERIES_DEFS:
        cur.execute(
            "INSERT OR REPLACE INTO series VALUES (?,?,?,?,?,?,?,?)",
            (series_id, name, ENTITY[0], "index", "daily", SOURCE, GPR_URL,
             "External geopolitical-risk salience measure (Caldara-Iacoviello). "
             "Loaded for event-list validation only; not a conditioner."))

        sub = df[["date", col]].dropna()
        # Replace the whole series each fetch: GPR revises, so we keep one vintage,
        # stamped with the fetch date as as_of (point-in-time honesty).
        cur.execute("DELETE FROM observations WHERE series_id = ?", (series_id,))
        payload = [
            (series_id, d.strftime("%Y-%m-%d"), float(v), fetch_date, now)
            for d, v in zip(sub["date"], sub[col])
        ]
        cur.executemany("INSERT OR REPLACE INTO observations VALUES (?,?,?,?,?)", payload)
        total += len(payload)
        print(f"  {series_id:<18} {len(payload):>6,} obs  "
              f"{sub['date'].min().date()} to {sub['date'].max().date()}")

    conn.commit()
    conn.close()
    print(f"\nLoaded {total:,} GPR observations (as_of {fetch_date}). "
          f"Next: python3 src/validate_gpr.py")


if __name__ == "__main__":
    main()
