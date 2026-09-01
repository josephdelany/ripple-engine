"""
test_brief.py -- the ANALYTICAL BRIEF holds its institutional-honesty contract.

The brief fuses narrative + numbers; these tests are the cage that keeps it HONEST and
non-fabricated: association not causation, expected magnitude not probability, every
conditional stat shipped with its base rate + a bootstrap CI, small-N gates enforced,
selection/confounder disclosures present, real corpus analogues only, and reproducible
output. Integration tests (need the built oil.db); conftest skips them on a DB-less checkout.

Run: python3 -m pytest -q tests/test_brief.py
"""

import sqlite3
from pathlib import Path

from fastapi.testclient import TestClient

import brief as B
import backend

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
client = TestClient(backend.app)

HEADLINE = "Iran seizes an oil tanker in the Strait of Hormuz amid rising tensions"
CAUSAL_VERBS = (" causes ", " caused ", " will move ", " drives ", " guarantees ")


def _real_ids():
    conn = sqlite3.connect(DB)
    ids = {r[0] for r in conn.execute("SELECT event_id FROM events")}
    conn.close()
    return ids


def _brief():
    return B.build_brief(HEADLINE)


def test_br1_quant_read_ships_base_rate_ci_and_cross_asset():
    """The quant read carries n, a bootstrap CI, a null-baseline lift, and cross-asset -- a
    conditional statistic never ships without its base rate (research R1/R2)."""
    qr = _brief()["quant_read"]
    assert qr and qr["n"] > 0
    a = qr["abs_car20"]
    assert a["ci90_median_pct"][0] is not None and a["ci90_median_pct"][1] is not None
    assert qr["baseline"]["ordinary_median_pct"] is not None          # base rate present
    assert qr["baseline"]["class_median_percentile"] is not None      # lift vs ordinary moves
    assert qr["cross_asset"] and all("unit" in c for c in qr["cross_asset"])


def test_br2_language_is_association_not_causation_and_discloses_limits():
    """No causal verbs in the generated prose; the mandatory disclosures are present."""
    b = _brief()
    prose = (b["bottom_line"] + " " + b["synthesis"]).lower()
    assert "association" in prose and "cause" in prose     # the standing honesty framing
    assert not any(v in f" {prose} " for v in CAUSAL_VERBS)
    # selection + confounder disclosures must be present (upper-bound honesty, Kilian confounders)
    disc = b["quant_read"]["disclosures"]
    assert "upper bound" in disc["selection"].lower()
    assert "opec" in disc["confounders"].lower() and "not isolated" in disc["confounders"].lower()


def test_br10_unclassified_is_a_clean_gap_with_no_story_read():
    """An off-topic story yields a documented gap: no quant read, no synthesis, no story-
    specific watch-items -- it must NOT render a confident read about an unrelated theatre."""
    b = B.build_brief("Apple unveils new iPhone at its annual event")
    assert b["quant_read"] is None
    assert b["synthesis"] == ""
    assert b["what_would_change"] == []
    assert "documented gap" in b["bottom_line"].lower()
    assert "context only" in b["bottom_line"].lower()


def test_br11_ordinals_are_correct_never_53th():
    """The lead sentence must never ship '53th'/'1th'/'2th'."""
    assert (B._ordinal(1), B._ordinal(2), B._ordinal(3)) == ("1st", "2nd", "3rd")
    assert (B._ordinal(11), B._ordinal(13), B._ordinal(53)) == ("11th", "13th", "53rd")
    import re
    for hl in (HEADLINE, "OPEC+ agrees a surprise output cut"):
        assert not re.search(r"\b\d*[123]th\b", B.build_brief(hl)["bottom_line"])


def test_br12_bluf_carries_no_market_gap_clause():
    """The market-wide gap is a standing read shown in its own section -- it must NOT be
    restated in every BLUF as if freshly derived from each story."""
    for hl in (HEADLINE, "OPEC+ agrees a surprise output cut", "US sanctions Russian oil exports"):
        bl = B.build_brief(hl)["bottom_line"].lower()
        assert "pricing the fear" not in bl and "pricing the risk" not in bl


def test_br13_type_only_match_is_flagged_and_capped_low():
    """A classified headline with no recognised entities is a type-only match: flagged in the
    BLUF and capped at low confidence however large n is."""
    b = B.build_brief("New sanctions announced today")
    if b["quant_read"] and not b["story"]["entities"]:
        assert b["confidence"]["tier"] == "low"
        assert "type-only" in b["bottom_line"].lower()


