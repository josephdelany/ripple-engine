"""Tests for src/grid_labels.py (Session G, G-4, the dyad-date probe).

Every test names the clause of data/grid/G4_REGISTRATION.md it covers. Nothing here writes to any
table; the fixtures are dicts built in the test, and the published-run assertions read
data/grid/g/PROBE.json.
"""
import datetime as dt
import json
import re
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import grid_labels as G  # noqa: E402
import ies90 as I        # noqa: E402

PROBE = ROOT / "data" / "grid" / "g" / "PROBE.json"


def rec(rule, dates, level, basis="dyadic", source="mid"):
    return {"source": source, "basis": basis, "rule": rule, "record": "r", "dates": dates, "level": level}


def res(level, recs, basis="dyadic", covering=("mid",)):
    return {"level": level, "recs": recs, "basis": basis, "covering": list(covering)}


# ------------------------------------------------------------------ §1 the windows

def test_g4_1_forward_window_excludes_the_grid_date_itself():
    """§1: L is over (t, t+90], so day t is in NEITHER window (OUTCOME_MAPPING A4.4). A rule that put
    day t in the forward window would let the grid date's own violence score its own label."""
    w0, w1 = I.window("2018-06-30")
    assert w0 == pd.Timestamp("2018-07-01") and w1 == pd.Timestamp("2018-09-28")
    b0, b1 = I.pre_window("2018-06-30")
    assert b0 == pd.Timestamp("2018-04-01") and b1 == pd.Timestamp("2018-06-29")
    assert b1 < pd.Timestamp("2018-06-30") < w0


# ------------------------------------------------------------------ §2 the active rule

def _spells():
    p = frozenset(("country.iran", "country.iraq"))
    return {p: [(pd.Timestamp("1990-01-01"), pd.Timestamp("1990-03-01"), "mid")]}, p


def test_g4_2_active_requires_a_record_in_the_lookback_window():
    sp, p = _spells()
    assert G.active_at("1992-01-31", sp, [p]) == [p]            # inside 5 years
    assert G.active_at("1999-01-31", sp, [p]) == []             # 9 years later: out


def test_g4_2_lookback_is_strictly_before_t():
    """§2 clause 2: A_w ends at t-1, so a record starting exactly at t does not make the dyad active."""
    p = frozenset(("country.iran", "country.iraq"))
    sp = {p: [(pd.Timestamp("1998-06-30"), pd.Timestamp("1998-07-30"), "mid")]}
    assert G.active_at("1998-06-30", sp, [p]) == []
    assert G.active_at("1998-07-31", sp, [p]) == [p]


def test_g4_VR3_excludes_a_dyad_selected_on_a_record_still_running_at_t():
    """§4 VR-3: a dyad admitted on a record whose spell ends AFTER t is selected on the future."""
    p = frozenset(("country.iran", "country.iraq"))
    sp = {p: [(pd.Timestamp("1998-01-01"), pd.Timestamp("1999-01-01"), "mid")]}
    assert G.active_at("1998-06-30", sp, [p]) == [p]
    assert G.active_at("1998-06-30", sp, [p], vr3=True) == []


def test_g4_2_ged_cannot_make_a_dyad_active():
    """§2: the GED cache has no dyad field, so it may not select dyads. dyadic_spells must never
    carry a 'ged' source."""
    import ies90 as _I
    src = {"mid": pd.DataFrame(columns=["pair", "start", "end"]), "midi": pd.DataFrame(columns=["incidnum"]),
           "midip": {}, "war": {"inter": [], "intra": []}, "icb": pd.DataFrame(columns=["crisno", "trigdate", "termdate"]),
           "icb_members": {}}
    out = G.dyadic_spells(src)
    assert all(s != "ged" for v in out.values() for _a, _b, s in v)
    assert "ged" not in _I.DYADIC_SOURCES


# ------------------------------------------------------------------ Amendment 1: the VR-2 stamp

def test_A1_1_only_setters_on_the_chosen_basis_are_stamped():
    """A1.1: a record on the OTHER basis, or one that did not set the level, says nothing about when
    the level became knowable. This was the country.canada|country.usa defect."""
    r = res(1, [rec("MID.pair.onset", "1997-11-14..1997-12-01", 1, basis="dyadic"),
                rec("ICB.single.onset", "1997-11-13..2003-02-23", 1, basis="location", source="icb")])
    vin, stamps = G.cell_vintage(r, "1997-11-01", "1998-01-30")
    assert vin == "1997-11-15"                       # the dyadic onset, not the 2003 location record
    assert [s[0] for s in stamps] == ["MID.pair.onset"]


