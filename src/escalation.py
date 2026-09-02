"""
escalation.py -- B2: Layer G, the Escalation Model (spec §4.2; A2, A3).
(Named escalation.py, not situation.py, because src/situation.py already owns live-intake
attachment to situation_log; this module is the geopolitical retrieval/forecast layer.)

Structured-analogy retrieval on the geopolitical block of the Situation Record, a conditioned
reference class, and branch base rates -- history's own frequencies, never an invented
probability. Discipline:
  - similarity over the geopolitical block, UNIFORM weights (displayed, W below);
  - "NO ADEQUATE PRECEDENT" when max similarity < RETRIEVE_MIN (unit-tested);
  - branch rates from the conditioned subset only at n >= COND_MIN_N; else hierarchical
    fallback to the parent class (same event type) with a "thin conditioning" flag
    (unit-tested);
  - a likeness/difference table: field-by-field then-vs-now, each difference tagged with its
    evidence status ("judgment, unmeasured" until the walk-forward measures the shift, B5).
No lookahead: the caller (walk_forward) passes as_of; load_geo then excludes event_date >= t.
"""
from __future__ import annotations

from collections import Counter

from _db import connect

GEO_TYPES = ("conflict_escalation", "infrastructure_attack", "chokepoint_disruption", "sanctions")
BRANCHES = ("CONTAINED", "LIMITED_RETALIATION", "WIDENING", "RESOLUTION_BY_DEAL")
RETRIEVE_MIN = 0.40      # below this max-similarity -> NO ADEQUATE PRECEDENT
COND_SIM = 0.50          # a candidate joins the conditioned class at/above this similarity
COND_MIN_N = 8           # conditioned subset must reach this n, else fall back to parent
# uniform-prior weights over the geopolitical block (displayed on the card)
W = {"type": 1.0, "actor": 1.0, "target": 1.0, "conflict_scope": 1.0, "tempo": 1.0,
     "diplomatic": 1.0, "alliance": 1.0, "target_capacity": 1.0, "prior_dyad": 1.0,
     "propensity": 1.0}


def _rec(row, cols):
    d = dict(zip(cols, row))
    return {
        "event_id": d["event_id"], "date": d["event_date"], "type": d["type"],
        "title": d.get("title", ""), "actor": d.get("sr_actor"), "target": d.get("sr_target"),
        "conflict_scope": d.get("sr_conflict_scope"), "tempo": d.get("sr_tempo"),
        "diplomatic": d.get("sr_diplomatic"), "alliance": d.get("sr_alliance"),
        "target_capacity": d.get("sr_target_capacity"), "prior_dyad": d.get("sr_prior_dyad"),
        "propensity": d.get("sr_actor_propensity"), "outcome": d.get("sr_outcome_90"),
    }


def load_geo(conn, as_of=None):
    cols = [c[1] for c in conn.execute("PRAGMA table_info(events)")]
    q = f"SELECT * FROM events WHERE type IN ({','.join('?'*len(GEO_TYPES))})"
    args = list(GEO_TYPES)
    if as_of:
        q += " AND event_date < ?"; args.append(as_of)   # point-in-time (no lookahead)
    return [_rec(r, cols) for r in conn.execute(q, args)]


def _field_sim(f, a, b):
    if a is None or b is None or a == "unknown" or b == "unknown":
        return None                      # unknown -> field not counted
    if f == "propensity":
        try:
            return max(0.0, 1.0 - abs(float(a) - float(b)))
        except Exception:
            return None
    return 1.0 if a == b else 0.0


def similarity(t, c):
    num = den = 0.0
    per = {}
    for f, w in W.items():
        s = _field_sim(f, t.get(f), c.get(f))
        if s is None:
            continue
        per[f] = s; num += w * s; den += w
    return (num / den if den else 0.0), per


def branch_rates(recs):
    outs = [r["outcome"] for r in recs if r["outcome"] in BRANCHES]
    n = len(outs)
    ct = Counter(outs)
    rates = {b: round(ct.get(b, 0) / n, 3) if n else None for b in BRANCHES}
    return {"n": n, "rates": rates, "counts": dict(ct)}


def likeness_difference(t, a):
    likes, diffs = [], []
    for f in W:
        tv, av = t.get(f), a.get(f)
        if tv in (None, "unknown") or av in (None, "unknown"):
            continue
        row = {"field": f, "now": tv, "then": av}
        if tv == av:
            likes.append(row)
        else:
            diffs.append({**row, "shifts_branch": "unmeasured",
                          "evidence": "judgment, unmeasured (measured by walk-forward, B5)"})
    return {"likenesses": likes, "differences": diffs}


def read(conn, target, k=5, as_of=None, pool=None):
    """target: a geopolitical Situation Record (dict). Returns the Layer-G read.
    `pool` (list of recs) overrides the DB load — used by unit tests."""
    base = pool if pool is not None else load_geo(conn, as_of=as_of)
    pool = [r for r in base if r["event_id"] != target.get("event_id")]
    scored = []
    for c in pool:
        s, per = similarity(target, c)
        scored.append({"rec": c, "similarity": round(s, 3), "per_field": per})
    scored.sort(key=lambda x: -x["similarity"])
    if not scored or scored[0]["similarity"] < RETRIEVE_MIN:
        return {"no_adequate_precedent": True,
                "max_similarity": round(scored[0]["similarity"], 3) if scored else 0.0,
                "threshold": RETRIEVE_MIN, "analogs": []}
    cond_scored = [x for x in scored if x["similarity"] >= COND_SIM]
    conditioned = [x["rec"] for x in cond_scored]
    if len(conditioned) >= COND_MIN_N:
        br = branch_rates(conditioned); br["basis"] = "conditioned"; br["thin"] = False
    else:
        parent = [r for r in pool if r["type"] == target.get("type")]
        br = branch_rates(parent)
        br["basis"] = f"fallback: parent class ({target.get('type')})"
        br["thin"] = True
    topk = scored[:k]
    return {
        "no_adequate_precedent": False,
        "weights": "uniform prior over the geopolitical block",
        "analogs": [{"event_id": x["rec"]["event_id"], "date": x["rec"]["date"],
                     "title": x["rec"]["title"], "similarity": x["similarity"],
                     "outcome_90": x["rec"]["outcome"],
                     "ld": likeness_difference(target, x["rec"])} for x in topk],
        "branch_rates": br,
        "conditioned_n": len(conditioned),
        # the conditioned subset itself (every member at/above COND_SIM), so a caller -- the
        # Challenge loop -- can show its counts and join its price-side outcomes by event id
        "subset": [{"event_id": x["rec"]["event_id"], "date": x["rec"]["date"], "title": x["rec"]["title"],
                    "type": x["rec"]["type"], "similarity": x["similarity"], "outcome_90": x["rec"]["outcome"]}
                   for x in cond_scored],
        "subset_counts": branch_rates(conditioned),
    }


def read_event(conn, event_id, as_of=None):
    cols = [c[1] for c in conn.execute("PRAGMA table_info(events)")]
    row = conn.execute("SELECT * FROM events WHERE event_id=?", (event_id,)).fetchone()
    if not row:
        return {"error": f"unknown event {event_id}"}
    return read(conn, _rec(row, cols), as_of=as_of)


if __name__ == "__main__":
    import json
    import sys
    c = connect(read_only=True)
    eid = sys.argv[1] if len(sys.argv) > 1 else \
        c.execute("SELECT event_id FROM events WHERE type='chokepoint_disruption' "
                  "ORDER BY event_date DESC LIMIT 1").fetchone()[0]
    print(json.dumps(read_event(c, eid), indent=2)[:2600])
