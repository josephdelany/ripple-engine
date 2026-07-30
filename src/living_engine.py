"""
living_engine.py -- run the FULL auto-corpus loop as one deliberate step (living-engine orchestrator).

refresh.py runs only the SAFE ingestion half every cycle (extract_prepare -> extract_events), which is
additive and never touches Joe's review sheet. This orchestrator runs the WHOLE loop, including the
admission half (triage_candidates -> admit_events), behind its own lock -- for when Joe wants the corpus
to accrete hands-off (auto-admit the overwhelmingly-corroborated, queue the rest). It never writes canon
directly: apply_review.py + load_events.py remain the one gated path, so Joe still runs those (or a
future daily step does) to move approved rows into the events table -- and can veto any auto-admit first.

Run:  python3 src/living_engine.py
"""

import subprocess
import sys
from pathlib import Path

from _lock import acquire, release

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
LOCK = ROOT / "data" / "living.lock"
STEPS = ["extract_prepare.py", "extract_events.py", "triage_candidates.py", "admit_events.py"]


def main():
    if not acquire(LOCK, stale_secs=1800):
        print("living_engine: another run holds the lock. Exiting.")
        return
    try:
        for s in STEPS:
            print(f"==> {s}")
            r = subprocess.run([PY, str(ROOT / "src" / s)], cwd=ROOT)
            if r.returncode != 0:
                print(f"   ({s} exited {r.returncode} -- continuing; a bad step never writes canon)")
        print("\nliving_engine: ingestion + tiering done. Review data/candidate_review.csv "
              "(auto-admits are pre-approved with a receipt; veto if needed), then run "
              "apply_review.py + load_events.py to move approved rows into canon.")
    finally:
        release(LOCK)


if __name__ == "__main__":
    main()
