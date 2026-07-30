"""
test_corroboration.py -- the cross-modal confidence layer (Pillar 3).

Hand-verifiable: cross-modal votes add independence and raise confidence; the priced modality is
a distinct evidence class; multi-modal means confirmed beyond headlines.
Run: python3 -m pytest -q tests/test_corroboration.py
"""

import corroborate as C


# c1 -- more independent evidence -> higher confidence, monotone, capped below certainty.
def test_c1_score_monotone_and_capped():
    p1 = C.score(1)[1]; p3 = C.score(3)[1]; p6 = C.score(8)[1]
    assert p1 < p3 < p6
    assert p6 <= C.DEFAULT_WEIGHTS["cap_prob"] + 1e-9      # never claims certainty


# c2 -- the priced modality fires when a repriced market names the same subject as the cluster.
def test_c2_priced_hit_matches_subject():
    cluster = [{"headline": "Tankers divert as Hormuz tensions spike"}]
    movers = [{"market": "Will the Strait of Hormuz close in 2026?", "move": 0.12}]
    assert C._priced_hit(cluster, movers) is not None
    # ...and does NOT fire on an unrelated market
    assert C._priced_hit(cluster, [{"market": "Fed cuts rates in March?", "move": 0.2}]) is None


# c3 -- convergence_summary reports multi-modal counts and the modality classes of the top event.
def test_c3_convergence_summary():
    events = [
        {"headline": "A", "confidence": 0.8, "multi_modal": True,
         "modality_classes": ["news", "physical", "priced"], "n_modality_classes": 3},
        {"headline": "B", "confidence": 0.4, "multi_modal": False,
         "modality_classes": ["news"], "n_modality_classes": 1},
    ]
    s = C.convergence_summary(events)
    assert s["n_events"] == 2 and s["n_multi_modal"] == 1
    assert s["max_modality_classes"] == 3
    assert s["top"]["modality_classes"] == ["news", "physical", "priced"]
