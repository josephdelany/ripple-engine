"""DESIGN.md §5 + Amendment 2 A2.6b — the record bar's verdicts carry §2 colour, read from the interval.

§5: the record bar's two verdicts are "in Evidence tier **with their colour from §2**". They were rendered
as plain text, which cannot express the three states §2 registers.

It stopped being cosmetic when walk_20260903T052633Z replaced walk_20260903T003422Z. Escalation against
climatology moved from skill −0.097, CI [−0.180, −0.018] — excluding zero, the amber "engine worse" state —
to skill −0.084, CI [−0.175, +0.004] — crossing zero, the neutral state. Price stayed at −0.074,
CI [−0.140, −0.021], which still excludes zero and stays amber.

Both estimates are negative. A bar that coloured by the SIGN of the estimate would call both amber and be
wrong about escalation; that is the specific error this file exists to prevent, and
`test_a26b_colour_is_not_the_sign_of_the_estimate` pins it against the live numbers.
"""
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
APP = ROOT / "src" / "app.html"

NODE_SCRIPT = r"""
const {JSDOM} = require('jsdom');
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const desk = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const dom = new JSDOM(html, {runScripts: 'outside-only', url: 'http://localhost/app'});
const w = dom.window;
w.scrollTo = () => {};
w.eval(html.match(/<script>([\s\S]*)<\/script>/)[1].replace(/\/\* @boot-start \*\/[\s\S]*?\/\* @boot-end \*\//, ''));
w.fetch = (u) => {
  const b = u.indexOf('/api/desk') === 0 ? desk
          : u.indexOf('/api/record') === 0 ? desk.record : null;
  return b === null ? Promise.reject(new Error('x'))
                    : Promise.resolve({ok: true, json: () => Promise.resolve(b)});
};
(async () => {
  await w.loadRecord();
  await w.loadResult();
  const fields = {};
  for (const sp of w.document.querySelectorAll('#recordbar span')) {
    const lab = sp.querySelector('.t-prov'), val = sp.querySelector('.t-ev');
    if (lab && val) {
      const svg = sp.querySelector('svg.iv');
      fields[lab.textContent.trim()] = {
        text: val.textContent.trim(),
        cls: svg ? svg.getAttribute('class') : '',        // the SHARED interval component's own class
        zero: svg ? svg.querySelectorAll('line.zero').length : 0,
      };
    }
  }
  // the walk forest on the landing screen, row state by row label
  const rows = [...w.document.querySelectorAll('#result .forest tr[data-state]')].map(tr => ({
    label: tr.querySelector('.lab') ? tr.querySelector('.lab').textContent.trim() : '',
    state: tr.getAttribute('data-state'),
  }));
  process.stdout.write(JSON.stringify({fields, rows, runId: desk.walk.run_id}));
})().catch(e => { console.error(e && e.stack || String(e)); process.exit(4); });
"""


def _node_path():
    for c in [os.environ.get("NODE_PATH"), str(ROOT / "tools" / "node_modules")]:
        if c and (Path(c) / "jsdom").exists():
            return c
    return None


@pytest.fixture(scope="module")
def rendered(tmp_path_factory):
    if not shutil.which("node"):
        pytest.skip("node not installed")
    np_ = _node_path()
    if not np_:
        pytest.skip("jsdom not found: npm install --prefix tools jsdom")
    if not (ROOT / "data" / "oil.db").exists():
        pytest.skip("data/oil.db absent")
    from fastapi.testclient import TestClient
    import backend
    desk = TestClient(backend.app).get("/api/desk").json()
    d = tmp_path_factory.mktemp("bar")
    dp, js = d / "desk.json", d / "r.js"
    dp.write_text(json.dumps(desk)); js.write_text(NODE_SCRIPT)
    proc = subprocess.run(["node", str(js), str(APP), str(dp)], capture_output=True, text=True,
                          timeout=180, env={**os.environ, "NODE_PATH": np_})
    assert proc.returncode == 0, proc.stderr[-1200:]
    return json.loads(proc.stdout), desk


def _state_from_interval(ci):
    lo, hi = min(ci), max(ci)
    if lo <= 0 <= hi:
        return "crosses"
    return "worse" if hi < 0 else "better"


