"""
test_kappa.py -- Cohen's kappa math is correct (F2.2 inter-coder reliability). Pure logic, no DB.
Run:  python3 -m pytest -q tests/test_kappa.py
"""

import kappa_report as K


def test_k1_perfect_agreement():
    assert K.cohen_kappa(["a", "b", "a", "c"], ["a", "b", "a", "c"]) == 1.0


def test_k2_known_value():
    # a=[1,1,1,0], b=[1,1,0,0]: po=0.75, pe=0.5 -> kappa=0.5 (hand-computed)
    assert K.cohen_kappa(["1", "1", "1", "0"], ["1", "1", "0", "0"]) == 0.5


def test_k3_chance_level_is_near_zero():
    # total disagreement in a 2-category, balanced setup -> kappa < 0
    k = K.cohen_kappa(["a", "a", "b", "b"], ["b", "b", "a", "a"])
    assert k is not None and k < 0


def test_k4_empty_and_degenerate():
    assert K.cohen_kappa([], []) is None
    # single category for both -> pe == 1 -> undefined (None), never a fake 1.0
    assert K.cohen_kappa(["a", "a"], ["a", "a"]) is None
