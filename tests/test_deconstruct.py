"""
test_deconstruct.py -- article deconstruction binds every claim to MEASURED evidence and
renders each verdict by the numbers, never a generated opinion (the quant engine rules).

Integration test (reads oil.db); conftest skips it on a DB-less checkout.
Run: python3 -m pytest -q tests/test_deconstruct.py
"""

from fastapi.testclient import TestClient

import deconstruct as D
import backend

client = TestClient(backend.app)

BESSENT = ("Treasury Secretary Scott Bessent announced an economic D-Day sanctions plan targeting "
           "Iran and its trade partners. The plan will cut Iran oil exports. Iran could retaliate by "
           "threatening the Strait of Hormuz.")


def test_dc1_claims_bound_to_measured_evidence():
    d = D.deconstruct(BESSENT)
    assert d["n_claims"] >= 2
    for c in d["claims"]:
        assert c["verdict"] and c["verdict"]["text"]
        if c["event_class"]:
            assert c["evidence"] and c["evidence"]["n"] > 0        # measured history attached


def test_dc2_dominant_is_the_topic_not_a_side_mention():
    """Sanctions article that mentions Hormuz once in a retaliation clause must be dominated by
    'sanctions', not the priority-ordered chokepoint side-mention."""
    assert D.deconstruct(BESSENT)["dominant_class"] == "sanctions"


def test_dc3_verdict_stances_are_measured_labels():
    allowed = {"material", "in_line", "insufficient", "no_class"}
    for c in D.deconstruct(BESSENT)["claims"]:
        assert c["verdict"]["stance"] in allowed


def test_dc7_no_verdict_calls_a_fat_tailed_class_ordinary_without_the_tail():
    """The reviewer's honesty gate: an 'in_line' verdict must still cite the class tail (never
    say 'ordinary' while hiding a large worst-case precedent)."""
    for c in D.deconstruct(BESSENT)["claims"]:
        v = c["verdict"]
        if v["stance"] == "in_line" and c.get("evidence"):
            assert "fat-tailed" in v["text"] or "worst case" in v["text"]


def test_dc8_hypothetical_clause_is_flagged():
    """A conditional retaliation clause is answered 'if it occurs', not as an event."""
    d = D.deconstruct(BESSENT)
    hypo = [c for c in d["claims"] if c.get("modality") == "hypothetical"]
    for c in hypo:
        if c.get("evidence"):
            assert c["verdict"]["text"].lower().startswith("if it occurs")


def test_dc4_opinion_vs_fact_detected():
    op = D.article_type("I believe we must act. In my view the government should never allow this. "
                        "Frankly, the truth is that we ought to respond. I argue for immediate action.")
    assert op["type"] == "opinion"
    fact = D.article_type("The central bank raised rates by 25 basis points on Wednesday, citing "
                          "persistent inflation and a tight labor market.")
    assert fact["type"] == "fact"


def test_dc5_verdicts_are_measured_not_opinionated():
    d = D.deconstruct(BESSENT)
    assert "measured" in d["discipline"].lower()
    for c in d["claims"]:
        if c["event_class"] and c["evidence"]:
            t = c["verdict"]["text"].lower()
            assert "history" in t or "median" in t                 # cites the record, not a view


def test_dc6_endpoint_serves_and_empty_is_a_documented_gap():
    r = client.post("/wb_deconstruct", json={"text": BESSENT})
    assert r.status_code == 200 and r.json()["n_claims"] >= 2
    assert client.post("/wb_deconstruct", json={"text": "   "}).json().get("error")