def test_A1_2_onset_rules_are_stamped_from_the_onset_not_the_end():
    """A1.2: the gbr|iraq defect -- MID.pair.onset 1997-11-14..2003-05-02 was stamped 2003-05-03 for a
    level asserted by a dispute that began in November 1997."""
    r = res(1, [rec("MID.pair.onset", "1997-11-14..2003-05-02", 1)])
    assert G.cell_vintage(r, "1997-11-01", "1998-01-30")[0] == "1997-11-15"


def test_A1_2_wholly_rules_are_stamped_from_the_end():
    """A .wholly level is the record's PEAK (hihost / viol), which is known only when it closes."""
    r = res(2, [rec("MID.pair.wholly", "1997-11-14..1997-12-20", 2)])
    assert G.cell_vintage(r, "1997-11-01", "1998-01-30")[0] == "1997-12-21"


def test_A1_2_ged_and_none_covered_are_stamped_at_the_window_close():
    r = res(2, [rec("GED.location.ge25", "2024-04-01..2024-06-29", 2, basis="location", source="ged")],
            basis="location")
    assert G.cell_vintage(r, "2024-04-01", "2024-06-29")[0] == "2024-06-30"


def test_A1_1_a_true_zero_is_stamped_at_the_window_close_not_left_unstamped():
    """A1.3: a covering source that looked and found nothing is knowable when the window closes."""
    r = res(0, [rec("NONE.covered", "2018-04-01..2018-06-29", 0, basis="location", source="ged")],
            basis="location")
    vin, stamps = G.cell_vintage(r, "2018-04-01", "2018-06-29")
    assert vin == "2018-06-30" and stamps[0][0] == "NONE.covered"


def test_A1_a_cell_with_no_level_is_never_stamped():
    """Amendment 4 refused to date it; there is nothing to stamp and the cell has no ΔIES."""
    r = res(None, [rec("MID.pair.ongoing", "1990-01-01..1999-01-01", None)])
    assert G.cell_vintage(r, "1997-11-01", "1998-01-30") == (None, [])


def test_A1_5_the_correction_can_only_raise_vr2_survival():
    """A1.5: every A1 correction removes a stamp or moves one earlier; none can move one later."""
    setter_only = res(1, [rec("MID.pair.onset", "1997-11-14..2003-05-02", 1)])
    with_noise = res(1, [rec("MID.pair.onset", "1997-11-14..2003-05-02", 1),
                         rec("ICB.single.wholly", "1997-11-13..2005-02-23", 1, basis="location", source="icb")])
    assert G.cell_vintage(setter_only, "1997-11-01", "1998-01-30")[0] == \
           G.cell_vintage(with_noise, "1997-11-01", "1998-01-30")[0]


# ------------------------------------------------------------------ §4 VR-1

def test_g4_VR1_uses_a_release_lower_bound_where_the_host_serves_none():
    """§4.1: an unknown release uses coverage_end + 1 day, a LOWER bound on release, which makes
    VR-1's count an UPPER bound on survival. No release date is guessed."""
    rel = G.release_dates()
    assert rel["icb"]["release"] is None and rel["icb"]["bounded"] is True
    assert rel["icb"]["release_lower_bound"] == "2022-01-01"          # ICB covers to 2021-12-31
    assert rel["ged"]["release_lower_bound"] == "2026-01-01"
    assert rel["war"]["release"] == "2022-07-12" and rel["war"]["bounded"] is False


def test_g4_VR1_rejects_a_cell_whose_source_was_released_after_t():
    rel = G.release_dates()
    r = res(2, [rec("MID.pair.wholly", "1997-11-14..1997-12-20", 2)])
    assert G.vr1_ok(r, "1998-01-31", rel)[0] is False                 # dyadic MID released 2025-04-06
    assert G.vr1_ok(r, "2026-01-31", rel)[0] is True


# ------------------------------------------------------------------ Amendment 2

def test_A2_evidence_basis_separates_sided_sources_from_icb_and_ged():
    p = frozenset(("country.gbr", "country.usa"))
    assert "opposed-side" in G.evidence_basis({"MID.pair.wholly"}, p, {p})
    assert "GED location count" in G.evidence_basis({"GED.location.ge25"}, p, {p})
    assert "may be allies" in G.evidence_basis({"ICB.pair.wholly"}, p, {p})
    assert "NEVER opposed" in G.evidence_basis({"ICB.pair.wholly"}, p, set())


