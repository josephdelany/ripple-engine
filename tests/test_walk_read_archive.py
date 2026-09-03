"""A hash this project has published must keep resolving after its run is archived, or every citation in the paper
rots at the next run. /api/walk/read takes an event_id, a full hash, or the 12-character prefix the demo pages and
the paper quote; it searches the live files first, then data/walk_forward/runs/<run_id>/*.jsonl.gz, and names the run
that served it. Regression: on 2026-09-03 the three demo hashes from walk_20260902T182828Z returned 404 while
docs/demos/ quoted them."""
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

# the hashes docs/demos/ quotes, from a run that has since been archived
DEMO_HASHES = {"8b7277ff28fc": "september_11_attacks_2001",
               "5bc0293dd2d9": "iraq_invades_kuwait_1990",
               "aed201938e98": "hormuz_closure_2026"}
ARCHIVED_RUN = "walk_20260902T182828Z"


@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient
    import backend
    return TestClient(backend.app)


def test_the_hashes_the_demo_pages_quote_are_the_ones_tested():
    """If the demo pages are requoted, this test must be updated with them -- it is the citation contract."""
    quoted = set()
    for f in (ROOT / "docs" / "demos").glob("*.md"):
        quoted |= set(re.findall(r"\b[0-9a-f]{12}\b", f.read_text()))
    if not quoted:
        pytest.skip("docs/demos/ quotes no hashes")
    assert set(DEMO_HASHES) <= quoted, f"docs/demos/ no longer quotes {set(DEMO_HASHES) - quoted}"


@pytest.mark.parametrize("h,eid", sorted(DEMO_HASHES.items()))
def test_published_hash_resolves_from_the_archive_and_names_its_run(client, h, eid):
    import walk as W
    if not (ROOT / "data" / "walk_forward" / "runs" / ARCHIVED_RUN).is_dir():
        pytest.skip(f"{ARCHIVED_RUN} is not archived here")
    r = client.get(f"/api/walk/read?id={h}")
    assert r.status_code == 200, f"{h} did not resolve: the paper's citation would be dead"
    j = r.json()
    served = j["served_from"]
    assert served["source"] == "archived" and served["run_id"] == ARCHIVED_RUN     # the reply names the run
    assert served["path"].endswith(".gz") and "runs/" in served["path"]
    read = j["read"]
    assert read["event_id"] == eid and read["hash"].startswith(h) and read["run_id"] == ARCHIVED_RUN
    assert W.verify_seal(read)                                                     # the archived row is intact
    assert j["score"].get("read_hash") == read["hash"]                             # its score came from the same run
    assert j["event"]["event_id"] == eid


def test_live_first_then_archive_and_event_ids_still_work(client):
    j = client.get("/api/walk/read?id=september_11_attacks_2001").json()
    assert j["served_from"]["source"] == "live"                                    # an event_id resolves live
    live_run = j["read"]["run_id"]
    full = j["read"]["hash"]
    assert client.get(f"/api/walk/read?id={full}").json()["read"]["hash"] == full  # a full live hash resolves too
    # the same event resolves to a DIFFERENT read in the archived run: live is preferred, the archive still reachable
    a = client.get(f"/api/walk/read?id={list(DEMO_HASHES)[0]}").json()
    assert a["read"]["run_id"] != live_run
    assert client.get("/api/walk/read?id=deadbeefdeadbeef").status_code == 404


def test_list_names_the_run_per_row_and_can_serve_an_archived_run(client):
    live = client.get("/api/walk/list").json()
    assert live and all(r.get("source") == "live" and r.get("run_id") for r in live)
    arch = client.get(f"/api/walk/list?run={ARCHIVED_RUN}")
    if arch.status_code == 404:
        pytest.skip(f"{ARCHIVED_RUN} not archived")
    rows = arch.json()
    assert rows and all(r["source"] == "archived" and r["run_id"] == ARCHIVED_RUN for r in rows)
    assert {DEMO_HASHES[h] for h in DEMO_HASHES} <= {r["event_id"] for r in rows}
    assert client.get("/api/walk/list?run=walk_not_a_run").status_code == 404


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
        api_v2._find_in(f, "abcdef123456")                       # matches two different reads
    assert e.value.status_code == 409 and "ambiguous" in e.value.detail
    # a prefix long enough to be unique resolves, and an exact hash beats any prefix
    assert api_v2._find_in(f, "abcdef1234560000")["event_id"] == "a"
    assert api_v2._find_in(f, "ffffffffffff")["event_id"] == "c"
    assert api_v2._find_in(f, "b")["event_id"] == "b"            # too short to be a hash prefix -> read as an event_id
    assert api_v2._find_in(f, "nope") is None
