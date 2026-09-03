"""antecedent.py -- session H, defect L-2: the antecedent gate for hypothetical claims.

CLAIM_LEDGER_REGISTRATION.md §2 says a hypothetical claim "resolves only if the antecedent event
enters the corpus". No code ever tested that, so ledger.resolve() skipped modality=hypothetical
outright and twelve checkable claims sat in `pending` for ever, promising resolutions that were
never coming. This is the test, registered as Amendment 9 BEFORE it was written.

It is built to refuse. Four statuses, of which exactly one resolves anything:

    NO_ANTECEDENT          no registered conditional marker -- a hedge, not a conditional. §2's
                           mechanism does not reach it and never will. Closed, not pending.
    ANTECEDENT_UNTESTABLE  a marker, but no predicate can be derived, or the corpus lacks the field
                           needed to test it. REFUSED: nothing resolved, the reason published.
    ANTECEDENT_NOT_MET     predicate derived and tested; the antecedent did not occur. VOID -- and
                           excluded from every scoreboard, because a conditional is NOT refuted by
                           its antecedent failing (Amendment 9 §9.5).
    ANTECEDENT_MET         predicate satisfied. Only now does ledger.resolve() resolve the consequent.

Why so much refusal (Amendment 9 §9.4): `sr_actor` is coded on 65 of 187 geopolitical records, and
8 of the 30 entity ids the reader emits -- country.united_states, country.united_kingdom,
country.united_arab_emirates among them -- never appear in `event_entities` at all. Testing a corpus
predicate naively against that would publish "the antecedent did not occur" where the truth is "the
field is blank" or "that entity is invisible to the corpus". A refusal is the correct output of a
missing field, so the predicate is testable only where the window actually carries a coded actor.

Run:  python3 src/antecedent.py            # status for every hypothetical claim
      python3 src/antecedent.py --apply    # ... and append them to data/ledger/antecedents.jsonl
"""
import json
import re
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ledger as L                                                     # noqa: E402

DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "ledger" / "antecedents.jsonl"
REGISTRATION = "CLAIM_LEDGER_REGISTRATION.md Amendment 9"

# Amendment 9 §9.1. Registered before the code; widening this list is a new amendment.
MARKERS = re.compile(r"\b(if|should|unless|were to|in the event that|provided that|so long as|"
                     r"as long as|whenever)\b", re.I)
# A hedge is NOT an antecedent: it qualifies an unconditional proposition.
HEDGES = re.compile(r"\b(could|would|may|might|risks?|expects?|expected|threaten\w*|potentially|"
                    r"possibly)\b", re.I)
GEO_TYPES = ("conflict_escalation", "infrastructure_attack", "chokepoint_disruption")
CLAUSE_END = re.compile(r"[.;]|\band\b|\bbut\b", re.I)

NO_ANTECEDENT = "NO_ANTECEDENT"
CIRCULAR = "ANTECEDENT_CIRCULAR"
UNTESTABLE = "ANTECEDENT_UNTESTABLE"
NOT_MET = "ANTECEDENT_NOT_MET"
MET = "ANTECEDENT_MET"


def antecedent_clause(text):
    """(marker, clause) or (None, None). The clause runs from the marker to the next clause
    boundary or the end of the sentence, verbatim. Never paraphrased, never model-supplied."""
    m = MARKERS.search(text or "")
    if not m:
        return None, None
    rest = text[m.end():]
    end = CLAUSE_END.search(rest)
    return m.group(1).lower(), rest[:end.start()].strip() if end else rest.strip()


def _clause_entities(conn, clause):
    """Country entities named in the clause, by the corpus's own registered names. Deterministic:
    a name match against the `entities` table, never an inference about who 'it' refers to."""
    found = []
    for eid, name in conn.execute("SELECT entity_id, name FROM entities WHERE entity_id LIKE 'country.%'"):
        if re.search(rf"\b{re.escape(name)}\b", clause, re.I):
            found.append(eid)
    return sorted(set(found))


def _price_predicate(claim, clause):
    """The clause states a level -> the series must touch it, in the direction the clause states."""
    lvl = L.LEVEL.search(clause)
    if not lvl:
        return None
    down = bool(re.search(r"\b(as low as|below|down to|under)\b", clause, re.I)) or bool(L.DOWN.search(clause))
    return {"type": "PRICE", "level": float(lvl.group(1)), "direction": "down" if down else "up",
            "series": claim.get("series") or "fred.DCOILBRENTEU", "clause": clause}


def _corpus_predicate(conn, clause):
    ents = _clause_entities(conn, clause)
    if not ents:
        return None
    return {"type": "CORPUS", "actors": ents, "classes": list(GEO_TYPES), "clause": clause}


