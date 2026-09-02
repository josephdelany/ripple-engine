"""PATH Step 10 / Brief A-4: the three demos run from sealed inputs on /walk.
For september_11_attacks_2001, iraq_invades_kuwait_1990 and hormuz_closure_2026: /api/walk/read returns the sealed
read; every analog is dated before the event; the read's hash re-verifies with walk.py's own sealing (imported, not
reimplemented); the read was sealed before the outcome was looked up; /api/engine_read at as_of = event date returns
only earlier analogs; /api/story has the engine block with G.n > 0."""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
DEMOS = ("september_11_attacks_2001", "iraq_invades_kuwait_1990", "hormuz_closure_2026")


@pytest.fixture(scope="module")
def client():
    if not (ROOT / "data" / "walk_forward" / "reads.jsonl").exists():
        pytest.skip("no sealed reads: run python3 src/walk.py")
    from fastapi.testclient import TestClient
    import backend
    return TestClient(backend.app)


@pytest.fixture(scope="module")
def dates():
    conn = sqlite3.connect(ROOT / "data" / "oil.db")
    d = dict(conn.execute("SELECT event_id, event_date FROM events"))
    conn.close()
    return d


def _analog_ids(read):
    ids = set()
    for it in read.get("items") or []:
        for row in it.get("ranked") or []:
            ids.add(row[0])
    for blk in ("engine", "frozen"):
        p = (read.get(blk) or {}).get("P") or {}
        ids.update(p.get("ids") or [])
    return ids


@pytest.mark.parametrize("eid", DEMOS)
def test_step10_demo_runs_from_the_sealed_read(client, dates, eid):
    import walk as W                                             # the sealing function itself, not a re-implementation
    r = client.get(f"/api/walk/read?id={eid}")
    assert r.status_code == 200, eid
    body = r.json()
    read, score = body["read"], body["score"]
    assert read["event_id"] == eid and read["hash"] and read["sealed_at"]
    event_date = dates[eid]
    assert read["date"] == event_date and read["as_of"] <= event_date
    ids = _analog_ids(read)
    assert ids, "the sealed read names no analogs"
    assert all(dates[a] < event_date for a in ids), sorted(a for a in ids if dates[a] >= event_date)
    # the hash re-verifies with walk.py's canonical sealing over the whole record (sealed_at included)
    assert W.verify_seal(read), "sealed read does not re-verify"
    assert read["hash"] == score.get("read_hash")
    # sealed before the outcome was looked up
    looked = (score.get("outcome") or {}).get("looked_up_at")
    assert looked and read["sealed_at"] <= looked, (read["sealed_at"], looked)
    # the point-in-time engine read at the event date sees only earlier analogs
    e = client.get(f"/api/engine_read?id={eid}&as_of={event_date}").json()
    assert e["as_of"] == event_date and e["analogs"] and all(a["date"] < event_date for a in e["analogs"])
    # the story page carries the engine block with a live IES-90 read
    st = client.get(f"/api/story?id={eid}").json()
    assert st["engine"]["available"] and st["engine"]["G"]["n"] > 0
    assert st["trust"]["walk_forward"]["run_id"] == json.loads((ROOT / "data" / "walk_forward" / "summary.json").read_text())["run_id"]
