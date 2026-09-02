"""gpr.py -- WS-S05..S09, WS-N01: Caldara-Iacoviello GPR monthly export (Recent 1985-> and Historical 1900->).

Source (register §2): https://www.matteoiacoviello.com/gpr.htm -> gpr_files/data_gpr_export.xls, one sheet:
month, GPR/GPRT/GPRA (Recent), GPRH/GPRHT/GPRHA (Historical), SHARE_GPR/SHARE_GPRH (article shares),
GPRC_<ISO3> country indexes. CC BY. Keyless. Updated on the 1st of each month: a month's value is dated knowable on the 1st of the
following month; release = the file's HTTP Last-Modified. The index is a constructed, revised series
(retrospective=1). The monthly vintage ARCHIVE (WS-S10) is not served under the file
names the register implies (404 on every pattern tried); that field stays unloaded and is reported.

Run:  python3 src/state/gpr.py
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402
import countries as C  # noqa: E402

SOURCE = "Caldara-Iacoviello GPR monthly export (data_gpr_export.xls)"
URL = "https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls"
RELEASE_FALLBACK = "2026-09-01"
COLS = {"GPR": "gpr_monthly", "GPRT": "gpr_threats_monthly", "GPRA": "gpr_acts_monthly", "GPRH": "gprh_monthly",
        "SHARE_GPRH": "gprh_newspaper_share"}
FIELDS = list(COLS.values()) + ["gpr_country_monthly"]


def fetch(force=False):
    return P.fetch_file(URL, P.raw_path("gpr", "data_gpr_export.xls"), force=force)


def parse(path, release):
    g = pd.read_csv(path) if str(path).endswith(".csv") else pd.read_excel(path)
    missing = {"month", "GPR", "GPRH"} - set(g.columns)
    if missing:
        raise ValueError(f"data_gpr_export.xls lacks {missing} -- layout changed; STOP")
    g["month"] = pd.to_datetime(g["month"])
    rows = []
    for col, field in COLS.items():
        if col not in g.columns:
            continue
        for m, v in zip(g["month"], g[col]):
            if pd.notna(v):
                rows.append({"entity_id": "world", "field": field, "obs_date": m.date().isoformat(), "value": float(v),
                             "unit": "percent" if field.endswith("share") else "index", "source": SOURCE,
                             "vintage": P.knowable_month(m), "release": release, "retrospective": 1})
    unmapped = []
    for col in g.columns:
        if col.startswith("GPRC_"):
            ent = C.from_iso3(col[5:])
            if not ent:
                unmapped.append(col[5:]); continue
            for m, v in zip(g["month"], g[col]):
                if pd.notna(v):
                    rows.append({"entity_id": ent, "field": "gpr_country_monthly", "obs_date": m.date().isoformat(),
                                 "value": float(v), "unit": "index", "source": SOURCE,
                                 "vintage": P.knowable_month(m), "release": release, "retrospective": 1})
    parse.unmapped = unmapped
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
    P.report("gpr", n, FIELDS, f"release {release}; a month is knowable on the 1st of the next month; retrospective index; country columns not in the country map: {parse.unmapped}")
    return n


if __name__ == "__main__":
    load()
