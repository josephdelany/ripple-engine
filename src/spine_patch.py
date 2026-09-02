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


# Phrases that mean "this dossier deliberately proposes NO change to this field".
NO_CHANGE_RE = re.compile(
    r"\b(unchanged|not proposed|no change|not changed|does not propose|do not propose|"
    r"only flags?|flagged only|leave null|leave as null|leaving null|keep\b|retain\b|"
    r"propose leaving null|cannot be (?:set|established)|none proposed)\b", re.I)

# Where a cell is "value -- reasoning", the value is what precedes the first dash-like
# separator or the first sentence break. We never guess past that.
SPLIT_RE = re.compile(r"\s+(?:[-\u2013\u2014]{1,2}|,\s*(?=because|since)|\()\s*", re.I)

VALID_PRECISION = {"day", "week", "month"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def norm_value(s: str):
    """'NULL'/'none'/'' -> None; digits -> int; else the trimmed string."""
    t = clean(s)
    if t.lower() in ("", "null", "none", "n/a", "-", "\u2014", "(null)"):
        return None
    if re.fullmatch(r"-?\d+", t):
        return int(t)
    return t


def split_value_and_rationale(cell: str) -> tuple[str, str | None]:
    """'5 -- because X' -> ('5', 'because X'). Prose with no leading value stays whole."""
    t = clean(MARKER_RE.sub("", cell))
    parts = SPLIT_RE.split(t, maxsplit=1)
    head = parts[0].strip().rstrip(".").strip()
    tail = parts[1].strip() if len(parts) > 1 else None
    return head, tail


def coerce(field: str, raw: str):
    """Reduce a proposal cell to a clean value for `field`.

    Returns (value, rationale, ok). ok is False when the cell could not be reduced to
    something safe to write into that column -- those rows are kept in the patch and
    marked `needs_joe`, never silently mangled into prose.
    """
    if NO_CHANGE_RE.search(raw):
        return None, clean(MARKER_RE.sub("", raw)), None      # None ok => 'no change'
    head, tail = split_value_and_rationale(raw)

    if field in ("severity", "surprise"):
        # "4", and also the natural "Proposed 4" / "Propose 4" the dossiers use.
        m = re.match(r"^(?:propos(?:e|ed)\s+)?(\d)\b", head, re.I)
        return (int(m.group(1)), tail, True) if m and 1 <= int(m.group(1)) <= 5 \
            else (head, tail, False)
    if field == "date_precision":
        w = head.strip("`").split()[0].strip("`").lower() if head else ""
        return (w, tail, True) if w in VALID_PRECISION else (head, tail, False)
    if field == "event_date":
        # The date must LEAD the cell. A date mentioned inside prose ("[S2] dates the
        # start to 1991-01-16, but this dossier does not propose a change") is discussion,
        # not a proposal, and must never be lifted out of it.
        m = re.match(r"^\d{4}-\d{2}-\d{2}", head)
        return (m.group(0), tail, True) if m else (head, tail, False)
    if field == "source_url":
        m = re.search(r"https?://[^\s)\]<>\"\'|]+", raw)
        return (m.group(0), tail, True) if m else (head, tail, False)
    if field == "confidence":
        w = head.split()[0].lower().strip("`\"'") if head else ""
        return (w, tail, True) if w in {"high", "medium", "low"} else (head, tail, False)
    if field in ("description", "title"):
        # A quoted replacement must OPEN the cell. A quotation buried in commentary is
        # discussion about the field, not the proposed value.
        q = re.match(r"\s*[\"\u201c](.{40,}?)[\"\u201d]", clean(MARKER_RE.sub("", raw)), re.S)
        if q:
            return q.group(1).strip(), None, True
        # No leading quotation: this cell is commentary about the field ("Drop the DRAFT
        # language...", "The $20M split is not supported..."), not a replacement value.
        # Flag it for Joe rather than writing an argument into the description column.
        return (head, tail, False)
    return head, tail, False


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
            cur, prop = norm_value(cells[1]), cells[2]
            if len(cells) >= 4 and not src:
                m = MARKER_RE.findall(cells[3])
                src = " ".join(m) if m else clean(cells[3]) or None
        else:
            m = re.match(r"^\s*[-*]?\s*([A-Za-z_]+)\s*[:=]\s*(.*?)\s*(?:->|→)\s*(.*)$",
                         MARKER_RE.sub("", line))
            if not m:
                continue
            field = m.group(1).strip().lower()
            cur, prop = norm_value(m.group(2)), m.group(3)

        if field in PATCHABLE:
            rows.append({"field": field, "dossier_current": cur,
                         "raw_proposed": (prop if (prop or "").strip() else None),
                         "source": src})
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

    rows, skipped, no_change = [], [], []
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
            if ch["raw_proposed"] is None:
                continue
            value, rationale, ok = coerce(ch["field"], ch["raw_proposed"])
            if ok is None:
                no_change.append(f"{eid}.{ch['field']}")
                continue          # the dossier deliberately proposes no change
            if ok and str(value) == str(live_val):
                no_change.append(f"{eid}.{ch['field']}")
                continue          # the dossier restates the live value
            rows.append({
                "event_id": eid,
                "field": ch["field"],
                "current_in_db": live_val,
                "proposed": value,
                "rationale": rationale,
                "needs_joe": not ok,
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
        "n_needs_joe": sum(1 for r in rows if r["needs_joe"]),
        "fields_left_unchanged": no_change,
        "rows": rows,
    }

    print(f"patch '{args.batch}': {len(rows)} proposed field changes "
          f"across {len({r['event_id'] for r in rows})} events")
    for r in rows:
        print(f"  {r['event_id']:<30} {r['field']:<15} "
              f"{str(r['current_in_db'])[:38]!r} -> {str(r['proposed'])[:60]!r}  {r['source'] or ''}")
    if skipped:
        print(f"  (no proposed changes parsed for: {', '.join(skipped)})")
    if no_change:
        print(f"  ({len(no_change)} fields the dossiers deliberately leave unchanged)")
    nj = [r for r in rows if r["needs_joe"]]
    if nj:
        print(f"  ({len(nj)} rows could not be reduced to a clean value -> needs_joe)")

    if args.do_print:
        return
    PATCH_DIR.mkdir(parents=True, exist_ok=True)
    out = PATCH_DIR / f"{args.batch}.json"
    out.write_text(json.dumps(patch, indent=1), encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)} (unapplied; Joe admits)")


if __name__ == "__main__":
    main()