# ------------------------------------------------------------------ the published run

@pytest.mark.skipif(not PROBE.exists(), reason="probe not run in this tree")
def test_g4_published_probe_agrees_with_the_registered_degeneracy_rule():
    o = json.loads(PROBE.read_text())
    v = o["verdict"]
    assert v["threshold"] == G.DEGENERATE_SHARE == 0.95
    s = o["years"]["1998"]
    assert v["share_zero_dIES"] == s["dIES"]["share_zero"]
    assert v["share_zero_L"] == s["L"]["share_zero"]
    assert v["degenerate"] == (v["share_zero_dIES"] >= 0.95 or v["share_zero_L"] >= 0.95)


@pytest.mark.skipif(not PROBE.exists(), reason="probe not run in this tree")
def test_g4_published_probe_VR1_is_zero_at_every_probe_year():
    """The finding, asserted: no cell survives the strict dataset-release stamp, at any probe year,
    and that count is already an upper bound (§4.1)."""
    o = json.loads(PROBE.read_text())
    for yr, s in o["years"].items():
        assert s["vintage"]["VR1_strict_release"]["n"] == 0, yr


@pytest.mark.skipif(not PROBE.exists(), reason="probe not run in this tree")
def test_g4_published_probe_has_no_sided_evidence_after_2014():
    """§3 + Amendment 2: MID, MIDI and COW War stop covering at 2014-10-02, so no non-zero cell in
    2018 or 2024 can rest on a source that records which side a state was on."""
    o = json.loads(PROBE.read_text())
    for yr in ("2018", "2024"):
        eb = o["years"][yr]["evidence_basis_of_nonzero_dIES"]
        assert not any("opposed-side" in k for k in eb), (yr, eb)
    assert any("opposed-side" in k for k in o["years"]["1998"]["evidence_basis_of_nonzero_dIES"])


@pytest.mark.skipif(not PROBE.exists(), reason="probe not run in this tree")
def test_g4_every_cell_is_retrospective():
    """§4.2: a COW hostility level, an ICB violence code and a UCDP death estimate are later
    constructions. Under WORLD_STATE_CODEBOOK Amendment 1 that caps what the panel can ever be."""
    o = json.loads(PROBE.read_text())
    for yr, cells in o["cells"].items():
        assert all(c["retrospective"] == 1 for c in cells), yr
        assert o["years"][yr]["vintage"]["retrospective_share"] == 1.0


def test_g4_writes_no_table_and_stays_out_of_Bs_tree():
    """Registration §0/§7: G writes only data/grid/** and src/grid_labels.py. B owns src/walk*.py and
    data/walk_forward/** this session. Checked on the CODE, with docstrings and comments stripped, so
    the module may say what it does not touch without the test reading that as touching it."""
    import ast
    src_text = (ROOT / "src" / "grid_labels.py").read_text()
    tree = ast.parse(src_text)
    for node in ast.walk(tree):                      # drop every docstring
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str)):
                node.body[0].value.value = ""
    code = ast.unparse(tree)
    code = "\n".join(ln.split("#", 1)[0] for ln in code.split("\n"))       # drop comments
    for bad in ("INSERT", "UPDATE ", "DELETE", "CREATE TABLE", "conn.commit", "walk_forward", "walk.py"):
        assert bad not in code, f"grid_labels.py references {bad!r} in code"
    assert "OUT_JSON" in code and 'data' in code


# ================================================================================================
# Amendment 3 — the build: span, VR-3 active set, evidence basis as a FIELD
# ================================================================================================

PANEL = ROOT / "data" / "grid" / "g" / "PANEL.json"


def test_A3_1_the_span_ends_where_the_last_sided_source_stops_covering():
    """A3.1: ies90.covers needs t+90 <= coverage end. MID / MIDI / COW intra-state War end 2014-12-31,
    so 2014-09-30 is the last month-end that clears it and 2014-10-31 is not."""
    assert G.PANEL_END == "2014-09-30"
    assert I.covers("mid", "2014-09-30") and I.covers("midi", "2014-09-30")
    assert not I.covers("mid", "2014-10-31") and not I.covers("midi", "2014-10-31")
    d = G.panel_dates()
    assert d[0] == "1987-01-31" and d[-1] == "2014-09-30" and len(d) == 333


