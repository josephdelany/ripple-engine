"""
delta_experiment.py -- WALK_FORWARD_PROTOCOL.md Amendment L (2026-09-03): does the analogue distribution
carry information about escalation BEYOND what the dyad's own last 90 days already say?

The published run says G-persistence beats the engine on the registered Brier, 0.4805 to 0.7687. That makes
the LEVEL estimand the wrong one: it asks the engine to REPLACE the dyad's recent history rather than
improve on it. Amendment L re-anchors the same sealed reads on the dyad's own pre-window level L- and asks
the engine to forecast the CHANGE:

    target      dIES = L - L-                      on the seven ordered categories -3..+3   (L.1)
    forecast    each analog votes with its OWN change  d_a = L_a - L-_a                     (L.2)
    baseline    no-change: a point mass on d = 0, Amendment B.2 smoothed  ==  G-persistence (L.3)
    object      the COMBINATION of the two, three registered rules C1/C2/C3                 (L.4)

Everything is computed from the SEALED files (Amendment K's discipline): no retrieval is repeated, no
analog re-read, no Hedge weight re-fitted. The single fitted quantity anywhere in this module is C2's
lambda, fitted walk-forward on a registered grid over closed reads only (L.4).

Registered before this file existed: WALK_FORWARD_PROTOCOL.md Amendment L, commit a2ae995.

Run:  python3 src/engine/delta_experiment.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from engine import scoring as SC          # noqa: E402
from engine import inference as INF       # noqa: E402
import walk as W                          # noqa: E402

WF = ROOT / "data" / "walk_forward"
OUT = WF / "delta_experiment.json"

DELTAS = ("-3", "-2", "-1", "0", "1", "2", "3")     # L.1: the ordered target categories
LAMBDA_GRID = tuple(round(0.1 * i, 1) for i in range(11))   # L.4 C2, registered
LAMBDA_MIN_N = 40                                            # L.4 C2, registered
LAMBDA_DEFAULT = 0.5                                         # L.4 C1 = C2's value below LAMBDA_MIN_N
ANALOG_ITEMS = 12                                            # L.2: M01-M12; M13 carries no analogs


# ---------------------------------------------------------------- distributions over dIES

def feasible(lm: int):
    """L.2: given L-, the reachable changes are exactly {-L-, ..., 3-L-} (levels are clipped into 0..3)."""
    return list(range(-lm, 4 - lm))


def clip(d: int, lm: int) -> int:
    """Amendment J.3 / L.2: an infeasible change moves to the nearest feasible one -- the same thing as
    clipping the implied level into 0..3 with the mass accumulating at the boundary."""
    return max(-lm, min(3 - lm, int(d)))


def dist(atoms, weights=None, lm=0) -> dict:
    """Frequency distribution over DELTAS of (optionally weighted) clipped atoms."""
    atoms = list(atoms)
    if not atoms:
        return {}
    w = np.full(len(atoms), 1.0 / len(atoms)) if weights is None else np.asarray(weights, float)
    w = w / w.sum()
    out = {d: 0.0 for d in DELTAS}
    for a, wi in zip(atoms, w):
        out[str(clip(a, lm))] += float(wi)
    return out


def no_change(lm: int) -> dict:
    """L.3 baseline 1: 0.9 on d = 0, 0.1 over the adjacent FEASIBLE changes -- Amendment B.2's smoothing,
    expressed in this estimand. At a boundary L- the single neighbour takes the whole 0.1."""
    nb = [d for d in (-1, 1) if d in feasible(lm)]
    out = {d: 0.0 for d in DELTAS}
    out["0"] = 0.9
    for d in nb:
        out[str(d)] += 0.1 / len(nb)
    return out


def pool(a: dict, b: dict, lam: float) -> dict:
    """L.4: the linear pool lam * a + (1 - lam) * b. Clipping is linear, so pooling clipped parts is the
    same as clipping the pool."""
    return {d: lam * float(a.get(d, 0.0)) + (1.0 - lam) * float(b.get(d, 0.0)) for d in DELTAS}


def brier(p, y):
    return SC.brier(p, y, branches=DELTAS)


def rps(p, y):
    return SC.rps(p, y, levels=DELTAS)


def assert_delta_level_identity(dd: dict, lm: int, y_delta: str, y_level: str):
    """L.2, registered so that it can never be presented later as a finding: after clipping, d <-> level is
    a bijection on the four feasible categories, so the 7-category dIES Brier and RPS of a clipped forecast
    are NUMERICALLY IDENTICAL to the 4-level Brier and RPS of its implied level forecast. Disagreement is a
    defect, not a result."""
    lvl = {l: 0.0 for l in SC.LEVELS}
    for d, p in dd.items():
        if p:
            assert int(d) in feasible(lm), f"infeasible mass on d = {d} at L- = {lm}: the forecast was not clipped"
            lvl[str(int(d) + lm)] += float(p)
    assert abs(brier(dd, y_delta) - SC.brier(lvl, y_level)) < 1e-9, "delta/level Brier identity broken"
    assert abs(rps(dd, y_delta) - SC.rps(lvl, y_level)) < 1e-9, "delta/level RPS identity broken"
    return lvl


# ---------------------------------------------------------------- building the per-read row

def _rows(name, run_id):
    return [r for r in (json.loads(l) for l in (WF / name).open(encoding="utf-8") if l.strip())
            if r["run_id"] == run_id]


def build(run_id=None):
    """Every forecaster's dIES distribution on every retained read, from the sealed files only."""
    summary = json.loads((WF / "summary.json").read_text())
    run_id = run_id or summary["run_id"]
    reads = {r["event_id"]: r for r in _rows("reads.jsonl", run_id)}
    scores = _rows("scores.jsonl", run_id)

    # L- for any event, from that event's OWN sealed read (window [d-90, d-1], strictly before its date)
    lminus, covering = {}, {}
    for eid, r in reads.items():
        p = (r["baselines"] or {}).get("persistence") or {}
        if p and not p.get("fallback") and p.get("level_pre") is not None:
            lminus[eid] = int(p["level_pre"])
            covering[eid] = len(p.get("covering_pre") or [])

    # the published scored daily-tier G set: exactly summary tiers.daily.G.engine_vs.climatology.n
    sel = [s for s in scores if s["tier"] == "daily" and s.get("burn_in_ok")
           and (s["scores"].get("engine") or {}).get("G") and (s["scores"].get("climatology") or {}).get("G")]
    sel.sort(key=lambda s: (s["date"], s["event_id"]))

    excl = Counter()
    rows, analog_slots, analog_dropped, analog_cover = [], 0, 0, []
    for s in sel:
        eid = s["event_id"]
        r = reads[eid]
        if s["outcome"].get("no_independent_outcome"):
            excl["no_independent_outcome"] += 1; continue
        if eid not in lminus:
            excl["persistence_fallback"] += 1; continue
        lm = lminus[eid]
        y_level = s["outcome"]["level"]
        y = str(int(y_level) - lm)

        # --- the analogue mixture (L.2): M01-M12 vote with their own analogs' changes, sealed Hedge weights
        wts = r["weights"]["G"][:ANALOG_ITEMS]
        item_atoms = []
        for it in r["items"][:ANALOG_ITEMS]:
            ids = it.get("G_ids") or []
            labs = it.get("G_labels") or []
            at = []
            for aid, lab in zip(ids, labs):
                analog_slots += 1
                if aid in lminus and lab in SC.LEVELS:
                    at.append(int(lab) - lminus[aid])
                    analog_cover.append(covering[aid])
                else:
                    analog_dropped += 1
            item_atoms.append(at)

        # --- climatology (L.3 baseline 3): the read's OWN point-in-time G pool, each member's own change
        pool_ids = r["baselines"]["random_analogs"]["g_pool_ids"]
        pool_labs = r["baselines"]["climatology"]["G_labels"] or []
        clim_atoms = [int(lab) - lminus[pid] for pid, lab in zip(pool_ids, pool_labs)
                      if pid in lminus and lab in SC.LEVELS] if len(pool_ids) == len(pool_labs) else []
        if not clim_atoms:
            excl["no_delta_climatology"] += 1; continue
        d_clim = dist(clim_atoms, lm=lm)

        # abstain rule, unchanged: an item with no dIES atom is charged the dIES-climatology forecast
        atoms, aw = [], []
        for at, wi in zip(item_atoms, wts):
            src = at if at else clim_atoms
            for a in src:
                atoms.append(a); aw.append(wi / len(src))
        if not atoms:
            excl["no_delta_analogue"] += 1; continue
        d_ana = dist(atoms, aw, lm=lm)
        d_frozen = dist([a for at in item_atoms for a in (at if at else clim_atoms)],
                        [1.0 / (ANALOG_ITEMS * len(at if at else clim_atoms))
                         for at in item_atoms for _ in (at if at else clim_atoms)], lm=lm)

        # --- random analogs (L.3 baseline 4): re-drawn from the same pool, same k, same seed, same draws
        b = r["baselines"]["random_analogs"]
        rng = np.random.default_rng(b["seed"])
        d_rand = []
        for _ in range(b["draws"]):
            pick = rng.choice(len(clim_atoms), size=min(b["k"], len(clim_atoms)), replace=False)
            d_rand.append(dist([clim_atoms[i] for i in pick], lm=lm))

        d_nc = no_change(lm)
        assert_delta_level_identity(d_ana, lm, y, y_level)
        assert_delta_level_identity(d_nc, lm, y, y_level)

        rows.append({
            "event_id": eid, "date": s["date"], "as_of": r["as_of"], "type": s["type"],
            "l_minus": lm, "level": int(y_level), "delta": y, "covering_pre": covering[eid],
            "g_closed_on": s["outcome"]["g_closed_on"],
            "atoms_analogue": atoms, "weights_analogue": aw,          # unclipped: the forecast permutation re-clips
            "d": {"no_change": d_nc, "analogue": d_ana, "climatology": d_clim,
                  "frozen": d_frozen, "random_analogs": d_rand},
        })
    return {"run_id": run_id, "rows": rows, "excluded": dict(excl), "n_published": len(sel),
            "analog_slots": analog_slots, "analog_delta_dropped": analog_dropped,
            "analog_covering_pre": analog_cover, "summary": summary}


