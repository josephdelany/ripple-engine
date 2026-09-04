"""Every Markdown file a reader might open must say what it is, on its first line.

The repository preserves six weeks of superseded work on purpose — the retractions are evidence
of research discipline, and deleting them would destroy that evidence. The cost is that a reader
who opens `docs/RIPPLE_FINDINGS.md` or `scaffolding/NORTH_STAR.md` has no way to know it is not
current guidance. `docs/audit/FILE_CLASSIFICATION.csv` classifies every tracked file, but nobody
consults a CSV before opening a plausible-looking document.

So the label goes on the document. Each non-authoritative Markdown file carries a first-line
blockquote declaring one of four statuses, and this guard fails if one is missing, unrecognised,
or attached to a document that is supposed to be authoritative.

This is deliberately a guard rather than a one-time relocation. Moving files would have taken the
1,005-test historical suite with `src/engine/**`, and a move can silently drift back; a check in
the release gate cannot.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Directories whose own name is the label. A reader inside `archive/` already knows.
EXEMPT_DIRS = ("archive/", "data/", "parked/", "practice/", "tests/", ".github/")

# The maintained public product plus the working files of the current phase. These must NOT carry
# a superseded banner; anything else must carry one of the four statuses below.
AUTHORITATIVE = {
    "README.md", "SUBMISSION_STATUS.md", "CLAUDE.md", "COORDINATION.md",
    "docs/README.md", "docs/PAPER.md", "docs/RESUME.md", "docs/DEMO.md",
    "registrations/STRUCTURAL_SURFACE_EXPERIMENT.md",
    "registrations/STRUCTURAL_COMPONENT_ABLATION.md",
    # Registered 2026-09-03 and not yet run. A live registration is authoritative about what was
    # pre-committed even before anything is executed under it; banner it only if it is superseded.
    "registrations/CONTEMPORANEOUS_AVAILABILITY_ARM.md",
}
AUTHORITATIVE_DIRS = ("docs/audit/",)

# SUPERSEDED   a claim document replaced by a current one; its conclusions may be wrong.
# ARCHIVED     a historical or evidence record, preserved for audit, not a current claim.
# REFERENCE    a specification or codebook, accurate for what it describes, claiming no result.
# WORKING NOTE internal build, ops or planning material; never a claim about findings.
STATUSES = ("SUPERSEDED", "ARCHIVED", "REFERENCE", "WORKING NOTE")
BANNER = re.compile(r"^> \*\*(" + "|".join(STATUSES) + r")\b")


def tracked_markdown():
    out = subprocess.run(["git", "ls-files", "*.md"], cwd=ROOT, capture_output=True, text=True,
                         check=True).stdout.split()
    return [p for p in out if not p.startswith(EXEMPT_DIRS)]


def is_authoritative(path):
    return path in AUTHORITATIVE or path.startswith(AUTHORITATIVE_DIRS)


def first_line(path):
    with (ROOT / path).open(encoding="utf-8") as f:
        return f.readline().rstrip("\n")


def problems():
    found = []
    for path in tracked_markdown():
        line = first_line(path)
        if is_authoritative(path):
            # An authoritative document carrying a superseded banner is the more dangerous
            # direction of this error: it makes the real product look retracted.
            if BANNER.match(line):
                found.append(f"{path}: authoritative document carries a status banner")
            continue
        if not BANNER.match(line):
            found.append(f"{path}: no status banner on line 1 "
                         f"(expected '> **{'|'.join(STATUSES)} ...**')")
    return found


def main():
    found = problems()
    if found:
        raise SystemExit("\n".join(found) + f"\n{len(found)} document(s) without a usable status")
    n = len(tracked_markdown())
    print(f"document status: VERIFIED ({n} tracked Markdown files outside "
          f"{', '.join(EXEMPT_DIRS)} each declare authoritative or one of {', '.join(STATUSES)})")


if __name__ == "__main__":
    main()
