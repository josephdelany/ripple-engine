"""
fetch_eia_fundamentals.py -- the physical oil "material": Cushing, refinery runs, SPR.

The engine tracked one physical gauge (total crude stocks, for H2). This fills out
the supply picture with three more official EIA weekly series -- all STATS-SAFE
(free, official, point-in-time, redistributable), so unlike the news/odds signals
these could be promoted to registered variables:

  eia.cushing_stocks  -- Cushing, OK crude storage (the WTI delivery point; drives
                         the WTI term structure and the Brent-WTI spread).
  eia.refinery_util   -- US refinery % utilization (a drop is the cleanest free
                         proxy for refinery OUTAGES -- runs falling = crude backing up).
  eia.spr_stocks      -- Strategic Petroleum Reserve crude (releases add supply;
                         refills pull it).

Same EIA v2 /seriesid/ route and key handling as fetch_eia.py (key from the
EIA_API_KEY env / user_settings.json, never printed, never committed).

Run:  python3 src/fetch_eia_fundamentals.py
"""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import requests

from fetch_eia import read_api_key       # reuse the exact key handling

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"

# (series_id, legacy EIA id, name, entity, unit, notes)
SERIES = [
    ("eia.cushing_stocks", "PET.W_EPC0_SAX_YCUOK_MBBL.W",
     "Cushing OK Ending Stocks of Crude Oil", "commodity.wti", "thousand bbl",
     "WTI physical delivery point; drives term structure + Brent-WTI spread"),
    ("eia.refinery_util", "PET.WPULEUS3.W",
     "US Percent Utilization of Refinery Operable Capacity", "commodity.wti",
     "percent", "refinery-run intensity; a drop is the free refinery-OUTAGE proxy"),
    ("eia.spr_stocks", "PET.WCSSTUS1.W",
     "US SPR Ending Stocks of Crude Oil", "commodity.wti", "thousand bbl",
     "Strategic Petroleum Reserve; releases add supply, refills pull it"),
]
URL = "https://api.eia.gov/v2/seriesid/{}"


def fetch_series(key, legacy_id):
    """All weekly (period, value) pairs for one legacy EIA series, deduped."""
    rows, offset = {}, 0
    while True:
        r = requests.get(URL.format(legacy_id),
                         params={"api_key": key, "offset": offset, "length": 5000},
                         timeout=60)
        r.raise_for_status()
        resp = r.json()["response"]
        batch = resp["data"]
        for row in batch:
            p, v = row.get("period"), row.get("value")
            if p and v is not None:
                rows[p] = float(v)
        offset += len(batch)
        if not batch or offset >= int(resp["total"]):
            break
    return sorted(rows.items())


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    key = read_api_key()
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    for sid, legacy, name, entity, unit, notes in SERIES:
        try:
            data = fetch_series(key, legacy)
        except requests.RequestException as e:
            print(f"  {sid} failed ({type(e).__name__}) -- skipped.")
            continue
        if not data:
            print(f"  {sid}: nothing returned -- skipped.")
            continue
        cur.execute("INSERT OR REPLACE INTO series VALUES (?,?,?,?,?,?,?,?)",
                    (sid, name, entity, unit, "weekly", "EIA",
                     "https://www.eia.gov/petroleum/", notes))
        cur.executemany("INSERT OR REPLACE INTO observations VALUES (?,?,?,?,?)",
                        [(sid, d, v, d, now) for d, v in data])
        conn.commit()
        print(f"  {sid:<22} {len(data):>4} obs, latest {data[-1][0]} = {data[-1][1]:g}")
    conn.close()
    print("fetch_eia_fundamentals -- Cushing / refinery util / SPR updated.")


if __name__ == "__main__":
    main()
