"""Brief A-3: the desk page (src/app.html) renders section 5 from trust.walk_forward as the API returns it.
Real story payloads for september_11_attacks_2001 and hormuz_closure_2026 go through renderStory() under jsdom;
the rendered text must be non-empty, carry the run_id and the two §7 statuses verbatim, and say VALIDATED nowhere.
jsdom is looked up via NODE_PATH, then tools/node_modules; absent -> skipped with the install line, never faked."""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
EVENTS = ("september_11_attacks_2001", "hormuz_closure_2026")

NODE_SCRIPT = r"""
const {JSDOM} = require('jsdom');
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const stories = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const dom = new JSDOM(html, {runScripts: 'outside-only', url: 'http://localhost/app'});
const w = dom.window;
w.fetch = () => Promise.reject(new Error('no network in the render check'));
w.scrollTo = () => {};
const m = html.match(/<script>([\s\S]*)<\/script>/);
const BOOT = /\/\* @boot-start \*\/[\s\S]*?\/\* @boot-end \*\//;
if (!BOOT.test(html)) { console.error('BOOT MARKER MISSING: the page must emit @boot-start/@boot-end for the harness to strip'); process.exit(3); }
w.eval(m[1].replace(BOOT, ''));            // define the page functions without the network bootstrap
const out = {};
for (const [id, s] of Object.entries(stories)) {
  w.renderStory(s);
  const sec = [...w.document.querySelectorAll('#story h2')].find(h => h.textContent.startsWith('5 ·'));
  out[id] = {text: w.document.querySelector('#story').textContent, section5: sec ? sec.parentElement.textContent : ''};
}
process.stdout.write(JSON.stringify(out));
"""


def _node_path():
    for cand in [os.environ.get("NODE_PATH"), str(ROOT / "tools" / "node_modules")]:
        if cand and (Path(cand) / "jsdom").exists():
            return cand
    return None


def test_a3_section5_renders_trust_from_the_api_under_jsdom(tmp_path):
    if not shutil.which("node"):
        pytest.skip("node not installed")
    np_ = _node_path()
    if not np_:
        pytest.skip("jsdom not found: npm install --prefix tools jsdom  (or set NODE_PATH to a node_modules with jsdom)")
    from fastapi.testclient import TestClient
    import backend
    c = TestClient(backend.app)
    stories = {e: c.get(f"/api/story?id={e}").json() for e in EVENTS}
    for e, s in stories.items():
        assert s["trust"]["walk_forward"]["run_id"], e
    sp = tmp_path / "stories.json"; sp.write_text(json.dumps(stories))
    js = tmp_path / "render.js"; js.write_text(NODE_SCRIPT)
    proc = subprocess.run(["node", str(js), str(ROOT / "src" / "app.html"), str(sp)], capture_output=True, text=True, timeout=120,
                          env={**os.environ, "NODE_PATH": np_})
    assert proc.returncode != 3, "the page no longer emits the @boot-start/@boot-end marker the harness strips by"
    assert proc.returncode == 0, proc.stderr[-800:]
    out = json.loads(proc.stdout)
    summary = json.loads((ROOT / "data" / "walk_forward" / "summary.json").read_text())
    rules = summary["verdict"]["rules"]
    for e in EVENTS:
        text, sec = out[e]["text"], out[e]["section5"]
        assert text.strip() and sec.strip(), e                                   # non-empty render
        wf = stories[e]["trust"]["walk_forward"]
        assert wf["run_id"] in sec and summary["run_id"] == wf["run_id"], e
        assert rules["engine:G"]["status"] in sec and rules["engine:P"]["status"] in sec, e   # the two §7 statuses verbatim
        for m in ("G Brier skill vs climatology", "P CRPS skill vs climatology", "Permutation p"):
            assert m in sec, (e, m)
        assert "VALIDATED" not in text, e
        assert "retired" in text and "IES-90" in text, e
    assert "VALIDATED" not in (ROOT / "src" / "app.html").read_text()
