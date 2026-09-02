"""
ripple_fetch.py -- loaders for the RIPPLE chain nodes (RIPPLE_SOURCES.md, brief R2/R3b).

WHAT THIS IS (plain language)
-----------------------------
The ripple study follows an oil shock down the chain: crude -> refined products (gasoline,
diesel, jet, propane) -> the physical system (refinery runs, stocks, imports, chokepoint
transits) -> gas/LNG -> fertilizer, with macro cross-checks and two EXTERNAL shock series
(Kaenzig 2021; Baumeister-Hamilton 2019) used only as sanity checks. Most crude/product/macro
nodes are already in oil.db (see RIPPLE_SOURCES.md, "already in the DB"). This module adds
only what was missing, from sources whose pages were opened and recorded in RIPPLE_SOURCES.md
on 2026-09-02. Nothing here is loaded from an unverified page.

RULES THIS FILE OBEYS
---------------------
- One database, the seven-table schema: new data = new rows in series/observations. No new
  tables. Entities are INSERT OR IGNORE; series INSERT OR REPLACE; observations INSERT OR
  IGNORE (append-only; a value already stored is never overwritten).
- Keyless only. Nothing paid. No EIA key is used here: the weekly EIA series come from the
  public hist_xls workbooks (same sourcekeys as the API).
- Licence-aware seeding. Sources whose licence permits redistribution (EIA public domain,
  FRED-hosted EIA/Fed series, World Bank CC BY 4.0, Kaenzig CC BY 4.0) are SEEDED under
  data/seed/ripple/ so the default run is offline and reproducible. Sources whose terms we
  could not read or that are personal-use (IMF PortWatch terms page returned 403; Yahoo via
  yfinance "personal use only"; Baumeister-Hamilton shocks carry a citation line but no licence
  text) are REFRESH-ONLY: pulled live into the local DB, never written to the repo.
- Every observation carries as_of (= obs_date, the convention used by the other loaders;
  publication lags are declared per source in RIPPLE_REGISTRATION.md, not hidden here) and
  retrieved_at.

RUN
---
  python3 src/ripple_fetch.py              # offline: seeds -> oil.db (refresh-only sources skipped)
  python3 src/ripple_fetch.py --refresh    # live: every source -> seeds (where allowed) + oil.db
  python3 src/ripple_fetch.py --verify     # live: print first/last/rows per source, write nothing
  python3 src/ripple_fetch.py --only wb.   # restrict to series ids with this prefix
"""

import argparse
import hashlib
import io
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

try:
    import requests
except Exception:                       # pragma: no cover
    requests = None

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
SEED_DIR = ROOT / "data" / "seed" / "ripple"
MANIFEST = SEED_DIR / "MANIFEST.json"
UA = {"User-Agent": "ripple-engine/1.0 (research; keyless public data)"}

FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
EIA_XLS = "https://www.eia.gov/dnav/pet/hist_xls/{key}w.xls"
PINK_URL = ("https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/"
            "related/CMO-Historical-Data-Monthly.xlsx")
PORTWATCH_URL = ("https://services9.arcgis.com/weJ1QsnbMYJlCHdG/ArcGIS/rest/services/"
                 "Daily_Chokepoints_Data/FeatureServer/0/query")
KANZIG_URL = ("https://raw.githubusercontent.com/dkaenzig/oilsupplynews/master/"
              "oilSupplyNewsShocks_2025M12.xlsx")
BH_SUPPLY_URL = "https://drive.google.com/uc?export=download&id=1OsA8btgm2rmDucUFngiLkwv4uywTDmya"
BH_DEMAND_URL = "https://drive.google.com/uc?export=download&id=1neFXLrIvGwggebQRwjmtrWK-dfQZ9NH8"
CFTC_BASE = "https://www.cftc.gov/files/dea/history/"
CFTC_DISAGG_BUNDLE = "fut_disagg_txt_hist_2006_2016.zip"      # verified 2026-09-02 (the name without _hist_ 404s)
CFTC_LEGACY_BUNDLE = "deacot1986_2016.zip"
CFTC_WTI, CFTC_BRENT_NYMEX = "067651", "06765T"                 # stable contract codes; names change over time
JODI_URL = ("https://www.jodidata.org/_resources/files/downloads/oil-data/annual-csv/"
            "{cls}/{year}.csv")
JODI_FIRST_YEAR = 2002
# JODI reports every (country, product, flow, month) in FIVE unit rows. CONVBBL is NOT a volume:
# it is the country's barrels-per-tonne conversion factor x1000 (verified 2026-09-02: Saudi crude
# production 2026-01 has KBBL/KTONS = 7.323 exactly equal to CONVBBL/1000, and KBD x 31 = KBBL).
# Reading "whichever unit is populated" would record Russia's crude production as 7356. So the
# unit is PINNED per measure below and CONVBBL is never used. Missing is "-" or "x".
JODI_MISSING = {"-", "x", ""}

# ----------------------------------------------------------------------------------------------
# The registry. Every entry names the RIPPLE_SOURCES.md line it comes from (the `src` key), the
# licence that decides whether a seed file may be committed, and how to fetch it live.
# ----------------------------------------------------------------------------------------------

