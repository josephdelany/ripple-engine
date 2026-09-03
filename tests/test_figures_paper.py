"""Session I -- the three paper figures (src/figures_paper.py, docs/figures/).

The brief for these figures was "pull every number from the committed files; type
nothing in by hand". That is exactly the kind of instruction that decays silently:
a number gets nudged to match a draft and nobody can see it. So these tests do not
check that the figures look right -- they check that the figures are ARITHMETIC ON
THE SOURCES, and that the design rules the figures claim to obey are measured
rather than asserted.

DB-free by construction: committed JSON and Markdown only, no oil.db, no browser.
Registered in conftest.DB_FREE_FILES so CI actually runs it (DESIGN.md Amendment 1
A1.3: a rule that can only be checked where the checker never runs is not a rule).
"""
import json
import re
from pathlib import Path

import pytest

import figures_paper as fp

ROOT = Path(__file__).resolve().parent.parent
FIGDIR = ROOT / "docs" / "figures"
RECEIPT = FIGDIR / "figures.json"
PNGS = ["fig1_vintage.png", "fig2_escalation_baselines.png",
        "fig3_price_baselines.png"]


@pytest.fixture(scope="module")
def receipt():
    if not RECEIPT.exists():
        pytest.skip("docs/figures/figures.json absent; run python3 src/figures_paper.py")
    return json.loads(RECEIPT.read_text())


@pytest.fixture(scope="module")
def summary():
    return fp.load_summary()


# --- the figures are the sources, not a transcription of them ----------------

def test_figures_paper_vintage_counts_are_the_knowable_file(receipt):
    """Figure 1 left: 313 / 51 / 262 are read and subtracted, never typed."""
    k = fp.load_knowable()
    got = receipt["figures"]["fig1_vintage.png"]
    assert got["events"] == k["events"]
    assert got["without"] == k["events_with_no_situation_field_at_t"]
    assert got["with_state_knowable_at_t"] == (
        k["events"] - k["events_with_no_situation_field_at_t"])
    assert got["fields_kept"] == k["kept"]
    assert got["fields_dropped_after_t"] == k["dropped_after_t"]


def test_figures_paper_escalation_skill_is_the_published_run(receipt, summary):
    """Figure 1 right, 'after': the registered daily-tier G comparison, verbatim."""
    src = summary["tiers"]["daily"]["G"]["engine_vs"]["climatology"]
    got = receipt["figures"]["fig1_vintage.png"]["skill_after_amendment_h"]
    assert got["est"] == src["skill"]
    assert got["ci95"] == src["ci95"]
    assert got["dm_p"] == src["dm_p"]
    assert got["n"] == src["n"]


def test_figures_paper_pre_amendment_h_sources_agree(receipt):
    """Figure 1 right, 'before': not in summary.json, so it comes from two other
    committed files -- and they must agree to 4 dp or nothing is drawn."""
    pre = fp.load_pre_amendment_h()
    got = receipt["figures"]["fig1_vintage.png"]["skill_before_amendment_h"]
    assert got["est"] == pre["skill"]
    assert got["ci95"] == pre["ci95"]
    assert got["run_id"] == pre["run_id"] == fp.PRE_H_RUN
    lo, hi = pre["ci95"]
    assert lo <= pre["skill"] <= hi
    assert pre["run_id"] != receipt["sources"]["summary"]["run_id"], \
        "the before/after panel would be comparing a run with itself"


def test_figures_paper_escalation_levels_are_the_summary_means(receipt, summary):
    """Figure 2: four Brier levels, each read out of its own block."""
    g = summary["tiers"]["daily"]["G"]
    ev, items = g["engine_vs"], g["items_vs_climatology"]
    got = receipt["figures"]["fig2_escalation_baselines.png"]["brier"]
    assert got["persistence"] == ev["persistence"]["ref_mean"]
    assert got["climatology"] == ev["climatology"]["ref_mean"]
    assert got["the engine"] == ev["climatology"]["engine_mean"]
    assert got["M13 recalibrated"] == items["M13_recalibrated"]["engine_mean"]
    # The figure's claim -- 'lower is better' and the engine is third of four --
    # is a property of the data, not of the drawing.
    assert got["persistence"] < got["climatology"] < got["the engine"] \
        < got["M13 recalibrated"]


