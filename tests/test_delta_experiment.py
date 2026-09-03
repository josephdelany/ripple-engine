"""
tests/test_delta_experiment.py -- WALK_FORWARD_PROTOCOL.md Amendment L.

Every test name carries the amendment clause it covers. The tests that touch the sealed run read
data/walk_forward/*.jsonl and never write.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from engine import delta_experiment as DX      # noqa: E402
from engine import scoring as SC               # noqa: E402

WF = ROOT / "data" / "walk_forward"
SEALED = (WF / "reads.jsonl").exists() and (WF / "scores.jsonl").exists()
sealed_only = pytest.mark.skipif(not SEALED, reason="sealed run not in the tree")


# ---------------------------------------------------------------- L.1 the target

def test_L1_feasible_set_is_exactly_the_reachable_changes():
    assert DX.feasible(0) == [0, 1, 2, 3]
    assert DX.feasible(1) == [-1, 0, 1, 2]
    assert DX.feasible(3) == [-3, -2, -1, 0]
    for lm in range(4):
        assert len(DX.feasible(lm)) == 4
        assert all(0 <= d + lm <= 3 for d in DX.feasible(lm))


def test_L1_delta_of_every_level_pair_is_in_the_registered_support():
    for lm in range(4):
        for lv in range(4):
            assert str(lv - lm) in DX.DELTAS


# ---------------------------------------------------------------- L.2 the forecast, clipping, the identity

def test_L2_clip_moves_infeasible_mass_to_the_nearest_feasible_change():
    assert DX.clip(-3, 0) == 0 and DX.clip(3, 0) == 3        # L- = 0: nothing can fall
    assert DX.clip(2, 3) == 0 and DX.clip(-3, 3) == -3       # L- = 3: nothing can rise
    d = DX.dist([-3, -2, 0, 3], lm=0)
    assert d["0"] == pytest.approx(0.75) and d["3"] == pytest.approx(0.25)
    assert sum(d.values()) == pytest.approx(1.0)


def test_L2_delta_brier_equals_implied_level_brier_for_every_clipped_forecast():
    """The identity L.2 registers so it can never be presented later as a finding."""
    rng = np.random.default_rng(0)
    for _ in range(200):
        lm = int(rng.integers(0, 4)); lv = int(rng.integers(0, 4))
        atoms = [int(x) for x in rng.integers(-3, 4, size=int(rng.integers(1, 13)))]
        d = DX.dist(atoms, lm=lm)
        DX.assert_delta_level_identity(d, lm, str(lv - lm), str(lv))     # raises if broken


def test_L2_a_deliberately_unclipped_forecast_breaks_the_identity():
    """The identity assertion is load-bearing: it must fail when infeasible mass is left in place."""
    bad = {d: 0.0 for d in DX.DELTAS}
    bad["3"] = 0.5; bad["0"] = 0.5                # L- = 2: +3 is infeasible (implied level 5)
    with pytest.raises(AssertionError):
        DX.assert_delta_level_identity(bad, 2, "0", "2")


@sealed_only
def test_L2_every_analog_L_minus_predates_the_read_it_is_used_in():
    """The filtration claim of L.2: an analog's L- comes from that analog's OWN sealed read, whose
    pre-window [d-90, d-1] closes strictly before the analog's date, which is strictly before as_of."""
    built = DX.build()
    reads = {r["event_id"]: r for r in DX._rows("reads.jsonl", built["run_id"])}
    checked = 0
    for row in built["rows"]:
        for it in reads[row["event_id"]]["items"][:DX.ANALOG_ITEMS]:
            for aid in (it.get("G_ids") or []):
                ar = reads[aid]
                p = ar["baselines"]["persistence"]
                assert ar["date"] < row["as_of"], f"{aid} not before {row['event_id']}"
                assert p["window_pre"][1] < row["as_of"]
                checked += 1
    assert checked > 1000, f"only {checked} analog slots checked"


# ---------------------------------------------------------------- L.3 the baselines

