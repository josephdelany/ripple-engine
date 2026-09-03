"""
tests/test_grid_price_walk.py -- GRID_STUDY_REGISTRATION.md Part III + Amendment 1.

Every test name carries the clause it covers. The leakage tests are the ones that matter: on a grid, the
whole design rests on an analog's own outcome having closed before the read that uses it, and on the inner
CV folds lying strictly before the outer read.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from engine.grid import price_walk as PW      # noqa: E402

PUBLISHED = PW.OUT_DIR / "summary.json"
published_only = pytest.mark.skipif(not PUBLISHED.exists(), reason="grid price summary not yet computed")


# ---------------------------------------------------------------- Amendment 1: the registered constants

def test_A1_the_block_set_is_the_four_that_have_fields_and_carries_thirteen_of_them():
    assert tuple(PW.BLOCKS) == ("physical", "market", "macro", "geopolitical")
    fields = [f for b in PW.BLOCKS.values() for f in b]
    assert len(fields) == 13 and len(set(fields)) == 13
    assert "actors" not in PW.BLOCKS and "dyads" not in PW.BLOCKS, \
        "Amendment 1 removed the two blocks that have no fields on a grid"


def test_A1_the_registered_candidate_set_is_the_simplex_grid_times_the_tau_grid():
    w = PW.simplex_grid()
    assert len(w) == 35, "four blocks in steps of 0.25"
    assert all(abs(v.sum() - 1.0) < 1e-9 for v in w)
    assert len(PW.CANDIDATES) == 35 * len(PW.TAU_GRID) == 175
    assert PW.K == 12 and PW.BURN_IN == 60


def test_A1_the_frozen_comparator_is_the_equal_weight_vector_at_tau_one():
    assert PW.FROZEN_W.tolist() == [0.25] * 4 and PW.FROZEN_TAU == 1.0
    assert any(np.allclose(w, PW.FROZEN_W) and t == PW.FROZEN_TAU for w, t in PW.CANDIDATES)


# ---------------------------------------------------------------- the filtration: the load-bearing tests

def test_A1_an_analog_is_eligible_only_once_its_own_outcome_has_closed():
    """u + h trading days <= t. A read may never use an analog whose window is still open at t."""
    gi = np.array([0, 10, 20, 30, 40])
    m = PW.eligible_mask(5, gi, h=20)
    assert not m[0].any() and not m[1].any()          # nothing has closed this early
    assert m[2].tolist() == [True, False, False, False, False]     # only u=0 closed by t=20
    assert m[3].tolist() == [True, True, False, False, False]
    assert not m[np.arange(5), np.arange(5)].any(), "a read is never its own analog"


def test_A1_eligibility_is_strictly_tighter_for_a_longer_horizon():
    gi = np.arange(0, 200, 10)
    n5 = PW.eligible_mask(len(gi), gi, 5).sum()
    n60 = PW.eligible_mask(len(gi), gi, 60).sum()
    assert n60 < n5, "a 60-day outcome closes later, so fewer analogs are eligible"


def test_A1_the_forecast_never_reads_a_return_that_had_not_closed():
    """The probe that would catch a real leak: poison every return whose window is still open at t and the
    scores must not move. If they move, the forecast was reading the future."""
    rng = np.random.default_rng(0)
    T = 120
    gi = np.arange(T) * 21
    R = rng.normal(0, 0.1, (T, 1, 1))
    D = {b: np.abs(rng.normal(size=(T, T))) for b in PW.BLOCK_NAMES}
    for b in D:
        D[b] = (D[b] + D[b].T) / 2
        np.fill_diagonal(D[b], 0.0)
    dist = PW.combined(D, np.array([0.25] * 4))
    elig = PW.eligible_mask(T, gi, 20)
    base, _ = PW.crps_grid(dist, R, elig, 0, 0)
    Rp = R.copy()
    for t in range(T):
        open_at_t = ~elig[t].copy()
        open_at_t[t] = False              # t's OWN outcome is the thing being scored, not an analog
        Rp_t = Rp.copy()
        Rp_t[open_at_t, 0, 0] = 99.0                  # poison only what is not closed by t
        got, _ = PW.crps_grid(dist, Rp_t, elig, 0, 0)
        if np.isfinite(base[t]):
            assert got[t] == pytest.approx(base[t]), f"read at {t} moved when open windows were poisoned"


def test_A1_nested_cv_selects_only_from_reads_whose_outcome_closed_by_the_outer_read():
    """Poison every candidate's score at reads that have NOT closed by t; the selection must not move."""
    rng = np.random.default_rng(1)
    C, T, A, H = 8, 200, 1, 1
    gi = np.arange(T) * 21
    cc = rng.normal(1.0, 0.2, (C, T, A, H))
    cands = [(np.array([0.25] * 4), 1.0)] * C
    chosen, n_inner = PW.nested_cv(cc, gi, cands)
    poisoned = cc.copy()
    maxh = max(PW.HORIZONS)
    for t in range(T):
        not_closed = (gi + maxh) > gi[t]
        p = cc.copy()
        p[:, not_closed] = -1e6                       # a score that would dominate any selection
        ch, _ = PW.nested_cv(p, gi, cands)
        assert ch[t] == chosen[t], f"selection at {t} moved when unclosed reads were poisoned"
    assert (chosen >= 0).sum() > 0, "the probe would be vacuous if nothing was ever fitted"


