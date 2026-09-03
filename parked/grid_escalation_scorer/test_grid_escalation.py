"""
tests/test_grid_escalation.py -- GRID_STUDY_REGISTRATION.md Part IV.

Every test name carries the clause it covers. The panel is session G's, so these run on a synthetic panel
that obeys G's declared schema; the two that need the real file skip until it lands (§4.0's gate).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from engine.grid import escalation_walk as EW      # noqa: E402

panel_only = pytest.mark.skipif(EW.panel_path() is None, reason="G's PANEL not in the tree yet (§4.0 gate)")


def synth(n_dates=120, n_dyads=12, zero_share=0.9, seed=0, running_at_t=0, span_end="2014-09-30"):
    """A panel obeying G's A3.5 schema. `running_at_t` injects VR-3 violations."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2000-01-31", periods=n_dates, freq="ME")
    dates = dates[dates <= pd.Timestamp(span_end)]
    rows = []
    for d in dates:
        for j in range(n_dyads):
            z = rng.random() < zero_share
            lpre = int(rng.integers(0, 4))
            lvl = lpre if z else int(np.clip(lpre + rng.choice([-2, -1, 1, 2]), 0, 3))
            rows.append({"date": d, "dyad": f"{j}-{j+100}", "L": lvl, "Lpre": lpre, "dIES": lvl - lpre,
                         "evidence_class": rng.choice(EW.EVIDENCE_ORDER[:4], p=[0.5, 0.2, 0.15, 0.15]),
                         "vr3": True,
                         "admit_record_end": d - pd.Timedelta(days=int(rng.integers(30, 900)))})
    df = pd.DataFrame(rows)
    for i in range(running_at_t):
        df.loc[i, "admit_record_end"] = df.loc[i, "date"] + pd.Timedelta(days=10)   # still running at t
    return df


# ---------------------------------------------------------------- §4.1 the three limits

def test_4_1_all_three_limits_are_carried_in_the_same_object_as_every_number():
    L = EW.LIMITS
    assert L["span_ends"] == "2014-09-30"
    assert L["ceiling"] == "SUGGESTIVE"
    assert L["panel_type"] == "recurrence"
    for k in ("span_rule", "ceiling_rule", "panel_type_rule"):
        assert len(L[k]) > 40, f"{k} must state the reason, not just the label"
    assert "never make a read VALIDATED" in L["ceiling_rule"]
    assert "NEVER onset" in L["panel_type_rule"] or "never onset" in L["panel_type_rule"].lower()


def test_4_1_2_the_ceiling_is_a_priori_and_n_cannot_move_it():
    """The sharpest fact about a study whose whole purpose was more n."""
    assert "n does not touch this" in EW.LIMITS["ceiling_rule"]


def test_4_1_the_limits_travel_with_the_computed_summary(tmp_path):
    df = synth()
    p = tmp_path / "PANEL.csv"
    df.to_csv(p, index=False)
    out = EW.compute(p)
    assert out["limits"] == EW.LIMITS
    assert out["unit"] == "dyad-date"
    assert out["reads_walk_forward"] is False


# ---------------------------------------------------------------- §4.0 the panel contract

def test_4_0_B_builds_no_panel_and_fails_loudly_when_G_s_file_is_absent():
    with pytest.raises(FileNotFoundError) as e:
        EW.load_panel(None) if EW.panel_path() is None else (_ for _ in ()).throw(FileNotFoundError("skip"))
    assert "B does not build a panel" in str(e.value) or "skip" in str(e.value)


def test_4_0_a_panel_missing_a_contract_column_names_exactly_what_is_missing(tmp_path):
    df = synth().drop(columns=["evidence_class"])
    p = tmp_path / "PANEL.csv"
    df.to_csv(p, index=False)
    with pytest.raises(KeyError) as e:
        EW.load_panel(p)
    assert "evidence_class" in str(e.value)
    assert "do not rename G's file" in str(e.value)


