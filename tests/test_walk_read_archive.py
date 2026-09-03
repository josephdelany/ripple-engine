"""Two separate contracts, so that requoting the demo pages can never break either.

1. **A citation in the docs is never dead.** Every read hash quoted anywhere in `docs/demos/` must resolve through
   `/api/walk/read`, whatever run serves it. This is the contract the paper depends on, and it survives Cowork
   requoting the pages after any run.
2. **The archive fallback works.** Pinned to a hash from a run that is already archived and will stay archived
   (`8b7277ff28fc`, `walk_20260902T182828Z`), so it tests the fallback path itself rather than whatever the demos
   happen to quote today.

Regression behind both: the walk archives every prior run into `data/walk_forward/runs/<run_id>/*.jsonl.gz`
(protocol Amendment D), and the endpoints read only the live files, so on 2026-09-03 the three hashes the demo
pages then quoted returned 404. Splitting the contracts also fixes the earlier test's own defect: it pinned the
demo hashes as constants, so requoting the pages to a newer run failed a test that was measuring the wrong thing.
"""
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

DEMOS = ROOT / "docs" / "demos"
HASH_RE = re.compile(r"\b[0-9a-f]{12,64}\b")

# A read hash from a run that has been archived and will stay archived: the fixture for the fallback path.
# Deliberately NOT read from the demo pages -- those get requoted, and this must not move with them.
ARCHIVED_HASH = "8b7277ff28fc"
ARCHIVED_RUN = "walk_20260902T182828Z"
ARCHIVED_EVENT = "september_11_attacks_2001"
DEMO_EVENTS = {"september_11_attacks_2001", "iraq_invades_kuwait_1990", "hormuz_closure_2026"}


@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient
    import backend
    return TestClient(backend.app)


def quoted_hashes():
    """Every read-hash-shaped token in docs/demos/, with the page(s) quoting it."""
    out = {}
    for f in sorted(DEMOS.glob("*.md")):
        for h in HASH_RE.findall(f.read_text()):
            out.setdefault(h, []).append(f.name)
    return out


# --- contract 1: a citation in the docs is never dead ---------------------------------------------------------

def test_every_hash_the_demo_pages_quote_resolves(client):
    """Whatever run serves it. Requoting the pages to a newer run keeps this passing; a dead citation fails it."""
    quoted = quoted_hashes()
    if not quoted:
        pytest.skip("docs/demos/ quotes no read hashes")
    dead = {}
    for h, pages in sorted(quoted.items()):
        r = client.get(f"/api/walk/read?id={h}")
        if r.status_code != 200:
            dead[h] = (r.status_code, pages)
            continue
        j = r.json()
        served = j.get("served_from") or {}
        assert served.get("run_id") and served.get("source") in ("live", "archived"), (h, served)
        assert j["read"]["hash"].startswith(h) and j["read"]["event_id"]
        assert j["score"].get("read_hash") == j["read"]["hash"], f"{h}: paired with another run's score"
    assert not dead, f"citations in docs/demos/ no longer resolve: {dead}"


def test_the_demo_pages_still_cite_a_sealed_read_for_each_demo_event(client):
    """The pages may be requoted to a new run, but each demo event must still carry a resolvable citation."""
    quoted = quoted_hashes()
    if not quoted:
        pytest.skip("docs/demos/ quotes no read hashes")
    events = set()
    for h in quoted:
        r = client.get(f"/api/walk/read?id={h}")
        if r.status_code == 200:
            events.add(r.json()["read"]["event_id"])
    assert DEMO_EVENTS <= events, f"no resolvable citation for {DEMO_EVENTS - events}"


# --- contract 2: the archive fallback itself ------------------------------------------------------------------

@pytest.fixture(scope="module")
def archived(client):
    if not (ROOT / "data" / "walk_forward" / "runs" / ARCHIVED_RUN).is_dir():
        pytest.skip(f"{ARCHIVED_RUN} is not archived in this checkout")
    return client


def test_the_fixture_hash_is_absent_from_the_live_files(archived):
    """Otherwise the fallback test would pass without the fallback ever running."""
    live = ROOT / "data" / "walk_forward" / "reads.jsonl"
    hashes = {json.loads(l)["hash"] for l in live.open(encoding="utf-8") if l.strip()}
    assert not any(h.startswith(ARCHIVED_HASH) for h in hashes)


def test_an_archived_hash_resolves_and_the_reply_names_the_archived_run(archived):
    import walk as W
    j = archived.get(f"/api/walk/read?id={ARCHIVED_HASH}").json()
    served = j["served_from"]
    assert served["source"] == "archived" and served["run_id"] == ARCHIVED_RUN
    assert served["path"] == f"data/walk_forward/runs/{ARCHIVED_RUN}/reads.jsonl.gz"
    read = j["read"]
    assert read["event_id"] == ARCHIVED_EVENT and read["hash"].startswith(ARCHIVED_HASH) and read["run_id"] == ARCHIVED_RUN
    assert W.verify_seal(read)                                        # the archived row is intact, not merely present
    assert j["score"]["read_hash"] == read["hash"]                    # paired with its own run's score, not a live one
    assert j["event"]["event_id"] == ARCHIVED_EVENT


def test_live_is_preferred_and_event_ids_still_resolve(archived):
    j = archived.get(f"/api/walk/read?id={ARCHIVED_EVENT}").json()
    assert j["served_from"]["source"] == "live"                       # an event_id gets the current run
    assert j["read"]["run_id"] != ARCHIVED_RUN
    full = j["read"]["hash"]
    assert archived.get(f"/api/walk/read?id={full}").json()["read"]["hash"] == full
    assert archived.get("/api/walk/read?id=deadbeefdeadbeef").status_code == 404


def test_list_names_the_run_per_row_and_can_serve_an_archived_run(archived):
    live = archived.get("/api/walk/list").json()
    assert live and all(r.get("source") == "live" and r.get("run_id") for r in live)
    rows = archived.get(f"/api/walk/list?run={ARCHIVED_RUN}").json()
    assert rows and all(r["source"] == "archived" and r["run_id"] == ARCHIVED_RUN for r in rows)
    assert ARCHIVED_EVENT in {r["event_id"] for r in rows}
    assert archived.get("/api/walk/list?run=walk_not_a_run").status_code == 404


def test_an_ambiguous_prefix_is_refused_not_guessed(tmp_path):
    """A prefix matching several different reads must say so rather than pick one."""
    import api_v2
    from fastapi import HTTPException
    f = tmp_path / "reads.jsonl"
    f.write_text("\n".join(json.dumps(r) for r in [
        {"event_id": "a", "hash": "abcdef1234560000" + "0" * 48, "run_id": "r1"},
        {"event_id": "b", "hash": "abcdef1234569999" + "9" * 48, "run_id": "r1"},
        {"event_id": "c", "hash": "ffffffffffff0000" + "0" * 48, "run_id": "r1"},
    ]) + "\n")
    with pytest.raises(HTTPException) as e:
        api_v2._find_in(f, "abcdef123456")                            # matches two different reads
    assert e.value.status_code == 409 and "ambiguous" in e.value.detail
    assert api_v2._find_in(f, "abcdef1234560000")["event_id"] == "a"  # a unique prefix resolves
    assert api_v2._find_in(f, "ffffffffffff")["event_id"] == "c"
    assert api_v2._find_in(f, "b")["event_id"] == "b"                 # too short for a hash -> read as an event_id
    assert api_v2._find_in(f, "nope") is None
