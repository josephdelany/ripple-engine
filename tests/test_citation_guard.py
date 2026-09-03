"""Session I -- the citation guard over the five published documents.

The figures got a run-id assertion so a superseded run goes RED rather than quietly
stale (tests/test_figures_paper.py). The prose had no such guard, and the prose is
where the damage lands: after a re-run overwrites data/walk_forward/summary.json,
nobody can hand-check 1,600 lines of published text, and a wrong number that the file
does not admit to is the worst defect this project can ship.

These tests do three things:

  1. RUN IDS ARE CURRENT. summary.json owns the run id; delta_experiment.json carries
     derived_from_run as a foreign key to it. When B's Amendment 4 re-run lands, both
     move and this goes red, naming the superseded object.
  2. EVERY NUMBER STILL EXISTS. Every claim the inventory recorded as being in the
     record is re-resolved against the LIVE files. A published −0.097 that is no
     longer anywhere in summary.json fails here, naming document, line and number.
  3. UNSOURCED HAS NOT GROWN. The 31 numbers we cannot trace are reported, not
     fixed -- but a NEW untraceable number entering the prose is red.

What these tests do NOT claim: that a resolved number is cited from the path it
matched. See src/citation_guard.py -- this is an existence and staleness guard.

DB-free: committed JSON and Markdown only.
"""
import json
from pathlib import Path

import pytest

import citation_guard as cg
import figures_paper as fp

ROOT = Path(__file__).resolve().parent.parent
INVENTORY = ROOT / "docs" / "citation_inventory.json"
REGENERATE = "regenerate with: python3 src/citation_guard.py"


@pytest.fixture(scope="module")
def inventory():
    if not INVENTORY.exists():
        pytest.skip(f"docs/citation_inventory.json absent; {REGENERATE}")
    return json.loads(INVENTORY.read_text())


@pytest.fixture(scope="module")
def record():
    return cg.load_record()


# --- 1. the run the prose is standing on -------------------------------------

def test_citation_guard_run_ids_are_current(inventory, record):
    """The published documents quote a run. RED when that run is superseded.

    This is the whole point of the file. It is expected to fail the moment the
    Amendment 4 re-run lands -- that failure is the signal to re-read the prose,
    not a bug to be silenced.
    """
    live = {r["path"]: r["run_id"] for r in record}
    stale = [(r["path"], r["run_id"], live.get(r["path"]))
             for r in inventory["record"]
             if r["run_key"] and live.get(r["path"]) != r["run_id"]]
    assert not stale, (
        "the documents were inventoried against a run that is no longer current:\n"
        + "\n".join(f"  {p}: inventory says {was}, the file now says {now}"
                    for p, was, now in stale)
        + f"\nEvery number quoted from that run must be re-checked. {REGENERATE}")


def test_citation_guard_derived_objects_agree_with_the_walk(record):
    """delta_experiment.json (§11) carries derived_from_run. It must point at the
    walk that is actually published, or §11 describes a run §8 does not."""
    current = cg.current_run_id(record)
    for r in record:
        if r["run_key"] and r["path"] != "data/walk_forward/summary.json":
            assert r["run_id"] == current, (
                f"{r['path']} says it derives from {r['run_id']}, but the published "
                f"walk is {current}. The documents quote both as one result.")


def test_citation_guard_inventory_run_id_matches_the_live_walk(inventory, record):
    assert inventory["current_run_id"] == cg.current_run_id(record), (
        f"docs/citation_inventory.json was built against run "
        f"{inventory['current_run_id']}; the tree now publishes "
        f"{cg.current_run_id(record)}. {REGENERATE}")


# --- 2. every number still exists in the record ------------------------------

def test_citation_guard_every_in_record_claim_still_resolves(inventory, record):
    """A number that has silently stopped existing anywhere in the record.

    Covers RESOLVED and AMBIGUOUS alike: both were found in the record when the
    inventory was built, so both are evidence that the prose matched the data. If a
    re-run moves the value, it will be found nowhere and this names it.
    """
    ordered = [(r["path"], r["lookup"]) for r in record]
    gone = []
    for c in inventory["claims"]:
        if c["status"] not in ("RESOLVED", "AMBIGUOUS"):
            continue
        primary, _ = cg.resolve(c, ordered)
        if primary is None:
            gone.append(f"  {c['document']}:{c['line']}  {c['raw']}  |  "
                        f"{c['context'][:90]}")
    assert not gone, (
        f"{len(gone)} published number(s) are no longer anywhere in the declared "
        f"record. The prose says something the data no longer says:\n"
        + "\n".join(gone[:40])
        + (f"\n  ... and {len(gone) - 40} more" if len(gone) > 40 else ""))


