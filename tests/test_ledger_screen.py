"""DESIGN.md §3.3 — the Ledger screen, rendered under jsdom against the real /api/ledger payload.

The screen's defect was that it "reads as broken": rows of Uncheckable and boards at zero, all honest and
all looking like failure. These assertions pin the four rules §3.3 gives, plus the §1/§2 obligations that
apply to the numbers it shows:

  - it leads with a Finding-tier sentence, computed, never an empty region                          §3.3 / §1
  - uncheckable claims collapse behind their count -- logged, not displayed                         §3.3 [T]
  - a board with nothing resolved shows the HORIZON, not a zero                                     §3.3 [T]
  - reader accuracy stays visible and labelled unaudited                                            §3.3
  - every proportion carries an interval, every chart draws its zero rule, and a rate below the
    registered minimum is hatched rather than coloured                                              §1 / §2

jsdom is looked up via NODE_PATH then tools/node_modules; absent -> skipped with the install line, never
faked (Amendment 1 A1.3: the static half of the spec lives in tests/test_design_spec.py and runs everywhere).
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

# Render loadLedger() twice: once against the ledger as it stands, once against the same payload with every
# resolution removed, which is the empty-board state §3.3 legislates for. The second is the real response
# shape with a field emptied -- no invented rows.
NODE_SCRIPT = r"""
const {JSDOM} = require('jsdom');
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const payload = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const dom = new JSDOM(html, {runScripts: 'outside-only', url: 'http://localhost/app'});
const w = dom.window;
w.scrollTo = () => {};
const m = html.match(/<script>([\s\S]*)<\/script>/);
const BOOT = /\/\* @boot-start \*\/[\s\S]*?\/\* @boot-end \*\//;
if (!BOOT.test(html)) { console.error('BOOT MARKER MISSING'); process.exit(3); }
w.eval(m[1].replace(BOOT, ''));

function serve(obj){
  w.fetch = (u) => u.indexOf('/api/ledger') === 0
    ? Promise.resolve({ok: true, json: () => Promise.resolve(obj)})
    : Promise.reject(new Error('unexpected fetch ' + u));
}
function snap(){
  const el = w.document.querySelector('#ledger');
  const tables = [...el.querySelectorAll('table')].map(t => t.textContent);
  const det = el.querySelector('details');
  return {
    html: el.innerHTML,
    text: el.textContent,
    find: [...el.querySelectorAll('.t-find')].map(n => n.textContent),
    empties: [...el.querySelectorAll('.empty')].map(n => n.textContent),
    details: det ? det.textContent : '',
    detailsSummary: det ? det.querySelector('summary').textContent : '',
    tablesOutsideDetails: [...el.querySelectorAll('table')].filter(t => !t.closest('details')).map(t => t.textContent),
    zeroLines: el.querySelectorAll('svg.iv line.zero').length,
    intervals: el.querySelectorAll('svg.iv').length,
    hatched: el.querySelectorAll('svg.iv .iv-hatch').length,
    coloured: el.querySelectorAll('svg.iv-better .span, svg.iv-worse .span').length,
    captions: [...el.querySelectorAll('.cap')].map(n => n.textContent),
    verbatim: [...el.querySelectorAll('[data-verbatim]')].map(n => n.textContent),
  };
}

(async () => {
  const out = {};
  serve(payload);
  await w.loadLedger();
  out.live = snap();

  const empty = JSON.parse(JSON.stringify(payload));
  empty.record_vs_narrative = {resolved: 0, with_record_call: 0, record_right: 0, narrative_right: 0,
                               record_only_right: 0, narrative_only_right: 0, status: 'seeding'};
  empty.sources = [];
  serve(empty);
  await w.loadLedger();
  out.empty = snap();
  process.stdout.write(JSON.stringify(out));
})().catch(e => { console.error(e && e.stack || String(e)); process.exit(4); });
"""

BANNED = ("predicts", "validated", "signal", "confirms")


def _node_path():
    for cand in [os.environ.get("NODE_PATH"), str(ROOT / "tools" / "node_modules")]:
        if cand and (Path(cand) / "jsdom").exists():
            return cand
    return None


@pytest.fixture(scope="module")
def rendered(tmp_path_factory):
    if not shutil.which("node"):
        pytest.skip("node not installed")
    np_ = _node_path()
    if not np_:
        pytest.skip("jsdom not found: npm install --prefix tools jsdom  (or set NODE_PATH to a node_modules with jsdom)")
    if not (ROOT / "data" / "oil.db").exists():
        pytest.skip("data/oil.db absent: /api/ledger needs the corpus")
    from fastapi.testclient import TestClient
    import backend
    payload = TestClient(backend.app).get("/api/ledger").json()
    tmp = tmp_path_factory.mktemp("ledger")
    pp = tmp / "ledger.json"; pp.write_text(json.dumps(payload))
    js = tmp / "render.js"; js.write_text(NODE_SCRIPT)
    proc = subprocess.run(["node", str(js), str(ROOT / "src" / "app.html"), str(pp)],
                          capture_output=True, text=True, timeout=180, env={**os.environ, "NODE_PATH": np_})
    assert proc.returncode == 0, proc.stderr[-1200:]
    return json.loads(proc.stdout), payload


def test_design_33_leads_with_a_computed_finding_line(rendered):
    """§3.3 'Lead with the checkable' + §1: one Finding-tier sentence, and it states the board's real result."""
    out, payload = rendered
    find = out["live"]["find"]
    assert len(find) == 1 and find[0].strip(), "the Ledger must open on exactly one Finding-tier line"
    rvn = payload["record_vs_narrative"]
    # the sentence is computed from the board, so it carries the board's own n
    assert str(rvn["with_record_call"]) in find[0]
    assert len(find[0].split()) <= 20, f"Finding tier is a sentence, not a paragraph: {find[0]!r}"
    # the counts line names what was logged, checkable and resolved -- with its receipt path in Provenance
    assert "claims logged" in out["live"]["text"] and "checkable" in out["live"]["text"]
    assert "data/ledger/claims.jsonl" in out["live"]["text"]


