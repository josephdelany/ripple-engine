"""PATH Step 8 -- the walk (src/walk.py + src/engine/{scoring,learning,inference}.py). Every test named in
PATH §1 Step 8: sealing (hash precedes outcome lookup; tampering detected); Brier/log/CRPS/pinball closed
forms; Hedge regret <= bound; DM/HLN textbook case; the leakage assertion; placebo ~ 0 on synthetic null
data. Plus: Hedge learns only from outcomes closed by t; the size-corrected (fair) diagnostics reproduce
their closed forms and their derived bias; a positive control for the label permutation. All DB-free
(synthetic corpus). The synthetic corpus is a P-NULL (Brent is a seeded random walk unrelated to any
field) but NOT a G-null: its IES-90 levels follow the actor field by construction, so a G-null is made by
shuffling them (seeded) where a null is needed. G is the IES-90 level (0-3, ordinal) + DEAL flag
(OUTCOME_MAPPING.md Amendment 1); sr_outcome_90 is retired and never appears here."""
import json
import math
import os
import sys

import numpy as np
import pandas as pd
import pytest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, HERE)
import engine.scoring as SC
import engine.learning as LN
import engine.inference as INF
import engine.read as R
import walk as W
from test_read import _synthetic

MENU = {"items": [
    {"id": "M01_uniform_k8", "block_weights": {"situation": 1, "market": 1}, "retrieve_min": 0.40, "k": 8},
    {"id": "M02_situation_only", "block_weights": {"situation": 1, "market": 0}, "retrieve_min": 0.40, "k": 8},
    {"id": "M03_market_only", "block_weights": {"situation": 0, "market": 1}, "retrieve_min": 0.40, "k": 8},
    {"id": "M06_uniform_k5", "block_weights": {"situation": 1, "market": 1}, "retrieve_min": 0.40, "k": 5},
]}
FAST = {"n_boot": 100, "n_spa_boot": 100, "n_perm": 60, "random_draws": 3, "placebo_reps": 2, "burn_in": 6}


def _walk(tmp_path, n=60, seed=3, **kw):
    c = _synthetic(n=n, seed=seed)
    w = W.Walk(c, MENU, out_dir=tmp_path, params=FAST | kw.pop("params", {}), quiet=True, **kw).run_reads()
    return c, w


# ----------------------------------------------------------------------------- sealing

def test_step8_sealing_hash_precedes_outcome_lookup_and_tampering_detected(tmp_path):
    c, w = _walk(tmp_path)
    ok, n, bad = W.verify_file(tmp_path / "reads.jsonl")
    assert ok and n == len(w.reads) and bad is None
    hashes = {r["hash"] for r in w.reads}
    for s in w.scores:
        assert s["read_hash"] in hashes                                     # every score points at a sealed read
        assert s["sealed_at"] < s["outcome"]["looked_up_at"] < s["scored_at"]   # seal, THEN outcome, THEN score
    # tampering: change one forecast value in a copy of the file -> the seal no longer verifies
    lines = (tmp_path / "reads.jsonl").read_text().splitlines()
    rec = json.loads(lines[5])
    rec["engine"]["M"] = "MATERIAL" if rec["engine"]["M"] != "MATERIAL" else "NOT_MATERIAL"
    lines[5] = json.dumps(rec, ensure_ascii=False, default=str)
    (tmp_path / "tampered.jsonl").write_text("\n".join(lines) + "\n")
    ok2, n2, bad2 = W.verify_file(tmp_path / "tampered.jsonl")
    assert ok2 is False and bad2 == 6
    # the file is append-only: a second run appends, never rewrites
    n_before = len(lines)
    W.Walk(c, MENU, out_dir=tmp_path, params=FAST, quiet=True).run_reads()
    assert len((tmp_path / "reads.jsonl").read_text().splitlines()) == 2 * n_before
    assert W.verify_file(tmp_path / "reads.jsonl")[0]


# ----------------------------------------------------------------------------- proper scores

