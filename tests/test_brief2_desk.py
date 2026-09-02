"""Brief A-9 / A-10: the gold set is well-formed and marked unaudited; the scorer is pure; the ledger endpoint carries the
reader score; the feed register lists every live feed; the watcher dedupes by URL+title and parses GDELT DOC replies
without inventing anything. No table is written."""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import reader_eval as RE   # noqa: E402
import watcher as W        # noqa: E402

CLASSES = {"conflict_escalation", "infrastructure_attack", "chokepoint_disruption", "sanctions", "opec_decision", "policy_response", "demand_shock"}


def test_a9_gold_is_100_real_headlines_in_codebook_terms_marked_unaudited():
    gold = RE.load_gold()
    assert len(gold) == 100 and len({g["id"] for g in gold}) == 100
    conn = sqlite3.connect(ROOT / "data" / "oil.db")
    ids = {e for (e,) in conn.execute("SELECT entity_id FROM entities")}
    titles = dict(conn.execute("SELECT event_id, title FROM events"))
    for g in gold:
        assert g["gold_class"] in CLASSES and g["coded_by"] == "session A" and g["audited_by_joe"] is False
        assert set(g["gold_entities"]) <= ids, g["id"]
        assert "1990-01-01" <= g["gold_knowable_date"] <= "2026-12-31"
        assert titles.get(g["id"]) == g["headline"]                       # a real corpus headline, not composed


def test_a9_scorer_is_pure_and_flags_the_mode():
    gold = [{"gold_class": "sanctions", "gold_entities": ["country.usa", "country.iran"], "gold_knowable_date": "2018-05-08"},
            {"gold_class": "opec_decision", "gold_entities": ["institution.opec"], "gold_knowable_date": "2020-04-12"}]
    reads = [{"event_class": "sanctions", "entities": [{"id": "country.usa"}, {"id": "country.china"}], "reader": {"mode": "llm"}},
             {"event_class": "policy_response", "entities": [{"id": "institution.opec"}], "reader": {"mode": "regex_fallback"}}]
    s = RE.score(gold, reads)
    assert s["class_accuracy"] == 0.5 and s["entity_tp_fp_fn"] == [2, 1, 1] and s["reader_modes"] == {"llm": 1, "regex_fallback": 1}
    assert s["entity_precision"] == round(2 / 3, 4) and s["entity_recall"] == round(2 / 3, 4)
    assert s["top_confusions"][0] == {"gold": "opec_decision", "read": "policy_response", "n": 1}


def test_a9_ledger_endpoint_carries_reader_eval():
    from fastapi.testclient import TestClient
    import backend
    j = TestClient(backend.app).get("/api/ledger").json()
    assert "reader_eval" in j and j["reader_eval"]["label"].startswith("reader accuracy")


def test_a10_register_lists_every_live_feed_and_watcher_dedupes_by_url_and_title(tmp_path):
    reg = (ROOT / "data" / "feeds" / "REGISTER.md").read_text()
    for name, url in W.load_feeds():
        assert url in reg, f"{name} not in data/feeds/REGISTER.md"
    assert "api.gdeltproject.org/api/v2/doc/doc" in reg and "one request per 5 s" in reg
    seen = sqlite3.connect(":memory:")
    seen.execute("CREATE TABLE seen (story_hash TEXT PRIMARY KEY, first_seen TEXT)")
    assert W.is_new(seen, "https://x/1", "Iran seizes tanker") is True
    assert W.is_new(seen, "https://x/1", "Iran seizes tanker") is False
    assert W.is_new(seen, "https://x/1", "IRAN  seizes tanker!") is False        # normalised title
    assert W.is_new(seen, "https://x/2", "Iran seizes tanker") is True            # different URL, same title -> new key
    assert W.is_new(seen, "https://x/3") is True and W.is_new(seen, "https://x/3") is False


def test_a10_gdelt_doc_parser_and_spacing():
    obj = {"articles": [{"url": "https://a.example/1", "title": "Tanker attacked near Hormuz", "domain": "a.example", "seendate": "20260902T120000Z"},
                        {"url": "not-a-url", "title": "x"}, {"url": "https://a.example/2", "title": ""}]}
    items = W.parse_gdelt_doc(obj, "strait of hormuz", "2026-09-02T12:00:00+00:00")
    assert len(items) == 1 and items[0]["url"] == "https://a.example/1" and items[0]["term"] == "strait of hormuz"
    assert W.parse_gdelt_doc({}, "x", "t") == [] and W.parse_gdelt_doc(None, "x", "t") == []
    # the runner waits the registered 5 s between terms and stops on 429
    calls, slept = [], []
    class R:
        def __init__(self, code, body): self.status_code, self.ok, self._b = code, code == 200, body
        def json(self): return self._b
    def get(term):
        calls.append(term); return R(200, obj) if len(calls) < 3 else R(429, None)
    seen = sqlite3.connect(":memory:"); seen.execute("CREATE TABLE seen (story_hash TEXT PRIMARY KEY, first_seen TEXT)")
    out = W.run_gdelt_doc(seen, ["tanker", "hormuz"], {}, "now", terms=["t1", "t2", "t3", "t4"], get=get, sleep=slept.append)
    assert calls == ["t1", "t2", "t3"] and slept == [5.0, 5.0] and len(out) == 1