def reanchoring_check(rows, run_id):
    """A CHECK ON THIS MODULE, not a new estimand and not a comparison: rebuild the SAME mixture over the
    SAME twelve items with the SAME sealed Hedge weights, but with the analogs voting on LEVEL as the
    sealed run does. If that reproduces the sealed engine's level Brier (up to M13's share of the weight,
    which this mixture drops), then the ONLY difference between the sealed engine's score and the analogue
    score of L.2 is the anchor. Computed from the sealed files; gates nothing."""
    reads = {r["event_id"]: r for r in _rows("reads.jsonl", run_id)}
    scores = {s["event_id"]: s for s in _rows("scores.jsonl", run_id)}
    mine, sealed = [], []
    for row in rows:
        r = reads[row["event_id"]]; y = scores[row["event_id"]]["outcome"]["level"]
        pool_labs = [l for pid, l in zip(r["baselines"]["random_analogs"]["g_pool_ids"],
                                         r["baselines"]["climatology"]["G_labels"] or []) if l in SC.LEVELS]
        lab, w = [], []
        for it, wi in zip(r["items"][:ANALOG_ITEMS], r["weights"]["G"][:ANALOG_ITEMS]):
            src = [x for x in (it.get("G_labels") or []) if x in SC.LEVELS] or pool_labs
            for x in src:
                lab.append(x); w.append(wi / len(src))
        w = np.array(w); w = w / w.sum()
        d = {L: float(w[[i for i, x in enumerate(lab) if x == L]].sum()) for L in SC.LEVELS}
        mine.append(SC.brier(d, y)); sealed.append(SC.brier(r["engine"]["G"], y))
    return {"what": "the same twelve items, the same sealed weights, the analogs voting on LEVEL instead of "
                    "on CHANGE -- a check that the re-anchoring is the only thing this experiment changes",
            "level_mixture_M01_M12": round(float(np.mean(mine)), 6),
            "sealed_engine_G_13_items": round(float(np.mean(sealed)), 6),
            "difference_is": "M13's share of the sealed Hedge weight, which the twelve-item mixture drops",
            "gates": "nothing; a validation of this module"}