def test_L3_no_change_is_amendment_B2_smoothing_expressed_in_this_estimand():
    for lm in range(4):
        d = DX.no_change(lm)
        assert sum(d.values()) == pytest.approx(1.0)
        assert d["0"] == pytest.approx(0.9)
        assert all(float(d[k]) == 0.0 for k in DX.DELTAS if int(k) not in DX.feasible(lm))
    assert DX.no_change(1)["-1"] == pytest.approx(0.05) and DX.no_change(1)["1"] == pytest.approx(0.05)
    assert DX.no_change(0)["1"] == pytest.approx(0.10)      # boundary: one neighbour takes the whole 0.1
    assert DX.no_change(3)["-1"] == pytest.approx(0.10)


def test_L3_no_change_scores_exactly_what_G_persistence_scores_in_level_space():
    """no-change IS G-persistence in this estimand -- the whole basis of the comparison."""
    for lm in range(4):
        for lv in range(4):
            lvl = {l: 0.0 for l in SC.LEVELS}
            nb = [x for x in (lm - 1, lm + 1) if 0 <= x <= 3]
            lvl[str(lm)] = 0.9
            for x in nb:
                lvl[str(x)] += 0.1 / len(nb)
            assert DX.brier(DX.no_change(lm), str(lv - lm)) == pytest.approx(SC.brier(lvl, str(lv)))


# ---------------------------------------------------------------- L.4 the combinations

def test_L4_C1_is_the_fixed_registered_half_and_pools_are_proper_distributions():
    a, b = DX.no_change(1), DX.dist([-1, 0, 0, 2], lm=1)
    p = DX.pool(a, b, DX.LAMBDA_DEFAULT)
    assert DX.LAMBDA_DEFAULT == 0.5
    assert sum(p.values()) == pytest.approx(1.0)
    assert all(v >= 0 for v in p.values())
    assert p["0"] == pytest.approx(0.5 * a["0"] + 0.5 * b["0"])


def test_L4_lambda_grid_and_min_n_are_the_registered_ones():
    assert list(DX.LAMBDA_GRID) == [round(0.1 * i, 1) for i in range(11)]
    assert DX.LAMBDA_MIN_N == 40


def _synthetic_rows(n=60, seed=3):
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n):
        lm = int(rng.integers(0, 4))
        lv = int(rng.integers(0, 4))
        atoms = [int(x) for x in rng.integers(-2, 3, size=6)]
        rows.append({"event_id": f"e{i:03d}", "date": f"2000-{1 + i // 28:02d}-{1 + i % 28:02d}",
                     "as_of": f"2000-{1 + i // 28:02d}-{1 + i % 28:02d}",
                     "l_minus": lm, "level": lv, "delta": str(lv - lm), "covering_pre": 2,
                     "g_closed_on": f"2000-{1 + (i + 3) // 28:02d}-{1 + (i + 3) % 28:02d}",
                     "atoms_analogue": atoms, "weights_analogue": [1 / 6] * 6,
                     "d": {"no_change": DX.no_change(lm), "analogue": DX.dist(atoms, lm=lm),
                           "climatology": DX.dist(atoms, lm=lm), "frozen": DX.dist(atoms, lm=lm),
                           "random_analogs": [DX.dist(atoms, lm=lm)]}})
    return rows


def test_L4_C2_lambda_never_uses_a_read_whose_window_had_not_closed():
    """Leakage, two directions. (a) With nothing closed, lambda must sit at the registered 0.5 forever.
    (b) Tampering with the target of reads that close only AFTER every as_of must leave the whole
    trajectory bit-identical -- an unclosed outcome may not reach the fit."""
    import copy
    rows = _synthetic_rows(n=120, seed=11)
    a = DX.combinations(copy.deepcopy(rows))["lambda_trajectory"]

    nothing_closed = copy.deepcopy(rows)
    for r in nothing_closed:
        r["g_closed_on"] = "2099-01-01"
    b = DX.combinations(nothing_closed)["lambda_trajectory"]
    assert all(x == DX.LAMBDA_DEFAULT for x in b), "with nothing closed, lambda must stay at the registered 0.5"

    tampered = copy.deepcopy(rows)
    touched = 0
    for r in tampered:
        if r["g_closed_on"] > max(q["as_of"] for q in rows):     # closes after every read in the walk
            r["level"] = (r["level"] + 2) % 4
            r["delta"] = str(r["level"] - r["l_minus"])
            touched += 1
    assert touched > 0, "no read closes after the walk; the leakage probe would be vacuous"
    assert DX.combinations(tampered)["lambda_trajectory"] == a