ENTITIES = [
    ("commodity.gasoline_nyh", "commodity", "Wholesale Gasoline (NY Harbor)", "NY Harbor conventional regular spot"),
    ("commodity.jet_fuel", "commodity", "Jet Fuel (US Gulf)", "Kerosene-type jet fuel, US Gulf Coast spot"),
    ("physical.us_stocks", "supplychain", "US petroleum stocks and imports", "EIA weekly petroleum status report"),
    ("commodity.pinksheet", "commodity", "World Bank Pink Sheet", "Monthly commodity prices, nominal USD, 1960->"),
    ("chokepoint.panama", "chokepoint", "Panama Canal", "IMF PortWatch chokepoint"),
    ("chokepoint.bosporus", "chokepoint", "Bosporus Strait", "IMF PortWatch chokepoint"),
    ("chokepoint.malacca", "chokepoint", "Malacca Strait", "IMF PortWatch chokepoint"),
    ("shock.kanzig", "derived", "Kaenzig (2021) oil supply news", "External identified-shock series (CC BY 4.0)"),
    ("shock.baumeister_hamilton", "derived", "Baumeister-Hamilton (2019) structural shocks", "External structural-shock series (citation required; no licence text found)"),
    ("equity.tankers", "supplychain", "Tanker equities", "EQUITY PROXY for freight, never a freight rate"),
    ("equity.refiners", "supplychain", "Refiner equities", "EQUITY PROXY for refining margin"),
    ("equity.fertilizer", "supplychain", "Fertilizer equities", "EQUITY PROXY for fertilizer"),
    ("equity.lng", "supplychain", "LNG exporter equities", "EQUITY PROXY for LNG"),
]

