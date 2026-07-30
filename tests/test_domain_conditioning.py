"""
test_domain_conditioning.py -- apt, pre-declared conditioning (Whole-3).

The hypotheses are fixed in the module (pre-registration); each is gated + FDR-corrected; validated
requires CI-excludes-zero AND FDR survival. Run: python3 -m pytest -q tests/test_domain_conditioning.py
"""


def test_dc1_predeclared_and_gated():
    import domain_conditioning as D
    # the hypothesis set is fixed in code (the pre-registration) -- not chosen after seeing results
    assert len(D.HYPOTHESES) == 4
    r = D.run()
    for x in r["results"]:
        if "amp" in x:
            # 'validated' implies CI excludes zero (a real effect), never asserted on a spanning CI
            if x.get("validated"):
                lo, hi = x["ci"]
                assert lo is not None and (lo > 0 or hi < 0)
    # wheat is honestly excluded (no clean market-state proxy), not force-fit
    assert "wheat" in r["note"].lower()


def test_dc2_copper_finds_its_apt_driver():
    import domain_conditioning as D
    r = D.run()
    copper = next(x for x in r["results"] if x["hypothesis"] == "copper_growth")
    # copper was null under generic stress; under its apt growth-regime driver it validates
    assert copper.get("validated") is True and copper["ci"][0] > 0
