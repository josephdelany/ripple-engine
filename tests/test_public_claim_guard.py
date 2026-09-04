import public_claim_guard as G


def test_authoritative_documents_match_frozen_summary():
    assert G.violations() == []


def test_guard_rejects_a_superseded_value_present_alongside_the_current_one(monkeypatch):
    """The failure mode this guard exists to catch, and the one it could NOT catch before 2026-09-03.

    `violations()` was a presence test: it asked whether the current figures appear, never whether a
    corrected-away figure had survived beside them. A README carrying both 8.341 and a leftover 8.337
    passed. That is how the off-by-one in the central target (07b760c, c2dacc4) could have shipped."""
    real = G.text()
    poisoned = dict(real)
    name = "README.md"
    poisoned[name] = real[name] + "\n\nStructural CRPS was 8.337 in an earlier cut.\n"
    monkeypatch.setattr(G, "text", lambda: poisoned)
    problems = G.violations()
    assert any("8.337" in p and "superseded" in p for p in problems), problems
    assert any(f"{name}:" in p for p in problems), "the offending file and line must be named"


def test_guard_covers_submission_status():
    """SUBMISSION_STATUS.md restates the whole result set and decides whether the product is releasable,
    yet it was outside the guard until 2026-09-03."""
    assert any(p.name == "SUBMISSION_STATUS.md" for p in G.PUBLIC)
    assert "SUBMISSION_STATUS.md" in G.text()


def test_guard_checks_p_values_and_intervals(monkeypatch):
    """The interval bounds and p-values are the most quotable figures in the paper and were untested."""
    e = G.evidence()
    real = G.text()
    for probe in (f"{e['ci'][0]:.3f}", f"{e['structure_uniform_p']:.3f}"):
        stripped = {k: v.replace(probe, "REMOVED").replace(probe.replace("-", "−"), "REMOVED")
                    for k, v in real.items()}
        monkeypatch.setattr(G, "text", lambda s=stripped: s)
        assert any("missing frozen values" in p for p in G.violations()), \
            f"removing {probe} from every public document must be caught"


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
