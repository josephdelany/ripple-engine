"""Brief 3 (A-12 candidates, A-13 priced-in display fields, A-14 record bar + blindspot lists, A-15 reader date/confidence).
No table is written; the desk renders under jsdom with real API payloads; nothing says VALIDATED."""
import csv
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def test_a12_candidate_sheet_excludes_corpus_neighbours_and_names_registered_states():
    p = ROOT / "data" / "candidates" / "post1987_candidates.csv"
    if not p.exists():
        pytest.skip("run python3 src/candidates_post1987.py")
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    assert rows and all("1987-01-01" <= r["event_date"] <= "2026-12-31" for r in rows)
    assert all(r["days_to_corpus"] == "" or int(r["days_to_corpus"]) > 3 for r in rows)      # never within 3 days of a corpus event
    assert {r["source"] for r in rows} <= {"icb", "mid", "ucdp", "gpr"}
    from dossier import STATE_SET
    for r in rows:
        if r["source"] != "gpr":
            assert set(int(x) for x in r["actors"].split(";")) & STATE_SET, r["source_id"]
    summ = json.loads((ROOT / "data" / "candidates" / "post1987_candidates_summary.json").read_text())
    assert summ["n"] == len(rows) and (ROOT / "data" / "candidates" / "DOSSIER_RULE.md").read_text().count("## 5.") == 1


def test_a13_priced_in_is_display_only_with_vintage_before_knowable():
    import story_read as SR
    conn = sqlite3.connect(ROOT / "data" / "oil.db")
    pin = SR.priced_in(conn, "1990-08-02")
    assert pin["ovx_percentile"]["status"] == "unknown" and pin["cot_managed_money_net_percentile"]["status"] == "unknown"   # before the series start
    pin = SR.priced_in(conn, "2026-02-28")
    for f in ("ovx_percentile", "cot_managed_money_net_percentile"):
        x = pin[f]
        assert x["status"] == "ok" and x["vintage"] <= "2026-02-28" and x["as_of"] <= "2026-02-25" and 0 <= x["percentile"] <= 100 and x["n"] > 0
    assert pin["curve_front_spread_m1_m4"]["status"] == "unknown" and "2024-04-05" in pin["curve_front_spread_m1_m4"]["note"]   # stale series
    assert pin["curve_slope_1_3"]["status"] == "unknown"
    pin = SR.priced_in(conn, "2001-09-11")
    assert pin["curve_front_spread_m1_m4"]["status"] == "ok" and pin["curve_front_spread_m1_m4"]["vintage"] <= "2001-09-11"
    # never scored: the ledger's verdict code does not read it
    assert "priced_in" not in (ROOT / "src" / "ledger.py").read_text() and "priced_in" not in (ROOT / "src" / "materiality.py").read_text()
    assert "Amendment 5" in (ROOT / "CLAIM_LEDGER_REGISTRATION.md").read_text()


def test_a14_record_endpoint_and_feed_flags():
    from fastapi.testclient import TestClient
    import backend
    c = TestClient(backend.app)
    r = c.get("/api/record").json()
    assert r["n_events"] > 0 and r["n_reads"] > 0 and r["run_id"] and r["statuses"]["engine:G"] and r["audit"]["status"] in ("pending", "in progress", "done")
    assert "VALIDATED" not in json.dumps(r)
    f = c.get("/api/feed").json()
    for it in f.get("material", []) + f.get("in_line", []) + f.get("noise", []):
        assert set(it.get("flags") or []) <= {"LOUD_QUIET", "QUIET_LOUD"}


NODE = r"""
const {JSDOM} = require('jsdom'); const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8'); const data = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const dom = new JSDOM(html, {runScripts: 'outside-only', url: 'http://localhost/app'}); const w = dom.window;
w.fetch = () => Promise.reject(new Error('no network')); w.scrollTo = () => {};
w.eval(html.match(/<script>([\s\S]*)<\/script>/)[1].replace(/loadFeed\(\); loadRecord\(\);\s*/m, ''));
w.renderRecordBar(data.record); w.renderFeed(data.feed);
process.stdout.write(JSON.stringify({bar: w.document.querySelector('#recordbar').textContent, lq: w.document.querySelector('#loudquiet').textContent,
  ql: w.document.querySelector('#quietloud').textContent, all: w.document.body.textContent}));
"""


def test_a14_jsdom_record_bar_on_every_screen_and_blindspot_lists(tmp_path):
    if not shutil.which("node"):
        pytest.skip("node not installed")
    np_ = next((c for c in [os.environ.get("NODE_PATH"), str(ROOT / "tools" / "node_modules")] if c and (Path(c) / "jsdom").exists()), None)
    if not np_:
        pytest.skip("jsdom not found: npm install --prefix tools jsdom")
    from fastapi.testclient import TestClient
    import backend
    c = TestClient(backend.app)
    data = {"record": c.get("/api/record").json(), "feed": c.get("/api/feed").json()}
    (tmp_path / "d.json").write_text(json.dumps(data)); (tmp_path / "r.js").write_text(NODE)
    proc = subprocess.run(["node", str(tmp_path / "r.js"), str(ROOT / "src" / "app.html"), str(tmp_path / "d.json")], capture_output=True, text=True, timeout=120,
                          env={**os.environ, "NODE_PATH": np_})
    assert proc.returncode == 0, proc.stderr[-600:]
    out = json.loads(proc.stdout)
    r = data["record"]
    assert str(r["n_events"]) in out["bar"] and r["run_id"] in out["bar"] and r["statuses"]["engine:G"] in out["bar"] and "label audit" in out["bar"]
    assert out["lq"].strip() and out["ql"].strip()                                          # both lists render (items or the stated empty reason)
    assert "VALIDATED" not in out["all"]
    html = (ROOT / "src" / "app.html").read_text()
    assert html.index('id="recordbar"') < html.index('<main>')                               # above every screen


def test_a15_reader_schema_states_date_and_confidence_and_fallback_never_dates():
    import reader as R
    for sch in (R.STORY_SCHEMA, R.BATCH_SCHEMA["properties"]["items"]["items"]):
        assert "event_date" in sch["properties"] and "confidence" in sch["properties"]
    assert R._iso_or_none("2019-09-14") == "2019-09-14" and R._iso_or_none("today") is None and R._iso_or_none(None) is None
    conn = sqlite3.connect(ROOT / "data" / "oil.db")
    voc = R.vocab(conn)
    r = R.cage({"event_class": "sanctions", "event_date": "2018-05-08", "confidence": "high", "entities": [], "unmapped": [], "claims": []}, "x", voc)
    assert r["event_date"] == "2018-05-08" and r["confidence"] == "high"
    r = R.cage({"event_class": "sanctions", "event_date": "yesterday", "confidence": "certain", "entities": [], "unmapped": [], "claims": []}, "x", voc)
    assert r["event_date"] is None and r["confidence"] is None
    os.environ["RIPPLE_READER"] = "off"
    try:
        fb = R.read_headlines(["US reimposes sanctions on Iran oil"], conn=conn, use_cache=False)[0]
    finally:
        os.environ.pop("RIPPLE_READER", None)
    assert fb["event_date"] is None and fb["confidence"] == "fallback" and fb["reader"]["mode"] == "regex_fallback"
    assert "Amendment 6" in (ROOT / "CLAIM_LEDGER_REGISTRATION.md").read_text()
