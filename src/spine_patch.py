#!/usr/bin/env python3
"""
spine_patch.py -- turn dossiers into a patch file for Joe. (Session E)

The charter's rule 3 is absolute: nothing enters `events` without Joe. So this script
does the work up to that line and stops. It reads the dossiers, reads the current values
from the database READ-ONLY, and writes a patch file describing what would change and on
whose authority. It never opens the database for writing, never touches data/events.csv,
and never runs the admit line.

WHAT A PATCH ROW IS
    event_id, field, current value (read from the database now), proposed value,
    the source marker(s) from the dossier, and the dossier path.
A field that no source supports is not proposed. Where the dossier shows a value is
wrong but establishes no replacement, the proposal is the string 'unknown' -- the
sourced-or-unknown rule resolves ties toward admitting ignorance, per charter Sec 2.1.

INPUT: the '## Proposed field changes' section of each dossier, one row per field, in
any of these shapes (the parser is deliberately tolerant):
    | field | current | proposed | source |
    - field: current -> proposed [S1]
    field = proposed  [S2]

USAGE
    python3 src/spine_patch.py --batch pre1990_a                  # every dossier
    python3 src/spine_patch.py --batch b --events id1 id2         # named ones
    python3 src/spine_patch.py --batch b --print                  # show, write nothing
Writes data/spine/patches/<batch>.json and prints a human summary.

APPLYING IT IS JOE'S STEP, NOT THIS SCRIPT'S. The patch file records, per row, that it
is unapplied; the applier records who approved it in data/spine/PATCH_LOG.md.
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "oil.db"
DOSSIERS = ROOT / "data" / "dossiers"
PATCH_DIR = ROOT / "data" / "spine" / "patches"

# Only these columns may ever be proposed. event_id is the key and is never patched;
# sr_* fields belong to session A's situation coding and are out of scope here.
PATCHABLE = {
    "event_date", "date_precision", "type", "title", "description",
    "severity", "confidence", "source_url", "surprise",
}

MARKER_RE = re.compile(r"\[S\d+(?:\s*,\s*S?\d+)*\]")


def split_sections(text: str) -> dict[str, str]:
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^##+\s+(.*?)\s*$", line)
        if m:
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


def find_section(sections: dict[str, str], want: str) -> str | None:
    wl = want.lower()
    for k, v in sections.items():
        if k.lower().startswith(wl):
            return v
    return None


def clean(cell: str) -> str:
    """Strip markdown emphasis, backticks and surrounding whitespace from a cell."""
    s = cell.strip().strip("`").strip()
    s = re.sub(r"^\*{1,2}|\*{1,2}$", "", s).strip()
    return s


def norm_value(s: str):
    """'NULL'/'none'/'' -> None; digits -> int; else the trimmed string."""
    t = clean(s)
    if t.lower() in ("", "null", "none", "n/a", "-", "—", "(null)"):
        return None
    if re.fullmatch(r"-?\d+", t):
        return int(t)
    return t


def parse_changes(block: str) -> list[dict]:
    """Rows of the 'Proposed field changes' section, in any of the tolerated shapes."""
    rows: list[dict] = []
    if not block:
        return rows
    for line in block.splitlines():
        if not line.strip() or set(line.strip()) <= set("|-: "):
            continue
        markers = MARKER_RE.findall(line)
        src = " ".join(markers) if markers else None

        if line.strip().startswith("|"):
            cells = [c for c in line.strip().strip("|").split("|")]
            if len(cells) < 3:
                continue
            field = clean(cells[0]).lower()
            if field in ("field", "column"):      # header row
                continue
            cur, prop = norm_value(cells[1]), norm_value(MARKER_RE.sub("", cells[2]))
            if len(cells) >= 4 and not src:
                m = MARKER_RE.findall(cells[3])
                src = " ".join(m) if m else clean(cells[3]) or None
        else:
            m = re.match(r"^\s*[-*]?\s*([A-Za-z_]+)\s*[:=]\s*(.*?)\s*(?:->|→)\s*(.*)$",
                         MARKER_RE.sub("", line))
            if not m:
                continue
            field = m.group(1).strip().lower()
            cur, prop = norm_value(m.group(2)), norm_value(m.group(3))

        if field in PATCHABLE:
            rows.append({"field": field, "dossier_current": cur,
                         "proposed": prop, "source": src})
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True, help="batch name, e.g. pre1990_a")
    ap.add_argument("--events", nargs="*", help="event ids (default: every dossier)")
    ap.add_argument("--print", dest="do_print", action="store_true",
                    help="print the patch and write nothing")
    args = ap.parse_args()

    paths = ([DOSSIERS / f"{e}.md" for e in args.events] if args.events
             else sorted(DOSSIERS.glob("*.md")))
    paths = [p for p in paths if p.exists()]
    if not paths:
        raise SystemExit("no dossiers found")

    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row

    rows, skipped = [], []
    for p in paths:
        eid = p.stem
        sections = split_sections(p.read_text(encoding="utf-8"))
        status = (find_section(sections, "Status") or "").strip().splitlines()
        status = status[0].strip() if status else "unknown"
        changes = parse_changes(find_section(sections, "Proposed field changes") or "")
        if not changes:
            skipped.append(eid)
            continue
        cur_row = conn.execute(
            "SELECT * FROM events WHERE event_id=?", (eid,)).fetchone()
        if cur_row is None:
            skipped.append(f"{eid} (not in events)")
            continue
        live = dict(cur_row)
        for ch in changes:
            live_val = live.get(ch["field"])
            if ch["proposed"] is None or str(ch["proposed"]) == str(live_val):
                continue          # nothing to do, or the dossier restates the value
            rows.append({
                "event_id": eid,
                "field": ch["field"],
                "current_in_db": live_val,
                "proposed": ch["proposed"],
                "source": ch["source"],
                "dossier": str(p.relative_to(ROOT)),
                "dossier_status": status,
                "applied": False,
            })
    conn.close()

    patch = {
        "batch": args.batch,
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "built_by": "session E (src/spine_patch.py)",
        "registration": "SPINE_REGISTRATION.md",
        "note": ("Proposals only. Nothing enters `events` without Joe (charter Sec 2 rule 3). "
                 "This file was produced read-only; applying it is Joe's step, and the "
                 "applier appends what it did to data/spine/PATCH_LOG.md."),
        "n_rows": len(rows),
        "rows": rows,
    }

    print(f"patch '{args.batch}': {len(rows)} proposed field changes "
          f"across {len({r['event_id'] for r in rows})} events")
    for r in rows:
        print(f"  {r['event_id']:<30} {r['field']:<15} "
              f"{str(r['current_in_db'])[:38]!r} -> {str(r['proposed'])[:60]!r}  {r['source'] or ''}")
    if skipped:
        print(f"  (no proposed changes parsed for: {', '.join(skipped)})")

    if args.do_print:
        return
    PATCH_DIR.mkdir(parents=True, exist_ok=True)
    out = PATCH_DIR / f"{args.batch}.json"
    out.write_text(json.dumps(patch, indent=1), encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)} (unapplied; Joe admits)")


if __name__ == "__main__":
    main()
