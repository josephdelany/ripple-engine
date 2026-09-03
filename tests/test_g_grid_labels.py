"""Tests for src/grid_labels.py (Session G, G-4, the dyad-date probe).

Every test names the clause of data/grid/G4_REGISTRATION.md it covers. Nothing here writes to any
table; the fixtures are dicts built in the test, and the published-run assertions read
data/grid/PROBE.json.
"""
import datetime as dt
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import grid_labels as G  # noqa: E402
import ies90 as I        # noqa: E402

PROBE = ROOT / "data" / "grid" / "PROBE.json"


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
