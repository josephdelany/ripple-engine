"""
situation.py -- the Situation Memory assembler (DETERMINISTIC; NO LLM).

The "middle clock": between the engine's deep history (coded events + base rates)
and the live tape (the watcher), this maintains a persistent per-conflict TIMELINE
so "where do we stand right now" is remembered state, not re-derived every session.

WHAT THIS FILE DOES (all deterministic Python -- no judgement, no math the engine
doesn't already compute):
  Slice 1 (attach): read the human-owned situations.yaml + the watcher's
    alert_queue.csv, and file each alert that touches a situation's member entities
    into situation_log as a sourced, tagged atom (status='observed').
  Slice 2 (render): read engine_read.json base rates + Brent and write a dossier
    markdown per situation (timeline + priced-state), with the "where we stand"
    synthesis left for the scoped agent (a later slice).

WHAT IT NEVER DOES: type/interpret the alerts (kind stays 'unmapped' until the
agent), compute a new metric, or touch the human gate. Attaching an alert here is
context/memory; it is orthogonal to promoting it into a coded event (that stays the
untouched watcher -> candidate_review -> apply_review -> load_events flow).

Run:  python3 src/situation.py
"""

import csv
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

# import-only reuse of the watcher's canonical GDELT country-code map (never
# modified). GDELT alerts carry country CODES (IRN, SAU); RSS alerts carry
# entity_ids (country.iran). We match against both, so we need this map.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from watcher import COUNTRY_CC  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
SIT_CONFIG = ROOT / "data" / "situations.yaml"
ALERT_QUEUE = ROOT / "data" / "alert_queue.csv"

# Alerts Joe has explicitly marked noise are not woven into the memory.
SKIP_ALERT_STATUS = {"dismissed"}


def load_situations(path=SIT_CONFIG):
    """The human-owned situation definitions. [] if the file is missing."""
    if not Path(path).exists():
        return []
    cfg = yaml.safe_load(Path(path).read_text()) or {}
    return cfg.get("situations", [])


def read_alerts(path=ALERT_QUEUE):
    """The watcher's alert queue as a list of dicts. [] if not generated yet."""
    if not Path(path).exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def match_set(member_entities):
    """The set an alert's tokens must intersect to belong to this situation:
    the member entity_ids PLUS the GDELT country code of each country member
    (so both alert formats attach)."""
    s = set(member_entities)
    for eid in member_entities:
        if eid.startswith("country."):
            code = COUNTRY_CC.get(eid.split(".", 1)[1])
            if code:
                s.add(code)
    return s


def alert_tokens(alert):
    """The entity tokens on an alert row (entity_ids and/or country codes)."""
    return {t for t in (alert.get("matched_entities") or "").split(";") if t}


def attach(conn, situations, alerts, now):
    """File every situation-touching alert into situation_log as a sourced,
    tagged 'observed' atom. Idempotent: UNIQUE(situation_id, source_url) + INSERT
    OR IGNORE means re-running adds 0 rows. Returns rows actually inserted."""
    before = conn.total_changes
    cur = conn.cursor()
    for sit in situations:
        if sit.get("status") == "closed":
            continue
        sid = sit["situation_id"]
        want = match_set(sit.get("member_entities", []))
        for a in alerts:
            if a.get("status") in SKIP_ALERT_STATUS:
                continue
            url = (a.get("url") or "").strip()
            if not url or not (alert_tokens(a) & want):
                continue
            # Provenance is COPIED, never generated. kind stays 'unmapped' (the
            # agent types it later); status is 'observed' (a real sourced
            # headline); confidence 'low' (unvetted), mirroring promote_alert.
            cur.execute(
                "INSERT OR IGNORE INTO situation_log "
                "(situation_id, ts, kind, actor_entity, headline, detail, "
                " source_url, retrieved_at, status, confidence, alert_url, "
                " promoted_event_id) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (sid, a.get("timestamp_utc") or now, "unmapped", None,
                 a.get("headline") or "(no headline)", None, url, now,
                 "observed", "low", url, None))
    return conn.total_changes - before


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    situations = load_situations()
    alerts = read_alerts()
    if not situations:
        print("No situations defined in data/situations.yaml -- nothing to do.")
        return
    conn = sqlite3.connect(DB)
    inserted = attach(conn, situations, alerts, now)
    conn.commit()
    print(f"Situation Memory attach -- {now}")
    print(f"  situations: {len(situations)}   alerts scanned: {len(alerts)}")
    print(f"  new situation_log atoms: {inserted}")
    for sit in situations:
        sid = sit["situation_id"]
        n = conn.execute("SELECT COUNT(*) FROM situation_log WHERE situation_id=?",
                         (sid,)).fetchone()[0]
        print(f"    {sid:<34} {n:>4} atoms")
    conn.close()


if __name__ == "__main__":
    main()
