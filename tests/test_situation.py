"""
test_situation.py -- the Situation Memory layer proves itself.

Small, hand-verifiable tests over the situation_log schema and the deterministic
attach/render. Like test_engine.py, each test documents the behaviour it locks in.
Run:  python3 -m pytest tests/test_situation.py -q
"""

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
sys.path.insert(0, str(ROOT / "src"))

# The situation_log DDL, lifted from init_db.SCHEMA, for isolated temp-DB tests.
# FKs are off by default in SQLite, so we don't need to seed entities here.
_SITUATION_LOG_DDL = """
CREATE TABLE situation_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    situation_id TEXT NOT NULL, ts TEXT NOT NULL, kind TEXT, actor_entity TEXT,
    headline TEXT NOT NULL, detail TEXT, source_url TEXT NOT NULL,
    retrieved_at TEXT NOT NULL, status TEXT NOT NULL, confidence TEXT,
    alert_url TEXT, promoted_event_id TEXT, UNIQUE (situation_id, source_url));
"""


def _temp_conn():
    conn = sqlite3.connect(":memory:")
    conn.executescript(_SITUATION_LOG_DDL)
    return conn


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


# s1 -- attach matches BOTH alert formats (GDELT country codes + RSS entity_ids)
# and is idempotent: a second run over the same alerts inserts 0 new rows.
def test_s1_attach_matches_both_formats_and_is_idempotent():
    import situation
    sit = [{"situation_id": "situation.test", "status": "active",
            "member_entities": ["country.iran", "chokepoint.hormuz"]}]
    alerts = [
        # GDELT-style: country code token -> matches via COUNTRY_CC[iran]=IRN.
        {"timestamp_utc": "2026-07-20T00:00:00", "headline": "IRGC clash",
         "url": "http://x/1", "matched_entities": "IRN", "status": "new"},
        # RSS-style: entity_id token -> matches directly.
        {"timestamp_utc": "2026-07-21T00:00:00", "headline": "Hormuz tanker",
         "url": "http://x/2", "matched_entities": "chokepoint.hormuz", "status": "new"},
        # Off-topic: neither token is in the situation -> must NOT attach.
        {"timestamp_utc": "2026-07-22T00:00:00", "headline": "Venezuela vote",
         "url": "http://x/3", "matched_entities": "VEN", "status": "new"},
        # Joe-dismissed noise -> must NOT attach even though it matches.
        {"timestamp_utc": "2026-07-23T00:00:00", "headline": "noise",
         "url": "http://x/4", "matched_entities": "IRN", "status": "dismissed"},
    ]
    conn = _temp_conn()
    first = situation.attach(conn, sit, alerts, "2026-07-27T00:00:00")
    assert first == 2, "only the two on-topic, non-dismissed alerts attach"
    second = situation.attach(conn, sit, alerts, "2026-07-27T00:00:00")
    assert second == 0, "re-running attaches nothing (idempotent)"
    # every atom is sourced and tagged observed/low, kind unmapped (agent's job).
    rows = conn.execute("SELECT source_url, retrieved_at, status, confidence, kind "
                        "FROM situation_log").fetchall()
    conn.close()
    assert len(rows) == 2
    for src, ret, status, conf, kind in rows:
        assert src and ret and status == "observed" and conf == "low"
        assert kind == "unmapped"
