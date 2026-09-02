"""archigos.py -- WS-A10/A11 leader_tenure_days, leader_change_last_365d: Archigos v4.1 (leaders 1875-2015).

Source (register §1): rochester.edu/…/hgoemans (Archigos_4.1_stata14.dta): one row per leader spell with
ccode, leader, startdate, enddate, entry, exit. Free; cite Goemans, Gleditsch & Chiozza 2009. Ends 2015
(dossier after). Representation: one panel row per spell start, field leader_tenure_days, value 0 at
startdate, value_text = leader; the join derives tenure at t as t - obs_date and leader_change_last_365d
as (tenure < 365). A leader's entry is public on the day: knowable = startdate.

Run:  python3 src/state/archigos.py
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402
import countries as C  # noqa: E402

SOURCE = "Archigos v4.1 (Archigos_4.1_stata14.dta)"
URL = "http://www.rochester.edu/college/faculty/hgoemans/Archigos_4.1_stata14.dta"
RELEASE_FALLBACK = "2016-02-29"
FIELDS = ["leader_tenure_days"]


def fetch(force=False):
    return P.fetch_file(URL, P.raw_path("archigos", "Archigos_4.1_stata14.dta"), force=force)


def read(path):
    if str(path).endswith(".csv"):
        return pd.read_csv(path)
    return pd.read_stata(path)


def parse(path, release):
    df = read(path)
    if not {"ccode", "leader", "startdate"} <= set(df.columns):
        raise ValueError("Archigos file lacks ccode/leader/startdate -- layout changed; STOP")
    rows = []
    for r in df.itertuples(index=False):
        ent = C.from_ccode(r.ccode)
        if not ent:
            continue
        d = pd.to_datetime(r.startdate, errors="coerce")
        if pd.isna(d):
            continue
        d = d.date().isoformat()
        rows.append({"entity_id": ent, "field": "leader_tenure_days", "obs_date": d, "value": 0.0, "value_text": str(r.leader).strip(),
                     "unit": "days", "source": SOURCE, "vintage": d, "release": release})
    return rows


def tenure_at(conn, entity_id, t):
    """(leader, tenure_days, change_last_365d) at t from the latest spell start knowable at t; None if none."""
    v = P.value_at(conn, entity_id, "leader_tenure_days", t)
    if not v:
        return None
    days = (pd.Timestamp(t) - pd.Timestamp(v["obs_date"])).days
    return {"leader": v["value_text"], "tenure_days": int(days), "change_last_365d": int(days < 365), "since": v["obs_date"], "source": v["source"]}


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
    P.report("archigos", n, FIELDS, f"release {release}; one row per leader spell start; ends 2015")
    return n


if __name__ == "__main__":
    load()
