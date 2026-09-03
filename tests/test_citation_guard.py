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
    lookups = {r["path"]: r["lookup"] for r in record}
    objs = {r["path"]: r["obj"] for r in record}
    gone = []
    for c in inventory["claims"]:
        if c["status"] not in ("RESOLVED", "AMBIGUOUS"):
            continue
        if c.get("in_correction_region"):
            # A number quoted as having been wrong is SUPPOSED to leave the record.
            # Checking it for drift would make every correction the project
            # publishes add noise here, penalising the behaviour this file exists
            # to protect.
            continue
        obj = objs.get(c["object"])
        assert obj is not None, (
            f"{c['object']} resolved a claim but is no longer a declared object")
        if c["status"] == "RESOLVED":
            # Sharp check: the exact field this number was traced to must still
            # print it. Renaming or dropping the field counts as drift too.
            ok = cg.still_at_path(c, obj)
            where = c["paths"][0]
        else:
            # AMBIGUOUS has no single field to point at, so the best available
            # check is that the value is still somewhere in the SAME object --
            # never in the record as a whole, which irf.json would always satisfy.
            ok = bool(cg.resolve_in(c, lookups[c["object"]])[0])
            where = c["object"]
        if not ok:
            gone.append(f"  {c['document']}:{c['line']}  {c['raw']}  "
                        f"({c['status'].lower()}, was {where})  |  {c['context'][:70]}")
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


# --- the three coverage gaps closed on 2026-09-03 ----------------------------

def test_citation_guard_indexes_csv_row_counts(record):
    """624 and 473 were untraceable for a reason that had nothing to do with the
    claim: the guard only read JSON, and those numbers are CSV row counts."""
    by_path = {r["path"]: r for r in record}
    pre = by_path["data/candidates/pre1987_candidates.csv"]
    post = by_path["data/candidates/post1987_candidates.csv"]
    assert pre["obj"]["n_rows"] == 624, pre["obj"]["n_rows"]
    assert post["obj"]["n_rows"] == 473, post["obj"]["n_rows"]


def test_citation_guard_csv_counts_actually_resolve_the_claims(inventory):
    """The paper's '624 pre-1987 candidates; 473 post-1987 candidates'."""
    got = {c["raw"]: c for c in inventory["claims"]
           if c["raw"] in ("624", "473") and c["status"] != "EXCLUDED"}
    assert got, "the candidate counts vanished from the documents"
    for raw, c in got.items():
        assert c["status"] in ("RESOLVED", "AMBIGUOUS"), (
            f"{raw} is {c['status']}; CSV indexing was supposed to resolve it")


def test_citation_guard_477_is_derived_from_its_published_predicate(record):
    """The propagation denominator: rows of irf.json carrying any verdict.

    401 NULL + 21 TRANSMITTING + 55 INSUFFICIENT of 932 rows, 455 unscored. The
    predicate is registered in PAPER_DRAFT section 12 and Appendix A; this asserts
    the arithmetic behind it rather than the number.
    """
    objs = {r["path"]: r["obj"] for r in record}
    rows = objs["data/ripple/irf.json"]["rows"]
    verdicts = {}
    for r in rows:
        verdicts[r.get("verdict")] = verdicts.get(r.get("verdict"), 0) + 1
    assert cg._scored_irf_cells(objs) == 477
    assert verdicts.get("NULL") == 401
    assert verdicts.get("TRANSMITTING") == 21
    assert verdicts.get("INSUFFICIENT") == 55
    assert verdicts.get(None) == 455
    assert len(rows) == 932


def test_citation_guard_self_referential_detector_fires_on_the_papers_own_sentence():
    """Proof the class works, using the sentence that motivated it.

    477 is DERIVED now, because its predicate was published. Before that it
    resolved ONLY as 21 + 401 + 55 from the sentence asserting it -- the exact
    shape a fabricated denominator takes. This asserts the detector would have
    caught it, so the class is not decoration.
    """
    claim = {"context": "**Result. Across 477 node×shock cells, 21 transmit, 401 "
                        "are null and 55 are insufficient.",
             "value": 477.0, "decimals": 0, "percent": False}
    addends = cg.self_referential_addends(claim)
    assert addends is not None, "the detector missed a self-asserting denominator"
    assert sorted(addends) == [21.0, 55.0, 401.0], addends


def test_citation_guard_self_referential_does_not_fire_on_ordinary_prose():
    """It must not flag every number that happens to be a sum."""
    claim = {"context": "The engine scored 0.769 against climatology's 0.701.",
             "value": 0.769, "decimals": 3, "percent": False}
    assert cg.self_referential_addends(claim) is None


