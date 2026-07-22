"""
fetch_kalshi.py -- READ-ONLY reader for Kalshi's public market data.

WHY THIS EXISTS (the forecasting layer's benchmark):
A forecast is only meaningful against a yardstick. Kalshi is a regulated
prediction market: its "yes" price for a contract IS the crowd's implied
probability that the thing happens (a contract pays $1 if yes, so a 0.34 price =
a 34% implied chance). We read those prices to benchmark Joe's own forecasts.
The market is the null hypothesis; beating it, over time and on a Brier score, is
the only honest evidence of edge.

HARD RULES (see CLAUDE.md + TASK_BRIEF_02):
  * READ-ONLY. We only ever GET public market data. No auth, no orders, no
    trading endpoints -- ever. There is deliberately no code here that could
    place a trade.
  * If Kalshi ever starts requiring a key even for public quotes, this stops and
    tells Joe what to sign up for. We never scrape around a paywall.

Public API (no credentials needed for market data):
  https://api.elections.kalshi.com/trade-api/v2
Markets are grouped into "series" (e.g. KXBRENTD = Brent Oil Daily), each series
has dated "markets". We search series by keyword, then read their open markets.

Run as a demo:  python3 src/fetch_kalshi.py
Import it:      from fetch_kalshi import search_markets, market_price
"""

import requests

BASE = "https://api.elections.kalshi.com/trade-api/v2"

# The categories where energy / geopolitics markets actually live. We search
# series within these rather than paging tens of thousands of sports markets.
RELEVANT_CATEGORIES = ["Commodities", "World", "Economics", "Financials",
                       "Climate and Weather"]

TIMEOUT = 30


def _f(x):
    """Coerce a Kalshi price field (may be str, float, or None) to float or None."""
    if x is None or x == "":
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def implied_prob(market):
    """The market's implied probability for YES, in [0, 1].

    Prefer the bid/ask midpoint (the fairest single 'what the market thinks'
    number); fall back to the last traded price, then to whichever quote exists.
    Returns None if the market has no price at all (illiquid / no quotes).
    """
    bid = _f(market.get("yes_bid_dollars"))
    ask = _f(market.get("yes_ask_dollars"))
    last = _f(market.get("last_price_dollars"))
    if bid is not None and ask is not None and (bid > 0 or ask > 0):
        return round((bid + ask) / 2, 4)
    if last is not None and last > 0:
        return round(last, 4)
    for v in (ask, bid):
        if v is not None and v > 0:
            return round(v, 4)
    return None


def _series_blob(s):
    """All the searchable text of a series, lower-cased."""
    return (s.get("title", "") + " " + s.get("ticker", "") + " "
            + " ".join(s.get("tags") or [])).lower()


def find_series(keyword, categories=RELEVANT_CATEGORIES):
    """Return series whose title/ticker/tags contain the keyword (case-insensitive)."""
    kw = keyword.lower()
    hits = []
    for cat in categories:
        r = requests.get(BASE + "/series", params={"category": cat}, timeout=TIMEOUT)
        r.raise_for_status()
        for s in r.json().get("series", []):
            if kw in _series_blob(s):
                hits.append(s)
    return hits


def open_markets_for_series(series_ticker, limit=50):
    """Fetch the currently-open markets under one series."""
    r = requests.get(BASE + "/markets",
                     params={"series_ticker": series_ticker, "status": "open",
                             "limit": limit},
                     timeout=TIMEOUT)
    r.raise_for_status()
    return r.json().get("markets", [])


def search_markets(keyword, max_markets=25):
    """Search open Kalshi markets by keyword.

    Returns a list of simple dicts: ticker, title, subtitle, implied_prob,
    series, close_time. Only markets that currently have a price are returned,
    because a probability with no market behind it is not a benchmark.
    """
    out = []
    for s in find_series(keyword):
        for m in open_markets_for_series(s["ticker"]):
            p = implied_prob(m)
            if p is None:
                continue
            out.append({
                "ticker": m.get("ticker"),
                "title": m.get("title"),
                "subtitle": m.get("yes_sub_title"),
                "implied_prob": p,
                "series": s["ticker"],
                "close_time": m.get("close_time"),
            })
            if len(out) >= max_markets:
                return out
    return out


def market_price(ticker):
    """Fetch ONE market by ticker; return its implied probability (or None).

    This is what forecast_log.py calls to auto-fill the market benchmark for a
    forecast Joe logs against a specific Kalshi ticker.
    """
    r = requests.get(BASE + f"/markets/{ticker}", timeout=TIMEOUT)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return implied_prob(r.json().get("market", {}))


def main():
    """Demo: print a handful of oil / geopolitics markets with implied odds."""
    print("Kalshi public market data (READ-ONLY). The 'yes' price = implied "
          "probability.\n")
    seen, shown = set(), 0
    # Spread the demo across keywords so it shows variety, not five near-identical
    # strikes of one series (up to 2 per keyword, 5 total).
    for keyword in ["Brent", "WTI", "OPEC", "Hormuz", "crude", "oil"]:
        if shown >= 5:
            break
        try:
            markets = search_markets(keyword, max_markets=8)
        except requests.RequestException as e:
            print(f"  [{keyword}] request failed: {type(e).__name__} -- "
                  f"if this is an auth error, tell Joe; we do not scrape.")
            continue
        per_kw = 0
        for m in markets:
            if m["ticker"] in seen or shown >= 5 or per_kw >= 2:
                continue
            seen.add(m["ticker"])
            print(f"  {m['implied_prob']*100:5.1f}%  {m['ticker']}")
            print(f"          {m['title']}")
            shown += 1
            per_kw += 1

    if not shown:
        print("  No priced oil/geopolitics markets are open right now. The reader "
              "works;\n  Kalshi simply has none live at the moment. Try again later.")
    else:
        print(f"\nShowing {shown} live markets. These are the benchmarks a logged "
              "forecast is scored against.")


if __name__ == "__main__":
    main()