def test_br14_magnitude_is_disclosed_as_size_not_direction():
    b = _brief()
    assert "size, not direction" in b["bottom_line"].lower()
    d = b["quant_read"]["direction"]
    assert d["up_pct"] + d["down_pct"] == 100


def test_br15_decision_read_present_and_hedged():
    b = _brief()
    dr = b["decision_read"].lower()
    assert "for a decision-maker" in dr and "watch" in dr


def test_br18_distribution_present_for_lift_chart():
    """The quant read carries the baseline distribution the 'is this bigger than normal?' chart
    needs: binned ordinary moves + this class's median and ordinary median."""
    dist = _brief()["quant_read"]["distribution"]
    assert dist and dist["bins"]
    assert dist["class_median"] is not None and dist["ordinary_median"] is not None
    assert dist["class_values"] and dist["axis_max"] > 0


def test_br16_opec_does_not_borrow_conflict_corroboration():
    """An OPEC/sanctions story must never inherit a conflict theatre's multi-modal corroboration,
    even if a shared country is a member of that situation."""
    b = B.build_brief("Saudi Arabia announces an OPEC+ output cut of 1 million barrels per day")
    if b["quant_read"]:
        c = b.get("corroboration")
        assert not (c and c.get("story_relevant"))        # opec_decision is not a conflict class
        assert b["confidence"]["tier"] != "moderate"


def test_br17_relevant_corroboration_only_for_conflict_classes():
    """If corroboration is flagged story-relevant, the story must be a conflict-class event and the
    confidence 'why' must not simultaneously deny it."""
    b = B.build_brief("Israel strikes military targets inside Iran overnight")
    c = b.get("corroboration")
    if c and c.get("story_relevant"):
        assert b["story"]["event_class"] in {"conflict_escalation", "infrastructure_attack",
                                             "chokepoint_disruption"}
        assert "no story-relevant corroboration" not in b["confidence"]["why"]


def test_br3_magnitude_not_probability():
    """The engine emits expected MAGNITUDE, never an occurrence probability. The discipline
    line says so, and no quant field is a probability of the event happening."""
    b = _brief()
    assert "magnitude" in b["discipline"].lower() and "probability" in b["discipline"].lower()
    # confidence is about evidence quality, explicitly NOT a probability of an outcome
    assert "not the probability" in b["confidence"]["why"].lower()
    # no quant_read field name implies an occurrence probability
    assert not any("prob" in k.lower() for k in b["quant_read"]["abs_car20"])


def test_br4_precedent_are_real_corpus_events_only():
    real = _real_ids()
    for a in _brief()["precedent"]:
        assert a["event_id"] in real                                  # never invented


def test_br5_sample_gates_enforced():
    """The small-N gate function drives the output mode (research R4)."""
    assert B.sample_gate(50) == "full"
    assert B.sample_gate(15) == "caveat"
    assert B.sample_gate(6) == "cases_only"
    assert B.sample_gate(2) == "insufficient"


def test_br6_reproducible_same_input_same_ci():
    """Fixed-seed bootstrap/baseline -> the brief is reproducible (same story, same CI)."""
    a = B.build_brief(HEADLINE)["quant_read"]["abs_car20"]["ci90_median_pct"]
    b = B.build_brief(HEADLINE)["quant_read"]["abs_car20"]["ci90_median_pct"]
    assert a == b


def test_br7_daily_brief_is_real_or_a_documented_gap():
    """The daily brief returns a real story's brief OR a documented gap -- never a fabricated one."""
    d = B.build_daily_brief()
    assert ("error" in d) or (d.get("story") and d.get("bottom_line"))
    if "story" in d:
        assert d["daily_pick"]["day"]


def test_br8_endpoints_serve_briefs():
    """POST /wb_brief and GET /wb_daily_brief return real briefs through the API."""
    r = client.post("/wb_brief", json={"text": HEADLINE})
    assert r.status_code == 200
    b = r.json()
    assert b["quant_read"]["n"] > 0 and b["bottom_line"]
    real = _real_ids()
    assert all(a["event_id"] in real for a in b["precedent"])
    d = client.get("/wb_daily_brief").json()
    assert ("error" in d) or d.get("bottom_line")


def test_br9_empty_input_is_a_documented_gap():
    assert client.post("/wb_brief", json={"text": "  "}).json().get("error")
