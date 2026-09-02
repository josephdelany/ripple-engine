"""WALK_FORWARD_PROTOCOL.md Amendment C (M13, Brief B-2): the recalibrator's closed forms by hand; it never sees
an outcome not closed by as_of (nor one looked up after the read was sealed); the leakage test extended to the
recalibration rule; M13 scored, replayed and permuted like any item. DB-free (synthetic corpus, 100 events ~55
days apart so the 40-closed-read threshold is crossed inside the walk)."""
import copy
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, HERE)
import engine.recalibrate as RC
import engine.similarity as S
import walk as W
from test_read import _synthetic
from test_walk import MENU, FAST

M13 = {"id": "M13_recalibrated", "kind": "recalibrated"}
MENU13 = {"items": MENU["items"] + [M13]}


def test_amendment_c_pav_platt_and_identity_by_hand():
    # PAV: y = 1,0,0,1 at x = .1,.2,.3,.4 -> (.1:1) pooled with (.2:0) then (.3:0) -> block mean 1/3 at x .2; (.4:1) stays
    bx, by = RC.pav([.1, .2, .3, .4], [1, 0, 0, 1])
    assert np.allclose(bx, [.2, .4]) and np.allclose(by, [1 / 3, 1.0])
    f = RC.isotonic_map([.1, .2, .3, .4], [1, 0, 0, 1])
    assert abs(float(f(0.2)) - 1 / 3) < 1e-12 and abs(float(f(0.4)) - 1.0) < 1e-12 and abs(float(f(0.3)) - 2 / 3) < 1e-12   # linear between block centres
    assert float(f(0.0)) == float(f(0.2)) and float(f(1.0)) == 1.0                                                      # clamped outside
    # Platt on a calibrated logistic sample recovers a ~ 1, b ~ 0; on forecasts twice too confident it halves them
    rng = np.random.default_rng(0); z = rng.normal(0, 1.5, 4000); p = 1 / (1 + np.exp(-z)); y = rng.random(4000) < p
    a, b, ok = RC.platt_fit(p, y)
    assert ok and abs(a - 1) < 0.08 and abs(b) < 0.08
    p2 = rng.uniform(0.05, 0.95, 4000); y2 = rng.random(4000) < 0.5 * p2
    a2, b2, _ = RC.platt_fit(p2, y2)
    assert abs(float(RC.platt_map(a2, b2)(0.8)) - 0.4) < 0.06
    # the rule: identity below 40 closed reads; renormalized above
    r = RC.Recalibrator().fit([{"0": .5, "1": .1, "2": .2, "3": .2}] * 39, ["0"] * 39)
    assert r.apply({"0": .5, "1": .1, "2": .2, "3": .2}) == {"0": .5, "1": .1, "2": .2, "3": .2} and r.state()["n_fit"] == 39
    probs = [{"0": float(x), "1": 0.0, "2": float(1 - x), "3": 0.0} for x in rng.uniform(0.05, 0.95, 200)]
    labs = ["0" if rng.random() < 0.5 * pr["0"] else "2" for pr in probs]
    r2 = RC.Recalibrator().fit(probs, labs)
    out = r2.apply({"0": .8, "1": 0.0, "2": .2, "3": 0.0})
    assert abs(sum(out.values()) - 1) < 1e-12 and out["0"] < 0.8 and r2.state()["mode"]["0"] in ("isotonic", "platt")
    v = RC.fit_apply_arrays(np.array([[pr[l] for l in RC.LEVELS] for pr in probs]), np.array([RC.LEVELS.index(l) for l in labs]), np.array([.8, 0, .2, 0]))
    assert np.allclose(v, [out[l] for l in RC.LEVELS])                                                                   # the array form is the same rule


