"""Amendment C (physical-quantity outcomes) as computed. Every test names the registered section
it covers. The point of these is that the SEAL held: Amendment C fixed each sample size in advance
and the code must reproduce them, and the estimator must be the v2 object, not a new one.

Nothing here fabricates a row. The counts are recomputed from the real corpus in data/oil.db and
the coefficients are read from the committed data/ripple/physical.json."""
import json
import sqlite3
from pathlib import Path

import numpy as np
import pytest

import ripple_lp as R
import ripple_physical as P

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "ripple" / "physical.json"


@pytest.fixture(scope="module")
def conn():
    c = sqlite3.connect(ROOT / "data" / "oil.db")
    yield c
    c.close()


@pytest.fixture(scope="module")
def payload():
    if not OUT.exists():
        pytest.skip("data/ripple/physical.json not built; run src/ripple_physical.py")
    return json.loads(OUT.read_text())


# --- the seal: every n Amendment C fixed in advance ------------------------------------------

C2_REGISTERED_N = {"chokepoint_disruption": 21, "infrastructure_attack": 21,
                   "conflict_escalation": 34, "opec_decision": 38, "sanctions": 36,
                   "demand_shock": 13, "policy_response": 36, "all": 67, "tightening": 51}
C3_REGISTERED_N = {"chokepoint_disruption": 14, "infrastructure_attack": 14,
                   "conflict_escalation": 17, "opec_decision": 15, "sanctions": 19,
                   "demand_shock": 9, "policy_response": 22, "all": 16, "tightening": 24}


def test_c2_jodi_deoverlapped_event_counts_match_the_registered_numbers(conn):
    ev = R.load_events(conn)
    sets, _ = P.window_shock_sets(ev, ("day", "week", "month"), P.JODI_W0, P.JODI_W1)
    assert {k: len(v) for k, v in sets.items()} == C2_REGISTERED_N


def test_c2_jodi_window_is_294_months_and_67_of_them_carry_an_event(conn):
    ev = R.load_events(conn)
    sets, _ = P.window_shock_sets(ev, ("day", "week", "month"), P.JODI_W0, P.JODI_W1)
    F = P.build_jodi_frame(conn, sets["all"])
    assert len(F["idx"]) == 294
    import pandas as pd
    months = {pd.Timestamp(d).to_period("M") for d in sets["all"]}
    assert len(months) == 67


def test_c3_portwatch_deoverlapped_event_counts_match_the_registered_numbers(conn):
    ev = R.load_events(conn)
    sets, _ = P.window_shock_sets(ev, ("day",), P.PW_W0, P.PW_W1)
    assert {k: len(v) for k, v in sets.items()} == C3_REGISTERED_N


def test_c3_the_registered_counterintuitive_fact_pooled_all_is_smaller_than_tightening(conn):
    """C.3 recorded this in advance so it would not later look like a bug: in the 2019+ window the
    35-day chain rule merges events, so 'all' de-overlaps to FEWER clusters than 'tightening'."""
    ev = R.load_events(conn)
    sets, _ = P.window_shock_sets(ev, ("day",), P.PW_W0, P.PW_W1)
    assert len(sets["all"]) < len(sets["tightening"])
    assert len(sets["all"]) == 16 and len(sets["tightening"]) == 24


def test_c3_portwatch_window_is_2799_calendar_days_with_no_missing_day(conn):
    ev = R.load_events(conn)
    sets, _ = P.window_shock_sets(ev, ("day",), P.PW_W0, P.PW_W1)
    F = P.build_pw_frame(conn, sets["all"], calendar=True)
    assert len(F["idx"]) == 2799
    for cp in P.CHOKEPOINTS:
        y = F["nodes"][f"{cp}.n_tanker"]["y"]
        assert np.isfinite(y).all(), cp


def test_c2_21_production_series_carry_at_least_200_months(conn):
    """Amendment C.2 stated 21 before anything was computed."""
    cov = P.jodi_coverage(conn)
    assert cov["production_series_ge_200_months"] == 21
    assert cov["n_series"] == 106


# --- the registered restrictions -------------------------------------------------------------

def test_c3_every_named_chokepoint_cell_is_below_the_registered_minimum(payload):
    """The registered PRIMARY test for PortWatch is the chokepoint the event itself names. It is
    INSUFFICIENT at all seven -- a fact about the corpus, not an estimate."""
    prim = payload["portwatch"]["named_chokepoint_primary"]
    assert len(prim) == 7
    for row in prim:
        assert row["n_named_deoverlapped"] < R.MIN_N, row["chokepoint"]
        assert row["verdict"] == "INSUFFICIENT"


def test_c2_the_producers_the_corpus_names_are_the_ones_that_stopped_reporting(payload):
    """The selection statement. Iran is named 21 times and reports production for 8 of them."""
    counts = {r["cc"]: r for r in payload["jodi"]["named_producer_counts"]}
    assert counts["ir"]["last_production_report"] == "2018-07-01"
    assert counts["ir"]["named_deoverlapped"] > counts["ir"]["named_within_span"]
    assert counts["ir"]["named_lost_to_go_dark"] > 0
    lost = sum(r["named_lost_to_go_dark"] for r in payload["jodi"]["named_producer_counts"])
    assert lost > 0


def test_c2_the_balanced_panel_excludes_every_reporter_that_went_dark(payload):
    """A country that stops REPORTING must never be able to look like a country that stopped
    PRODUCING. The panel is balanced for exactly that reason."""
    members = {k.split(".")[0] for k in payload["jodi"]["balanced_panel_members"]["crude_production"]}
    went_dark = set(payload["jodi_coverage"]["went_dark"])
    assert not (members & went_dark), members & went_dark


