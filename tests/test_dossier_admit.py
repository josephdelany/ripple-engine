"""Brief A-6: dossiers carry the two-source rule with opened citations; admit.py refuses without Joe's flag, refuses an
inadmissible dossier, and on Joe's line writes the row to a COPY of events.csv and a scratch DB with the dossier as provenance.
The real events table and data/events.csv are never touched by these tests."""
import csv
import json
import shutil
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import admit as A     # noqa: E402
import dossier as D   # noqa: E402


def test_a6_rule_registered_and_dossier_shape():
    assert (ROOT / "data" / "candidates" / "DOSSIER_RULE.md").exists()
    assert D.proposed_class("SUEZ CANAL") == "chokepoint_disruption" and D.proposed_class("OIL EMBARGO") == "sanctions" and D.proposed_class("X") == "conflict_escalation"
    idx = ROOT / "data" / "candidates" / "dossiers_index.json"
    if not idx.exists():
        pytest.skip("run python3 src/dossier.py first")
    j = json.loads(idx.read_text())
    assert j["n"] >= 1 and j["admissible"] <= j["n"]
    for d in j["dossiers"][:50]:
        front, text = A.read_front(ROOT / "data" / "candidates" / "dossiers" / f"{d['id']}.md")
        assert front["built_by"] == "session A" and front["approved_by"] is None          # the code never approves
        ss = front["second_source"]
        if front["admissible"]:
            assert ss["found"] and ss["url"].startswith("https://history.state.gov/") and ss["date"] and ss["window"][0] <= ss["date"] <= ss["window"][1]
        else:
            assert not ss["found"] and "second source: none found — not admissible" in text


def _scratch(tmp_path):
    dossiers = tmp_path / "dossiers"; dossiers.mkdir()
    idx = json.loads((ROOT / "data" / "candidates" / "dossiers_index.json").read_text())
    ok = next(d for d in idx["dossiers"] if d["admissible"]); bad = next((d for d in idx["dossiers"] if not d["admissible"]), None)
    for d in (ok, bad):
        if d:
            shutil.copy(ROOT / "data" / "candidates" / "dossiers" / f"{d['id']}.md", dossiers / f"{d['id']}.md")
    csvp = tmp_path / "events.csv"
    with open(ROOT / "data" / "events.csv", encoding="utf-8") as f:
        csvp.write_text("".join([next(f) for _ in range(3)]), encoding="utf-8")
    db = tmp_path / "scratch.db"
    conn = sqlite3.connect(db)
    src = sqlite3.connect(ROOT / "data" / "oil.db")
    for t in ("events", "entities", "event_entities"):
        conn.execute(src.execute("SELECT sql FROM sqlite_master WHERE name=?", (t,)).fetchone()[0])
    src.close(); conn.commit(); conn.close()
    return dossiers, csvp, db, ok, bad


def test_a6_admit_refuses_without_joe_and_refuses_inadmissible(tmp_path):
    if not (ROOT / "data" / "candidates" / "dossiers_index.json").exists():
        pytest.skip("run python3 src/dossier.py first")
    dossiers, csvp, db, ok, bad = _scratch(tmp_path)
    with pytest.raises(A.Refused):
        A.admit(ok["id"], None, dossiers, csvp, db)
    with pytest.raises(A.Refused):
        A.admit(ok["id"], "session A", dossiers, csvp, db)
    if bad:
        with pytest.raises(A.Refused):
            A.admit(bad["id"], "joe", dossiers, csvp, db)
    assert sqlite3.connect(db).execute("SELECT COUNT(*) FROM events").fetchone()[0] == 0


def test_a6_admit_on_joes_line_writes_csv_db_and_provenance(tmp_path):
    if not (ROOT / "data" / "candidates" / "dossiers_index.json").exists():
        pytest.skip("run python3 src/dossier.py first")
    dossiers, csvp, db, ok, _ = _scratch(tmp_path)
    row = A.admit(ok["id"], "joe", dossiers, csvp, db, now="2026-09-02T20:00:00+00:00")
    rows = list(csv.DictReader(open(csvp, encoding="utf-8")))
    assert rows[-1]["event_id"] == ok["id"] and "dossier" in rows[-1]["description"] and "approved by joe" in rows[-1]["description"]
    conn = sqlite3.connect(db)
    assert conn.execute("SELECT type, source_url FROM events WHERE event_id=?", (ok["id"],)).fetchone() == (row["type"], row["source_url"])
    front, _ = A.read_front(dossiers / f"{ok['id']}.md")
    assert front["approved_by"] == "joe" and front["approved_at"] == "2026-09-02T20:00:00+00:00"
    with pytest.raises(A.Refused):                      # idempotent: a second admission is refused
        A.admit(ok["id"], "joe", dossiers, csvp, db)
    # the real corpus is untouched
    real = sqlite3.connect(ROOT / "data" / "oil.db")
    assert real.execute("SELECT COUNT(*) FROM events WHERE event_id=?", (ok["id"],)).fetchone()[0] == 0