# series_id -> spec.  kind: fred | eia_xls | pink | portwatch | kanzig | bh | yf
SPECS = {
    # --- FRED daily spots that were missing (source EIA, public domain; FRED citation requested)
    "fred.DGASNYH": dict(kind="fred", key="DGASNYH", entity="commodity.gasoline_nyh",
        name="Conventional Gasoline Spot, New York Harbor, Regular", unit="USD/gal", freq="daily",
        source="FRED", url="https://fred.stlouisfed.org/series/DGASNYH",
        licence="EIA public domain; FRED: cite source and FRED", seed=True,
        src="RIPPLE_SOURCES.md #2 crude & products"),
    "fred.DJFUELUSGULF": dict(kind="fred", key="DJFUELUSGULF", entity="commodity.jet_fuel",
        name="Kerosene-Type Jet Fuel Spot, US Gulf Coast", unit="USD/gal", freq="daily",
        source="FRED", url="https://fred.stlouisfed.org/series/DJFUELUSGULF",
        licence="EIA public domain; FRED: cite source and FRED", seed=True,
        src="RIPPLE_SOURCES.md #2 crude & products"),
    # --- EIA weekly physical (keyless hist_xls; public domain). Refinery utilization
    #     (WPULEUS3) and crude stocks ex-SPR (WCESTUS1) already exist as eia.refinery_util and
    #     eia.crude_stocks_xspr from the API loader; not duplicated here.
    "eia.distillate_stocks": dict(kind="eia_xls", key="WDISTUS1", entity="physical.us_stocks",
        name="Weekly U.S. Ending Stocks of Distillate Fuel Oil", unit="thousand bbl", freq="weekly",
        source="EIA", url="https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=WDISTUS1&f=W",
        licence="EIA public domain (eia.gov/about/copyrights_reuse.php)", seed=True,
        src="RIPPLE_SOURCES.md #3 EIA weekly"),
    "eia.gasoline_stocks": dict(kind="eia_xls", key="WGTSTUS1", entity="physical.us_stocks",
        name="Weekly U.S. Ending Stocks of Total Gasoline", unit="thousand bbl", freq="weekly",
        source="EIA", url="https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=WGTSTUS1&f=W",
        licence="EIA public domain", seed=True, src="RIPPLE_SOURCES.md #3 EIA weekly"),
    "eia.crude_imports": dict(kind="eia_xls", key="WCRIMUS2", entity="physical.us_stocks",
        name="Weekly U.S. Imports of Crude Oil", unit="thousand bbl/day", freq="weekly",
        source="EIA", url="https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=WCRIMUS2&f=W",
        licence="EIA public domain", seed=True, src="RIPPLE_SOURCES.md #3 EIA weekly"),
    # --- World Bank Pink Sheet monthly (CC BY 4.0). The fertilizer and LNG spine.
    "wb.crude_avg": dict(kind="pink", key="Crude oil, average", unit="USD/bbl"),
    "wb.brent": dict(kind="pink", key="Crude oil, Brent", unit="USD/bbl"),
    "wb.ngas_us": dict(kind="pink", key="Natural gas, US", unit="USD/mmbtu"),
    "wb.ngas_eu": dict(kind="pink", key="Natural gas, Europe", unit="USD/mmbtu"),
    "wb.lng_japan": dict(kind="pink", key="Liquefied natural gas, Japan", unit="USD/mmbtu"),
    "wb.urea": dict(kind="pink", key="Urea", unit="USD/mt"),
    "wb.dap": dict(kind="pink", key="DAP", unit="USD/mt"),
    "wb.tsp": dict(kind="pink", key="TSP", unit="USD/mt"),
    "wb.potash": dict(kind="pink", key="Potassium chloride", unit="USD/mt"),
    "wb.coal_aus": dict(kind="pink", key="Coal, Australian", unit="USD/mt"),
    # --- Kaenzig (2021) external shock series (CC BY 4.0)
    "kanzig.surprise_daily_pc": dict(kind="kanzig", key="daily_pc", entity="shock.kanzig",
        name="Kaenzig oil supply surprise, daily PC (OPEC announcement days)", unit="log-diff futures PC",
        freq="daily", source="Kaenzig (2021) AER; github.com/dkaenzig/oilsupplynews",
        url="https://github.com/dkaenzig/oilsupplynews", licence="CC BY 4.0 (repo README)", seed=True,
        src="RIPPLE_SOURCES.md #7 external shocks"),
    "kanzig.surprise_monthly": dict(kind="kanzig", key="monthly_surprise", entity="shock.kanzig",
        name="Kaenzig oil supply surprise series, monthly", unit="log-diff futures PC (sum in month)",
        freq="monthly", source="Kaenzig (2021) AER; github.com/dkaenzig/oilsupplynews",
        url="https://github.com/dkaenzig/oilsupplynews", licence="CC BY 4.0 (repo README)", seed=True,
        src="RIPPLE_SOURCES.md #7 external shocks"),
    "kanzig.news_shock_monthly": dict(kind="kanzig", key="monthly_shock", entity="shock.kanzig",
        name="Kaenzig oil supply news shock, monthly (VAR-extracted)", unit="structural shock",
        freq="monthly", source="Kaenzig (2021) AER; github.com/dkaenzig/oilsupplynews",
        url="https://github.com/dkaenzig/oilsupplynews", licence="CC BY 4.0 (repo README)", seed=True,
        src="RIPPLE_SOURCES.md #7 external shocks"),
    # --- Baumeister-Hamilton (2019) structural shocks: REFRESH-ONLY (no licence text found)
    "bh.supply_shock": dict(kind="bh", key=("supply", 1), entity="shock.baumeister_hamilton",
        name="B-H oil supply shock (posterior median)", unit="structural shock", freq="monthly",
        source="Baumeister & Hamilton (2019) AER; sites.google.com/site/cjsbaumeister/datasets",
        url="https://sites.google.com/site/cjsbaumeister/datasets",
        licence="citation line only; no licence text found -> not redistributed", seed=False,
        src="RIPPLE_SOURCES.md #7 external shocks"),
    "bh.activity_shock": dict(kind="bh", key=("demand", 1), entity="shock.baumeister_hamilton",
        name="B-H economic activity shock", unit="structural shock", freq="monthly",
        source="Baumeister & Hamilton (2019) AER", url="https://sites.google.com/site/cjsbaumeister/datasets",
        licence="citation line only; not redistributed", seed=False, src="RIPPLE_SOURCES.md #7"),
    "bh.consumption_demand_shock": dict(kind="bh", key=("demand", 2), entity="shock.baumeister_hamilton",
        name="B-H oil consumption demand shock", unit="structural shock", freq="monthly",
        source="Baumeister & Hamilton (2019) AER", url="https://sites.google.com/site/cjsbaumeister/datasets",
        licence="citation line only; not redistributed", seed=False, src="RIPPLE_SOURCES.md #7"),
    "bh.inventory_demand_shock": dict(kind="bh", key=("demand", 3), entity="shock.baumeister_hamilton",
        name="B-H oil inventory demand shock", unit="structural shock", freq="monthly",
        source="Baumeister & Hamilton (2019) AER", url="https://sites.google.com/site/cjsbaumeister/datasets",
        licence="citation line only; not redistributed", seed=False, src="RIPPLE_SOURCES.md #7"),
    # --- Equity proxies via yfinance: REFRESH-ONLY (Yahoo: personal use). Labelled EQUITY PROXY.
    "yf.eq_fro": dict(kind="yf", key="FRO", entity="equity.tankers", name="EQUITY PROXY tanker: Frontline (FRO)"),
    "yf.eq_dht": dict(kind="yf", key="DHT", entity="equity.tankers", name="EQUITY PROXY tanker: DHT Holdings (DHT)"),
    "yf.eq_tnk": dict(kind="yf", key="TNK", entity="equity.tankers", name="EQUITY PROXY tanker: Teekay Tankers (TNK)"),
    "yf.eq_insw": dict(kind="yf", key="INSW", entity="equity.tankers", name="EQUITY PROXY tanker: International Seaways (INSW)"),
    "yf.eq_vlo": dict(kind="yf", key="VLO", entity="equity.refiners", name="EQUITY PROXY refiner: Valero (VLO)"),
    "yf.eq_mpc": dict(kind="yf", key="MPC", entity="equity.refiners", name="EQUITY PROXY refiner: Marathon Petroleum (MPC)"),
    "yf.eq_psx": dict(kind="yf", key="PSX", entity="equity.refiners", name="EQUITY PROXY refiner: Phillips 66 (PSX)"),
    "yf.eq_cf": dict(kind="yf", key="CF", entity="equity.fertilizer", name="EQUITY PROXY fertilizer: CF Industries (CF)"),
    "yf.eq_ntr": dict(kind="yf", key="NTR", entity="equity.fertilizer", name="EQUITY PROXY fertilizer: Nutrien (NTR)"),
    "yf.eq_mos": dict(kind="yf", key="MOS", entity="equity.fertilizer", name="EQUITY PROXY fertilizer: Mosaic (MOS)"),
    "yf.eq_lng": dict(kind="yf", key="LNG", entity="equity.lng", name="EQUITY PROXY LNG: Cheniere (LNG)"),
}
# --- C-5 priced-in inputs: CFTC Commitments of Traders (public domain; acknowledgement requested).
#     Disaggregated futures-only 2006-06-13 -> (WTI code 067651; the NYMEX Brent Last Day 06765T is a
#     PROXY -- ICE Futures Europe Brent does not appear in the CFTC files, RIPPLE_SOURCES.md #11);
#     Legacy futures-only 1986-01-15 -> (WTI only). Weekly, Tuesday-dated, released Friday 15:30 ET.
_DISAGG_FIELDS = {
    "mm_long": ("M_Money_Positions_Long_All", "managed money long"),
    "mm_short": ("M_Money_Positions_Short_All", "managed money short"),
    "mm_spread": ("M_Money_Positions_Spread_All", "managed money spreading"),
    "pm_long": ("Prod_Merc_Positions_Long_All", "producer/merchant long"),
    "pm_short": ("Prod_Merc_Positions_Short_All", "producer/merchant short"),
    "swap_long": ("Swap_Positions_Long_All", "swap dealer long"),
    "swap_short": ("Swap__Positions_Short_All", "swap dealer short"),   # CFTC's own double underscore
    "oi": ("Open_Interest_All", "open interest"),
}
_LEGACY_FIELDS = {
    "noncomm_long": ("Noncommercial Positions-Long (All)", "non-commercial long"),
    "noncomm_short": ("Noncommercial Positions-Short (All)", "non-commercial short"),
    "noncomm_spread": ("Noncommercial Positions-Spreading (All)", "non-commercial spreading"),
    "comm_long": ("Commercial Positions-Long (All)", "commercial long"),
    "comm_short": ("Commercial Positions-Short (All)", "commercial short"),
    "oi": ("Open Interest (All)", "open interest"),
}
for _f, (_col, _lab) in _DISAGG_FIELDS.items():
    SPECS[f"cftc.wti_{_f}"] = dict(kind="cftc_disagg", key=(CFTC_WTI, _col), entity="commodity.wti",
        name=f"COT disaggregated futures-only, NYMEX WTI (067651): {_lab}", unit="contracts", freq="weekly",
        source="CFTC", url="https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm",
        licence="CFTC public domain (cftc.gov/webpolicy)", seed=True, src="RIPPLE_SOURCES.md #11 priced-in")
    SPECS[f"cftc.brent_nymex_{_f}"] = dict(kind="cftc_disagg", key=(CFTC_BRENT_NYMEX, _col), entity="commodity.brent_nymex_lastday",
        name=f"COT disaggregated futures-only, PROXY NYMEX Brent Last Day (06765T, not ICE Europe Brent): {_lab}",
        unit="contracts", freq="weekly", source="CFTC",
        url="https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm",
        licence="CFTC public domain (cftc.gov/webpolicy)", seed=True, src="RIPPLE_SOURCES.md #11 priced-in")