def test_design_33_uncheckable_claims_collapse_behind_their_count(rendered):
    """§3.3 [T]: 'Uncheckable claims collapse behind their count. They are logged, not displayed.'"""
    out, payload = rendered
    unch = [r for r in payload["recent"] if not r.get("checkable")]
    if not unch:
        pytest.skip("no uncheckable claims in the current ledger")
    summary = out["live"]["detailsSummary"]
    assert str(len(unch)) in summary and "uncheckable" in summary.lower(), summary
    # every uncheckable claim's text sits inside the collapsed region, and none of it is in the open table
    open_text = " ".join(out["live"]["tablesOutsideDetails"])
    for r in unch[:6]:
        t = (r.get("text") or "")[:40]
        if t:
            assert t not in open_text, f"uncheckable claim displayed inline: {t!r}"
            assert t in out["live"]["details"], f"uncheckable claim not logged in the collapsed region: {t!r}"


def test_design_33_empty_board_shows_a_horizon_not_a_zero(rendered):
    """§3.3 [T]: 'A scoreboard with no resolved claims shows the horizon, not a zero.'"""
    out, _ = rendered
    empty = out["empty"]
    assert empty["empties"], "an unscored board must render an empty state, not three cards reading zero"
    why = " ".join(empty["empties"])
    assert "horizon" in why.lower(), why
    # and it must not print a fabricated scoreboard of zeros
    assert "Record right — 0 of 0" not in empty["text"]
    assert empty["find"] and empty["find"][0].strip(), "the empty board still leads with a Finding-tier line"


def test_design_33_reader_accuracy_stays_visible_and_labelled(rendered):
    """§3.3: 'Reader accuracy stays visible, labelled unaudited gold.'"""
    out, payload = rendered
    text = out["live"]["text"]
    label = (payload.get("reader_eval") or {}).get("label") or ""
    assert "unaudited" in (label + text).lower(), "the reader's own accuracy is shown, and never unlabelled"
    assert "data/reader_eval/score.json" in text, "§6: the number's file is named on the screen"


def test_design_1_and_2_every_rate_carries_an_interval_and_a_zero_rule(rendered):
    """§1: a proportion appears with its interval or not at all. §2: the zero rule is always drawn."""
    out, payload = rendered
    live = out["live"]
    n_rows = 3 + len(payload.get("sources") or [])          # three boards + one row per source
    assert live["intervals"] >= n_rows, (live["intervals"], n_rows)
    assert live["zeroLines"] == live["intervals"], "every interval draws its zero rule (§2, no exceptions)"
    assert live["captions"], "§2: every null gets a caption in plain words, not a symbol"
    # the board says in words what its zero rule means, because here it is a coin flip and not a null effect
    assert "coin flip" in live["text"]


def test_design_2_thin_sources_are_hatched_never_coloured(rendered):
    """§2: 'Insufficient != null. A cell with too little data is hatched, never coloured, and labelled.'"""
    out, payload = rendered
    thin = [s for s in (payload.get("sources") or []) if s["n"] < 8]
    if not thin:
        pytest.skip("every source has reached the registered minimum")
    live = out["live"]
    assert live["hatched"] >= len(thin), (live["hatched"], len(thin))
    assert any("insufficient" in c.lower() for c in live["captions"]), live["captions"][:3]
    # a hatched row never also carries a verdict colour
    assert live["coloured"] <= live["intervals"] - live["hatched"]


def test_design_6_no_word_stronger_than_the_record_outside_a_verbatim_node(rendered):
    """§6 + Amendment 1 A1.2: absolute ban on the desk's own strings; quoted material is inventoried."""
    out, _ = rendered
    for key in ("live", "empty"):
        snap = out[key]
        quoted = " ".join(snap["verbatim"]).lower()
        text = snap["text"].lower()
        for w in BANNED:
            if w in text:
                # every occurrence must be inside a data-verbatim node
                assert w in quoted, f"{key}: the desk wrote a banned word itself: {w!r}"
        assert "validated" not in text.replace("unvalidated", "")
