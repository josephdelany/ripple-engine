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


_READS_DDL = """
CREATE TABLE reads (
    read_id INTEGER PRIMARY KEY AUTOINCREMENT, made_at TEXT NOT NULL,
    situation_id TEXT, kind TEXT NOT NULL, anchor_date TEXT NOT NULL,
    anchor_series TEXT NOT NULL, anchor_value REAL, horizon_days INTEGER NOT NULL,
    expected_car REAL NOT NULL, basis TEXT, amp_context TEXT, resolved_at TEXT,
    realized_car REAL, error REAL, notes TEXT);
CREATE TABLE observations (series_id TEXT, obs_date TEXT, value REAL, as_of TEXT);
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
        assert kind == "unmapped"      # no heuristic_type on these fixtures


# s1b -- the watcher's heuristic_type flows into `kind` deterministically (a
# labelled hint, no LLM), and a later re-run backfills any legacy 'unmapped' row.
def test_s1b_heuristic_type_becomes_kind():
    import situation
    sit = [{"situation_id": "situation.test", "status": "active",
            "member_entities": ["country.iran"]}]
    typed = [{"timestamp_utc": "2026-07-20T00:00:00", "headline": "Hormuz strike",
              "url": "http://x/9", "matched_entities": "IRN",
              "heuristic_type": "chokepoint_disruption", "status": "new"}]
    conn = _temp_conn()
    situation.attach(conn, sit, typed, "2026-07-27T00:00:00")
    kind = conn.execute("SELECT kind FROM situation_log").fetchone()[0]
    assert kind == "chokepoint_disruption"
    # Simulate a legacy 'unmapped' row, then re-attach: it must be backfilled.
    conn.execute("UPDATE situation_log SET kind='unmapped'")
    situation.attach(conn, sit, typed, "2026-07-27T00:00:00")
    assert conn.execute("SELECT kind FROM situation_log").fetchone()[0] == \
        "chokepoint_disruption"
    conn.close()


# s2 -- the dossier renders deterministically: it shows the synthesis-pending
# marker (never fabricated prose), the priced-state numbers copied verbatim from
# engine_read (no new metric), a base-rate row per dominant kind, and a sourced
# link for every timeline atom.
def test_s2_render_is_deterministic_and_sourced():
    import situation
    sit = {"situation_id": "situation.test", "title": "Test War",
           "status": "active", "started_at": "2025-06-13",
           "member_entities": ["country.iran"],
           "dominant_kinds": ["conflict_escalation", "chokepoint_disruption"]}
    # a canned engine_read: render must echo THESE numbers, invent none.
    er = {"as_of": "2026-07-24", "read": "primed but stressed.",
          "hypotheses": {"H1": {"label": "Market stress", "amplifier": "ON",
                                "latest": 54.93, "event_median": 45.94}},
          "gpr_context": {"gpr_pct": 94.8, "gpr_value": 195.9},
          "base_rates": [
              {"type": "conflict_escalation", "n": 15, "car1": -0.7, "car5": 1.5,
               "car10": -0.6, "car20": -2.2},
              {"type": "chokepoint_disruption", "n": 3, "car1": 0.1, "car5": -1.0,
               "car10": -3.0, "car20": -7.5}]}
    conn = _temp_conn()
    # observations table for the Brent lookup + one sourced atom.
    conn.execute("CREATE TABLE observations (series_id TEXT, obs_date TEXT, "
                 "value REAL, as_of TEXT)")
    conn.execute("INSERT INTO observations VALUES "
                 "('fred.DCOILBRENTEU','2026-07-20',86.99,'2026-07-20')")
    conn.execute("INSERT INTO situation_log (situation_id, ts, kind, headline, "
                 "source_url, retrieved_at, status) VALUES "
                 "('situation.test','2026-07-27','unmapped','Abqaiq struck',"
                 "'http://src/abqaiq','2026-07-27','observed')")
    md = situation.render_dossier(conn, sit, er, "2026-07-27T00:00:00")
    conn.close()
    assert "synthesis (pending)" in md.lower()      # never fabricated prose
    assert "86.99" in md                             # Brent echoed verbatim
    assert "54.93" in md and "45.94" in md           # amplifier numbers verbatim
    assert "94.8" in md                              # GPR descriptive
    assert "| conflict_escalation | 15 |" in md      # base-rate row per kind
    assert "| chokepoint_disruption | 3 |" in md
    assert "http://src/abqaiq" in md                 # every atom sourced
    assert "not a forecast" in md.lower()             # the discipline caveat is on it


# ---- Slice 3b: the cage around the synthesizer agent -----------------------

def _agent_fixture(tmp_path, monkeypatch):
    """A temp DB (situation_log + observations + one atom) and a patched situation
    module so the agent validator runs in isolation from the live repo."""
    import situation
    conn = _temp_conn()
    conn.execute("CREATE TABLE observations (series_id TEXT, obs_date TEXT, "
                 "value REAL, as_of TEXT)")
    conn.execute("INSERT INTO observations VALUES "
                 "('fred.DCOILBRENTEU','2026-07-20',86.99,'2026-07-20')")
    conn.execute("INSERT INTO situation_log (situation_id, ts, kind, headline, "
                 "source_url, retrieved_at, status) VALUES "
                 "('situation.test','2026-07-27','unmapped','Abqaiq struck, 5pct "
                 "of supply','http://src/abqaiq','2026-07-27','observed')")
    conn.commit()
    sit = {"situation_id": "situation.test", "title": "Test War", "status": "active",
           "started_at": "2025-06-13", "member_entities": ["country.yemen"],
           "dominant_kinds": ["chokepoint_disruption"]}
    er = {"as_of": "2026-07-24", "read": "primed.", "hypotheses": {},
          "base_rates": [{"type": "chokepoint_disruption", "n": 3, "car1": 0.1,
                          "car5": -1.0, "car10": -3.0, "car20": -7.5}]}
    monkeypatch.setattr(situation, "load_situations", lambda: [sit])
    monkeypatch.setattr(situation, "load_engine_read", lambda: er)
    monkeypatch.setattr(situation, "DOSSIER_DIR", tmp_path)
    monkeypatch.setattr(situation, "ROOT", tmp_path)
    return conn


# s3a -- a CLEAN agent output applies: a valid typing refines the atom, and the
# synthesis (using only allowed numbers + words) is written as a tagged file.
def test_s3a_clean_agent_output_applies(tmp_path, monkeypatch):
    import apply_situation_agent as asa
    conn = _agent_fixture(tmp_path, monkeypatch)
    out = {"situation_id": "situation.test",
           "typings": [{"source_url": "http://src/abqaiq",
                        "kind": "infrastructure_attack",
                        "actor_entity": "country.yemen"}],
           "synthesis": "Abqaiq was struck (5pct of supply). History prices "
                        "chokepoint shocks near -7.5 at twenty days; Brent sits at "
                        "86.99. Direction, not a call.",
           "gaps": ["did Saudi flow resume?"]}
    res = asa.apply(out, conn)
    assert res["applied"] is True and res["typings_applied"] == 1
    row = conn.execute("SELECT kind, actor_entity, status FROM situation_log "
                       "WHERE source_url='http://src/abqaiq'").fetchone()
    assert row == ("infrastructure_attack", "country.yemen", "observed")
    assert (tmp_path / "situation.test.synthesis.md").exists()
    conn.close()


# s3b -- the fabrication guard bites: a synthesis with a number that is neither
# engine-computed nor in a sourced headline (here $120) is rejected, nothing writes.
def test_s3b_rejects_fabricated_number(tmp_path, monkeypatch):
    import apply_situation_agent as asa
    conn = _agent_fixture(tmp_path, monkeypatch)
    out = {"situation_id": "situation.test", "typings": [],
           "synthesis": "Brent is heading to 120 dollars imminently."}
    res = asa.apply(out, conn)
    assert res["applied"] is False
    assert any("fabrication" in e for e in res["errors"])
    assert not (tmp_path / "situation.test.synthesis.md").exists()
    conn.close()


# s3c -- closed-vocab guard: an out-of-vocab kind (or a non-member actor) is
# rejected before anything is written.
def test_s3c_rejects_out_of_vocab(tmp_path, monkeypatch):
    import apply_situation_agent as asa
    conn = _agent_fixture(tmp_path, monkeypatch)
    bad_kind = {"situation_id": "situation.test",
                "typings": [{"source_url": "http://src/abqaiq",
                             "kind": "alien_invasion", "actor_entity": None}],
                "synthesis": "words only."}
    r1 = asa.apply(bad_kind, conn)
    assert r1["applied"] is False and any("registered" in e for e in r1["errors"])
    bad_actor = {"situation_id": "situation.test",
                 "typings": [{"source_url": "http://src/abqaiq",
                              "kind": "infrastructure_attack",
                              "actor_entity": "country.narnia"}],
                 "synthesis": "words only."}
    r2 = asa.apply(bad_actor, conn)
    assert r2["applied"] is False and any("member" in e for e in r2["errors"])
    conn.close()


# ---- Wire 4: the record keeper (log -> resolve -> score) -------------------

# s4 -- resolution scores magnitude honestly: on a perfectly FLAT price series the
# abnormal return (CAR) is exactly 0, so a read that expected -7.5% resolves with
# error = 0 - (-7.5) = +7.5pp, and the calibration bias reflects it.
def test_s4_resolve_scores_magnitude_error():
    import sqlite3
    import pandas as pd
    import resolve_reads
    conn = sqlite3.connect(":memory:")
    conn.executescript(_READS_DDL)
    # 200 business days of flat Brent=100 -> log-returns 0 -> CAR 0.
    days = pd.bdate_range("2020-01-01", periods=200)
    conn.executemany("INSERT INTO observations VALUES ('fred.DCOILBRENTEU',?,?,?)",
                     [(d.strftime("%Y-%m-%d"), 100.0, d.strftime("%Y-%m-%d"))
                      for d in days])
    anchor = days[150].strftime("%Y-%m-%d")   # 150 days before, 49 after -> resolvable
    conn.execute("INSERT INTO reads (made_at, kind, anchor_date, anchor_series, "
                 "horizon_days, expected_car) VALUES "
                 "('2020-01-01','chokepoint_disruption',?, 'fred.DCOILBRENTEU', 20, -7.5)",
                 (anchor,))
    n = resolve_reads.resolve_pending(conn, now="2020-12-31T00:00:00")
    assert n == 1
    realized, error = conn.execute(
        "SELECT realized_car, error FROM reads WHERE read_id=1").fetchone()
    assert abs(realized) < 1e-6            # flat series -> zero abnormal return
    assert abs(error - 7.5) < 1e-6         # 0 - (-7.5) = +7.5pp
    cal = resolve_reads.calibration(conn)
    assert cal["n"] == 1 and abs(cal["overall"]["bias_pp"] - 7.5) < 1e-6
    conn.close()


# ---- Operating model: state round-trip (export -> rebuild -> import) --------

# s5 -- the durable memory survives a DB rebuild losslessly: export situation_log
# + reads to CSV, rebuild an empty DB, import, and every row (incl. NULLs) returns.
def test_s5_state_roundtrip_is_lossless(tmp_path, monkeypatch):
    import sqlite3
    import export_state
    import import_state
    monkeypatch.setattr(export_state, "STATE", tmp_path)
    monkeypatch.setattr(import_state, "STATE", tmp_path)

    src = sqlite3.connect(":memory:")
    src.executescript(_SITUATION_LOG_DDL + _READS_DDL)
    # one full row + one with NULL actor/detail/promoted -> tests NULL round-trip.
    src.execute("INSERT INTO situation_log (situation_id, ts, kind, actor_entity, "
                "headline, detail, source_url, retrieved_at, status) VALUES "
                "('situation.test','2026-07-27','infrastructure_attack','country.iran',"
                "'full row','detail here','http://x/a','2026-07-27','observed')")
    src.execute("INSERT INTO situation_log (situation_id, ts, headline, source_url, "
                "retrieved_at, status) VALUES ('situation.test','2026-07-26',"
                "'sparse row','http://x/b','2026-07-26','observed')")
    src.execute("INSERT INTO reads (made_at, kind, anchor_date, anchor_series, "
                "horizon_days, expected_car) VALUES ('2026-07-27',"
                "'chokepoint_disruption','2026-07-20','fred.DCOILBRENTEU',20,-7.5)")
    src.commit()
    for t in ("situation_log", "reads"):
        export_state.export_table(src, t)
    src.close()

    dst = sqlite3.connect(":memory:")
    dst.executescript(_SITUATION_LOG_DDL + _READS_DDL)
    for t in ("situation_log", "reads"):
        import_state.import_table(dst, t)
    assert dst.execute("SELECT COUNT(*) FROM situation_log").fetchone()[0] == 2
    assert dst.execute("SELECT COUNT(*) FROM reads").fetchone()[0] == 1
    # the sparse row's actor_entity came back as NULL, not "".
    got = dst.execute("SELECT actor_entity FROM situation_log WHERE "
                      "source_url='http://x/b'").fetchone()[0]
    assert got is None
    # a pending read's realized_car is NULL, not "".
    assert dst.execute("SELECT realized_car FROM reads").fetchone()[0] is None
    # re-importing is idempotent (UNIQUE guard) -> still 2 situation_log rows.
    import_state.import_table(dst, "situation_log")
    assert dst.execute("SELECT COUNT(*) FROM situation_log").fetchone()[0] == 2
    dst.close()
