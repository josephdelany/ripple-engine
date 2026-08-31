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
    assert "associated with" in prose
    assert not any(v in f" {prose} " for v in CAUSAL_VERBS)
    # selection + confounder disclosures must be present (upper-bound honesty, Kilian confounders)
    disc = b["quant_read"]["disclosures"]
    assert "upper bound" in disc["selection"].lower()
    assert "opec" in disc["confounders"].lower() and "not isolated" in disc["confounders"].lower()


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