# ---------------------------------------------------------------- the three combinations (L.4)

def combinations(rows):
    """C1 fixed lambda 0.5; C2 lambda fitted walk-forward on the registered grid over CLOSED reads only;
    C3 Hedge over {no-change, analogue} at the registered eta, from past closed losses only."""
    n = len(rows)
    y = [r["delta"] for r in rows]
    b_nc = np.array([brier(r["d"]["no_change"], y[i]) for i, r in enumerate(rows)])
    b_an = np.array([brier(r["d"]["analogue"], y[i]) for i, r in enumerate(rows)])
    # B[j, g] = registered Brier of the pool at grid weight g on read j
    B = np.array([[brier(pool(r["d"]["no_change"], r["d"]["analogue"], g), y[i]) for g in LAMBDA_GRID]
                  for i, r in enumerate(rows)])
    closed = np.zeros((n, n), bool)                 # closed[i, j]: read j's branch window had closed by read i's as_of
    for i, ri in enumerate(rows):
        for j, rj in enumerate(rows):
            if i != j and rj["g_closed_on"] and rj["g_closed_on"] <= ri["as_of"]:
                closed[i, j] = True

    lam, hedge_w = [], []
    for i in range(n):
        past = np.where(closed[i])[0]
        if len(past) < LAMBDA_MIN_N:
            lam.append(LAMBDA_DEFAULT)
        else:
            cum = B[past].sum(axis=0)
            best = float(cum.min())
            lam.append(max(g for g, c in zip(LAMBDA_GRID, cum) if c <= best + 1e-12))   # ties -> larger lambda
        if len(past) == 0:
            hedge_w.append(0.5)
        else:
            cl = np.array([b_nc[past].sum(), b_an[past].sum()]) / W.REGISTERED["g_scale"]
            e = np.exp(-W.REGISTERED["eta"] * (cl - cl.min()))
            hedge_w.append(float(e[0] / e.sum()))

    c1 = [pool(r["d"]["no_change"], r["d"]["analogue"], LAMBDA_DEFAULT) for r in rows]
    c2 = [pool(r["d"]["no_change"], r["d"]["analogue"], lam[i]) for i, r in enumerate(rows)]
    c3 = [pool(r["d"]["no_change"], r["d"]["analogue"], hedge_w[i]) for i, r in enumerate(rows)]
    for i, r in enumerate(rows):
        r["d"]["C1_fixed_0.5"] = c1[i]; r["d"]["C2_walkforward_lambda"] = c2[i]; r["d"]["C3_hedge"] = c3[i]
        r["lambda_c2"] = lam[i]; r["w_nochange_c3"] = hedge_w[i]
    return {"lambda_trajectory": lam, "lambda_terminal": lam[-1],
            "lambda_final_all_closed": max(g for g, c in zip(LAMBDA_GRID, B.sum(axis=0))
                                           if c <= float(B.sum(axis=0).min()) + 1e-12),
            "lambda_n_fitted": int(sum(1 for i in range(n) if closed[i].sum() >= LAMBDA_MIN_N)),
            "hedge_w_nochange_trajectory": hedge_w, "hedge_w_nochange_terminal": hedge_w[-1],
            "grid": list(LAMBDA_GRID), "min_n": LAMBDA_MIN_N}


