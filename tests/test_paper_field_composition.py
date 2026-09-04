"""The paper's account of the structural vector must match the frozen reads that produced it.

The project's recurring defect is prose that describes a different quantity from the code. The
composition of the structural state vector is exactly that kind of claim: it is asserted in the
paper, it is not any number the experiment reports in `summary.json`, and it was wrong until
2026-09-03. So it is recomputed here from `data/structural_surface/reads.jsonl` and the paper is
required to agree.

This reads the frozen ledger and writes nothing. The published field-use artifact itself belongs
to the registered component ablation (`registrations/STRUCTURAL_COMPONENT_ABLATION.md`); this is
a guard on the prose, not a second copy of that analysis.
"""
import collections
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
READS = ROOT / "data" / "structural_surface" / "reads.jsonl"
PAPER = ROOT / "docs" / "PAPER.md"


@pytest.fixture(scope="module")
def composition():
    if not READS.exists():
        pytest.skip("frozen reads ledger not present in this checkout")
    fields = collections.Counter()
    blocks = collections.Counter()
    comparisons = 0
    market_only = 0
    reads = 0
    all_market_only_reads = 0
    combinations = set()
    for line in READS.open(encoding="utf-8"):
        detail = json.loads(line)["structural"]["detail"]
        reads += 1
        every = bool(detail)
        for d in detail:
            comparisons += 1
            names = tuple(d["fields"])
            combinations.add(names)
            fields.update(names)
            blocks.update(d["blocks"].keys())  # count which blocks appear, not their distances
            if all(f.startswith("market:") for f in names):
                market_only += 1
            else:
                every = False
        if every:
            all_market_only_reads += 1
    return {"fields": fields, "blocks": blocks, "comparisons": comparisons,
            "market_only": market_only, "reads": reads,
            "all_market_only_reads": all_market_only_reads, "combinations": combinations}


def test_frozen_reads_have_the_composition_the_paper_reports(composition):
    """The counts the paper publishes, recomputed from the ledger rather than trusted."""
    c = composition
    assert c["reads"] == 264
    assert c["comparisons"] == 41997
    assert c["market_only"] == 20915
    assert c["all_market_only_reads"] == 73
    assert len(c["combinations"]) == 6
    assert c["fields"]["market:wti_chg20"] == 41997
    assert c["fields"]["market:brent_chg20"] == 41982
    assert c["fields"]["market:brent_vol20"] == 41982
    assert c["fields"]["market:vix_close"] == 41322
    assert c["fields"]["panel:leader_change_last_365d"] == 21082
    assert c["fields"]["panel:leader_tenure_days"] == 21082
    assert c["fields"]["panel:mid_last_date"] == 3


def test_no_block_beyond_market_actors_and_dyads_ever_enters_a_distance(composition):
    """The registered question is about the wider state; three blocks is what the code reaches."""
    assert set(composition["blocks"]) == {"market", "actors", "dyads"}
    assert composition["blocks"]["market"] == 41997
    assert composition["blocks"]["actors"] == 21082
    assert composition["blocks"]["dyads"] == 3


def test_paper_publishes_the_measured_counts(composition):
    """Every count above must appear in the paper, so the prose cannot drift from the ledger."""
    text = PAPER.read_text(encoding="utf-8").replace("−", "-")
    c = composition
    required = [
        f"{c['comparisons']:,}", f"{c['market_only']:,}", str(c["all_market_only_reads"]),
        f"{c['fields']['panel:leader_tenure_days']:,}", f"{c['fields']['market:vix_close']:,}",
        "49.8", "50.2",
    ]
    missing = [x for x in required if x not in text]
    assert not missing, f"docs/PAPER.md no longer states: {missing}"


def test_paper_does_not_call_the_vector_a_full_geopolitical_state(composition):
    """The phrasing that made the arm sound broader than it is. It must not come back."""
    text = PAPER.read_text(encoding="utf-8").lower()
    for phrase in ("full geopolitical state", "full observable state around past events"):
        assert phrase not in text, f"docs/PAPER.md overstates the vector: {phrase!r}"


def test_two_independent_implementations_agree_on_the_composition(composition):
    """The ablation computes this audit too, from the same ledger, by different code.

    Codex's `src/structural_component_ablation.py` publishes a `field_use_audit` block under the
    registered ablation; this file recomputes the same quantities directly. They must agree. Two
    implementations agreeing is the only reason to believe either of them.
    """
    ablation = ROOT / "data" / "structural_surface" / "ablation" / "summary.json"
    if not ablation.exists():
        pytest.skip("registered ablation outputs not present in this checkout")
    audit = json.loads(ablation.read_text(encoding="utf-8"))["field_use_audit"]
    c = composition
    assert audit["n_comparisons"] == c["comparisons"]
    assert audit["market_only"] == c["market_only"]
    assert audit["dates_all_comparisons_market_only"] == c["all_market_only_reads"]
    assert audit["field_counts"] == dict(c["fields"])
    assert audit["containing_actors"] == c["blocks"]["actors"]
    assert audit["containing_dyads_or_other"] == c["blocks"]["dyads"]
