"""The Challenge loop (CLAIM_LEDGER_REGISTRATION.md Amendment 4) on abqaiq_attack_2019.

Point-in-time, coded vocabulary only, THIN / NO PRECEDENT first-class, price side from the same
subset, refusals logged, nothing edited. The ledger is redirected to a scratch file in every test.
"""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import challenge as C          # noqa: E402
import escalation as ES        # noqa: E402

ABQ = "event:abqaiq_attack_2019"
KNOWABLE = "2019-09-14"


@pytest.fixture(autouse=True)
def _scratch(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "LEDGER_DIR", tmp_path)
    monkeypatch.setattr(C, "CHALLENGES", tmp_path / "challenges.jsonl")


@pytest.fixture
def conn():
    c = sqlite3.connect(C.DB)
    yield c
    c.close()


def test_ch1_abqaiq_conditioned_on_actor_usa_is_point_in_time_and_from_the_same_subset(conn):
    r = C.run(conn, ABQ, {"actor": "country.usa"})
    assert r["status"] in ("CONDITIONED", "THIN", "NO PRECEDENT")
    assert r["knowable"] == KNOWABLE and r["conditions_applied"] == {"actor": "country.usa"}
    assert r["target"]["actor"] == "unknown" and r["conditioned_target"]["actor"] == "country.usa"
    assert r["field_coverage"]["actor"]["coverage"] > 0 and not r["flags"]
    sub = r["subset"]
    assert all(a["date"] < KNOWABLE for a in sub["analogs"])                       # no lookahead
    assert all(a["event_id"] != "abqaiq_attack_2019" for a in sub["analogs"])      # the event itself excluded
    assert sub["n"] == len(sub["analogs"]) and sum(sub["counts"].values()) <= sub["n"]
    # the price side is computed for exactly the subset's ids, no others
    ids = {a["event_id"] for a in sub["analogs"]}
    p = r["price"]
    if p["n"]:
        assert p["tails"]["low"]["event_id"] in ids and p["tails"]["high"]["event_id"] in ids
        assert p["n"] <= sub["n"] and p["bar"]["n"] == p["n"]
    cmp_ = r["comparison"]
    assert set(cmp_) == {"unconditioned", "conditioned", "delta"}
    assert cmp_["conditioned"]["n"] == sub["n"]
    if r["status"] == "CONDITIONED":
        assert sub["n"] >= ES.COND_MIN_N and r["branch_rates"]["basis"] == "conditioned"
    if r["status"] == "THIN":
        assert sub["n"] < ES.COND_MIN_N and r["branch_rates"]["thin"] is True
    # every challenge is appended verbatim, once
    rows = C.rows()
    assert len(rows) == 1 and rows[0]["challenge_id"] == r["challenge_id"] and rows[0]["conditions"] == {"actor": "country.usa"}
    assert rows[0]["status"] == r["status"] and rows[0]["n"] == sub["n"]


def test_ch2_target_capacity_substantial_is_not_in_the_vocabulary_and_is_refused_but_logged(conn):
    r = C.run(conn, ABQ, {"target_capacity": "substantial"})
    assert r["status"] == "REFUSED"
    assert any("substantial" in e and "significant" in e for e in r["errors"])     # the codebook enum is shown
    rows = C.rows()
    assert len(rows) == 1 and rows[0]["status"] == "REFUSED" and rows[0]["conditions"] == {"target_capacity": "substantial"}


def test_ch3_target_capacity_is_uncoded_so_the_condition_cannot_bite_and_says_so(conn):
    """alliance / diplomatic / target_capacity are 'unknown' in every corpus record today: a condition on
    them is inert (unknown fields are not counted in similarity). The panel must say field_uncoded and
    the subset must equal the unconditioned one, rather than pretend the condition changed anything."""
    r = C.run(conn, ABQ, {"target_capacity": "significant"})
    assert r["status"] != "REFUSED"
    cov = r["field_coverage"]["target_capacity"]
    if cov["coverage"] == 0:
        assert "field_uncoded:target_capacity" in r["flags"]
        assert r["comparison"]["delta"]["n"] == 0 and r["comparison"]["delta"]["escalated_share"] in (0.0, None)
    else:                                                       # once the field is coded, the flag must be gone
        assert "field_uncoded:target_capacity" not in r["flags"]


def test_ch4_no_precedent_and_thin_are_first_class(conn, monkeypatch):
    # no precedent: force the retrieval threshold above any possible similarity
    monkeypatch.setattr(ES, "RETRIEVE_MIN", 1.01)
    r = C.run(conn, ABQ, {"actor": "country.usa"})
    assert r["status"] == "NO PRECEDENT" and r["subset"]["n"] == 0 and r["price"]["n"] == 0
    assert r["comparison"]["conditioned"]["counts"] == {}
    monkeypatch.setattr(ES, "RETRIEVE_MIN", 0.40)
    # thin: force the conditioned minimum above the corpus size
    monkeypatch.setattr(ES, "COND_MIN_N", 10_000)
    r = C.run(conn, ABQ, {"actor": "country.usa"})
    assert r["status"] == "THIN" and r["branch_rates"]["thin"] is True and "fallback" in r["branch_rates"]["basis"]
    assert r["subset"]["n"] == len(r["subset"]["analogs"])                       # the thin subset's own counts still shown


def test_ch5_refusals_unknown_field_unknown_story_non_geo_class(conn):
    assert C.run(conn, ABQ, {"severity": "5"})["status"] == "REFUSED"
    assert C.run(conn, "event:not_a_real_event", {"actor": "country.usa"})["status"] == "REFUSED"
    assert C.run(conn, ABQ, {})["status"] == "REFUSED"
    opec = conn.execute("SELECT event_id FROM events WHERE type='opec_decision' LIMIT 1").fetchone()[0]
    r = C.run(conn, f"event:{opec}", {"actor": "country.usa"})
    assert r["status"] == "REFUSED" and "not a geopolitical class" in r["errors"][0]
    assert len(C.rows()) == 4                                                    # each refusal logged


def test_ch6_vocab_reports_coverage_and_the_codebook_enums(conn):
    v = C.vocab(conn)
    assert v["n_records"] > 100
    f = v["fields"]
    assert f["conflict_scope"]["allowed"][:3] == ["isolated", "campaign", "war"] and f["conflict_scope"]["coverage"] > 0
    assert f["target_capacity"]["allowed"] == ["none", "limited", "significant"]
    assert "country.usa" in f["actor"]["allowed"] and f["actor"]["coverage"] == sum(f["actor"]["coded"].values())


def test_ch7_endpoints(monkeypatch):
    from fastapi.testclient import TestClient
    import backend
    c = TestClient(backend.app)
    v = c.get("/api/challenge/vocab").json()
    assert v["fields_order"][0] == "actor" and "target_capacity" in v["fields"]
    r = c.post("/api/challenge", json={"story_id": ABQ, "conditions": {"actor": "country.usa"}, "note": "what if Washington is the actor"})
    assert r.status_code == 200 and r.json()["status"] in ("CONDITIONED", "THIN", "NO PRECEDENT") and r.json()["note"] == "what if Washington is the actor"
    bad = c.post("/api/challenge", json={"story_id": ABQ, "conditions": {"target_capacity": "substantial"}})
    assert bad.status_code == 400 and "substantial" in json.dumps(bad.json())
    assert c.get("/api/challenges?story_id=" + ABQ).status_code == 200