# ---------------------------------------------------------------- scoring and inference (L.5, L.6)

FORECASTERS = ("C1_fixed_0.5", "C2_walkforward_lambda", "C3_hedge", "analogue",
               "no_change", "climatology", "frozen", "random_analogs")
ATOMIC = ("analogue", "climatology", "frozen", "random_analogs")   # L.5: fair scores defined only here


def score_rows(rows):
    """Registered Brier (the gate), RPS and log score beside it, Ferro fair forms as diagnostic."""
    S = {f: {"brier": [], "rps": [], "log": [], "brier_fair": [], "rps_fair": []} for f in FORECASTERS}
    for r in rows:
        y = r["delta"]
        for f in FORECASTERS:
            d = r["d"][f]
            if f == "random_analogs":
                S[f]["brier"].append(float(np.mean([brier(x, y) for x in d])))
                S[f]["rps"].append(float(np.mean([rps(x, y) for x in d])))
                S[f]["log"].append(float(np.mean([SC.log_score(x, y, branches=DELTAS) for x in d])))
                S[f]["brier_fair"].append(None); S[f]["rps_fair"].append(None)
                continue
            S[f]["brier"].append(brier(d, y)); S[f]["rps"].append(rps(d, y))
            S[f]["log"].append(SC.log_score(d, y, branches=DELTAS))
            if f == "analogue":
                lab = [str(clip(a, r["l_minus"])) for a in r["atoms_analogue"]]
                S[f]["brier_fair"].append(SC.brier_fair(lab, y, r["weights_analogue"], branches=DELTAS))
                S[f]["rps_fair"].append(SC.rps_fair(lab, y, r["weights_analogue"], levels=DELTAS))
            elif f == "no_change":
                S[f]["brier_fair"].append(S[f]["brier"][-1])       # a point mass has no spread to correct (F.4)
                S[f]["rps_fair"].append(S[f]["rps"][-1])
            else:
                S[f]["brier_fair"].append(None); S[f]["rps_fair"].append(None)
    return S