def test_L4_C2_lambda_moves_when_a_closed_read_changes_and_ties_go_to_the_larger_lambda():
    import copy
    rows = _synthetic_rows(n=120, seed=11)
    base = DX.combinations(copy.deepcopy(rows))
    assert base["lambda_n_fitted"] > 0, "no read had >= 40 closed predecessors; the fit never engaged"
    shifted = copy.deepcopy(rows)
    for r in shifted:                              # make no-change perfect everywhere: lambda must go to 1.0
        r["level"] = r["l_minus"]; r["delta"] = "0"
    assert DX.combinations(shifted)["lambda_terminal"] == 1.0


def test_L4_C3_hedge_uses_the_registered_eta_and_scale():
    import walk as W
    rows = _synthetic_rows(n=80, seed=5)
    out = DX.combinations(rows)
    w = out["hedge_w_nochange_trajectory"]
    assert w[0] == pytest.approx(0.5)              # nothing closed yet -> uniform
    assert all(0.0 <= x <= 1.0 for x in w)
    assert W.REGISTERED["eta"] == 0.25 and W.REGISTERED["g_scale"] == 2.0


# ---------------------------------------------------------------- L.6 inference

def test_L6_label_permutation_targets_stay_feasible():
    """(i) permutes the realized LEVEL, not the change, so every permuted target is reachable from the
    read's own L-. Nothing may fall outside the feasible set."""
    rows = _synthetic_rows(n=40, seed=7)
    cl = DX.clusters_of([r["date"] for r in rows], 35)
    rng = np.random.default_rng(0)
    for _ in range(50):
        seq = [i for k in rng.permutation(len(cl)) for i in cl[k]]
        for i, j in enumerate(seq):
            d = rows[j]["level"] - rows[i]["l_minus"]
            assert d in DX.feasible(rows[i]["l_minus"])


def test_L6_forecast_permutation_reclips_to_the_receiving_read():
    rows = _synthetic_rows(n=40, seed=9)
    for i, r in enumerate(rows):
        j = (i + 7) % len(rows)
        d = DX.dist(rows[j]["atoms_analogue"], rows[j]["weights_analogue"], lm=r["l_minus"])
        assert sum(d.values()) == pytest.approx(1.0)
        assert all(float(d[k]) == 0.0 for k in DX.DELTAS if int(k) not in DX.feasible(r["l_minus"]))


def test_L6_clusters_follow_the_registered_35_day_rule():
    dates = ["2000-01-01", "2000-01-10", "2000-03-01", "2000-03-02", "2000-09-09"]
    assert DX.clusters_of(dates, 35) == [[0, 1], [2, 3], [4]]


# ---------------------------------------------------------------- L.7 the verdict

def _b(skill, dm_p, lo, hi):
    return {"skill": skill, "dm_p": dm_p, "ci95": [lo, hi]}


def test_L7_all_four_registered_verdicts_are_reachable_by_the_rule_as_written():
    win = _b(0.10, 0.01, 0.02, 0.18)
    lose = _b(-0.30, 0.001, -0.55, -0.05)
    flat = _b(0.01, 0.60, -0.09, 0.11)
    assert DX.verdict(win, flat, 0.01, 0.01, 0.4)[0] == "INCREMENTAL"
    assert DX.verdict(flat, win, 0.30, 0.30, 0.3)[0] == "INCREMENTAL-UNDER-FITTED-WEIGHT"
    assert DX.verdict(lose, flat, 0.90, 0.90, 1.0)[0] == "DEGRADES"
    assert DX.verdict(flat, flat, 0.90, 0.90, 0.5)[0] == "NO ADDITION"