def test_step8_proper_scores_match_closed_forms():
    p = {"0": 0.7, "1": 0.2, "2": 0.1, "3": 0.0}                                # forecast over the IES-90 levels
    assert abs(SC.brier(p, "0") - 0.14) < 1e-12                               # .09 + .04 + .01 + 0
    assert abs(SC.brier(p, "2") - (0.49 + 0.04 + 0.81)) < 1e-12
    fl = SC.floor_probs(p, 0.01)                                              # zero -> 0.01, renormalized
    assert abs(SC.log_score(p, "0") - (-math.log(0.7 / 1.01))) < 1e-12 and abs(sum(fl.values()) - 1) < 1e-12
    # ranked probability score (ordinal): cumulative F = (.7, .9, 1.0); realized 0 -> O = (1,1,1): .09+.01+0 = .10;
    # realized 3 -> O = (0,0,0): .49+.81+1 = 2.30 -- a miss by three levels costs more than Brier's flat 1.34+
    assert abs(SC.rps(p, "0") - 0.10) < 1e-12 and abs(SC.rps(p, "3") - 2.30) < 1e-12
    assert SC.rps({"1": 1.0}, "1") == 0.0 and SC.rps({"0": 1.0}, "3") == 3.0 and SC.rps({"0": 1.0}, "1") == 1.0
    assert SC.brier_binary(0.25, 1) == 0.5625 and SC.brier_binary(0.25, 0) == 0.0625
    assert SC.crps([0.0, 2.0], 1.0) == 0.5                                    # E|X-y| = 1, E|X-X'| = 1
    assert SC.crps([3.0], 1.0) == 2.0                                         # point mass: |y - mu|
    assert abs(SC.crps([0.0, 2.0], 1.0) - SC.crps([0.0, 0.0, 2.0, 2.0], 1.0)) < 1e-12   # duplicated atoms
    assert abs(SC.crps([0.0, 2.0], 1.0) - SC.crps([0.0, 2.0], 1.0, [0.5, 0.5])) < 1e-12  # weights
    rng = np.random.default_rng(0); x = rng.normal(0, 2.0, 40000)
    gauss = 2.0 * (2 / math.sqrt(2 * math.pi) - 1 / math.sqrt(math.pi))        # sigma * (2 phi(0) - 1/sqrt(pi)) at y = mu
    assert abs(SC.crps(x, 0.0) - gauss) / gauss < 0.02
    assert abs(SC.pinball([2.0], 3.0, 0.9) - 0.9) < 1e-12 and abs(SC.pinball([2.0], 1.0, 0.9) - 0.1) < 1e-12
    assert SC.pit([1, 2, 3, 4], 2.5) == 0.5 and SC.pit([1, 2, 3, 4], 2.0) == 0.375 and SC.pit([1, 2], 5) == 1.0
    assert SC.weighted_quantile([1, 2, 3, 4, 5], 0.5) == 3 and SC.weighted_quantile([1, 10], 0.5, [0.9, 0.1]) == 1
    # Murphy: for continuous forecasts binned afterwards the EXACT identity carries the within-bin terms
    # (Stephenson, Coelho & Jolliffe 2008): Brier = rel - res + unc + WBV - WBC; the three-term identity is
    # exact only when every forecast in a bin equals the bin mean (checked with forecasts on the bin means).
    m = SC.murphy(rng.uniform(0, 1, 500), rng.integers(0, 2, 500), bins=5)
    assert abs(m["identity_gap"]) < 1e-9
    assert m["murphy_gap"] != 0 and abs(m["murphy_gap"] - (m["within_bin_variance"] - m["within_bin_covariance"])) < 3e-6
    md = SC.murphy(rng.choice([0.1, 0.3, 0.5, 0.7, 0.9], 500), rng.integers(0, 2, 500), bins=5)
    assert abs(md["murphy_gap"]) < 1e-9 and md["within_bin_variance"] == 0 and abs(md["identity_gap"]) < 1e-9
    assert abs(SC.skill(0.3, 0.4) - 0.25) < 1e-12 and SC.skill(0.4, 0.4) == 0.0
    # size-corrected diagnostics (NOT registered; Ferro 2014), by hand:
    assert SC.crps_fair([0.0, 2.0], 1.0) == 0.0                                # m=2: E|X-y| = 1; sum_{i!=j} w_i w_j |x_i-x_j| / (1 - 1/2) = 2
    assert abs(SC.crps_fair([0.0, 0.0, 2.0, 2.0], 1.0) - 1 / 3) < 1e-12        # m=4: 1 - 0.5 * 1 * 4/3
    assert SC.crps_fair([3.0], 1.0) == 2.0                                     # one atom: nothing to correct
    assert abs(SC.crps_fair([0.0, 2.0], 1.0, [0.5, 0.5]) - SC.crps_fair([0.0, 2.0], 1.0)) < 1e-12
    l0002 = ["0"] * 3 + ["2"]                                                  # p = (.75, 0, .25, 0); c = (1/4)/(3/4) = 1/3; sum p(1-p) = .375
    assert abs(SC.brier_fair(l0002, "0") - (0.125 - 0.125)) < 1e-12
    assert abs(SC.brier_fair(l0002, "2") - (0.5625 + 0.5625 - 0.125)) < 1e-12
    assert SC.brier_fair(["2"], "0") == SC.brier({"2": 1.0}, "0") == 2.0
    # rps_fair on 0,0,0,3 realized 0: F = (.75,.75,.75), RPS = 3 * .0625 = .1875; correction (1/3) * 3 * .1875 = .1875 -> 0
    assert abs(SC.rps({"0": 0.75, "3": 0.25}, "0") - 0.1875) < 1e-12 and abs(SC.rps_fair(["0", "0", "0", "3"], "0")) < 1e-12
    assert SC.rps_fair(["3"], "0") == SC.rps({"3": 1.0}, "0") == 3.0
    # merging duplicate analogs by id leaves the registered CRPS unchanged and changes only the effective sample size
    v, w, ids = SC.mixture_p([[1.0, 2.0], [2.0, 3.0]], [0.5, 0.5], [["a", "b"], ["b", "c"]])
    assert (v, w, ids) == ([1.0, 2.0, 3.0], [0.25, 0.5, 0.25], ["a", "b", "c"])
    v0, w0 = SC.mixture_p([[1.0, 2.0], [2.0, 3.0]], [0.5, 0.5])
    assert abs(SC.crps(v, 1.5, w) - SC.crps(v0, 1.5, w0)) < 1e-12 and SC.crps_fair(v, 1.5, w) != SC.crps_fair(v0, 1.5, w0)


