"""The Story object and the v2 endpoints, on real corpus events (point-in-time) and a pasted story."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import ledger as L                 # noqa: E402
import story_read as SR            # noqa: E402


@pytest.fixture(autouse=True)
def _scratch_ledger(tmp_path, monkeypatch):
    """Never let tests write to the real ledger."""
    monkeypatch.setattr(L, "LEDGER_DIR", tmp_path)
    monkeypatch.setattr(L, "CLAIMS", tmp_path / "claims.jsonl")
    monkeypatch.setattr(L, "RESOLUTIONS", tmp_path / "resolutions.jsonl")


def test_abqaiq_is_read_point_in_time():
    s = SR.read(event_id="abqaiq_attack_2019", log=False)
    assert s["event_class"] == "infrastructure_attack" and s["knowable"] == "2019-09-14"
    pr = s["priced"]
    assert pr["fan"] and pr["fan"]["n"] > 5 and pr["complete"]
    assert pr["price_at_knowable"] and len(pr["path_pct"]) == 21
    # every analog knowable before the event; the event itself excluded
    assert pr["tails"]["high"]["date"] < "2019-09-14" and pr["tails"]["low"]["date"] < "2019-09-14"
    assert pr["tails"]["high"]["event_id"] != "abqaiq_attack_2019"
    br = s["branches"]
    assert br["applicable"] and all(a["date"] < "2019-09-14" for a in br["analogs"])
    assert s["significance"]["significance"] in ("MATERIAL", "IN_LINE", "NOISE")
    assert s["propagation"]["hops"] and all("n" in h for h in s["propagation"]["hops"])
    # Brief A-2: trust rows come from the walk summary on IES-90 labels; the corpus-derived branch rates carry the retired label
    wf = s["trust"]["walk_forward"]
    assert "IES-90" in wf["label"] and "protocol §7" in wf["label"] and wf["run_id"] and wf["run_id"] in wf["label"]
    assert {r["metric"] for r in wf["rows"]} >= {"G Brier skill vs climatology", "P CRPS skill vs climatology", "Permutation p (G skill vs label shuffles)"}
    assert wf["statuses"]["engine:G"] and wf["statuses"]["engine:P"] and "VALIDATED" not in json.dumps(wf["statuses"])
    assert "retired" in br["outcome_label"] and "sr_outcome_90" in br["outcome_label"]
    assert br["ies90"]["n"] > 0 and br["ies90"]["rates"] and "IES-90" in br["ies90"]["label"]


def test_pasted_story_types_and_scores_claims_and_logs_them():
    s = SR.read(arg="Analysts say the strike on Kharg Island could send Brent past $110 a barrel within weeks. "
                    "Iran will retaliate against Gulf shipping, and fertilizer prices will spike.", log=True)
    kinds = {c["kind"] for c in s["claims"]}
    assert {"level", "escalation", "direction"} <= kinds
    for c in s["claims"]:
        v = c["verdict"]
        assert v["verdict"] in ("SUPPORTED", "MIXED", "UNSUPPORTED", "THIN", "NO PRECEDENT", "UNCHECKABLE")
        if v.get("r") is not None:
            assert 0 <= v["r"] <= 1 and v["n"] >= 1
    assert s["ledger_ids"] and len(L._rows(L.CLAIMS)) == len([c for c in s["claims"]])


def test_off_topic_text_is_noise_without_fabrication():
    s = SR.read(arg="The local library extended its weekend opening hours.", log=False)
    assert s["event_class"] in (None, "")
    assert s["significance"]["significance"] == "NOISE"
    assert s["priced"].get("fan") is None
    assert not s["propagation"]


def test_v2_endpoints():
    sys.path.insert(0, str(ROOT / "src"))
    from fastapi.testclient import TestClient
    import backend
    c = TestClient(backend.app)
    for u in ("/api/market_state", "/api/feed", "/api/big_moves?asset=brent", "/api/ledger", "/api/events?q=hormuz", "/app", "/big_moves"):
        r = c.get(u)
        assert r.status_code == 200, u
    bm = c.get("/api/big_moves?asset=brent").json()
    assert bm["n_episodes"] > 20 and "p_big_given_class" in bm and bm["registration"].startswith("BIG_MOVES_REGISTRATION")
    st = c.get("/api/story?id=hormuz_closure_2026").json()
    assert st["event_class"] == "chokepoint_disruption" and st["knowable"] == "2026-03-04"
    assert c.get("/api/story?id=not_a_real_event").status_code == 404
    assert c.post("/api/story", json={"text": ""}).status_code == 400
    led = c.get("/api/ledger").json()
    assert led["record_vs_narrative"]["status"] in ("seeding", "live") and "engine" in led


def test_walk_and_engine_endpoints():
    sys.path.insert(0, str(ROOT / "src"))
    from fastapi.testclient import TestClient
    import backend
    c = TestClient(backend.app)
    s = c.get("/api/walk/summary")
    assert s.status_code == 200 and "tiers" in s.json() and "verdict" in s.json()
    # Brief A-1: the endpoint carries the published summary whole (no stale whitelist); per-item tables dropped
    sj = s.json()
    for k in ("leakage_test", "fdr", "seal_check", "placebo", "permutation", "regime_blocks", "spec_curve", "run_id", "limits", "data_state"):
        assert k in sj, k
    assert "rps" in sj["tiers"]["daily"]["G"] and "spa" in sj["tiers"]["daily"]["G"]
    assert "frozen" in sj["tiers"]["daily"]["M"] and "engine" in sj["tiers"]["daily"]["M"]
    assert "items_vs_climatology" not in sj["tiers"]["daily"]["G"]
    assert sj["run_id"] == json.loads((ROOT / "data" / "walk_forward" / "summary.json").read_text())["run_id"]
    lst = c.get("/api/walk/list").json()
    assert lst and all("event_id" in r and "sealed_at" in r for r in lst)
    eid = next(r["event_id"] for r in lst if r["burn_in_ok"])
    r = c.get(f"/api/walk/read?id={eid}").json()
    assert r["read"]["hash"] and r["read"]["sealed_at"] and "score" in r
    assert r["read"]["sealed_at"] <= (r["score"].get("outcome") or {}).get("looked_up_at", "9999")   # sealed before the outcome was looked up
    e = c.get("/api/engine_read?id=september_11_attacks_2001").json()
    assert e["as_of"] == "2001-09-11" and all(a["date"] < "2001-09-11" for a in e["analogs"])        # point-in-time
    st = c.get("/api/story?id=september_11_attacks_2001").json()
    assert st["engine"]["available"] and st["engine"]["G"]["n"] > 0
    assert c.get("/api/walk/read?id=not_a_real_event").status_code == 404