def _block(a, b, mean_block, lag, n_boot):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3:
        return {"n": len(a), "skill": None}
    ci = INF.bootstrap_ci(lambda ix: None if b[ix].mean() == 0 else 1.0 - a[ix].mean() / b[ix].mean(),
                          len(a), n_boot=n_boot, mean_block=mean_block)
    dm = INF.dm_test(a, b, h=1, lag=lag)
    return {"n": len(a), "mean": float(a.mean()), "ref_mean": float(b.mean()), "skill": ci["estimate"],
            "ci95": [ci["lo"], ci["hi"]], "dm_hln": dm.get("dm_hln"), "dm_p": dm.get("p_value"),
            "dm_ok": dm.get("ok", False)}


def clusters_of(dates, cluster_days):
    """Amendment F.2's construction: reads within cluster_days of the previous read are one cluster."""
    out, cur = [], [0]
    for i in range(1, len(dates)):
        if (pd.Timestamp(dates[i]) - pd.Timestamp(dates[i - 1])).days <= cluster_days:
            cur.append(i)
        else:
            out.append(cur); cur = [i]
    out.append(cur)
    return out


def permutations(rows, cl, n_perm, seed=19900802):
    """L.6 (i) block LABEL permutation -- the §7-form condition: the realized LEVEL is permuted across intact
    clusters and dIES recomputed with each read's OWN L-, so every permuted target is feasible by
    construction. (ii) FORECAST permutation: the analogue distributions are permuted across intact clusters
    and RE-CLIPPED to the receiving read's feasible set. Both on C1 vs no-change."""
    n = len(rows)
    lm = np.array([r["l_minus"] for r in rows])
    lev = np.array([r["level"] for r in rows])
    nc = [r["d"]["no_change"] for r in rows]

    def skill(levels, ana):
        ys = [str(int(levels[i]) - lm[i]) for i in range(n)]
        e = np.array([brier(pool(nc[i], ana[i], LAMBDA_DEFAULT), ys[i]) for i in range(n)])
        b = np.array([brier(nc[i], ys[i]) for i in range(n)])
        return 1.0 - e.mean() / b.mean()

    ana0 = [r["d"]["analogue"] for r in rows]
    obs = skill(lev, ana0)

    rng = np.random.default_rng(seed)
    null_lab = []
    for _ in range(n_perm):
        seq = [i for k in rng.permutation(len(cl)) for i in cl[k]]
        null_lab.append(skill(lev[np.array(seq)], ana0))

    rng2 = np.random.default_rng(seed + 1)
    null_fc = []
    for _ in range(n_perm):
        seq = [i for k in rng2.permutation(len(cl)) for i in cl[k]]
        ana = [dist(rows[seq[i]]["atoms_analogue"], rows[seq[i]]["weights_analogue"], lm=lm[i]) for i in range(n)]
        null_fc.append(skill(lev, ana))

    def blk(null, rule):
        null = np.array(null)
        return {"p_value": INF.permutation_p(obs, null), "null_mean": float(null.mean()),
                "null_sd": float(null.std()), "null_p95": float(np.percentile(null, 95)), "rule": rule}

    return {"observed_skill": float(obs), "n_perm": n_perm, "n_clusters": len(cl),
            "decides": "label (block form, Amendment F.2 / L.6 i)",
            "label_block": blk(null_lab, "the realized LEVEL permuted across intact 35-day clusters; dIES "
                                         "recomputed with each read's own L- (feasible by construction)"),
            "forecast_block": blk(null_fc, "the analogue dIES distributions permuted across intact clusters and "
                                           "re-clipped to the receiving read's feasible set; gates nothing")}


