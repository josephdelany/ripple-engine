import public_claim_guard as G


def test_authoritative_documents_match_frozen_summary():
    assert G.violations() == []


def test_uniform_qualification_is_numerically_correct():
    e = G.evidence()
    assert e["structure_uniform_ci"][0] < 0 < e["structure_uniform_ci"][1]
    assert e["structure_uniform_p"] > 0.05
    assert e["surface_uniform_difference"] > 0


def test_primary_comparison_is_numerically_correct():
    e = G.evidence()
    assert e["ci"][1] < 0
    assert e["p"] < 0.05
    assert e["structural"] < e["surface"]
