"""
test_triage.py -- the live-triage cage (V4) holds: deterministic extraction, REAL analogues only,
expected-magnitude (never a probability), n+range always shown, caveats + latency on every card.
Run: python3 -m pytest -q tests/test_triage.py
"""

import sqlite3
from pathlib import Path

import triage as T

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"


def _card():
    return T.triage("Iran seizes an oil tanker in the Strait of Hormuz amid rising tensions")


def test_tr1_deterministic_extraction():
    a, b = _card()["extracted"], _card()["extracted"]
    assert a == b                                            # same input -> same extraction
    assert a["event_type"] == "chokepoint_disruption"
    assert "chokepoint.hormuz" in a["entities"] and "country.iran" in a["entities"]


def test_tr2_analogues_are_real_corpus_events():
    conn = sqlite3.connect(DB)
    real = {r[0] for r in conn.execute("SELECT event_id FROM events")}
    conn.close()
    for a in _card()["nearest_verified_analogs"]:
        assert a["event_id"] in real                        # never invented


def test_tr3_expected_magnitude_not_a_probability_and_shows_n_range():
    em = _card()["expected_magnitude"]
    assert em is not None
    br = em["base_rate"]
    assert "n" in br and "range_pct" in br and "iqr_pct" in br       # n + range ALWAYS shown
    assert em["current_amplifier"]["state"] in ("ON", "OFF", "?", "unknown")
    # the score is an expected MAGNITUDE, explicitly disclaimed as NOT a probability
    assert "magnitude" in em["caveat"].lower() and "probability" in em["caveat"].lower()
    # no probability-valued field is exposed (only magnitudes in %)
    assert not any("prob" in k.lower() for k in br)


def test_tr4_card_has_caveats_and_latency():
    c = _card()
    assert c["caveats"] and c["latency_ms"] >= 0
    assert any("no invented" in x for x in c["caveats"])
    assert any("expected magnitude" in x.lower() for x in c["caveats"])


def test_tr5_inflected_headlines_classify_not_dropped():
    """The commonest live-demo headline forms are INFLECTED (strikeS, invadeS, missileS,
    escalatION, clashES). A \\b-wrapped bare stem silently drops them -- regression guard."""
    cases = {
        "Israel strikes military targets inside Iran overnight": {"infrastructure_attack",
                                                                  "conflict_escalation"},
        "Russia invades a neighbouring region": {"conflict_escalation"},
        "Houthi missiles hit a tanker in the Red Sea": {"infrastructure_attack", "conflict_escalation"},
        "Iran-Israel tensions escalate sharply": {"conflict_escalation"},
        "US sanctions Russian oil exporters": {"sanctions"},
        "OPEC+ agrees a surprise output cut": {"opec_decision"},
    }
    for text, ok in cases.items():
        assert T.classify_type(text) in ok, f"{text!r} -> {T.classify_type(text)}"
    assert T.classify_type("Apple unveils a new iPhone at its annual event") is None
