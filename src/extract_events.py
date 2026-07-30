"""
extract_events.py -- THE CAGE around the extraction worker (living-engine step 2).

The Cowork worker (Claude, no API key) proposes codebook-coded candidate events per ops/extract_agent.md.
This deterministic gate decides whether each proposal is allowed to become a CANDIDATE. It runs no LLM
and does no analysis. It enforces, hard (generalizing apply_situation_agent.py from typing -> events):

  * type/date_precision/confidence/severity/surprise obey the SAME closed vocab + ranges as
    load_events.check (the codebook gate) -- applied here at the FRONT, not just at the end;
  * FABRICATION GUARD: source_url must be a URL that physically appeared in this batch (an alert url,
    or a corroborating_url the worker supplied). An invented URL cannot enter -> routed to review;
  * POINT-IN-TIME: event_date must be <= the alert's timestamp AND <= today (no lookahead, no
    post-dating); the date is frozen at write time and made immovable by dedup;
  * DEDUP: against extract_seen (sidecar), against canon (events.csv ids + source_urls), and against
    pending candidates.

Clean proposals -> data/candidate_events.csv (status='candidate', candidate_source='llm_extract'),
severity/surprise LEFT BLANK (the worker's numbers are advisory only -- kept in the description, never
auto-committed; admit_events assigns a deterministic provisional band for auto-admits, Joe codes the
rest). Rejected proposals -> data/extract/review_queue.csv with the reason. A malformed batch writes
NOTHING and exits non-zero. Canon is only ever written later by apply_review.py + load_events.py.

Run:  python3 src/extract_events.py [proposals.json]   (default: newest data/extract/proposals_*.json)
"""

import csv
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

from load_events import VALID_TYPES, VALID_PRECISION, VALID_CONFIDENCE
from extract_prepare import SEEN_DB, EXTRACT_DIR, open_seen, _hash

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES = ROOT / "data" / "candidate_events.csv"
EVENTS = ROOT / "data" / "events.csv"
REVIEW_QUEUE = EXTRACT_DIR / "review_queue.csv"
CAND_FIELDS = ["event_id", "event_date", "date_precision", "type", "title", "description",
               "severity", "surprise", "confidence", "source_url", "entities", "status",
               "candidate_source"]


def _slug(title, url):
    import re
    base = re.sub(r"[^a-z0-9]+", "_", (title or "event").lower()).strip("_")[:40]
    tail = re.sub(r"[^a-z0-9]+", "", (url or "").lower())[-6:] or "xxxxxx"
    return f"{base}_{tail}_llm".strip("_")


def _rows(path):
    return list(csv.DictReader(open(path, newline="", encoding="utf-8"))) if Path(path).exists() else []


def _newest_proposals():
    files = sorted(EXTRACT_DIR.glob("proposals_*.json"))
    return files[-1] if files else None


