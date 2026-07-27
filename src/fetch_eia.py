"""
fetch_eia.py -- EIA weekly crude inventories: the H2 physical-tightness data.

WHY (this is the H2 data):
The pre-registered hypothesis H2 says a geopolitical shock lands harder when the
physical market has no cushion. The cleanest public gauge of that cushion is how
much crude the US is actually holding in tank. When stocks sit below their
seasonal norm, there is no buffer to absorb a supply scare, so the price has to
do the absorbing instead. This adapter pulls the raw stock level; the seasonal
"tightness" signal is derived from it later in derive_signals.py.

DATA SOURCE (free, needs a key):
EIA Open Data v2 API. The series is WCESTUS1 -- "Weekly US Ending Stocks
excluding SPR of Crude Oil (Thousand Barrels)". The v2 API addresses legacy
series through the /seriesid/ route using the old fully-qualified id
"PET.WCESTUS1.W" (product PET, series WCESTUS1, weekly). The API key lives in
~/.openbb_platform/user_settings.json under credentials.eia_api_key -- we read it
from there, we never hard-code it and never print it.

Writes one series into the canonical schema:  eia.crude_stocks_xspr
(US crude stocks excluding the Strategic Petroleum Reserve, weekly, thousand bbl)

Run:  python3 src/fetch_eia.py
"""

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"

# EIA v2 "seriesid" route resolves the legacy fully-qualified id for WCESTUS1.
EIA_URL = "https://api.eia.gov/v2/seriesid/PET.WCESTUS1.W"
SETTINGS = Path.home() / ".openbb_platform" / "user_settings.json"

SERIES_ID = "eia.crude_stocks_xspr"
SERIES_ROW = (
    SERIES_ID,
    "US Ending Stocks of Crude Oil excluding SPR",
    "commodity.wti",
    "thousand bbl",
    "weekly",
    "EIA",
    "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=WCESTUS1&f=W",
    "H2 conditioning input: thin physical buffers cannot absorb supply risk, so price must",
)


def read_api_key():
    """Pull the EIA key. In CI (GitHub Actions) it comes from the EIA_API_KEY
    environment variable, sourced from an encrypted repo Secret -- so the key is
    never committed. Locally it comes from OpenBB's settings file. Fail loudly if
    neither is present."""
    env_key = os.environ.get("EIA_API_KEY")
    if env_key:
        return env_key.strip()
    if not SETTINGS.exists():
        raise SystemExit(f"STOP: settings file not found at {SETTINGS}. Tell Joe.")
    creds = json.load(open(SETTINGS)).get("credentials", {})
    key = creds.get("eia_api_key")
    if not key:
        raise SystemExit(
            "STOP: credentials.eia_api_key missing from user_settings.json. "
            "Tell Joe -- do not work around it, do not scrape."
        )
    return key


def fetch_all(key):
    """Page through the v2 API until we've collected every weekly observation."""
    rows, offset = [], 0
    while True:
        r = requests.get(
            EIA_URL,
            params={"api_key": key, "offset": offset, "length": 5000},
            timeout=60,
        )
        r.raise_for_status()
        resp = r.json()["response"]
        total = int(resp["total"])
        batch = resp["data"]
        if not batch:
            break
        rows.extend(batch)
        offset += len(batch)
        if offset >= total:
            break
    return rows


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    key = read_api_key()

    raw = fetch_all(key)
    # Keep only (date, value) pairs with a real reading; the API dates are the
    # week-ending Friday, which IS the point-in-time the number refers to.
    clean = {}
    for row in raw:
        period, value = row.get("period"), row.get("value")
        if period and value is not None:
            clean[period] = float(value)  # dict de-dupes any repeated period
    data = sorted(clean.items())
    if not data:
        print("Nothing returned from EIA -- check the key and connection, then retry.")
        return
    print(f"Fetched {len(data):,} weekly observations, "
          f"{data[0][0]} to {data[-1][0]}")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO series VALUES (?,?,?,?,?,?,?,?)", SERIES_ROW)
    payload = [(SERIES_ID, d, v, d, now) for d, v in data]
    cur.executemany("INSERT OR REPLACE INTO observations VALUES (?,?,?,?,?)", payload)
    conn.commit()

    total = cur.execute(
        "SELECT COUNT(*) FROM observations WHERE series_id = ?", (SERIES_ID,)
    ).fetchone()[0]
    print(f"Saved {total:,} rows as {SERIES_ID}. "
          f"Next: python3 src/derive_signals.py to compute the seasonal tightness signal.")
    conn.close()


if __name__ == "__main__":
    main()
