"""Session H, H-2/H-3: why claims are UNCHECKABLE -- the reader, or the sources?

The ledger's first 14 claims were 13/14 uncheckable and that ratio was being read as a broken
reader. These tests hold the audit to its own terms: it must reconcile against the claim rows, it
must not touch the verdict rule that produced the ratio (INV-6 / charter §2), and the headline
finding -- that 93% was a source-selection artefact -- must recompute from the committed populations.
"""
import json
import sys
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import ledger as L                                                     # noqa: E402

LEDGER = ROOT / "data" / "ledger"
CAUSES = {"reader_defect", "data_gap", "source_property"}


def _rows(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


@pytest.fixture(scope="module")
def audit():
    return json.loads((LEDGER / "uncheckable_audit.json").read_text())


@pytest.fixture(scope="module")
def claims():
    return _rows(LEDGER / "claims.jsonl")


# --------------------------------------------------------------- it reconciles against the rows

def test_H2_totals_match_the_claim_ledger(audit, claims):
    assert audit["totals"]["claims"] == len(claims)
    assert audit["totals"]["uncheckable"] == sum(1 for c in claims if not c.get("checkable"))


def test_H2_cause_and_bucket_partitions_both_sum_to_the_uncheckable(audit):
    """Two independent decompositions of the same set. Either failing to sum means a claim was
    double-counted or dropped, and the percentages in the finding are wrong."""
    n = audit["totals"]["uncheckable"]
    assert sum(audit["totals"]["by_cause"].values()) == n
    assert sum(audit["totals"]["by_bucket"].values()) == n
    assert set(audit["totals"]["by_cause"]) <= CAUSES


def test_H2_populations_partition_the_ledger(audit, claims):
    pop = audit["by_population"]
    assert pop["original_live"]["n"] + pop["backfill"]["n"] == len(claims)
    assert pop["original_live"]["uncheckable"] + pop["backfill"]["uncheckable"] == audit["totals"]["uncheckable"]
    hist = [c for c in claims if c["story_id"].startswith("hist:")]
    assert pop["backfill"]["n"] == len(hist)


def test_H2_every_uncheckable_claim_is_adjudicated_exactly_once(audit, claims):
    """The audit publishes a row per claim; the UNCHECKABLE ones are the adjudicated subset. None may
    be left out and none may appear twice."""
    unchk = {c["claim_id"] for c in claims if not c.get("checkable")}
    listed = [r["claim_id"] for r in audit["rows"]]
    assert len(listed) == len(set(listed)) == len(claims), "a claim is published twice or missing"
    assert {r["claim_id"] for r in audit["rows"] if not r["checkable"]} == unchk, (
        "the audit and the ledger disagree about which claims are uncheckable")


def test_H2_rows_agree_with_the_published_totals(audit):
    adjudicated = [r for r in audit["rows"] if not r["checkable"]]
    assert Counter(r["cause"] for r in adjudicated) == Counter(audit["totals"]["by_cause"])
    assert Counter(r["bucket"] for r in adjudicated) == Counter(audit["totals"]["by_bucket"])


def test_H2_checkable_claims_are_never_given_an_uncheckable_cause(audit, claims):
    """A checkable claim must not be filed under a defect bucket -- that would inflate the diagnosis."""
    checkable = {c["claim_id"] for c in claims if c.get("checkable")}
    for r in audit["rows"]:
        if r["claim_id"] in checkable:
            assert r["checkable"] is True
            assert r["cause"] == "checkable" and r["bucket"] == "CHECKABLE"


# --------------------------------------------------------------- INV-6: the ratio was explained, not improved

def test_H2_the_verdict_rule_was_not_touched(audit):
    """The whole point is to explain the ratio, not to move it. The audit declares this and the
    registration it names must be the unchanged §2."""
    assert audit["verdict_rule_changed"] is False
    assert "unchanged" in audit["registration"]


def test_H2_every_backfill_quote_appears_verbatim_in_the_archived_page(claims):
    """THE FABRICATION GUARD, checked against the receipts rather than trusted.

    Claims are proposed by the reader model and validated by reader.cage_claim, which rejects any
    quote that is not in the source text. This re-runs that check offline: every backfill claim's
    text must appear verbatim in the committed page it was read from. A claim that cannot be found
    in its own archived page is an invented sentence, and no diagnosis built on it means anything.
    """
    import reader as R
    pages = ROOT / "data" / "ledger" / "backfill_pages"
    bodies, checked = {}, 0
    for c in claims:
        if not c["story_id"].startswith("hist:"):
            continue
        eid = c["story_id"].split(":", 1)[1]
        if eid not in bodies:
            html = (pages / f"{eid}.html").read_text(encoding="utf-8", errors="replace")
            bodies[eid] = R._canon(R.body_from_html(html))
        assert R._canon(c["text"]) in bodies[eid], (
            f"{c['claim_id']} is not in its own archived page ({eid}.html) -- fabricated quote")
        checked += 1
    assert checked == 98, f"expected the 98 backfill claims, checked {checked}"


def test_H2_stored_typing_is_the_caged_reader_not_a_fresh_regex(claims):
    """RECORDED, so nobody re-derives the ratio the wrong way.

    The stored kind/checkable come from the reader model's proposal after reader.cage_claim has
    downgraded it; only the labelled regex fallback uses ledger.type_claim. So re-typing a stored
    sentence does NOT reproduce its stored flag, and the uncheckable ratio cannot be recomputed
    offline from type_claim alone. This test pins how far the two diverge, so a change in either the
    prompt or the cage shows up here instead of silently moving the diagnosis.
    """
    same = diff = skipped = 0
    for c in claims:
        if not c.get("text") or not c.get("event_class"):
            skipped += 1
            continue
        t = L.type_claim(c["text"], c["event_class"], c.get("entities") or [])
        if bool(t["checkable"]) == bool(c.get("checkable")):
            same += 1
        else:
            diff += 1
    assert same + diff + skipped == len(claims)
    assert diff > 0, ("type_claim now reproduces every stored flag; if the reader path changed to the "
                      "regex cage, the H-3 diagnosis needs re-reading")
    assert same >= 48, f"only {same} of {len(claims)} agree -- the two typings have diverged further"


# --------------------------------------------------------------- the headline finding recomputes

def test_H3_the_93_percent_was_source_selection_not_the_reader(audit):
    """13/14 on the original two documents vs 35/98 on the mechanically-selected backfill, SAME
    reader. The finding text must match the arithmetic it rests on."""
    live, back = audit["by_population"]["original_live"], audit["by_population"]["backfill"]
    live_rate = live["uncheckable"] / live["n"]
    back_rate = back["uncheckable"] / back["n"]
    assert round(live_rate * 100) == 93, round(live_rate * 100)
    assert round(back_rate * 100) == 36, round(back_rate * 100)
    assert back_rate < live_rate / 2, "the drop is not large enough to support the finding as written"
    assert "SOURCE-SELECTION ARTEFACT" in audit["finding"].upper()


def test_H3_reader_defects_are_a_minority_and_are_named(audit):
    """The reader is not exonerated: its own defects must still be counted, and each one published
    verbatim so the call can be checked rather than taken on trust."""
    n_reader = audit["totals"]["by_cause"]["reader_defect"]
    assert 0 < n_reader < audit["totals"]["uncheckable"] / 2
    rows = [r for r in audit["rows"] if r["cause"] == "reader_defect"]
    assert len(rows) == n_reader
    for r in rows:
        assert r.get("text"), "a reader defect is claimed without publishing the sentence"
        assert r.get("note"), "a reader defect is claimed without saying why"


def test_H3_one_coder_unaudited_is_declared(audit):
    """Layer 2 is session H's own coding. It must not be presented as anything more."""
    st = audit["coding_status"].upper()
    assert "ONE CODER" in st and "UNAUDITED" in st
