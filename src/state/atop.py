"""atop.py -- WS-D01/D02 atop_defense_pact, atop_any_obligation: ATOP 5.1 directed-dyad-year (1815-2018).

Source (register §1): http://www.atopdata.org/data.html -> atop_5.1__.csv_.zip -> atop5_1ddyr.csv
(ddyad = ccode1*1000 + ccode2, year, atopally, defense, offense, neutral, nonagg, consul). Free; cite
Leeds et al. 2002. Ends 2018 (dossier after). Directed rows are folded to the undirected dyad: a
defense obligation in either direction counts. Treaties are public: in force in Y = knowable 1 Jan Y. Release = the zip's HTTP Last-Modified.

Run:  python3 src/state/atop.py
"""
import sys
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402
import countries as C  # noqa: E402

SOURCE = "ATOP 5.1 directed dyad-year (atop5_1ddyr.csv)"
URL = "https://www.atopdata.org/uploads/6/9/1/3/69134503/atop_5.1__.csv_.zip"
RELEASE_FALLBACK = "2022-08-01"          # 'last updated Aug 2022' on the page
FIELDS = ["atop_defense_pact", "atop_any_obligation"]
USECOLS = ["ddyad", "year", "atopally", "defense", "offense", "neutral", "nonagg", "consul"]


def fetch(force=False):
    zp, meta = P.fetch_file(URL, P.raw_path("atop", "atop_5.1_csv.zip"), force=force)
    csv = P.raw_path("atop", "atop5_1ddyr.csv")
    if not csv.exists() or force:
        z = zipfile.ZipFile(zp)
        name = next(n for n in z.namelist() if n.endswith("atop5_1ddyr.csv") and "NNA" not in n)
        csv.write_bytes(z.read(name))
    return csv, meta


def parse(path, release):
    df = pd.read_csv(path, usecols=lambda c: c in USECOLS)
    if not set(USECOLS) <= set(df.columns):
        raise ValueError("atop5_1ddyr.csv lacks expected columns -- layout changed; STOP")
    df["ea"] = (df["ddyad"] // 1000).map(C.from_ccode); df["eb"] = (df["ddyad"] % 1000).map(C.from_ccode)
    df = df.dropna(subset=["ea", "eb"])
    df = df[df["ea"] != df["eb"]]
    df["dyad"] = [C.dyad_id(a, b) for a, b in zip(df["ea"], df["eb"])]
    g = df.groupby(["dyad", "year"]).agg(defense=("defense", "max"), any_=("atopally", "max")).reset_index()
    rows = []
    for r in g.itertuples(index=False):
        d = f"{int(r.year)}-01-01"
        rows.append({"entity_id": r.dyad, "field": "atop_defense_pact", "obs_date": d, "value": float(r.defense), "unit": "0/1", "source": SOURCE, "vintage": d, "release": release})
        rows.append({"entity_id": r.dyad, "field": "atop_any_obligation", "obs_date": d, "value": float(r.any_), "unit": "0/1", "source": SOURCE, "vintage": d, "release": release})
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
    P.report("atop", n, FIELDS, f"release {release}; in force in Y = knowable 1 Jan Y; ends 2018")
    return n


if __name__ == "__main__":
    load()
