"""
fetch_predmkt.py -- prediction-market odds (Polymarket), the priced-probability anchor.

WHY THIS EXISTS: the engine's whole thesis is "our read vs. what's PRICED." A
prediction market is a continuously-priced probability of exactly the geopolitical /
oil events we track ("Strait of Hormuz traffic returns to normal?", "US seizes an
Iran-linked oil tanker?"). Bridgewater's AIA Forecaster (arXiv:2511.07678) found an
ensemble of a model WITH market consensus beats consensus alone -- markets carry
additive information. So we ingest them as a live signal to sit beside the engine's read.

DISCIPLINE: this is DISPLAY / CONTEXT, never stats-safe. Prediction-market prices are
risk-neutral probabilities from thin/gameable markets -- great context, never fed into
the registered H1-H3 statistics. Stored tagged (source='Polymarket'), and thin markets
carry their volume so downstream can discount them (favorite-longshot bias, whales).

Polymarket's Gamma API is free and needs NO auth for data. We discover relevant markets
via keyword search, then snapshot each one's probability daily into observations.

Run:  python3 src/fetch_predmkt.py
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT_JSON = ROOT / "data" / "predmkt.json"
SEARCH = "https://gamma-api.polymarket.com/public-search"
UA = {"User-Agent": "ripple-engine/1.0 (research)"}

# Discovery queries -- the oil / geopolitics surface the engine cares about.
QUERIES = ["oil", "crude", "brent", "wti", "opec", "iran oil", "strait of hormuz",
           "saudi", "houthi", "red sea shipping", "russia oil", "oil sanctions",
           "natural gas", "gasoline price"]
# Keep only markets with at least this much traded volume (thin markets are noise).
MIN_VOLUME = 1000.0


def _f(x, default=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def parse_market(m, query=""):
    """A Gamma market dict -> a flat record, or None if not a usable live binary.
    Pure function (no I/O) so it can be unit-tested."""
    if not m or m.get("closed") or not m.get("active"):
        return None
    slug = m.get("slug") or str(m.get("id") or "")
    if not slug:
        return None
    # outcomes / outcomePrices arrive as JSON-encoded strings.
    try:
        outcomes = json.loads(m.get("outcomes") or "[]")
        prices = [float(p) for p in json.loads(m.get("outcomePrices") or "[]")]
    except (ValueError, TypeError):
        return None
    if len(prices) < 2 or not outcomes:
        return None
    vol = _f(m.get("volume"))
    return {
        "series_id": f"predmkt.polymarket.{slug}",
        "slug": slug,
        "question": (m.get("question") or "").strip(),
        "outcome": str(outcomes[0]),
        "prob": round(prices[0], 4),          # P(first outcome), 0..1
        "volume": round(vol, 0),
        "liquidity": round(_f(m.get("liquidity")), 0),
        "end_date": (m.get("endDate") or "")[:10],
        "url": f"https://polymarket.com/event/{m.get('slug') or slug}",
        "query": query,
    }


def _markets_from_event(ev):
    """Yield the market dicts nested under a search 'event' (or the event itself)."""
    mk = ev.get("markets")
    if isinstance(mk, list) and mk:
        yield from mk
    elif ev.get("outcomePrices"):
        yield ev


def discover():
    """Search each query term, collect unique relevant markets (dedup by slug)."""
    found = {}
    for q in QUERIES:
        try:
            r = requests.get(SEARCH, params={"q": q, "limit_per_type": 20},
                             headers=UA, timeout=20)
            events = r.json().get("events", []) if r.ok else []
        except (requests.RequestException, ValueError) as e:
            print(f"  search '{q}' failed ({type(e).__name__}) -- skipped.")
            continue
        for ev in events:
            for m in _markets_from_event(ev):
                rec = parse_market(m, query=q)
                if rec and rec["volume"] >= MIN_VOLUME:
                    found[rec["slug"]] = rec        # dedup: last query wins
    return sorted(found.values(), key=lambda r: r["volume"], reverse=True)


def store(conn, records, now, today):
    """Register each market as a series and snapshot today's probability. Daily
    snapshot (INSERT OR REPLACE on the day) so we get one clean point per day."""
    for r in records:
        conn.execute(
            "INSERT OR IGNORE INTO series "
            "(series_id, name, entity_id, unit, frequency, source, source_url, notes) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (r["series_id"], r["question"][:200], None, "probability", "daily",
             "Polymarket", r["url"],
             f"outcome={r['outcome']}; ends {r['end_date']}; DISPLAY/context only"))
        conn.execute(
            "INSERT OR REPLACE INTO observations "
            "(series_id, obs_date, value, as_of, retrieved_at) VALUES (?,?,?,?,?)",
            (r["series_id"], today, r["prob"], today, now))
    conn.commit()


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    today = now[:10]
    records = discover()
    conn = sqlite3.connect(DB)
    store(conn, records, now, today)
    conn.close()
    OUT_JSON.write_text(json.dumps(
        {"as_of": today, "generated_at": now, "source": "Polymarket (free)",
         "caveat": "Market-implied (risk-neutral) probabilities. DISPLAY/context "
                   "only -- never fed to the registered statistics. Thin markets "
                   "(low volume) are unreliable; de-bias longshots.",
         "markets": records}, indent=2))
    print(f"fetch_predmkt -- {len(records)} oil/geopolitics markets snapshot "
          f"({today}).")
    for r in records[:8]:
        print(f"  {r['prob']*100:5.1f}%  {r['question'][:56]:56}  vol={r['volume']:.0f}")


if __name__ == "__main__":
    main()
