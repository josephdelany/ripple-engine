"""
fetch_fred_alfred.py -- point-in-time macro VINTAGES from ALFRED, keyless (Step 7).

FRED gives you today's (revised) value of a series. ALFRED gives you the value AS IT WAS KNOWN
on a past date -- the "vintage". That distinction is the whole game for honest nowcast backtests:
if you train a nowcast on revised data you leak the future, because the revisions embed information
nobody had at the time. This adapter pulls real vintages and stores each under its own `as_of`, so
the bitemporal observations table (`(series_id, obs_date, as_of)`) holds the true point-in-time
picture. No API key required (verified): the ALFRED graph-CSV endpoint is public.

New data = new rows: nothing here adds a table. Each vintage lands as observations with
as_of = the vintage date. A revised series therefore appears as multiple (obs_date, as_of) rows,
and any point-in-time query can ask "what did we know on date X?".

Run:  python3 src/fetch_fred_alfred.py            (default demo catalog)
      python3 src/fetch_fred_alfred.py INDPRO 2020-01-01 2020-04-01 2020-07-01   (series + vintages)
"""

import io
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
ALFRED = "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={sid}&vintage_dates={vintages}"

# (fred_id, entity_id, name, unit, why) -- oil-relevant macro that gets revised (so vintages matter)
CATALOG = [
    ("INDPRO", "macro.activity", "US Industrial Production", "index",
     "Real-activity / oil-demand proxy; heavily revised, so point-in-time vintages matter."),
    ("PAYEMS", "macro.activity", "US Nonfarm Payrolls", "thousands",
     "The headline growth surprise markets trade; first prints are revised substantially."),
]
ENTITIES = [("macro.activity", "macro", "US Real Activity", "Industrial production / payrolls")]

# A quarterly vintage schedule over recent years -- enough to demonstrate real revisions.
DEMO_VINTAGES = [f"{y}-{m:02d}-15" for y in range(2018, 2026) for m in (1, 4, 7, 10)]


def fetch_vintages(sid, vintages):
    """Return a long (obs_date, as_of, value) frame across the requested vintage dates."""
    url = ALFRED.format(sid=sid, vintages=",".join(vintages))
    r = requests.get(url, timeout=45)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    date_col = df.columns[0]                          # 'observation_date'
    out = []
    for col in df.columns[1:]:                        # each col is SID_YYYYMMDD (one vintage)
        vd = col.split("_")[-1]
        try:
            as_of = datetime.strptime(vd, "%Y%m%d").strftime("%Y-%m-%d")
        except ValueError:
            continue
        sub = df[[date_col, col]].copy()
        sub.columns = ["obs_date", "value"]
        sub["value"] = pd.to_numeric(sub["value"], errors="coerce")
        sub = sub.dropna()
        for d, v in zip(sub["obs_date"], sub["value"]):
            out.append((str(d)[:10], as_of, float(v)))
    return out


def main():
    args = sys.argv[1:]
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO entities VALUES (?,?,?,?)", ENTITIES)

    if args:                                           # ad-hoc: series_id vintage1 vintage2 ...
        catalog = [(args[0], "macro.activity", args[0], "", "ad-hoc vintage pull")]
        vintages = args[1:] or DEMO_VINTAGES
    else:
        catalog, vintages = CATALOG, DEMO_VINTAGES

    for sid, entity, name, unit, why in catalog:
        series_id = f"fred.{sid}"
        print(f"Pulling {name} ({sid}) across {len(vintages)} vintages ...")
        try:
            rows = fetch_vintages(sid, vintages)
        except Exception as e:
            print(f"  ! failed: {e}")
            continue
        cur.execute("INSERT OR REPLACE INTO series VALUES (?,?,?,?,?,?,?,?)",
                    (series_id, name, entity, unit, "monthly", "ALFRED",
                     f"https://alfred.stlouisfed.org/series?seid={sid}", why))
        payload = [(series_id, obs_date, value, as_of, now) for obs_date, as_of, value in rows]
        cur.executemany("INSERT OR IGNORE INTO observations VALUES (?,?,?,?,?)", payload)
        n_vintages = len({r[1] for r in rows})
        print(f"  {len(payload):,} obs across {n_vintages} distinct as_of vintages")
    conn.commit()

    # prove the point-in-time capability: does the latest value for a recent month differ by vintage?
    demo = cur.execute(
        "SELECT obs_date, as_of, value FROM observations WHERE series_id='fred.INDPRO' "
        "AND obs_date >= '2019-10-01' AND obs_date < '2020-01-01' ORDER BY obs_date, as_of").fetchall()
    if demo:
        print("\n  point-in-time check (INDPRO late-2019, value as known on each vintage):")
        for d, a, v in demo[:8]:
            print(f"    obs {d}  as-of {a}  = {v}")
    conn.close()


if __name__ == "__main__":
    main()
