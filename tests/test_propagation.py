"""
test_propagation.py -- the validated propagation graph (Step 2).

Coherence: the graph builds three honest layers, the backbone is validated (CI excludes zero),
node->node edges are classified, and the table persists. Run: python3 -m pytest -q tests/test_propagation.py
"""

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "oil.db"


def test_p1_graph_layers_and_backbone():
    import propagation_graph as P
    conn = sqlite3.connect(DB)
    r = P.build(conn)
    # count only THIS module's kinds (supply_chain.py shares the table with kind='supplychain')
    n_table = conn.execute("SELECT COUNT(*) FROM propagation_edges WHERE kind IN "
                           "('stress->node','event->node','node->node')").fetchone()[0]
    conn.close()
    assert r["n_edges"] == n_table and r["n_edges"] > 0

    # backbone edges are all validated with a CI that excludes zero
    for e in r["backbone_validated"]:
        assert e["status"] == "validated"
        lo, hi = e["ci"]
        assert lo is not None and (lo > 0 or hi < 0)
    # Joe's Ruling 1 (2026-09-02, EDGE_PORTFOLIO.md amendment): the five stress->node edges that made up the
    # backbone -- Brent among them -- were RETRACTED after session C's registered re-test returned NULL for
    # every one. The anchor assertion is therefore inverted: Brent must NOT be in the validated backbone, must
    # be named in the retracted list, and must carry the retracted status in the table it was just written to.
    import propagation_graph as PG
    assert r["backbone_validated"] == []
    assert set(r["backbone_retracted_2026_09_02"]) == {e.split(".", 1)[1] for e in PG.RETRACTED_EDGE_IDS}
    assert "Brent oil" in r["backbone_retracted_2026_09_02"]
    conn2 = sqlite3.connect(DB)
    statuses = dict(conn2.execute("SELECT edge_id, status FROM propagation_edges WHERE kind='stress->node'"))
    conn2.close()
    for e in PG.RETRACTED_EDGE_IDS:
        assert statuses[e] == PG.RETRACTED_STATUS, e


def test_p2_node_edges_classified_and_traps_honest():
    import propagation_graph as P
    conn = sqlite3.connect(DB)
    r = P.build(conn)
    conn.close()
    for e in r["node_to_node"]:
        assert e["status_pre_fdr"] in ("validated", "trap", "null")
        # a 'trap' must genuinely co-move (|contemp|>=0.2) yet not lead
        if e["status_pre_fdr"] == "trap":
            assert abs(e["contemp_corr"]) >= 0.2
