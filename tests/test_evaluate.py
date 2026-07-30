"""
test_evaluate.py -- the soundness checks themselves stay sound.

The two load-bearing guarantees: the negative-control placebo comes back NULL (if it ever "passes", the
whole gate is finding signal in noise), and the surfaces agree on the headline number. A regression that
breaks either fails here. Run: python3 -m pytest -q tests/test_evaluate.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVAL = ROOT / "data" / "evaluation.json"


def _load():
    assert EVAL.exists(), "run: python3 src/evaluate.py"
    return json.loads(EVAL.read_text())


def test_ev1_placebo_is_null():
    r = _load()
    pl = r["placebo"]
    assert pl.get("ran") is True
    assert pl.get("null_as_expected") is True          # shuffled-label amplification must span zero
    lo, hi = pl["placebo_ci95"]
    assert lo <= 0 <= hi


def test_ev2_surfaces_consistent():
    r = _load()
    assert r["surface_consistency"]["all_consistent"] is True


def test_ev3_validated_claims_are_robust():
    # every validated claim the evaluation reports must survive leave-one-cluster-out
    r = _load()
    for c in r["power"]["claims"]:
        if c.get("n"):
            assert c.get("robust_leave_one_out") in (True, None)   # True (robust) or arrays-unavailable
    # at least H1 must be present and robust
    h1 = next((c for c in r["power"]["claims"] if c["claim"] == "H1"), None)
    assert h1 and h1["robust_leave_one_out"] is True


def test_ev4_framework_sound():
    r = _load()
    assert r["overall"]["framework_sound"] is True