def test_citation_guard_derived_claims_still_recompute(inventory, record):
    """A DERIVED number is only allowed to stand while its formula reproduces it."""
    objs = {r["path"]: r["obj"] for r in record}
    broken = []
    for c in inventory["claims"]:
        if c["status"] != "DERIVED":
            continue
        if cg.match_derived(c, objs) is None:
            broken.append(f"  {c['document']}:{c['line']}  {c['raw']}  ({c['why']})")
    assert not broken, (
        "a derived number no longer follows from the record:\n" + "\n".join(broken))


def test_citation_guard_registered_exceptions_still_hold():
    """The one number that legitimately lives outside the run objects.

    The pre-Amendment-H skill is parsed from two committed text files that must keep
    agreeing with each other; src/figures_paper.py raises if they do not.
    """
    pre = fp.load_pre_amendment_h()
    lo, hi = pre["ci95"]
    assert lo <= pre["skill"] <= hi
    assert pre["run_id"] == fp.PRE_H_RUN
    assert round(abs(pre["skill"]), 3) == 0.005, (
        "the registered exception in src/citation_guard.py is written for a "
        f"pre-Amendment-H skill of -0.005; the sources now give {pre['skill']}")


# --- 3. what we cannot trace, reported and held ------------------------------

def test_citation_guard_unsourced_has_not_grown(inventory):
    """UNSOURCED is reported, not fixed -- but it must not quietly grow.

    Pinned on (document, number) rather than line, so moving a paragraph is not a
    failure and adding an untraceable number is.
    """
    pinned = {(c["document"], c["raw"]) for c in inventory["claims"]
              if c["status"] == "UNSOURCED"}
    live = cg.build()
    now = {(c["document"], c["raw"]) for c in live["claims"]
           if c["status"] == "UNSOURCED"}
    added = sorted(now - pinned)
    assert not added, (
        f"{len(added)} number(s) entered the published documents that cannot be "
        f"traced to any declared path:\n"
        + "\n".join(f"  {d}  {r}" for d, r in added)
        + f"\nEither register the object that holds them in "
          f"src/citation_guard.RUN_OBJECTS, or accept them and {REGENERATE}")


def test_citation_guard_unsourced_is_published_for_a_reader(inventory):
    """The list is only useful if a person can read it without running anything."""
    md = (ROOT / "docs" / "CITATION_INVENTORY.md")
    assert md.exists(), f"docs/CITATION_INVENTORY.md missing; {REGENERATE}"
    text = md.read_text()
    assert "## UNSOURCED" in text
    unsourced = [c for c in inventory["claims"] if c["status"] == "UNSOURCED"]
    for c in unsourced[:15]:
        assert c["context"][:40].replace("|", "\\|") in text or c["raw"] in text, (
            f"{c['document']}:{c['line']} {c['raw']} is UNSOURCED in the JSON but "
            f"does not appear in the Markdown a person actually reads")


# --- the guard's own machinery ------------------------------------------------

def test_citation_guard_declared_record_is_all_present(record):
    assert len(record) == len(cg.RUN_OBJECTS)
    for r in record:
        assert r["n_leaves"] > 0, f"{r['path']} contributes no numbers to the record"


def test_citation_guard_line_numbers_survive_code_fences():
    """Regression: blanking a fenced block to plain spaces ate its newlines and
    shifted every line number after the first fence in the document."""
    text = "alpha 1\n```\nfence 2\nfence 3\n```\nomega 0.480\n"
    claims = cg.extract_claims("t.md", text)
    omega = [c for c in claims if c["value"] == 0.48]
    assert omega and omega[0]["line"] == 6, \
        f"expected line 6, got {[c['line'] for c in omega]}"
    assert not any(c["value"] in (2.0, 3.0) for c in claims), \
        "numbers inside a code fence were treated as published claims"


def test_citation_guard_exceptions_need_the_sentence_not_just_the_value():
    """A value-only exception rule would file a pre-Amendment-H number under a live
    field, because -0.005 also happens to be the current price-vs-random-analogs
    skill. The context is what makes the exception safe."""
    hit = cg.match_exception({"context": "showed parity with the base rate (-0.005)",
                              "value": -0.005, "decimals": 3})
    miss = cg.match_exception({"context": "Vs random analogs -0.005 (p = 0.85).",
                               "value": -0.005, "decimals": 3})
    assert hit is not None and miss is None
