#!/usr/bin/env python3
"""spine_apply.py -- apply a spine patch to `events`, only on Joe's line (Session E).

    python3 src/spine_apply.py --batch pre1990_a --approved-by joe
    python3 src/spine_apply.py --batch pre1990_a --dry-run      # show, change nothing

This is the admit line SPINE_REGISTRATION.md §3 step 3 describes, and the ONLY file in
Session E's toolchain that writes to the database. `src/spine_patch.py` builds a patch and
can never write; `src/spine_audit.py` and `src/spine_check.py` only read. Keeping the
writer in one small file is the point: there is exactly one place to audit.

WHAT IT REFUSES
  - no `--approved-by joe`                (charter §2 rule 3: nothing enters events without Joe)
  - a row flagged `needs_joe`             (the builder could not reduce it to a clean value)
  - a column outside the patch whitelist  (sr_* belongs to session A; event_id is the key)
  - a row already marked applied          (so re-running is safe and never double-applies)
  - a row whose live value has changed since the patch was built (someone else edited it)
  - a value that fails its column's own check (severity/surprise 1-5, precision day|week|
    month, event_date ISO, confidence high|medium|low, source_url http(s))

WHAT IT DOES, in order
  1. re-reads the live row and compares it against `current_in_db` recorded in the patch;
  2. gzips a timestamped backup of data/oil.db into data/backups/ before touching anything;
  3. runs the changes in ONE transaction, rolling back entirely on any error;
  4. re-runs src/spine_audit.py and records the scoreboard before and after;
  5. stamps `applied`, `applied_at` and `applied_by` on each row in the patch JSON;
  6. appends a dated entry to data/spine/PATCH_LOG.md saying what changed and what it moved.

It does not touch data/events.csv. For the pre-1990 tier that file holds only 2 of the 19
records (E→A handoff, 2026-09-02), so the CSV is not the source of truth there; A owns the
question of which path is canonical for that tier.
"""
from __future__ import annotations

import argparse
import gzip
import json
import re
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "oil.db"
PATCH_DIR = ROOT / "data" / "spine" / "patches"
BACKUPS = ROOT / "data" / "backups"
LOG = ROOT / "data" / "spine" / "PATCH_LOG.md"

PATCHABLE = {"event_date", "date_precision", "type", "title", "description",
             "severity", "confidence", "source_url", "surprise"}
VALID_PRECISION = {"day", "week", "month"}
VALID_CONFIDENCE = {"high", "medium", "low"}
# The closed set from EVENTS_CODEBOOK.md. A class outside it is refused.
VALID_TYPE = {"chokepoint_disruption", "opec_decision", "sanctions", "conflict_escalation",
              "infrastructure_attack", "demand_shock", "policy_response"}


class Refused(Exception):
    pass


def validate(field: str, value):
    """Return the value to write, or raise Refused. Mirrors the codebook's own ranges."""
    if field in ("severity", "surprise"):
        if not isinstance(value, int) or not 1 <= value <= 5:
            raise Refused(f"{field}={value!r} is not an integer 1-5 (codebook scale)")
        return value
    if field == "date_precision":
        if value not in VALID_PRECISION:
            raise Refused(f"date_precision={value!r} not in {sorted(VALID_PRECISION)}")
        return value
    if field == "confidence":
        if value not in VALID_CONFIDENCE:
            raise Refused(f"confidence={value!r} not in {sorted(VALID_CONFIDENCE)}")
        return value
    if field == "type":
        if value not in VALID_TYPE:
            raise Refused(f"type={value!r} is outside the codebook's closed set")
        return value
    if field == "event_date":
        if not (isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)):
            raise Refused(f"event_date={value!r} is not YYYY-MM-DD")
        return value
    if field == "source_url":
        if not (isinstance(value, str) and value.startswith(("http://", "https://"))):
            raise Refused(f"source_url={value!r} is not an http(s) URL")
        if "wikipedia.org" in value or "britannica.com" in value:
            raise Refused(f"source_url={value!r} is an encyclopaedia "
                          "(SPINE_REGISTRATION §1a: may orient a search, never cited)")
        return value
    if field in ("title", "description"):
        if not isinstance(value, str) or not value.strip():
            raise Refused(f"{field} is empty")
        return value.strip()
    raise Refused(f"{field} is not patchable")


def backup_db() -> Path:
    BACKUPS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out = BACKUPS / f"oil_{stamp}_pre_spine_apply.db.gz"
    with open(DB, "rb") as fin, gzip.open(out, "wb") as fout:
        shutil.copyfileobj(fin, fout)
    return out


