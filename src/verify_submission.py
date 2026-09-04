"""Fast non-statistical submission checks; expensive reproduction is in Makefile."""
import re
from pathlib import Path

import public_claim_guard as claims

ROOT = Path(__file__).resolve().parent.parent
DOCS = [ROOT / "README.md", ROOT / "docs" / "PAPER.md", ROOT / "docs" / "RESUME.md",
        ROOT / "docs" / "README.md", ROOT / "docs" / "DEMO.md"]
LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def broken_links():
    broken = []
    for doc in DOCS:
        for target in LINK.findall(doc.read_text(encoding="utf-8")):
            target = target.split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            if not (doc.parent / target).resolve().exists():
                broken.append(f"{doc.relative_to(ROOT)} -> {target}")
    return broken


def main():
    problems = claims.violations()
    problems += [f"broken link: {x}" for x in broken_links()]
    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if "Market state versus event labels in historical analogy" not in cff:
        problems.append("CITATION.cff does not name the authoritative project")
    if problems:
        raise SystemExit("\n".join(problems))
    print("submission metadata, claims, and local links: VERIFIED")


if __name__ == "__main__":
    main()
