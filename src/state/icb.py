"""icb.py -- WS-D06..D09 icb_crisis_count, icb_last_outcome_form, icb_last_violence, icb_last_tension:
ICB v16 (Duke), system level (icb1v16.csv) + crisis dyads (icb_dyads_v16.csv).

Source (register §1): https://sites.duke.edu/icbdata/data-collections/ (Box downloads). 512 crises
1918-2021; cite Brecher & Wilkenfeld / Brecher et al. 2025. Free. Per mapped dyad, as of the day after
each crisis terminates: cumulative crisis count and the last crisis's FOROUT (form of outcome), VIOL
(violence 1 none .. 4 full-scale war) and OUTESR (escalation/reduction of tension). The raw system-level
file is also what PATH Step 4 reads for independent outcomes (`crises()`).
Knowable the day after the crisis terminates; release = the Box file's date when served, else the v16 release (2025).

Run:  python3 src/state/icb.py
"""
import json
import re
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402
import countries as C  # noqa: E402

SOURCE = "ICB v16 system level + dyads (Duke)"
PAGE = "https://sites.duke.edu/icbdata/data-collections/"
DYADS_URL = "https://duke.box.com/shared/static/ipk9fsayfen4d4vg1u3hkb3y7s83f9vp.csv"
RELEASE_FALLBACK = "2025-01-01"
FIELDS = ["icb_crisis_count", "icb_last_outcome_form", "icb_last_violence", "icb_last_tension"]


def _box_download(share_url, dest):
    """Resolve a Box share page to its file download (the page carries the file id)."""
    h = requests.get(share_url, timeout=60, headers={"User-Agent": "Mozilla/5.0 (ripple-engine research)"}).text
    fid = re.search(r'"itemID":\s*(\d+)', h) or re.search(r'f_(\d+)', h)
    shared = re.search(r"/s/([a-z0-9]+)", share_url).group(1)
    if not fid:
        raise ValueError(f"could not resolve Box file id for {share_url}")
    url = f"https://duke.box.com/index.php?rm=box_download_shared_file&shared_name={shared}&file_id=f_{fid.group(1)}"
    return P.fetch_file(url, dest)


def fetch(force=False):
    page = requests.get(PAGE, timeout=60, headers={"User-Agent": "Mozilla/5.0 (ripple-engine research)"}).text
    links = dict((t.strip(), u) for u, t in re.findall(r'<a[^>]+href="(https://duke\.box\.com[^"]+)"[^>]*>(.*?)</a>', page, re.S))
    sys_p = P.raw_path("icb", "icb1v16.csv")
    if not sys_p.exists() or force:
        _box_download(links["ICB1 v16 data"], sys_p)
    dy_p, meta = P.fetch_file(links.get("ICB Dyads v16", DYADS_URL), P.raw_path("icb", "icb_dyads_v16.csv"), force=force)
    return {"system": sys_p, "dyads": dy_p}, meta


def crises(path=None):
    """The system-level table with a real termination date per crisis (for Step 4 and the panel)."""
    p = path or P.raw_path("icb", "icb1v16.csv")
    d = pd.read_csv(p, encoding="latin-1")
    d.columns = [c.replace("ï»¿", "").replace("﻿", "") for c in d.columns]
    need = {"crisno", "crisname", "yrtrig", "motrig", "datrig", "yrterm", "moterm", "daterm", "viol", "forout", "outesr"}
    if not need <= set(d.columns):
        raise ValueError(f"icb1v16.csv lacks {need - set(d.columns)} -- layout changed; STOP")
    for c in ("motrig", "datrig", "moterm", "daterm"):
        d[c] = d[c].fillna(1).clip(1, 12 if "mo" in c else 28)
    d["trigdate"] = pd.to_datetime(dict(year=d.yrtrig, month=d.motrig, day=d.datrig), errors="coerce")
    d["termdate"] = pd.to_datetime(dict(year=d.yrterm, month=d.moterm, day=d.daterm), errors="coerce")
    return d


def parse(paths, release):
    sysd = crises(paths["system"])
    dy = pd.read_csv(paths["dyads"], encoding="latin-1")
    if not {"crisno", "statea", "stateb"} <= set(dy.columns):
        raise ValueError("icb dyads csv lacks crisno/statea/stateb -- layout changed; STOP")
    dy["ea"] = dy["statea"].map(C.from_ccode); dy["eb"] = dy["stateb"].map(C.from_ccode)
    dy = dy.dropna(subset=["ea", "eb"]).drop_duplicates(["crisno", "ea", "eb"])
    dy["dyad"] = [C.dyad_id(a, b) for a, b in zip(dy["ea"], dy["eb"])]
    m = dy.merge(sysd[["crisno", "termdate", "viol", "forout", "outesr"]], on="crisno", how="inner").dropna(subset=["termdate"])
    m = m.sort_values("termdate")
    rows = []
    for dyad, g in m.groupby("dyad"):
        g = g.drop_duplicates("crisno")
        for i, r in enumerate(g.itertuples(index=False), start=1):
            d = (r.termdate + pd.Timedelta(days=1)).date().isoformat()     # knowable once the crisis has terminated
            base = {"entity_id": dyad, "obs_date": d, "source": SOURCE, "vintage": d, "release": release}
            rows.append({**base, "field": "icb_crisis_count", "value": float(i), "unit": "count"})
            for col, field in (("forout", "icb_last_outcome_form"), ("viol", "icb_last_violence"), ("outesr", "icb_last_tension")):
                v = getattr(r, col)
                if pd.notna(v):
                    rows.append({**base, "field": field, "value": float(v), "unit": "code"})
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
    P.report("icb", n, FIELDS, f"release {release}; knowable the day after termination; {len(crises(paths['system']))} crises in the system file")
    return n


if __name__ == "__main__":
    load()
