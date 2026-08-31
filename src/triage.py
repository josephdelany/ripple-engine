"""
triage.py -- "throw anything at it": one card for any news item (VISION_ROADMAP V4).

Paste a headline / paragraph / URL and get ONE card: what the engine thinks it is (entities + event
type, extracted deterministically from the vocab -- no LLM in the loop, no fabrication), the nearest
VERIFIED historical analogues (real corpus events, with their sources), a BACKGROUND count from the
reference tier (labelled, never corpus), and an EXPECTED-MAGNITUDE read = the event class's historical
base rate x today's registered amplifier state (H1/VIX). n and range are ALWAYS shown.

CAGE (hard rules, enforced here):
  * analogues are only REAL corpus events -- never invented.
  * the score is an expected MAGNITUDE (abnormal-move size), NEVER an occurrence probability.
  * every card carries its caveats and a latency receipt (paste -> card, in ms).

Reuses: the entity vocab (entities table), event_study (CAR base rates), reference_tier (background),
engine_read.json (the live H1 amplifier state). $0 / keyless / deterministic.

Run:  python3 src/triage.py "Iran seizes a tanker in the Strait of Hormuz"
      python3 src/triage.py https://example.com/story
"""

import json
import re
import sqlite3
import sys
import time
from pathlib import Path

import numpy as np

import event_study as ES
import reference_tier as RT

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
ENGINE_READ = ROOT / "data" / "engine_read.json"

# Event-type keyword rules (deterministic classifier; first match by priority wins).
TYPE_RULES = [
    ("chokepoint_disruption", r"\b(strait|canal|chokepoint|blockade|blocked|transit|hormuz|suez|"
                              r"bab[- ]el[- ]mandeb|pipeline (halt|closed|shut)|reroute)\b"),
    ("infrastructure_attack", r"\b(strike|struck|attack|drone|missile|sabotage|explosion|refinery|"
                              r"oil field|terminal|facility|set (on )?fire)\b"),
    ("opec_decision",         r"\b(opec|opec\+|quota|production (cut|hike|target)|output (cut|target)|"
                              r"barrels per day|mb/?d|voluntary cut)\b"),
    ("sanctions",             r"\b(sanctions?|sanctioned|embargo|price cap|export ban|blacklist|"
                              r"designat|waiver)\b"),
    ("conflict_escalation",   r"\b(invade|invasion|war|coup|mutiny|offensive|escalat|militar|troops|"
                              r"clash|airstrike|rebellion)\b"),
    ("demand_shock",          r"\b(recession|demand|pandemic|lockdown|stimulus|tariff|trade (deal|war)|"
                              r"subsidy|gdp|growth outlook)\b"),
    ("policy_response",       r"\b(spr|strategic (petroleum )?reserve|release|permit|revoke|intervention|"
                              r"price control)\b"),
]


def classify_type(text):
    """Type-only classifier (no DB) -- used to rank the wire by expected magnitude. Returns type|None."""
    low = (text or "").lower()
    return next((t for t, pat in TYPE_RULES if re.search(pat, low)), None)


def base_rate_by_type():
    """{event_type -> expected-magnitude %} for ranking, from the committed engine_read base rates
    (|mean CAR+20|). Fast (no recompute); 0 for types not present."""
    try:
        br = json.loads(ENGINE_READ.read_text()).get("base_rates", [])
        return {r["type"]: abs(float(r.get("car20") or 0)) for r in br}
    except (OSError, ValueError, KeyError):
        return {}


def wire_score(headline, rates=None):
    """Expected-magnitude rank score for one wire headline: base-rate |CAR20| of its classified type."""
    rates = base_rate_by_type() if rates is None else rates
    t = classify_type(headline)
    return {"type": t, "expected_magnitude_pct": round(rates.get(t, 0.0), 2) if t else 0.0}


