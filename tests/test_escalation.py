"""Unit tests for Layer G (escalation.py) — A2/A3 discipline, both ways."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import escalation as E


def _rec(eid, **kw):
    base = {"event_id": eid, "date": "2000-01-01", "type": "conflict_escalation",
            "title": eid, "actor": "country.a", "target": "country.b",
            "conflict_scope": "isolated", "tempo": "first", "diplomatic": "none",
            "alliance": "none", "target_capacity": "limited", "prior_dyad": "none",
            "propensity": 0.3, "outcome": "CONTAINED"}
    base.update(kw)
    return base


def test_similarity_bounds():
    a = _rec("a"); b = _rec("b")
    s, _ = E.similarity(a, b)
    assert s == 1.0                       # identical geo blocks -> 1.0
    c = _rec("c", actor="country.x", target="country.y", conflict_scope="war",
             tempo="nth", target_capacity="significant", propensity=0.9,
             diplomatic="talks", alliance="military", prior_dyad="WIDENING")
    s2, _ = E.similarity(a, c)
    assert s2 < 0.3                       # disjoint geo blocks -> low


def test_branch_rates():
    recs = [_rec(f"e{i}", outcome="CONTAINED") for i in range(6)] + \
           [_rec(f"w{i}", outcome="WIDENING") for i in range(4)]
    br = E.branch_rates(recs)
    assert br["n"] == 10
    assert br["rates"]["CONTAINED"] == 0.6 and br["rates"]["WIDENING"] == 0.4


def test_no_adequate_precedent_fires():
    # target whose geo block is entirely unknown -> similarity 0 to everyone -> no precedent
    target = _rec("t", actor="unknown", target="unknown", conflict_scope="unknown",
                  tempo="unknown", diplomatic="unknown", alliance="unknown",
                  target_capacity="unknown", prior_dyad="unknown", propensity=None, type="x")
    pool = [_rec(f"p{i}") for i in range(20)]
    out = E.read(None, target, pool=pool)
    assert out["no_adequate_precedent"] is True
    assert out["max_similarity"] < E.RETRIEVE_MIN


def test_conditioned_vs_fallback_both_ways():
    target = _rec("t")
    # 10 near-identical analogs -> conditioned class used (n>=8), not thin
    rich = [_rec(f"a{i}") for i in range(10)]
    out_rich = E.read(None, target, pool=rich)
    assert out_rich["no_adequate_precedent"] is False
    assert out_rich["branch_rates"]["thin"] is False
    assert out_rich["branch_rates"]["basis"] == "conditioned"
    # only 3 similar (>=COND_SIM) but a same-type parent exists -> fallback + thin flag
    thin_pool = [_rec(f"s{i}") for i in range(3)] + \
        [_rec(f"d{i}", actor="country.x", target="country.y", conflict_scope="war",
              tempo="nth", target_capacity="significant", propensity=0.95,
              diplomatic="talks", alliance="military", prior_dyad="WIDENING") for i in range(9)]
    out_thin = E.read(None, target, pool=thin_pool)
    assert out_thin["branch_rates"]["thin"] is True
    assert out_thin["branch_rates"]["basis"].startswith("fallback")
