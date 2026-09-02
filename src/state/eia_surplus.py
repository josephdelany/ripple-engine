"""eia_surplus.py -- WS-P01 surplus_capacity_world: EIA Global Surplus Crude Oil Production Capacity 1970-2021.

Source (register §3): figure2.xlsx on the EIA special-topic page; annual, million b/d, world / OPEC /
non-OPEC. Public domain. Keyless. A 2022 RECONSTRUCTION (retrospective=1): each year's value is dated knowable on
1 Jan of the following year; release = the file's HTTP Last-Modified (2022-06-09). Annual carry (WS-R2).

Run:  python3 src/state/eia_surplus.py
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402

SOURCE = "EIA Global Surplus Crude Oil Production Capacity 1970-2021 (figure2.xlsx)"
URL = ("https://www.eia.gov/international/content/analysis/special_topics/"
       "Global_Surplus_Crude_Oil_Production_Capacity/xls/figure2.xlsx")
RELEASE_FALLBACK = "2022-06-09"          # the page's file date; used only if the server sends no Last-Modified
FIELDS = ["surplus_capacity_world"]
ENTITY_ROWS = {"Surplus Capacity": "world", "OPEC": "opec", "non-OPEC": "region.non_opec"}


def fetch(force=False):
    return P.fetch_file(URL, P.raw_path("eia_surplus", "figure2.xlsx"), force=force)


def parse(path, release):
    """Rows for world / OPEC / non-OPEC surplus capacity, one per year. Years come from the header row
    beside each block; nothing is positional beyond that."""
    f = pd.read_excel(path, header=None)
    rows = []
    years = None
    for i in range(len(f)):
        label = str(f.iloc[i, 0]).strip()
        if label == "million barrels per day":
            years = [int(y) for y in f.iloc[i, 1:].tolist() if pd.notna(y)]
            continue
        if label in ENTITY_ROWS and years:
            vals = f.iloc[i, 1:1 + len(years)].tolist()
            for y, v in zip(years, vals):
                if pd.notna(v):
                    rows.append({"entity_id": ENTITY_ROWS[label], "field": "surplus_capacity_world", "obs_date": f"{y}-01-01",
                                 "value": float(v), "unit": "mb/d", "source": SOURCE,
                                 "vintage": P.knowable_annual(y), "release": release, "retrospective": 1})
    if not rows:
        raise ValueError("figure2.xlsx: expected 'million barrels per day' header rows and 'Surplus Capacity' rows -- layout changed; STOP")
    return rows


def load(conn=None, force=False):
    path, meta = fetch(force)
    release = P.vintage_from(meta, RELEASE_FALLBACK)
    rows = parse(path, release)
    own = conn is None
    conn = conn or P.connect()
    try:
        n = P.write(conn, rows)
    finally:
        if own:
            conn.close()
    P.report("eia_surplus", n, FIELDS, f"release {release}; retrospective reconstruction (2022); knowable 1 Jan of Y+1")
    return n


if __name__ == "__main__":
    load()
