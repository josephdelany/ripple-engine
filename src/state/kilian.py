"""kilian.py -- WS-M12 kilian_igrea: Kilian's global real economic activity index, published monthly by the Dallas Fed
as IGREA and mirrored on FRED. WS-M13 (the exogenous OPEC supply-shock series 1971-2004) has no direct
download link on the register's page and is a stub (local file instructions).

Source (register §3): https://sites.google.com/site/lkilian2019/research/data-sets -> Dallas Fed IGREA
(https://www.dallasfed.org/research/igrea) -> FRED fredgraph.csv?id=IGREA. Free; cite Kilian (2009, 2019).
A constructed, revised index (retrospective=1). The Dallas Fed posts month m during m+1; each month's
value is dated knowable on the first day of m+2 (conservative). Release = the server's date for the CSV.

Run:  python3 src/state/kilian.py
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402

SOURCE = "Kilian global real economic activity index (Dallas Fed IGREA via FRED)"
URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=IGREA"
FIELDS = ["kilian_igrea"]
SHOCK_INSTRUCTIONS = ("WS-M13 opec_supply_shock_kilian: download the exogenous OPEC supply-shock series (quarterly, 1971-2004) from "
                      "https://sites.google.com/site/lkilian2019/research/data-sets into data/state/local/kilian/opec_shocks.csv "
                      "(columns: quarter, value); the page offers no direct file link to a script.")


def fetch(force=False):
    return P.fetch_file(URL, P.raw_path("kilian", "IGREA.csv"), force=force)


def parse(path, release):
    df = pd.read_csv(path)
    if not {"observation_date", "IGREA"} <= set(df.columns):
        raise ValueError("IGREA csv lacks observation_date/IGREA -- layout changed; STOP")
    rows = []
    for d, v in zip(pd.to_datetime(df["observation_date"]), pd.to_numeric(df["IGREA"], errors="coerce")):
        if pd.notna(v):
            know = (d + pd.offsets.MonthBegin(2)).date().isoformat()
            rows.append({"entity_id": "world", "field": "kilian_igrea", "obs_date": d.date().isoformat(), "value": float(v),
                         "unit": "index", "source": SOURCE, "vintage": know, "release": release, "retrospective": 1})
    return rows


def load(conn=None, force=False):
    path, meta = fetch(force)
    try:
        release = P.vintage_from(meta, None)
    except ValueError:                                   # a cached copy without its server date: fetch it again, once
        path, meta = fetch(force=True)
        release = P.vintage_from(meta, None)
    rows = parse(path, release)
    own = conn is None
    conn = conn or P.connect()
    try:
        n = P.write(conn, rows)
    finally:
        if own:
            conn.close()
    P.report("kilian", n, FIELDS, f"release {release}; month m knowable on the 1st of m+2; opec_supply_shock_kilian: STUB ({SHOCK_INSTRUCTIONS[:60]}...)")
    return n


if __name__ == "__main__":
    load()
