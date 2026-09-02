"""OUTCOME_MAPPING.md Amendment 1 + 1.1 + 2 tests: the IES-90 rules are total, dated and deterministic on synthetic
records; a level is never guessed when no source covers the window; the corpus run (event_outcomes source='ies90',
data/state/ies90_distribution.json, data/audits/ies90_audit_30.csv) is internally consistent. The corpus-level tests
run against oil.db after `python3 src/state/ies90.py` and skip, never fake, when it has not run."""
import csv
import json
import sqlite3
from collections import Counter

import pandas as pd
import pytest

from _helpers import P
import ies90 as I


def _frames():
    """Tiny synthetic sources: one MID dispute wholly inside W, one ongoing at d; one ICB crisis triggered in W that ends
    after W; one COW inter-state war spell; GED deaths in Iran."""
    mid = pd.DataFrame([
        {"disno": 1, "namea": "IRN", "nameb": "IRQ", "ea": "country.iran", "eb": "country.iraq", "pair": frozenset(("country.iran", "country.iraq")),
         "start": pd.Timestamp("2000-02-01"), "end": pd.Timestamp("2000-03-01"), "hihost": 4, "settlmnt": 1, "war": 0, "year": 2000},
        {"disno": 2, "namea": "IRN", "nameb": "USA", "ea": "country.iran", "eb": "country.usa", "pair": frozenset(("country.iran", "country.usa")),
         "start": pd.Timestamp("1999-06-01"), "end": pd.Timestamp("2000-06-01"), "hihost": 4, "settlmnt": 0, "war": 0, "year": 2000},
    ])
    icb = pd.DataFrame([{"crisno": 9, "crisname": "SYNTH", "trigdate": pd.Timestamp("2000-01-20"), "termdate": pd.Timestamp("2000-08-01"),
                         "viol": 4, "forout": 1, "outesr": 1}])
    members = {9: {"country.iran", "country.iraq"}}
    war = {"inter": [{"war": 7, "name": "Synthetic War", "ent": "country.iran", "side": 1, "spells": [(pd.Timestamp("2000-03-15"), pd.Timestamp("2000-05-01"))]},
                     {"war": 7, "name": "Synthetic War", "ent": "country.iraq", "side": 2, "spells": [(pd.Timestamp("2000-03-15"), pd.Timestamp("2000-05-01"))]}],
           "intra": [{"war": 8, "name": "Synthetic Civil War", "ents": {"country.libya"}, "spells": [(pd.Timestamp("1999-01-01"), pd.Timestamp("2001-01-01"))]}]}
    midi = pd.DataFrame([{"incidnum": 100, "dispnum": 1, "start": pd.Timestamp("2000-02-10"), "end": pd.Timestamp("2000-02-12"), "hostlev": 3, "fatality": 0, "action": 7}])
    midip = {100: [("country.iran", 1), ("country.iraq", 0)]}
    import numpy as np
    ged = {"country.iran": {"state": (np.array(["2000-01-05", "2000-02-01", "2000-03-30"], dtype="datetime64[D]"), np.array([0.0, 10.0, 40.0, 300.0]))}}
    return {"icb": icb, "icb_members": members, "mid": mid, "midi": midi, "midip": midip, "ged": ged, "war": war}


def test_i1_maps_and_thresholds_are_total_and_dated():
    assert set(I.HOSTLEV_TO_LEVEL) == {1, 2, 3, 4, 5} and set(I.HOSTLEV_TO_LEVEL.values()) <= {0, 1, 2, 3}
    assert set(I.VIOL_TO_LEVEL) == {1, 2, 3, 4} and I.VIOL_TO_LEVEL[4] == 3 and I.VIOL_TO_LEVEL[1] == 1
    assert I.ged_level(24) == 0 and I.ged_level(25) == 2 and I.ged_level(249) == 2 and I.ged_level(250) == 3
    assert round(1000 * 90 / 365, 1) == 246.6 and I.GED_WAR == 250          # the pro-rated war line, executed
    w0, w1 = I.window("2000-01-01")
    assert (w0.date().isoformat(), w1.date().isoformat()) == ("2000-01-02", "2000-03-31")   # (d, d+90]