def _window(claim):
    k0 = pd.Timestamp(claim["knowable"])
    if claim.get("horizon_unit") == "calendar":
        return k0, k0 + timedelta(days=int(claim["horizon_days"]))
    return k0, None                      # trading-day windows are resolved on the series, not the calendar


def _test_price(conn, claim, pred):
    s = L._price(conn, pred["series"])
    pos = s.index.searchsorted(pd.Timestamp(claim["knowable"]))
    h = int(claim["horizon_days"])
    if pos + h >= len(s):
        return UNTESTABLE, {"reason": "the series does not yet cover the claim's horizon"}
    path = s.iloc[pos:pos + h + 1]
    hit = bool(path.min() <= pred["level"]) if pred["direction"] == "down" else bool(path.max() >= pred["level"])
    ev = {"level": pred["level"], "direction": pred["direction"],
          "path_min": round(float(path.min()), 2), "path_max": round(float(path.max()), 2),
          "resolved_on": str(path.index[-1].date())}
    return (MET if hit else NOT_MET), ev


def _test_corpus(conn, claim, pred):
    k0, k1 = _window(claim)
    if k1 is None:                       # a trading-day horizon on a corpus predicate: use calendar days
        k1 = k0 + timedelta(days=int(claim["horizon_days"]) * 7 // 5)
    args = [str(k0.date()), str(k1.date())]
    q_all = (f"SELECT COUNT(*) FROM events WHERE event_date > ? AND event_date <= ? "
             f"AND type IN ({','.join('?' * len(GEO_TYPES))})")
    n_window = conn.execute(q_all, args + list(GEO_TYPES)).fetchone()[0]
    n_coded = conn.execute(q_all + " AND sr_actor IS NOT NULL AND sr_actor != 'unknown'",
                           args + list(GEO_TYPES)).fetchone()[0]
    # Amendment 9 §9.4: an actor that never appears as a coded actor cannot be tested, only refused.
    known = []
    for e in pred["actors"]:
        seen = conn.execute("SELECT COUNT(*) FROM events WHERE sr_actor=?", (e,)).fetchone()[0]
        if seen:
            known.append(e)
    if not known:
        return UNTESTABLE, {"reason": "no actor named in the antecedent is ever a coded sr_actor in the corpus",
                            "actors_named": pred["actors"], "events_in_window": n_window}
    if not n_coded:
        return UNTESTABLE, {"reason": f"none of the {n_window} corpus events in the window carries a coded "
                                      f"sr_actor; 'not met' would be a missing-field artefact",
                            "actors_testable": known, "events_in_window": n_window}
    q = (f"SELECT COUNT(*) FROM events WHERE event_date > ? AND event_date <= ? "
         f"AND type IN ({','.join('?' * len(GEO_TYPES))}) AND sr_actor IN ({','.join('?' * len(known))})")
    n = conn.execute(q, args + list(GEO_TYPES) + known).fetchone()[0]
    ev = {"actors_testable": known, "actors_named": pred["actors"], "events_in_window": n_window,
          "events_with_a_coded_actor": n_coded, "matching_events": n,
          "window": [str(k0.date()), str(k1.date())]}
    return (MET if n else NOT_MET), ev


def _consequent_event_ids(conn, claim, k0, k1):
    """The event_ids ledger.resolve() would count for this claim's escalation consequent."""
    ents = tuple(e for e in (claim.get("entities") or []) if e.startswith("country."))
    q = ("SELECT DISTINCT e.event_id FROM events e JOIN event_entities ee ON ee.event_id=e.event_id "
         f"WHERE e.event_date > ? AND e.event_date <= ? AND e.type IN ({','.join('?' * len(GEO_TYPES))})")
    args = [str(k0.date()), str(k1.date())] + list(GEO_TYPES)
    if ents:
        q += f" AND ee.entity_id IN ({','.join('?' * len(ents))})"
        args += list(ents)
    return {r[0] for r in conn.execute(q, args)}


def _antecedent_event_ids(conn, actors, k0, k1):
    q = ("SELECT DISTINCT event_id FROM events WHERE event_date > ? AND event_date <= ? "
         f"AND type IN ({','.join('?' * len(GEO_TYPES))}) AND sr_actor IN ({','.join('?' * len(actors))})")
    return {r[0] for r in conn.execute(q, [str(k0.date()), str(k1.date())] + list(GEO_TYPES) + list(actors))}


def circularity(conn, claim, pred, ev):
    """Amendment 9.1. (is_circular, evidence). Containment is COMPUTED, never assumed."""
    if pred["type"] == "PRICE":
        same = (claim.get("kind") == "level"
                and (claim.get("series") or "fred.DCOILBRENTEU") == pred["series"]
                and claim.get("level") is not None and float(claim["level"]) == pred["level"]
                and claim.get("direction") == pred["direction"])
        return same, {"reason": "the antecedent predicate is the claim's own typed consequent "
                                "(same series, level and direction): resolving it would test the "
                                "antecedent and score it as the consequent",
                      "consequent": {"kind": claim.get("kind"), "series": claim.get("series"),
                                     "level": claim.get("level"), "direction": claim.get("direction")},
                      "antecedent": {k: pred[k] for k in ("series", "level", "direction")}} if same else {}
    if claim.get("kind") != "escalation":
        return False, {}
    k0, k1 = _window(claim)
    if k1 is None:
        k1 = k0 + timedelta(days=int(claim["horizon_days"]) * 7 // 5)
    a = _antecedent_event_ids(conn, ev.get("actors_testable") or [], k0, k1)
    c = _consequent_event_ids(conn, claim, k0, k1)
    sub = bool(a) and a <= c
    return sub, {"reason": "every corpus event satisfying the antecedent also satisfies the consequent "
                           "test resolve() would run, so ANTECEDENT_MET implies claim_true by "
                           "construction",
                 "n_antecedent": len(a), "n_consequent": len(c),
                 "antecedent_is_subset": sub} if sub else {"n_antecedent": len(a), "n_consequent": len(c),
                                                           "antecedent_is_subset": sub}


def status_for(conn, claim):
    """One claim -> its Amendment 9 status. Pure apart from reads."""
    base = {"claim_id": claim["claim_id"], "story_id": claim["story_id"], "kind": claim["kind"],
            "text": claim["text"], "registration": REGISTRATION}
    marker, clause = antecedent_clause(claim.get("text"))
    if not marker:
        return {**base, "status": NO_ANTECEDENT, "marker": None, "clause": None,
                "evidence": {"reason": "no registered conditional marker; the sentence is a hedge or a "
                                       "forecast, not a conditional, so §2's mechanism does not reach it",
                             "hedge_present": bool(HEDGES.search(claim.get("text") or ""))}}
    pred = _price_predicate(claim, clause) or _corpus_predicate(conn, clause)
    if pred is None:
        return {**base, "status": UNTESTABLE, "marker": marker, "clause": clause,
                "evidence": {"reason": "the antecedent clause states no price level and names no country "
                                       "entity (its subject is a pronoun, a mass noun or an unnamed situation)"}}
    st, ev = (_test_price if pred["type"] == "PRICE" else _test_corpus)(conn, claim, pred)
    row = {**base, "marker": marker, "clause": clause,
           "predicate": {k: v for k, v in pred.items() if k != "clause"}}
    if st == MET:                       # Amendment 9.1: a met antecedent is checked for circularity
        circ, cev = circularity(conn, claim, pred, ev)
        if circ:
            return {**row, "status": CIRCULAR, "evidence": {**ev, **cev}}
        ev = {**ev, **cev}
    return {**row, "status": st, "evidence": ev}


def hypotheticals(claims=None, resolutions=None):
    claims = claims if claims is not None else L._rows(L.CLAIMS)
    done = {r["claim_id"] for r in (resolutions if resolutions is not None else L._rows(L.RESOLUTIONS))}
    return [c for c in claims if c.get("checkable") and c.get("modality") == "hypothetical"
            and c["claim_id"] not in done]


def met_ids(path=None):
    """Claim ids recorded ANTECEDENT_MET. ledger.resolve() lifts its hypothetical skip for these
    and for no others."""
    p = Path(path or OUT)
    if not p.exists():
        return set()
    return {r["claim_id"] for r in (json.loads(l) for l in open(p, encoding="utf-8") if l.strip())
            if r.get("status") == MET}


def run(conn=None, apply=False, echo=print, out=None):
    own = conn is None
    conn = conn or sqlite3.connect(DB)
    rows = [status_for(conn, c) for c in hypotheticals()]
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    counts = Counter(r["status"] for r in rows)
    echo(f"antecedent gate ({REGISTRATION}) over {len(rows)} unresolved hypothetical claims:")
    for st in (MET, NOT_MET, CIRCULAR, UNTESTABLE, NO_ANTECEDENT):
        echo(f"  {st:24} {counts.get(st, 0)}")
    for r in rows:
        echo(f"  - {r['claim_id']} {r['status']:22} {(r.get('evidence') or {}).get('reason', '')[:70]}")
    if apply:
        p = Path(out or OUT)
        p.parent.mkdir(parents=True, exist_ok=True)
        seen = {(x["claim_id"], x["status"]) for x in (L._rows(p) if p.exists() else [])}
        with open(p, "a", encoding="utf-8") as f:
            for r in rows:
                if (r["claim_id"], r["status"]) in seen:
                    continue                                  # append-only and idempotent
                f.write(json.dumps({**r, "recorded_at": now}, ensure_ascii=False) + "\n")
        echo(f"  -> {p}")
    if own:
        conn.close()
    return rows


if __name__ == "__main__":
    run(apply="--apply" in sys.argv)