def validate_one(p, batch, today):
    """Return (errors, frozen_row_or_None). Empty errors == clean; the row is ready for candidates."""
    errors = []
    alerts = {a["alert_id"]: a for a in batch.get("alerts", [])}
    known_urls = {a.get("url", "") for a in batch.get("alerts", [])}
    known_urls |= set(p.get("corroborating_urls") or [])

    # vocab / range gate (identical predicates to load_events.check, applied at the front)
    if p.get("type") not in VALID_TYPES:
        errors.append(f"type '{p.get('type')}' not registered")
    if p.get("date_precision") not in VALID_PRECISION:
        errors.append(f"date_precision '{p.get('date_precision')}' invalid")
    if p.get("confidence") not in VALID_CONFIDENCE:
        errors.append(f"confidence '{p.get('confidence')}' invalid")
    for k in ("severity_suggestion", "surprise_suggestion"):
        try:
            v = int(p.get(k))
            if not 1 <= v <= 5:
                errors.append(f"{k} must be 1-5")
        except (TypeError, ValueError):
            errors.append(f"{k} must be an integer 1-5")

    # fabrication guard: the source must be a real URL from this batch
    src = (p.get("source_url") or "").strip()
    if not src.startswith("http"):
        errors.append("source_url missing/not http")
    elif src not in known_urls:
        errors.append("source_url is not present in this batch (fabrication guard)")

    # point-in-time freeze
    ev_date = (p.get("event_date") or "").strip()
    try:
        d = datetime.strptime(ev_date, "%Y-%m-%d").date()
        if d > today:
            errors.append(f"event_date {ev_date} is in the future (lookahead)")
        alert = alerts.get(p.get("alert_id"))
        if alert and (alert.get("timestamp_utc") or "")[:10]:
            ats = datetime.strptime(alert["timestamp_utc"][:10], "%Y-%m-%d").date()
            if d > ats:
                errors.append(f"event_date {ev_date} is after the alert timestamp (lookahead)")
    except ValueError:
        errors.append(f"event_date '{ev_date}' is not YYYY-MM-DD")

    if errors:
        return errors, None
    sug = f"LLM-EXTRACTED (advisory sev={p['severity_suggestion']} surprise={p['surprise_suggestion']}; " \
          f"NOT coded -- gate/Joe codes). {p.get('rationale', '')}".strip()
    row = {"event_id": _slug(p.get("title"), src), "event_date": ev_date,
           "date_precision": p["date_precision"], "type": p["type"], "title": p.get("title", ""),
           "description": (p.get("description", "") + "  " + sug).strip(),
           "severity": "", "surprise": "", "confidence": p["confidence"], "source_url": src,
           "entities": p.get("entities", ""), "status": "candidate", "candidate_source": "llm_extract"}
    return [], row


def apply(proposals, batch):
    """Cage a whole batch. Returns a result dict; writes candidates only for clean proposals, routes
    the rest to the review queue, and marks each processed alert extract_seen (idempotent)."""
    today = datetime.now(timezone.utc).date()
    existing_ids = {r["event_id"] for r in _rows(EVENTS)} | {r["event_id"] for r in _rows(CANDIDATES)}
    existing_urls = {r["source_url"] for r in _rows(EVENTS)} | {r["source_url"] for r in _rows(CANDIDATES)}
    seen = open_seen()

    admitted, rejected = [], []
    for p in proposals:
        errs, row = validate_one(p, batch, today)
        if not errs:
            if row["event_id"] in existing_ids or row["source_url"] in existing_urls:
                errs = ["duplicate of an existing event/candidate"]
        if errs:
            rejected.append({"alert_id": p.get("alert_id"), "title": p.get("title", ""),
                             "source_url": p.get("source_url", ""), "reason": "; ".join(errs)})
        else:
            admitted.append(row)
            existing_ids.add(row["event_id"]); existing_urls.add(row["source_url"])
        # mark the alert seen for extraction regardless (a bad proposal shouldn't be re-bundled forever;
        # it lives in the review queue now)
        if p.get("alert_id"):
            seen.execute("INSERT OR IGNORE INTO extract_seen VALUES (?,?)",
                         (p["alert_id"], datetime.now(timezone.utc).isoformat(timespec="seconds")))
    seen.commit(); seen.close()

    if admitted:
        first = not CANDIDATES.exists()
        with open(CANDIDATES, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=CAND_FIELDS)
            if first:
                w.writeheader()
            for row in admitted:
                w.writerow(row)
    if rejected:
        first = not REVIEW_QUEUE.exists()
        EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
        with open(REVIEW_QUEUE, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["alert_id", "title", "source_url", "reason"])
            if first:
                w.writeheader()
            for r in rejected:
                w.writerow(r)
    return {"admitted": len(admitted), "rejected_to_review": len(rejected)}


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else _newest_proposals()
    if not path or not path.exists():
        print("extract_events: no proposals file (no-op).")
        return
    try:
        data = json.loads(path.read_text())
    except (ValueError, OSError) as e:
        print(f"extract_events: malformed proposals file -- writing nothing. ({e})")
        sys.exit(1)
    batch_id = data.get("batch_id", "")
    inbox = EXTRACT_DIR / f"{batch_id}.json"
    batch = json.loads(inbox.read_text()) if inbox.exists() else {"alerts": []}
    res = apply(data.get("proposals", []), batch)
    print(f"extract_events: {res['admitted']} candidate(s) staged, "
          f"{res['rejected_to_review']} routed to review from {path.name}.")


if __name__ == "__main__":
    main()