def test_amendment_c_recalibrator_sees_only_outcomes_closed_by_as_of(tmp_path):
    c = _synthetic(n=100, seed=3)
    w = W.Walk(c, MENU13, out_dir=tmp_path / "s", params=FAST, quiet=True).run_reads()
    frozen_G = {r["event_id"]: r["frozen"]["G"] for r in w.reads}       # a read with no frozen forecast is nothing to fit on
    active = 0
    for r in w.reads:
        it = r["items"][-1]
        assert it["kind"] == "recalibrated" and it["id"] == "M13_recalibrated" and it["ranked"] == []
        rc = it["recal"]
        # what the recalibrator used: exactly this tier's earlier reads with a label, whose window closed by as_of
        expect = [s_ for s_ in w.scores if s_["tier"] == r["tier"] and s_["date"] < r["date"] and s_["outcome"]["level"]
                  and s_["outcome"]["g_closed_on"] <= r["as_of"] and frozen_G[s_["event_id"]]]
        assert rc["n_closed_used"] == len(expect) == rc["n_fit"]
        if rc["fit_max_closed_on"]:
            assert rc["fit_max_closed_on"] <= r["as_of"]                                # C.2: closed by t
            assert rc["fit_max_looked_up_at"] < r["sealed_at"]                          # looked up before this read was sealed
        if rc["n_fit"] < RC.MIN_N:
            assert all(v == "identity" for v in rc["mode"].values()) and it["G"] == r["frozen"]["G"]
        else:
            active += 1
            assert abs(sum(it["G"].values()) - 1) < 1e-9
        assert it["P"] == (r["frozen"]["P"] or {}).get("values") and it["M"] == r["frozen"]["M"]   # C.3: P and M are the frozen mixture's
    assert active >= 20, active                                                         # the threshold is crossed inside the walk
    assert any(v != "identity" for r in w.reads for v in r["items"][-1]["recal"]["mode"].values())
    # Hedge runs over thirteen items and every weight vector sums to 1
    logs = [json.loads(l) for l in (tmp_path / "s" / "weights.jsonl").read_text().splitlines()]
    assert all(len(lg["G"]["weights"]) == 5 and abs(sum(lg["G"]["weights"]) - 1) < 1e-5 for lg in logs)   # weights logged at 6 decimals
    # C.6: the recalibration rule broken (close dates ignored) changes M13 on some read while the twelve weightings are untouched
    broken = W.Walk(c, MENU13, out_dir=tmp_path / "b", params=FAST, quiet=True, break_filtration=True).run_reads()
    rb = W.Walk(c, MENU13, out_dir=tmp_path / "rb", params=FAST, quiet=True, break_recal=True).run_reads()
    lk = W.leakage_test(w, broken, rb)
    assert lk["asserted"] and lk["recalibration_rule"]["asserted"]
    assert lk["recalibration_rule"]["n_reads_with_different_M13"] > 0 and lk["recalibration_rule"]["base_items_identical"]
    assert lk["recalibration_rule"]["n_broken_reads_that_used_an_unclosed_outcome"] > 0
    # and a sealed run compared with itself does not assert
    again = W.Walk(c, MENU13, out_dir=tmp_path / "s2", params=FAST, quiet=True).run_reads()
    assert W.leakage_test(w, broken, again)["recalibration_rule"]["asserted"] is False


def test_amendment_c_m13_scored_replayed_and_permuted_like_an_item(tmp_path):
    c = _synthetic(n=100, seed=3)
    w = W.Walk(c, MENU13, out_dir=tmp_path, params=FAST, quiet=True).run_reads()
    p = dict(W.REGISTERED) | FAST
    tier = W.summarize_tier(w.reads, w.scores, p, "daily", n_boot=100, n_spa=50)
    g = tier["G"]
    assert g["items_vs_climatology"]["M13_recalibrated"]["n"] >= 20 and g["rps"]["items_vs_climatology"]["M13_recalibrated"]["n"] >= 20
    assert "M13_recalibrated" in g["spa"]["models"] and g["recalibration"]["item"] == "M13_recalibrated" and g["recalibration"]["n_reads_recalibrated"] >= 20
    assert "murphy_M13" in g
    assert tier["M"]["M13_recalibrated"]["n"] > 0
    perm = W.permutation_test(w.reads, w.scores, p, n_perm=30)
    assert perm["n_reads"] >= 20 and 0 < perm["p_value"] <= 1
    p_small = dict(p, spec={"burn_in": [6], "k": [5, 8], "horizon_daily": [20], "cluster_days": [35], "big_move_q": [0.95]})   # a slice of the registered grid, for speed
    sc = W.spec_curve(c, w.reads, w.scores, p_small)
    assert sc["n_specs"] == 4 and all(r["task"] in ("G", "P") for r in sc["rows"])
    # the retrieval never receives M13 as a weighting
    import engine.read as R
    try:
        R.read(c, c.by_id["ev50"], weighting=M13); raise AssertionError("M13 accepted as a weighting")
    except ValueError:
        pass
    assert [it["id"] for it in S.weighting_items(MENU13)] == [it["id"] for it in MENU["items"]]