def test_a26b_both_verdicts_are_coloured_at_all(rendered):
    """§5: the two verdicts carry their colour from §2. Plain text is the defect this replaced."""
    out, _ = rendered
    for k in ("G", "P"):
        assert k in out["fields"], f"the record bar has no {k} field"
        cls = out["fields"][k]["cls"]
        assert re.search(r"\biv-(crosses|worse|better|insufficient)\b", cls), \
            f"{k} carries no §2 verdict colour: class={cls!r}"
        assert out["fields"][k]["zero"] == 1, f"{k}'s verdict mark must draw the zero rule (§2)"


def test_a26b_colour_matches_the_interval_not_the_status_string(rendered):
    """The colour is computed from the CI, through the same rule the forest rows use."""
    out, desk = rendered
    for k, task in (("G", "G"), ("P", "P")):
        ci = (((desk["walk"].get(task) or {}).get("climatology")) or {}).get("ci95")
        assert ci, f"no climatology interval for {task}"
        assert f"iv-{_state_from_interval(ci)}" in out["fields"][k]["cls"], \
            f"{k}: interval {ci} implies {_state_from_interval(ci)}, bar says {out['fields'][k]['cls']!r}"


def test_a26b_colour_is_not_the_sign_of_the_estimate(rendered):
    """The specific error A2.6b names. On this run BOTH climatology skills are negative, and yet the two
    verdicts are in different §2 states — so a bar keyed to the sign would be wrong about escalation."""
    out, desk = rendered
    g = (desk["walk"]["G"] or {})["climatology"]
    p = (desk["walk"]["P"] or {})["climatology"]
    assert g["skill"] < 0 and p["skill"] < 0, "precondition changed: both skills were negative on this run"
    gs, ps = _state_from_interval(g["ci95"]), _state_from_interval(p["ci95"])
    if gs == ps:
        pytest.skip(f"both verdicts are in the same state ({gs}); this test needs them to differ")
    assert f"iv-{gs}" in out["fields"]["G"]["cls"] and f"iv-{ps}" in out["fields"]["P"]["cls"]
    # and the state that differs is the one the interval decides, not the sign
    assert gs == "crosses", f"escalation's interval {g['ci95']} should cross zero on this run"
    assert ps == "worse", f"price's interval {p['ci95']} should exclude zero on this run"


def test_a26b_the_forest_row_agrees_with_the_bar(rendered):
    """One predicate, two surfaces: the landing screen's forest row and the record bar must not disagree."""
    out, desk = rendered
    row = next((r for r in out["rows"] if "escalation vs climatology" in r["label"]), None)
    if row is None:
        pytest.skip("the escalation-vs-climatology row is not on the landing screen")
    ci = desk["walk"]["G"]["climatology"]["ci95"]
    assert row["state"] == _state_from_interval(ci), (row, ci)
    assert f"iv-{row['state']}" in out["fields"]["G"]["cls"], \
        f"forest row says {row['state']!r} and the record bar says {out['fields']['G']['cls']!r}"


def test_a26b_the_desk_reads_the_current_run(rendered):
    """The desk renders whatever summary.json holds; this pins that it is not caching an older run."""
    out, desk = rendered
    from pathlib import Path as _P
    on_disk = json.loads((_P(ROOT) / "data" / "walk_forward" / "summary.json").read_text())["run_id"]
    assert out["runId"] == on_disk, f"desk served {out['runId']}, summary.json holds {on_disk}"


def test_a26b_the_bar_reuses_the_shared_component_and_does_not_invent_a_second_language():
    """§2 registers ONE absence language, "so it is used identically everywhere".

    My first cut of this gave the bar its own `.v-worse` / `.v-better` text-colour rules. That is exactly
    the duplicate the spec already outlawed once — tests/test_design_spec.py records that the propagation
    band "carried a private .ib/.v-* implementation of the same idea" and was made to consume the shared
    component instead. The bar draws the same `interval()` mark as every other verdict on the desk, so §5's
    "colour from §2" is satisfied by §2's own component and there are still exactly two amber/green rules
    in the stylesheet.
    """
    html = APP.read_text()
    assert ".v-worse{" not in html and ".v-better{" not in html, \
        "a second set of verdict-colour rules is a second absence language"
    bar = html.split("function renderRecordBar", 1)[1].split("\nasync function loadRecord", 1)[0]
    assert "interval(" in bar and "verdictOf(" in bar, \
        "the record bar must draw the shared interval component, keyed by verdictOf"
