"""
evidence_pack.py -- one command per paper, so a writing session never hunts for a
number or cites a stale one.

Each paper cites a handful of frozen numbers that the engine already computed and
committed to a results file. This tool gathers exactly those, VERBATIM from the
committed files, and stamps each with (a) the file it came from and (b) the git
commit hash of the run that produced that file -- so every number in the paper is
traceable to an exact, reproducible state of the repository. It generates no prose
beyond fixed labels; it copies and cites.

Topics:  flagship  (the cost-of-coercion ripple paper)
         buffers   (physical tightness / inventories, H2)
         alarm     (threat inflation / the quiet-set control)
         me        (Middle East conflict subset)

Run:  python3 src/evidence_pack.py flagship
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# topic -> [(results_file, label, regex)]. Each regex pulls the exact lines the
# paper cites. Lines are copied verbatim; the label is the only added text.
TOPICS = {
    "flagship": [
        ("registered_run_results.txt", "Registered verdict (n=20, confirmatory)",
         r"H[123] (?:HOLDS|FAILS) \(clustered [+-][\d.]+ pp"),
        ("expanded_run_results.txt", "Expanded-sample verdict (n=30, alongside)",
         r"H[123]\s+(?:HOLDS|FAILS)\s+\([+-][\d.]+ pp\)"),
        ("cross_asset_results.txt", "Conflict-escalation Brent ripple (clustered)",
         r"^\s*conflict_escalation\s"),
        ("inference_results.txt", "H1 under standardization (robustness lens)",
         r"H1 \(VIX\) read:"),
    ],
    "buffers": [
        ("registered_run_results.txt", "H2 inventories verdict (registered)",
         r"H2 (?:HOLDS|FAILS) \(clustered"),
        ("inference_results.txt", "H2 raw / standardized / permutation",
         r"H2 \(inv_sigma\):"),
        ("cross_asset_results.txt", "Physical-tightness context (natgas row)",
         r"^\s*infrastructure_attack\s"),
    ],
    "alarm": [
        ("quiet_comparison.txt", "Quiet set vs corpus |CAR+20| + permutation p",
         r"(quiet set\s+n=|main corpus\s+n=|difference in means|two-sided permutation p \()"),
    ],
    "me": [
        ("me_report.txt", "ME corpus size + type mix", r"ME events in corpus:"),
        ("me_report.txt", "Per-decade clustered CAR+20 (ME conflict + infra)",
         r"^\s*(1990s|2000s|2010s|2020s)\s"),
    ],
}


def git_hash(path):
    """Short commit hash of the last commit that touched this file (or 'uncommitted')."""
    try:
        out = subprocess.check_output(
            ["git", "-C", str(ROOT), "log", "-1", "--format=%h", "--", str(path)],
            stderr=subprocess.DEVNULL).decode().strip()
        return out or "uncommitted"
    except subprocess.CalledProcessError:
        return "uncommitted"


def main():
    topic = sys.argv[1] if len(sys.argv) > 1 else ""
    if topic not in TOPICS:
        print(f"Usage: python3 src/evidence_pack.py <{' | '.join(TOPICS)}>")
        return

    out = [f"# Evidence pack -- {topic}", "",
           "_Frozen numbers this paper cites, copied verbatim from committed "
           "results files. Each is stamped with its source file and the git commit "
           "hash of the run that produced it. No number here is retyped or "
           "recomputed._", ""]
    total = 0
    for fname, label, pattern in TOPICS[topic]:
        path = DATA / fname
        out.append(f"## {label}")
        if not path.exists():
            out.append(f"- _MISSING: {fname} not found (run the step that "
                       f"produces it)._\n")
            continue
        h = git_hash(path)
        matches = [ln.rstrip() for ln in path.read_text().splitlines()
                   if re.search(pattern, ln)]
        if not matches:
            out.append(f"- _no matching lines in {fname} @ {h}_\n")
            continue
        out.append(f"_source: `data/{fname}` @ commit `{h}`_")
        out.append("```")
        out.extend(m.strip() for m in matches)
        out.append("```")
        out.append("")
        total += len(matches)

    dest = DATA / f"pack_{topic}.md"
    dest.write_text("\n".join(out) + "\n")
    print("\n".join(out))
    print(f"\nWrote {dest}  ({total} cited lines).")


if __name__ == "__main__":
    main()
