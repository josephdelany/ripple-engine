"""The guard: a retracted claim may not be marked live in any machine-readable belief file.

WHY. This defect has appeared six times. A claim is retracted or downgraded in the prose and the JSON
that asserts it is never updated, so every consumer downstream of the JSON keeps reading the retracted
belief and nothing notices:

  * `edge_battery.json` carried `severity_dose_response` as validated after PAPER_DRAFT §12.2 marked
    it **RETRACTED**, along with `copper_growth` and `hy_credit_stress`;
  * `EVALUATION.md` asserted H1 held out of sample (fixed before this guard existed);
  * `signal_registry.json` carried `h1_vix_conditioning` as **live** with "survives_bonferroni=True";
  * `discovery.json` labelled its VIX hit "already validated";
  * `validation_claims.json` carried H1 at `current_verdict: HOLDS`, `survives_bonferroni_5pct: true`;
  * `cross_chain.json` carried both adjudicated CC claims as validated.

Every one was found by a human reading a file. This test is the mechanism that finds the seventh.

DESIGN NOTE — why the scan is generic rather than a list of files. An allow-list of known belief files
would not have caught `validation_claims.json` or `cross_chain.json`, because nobody knew they carried
the claim. `test_no_belief_file_anywhere_marks_a_retracted_claim_live` walks EVERY `data/**/*.json`, so
a belief file invented tomorrow is covered without being registered here.
"""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import retractions as R          # noqa: E402

DATA = ROOT / "data"
PAPER = ROOT / "docs" / "PAPER_DRAFT.md"


# --------------------------------------------------------------------------- the record cannot drift
def test_the_adjudication_file_is_readable_and_non_empty():
    """Everything here keys off data/evidentiary_bar.json. If it goes missing the guard must fail loudly
    rather than silently pass by having nothing to check."""
    adj = R.adjudication()
    assert adj, "no adjudicated claims found -- evidentiary_bar.json missing or empty"
    assert "H1_vix_oil" in adj, "H1 is not in the adjudication; the single evidentiary bar changed shape"


def test_paper_retractions_still_appear_in_the_paper():
    """src/retractions.py hard-codes the paper's outright RETRACTIONS because prose cannot be parsed for
    a verdict. This asserts each one is still in the paper, so the module cannot drift from the record."""
    paper = PAPER.read_text()
    for claim, rec in R.PAPER_RETRACTIONS.items():
        assert rec["paper_marker"] in paper, (
            f"{claim}: retractions.py claims {PAPER.name} contains {rec['paper_marker']!r} and it does not. "
            "Either the paper changed or the module is stale -- reconcile before shipping.")
        section = rec["section"].split("§")[-1]
        assert f"### {section}" in paper or f"## {section}" in paper, \
            f"{claim}: {rec['section']} is not a section of the paper any more"


def test_severity_dose_response_is_retracted_not_merely_downgraded():
    """The paper's verdict is stronger than the bar's for this one, and the stronger verdict must win."""
    assert R.adjudication()["severity_dose_response"]["verdict"] == "RETRACTED"


# --------------------------------------------------------------------------- the guard itself
def _belief_files():
    return sorted(p for p in DATA.rglob("*.json") if p.is_file())


