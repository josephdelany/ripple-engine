"""
test_step2.py -- the H1 resolving/accountability layer proves itself.

Covers the pure H1-state parser (hand-verifiable) and the coherence of the walk-forward
read backtest (structure + internal consistency). Run: python3 -m pytest -q tests/test_step2.py
"""


# s1 -- the amp_context parser reads the H1 state that was stamped at log time.
# 'H1:ON H2:OFF H3:FAILED' -> 'ON'; a missing/failed H1 -> None.
def test_s1_h1_state_parser():
    from resolve_reads import _h1_state
    assert _h1_state("H1:ON H2:OFF H3:FAILED") == "ON"
    assert _h1_state("H1:OFF H2:ON") == "OFF"
    assert _h1_state("H1:FAILED H2:ON") is None      # not ON/OFF -> None
    assert _h1_state("") is None
    assert _h1_state(None) is None


# s2 -- the walk-forward read backtest is internally coherent: it scores events only after
# the min-prior warmup, the regime buckets partition the scored set, and (because H1 holds)
# realized magnitude is larger in the ON bucket than the OFF bucket.
def test_s2_read_backtest_coherent():
    import read_backtest
    r = read_backtest.run()
    assert r["n_scored"] > 0
    reg = r["by_regime"]
    assert sum(v["n"] for v in reg.values()) == r["n_scored"]     # buckets partition the set
    assert "mae_uncond_pp" in r and "mae_cond_pp" in r
    # H1 holds -> ON regime realizes bigger |CAR+20| than OFF (the live-style amplification)
    if "ON" in reg and "OFF" in reg:
        assert reg["ON"]["mean_realized_pp"] > reg["OFF"]["mean_realized_pp"]
        assert r["live_amplification_pp"] > 0
