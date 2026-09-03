"""Joe's Ruling 1 (data/gates/ripple_2026-09-02.md; EDGE_PORTFOLIO.md amendment 2026-09-02): the five
stress->node amplification edges are retracted, no surface calls them validated, palladium is recorded but is
not a finding, and a REBUILD of propagation_edges cannot silently undo any of it. DB-free: the rebuild path is
exercised on rows, and the committed artifacts are read as files."""
import json
import os
import sys

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
import propagation_graph as PG

FIVE = {"amp.Brent oil", "amp.Heating oil", "amp.5Y breakeven", "amp.S&P 500", "amp.Platinum"}


def test_ruling1_the_registered_set_is_exactly_the_five():
    assert PG.RETRACTED_EDGE_IDS == FIVE
    assert PG.RETRACTED_STATUS == "retracted_h1_retest"
    for token in ("retraction_six.json", "red_team_1.md", "Ruling 1"):
        assert token in PG.RETRACTED_POINTER


def test_ruling1_a_rebuild_cannot_re_validate_them():
    """apply_ruling1 is the gate in the code that WRITES the table: whatever this run computed, the five come
    out retracted with the pointer, and palladium carries its note."""
    rows = [(f"amp.{n}", "stress->node", "geopolitical shock (VIX-stress regime)", n, "20d",
             9.9, 1.0, 18.0, None, "validated", f"under stress, a shock ripples harder into {n}")
            for n in ("Brent oil", "Heating oil", "5Y breakeven", "S&P 500", "Platinum", "Palladium", "Gold")]
    out = {r[0]: r for r in PG.apply_ruling1(rows)}
    for e in FIVE:
        assert out[e][9] == "retracted_h1_retest", e
        assert PG.RETRACTED_POINTER in out[e][10]
        assert out[e][5] == 9.9 and out[e][6] == 1.0 and out[e][7] == 18.0        # a status, not an erasure
    assert out["amp.Gold"][9] == "validated"                                       # nothing else is touched
    p = out["amp.Palladium"]
    assert p[9] == "validated" and "not on the oil chain" in p[10] and "noise looks like" in p[10]


def test_ruling1_no_surface_calls_the_five_validated():
    import sqlite3
    db = os.path.join(ROOT, "data", "oil.db")
    if os.path.exists(db):
        c = sqlite3.connect(db)
        rows = dict(c.execute("SELECT edge_id, status FROM propagation_edges WHERE kind='stress->node'"))
        for e in FIVE:
            assert rows.get(e) == "retracted_h1_retest", e
        assert c.execute("SELECT COUNT(*) FROM propagation_edges WHERE status='validated'").fetchone()[0] == 0
    g = json.load(open(os.path.join(ROOT, "data", "propagation_graph.json")))
    assert g["backbone_validated"] == []
    assert set(g["backbone_retracted_2026_09_02"]) == {e.split(".", 1)[1] for e in FIVE}
    ev = open(os.path.join(ROOT, "docs", "reference", "EVIDENCE.md"), encoding="utf-8").read()
    assert "Retracted 2026-09-02" in ev and "retracted_h1_retest" in ev
    for node in ("brent_oil", "platinum", "heating_oil", "5y_breakeven", "s&p_500"):
        card = json.load(open(os.path.join(ROOT, "data", "evidence", f"node.{node}.json")))
        assert card["tier"] == "RETRACTED" and card["retraction"]["edge_status"] == "retracted_h1_retest"
    pall = json.load(open(os.path.join(ROOT, "data", "evidence", "node.palladium.json")))
    assert pall["tier"] == "NOT_A_FINDING" and len(pall["not_a_finding"]["reasons"]) == 4