def _violations(obj, path, out):
    """Recursively find any place a retracted claim is asserted as live.

    Two shapes are checked, because belief files use both:
      A. a dict that names a claim AND carries a live flag -- {"hypothesis": "...", "validated": true}
      B. a list under a live-word key -- {"validated": [...]} or {"by_status": {"live": [...]}}
    """
    if isinstance(obj, dict):
        # shape A: this dict identifies a claim; check its own live flags
        named = None
        for k in ("hypothesis", "signal_id", "id", "hid", "claim", "name", "edge_id", "cc", "feature"):
            if isinstance(obj.get(k), str) and R.canonical(obj[k]):
                named = obj[k]
                break
        if named is not None and not R.may_be_live(named):
            for k, v in obj.items():
                if k in ("retier", "retracted", "retracted_on", "retracted_reference", "retraction_note",
                         "status", "current_verdict") and k != "status":
                    continue
                # NOTE: `survives_fdr` / `survives_bonferroni` are deliberately NOT live-flags. They are
                # statements about what the ORIGINAL test did, and the convention is that a retracted
                # entry keeps its figures. Flagging them would push toward deleting the record, which is
                # the opposite of what retraction means here. What must not survive is a claim of CURRENT
                # validity, which is what the keys below assert.
                if isinstance(v, bool) and v and k in ("validated", "live", "statistically_validated",
                                                       "holds", "is_validated", "confirmed"):
                    out.append((path + "/" + k, named, f"{k}=true"))
                elif isinstance(v, str) and v.strip().lower() in R.LIVE_WORDS and k in (
                        "status", "verdict", "current_verdict", "retier"):
                    out.append((path + "/" + k, named, f"{k}={v!r}"))
        # shape B: a live-word key holding claim names
        for k, v in obj.items():
            kl = k.strip().lower()
            if kl in R.LIVE_WORDS and isinstance(v, list):
                for item in v:
                    if isinstance(item, str) and not R.may_be_live(item):
                        out.append((path + "/" + k, item, f"listed under {k!r}"))
            _violations(v, path + "/" + k, out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _violations(v, f"{path}[{i}]", out)


def test_no_belief_file_anywhere_marks_a_retracted_claim_live():
    """THE GUARD. Walks every data/**/*.json; fails if any retracted or downgraded claim is asserted live."""
    bad = []
    for p in _belief_files():
        try:
            doc = json.loads(p.read_text())
        except (ValueError, OSError):
            continue                                   # not a JSON belief file; nothing to check
        found = []
        _violations(doc, "", found)
        for where, claim, how in found:
            bad.append(f"{p.relative_to(ROOT)}{where}: {claim!r} is {how}, but it is "
                       f"{R.adjudication()[R.canonical(claim)]['verdict']} "
                       f"({R.adjudication()[R.canonical(claim)]['reference']})")
    assert not bad, (
        "a retracted or downgraded claim is marked live in a machine-readable belief file:\n  "
        + "\n  ".join(bad)
        + "\n\nMark it with src/retractions.stamp() -- keep the figures, change the status, add the "
          "dated pointer. Do not delete the entry.")


def test_every_retracted_entry_kept_its_numbers():
    """Retraction marks, it does not erase. The propagation-graph convention (Joe's Ruling 1): the row
    keeps its numbers, its status changes, a dated pointer is appended."""
    eb = json.loads((DATA / "edge_battery.json").read_text())
    retracted = [e for e in eb["amplification"] if e.get("retracted")]
    assert retracted, "edge_battery has no retracted entries; the adjudication should have marked four"
    for e in retracted:
        assert e.get("amp") is not None and e.get("ci"), f"{e['hypothesis']}: figures were deleted, not marked"
        assert e.get("retracted_on") and e.get("retracted_reference"), \
            f"{e['hypothesis']}: retracted without a dated reference"


def test_the_guard_can_actually_fail():
    """A guard that cannot fail is not a guard. Both shapes must be caught."""
    shape_a = {"signals": [{"signal_id": "h1_vix_conditioning", "status": "live"}]}
    shape_b = {"validated": ["severity_dose_response"]}
    nested = {"by_status": {"live": ["h1_vix_conditioning"]}}
    for name, doc in (("A", shape_a), ("B", shape_b), ("nested", nested)):
        found = []
        _violations(doc, "", found)
        assert found, f"the guard failed to catch shape {name}: {doc}"
    # and it must NOT fire on an unadjudicated claim, or on a correctly-marked retraction
    clean = {"signals": [{"signal_id": "gold_safe_haven", "status": "live"},
                         {"signal_id": "h1_vix_conditioning", "status": "retracted",
                          "retracted_on": "2026-09-03", "retracted_reference": "x"}]}
    found = []
    _violations(clean, "", found)
    assert not found, f"the guard false-positived on a clean file: {found}"


# --------------------------------------------------------------------------- the generators must consult it
GENERATORS = {
    "src/signal_registry.py": "data/signal_registry.json",
    "src/edge_battery.py": "data/edge_battery.json",
}


@pytest.mark.parametrize("gen,out", sorted(GENERATORS.items()))
def test_the_generator_adjudicates_before_writing(gen, out):
    """Patching the JSON is cosmetic: these files are regenerated, so the WRITER must apply the
    adjudication or the next run restores the stale belief. This is a static check because running the
    generators writes to real tables in data/oil.db."""
    src = (ROOT / gen).read_text()
    assert "retractions" in src, (
        f"{gen} writes {out} but never consults src/retractions.py -- the next run will restore the "
        "retracted claim as live. Import it and stamp the entries before writing.")
    assert ("may_be_live" in src) or ("stamp(" in src), \
        f"{gen} imports retractions but does not call may_be_live() or stamp()"


def test_retractions_module_is_the_only_place_the_verdicts_live():
    """The adjudication is READ from data/evidentiary_bar.json, never restated in code. If someone
    hard-codes 'DOWNGRADE' verdicts into the module, the two can drift and the guard becomes decorative."""
    src = (ROOT / "src" / "retractions.py").read_text()
    body = src.split("def adjudication", 1)[1].split("def ", 1)[0]
    assert "BAR.read_text()" in body, "adjudication() must read data/evidentiary_bar.json, not restate it"
