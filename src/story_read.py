"""story_read.py -- the Story Page object (NORTH_STAR §2): one development read as a desk reads it.

Order is the desk's order and nothing else is on the page:
  0 significance   -- MATERIAL / IN LINE / NOISE from the market-defined gate (materiality.py)
  1 is it priced?  -- price since knowable vs the analog fan (median, IQR, dated tails); flow side
  2 is it right?   -- the story's claims verbatim, typed and given a measured verdict (ledger.py)
  3 the tail       -- escalation branches from Layer G (escalation.py), then-vs-now table
  4 where it goes  -- propagation hops per class (propagate.py), price and flow separately
  5 trust          -- walk-forward stamp (as computed, labelled), retrieval quality, freshness, sources

Inputs: a pasted headline/paragraph/URL (live) or a corpus event_id (historical, point-in-time).
Every number carries its n and the file/module it came from. Nothing is generated prose.
"""
import json
import sqlite3
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DB = DATA / "oil.db"
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import deconstruct as DC          # noqa: E402
import escalation as ES           # noqa: E402
import ledger as L                # noqa: E402
import materiality as M           # noqa: E402
import propagate as P             # noqa: E402

BRENT = "fred.DCOILBRENTEU"
HORIZON = 20
GEO = set(ES.GEO_TYPES)


def _price(conn, sid=BRENT):
    return L._price(conn, sid)


def _domain(url):
    try:
        return urlparse(url).netloc.replace("www.", "") if url else None
    except Exception:
        return None


def _load(name):
    try:
        return json.load(open(DATA / name))
    except Exception:
        return {}


# ----------------------------------------------------------------------------- 1. priced?

def priced(conn, etype, knowable, exclude_event=None):
    """Brent since knowable (simple % from the first trading day on/after) beside the analog fan:
    every class event's +0..+20 trading-day % path -> median, IQR, min/max per day, dated tails."""
    s = _price(conn)
    k = pd.Timestamp(knowable)
    pos = s.index.searchsorted(k)
    out = {"series": BRENT, "knowable": str(k.date()), "horizon_td": HORIZON}
    if pos >= len(s):
        pos = len(s) - 1                              # live story after the last print: price as of the last observation
        out["price_note"] = f"price series ends {s.index[-1].date()}; path starts at the next refresh"
    if pos < len(s):
        p0 = float(s.iloc[pos])
        path = s.iloc[pos:pos + HORIZON + 1]
        out["price_at_knowable"] = round(p0, 2)
        out["price_now"] = round(float(s.iloc[-1]), 2)
        out["as_of"] = str(s.index[-1].date())
        out["path_pct"] = [round(float(v / p0 - 1) * 100, 2) for v in path]
        out["days_elapsed"] = len(path) - 1
        out["complete"] = len(path) == HORIZON + 1
    else:
        out.update(price_at_knowable=None, path_pct=[], days_elapsed=0, complete=False)
    paths, tails = [], []
    for eid, d, title in conn.execute("SELECT event_id, event_date, title FROM events WHERE type=?", (etype,)):
        if eid == exclude_event:
            continue
        p = s.index.searchsorted(pd.Timestamp(d))
        if p >= len(s) or p + HORIZON >= len(s) or pd.Timestamp(d) >= k:
            continue                                  # point-in-time: only analogs knowable before k
        q0 = float(s.iloc[p]); arr = (s.iloc[p:p + HORIZON + 1].to_numpy() / q0 - 1) * 100
        paths.append(arr); tails.append((eid, d, title, float(arr[-1])))
    if paths:
        A = np.vstack(paths)
        out["fan"] = {"n": len(paths), "median": np.round(np.median(A, 0), 2).tolist(),
                      "p25": np.round(np.percentile(A, 25, 0), 2).tolist(),
                      "p75": np.round(np.percentile(A, 75, 0), 2).tolist(),
                      "min": np.round(A.min(0), 2).tolist(), "max": np.round(A.max(0), 2).tolist()}
        tails.sort(key=lambda t: t[3])
        out["tails"] = {"low": {"event_id": tails[0][0], "date": tails[0][1], "title": tails[0][2], "chg_pct": round(tails[0][3], 1)},
                        "high": {"event_id": tails[-1][0], "date": tails[-1][1], "title": tails[-1][2], "chg_pct": round(tails[-1][3], 1)}}
        if out.get("path_pct"):
            d = out["days_elapsed"]
            med = out["fan"]["median"][d]
            out["now_vs_median_pct"] = round(out["path_pct"][-1] - med, 2)
            up_share = float((A[:, d] > 0).mean())
            out["share_up_at_day"] = round(up_share, 2)
    else:
        out["fan"] = None
    return out


