"""csp.py -- WS-A14 coup_last_5y, WS-S13 mepv_regional_war: CSP Coups d'Etat 1946-2021 and Major Episodes of
Political Violence 1946-2018 (CSP/INSCR, LOCAL ONLY).

Source (register §1): https://www.systemicpeace.org/inscrdata.html -> CSPCoupsAnnualv2021.xls (scoup1
successful, atcoup2 attempted, per country-year) and MEPVv2018.xls (nregion = summed war magnitude in the
country's region, actotal = the country's own total). Copyrighted; files in data/state/local/csp/, never
committed; cite Marshall. coup_last_5y as of 1 Jan Y = successful + attempted coups in [Y-5, Y-1]
(knowable 1 Jan Y). mepv_regional_war for year Y = nregion, knowable 1 Jan Y+1.

Run:  python3 src/state/csp.py
"""
import datetime as dt
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402
import countries as C  # noqa: E402

SOURCE_COUPS = "CSP Coups d'Etat 1946-2021 (CSPCoupsAnnualv2021.xls, local file)"
SOURCE_MEPV = "CSP Major Episodes of Political Violence 1946-2018 (MEPVv2018.xls, local file)"
FIELDS = ["coup_last_5y", "mepv_regional_war"]
INSTRUCTIONS = "Download CSPCoupsAnnualv2021.xls and MEPVv2018.xls from https://www.systemicpeace.org/inscrdata.html into data/state/local/csp/. Never commit them."


def local_files():
    return {"coups": P.require_local("csp", "CSPCoupsAnnualv2021.xls", INSTRUCTIONS),
            "mepv": P.require_local("csp", "MEPVv2018.xls", INSTRUCTIONS)}


def _read(path):
    return pd.read_csv(path) if str(path).endswith(".csv") else pd.read_excel(path)


def parse(paths, release):
    rows = []
    co = _read(paths["coups"])
    if not {"ccode", "year", "scoup1", "atcoup2"} <= set(co.columns):
        raise ValueError("coups file lacks ccode/year/scoup1/atcoup2 -- layout changed; STOP")
    co["ent"] = co["ccode"].map(C.from_ccode)
    co = co.dropna(subset=["ent"])
    co["n"] = co["scoup1"].fillna(0) + co["atcoup2"].fillna(0)
    for ent, g in co.groupby("ent"):
        byy = dict(zip(g["year"], g["n"]))
        for Y in range(int(g["year"].min()) + 1, int(g["year"].max()) + 2):
            v = sum(byy.get(y, 0) for y in range(Y - 5, Y))
            rows.append({"entity_id": ent, "field": "coup_last_5y", "obs_date": f"{Y}-01-01", "value": float(v), "unit": "count",
                         "source": SOURCE_COUPS, "vintage": f"{Y}-01-01", "release": release})
    me = _read(paths["mepv"])
    if not {"ccode", "year", "nregion"} <= set(me.columns):
        raise ValueError("MEPV file lacks ccode/year/nregion -- layout changed; STOP")
    for r in me.itertuples(index=False):
        ent = C.from_ccode(r.ccode)
        if ent and pd.notna(r.nregion):
            rows.append({"entity_id": ent, "field": "mepv_regional_war", "obs_date": f"{int(r.year)}-01-01", "value": float(r.nregion),
                         "unit": "magnitude", "source": SOURCE_MEPV, "vintage": P.knowable_annual(r.year), "release": release})
    return rows


def load(conn=None, force=False):
    paths = local_files()
    release = dt.date.fromtimestamp(max(p.stat().st_mtime for p in paths.values())).isoformat()
    rows = parse(paths, release)
    own = conn is None
    conn = conn or P.connect()
    try:
        n = P.write(conn, rows)
    finally:
        if own:
            conn.close()
    P.report("csp", n, FIELDS, f"local files; release {release} (file date)")
    return n


if __name__ == "__main__":
    load()
