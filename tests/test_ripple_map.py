"""
test_ripple_map.py -- the conditioned ripple map / cross-asset generalization (Pillar 4).

Coherence: the map runs the H1 gate on every daily asset, oil (H1) generalizes, and every cell
carries a CI + permutation p + an FDR-derived verdict. Run: python3 -m pytest -q tests/test_ripple_map.py
"""


def test_r1_map_coherent_and_oil_generalizes():
    import cross_asset_conditioned as X
    r = X.run()
    assert r["n_assets"] >= 3
    labels = {c["label"] for c in r["map"]}
    assert "Brent oil" in labels
    # oil (H1) must generalize within the map -- it's the validated edge, same gate
    oil = next(c for c in r["map"] if c["label"] == "Brent oil")
    assert oil["generalizes"] is True and oil["ci_excludes_zero"] is True
    # every cell carries the receipts, and 'generalizes' implies CI-excludes-zero AND FDR-survival
    for c in r["map"]:
        assert "ci95" in c and "perm_p" in c and "survives_fdr" in c
        if c["generalizes"]:
            assert c["ci_excludes_zero"] and c["survives_fdr"]
    # oil should be among the generalizing assets in the summary
    assert "Brent oil" in r["assets_generalizing"]