def test_figures_paper_price_skills_are_the_summary_intervals(receipt, summary):
    """Figure 3: CRPS skill against all four registered baselines."""
    ev = summary["tiers"]["daily"]["P"]["engine_vs"]
    got = receipt["figures"]["fig3_price_baselines.png"]["crps_skill"]
    assert set(got) == set(ev), "a baseline was dropped from or added to the figure"
    for ref, row in got.items():
        assert row["est"] == ev[ref]["skill"]
        assert row["ci95"] == ev[ref]["ci95"]
        assert row["dm_p"] == ev[ref]["dm_p"]
        assert row["n"] == ev[ref]["n"]


def test_figures_paper_holds_no_result_as_a_literal(receipt):
    """No published result may appear as a literal in the drawing code.

    The one way this module can lie is a number typed to match a draft. Every
    figure's own headline values are searched for in its source; finding one is
    the failure.
    """
    src = fp.__file__ and Path(fp.__file__).read_text()
    figs = receipt["figures"]
    banned = set()
    for v in (figs["fig2_escalation_baselines.png"]["brier"].values()):
        banned.add(f"{v:.3f}")
    for row in figs["fig3_price_baselines.png"]["crps_skill"].values():
        banned.add(f"{abs(row['est']):.3f}")
    f1 = figs["fig1_vintage.png"]
    banned |= {str(f1["events"]), str(f1["without"]),
               str(f1["with_state_knowable_at_t"]), str(f1["fields_kept"]),
               str(f1["fields_dropped_after_t"]),
               f"{abs(f1['skill_after_amendment_h']['est']):.3f}"}
    # Bounded match: '60' must not be found inside '0.160' or '1600'. Only a
    # number standing on its own counts as a value typed into the code.
    found = sorted(b for b in banned
                   if re.search(rf"(?<![\d.]){re.escape(b)}(?![\d.])", src))
    assert not found, f"result values typed into src/figures_paper.py: {found}"


# --- the design rules are measured, not asserted -----------------------------

def test_figures_paper_verdict_colour_follows_design_section_2():
    """DESIGN.md section 2: colour carries the verdict, never the sign."""
    assert fp.verdict_of(-0.180, -0.018) == "excludes_zero_worse"
    assert fp.verdict_of(0.004, 0.011) == "excludes_zero_better"
    assert fp.verdict_of(-0.060, 0.049) == "crosses_zero"
    assert fp.verdict_of(0.0, 0.049) == "crosses_zero", "an interval touching zero crosses it"
    assert fp.verdict_of(-0.060, 0.0) == "crosses_zero"
    # Three states, and no fourth.
    assert set(fp.VERDICT_COLOR) == set(fp.VERDICT_CAPTION) == {
        "crosses_zero", "excludes_zero_worse", "excludes_zero_better"}


def test_figures_paper_meets_the_design_section_4_contrast_floors():
    """DESIGN.md section 4, measured -- the check its own Amendment A1.1 failed."""
    ratios = fp.assert_contrast()          # raises if any floor is missed
    assert ratios["finding"] >= 12.0
    assert ratios["evidence"] >= 7.0
    assert ratios["provenance"] >= 4.5
    assert min(v for k, v in ratios.items() if k.startswith("verdict:")) >= 4.5


# --- the artefacts on disk ---------------------------------------------------

def test_figures_paper_pngs_are_present_and_not_stale(receipt, summary):
    for name in PNGS:
        png = FIGDIR / name
        assert png.exists(), f"docs/figures/{name} missing"
        assert png.stat().st_size > 20_000, f"docs/figures/{name} is suspiciously small"
        assert name in receipt["figures"]
    assert receipt["sources"]["summary"]["run_id"] == summary["run_id"], (
        "docs/figures/ was drawn from a different run than the one published in "
        "data/walk_forward/summary.json; re-run python3 src/figures_paper.py")


def test_figures_paper_every_figure_is_reachable_from_a_page():
    """DESIGN.md section 6: no number without the file it came from, one click away."""
    pages = [(ROOT / "README.md").read_text(), (ROOT / "docs" / "BRIEF.md").read_text()]
    for name in PNGS:
        assert any(name in p for p in pages), f"{name} is drawn but never shown"
    for page in pages:
        assert "src/figures_paper.py" in page, \
            "the page shows the figures without naming what drew them"
