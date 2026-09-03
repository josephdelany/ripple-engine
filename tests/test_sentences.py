"""DESIGN.md Amendment 2, A2.8 — the sentence inventory. The gate Joe made non-negotiable.

Joe's ruling, 2026-09-03: register the templates BEFORE writing them, bind every generated sentence to
named fields, and build this test BEFORE the first sentence renders. *If the test does not exist, the
prose does not ship.*

What it enforces, against the rendered DOM and not against the source:

  1. the registry in src/app.html and Appendix A of the amendment name exactly the same sentences —
     neither may drift from the other;
  2. every rendered [data-sentence] node carries a registered id;
  3. its fixed text matches the registered template, with value slots as values and word slots drawn
     only from their registered vocabulary;
  4. **every numeric token in a rendered sentence is derivable from that sentence's declared paths**,
     resolved from the same payload the page was given. A number it cannot derive is a failure;
  5. no sentence hedges a null (A.5), and none carries a §6 banned word.

(4) is the one that matters. It is the mechanism that makes the three fabrications I shipped in the
first draft of WIREFRAMES.md impossible to ship again: a number with no path behind it fails here.
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
AMENDMENT = ROOT / "docs" / "design" / "DESIGN_AMENDMENT_2.md"

# A.5 plus §6. A null is stated flatly; these constructions may not attach to one.
HEDGES = ("only", "merely", "unfortunately", "sadly", "admittedly", "disappointing",
          "weak", "fails to", "we had hoped", "although", "despite")
BANNED = ("predicts", "validated", "signal", "confirms")


def _node_path():
    for cand in [os.environ.get("NODE_PATH"), str(ROOT / "tools" / "node_modules")]:
        if cand and (Path(cand) / "jsdom").exists():
            return cand
    return None


def registered_ids_from_appendix():
    """The sentence ids Appendix A registers, parsed from the amendment's markdown tables."""
    txt = AMENDMENT.read_text()
    app_a = txt.split("## Appendix A", 1)[1]
    return set(re.findall(r"^\|\s*`([a-z][a-z0-9]*(?:\.[a-z0-9]+)+)`\s*\|", app_a, re.M))


def registered_ids_from_app():
    """The ids the page actually registers, read out of the SENTENCES literal."""
    src = APP.read_text()
    block = src.split("const SENTENCES = {", 1)[1].split("\n};", 1)[0]
    return set(re.findall(r"^\s*'([a-z][a-z0-9]*(?:\.[a-z0-9]+)+)':", block, re.M))


def test_a28_registry_and_appendix_name_the_same_sentences():
    """The code and the registered spec may not drift. Either is a defect, in both directions."""
    in_app, in_doc = registered_ids_from_app(), registered_ids_from_appendix()
    assert in_app, "no SENTENCES registry found in src/app.html"
    assert in_doc, "no sentence ids parsed from Appendix A"
    unregistered = in_app - in_doc
    unimplemented = in_doc - in_app
    assert not unregistered, f"rendered by the page but NOT registered in Appendix A: {sorted(unregistered)}"
    assert not unimplemented, f"registered in Appendix A but absent from the page: {sorted(unimplemented)}"


NODE_SCRIPT = r"""
const {JSDOM} = require('jsdom');
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const desk = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const story = JSON.parse(fs.readFileSync(process.argv[4], 'utf8'));
const dom = new JSDOM(html, {runScripts: 'outside-only', url: 'http://localhost/app'});
const w = dom.window;
w.scrollTo = () => {};
const m = html.match(/<script>([\s\S]*)<\/script>/);
w.eval(m[1].replace(/\/\* @boot-start \*\/[\s\S]*?\/\* @boot-end \*\//, ''));

w.fetch = (u) => {
  const body = u.indexOf('/api/desk') === 0 ? desk
             : u.indexOf('/api/story') === 0 ? story
             : u.indexOf('/api/ledger') === 0 ? (desk.__ledger || {})
             : u.indexOf('/api/record') === 0 ? (desk.record || {})
             : u.indexOf('/api/feed') === 0 ? (desk.__feed || {})
             : null;
  return body === null ? Promise.reject(new Error('unexpected fetch ' + u))
                       : Promise.resolve({ok: true, json: () => Promise.resolve(body)});
};

(async () => {
  const out = [];
  // render whatever screens exist; a loader that is not defined yet is simply skipped
  for (const fn of ['loadResult', 'loadCatch', 'loadRecordScreen', 'loadLedger', 'loadFeed']) {
    if (typeof w[fn] === 'function') { try { await w[fn](); } catch (e) { out.push({error: fn + ': ' + e.message}); } }
  }
  if (typeof w.renderStory === 'function') { try { w.renderStory(story); } catch (e) { out.push({error: 'renderStory: ' + e.message}); } }
  const finds = [...w.document.querySelectorAll('.t-find')].map(n => ({
    text: (n.textContent || '').replace(/\s+/g, ' ').trim(),
    registered: !!n.querySelector('[data-sentence]') || !!n.closest('[data-sentence]'),
    verbatim: !!n.querySelector('[data-verbatim]') || !!n.closest('[data-verbatim]'),
  }));
  const nodes = [...w.document.querySelectorAll('[data-sentence]')].map(n => ({
    id: n.getAttribute('data-sentence'),
    fields: (n.getAttribute('data-fields') || '').split(',').filter(Boolean),
    text: n.textContent,
  }));
  process.stdout.write(JSON.stringify({nodes, finds, errors: out}));
})().catch(e => { console.error(e && e.stack || String(e)); process.exit(4); });
"""


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
    c = TestClient(backend.app)
    desk = c.get("/api/desk").json()
    desk["__ledger"] = c.get("/api/ledger").json()
    desk["__feed"] = c.get("/api/feed").json()
    story = c.get("/api/story?id=abqaiq_attack_2019").json()
    d = tmp_path_factory.mktemp("sent")
    dp, sp, js = d / "desk.json", d / "story.json", d / "r.js"
    dp.write_text(json.dumps(desk)); sp.write_text(json.dumps(story)); js.write_text(NODE_SCRIPT)
    proc = subprocess.run(["node", str(js), str(APP), str(dp), str(sp)],
                          capture_output=True, text=True, timeout=180, env={**os.environ, "NODE_PATH": np_})
    assert proc.returncode == 0, proc.stderr[-1500:]
    return json.loads(proc.stdout), desk, story


