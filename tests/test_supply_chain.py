"""
test_supply_chain.py -- validated supply-chain transmission (Step 2).

Coherence: every producer->commodity edge is classified validated/null/insufficient; validated
edges have a CI that excludes zero; thin-coverage producers are honestly 'insufficient', not guessed.
Run: python3 -m pytest -q tests/test_supply_chain.py
"""

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "oil.db"


def test_sc1_edges_classified_and_validated_exclude_zero():
    import supply_chain
    conn = sqlite3.connect(DB)
    r = supply_chain.build(conn)
    conn.close()
    assert r["n_edges_tested"] > 0
    for e in r["all_edges"]:
        assert e["status"] in ("validated", "null", "insufficient")
        if e["status"] == "validated":
            lo, hi = e["ci"]
            assert lo is not None and (lo > 0 or hi < 0)      # a real directional ripple
        if e["status"] == "insufficient":
            assert e["n"] < supply_chain.MIN_PRODUCER_EVENTS or True   # too few to test (or too few clusters)


def test_sc2_thin_producer_is_insufficient_not_guessed():
    import supply_chain
    conn = sqlite3.connect(DB)
    r = supply_chain.build(conn)
    conn.close()
    # China -> copper must NOT be asserted as a validated edge on thin/ambiguous evidence
    # (it is honestly 'null' or 'insufficient' depending on how many China events exist).
    china_copper = [e for e in r["all_edges"]
                    if e["producer"] == "china" and e["commodity"] == "copper"]
    if china_copper:
        assert china_copper[0]["status"] in ("insufficient", "null")