def audit_numbers() -> dict:
    """Run the audit and return the overall block, so the log records what moved."""
    subprocess.run([sys.executable, str(ROOT / "src" / "spine_audit.py")],
                   cwd=ROOT, capture_output=True, text=True, check=False)
    p = ROOT / "data" / "spine" / "audit.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8")).get("overall", {})


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--batch", required=True)
    ap.add_argument("--approved-by", dest="approved_by", default=None)
    ap.add_argument("--dry-run", action="store_true",
                    help="print exactly what would change and write nothing")
    args = ap.parse_args()

    patch_path = PATCH_DIR / f"{args.batch}.json"
    if not patch_path.exists():
        raise Refused(f"no such patch: {patch_path.relative_to(ROOT)}")
    patch = json.loads(patch_path.read_text(encoding="utf-8"))
    rows = patch["rows"]

    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    todo, skipped = [], []
    for i, r in enumerate(rows):
        why = None
        if r.get("applied"):
            why = "already applied"
        elif r.get("needs_joe"):
            why = "needs_joe: the builder could not reduce it to a clean value"
        elif r["field"] not in PATCHABLE:
            why = f"{r['field']} is not patchable"
        if why is None:
            live = conn.execute("SELECT * FROM events WHERE event_id=?",
                                (r["event_id"],)).fetchone()
            if live is None:
                why = "event_id not in events"
            elif str(live[r["field"]]) != str(r["current_in_db"]):
                why = (f"live value moved since the patch was built "
                       f"({live[r['field']]!r} now, {r['current_in_db']!r} then)")
            else:
                try:
                    r["_value"] = validate(r["field"], r["proposed"])
                    r["_idx"] = i
                    todo.append(r)
                except Refused as e:
                    why = str(e)
        if why:
            skipped.append((r, why))
    conn.close()

    print(f"patch {args.batch}: {len(rows)} rows -> {len(todo)} to apply, "
          f"{len(skipped)} skipped")
    for r in todo:
        print(f"  APPLY  {r['event_id']:<30} {r['field']:<15} "
              f"{str(r['current_in_db'])[:34]!r} -> {str(r['_value'])[:60]!r}")
    for r, why in skipped:
        print(f"  skip   {r['event_id']:<30} {r['field']:<15} {why}")

    if args.dry_run:
        print("\n--dry-run: nothing written.")
        return
    if args.approved_by != "joe":
        raise Refused(
            "\nrefused: applying a patch requires --approved-by joe "
            "(SESSION_CHARTER.md §2 rule 3: nothing enters events without Joe). "
            "Use --dry-run to see the change without writing.")
    if not todo:
        print("\nnothing to apply.")
        return

    before = audit_numbers()
    backup = backup_db()
    print(f"\nbacked up the database to {backup.relative_to(ROOT)}")

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    w = sqlite3.connect(DB)
    try:
        with w:                      # one transaction; any exception rolls it all back
            for r in todo:
                w.execute(f"UPDATE events SET {r['field']}=? WHERE event_id=?",
                          (r["_value"], r["event_id"]))
    finally:
        w.close()

    for r in todo:
        rows[r["_idx"]].update(applied=True, applied_at=now, applied_by=args.approved_by)
        rows[r["_idx"]].pop("_value", None)
        rows[r["_idx"]].pop("_idx", None)
    patch["applied_at"] = now
    patch["applied_by"] = args.approved_by
    patch_path.write_text(json.dumps(patch, indent=1), encoding="utf-8")

    after = audit_numbers()
    keys = [("two_or_more_domains", "events with ≥2 source domains"),
            ("tertiary_source_url", "encyclopaedia-only source_url"),
            ("generic_root_url", "bare site-root source_url"),
            ("placeholder", "drafting scaffolding"),
            ("desc_ge_700", "descriptions ≥700 chars")]
    print("\nscoreboard (src/spine_audit.py):")
    lines = []
    for k, label in keys:
        b, a = before.get(k), after.get(k)
        if b is not None:
            mark = "" if b == a else "   <-- moved"
            print(f"  {label:<34} {b} -> {a}{mark}")
            lines.append(f"| {label} | {b} | {a} |")

    events = sorted({r["event_id"] for r in todo})
    entry = [f"\n### APPLIED `{args.batch}` — {now}, approved by {args.approved_by}", "",
             f"{len(todo)} field changes across {len(events)} events; "
             f"{len(skipped)} rows skipped. Backup: `{backup.relative_to(ROOT)}`.", ""]
    entry += ["| field change | from | to |", "|---|---|---|"]
    entry += [f"| `{r['event_id']}`.{r['field']} | {str(r['current_in_db'])[:60]} "
              f"| {str(r['_value'] if '_value' in r else r['proposed'])[:80]} |" for r in todo]
    if skipped:
        entry += ["", "Skipped:", ""]
        entry += [f"- `{r['event_id']}`.{r['field']} — {why}" for r, why in skipped]
    entry += ["", "Scoreboard before → after:", "", "| measure | before | after |",
              "|---|---|---|"] + lines + [""]
    txt = LOG.read_text(encoding="utf-8")
    LOG.write_text(txt.rstrip() + "\n" + "\n".join(entry) + "\n", encoding="utf-8")
    print(f"\nlogged to {LOG.relative_to(ROOT)}")


if __name__ == "__main__":
    try:
        main()
    except Refused as e:
        print(str(e), file=sys.stderr)
        sys.exit(2)