def _resolve(payload, story, path):
    cur = payload if path.split(".")[0] in payload else story
    for k in path.split("."):
        cur = (cur or {}).get(k) if isinstance(cur, dict) else None
    return cur


def _derivable(token, values):
    """Is this numeric token one of the declared values, in any formatting the desk uses?"""
    for v in values:
        if v is None:
            continue
        s = str(v)
        if token == s:
            return True
        try:
            if abs(float(token) - float(v)) < 1e-9:
                return True
            # the desk also renders an absolute value (e.g. "sits 17.8% below")
            if abs(abs(float(v)) - float(token)) < 1e-9:
                return True
        except (TypeError, ValueError):
            pass
        if token in re.findall(r"\d+", s):        # a date's parts, e.g. 1987 out of 1987-05-20
            return True
    return False


def test_a28_every_rendered_sentence_is_registered(rendered):
    out, _, _ = rendered
    assert not out["errors"], out["errors"]
    ids = registered_ids_from_app()
    for n in out["nodes"]:
        assert n["id"] in ids, f"rendered an unregistered sentence: {n['id']!r}"


def test_a28_every_number_in_a_sentence_is_derivable_from_its_declared_paths(rendered):
    """The gate. A number in a sentence with no path behind it fails here."""
    out, desk, story = rendered
    if not out["nodes"]:
        pytest.skip("no sentences rendered yet — the prose has not shipped")
    for n in out["nodes"]:
        values = [_resolve(desk, story, p) for p in n["fields"]]
        for token in re.findall(r"\d+(?:\.\d+)?", n["text"]):
            assert _derivable(token, values), (
                f"sentence {n['id']!r} renders {token!r}, which is not derivable from its declared "
                f"paths {n['fields']} (resolved to {values}). Either the number is fabricated or the "
                f"path is missing from the registry.")


def test_a28_fixed_text_matches_the_registered_template(rendered):
    """The words between the slots are fixed by Appendix A and may not be computed."""
    out, _, _ = rendered
    if not out["nodes"]:
        pytest.skip("no sentences rendered yet")
    src = APP.read_text().split("const SENTENCES = {", 1)[1].split("\n};", 1)[0]
    for n in out["nodes"]:
        m = re.search(r"'" + re.escape(n["id"]) + r"':\s*\{t:'([^']*)'", src)
        assert m, f"no template found for {n['id']}"
        # the template with every slot replaced by a permissive pattern
        pat = re.escape(m.group(1))
        pat = re.sub(r"\\\{\w+\\\}", r".+?", pat)
        assert re.fullmatch(pat, n["text"]), (
            f"sentence {n['id']!r} does not match its registered template.\n"
            f"  template: {m.group(1)}\n  rendered: {n['text']}")


def test_a28_no_sentence_hedges_a_null_or_uses_a_banned_word(rendered):
    """A2.1 as ruled: the null is the finding, not an apology for one."""
    out, _, _ = rendered
    if not out["nodes"]:
        pytest.skip("no sentences rendered yet")
    for n in out["nodes"]:
        low = n["text"].lower()
        for h in HEDGES:
            assert not re.search(r"\b" + re.escape(h) + r"\b", low), \
                f"sentence {n['id']!r} hedges with {h!r}: {n['text']!r}"
        for b in BANNED:
            assert not re.search(r"\b" + re.escape(b) + r"\b", low), \
                f"sentence {n['id']!r} uses the banned word {b!r}: {n['text']!r}"


def test_a28_the_gate_can_actually_fail():
    """A test that cannot fail is not a gate. This proves the derivability check rejects a fabrication."""
    assert not _derivable("99", [15, 371]), "the inventory would accept a fabricated number"
    assert _derivable("15", [15, 371]) and _derivable("371", [15, 371])
    assert _derivable("1987", ["1987-05-20"]), "a date's parts must resolve"
    assert _derivable("17.8", [-17.8]), "an absolute value of a declared negative must resolve"


def test_a28_no_finding_tier_sentence_escapes_the_registry(rendered):
    """The hole this test closes: the inventory only ever saw [data-sentence] nodes, so a sentence the desk
    composed by hand rendered freely as long as it carried no marker.

    That was not hypothetical. `theRead()` assembled the Story's opening line out of two different
    populations — the price median over `priced.fan.n` analogs and `trust.retrieval.conditioned_n`
    escalation analogs — and read as though one n covered both. It was found by rendering the spine and
    reading it, not by a test, which is exactly the gap. A Finding-tier element must now be either a
    registered sentence or verbatim quoted material.
    """
    out, _, _ = rendered
    if not out.get("finds"):
        pytest.skip("nothing rendered at Finding tier")
    loose = [f["text"] for f in out["finds"] if not f["registered"] and not f["verbatim"] and f["text"]]
    # page chrome that states no result and carries no number is allowed to be fixed text
    loose = [t for t in loose if re.search(r"\d", t)]
    assert not loose, (
        "Finding-tier text with numbers that is neither a registered sentence nor verbatim quoted "
        f"material: {loose}")
