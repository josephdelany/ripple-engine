"""
amendment_p_run.py -- WALK_FORWARD_PROTOCOL.md Amendment P (2026-09-03).

Runs the walk ONCE with the class filter removed (`read.CLASS_FILTER = False`), writing to a SEPARATE
output directory so that `walk_20260903T052633Z` and every number in it stand untouched. Exactly one thing
differs from the registered design: the candidate pool is all prior events with a closed outcome rather
than same-class ones. Retrieval, k, the menu, Hedge, the scores, the baselines, the clustering, the seeds
and the inference are unchanged.

Tests the hypothesis published in docs/ABNORMAL_RETURN_RESULT.md §2, which this run can falsify.

Run:  python3 src/engine/amendment_p_run.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from engine import read as R          # noqa: E402
import walk as W                      # noqa: E402

OUT = ROOT / "data" / "walk_forward" / "unfiltered"


def main():
    assert R.CLASS_FILTER is True, "the registered default must be True before this run flips it"
    R.CLASS_FILTER = False
    OUT.mkdir(parents=True, exist_ok=True)
    print("Amendment P: class filter OFF; writing to", OUT.relative_to(ROOT), flush=True)
    s = W.run(out_dir=OUT, with_figures=False)
    s["amendment_p"] = {
        "what": "the registered walk with read.CLASS_FILTER = False -- the candidate pool is every prior "
                "event with a closed outcome, not only same-class ones",
        "registered": "WALK_FORWARD_PROTOCOL.md Amendment P (2026-09-03), commit a69bd15, before this code",
        "changes_exactly_one_thing": "the class filter at src/engine/read.py:213. Retrieval, k, menu, Hedge, "
                                     "scores, baselines, clustering, seeds and inference are unchanged.",
        "does_not_supersede": "walk_20260903T052633Z stands; this is an additionally published diagnostic "
                              "run and it cannot move a §7 verdict (P.3).",
    }
    (OUT / "summary.json").write_text(json.dumps(s, indent=1, default=str))
    print("done:", s["run_id"])


if __name__ == "__main__":
    main()