def test_step8_registered_skill_vs_climatology_is_biased_by_sample_size_and_fair_is_not():
    """Executed, not asserted by hand: k iid atoms from the truth vs y from the truth. The registered
    CRPS/Brier of the k-atom distribution exceed the population score by E|X-X'|/(2k) and sum p(1-p)/k;
    the size-corrected scores land on the population value. This is why a null engine (k = 5..12)
    shows negative registered skill against climatology (n ~ 10k): it is not the retrieval, it is k."""
    rng = np.random.default_rng(0); sd, k, n = 2.0, 8, 6000
    std, fair, pop = [], [], []
    for _ in range(n):
        x = rng.normal(0, sd, k); y = rng.normal(0, sd)
        std.append(SC.crps(x, y)); fair.append(SC.crps_fair(x, y))
        z = y / sd                                                              # CRPS of N(0, sd) at y, closed form (Gneiting & Raftery)
        pop.append(sd * (z * (2 * 0.5 * (1 + math.erf(z / math.sqrt(2))) - 1) + 2 * math.exp(-z * z / 2) / math.sqrt(2 * math.pi) - 1 / math.sqrt(math.pi)))
    bias_pred = 2 * sd / math.sqrt(math.pi) / (2 * k)                          # E|X-X'| = 2 sd / sqrt(pi) for a normal
    assert abs((np.mean(std) - np.mean(pop)) - bias_pred) < 0.25 * bias_pred   # the registered bias, as derived
    assert abs(np.mean(fair) - np.mean(pop)) < 0.1 * bias_pred                 # the corrected score is unbiased
    p_true = np.array([0.5, 0.3, 0.2, 0.0]); B = list(SC.LEVELS); sb, fb, pb = [], [], []
    for _ in range(n):
        lab = [B[i] for i in rng.choice(4, k, p=p_true)]; y = B[rng.choice(4, p=p_true)]
        sb.append(SC.brier({b: lab.count(b) / k for b in B}, y)); fb.append(SC.brier_fair(lab, y)); pb.append(SC.brier(dict(zip(B, p_true)), y))
    bias_b = float(np.sum(p_true * (1 - p_true)) / k)
    assert abs((np.mean(sb) - np.mean(pb)) - bias_b) < 0.25 * bias_b and abs(np.mean(fb) - np.mean(pb)) < 0.1 * bias_b


# ----------------------------------------------------------------------------- Hedge

def test_step8_hedge_regret_within_bound():
    rng = np.random.default_rng(1)
    L = rng.uniform(0, 1, (300, 6))
    hl, Wt, regret, bound = LN.run_hedge(L, eta=0.25)
    assert regret <= bound
    assert np.allclose(Wt.sum(axis=1), 1.0) and np.all(Wt[0] == 1 / 6)        # starts uniform
    # one expert always best -> Hedge concentrates on it and its regret is far below the bound
    L2 = rng.uniform(0.5, 1, (300, 6)); L2[:, 2] = rng.uniform(0, 0.2, 300)
    hl2, W2, reg2, b2 = LN.run_hedge(L2, eta=0.25)
    assert W2[-1].argmax() == 2 and W2[-1][2] > 0.99 and reg2 <= b2
    with pytest.raises(ValueError):
        LN.Hedge(3).update([0.5, 1.5, 0.2])                                  # losses must be scaled to [0,1]


