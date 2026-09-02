"""voeten.py -- WS-D12 unga_ideal_point_distance: Bailey, Strezhnev & Voeten UNGA ideal points (Harvard Dataverse).

Source (register §1 "Voeten UNGA ideal points"): IdealpointestimatesAll_Jun2024.csv (ccode, session,
IdealPointAll, iso3c). Free; cite Bailey, Strezhnev & Voeten 2017. Session s sits in year 1945+s
(session 1 = 1946); votes close by December, so the year's value is dated knowable on 1 Jan of the next
year. Per mapped dyad: |ideal_a - ideal_b|. Release = the Dataverse file's Last-Modified.

Run:  python3 src/state/voeten.py
"""
import itertools
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402
import countries as C  # noqa: E402

SOURCE = "UNGA ideal points, Bailey-Strezhnev-Voeten (IdealpointestimatesAll_Jun2024.csv)"
URL = "https://dataverse.harvard.edu/api/access/datafile/10295878"
RELEASE_FALLBACK = "2024-06-01"
FIELDS = ["unga_ideal_point_distance"]


def fetch(force=False):
    return P.fetch_file(URL, P.raw_path("voeten", "IdealpointestimatesAll_Jun2024.csv"), force=force)


def parse(path, release):
    df = pd.read_csv(path)
    if not {"ccode", "session", "IdealPointAll"} <= set(df.columns):
        raise ValueError("ideal-point csv lacks ccode/session/IdealPointAll -- layout changed; STOP")
    df["ent"] = df["ccode"].map(C.from_ccode)
    df = df.dropna(subset=["ent", "IdealPointAll"])
    rows = []
    for s, g in df.groupby("session"):
        year = 1945 + int(s)
        pts = dict(zip(g["ent"], g["IdealPointAll"]))
        for a, b in itertools.combinations(sorted(pts), 2):
            rows.append({"entity_id": C.dyad_id(a, b), "field": "unga_ideal_point_distance", "obs_date": f"{year}-01-01",
                         "value": round(abs(float(pts[a]) - float(pts[b])), 6), "unit": "distance", "source": SOURCE,
                         "vintage": P.knowable_annual(year), "release": release})
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
    P.report("voeten", n, FIELDS, f"release {release}; session s = year 1945+s, knowable 1 Jan next year")
    return n


if __name__ == "__main__":
    load()