def test_4_1_1_the_span_is_truncated_at_2014_09_30_on_load(tmp_path):
    df = synth(n_dates=400, span_end="2020-12-31")
    p = tmp_path / "PANEL.csv"
    df.to_csv(p, index=False)
    got, _ = EW.load_panel(p)
    assert got["date"].max() <= pd.Timestamp("2014-09-30")
    assert len(got) < len(df), "rows past the span must be dropped, not carried"


# ---------------------------------------------------------------- §4.8 the VR-3 assertion

def test_4_8_a_cell_admitted_on_a_record_still_running_at_t_voids_the_run(tmp_path):
    """G's probe caught 39 of 335 such cells in 2018. B inherits the fix and asserts it."""
    df = synth(running_at_t=3)
    p = tmp_path / "PANEL.csv"
    df.to_csv(p, index=False)
    out = EW.compute(p)
    assert out["vr3_assertion"]["asserted"] is False
    assert out["vr3_assertion"]["n_admitting_record_not_closed_before_t"] == 3
    assert out["status"].startswith("VOID")
    assert "n_eff_full" not in out, "no score may be computed on a run the assertion voided"


def test_4_8_a_clean_panel_passes_the_assertion(tmp_path):
    df = synth(running_at_t=0)
    p = tmp_path / "PANEL.csv"
    df.to_csv(p, index=False)
    out = EW.compute(p)
    assert out["vr3_assertion"]["asserted"] is True
    assert out["vr3_assertion"]["n_admitting_record_not_closed_before_t"] == 0


# ---------------------------------------------------------------- §4.7 the tripwire

def test_4_7_the_bar_is_the_registered_0_95_and_a_breach_is_flagged_not_dropped(tmp_path):
    df = synth(zero_share=0.99, seed=5)
    p = tmp_path / "PANEL.csv"
    df.to_csv(p, index=False)
    out = EW.compute(p)
    t = out["tripwire"]
    assert t["bar"] == 0.95
    assert t["breached"] is True and t["breaches"], "a 99 % zero panel must trip the wire"
    assert out["status"].startswith("TRIPWIRE")
    assert "not dropped" in t["rule"] and "not moved" in t["rule"]
    # the breaching slice is still counted, never removed
    yrs = out["tripwire"]["full|delta|by_year"]
    assert all(v is None or 0.0 <= v <= 1.0 for v in yrs.values())


def test_4_7_a_healthy_panel_does_not_trip_the_wire(tmp_path):
    df = synth(zero_share=0.60, seed=6)
    p = tmp_path / "PANEL.csv"
    df.to_csv(p, index=False)
    out = EW.compute(p)
    assert out["tripwire"]["breached"] is False
    assert out["status"].startswith("READY")


def test_4_7_share_zero_is_reported_per_year_and_for_both_subsets(tmp_path):
    df = synth()
    p = tmp_path / "PANEL.csv"
    df.to_csv(p, index=False)
    t = EW.compute(p)["tripwire"]
    for key in ("full|delta|window", "full|level|window", "strict|delta|window", "strict|delta|by_year"):
        assert key in t, key


# ---------------------------------------------------------------- §4.5 / §4.6

def test_4_5_evidence_class_is_a_field_and_every_number_is_computed_on_both_subsets(tmp_path):
    df = synth()
    p = tmp_path / "PANEL.csv"
    df.to_csv(p, index=False)
    out = EW.compute(p)
    assert set(out["evidence_mix"]) <= set(EW.EVIDENCE_ORDER)
    assert "n_eff_full" in out and "n_eff_strict" in out, "a number without its pair is a misquotation"
    assert EW.STRICT == "opposed_side"
    assert EW.EVIDENCE_ORDER[0] == "opposed_side" and EW.EVIDENCE_ORDER[-1] == "undefined"


