"""
load_quiet.py -- load the QUIET comparison set into its OWN table.

WHY A SEPARATE TABLE (this is a discipline point, not a convenience):
The quiet events are high-alarm shocks with NO oil-supply channel -- North Korea's
nuclear test, the Balakot airstrike, the Capitol... events an alarmist narrative
would expect to move oil, but which have no mechanism to. They are a COMPARISON
CLASS, not part of the studied corpus. If they ever leaked into the `events`
table they would contaminate every base rate and every registered hypothesis. So
they live in their own `quiet_events` table (same schema as events) and are only
ever read by quiet_compare.py. They must NEVER enter `events`.

Run:  python3 src/load_quiet.py     (or it is loaded on demand by quiet_compare.py)
"""

import csv
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
CSV_PATH = ROOT / "data" / "quiet_events.csv"

# Same columns as the events table (see init_db.py) -- a parallel, isolated table.
SCHEMA = """
CREATE TABLE IF NOT EXISTS quiet_events (
    event_id       TEXT PRIMARY KEY,
    event_date     TEXT NOT NULL,
    date_precision TEXT,
    type           TEXT NOT NULL,
    title          TEXT NOT NULL,
    description    TEXT,
    severity       INTEGER,
    surprise       INTEGER,
    confidence     TEXT,
    source_url     TEXT NOT NULL,
    added_at       TEXT
);
"""

COLS = ["event_id", "event_date", "date_precision", "type", "title",
        "description", "severity", "surprise", "confidence", "source_url"]


def load(conn):
    """Create the table if needed and (re)load it from the CSV. Returns row count."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn.executescript(SCHEMA)
    rows = list(csv.DictReader(open(CSV_PATH, newline="", encoding="utf-8")))
    for r in rows:
        conn.execute(
            "INSERT OR REPLACE INTO quiet_events "
            "(event_id, event_date, date_precision, type, title, description, "
            " severity, surprise, confidence, source_url, added_at) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (r["event_id"], r["event_date"], r["date_precision"], r["type"],
             r["title"], r["description"], int(r["severity"]), int(r["surprise"]),
             r["confidence"], r["source_url"], now))
    conn.commit()
    return len(rows)


def main():
    conn = sqlite3.connect(DB)
    n = load(conn)
    total = conn.execute("SELECT COUNT(*) FROM quiet_events").fetchone()[0]
    conn.close()
    print(f"Loaded {n} quiet comparison events into quiet_events "
          f"(table now holds {total}). These NEVER enter the events table.")


if __name__ == "__main__":
    main()
