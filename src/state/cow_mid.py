"""cow_mid.py -- WS-D03..D05 mid_count_10y, mid_max_hostlev_10y, mid_last_date: COW Dyadic MID 4.03 (1816-2014).

Source (register §1): https://correlatesofwar.org/data-sets/mids/ -> dyadic_mid_4.03_update.zip ->
dyadic_mid_4.03.csv (disno, statea, stateb, year, strt*/end*, hihost 1..5, fatlev, ...). Free; cite
Palmer et al. 2020. Ends 2014 (UCDP carries after). Per mapped dyad and year Y (state as of 1 Jan Y):
count of dispute-years in [Y-10, Y-1], the max hostility level in that window, and the last dispute
start date before Y. All knowable on 1 Jan Y. Release = the zip's HTTP Last-Modified.

Run:  python3 src/state/cow_mid.py
"""
import sys
import zipfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402
import countries as C  # noqa: E402

SOURCE = "COW Dyadic MID 4.03 (dyadic_mid_4.03.csv)"
URL = "https://correlatesofwar.org/wp-content/uploads/dyadic_mid_4.03_update.zip"
RELEASE_FALLBACK = "2025-04-06"
FIELDS = ["mid_count_10y", "mid_max_hostlev_10y", "mid_last_date"]
WINDOW = 10


def fetch(force=False):
    zp, meta = P.fetch_file(URL, P.raw_path("cow_mid", "dyadic_mid_4.03_update.zip"), force=force)
    csv = P.raw_path("cow_mid", "dyadic_mid_4.03.csv")
    if not csv.exists() or force:
        z = zipfile.ZipFile(zp)
        name = next(n for n in z.namelist() if n.endswith("dyadic_mid_4.03.csv"))
        csv.write_bytes(z.read(name))
    return csv, meta


def parse(path, release, last_year=2014):
    df = pd.read_csv(path)
    need = {"disno", "statea", "stateb", "year", "hihost", "strtyr", "strtmnth", "strtday"}
    if not need <= set(df.columns):
        raise ValueError(f"dyadic MID csv lacks {need - set(df.columns)} -- layout changed; STOP")
    df["ea"] = df["statea"].map(C.from_ccode); df["eb"] = df["stateb"].map(C.from_ccode)
    df = df.dropna(subset=["ea", "eb"])
    df["dyad"] = [C.dyad_id(a, b) for a, b in zip(df["ea"], df["eb"])]
    df["start"] = pd.to_datetime(dict(year=df.strtyr, month=df.strtmnth.clip(1, 12), day=df.strtday.clip(1, 28)), errors="coerce")
    rows = []
    for dyad, g in df.groupby("dyad"):
        years = sorted(g["year"].unique())
        first = int(min(years))
        for Y in range(first + 1, last_year + 2):               # state as of 1 Jan Y, up to the year after the data ends
            w = g[(g["year"] >= Y - WINDOW) & (g["year"] <= Y - 1)]
            before = g[g["year"] <= Y - 1]
            if before.empty:
                continue
            d = f"{Y}-01-01"
            rows.append({"entity_id": dyad, "field": "mid_count_10y", "obs_date": d, "value": float(w["disno"].nunique()), "unit": "count", "source": SOURCE, "vintage": d, "release": release})
            rows.append({"entity_id": dyad, "field": "mid_max_hostlev_10y", "obs_date": d, "value": float(w["hihost"].max()) if len(w) else 0.0, "unit": "1..5", "source": SOURCE, "vintage": d, "release": release})
            last = before["start"].max()
            if pd.notna(last):
                rows.append({"entity_id": dyad, "field": "mid_last_date", "obs_date": d, "value_text": last.date().isoformat(), "unit": "date", "source": SOURCE, "vintage": d, "release": release})
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
    P.report("cow_mid", n, FIELDS, f"release {release}; state as of 1 Jan Y is knowable then; dyads among mapped countries only; ends 2014")
    return n


if __name__ == "__main__":
    load()
