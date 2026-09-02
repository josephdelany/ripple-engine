"""ucdp.py -- WS-S01..S03 ucdp_active_conflicts, ucdp_intensity_max, ucdp_battle_deaths: UCDP v26.1.

Source (register §1): https://ucdp.uu.se/downloads/ -> UCDP/PRIO Armed Conflict (conflict-year 1946-2025:
location, year, intensity_level 1 minor / 2 war, gwno_loc) and Battle-Related Deaths (1989-2025, bd_best).
CC BY 4.0. Keyless. Rows for `world` and for every mapped location country (a conflict located in more
than one country counts for each). Annual as of 1 Jan of the following year -- UCDP's year Y is knowable
only after Y ends (its release lands the following June; dated knowable 1 Jan Y+1; release = the zip's Last-Modified).

Run:  python3 src/state/ucdp.py
"""
import sys
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402
import countries as C  # noqa: E402

SOURCE = "UCDP/PRIO Armed Conflict v26.1 + UCDP Battle-Related Deaths v26.1"
ACD_URL = "https://ucdp.uu.se/downloads/ucdpprio/ucdp-prio-acd-261-csv.zip"
BRD_URL = "https://ucdp.uu.se/downloads/brd/ucdp-brd-conf-261-csv.zip"
RELEASE_FALLBACK = "2026-06-08"
FIELDS = ["ucdp_active_conflicts", "ucdp_intensity_max", "ucdp_battle_deaths"]


def _extract(zp, suffix, dest):
    if not dest.exists():
        z = zipfile.ZipFile(zp)
        name = next(n for n in z.namelist() if n.endswith(suffix))
        dest.write_bytes(z.read(name))
    return dest


def fetch(force=False):
    acd_zip, meta = P.fetch_file(ACD_URL, P.raw_path("ucdp", "ucdp-prio-acd-261-csv.zip"), force=force)
    brd_zip, _ = P.fetch_file(BRD_URL, P.raw_path("ucdp", "ucdp-brd-conf-261-csv.zip"), force=force)
    return {"acd": _extract(acd_zip, ".csv", P.raw_path("ucdp", "UcdpPrioConflict_v26_1.csv")),
            "brd": _extract(brd_zip, ".csv", P.raw_path("ucdp", "BattleDeaths_v26_1_conf.csv"))}, meta


def _locations(gw):
    """gwno_loc holds one or more Gleditsch-Ward numbers ('2, 645'); GW numbers equal COW ccodes for the states we map."""
    out = []
    for tok in str(gw).replace(";", ",").split(","):
        tok = tok.strip()
        if tok.isdigit():
            e = C.from_ccode(int(tok))
            if e:
                out.append(e)
    return out


def parse(paths, release):
    acd = pd.read_csv(paths["acd"])
    if not {"conflict_id", "year", "intensity_level", "gwno_loc"} <= set(acd.columns):
        raise ValueError("UCDP/PRIO csv lacks conflict_id/year/intensity_level/gwno_loc -- layout changed; STOP")
    rows = []
    for y, g in acd.groupby("year"):
        d = f"{int(y) + 1}-01-01"
        rows.append({"entity_id": "world", "field": "ucdp_active_conflicts", "obs_date": d, "value": float(g["conflict_id"].nunique()), "unit": "count", "source": SOURCE, "vintage": d, "release": release})
        rows.append({"entity_id": "world", "field": "ucdp_intensity_max", "obs_date": d, "value": float(g["intensity_level"].max()), "unit": "1..2", "source": SOURCE, "vintage": d, "release": release})
        per = {}
        for r in g.itertuples(index=False):
            for e in _locations(r.gwno_loc):
                per.setdefault(e, []).append((r.conflict_id, r.intensity_level))
        for e, lst in per.items():
            rows.append({"entity_id": e, "field": "ucdp_active_conflicts", "obs_date": d, "value": float(len({c for c, _ in lst})), "unit": "count", "source": SOURCE, "vintage": d, "release": release})
            rows.append({"entity_id": e, "field": "ucdp_intensity_max", "obs_date": d, "value": float(max(i for _, i in lst)), "unit": "1..2", "source": SOURCE, "vintage": d, "release": release})
    brd = pd.read_csv(paths["brd"])
    if not {"year", "bd_best", "gwno_loc"} <= set(brd.columns):
        raise ValueError("UCDP BRD csv lacks year/bd_best/gwno_loc -- layout changed; STOP")
    for y, g in brd.groupby("year"):
        d = f"{int(y) + 1}-01-01"
        rows.append({"entity_id": "world", "field": "ucdp_battle_deaths", "obs_date": d, "value": float(g["bd_best"].sum()), "unit": "deaths (best)", "source": SOURCE, "vintage": d, "release": release})
        per = {}
        for r in g.itertuples(index=False):
            for e in _locations(r.gwno_loc):
                per[e] = per.get(e, 0.0) + float(r.bd_best)
        for e, v in per.items():
            rows.append({"entity_id": e, "field": "ucdp_battle_deaths", "obs_date": d, "value": v, "unit": "deaths (best)", "source": SOURCE, "vintage": d, "release": release})
    return rows


def load(conn=None, force=False):
    paths, meta = fetch(force)
    release = P.vintage_from(meta, RELEASE_FALLBACK)
    rows = parse(paths, release)
    own = conn is None
    conn = conn or P.connect()
    try:
        n = P.write(conn, rows)
    finally:
        if own:
            conn.close()
    P.report("ucdp", n, FIELDS, f"release {release}; year Y knowable 1 Jan Y+1")
    return n


if __name__ == "__main__":
    load()
