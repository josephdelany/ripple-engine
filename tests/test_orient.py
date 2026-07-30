"""
test_orient.py -- the read-support brief is honest raw material (tiered, receipted, gaps shown).

orient() must resolve topics, only ever label validated items as claims, always surface the coverage
gaps (so a writer can't over-claim), and give a receipts index. It must NEVER contain prose/opinion.
Run: python3 -m pytest -q tests/test_orient.py
"""

import orient as O


def test_or1_resolves_topics():
    assert O._resolve("middle east") == "me-risk"
    assert O._resolve("iran") == "me-risk"
    assert O._resolve("shipping") == "supply-chain"
    assert O._resolve("commodities") == "commodities"


def test_or2_brief_is_tiered_raw_material():
    r = O.orient("middle east")
    assert r["ok"] is True and r["domain"] == "me-risk"
    # every validated edge is labelled a claim and has a receipt id
    for e in r["validated_edges"]:
        assert e["tier"] == "validated"
        assert e["node"] in r["receipts_index"]
    # coverage gaps are always present (the negative space a writer must respect)
    assert "gaps_in_coverage" in r
    assert "underpowered_event_types" in r["gaps_in_coverage"]
    # discipline statement makes clear the engine gives material, not the read
    assert "you write the read" in r["discipline"].lower()


def test_or3_unknown_topic_falls_back_not_crashes():
    r = O.orient("something random xyz")
    assert r["ok"] is True                         # falls back to a default domain, never errors