def test_A3_3_evidence_class_order_is_a_total_order_weakest_last():
    assert G.EVIDENCE_ORDER[0] == "opposed_side" and G.EVIDENCE_ORDER[-1] == "undefined"
    assert G.weaker("opposed_side", "ged_location") == "ged_location"
    assert G.weaker("icb_co_actor", "opposed_side") == "icb_co_actor"
    assert G.weaker("opposed_side", "opposed_side") == "opposed_side"


def test_A3_3_a_true_zero_is_classified_by_what_was_covering_not_left_blank():
    """A3.3: a zero recorded while a sided source was covering is a statement about the pair; a zero
    while only GED covers is 'no deaths in either country', which is not."""
    p = frozenset(("country.iran", "country.iraq"))
    sided = {"level": 0, "recs": [], "basis": "dyadic", "covering": ["mid", "ged"], "covering_dyadic": ["mid"]}
    ged_only = {"level": 0, "recs": [], "basis": "location", "covering": ["ged"], "covering_dyadic": []}
    icb_only = {"level": 0, "recs": [], "basis": "dyadic", "covering": ["icb"], "covering_dyadic": ["icb"]}
    assert G.evidence_class_of(sided, p, {p}) == "opposed_side"
    assert G.evidence_class_of(ged_only, p, {p}) == "ged_location"
    assert G.evidence_class_of(icb_only, p, {p}) == "icb_co_actor"
    assert G.evidence_class_of(icb_only, p, set()) == "icb_co_actor_never_opposed"


def test_A3_3_a_nonzero_is_classified_by_the_rule_that_set_it():
    p = frozenset(("country.gbr", "country.usa"))
    icb = res(3, [rec("ICB.pair.wholly", "2018-04-07..2018-04-14", 3, source="icb")])
    mid = res(2, [rec("MID.pair.wholly", "1998-01-16..1998-01-27", 2)])
    ged = res(2, [rec("GED.location.ge25", "2024-04-01..2024-06-29", 2, basis="location", source="ged")],
              basis="location")
    assert G.evidence_class_of(icb, p, set()) == "icb_co_actor_never_opposed"
    assert G.evidence_class_of(mid, p, {p}) == "opposed_side"
    assert G.evidence_class_of(ged, p, {p}) == "ged_location"


def test_A3_3_undefined_is_its_own_class_and_is_the_weakest():
    r = {"level": None, "recs": [], "basis": None, "covering": ["mid"]}
    assert G.evidence_class_of(r, frozenset(("country.a", "country.b")), set()) == "undefined"
    assert G.weaker("opposed_side", "undefined") == "undefined"


def test_A3_6_icb_replication_counts_dyads_per_crisis():
    """A3.6: a crisis with k register actors on the grid sets a level for up to k(k-1)/2 dyads."""
    cells = [{"dyad": d, "L_rules": "ICB.pair.wholly", "L_records": "crisis 489 SYRIA CHEMICAL WEAPONS III"}
             for d in ("a|b", "a|c", "a|d", "b|c", "b|d", "c|d")]
    out = G.icb_replication(cells)
    assert out["n_crises_setting_a_level"] == 1
    assert out["dyads_per_crisis"]["max"] == 6
    assert out["k_to_pairs"]["4"] == 6
    assert out["cells_set_by_icb"] == 6


@pytest.mark.skipif(not PANEL.exists(), reason="panel not built in this tree")
def test_A3_4_the_three_limits_are_carried_in_the_published_panel():
    s = json.loads(PANEL.read_text())
    assert len(s["limits"]) == 3
    joined = " ".join(s["limits"]).lower()
    for must in ("never reaches the present", "never carry validated", "never scores onset"):
        assert must.split()[1] in joined
    assert s["vintage"]["retrospective_share"] == 1.0


@pytest.mark.skipif(not PANEL.exists(), reason="panel not built in this tree")
def test_A3_the_panel_is_never_filtered_by_evidence_class():
    """A3.3: the strict subset is a SELECTION on a field, not a smaller build. Every class must be
    present in the panel, and the classes must sum to the cell count."""
    s = json.loads(PANEL.read_text())
    assert sum(s["evidence_class"].values()) == G.nom(s["size"]["cells"])
    assert G.nom(s["strict_subset"]["cells"]) <= G.nom(s["size"]["cells"])
    assert G.nom(s["strict_subset"]["cells"]) == s["evidence_class"].get("opposed_side", 0)