def test_i2_coverage_means_the_whole_window_is_inside_the_source_period():
    assert I.covers("midi", "1993-01-01") and not I.covers("midi", "1992-12-31")
    assert I.covers("midi", "2014-10-02") and not I.covers("midi", "2014-10-03")   # d+90 = 2014-12-31 vs 2015-01-01
    assert I.covers("war", "2007-10-02") and not I.covers("war", "2007-10-03") and I.covers("war_intra", "2014-10-02")
    assert I.covers("ged", "2025-10-02") and not I.covers("ged", "2025-10-03") and not I.covers("icb", "2022-01-01")


def test_i3_each_source_asserts_only_what_it_can_date():
    F = _frames()
    d, A = "2000-01-15", {"country.iran", "country.iraq"}
    pairs = {frozenset(A)}
    # MID: dispute 1 wholly inside W -> hihost 4 -> 2 and a negotiated end in W -> DEAL; dispute 2 (iran-usa) is not in P
    lv, deal, recs = I.score_mid(d, A, pairs, F["mid"])
    assert lv == 2 and deal == 1 and [r["record"] for r in recs] == ["dispute 1 IRN-IRQ"]
    # ICB: triggered in W (01-20) but ends after W -> onset only -> 1, viol 4 recorded as undated peak; no DEAL (termdate outside W)
    lv, deal, recs = I.score_icb(d, A, F["icb"], F["icb_members"])
    assert lv == 1 and deal == 0 and "undated peak" in recs[0]["code"]
    # ICB wholly inside W -> the peak dates -> 3; and its agreement termination in W -> DEAL
    lv, deal, _ = I.score_icb("2000-01-15", A, F["icb"].assign(termdate=pd.Timestamp("2000-03-01")), F["icb_members"])
    assert lv == 3 and deal == 1
    # ICB ongoing at d -> no level
    lv, _, recs = I.score_icb("2000-02-01", A, F["icb"], F["icb_members"])
    assert lv == 0 and recs[0]["level"] is None
    # COW inter-state war: iran and iraq on opposite sides, spell 03-15..05-01 overlaps W -> 3; same-side pairs do not count
    lv, recs = I.score_war(d, A, pairs, A, F["war"], True, True)
    assert lv == 3 and recs[0]["source"] == "war"
    same = {"inter": [{**F["war"]["inter"][0]}, {**F["war"]["inter"][1], "side": 1}], "intra": []}
    assert I.score_war(d, A, pairs, A, same, True, True)[0] == 0
    # intra-state war: location libya in L -> 3
    assert I.score_war(d, {"country.libya"}, set(), {"country.libya"}, F["war"], True, True)[0] == 3
    # MIDI: incident 100 iran vs iraq on opposite sides, hostlev 3 -> 1
    assert I.score_midi(d, A, pairs, F["midi"], F["midip"])[0] == 1
    # GED cum [0, 10, 40, 300] at 01-05 / 02-01 / 03-30: deaths in (01-15, 04-15] = (40-10) + (300-40) = 290 -> 3;
    # pre-window (10-17, 01-15] = 10 (executed below, not recalled)
    lv, d90, pre, other, _ = I.score_ged(d, {"country.iran"}, F["ged"])
    assert (lv, float(d90), float(pre), float(other)) == (3, float((40 - 10) + (300 - 40)), 10.0, 0.0)


