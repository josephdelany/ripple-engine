"""
situation_record.py -- B1: code a Situation Record for every corpus event, per
SITUATION_CODEBOOK_V2.md. DETERMINISTIC and sourced-or-unknown: fields are derived only
from data already in oil.db (event_entities coded from each event's source; the corpus's
own dated, sourced events; situation_log) or left "unknown". Nothing is invented, nothing
is inferred from prices/outcomes-by-hindsight. Low-confidence codings go to the borderline
queue for the human gate (B1 Joe-gate).

Outcome branches (+30/+90d) are OBSERVED from the corpus record itself: what sourced events
actually followed in the same actor/target dyad within the window. The method is a documented
coding rule, not a guess; ambiguous cases are flagged low-confidence for review.

Run:  python3 src/situation_record.py            # code all, write back, emit gate artifacts
"""
from __future__ import annotations

import csv
import datetime as dt
import json
from collections import defaultdict

from _db import connect, DB
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEO_TYPES = {"conflict_escalation", "infrastructure_attack", "chokepoint_disruption", "sanctions"}
DEAL_KW = ("ceasefire", "cease-fire", "truce", "agreement", "deal", "accord", "talks",
           "resume", "reopen", "restored", "mou", "peace")
SR_COLS = [
    ("sr_actor", "TEXT"), ("sr_target", "TEXT"), ("sr_asset_role", "TEXT"),
    ("sr_conflict_scope", "TEXT"), ("sr_tempo", "TEXT"), ("sr_alliance", "TEXT"),
    ("sr_diplomatic", "TEXT"), ("sr_target_capacity", "TEXT"),
    ("sr_outcome_30", "TEXT"), ("sr_outcome_90", "TEXT"),
    ("sr_actor_propensity", "REAL"), ("sr_prior_dyad", "TEXT"),
    ("sr_confidence", "REAL"), ("sr_json", "TEXT"),
]


def _migrate(conn):
    have = {r[1] for r in conn.execute("PRAGMA table_info(events)")}
    for name, typ in SR_COLS:
        if name not in have:
            conn.execute(f"ALTER TABLE events ADD COLUMN {name} {typ}")
    conn.commit()


def _load(conn):
    cols = [c[1] for c in conn.execute("PRAGMA table_info(events)")]
    events = [dict(zip(cols, r)) for r in conn.execute("SELECT * FROM events ORDER BY event_date")]
    ent = defaultdict(lambda: defaultdict(set))   # event_id -> role -> {entity_id}
    for eid, en, role in conn.execute("SELECT event_id, entity_id, role FROM event_entities"):
        ent[eid][role].add(en)
    return events, ent


def _parties(ent_e):
    actors = ent_e.get("actor", set())
    targets = ent_e.get("target", set()) or ent_e.get("location", set())
    return actors, targets


def _days(a, b):
    try:
        return (dt.date.fromisoformat(b[:10]) - dt.date.fromisoformat(a[:10])).days
    except Exception:
        return 10**9


def _observe_outcome(e, events, ent, horizon):
    """Observe the branch from the corpus: sourced events that followed in the same dyad
    within `horizon` days. Returns (branch, confidence, evidence_ids)."""
    if e["type"] not in GEO_TYPES:
        return "unknown", 0.0, []
    A, T = _parties(ent[e["event_id"]])
    dyad = A | T
    if not dyad:
        return "unknown", 0.0, []
    d0 = e["event_date"]
    subs = []
    for o in events:
        if o["event_id"] == e["event_id"]:
            continue
        gap = _days(d0, o["event_date"])
        if 0 < gap <= horizon:
            oe = ent[o["event_id"]]
            oent = set().union(*oe.values()) if oe else set()
            if oent & dyad:
                subs.append((o, gap, oent))
    conflict_subs = [(o, g, oe) for (o, g, oe) in subs if o["type"] in GEO_TYPES]
    # third-party countries drawn in by the FOLLOW-ON conflict events (not the original dyad)
    new_actors = {x for (_, _, oe) in conflict_subs for x in oe
                  if x.startswith("country.")} - dyad
    deal = any(any(k in (o["title"] or "").lower() for k in DEAL_KW) for (o, _, _) in subs)
    if deal:
        return "RESOLUTION_BY_DEAL", 0.7, [o["event_id"] for (o, _, _) in subs][:6]
    if (new_actors and conflict_subs) or len(conflict_subs) >= 3:
        return "WIDENING", 0.7, [o["event_id"] for (o, _, _) in conflict_subs][:6]
    if len(conflict_subs) >= 1:
        return "LIMITED_RETALIATION", 0.6, [o["event_id"] for (o, _, _) in conflict_subs]
    return "CONTAINED", 0.55, []