def flow_side(conn, etype):
    pw = _load("portwatch.json")
    prop = P.propagate(conn, event_type=etype) if etype else {}
    return {"chokepoints": [{"chokepoint": c.get("chokepoint"), "flag": c.get("flag"), "pct_of_median": c.get("pct_of_median"),
                             "latest_date": c.get("latest_date")} for c in (pw.get("chokepoints") or [])],
            "flow_now_pct_vs_base": prop.get("flow_now"),
            "realized_disruption_fraction_pct": prop.get("realized_disruption_fraction_pct"),
            "contributing_n": prop.get("contributing_n"),
            "reading": prop.get("reading"), "caveat": prop.get("caveat")}


# ----------------------------------------------------------------------------- 3. branches

def branches(conn, etype, event_id=None, entities=None, as_of=None):
    if etype not in GEO:
        return {"applicable": False, "note": f"'{etype}' is not a geopolitical class; escalation branches do not apply."}
    if event_id:
        r = ES.read_event(conn, event_id, as_of=as_of)
        basis_note = "conditioned on the event's coded situation record (point-in-time)"
    else:
        target = {"event_id": None, "type": etype, "actor": "unknown", "target": "unknown", "conflict_scope": "unknown",
                  "tempo": "unknown", "diplomatic": "unknown", "alliance": "unknown", "target_capacity": "unknown",
                  "prior_dyad": "unknown", "propensity": None}
        # a live story carries no coded situation fields yet -> class-only conditioning, said so
        for e in entities or []:
            if e.startswith("country.") and target["target"] == "unknown":
                target["target"] = e
        r = ES.read(conn, target, as_of=as_of)
        basis_note = "live story: situation fields not yet coded -> conditioned on class" + (" + target" if target["target"] != "unknown" else "") + " only"
    r["basis_note"] = basis_note
    r["outcome_label"] = "outcomes at +90d are corpus-derived (subsequent corpus events), not source-audited"
    r["applicable"] = True
    return r


# ----------------------------------------------------------------------------- 5. trust

def trust(conn, etype, br):
    wf = _load("walk_forward/summary.json")
    st = _load("engine_status.json")
    rows = []
    for w, d in (wf.get("windows") or {}).items():
        rows.append({"window": w, "test": d.get("test_window"), "n": d.get("n_scored"),
                     "G_brier": d.get("G_brier_conditioned"), "G_base": d.get("G_brier_baseline"), "G_skill": d.get("G_skill"),
                     "P_skill": d.get("P_skill")})
    return {"walk_forward": {"rows": rows, "verdict": wf.get("verdict"), "protocol": wf.get("protocol"),
                             "label": "as computed by src/walk_forward.py; outcome labels corpus-derived, not source-audited"},
            "retrieval": {"conditioned_n": (br or {}).get("conditioned_n"), "basis": ((br or {}).get("branch_rates") or {}).get("basis"),
                          "no_adequate_precedent": (br or {}).get("no_adequate_precedent")},
            "freshness": {"status": st.get("status") or st.get("light"), "as_of": st.get("as_of") or st.get("generated_at")}}


# ----------------------------------------------------------------------------- the read

