"""
fetch_wider_nodes.py -- broaden the ripple map to commodities + macro, keyless (Step 1).

Six analyst domains, one engine: adding these nodes lets the SAME validated framework speak to
commodities, macro, ME-risk and supply-chain at once. All free/keyless:
  - Commodity daily futures via yfinance (already a dependency): gold, copper, silver, wheat,
    palladium (FRED blocks gold/palladium; Yahoo serves them). gold=safe-haven, copper=growth,
    wheat=food security, palladium=Russia supply-chain node.
  - Macro via keyless FRED: S&P 500 (risk), high-yield credit spread (stress), CNY (China).
New data = new rows in observations (as_of = obs date, point-in-time); no schema change. Degrades
gracefully per source. These are NODES for the conditioned ripple map / propagation graph -- each
is then VALIDATED (or nulled) through the gate, never asserted.

Run:  python3 src/fetch_wider_nodes.py
"""

import io
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd=1980-01-01"

# clean series_id -> (yfinance symbol, entity, name, unit)
YF_NODES = {
    "yf.gold":      ("GC=F", "commodity.gold",      "Gold (COMEX front)",      "USD/oz"),
    "yf.copper":    ("HG=F", "commodity.copper",    "Copper (COMEX front)",    "USD/lb"),
    "yf.silver":    ("SI=F", "commodity.silver",    "Silver (COMEX front)",    "USD/oz"),
    "yf.wheat":     ("ZW=F", "commodity.wheat",     "Wheat (CBOT front)",      "USc/bu"),
    "yf.palladium": ("PA=F", "commodity.palladium", "Palladium (NYMEX front)", "USD/oz"),
    # macro nodes via yfinance for FULL history (FRED keyless caps SP500 to 10y and HY-spread to 3y,
    # which was an UNFAIR test at n=30/n=5). ^GSPC -> 1927; HYG (HY-credit ETF, inverse of spreads) -> 2007.
    "yf.sp500":     ("^GSPC", "macro.equities",     "S&P 500 index",           "index"),
    "yf.hyg":       ("HYG",   "macro.credit",       "HY credit ETF (HYG)",     "USD"),
}
# FRED keyless macro nodes (full-history ones only)
FRED_NODES = {
    "fred.DEXCHUS":      ("country.china",  "CNY per USD (China FX)",      "CNY/USD"),
}
ENTITIES = [
    ("commodity.gold", "commodity", "Gold", "safe-haven metal"),
    ("commodity.copper", "commodity", "Copper", "growth/industrial metal"),
    ("commodity.silver", "commodity", "Silver", "precious/industrial metal"),
    ("commodity.wheat", "commodity", "Wheat", "food-security grain"),
    ("commodity.palladium", "commodity", "Palladium", "Russia-concentrated PGM"),
    ("macro.equities", "macro", "Equities", "S&P 500"),
    ("macro.credit", "macro", "Credit", "US high-yield spread"),
    ("country.china", "country", "China", "CNY FX / demand"),
]


def _fred(sid):
    r = requests.get(FRED.format(sid=sid.split(".", 1)[1]), timeout=30)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df.columns = ["date", "value"]
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
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

    for sid, (sym, entity, name, unit) in YF_NODES.items():
        try:
            df = _yf(sym)
        except Exception as e:
            print(f"  ! {sid} ({sym}) failed: {type(e).__name__}: {e}"); continue
        if df is None or df.empty:
            print(f"  ! {sid} ({sym}) empty"); continue
        conn.execute("INSERT OR REPLACE INTO series VALUES (?,?,?,?,?,?,?,?)",
                     (sid, name, entity, unit, "daily", "Yahoo (yfinance)",
                      "https://finance.yahoo.com", "commodity node for the ripple map"))
        conn.executemany("INSERT OR IGNORE INTO observations VALUES (?,?,?,?,?)",
                         [(sid, d, v, d, now) for d, v in zip(df["date"], df["value"])])
        print(f"  {sid:<16} {len(df):>6,} rows  {df['date'].min()} .. {df['date'].max()}")

    for sid, (entity, name, unit) in FRED_NODES.items():
        try:
            df = _fred(sid)
        except Exception as e:
            print(f"  ! {sid} failed: {type(e).__name__}: {e}"); continue
        conn.execute("INSERT OR REPLACE INTO series VALUES (?,?,?,?,?,?,?,?)",
                     (sid, name, entity, unit, "daily", "FRED",
                      f"https://fred.stlouisfed.org/series/{sid.split('.',1)[1]}", "macro node for the ripple map"))
        conn.executemany("INSERT OR IGNORE INTO observations VALUES (?,?,?,?,?)",
                         [(sid, d, v, d, now) for d, v in zip(df["date"], df["value"])])
        print(f"  {sid:<16} {len(df):>6,} rows  {df['date'].min()} .. {df['date'].max()}")

    conn.commit()
    conn.close()
    print("wider nodes loaded (commodities via yfinance, macro via FRED; all keyless).")


if __name__ == "__main__":
    main()