# ---------------------------------------------------------------- the verdict (L.7)

def verdict(c1, c2, spa_p, perm_p, lam_terminal):
    """L.7's four registered verdicts, decided by conditions written before the numbers existed."""
    def beats(b):
        return b.get("skill") is not None and b["skill"] > 0 and b.get("dm_p") is not None \
            and b["dm_p"] < 0.05 and b["ci95"][0] is not None and b["ci95"][0] > 0
    def beaten(b):
        return b.get("skill") is not None and b["skill"] < 0 and b.get("dm_p") is not None \
            and b["dm_p"] < 0.05 and b["ci95"][1] is not None and b["ci95"][1] < 0

    if beats(c1) and spa_p is not None and spa_p < 0.05 and perm_p is not None and perm_p < 0.05:
        return "INCREMENTAL", ("historical analogy carries information about escalation beyond the dyad's own "
                               "last 90 days: the registered equal pool beats no-change on every condition of L.7")
    if beats(c2) and lam_terminal < 0.5:
        return "INCREMENTAL-UNDER-FITTED-WEIGHT", ("the analogue carries information, but only at a weight the "
                                                   "registered equal pool does not use; strictly weaker than "
                                                   "INCREMENTAL and never to be reported as it")
    if beaten(c1) and lam_terminal >= 0.9:
        return "DEGRADES", ("the analogue actively degrades a good baseline -- the walk-forward weight runs away "
                            "from it too")
    note = ("the equal pool loses but the walk-forward weight does not run away from the analogue "
            f"(terminal lambda {lam_terminal}), so the loss is attributable to the REGISTERED EQUAL WEIGHT, not "
            "to the analogue's content (L.7, L.8.2)") if beaten(c1) else \
           "no combination separates from no-change at the registered conditions"
    return "NO ADDITION", note


# ---------------------------------------------------------------- run

