"""Priority E tooling (session A owns routes + fetch/verify): the route table matches what the code actually wires,
each route may only yield the outcome the rule allows it to, and a refusal is never written as an absence."""
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "state"))
import source_repair as SR    # noqa: E402


def test_route_table_matches_the_wired_routes_and_states_the_unreachable_ones():
    t = (ROOT / "data" / "candidates" / "ROUTE_TABLE.md").read_text()
    for wired in ("history.state.gov", "federalregister.gov/api/v1/documents.json",
                  "discovery.nationalarchives.gov.uk/API/search/records", "api.gdeltproject.org/api/v2/doc/doc"):
        assert wired in t
    for unreachable in ("CIA CREST", "UN Digital Library", "OPEC archive", "NARA"):
        assert unreachable in t
    assert "govinfo" in t and "DEMO_KEY" in t            # reachable but deliberately not wired, with the reason
    for u in SR.UNREACHABLE:                              # the tool's own list agrees with the table, route by route
        name = u.split(":")[0].split(" (")[0].strip()     # e.g. "CIA CREST", "US NARA catalog"
        assert name.split(" /")[0] in t, name


def test_each_route_can_only_yield_the_outcome_the_rule_allows():
    ev = {"event_id": "x", "title": "Venezuela sanctions", "parties": ["Venezuela"], "source_url": "", "cohort": "encyclopaedia"}
    d = pd.Timestamp("2019-01-28")
    # UK National Archives is file-level: partial at best, never closed
    src = (ROOT / "src" / "source_repair.py").read_text()
    tna = src[src.index("def tna_route"):src.index("def fedreg_route")]
    assert '"status": "partial"' in tna and '"closed' not in tna
    # FRUS and the Federal Register carry a document date, so they may close
    frus = src[src.index("def frus_route"):src.index("def tna_route")]
    fed = src[src.index("def fedreg_route"):src.index("def gdelt_route")]
    assert '"status": "closed-primary"' in frus and '"status": "closed-primary"' in fed     # §6.3: government documents
    gd = src[src.index("def gdelt_route"):src.index("def repair")]
    assert "press_candidate" in gd and "closed" not in gd                                    # §6.5: press never closes anything
    # coverage guards: nothing is asked outside the era the table states
    assert SR.frus_route(ev, pd.Timestamp("2019-01-28"))["status"] == "out_of_coverage"
    assert SR.fedreg_route(ev, pd.Timestamp("1975-01-01"))["status"] == "out_of_coverage"
    assert SR.gdelt_route(ev, pd.Timestamp("2005-01-01"))["status"] == "out_of_coverage"