@pytest.mark.skipif(not PANEL.exists(), reason="panel not built in this tree")
def test_A3_2_VR3_removed_dyad_dates_and_the_count_is_published():
    s = json.loads(PANEL.read_text())
    assert s["size"]["cells_dropped_by_VR3"] >= 0
    assert s["size"]["active_per_date_ract"]["mean"] >= s["size"]["active_per_date_vr3"]["mean"]


@pytest.mark.skipif(not PANEL.exists(), reason="panel not built in this tree")
def test_A3_1_no_cell_falls_outside_the_registered_span():
    s = json.loads(PANEL.read_text())
    assert s["span"]["start"] == "1987-01-31" and s["span"]["end"] == "2014-09-30"
    assert s["span"]["grid_dates"] == 333


# ================================================================================================
# A3.6 — the ICB dyadic-replication finding, as a regression test on the source files
# ================================================================================================

def _icb_files():
    sys.path.insert(0, str(ROOT / "src" / "state"))
    import pandas as _pd
    import panel as _P
    dy = _pd.read_csv(_P.raw_path("icb", "icb_dyads_v16.csv"), encoding="latin-1")
    dy.columns = [c.replace("ï»¿", "").replace("﻿", "") for c in dy.columns]
    act = _pd.read_csv(_P.raw_path("icb", "icb2v16.csv"), encoding="latin-1")
    act.columns = [c.replace("ï»¿", "").replace("﻿", "") for c in act.columns]
    return dy, act


def test_A3_6_icb_crisis_489_has_five_actors_and_only_four_adversarial_dyads():
    """The published claim, asserted against the source files: ICB's ACTOR list for crisis 489 has
    five states (10 possible pairs) while ICB's own DYAD file records four, and UKG-USA is not one
    of them. If ICB v16 is ever replaced this test says so before the paper is wrong."""
    dy, act = _icb_files()
    actors = set(act[act.crisno == 489].cracid.astype(int))
    assert actors == {2, 200, 220, 652, 365}, actors            # USA, UKG, FRN, SYR, RUS
    d489 = dy[dy.crisno == 489]
    pairs = {frozenset((int(a), int(b))) for a, b in zip(d489.statea, d489.stateb)}
    assert pairs == {frozenset((2, 652)), frozenset((200, 652)),
                     frozenset((220, 652)), frozenset((2, 365))}, pairs
    assert frozenset((200, 2)) not in pairs                      # UKG-USA: allies, not a dyad
    assert len(actors) * (len(actors) - 1) // 2 == 10 and len(pairs) == 4


def test_A3_6_score_icb_pairs_on_the_actor_list_not_the_dyad_file():
    """The mechanism, asserted on session A's code rather than described: the dyadic test is set
    containment in the crisis's ACTOR set. Reported to A, never patched by G."""
    src_text = (ROOT / "src" / "state" / "ies90.py").read_text()
    assert "dy = any(set(p) <= mem for p in pairs)" in src_text
    out_text = (ROOT / "src" / "state" / "outcomes.py").read_text()
    assert 'dy = pd.read_csv(P.raw_path("icb", "icb_dyads_v16.csv")' in out_text
    assert "members[int(r.crisno)].add(e)" in out_text            # the pairing is flattened away


def test_A3_6_the_grid_scores_two_allies_as_level_3():
    """The instance, end to end. Slow (loads every source), so it is the only test here that does."""
    import ies90 as _I
    s = _I.load_sources()
    r = _I.score_event("2018-01-31", {"country.gbr", "country.usa"},
                       {frozenset(("country.gbr", "country.usa"))}, {"country.gbr", "country.usa"}, s)
    assert r["level"] == 3 and r["basis"] == "dyadic"
    assert any(x["rule"] == "ICB.pair.wholly" and "489" in x["record"] for x in r["recs"])


# ================================================================================================
# Amendment 4 — the three checks B handed back (share-zero tripwire, VR-3 assertion, effective n)
# ================================================================================================

def _fake_panel(n_zero, n_nonzero, year="1998", cls="opposed_side"):
    rows = [{"date": f"{year}-06-30", "dyad": f"a|b{i}", "dIES": 0.0, "L": 0.0, "evidence_class": cls}
            for i in range(n_zero)]
    rows += [{"date": f"{year}-06-30", "dyad": f"c|d{i}", "dIES": 1.0, "L": 1.0, "evidence_class": cls}
             for i in range(n_nonzero)]
    return pd.DataFrame(rows)


