"""Session H, H-4: the challenge loop refuses rather than invents.

A challenge lets a reader re-cut a situation record on a condition ("only when the actor is Iran").
The property that matters is not that it answers -- it is that it declines to answer when the
condition is outside the coded vocabulary, and that a refusal carries no numbers. These tests hold
that line on the committed log and on live calls against the corpus.
"""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import challenge as C                                                  # noqa: E402

LEDGER = ROOT / "data" / "ledger"
DB = ROOT / "data" / "oil.db"
NUMERIC = ("n", "price_n", "price_median_pct", "unconditioned_n", "unconditioned_price_median_pct")


@pytest.fixture(scope="module")
def log():
    return [json.loads(l) for l in open(LEDGER / "challenges.jsonl", encoding="utf-8") if l.strip()]


@pytest.fixture(scope="module")
def conn():
    if not DB.exists():
        pytest.skip("needs the built oil.db")
    c = sqlite3.connect(DB)
    yield c
    c.close()


# --------------------------------------------------------------- the committed log

def test_H4_challenge_ids_are_unique_and_append_only(log):
    ids = [r["challenge_id"] for r in log]
    assert len(ids) == len(set(ids)), "a challenge id repeats -- the log is not append-only"


def test_H4_every_row_has_a_registered_status(log):
    assert {r["status"] for r in log} <= {"REFUSED", "CONDITIONED", "THIN", "NO PRECEDENT"}


def test_H4_a_refusal_carries_a_reason_and_no_numbers(log):
    """The core property. A refusal that still published an n would be a number with no basis."""
    refused = [r for r in log if r["status"] == "REFUSED"]
    assert refused, "no refusals in the log -- the loop has not been exercised adversarially"
    for r in refused:
        assert r.get("errors"), f"{r['challenge_id']} refused with no reason"
        for k in NUMERIC:
            assert r.get(k) is None, f"{r['challenge_id']} is REFUSED but published {k}={r[k]}"


def test_H4_an_answered_challenge_carries_its_n_and_its_comparison(log):
    """Every answered challenge shows the conditioned n AND the unconditioned n it is to be read
    against; a conditioned median with nothing to compare it to is not a result."""
    for r in log:
        if r["status"] in ("REFUSED", "NO PRECEDENT"):
            continue
        assert r.get("n") is not None, f"{r['challenge_id']} answered without an n"
        assert r.get("unconditioned_n") is not None, f"{r['challenge_id']} has no unconditioned baseline"
        assert r.get("conditions_applied"), f"{r['challenge_id']} answered with no conditions applied"


def test_H4_the_refusals_cover_the_distinct_failure_modes(log):
    """The log must show the loop refusing for each registered reason, not the same one seven times."""
    reasons = " | ".join(e for r in log if r["status"] == "REFUSED" for e in (r.get("errors") or []))
    for probe in ("not in the coded vocabulary",
                  "is not a conditionable field",
                  "no conditions given",
                  "unknown event",
                  "not a geopolitical class"):
        assert probe in reasons, f"no refusal in the log for: {probe}"


def test_H4_uncoded_fields_are_flagged_where_they_change_nothing(log):
    """KNOWN WEAKNESS, pinned rather than hidden. A field whose corpus coverage is 0/N passes
    validation (the VALUE is in the codebook enum) and returns the unconditioned set unchanged. The
    row is flagged field_uncoded, but its status still reads CONDITIONED, which overstates it. Until
    that is amended, the invariant is: a field_uncoded row must not claim to have narrowed anything.
    """
    flagged = [r for r in log if any(str(f).startswith("field_uncoded:") for f in (r.get("flags") or []))]
    assert flagged, "no uncoded-field challenge in the log"
    for r in flagged:
        assert r["n"] == r["unconditioned_n"], (
            f"{r['challenge_id']} is flagged field_uncoded but reports a narrowed n")
        assert r["price_median_pct"] == r["unconditioned_price_median_pct"]


# --------------------------------------------------------------- live, against the corpus

def test_H4_validate_refuses_outside_the_coded_vocabulary(conn):
    voc = C.vocab(conn)
    clean, errors = C.validate({"conflict_scope": "skirmish"}, voc)
    assert clean == {} and errors and "not in the coded vocabulary" in errors[0]


def test_H4_validate_refuses_a_field_that_is_not_conditionable(conn):
    voc = C.vocab(conn)
    clean, errors = C.validate({"weather": "rainy"}, voc)
    assert clean == {} and any("not a conditionable field" in e for e in errors)


def test_H4_validate_refuses_an_empty_condition(conn):
    voc = C.vocab(conn)
    clean, errors = C.validate({}, voc)
    assert clean == {} and any("no conditions" in e for e in errors)


def test_H4_validate_never_repairs_a_condition(conn):
    """The cage downgrades and refuses; it never guesses what the reader meant. A bad value must not
    come back silently corrected to a near neighbour."""
    voc = C.vocab(conn)
    clean, errors = C.validate({"conflict_scope": "WAR "}, voc)
    assert "WAR " not in clean.values() if clean else True
    assert clean == {} and errors, "a malformed value was repaired instead of refused"


def test_H4_a_refusal_is_logged_but_writes_no_numbers(conn, monkeypatch, tmp_path):
    """Refusals are logged (charter §2.3: append-only, including the failures) -- into a tmp file
    here, never the real ledger."""
    monkeypatch.setattr(C, "CHALLENGES", tmp_path / "challenges.jsonl")
    res = C.run(conn, "event:not_a_real_event", {"tempo": "first"}, note="unit test")
    assert res["status"] == "REFUSED" and res["errors"]
    rows = [json.loads(l) for l in open(tmp_path / "challenges.jsonl", encoding="utf-8") if l.strip()]
    assert len(rows) == 1
    for k in NUMERIC:
        assert rows[0].get(k) is None
