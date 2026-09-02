"""wdi.py -- WS-A12 oil_rents_gdp: World Bank WDI NY.GDP.PETR.RT.ZS (oil rents, % of GDP), free API, keyless.

Source (register §4 "World Bank WDI (oil rents % GDP, 1970→; free API)"): api.worldbank.org/v2, one JSON
per mapped country, cached in data/state/raw/wdi/. Cite World Bank. The API reply carries `lastupdated`
(= release). WDI publishes year Y about a year later: dated knowable 1 July of Y+1 (conservative).

Run:  python3 src/state/wdi.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402
import countries as C  # noqa: E402

SOURCE = "World Bank WDI NY.GDP.PETR.RT.ZS (api.worldbank.org/v2)"
INDICATOR = "NY.GDP.PETR.RT.ZS"
URL = "https://api.worldbank.org/v2/country/{iso3}/indicator/" + INDICATOR + "?format=json&per_page=200&date=1970:2030"
FIELDS = ["oil_rents_gdp"]


def fetch(force=False, entities=None):
    paths = {}
    for ent, (_cc, _abb, iso3, _name) in C.ALL.items():
        if entities and ent not in entities:
            continue
        p, meta = P.fetch_file(URL.format(iso3=iso3), P.raw_path("wdi", f"{iso3}_{INDICATOR}.json"), force=force)
        paths[ent] = (p, meta)
    return paths


def parse_one(path, ent):
    if not hasattr(parse_one, "errors"):
        parse_one.errors = {}
    j = json.loads(Path(path).read_text())
    if isinstance(j, list) and j and isinstance(j[0], dict) and "message" in j[0]:
        parse_one.errors[ent] = str(j[0]["message"])[:120]              # the API's own error (unknown country code etc.): reported, no rows
        return []
    if not isinstance(j, list) or len(j) < 2 or not isinstance(j[0], dict) or "lastupdated" not in j[0]:
        raise ValueError(f"{path}: not a WDI v2 reply -- STOP")
    if not j[0].get("lastupdated") or not j[1]:
        parse_one.errors[ent] = "no data for this country in WDI (empty reply)"     # e.g. Taiwan: the API returns null
        return []
    release = j[0]["lastupdated"][:10]
    rows = []
    for x in j[1] or []:
        if x.get("value") is None:
            continue
        y = int(x["date"])
        rows.append({"entity_id": ent, "field": "oil_rents_gdp", "obs_date": f"{y}-01-01", "value": float(x["value"]), "unit": "percent",
                     "source": SOURCE, "vintage": f"{y + 1}-07-01", "release": release})
    return rows


def parse(paths):
    rows = []
    for ent, (p, _meta) in paths.items():
        rows += parse_one(p, ent)
    return rows


def load(conn=None, force=False):
    paths = fetch(force)
    rows = parse(paths)
    own = conn is None
    conn = conn or P.connect()
    try:
        n = P.write(conn, rows)
    finally:
        if own:
            conn.close()
    P.report("wdi", n, FIELDS, f"{len(paths)} countries; release = API lastupdated; year Y knowable 1 Jul Y+1; API errors: {parse_one.errors}")
    return n


if __name__ == "__main__":
    load()