def test_A4_1_tripwire_fires_at_the_registered_bar_and_never_moves_it():
    """A4.1: the bar is §5.1's 0.95 and is never moved; a breach is reported, never dropped."""
    out = G.share_zero_tripwire(_fake_panel(96, 4))
    assert out["bar"] == 0.95 == G.DEGENERATE_SHARE
    assert out["n_breaches"] > 0
    assert out["series"]["full_panel.dIES"]["breach_overall"] is True
    assert out["series"]["full_panel.dIES"]["share_zero_overall"] == 0.96
    # the breaching slice is still in the reported series, not removed
    assert out["series"]["full_panel.dIES"]["per_year"]["1998"]["n"] == 100


def test_A4_1_tripwire_is_silent_below_the_bar():
    out = G.share_zero_tripwire(_fake_panel(90, 10))
    assert out["n_breaches"] == 0
    assert out["series"]["full_panel.dIES"]["breach_overall"] is False


def test_A4_1_tripwire_reports_the_strict_subset_separately():
    """Eight series: {full_panel, opposed_side} x {dIES, L}, each overall and per year."""
    df = pd.concat([_fake_panel(96, 4, cls="opposed_side"), _fake_panel(1, 9, cls="ged_location")])
    out = G.share_zero_tripwire(df)
    assert set(out["series"]) == {"full_panel.dIES", "full_panel.L",
                                  "opposed_side.dIES", "opposed_side.L"}
    assert out["series"]["opposed_side.dIES"]["n_defined"] == 100      # the ged rows excluded
    assert out["series"]["full_panel.dIES"]["n_defined"] == 110


def test_A4_2_admission_audit_catches_a_cell_admitted_on_a_record_running_at_t():
    """A4.2: applying VR-3 and checking it held are different things. One violation voids the panel."""
    p = frozenset(("country.iran", "country.iraq"))
    df = pd.DataFrame([{"date": "1998-06-30", "dyad": "country.iran|country.iraq"}])
    ok = {p: [(pd.Timestamp("1997-01-01"), pd.Timestamp("1997-06-01"), "mid")]}
    bad = {p: [(pd.Timestamp("1997-01-01"), pd.Timestamp("1999-06-01"), "mid")]}   # still running at t
    assert G.admission_audit(df, ok)["asserted"] is True
    a = G.admission_audit(df, bad)
    assert a["asserted"] is False and a["violations"] == 1 and a["first_violation"]["dyad"].endswith("iraq")


def test_A4_2_admission_audit_catches_a_dyad_with_no_admitting_record_at_all():
    df = pd.DataFrame([{"date": "1998-06-30", "dyad": "country.iran|country.iraq"}])
    assert G.admission_audit(df, {})["asserted"] is False


@pytest.mark.skipif(not PANEL.exists(), reason="panel not built in this tree")
def test_A4_2_the_published_panel_passes_its_own_admission_audit():
    s = json.loads(PANEL.read_text())
    a = s["admission_audit"]
    assert a["asserted"] is True and a["violations"] == 0
    assert a["cells_checked"] == G.nom(s["size"]["cells"])


@pytest.mark.skipif(not PANEL.exists(), reason="panel not built in this tree")
def test_A4_3_effective_n_never_exceeds_nominal():
    """B's same-day correction, taken: a DEFF below 1 is a finite-sample artefact and is floored,
    so n_eff may never exceed n_nominal."""
    s = json.loads(PANEL.read_text())
    for scope in ("full_panel", "opposed_side"):
        v = s["effective_n"][scope]
        assert v["n_eff_two_way"] <= v["n_nominal"]
        assert v["n_eff_block"] <= v["n_nominal"]
        assert v["block"]["deff_used"] >= 1.0


@pytest.mark.skipif(not PANEL.exists(), reason="panel not built in this tree")
def test_A4_3_the_reconciliation_with_Bs_deff_is_published_with_both_panels():
    """A reader seeing DEFF 1.5 here and 56 in B's file must be given both panels, not one number."""
    s = json.loads(PANEL.read_text())
    r = s["effective_n"]["reconciliation_with_B"]
    assert r["B_panel"]["n_dyads"] > r["G_panel"]["n_dyads"]
    assert r["B_panel"]["n_nominal_cells"] > r["G_panel"]["n_nominal_cells"]
    assert r["B_panel"]["n_dyads_with_any_variation"] < r["B_panel"]["n_dyads"]
    assert "different objects" in r["why_they_differ"]