def test_i4_precedence_is_the_max_over_covering_sources_and_never_a_guess():
    F = _frames()
    A = {"country.iran", "country.iraq"}
    res = I.score_event("2000-01-15", A, {frozenset(A)}, A, F)
    assert res["level"] == 3 and res["covering"] == ["midi", "war", "icb", "mid", "ged"]
    # A2.1: the pair-matched war sets the level; GED (location) is stored beside it, not a setter
    assert res["basis"] == "dyadic" and res["level_source"] == ["war"] and res["rule_fired"] == ["WAR.inter.pair"]
    assert res["level_location"] == 3 and res["covering_location"] == ["ged"] and res["deal"] == 1
    # no country at all -> nothing covers -> no level, no deal
    res = I.score_event("2000-01-15", set(), set(), set(), F)
    assert res["level"] is None and res["covering"] == [] and res["deal"] is None
    # 2026: beyond every source -> no level
    res = I.score_event("2026-02-28", A, {frozenset(A)}, A, F)
    assert res["level"] is None and res["covering"] == []
    # a covering source with nothing in W asserts 0 (GED-only year, no deaths) -- location basis, NONE.covered
    res = I.score_event("2023-01-15", {"country.qatar"}, set(), {"country.qatar"}, F)
    assert res["level"] == 0 and res["covering"] == ["ged"] and res["deal"] is None
    assert res["basis"] == "location" and res["rule_fired"] == ["NONE.covered"]


def test_i8_amendment_2_dyadic_precedence_over_location_evidence():
    """A2.1: dyadic sources cover W and record nothing for the pair -> level 0 on the dyadic basis even though
    GED reports 290 state-based deaths in the location; the location level is kept beside it."""
    F = _frames()
    A = {"country.iran", "country.iraq"}
    F2 = {**F, "war": {"inter": [], "intra": []}, "midi": F["midi"].iloc[0:0], "midip": {},
          "mid": F["mid"].iloc[0:0], "icb": F["icb"].iloc[0:0]}
    res = I.score_event("2000-01-15", A, {frozenset(A)}, {"country.iran"}, F2)
    assert res["basis"] == "dyadic" and res["level"] == 0 and res["level_location"] == 3
    assert res["rule_fired"] == ["NONE.covered"] and res["covering_dyadic"] == ["midi", "war", "icb", "mid"]
    # the same event with P empty (single country) falls to the location basis and GED decides
    res = I.score_event("2000-01-15", {"country.iran"}, set(), {"country.iran"}, F2)
    assert res["basis"] == "location" and res["level"] == 3 and res["rule_fired"] == ["GED.location.ge250"]


def test_i8b_amendment_2_littoral_map_is_location_only_and_maps_to_known_countries():
    import countries as C
    for ent, states in I.LITTORAL.items():
        assert ent.startswith("chokepoint.") and states and all(s in C.ALL for s in states), ent
    # registered rule ids only
    ok = {"MIDI.pair.overlap", "MIDI.single.overlap", "WAR.inter.pair", "WAR.inter.single", "WAR.intra.location",
          "ICB.pair.wholly", "ICB.pair.onset", "ICB.single.wholly", "ICB.single.onset", "MID.pair.wholly", "MID.pair.onset",
          "MID.single.wholly", "MID.single.onset", "GED.location.ge250", "GED.location.ge25", "NONE.covered", "UNCOVERED"}
    conn = _conn()
    seen = {r for (v,) in conn.execute("SELECT value_text FROM event_outcomes WHERE source='ies90' AND field='rule_fired'") for r in v.split(",")}
    assert seen <= ok, seen - ok
    # every level row has a basis and a rule; location-basis rows carry the Amendment 2 note
    n_lv = conn.execute("SELECT COUNT(*) FROM event_outcomes WHERE source='ies90' AND field='level'").fetchone()[0]
    n_b = conn.execute("SELECT COUNT(*) FROM event_outcomes WHERE source='ies90' AND field='basis' AND value_text IN ('dyadic','location')").fetchone()[0]
    assert n_lv == n_b


# ----------------------------------------------------------------------------- corpus level (after the run)

def _conn():
    if not P.DB.exists():
        pytest.skip("oil.db absent")
    conn = sqlite3.connect(P.DB)
    n = conn.execute("SELECT COUNT(*) FROM event_outcomes WHERE source = 'ies90'").fetchone()[0]
    if n == 0:
        pytest.skip("run python3 src/state/ies90.py first")
    return conn


