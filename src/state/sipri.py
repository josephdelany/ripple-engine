"""sipri.py -- WS-A04/A05 milex_sipri, milex_gdp_share_sipri: SIPRI Military Expenditure Database (LOCAL ONLY).

Source (register §1): https://www.sipri.org/databases/milex -> SIPRI-Milex-data-1949-2025_v1.2.xlsx
(sheets 'Constant (2024) US$' and 'Share of GDP'; header row 'Country | Notes | 1949 ...'). SIPRI user terms:
the file lives in data/state/local/sipri/ and is never committed. Year Y (SIPRI publishes in April Y+1)
is dated knowable 1 May of Y+1. Release = the file's Last-Modified. WS-A06 arms_imports_tiv needs the
separate Arms Transfers export (stub: instructions below).

Run:  python3 src/state/sipri.py
"""
import glob
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402
import countries as C  # noqa: E402

SOURCE = "SIPRI Military Expenditure Database (local file)"
FIELDS = ["milex_sipri", "milex_gdp_share_sipri"]
INSTRUCTIONS = ("Download the Military Expenditure Database Excel from https://www.sipri.org/databases/milex into "
                "data/state/local/sipri/ (any SIPRI-Milex-data-*.xlsx). Never commit it. Arms transfers (WS-A06): export the TIV "
                "importer table from the Arms Transfers Database into data/state/local/sipri/arms_imports_tiv.csv (columns: country, year, tiv).")
SHEETS = {"Constant (2024) US$": ("milex_sipri", "USD m (constant 2024)"), "Share of GDP": ("milex_gdp_share_sipri", "percent")}
NAMES = {"United States of America": "country.usa", "USA": "country.usa", "Russia": "country.russia", "Russian Federation": "country.russia",
         "UAE": "country.uae", "United Arab Emirates": "country.uae", "Korea, South": "country.south_korea", "South Korea": "country.south_korea",
         "Congo, DR": "country.congo_drc", "Congo, Dem. Rep.": "country.congo_drc", "DR Congo": "country.congo_drc", "Türkiye": "country.turkey",
         "Turkey": "country.turkey", "Viet Nam": "country.vietnam", "Vietnam": "country.vietnam", "Myanmar": "country.myanmar",
         "Iran": "country.iran", "Taiwan": "country.taiwan", "Serbia": "country.serbia", "Yemen": "country.yemen", "United Kingdom": "country.gbr",
         "Germany": "country.deu", "France": "country.fra"}


def local_file():
    hits = sorted(glob.glob(str(P.LOCAL / "sipri" / "SIPRI-Milex-data-*.xlsx")))
    if not hits:
        raise P.MissingInput(f"data/state/local/sipri/SIPRI-Milex-data-*.xlsx is absent. {INSTRUCTIONS}")
    return Path(hits[-1])


def _entity(name):
    n = str(name).strip()
    if n in NAMES:
        return NAMES[n]
    for ent, (_c, _a, _i, full) in C.ALL.items():
        if full.split(" (")[0].lower() == n.lower():
            return ent
    return None


def parse(path, release):
    rows = []
    for sheet, (field, unit) in SHEETS.items():
        f = pd.read_excel(path, sheet_name=sheet, header=None)
        hdr = f.index[f.iloc[:, 0].astype(str).str.strip() == "Country"]
        if len(hdr) == 0:
            raise ValueError(f"SIPRI sheet '{sheet}': no 'Country' header row -- layout changed; STOP")
        h = hdr[0]
        years = {j: int(f.iloc[h, j]) for j in range(f.shape[1]) if str(f.iloc[h, j]).strip().isdigit()}
        for i in range(h + 1, len(f)):
            ent = _entity(f.iloc[i, 0])
            if not ent:
                continue
            for j, y in years.items():
                v = pd.to_numeric(f.iloc[i, j], errors="coerce")
                if pd.notna(v):
                    rows.append({"entity_id": ent, "field": field, "obs_date": f"{y}-01-01", "value": float(v), "unit": unit,
                                 "source": SOURCE, "vintage": f"{y + 1}-05-01", "release": release})
    if not rows:
        raise ValueError("SIPRI: no rows parsed -- STOP")
    return rows


def load(conn=None, force=False):
    path = local_file()
    import datetime as dt
    release = dt.date.fromtimestamp(path.stat().st_mtime).isoformat()
    rows = parse(path, release)
    own = conn is None
    conn = conn or P.connect()
    try:
        n = P.write(conn, rows)
    finally:
        if own:
            conn.close()
    P.report("sipri", n, FIELDS, f"local file {path.name}; release {release} (file date); year Y knowable 1 May Y+1; arms_imports_tiv: STUB")
    return n


if __name__ == "__main__":
    load()
