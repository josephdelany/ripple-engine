"""stubs.py -- loaders whose input is absent on this machine: they STOP with instructions, never a fake
(PATH Step 2: "if a file or key is absent, stub the loader with instructions and a failing-skipped test").

Each `load()` raises panel.MissingInput until the file/key is present; the parse for each is written
against the documented layout so that placing the file makes the loader live. Modules below are re-exported
as ei_review, eia_intl, gsdb, nyt, vdem, dots (see the thin module files) so status.py lists them by name.
"""
import json
import os
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel as P  # noqa: E402
import countries as C  # noqa: E402


# ----------------------------------------------------------------------------- EI Statistical Review (WS-P04..P08)
EI_FIELDS = ["crude_production_annual", "consumption_annual", "refinery_capacity_annual", "proven_reserves", "net_import_dependence"]
EI_INSTRUCTIONS = ("The EI archive xlsx returns HTTP 403 to a script. Download 'EI-Stats-Review-ALL-data.xlsx' (2025 archive) or the 2026 "
                   "consolidated file from https://www.energyinst.org/statistical-review/resources-and-data-downloads into "
                   "data/state/local/ei/ (a public good; cite Energy Institute). The loader parses the 'Oil Production - barrels', "
                   "'Oil Consumption - barrels', 'Oil - Refinery capacity' and 'Oil - Proved reserves' sheets (country rows, year columns).")
EI_SHEETS = {"Oil Production - barrels": ("crude_production_annual", "kb/d"), "Oil Consumption - barrels": ("consumption_annual", "kb/d"),
             "Oil - Refinery capacity": ("refinery_capacity_annual", "kb/d"), "Oil - Proved reserves": ("proven_reserves", "bn bbl")}


def ei_load(conn=None, force=False):
    path = P.require_local("ei", "EI-Stats-Review-ALL-data.xlsx", EI_INSTRUCTIONS)
    import datetime as dt
    release = dt.date.fromtimestamp(path.stat().st_mtime).isoformat()
    rows = []
    x = pd.ExcelFile(path)
    for sheet, (field, unit) in EI_SHEETS.items():
        if sheet not in x.sheet_names:
            continue
        f = x.parse(sheet, header=None)
        hdr = next((i for i in range(min(10, len(f))) if str(f.iloc[i, 1]).strip().isdigit()), None)
        if hdr is None:
            raise ValueError(f"EI sheet '{sheet}': no year header row found -- layout changed; STOP")
        years = {j: int(f.iloc[hdr, j]) for j in range(1, f.shape[1]) if str(f.iloc[hdr, j]).strip().isdigit()}
        for i in range(hdr + 1, len(f)):
            name = str(f.iloc[i, 0]).strip()
            ent = next((e for e, v in C.ALL.items() if v[3].split(" (")[0].lower() == name.lower()), None)
            if not ent:
                continue
            for j, y in years.items():
                v = pd.to_numeric(f.iloc[i, j], errors="coerce")
                if pd.notna(v):
                    rows.append({"entity_id": ent, "field": field, "obs_date": f"{y}-01-01", "value": float(v), "unit": unit,
                                 "source": f"EI Statistical Review ({path.name})", "vintage": f"{y + 1}-07-01", "release": release})
    own = conn is None
    conn = conn or P.connect()
    try:
        n = P.write(conn, rows)
    finally:
        if own:
            conn.close()
    P.report("ei_review", n, EI_FIELDS)
    return n


# ----------------------------------------------------------------------------- EIA International (WS-P03)
EIA_INTL_FIELDS = ["crude_production"]
EIA_INTL_INSTRUCTIONS = ("Set EIA_API_KEY (free registration at https://www.eia.gov/opendata/). The loader queries the "
                         "international series for crude production by country (monthly, 1973->) and caches replies in data/state/raw/eia_intl/.")


def eia_intl_load(conn=None, force=False):
    key = P.require_env("EIA_API_KEY", EIA_INTL_INSTRUCTIONS)
    import requests
    rows = []
    for ent, (_c, _a, iso3, _n) in C.ALL.items():
        url = ("https://api.eia.gov/v2/international/data/?api_key=" + key + "&frequency=monthly&data[0]=value&facets[activityId][]=1"
               "&facets[productId][]=57&facets[unit][]=TBPD&facets[countryRegionId][]=" + iso3 + "&sort[0][column]=period&sort[0][direction]=asc&length=5000")
        p = P.raw_path("eia_intl", f"{iso3}_crude_monthly.json")
        if not p.exists() or force:
            r = requests.get(url, timeout=120); r.raise_for_status(); p.write_text(r.text)
        j = json.loads(p.read_text())
        for x in (j.get("response") or {}).get("data") or []:
            if x.get("value") is None:
                continue
            d = pd.Timestamp(x["period"] + "-01")
            rows.append({"entity_id": ent, "field": "crude_production", "obs_date": d.date().isoformat(), "value": float(x["value"]), "unit": "kb/d",
                         "source": "EIA International Energy Statistics API v2", "vintage": (d + pd.offsets.MonthBegin(3)).date().isoformat(),
                         "release": P.now()[:10]})
    own = conn is None
    conn = conn or P.connect()
    try:
        n = P.write(conn, rows)
    finally:
        if own:
            conn.close()
    P.report("eia_intl", n, EIA_INTL_FIELDS)
    return n


# ----------------------------------------------------------------------------- GSDB (WS-D10)
GSDB_FIELDS = ["sanctions_in_force"]
GSDB_INSTRUCTIONS = ("GSDB R5 is by request (https://www.globalsanctionsdatabase.com/, 24 h, non-commercial). Joe requests it with the project "
                     "title; place the dyadic file as data/state/local/gsdb/GSDB_V5_dyadic.csv (columns sanctioning_state, sanctioned_state "
                     "(ISO3), begin, end, and the type flags). Never commit it.")


