"""retractions.py -- the one place that says which claims this project has withdrawn.

WHY THIS EXISTS. The same defect has now appeared six times: a claim is retracted or downgraded in
the prose, and the machine-readable file that asserts it is never updated. `edge_battery.json`
carried `severity_dose_response` as validated after PAPER_DRAFT §12.2 marked it RETRACTED;
`EVALUATION.md` asserted H1 held out of sample (since fixed); `signal_registry.json` carries
`h1_vix_conditioning` as **live** with "survives_bonferroni=True" after the paper and
`docs/red_team_1.md` downgraded it. `discovery.json`, `sowhat.json`, `validation_claims.json` and
`cross_chain.json` carry the same stale beliefs.

The prose is the record; the JSON is what other code reads. When they disagree, every consumer
downstream of the JSON is wrong and nothing notices. So:

  * the adjudication lives in ONE machine-readable place -- `data/evidentiary_bar.json`, the single
    evidentiary bar of `docs/red_team_1.md` R7 -- and this module reads it rather than restating it;
  * the paper's harder verdicts (an explicit RETRACTED, as against a DOWNGRADE) are recorded here
    with their section, because the paper is prose and cannot be parsed for a verdict reliably;
  * every file that publishes a belief consults this module before writing `validated`/`live`;
  * `tests/test_retraction_guard.py` fails the build if any belief file marks an adjudicated claim
    live, and separately fails if this module and the paper drift apart.

NOTHING IS DELETED. The convention is the one used for the propagation backbone
(`src/propagation_graph.py` RETRACTED_POINTER, Joe's Ruling 1, 2026-09-02): the row keeps its
numbers, its status changes, and a dated pointer to the retraction is appended. A retracted result's
diagnostics are part of the record.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
BAR = DATA / "evidentiary_bar.json"
PAPER = ROOT / "docs" / "PAPER_DRAFT.md"

# The date the single evidentiary bar was adjudicated (docs/red_team_1.md R7).
ADJUDICATED_ON = "2026-09-03"

# Claims the PAPER retracts outright, as against downgrading. A DOWNGRADE says "not validated";
# a RETRACTION says "withdrawn". Kept here with the section because prose cannot be parsed for a
# verdict, and `test_retraction_guard.py` asserts each string below still appears in the paper.
PAPER_RETRACTIONS = {
    "severity_dose_response": {
        "verdict": "RETRACTED",
        "section": "PAPER_DRAFT.md §12.2",
        "on": "2026-09-03",
        "evidence": "re-tested under a registration with verdict words fixed in advance: amplification "
                    "+2.071 [-4.067, +8.209], permutation p 0.269, inside a VIX-and-GPR-matched placebo; "
                    "the dose-response points the wrong way. Unit-of-dependence error: 36 overlapping "
                    "same-severity episodes counted as independent.",
        "paper_marker": "**Status: RETRACTED.**",
    },
}

# The same claim is named differently in different files. Every alias resolves to one canonical id,
# because a guard that only knows one spelling is a guard that misses five files.
ALIASES = {
    "h1": "H1_vix_oil",
    "h1_vix_oil": "H1_vix_oil",
    "h1_vix_conditioning": "H1_vix_oil",
    "h1_vix": "H1_vix_oil",
    "copper_growth": "copper_growth",
    "hy_credit_stress": "hy_credit_stress",
    "severity_dose_response": "severity_dose_response",
    "palladium_supply": "palladium_supply",
    "cc2_supply_gasoline_crack": "CC2_supply_gasoline_crack",
    "cc5_fertilizer_corn": "CC5_fertilizer_corn",
    "under_priced_risk_oos": "under_priced_risk_oos_MISPRICING",
    "under_priced_risk_oos_mispricing": "under_priced_risk_oos_MISPRICING",
}

# Words a belief file uses to mean "this is a current claim". Case-insensitive.
LIVE_WORDS = {"live", "validated", "holds", "confirmed", "true"}


def canonical(name):
    """Resolve a claim's spelling to its canonical id, or None if it is not an adjudicated claim."""
    if name is None:
        return None
    return ALIASES.get(str(name).strip().lower())


def adjudication():
    """The canonical verdict per claim, read from data/evidentiary_bar.json (never restated here).

    Returns {canonical_id: {"retier", "on", "reference", "verdict"}}. `verdict` is RETRACTED where the
    paper retracts outright, otherwise the bar's own retier (DOWNGRADE (SUGGESTIVE) and friends).
    """
    bar = json.loads(BAR.read_text())
    out = {}
    for claim, retier in (bar.get("summary") or {}).items():
        out[claim] = {
            "retier": retier,
            "verdict": retier,
            "on": ADJUDICATED_ON,
            "reference": "data/evidentiary_bar.json#/summary · docs/red_team_1.md R7 (the single evidentiary bar)",
        }
    for claim, rec in PAPER_RETRACTIONS.items():
        out.setdefault(claim, {})
        out[claim].update({"verdict": rec["verdict"], "on": rec["on"],
                           "reference": rec["section"], "evidence": rec["evidence"]})
    return out


def may_be_live(name):
    """False if this claim has been retracted or downgraded. Unknown claims are permitted -- this
    module is a retraction list, not an allow-list, and must not block a new hypothesis."""
    cid = canonical(name)
    return cid is None or cid not in adjudication()


def pointer(name):
    """The dated pointer to append to a retracted claim's note, in the propagation-graph convention."""
    cid = canonical(name)
    rec = adjudication().get(cid)
    if rec is None:
        return None
    return f"{rec['verdict']} {rec['on']}; {rec['reference']}"


def stamp(entry, name, live_keys=("validated", "live", "status", "current_verdict")):
    """Apply the adjudication to one belief entry IN PLACE, keeping its numbers and its history.

    Sets `retracted: true`, records `retier`, `retracted_on`, `retracted_reference`, and flips any
    live-flag to the honest value. Returns True if anything changed. Every original figure survives:
    a retracted result's diagnostics are part of the record, not evidence that revives it.
    """
    cid = canonical(name)
    rec = adjudication().get(cid)
    if rec is None:
        return False
    changed = False
    for k in live_keys:
        if k not in entry:
            continue
        v = entry[k]
        if isinstance(v, bool) and v:
            entry[k] = False; changed = True
        elif isinstance(v, str) and v.strip().lower() in LIVE_WORDS:
            entry[k] = rec["verdict"]; changed = True
    if not entry.get("retracted"):
        changed = True
    entry["retracted"] = True
    entry["retier"] = rec["retier"]
    entry["retracted_on"] = rec["on"]
    entry["retracted_reference"] = rec["reference"]
    return changed
