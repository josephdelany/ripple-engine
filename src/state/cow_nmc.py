"""cow_nmc.py -- WS-A01..A03 cinc, milex_cow, milper_cow: COW National Material Capabilities v7.0 (1816-2022).

Source (register §1): https://correlatesofwar.org/data-sets/national-material-capabilities/ -> NMCv7.zip,
which nests NMC-v7-abridged.zip / NMC-70-abridged.csv (stateabb, ccode, year, milex, milper, irst, pec,
tpop, upop, cinc, version). Free, cite Singer, Bremer & Stuckey 1972. The page warns raw components vary
in quality over time: we load CINC (a share) plus milex/milper as labelled levels. Year Y is dated knowable on 1 Jan Y+1;
release = the zip's HTTP Last-Modified (v7 file, 2026-06-03). Country codes map through countries.py (WS-R4).

Run:  python3 src/state/cow_nmc.py
"""
import io
import sys
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402
import countries as C  # noqa: E402

SOURCE = "COW National Material Capabilities v7.0 (NMC-70-abridged.csv)"
URL = "https://correlatesofwar.org/wp-content/uploads/NMCv7.zip"
RELEASE_FALLBACK = "2025-01-01"          # NMC v7 'version' column = 2025
FIELDS = ["cinc", "milex_cow", "milper_cow"]
COLS = {"cinc": ("cinc", "share"), "milex": ("milex_cow", "thousand USD (current)"), "milper": ("milper_cow", "thousands")}


def fetch(force=False):
    """Download the zip once and extract the abridged CSV beside it (cached)."""
    zp, meta = P.fetch_file(URL, P.raw_path("cow_nmc", "NMCv7.zip"), force=force)
    csv = P.raw_path("cow_nmc", "NMC-70-abridged.csv")
    if not csv.exists() or force:
        outer = zipfile.ZipFile(zp)
        inner_name = next(n for n in outer.namelist() if n.endswith("NMC-v7-abridged.zip"))
        inner = zipfile.ZipFile(io.BytesIO(outer.read(inner_name)))
        name = next(n for n in inner.namelist() if n.endswith("NMC-70-abridged.csv"))
        csv.write_bytes(inner.read(name))
    return csv, meta


def parse(path, release):
    df = pd.read_csv(path, encoding="latin-1")
    need = {"stateabb", "ccode", "year", "cinc", "milex", "milper"}
    if not need <= set(df.columns):
        raise ValueError(f"NMC abridged csv lacks {need - set(df.columns)} -- layout changed; STOP")
    rows, unmapped = [], set()
    for r in df.itertuples(index=False):
        ent = C.from_ccode(r.ccode)
        if not ent:
            unmapped.add(int(r.ccode)); continue
        for col, (field, unit) in COLS.items():
            v = getattr(r, col)
            if pd.notna(v) and v >= 0:                       # NMC codes missing as -9
                rows.append({"entity_id": ent, "field": field, "obs_date": f"{int(r.year)}-01-01", "value": float(v),
                             "unit": unit, "source": SOURCE, "vintage": P.knowable_annual(r.year), "release": release})
    parse.unmapped = sorted(unmapped)
    parse.stateabb = {int(r.ccode): r.stateabb for r in df.drop_duplicates("ccode").itertuples(index=False)}
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
    P.report("cow_nmc", n, FIELDS, f"release {release}; year Y knowable 1 Jan Y+1; {len(parse.unmapped)} ccodes outside the country map (states the corpus does not name)")
    return n


if __name__ == "__main__":
    load()
