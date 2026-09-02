"""
load_deep_history.py -- B6: load the deep-history tier (1970-1989) into the events table
for Layer G only (events-only; no price layer pre-1987). Each event is inserted with its
situation-record fields set from the curated, source-anchored record; entity rows are
ensured; the tier is flagged in sr_json ("tier":"deep_history_no_price"). Idempotent
(INSERT OR IGNORE). These enlarge Layer-G training pools; the walk-forward test windows
(2015+/2020+) are unchanged, so this only adds precedent, never leaks.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from _db import connect, DB

ROOT = Path(__file__).resolve().parent.parent
SEED = ROOT / "data" / "deep_history_1970_1989.json"


def _ensure_entity(conn, eid):
    if not eid or "." not in eid:
        return
    kind, slug = eid.split(".", 1)
    typ = {"country": "country", "chokepoint": "chokepoint"}.get(kind, "other")
    name = slug.replace("_", " ").title()
    conn.execute("INSERT OR IGNORE INTO entities(entity_id, type, name, notes) VALUES (?,?,?,?)",
                 (eid, typ, name, "added by deep-history loader (B6)"))


def run():
    seed = json.loads(SEED.read_text())["events"]
    conn = connect(DB)
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    n_new = 0
    for e in seed:
        exists = conn.execute("SELECT 1 FROM events WHERE event_id=?", (e["event_id"],)).fetchone()
        conn.execute(
            "INSERT OR IGNORE INTO events(event_id,event_date,date_precision,type,title,"
            "description,confidence,source_url,added_at) VALUES (?,?,?,?,?,?,?,?,?)",
            (e["event_id"], e["event_date"], "day", e["type"], e["title"],
             e["title"] + " [deep-history tier 1970-1989; events-only]", "medium",
             e["source_url"], now))
        for role, ent in (("actor", e.get("actor")), ("target", e.get("target"))):
            if ent:
                _ensure_entity(conn, ent)
                conn.execute("INSERT OR IGNORE INTO event_entities(event_id,entity_id,role) "
                             "VALUES (?,?,?)", (e["event_id"], ent, role))
        rec = {"physical": {"asset_role": "unknown"},
               "geopolitical": {"actor": e.get("actor"), "target": e.get("target"),
                                "conflict_scope": "unknown", "tempo": "unknown",
                                "alliance_engagement": "unknown", "diplomatic_state": "unknown",
                                "target_response_capacity": "unknown",
                                "actor_response_propensity": None, "prior_outcome_in_dyad": "unknown"},
               "outcome": {"branch_30d": e["outcome_90"], "branch_90d": e["outcome_90"]},
               "sources": {"outcome_90": e["source_url"], "actor": e["source_url"],
                           "target": e["source_url"]},
               "tier": "deep_history_no_price", "confidence": 0.5,
               "method": "deep-history seed (Hamilton NBER w16790 / EIA chronology), Joe-gated"}
        conn.execute(
            "UPDATE events SET sr_actor=?,sr_target=?,sr_conflict_scope='unknown',sr_tempo='unknown',"
            "sr_alliance='unknown',sr_diplomatic='unknown',sr_target_capacity='unknown',"
            "sr_outcome_30=?,sr_outcome_90=?,sr_prior_dyad='unknown',sr_confidence=0.5,sr_json=? "
            "WHERE event_id=?",
            (e.get("actor"), e.get("target"), e["outcome_90"], e["outcome_90"],
             json.dumps(rec), e["event_id"]))
        n_new += 0 if exists else 1
    conn.commit()
    tot70 = conn.execute("SELECT COUNT(*) FROM events WHERE event_date<'1990-01-01'").fetchone()[0]
    seeded = conn.execute("SELECT COUNT(*) FROM events WHERE event_date<'1990-01-01' "
                          "AND description LIKE '%deep-history tier%'").fetchone()[0]
    conn.close()
    print(json.dumps({"seed_events": len(seed), "newly_inserted": n_new,
                      "deep_history_events_pre1990": seeded,
                      "all_events_pre1990": tot70,
                      "target": ">=60 (spec A8)",
                      "gap_note": "curated high-confidence seed; remainder via the caged "
                                  "extractor over Hamilton/EIA under the two-source rule, Joe-gated"},
                     indent=2))


if __name__ == "__main__":
    run()