def test_4_6_effective_n_never_exceeds_nominal_and_carries_its_ceiling_warning(tmp_path):
    df = synth()
    p = tmp_path / "PANEL.csv"
    df.to_csv(p, index=False)
    b = EW.compute(p)["n_eff_full"]["delta"]
    assert b["n_eff"] <= b["n_nominal_cells"] + 1e-6, "n_eff may never exceed n_nominal"
    assert b["deff_used"] >= 1.0 - 1e-9, "a design effect below 1 is a finite-sample artefact, floored at 1"
    assert b["informative_cells"] < b["n_nominal_cells"]
    assert "ceiling, not an estimate" in b["ceiling_warning"]


def test_4_6_a_design_effect_below_one_is_floored_and_the_floor_is_recorded(tmp_path):
    """Independent synthetic cells measure DEFF at or below 1; the floor must fire and be visible."""
    df = synth(seed=11)
    p = tmp_path / "PANEL.csv"
    df.to_csv(p, index=False)
    b = EW.compute(p)["n_eff_full"]["delta"]
    # the value the floor is applied to: the tie-break's winner if it fired, else the separable form
    pre = max(b["deff_separable"], b["deff_two_way"]) if b["tiebreak_fired"] else b["deff_separable"]
    assert b["deff_floored_at_1"] is (pre < 1.0), (pre, b["deff_floored_at_1"])
    assert b["deff_used"] == pytest.approx(max(pre, 1.0))
    if b["deff_floored_at_1"]:
        assert b["n_eff"] == pytest.approx(b["n_nominal_cells"])


def test_4_6_a_panel_with_real_dependence_loses_effective_n(tmp_path):
    """The estimator must actually bite: give every dyad the same date-level shock and n_eff must fall
    well below nominal."""
    rng = np.random.default_rng(3)
    dates = pd.date_range("2000-01-31", periods=120, freq="ME")
    common = rng.integers(0, 4, size=len(dates))
    rows = []
    for i, d in enumerate(dates):
        for j in range(12):
            lpre = int(common[i])                       # every dyad moves together, by construction
            lvl = int(np.clip(lpre + (1 if rng.random() < 0.3 else 0), 0, 3))
            rows.append({"date": d, "dyad": f"{j}-{j+100}", "L": lvl, "Lpre": lpre, "dIES": lvl - lpre,
                         "evidence_class": "opposed_side", "vr3": True,
                         "admit_record_end": d - pd.Timedelta(days=100)})
    p = tmp_path / "PANEL.csv"
    pd.DataFrame(rows).to_csv(p, index=False)
    b = EW.compute(p)["n_eff_full"]["delta"]
    assert b["deff_used"] > 2.0, f"perfectly clustered dates must show a large design effect, got {b}"
    assert b["n_eff"] < 0.5 * b["n_nominal_cells"]


# ---------------------------------------------------------------- §4.9 the walk freeze

def test_4_9_this_arm_never_reads_the_frozen_event_target():
    """The names may appear in prose explaining the rule; what must not exist is CODE reaching them. Parse
    the module and inspect identifiers, attributes, imports and the DB path -- never raw text."""
    import ast
    src = (ROOT / "src" / "engine" / "grid" / "escalation_walk.py").read_text()
    tree = ast.parse(src)
    names, attrs, mods = set(), set(), set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            attrs.add(node.attr)
        elif isinstance(node, ast.Import):
            mods.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            mods.add(node.module or "")
    for forbidden in ("event_outcomes", "score_event", "ies90"):
        assert forbidden not in names | attrs, f"{forbidden} is reachable as code from this arm (§4.9)"
    assert "sqlite3" not in mods, "this arm must not open the corpus database at all (§4.9)"
    assert "oil.db" not in "".join(
        n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)
    ), "no path to the corpus DB may appear in this arm"


@panel_only
def test_4_0_the_real_panel_satisfies_the_declared_contract():
    df, path = EW.load_panel()
    assert len(df) > 0 and df["date"].max() <= pd.Timestamp("2014-09-30")
    assert set(df["evidence_class"].dropna().unique()) <= set(EW.EVIDENCE_ORDER)
