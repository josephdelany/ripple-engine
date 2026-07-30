"""
test_living_engine.py -- the caged auto-corpus loop can never fabricate and never leak lookahead.

These lock the invariants that make auto-registration safe (in the hand-verifiable style of
test_situation.py): the cage rejects unsourced/hallucinated/out-of-vocab/future-dated proposals, admits
only clean ones (severity blank -- the LLM number never auto-enters), and the admission tier needs
strong corroboration. Run: python3 -m pytest -q tests/test_living_engine.py
"""

from datetime import date

import extract_events as EE
import admit_events as AE

TODAY = date(2026, 7, 30)
BATCH = {"batch_id": "inbox_x", "alerts": [
    {"alert_id": "a1", "timestamp_utc": "2026-07-29T10:00:00Z",
     "url": "https://reuters.com/real-story"}]}


def _proposal(**over):
    p = {"alert_id": "a1", "type": "chokepoint_disruption", "event_date": "2026-07-29",
         "date_precision": "day", "title": "Strait event", "description": "A tanker was struck.",
         "entities": "chokepoint.hormuz:location", "source_url": "https://reuters.com/real-story",
         "severity_suggestion": 3, "surprise_suggestion": 3, "confidence": "medium",
         "rationale": "supply route hit"}
    p.update(over)
    return p


def test_le1_clean_proposal_admitted_severity_blank():
    errs, row = EE.validate_one(_proposal(), BATCH, TODAY)
    assert errs == []
    assert row["type"] == "chokepoint_disruption" and row["candidate_source"] == "llm_extract"
    # the LLM's suggested numbers NEVER auto-populate the coded fields
    assert row["severity"] == "" and row["surprise"] == ""
    assert "advisory" in row["description"].lower()          # suggestion kept as advisory prose only


def test_le2_missing_source_rejected():
    errs, row = EE.validate_one(_proposal(source_url=""), BATCH, TODAY)
    assert row is None and any("source_url" in e for e in errs)


def test_le3_hallucinated_url_rejected():
    # a url that is NOT in the batch (and not a corroborating_url) is a fabrication -> rejected
    errs, row = EE.validate_one(_proposal(source_url="https://evil.example/made-up"), BATCH, TODAY)
    assert row is None and any("fabrication guard" in e for e in errs)


def test_le4_out_of_vocab_type_rejected():
    errs, _ = EE.validate_one(_proposal(type="alien_invasion"), BATCH, TODAY)
    assert any("not registered" in e for e in errs)


def test_le5_future_dated_rejected():
    errs, _ = EE.validate_one(_proposal(event_date="2026-08-15"), BATCH, TODAY)
    assert any("future" in e for e in errs)


def test_le6_event_after_alert_is_lookahead():
    # event_date after the alert timestamp = coding something the alert couldn't have known yet
    errs, _ = EE.validate_one(_proposal(event_date="2026-07-30"), BATCH, TODAY)
    assert any("after the alert" in e for e in errs)


def test_le7_bad_suggestion_range_rejected():
    errs, _ = EE.validate_one(_proposal(severity_suggestion=9), BATCH, TODAY)
    assert any("severity_suggestion" in e for e in errs)


def test_le8_corroborating_url_is_allowed_source():
    # a source not in the alert list but supplied as a corroborating_url is legitimate
    p = _proposal(source_url="https://apnews.com/confirm", corroborating_urls=["https://apnews.com/confirm"])
    errs, row = EE.validate_one(p, BATCH, TODAY)
    assert errs == [] and row["source_url"] == "https://apnews.com/confirm"


def test_le9_admission_tiers():
    corrob = {"https://reuters.com/real-story": (0.95, 5),
              "https://x/weak": (0.80, 2)}
    keep = {"recommendation": "keep", "source_url": "https://reuters.com/real-story", "type": "sanctions"}
    assert AE.tier_for(keep, corrob)[0] == "AUTO_ADMIT"
    weak = {"recommendation": "keep", "source_url": "https://x/weak", "type": "sanctions"}
    assert AE.tier_for(weak, corrob)[0] == "FAST_REVIEW"
    nomatch = {"recommendation": "keep", "source_url": "https://x/none", "type": "sanctions"}
    assert AE.tier_for(nomatch, corrob)[0] == "REVIEW"          # fail-closed: no exact url match
    rej = {"recommendation": "reject", "source_url": "https://reuters.com/real-story", "type": "sanctions"}
    assert AE.tier_for(rej, corrob)[0] == "PARK"
