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
    """Until 2026-09-03 this pinned framework_sound to True. That was the defect, not the check:
    evaluate.py graded itself with its own placebo shuffle, which passes, while the REGISTERED
    placebo (WALK_FORWARD_PROTOCOL §6, summary.json#/placebo/null_holds) was failing and H1 had
    been downgraded under the red_team_1 R7 bar. A test that pins the answer cannot notice that.
    It now asserts the RELATION -- sound if and only if the registered gates pass -- so it fails
    whichever way the two disagree, and never has to be edited when a run changes."""
    import json as _j
    r = _load()
    fw = r["overall"]["framework_sound"]
    g = r.get("registered_gates") or {}
    nh = (g.get("placebo") or {}).get("null_holds")
    legs = (g.get("h1") or {}).get("legs") or {}
    h1_ok = all(legs.values()) if legs else None
    assert g, "the report must carry the registered gates it read"
    if nh is False or h1_ok is False:
        assert fw is False, f"framework_sound is {fw} while a registered gate fails (placebo {nh}, H1 {h1_ok})"
    if nh is True and h1_ok is True:
        assert fw == bool(r["surface_consistency"]["all_consistent"])
    # and it must never be graded from this module's own placebo, which currently PASSES
    assert r["placebo"].get("gates") is False
