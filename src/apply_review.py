"""
apply_review.py -- apply Joe's decisions from the review sheet. Joe's gate only.

WHAT IT DOES:
Reads data/candidate_review.csv AFTER Joe has filled the joe_decision column with
approve / reject. Then, and only then:
  * approve -> the row is appended to data/events.csv in the canonical 11-column
    format, and its status becomes 'approved' in candidate_events.csv.
  * reject  -> its status becomes 'rejected' in candidate_events.csv (kept on
    record, never deleted -- the rejection is part of reproducibility).

GUARDRAIL: an approved row is only written if it has a source_url AND a
severity AND a surprise (1-5). If any is missing, it is NOT appended -- it is
listed back to Joe to fix. A row you can't defend does not enter the dataset.
This tool never invents a value and never approves anything on its own.

Only load_events.py then moves approved rows from events.csv into the database.

It also WARNS (never blocks) when an approved event falls inside the 35-day
episode window of one already in the dataset: under the pre-registered clustering
those collapse into one episode (earliest kept), so the new event adds no
independent clustered observation. Joe still decides -- the warning is a heads-up,
not a gate.

Run:  python3 src/apply_review.py
"""

import csv
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEW = ROOT / "data" / "candidate_review.csv"
CANDIDATES = ROOT / "data" / "candidate_events.csv"
EVENTS = ROOT / "data" / "events.csv"

# 35-day episode window. Mirrors robustness.py's CLUSTER_DAYS; kept as a local
# constant so this lightweight CLI needn't import the whole analysis stack for one
# number. Two events within this many CALENDAR days collapse to one clustered
# episode (the earliest is kept), which is what the collision warning is about.
CLUSTER_DAYS = 35

CAND_FIELDS = ["event_id", "event_date", "date_precision", "type", "title",
               "description", "severity", "surprise", "confidence", "source_url",
               "entities", "status", "candidate_source"]
EVENT_FIELDS = [c for c in CAND_FIELDS if c not in ("status", "candidate_source")]

APPROVE = {"approve", "approved", "a", "yes", "y", "keep"}
REJECT = {"reject", "rejected", "r", "no", "n"}


def load(path):
    if not path.exists():
        return []
    return list(csv.DictReader(open(path, newline="", encoding="utf-8")))


