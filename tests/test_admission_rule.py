"""
test_admission_rule.py -- the registered V2 auto-admit rule (admission_rule.evaluate) enforces all
five gates and fail-closes. A candidate reaches AUTO_ADMIT only if every gate passes; any failure ->
BORDERLINE with a reason. Locks the invariants so the corpus can never silently admit a single-source,
imprecise, unsourced, out-of-vocab, or duplicate event. Run: python3 -m pytest -q tests/test_admission_rule.py
"""

from datetime import date

import admission_rule as AR

TODAY = date(2026, 8, 3)
EXISTING = [("1990-08-02", "conflict_escalation")]     # one corpus event, for the G5 duplicate check


def _clean(**over):
    c = {"type": "sanctions", "event_date": "2015-07-14", "date_precision": "day",
         "entities": "country.iran:target;institution.opec:actor",
         "source_url": "https://www.reuters.com/x|https://www.bbc.com/y"}
    c.update(over)
    return c


def test_ar1_clean_two_source_admits():
    r = AR.evaluate(_clean(), EXISTING, TODAY)
    assert r["verdict"] == "AUTO_ADMIT" and all(r["gates"].values())


def test_ar2_single_source_borderline():                 # G1
    r = AR.evaluate(_clean(source_url="https://www.reuters.com/only"), EXISTING, TODAY)
    assert r["verdict"] == "BORDERLINE" and not r["gates"]["G1_two_independent_sources"]


def test_ar3_same_publisher_not_independent():           # G1 (two urls, one publisher)
    r = AR.evaluate(_clean(source_url="https://reuters.com/a|https://www.reuters.com/b"), EXISTING, TODAY)
    assert not r["gates"]["G1_two_independent_sources"]


def test_ar4_week_precision_borderline():                # G2
    r = AR.evaluate(_clean(date_precision="week"), EXISTING, TODAY)
    assert not r["gates"]["G2_date_precision_day"]


def test_ar5_bad_entities_borderline():                  # G3
    r = AR.evaluate(_clean(entities="blah;nope"), EXISTING, TODAY)
    assert not r["gates"]["G3_clean_entity_match"]


def test_ar6_cage_rejects_future_and_vocab_and_fakeurl():  # G4
    assert not AR.evaluate(_clean(event_date="2026-09-01"), EXISTING, TODAY)["gates"]["G4_passes_cage"]
    assert not AR.evaluate(_clean(type="alien_invasion"), EXISTING, TODAY)["gates"]["G4_passes_cage"]
    assert not AR.evaluate(_clean(source_url="not-a-url|also-bad"), EXISTING, TODAY)["gates"]["G4_passes_cage"]


def test_ar7_cluster_duplicate_borderline():             # G5
    dup = _clean(type="conflict_escalation", event_date="1990-08-10")   # within 35d of the existing one
    r = AR.evaluate(dup, EXISTING, TODAY)
    assert not r["gates"]["G5_not_cluster_duplicate"] and r["verdict"] == "BORDERLINE"