for _f, (_col, _lab) in _LEGACY_FIELDS.items():
    SPECS[f"cftc.wti_legacy_{_f}"] = dict(kind="cftc_legacy", key=(CFTC_WTI, _col), entity="commodity.wti",
        name=f"COT legacy futures-only, NYMEX WTI (067651): {_lab}", unit="contracts", freq="weekly",
        source="CFTC", url="https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm",
        licence="CFTC public domain (cftc.gov/webpolicy)", seed=True, src="RIPPLE_SOURCES.md #11 priced-in")
ENTITIES.append(("commodity.brent_nymex_lastday", "commodity", "NYMEX Brent Last Day (06765T)",
                 "CFTC COT proxy for Brent positioning; NOT the ICE Futures Europe Brent contract"))
# --- JODI-Oil (Joe's ruling 2026-09-02, option (a)): monthly country data, REFRESH-ONLY.
#     No licence page exists on jodidata.org; "freely available" is read as ACCESS, not RIGHTS,
#     so nothing is redistributed -- no seed, never committed. Cite as JODI-Oil with the
#     retrieval date. None of these is a node in the sealed RIPPLE_REGISTRATION.md Table N;
#     they are loaded for later work and were not used in the computed study.
JODI_COUNTRIES = {
    "SA": "Saudi Arabia", "US": "United States", "RU": "Russia", "CN": "China", "IN": "India",
    "JP": "Japan", "IQ": "Iraq", "AE": "United Arab Emirates", "KW": "Kuwait", "NO": "Norway",
    "CA": "Canada", "BR": "Brazil", "MX": "Mexico", "KR": "Korea", "DE": "Germany",
    "GB": "United Kingdom", "NG": "Nigeria", "DZ": "Algeria", "QA": "Qatar", "KZ": "Kazakhstan",
    "VE": "Venezuela", "IR": "Iran",
}
# measure -> (classification, ENERGY_PRODUCT, FLOW_BREAKDOWN, pinned UNIT_MEASURE, unit label, what)
JODI_MEASURES = {
    "crude_production": ("primary", "CRUDEOIL", "INDPROD", "KBD", "thousand bbl/day", "crude oil production"),
    "refinery_intake": ("primary", "CRUDEOIL", "REFINOBS", "KBD", "thousand bbl/day", "refinery observed intake of crude"),
    "crude_stocks": ("primary", "CRUDEOIL", "CLOSTLV", "KBBL", "thousand bbl", "closing crude stock level"),
    "crude_exports": ("primary", "CRUDEOIL", "TOTEXPSB", "KBD", "thousand bbl/day", "total crude exports"),
    "products_demand": ("secondary", "TOTPRODS", "TOTDEMO", "KBD", "thousand bbl/day", "total refined-product demand"),
}
for _cc, _cname in JODI_COUNTRIES.items():
    _ent = f"country.{_cname.lower().replace(' ', '_')}"
    ENTITIES.append((_ent, "country", _cname, "JODI-Oil reporter"))
    for _mk, (_cls, _prod, _flow, _unit, _ulab, _what) in JODI_MEASURES.items():
        SPECS[f"jodi.{_cc.lower()}.{_mk}"] = dict(kind="jodi", key=(_cls, _prod, _flow, _unit, _cc),
            entity=_ent, name=f"JODI-Oil: {_cname} {_what}", unit=_ulab, freq="monthly",
            source="JODI-Oil", url="https://www.jodidata.org/oil/database/data-downloads.aspx",
            licence="no licence page on the site; 'freely available' read as access not rights -> never redistributed",
            seed=False, src="RIPPLE_SOURCES.md #5 JODI-Oil")
# STNG (product tankers) already exists as yf.tankers; not duplicated.