@pytest.mark.skipif(not PANEL.exists(), reason="panel not built in this tree")
def test_A4_1_the_published_tripwire_reports_breaches_without_dropping_them():
    """The panel is inside the bar overall and breaches it in the Gulf War shadow years. Both facts
    must be published, and the breaching years must still be in the panel."""
    s = json.loads(PANEL.read_text())
    t = s["share_zero_tripwire"]
    assert t["bar"] == 0.95
    assert t["series"]["full_panel.dIES"]["breach_overall"] is False        # inside the bar overall
    assert t["n_breaches"] > 0                                             # and breaching in slices
    years = {b["year"] for b in t["breaches"]}
    assert years & {"1991", "1992", "1993"}, years
    assert s["by_year"]["1992"]["cells"] > 0                               # not dropped


# ================================================================================================
# Amendment 5 — the effective count is not optional. These tests are the enforcement; without them
# A5 is a convention an author in a hurry can drop.
# ================================================================================================

PANEL_MD = ROOT / "data" / "grid" / "g" / "PANEL.md"
HEADLINE_KEYS = (("size", "cells"), ("dIES", "n_defined"), ("strict_subset", "cells"))


def test_A5_1_paired_is_an_object_and_never_exceeds_nominal():
    en = {"n_eff_two_way": 900.0, "n_eff_block": 950.0, "n_nonzero_nominal": 40}
    p = G.paired(1000, en)
    assert p["nominal"] == 1000 and p["n_eff_two_way"] == 900.0 and p["informative"] == 40
    assert "note" in p and p["n_eff_two_way"] <= p["nominal"]
    assert G.nom(p) == 1000 and G.nom(1000) == 1000              # readers use nom() for either shape


def test_A5_1_apply_amendment_5_is_idempotent():
    s = {"size": {"cells": 10, "distinct_dyads": 3}, "dIES": {"n_defined": 8, "n_nonzero": 2},
         "strict_subset": {"cells": 7, "dIES_nonzero": 1}, "span": {"start": "a", "end": "b"},
         "effective_n": {"full_panel": {"n_eff_two_way": 5.0, "n_eff_block": 6.0, "n_nonzero_nominal": 2},
                         "opposed_side": {"n_eff_two_way": 4.0, "n_eff_block": 5.0, "n_nonzero_nominal": 1}}}
    a = G.apply_amendment_5(dict(s))
    b = G.apply_amendment_5(G.apply_amendment_5(dict(s)))
    assert a["size"]["cells"] == b["size"]["cells"] == {"nominal": 10, "n_eff_two_way": 5.0,
                                                       "n_eff_block": 6.0, "informative": 2,
                                                       "note": G.PAIR_NOTE}


def test_A5_3_the_citation_line_cannot_exist_without_the_effective_count():
    s = G.apply_amendment_5({
        "size": {"cells": 15740, "distinct_dyads": 156}, "dIES": {"n_defined": 14344, "n_nonzero": 1160},
        "strict_subset": {"cells": 14232, "dIES_nonzero": 1059},
        "span": {"start": "1987-01-31", "end": "2014-09-30"},
        "effective_n": {"full_panel": {"n_eff_two_way": 9732.7, "n_eff_block": 13553.8, "n_nonzero_nominal": 1160},
                        "opposed_side": {"n_eff_two_way": 12076.4, "n_eff_block": 13589.2, "n_nonzero_nominal": 1059}}})
    assert "15,740" in s["cite"] and "9,733" in s["cite"] and "1,160" in s["cite"]
    assert "overstates" in s["cite"]


@pytest.mark.skipif(not PANEL.exists(), reason="panel not built in this tree")
def test_A5_1_no_headline_count_in_the_published_json_is_a_bare_integer():
    """A5.1: a programmatic reader gets the pair or a KeyError. If this ever fails, someone can quote
    the nominal size of this panel without its effective size, which is the thing A5 exists to stop."""
    s = json.loads(PANEL.read_text())
    for a, b in HEADLINE_KEYS:
        v = s[a][b]
        assert isinstance(v, dict), f"{a}.{b} is a bare {type(v).__name__} -- Amendment 5 violated"
        for k in ("nominal", "n_eff_two_way", "n_eff_block", "informative", "note"):
            assert k in v, f"{a}.{b} missing {k}"
        assert v["n_eff_two_way"] <= v["nominal"]
        assert v["informative"] <= v["nominal"]