def test_A1_standardisation_uses_only_dates_strictly_before_the_read():
    """Both endpoints share t's stats, and those stats come from S[:t] only -- so appending future rows
    must not change any distance already computed."""
    rng = np.random.default_rng(2)
    S = rng.normal(size=(80, 13))
    fields = [f for b in PW.BLOCKS.values() for f in b]
    D1 = PW.block_distances(S, fields)
    S2 = np.vstack([S, rng.normal(size=(20, 13)) * 50 + 100])      # a wild future
    D2 = PW.block_distances(S2, fields)
    for b in PW.BLOCK_NAMES:
        a, c = D1[b][:80, :80], D2[b][:80, :80]
        m = np.isfinite(a) & np.isfinite(c)
        assert np.allclose(a[m], c[m]), f"block {b} distances moved when future rows were appended"


def test_A1_a_block_with_no_commonly_known_field_is_dropped_and_its_weight_redistributed():
    D = {b: np.array([[0.0, 1.0], [1.0, 0.0]]) for b in PW.BLOCK_NAMES}
    D["macro"] = np.array([[np.nan, np.nan], [np.nan, np.nan]])
    out = PW.combined(D, np.array([0.25] * 4))
    assert out[0, 1] == pytest.approx(1.0), "the three defined blocks must renormalise to 1, not to 0.75"
    allnan = {b: np.full((2, 2), np.nan) for b in PW.BLOCK_NAMES}
    assert np.isnan(PW.combined(allnan, np.array([0.25] * 4))[0, 1])


# ---------------------------------------------------------------- the published run

@published_only
def test_III_the_published_run_labels_its_unit_and_does_not_re_judge_the_event_study():
    s = json.loads(PUBLISHED.read_text())
    assert s["unit"] == "date"
    assert "not the event-triggered estimand" in s["estimand"].lower() or \
           "NOT the event-triggered" in s["estimand"]
    assert str(PW.OUT_DIR).endswith("data/grid/price")


@published_only
def test_III_3_2_every_pooled_horizon_number_carries_the_H_eff_disclosure():
    s = json.loads(PUBLISHED.read_text())
    d = s["pooling_disclosure"]
    assert d["H_eff"] == pytest.approx(1.547, abs=0.01)
    assert d["H_eff_random_walk_benchmark"] == pytest.approx(1.550, abs=0.01)
    assert d["n_eff_joint"] < s["panel"]["n_scored_cells"], "n_eff is never the nominal cell count"


@published_only
def test_III_3_4_the_comparison_that_is_the_point_is_published_whichever_way_it_came_out():
    s = json.loads(PUBLISHED.read_text())
    c = s["the_comparison"]
    assert c["ref"] == "frozen"
    assert c["skill"] is not None and c["dm_p"] is not None
    assert s["training"]["fitted_parameters"] == 5
    assert s["training"]["available_inner_effective"] >= s["training"]["required_effective_units"]


@published_only
def test_III_3_7_3_the_weight_trajectory_is_published():
    traj = json.loads((PW.OUT_DIR / "training.json").read_text())
    assert len(traj) > 100
    fitted = [t for t in traj if t["w"]]
    assert fitted, "no read carried a fit"
    assert all(abs(sum(t["w"]) - 1.0) < 1e-9 for t in fitted)
    s = json.loads(PUBLISHED.read_text())
    assert s["training"]["distinct_selections"] >= 1
    assert 0.0 < s["training"]["modal_share"] <= 1.0