def parse_date(s):
    """Parse an event_date; return a date or None if it isn't YYYY-MM-DD."""
    try:
        return datetime.strptime((s or "")[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def missing_required(row):
    """Return the list of required fields that are missing/invalid for approval."""
    problems = []
    if not (row.get("source_url", "") or "").strip().startswith("http"):
        problems.append("source_url")
    for fld in ("severity", "surprise"):
        val = (row.get(fld, "") or "").strip()
        try:
            if not (1 <= int(val) <= 5):
                problems.append(f"{fld} (must be 1-5)")
        except ValueError:
            problems.append(f"{fld} (missing)")
    return problems


def main():
    review = load(REVIEW)
    if not review:
        print(f"No review sheet at {REVIEW}. Run triage_candidates.py first, "
              f"then fill the joe_decision column.")
        return
    if "joe_decision" not in review[0]:
        print("The review sheet has no joe_decision column -- regenerate it with "
              "triage_candidates.py.")
        return

    decided = {r["event_id"]: (r.get("joe_decision", "") or "").strip().lower()
               for r in review}
    review_by_id = {r["event_id"]: r for r in review}

    # Nothing decided at all? Say so plainly.
    if not any(decided.values()):
        print("joe_decision is empty for every row -- fill in approve/reject in "
              f"{REVIEW.name} and re-run. Nothing applied.")
        return

    candidates = load(CANDIDATES)
    cand_by_id = {r["event_id"]: r for r in candidates}
    existing_rows = load(EVENTS)
    existing_event_ids = {r["event_id"] for r in existing_rows}
    # Running (date, id) list for collision detection -- seeded with the events
    # already in the dataset, and grown as we approve so a batch that approves two
    # nearby candidates flags the second against the first.
    prior_events = [(parse_date(r.get("event_date", "")), r["event_id"])
                    for r in existing_rows]

    approved, rejected, needs_input, dup, unknown, pending = [], [], [], [], [], 0
    collisions = []

    for eid, dec in decided.items():
        if dec == "":
            pending += 1
            continue
        row = review_by_id[eid]
        if dec in APPROVE:
            if eid in existing_event_ids:
                dup.append(eid)
                continue
            problems = missing_required(row)
            if problems:
                needs_input.append((eid, problems))
                continue
            # Cluster-collision check (informational, NON-blocking): is this event
            # inside the 35-day window of one already present or approved earlier
            # this run? If so it won't add an independent clustered observation.
            ed = parse_date(row.get("event_date", ""))
            hits = [(oid, od, abs((ed - od).days)) for (od, oid) in prior_events
                    if ed is not None and od is not None
                    and abs((ed - od).days) <= CLUSTER_DAYS]
            # Append to events.csv (Joe approved; this is the sanctioned path).
            write_header = not EVENTS.exists()
            with open(EVENTS, "a", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=EVENT_FIELDS)
                if write_header:
                    w.writeheader()
                w.writerow({k: row.get(k, "") for k in EVENT_FIELDS})
            existing_event_ids.add(eid)
            prior_events.append((ed, eid))    # later approvals can collide with it
            if hits:
                collisions.append((eid, ed, hits))
            if eid in cand_by_id:
                cand_by_id[eid]["status"] = "approved"
            approved.append(eid)
        elif dec in REJECT:
            if eid in cand_by_id:
                cand_by_id[eid]["status"] = "rejected"
            rejected.append(eid)
        else:
            unknown.append((eid, dec))

    # Persist status changes back to the candidate file.
    with open(CANDIDATES, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAND_FIELDS)
        w.writeheader()
        for r in candidates:
            w.writerow({k: r.get(k, "") for k in CAND_FIELDS})

    # --- Summary ---
    print("=" * 66)
    print("APPLY REVIEW -- what happened")
    print("=" * 66)
    print(f"  Appended to events.csv (approved): {len(approved)}")
    for eid in approved:
        print(f"      + {eid}")
    print(f"  Marked rejected:                   {len(rejected)}")
    if dup:
        print(f"  Skipped (already in events.csv):   {len(dup)}")
        for eid in dup:
            print(f"      = {eid}")
    if needs_input:
        print(f"\n  NEEDS YOUR INPUT before it can be approved: {len(needs_input)}")
        print("  (approved by you, but missing required fields -- not appended)")
        for eid, probs in needs_input:
            print(f"      ! {eid}: fix {', '.join(probs)}")
    if unknown:
        print(f"\n  Unrecognised joe_decision values (left pending): {len(unknown)}")
        for eid, dec in unknown:
            print(f"      ? {eid}: '{dec}'  (use approve or reject)")
    if collisions:
        print(f"\n  CLUSTER COLLISIONS ({len(collisions)}): approved, but within "
              f"{CLUSTER_DAYS}d of another event.")
        print(f"  Under the pre-registered clustering these collapse into ONE "
              f"episode (earliest kept), so")
        print(f"  they add no INDEPENDENT clustered observation. Approved anyway "
              f"(your call) -- just so you know:")
        for eid, ed, hits in collisions:
            for oid, od, gap in hits:
                print(f"      ~ {eid} ({ed}) <-> {oid} ({od}, {gap}d apart)")
    if pending:
        print(f"\n  Still blank / undecided: {pending}")
    if needs_input or pending or unknown:
        print("\n  Fix the flagged rows in the review sheet and re-run apply_review.py.")
    if approved:
        print("\n  Load the newly-approved events into the DB with: "
              "python3 src/load_events.py")


if __name__ == "__main__":
    main()
