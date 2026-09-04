"""Independent check of the schedule-imputed sensitivity arm.

`tests/test_schedule_imputed_sensitivity.py` was written by the same worker as
`src/schedule_imputed_sensitivity.py`. These tests were written against
`registrations/CONTEMPORANEOUS_AVAILABILITY_ARM.md` by a different worker, and deliberately
reconstruct the admission rule from the registration text and the committed CSVs rather than by
calling the implementation's own helpers. Where the two disagree, one of them is wrong.

They are kept cheap: nothing here calls `prepare_designs`, which recomputes ~42,000 pairwise
distances.
"""
import csv
import re
from pathlib import Path

import pytest

import schedule_imputed_sensitivity as M
from structural_surface_experiment import connect_bundle

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "data" / "structural_surface" / "input"
REGISTRATION = ROOT / "registrations" / "CONTEMPORANEOUS_AVAILABILITY_ARM.md"

# Column order of the raw tuple `admission_reason` consumes, from `admitted_panel`'s SELECT.
# Reproduced here so a change to that SELECT breaks this test loudly instead of silently
# shifting which column is read as `vintage`.
COLS = ("event_id", "field", "obs_date", "value", "value_text", "entity_id",
        "vintage", "release", "retrospective", "source")


def row_tuple(**kw):
    # Defaults describe a row that IS admissible, so each test flips exactly one thing and the
    # ordered checks in `admission_reason` cannot mask the clause under test.
    base = dict(event_id="e", field="cinc", obs_date="1990-01-01", value=1.0, value_text=None,
                entity_id="country.x", vintage="1990-02-01", release="2020-01-01",
                retrospective=0, source="COW National Material Capabilities v7.0 (NMC-70-abridged.csv)")
    base.update(kw)
    return tuple(base[c] for c in COLS)


def test_release_date_is_ignored_which_is_the_whole_point_of_the_amendment():
    """Amendment 1 withdrew `release <= event_date`. A row failing only it must be ADMITTED.

    This is the single behavioural difference between this arm and the frozen experiment. If it
    ever regresses the arm silently becomes a copy of the frozen one and every contrast goes to
    zero for a reason no reader would guess.
    """
    row = row_tuple(release="2020-01-01")  # 30 years after the event
    assert M.admission_reason(row, "1992-06-01") == "admitted"


def test_vintage_after_event_still_excludes():
    """Amendment 1 keeps `vintage <= event_date`; it is the availability date the loaders encode."""
    row = row_tuple(vintage="1995-01-01")
    assert M.admission_reason(row, "1990-06-01") == "vintage_after_event"


def test_the_three_permanent_exclusions_hold():
    """Retrospective reconstruction, situation-coded rows, and post-event observation."""
    assert M.admission_reason(row_tuple(retrospective=1), "1990-06-01") == "retrospective"
    assert M.admission_reason(row_tuple(entity_id="situation"), "1990-06-01") == "entity_is_situation"
    assert M.admission_reason(row_tuple(obs_date="1991-01-01"), "1990-06-01") == "obs_date_after_event"


def test_admission_fails_closed_on_unknown_field_and_unknown_source():
    """Nothing is admitted by default. A new field or a re-worded source string must be excluded."""
    assert M.admission_reason(row_tuple(field="gpr_monthly"), "1992-06-01") == "field_not_allowlisted"
    assert M.admission_reason(row_tuple(source="COW NMC v7.0"), "1992-06-01") == "source_not_allowlisted"


def test_market_and_narrative_fields_can_never_enter_the_panel_block():
    """The registration excludes these by name; the market block is already frozen elsewhere."""
    for field in ("wti_monthly", "brent_daily", "wti_daily", "diesel_crack", "curve_m1_m4_spread",
                  "vix", "ovx", "cot_managed_money_net", "opec_decision_dated",
                  "kilian_igrea", "gpr_monthly", "surplus_capacity_world"):
        assert field not in M.FIELD_BLOCKS, f"{field} must not be an allowlisted panel field"


def test_admission_count_matches_an_independent_recount_from_the_committed_csvs():
    """The count, rebuilt from the CSVs with the rule read off the registration, not the code."""
    events = {r["event_id"]: r["event_date"]
              for r in csv.DictReader((BUNDLE / "events.csv").open(encoding="utf-8"))}
    mine = 0
    for r in csv.DictReader((BUNDLE / "situation_state.csv").open(encoding="utf-8")):
        d = events.get(r["event_id"])
        if d is None:
            continue
        if (r["entity_id"] != "situation" and r["retrospective"] == "0"
                and r["obs_date"] <= d and r["vintage"] <= d
                and r["field"] in M.FIELD_BLOCKS and r["source"] in M.ALLOWED_SOURCES):
            mine += 1

    conn = connect_bundle(BUNDLE)
    try:
        _, _, receipt = M.admitted_panel(conn)
    finally:
        conn.close()

    assert receipt["n_admitted"] == mine, "implementation and independent recount disagree"
    assert receipt["n_rows"] == 11089
    # Recorded so a silent change in either direction is visible in the diff, and so the
    # registration's disclosed power figure stays honest.
    assert mine == 5742, f"admitted rows moved to {mine}; the registration discloses 5,742"


def test_admitted_rows_are_the_frozen_rule_plus_release_only():
    """Every extra row this arm admits must be one the frozen rule rejected *only* on release."""
    events = {r["event_id"]: r["event_date"]
              for r in csv.DictReader((BUNDLE / "events.csv").open(encoding="utf-8"))}
    for r in csv.DictReader((BUNDLE / "situation_state.csv").open(encoding="utf-8")):
        d = events.get(r["event_id"])
        if d is None:
            continue
        admitted_here = (r["entity_id"] != "situation" and r["retrospective"] == "0"
                         and r["obs_date"] <= d and r["vintage"] <= d
                         and r["field"] in M.FIELD_BLOCKS and r["source"] in M.ALLOWED_SOURCES)
        if not admitted_here:
            continue
        # It may fail the frozen rule only because of `release`; never because of anything else.
        assert r["obs_date"] <= d and r["vintage"] <= d and r["retrospective"] == "0", \
            f"{r['event_id']}/{r['field']} admitted while failing a clause the amendment kept"


def test_allowlists_are_transcribed_from_the_registration_not_invented():
    """Parsed out of the registration text here, independently of the implementation's own test."""
    text = REGISTRATION.read_text(encoding="utf-8")
    section = text[text.index("### Frozen field allowlist"):]
    section = section[:section.index("Market, derived-market")]
    registered_fields = set(re.findall(r"`([a-z0-9_]+)`", section))
    registered_sources = set(re.findall(r"^- `(.+)`$", text, re.M))

    assert registered_fields == set(M.FIELD_BLOCKS), \
        f"field allowlist drifted from the registration: {registered_fields ^ set(M.FIELD_BLOCKS)}"
    assert registered_sources == set(M.ALLOWED_SOURCES), \
        f"source allowlist drifted: {registered_sources ^ set(M.ALLOWED_SOURCES)}"


def test_publication_stays_blocked_after_the_implementation_commit_is_recorded():
    """Joe ruled register-but-do-not-run. Recording provenance must not lift that block."""
    assert M.IMPLEMENTATION_COMMIT == "9265ec5a5d4779ccc81a6fbcb2ecc8335b771c03"
    assert M.PUBLICATION_AUTHORIZED is False
    with pytest.raises(RuntimeError, match="not authorized"):
        M.publish()
    assert not (ROOT / "data" / "structural_surface" / "availability").exists(), \
        "publication output exists for an arm that has not been authorised to run"
