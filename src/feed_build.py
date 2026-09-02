"""feed_build.py -- the Feed (NORTH_STAR §7.1) and the market-state strip.

FEED: the freshest day's watcher items that classify to an event class, each passed through
the market-defined materiality gate; MATERIAL items ranked by gate ratio, then by the gap
between what the headline claims and what the record says; everything else on the NOISE shelf,
visible and unranked. Nothing is dropped silently: counts are reported.

MARKET STATE: each asset against its own history -- latest value, percentile of the full
distribution, 20-day change, and the nearest historical state ("rhymes with"), found by
nearest neighbour on (percentile, 20d change, 20d vol percentile) over month-ends at least
six months old. Descriptive; never causal; every value carries its as-of.

Run:  python3 src/feed_build.py   -> data/feed.json, data/market_state.json
"""
import csv
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DB = DATA / "oil.db"
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ledger as L          # noqa: E402
import materiality as M     # noqa: E402
import reader as R          # noqa: E402  the caged reader (Amendment 3): headlines batched, cached, fallback labelled

ASSETS = [
    ("Brent", "fred.DCOILBRENTEU", "$/bbl"), ("WTI", "fred.DCOILWTICO", "$/bbl"),
    ("Diesel crack", "derived.diesel_crack", "$/bbl"), ("Gasoline crack", "derived.gasoline_crack", "$/bbl"),
    ("Henry Hub", "fred.DHHNGSP", "$/MMBtu"), ("TTF", "yf.ttf", "€/MWh"), ("JKM LNG", "yf.jkm", "$/MMBtu"),
    ("Propane", "fred.DPROPANEMBTX", "$/gal"),
]
SIG_ORDER = {"MATERIAL": 0, "IN_LINE": 1, "NOISE": 2}


def _series(conn, sid):
    return L._price(conn, sid)


def market_state(conn):
    out = []
    for label, sid, unit in ASSETS:
        s = _series(conn, sid)
        if len(s) < 300:
            continue
        v = float(s.iloc[-1])
        pct = float((s < v).mean() * 100)
        chg20 = float((s.iloc[-1] / s.iloc[-21] - 1) * 100) if s.iloc[-21] else None
        lr = np.log(s[s > 0]).diff().dropna()
        vol20 = lr.rolling(20).std() * np.sqrt(252) * 100
        volpct = float((vol20 < vol20.iloc[-1]).mean() * 100) if len(vol20.dropna()) else None
        # nearest historical state over month-ends, >= 6 months old
        m = s.resample("ME").last().dropna()
        cand = []
        for d, val in m.items():
            if (s.index[-1] - d).days < 180:
                continue
            hist = s.loc[:d]
            if len(hist) < 260:
                continue
            p = float((hist < val).mean() * 100)
            c20 = float((hist.iloc[-1] / hist.iloc[-21] - 1) * 100) if len(hist) > 21 and hist.iloc[-21] else 0.0
            vp = float((vol20.loc[:d].dropna() < vol20.loc[:d].dropna().iloc[-1]).mean() * 100) if len(vol20.loc[:d].dropna()) > 20 else 50.0
            dist = ((p - pct) / 25) ** 2 + ((c20 - (chg20 or 0)) / 10) ** 2 + ((vp - (volpct or 50)) / 25) ** 2
            cand.append((dist, str(d.date())[:7], round(p), round(c20, 1)))
        cand.sort()
        out.append({"asset": label, "series": sid, "unit": unit, "value": round(v, 2), "as_of": str(s.index[-1].date()),
                    "pct_of_history": round(pct), "chg20_pct": round(chg20, 1) if chg20 is not None else None,
                    "vol20_pct": round(volpct) if volpct is not None else None,
                    "rhymes": [{"month": c[1], "pct": c[2], "chg20": c[3]} for c in cand[:3]],
                    "history_from": str(s.index[0].date())})
    return {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "assets": out,
            "note": "percentile of the asset's own full history; 'rhymes' = nearest month-end state on (level pct, 20d change, vol pct), descriptive only"}


def _headline_gap(conn, t):
    """If the headline itself makes a checkable claim (typed by the reader), the gap between it and the record."""
    if not t or t["kind"] not in ("direction", "level", "flow", "escalation") or not t["checkable"]:
        return None, None
    try:
        v = L.verdict_for(conn, t)
    except Exception:
        return None, None
    if v.get("r") is None:
        return None, v.get("verdict")
    return round(1 - v["r"], 2), v.get("verdict")


