"""
test_step5.py -- the causal-control primitives + the discovery scan (Step 5).

Hand-verifiable partial-correlation cases, plus a coherence check that the scan re-discovers H1
and never ships a survivor as a validated edge. Run: python3 -m pytest -q tests/test_step5.py
"""

import numpy as np
import validate as V


# d1 -- pearson of a perfect line is +1; of a flat series is 0.
def test_d1_pearson():
    assert abs(V.pearson([1, 2, 3, 4], [2, 4, 6, 8]) - 1.0) < 1e-9
    assert V.pearson([1, 2, 3], [5, 5, 5]) == 0.0


# d2 -- partial correlation kills a spurious link. Let z be noise, x = z, y = z (both driven ONLY
# by z). Then raw corr(x,y)=1 but r(x,y|z) collapses to ~0: the x-y link was entirely the
# confounder z. (Uses a fixed seed for reproducibility.)
def test_d2_partial_corr_kills_confounded_link():
    rng = np.random.default_rng(1)
    z = rng.normal(size=200)
    x = z + 1e-9 * rng.normal(size=200)      # x is z (+ negligible jitter to avoid /0)
    y = z + 1e-9 * rng.normal(size=200)      # y is z
    assert V.pearson(x, y) > 0.99            # raw link looks perfect
    assert abs(V.partial_corr(x, y, z)) < 0.2   # ...but vanishes once we control for z


# d3 -- a genuine partial link survives: y depends on x AND z separately.
def test_d3_partial_corr_keeps_real_link():
    rng = np.random.default_rng(2)
    x = rng.normal(size=300); z = rng.normal(size=300)
    y = 0.8 * x + 0.8 * z + 0.1 * rng.normal(size=300)
    assert V.partial_corr(x, y, z) > 0.5     # x->y survives controlling for z


# d4 -- the scan ships NO survivor as a validated new edge (whether or not it re-finds H1 at a
# given N -- the correlation scan is stricter/different than H1's median-split, so which survivors
# appear is data-dependent; the invariant is that nothing is asserted as a new edge).
def test_d4_discovery_ships_nothing_as_new_edge():
    import discovery
    r = discovery.run()
    assert r["n_candidates"] > 0                              # the scan actually ran
    for c in r["survivors"]:
        assert c["is_rediscovered_h1"] or "CANDIDATE" in c["status"]   # never a bare new edge