def test_step8_hedge_updates_only_from_outcomes_closed_by_t(tmp_path):
    c, w = _walk(tmp_path, n=100)                       # ~55 days apart: the +90d branch window is still open at the next read
    logs = [json.loads(l) for l in (tmp_path / "weights.jsonl").read_text().splitlines()]
    by_id = {s["event_id"]: s for s in w.scores}
    for lg in logs:
        t = lg["date"]
        prior = [s for s in w.scores if s["tier"] == lg["tier"] and s["date"] < t]
        n_g = sum(1 for s in prior if s["items_loss"]["G"] is not None and s["outcome"]["g_closed_on"] <= t)
        n_p = sum(1 for s in prior if s["items_loss"]["P"] is not None and s["outcome"]["closed_on"] <= t)
        assert lg["G"]["n_updates"] == n_g and lg["P"]["n_updates"] == n_p
    # some outcome must have been pending at some read, else the rule was never exercised
    pending = [lg for lg in logs if lg["G"]["n_updates"] < sum(1 for s in w.scores if s["tier"] == lg["tier"] and s["date"] < lg["date"] and s["items_loss"]["G"] is not None)]
    assert len(pending) >= 10


# ----------------------------------------------------------------------------- DM / HLN

def test_step8_dm_hln_textbook_case():
    # the t-table (two-sided 5% critical values): F(2.776; 4) = F(2.228; 10) = F(2.042; 30) = 0.975
    for x, df in ((2.776, 4), (2.228, 10), (2.042, 30), (1.960, 10 ** 7)):
        assert abs(INF.t_cdf(x, df) - 0.975) < 6e-4
    assert abs(INF.t_cdf(0, 7) - 0.5) < 1e-12 and abs(INF.t_cdf(-2.776, 4) - 0.025) < 6e-4
    # DM on d = [1,2,3,4,5] against zero loss: dbar 3, gamma0 2, DM = 3/sqrt(2/5) = 4.7434,
    # HLN factor for h=1, T=5: sqrt((T+1-2)/T) = sqrt(4/5) -> 4.2426; p = 2(1 - F_t4(4.2426)) = 0.01324
    r = INF.dm_test([1, 2, 3, 4, 5], [0, 0, 0, 0, 0], h=1)
    assert abs(r["dm"] - 3 / math.sqrt(2 / 5)) < 1e-9 and abs(r["dm_hln"] - 4.2426407) < 1e-6
    assert abs(r["p_value"] - 0.01324) < 2e-4 and r["better"] == "B"
    # HLN factor at h=3, T=20: sqrt((20+1-6+6/20)/20)
    r3 = INF.dm_test(np.arange(20) * 0.1 + np.sin(np.arange(20)), np.zeros(20), h=3)
    assert abs(r3["dm_hln"] / r3["dm"] - math.sqrt((20 + 1 - 6 + 6 / 20) / 20)) < 1e-9
    # Newey-West with lag 1 on a known series equals the hand formula gamma0 + 2*(1/2)*gamma1
    d = np.array([1.0, 3.0, 2.0, 4.0, 3.0, 5.0]); dc = d - d.mean()
    g0 = np.mean(dc * dc); g1 = np.mean(dc[1:] * dc[:-1])
    assert abs(INF.newey_west_var(d, 1) - (g0 + 2 * 0.5 * g1)) < 1e-12
    # BH step-up by hand: sorted p = .01, .02, .03, .20 vs k/4 * .05 = .0125, .025, .0375, .05 -> largest k passing is 3
    bh = INF.bh_fdr([0.01, 0.03, 0.02, 0.20], q=0.05)
    assert bh["survive"] == [True, True, True, False]
    # with .04 at rank 3 (.04 > .0375) only rank 1 survives; q-values .04, .0533, .0533, .20 (step-down minima of p_(k) * 4/k)
    bh2 = INF.bh_fdr([0.01, 0.04, 0.03, 0.20], q=0.05)
    assert bh2["survive"] == [True, False, False, False]
    assert np.allclose(bh2["qvalues"], [0.04, 0.04 * 4 / 3, 0.04 * 4 / 3, 0.20])