# fill the repetitive fields for the Pink Sheet and yfinance entries
for _sid, _s in SPECS.items():
    if _s["kind"] == "pink":
        _s.update(entity="commodity.pinksheet", name=f"World Bank Pink Sheet: {_s['key']}",
                  freq="monthly", source="World Bank CMO (Pink Sheet)",
                  url="https://www.worldbank.org/en/research/commodity-markets",
                  licence="CC BY 4.0 (data.worldbank.org/summary-terms-of-use)", seed=True,
                  src="RIPPLE_SOURCES.md #4 Pink Sheet")
    elif _s["kind"] == "yf":
        _s.update(unit="USD (adj. close)", freq="daily", source="Yahoo (yfinance)",
                  url="https://finance.yahoo.com", licence="Yahoo personal use (yfinance README) -> not redistributed",
                  seed=False, src="RIPPLE_SOURCES.md #6 freight & equity proxies")

PORTWATCH = {   # portname exactly as PortWatch spells it -> our slug (existing slugs reused)
    "Strait of Hormuz": "hormuz", "Bab el-Mandeb Strait": "bab_el_mandeb", "Suez Canal": "suez",
    "Cape of Good Hope": "cape_of_good_hope", "Malacca Strait": "malacca",
    "Panama Canal": "panama", "Bosporus Strait": "bosporus",
}
PORTWATCH_FIELDS = {"n_tanker": "tankers/day", "n_total": "ships/day", "capacity_tanker": "metric tons/day"}
for _pname, _slug in PORTWATCH.items():
    for _f, _u in PORTWATCH_FIELDS.items():
        SPECS[f"portwatch.{_slug}.{_f}"] = dict(kind="portwatch", key=(_pname, _f), entity=f"chokepoint.{_slug}",
            name=f"{_pname} daily {_f}", unit=_u, freq="daily", source="IMF PortWatch",
            url="https://portwatch.imf.org/",
            licence=("IMF Terms and Conditions, Copyright and Usage, special terms for statistical Data "
                     "(imf.org/external/terms.htm, effective 2020-01-02): users may download, copy, publish "
                     "and distribute Data from IMF Sites, with attribution 'Source: International Monetary Fund' "
                     "and no alteration of integrity. Published daily aggregates only -- upstream AIS inputs "
                     "are third-party. Attribution: Sources: UN Global Platform; IMF PortWatch."),
            seed=True, src="RIPPLE_SOURCES.md #5 physical flows")


# ----------------------------------------------------------------------------------------------
# HTTP helpers (requests only; bounded retries; no keys)
# ----------------------------------------------------------------------------------------------

def _get_bytes(url, params=None, tries=3, timeout=60):
    if requests is None:
        raise RuntimeError("requests not importable")
    last = None
    for attempt in range(tries):
        try:
            r = requests.get(url, params=params, headers=UA, timeout=timeout)
            if r.status_code in (429, 500, 502, 503, 504):
                raise IOError(f"HTTP {r.status_code}")
            r.raise_for_status()
            return r.content
        except Exception as e:              # noqa: BLE001 -- retry then re-raise
            last = e
            if attempt < tries - 1:
                time.sleep(2.0 * (2 ** attempt))
    raise last


# ----------------------------------------------------------------------------------------------
# Parsers. Each takes bytes (so tests can feed fixture files) and returns DataFrame[date,value]
# with ISO dates as strings and float values, NaN rows dropped. Pure; no network.
# ----------------------------------------------------------------------------------------------

def parse_fred_csv(raw):
    df = pd.read_csv(io.StringIO(raw.decode("utf-8")))
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"]).dt.date.astype(str)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")     # "." -> NaN
    return df.dropna().reset_index(drop=True)


def parse_eia_xls(raw, sourcekey):
    """EIA hist_xls workbook: sheet 'Data 1', row 1 = Sourcekey, row 2 = header, data from row 3."""
    x = pd.read_excel(io.BytesIO(raw), sheet_name="Data 1", header=None)
    found = str(x.iloc[1, 1]).strip()
    if found != sourcekey:
        raise ValueError(f"EIA workbook sourcekey mismatch: expected {sourcekey}, found {found}")
    df = x.iloc[3:, :2].copy()
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"]).dt.date.astype(str)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna().reset_index(drop=True)


def eia_title(raw):
    x = pd.read_excel(io.BytesIO(raw), sheet_name="Data 1", header=None)
    return str(x.iloc[2, 1])


def parse_pink(raw):
    """World Bank Pink Sheet 'Monthly Prices': row 4 names, row 5 units, data from row 6,
    col 0 = 'YYYYMmm'. Returns {commodity name (stripped of footnote marks): DataFrame}."""
    x = pd.read_excel(io.BytesIO(raw), sheet_name="Monthly Prices", header=None)
    names = [str(n).replace("**", "").strip() if isinstance(n, str) else None for n in x.iloc[4]]
    dates = x.iloc[6:, 0].astype(str)
    iso = dates.str.extract(r"^(\d{4})M(\d{2})$")
    out = {}
    for i, n in enumerate(names):
        if not n or i == 0:
            continue
        vals = pd.to_numeric(x.iloc[6:, i], errors="coerce")
        df = pd.DataFrame({"date": (iso[0] + "-" + iso[1] + "-01").values, "value": vals.values})
        out[n] = df.dropna().reset_index(drop=True)
    return out


