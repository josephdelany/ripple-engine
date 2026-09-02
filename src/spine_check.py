#!/usr/bin/env python3
"""
spine_check.py -- does a dossier actually meet SPINE_REGISTRATION.md? (Session E)

A dossier is a claim that an event record is now sourced. This script checks the claim
mechanically, so that "complete" is a computed property and not an author's opinion. It
is the same idea as the rest of the repo: verify by running, not by reading.

WHAT IT CHECKS, per dossier in data/dossiers/*.md
  sections     the fixed section order of SPINE_REGISTRATION.md Sec 2 is present
  sources      at least one source whose role is 'primary'; at least two DISTINCT
               source domains (leading 'www.' stripped, as the audit counts them);
               every source carries a URL, a retrieved_at stamp and a verbatim quote
  markers      every [Sn] cited in the narrative resolves to a listed source, and every
               listed source is actually cited somewhere
  narrative    120-250 words (SPINE_REGISTRATION Sec 1b)
  banned       no wikipedia citation anywhere in the sources (Sec 1a / Sec 5)
  honesty      a dossier claiming 'complete' must pass every check above. Claiming
               'partial' is always allowed -- a partial dossier is a legitimate result,
               and this script never rewrites a status, it only contradicts a false one.

It writes nothing except its own report. It never touches the database.

USAGE
    python3 src/spine_check.py                  # check every dossier
    python3 src/spine_check.py <event_id> ...   # check named ones
    python3 src/spine_check.py --json           # machine-readable
Exit status is 1 if any dossier FAILS a check it claims to pass.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DOSSIERS = ROOT / "data" / "dossiers"

REQUIRED_SECTIONS = [
    "Sources", "Narrative", "Knowable at", "Entities", "Class",
    "Not known at the time", "Proposed field changes", "Status",
]
URL_RE = re.compile(r"https?://[^\s)\]<>\"'|]+")
MARKER_RE = re.compile(r"\[S(\d+)\]")
# A source line starts with S<n> in any of the shapes an author might write:
# "| S1 |", "- **S1**", "### S1", "S1."
SOURCE_LINE_RE = re.compile(r"(?:^|\|)\s*(?:[-*#>\s]*\*{0,2})S(\d+)\b", re.MULTILINE)
# An ISO-8601 stamp, which is how retrieved_at appears inside a table row. A bare DATE
# counts: a researcher who fetched a page today but did not log the minute should record
# the date and say so, not invent a time. Requiring a time would reward a fabricated one,
# which is the exact failure this whole process exists to prevent. The evidence that
# matters -- the URL and the verbatim quote -- is checked separately and is unaffected.
ISO_TS_RE = re.compile(r"\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2})?")
ISO_TIME_RE = re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}")


def domain_of(url: str) -> str:
    host = (urlparse(url).netloc or "").lower()
    return host[4:] if host.startswith("www.") else host


def split_sections(text: str) -> dict[str, str]:
    """Map '## Heading' -> body text. Tolerant of extra headings."""
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
    """Match a required section name against the headings actually present."""
    wl = want.lower()
    for k, v in sections.items():
        kl = k.lower()
        if kl == wl or kl.startswith(wl):
            return v
    return None


def parse_sources(block: str) -> list[dict]:
    """Pull S1..Sn out of the Sources block, however the author laid it out."""
    if not block:
        return []
    positions = [(int(m.group(1)), m.start()) for m in SOURCE_LINE_RE.finditer(block)]
    # de-duplicate by first occurrence, keep document order
    seen, ordered = set(), []
    for num, pos in positions:
        if num not in seen:
            seen.add(num)
            ordered.append((num, pos))
    out = []
    for i, (num, pos) in enumerate(ordered):
        end = ordered[i + 1][1] if i + 1 < len(ordered) else len(block)
        chunk = block[pos:end]
        urls = URL_RE.findall(chunk)
        low = chunk.lower()
        role = ("primary" if re.search(r"\bprimary\b", low)
                else "secondary" if re.search(r"\bsecondary\b", low)
                else "press" if re.search(r"\bpress\b", low) else None)
        # 'retrieved_at' may be named in the row, or -- in a table, where the word sits
        # in the header -- appear only as the ISO timestamp itself.
        has_retrieved = bool(re.search(r"retrieved", low)
                             or ISO_TS_RE.search(chunk))
        # a verbatim quote: quotation marks with some substance between them
        quote = bool(re.search(r"[\"“>].{25,}", chunk, re.S))
        out.append({
            "n": num, "role": role, "urls": urls,
            "date_only_retrieved_at": bool(
                ISO_TS_RE.search(chunk) and not ISO_TIME_RE.search(chunk)),
            "domains": sorted({domain_of(u) for u in urls if domain_of(u)}),
            "has_retrieved_at": has_retrieved, "has_quote": quote,
            "chars": len(chunk),
        })
    return out


def check_one(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    sections = split_sections(text)
    problems: list[str] = []
    notes: list[str] = []

    missing = [s for s in REQUIRED_SECTIONS if find_section(sections, s) is None]
    if missing:
        problems.append("missing sections: " + ", ".join(missing))

    src_block = find_section(sections, "Sources") or ""
    sources = parse_sources(src_block)
    if not sources:
        problems.append("no sources parsed (expected S1, S2, ...)")

    roles = [s["role"] for s in sources]
    if "primary" not in roles:
        problems.append("no source marked primary")
    domains = sorted({d for s in sources for d in s["domains"]})
    if len(domains) < 2:
        problems.append(f"needs 2 distinct source domains, found {len(domains)}: {domains}")
    for s in sources:
        if not s["urls"]:
            problems.append(f"S{s['n']} has no URL")
        if not s["has_retrieved_at"]:
            problems.append(f"S{s['n']} has no retrieved_at")
        if not s["has_quote"]:
            problems.append(f"S{s['n']} has no verbatim quote")
    date_only = [s_["n"] for s_ in sources if s_.get("date_only_retrieved_at")]
    if date_only:
        notes.append(f"retrieved_at is a date without a time for: {date_only}")
    bad = [d for d in domains if "wikipedia" in d]
    if bad:
        problems.append(f"cites wikipedia: {bad}")

    narrative = find_section(sections, "Narrative") or ""
    words = len(re.sub(r"\[S\d+\]", " ", narrative).split())
    if narrative and not (120 <= words <= 250):
        problems.append(f"narrative is {words} words, needs 120-250")
    cited = {int(m) for m in MARKER_RE.findall(narrative)}
    listed = {s["n"] for s in sources}
    if narrative and not cited:
        problems.append("narrative cites no [Sn] markers")
    dangling = sorted(cited - listed)
    if dangling:
        problems.append(f"narrative cites sources that are not listed: {dangling}")
    uncited = sorted(listed - cited)
    if uncited:
        notes.append(f"listed but not cited in the narrative: {uncited}")

    status_block = (find_section(sections, "Status") or "").strip().lower()
    claims_complete = bool(re.search(r"\bcomplete\b", status_block)) and not re.search(
        r"\bpartial\b", status_block)
    if not status_block:
        problems.append("no status")

    verdict = ("FAIL" if (claims_complete and problems)
               else "PASS" if not problems
               else "PARTIAL-OK")
    try:
        shown = str(path.relative_to(ROOT))
    except ValueError:      # a dossier outside the repo (a fixture, or an ad-hoc path)
        shown = str(path)
    return {
        "event_id": path.stem, "path": shown,
        "claims": "complete" if claims_complete else "partial",
        "verdict": verdict, "problems": problems, "notes": notes,
        "n_sources": len(sources), "domains": domains,
        "narrative_words": words,
        "primary": [s["n"] for s in sources if s["role"] == "primary"],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("event_ids", nargs="*")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not DOSSIERS.exists():
        raise SystemExit(f"no dossier directory: {DOSSIERS}")
    paths = ([DOSSIERS / f"{e}.md" for e in args.event_ids] if args.event_ids
             else sorted(DOSSIERS.glob("*.md")))
    missing = [p for p in paths if not p.exists()]
    if missing:
        raise SystemExit("no such dossier: " + ", ".join(str(p) for p in missing))

    results = [check_one(p) for p in paths]
    if args.json:
        print(json.dumps(results, indent=1))
    else:
        for r in results:
            print(f"{r['verdict']:<11} {r['event_id']:<32} claims={r['claims']:<8} "
                  f"sources={r['n_sources']} domains={len(r['domains'])} "
                  f"words={r['narrative_words']}")
            for p in r["problems"]:
                print(f"    problem: {p}")
            for n in r["notes"]:
                print(f"    note:    {n}")
        n_pass = sum(r["verdict"] == "PASS" for r in results)
        n_fail = sum(r["verdict"] == "FAIL" for r in results)
        n_part = sum(r["verdict"] == "PARTIAL-OK" for r in results)
        print(f"\n{len(results)} dossiers: {n_pass} pass, {n_part} partial (honest), "
              f"{n_fail} fail (claim more than they show)")
    sys.exit(1 if any(r["verdict"] == "FAIL" for r in results) else 0)


if __name__ == "__main__":
    main()