def test_i5_corpus_every_geopolitical_event_has_one_level_or_is_uncovered():
    conn = _conn()
    geo = {e for (e,) in conn.execute("SELECT event_id FROM events WHERE type IN (?,?,?,?)", I.O.GEO_TYPES)}
    lv = dict(conn.execute("SELECT event_id, value FROM event_outcomes WHERE source='ies90' AND field='level'"))
    un = {e for (e,) in conn.execute("SELECT event_id FROM event_outcomes WHERE source='ies90' AND field='no_independent_outcome'")}
    assert set(lv) | un == geo and not (set(lv) & un)
    assert all(v in (0.0, 1.0, 2.0, 3.0) for v in lv.values())
    cov = dict(conn.execute("SELECT event_id, value_text FROM event_outcomes WHERE source='ies90' AND field='covering'"))
    assert all(cov.get(e) for e in lv) and all(not cov.get(e) for e in un)        # level <=> a covering source
    # Amendment 2: location basis -> level == level_location; dyadic basis -> level <= max over the dyadic sources' levels
    basis = dict(conn.execute("SELECT event_id, value_text FROM event_outcomes WHERE source='ies90' AND field='basis'"))
    loc = dict(conn.execute("SELECT event_id, value FROM event_outcomes WHERE source='ies90' AND field='level_location'"))
    dyc = dict(conn.execute("SELECT event_id, value_text FROM event_outcomes WHERE source='ies90' AND field='covering_dyadic'"))
    per = {}
    for e, f, v in conn.execute("SELECT event_id, field, value FROM event_outcomes WHERE source='ies90' AND field LIKE 'level_%' AND field NOT IN ('level_source', 'level_location')"):
        per.setdefault(e, {})[f[6:]] = v
    for e in lv:
        if basis[e] == "location":
            assert lv[e] == loc[e], (e, lv[e], loc[e])
        else:
            assert lv[e] <= max(per[e][s_] for s_ in dyc[e].split(",")), e
    # the other sources' rows (Step 4) are untouched by the ies90 run
    assert conn.execute("SELECT COUNT(*) FROM event_outcomes WHERE source IN ('icb','mid','ucdp','precedence')").fetchone()[0] > 0


def test_i6_distribution_file_matches_the_database():
    conn = _conn()
    dist = json.loads(I.DIST_OUT.read_text())
    lv = Counter(str(int(v)) for (v,) in conn.execute("SELECT value FROM event_outcomes WHERE source='ies90' AND field='level'"))
    lv["null"] = conn.execute("SELECT COUNT(*) FROM event_outcomes WHERE source='ies90' AND field='no_independent_outcome'").fetchone()[0]
    assert dist["level_counts"] == {k: v for k, v in lv.items() if v}
    assert sum(sum(c.values()) for c in dist["by_decade"].values()) == dist["n_geopolitical_events"]
    assert dist["ged"]["location_only"] is True and isinstance(dist["ged"]["unmapped_country_names"], list)
    assert "retired" in dist["for_the_record_only"]["note"]


def test_i7_audit_sheet_is_30_events_stratified_by_level_and_decade_with_source_rows():
    _conn()
    rows = list(csv.DictReader(open(I.AUDIT_OUT, encoding="utf-8")))
    ev = [r for r in rows if r["row_type"] == "event"]
    assert len(ev) == 30 and all(r["ies90_level"] in ("0", "1", "2", "3") for r in ev)
    assert all(r["basis"] in ("dyadic", "location") and r["rule_fired"] for r in ev)          # A2.3 columns
    assert all(r["joe_check"] == "" and r["joe_note"] == "" for r in rows)
    # every event row is followed by >= 1 source row for the same event
    for i, r in enumerate(rows):
        if r["row_type"] == "event":
            assert rows[i + 1]["row_type"] == "source" and rows[i + 1]["event_id"] == r["event_id"]
    # stratification: no (level, decade) stratum over-represented by more than one seat vs its share of the pool
    dist = json.loads(I.DIST_OUT.read_text())
    pool = dist["audit"]["pool_with_level"]
    strata = Counter((r["ies90_level"], r["event_date"][:3] + "0s") for r in ev)
    pool_strata = {(l, dec): n for dec, c in dist["by_decade"].items() for l, n in c.items() if l != "null"}
    for k, n in strata.items():
        assert abs(n - 30 * pool_strata[k] / pool) < 1.0 + 1e-9, (k, n, pool_strata[k])
