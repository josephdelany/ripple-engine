"""polity.py -- WS-A07/A08 polity2, polity_durable: Polity5 annual 1946-2018 (CSP/INSCR, LOCAL ONLY).

Source (register §1): https://www.systemicpeace.org/inscrdata.html -> p5v2018.xls (ccode, scode, year,
polity2, durable ...). Copyrighted; redistribution prohibited: the file lives in data/state/local/csp/,
never committed; cite Marshall & Gurr. Year Y is dated knowable 1 Jan Y+1 (regime scores describe the
year). Release = the file's date. V-Dem (WS-A09) carries 2019→ (separate loader, stub until the file is
placed).

Run:  python3 src/state/polity.py
"""
import datetime as dt
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402
import countries as C  # noqa: E402

SOURCE = "Polity5 (p5v2018.xls, local file)"
FIELDS = ["polity2", "polity_durable"]
INSTRUCTIONS = "Download p5v2018.xls from https://www.systemicpeace.org/inscrdata.html into data/state/local/csp/. Never commit it."


def local_file():
    return P.require_local("csp", "p5v2018.xls", INSTRUCTIONS)


def parse(path, release):
    df = pd.read_csv(path) if str(path).endswith(".csv") else pd.read_excel(path)
    if not {"ccode", "year", "polity2", "durable"} <= set(df.columns):
        raise ValueError("Polity5 file lacks ccode/year/polity2/durable -- layout changed; STOP")
    rows = []
    for r in df.itertuples(index=False):
        ent = C.from_ccode(r.ccode)
        if not ent:
            continue
        for col, field, unit in (("polity2", "polity2", "score -10..10"), ("durable", "polity_durable", "years")):
            v = getattr(r, col)
            if pd.notna(v):
                rows.append({"entity_id": ent, "field": field, "obs_date": f"{int(r.year)}-01-01", "value": float(v), "unit": unit,
                             "source": SOURCE, "vintage": P.knowable_annual(r.year), "release": release})
    return rows


def load(conn=None, force=False):
    path = local_file()
    release = dt.date.fromtimestamp(path.stat().st_mtime).isoformat()
    rows = parse(path, release)
    own = conn is None
    conn = conn or P.connect()
    try:
        n = P.write(conn, rows)
    finally:
        if own:
            conn.close()
    P.report("polity", n, FIELDS, f"local file; release {release} (file date); year Y knowable 1 Jan Y+1; ends 2018")
    return n


if __name__ == "__main__":
    load()