def test_c2_demand_shock_was_registered_insufficient_in_advance_and_is_withheld(payload):
    """C.2 fixed demand_shock at n=13 < 15 BEFORE computing. Its pooled-panel band happens to
    exclude zero; the registered verdict is still INSUFFICIENT and the number is not read."""
    row = next(r for r in payload["jodi"]["pooled_panel"]
               if r.get("flow") == "crude_production" and r.get("shock") == "demand_shock")
    assert row["n_events"] == 13
    assert row["verdict"] == "INSUFFICIENT"


# --- the estimator is the v2 object ----------------------------------------------------------

def test_amendment_c4_no_registered_constant_was_changed():
    """C.4: no change to horizons, lag lengths, minimum n, clustering rule or BH level."""
    assert R.MIN_N == 15 and R.CLUSTER_DAYS == 35 and R.BH_Q == 0.10
    assert R.H_MONTHLY == [0, 1, 2, 3, 6, 9, 12] and R.P_MONTHLY == 6
    assert R.H_DAILY == [0, 1, 2, 5, 10, 20, 40, 60] and R.P_DAILY == 5
    assert P.JODI_HEADLINE == 3 and P.PW_HEADLINE == 5
    assert P.PW_SHOCKS == R.CLASSES + ["tightening"]          # the pooled 'all' is not used [C.3]


def test_estimator_primitives_are_imported_from_ripple_lp_not_reimplemented():
    src = (ROOT / "src" / "ripple_physical.py").read_text()
    assert "import ripple_lp as R" in src
    for fn in ["def ols(", "def lp_design(", "def run_lp(", "def placebo(", "def verdict(",
               "def bh_flags(", "def cluster_first_dates("]:
        assert fn not in src, f"{fn} is re-implemented; it must come from ripple_lp"


def test_verdict_vocabulary_is_only_the_registered_three(payload):
    allowed = {"TRANSMITTING", "NULL", "INSUFFICIENT", None}
    for group in [payload["jodi"]["exploratory"], payload["jodi"]["balanced_aggregate"],
                  payload["portwatch"]["secondary_calendar"]]:
        for r in group:
            assert r["verdict"] in allowed, r["verdict"]


# --- the results that must not be misread ----------------------------------------------------

def test_c3_no_transit_cell_transmits(payload):
    t = payload["portwatch"]["secondary_tally"]
    assert t["TRANSMITTING"] == 0
    assert t["cells"] == t["TRANSMITTING"] + t["NULL"] + t["INSUFFICIENT"]


def test_exploratory_transmitting_count_sits_inside_its_own_null_expectation(payload):
    """21-22 hits out of ~954 cells is what a complete null looks like at this base rate. The
    test exists so nobody reads the table as a discovery."""
    t = payload["jodi"]["exploratory_tally"]
    lo, hi = t["null_expected_range"]
    assert lo <= t["TRANSMITTING"] <= hi
    tc = payload["jodi"]["exploratory_tally_clean"]
    lo, hi = tc["null_expected_range"]
    assert lo <= tc["TRANSMITTING"] <= hi


def test_external_check_recovers_the_identified_supply_shock_in_the_physical_data(payload):
    """The check that separates 'weak shocks' from 'broken data'. B-H's identified structural
    supply shock must move JODI aggregate production with the registered expected sign at impact,
    using the same code that produces every null above."""
    ec = payload["jodi"]["external_check"]["bh_supply_shock"]
    h0 = next(x for x in ec["irf"] if x["h"] == 0)
    assert h0["beta"] > 0                       # positive B-H supply shock = more production
    assert h0["ehw_covers_zero"] is False
    price = next(x for x in ec["on_crude_price"]["irf"] if x["h"] == 0)
    assert price["beta"] < 0                    # ... and a lower price
    assert price["ehw_covers_zero"] is False


def test_the_production_response_dies_before_the_registered_headline_horizon(payload):
    """Why the h=3 headline could not have found a physical response: even for an identified
    shock, the production effect is gone by h=2 while the price effect runs to h=12."""
    ec = payload["jodi"]["external_check"]["bh_supply_shock"]
    prod = {x["h"]: x for x in ec["irf"]}
    price = {x["h"]: x for x in ec["on_crude_price"]["irf"]}
    assert prod[0]["ehw_covers_zero"] is False and prod[1]["ehw_covers_zero"] is False
    assert prod[3]["ehw_covers_zero"] is True
    for h in [0, 1, 2, 3, 6, 9, 12]:
        assert price[h]["ehw_covers_zero"] is False, h


def test_the_null_is_bounded_not_empty(payload):
    """A null with no yardstick says nothing. At h=0 the pooled tightening dummy rules out a
    production fall larger than a fraction of one SD of the identified shock."""
    b = payload["jodi"]["bounded_null"]["h0"]
    assert b["one_sd_identified_shock_on_production_pct"] > 0
    t = b["tightening"]
    assert t["as_share_of_one_sd_identified_shock"] < 1.0


def test_hormuz_2026_is_reported_as_an_episode_and_never_as_an_estimate(payload):
    """n = 1. The largest physical disruption in the sample must appear as a level, and no
    verdict word may be attached to it."""
    e = payload["episodes"]["hormuz_2026"]["hormuz"]
    assert e["change_pct"] < -50
    assert "verdict" not in e and "beta" not in e


def test_the_degeneracy_screen_is_computed_from_series_only(payload):
    """The screen is post-hoc and says so; it may only look at the data, never at a coefficient."""
    sc = payload["degeneracy_screen"]
    assert "post-hoc" in sc["rule"].lower() or "degenerate if" in sc["rule"]
    for sid, v in sc["per_series"].items():
        assert set(v) == {"zero_share", "sd_dlog", "median", "degenerate"}
