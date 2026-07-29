"""
test_step4.py -- the kNN probability function's gate proves itself (Step 4).

Checks the walk-forward gate is coherent and, critically, that the de-overlapped (clustered)
sample is the one that governs the verdict -- the guard that stopped a clustering-artifact
"edge" from being shipped. Run: python3 -m pytest -q tests/test_step4.py
"""

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "oil.db"


def test_s4_gate_governed_by_clustered_sample():
    import probability
    conn = sqlite3.connect(DB)
    probability.build_library(conn)
    r = probability.backtest(conn)
    conn.close()
    # both samples scored; clustering strictly reduces N (overlapping episodes collapsed)
    assert r["clustered"]["n_scored"] > 0 and r["all_events"]["n_scored"] > 0
    assert r["clustered"]["n_scored"] < r["all_events"]["n_scored"]
    # the top-level verdict is the CLUSTERED gate, never the naive all-events one
    assert r["gate_passes"] == r["clustered"]["gate_passes"]
    # each gate carries the anti-overfitting receipts
    for g in (r["clustered"], r["all_events"]):
        assert "pbo" in g and "diebold_mariano" in g and "skill_vs_base" in g
