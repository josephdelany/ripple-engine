"""
fetch_value_chain.py -- the value chain: everything downstream of crude (VISION_ROADMAP V1.1).

An oil shock does not stop at crude. It flows down a chain of refined and derived products, each
with its own market and its own lag:

    crude -> refined fuels (gasoline, distillate, propane)
          -> petrochemicals (resins/plastics, from naphtha & ethylene)
          -> fertilizer (nitrogenous, from natural gas)
    and, in parallel, the global gas complex (US Henry Hub, European TTF, Asian LNG/JKM).

This adapter adds the priceable NODES for that chain. Same discipline as every other fetcher:
new data = new rows in the existing series/observations schema, NO new tables. Every series is
free + keyless (FRED's public CSV endpoint, or Yahoo front-month futures via yfinance -- the same
source the engine already uses for gold/copper/wheat).

Honest cadence labels: FRED daily petroleum spots publish with a few days' lag; the two PPI series
are MONTHLY and post ~mid the following month (see data/series_cadence_overrides.json -- they are
NOT mixed silently with the daily series). The cracks (gasoline/diesel margin) are DERIVED from
these prices in derive_signals.py, not here (mechanism-gated, per CLAUDE.md).

A note on fertilizer: the roadmap's first choice was the World Bank "Pink Sheet" DAP/urea spot
series. That workbook IS keyless, but its download URL is version-pinned and the copy reachable at
build time was frozen at 2025M12 -- shipping it would read STALE/DEAD on day one and lie about
freshness. The FRED nitrogenous-fertilizer PPI is keyless, stable, and current, and tracks the same
urea/DAP price direction, so it is the honest live proxy. WB Pink Sheet DAP/urea is left as a
richer-but-fragile upgrade for later.

Run:  python3 src/fetch_value_chain.py
"""

import io
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"

# FRED series: series_id -> (fred_id, entity_id, name, unit, frequency, why)
FRED_NODES = {
    "fred.DGASUSGULF": ("DGASUSGULF", "commodity.gasoline_spot",
        "US Gulf Coast Conventional Gasoline Spot", "USD/gal", "daily",
        "Refined-fuel node + the input to the gasoline crack (wholesale, not the GASREGW retail pump)."),
    "fred.DPROPANEMBTX": ("DPROPANEMBTX", "commodity.propane",
        "Mont Belvieu Propane Spot", "USD/gal", "daily",
        "NGL / petrochemical-feedstock node: propane tracks both the fuel and the petchem channel."),
    "fred.PCU325211325211": ("PCU325211325211", "commodity.petchem",
        "Plastics Material & Resins PPI", "index", "monthly",
        "Petrochemical proxy: resins are made from naphtha/ethylene, one hop downstream of crude."),
    "fred.PCU325311325311": ("PCU325311325311", "commodity.fertilizer",
        "Nitrogenous Fertilizer PPI", "index", "monthly",
        "Fertilizer proxy: nitrogen fertilizer is made from natural gas; proxy for urea/DAP prices."),
}

# Yahoo front-month futures: series_id -> (symbol, entity_id, name, unit)  [all daily]
YF_NODES = {
    "yf.ttf": ("TTF=F", "commodity.eu_gas",  "TTF Dutch Natural Gas (front)", "EUR/MWh"),
    "yf.jkm": ("JKM=F", "commodity.lng_asia", "JKM Asia LNG (front)",         "USD/MMBtu"),
}

ENTITIES = [
    ("commodity.gasoline_spot", "commodity", "Wholesale Gasoline", "US Gulf Coast conventional spot"),
    ("commodity.propane",       "commodity", "Propane",            "Mont Belvieu spot (NGL/petchem feedstock)"),
    ("commodity.petchem",       "commodity", "Petrochemicals",     "Plastics/resins PPI (naphtha/ethylene-derived)"),
    ("commodity.fertilizer",    "commodity", "Fertilizer",         "Nitrogenous PPI (gas-derived; urea/DAP proxy)"),
    ("commodity.eu_gas",        "commodity", "European Gas (TTF)",  "Dutch TTF hub, front futures"),
    ("commodity.lng_asia",      "commodity", "Asian LNG (JKM)",     "Japan-Korea Marker, front futures"),
]


def _fred(fred_id):
    r = requests.get(FRED.format(sid=fred_id), timeout=30)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"]).dt.date.astype(str)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")   # "." -> missing
    return df.dropna()


def _yf(symbol):
    import yfinance as yf
    df = yf.download(symbol, period="max", interval="1d", progress=False, auto_adjust=True)
    if df is None or df.empty:
        return None
    close = df["Close"]
    s = close.iloc[:, 0] if hasattr(close, "columns") else close   # single-symbol -> Series
    s = s.dropna()
    return pd.DataFrame({"date": [d.date().isoformat() for d in s.index],
                         "value": [float(v) for v in s.to_numpy()]})


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn = sqlite3.connect(DB)
    conn.executemany("INSERT OR IGNORE INTO entities VALUES (?,?,?,?)", ENTITIES)

    for series_id, (fred_id, entity, name, unit, freq, why) in FRED_NODES.items():
        try:
            df = _fred(fred_id)
        except Exception as e:
            print(f"  ! {series_id} failed: {type(e).__name__}: {e}"); continue
        conn.execute("INSERT OR REPLACE INTO series VALUES (?,?,?,?,?,?,?,?)",
                     (series_id, name, entity, unit, freq, "FRED",
                      f"https://fred.stlouisfed.org/series/{fred_id}", why))
        conn.executemany("INSERT OR IGNORE INTO observations VALUES (?,?,?,?,?)",
                         [(series_id, d, float(v), d, now) for d, v in zip(df["date"], df["value"])])
        print(f"  {series_id:<24} {freq:<8} {len(df):>6,} rows  {df['date'].min()} .. {df['date'].max()}")

    for series_id, (sym, entity, name, unit) in YF_NODES.items():
        try:
            df = _yf(sym)
        except Exception as e:
            print(f"  ! {series_id} ({sym}) failed: {type(e).__name__}: {e}"); continue
        if df is None or df.empty:
            print(f"  ! {series_id} ({sym}) empty (Yahoo returned nothing)"); continue
        conn.execute("INSERT OR REPLACE INTO series VALUES (?,?,?,?,?,?,?,?)",
                     (series_id, name, entity, unit, "daily", "Yahoo (yfinance)",
                      "https://finance.yahoo.com", "global-gas node for the value chain"))
        conn.executemany("INSERT OR IGNORE INTO observations VALUES (?,?,?,?,?)",
                         [(series_id, d, v, d, now) for d, v in zip(df["date"], df["value"])])
        print(f"  {series_id:<24} {'daily':<8} {len(df):>6,} rows  {df['date'].min()} .. {df['date'].max()}")

    conn.commit()
    conn.close()
    print("value-chain nodes loaded (keyless; monthly PPIs cadence-labelled, not mixed with daily).")


if __name__ == "__main__":
    main()