def compute(run_id=None, n_boot=None, n_spa=None, n_perm=None):
    p = W.REGISTERED
    n_boot = n_boot or p["n_boot"]; n_spa = n_spa or p["n_spa_boot"]; n_perm = n_perm or p["n_perm"]
    built = build(run_id)
    rows = built["rows"]
    if len(rows) < p["min_tier_n"]:
        return {"note": f"only {len(rows)} retained reads; below the registered min_tier_n {p['min_tier_n']}"}
    comb = combinations(rows)
    S = score_rows(rows)
    dates = [r["date"] for r in rows]
    mb = W._mean_block(dates, p["cluster_days"]); lag = max(int(round(mb)) - 1, 0)
    cl = clusters_of(dates, p["cluster_days"])

    def vs_nc(key):
        return {f: _block(S[f][key], S["no_change"][key], mb, lag, n_boot)
                for f in FORECASTERS if f != "no_change"}

    fam = ["C1_fixed_0.5", "C2_walkforward_lambda", "C3_hedge"]
    d = np.array([[S["no_change"]["brier"][i] - S[f]["brier"][i] for f in fam] for i in range(len(rows))])
    spa = INF.spa(d, n_boot=n_spa, mean_block=mb)
    spa["best_model"] = fam[spa["best_model"]]; spa["models"] = fam; spa["benchmark"] = "no_change"

    perm = permutations(rows, cl, n_perm)

    diff = np.array(S["C1_fixed_0.5"]["brier"]) - np.array(S["no_change"]["brier"])
    power = INF.power_block(diff, mb, lag, float(np.mean(S["no_change"]["brier"])), n_list=[len(rows)])

    brier_vs = vs_nc("brier"); rps_vs = vs_nc("rps")
    v, why = verdict(brier_vs["C1_fixed_0.5"], brier_vs["C2_walkforward_lambda"],
                     spa.get("p_spa"), perm["label_block"]["p_value"], comb["lambda_terminal"])   # INF.spa returns p_spa / p_rc

    # L.8.4 sensitivity: reads whose L- is carried by >= 2 sources
    idx2 = [i for i, r in enumerate(rows) if r["covering_pre"] >= 2]
    sens = None
    if len(idx2) >= p["min_tier_n"]:
        d2 = [rows[i]["date"] for i in idx2]
        mb2 = W._mean_block(d2, p["cluster_days"]); lag2 = max(int(round(mb2)) - 1, 0)
        sens = {"n": len(idx2), "mean_block": round(mb2, 2),
                "brier": {f: _block([S[f]["brier"][i] for i in idx2], [S["no_change"]["brier"][i] for i in idx2],
                                    mb2, lag2, n_boot) for f in ("C1_fixed_0.5", "C2_walkforward_lambda", "analogue")}}

    dshare = Counter(r["delta"] for r in rows)
    n = len(rows)
    fdr_names, fdr_p = [], []
    for key, blocks in (("brier", brier_vs), ("rps", rps_vs)):
        for f, b in blocks.items():
            if b.get("dm_p") is not None:
                fdr_names.append(f"{key}:{f}_vs_no_change"); fdr_p.append(b["dm_p"])
    bh = INF.bh_fdr(fdr_p, q=0.05)

    out = {
        "amendment": "WALK_FORWARD_PROTOCOL.md Amendment L (2026-09-03), registered in commit a2ae995 before "
                     "this module existed",
        "question": "does the analogue distribution carry information about escalation BEYOND what the dyad's "
                    "own last 90 days already say?",
        "registered": True, "gates": "nothing in §7; engine:G on the level estimand is unchanged",
        "derived_from_run": built["run_id"],
        "computed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tier": "daily", "n_published_scored_G": built["n_published"], "n_retained": n,
        "excluded": built["excluded"],
        "analogs": {"slots": built["analog_slots"], "delta_dropped": built["analog_delta_dropped"],
                    "mean_covering_pre": round(float(np.mean(built["analog_covering_pre"])), 2)
                    if built["analog_covering_pre"] else None},
        "target": {"support": list(DELTAS),
                   "marginal": {k: dshare.get(k, 0) for k in DELTAS},
                   "share_zero": round(dshare.get("0", 0) / n, 4),
                   "near_degenerate": dshare.get("0", 0) / n > 0.90,
                   "mean_l_minus": round(float(np.mean([r["l_minus"] for r in rows])), 3)},
        "dependence": {"cluster_days": p["cluster_days"], "mean_block": round(mb, 2), "hac_lag": lag,
                       "n_clusters": len(cl)},
        "scores": {f: {"brier": round(float(np.mean(S[f]["brier"])), 6),
                       "rps": round(float(np.mean(S[f]["rps"])), 6),
                       "log": round(float(np.mean(S[f]["log"])), 6),
                       "brier_fair": (round(float(np.mean([x for x in S[f]["brier_fair"] if x is not None])), 6)
                                      if any(x is not None for x in S[f]["brier_fair"]) else None),
                       "rps_fair": (round(float(np.mean([x for x in S[f]["rps_fair"] if x is not None])), 6)
                                    if any(x is not None for x in S[f]["rps_fair"]) else None)}
                   for f in FORECASTERS},
        "fair_scope": "L.5: the Ferro size-corrected scores are defined for the atomic forecasters and for the "
                      "point-mass baseline (whose fair score equals its registered one, Amendment F.4). For the "
                      "pools C1/C2/C3 they are null: a mixture with a non-atomic component has no registered "
                      "Ferro form, and inventing one after registration is not admissible. The gate is the "
                      "registered Brier either way (E.1).",
        "vs_no_change": {"brier": brier_vs, "rps": rps_vs},
        "reanchoring_check": reanchoring_check(rows, built["run_id"]),
        "combination": {k: v for k, v in comb.items() if not k.endswith("trajectory")},
        "lambda_trajectory": comb["lambda_trajectory"],
        "hedge_w_nochange_trajectory": comb["hedge_w_nochange_trajectory"],
        "spa": spa, "permutation": perm, "power": power, "fdr": {"names": fdr_names, "p": fdr_p, "bh": bh},
        "sensitivity_covering_ge2": sens,
        "verdict": {"label": v, "reading": why,
                    "rule": "WALK_FORWARD_PROTOCOL.md Amendment L.7, written before these numbers existed",
                    "cannot": "make anything VALIDATED -- the §7 label audit is 1 of 30 rows in"},
        "limits": [
            f"n = {n} retained of {built['n_published']} scored G reads; the measured minimum detectable skill "
            f"at n = 150 on the level target was 0.127, so a null here reads as 'not detectable at this n'.",
            "the registered Brier charges the analogue's k-atom distribution a penalty it cannot charge the "
            "point mass (E.3); the direction of that bias is known and runs AGAINST the analogue. The Ferro "
            "fair scores are published beside it and do not gate.",
            "L- enters the target, the baseline and the analogue anchor at once; an L- coverage error cancels "
            "in no-change and does not cancel in the target. The >= 2-source sensitivity is published.",
            "a diagnostic-standing re-anchoring of a SEALED run: no retrieval repeated, no Hedge weight "
            "re-fitted; C2's lambda is the only fitted quantity and is fitted walk-forward on closed reads.",
        ],
    }
    return out, rows, built["summary"]


def main():
    res = compute()
    if isinstance(res, dict):
        print(json.dumps(res)); return
    out, rows, summary = res
    OUT.write_text(json.dumps(out, indent=1, default=str))
    per_read = [{k: r[k] for k in ("event_id", "date", "l_minus", "level", "delta", "covering_pre",
                                   "lambda_c2", "w_nochange_c3")} for r in rows]
    (WF / "delta_experiment_reads.json").write_text(json.dumps(per_read, indent=1))
    summary["tiers"]["daily"]["G"]["experiment_delta"] = out
    (WF / "summary.json").write_text(json.dumps(summary, indent=1, default=str))
    print(json.dumps({k: out[k] for k in ("n_retained", "excluded", "target", "scores", "verdict")}, indent=1))
    print(json.dumps({"vs_no_change_brier": out["vs_no_change"]["brier"], "spa": {k: out["spa"].get(k) for k in
                      ("p_spa", "p_rc", "best_model")}, "permutation": {k: out["permutation"][k]["p_value"] for k in
                      ("label_block", "forecast_block")}, "lambda_terminal": out["combination"]["lambda_terminal"]},
                     indent=1))


if __name__ == "__main__":
    main()