def test_L7_a_losing_equal_pool_with_a_weight_that_stays_off_persistence_is_NO_ADDITION_not_DEGRADES():
    """L.8.2: a fixed 50/50 pool losing is not evidence that analogy degrades."""
    lose = _b(-0.30, 0.001, -0.55, -0.05)
    label, why = DX.verdict(lose, _b(0.00, 0.80, -0.10, 0.10), 0.9, 0.9, 0.6)
    assert label == "NO ADDITION"
    assert "REGISTERED EQUAL WEIGHT" in why


def test_L7_INCREMENTAL_requires_every_registered_condition():
    win = _b(0.10, 0.01, 0.02, 0.18)
    flat = _b(0.01, 0.60, -0.09, 0.11)
    assert DX.verdict(win, flat, 0.20, 0.01, 0.5)[0] != "INCREMENTAL"      # SPA fails
    assert DX.verdict(win, flat, 0.01, 0.20, 0.5)[0] != "INCREMENTAL"      # permutation fails
    assert DX.verdict(_b(0.10, 0.30, -0.02, 0.20), flat, 0.01, 0.01, 0.5)[0] != "INCREMENTAL"   # DM fails


# ---------------------------------------------------------------- the published object

@sealed_only
def test_L9_published_json_matches_the_module_on_the_headline_numbers():
    if not DX.OUT.exists():
        pytest.skip("delta_experiment.json not yet computed")
    out = json.loads(DX.OUT.read_text())
    assert out["registered"] is True and out["amendment"].startswith("WALK_FORWARD_PROTOCOL.md Amendment L")
    assert out["verdict"]["label"] in ("INCREMENTAL", "INCREMENTAL-UNDER-FITTED-WEIGHT",
                                       "NO ADDITION", "DEGRADES")
    assert out["n_retained"] >= 30
    assert out["scores"]["no_change"]["brier_fair"] == out["scores"]["no_change"]["brier"]
    for f in ("C1_fixed_0.5", "C2_walkforward_lambda", "C3_hedge"):
        assert out["scores"][f]["brier_fair"] is None, "a pool with a non-atomic component has no Ferro form"


# ---------------------------------------------------------------- M: pooling or similarity? (diagnostic)

def test_M2_the_three_pools_share_the_registered_lambda_and_differ_only_in_the_second_component():
    """M.2: if the weight differed between the pools it could explain any gap between them, and the
    control would answer nothing."""
    rows = _synthetic_rows(n=60, seed=13)
    DX.combinations(rows)                       # the pools live on the rows the combinations build
    out = DX.diagnostic_pools(rows, DX.score_rows(rows), 1.5, 0, 200)
    assert out["lambda"] == DX.LAMBDA_DEFAULT == 0.5
    r = rows[0]
    for second in ("analogue", "climatology"):
        p = DX.pool(r["d"]["no_change"], r["d"][second], DX.LAMBDA_DEFAULT)
        assert p["0"] == pytest.approx(0.5 * r["d"]["no_change"]["0"] + 0.5 * r["d"][second]["0"])
    assert set(out["means"]) == {"C1_analogue", "C0r_random_analogs", "C0_climatology", "no_change"}


def test_M2_the_control_is_labelled_post_hoc_and_gates_nothing():
    """Registered post hoc and said so: the standing of Amendment K, never dressed up as foresight."""
    rows = _synthetic_rows(n=60, seed=17)
    DX.combinations(rows)
    out = DX.diagnostic_pools(rows, DX.score_rows(rows), 1.5, 0, 200)
    assert out["registered_post_hoc"] is True
    assert out["gates"].startswith("nothing")


@sealed_only
def test_M4_published_control_does_not_move_the_L7_verdict():
    if not DX.OUT.exists():
        pytest.skip("delta_experiment.json not yet computed")
    o = json.loads(DX.OUT.read_text())
    assert o["diagnostic_pools"]["registered_post_hoc"] is True
    assert o["verdict"]["label"] == "NO ADDITION", "L.7's verdict is decided by L's registered conditions alone"
