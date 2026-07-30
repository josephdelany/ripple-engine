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
    n_table = conn.execute("SELECT COUNT(*) FROM propagation_edges").fetchone()[0]
    conn.close()
    assert r["n_edges"] == n_table and r["n_edges"] > 0

    # backbone edges are all validated with a CI that excludes zero
    for e in r["backbone_validated"]:
        assert e["status"] == "validated"
        lo, hi = e["ci"]
        assert lo is not None and (lo > 0 or hi < 0)
    # oil is in the validated backbone (H1) -- the anchor
    assert any(e["to"] == "Brent oil" for e in r["backbone_validated"])


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
