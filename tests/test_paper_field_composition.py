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
import csv
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
READS = ROOT / "data" / "structural_surface" / "reads.jsonl"
PAPER = ROOT / "docs" / "PAPER.md"
EVENTS = ROOT / "data" / "structural_surface" / "input" / "events.csv"
STATE = ROOT / "data" / "structural_surface" / "input" / "situation_state.csv"


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
    dates = []
    for line in READS.open(encoding="utf-8"):
        read = json.loads(line)
        detail = read["structural"]["detail"]
        dates.append(read["date"])
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
            "all_market_only_reads": all_market_only_reads, "combinations": combinations,
            "dates": dates}


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


def test_paper_states_that_the_full_state_question_is_untested(composition):
    """The status of the original research question must be stated, not left to inference.

    Asserted positively rather than by banning phrases. A substring ban cannot tell
    "correspondence across the full geopolitical state" (an overstatement) from "the full
    geopolitical state is never compared" (the correction), so it would eventually pressure
    someone into weakening accurate prose to make a test pass.
    """
    text = PAPER.read_text(encoding="utf-8").lower()
    assert "untested" in text, "docs/PAPER.md no longer says the stronger test is untested"
    assert any(p in text for p in ("never enter a distance", "never enters a distance",
                                   "never reach the arithmetic")), \
        "docs/PAPER.md no longer says which variables are absent from the computation"


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


def _multi_entity_cells(rows):
    grouped = collections.defaultdict(set)
    for row in rows:
        grouped[(row["event_id"], row["field"])].add(row["entity_id"])
    return grouped, sum(len(entities) >= 2 for entities in grouped.values())


def test_paper_discloses_the_relational_aggregation_boundary():
    """The event reducer averages actors; the paper must quantify and interpret that loss."""
    events = {r["event_id"]: r["event_date"] for r in csv.DictReader(EVENTS.open())}
    rows = list(csv.DictReader(STATE.open()))
    all_cells, all_multi = _multi_entity_cells(rows)
    strict = [r for r in rows if r["entity_id"] != "situation"
              and r["obs_date"] <= events[r["event_id"]]
              and r["vintage"] <= events[r["event_id"]]
              and r["release"] <= events[r["event_id"]]
              and r["retrospective"] == "0"]
    strict_cells, strict_multi = _multi_entity_cells(strict)

    assert (len(all_cells), all_multi) == (9264, 1643)
    assert (len(strict_cells), strict_multi) == (535, 127)

    btc = [r for r in rows if r["event_id"] == "btc_pipeline_blast_2008"
           and r["field"] == "polity2"]
    assert {(r["entity_id"], float(r["value"])) for r in btc} == {
        ("country.azerbaijan", -7.0), ("country.turkey", 7.0)}

    paper = PAPER.read_text(encoding="utf-8").lower()
    for value in ("1,643", "9,264", "17.7%", "127", "535", "23.7%"):
        assert value in paper
    assert "actor roles" in paper
    assert "relational geopolitical structure" in paper


def test_paper_discloses_the_actual_scored_era(composition):
    dates = composition["dates"]
    decades = collections.Counter(f"{d[:3]}0s" for d in dates)
    assert min(dates) == "2001-09-11"
    assert max(dates) == "2026-06-17"
    assert decades == {"2000s": 34, "2010s": 83, "2020s": 147}
    paper = PAPER.read_text(encoding="utf-8")
    for value in ("2001-09-11", "2026-06-17", "34", "83", "147", "55.7%"):
        assert value in paper