def build_feed(conn, limit=60):
    p = DATA / "alert_queue.csv"
    if not p.exists():
        return {"day": None, "material": [], "in_line": [], "noise": [], "counts": {}, "note": "no watcher queue yet"}
    rows = list(csv.DictReader(open(p, newline="", encoding="utf-8")))
    days = sorted({(r.get("timestamp_utc") or "")[:10] for r in rows if r.get("timestamp_utc")})
    day = days[-1] if days else None
    todays = [r for r in rows if (r.get("timestamp_utc") or "")[:10] == day]
    todays.reverse()
    material, in_line, noise = [], [], []
    n_gdelt = 0
    seen = set()
    items = []
    for r in todays:
        head = (r.get("headline") or "").strip()
        if not head or head in seen:
            continue
        seen.add(head)
        if head.startswith("[GDELT]"):
            n_gdelt += 1
            continue
        items.append((head, r))
    reads = R.read_headlines([h for h, _ in items], conn=conn)          # one caged read per headline
    modes = {}
    for (head, r), rd in zip(items, reads):
        etype = rd["event_class"]
        ents = [e["id"] for e in rd["entities"]]
        g = M.gate(etype)
        att = M.attention(ents)
        flags = M.flags_for(g["significance"], att.get("score"))
        gap, hv = _headline_gap(conn, rd["claims"][0] if rd["claims"] else None) if etype else (None, None)
        sig = g["significance"]
        gflags = list(g.get("flags") or [])
        if sig == "MATERIAL" and not rd["qualifying_entities"]:
            sig = "IN_LINE"; gflags.append("no_entity")          # Amendment 3 rule 5: a tracked petro entity in a gate role
        mode = rd["reader"]["mode"]
        modes[mode] = modes.get(mode, 0) + 1
        item = {"headline": head[:200], "url": r.get("url"), "source": r.get("source"), "when": (r.get("timestamp_utc") or "")[:16],
                "event_class": etype, "entities": ents, "roles": [{"id": e["id"], "role": e["role"]} for e in rd["entities"]],
                "qualifying_entities": rd["qualifying_entities"], "reader": mode,
                "significance": sig, "why": g.get("why"),
                "ratio": g.get("ratio"), "rates": g.get("rates"), "gate_flags": gflags, "attention": att.get("score"),
                "flags": flags, "headline_gap": gap, "headline_verdict": hv}
        {"MATERIAL": material, "IN_LINE": in_line, "NOISE": noise}[sig].append(item)
    material.sort(key=lambda i: (-(i["ratio"] or 0), -len(i["qualifying_entities"]), -(i["headline_gap"] or 0), i["when"]))
    return {"day": day, "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "material": material[:limit], "in_line": in_line[:limit], "noise": noise[:limit],
            "counts": {"day_total": len(todays), "gdelt_hidden": n_gdelt, "material": len(material), "in_line": len(in_line),
                       "noise": len(noise), "reader": modes},
            "gate": "CLAIM_LEDGER_REGISTRATION.md §1 (+ Amendments 1-3)",
            "note": "ranked by gate ratio, then qualifying entities, then headline-vs-record gap; headlines read by the caged reader (regex_fallback labelled)"}


def run():
    conn = sqlite3.connect(DB)
    ms = market_state(conn)
    fd = build_feed(conn)
    json.dump(ms, open(DATA / "market_state.json", "w"), indent=1)
    json.dump(fd, open(DATA / "feed.json", "w"), indent=1)
    conn.close()
    print(f"market_state: {len(ms['assets'])} assets; feed {fd['day']}: {fd['counts']}")
    return ms, fd


if __name__ == "__main__":
    ms, fd = run()
    for a in ms["assets"]:
        print(f"  {a['asset']:<15} {a['value']:>8} {a['unit']:<8} pct {a['pct_of_history']:>3} chg20 {a['chg20_pct']:>6} vol {a['vol20_pct']:>3} rhymes {[r['month'] for r in a['rhymes']]}")
    for i in fd["material"][:8]:
        print(f"  MATERIAL {i['ratio']} {i['event_class']:<22} gap={i['headline_gap']} {i['flags']} :: {i['headline'][:70]}")
