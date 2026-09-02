"""admit.py -- admit ONE dossier into the corpus, only on Joe's line (Brief A-6; data/candidates/DOSSIER_RULE.md §3-§4).

    python3 src/admit.py --dossier <id> --approved-by joe

Refuses without `--approved-by joe`, refuses a dossier whose front matter says `admissible: false`, refuses an
event_id already in the corpus. On approval: appends the row to data/events.csv (the corpus source of truth that
load_events.py upserts) and inserts it into `events` + `event_entities` with the dossier path as provenance in the
description, and stamps the dossier's front matter with approved_by / approved_at. The code never runs this itself.
"""
import argparse
import csv
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOSSIERS = ROOT / "data" / "candidates" / "dossiers"
EVENTS_CSV = ROOT / "data" / "events.csv"
DB = ROOT / "data" / "oil.db"
COLS = ["event_id", "event_date", "date_precision", "type", "title", "description", "severity", "surprise", "confidence", "source_url", "entities"]


class Refused(Exception):
    pass


def read_front(path):
    text = Path(path).read_text(encoding="utf-8")
    m = re.search(r"```json\n(.*?)\n```", text, re.S)
    if not m:
        raise Refused(f"{path}: no front matter")
    return json.loads(m.group(1)), text


def event_row(front, dossier_rel, approved_by, now):
    ss = front.get("second_source") or {}
    if not front.get("admissible") or not ss.get("found"):
        raise Refused(f"{front.get('id')}: dossier is not admissible (second source: none found)")
    prim = front["primary"]
    ents = ";".join(f"{e['entity']}:{e['role']}" for e in front.get("entities") or [] if e.get("entity"))
    title = f"{prim.get('crisno') and 'ICB crisis ' + str(prim['crisno']) + ': ' or ''}{front['id'].split('_', 2)[-1].replace('_', ' ')}"
    desc = (f"Pre-1987 admission from dossier {dossier_rel} (rule data/candidates/DOSSIER_RULE.md); approved by {approved_by} on {now[:10]}. "
            f"Primary record: {prim.get('dataset')} {prim.get('url')}; second source: {ss.get('route')} {ss.get('url')} ({ss.get('date')}).")
    return {"event_id": front["id"], "event_date": front["event_date"], "date_precision": front.get("date_precision", "day"), "type": front["proposed_class"],
            "title": title, "description": desc, "severity": int(front.get("proposed_severity", 2)), "surprise": int(front.get("proposed_surprise", 3)),
            "confidence": front.get("proposed_confidence", "medium"), "source_url": prim["url"], "entities": ents}


def admit(dossier_id, approved_by, dossiers=DOSSIERS, events_csv=EVENTS_CSV, db=DB, now=None):
    if approved_by != "joe":
        raise Refused("refused: admission requires --approved-by joe (SESSION_CHARTER.md §2.3: nothing enters events without Joe)")
    path = Path(dossiers) / f"{dossier_id}.md"
    if not path.exists():
        raise Refused(f"no dossier {path}")
    front, text = read_front(path)
    now = now or datetime.now(timezone.utc).isoformat(timespec="seconds")
    row = event_row(front, str(path.relative_to(ROOT)) if str(path).startswith(str(ROOT)) else str(path), approved_by, now)
    conn = sqlite3.connect(db)
    try:
        if conn.execute("SELECT 1 FROM events WHERE event_id=?", (row["event_id"],)).fetchone():
            raise Refused(f"{row['event_id']} is already in events")
        with open(events_csv, newline="", encoding="utf-8") as f:
            if any(r.get("event_id") == row["event_id"] for r in csv.DictReader(f)):
                raise Refused(f"{row['event_id']} is already in {events_csv}")
        with open(events_csv, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLS)
            w.writerow(row)
        conn.execute("INSERT INTO events (event_id, event_date, date_precision, type, title, description, severity, confidence, source_url, added_at, surprise) "
                     "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                     (row["event_id"], row["event_date"], row["date_precision"], row["type"], row["title"], row["description"], row["severity"],
                      row["confidence"], row["source_url"], now, row["surprise"]))
        for pair in filter(None, row["entities"].split(";")):
            ent, role = pair.split(":")
            conn.execute("INSERT OR IGNORE INTO entities (entity_id, type, name, notes) VALUES (?,?,?,?)", (ent, ent.split(".")[0], ent.split(".", 1)[1], "dossier admission"))
            conn.execute("INSERT OR IGNORE INTO event_entities (event_id, entity_id, role) VALUES (?,?,?)", (row["event_id"], ent, role))
        conn.commit()
    finally:
        conn.close()
    front["approved_by"], front["approved_at"] = approved_by, now
    text = re.sub(r"```json\n.*?\n```", "```json\n" + json.dumps(front, indent=1, default=str) + "\n```", text, count=1, flags=re.S)
    path.write_text(text, encoding="utf-8")
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dossier", required=True)
    ap.add_argument("--approved-by", default=None)
    a = ap.parse_args()
    try:
        row = admit(a.dossier, a.approved_by)
    except Refused as e:
        print(str(e)); sys.exit(2)
    print(f"admitted {row['event_id']} ({row['event_date']}, {row['type']}) -> data/events.csv + events; provenance in description")


if __name__ == "__main__":
    main()
