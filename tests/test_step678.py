"""
test_step678.py -- local projections (6), nowcast Kalman (7), signal registry (8).

Hand-verifiable Kalman arithmetic + coherence checks that the honest tiering falls out of the
validation artifacts. Run: python3 -m pytest -q tests/test_step678.py
"""

import numpy as np


# --- Step 7: Kalman local-level, hand-computed ---
# k1 -- one update from prior N(0,1), obs=10, obs_var=1, process_var=0:
# pred_var = 1+0 = 1; gain = 1/(1+1) = 0.5; post_mean = 0 + 0.5*(10-0) = 5; post_var = 0.5.
def test_k1_kalman_step_by_hand():
    from nowcast import kalman_step
    m, v, g = kalman_step(0.0, 1.0, 10.0, 1.0, 0.0)
    assert abs(m - 5.0) < 1e-9 and abs(v - 0.5) < 1e-9 and abs(g - 0.5) < 1e-9


# k2 -- on a constant series the one-step-ahead prediction converges to the constant.
def test_k2_kalman_tracks_constant():
    from nowcast import kalman_filter
    z = np.full(50, 7.0)
    pm, pv = kalman_filter(z, process_var=1.0, obs_var=1.0)
    assert abs(pm[-1] - 7.0) < 1e-6


# k3 -- the nowcast backtest is coherent: coverage is a probability and the verdict is honest
# (gate passes only if calibrated AND it beats persistence).
def test_k3_nowcast_backtest_coherent():
    import sqlite3, nowcast
    from pathlib import Path
    conn = sqlite3.connect(Path(nowcast.DB))
    r = nowcast.backtest(conn, nowcast.DEFAULT_SERIES)
    conn.close()
    assert 0.0 <= r["ci68_coverage"] <= 1.0
    assert r["gate_passes"] == (r["coverage_in_band"] and r["beats_persistence"])


# --- Step 6: local-projection IRF + pooling ---
# lp1 -- the IRF reports all four horizons, each raw slope carries a bootstrap CI, and the
# partial-pooled per-type amp sits between the raw estimate and the grand mean (shrinkage).
def test_lp1_irf_and_pooling():
    import local_projections
    r = local_projections.run()
    assert [x["horizon"] for x in r["irf"]] == [1, 5, 10, 20]
    assert all(x["raw_pp_per_sd"] and "lo" in x["raw_pp_per_sd"] for x in r["irf"])
    pool = r["pooling"]["by_type"]; grand = r["pooling"]["grand_mean_pp"]
    for t, s in pool.items():
        lo, hi = sorted([s["raw_amp_pp"], grand])
        assert lo - 1e-6 <= s["pooled_amp_pp"] <= hi + 1e-6    # shrunk toward the grand mean


# --- Step 8: signal registry ---
# sr1 -- status is DERIVED: H1 is the one live edge; H2/H3/analogue/kNN/nowcast are rejected;
# and H1's 'live' matches its statistically_validated flag in the claims artifact.
def test_sr1_registry_tiering_is_derived():
    import signal_registry, json
    r = signal_registry.build()
    by = r["by_status"]
    # H1 was downgraded under the single evidentiary bar (data/evidentiary_bar.json,
    # docs/red_team_1.md R7) and the registry now tiers it as retracted. This assertion used to
    # require it to be LIVE, which made a green suite depend on carrying a retracted claim.
    assert "h1_vix_conditioning" in by["retracted"]
    assert "h1_vix_conditioning" not in by["live"]
    for null_sig in ("h2_conditioning", "h3_conditioning", "analogue_turbulence",
                     "knn_state_probability"):
        assert null_sig in by["rejected"]
    vc = {h["hid"]: h for h in json.loads(
        (signal_registry.DATA / "validation_claims.json").read_text())["hypotheses"]}
    h1_live = "h1_vix_conditioning" in by["live"]
    assert h1_live == bool(vc["H1"]["statistically_validated"])