def _text_from(arg):
    """Return (text, was_url). If arg looks like a URL, fetch + crude-strip HTML (keyless)."""
    if re.match(r"^https?://", arg.strip()):
        try:
            import requests
            html = requests.get(arg.strip(), timeout=15,
                                headers={"User-Agent": "ripple-engine triage (research)"}).text
            text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
            text = re.sub(r"<[^>]+>", " ", text)
            return re.sub(r"\s+", " ", text)[:4000], True
        except Exception:
            return arg, True                       # fetch failed -> treat the URL string as text
    return arg, False


def extract(conn, text):
    """Deterministic extraction: entity_ids whose name/id appears in the text, + the event type."""
    low = text.lower()
    ents = []
    for eid, name in conn.execute("SELECT entity_id, name FROM entities"):
        tail = eid.split(".", 1)[-1].replace("_", " ")
        for needle in {(name or "").lower(), tail.lower()}:
            if len(needle) >= 3 and re.search(r"\b" + re.escape(needle) + r"\b", low):
                ents.append(eid); break
    etype = next((t for t, pat in TYPE_RULES if re.search(pat, low)), None)
    return sorted(set(ents)), etype


def _car20(ret, date):
    car = ES.car_for_event(ret, date)
    return abs(float(car[ES.PRE + 20])) * 100 if car is not None else None


def base_rate(conn, ret, etype):
    """|CAR+20| distribution in Brent for the event class: mean, n, range. Always shown honestly."""
    rows = conn.execute("SELECT event_date FROM events WHERE type=?", (etype,)).fetchall()
    mags = [m for (d,) in rows if (m := _car20(ret, d)) is not None]
    if not mags:
        return None
    a = np.array(mags)
    return {"n": len(a), "mean_abs_car20_pct": round(float(a.mean()), 2),
            "range_pct": [round(float(a.min()), 2), round(float(a.max()), 2)],
            "iqr_pct": [round(float(np.percentile(a, 25)), 2), round(float(np.percentile(a, 75)), 2)]}


def analogs(conn, ret, ents, etype, k=5):
    """Nearest VERIFIED corpus analogues: score by type match + entity overlap. Real events only."""
    entset = set(ents)
    scored = []
    for eid, d, t, title, url in conn.execute(
            "SELECT event_id, event_date, type, title, source_url FROM events"):
        eents = {r[0] for r in conn.execute(
            "SELECT entity_id FROM event_entities WHERE event_id=?", (eid,))}
        score = (2 if t == etype else 0) + len(entset & eents)
        if score <= 0:
            continue
        scored.append((score, {"event_id": eid, "date": d, "type": t, "title": title,
                               "source_url": url, "abs_car20_pct": _car20(ret, d)}))
    scored.sort(key=lambda s: (s[0], s[1]["abs_car20_pct"] or 0), reverse=True)
    return [a for _, a in scored[:k]]


def amplifier():
    """Today's REGISTERED amplifier state (H1/VIX) from the live engine read. Only H1 (validated) counts."""
    try:
        er = json.loads(ENGINE_READ.read_text())
        h1 = (er.get("hypotheses", {}) or {}).get("H1", {})
        return {"registered_amplifier": "H1 (VIX stress)", "state": h1.get("amplifier", "?"),
                "vix_pct": h1.get("latest"), "event_median": h1.get("event_median"),
                "as_of": h1.get("as_of_reading"),
                "note": ("H1 ON -> the registered +5pp stress amplification applies to |CAR+20|"
                         if h1.get("amplifier") == "ON" else
                         "H1 OFF -> no stress amplification today; expect the unamplified base rate")}
    except (OSError, ValueError):
        return {"registered_amplifier": "H1 (VIX stress)", "state": "unknown"}