def parse_kanzig(raw):
    """Kaenzig workbook: sheets Daily (Date/Contract, Front, 1M..12M, PC) and Monthly
    (Date 'YYYYMmm', Oil supply surprise series, Oil supply news shock)."""
    d = pd.read_excel(io.BytesIO(raw), sheet_name="Daily", header=0)
    daily = pd.DataFrame({"date": pd.to_datetime(d.iloc[:, 0]).dt.date.astype(str),
                          "value": pd.to_numeric(d["PC"], errors="coerce")}).dropna()
    m = pd.read_excel(io.BytesIO(raw), sheet_name="Monthly", header=0)
    iso = m.iloc[:, 0].astype(str).str.extract(r"^(\d{4})M(\d{2})$")
    dates = (iso[0] + "-" + iso[1] + "-01").values
    surprise = pd.DataFrame({"date": dates, "value": pd.to_numeric(m.iloc[:, 1], errors="coerce")}).dropna()
    shock = pd.DataFrame({"date": dates, "value": pd.to_numeric(m.iloc[:, 2], errors="coerce")}).dropna()
    return {"daily_pc": daily.reset_index(drop=True), "monthly_surprise": surprise.reset_index(drop=True),
            "monthly_shock": shock.reset_index(drop=True)}


def parse_bh(raw, col):
    """Baumeister workbook: two header rows (NaT), data from row 2, col 0 = date, value in `col`."""
    x = pd.read_excel(io.BytesIO(raw), header=None)
    df = pd.DataFrame({"date": pd.to_datetime(x.iloc[2:, 0], errors="coerce"),
                       "value": pd.to_numeric(x.iloc[2:, col], errors="coerce")}).dropna()
    df["date"] = df["date"].dt.date.astype(str)
    return df.reset_index(drop=True)


