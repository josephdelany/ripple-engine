"""
test_edge_battery.py -- the pre-registered edge battery (family-wise corrected; honest nulls).

These tests protect the DISCIPLINE, not a particular result: the battery must be pre-registered (a
fixed hypothesis set), family-wise corrected, and every 'validated' verdict must clear the full gate.
They read the committed data/edge_battery.json (the receipts) plus the frozen module constants.

Run: python3 -m pytest -q tests/test_edge_battery.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BATTERY = ROOT / "data" / "edge_battery.json"


def _load():
    assert BATTERY.exists(), "run: python3 src/edge_battery.py"
    return json.loads(BATTERY.read_text())


def test_eb1_pre_registration_is_fixed():
    """The hypothesis set is frozen in code (the pre-registration), not chosen after seeing results."""
    import edge_battery as EB
    import domain_conditioning as DC
    # 7 apt conditioners (4 + WS-S credit/real-rate + UCDP conflict-intensity) + 4 prior domain tests
    # + 2 event-type = 13.
    assert len(EB.CONDITIONING) == 7
    assert len(DC.HYPOTHESES) == 4
    r = _load()
    assert r["family_size"] == 13
    assert len(r["amplification"]) == 13


def test_eb2_family_wise_correction_applied():
    """Every testable hypothesis carries a family-wise FDR q AND a Bonferroni verdict -- the honest
    multiple-comparisons accounting across the whole family, not per-test."""
    r = _load()
    assert "fdr" in r and "bonferroni" in r
    for x in r["amplification"]:
        if x.get("testable"):
            assert "fdr_q" in x and "survives_fdr" in x
            assert "survives_bonferroni" in x


def test_eb3_validated_clears_the_full_gate():
    """'validated' implies CI excludes zero AND predicted direction AND survives family FDR AND
    survives leave-one-cluster-out robustness. No shortcut to a claim."""
    r = _load()
    for x in r["amplification"]:
        if x.get("validated"):
            lo, hi = x["ci"]
            assert lo is not None and (lo > 0 or hi < 0)     # CI excludes zero
            assert x["amp"] > 0                              # predicted direction (sign folded in)
            assert x["survives_fdr"] is True
            assert x.get("robustness", {}).get("robust") is True


def test_eb4_nulls_are_reported_not_hidden():
    """The scorecard shows nulls -- the point of the battery. At least one testable null must be present
    (a battery where everything 'passes' would be the p-hacking this engine refuses)."""
    r = _load()
    testable = [x for x in r["amplification"] if x.get("testable")]
    assert len(testable) >= 8
    assert any(not x.get("validated") for x in testable)


def test_eb5_mispricing_is_suggestive_never_validated():
    """The mispricing edge is small-N and in-sample by construction -- reported, but never 'validated'."""
    r = _load()
    m = r["mispricing"]
    assert m.get("verdict") == "suggestive"
    assert m.get("validated") is not True
    # it must NOT be in the amplification FDR family (different statistic)
    assert "under_priced_risk_oos" not in [a["hypothesis"] for a in r["amplification"]]


def test_eb6_exclusions_declared_and_conditioners_distinct():
    """Honest exclusions are named (not force-fit) and the conditioners are shown to be distinct
    drivers, not one collinear proxy for VIX."""
    r = _load()
    for key in ("natural_gas", "wheat"):           # credit was un-capped (WS-S) -> no longer excluded
        assert key in r["exclusions"]
    assert "hy_credit" not in r["exclusions"]       # now a tested hypothesis, not an exclusion
    assert r["collinearity"]["abs_max"] < 0.6      # distinct economic drivers, not VIX in disguise
