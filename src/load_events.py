"""
load_events.py -- loads your hand-curated events from data/events.csv into the database.

Why a CSV? Because curating events is ANALYST work, not coding work. You edit the
CSV in a spreadsheet; this script validates it and loads it into the `events` and
`event_entities` tables. Re-run it any time you add rows.

It also enforces the codebook: unsourced or badly-typed rows are REPORTED, not
silently accepted. A dataset you can't defend is worse than no dataset.

Run:  python3 src/load_events.py
"""

import csv
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
CSV_PATH = ROOT / "data" / "events.csv"

# Pre-registered event types (see EVENTS_CODEBOOK.md). Anything else is rejected.
VALID_TYPES = {
    "chokepoint_disruption",
    "opec_decision",
    "sanctions",
    "conflict_escalation",
    "infrastructure_attack",
    "demand_shock",
    # Amendment 2026-07-23, approved by Joe with batch 3: deliberate government/
    # agency market interventions (SPR/IEA releases). Severity = scale of intervention.
    "policy_response",
}
VALID_PRECISION = {"day", "week", "month"}
VALID_CONFIDENCE = {"high", "medium", "low"}


def check(row, i):
    """Return a list of problems with this row (empty list = clean)."""
    problems = []
    if row["type"] not in VALID_TYPES:
        problems.append(f"type '{row['type']}' is not a registered type")
    if row["date_precision"] not in VALID_PRECISION:
        problems.append(f"date_precision '{row['date_precision']}' invalid")
    if row["confidence"] not in VALID_CONFIDENCE:
        problems.append(f"confidence '{row['confidence']}' invalid")
    try:
        datetime.strptime(row["event_date"], "%Y-%m-%d")
    except ValueError:
        problems.append(f"event_date '{row['event_date']}' is not YYYY-MM-DD")
    try:
        sev = int(row["severity"])
        if not 1 <= sev <= 5:
            problems.append("severity must be 1-5")
    except ValueError:
        problems.append("severity must be a number 1-5")
    try:
        sur = int(row.get("surprise") or 0)
        if not 1 <= sur <= 5:
            problems.append("surprise must be 1-5")
    except ValueError:
        problems.append("surprise must be a number 1-5")
    if not row["source_url"] or row["source_url"].strip() == "FILL_ME":
        problems.append("MISSING SOURCE (codebook: no source = not in the dataset)")
    return problems


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    rows = list(csv.DictReader(open(CSV_PATH, newline="", encoding="utf-8")))
    loaded, unsourced, rejected = 0, 0, 0

    for i, row in enumerate(rows, start=2):  # start=2 because line 1 is the header
        problems = check(row, i)
        # A missing source is a WARNING (you can keep drafting); anything else is fatal.
        fatal = [p for p in problems if not p.startswith("MISSING SOURCE")]
        if fatal:
            print(f"  ! line {i} ({row['event_id']}) REJECTED: {'; '.join(fatal)}")
            rejected += 1
            continue
        if problems:
            print(f"  ~ line {i} ({row['event_id']}): {problems[0]}")
            unsourced += 1

        # NOTE: columns are named explicitly rather than positional. After a
        # migration adds a column, positional inserts silently break -- named
        # ones don't. This is the safer habit.
        cur.execute(
            "INSERT OR REPLACE INTO events "
            "(event_id, event_date, date_precision, type, title, description, "
            " severity, surprise, confidence, source_url, added_at) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (
                row["event_id"], row["event_date"], row["date_precision"],
                row["type"], row["title"], row["description"],
                int(row["severity"]), int(row["surprise"]),
                row["confidence"], row["source_url"], now,
            ),
        )

        # Link the event to its entities, creating any entity we haven't seen before.
        for pair in filter(None, (p.strip() for p in row["entities"].split(";"))):
            entity_id, _, role = pair.partition(":")
            etype = entity_id.split(".")[0]          # 'country.iraq' -> 'country'
            pretty = entity_id.split(".", 1)[1].replace("_", " ").title()
            cur.execute(
                "INSERT OR IGNORE INTO entities VALUES (?,?,?,?)",
                (entity_id, etype, pretty, "auto-created by load_events"),
            )
            cur.execute(
                "INSERT OR IGNORE INTO event_entities VALUES (?,?,?)",
                (row["event_id"], entity_id, role or "affected_market"),
            )
        loaded += 1

    conn.commit()

    total = cur.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    ents = cur.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
    links = cur.execute("SELECT COUNT(*) FROM event_entities").fetchone()[0]
    print(f"\nLoaded {loaded} events ({rejected} rejected).")
    if unsourced:
        print(f"WARNING: {unsourced} event(s) still have no source_url - fill these before any analysis is publishable.")
    print(f"Database now holds: {total} events, {ents} entities, {links} event-entity links.")

    by_type = cur.execute(
        "SELECT type, COUNT(*) FROM events GROUP BY type ORDER BY COUNT(*) DESC"
    ).fetchall()
    print("\nEvents by type (this is your sample size per category):")
    for t, c in by_type:
        print(f"  {t:<24} {c}")
    conn.close()


if __name__ == "__main__":
    main()