def parse_portwatch_features(features):
    """ArcGIS features -> {field: DataFrame}. `date` may be epoch-ms or 'YYYY-MM-DD'."""
    rows = [f["attributes"] for f in features]
    def _iso(v):
        if isinstance(v, (int, float)):
            return datetime.fromtimestamp(v / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
        return str(v)[:10]
    out = {}
    for fld in PORTWATCH_FIELDS:
        df = pd.DataFrame({"date": [_iso(r["date"]) for r in rows],
                           "value": [r.get(fld) for r in rows]})
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        out[fld] = df.dropna().drop_duplicates("date").sort_values("date").reset_index(drop=True)
    return out


def parse_jodi(raw, product, flow, unit, country):
    """One JODI annual CSV -> DataFrame[date,value] for one country/product/flow at the PINNED
    unit. Month 'YYYY-MM' -> first of month. CONVBBL is never accepted (it is a conversion
    factor, not a volume); missing markers '-' and 'x' are dropped, never zero-filled."""
    if unit == "CONVBBL":
        raise ValueError("CONVBBL is a conversion factor, not a volume -- refusing to load it as data")
    df = pd.read_csv(io.BytesIO(raw), dtype=str)
    m = ((df["REF_AREA"] == country) & (df["ENERGY_PRODUCT"] == product)
         & (df["FLOW_BREAKDOWN"] == flow) & (df["UNIT_MEASURE"] == unit))
    sub = df[m]
    if not len(sub):
        return pd.DataFrame(columns=["date", "value"])
    val = sub["OBS_VALUE"].astype(str).str.strip()
    keep = ~val.isin(JODI_MISSING)
    out = pd.DataFrame({"date": sub.loc[keep, "TIME_PERIOD"].astype(str) + "-01",
                        "value": pd.to_numeric(val[keep], errors="coerce")})
    return out.dropna().drop_duplicates("date").sort_values("date").reset_index(drop=True)


def parse_cftc_zip(raw, family):
    """One CFTC historical zip -> DataFrame (all rows, str dtype) with normalised columns `code`,
    `date` (ISO). family: 'disagg' or 'legacy'. Handles the three date-column variants seen in the
    files (Report_Date_as_YYYY-MM-DD, Report_Date_as_MM_DD_YYYY, As of Date in Form YYYY-MM-DD)."""
    import zipfile
    z = zipfile.ZipFile(io.BytesIO(raw))
    name = next(n for n in z.namelist() if n.lower().endswith(".txt"))
    df = pd.read_csv(io.BytesIO(z.read(name)), dtype=str, low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    if family == "disagg":
        code_col = "CFTC_Contract_Market_Code"
        if "Report_Date_as_YYYY-MM-DD" in df.columns:
            date = pd.to_datetime(df["Report_Date_as_YYYY-MM-DD"], errors="coerce")
        elif "Report_Date_as_MM_DD_YYYY" in df.columns:
            date = pd.to_datetime(df["Report_Date_as_MM_DD_YYYY"], format="%m/%d/%Y", errors="coerce")
        else:
            date = pd.to_datetime(df["As_of_Date_In_Form_YYMMDD"], format="%y%m%d", errors="coerce")
    else:
        code_col = "CFTC Contract Market Code"
        date = pd.to_datetime(df["As of Date in Form YYYY-MM-DD"], errors="coerce")
    df["code"] = df[code_col].astype(str).str.strip()
    df["date"] = date.dt.date.astype(str)
    return df[df["date"] != "NaT"]


def cftc_series(frames, code, col):
    """Weekly DataFrame[date,value] for one contract code and one column across several files."""
    parts = []
    for df in frames:
        sub = df[df["code"] == code]
        if col in sub.columns and len(sub):
            parts.append(pd.DataFrame({"date": sub["date"].values,
                                       "value": pd.to_numeric(sub[col].str.replace(",", ""), errors="coerce").values}))
    if not parts:
        return pd.DataFrame(columns=["date", "value"])
    out = pd.concat(parts).dropna().drop_duplicates("date", keep="last").sort_values("date")
    return out.reset_index(drop=True)


def fetch_cftc_frames(family):
    """Download the bundle + yearly zips for a family; return list of parsed frames."""
    year_now = datetime.now(timezone.utc).year
    if family == "disagg":
        names = [CFTC_DISAGG_BUNDLE] + [f"fut_disagg_txt_{y}.zip" for y in range(2017, year_now + 1)]
    else:
        names = [CFTC_LEGACY_BUNDLE] + [f"deacot{y}.zip" for y in range(2017, year_now + 1)]
    frames = []
    for n in names:
        frames.append(parse_cftc_zip(_get_bytes(CFTC_BASE + n, timeout=120), family))
    return frames


# ----------------------------------------------------------------------------------------------
# Live fetchers (grouped by download so one file feeds several series)
# ----------------------------------------------------------------------------------------------

def fetch_portwatch(portname):
    feats, offset = [], 0
    while True:
        params = {"where": f"portname='{portname}'", "outFields": "date," + ",".join(PORTWATCH_FIELDS),
                  "orderByFields": "date ASC", "resultOffset": offset, "resultRecordCount": 2000,
                  "f": "json"}
        js = json.loads(_get_bytes(PORTWATCH_URL, params=params).decode("utf-8"))
        batch = js.get("features", [])
        feats.extend(batch)
        if not js.get("exceededTransferLimit") or not batch:
            break
        offset += len(batch)
    return parse_portwatch_features(feats)


def fetch_yf(symbol):
    import yfinance as yf
    df = yf.download(symbol, period="max", interval="1d", progress=False, auto_adjust=True)
    if df is None or df.empty:
        return pd.DataFrame(columns=["date", "value"])
    close = df["Close"]
    s = close.iloc[:, 0] if hasattr(close, "columns") else close
    s = s.dropna()
    return pd.DataFrame({"date": [d.date().isoformat() for d in s.index],
                         "value": [float(v) for v in s.to_numpy()]})


def fetch_live(only=None):
    """Pull every source once and return {series_id: (DataFrame, extra_notes)}. Grouped so a
    workbook is downloaded once. Failures are isolated per source and reported, not raised."""
    want = {sid: s for sid, s in SPECS.items() if not only or sid.startswith(only)}
    got, errors = {}, {}
    kinds = {s["kind"] for s in want.values()}

    for sid, s in want.items():
        if s["kind"] == "fred":
            try:
                got[sid] = (parse_fred_csv(_get_bytes(FRED_CSV.format(sid=s["key"]))), "")
            except Exception as e:
                errors[sid] = f"{type(e).__name__}: {e}"
        elif s["kind"] == "eia_xls":
            try:
                raw = _get_bytes(EIA_XLS.format(key=s["key"]))
                got[sid] = (parse_eia_xls(raw, s["key"]), f"workbook title: {eia_title(raw)}")
            except Exception as e:
                errors[sid] = f"{type(e).__name__}: {e}"

    if "pink" in kinds:
        try:
            tables = parse_pink(_get_bytes(PINK_URL))
            for sid, s in want.items():
                if s["kind"] == "pink":
                    if s["key"] in tables:
                        got[sid] = (tables[s["key"]], "")
                    else:
                        errors[sid] = f"column '{s['key']}' not found in Pink Sheet"
        except Exception as e:
            for sid, s in want.items():
                if s["kind"] == "pink":
                    errors[sid] = f"{type(e).__name__}: {e}"

    if "kanzig" in kinds:
        try:
            tables = parse_kanzig(_get_bytes(KANZIG_URL))
            for sid, s in want.items():
                if s["kind"] == "kanzig":
                    got[sid] = (tables[s["key"]], "file oilSupplyNewsShocks_2025M12.xlsx")
        except Exception as e:
            for sid, s in want.items():
                if s["kind"] == "kanzig":
                    errors[sid] = f"{type(e).__name__}: {e}"

    if "bh" in kinds:
        raws = {}
        for which, url in (("supply", BH_SUPPLY_URL), ("demand", BH_DEMAND_URL)):
            try:
                raws[which] = _get_bytes(url)
            except Exception as e:
                raws[which] = e
        for sid, s in want.items():
            if s["kind"] == "bh":
                which, col = s["key"]
                raw = raws.get(which)
                if isinstance(raw, Exception):
                    errors[sid] = f"{type(raw).__name__}: {raw}"
                else:
                    try:
                        got[sid] = (parse_bh(raw, col), "")
                    except Exception as e:
                        errors[sid] = f"{type(e).__name__}: {e}"

    if "portwatch" in kinds:
        cache = {}
        for sid, s in want.items():
            if s["kind"] != "portwatch":
                continue
            pname, fld = s["key"]
            if pname not in cache:
                try:
                    cache[pname] = fetch_portwatch(pname)
                except Exception as e:
                    cache[pname] = e
            res = cache[pname]
            if isinstance(res, Exception):
                errors[sid] = f"{type(res).__name__}: {res}"
            else:
                got[sid] = (res[fld], "")

    if "jodi" in kinds:
        year_now = datetime.now(timezone.utc).year
        jodi_specs = [(sid, sp) for sid, sp in want.items() if sp["kind"] == "jodi"]
        acc = {sid: [] for sid, _ in jodi_specs}
        for cls in sorted({sp["key"][0] for _, sp in jodi_specs}):
            for year in range(JODI_FIRST_YEAR, year_now + 1):
                try:
                    raw = _get_bytes(JODI_URL.format(cls=cls, year=year), timeout=180)
                except Exception as e:
                    print(f"  ! JODI {cls} {year}: {type(e).__name__}: {e}")
                    continue
                for sid, sp in jodi_specs:
                    c, prod, flow, unit, country = sp["key"]
                    if c != cls:
                        continue
                    try:
                        part = parse_jodi(raw, prod, flow, unit, country)
                        if len(part):
                            acc[sid].append(part)
                    except Exception as e:
                        errors[sid] = f"{type(e).__name__}: {e}"
        for sid, parts in acc.items():
            if parts:
                df = pd.concat(parts).drop_duplicates("date").sort_values("date").reset_index(drop=True)
                got[sid] = (df, f"JODI annual CSVs {JODI_FIRST_YEAR}-{year_now}")
            elif sid not in errors:
                errors[sid] = "no rows at the pinned unit (this reporter does not publish this measure)"

    for family, kind in (("disagg", "cftc_disagg"), ("legacy", "cftc_legacy")):
        if kind in kinds:
            try:
                frames = fetch_cftc_frames(family)
                for sid, s in want.items():
                    if s["kind"] == kind:
                        code, col = s["key"]
                        df = cftc_series(frames, code, col)
                        if df.empty:
                            errors[sid] = f"no rows for code {code} column {col}"
                        else:
                            got[sid] = (df, f"{len(frames)} CFTC files")
            except Exception as e:
                for sid, s in want.items():
                    if s["kind"] == kind:
                        errors[sid] = f"{type(e).__name__}: {e}"

    for sid, s in want.items():
        if s["kind"] == "yf":
            try:
                df = fetch_yf(s["key"])
                if df.empty:
                    errors[sid] = "Yahoo returned nothing"
                else:
                    got[sid] = (df, "")
            except Exception as e:
                errors[sid] = f"{type(e).__name__}: {e}"
    return got, errors


# ----------------------------------------------------------------------------------------------
# Seeds (committed, licence-permitting) and the manifest
# ----------------------------------------------------------------------------------------------

def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_seed(sid, df, retrieved_at):
    SEED_DIR.mkdir(parents=True, exist_ok=True)
    path = SEED_DIR / f"{sid}.csv"
    df[["date", "value"]].to_csv(path, index=False)
    man = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    s = SPECS[sid]
    man[sid] = {"source_url": s["url"], "licence": s["licence"], "retrieved_at": retrieved_at,
                "rows": int(len(df)), "first": str(df["date"].min()), "last": str(df["date"].max()),
                "sha256": _sha256(path), "registered_in": s["src"]}
    MANIFEST.write_text(json.dumps(dict(sorted(man.items())), indent=1) + "\n")
    return path


def read_seeds(only=None):
    """{series_id: (DataFrame, retrieved_at)} from data/seed/ripple/, checking the manifest hash."""
    if not MANIFEST.exists():
        return {}
    man = json.loads(MANIFEST.read_text())
    out = {}
    for sid, meta in man.items():
        if only and not sid.startswith(only):
            continue
        path = SEED_DIR / f"{sid}.csv"
        if not path.exists():
            continue
        if _sha256(path) != meta["sha256"]:
            raise ValueError(f"seed {path.name} does not match MANIFEST sha256 -- refusing to load")
        df = pd.read_csv(path, dtype={"date": str})
        out[sid] = (df, meta["retrieved_at"])
    return out


# ----------------------------------------------------------------------------------------------
# DB writes
# ----------------------------------------------------------------------------------------------

def load_into(conn, sid, df, retrieved_at):
    s = SPECS[sid]
    conn.executemany("INSERT OR IGNORE INTO entities VALUES (?,?,?,?)", ENTITIES)
    conn.execute("INSERT OR REPLACE INTO series VALUES (?,?,?,?,?,?,?,?)",
                 (sid, s["name"], s["entity"], s["unit"], s["freq"], s["source"], s["url"],
                  f"{s['src']}; licence: {s['licence']}"))
    before = conn.execute("SELECT COUNT(*) FROM observations WHERE series_id=?", (sid,)).fetchone()[0]
    conn.executemany("INSERT OR IGNORE INTO observations VALUES (?,?,?,?,?)",
                     [(sid, str(d), float(v), str(d), retrieved_at) for d, v in zip(df["date"], df["value"])])
    after = conn.execute("SELECT COUNT(*) FROM observations WHERE series_id=?", (sid,)).fetchone()[0]
    return after - before


def _connect():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _db import connect
    return connect(DB)


def _report(sid, df, extra="", added=None):
    tag = f"  +{added:>6,} new" if added is not None else ""
    print(f"  {sid:<34} {SPECS[sid]['freq']:<8} {len(df):>6,} rows  {df['date'].min()} .. {df['date'].max()}{tag}  {extra}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refresh", action="store_true", help="pull live; write seeds where licence allows; load DB")
    ap.add_argument("--verify", action="store_true", help="pull live; print inventory; write nothing")
    ap.add_argument("--only", default=None, help="series_id prefix filter")
    args = ap.parse_args(argv)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    if args.verify or args.refresh:
        got, errors = fetch_live(args.only)
        print(f"live fetch {now}: {len(got)} series ok, {len(errors)} failed")
        if args.verify:
            for sid, (df, extra) in got.items():
                _report(sid, df, extra)
            for sid, e in errors.items():
                print(f"  ! {sid:<32} {e}")
            return 0
        conn = _connect()
        for sid, (df, extra) in got.items():
            added = load_into(conn, sid, df, now)
            if SPECS[sid]["seed"]:
                write_seed(sid, df, now)
            _report(sid, df, extra + (" [seeded]" if SPECS[sid]["seed"] else " [refresh-only, not seeded]"), added)
        for sid, e in errors.items():
            print(f"  ! {sid:<32} {e}")
        conn.commit(); conn.close()
        return 0 if not errors else 1

    seeds = read_seeds(args.only)
    if not seeds:
        print("no seeds found under data/seed/ripple/ -- run with --refresh first")
        return 1
    conn = _connect()
    for sid, (df, retrieved_at) in seeds.items():
        added = load_into(conn, sid, df, retrieved_at)
        _report(sid, df, f"seed retrieved {retrieved_at}", added)
    skipped = [sid for sid, s in SPECS.items() if not s["seed"] and (not args.only or sid.startswith(args.only))]
    if skipped:
        print(f"  ({len(skipped)} refresh-only series not seeded by licence; run --refresh to pull them live)")
    conn.commit(); conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