def test_citation_guard_marks_correction_regions():
    """A paper that publishes its corrections contains wrong numbers on purpose."""
    text = ("Live claim: skill 0.123.\n"
            "\n"
            "*Correction of record.* An earlier draft reported +0.0103, CI "
            "[+0.0022, +0.0184].\n"
            "It is now +0.0102.\n"
            "\n"
            "Back to live prose: 0.456.\n")
    lines = cg._correction_lines(text)
    assert 3 in lines and 4 in lines, lines
    assert 1 not in lines and 6 not in lines, lines


def test_citation_guard_correction_heading_covers_its_section():
    text = ("## 12 Results\n"
            "value 0.111\n"
            "\n"
            "### 12.1 Two errata, from the follow-up\n"
            "we reported 0.222\n"
            "\n"
            "## 13 Next\n"
            "value 0.333\n")
    lines = cg._correction_lines(text)
    assert 5 in lines, lines
    assert 2 not in lines and 8 not in lines, lines


def test_citation_guard_historical_numbers_are_exempt_from_drift(inventory):
    """The functional point of the HISTORICAL class: a superseded number is
    EXPECTED to leave the record, so it must never be reported as drift."""
    corr = [c for c in inventory["claims"]
            if c.get("in_correction_region") and c["status"] != "EXCLUDED"]
    assert corr, "no correction regions found; the detector has stopped working"
    assert any(c["status"] == "HISTORICAL" for c in inventory["claims"]), \
        "a correction region exists but nothing was classed HISTORICAL"


def test_citation_guard_keeps_the_graded_protection_statement_verbatim():
    """The framing is load-bearing and must not be softened by a later edit.

    Nobody may quote this guard as though it validated the paper.
    """
    # Whitespace-collapsed: these phrases are wrapped for line width in both files,
    # and the requirement is that the WORDING survives, not its line breaks.
    def flat(path):
        return " ".join((ROOT / path).read_text().split())

    src = flat("src/citation_guard.py")
    md = flat("docs/CITATION_INVENTORY.md")
    for phrase in ("STRONG", "SHARP", "WEAK"):
        assert phrase in src, f"the graded-protection statement lost {phrase}"
    for phrase in ('not obviously broken', 'never as \\"checked\\"'.replace("\\", ""),
                   "not a substitute for reading"):
        assert phrase in src, f"src lost: {phrase}"
    for phrase in ("not obviously broken", "never as", "checked",
                   "never be quoted as though it validated the paper"):
        assert phrase in md, f"the published inventory lost: {phrase}"
    for grade in ("strong", "sharp", "weak"):
        assert grade in md, f"the inventory's graded table lost {grade}"


def test_citation_guard_correction_regions_do_not_over_capture():
    """Over-capture is the dangerous direction.

    Nothing in a correction region is checked for drift, so a live paragraph swept
    in by a loose rule would be silently exempted -- a worse failure than the noise
    the class was added to remove. Two properties are asserted: every region really
    does open with a correction marker, and no document is mostly correction.
    """
    for doc in cg.DOCUMENTS:
        text = (ROOT / doc).read_text()
        raw = text.splitlines()
        lines = cg._correction_lines(text)
        if not lines:
            continue
        share = len(lines) / max(len(raw), 1)
        assert share <= 0.25, (
            f"{doc}: {share:.0%} of the document is classed as a correction region; "
            f"the opener rule has gone loose and is exempting live prose from drift")
        starts = [n for n in sorted(lines) if n - 1 not in lines]
        for n in starts:
            head = raw[n - 1]
            assert (cg._paragraph_is_a_correction(head)
                    or head.strip().startswith("#")), (
                f"{doc}:{n} was classed as a correction region but does not announce "
                f"itself as one: {head.strip()[:80]!r}")


def test_citation_guard_a_retraction_lead_in_is_detected():
    """Regression: the opener was start-anchored and missed a paragraph that
    announces its retraction inside a bolded lead-in, which is how OPEN_ITEMS
    writes them."""
    assert cg._paragraph_is_a_correction(
        "**1.5 ~~A VALIDATED claim in `edge_battery.json`~~ — CLOSED, RETRACTED.**")
    assert cg._paragraph_is_a_correction("*Correction of record.* An earlier draft")
    assert not cg._paragraph_is_a_correction(
        "Pre-registration with git timestamps · three published retractions of the "
        "project's own earlier positive findings, which is the record working.")


def test_citation_guard_the_same_number_is_classed_by_its_context():
    """The same value must be treated differently inside and outside a correction.

    Synthetic rather than pinned to live prose: both real occurrences of +8.209 now
    sit in retraction paragraphs, which is correct but makes the documents unable to
    demonstrate the distinction.
    """
    text = ("A live claim of 8.209 in ordinary prose.\n"
            "\n"
            "*Correction of record.* We earlier reported 8.209 and withdraw it.\n")
    claims = [c for c in cg.extract_claims("t.md", text) if c["value"] == 8.209]
    assert len(claims) == 2, claims
    flags = {c["line"]: c["in_correction_region"] for c in claims}
    assert flags == {1: False, 3: True}, flags
