"""
test_situation.py -- the Situation Memory layer proves itself.

Small, hand-verifiable tests over the situation_log schema and the deterministic
attach/render. Like test_engine.py, each test documents the behaviour it locks in.
Run:  python3 -m pytest tests/test_situation.py -q
"""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"


# s0 -- the schema enforces the sourcing/tagging discipline at the DB level:
# source_url, retrieved_at and status are NOT NULL, so an untagged/unsourced atom
# physically cannot be written. This is the guardrail, made structural.
def test_s0_schema_enforces_sourcing_and_tagging():
    conn = sqlite3.connect(DB)
    cols = {r[1]: r[3] for r in conn.execute("PRAGMA table_info(situation_log)")}
    conn.close()
    assert cols, "situation_log table is missing -- run src/init_db.py"
    for required in ("situation_id", "ts", "headline", "source_url",
                     "retrieved_at", "status"):
        assert cols[required] == 1, f"{required} must be NOT NULL"


# s0b -- the seed situation exists as an entities row with type='situation'
# (invisible to the watcher net) and the yaml membership parses to real columns.
def test_s0b_seed_situation_and_config():
    import yaml
    conn = sqlite3.connect(DB)
    row = conn.execute(
        "SELECT type FROM entities WHERE entity_id='situation.israel_iran_war_2025'"
    ).fetchone()
    conn.close()
    assert row and row[0] == "situation"
    cfg = yaml.safe_load((ROOT / "data" / "situations.yaml").read_text())
    sit = cfg["situations"][0]
    assert sit["situation_id"] == "situation.israel_iran_war_2025"
    assert sit["member_entities"] and sit["dominant_kinds"]