def gsdb_load(conn=None, force=False):
    path = P.require_local("gsdb", "GSDB_V5_dyadic.csv", GSDB_INSTRUCTIONS)
    import datetime as dt
    release = dt.date.fromtimestamp(path.stat().st_mtime).isoformat()
    df = pd.read_csv(path)
    cols = {c.lower(): c for c in df.columns}
    a = cols.get("sanctioning_state") or cols.get("sender"); b = cols.get("sanctioned_state") or cols.get("target")
    if not (a and b and "begin" in cols and "end" in cols):
        raise ValueError("GSDB dyadic file: expected sanctioning_state/sanctioned_state/begin/end columns -- STOP")
    rows = []
    for r in df.itertuples(index=False):
        ea, eb = C.from_iso3(getattr(r, a)), C.from_iso3(getattr(r, b))
        if not (ea and eb) or ea == eb:
            continue
        for y in range(int(getattr(r, cols["begin"])), int(getattr(r, cols["end"])) + 1):
            rows.append({"entity_id": C.dyad_id(ea, eb), "field": "sanctions_in_force", "obs_date": f"{y}-01-01", "value": 1.0, "unit": "0/1",
                         "source": "GSDB R5 dyadic (local file)", "vintage": f"{y}-01-01", "release": release})
    own = conn is None
    conn = conn or P.connect()
    try:
        n = P.write(conn, rows)
    finally:
        if own:
            conn.close()
    P.report("gsdb", n, GSDB_FIELDS)
    return n


# ----------------------------------------------------------------------------- NYT (WS-N02)
NYT_FIELDS = ["nyt_article_count"]
NYT_INSTRUCTIONS = ("Set NYT_API_KEY (free key from https://developer.nytimes.com/; never committed). The loader counts Article Search hits "
                    "per month for each mapped country name (rate-limited; run on Joe's machine).")


def nyt_load(conn=None, force=False):
    P.require_env("NYT_API_KEY", NYT_INSTRUCTIONS)
    raise P.MissingInput("NYT loader: key present but the per-event query plan (WS-N02, per-event dossier) runs from the dossier pipeline, "
                         "not the panel; nothing to load into state_panel yet. " + NYT_INSTRUCTIONS)


# ----------------------------------------------------------------------------- V-Dem (WS-A09)
VDEM_FIELDS = ["vdem_polyarchy"]
VDEM_INSTRUCTIONS = ("V-Dem v16 is served through a form (no direct link). Download the Country-Year Core CSV from "
                     "https://www.v-dem.net/data/the-v-dem-dataset/ into data/state/local/vdem/V-Dem-CY-Core-v16.csv (CC BY-SA; pin v16).")


def vdem_load(conn=None, force=False):
    path = P.require_local("vdem", "V-Dem-CY-Core-v16.csv", VDEM_INSTRUCTIONS)
    import datetime as dt
    release = dt.date.fromtimestamp(path.stat().st_mtime).isoformat()
    df = pd.read_csv(path, usecols=lambda c: c in {"country_text_id", "year", "v2x_polyarchy"})
    rows = []
    for r in df.itertuples(index=False):
        ent = C.from_iso3(r.country_text_id)
        if ent and pd.notna(r.v2x_polyarchy):
            rows.append({"entity_id": ent, "field": "vdem_polyarchy", "obs_date": f"{int(r.year)}-01-01", "value": float(r.v2x_polyarchy), "unit": "index 0..1",
                         "source": "V-Dem v16 Country-Year Core (local file)", "vintage": P.knowable_annual(r.year), "release": release})
    own = conn is None
    conn = conn or P.connect()
    try:
        n = P.write(conn, rows)
    finally:
        if own:
            conn.close()
    P.report("vdem", n, VDEM_FIELDS)
    return n


# ----------------------------------------------------------------------------- IMF DOTS (WS-D11)
DOTS_FIELDS = ["trade_share_bilateral"]
DOTS_INSTRUCTIONS = ("The IMF DataMapper and legacy SDMX endpoints refuse scripted access (403 / 404 from this machine). Export the "
                     "Direction of Trade Statistics bilateral exports table (reporter, partner, year, value) from https://data.imf.org into "
                     "data/state/local/dots/dots_exports.csv.")


def dots_load(conn=None, force=False):
    path = P.require_local("dots", "dots_exports.csv", DOTS_INSTRUCTIONS)
    import datetime as dt
    release = dt.date.fromtimestamp(path.stat().st_mtime).isoformat()
    df = pd.read_csv(path)
    need = {"reporter", "partner", "year", "value"}
    if not need <= set(df.columns):
        raise ValueError(f"DOTS export lacks {need - set(df.columns)} -- STOP")
    df["ea"] = df["reporter"].map(C.from_iso3); df["eb"] = df["partner"].map(C.from_iso3)
    df = df.dropna(subset=["ea", "eb"])
    tot = df.groupby(["ea", "year"])["value"].sum()
    rows = []
    for r in df.itertuples(index=False):
        t = tot.get((r.ea, r.year))
        if t:
            rows.append({"entity_id": C.dyad_id(r.ea, r.eb), "field": "trade_share_bilateral", "obs_date": f"{int(r.year)}-01-01",
                         "value": round(100.0 * float(r.value) / float(t), 4), "unit": "percent of exports", "source": "IMF DOTS (local export)",
                         "vintage": f"{int(r.year) + 1}-07-01", "release": release})
    own = conn is None
    conn = conn or P.connect()
    try:
        n = P.write(conn, rows)
    finally:
        if own:
            conn.close()
    P.report("dots", n, DOTS_FIELDS)
    return n
