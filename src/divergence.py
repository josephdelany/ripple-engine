"""
divergence.py -- the autonomous analyst's EYES (deterministic gap detection).

The two analyses Claude gave in chat weren't magic -- they were *divergences* between
what the engine SEES (attention, physical flow, corroboration) and what the market
PRICES. This module computes those divergences DETERMINISTICALLY, every run, so the
"analytical insight" is a reproducible number, not an LLM's opinion. An LLM (Claude,
on the subscription -- see ops/analyst.md) then merely writes them up; it can never
invent an edge the data doesn't show, because the gaps are pre-computed here.

Two detectors (both reproduce a real chat analysis):
  1. attention_vs_priced -- a chokepoint whose ATTENTION is spiking while the market
     prices its disruption cheap = the crowd looking away from a rising signal.
  2. market_movers -- prediction-market odds that have MOVED the most (from the
     committed daily snapshots) = the market quietly repricing something.

Output: data/divergence.json (ranked candidate reads, tagged + sourced). This is
DISPLAY/context -- it surfaces gaps, it does not forecast.

Run:  python3 src/divergence.py
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "divergence.json"

# chokepoint -> (Wikipedia page label, predmkt question keywords, framing)
CHOKEPOINTS = [
    ("Bab el-Mandeb", "Bab el-Mandeb", ["bab el-mandeb"], "closed"),
    ("Strait of Hormuz", "Strait of Hormuz", ["strait of hormuz", "hormuz"], "normal"),
    ("Suez Canal", "Suez Canal", ["suez"], "closed"),
]


def _rj(name):
    p = ROOT / "data" / name
    try:
        return json.loads(p.read_text()) if p.exists() else {}
    except (ValueError, OSError):
        return {}


def attention_vs_priced(wiki_pages, markets):
    """A chokepoint with spiking attention but a cheap/thin priced disruption =
    'the crowd is looking away from a rising signal.' Pure (testable)."""
    att = {p["page"]: p for p in wiki_pages}
    out = []
    for name, page, kws, framing in CHOKEPOINTS:
        a = att.get(page)
        if not a or a.get("flag") not in ("spike", "elevated"):
            continue
        # best-matching, most-liquid priced market for this chokepoint.
        cand = [m for m in markets
                if any(k in (m.get("question") or "").lower() for k in kws)]
        if not cand:
            continue
        m = max(cand, key=lambda m: m.get("volume", 0))
        prob = m.get("prob", 0)
        # disruption probability: 'closed' markets price disruption directly;
        # 'normal' markets price the opposite, so invert.
        disruption = prob if framing == "closed" else round(1 - prob, 2)
        out.append({
            "type": "attention_vs_priced", "subject": name,
            "attention": f"{a.get('pct_of_median')}x ({a.get('flag')})",
            "attention_pct": a.get("pct_of_median", 0),
            "priced_disruption": f"{disruption*100:.0f}%",
            "priced_volume": m.get("volume", 0),
            "market": m.get("question", ""), "market_url": m.get("url", ""),
            "note": f"{name}: attention {a.get('pct_of_median')}x while the market "
                    f"prices disruption at {disruption*100:.0f}% "
                    f"(${m.get('volume',0):,.0f} vol) -- signal rising ahead of price.",
        })
    return sorted(out, key=lambda d: d["attention_pct"], reverse=True)


def market_movers(conn, lookback=14, min_move=0.08):
    """Prediction markets whose probability moved most over the committed snapshots
    -- the market quietly repricing something. Needs >=2 days of snapshots."""
    movers = []
    sids = [r[0] for r in conn.execute(
        "SELECT DISTINCT series_id FROM observations WHERE series_id LIKE 'predmkt.%'")]
    for sid in sids:
        rows = conn.execute(
            "SELECT obs_date, value FROM observations WHERE series_id=? "
            "ORDER BY obs_date DESC LIMIT ?", (sid, lookback)).fetchall()
        if len(rows) < 2:
            continue
        latest, earliest = rows[0][1], rows[-1][1]
        move = latest - earliest
        if abs(move) < min_move:
            continue
        name = conn.execute("SELECT name FROM series WHERE series_id=?",
                            (sid,)).fetchone()
        movers.append({
            "type": "market_mover", "market": name[0] if name else sid,
            "from": f"{earliest*100:.0f}%", "to": f"{latest*100:.0f}%",
            "move": round(move, 3), "days": len(rows),
            "note": f"'{(name[0] if name else sid)[:60]}' repriced "
                    f"{earliest*100:.0f}% -> {latest*100:.0f}% over {len(rows)} days.",
        })
    return sorted(movers, key=lambda d: abs(d["move"]), reverse=True)[:8]


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    wiki = _rj("wiki_attention.json").get("pages", [])
    markets = _rj("predmkt.json").get("markets", [])
    conn = sqlite3.connect(DB)
    gaps = attention_vs_priced(wiki, markets)
    movers = market_movers(conn)
    conn.close()
    OUT.write_text(json.dumps(
        {"as_of": now[:10], "generated_at": now,
         "note": "Deterministic divergences between what the engine sees and what "
                 "the market prices. DISPLAY/context -- surfaces gaps, never forecasts.",
         "attention_vs_priced": gaps, "market_movers": movers}, indent=2))
    print(f"divergence -- {len(gaps)} attention-vs-priced gaps, "
          f"{len(movers)} market movers.")
    for g in gaps[:3]:
        print(f"  GAP  {g['note']}")
    for m in movers[:3]:
        print(f"  MOVE {m['note']}")


if __name__ == "__main__":
    main()
