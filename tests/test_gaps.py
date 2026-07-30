"""
test_gaps.py -- the Gap object + resolving ledger (Pillar 1).

Coherence checks: gaps build and persist, the ledger scores with honest small-N CIs, and a live
(unresolved) gap is always present. Run: python3 -m pytest -q tests/test_gaps.py
"""

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "data" / "oil.db"


def test_g1_gaps_build_and_ledger_coherent():
    import gaps
    conn = sqlite3.connect(DB)
    rows = gaps.build(conn)
    n_table = conn.execute("SELECT COUNT(*) FROM gaps").fetchone()[0]
    conn.close()
    assert len(rows) == n_table and len(rows) > 0          # persisted what it built

    led = gaps.ledger(rows)
    assert led["n_scored"] > 0
    assert 0.0 <= led["turbulence_base_rate"] <= 1.0
    # every populated gap-direction group carries a valid rate inside a valid Wilson CI
    for g in led["by_gap_direction"].values():
        if g:
            lo, hi = g["turbulence_rate_ci95"]
            assert 0.0 <= lo <= g["turbulence_rate"] <= hi <= 1.0
            assert g["n"] >= 1


def test_g2_live_gap_present_and_typed():
    import gaps
    conn = sqlite3.connect(DB)
    rows = gaps.build(conn)
    conn.close()
    live = [r for r in rows if r["gap_id"] == "gap.LIVE"]
    assert len(live) == 1
    assert live[0]["gap_direction"] in ("under_priced_risk", "over_priced_fear", "aligned")
    assert live[0]["outcome"] is None                      # live gap is unresolved by definition
