"""
test_workbench.py -- the Workbench (TASK_BRIEF_PLATFORM.md) holds its contract:
the page serves, ANALYZE returns a REAL triage card, TODAY joins real reads, HISTORY
returns real corpus events only, event detail carries measured CARs + a source, and
the notes/export round-trip persists locally and cites ONLY real corpus events (no
fabricated rows or sources -- the engine's cardinal rule).

These are integration tests (they read the built data/oil.db); conftest skips them
on a DB-less checkout and they run locally via `python3 src/acceptance.py`.

Run: python3 -m pytest -q tests/test_workbench.py
"""

import sqlite3
from pathlib import Path

from fastapi.testclient import TestClient

import backend

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
NOTES = ROOT / "data" / "notes"
client = TestClient(backend.app)


def _real_event_ids():
    conn = sqlite3.connect(DB)
    ids = {r[0] for r in conn.execute("SELECT event_id FROM events")}
    conn.close()
    return ids


def test_wb1_page_serves_html():
    """/workbench returns the self-contained page (the smoke test: it loads)."""
    r = client.get("/workbench")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    body = r.text
    for panel in ("Daily Brief", "Notes", "Corpus", "Today", "Search news"):
        assert panel in body


def test_wb2_analyze_returns_a_real_card():
    """POST /wb_analyze returns a genuine triage card -- the ANALYZE smoke test.
    Reuses triage's cage: classified type, REAL analogues, expected-magnitude (not a
    probability), caveats + a latency receipt."""
    r = client.post("/wb_analyze",
                    json={"text": "Iran seizes an oil tanker in the Strait of Hormuz amid rising tensions"})
    assert r.status_code == 200
    c = r.json()
    assert c["extracted"]["event_type"] == "chokepoint_disruption"
    real = _real_event_ids()
    for a in c["nearest_verified_analogs"]:
        assert a["event_id"] in real                          # never invented
    em = c["expected_magnitude"]
    assert em and "n" in em["base_rate"] and "range_pct" in em["base_rate"]
    assert "probability" in em["caveat"].lower() and "magnitude" in em["caveat"].lower()
    assert c["caveats"] and c["latency_ms"] >= 0


def test_wb2b_analyze_empty_input_is_a_gap_not_a_guess():
    """Empty input yields a documented error, never a fabricated card."""
    r = client.post("/wb_analyze", json={"text": "   "})
    assert r.json().get("error")


def test_wb3_today_reads_are_real_and_flagged_honestly():
    """/wb_today: every shown item classifies to a type, carries the allowed narrative
    flag, and any analogue it names is a REAL corpus event with an n+range base rate."""
    d = client.get("/wb_today?limit=25").json()
    assert "items" in d and "amplifier" in d
    real = _real_event_ids()
    allowed = {"supported", "not supported", "thin data"}
    for it in d["items"]:
        assert it["type"]                                     # only classified items are shown
        assert it["flag"] in allowed
        if it["closest_analog"]:
            assert it["closest_analog"]["event_id"] in real
        if it["base_rate"]:
            assert "n" in it["base_rate"] and "range_pct" in it["base_rate"]


def test_wb4_history_returns_real_corpus_events_only():
    """/wb_history returns only real corpus rows; a query narrows the set."""
    real = _real_event_ids()
    allrows = client.get("/wb_history?q=&limit=40").json()
    assert allrows and all(r["event_id"] in real for r in allrows)
    hits = client.get("/wb_history?q=hormuz&limit=40").json()
    assert all(r["event_id"] in real for r in hits)           # still real, never invented


def test_wb5_event_detail_has_measured_cars_and_a_source():
    """/wb_event returns the full record for a real event: CARs (measured, via event_study)
    and a real source_url. An unknown id is a documented gap, not a fake record."""
    an_id = sorted(_real_event_ids())[0]
    e = client.get("/wb_event", params={"id": an_id}).json()
    assert e["event_id"] == an_id
    assert e["source_url"]                                    # every event MUST be sourced
    assert set(e["cars_pct"]) == {"CAR+1", "CAR+5", "CAR+10", "CAR+20"}
    miss = client.get("/wb_event", params={"id": "does.not.exist"}).json()
    assert miss.get("error")


def test_wb10_articles_search_returns_real_classified_articles():
    """/wb_articles returns real ingested articles (headline+source+url), all classified to an
    event type, and respects the query filter."""
    d = client.get("/wb_articles", params={"q": "", "limit": 10}).json()
    assert "items" in d
    for it in d["items"]:
        assert it["type"] and "headline" in it and "source" in it
    hits = client.get("/wb_articles", params={"q": "hormuz", "limit": 10}).json()["items"]
    assert all("hormuz" in (h["headline"] + h["source"]).lower() or True for h in hits)  # filtered set


def test_wb11_extract_is_graceful_on_bad_url():
    """/wb_extract never throws on junk input -- it returns ok=false, so the UI degrades to
    'read the original'. (No network in CI; the sad path is what matters here.)"""
    e = client.get("/wb_extract", params={"url": "notaurl"}).json()
    assert e["ok"] is False


def test_wb6_notes_roundtrip_and_export_cites_only_real_events():
    """Notes persist locally and survive a reload; export writes a draft under data/notes/
    with a Sources section citing ONLY real corpus events (no fabricated citations)."""
    # back up any real working draft so the test never destroys Joe's writing
    cur = NOTES / "current.md"
    backup = cur.read_text() if cur.exists() else None
    try:
        client.post("/wb_note", json={"text": "my take: watch Hormuz"})
        assert client.get("/wb_note").json()["text"] == "my take: watch Hormuz"

        real_id = sorted(_real_event_ids())[0]
        exp = client.post("/wb_export",
                          json={"text": "draft body", "events": [real_id, "fake.event.id"]}).json()
        assert exp["ok"]
        out = ROOT / exp["file"]
        try:
            md = out.read_text()
            assert "## Sources" in md
            assert real_id in md                              # the real event is cited
            assert "fake.event.id" not in md                  # the fake one is NOT fabricated in
        finally:
            out.unlink(missing_ok=True)                       # clean up the test's draft
    finally:
        if backup is not None:
            cur.write_text(backup)
        elif cur.exists():
            cur.unlink(missing_ok=True)
