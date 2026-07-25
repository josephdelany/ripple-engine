"""
promote_alert.py -- Joe's one move from "alert" to "candidate". The gate stays shut.

The watcher only ever SURFACES. This is the single, deliberate, human step that
moves one alert into the candidate review sheet -- and even then it lands with
joe_decision BLANK and no severity/surprise. It is now a candidate awaiting Joe's
coding and approval, exactly like any other candidate. It is NOT an event, and it
cannot become one until Joe fills in the codings and sets joe_decision=approve and
runs apply_review/load_events. Nothing here shortcuts that.

Usage:
  python3 src/promote_alert.py <N>    # promote alert #N from data/alert_queue.csv
                                       # (N = 1-based row order; run with no args to list)
"""

import csv
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALERT_QUEUE = ROOT / "data" / "alert_queue.csv"
REVIEW = ROOT / "data" / "candidate_review.csv"

# The candidate_review.csv column order (triage_candidates.py's OUT_FIELDS).
REVIEW_FIELDS = ["recommendation", "rec_reason", "salience_mentions",
                 "event_id", "event_date", "date_precision", "type", "title",
                 "description", "severity", "surprise", "confidence", "source_url",
                 "entities", "status", "candidate_source", "joe_decision"]


def load_alerts():
    if not ALERT_QUEUE.exists():
        return []
    return list(csv.DictReader(open(ALERT_QUEUE, newline="", encoding="utf-8")))


def slug(headline, url):
    """A readable, unique-ish event_id for the candidate row."""
    base = re.sub(r"[^a-z0-9]+", "_", (headline or "alert").lower()).strip("_")[:40]
    tail = re.sub(r"[^a-z0-9]+", "", url.lower())[-6:] or "xxxxxx"
    return f"{base}_{tail}_watch".strip("_")


def promote(alert):
    """Append one alert to candidate_review.csv as a BLANK-decision candidate."""
    # Event date defaults to the alert's date -- Joe must confirm the real event date.
    alert_date = (alert.get("timestamp_utc") or "")[:10] or \
        datetime.now(timezone.utc).date().isoformat()
    row = {
        "recommendation": "(from watcher)",
        "rec_reason": f"watcher alert [{alert.get('source', '')}]; matched "
                      f"kw={alert.get('matched_keywords') or '-'} "
                      f"ents={alert.get('matched_entities') or '-'}",
        "salience_mentions": "-",
        "event_id": slug(alert.get("headline", ""), alert.get("url", "")),
        "event_date": alert_date,
        "date_precision": "day",
        "type": alert.get("heuristic_type", "") or "",   # heuristic; Joe confirms
        "title": alert.get("headline", ""),
        "description": ("PROMOTED FROM A WATCHER ALERT -- UNVERIFIED. Joe must "
                        "confirm the event, its real date, and code severity/"
                        "surprise before this can be approved."),
        "severity": "",                                  # BLANK -- Joe codes
        "surprise": "",                                  # BLANK -- Joe codes
        "confidence": "low",
        "source_url": alert.get("url", ""),
        "entities": alert.get("matched_entities", ""),
        "status": "candidate",
        "candidate_source": "watcher",
        "joe_decision": "",                              # BLANK -- the gate stays a gate
    }
    exists = REVIEW.exists()
    with open(REVIEW, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=REVIEW_FIELDS)
        if not exists:
            w.writeheader()
        w.writerow(row)
    return row["event_id"]


def main():
    alerts = load_alerts()
    if not alerts:
        print(f"No alerts in {ALERT_QUEUE}. Run: python3 src/watcher.py")
        return
    args = sys.argv[1:]
    if not args:
        print(f"{len(alerts)} alerts. Promote one with: "
              f"python3 src/promote_alert.py <N>\n")
        for i, a in enumerate(alerts, 1):
            print(f"  {i:>3}  [{a['source']}] {a['heuristic_type']:<20} "
                  f"{a['headline'][:60]}")
        return
    try:
        n = int(args[0])
        alert = alerts[n - 1]
    except (ValueError, IndexError):
        print(f"Give a valid alert number 1..{len(alerts)}.")
        return
    eid = promote(alert)
    print(f"Promoted alert #{n} -> candidate_review.csv as '{eid}'")
    print("  status=candidate, joe_decision=BLANK, severity/surprise BLANK.")
    print("  It is NOT an event. Code it, set joe_decision=approve, then run "
          "apply_review.py + load_events.py.")


if __name__ == "__main__":
    main()