def triage(arg):
    t0 = time.perf_counter()
    text, was_url = _text_from(arg)
    conn = sqlite3.connect(DB)
    ret = ES.load_returns(conn)
    ents, etype = extract(conn, text)
    br = base_rate(conn, ret, etype) if etype else None
    ana = analogs(conn, ret, ents, etype) if etype else []
    bg = RT.nearest(_guess_date(text), type=etype or "", k=5) if etype else {"n": 0}
    amp = amplifier()
    px = conn.execute("SELECT value FROM observations WHERE series_id='fred.DCOILBRENTEU' "
                      "ORDER BY obs_date DESC LIMIT 1").fetchone()
    conn.close()
    brent = float(px[0]) if px else None
    usd = round(br["mean_abs_car20_pct"] / 100 * brent, 2) if (br and brent) else None
    latency_ms = round((time.perf_counter() - t0) * 1000, 1)
    return {
        "input": arg[:200], "was_url": was_url,
        "extracted": {"entities": ents, "event_type": etype,
                      "note": "deterministic vocab/keyword extraction -- no LLM, no fabrication"},
        "expected_magnitude": None if not br else {
            "event_class": etype, "base_rate": br,
            "current_amplifier": amp,
            "tradeable_terms": (f"~{br['mean_abs_car20_pct']}% of a 20-day abnormal Brent move "
                                f"~= ${usd}/bbl at ${brent:.0f}; effect SIZE, research not advice"
                                if usd else None),
            "caveat": "EXPECTED MAGNITUDE (size of the abnormal move), NOT an occurrence probability."},
        "nearest_verified_analogs": ana,
        "background_reference": {"label": bg.get("tier_label", RT.LABEL),
                                 "n_nearby": bg.get("n", 0), "events": bg.get("events", [])},
        "caveats": ["analogues are real corpus events only (no invented analogues)",
                    "no occurrence probability is given -- expected magnitude only",
                    "base rate is unconditional unless the amplifier is ON; n + range shown"],
        "latency_ms": latency_ms,
    }


def _guess_date(text):
    m = re.search(r"\b(20\d{2})-(\d{2})-(\d{2})\b", text) or re.search(r"\b(20\d{2})\b", text)
    if not m:
        return "2026-08-04"
    return m.group(0) if "-" in m.group(0) else f"{m.group(1)}-01-01"


def _card_text(c):
    L = [f"TRIAGE CARD  (latency {c['latency_ms']}ms)", "=" * 60,
         f"input: {c['input']}", f"type: {c['extracted']['event_type'] or 'UNCLASSIFIED'}   "
         f"entities: {', '.join(c['extracted']['entities']) or 'none matched'}"]
    em = c["expected_magnitude"]
    if em:
        br, amp = em["base_rate"], em["current_amplifier"]
        L += ["", f"EXPECTED MAGNITUDE (class {em['event_class']}):",
              f"  base rate |CAR+20| = {br['mean_abs_car20_pct']}%  (n={br['n']}, "
              f"range {br['range_pct']}, IQR {br['iqr_pct']})",
              f"  registered amplifier {amp['registered_amplifier']}: {amp['state']} "
              f"(VIX {amp.get('vix_pct')} vs median {amp.get('event_median')})",
              f"  {amp.get('note','')}",
              f"  tradeable: {em['tradeable_terms']}", f"  ! {em['caveat']}"]
    else:
        L += ["", "EXPECTED MAGNITUDE: n/a (event type not classified from the vocab)"]
    L += ["", "NEAREST VERIFIED ANALOGUES (real corpus events):"]
    for a in c["nearest_verified_analogs"]:
        mag = f"{a['abs_car20_pct']:.1f}%" if a["abs_car20_pct"] is not None else "n/a"
        L.append(f"  {a['date']} {a['type']:22} |CAR20|={mag:>6}  {a['title'][:42]}")
    if not c["nearest_verified_analogs"]:
        L.append("  (none -- no corpus event shares this type/entities)")
    bg = c["background_reference"]
    L += ["", f"BACKGROUND: {bg['n_nearby']} nearby reference-tier events  [{bg['label'][:60]}]",
          "", "CAVEATS: " + " | ".join(c["caveats"])]
    return "\n".join(L)


def main():
    if len(sys.argv) < 2:
        print('usage: python3 src/triage.py "<headline or text>" | <url>'); return
    card = triage(" ".join(sys.argv[1:]))
    if "--json" in sys.argv:
        print(json.dumps(card, indent=2))
    else:
        print(_card_text(card))


if __name__ == "__main__":
    main()
