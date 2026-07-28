"""
fetch_market_live.py -- the FRESH real-price spine (Sprint 2 core; free, autonomous-safe).

The engine was showing a WEEK-STALE Brent (FRED, lagged) and missed a 7% move. This pulls
the live oil complex + risk assets from Yahoo (yfinance) -- free, no key, runs headless in
GitHub Actions -- and writes them to data/market_live.json with a freshness stamp, and into
the canonical `observations` table as live.* series (point-in-time: as_of = obs date,
retrieved_at = now). When I (Claude) am driving interactively, FMP can override for the
sharpest read; the autonomous loop uses this.

Degrades gracefully: if Yahoo is unreachable, writes an honest stale marker rather than
crashing or interpolating. NOT a registered statistic -- a live display/analysis feed.

Run:  python3 src/fetch_market_live.py
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "market_live.json"

# clean id -> (yfinance symbol, human name, unit)
ASSETS = {
    "live.brent": ("BZ=F", "Brent crude", "USD/bbl"),
    "live.wti": ("CL=F", "WTI crude", "USD/bbl"),
    "live.natgas": ("NG=F", "Henry Hub natgas", "USD/MMBtu"),
    "live.gold": ("GC=F", "Gold", "USD/oz"),
    "live.vix": ("^VIX", "VIX", "index"),
    "live.us10y": ("^TNX", "US 10Y yield", "percent"),
    "live.dxy": ("DX-Y.NYB", "US dollar index", "index"),
    "live.xle": ("XLE", "Energy equities (XLE)", "USD"),
    "live.sp500": ("^GSPC", "S&P 500", "index"),
}


def pct(a, b):
    return round((a / b - 1) * 100, 2) if (b and b == b) else None


def fetch():
    """Pull ~20 sessions for each asset; return {id: {price, chg1d, chg5d, as_of}} or {}."""
    import yfinance as yf
    syms = [v[0] for v in ASSETS.values()]
    df = yf.download(syms, period="20d", interval="1d", progress=False,
                     auto_adjust=True, threads=True)
    if df is None or df.empty:
        return {}
    close = df["Close"]
    out = {}
    for sid, (sym, name, unit) in ASSETS.items():
        try:
            s = close[sym].dropna()
        except (KeyError, TypeError):
            continue
        if len(s) < 2:
            continue
        last = float(s.iloc[-1])
        out[sid] = {"name": name, "unit": unit, "price": round(last, 2),
                    "chg1d": pct(last, float(s.iloc[-2])),
                    "chg5d": pct(last, float(s.iloc[-6])) if len(s) >= 6 else None,
                    "as_of": s.index[-1].date().isoformat()}
    return out


def store(conn, data, now):
    """Upsert the latest value of each live series into observations (point-in-time)."""
    cur = conn.cursor()
    for sid, d in data.items():
        cur.execute("INSERT OR IGNORE INTO series VALUES (?,?,?,?,?,?,?,?)",
                    (sid, d["name"], None, d["unit"], "daily", "Yahoo (yfinance)",
                     "https://finance.yahoo.com", "live real-price feed; display/analysis only"))
        cur.execute("INSERT OR REPLACE INTO observations VALUES (?,?,?,?,?)",
                    (sid, d["as_of"], d["price"], d["as_of"], now))
    conn.commit()


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    try:
        data = fetch()
    except Exception as e:                       # yfinance/network can fail; degrade honestly
        data = {}
        print(f"fetch_market_live -- WARN: live fetch failed ({type(e).__name__}: {e}).")

    if not data:
        OUT.write_text(json.dumps({"as_of": None, "generated_at": now, "stale": True,
                                   "note": "live fetch failed; engine falls back to FRED."},
                                  indent=2))
        print("fetch_market_live -- no live data; wrote stale marker.")
        return

    conn = sqlite3.connect(DB)
    store(conn, data, now)
    conn.close()
    freshest = max(d["as_of"] for d in data.values())
    OUT.write_text(json.dumps({"as_of": freshest, "generated_at": now, "stale": False,
                               "source": "Yahoo (yfinance)", "assets": data}, indent=2))
    b = data.get("live.brent", {})
    print(f"fetch_market_live -- {len(data)} assets, freshest {freshest}. "
          f"Brent {b.get('price')} ({b.get('chg1d')}% 1d, {b.get('chg5d')}% 5d).")


if __name__ == "__main__":
    main()