def read(arg=None, event_id=None, knowable=None, log=True):
    conn = sqlite3.connect(DB)
    try:
        if event_id:
            row = conn.execute("SELECT event_id, event_date, type, title, description, source_url FROM events WHERE event_id=?",
                               (event_id,)).fetchone()
            if not row:
                return {"error": f"unknown event {event_id}"}
            eid, edate, etype, title, desc, url = row
            text = f"{title}. {desc or ''}"
            ents = [r[0] for r in conn.execute("SELECT entity_id FROM event_entities WHERE event_id=?", (eid,))]
            knowable = edate
            cs = DC.claims(conn, text)
            source = _domain(url); was_url = False; scope = None; article_type = "corpus event"
            story_id = f"event:{eid}"
        else:
            d = DC.deconstruct(arg)
            if d.get("scope") in ("off_topic",):
                etype = None
            else:
                etype = d.get("dominant_class")
            cs = d.get("claims") or []
            ents = sorted({e for c in cs for e in c.get("entities", [])})
            url = d.get("url"); title = (arg or "")[:160]; desc = None
            source = _domain(url) or "pasted"; was_url = d.get("was_url"); scope = d.get("scope"); article_type = d.get("article_type")
            knowable = knowable or date.today().isoformat()
            story_id = "live:" + L._cid(source or "pasted", (arg or "")[:400])
            eid = None
        k = pd.Timestamp(knowable)
        gate = M.gate(etype)
        att = M.attention(ents)
        flags = M.flags_for(gate["significance"], att.get("score"))
        pr = priced(conn, etype, k, exclude_event=eid) if etype else {"fan": None, "knowable": str(k.date())}
        br = branches(conn, etype, event_id=eid, entities=ents, as_of=str(k.date()) if eid else None) if etype else {"applicable": False, "note": "no event class"}
        p0 = pr.get("price_at_knowable")
        claims = []
        for c in cs:
          for clause in L.split_clauses(c["text"]):
            t = L.type_claim(clause, c.get("event_class") or etype, c.get("entities"), c.get("modality", "asserted"))
            t["sentence"] = c["text"]
            v = L.verdict_for(conn, t, price_at_knowable=p0, as_of=str(k.date()) if eid else None,
                              escalation_read=br if br.get("applicable") else None)
            t["verdict"] = v
            claims.append(t)
        prop = P.propagate(conn, event_type=etype) if etype else {}
        story = {
            "story_id": story_id, "event_id": eid, "title": title, "description": desc, "url": url, "source": source,
            "article_type": article_type, "scope": scope, "was_url": was_url,
            "knowable": str(k.date()), "read_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "event_class": etype, "entities": ents,
            "significance": {**gate, "attention": att, "flags": flags},
            "priced": pr,
            "flow": flow_side(conn, etype) if etype else {},
            "claims": claims,
            "n_checkable": sum(1 for c in claims if c["checkable"]),
            "branches": br,
            "propagation": {"hops": prop.get("hops"), "contributing_n": prop.get("contributing_n"),
                            "realized_disruption_fraction_pct": prop.get("realized_disruption_fraction_pct"),
                            "caveat": prop.get("caveat")} if prop else {},
            "trust": trust(conn, etype, br),
            "sources_board": [b for b in L.scoreboards(conn)["sources"] if b["source"] == source],
            "registrations": ["CLAIM_LEDGER_REGISTRATION.md", "BIG_MOVES_REGISTRATION.md", "PRE_REGISTRATION_V2.md"],
        }
        if log and not eid:
            story["ledger_ids"] = L.log_claims(story_id, source, k.date(), claims, price_at_knowable=p0, url=url)
        return story
    finally:
        conn.close()


def _print(s):
    sig = s["significance"]
    print(f"\n{s['title'][:90]}\n  class={s['event_class']} knowable={s['knowable']} source={s['source']}")
    print(f"  SIGNIFICANCE {sig['significance']} {sig.get('flags')} -- {sig.get('why')}")
    pr = s["priced"]
    if pr.get("fan"):
        print(f"  PRICED: Brent {pr['price_at_knowable']} at knowable; +{pr['days_elapsed']}d path {pr['path_pct'][-1]:+.1f}% "
              f"vs analog median {pr['fan']['median'][pr['days_elapsed']]:+.1f}% (n={pr['fan']['n']}); tails "
              f"{pr['tails']['low']['chg_pct']}% ({pr['tails']['low']['date'][:4]}) .. {pr['tails']['high']['chg_pct']}% ({pr['tails']['high']['date'][:4]})")
    fl = s["flow"]
    print(f"  FLOW: realized disruption {fl.get('realized_disruption_fraction_pct')}% of {fl.get('contributing_n')}; now {fl.get('flow_now_pct_vs_base')}")
    for c in s["claims"]:
        v = c["verdict"]
        print(f"  CLAIM [{c['kind']:11s}] {v['verdict']:12s} r={v.get('r')} n={v.get('n')} :: {c['text'][:80]}")
    b = s["branches"]
    if b.get("applicable"):
        br = b.get("branch_rates") or {}
        print(f"  BRANCHES ({br.get('basis')}, n={br.get('n')}): {br.get('counts')} -- {b.get('basis_note')}")
        for a in (b.get("analogs") or [])[:3]:
            print(f"    analog {a['date']} sim={a['similarity']} {a['outcome_90']} :: {a['title'][:60]}")
    for h in (s["propagation"].get("hops") or [])[:5]:
        print(f"  HOP {h['label']:<22} signed_med {h['signed_median_pct']:>6}% n={h['n']} material {h['material_move_pct']}%")
    print(f"  TRUST: {s['trust']['walk_forward']['verdict']}")


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "abqaiq_attack_2019"
    s = read(event_id=a) if not a.strip().startswith(("http", " ")) and " " not in a.strip() else read(arg=a, log=False)
    _print(s)
