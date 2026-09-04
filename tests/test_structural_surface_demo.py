import structural_surface_demo as D


def test_demo_is_one_verified_frozen_read_and_never_the_average_evidence():
    d = D.load()
    assert d["event"]["event_id"] == "hormuz_closure_2026"
    assert d["score"]["read_hash"] == d["read"]["hash"]
    text = D.render()
    assert "single frozen historical read" in text
    assert "all 264 inferential dates" in text
    assert "not from this example" in text
    assert "**uniform pooling** scored best overall" in text


def test_demo_arms_have_identical_candidates_and_forecast_atoms():
    d = D.load()
    r = d["read"]
    assert len(r["candidate_ids"]) == len(r["forecasts"]["20"]["abnormal_atoms"])
    assert len(r["structural"]["weights"]) == len(r["candidate_ids"])
    assert len(r["surface"]["weights"]) == len(r["candidate_ids"])
