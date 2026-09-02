"""eia_steo.py -- WS-P02 spare_capacity_opec: EIA Short-Term Energy Outlook, Table 3d 'Surplus crude oil production
capacity' (OPEC total / Middle East / Other), monthly, million b/d.

Source (register §3 "Monthly STEO country spare capacity 2003→"): the current STEO workbook
https://www.eia.gov/outlooks/steo/xls/STEO_m.xlsx (public domain, keyless). The workbook carries the
last ~4 years of history plus FORECAST months; only months before the forecast date are loaded --
forecasts are never stored as state. The STEO archive (2003→) refuses scripted access (403), so coverage
here starts where the current file starts (reported by status.py; the register's 2003→ is a gap until
the archive is obtained). Month m is dated knowable on the 1st of m+2 (STEO for month m+1 reports m);
release = the workbook's Last-Modified.

Run:  python3 src/state/eia_steo.py
"""
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402

SOURCE = "EIA STEO Table 3d, surplus crude oil production capacity (STEO_m.xlsx)"
URL = "https://www.eia.gov/outlooks/steo/xls/STEO_m.xlsx"
FIELDS = ["spare_capacity_opec"]
ENTITIES = {"cops_opec": "opec", "cops_opec_r05": "region.opec_middle_east", "cops_opec_rot": "region.opec_other"}
MONTHS = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}


def fetch(force=False):
    return P.fetch_file(URL, P.raw_path("eia_steo", "STEO_m.xlsx"), force=force)


def read_table(path):
    if str(path).endswith(".csv"):
        return pd.read_csv(path, header=None)
    return pd.read_excel(path, sheet_name="3dtab", header=None)


def parse(path, release):
    f = read_table(path)
    # header: row with 'Forecast date:' carries years at each January column; the next row carries month names
    hy = f.index[f.iloc[:, 0].astype(str).str.strip().str.startswith("Forecast date")]
    if len(hy) == 0:
        raise ValueError("STEO 3dtab: no 'Forecast date' header row -- layout changed; STOP")
    hy = hy[0]; hm = hy + 1
    fdate = pd.to_datetime(str(f.iloc[hm, 0]), errors="coerce")           # e.g. 'Thursday, August 6, 2026'
    if pd.isna(fdate):
        raise ValueError("STEO 3dtab: forecast date not parseable -- STOP")
    cols, year = {}, None
    for j in range(2, f.shape[1]):
        y = f.iloc[hy, j]
        if pd.notna(y) and str(y).strip()[:4].isdigit():
            year = int(str(y).strip()[:4])
        m = str(f.iloc[hm, j]).strip()[:3]
        if year and m in MONTHS:
            cols[j] = pd.Timestamp(year=year, month=MONTHS[m], day=1)
    rows = []
    for i in range(len(f)):
        key = str(f.iloc[i, 0]).strip()
        if key in ENTITIES:
            for j, d in cols.items():
                if d >= fdate.replace(day=1):                                  # forecast months: never stored as state
                    continue
                v = pd.to_numeric(f.iloc[i, j], errors="coerce")
                if pd.notna(v):
                    rows.append({"entity_id": ENTITIES[key], "field": "spare_capacity_opec", "obs_date": d.date().isoformat(), "value": float(v),
                                 "unit": "mb/d", "source": SOURCE, "vintage": (d + pd.offsets.MonthBegin(2)).date().isoformat(), "release": release})
    if not rows:
        raise ValueError("STEO 3dtab: no surplus-capacity rows parsed -- layout changed; STOP")
    parse.forecast_date = fdate.date().isoformat()
    return rows


def load(conn=None, force=False):
    path, meta = fetch(force)
    release = P.vintage_from(meta, None)
    rows = parse(path, release)
    own = conn is None
    conn = conn or P.connect()
    try:
        n = P.write(conn, rows)
    finally:
        if own:
            conn.close()
    P.report("eia_steo", n, FIELDS, f"release {release}; forecast date {parse.forecast_date} (forecast months excluded); history starts {rows[0]['obs_date']} -- the 2003+ archive is a gap")
    return n


if __name__ == "__main__":
    load()