@pytest.mark.skipif(not PANEL_MD.exists(), reason="panel not built in this tree")
def test_A5_5_every_nominal_figure_in_the_report_has_an_effective_figure_beside_it():
    """A5.5, the enforcement Joe asked for: 'make the effective number impossible to omit'. Every
    occurrence of the nominal cell count in PANEL.md must have an effective figure within 300
    characters. A future edit that reintroduces a bare count fails here."""
    s = json.loads(PANEL.read_text())
    md = PANEL_MD.read_text()
    nominal = f"{G.nom(s['size']['cells']):,}"
    eff = f"{s['size']['cells']['n_eff_two_way']:,.0f}"
    assert nominal in md, f"the nominal count {nominal} does not appear in PANEL.md at all"
    hits = [m.start() for m in re.finditer(re.escape(nominal), md)]
    bare = G.bare_nominal_offsets(md, nominal, eff)
    assert not bare, (f"{len(bare)} of {len(hits)} occurrences of {nominal} in PANEL.md carry no "
                      f"effective figure ({eff}) within 300 characters; first at offset {bare[:1]}")


@pytest.mark.skipif(not PANEL_MD.exists(), reason="panel not built in this tree")
def test_A5_3_the_report_leads_with_the_citation_line():
    s = json.loads(PANEL.read_text())
    md = PANEL_MD.read_text()
    assert s["cite"] in md
    assert md.index(s["cite"]) < md.index("## 1. Size"), "the cite line must precede the size section"


def test_A5_4_there_is_exactly_one_writer_and_it_runs_the_checks_first():
    """A5.4: no code path publishes a panel without its effective counts, because the only writer
    applies Amendment 5 and the only route to it runs A4.1-A4.3 first."""
    src_text = (ROOT / "src" / "grid_labels.py").read_text()
    assert src_text.count('(PANEL_DIR / "PANEL.json").write_text') == 1
    assert src_text.count('(PANEL_DIR / "PANEL.md").write_text') == 1
    i = src_text.index("def write_panel(")
    assert "apply_amendment_5(s)" in src_text[i:i + 700]
    j = src_text.index("def finalize(")
    body = src_text[j:j + 900]
    for check in ("share_zero_tripwire(df)", "admission_audit(df, spells)", "effective_n(df)", "write_panel("):
        assert check in body, check


def test_A5_5_the_enforcement_itself_catches_a_bare_nominal():
    """A test of the test. An enforcement nobody has seen fail is not an enforcement."""
    good = "the panel has 15,740 cells (n_eff 9,733) and that is the pair"
    bad = "the panel has 15,740 cells." + (" filler." * 60) + " n_eff 9,733 much later"
    assert G.bare_nominal_offsets(good, "15,740", "9,733") == []
    assert G.bare_nominal_offsets(bad, "15,740", "9,733") == [bad.index("15,740")]
    # it is the WINDOW that decides, not the presence of the number somewhere in the file
    assert G.bare_nominal_offsets(bad, "15,740", "9,733", window=10_000) == []
    # and it fires on the real published file the moment a pair is broken (negative control)
    md = PANEL_MD.read_text() if PANEL_MD.exists() else good
    tampered = md.replace("15,740 cells nominal — n_eff 9,733", "15,740 cells", 1)
    if tampered != md:
        assert G.bare_nominal_offsets(tampered, "15,740", "9,733")


G_SURFACES = (
    ROOT / "data" / "grid" / "g" / "PANEL.md",
    ROOT / "data" / "grid" / "g" / "ICB_DYADIC_REPLICATION.md",
    ROOT / "data" / "handoffs" / "G_to_B_2026-09-03_panel_built.md",
)


@pytest.mark.skipif(not PANEL.exists(), reason="panel not built in this tree")
def test_A5_5_no_G_authored_surface_quotes_the_nominal_alone():
    """A5.5 extended to every surface Session G writes about this panel, not just the report. Joe's
    instruction was that the effective number be impossible to omit; a handoff that quotes 15,740
    bare omits it just as effectively as a report would."""
    s = json.loads(PANEL.read_text())
    nominal = f"{G.nom(s['size']['cells']):,}"
    eff = f"{s['size']['cells']['n_eff_two_way']:,.0f}"
    offenders = {}
    for p in G_SURFACES:
        if not p.exists():
            continue
        bare = G.bare_nominal_offsets(p.read_text(), nominal, eff)
        if bare:
            offenders[p.name] = bare
    assert not offenders, (f"these G-authored surfaces quote the nominal count {nominal} with no "
                           f"effective figure ({eff}) within 300 characters: {offenders}")