def test_a_refusal_is_undetermined_and_blocks_only_on_no_answer(monkeypatch):
    ev = {"event_id": "x", "event_date": "2019-01-28", "title": "Venezuela sanctions", "parties": ["Venezuela"],
          "source_url": "", "cohort": "encyclopaedia"}
    d = pd.Timestamp("2019-01-28")
    monkeypatch.setattr(SR, "_get", lambda url, params=None: {"status": 429, "text": "", "url": url})
    r = SR.fedreg_route(ev, d)
    assert r["status"] == "undetermined" and "refused" in r["note"]
    assert SR.tna_route(ev, d)["status"] == "undetermined"
    # every route undetermined or out of coverage -> blocked-by-declassification, never "none found"
    res = SR.repair(ev, routes=[lambda e, dd: {"route": "a", "status": "undetermined"}, lambda e, dd: {"route": "b", "status": "out_of_coverage"}])
    assert res["outcome"] == "blocked-by-declassification"
    # one route answering with nothing is an absence in the reachable record, not a block
    res = SR.repair(ev, routes=[lambda e, dd: {"route": "a", "status": "none_found"}, lambda e, dd: {"route": "b", "status": "undetermined"}])
    assert res["outcome"] == "none_found"
    # a file-level hit is partial even when a dated one is absent; a dated hit wins
    res = SR.repair(ev, routes=[lambda e, dd: {"route": "a", "status": "none_found"}, lambda e, dd: {"route": "b", "status": "partial"}])
    assert res["outcome"] == "partial"
    res = SR.repair(ev, routes=[lambda e, dd: {"route": "b", "status": "partial"}, lambda e, dd: {"route": "a", "status": "closed-primary"}])
    assert res["outcome"] == "closed-primary"
    # §6.5: only a primary document repairs an event; a press hit is a place to look and ranks below even a file-level pointer
    res = SR.repair(ev, routes=[lambda e, dd: {"route": "b", "status": "press_candidate"}, lambda e, dd: {"route": "a", "status": "closed-primary"}])
    assert res["outcome"] == "closed-primary"
    res = SR.repair(ev, routes=[lambda e, dd: {"route": "b", "status": "press_candidate"}, lambda e, dd: {"route": "a", "status": "partial"}])
    assert res["outcome"] == "partial"
    res = SR.repair(ev, routes=[lambda e, dd: {"route": "b", "status": "press_candidate"}, lambda e, dd: {"route": "a", "status": "none_found"}])
    assert res["outcome"] == "press_candidate"
    assert SR.AGGREGATOR.search("Uae Yemen Drones : Latest News , Photos , Videos on Uae Yemen")
    assert not SR.AGGREGATOR.search("Israeli airstrike destroys Iran consular building in Damascus")


def test_the_ownership_split_is_enforced_by_the_era_filter():
    import sqlite3
    conn = sqlite3.connect(ROOT / "data" / "oil.db")
    mine = SR.weak_events(conn, "encyclopaedia", "2000-01-01")
    theirs = SR.weak_events(conn, "encyclopaedia", None, "1999-12-31")
    conn.close()
    assert mine and theirs
    assert not ({e["event_id"] for e in mine} & {e["event_id"] for e in theirs})     # A and E never write the same dossier
    assert all(e["event_date"] >= "2000-01-01" for e in mine)


def test_written_dossiers_never_claim_more_than_the_route_gave():
    idx = ROOT / "data" / "candidates" / "repairs_index_sessionA_post2000.json"
    if not idx.exists():
        pytest.skip("run python3 src/source_repair.py --cohort encyclopaedia --from 2000-01-01 --index-tag sessionA_post2000")
    j = json.loads(idx.read_text())
    assert j["scope"]["date_from"] == "2000-01-01" and j["n"] > 0
    for r in j["repairs"]:
        assert r["outcome"] in ("closed-primary", "press_candidate", "partial", "none_found", "blocked-by-declassification")
        assert r["event_date"] >= "2000-01-01"
        text = (ROOT / "data" / "candidates" / "repairs" / f"{r['event_id']}.md").read_text()
        assert "Joe: this replaces nothing until you say so" in text
        if r["outcome"] == "closed-primary":
            assert r["proposed"]["route"] in SR.PRIMARY_ROUTES and r["proposed"]["date"] and "PRIMARY document" in text
        if r["outcome"] == "press_candidate":
            assert r["proposed"]["route"] == "GDELT DOC 2.0" and r["proposed"]["date"]
            assert "A PLACE TO LOOK, not a repair" in text and "NOT counted as a repair" in text
            assert not SR.AGGREGATOR.search(r["proposed"]["title"] or "")
        if r["outcome"] == "partial":
            assert r["proposed"]["route"] == "UK National Archives" and "NOT a record of the event" in text
        if r["outcome"] == "blocked-by-declassification":
            assert "statement about ACCESS" in text
    # §6.5(3): the index keeps repairs and press candidates apart, so no report can add them into one number
    assert "closed-contemporaneous" not in json.dumps(j)
    assert set(j["outcomes"]) <= {"closed-primary", "press_candidate", "partial", "none_found", "blocked-by-declassification"}
