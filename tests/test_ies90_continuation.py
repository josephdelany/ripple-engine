"""Session K: OUTCOME_MAPPING.md Amendment 4 — the ongoing-conflict rule, as unit tests.

Amendment 1.1 gave ICB and Dyadic MID an "ongoing at d -> no level" carve-out and never
extended it to COW War or UCDP GED, so 34 of 54 level-3 "war" labels were wars that were
already running. Amendment 4 extends it, and fixes the mirror-image defect that "no level"
fell through `max(default=0)` to level 0 = "none" on 18 events, including the Abqaiq attack
and the Soleimani strike.

These tests are on the *rules*, not on the database: every fixture is a hand-built source
record, so a test failure means the rule changed, not that the corpus did. Nothing here
writes anything, and no fixture is ever inserted into a real table (CLAUDE.md
<no_fabrication>: these are pure-function inputs, not rows).

Each test names the amendment clause it covers.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "state"))
import ies90  # noqa: E402

D = "2020-06-01"          # a convenient event date; W = 2020-06-02..2020-08-30, B = 2020-03-03..2020-05-31
IRAN, IRAQ = "country.iran", "country.iraq"


def _spell(a, b):
    return (pd.Timestamp(a), pd.Timestamp(b))


def _war(inter=(), intra=()):
    return {"inter": list(inter), "intra": list(intra)}


def _ged(ent, day_deaths):
    """A GED series for one entity: {date: deaths} -> the (dates, cumsum) shape load_ged builds."""
    import numpy as np
    dd = {k: float(v) for k, v in sorted(day_deaths.items())}
    dates = np.array(sorted(dd), dtype="datetime64[D]")
    cum = np.concatenate([[0.0], np.cumsum([dd[str(x)] for x in dates])])
    return {ent: {"state": (dates, cum), "other": (np.array([], dtype="datetime64[D]"), np.array([0.0]))}}


# --------------------------------------------------------------------------- A4.2: the windows

def test_A4_2_pre_window_is_strictly_before_d_and_day_d_is_in_neither():
    w0, w1 = ies90.window(D)
    b0, b1 = ies90.pre_window(D)
    assert (w0, w1) == (pd.Timestamp("2020-06-02"), pd.Timestamp("2020-08-30"))
    assert (b0, b1) == (pd.Timestamp("2020-03-03"), pd.Timestamp("2020-05-31"))
    assert b1 < pd.Timestamp(D) < w0, "day d belongs to the event and lies in neither window (A4.2)"
    assert (w1 - w0).days == (b1 - b0).days, "B is the scale's own 90 days run backwards -- no new constant"


def test_A4_2_covered_by_is_whole_of_B_not_mere_overlap():
    b0, b1 = ies90.pre_window(D)
    assert ies90.covered_by([_spell("2019-01-01", "2021-01-01")], b0, b1) is True
    assert ies90.covered_by([_spell("2020-04-01", "2021-01-01")], b0, b1) is False, "starts inside B: a recent onset"
    assert ies90.covered_by([_spell("2019-01-01", "2020-05-01")], b0, b1) is False, "ended inside B"


# --------------------------------------------------------------------------- A4.2: COW War

def test_A4_2_cow_war_running_across_all_of_B_is_a_continuation_and_sets_no_level():
    war = _war(inter=[{"war": 1, "name": "Long War", "ent": IRAN, "side": 1, "spells": [_spell("2015-01-01", "2021-01-01")]},
                      {"war": 1, "name": "Long War", "ent": IRAQ, "side": 2, "spells": [_spell("2015-01-01", "2021-01-01")]}])
    level, recs = ies90.score_war(D, {IRAN, IRAQ}, {frozenset((IRAN, IRAQ))}, {IRAN}, war)
    assert level == 0, "a war that was already running across all of B asserts nothing about this event"
    assert [r["rule"] for r in recs] == ["WAR.inter.continuation"]
    assert recs[0]["level"] is None, "undated-for-W: no level, not level 0 (the record is kept as detail)"


def test_A4_2_a_war_that_STARTS_at_or_near_d_keeps_level_3():
    """The case the rule must not break: Yom Kippur 1973, Kuwait 1990, Iraq 2003 are war ONSETS, and level 3
    on them is the correct label, not a mechanical one."""
    for start in ("2020-06-01", "2020-05-31", "2020-06-15"):      # on d, the day before d, and inside W
        war = _war(inter=[{"war": 2, "name": "New War", "ent": IRAN, "side": 1, "spells": [_spell(start, "2021-01-01")]},
                          {"war": 2, "name": "New War", "ent": IRAQ, "side": 2, "spells": [_spell(start, "2021-01-01")]}])
        level, recs = ies90.score_war(D, {IRAN, IRAQ}, {frozenset((IRAN, IRAQ))}, {IRAN}, war)
        assert level == 3, f"war starting {start} is an onset, not a continuation"
        assert recs[0]["rule"] == "WAR.inter.pair"


def test_A4_2_intra_state_continuation_uses_the_same_predicate():
    war = _war(intra=[{"war": 9, "name": "Long Insurgency", "ents": {IRAN}, "spells": [_spell("2010-01-01", "2021-01-01")]}])
    level, recs = ies90.score_war(D, {IRAN}, set(), {IRAN}, war)
    assert level == 0 and recs[0]["rule"] == "WAR.intra.continuation" and recs[0]["level"] is None


# --------------------------------------------------------------------------- A4.2 / A4.4: UCDP GED

def test_A4_2_ged_level_already_reached_over_B_is_a_continuation():
    series = _ged(IRAN, {"2020-04-01": 5000, "2020-07-01": 6000})     # war level before AND after
    lv, delta_lv, deaths, recs = ies90.score_ged(D, {IRAN}, series)
    assert lv is None, "the war was already at level 3 across B: the count in W says nothing about the event"
    assert recs[0]["rule"] == "GED.location.continuation"
    assert deaths["deaths_ged_pre90"] == 5000 and deaths["deaths_ged_90"] == 6000


def test_A4_2_ged_fresh_escalation_from_a_quiet_baseline_keeps_its_level():
    series = _ged(IRAN, {"2020-04-01": 10, "2020-07-01": 6000})
    lv, delta_lv, deaths, recs = ies90.score_ged(D, {IRAN}, series)
    assert lv == 3 and recs[0]["rule"] == "GED.location.ge250"
    assert delta_lv == 3


def test_A4_4_deaths_on_day_d_are_reported_separately_and_are_in_neither_window():
    """The correction in A4.1(ii): the old pre-window ran [d-89, d] and counted the event's own violence as
    'before'. Ukraine 2022 read 20,473 'before' of which 20,394 were on d itself."""
    series = _ged(IRAN, {"2020-06-01": 9000, "2020-07-01": 300})
    lv, delta_lv, deaths, recs = ies90.score_ged(D, {IRAN}, series)
    assert deaths["deaths_ged_on_d"] == 9000
    assert deaths["deaths_ged_pre90"] == 0, "day d is not 'before'"
    assert deaths["deaths_ged_90"] == 300, "day d is not 'after' either"
    assert lv == 3, "with a quiet B this is a fresh escalation, not a continuation"


def test_A4_4_delta_level_is_computed_and_is_never_the_level():
    series = _ged(IRAN, {"2020-04-01": 5000, "2020-07-01": 5400})     # +400 on a war-level baseline
    lv, delta_lv, deaths, recs = ies90.score_ged(D, {IRAN}, series)
    assert lv is None, "the G target excludes it (A4.3)"
    assert delta_lv == 3, "the increment is published beside it (A4.4)"
    assert deaths["deaths_ged_delta"] == 400


def test_A4_4_delta_level_floors_at_zero_when_violence_falls():
    series = _ged(IRAN, {"2020-04-01": 5000, "2020-07-01": 30})
    lv, delta_lv, deaths, recs = ies90.score_ged(D, {IRAN}, series)
    assert deaths["deaths_ged_delta"] == -4970 and delta_lv == 0


def test_A4_2_a_dated_zero_in_W_is_still_a_zero_not_a_continuation():
    """Rule 3 must survive: a covering source that looked at W and found nothing is a TRUE zero."""
    series = _ged(IRAN, {"2020-04-01": 5000})
    lv, delta_lv, deaths, recs = ies90.score_ged(D, {IRAN}, series)
    assert lv == 0 and recs[0]["rule"] == "NONE.covered", "nothing in W is a dated zero, whatever B held"


# --------------------------------------------------------------------------- A4.2 rule 2: no level is not level 0

def test_A4_2_rule_2_an_event_whose_records_are_all_undated_is_no_independent_outcome_not_zero():
    """The 18 false zeros (A4.1 iii): abqaiq_attack_2019 and soleimani_strike_2020 were scored level 0 = 'none'
    while ICB recorded a crisis ongoing at d. Under rule 2 they are no_independent_outcome, and counted."""
    sysd = pd.DataFrame([{"crisno": 1, "crisname": "ONGOING CRISIS", "trigdate": pd.Timestamp("2019-01-01"),
                          "termdate": pd.Timestamp("2021-01-01"), "viol": 4, "forout": 5}])
    level, deal, recs = ies90.score_icb(D, {IRAN}, sysd, {1: {IRAN}})
    assert recs[0]["level"] is None, "ongoing at d yields no level (Amendment 1.1)"
    assert recs[0]["rule"] == "ICB.single.ongoing", "and now carries a rule id, so rule 2 can see it (A4.2)"
    assert level == 0, "score_icb still returns its own max; the event-level rule is what must not call this 0"


def test_A4_2_ongoing_icb_and_mid_records_carry_rule_ids_so_they_are_never_silently_dropped():
    """A null rule_fired made the undated records invisible to the event-level decision; they are now labelled."""
    mid = pd.DataFrame([{"disno": 7, "namea": "IRN", "nameb": "IRQ", "ea": IRAN, "eb": IRAQ,
                         "pair": frozenset((IRAN, IRAQ)), "start": pd.Timestamp("2019-01-01"),
                         "end": pd.Timestamp("2021-01-01"), "hihost": 5, "settlmnt": 0, "war": 1}])
    level, deal, recs = ies90.score_mid(D, {IRAN, IRAQ}, {frozenset((IRAN, IRAQ))}, mid)
    assert recs[0]["level"] is None and recs[0]["rule"] == "MID.pair.ongoing"


# --------------------------------------------------------------------------- A4.6 / A4.7: the guard rails

def test_A4_6_the_counts_mode_does_not_write_to_event_outcomes():
    """Session K publishes counts with write=False while B holds an experiment open on the table."""
    src_txt = (ROOT / "src" / "state" / "ies90.py").read_text()
    i = src_txt.index("def run(")
    body = src_txt[i:src_txt.index("\ndef ", i + 10)]
    assert "if write:" in body, "the DELETE/INSERT must stay behind the write flag"
    delete_at = body.index("DELETE FROM event_outcomes")
    assert body.index("if write:") < delete_at, "no path may delete ies90 rows with write=False"


def test_A4_5_the_prediction_is_registered_in_the_amendment_before_it_is_scored():
    """The numbers in A4_PREDICTION must be the ones written into OUTCOME_MAPPING.md, or the prediction is
    being edited after the fact."""
    doc = (ROOT / "docs" / "reference" / "OUTCOME_MAPPING.md").read_text()
    assert "### A4.5 Expected effect on n and on the level distribution" in doc
    for point in ("~15", "~34", "~58", "~62", "~122"):
        assert point in doc, f"predicted point estimate {point} missing from the registered amendment"
    for k, v in ies90.A4_PREDICTION.items():
        assert f"~{v['point']}" in doc, f"{k}: code predicts {v['point']}, the amendment does not say so"
