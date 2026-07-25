"""
review_candidates.py -- the human gate. Nothing enters the dataset without Joe.

WHY THIS IS THE WHOLE POINT:
The harvester can propose a thousand candidates; none of them are data until a
human has looked at the source, agreed the event is real and relevant, and coded
it. This tool is that gate. It walks the candidate file one row at a time and
takes exactly one of: approve / reject / edit / skip. Approved rows are appended
to data/events.csv in the canonical format (and only load_events.py then puts
them in the database). Rejected rows are KEPT with status=rejected -- never
deleted -- because the record of what you turned down is part of reproducibility.

Run:  python3 src/review_candidates.py
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES = ROOT / "data" / "candidate_events.csv"
EVENTS = ROOT / "data" / "events.csv"

# The candidate file's columns (events.csv columns + the two review columns).
CAND_FIELDS = ["event_id", "event_date", "date_precision", "type", "title",
               "description", "severity", "surprise", "confidence", "source_url",
               "entities", "status", "candidate_source"]
# events.csv is the same, MINUS the two review-only columns.
EVENT_FIELDS = [c for c in CAND_FIELDS if c not in ("status", "candidate_source")]

# The fields a human may correct during review (everything except the bookkeeping).
EDITABLE = ["event_date", "date_precision", "type", "title", "description",
            "severity", "surprise", "confidence", "source_url", "entities"]

VALID_TYPES = {"chokepoint_disruption", "opec_decision", "sanctions",
               "conflict_escalation", "infrastructure_attack", "demand_shock",
               "policy_response"}   # amendment 2026-07-23 (batch 3); see load_events.py


def load(path, fields=None):
    if not path.exists():
        return []
    return list(csv.DictReader(open(path, newline="", encoding="utf-8")))


def save_candidates(rows):
    """Rewrite the whole candidate file so review progress persists after each step."""
    with open(CANDIDATES, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAND_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in CAND_FIELDS})


def append_to_events(row):
    """Append an approved candidate to events.csv in the exact canonical format."""
    exists = EVENTS.exists()
    with open(EVENTS, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=EVENT_FIELDS)
        if not exists:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in EVENT_FIELDS})


def show(row):
    print("-" * 78)
    for k in CAND_FIELDS:
        print(f"  {k:<16} {row.get(k, '')}")
    print("-" * 78)


def do_edit(row):
    """Prompt for each editable field; Enter keeps the current value."""
    print("Edit fields (press Enter to keep the shown value):")
    for k in EDITABLE:
        cur = row.get(k, "")
        new = input(f"  {k} [{cur}]: ").strip()
        if new:
            row[k] = new
    # A couple of gentle codebook checks -- warn, don't block (Joe decides).
    if row.get("type") not in VALID_TYPES:
        print(f"  ! note: type '{row.get('type')}' is not a registered type.")
    if not (row.get("source_url", "").startswith("http")):
        print("  ! note: source_url is empty or not a URL -- the codebook needs a real source.")


def existing_event_ids():
    return {r["event_id"] for r in load(EVENTS)}


def main():
    rows = load(CANDIDATES)
    if not rows:
        print(f"No candidate file at {CANDIDATES}. Run the seed/harvester first.")
        return

    pending = [r for r in rows if r.get("status") == "candidate"]
    if not pending:
        print("No candidates are pending review. "
              "(All are already approved or rejected.)")
        return

    print(f"{len(pending)} candidate(s) pending review. "
          f"For each: [a]pprove  [r]eject  [e]dit  [s]kip  [q]uit\n")
    known_ids = existing_event_ids()
    approved = rejected = 0

    for row in pending:
        while True:
            show(row)
            choice = input("  a/r/e/s/q > ").strip().lower()
            if choice == "a":
                if row["event_id"] in known_ids:
                    print(f"  ! {row['event_id']} is already in events.csv -- "
                          f"skipping to avoid a duplicate.")
                    break
                row["status"] = "approved"
                append_to_events(row)
                known_ids.add(row["event_id"])
                save_candidates(rows)
                approved += 1
                print(f"  approved -> appended to events.csv")
                break
            if choice == "r":
                row["status"] = "rejected"
                save_candidates(rows)
                rejected += 1
                print("  rejected (kept on record, not deleted)")
                break
            if choice == "e":
                do_edit(row)
                save_candidates(rows)          # persist edits even before decision
                continue                        # re-show, then decide
            if choice == "s":
                print("  skipped (stays a candidate for next time)")
                break
            if choice == "q":
                print("  quitting -- progress saved.")
                save_candidates(rows)
                _summary(rows, approved, rejected)
                return
            print("  please type one of: a r e s q")

    save_candidates(rows)
    _summary(rows, approved, rejected)


def _summary(rows, approved, rejected):
    counts = {}
    for r in rows:
        counts[r.get("status", "?")] = counts.get(r.get("status", "?"), 0) + 1
    print(f"\nThis session: {approved} approved, {rejected} rejected.")
    print("Candidate file now:",
          ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    if approved:
        print("Load the newly-approved events with: python3 src/load_events.py")


if __name__ == "__main__":
    main()