# ----------------------------------------------------------------------------- leakage

def test_step8_leakage_broken_filtration_must_differ(tmp_path):
    c = _synthetic(n=60)
    sealed = W.Walk(c, MENU, out_dir=tmp_path / "s", params=FAST, quiet=True).run_reads()
    broken = W.Walk(c, MENU, out_dir=tmp_path / "b", params=FAST, quiet=True, break_filtration=True).run_reads()
    lk = W.leakage_test(sealed, broken)
    assert lk["asserted"] is True and lk["reads_differ"] and lk["n_reads_with_different_analogs"] > 0
    assert all(r["filtration_broken"] for r in broken.reads) and not any(r["filtration_broken"] for r in sealed.reads)
    # and a sealed run compared with itself is NOT asserted (the test is not vacuous)
    again = W.Walk(c, MENU, out_dir=tmp_path / "s2", params=FAST, quiet=True).run_reads()
    same = W.leakage_test(sealed, again)
    assert same["n_reads_with_different_analogs"] == 0 and same["asserted"] is False


# ----------------------------------------------------------------------------- placebo null

def test_step8_placebo_skill_is_zero_within_ci_on_synthetic_null_data(tmp_path):
    # P-null: Brent is a seeded random walk unrelated to any state field. G-null: the labels are shuffled
    # (seeded) within the class, because _synthetic's labels follow the actor field by construction.
    c = _synthetic(n=60, seed=11)
    rng = np.random.default_rng(11)
    keys = list(c.ies90); labs = [c.ies90[k] for k in keys]
    c.ies90 = {k: labs[i] for k, i in zip(keys, rng.permutation(len(keys)))}   # level + deal shuffled together
    w = W.Walk(c, MENU, out_dir=tmp_path, params=FAST, quiet=True).run_reads()
    p = dict(W.REGISTERED) | FAST
    tier = W.summarize_tier(w.reads, w.scores, p, "daily", n_boot=200, n_spa=100)
    for task in ("P", "G"):
        blk = tier[task]
        rand = blk["engine_vs"]["random_analogs"]                             # size-matched (protocol §4 baseline 3): the honest null for retrieval
        assert rand["n"] >= 20 and rand["ci95"][0] <= 0 <= rand["ci95"][1], (task, rand)
        fair = blk["diagnostic_fair"]["engine_vs_climatology"]              # size-corrected: no skill beyond sample size
        assert fair["ci95"][0] <= 0 <= fair["ci95"][1], (task, fair)
        reg = blk["engine_vs"]["climatology"]                                 # the registered skill sits BELOW the corrected one: the bias, in the derived direction
        assert reg["skill"] < fair["skill"], (task, reg, fair)
    rr = tier["G"]["rps"]["engine_vs"]["random_analogs"]                       # RPS over the ordinal levels: null too
    assert rr["n"] >= 20 and rr["ci95"][0] <= 0 <= rr["ci95"][1], rr
    assert tier["G"]["deal"]["n_scored"] >= 10 and tier["G"]["deal"]["base_rate"] is not None
    pl = W.placebo(c, MENU, w.reads, w.scores, p, reps=2)
    assert pl["n"] >= 10 and pl["null_holds"] is True and pl["vs_random_analogs"]["covers_zero"]
    assert pl["fair_vs_climatology"]["covers_zero"]
    assert pl["vs_climatology"]["skill"] < pl["fair_vs_climatology"]["skill"]
    perm = W.permutation_test(w.reads, w.scores, p, n_perm=60)
    assert perm["n_reads"] >= 20 and perm["p_value"] > 0.01                   # no label skill on null labels
    v = W.verdict({"tiers": {"daily": tier}, "regime_blocks": W.regime_blocks(w.reads, w.scores, p, n_boot=50),
                   "placebo": pl, "permutation": perm}, p)
    assert v["audit_passed"] is False                                          # Step 4 not recorded -> never VALIDATED
    assert all(r["status"] != "VALIDATED" for r in v["rules"].values())


def test_step8_label_permutation_positive_control(tmp_path):
    """The permutation test must DETECT real label skill: _synthetic's labels follow the actor field, so the
    engine's G skill vs climatology is real and its permutation p must be small (and the null-label case above
    is the negative control)."""
    c, w = _walk(tmp_path, n=60, seed=11)
    p = dict(W.REGISTERED) | FAST
    perm = W.permutation_test(w.reads, w.scores, p, n_perm=200)
    assert perm["observed_skill"] > 0 and perm["p_value"] < 0.05, perm
