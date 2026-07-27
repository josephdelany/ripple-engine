"""
backfill_promotions.py -- link situation atoms to coded events (Wire 4).

When an alert is promoted through the HUMAN GATE (watcher -> candidate_review ->
apply_review -> load_events) it becomes a coded event with a source_url. If that
same source_url is sitting in situation_log as an 'observed' atom, this marks the
atom: it sets promoted_event_id and flips its status to 'promoted'. That is the
one place memory connects back to canon -- and it is READ-of-events / UPDATE-of-log
only. It never creates an event, never approves anything, and never runs the LLM.
The gate stays a gate; this just records that the gate acted.

Run:  python3 src/backfill_promotions.py   (safe to re-run; idempotent)
"""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"


def backfill(conn):
    """Set promoted_event_id + status='promoted' on atoms whose source_url now
    matches a coded event. Only touches atoms not already promoted. Returns count."""
    matches = conn.execute(
        "SELECT sl.log_id, e.event_id FROM situation_log sl "
        "JOIN events e ON e.source_url = sl.source_url "
        "WHERE sl.promoted_event_id IS NULL").fetchall()
    for log_id, event_id in matches:
        conn.execute(
            "UPDATE situation_log SET promoted_event_id=?, status='promoted' "
            "WHERE log_id=?", (event_id, log_id))
    conn.commit()
    return len(matches)


def main():
    conn = sqlite3.connect(DB)
    n = backfill(conn)
    conn.close()
    print(f"backfill_promotions -- linked {n} situation atom(s) to coded events.")


if __name__ == "__main__":
    main()