def _conflict_scope(e, events, ent):
    """isolated / campaign / war from the density of same-dyad conflict events in +-120d."""
    if e["type"] not in GEO_TYPES:
        return "unknown", 0.0
    A, T = _parties(ent[e["event_id"]]); dyad = A | T
    if not dyad:
        return "unknown", 0.0
    near = 0
    for o in events:
        if o["event_id"] == e["event_id"] or o["type"] not in GEO_TYPES:
            continue
        if abs(_days(e["event_date"], o["event_date"])) <= 120:
            oe = ent[o["event_id"]]
            if (set().union(*oe.values()) if oe else set()) & dyad:
                near += 1
    scope = "isolated" if near <= 1 else ("campaign" if near <= 5 else "war")
    return scope, 0.5


def _asset_role(e, ent):
    ents = set().union(*ent[e["event_id"]].values()) if ent[e["event_id"]] else set()
    if any(x.startswith("chokepoint.") for x in ents):
        return "chokepoint", 0.7
    if e["type"] == "chokepoint_disruption":
        return "chokepoint", 0.6
    return "unknown", 0.0


def code_all():
    conn = connect(DB)   # writable pipeline connection
    _migrate(conn)
    events, ent = _load(conn)
    by_date = sorted(events, key=lambda x: x["event_date"])

    # pass 1: per-event fields + outcomes
    coded = {}
    for e in by_date:
        A, T = _parties(ent[e["event_id"]])
        actor = sorted(A)[0] if A else "unknown"
        target = sorted(T)[0] if T else "unknown"
        role, role_c = _asset_role(e, ent)
        scope, scope_c = _conflict_scope(e, events, ent)
        # tempo: prior event in same dyad before this date?
        prior = None
        for o in reversed([x for x in by_date if x["event_date"] < e["event_date"]]):
            oe = ent[o["event_id"]]
            if o["type"] in GEO_TYPES and (set().union(*oe.values()) if oe else set()) & (A | T):
                prior = o; break
        tempo = "unknown" if e["type"] not in GEO_TYPES else ("nth" if prior else "first")
        o30, c30, _ = _observe_outcome(e, events, ent, 30)
        o90, c90, ev90 = _observe_outcome(e, events, ent, 90)
        src = {
            "actor": e.get("source_url") if actor != "unknown" else None,
            "target": e.get("source_url") if target != "unknown" else None,
            "asset_role": "corpus:entities" if role != "unknown" else None,
            "conflict_scope": "corpus:density" if scope != "unknown" else None,
            "tempo": "corpus:dyad" if tempo != "unknown" else None,
            "outcome_30": "corpus:observed" if o30 != "unknown" else None,
            "outcome_90": "corpus:observed(" + ",".join(ev90) + ")" if o90 != "unknown" else None,
            "alliance": None, "diplomatic": None, "target_capacity": None,  # need source read -> unknown
        }
        # record-level confidence: mean of coded-field confidences, penalized for unknowns
        key_conf = [role_c, scope_c, (0.6 if tempo != "unknown" else 0.0), c90]
        conf = round(sum(key_conf) / len(key_conf), 3)
        coded[e["event_id"]] = dict(actor=actor, target=target, asset_role=role,
                                    conflict_scope=scope, tempo=tempo, alliance="unknown",
                                    diplomatic="unknown", target_capacity="unknown",
                                    outcome_30=o30, outcome_90=o90, prior=prior["event_id"] if prior else "none",
                                    conf=conf, src=src, prior_ev=prior)

    # pass 2: actor response propensity (share of an actor's geo events that escalated)
    esc = {"LIMITED_RETALIATION", "WIDENING"}
    actor_events = defaultdict(list)
    for e in by_date:
        c = coded[e["event_id"]]
        if e["type"] in GEO_TYPES and c["actor"] != "unknown" and c["outcome_90"] != "unknown":
            actor_events[c["actor"]].append(c["outcome_90"])
    propensity = {a: round(sum(1 for o in outs if o in esc) / len(outs), 3)
                  for a, outs in actor_events.items()}

    # pass 3: prior_outcome_in_dyad + write back
    borderline = []
    for e in by_date:
        c = coded[e["event_id"]]
        prior_outcome = coded[c["prior_ev"]["event_id"]]["outcome_90"] if c["prior_ev"] else "none"
        prop = propensity.get(c["actor"])
        rec = {"physical": {"asset_role": c["asset_role"]},
               "geopolitical": {"actor": c["actor"], "target": c["target"],
                                "conflict_scope": c["conflict_scope"], "tempo": c["tempo"],
                                "alliance_engagement": c["alliance"], "diplomatic_state": c["diplomatic"],
                                "target_response_capacity": c["target_capacity"],
                                "actor_response_propensity": prop, "prior_outcome_in_dyad": prior_outcome},
               "outcome": {"branch_30d": c["outcome_30"], "branch_90d": c["outcome_90"]},
               "sources": c["src"], "confidence": c["conf"],
               "method": "deterministic v2 (sourced-or-unknown); outcomes observed from corpus"}
        conn.execute(
            "UPDATE events SET sr_actor=?,sr_target=?,sr_asset_role=?,sr_conflict_scope=?,sr_tempo=?,"
            "sr_alliance=?,sr_diplomatic=?,sr_target_capacity=?,sr_outcome_30=?,sr_outcome_90=?,"
            "sr_actor_propensity=?,sr_prior_dyad=?,sr_confidence=?,sr_json=? WHERE event_id=?",
            (c["actor"], c["target"], c["asset_role"], c["conflict_scope"], c["tempo"], c["alliance"],
             c["diplomatic"], c["target_capacity"], c["outcome_30"], c["outcome_90"], prop,
             prior_outcome, c["conf"], json.dumps(rec), e["event_id"]))
        if c["conf"] < 0.45 or c["outcome_90"] == "unknown":
            borderline.append((e["event_id"], e["event_date"], e["type"], c["conf"],
                               c["outcome_90"], e.get("title", "")[:70]))
    conn.commit()

    # artifacts
    (ROOT / "data").mkdir(exist_ok=True)
    with open(ROOT / "data" / "borderline_codings.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["event_id", "date", "type", "confidence", "outcome_90", "title"])
        w.writerows(sorted(borderline, key=lambda r: r[3]))
    n = len(by_date)
    geo = [e for e in by_date if e["type"] in GEO_TYPES]
    branch_dist = defaultdict(int)
    for e in geo:
        branch_dist[coded[e["event_id"]]["outcome_90"]] += 1
    summary = {"n_events": n, "n_geo": len(geo), "n_borderline": len(borderline),
               "branch_dist_90d_geo": dict(branch_dist),
               "actors_with_propensity": len(propensity),
               "pct_geo_outcome_coded": round(100 * sum(1 for e in geo
                   if coded[e["event_id"]]["outcome_90"] != "unknown") / max(len(geo), 1), 1)}
    (ROOT / "data" / "situation_records_summary.json").write_text(json.dumps(summary, indent=2))
    conn.close()
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    code_all()
