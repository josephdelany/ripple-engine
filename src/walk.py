"""
walk.py -- PATH Step 8 / BUILD_V3 S6: the walk, per WALK_FORWARD_PROTOCOL.md (registered 2026-09-02).

Stand at each corpus event in order, read, SEAL the read, only then look up the outcome, score it,
and let the engine learn -- but only from outcomes that had closed by the next read. Then ask
whether the skill is real: DM/HLN against four baselines, stationary block bootstrap, Reality Check
/ SPA over the family, BH-FDR, VIX-matched placebo, label permutation, regime-block leave-out,
specification curve, simulation power, and the leakage test (a run with the filtration broken must
differ). Everything is published as computed; VALIDATED is decided by §7 of the protocol including
the Step 4 audit flag, which is false until data/audits/outcome_audit.json records a pass.

Outputs (data/walk_forward/): reads.jsonl (sealed, append-only), scores.jsonl, weights.jsonl,
summary.json, big_moves_knew.json, figures/*.png.

Run:  python3 src/walk.py            (full run; ~minutes)
      python3 src/walk.py --fast     (fewer bootstrap/permutation draws; for smoke checks only)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine import similarity as S      # noqa: E402
from engine import read as R            # noqa: E402
from engine import scoring as SC        # noqa: E402
from engine import learning as LN       # noqa: E402
from engine import inference as INF     # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WF = ROOT / "data" / "walk_forward"
AUDIT = ROOT / "data" / "audits" / "outcome_audit.json"
BRANCHES = SC.BRANCHES
GEO = set(R.GEO_TYPES)
TIER_ORDER = ("monthly", "daily")

REGISTERED = {
    "protocol": "WALK_FORWARD_PROTOCOL.md (2026-09-02)",
    "burn_in": 8,                # class needs >= 8 prior members with closed outcomes to be scored (§2)
    "k_max": 12,                 # analogs kept per item so the spec curve can slice k without re-reading
    "cluster_days": 35,          # reads within 35 days are one cluster (§6): sets the bootstrap block + HAC lag
    "eta": LN.ETA,               # Hedge learning rate (§5)
    "g_scale": 2.0,              # Hedge loss for G = Brier / 2  (Brier in [0,2])
    "p_scale": 30.0,             # Hedge loss for P = min(CRPS / 30 pct-points, 1)
    "abstain_rule": "an item with no adequate precedent is charged the climatology loss for that read",
    "random_draws": 25,          # baseline 3: k random analogs from the class, averaged over 25 seeded draws
    "n_boot": 2000, "n_spa_boot": 1000, "n_perm": 1000,
    "min_tier_n": 30,            # a tier with fewer scored reads 'describes, does not validate' (§9)
    "regime_blocks": [2008, 2020, 2026],
    "placebo_reps": 5, "placebo_excl_days": 30,
    "spec": {"burn_in": [6, 8, 10], "k": [5, 8, 12], "horizon_daily": [15, 20, 25],
             "cluster_days": [25, 35, 45], "big_move_q": [0.90, 0.95, 0.975]},
    "pit_bins": 10, "reliability_bins": 5,
}
FAST = {"n_boot": 200, "n_spa_boot": 200, "n_perm": 100, "random_draws": 5, "placebo_reps": 1}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def seal(record):
    """Content hash over the whole record (sealed_at included) -- any later change is detectable."""
    record["sealed_at"] = _now()
    record["hash"] = hashlib.sha256(_canon({k: v for k, v in record.items() if k != "hash"}).encode()).hexdigest()
    return record


def verify_seal(record):
    body = {k: v for k, v in record.items() if k != "hash"}
    return hashlib.sha256(_canon(body).encode()).hexdigest() == record.get("hash")


def verify_file(path):
    """Every line re-hashes to its own seal. Returns (ok, n_checked, first_bad_line)."""
    n = 0
    for i, line in enumerate(open(path, encoding="utf-8")):
        if not line.strip():
            continue
        n += 1
        if not verify_seal(json.loads(line)):
            return False, n, i + 1
    return True, n, None


# ============================================================================ the walk

class Walk:
    def __init__(self, corpus, menu, out_dir=WF, run_id=None, params=None, break_filtration=False, quiet=False):
        self.c = corpus
        self.menu = menu["items"]
        self.N = len(self.menu)
        self.out = Path(out_dir)
        self.out.mkdir(parents=True, exist_ok=True)
        self.p = dict(REGISTERED) | (params or {})
        self.broken = break_filtration
        self.quiet = quiet
        self.run_id = run_id or f"walk_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}" + ("_BROKEN" if break_filtration else "")
        self.reads, self.scores, self.weights_log = [], [], []

    def log(self, *a):
        if not self.quiet:
            print(*a, flush=True)

    # ---------------------------------------------------------------- phase 1: sealed reads
    def run_reads(self):
        rf = open(self.out / "reads.jsonl", "a", encoding="utf-8")
        sf = open(self.out / "scores.jsonl", "a", encoding="utf-8")
        wf = open(self.out / "weights.jsonl", "a", encoding="utf-8")
        try:
            for tier in TIER_ORDER:
                self._tier(tier, rf, sf, wf)
        finally:
            rf.close(); sf.close(); wf.close()
        return self

    def _tier(self, tier, rf, sf, wf):
        events = [e for e in self.c.events if e["tier"] == tier]
        H = R.TIERS[tier]["horizon"]
        hedge = {"G": LN.Hedge(self.N, self.p["eta"]), "P": LN.Hedge(self.N, self.p["eta"])}
        pending = []                                            # (close_date, task, losses)
        t0 = time.time()
        for i, e in enumerate(events):
            t = e["event_date"]
            # (1) learn from outcomes that had closed by t -- never from this read's own outcome
            still = []
            for close, task, losses in pending:
                if close <= t:
                    hedge[task].update(losses)
                else:
                    still.append((close, task, losses))
            pending = still
            w = {task: hedge[task].weights() for task in hedge}
            # (2) the twelve reads at t (pool identical across items; threshold/k/weights differ)
            items, n_pool = [], 0
            for m in self.menu:
                r = R.read(self.c, e, weighting=dict(m, k=self.p["k_max"]), with_propagation=False,
                           with_differencing=False, break_filtration=self.broken)
                n_pool = max(n_pool, r["filtration"]["n_pool"])
                if r["no_adequate_precedent"]:
                    items.append({"id": m["id"], "k": m["k"], "no_precedent": True, "ranked": [], "G": None, "P": None, "M": None})
                    continue
                top = r["analogs"][: m["k"]]
                g = R.g_distribution(top) if e["type"] in GEO else None
                pdist = R.p_distribution(self.c, top, tier)
                mm = R.m_read(self.c, top, tier)
                g_atoms = [(a["event_id"], a["outcome"]) for a in top if a.get("g_closed") and a.get("outcome") in BRANCHES] if g else []
                items.append({"id": m["id"], "k": m["k"], "no_precedent": False,
                              "ranked": [[a["event_id"], a["similarity"], bool(a["g_closed"]), bool(a["p_closed"])] for a in r["analogs"]],
                              "G": (g["rates"] if g and g["n"] else None), "G_n": (g["n"] if g else 0),
                              "G_ids": [i for i, _ in g_atoms], "G_labels": [l for _, l in g_atoms],
                              "P": (pdist["values"] if pdist["n"] else None), "P_ids": pdist.get("analog_ids", []),
                              "M": mm["call"]})
            pool = self.c.pool(self.c.vector(e["event_id"]) | {"tier": tier}, t, break_filtration=self.broken)
            g_pool = [c for c in pool if c["g_closed"]]
            p_pool = [c for c in pool if c["p_closed"]]
            clim_G = None
            if e["type"] in GEO and g_pool:
                outs = [c["outcome"] for c in g_pool]
                clim_G = {b: outs.count(b) / len(outs) for b in BRANCHES}
            clim_P = [round(self.c.outcome(c["event_id"], H, tier)["chg_pct"], 3) for c in p_pool] or None
            burn_in_ok = len(p_pool if e["type"] not in GEO else g_pool) >= self.p["burn_in"]
            # engine (Hedge mixture) and frozen (uniform mixture)
            eng = self._mix(items, w["G"], w["P"], tier)
            frozen = self._mix(items, np.full(self.N, 1.0 / self.N), np.full(self.N, 1.0 / self.N), tier)
            rec = {"run_id": self.run_id, "tier": tier, "event_id": e["event_id"], "date": t, "as_of": t, "type": e["type"],
                   "horizon": H, "unit": R.TIERS[tier]["unit"], "n_pool": len(pool), "n_pool_g": len(g_pool), "n_pool_p": len(p_pool),
                   "burn_in_ok": bool(burn_in_ok), "filtration_broken": self.broken,
                   "weights": {"G": [round(float(x), 6) for x in w["G"]], "P": [round(float(x), 6) for x in w["P"]]},
                   "items": items, "engine": eng, "frozen": frozen,
                   "baselines": {"climatology": {"G": clim_G, "G_labels": [c["outcome"] for c in g_pool] if clim_G else [], "P": clim_P},
                                 "persistence": {"P": [0.0]},
                                 "random_analogs": {"k": self.menu[0]["k"], "draws": self.p["random_draws"],
                                                    "seed": int(hashlib.sha256(e["event_id"].encode()).hexdigest()[:8], 16),
                                                    "g_pool_ids": [c["event_id"] for c in g_pool], "p_pool_ids": [c["event_id"] for c in p_pool]}},
                   "state_unknown": self.c.vector(e["event_id"])["unknown"]}
            seal(rec)
            rf.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n"); rf.flush()
            self.reads.append(rec)
            wf.write(json.dumps({"run_id": self.run_id, "tier": tier, "date": t, "event_id": e["event_id"],
                                 "G": hedge["G"].state(), "P": hedge["P"].state()}) + "\n")
            # (3) ONLY NOW the outcome
            outcome = self._outcome(e, tier, H)
            sc = self._score(rec, outcome)
            sf.write(json.dumps(sc, ensure_ascii=False, default=str) + "\n"); sf.flush()
            self.scores.append(sc)
            # (4) queue the items' losses for Hedge, keyed by the date the outcome became knowable
            if outcome["branch"] and e["type"] in GEO and sc["items_loss"]["G"] is not None:
                pending.append((outcome["g_closed_on"], "G", sc["items_loss"]["G"]))
            if outcome["chg_pct"] is not None and sc["items_loss"]["P"] is not None:
                pending.append((outcome["closed_on"], "P", sc["items_loss"]["P"]))
            if (i + 1) % 50 == 0:
                self.log(f"  {tier}: {i + 1}/{len(events)} reads ({time.time() - t0:.0f}s)")
        self.log(f"{tier}: {len(events)} reads sealed")

    def _mix(self, items, wG, wP, tier):
        G = SC.mixture_g([it["G"] for it in items], wG) if any(it["G"] for it in items) else None
        g_ids, g_labels, g_ws = SC.mixture_atoms([it.get("G_ids") or [] for it in items], [it.get("G_labels") or [] for it in items], wG)
        vals, ws, ids = SC.mixture_p([it["P"] for it in items], wP, [it.get("P_ids") or [] for it in items])
        mcalls = [(it["M"], w) for it, w in zip(items, wP) if it["M"]]
        M = None
        if mcalls:
            z = sum(w for _, w in mcalls)
            M = "MATERIAL" if z > 0 and sum(w for m, w in mcalls if m == "MATERIAL") / z >= 0.5 else "NOT_MATERIAL"
        out = {"G": ({b: round(v, 5) for b, v in G.items()} if G else None), "M": M,
               "G_atoms": ({"ids": g_ids, "labels": g_labels, "weights": [round(x, 6) for x in g_ws]} if G else None),
               "P": ({"values": [round(v, 3) for v in vals], "weights": [round(x, 6) for x in ws], "ids": ids,
                      "p10": round(SC.weighted_quantile(vals, 0.10, ws), 2), "p50": round(SC.weighted_quantile(vals, 0.50, ws), 2),
                      "p90": round(SC.weighted_quantile(vals, 0.90, ws), 2), "n_atoms": len(vals)} if vals else None)}
        return out

    def _outcome(self, e, tier, H):
        o = self.c.outcome(e["event_id"], H, tier)
        br = e.get("sr_outcome_90") if (e["type"] in GEO and e.get("sr_outcome_90") in BRANCHES) else None
        return {"branch": br, "chg_pct": (None if o is None else o["chg_pct"]), "closed_on": (None if o is None else o["closed_on"]),
                "g_closed_on": str((pd.Timestamp(e["event_date"]) + pd.Timedelta(days=R.G_HORIZON_DAYS)).date()),
                "in_big_move": self.c.in_big_move(e["event_id"]), "looked_up_at": _now()}

    def _score_p(self, vals, y, ws=None):
        return {"crps": SC.crps(vals, y, ws), "pin10": SC.pinball(vals, y, 0.10, ws), "pin50": SC.pinball(vals, y, 0.50, ws),
                "pin90": SC.pinball(vals, y, 0.90, ws), "pit": SC.pit(vals, y, ws), "sign_ok": SC.sign_correct(vals, y, ws),
                "crps_fair": SC.crps_fair(vals, y, ws), "n_atoms": len(vals)}

    def _score_g(self, probs, br, labels=None, weights=None):
        out = {"brier": SC.brier(probs, br), "log": SC.log_score(probs, br)}
        if labels:
            out["brier_fair"] = SC.brier_fair(labels, br, weights); out["n_atoms"] = len(labels)
        return out

    def _score(self, rec, outcome):
        br, y, tier = outcome["branch"], outcome["chg_pct"], rec["tier"]
        clim = rec["baselines"]["climatology"]
        f = {}
        # G
        if br:
            for name in ("engine", "frozen"):
                src, at = rec[name]["G"], rec[name].get("G_atoms")
                f.setdefault(name, {})["G"] = self._score_g(src, br, at["labels"], at["weights"]) if src and at else (self._score_g(src, br) if src else None)
            f.setdefault("climatology", {})["G"] = self._score_g(clim["G"], br, clim.get("G_labels")) if clim["G"] else None
            for it in rec["items"]:
                f.setdefault(it["id"], {})["G"] = self._score_g(it["G"], br, it.get("G_labels")) if it["G"] else None
            f.setdefault("random_analogs", {})["G"] = self._random_g(rec, br)
        # P
        if y is not None:
            for name, src in (("engine", rec["engine"]["P"]), ("frozen", rec["frozen"]["P"])):
                f.setdefault(name, {})["P"] = self._score_p(src["values"], y, src["weights"]) if src else None
            f.setdefault("climatology", {})["P"] = self._score_p(clim["P"], y) if clim["P"] else None
            f.setdefault("persistence", {})["P"] = self._score_p([0.0], y)
            for it in rec["items"]:
                f.setdefault(it["id"], {})["P"] = self._score_p(it["P"], y) if it["P"] else None
            f.setdefault("random_analogs", {})["P"] = self._random_p(rec, y, tier)
        # M
        truth = outcome["in_big_move"]
        m = {"truth": truth, "engine": rec["engine"]["M"], "frozen": rec["frozen"]["M"], **{it["id"]: it["M"] for it in rec["items"]}}
        # Hedge losses per item (abstaining item charged the climatology loss)
        cg = f.get("climatology", {}).get("G")
        cp = f.get("climatology", {}).get("P")
        items_loss = {"G": None, "P": None}
        if br and cg:
            items_loss["G"] = [min((f[it["id"]]["G"] or cg)["brier"] / self.p["g_scale"], 1.0) for it in rec["items"]]
        if y is not None and cp:
            items_loss["P"] = [min((f[it["id"]]["P"] or cp)["crps"] / self.p["p_scale"], 1.0) for it in rec["items"]]
        return {"run_id": rec["run_id"], "tier": tier, "event_id": rec["event_id"], "date": rec["date"], "type": rec["type"],
                "read_hash": rec["hash"], "sealed_at": rec["sealed_at"], "scored_at": _now(), "burn_in_ok": rec["burn_in_ok"],
                "outcome": outcome, "scores": f, "materiality": m, "items_loss": items_loss}

    def _random_g(self, rec, br):
        b = rec["baselines"]["random_analogs"]
        ids = b["g_pool_ids"]
        if len(ids) < 1:
            return None
        rng = np.random.default_rng(b["seed"])
        vals = []
        for _ in range(b["draws"]):
            pick = rng.choice(len(ids), size=min(b["k"], len(ids)), replace=False)
            outs = [self.c.by_id[ids[i]]["sr_outcome_90"] for i in pick]
            probs = {x: outs.count(x) / len(outs) for x in BRANCHES}
            vals.append(self._score_g(probs, br, outs))
        return {k: float(np.mean([v[k] for v in vals])) for k in vals[0]}

    def _random_p(self, rec, y, tier):
        b = rec["baselines"]["random_analogs"]
        ids = b["p_pool_ids"]
        if len(ids) < 1:
            return None
        rng = np.random.default_rng(b["seed"] + 1)
        H = rec["horizon"]
        vals = []
        for _ in range(b["draws"]):
            pick = rng.choice(len(ids), size=min(b["k"], len(ids)), replace=False)
            xs = [self.c.outcome(ids[i], H, tier)["chg_pct"] for i in pick]
            vals.append(self._score_p(xs, y))
        out = {k: float(np.mean([v[k] for v in vals])) for k in ("crps", "pin10", "pin50", "pin90", "pit", "crps_fair")}
        out["sign_ok"] = float(np.mean([1.0 if v["sign_ok"] else 0.0 for v in vals if v["sign_ok"] is not None] or [np.nan]))
        return out


# ============================================================================ phase 2: summary

def _mean_block(scored_dates, cluster_days):
    """Average number of reads per `cluster_days` window -> the stationary-bootstrap mean block / HAC lag."""
    if len(scored_dates) < 2:
        return 1.0
    d = pd.to_datetime(scored_dates).sort_values()
    sizes, i = [], 0
    while i < len(d):
        j = i
        while j + 1 < len(d) and (d[j + 1] - d[i]).days <= cluster_days:
            j += 1
        sizes.append(j - i + 1); i = j + 1
    return float(max(np.mean(sizes), 1.0))


def _series(scores, task, forecaster, key):
    out = []
    for s in scores:
        v = (s["scores"].get(forecaster) or {}).get(task)
        out.append(None if v is None else v.get(key))
    return out


def _paired(scores, task, key, a, b):
    xa, xb, keep = _series(scores, task, a, key), _series(scores, task, b, key), []
    for s, va, vb in zip(scores, xa, xb):
        if va is not None and vb is not None:
            keep.append((s, va, vb))
    return keep


def _skill_block(rows, task, key, engine, ref, mean_block, n_boot, lag):
    """Skill = 1 - mean(engine)/mean(ref) with a stationary-bootstrap CI and a DM/HLN p-value."""
    if len(rows) < 3:
        return {"n": len(rows), "skill": None}
    ea = np.array([r[1] for r in rows]); rb = np.array([r[2] for r in rows])
    def stat(idx):
        m_ref = rb[idx].mean()
        return None if m_ref == 0 else 1.0 - ea[idx].mean() / m_ref
    ci = INF.bootstrap_ci(stat, len(rows), n_boot=n_boot, mean_block=mean_block)
    dm = INF.dm_test(ea, rb, h=1, lag=lag)
    return {"n": len(rows), "engine_mean": float(ea.mean()), "ref_mean": float(rb.mean()), "skill": ci["estimate"],
            "ci95": [ci["lo"], ci["hi"]], "dm_hln": dm.get("dm_hln"), "dm_p": dm.get("p_value"), "dm_ok": dm.get("ok", False),
            "ref": ref, "score": key}


def _learning_curve(scores, task, key):
    """Cumulative mean loss over the scored sequence for engine, frozen, climatology (the learning curve)."""
    pts, cum = [], defaultdict(float)
    n = 0
    for s in scores:
        vals = {f: (s["scores"].get(f) or {}).get(task) for f in ("engine", "frozen", "climatology")}
        if any(v is None for v in vals.values()):
            continue
        n += 1
        for f, v in vals.items():
            cum[f] += v[key]
        pts.append({"date": s["date"], "n": n, **{f: round(cum[f] / n, 5) for f in cum},
                    "skill_engine_vs_clim": round(1 - cum["engine"] / cum["climatology"], 5) if cum["climatology"] else None,
                    "skill_frozen_vs_clim": round(1 - cum["frozen"] / cum["climatology"], 5) if cum["climatology"] else None})
    return pts


def _reliability(scores, forecaster, bins, n_boot, mean_block):
    """Per-branch Murphy decomposition and reliability diagram with stationary-bootstrap bands."""
    out = {}
    rows = [(s["scores"][forecaster]["G"], s["outcome"]["branch"], s) for s in scores
            if s["outcome"]["branch"] and (s["scores"].get(forecaster) or {}).get("G")]
    if not rows:
        return out
    reads = [r[2] for r in rows]
    for b in BRANCHES:
        src = "engine" if forecaster == "engine" else forecaster
        probs = np.array([float(((r[2]["_probs"] if "_probs" in r[2] else {}).get(src) or {}).get(b, np.nan)) for r in rows])
        outs = np.array([1.0 if r[1] == b else 0.0 for r in rows])
        keep = np.isfinite(probs)
        if keep.sum() < 3:
            continue
        m = SC.murphy(probs[keep], outs[keep], bins)
        rng = np.random.default_rng(7)
        bands = defaultdict(list)
        pk, ok = probs[keep], outs[keep]
        for _ in range(min(n_boot, 500)):
            idx = INF.stationary_bootstrap(len(pk), mean_block, rng)
            for d in SC.murphy(pk[idx], ok[idx], bins)["diagram"]:
                bands[tuple(d["bin"])].append(d["observed_freq"])
        for d in m["diagram"]:
            v = bands.get(tuple(d["bin"]), [])
            d["band95"] = [round(float(np.percentile(v, 2.5)), 4), round(float(np.percentile(v, 97.5)), 4)] if len(v) >= 20 else None
        out[b] = m
    return out


def _attach_probs(reads, scores):
    """The scorer needs the sealed forecast probabilities for reliability diagrams: attach by hash."""
    by_hash = {r["hash"]: r for r in reads}
    for s in scores:
        r = by_hash.get(s["read_hash"])
        if not r:
            continue
        s["_probs"] = {"engine": r["engine"]["G"], "frozen": r["frozen"]["G"], "climatology": r["baselines"]["climatology"]["G"],
                       **{it["id"]: it["G"] for it in r["items"]}}


def _pit_hist(scores, forecaster, bins):
    p = [v for v in _series(scores, "P", forecaster, "pit") if v is not None]
    if not p:
        return None
    h, _ = np.histogram(p, bins=bins, range=(0, 1))
    return {"n": len(p), "bins": bins, "counts": h.tolist(), "expected_per_bin": round(len(p) / bins, 2),
            "chi2": float(np.sum((h - len(p) / bins) ** 2 / (len(p) / bins)))}


def _materiality(scores, forecaster):
    tp = fp = fn = tn = 0
    for s in scores:
        m = s["materiality"]
        call, truth = m.get(forecaster), m.get("truth")
        if call is None or truth is None:
            continue
        pos = call == "MATERIAL"
        tp += pos and truth; fp += pos and not truth; fn += (not pos) and truth; tn += (not pos) and not truth
    n = tp + fp + fn + tn
    return {"n": n, "tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": round(tp / (tp + fp), 3) if tp + fp else None, "recall": round(tp / (tp + fn), 3) if tp + fn else None,
            "base_rate": round((tp + fn) / n, 3) if n else None}


def summarize_tier(reads, scores, p, tier, n_boot=None, n_spa=None):
    n_boot = n_boot or p["n_boot"]; n_spa = n_spa or p["n_spa_boot"]
    sc = [s for s in scores if s["tier"] == tier and s["burn_in_ok"]]
    all_tier = [s for s in scores if s["tier"] == tier]
    _attach_probs(reads, sc)
    item_ids = [it["id"] for it in reads[0]["items"]] if reads else []
    out = {"tier": tier, "n_reads": len(all_tier), "n_scored_burn_in": len(sc),
           "n_not_scored_burn_in": len(all_tier) - len(sc), "horizon": R.TIERS[tier]["horizon"], "unit": R.TIERS[tier]["unit"],
           "permits_validation": len(sc) >= p["min_tier_n"], "min_tier_n": p["min_tier_n"]}
    dates = [s["date"] for s in sc]
    mb = _mean_block(dates, p["cluster_days"])
    lag = int(round(mb)) - 1
    out["dependence"] = {"cluster_days": p["cluster_days"], "mean_block": round(mb, 2), "hac_lag": max(lag, 0)}
    fam_p, fam_labels = [], []
    for task, key, refs in (("G", "brier", ("climatology", "frozen", "random_analogs")),
                            ("P", "crps", ("climatology", "persistence", "random_analogs", "frozen"))):
        blk = {"score": key, "engine_vs": {}, "per_class": {}, "items_vs_climatology": {}}
        for ref in refs:
            rows = _paired(sc, task, key, "engine", ref)
            blk["engine_vs"][ref] = _skill_block(rows, task, key, "engine", ref, mb, n_boot, max(lag, 0))
            if blk["engine_vs"][ref].get("dm_p") is not None:
                fam_p.append(blk["engine_vs"][ref]["dm_p"]); fam_labels.append(f"{tier}:{task}:engine_vs_{ref}")
        for cls in sorted({s["type"] for s in sc}):
            rows = [r for r in _paired(sc, task, key, "engine", "climatology") if r[0]["type"] == cls]
            blk["per_class"][cls] = _skill_block(rows, task, key, "engine", "climatology", mb, min(n_boot, 500), max(lag, 0))
        for iid in item_ids:
            rows = _paired(sc, task, key, iid, "climatology")
            blk["items_vs_climatology"][iid] = _skill_block(rows, task, key, iid, "climatology", mb, min(n_boot, 500), max(lag, 0))
            if blk["items_vs_climatology"][iid].get("dm_p") is not None:
                fam_p.append(blk["items_vs_climatology"][iid]["dm_p"]); fam_labels.append(f"{tier}:{task}:{iid}_vs_climatology")
        # DIAGNOSTIC, not registered (scoring.py docstring): the same comparison on the size-corrected score.
        # The gap between this block and engine_vs.climatology is the sample-size bias of the registered skill.
        fk = "brier_fair" if task == "G" else "crps_fair"
        blk["diagnostic_fair"] = {"score": fk, "registered": False,
                                  "engine_vs_climatology": _skill_block(_paired(sc, task, fk, "engine", "climatology"), task, fk, "engine", "climatology", mb, min(n_boot, 500), max(lag, 0)),
                                  "frozen_vs_climatology": _skill_block(_paired(sc, task, fk, "frozen", "climatology"), task, fk, "frozen", "climatology", mb, min(n_boot, 500), max(lag, 0)),
                                  "note": "size-corrected (Ferro 2014) scores published beside the registered ones; gates use the registered scores only"}
        # secondary scores
        if task == "G":
            rows = _paired(sc, task, "log", "engine", "climatology")
            blk["log_score_vs_climatology"] = _skill_block(rows, task, "log", "engine", "climatology", mb, min(n_boot, 500), max(lag, 0))
            blk["murphy_engine"] = _reliability(sc, "engine", p["reliability_bins"], n_boot, mb)
            blk["murphy_climatology"] = _reliability(sc, "climatology", p["reliability_bins"], n_boot, mb)
        else:
            for q in ("pin10", "pin50", "pin90"):
                rows = _paired(sc, task, q, "engine", "climatology")
                blk[f"{q}_vs_climatology"] = _skill_block(rows, task, q, "engine", "climatology", mb, min(n_boot, 500), max(lag, 0))
            sg = [v for v in _series(sc, "P", "engine", "sign_ok") if v is not None]
            blk["sign_accuracy_engine"] = {"n": len(sg), "rate": round(float(np.mean(sg)), 3) if sg else None}
            blk["pit_engine"] = _pit_hist(sc, "engine", p["pit_bins"])
            blk["pit_climatology"] = _pit_hist(sc, "climatology", p["pit_bins"])
        # Reality Check / SPA over the family {items, engine, frozen} vs climatology
        cols, names = [], []
        base = _series(sc, task, "climatology", key)
        for name in item_ids + ["engine", "frozen"]:
            v = _series(sc, task, name, key)
            cols.append(v); names.append(name)
        keep = [i for i in range(len(sc)) if base[i] is not None and all(c[i] is not None for c in cols)]
        if len(keep) >= 10:
            d = np.array([[base[i] - c[i] for c in cols] for i in keep])
            spa = INF.spa(d, n_boot=n_spa, mean_block=mb)
            spa["best_model"] = names[spa["best_model"]]; spa["models"] = names
            blk["spa"] = spa
        else:
            blk["spa"] = {"note": f"only {len(keep)} complete rows; SPA needs >= 10"}
        blk["learning_curve"] = _learning_curve(sc, task, key)
        out[task] = blk
    out["M"] = {"engine": _materiality(sc, "engine"), "frozen": _materiality(sc, "frozen"),
                **{iid: _materiality(sc, iid) for iid in item_ids}}
    out["family_p"] = {"labels": fam_labels, "p": fam_p}
    out["power"] = {}
    for task, key in (("G", "brier"), ("P", "crps")):
        rows = _paired(sc, task, key, "engine", "climatology")
        if len(rows) >= 5:
            d = np.array([r[1] - r[2] for r in rows])
            pw = INF.power_mds(float(d.std(ddof=1)), len(rows), lag=max(lag, 0))
            ref_mean = float(np.mean([r[2] for r in rows]))
            pw["mds_as_skill"] = round(pw["mds"] / ref_mean, 4) if pw.get("mds") and ref_mean else None
            out["power"][task] = pw
    for s in sc:
        s.pop("_probs", None)
    return out


# ============================================================================ phase 3: the tests of the test

def permutation_test(reads, scores, p, n_perm=None, seed=19900802):
    """Label permutation (§6): outcome branches shuffled within class, n_perm times; the engine's G
    skill vs climatology is recomputed from the SEALED analog ids (retrieval is label-free), Hedge
    weights replayed from the permuted losses with the same closed-by-t rule. Joint over tiers."""
    n_perm = n_perm or p["n_perm"]
    geo = [(r, s) for r, s in zip(reads, scores) if r["type"] in GEO and s["outcome"]["branch"] and s["burn_in_ok"]]
    if len(geo) < 10:
        return {"note": f"only {len(geo)} scored geopolitical reads; permutation not run"}
    ids = sorted({r["event_id"] for r, _ in geo} | {a[0] for r, _ in geo for it in r["items"] for a in it["ranked"]}
                 | {i for r, _ in geo for i in r["baselines"]["random_analogs"]["g_pool_ids"]})
    pos = {e: i for i, e in enumerate(ids)}
    labels, cls = {}, {}
    by_id = {}
    for r, s in geo:
        by_id[r["event_id"]] = (r, s)
    # labels for every id we touch: from the scored reads' outcomes or from the corpus rows carried in reads
    lab = np.full(len(ids), -1)
    for r, s in geo:
        lab[pos[r["event_id"]]] = BRANCHES.index(s["outcome"]["branch"])
    # analog labels come from the corpus: the reads carry each analog's id; fetch its label via the scores of that id
    # (every analog with g_closed was itself a corpus event with a branch label)
    known = {s["event_id"]: s["outcome"]["branch"] for s in scores if s["outcome"]["branch"]}
    for e, i in pos.items():
        if lab[i] < 0 and e in known:
            lab[i] = BRANCHES.index(known[e])
    class_of = {r["event_id"]: r["type"] for r, _ in geo}
    for s in scores:
        class_of.setdefault(s["event_id"], s["type"])
    N = len(reads[0]["items"]); K = p["k_max"]
    T = len(geo)
    A = np.full((T, N, K), -1)
    for t, (r, _) in enumerate(geo):
        for m, it in enumerate(r["items"]):
            for j, a in enumerate([a for a in it["ranked"] if a[2]][: it["k"]]):
                A[t, m, j] = pos[a[0]]
    pool = np.zeros((T, len(ids)), bool)
    for t, (r, _) in enumerate(geo):
        for e in r["baselines"]["random_analogs"]["g_pool_ids"]:
            if e in pos:
                pool[t, pos[e]] = True
    tgt = np.array([pos[r["event_id"]] for r, _ in geo])
    dates = np.array([r["date"] for r, _ in geo]); tiers = np.array([r["tier"] for r, _ in geo])
    closes = np.array([s["outcome"]["g_closed_on"] for _, s in geo])
    C = np.zeros((T, T), bool)                        # C[t, u]: read u's outcome had closed by read t's date, same tier
    for t in range(T):
        C[t] = (closes <= dates[t]) & (tiers == tiers[t]) & (np.arange(T) != t)
    eta, gs = p["eta"], p["g_scale"]
    valid_lab = lab >= 0
    groups = defaultdict(list)
    for e, i in pos.items():
        if valid_lab[i]:
            groups[class_of.get(e, "?")].append(i)

    def skill_for(labv):
        onehot = np.zeros((len(ids), 4)); ok = labv >= 0
        onehot[np.where(ok)[0], labv[ok]] = 1.0
        Am = A >= 0
        F = onehot[np.where(Am, A, 0)] * Am[..., None]                       # T x N x K x 4
        cnt = Am.sum(axis=2)                                                 # T x N
        item_f = np.divide(F.sum(axis=2), np.maximum(cnt, 1)[..., None])     # T x N x 4
        has = cnt > 0
        clim = pool.astype(float) @ onehot
        clim = clim / np.maximum(clim.sum(axis=1, keepdims=True), 1e-12)
        y = onehot[tgt]                                                      # T x 4
        item_brier = ((item_f - y[:, None, :]) ** 2).sum(axis=2)             # T x N
        clim_brier = ((clim - y) ** 2).sum(axis=1)                           # T
        item_loss = np.where(has, item_brier, clim_brier[:, None]) / gs
        cum = C.astype(float) @ item_loss                                    # T x N cumulative past closed losses
        w = np.exp(-eta * (cum - cum.min(axis=1, keepdims=True))); w /= w.sum(axis=1, keepdims=True)
        w = w * has
        z = w.sum(axis=1, keepdims=True)
        eng = np.where(z > 0, (w[..., None] * item_f).sum(axis=1) / np.maximum(z, 1e-12), clim)
        eng_brier = ((eng - y) ** 2).sum(axis=1)
        return 1.0 - eng_brier.mean() / clim_brier.mean(), eng_brier.mean(), clim_brier.mean()

    obs, ob_e, ob_c = skill_for(lab)
    rng = np.random.default_rng(seed)
    null = []
    for _ in range(n_perm):
        lp = lab.copy()
        for cls_, idxs in groups.items():
            idxs = np.array(idxs)
            lp[idxs] = lab[idxs][rng.permutation(len(idxs))]
        null.append(skill_for(lp)[0])
    null = np.array(null)
    return {"n_reads": T, "n_perm": n_perm, "observed_skill": float(obs), "engine_brier": float(ob_e), "climatology_brier": float(ob_c),
            "null_mean": float(null.mean()), "null_sd": float(null.std()), "null_p95": float(np.percentile(null, 95)),
            "p_value": INF.permutation_p(obs, null),
            "note": "recomputed from sealed analog ids with labels shuffled within class; Hedge replayed with the closed-by-t rule"}


def regime_blocks(reads, scores, p, n_boot=300):
    out = {}
    for blocks in ([b] for b in p["regime_blocks"]):
        key = "drop_" + "_".join(str(b) for b in blocks)
        keep = [s for s in scores if int(s["date"][:4]) not in blocks]
        out[key] = {}
        for tier in TIER_ORDER:
            sc = [s for s in keep if s["tier"] == tier and s["burn_in_ok"]]
            mb = _mean_block([s["date"] for s in sc], p["cluster_days"]); lag = max(int(round(mb)) - 1, 0)
            out[key][tier] = {task: _skill_block(_paired(sc, task, k_, "engine", "climatology"), task, k_, "engine", "climatology", mb, n_boot, lag)
                              for task, k_ in (("G", "brier"), ("P", "crps"))}
            out[key][tier]["n_dropped"] = sum(1 for s in scores if s["tier"] == tier and int(s["date"][:4]) in blocks)
    return out


def spec_curve(corpus, reads, scores, p):
    """Every registered threshold varied across its pre-declared range (§6). Recomputed from the SEALED
    analog ids (no new retrieval): burn-in x k x horizon (daily P) x cluster-days (inference only), plus the
    Big Moves quantile for materiality. Skill of the Hedge engine vs climatology, published as a distribution."""
    spec = p["spec"]
    by_hash = {r["hash"]: r for r in reads}
    rows = []
    for tier in TIER_ORDER:
        sc = [s for s in scores if s["tier"] == tier]
        rd = [by_hash[s["read_hash"]] for s in sc]
        horizons = spec["horizon_daily"] if tier == "daily" else [R.TIERS[tier]["horizon"]]
        for burn in spec["burn_in"]:
            for k in spec["k"]:
                for H in horizons:
                    for cd in spec["cluster_days"]:
                        res = _replay(corpus, rd, sc, tier, burn, k, H, cd, p)
                        for task in ("G", "P"):
                            if res.get(task):
                                rows.append({"tier": tier, "task": task, "burn_in": burn, "k": k, "horizon": H, "cluster_days": cd, **res[task]})
    # materiality vs the Big Moves quantile
    mat = []
    try:
        import big_moves as BM
        for q in spec["big_move_q"]:
            old = BM.TOP_Q; BM.TOP_Q = q
            try:
                for tier in TIER_ORDER:
                    if tier not in corpus.prices:
                        continue
                    eps = BM.episodes_for(corpus.prices[tier], "price", tier)
                    before = R.TIERS[tier]["before_days"]
                    win = [(pd.Timestamp(m["onset"]) - pd.Timedelta(days=before), pd.Timestamp(m["end"])) for m in eps]
                    tp = fp = fn = tn = 0
                    for s in scores:
                        if s["tier"] != tier or not s["burn_in_ok"] or s["materiality"].get("engine") is None:
                            continue
                        d = pd.Timestamp(s["date"]); truth = any(a <= d <= b for a, b in win); call = s["materiality"]["engine"] == "MATERIAL"
                        tp += call and truth; fp += call and not truth; fn += (not call) and truth; tn += (not call) and not truth
                    mat.append({"tier": tier, "top_q": q, "n_episodes": len(eps), "precision": round(tp / (tp + fp), 3) if tp + fp else None,
                                "recall": round(tp / (tp + fn), 3) if tp + fn else None, "n": tp + fp + fn + tn})
            finally:
                BM.TOP_Q = old
    except Exception as ex:                          # big_moves needs the DB series; synthetic corpora may lack them
        mat.append({"note": f"materiality spec not run: {ex}"})
    sk = [r["skill"] for r in rows if r.get("skill") is not None]
    return {"n_specs": len(rows), "rows": rows, "materiality": mat,
            "skill_distribution": {"min": float(min(sk)), "p25": float(np.percentile(sk, 25)), "median": float(np.median(sk)),
                                   "p75": float(np.percentile(sk, 75)), "max": float(max(sk)),
                                   "share_positive": float(np.mean([s > 0 for s in sk]))} if sk else None}


def _replay(corpus, reads, scores, tier, burn, k, H, cluster_days, p):
    """Replay engine-vs-climatology from sealed analog ids under one specification."""
    N = len(reads[0]["items"]) if reads else 0
    hedge = {"G": LN.Hedge(N, p["eta"]), "P": LN.Hedge(N, p["eta"])}
    pending = []
    G_rows, P_rows, dates = [], [], []
    for r, s in zip(reads, scores):
        t = r["date"]
        still = []
        for close, task, losses in pending:
            (hedge[task].update(losses) if close <= t else still.append((close, task, losses)))
        pending = still
        n_pool = r["n_pool_g"] if r["type"] in GEO else r["n_pool_p"]
        if n_pool < burn:
            continue
        br, y = s["outcome"]["branch"], None
        oc = corpus.outcome(r["event_id"], H, tier) if r["event_id"] in corpus.by_id else None
        y = oc["chg_pct"] if oc else None
        # per-item forecasts at k and H from the sealed ranked ids
        gI, pI = [], []
        for it in r["items"]:
            g_ids = [a[0] for a in it["ranked"] if a[2]][:k]
            p_ids = [a[0] for a in it["ranked"] if a[3]][:k]
            outs = [corpus.by_id[i]["sr_outcome_90"] for i in g_ids if i in corpus.by_id]
            gI.append({b: outs.count(b) / len(outs) for b in BRANCHES} if outs else None)
            vals = [corpus.outcome(i, H, tier)["chg_pct"] for i in p_ids if corpus.outcome(i, H, tier)]
            pI.append(vals or None)
        cg, cp = r["baselines"]["climatology"]["G"], None
        p_pool = r["baselines"]["random_analogs"]["p_pool_ids"]
        cpv = [corpus.outcome(i, H, tier)["chg_pct"] for i in p_pool if corpus.outcome(i, H, tier)]
        cp = cpv or None
        if br and cg and any(gI):
            wG = hedge["G"].weights()
            eng = SC.mixture_g(gI, wG)
            eb, cb = SC.brier(eng, br), SC.brier(cg, br)
            G_rows.append((eb, cb)); dates.append(t)
            pending.append((s["outcome"]["g_closed_on"], "G", [min((SC.brier(g, br) if g else cb) / p["g_scale"], 1.0) for g in gI]))
        if y is not None and cp and any(pI):
            wP = hedge["P"].weights()
            vals, ws = SC.mixture_p(pI, wP)
            ec, cc = SC.crps(vals, y, ws), SC.crps(cp, y)
            P_rows.append((ec, cc))
            pending.append((oc["closed_on"], "P", [min((SC.crps(v, y) if v else cc) / p["p_scale"], 1.0) for v in pI]))
    out = {}
    for task, rows in (("G", G_rows), ("P", P_rows)):
        if len(rows) >= 3:
            e = np.array([x[0] for x in rows]); c = np.array([x[1] for x in rows])
            mb = _mean_block(dates if task == "G" else [s["date"] for s in scores][: len(rows)], cluster_days)
            dm = INF.dm_test(e, c, h=1, lag=max(int(round(mb)) - 1, 0))
            out[task] = {"n": len(rows), "skill": float(1 - e.mean() / c.mean()) if c.mean() else None, "dm_p": dm.get("p_value")}
    return out


def placebo(corpus, menu, reads, scores, p, reps=None, seed=19900802):
    """VIX-matched pseudo-events (§6): for each scored daily read, a non-event date in the same VIX decile,
    >= 30 days from any corpus event; the same coded situation fields at that date; the frozen (uniform)
    mixture of the menu read as of the pseudo-date; engine P-skill vs climatology must be ~0."""
    reps = reps or p["placebo_reps"]
    k_rand, draws = menu["items"][0]["k"], p["random_draws"]
    daily = [s for s in scores if s["tier"] == "daily" and s["burn_in_ok"] and (s["scores"].get("engine") or {}).get("P")]
    if not daily or "daily" not in corpus.prices:
        return {"note": "no daily scored reads; placebo not run"}
    vix = corpus.info._s.get("vix_pct")
    if vix is None:
        return {"note": "no VIX percentile series; placebo not run"}
    vidx, vval = vix[0], vix[1]
    ev_dates = pd.to_datetime([e["event_date"] for e in corpus.events]).sort_values().to_numpy()
    s_daily = corpus.prices["daily"]
    H = R.TIERS["daily"]["horizon"]
    cand = []
    for i, d in enumerate(s_daily.index):
        if i + H >= len(s_daily):
            break
        gap = np.min(np.abs((ev_dates - np.datetime64(d)).astype("timedelta64[D]").astype(int)))
        if gap < p["placebo_excl_days"]:
            continue
        j = np.searchsorted(vidx, np.datetime64(d)) - 1
        if j < 0:
            continue
        cand.append((d, int(min(9, max(0, vval[j] // 10)))))
    by_dec = defaultdict(list)
    for d, dec in cand:
        by_dec[dec].append(d)
    rng = np.random.default_rng(seed)
    uniform = np.full(len(menu["items"]), 1.0 / len(menu["items"]))
    rows = []
    for rep in range(reps):
        for s in daily:
            e = corpus.by_id[s["event_id"]]
            j = np.searchsorted(vidx, np.datetime64(pd.Timestamp(e["event_date"]))) - 1
            if j < 0:
                continue
            dec = int(min(9, max(0, vval[j] // 10)))
            pool_dates = by_dec.get(dec) or []
            if not pool_dates:
                continue
            pd_ = pool_dates[int(rng.integers(0, len(pool_dates)))]
            pseudo = {k_: v for k_, v in e.items() if k_.startswith("sr_") or k_ in ("type", "title")}
            pseudo |= {"event_id": f"placebo:{e['event_id']}:{rep}", "event_date": str(pd_.date())}
            vals_items, ids_items = [], []
            for m in menu["items"]:
                r = R.read(corpus, pseudo, weighting=m, with_propagation=False, with_differencing=False)
                ok = not r["no_adequate_precedent"] and r["P"]["n"]
                vals_items.append(r["P"]["values"] if ok else None); ids_items.append(r["P"]["analog_ids"] if ok else None)
            tgt = S.state_vector(pseudo, info=corpus.info) | {"tier": "daily"}
            pool = [c for c in corpus.pool(tgt, pseudo["event_date"]) if c["p_closed"]]
            if len(pool) < p["burn_in"] or not any(vals_items):
                continue
            clim = [corpus.outcome(c["event_id"], H, "daily")["chg_pct"] for c in pool]
            pos = int(s_daily.index.searchsorted(pd_))
            y = float((s_daily.iloc[pos + H] / s_daily.iloc[pos] - 1) * 100)
            vals, ws, _ids = SC.mixture_p(vals_items, uniform, ids_items)
            # baseline 3 at the pseudo-date: k random analogs from the same pool, averaged over `draws` (as in the walk)
            rand = float(np.mean([SC.crps([clim[i] for i in rng.choice(len(clim), size=min(k_rand, len(clim)), replace=False)], y)
                                  for _ in range(draws)]))
            rows.append({"rep": rep, "event_id": e["event_id"], "pseudo_date": str(pd_.date()), "vix_decile": dec,
                         "engine_crps": SC.crps(vals, y, ws), "clim_crps": SC.crps(clim, y), "rand_crps": rand,
                         "engine_crps_fair": SC.crps_fair(vals, y, ws), "clim_crps_fair": SC.crps_fair(clim, y)})
    if len(rows) < 10:
        return {"note": f"only {len(rows)} placebo reads; not enough", "n": len(rows), "null_holds": None}

    def block(ek, rk, label):
        e_ = np.array([r[ek] for r in rows]); c_ = np.array([r[rk] for r in rows])
        ci = INF.bootstrap_ci(lambda idx: 1 - e_[idx].mean() / c_[idx].mean(), len(rows), n_boot=min(p["n_boot"], 1000), mean_block=1.0)
        dm = INF.dm_test(e_, c_, h=1, lag=0)
        return {"reference": label, "skill": ci["estimate"], "ci95": [ci["lo"], ci["hi"]], "dm_p": dm.get("p_value"),
                "engine_mean": float(e_.mean()), "ref_mean": float(c_.mean()),
                "covers_zero": bool(ci["lo"] is not None and ci["lo"] <= 0 <= ci["hi"])}
    vs_rand = block("engine_crps", "rand_crps", f"random_analogs, k={k_rand} (registered CRPS; size-matched)")
    vs_clim = block("engine_crps", "clim_crps", "climatology (registered CRPS)")
    fair = block("engine_crps_fair", "clim_crps_fair", "climatology (crps_fair -- diagnostic, not registered)")
    return {"n": len(rows), "reps": reps, "k_random": k_rand, "random_draws": draws,
            "vs_random_analogs": vs_rand, "vs_climatology": vs_clim, "fair_vs_climatology": fair,
            "skill": vs_rand["skill"], "ci95": vs_rand["ci95"], "dm_p": vs_rand["dm_p"], "null_holds": vs_rand["covers_zero"],
            "null_reference": ("random_analogs -- protocol §4 baseline 3, the same k drawn at random from the class: size-matched, so a "
                               "null engine has zero expected skill against it. Against climatology the registered CRPS of a k-atom "
                               "distribution is biased upward by E|X-X'|/(2k) (Ferro 2014), so that skill is negative under the null by "
                               "sample size alone; it is published beside this, not gated on."),
            "note": "frozen (uniform) mixture; situation fields copied from the matched real event; P only (no branch outcome exists at a non-event date)"}


def leakage_test(sealed: Walk, broken: Walk):
    """§1: the walk with the filtration broken must differ from the sealed run, or the result is void."""
    hs = {r["hash"] for r in sealed.reads}; hb = {r["hash"] for r in broken.reads}
    def mean(scores, task, key):
        v = [x for x in _series([s for s in scores if s["burn_in_ok"]], task, "engine", key) if x is not None]
        return float(np.mean(v)) if v else None
    diffs = {}
    for task, key in (("G", "brier"), ("P", "crps")):
        a, b = mean(sealed.scores, task, key), mean(broken.scores, task, key)
        diffs[task] = {"sealed": a, "broken": b, "differs": (a is not None and b is not None and abs(a - b) > 1e-9)}
    # a stricter check: the analog sets themselves differ for some reads
    analog_diff = sum(1 for rs, rb in zip(sealed.reads, broken.reads)
                      if [it["ranked"] for it in rs["items"]] != [it["ranked"] for it in rb["items"]])
    ok = (hs != hb) and any(d["differs"] for d in diffs.values()) and analog_diff > 0
    return {"reads_differ": hs != hb, "scores": diffs, "n_reads_with_different_analogs": analog_diff,
            "asserted": ok, "verdict": "filtration is binding" if ok else "VOID: the filtration changed nothing"}


def big_moves_knew(corpus, reads, scores):
    """'What the engine knew at each Big Move': reads sealed inside each daily Big Moves window."""
    bm = corpus.big_moves.get("daily")
    if not bm:
        return []
    by_hash = {r["hash"]: r for r in reads}
    out = []
    for a, b in bm["windows"]:
        inside = [(by_hash[s["read_hash"]], s) for s in scores if s["tier"] == "daily" and a <= s["date"] <= b]
        out.append({"window": [a, b], "n_reads": len(inside),
                    "reads": [{"event_id": r["event_id"], "date": r["date"], "type": r["type"],
                               "engine_p50": (r["engine"]["P"] or {}).get("p50"), "engine_p10": (r["engine"]["P"] or {}).get("p10"),
                               "engine_p90": (r["engine"]["P"] or {}).get("p90"), "M": r["engine"]["M"],
                               "G_top": (max(r["engine"]["G"], key=r["engine"]["G"].get) if r["engine"]["G"] else None),
                               "realized_chg_pct": s["outcome"]["chg_pct"], "realized_branch": s["outcome"]["branch"]}
                              for r, s in inside]})
    return out


def data_state(corpus):
    """What the corpus carried when the walk ran. The situation record (sr_* columns) is written by
    src/situation_record.py; refresh.py's load_events step used to BLANK it on every re-insert (observed
    2026-09-02 15:25Z; fixed in 9e1537e -- load_events now upserts only the CSV columns). A walk on a
    blanked corpus has no branch labels: G cannot be scored and the situation block is empty. The count
    is published with every summary so the numbers are never read without it."""
    n = len(corpus.events)
    geo = [e for e in corpus.events if e["type"] in GEO]
    coded = sum(1 for e in corpus.events if any(not S.is_unknown(e.get(c)) for c in S.SR_MAP.values()))
    labelled = sum(1 for e in geo if e.get("sr_outcome_90") in BRANCHES)
    out = {"n_events": n, "n_geo": len(geo), "n_with_any_situation_field": coded, "n_geo_with_branch_label": labelled,
           "share_geo_labelled": round(labelled / len(geo), 3) if geo else None,
           "panel_events_with_rows": len(corpus.panel), "codebook_fields": len(corpus.schema_extra)}
    if geo and labelled < 0.5 * len(geo):
        out["warning"] = ("situation record largely absent: G is not scorable and similarity runs on the market block only. "
                          "Re-run src/situation_record.py (writes the events table; Joe's call) and then src/walk.py.")
    return out


def audit_flag():
    """PATH Step 4 records the label audit in data/audits/outcome_audit.json {"kappa": x, "passed": bool}.
    Absent -> False. Never inferred."""
    try:
        j = json.load(open(AUDIT))
        return bool(j.get("passed")), j
    except Exception:
        return False, {"note": f"{AUDIT.relative_to(ROOT)} absent: label audit not recorded (Step 4 pending)"}


def verdict(summary, p):
    """§7 promotion rule for the learning loop (engine) and each conditioner (menu item)."""
    flag, audit = audit_flag()
    tiers = [t for t in TIER_ORDER if summary["tiers"].get(t)]
    permit = [t for t in tiers if summary["tiers"][t]["permits_validation"]]
    out = {"audit_passed": flag, "audit_record": audit, "tiers_permitting_validation": permit, "rules": {}}
    def one(name, task):
        conds = {}
        for t in permit:
            blk = summary["tiers"][t][task]
            row = blk["engine_vs"]["climatology"] if name == "engine" else blk["items_vs_climatology"].get(name, {})
            conds[f"{t}:skill>0"] = bool(row.get("skill") is not None and row["skill"] > 0)
            conds[f"{t}:dm_p<0.05"] = bool(row.get("dm_p") is not None and row["dm_p"] < 0.05)
            spa = blk.get("spa", {})
            conds[f"{t}:spa_p<0.05"] = bool(spa.get("p_spa") is not None and spa["p_spa"] < 0.05)
            for key, rb in summary["regime_blocks"].items():
                r = rb[t][task]
                conds[f"{t}:{key}:skill>0"] = bool(r.get("skill") is not None and r["skill"] > 0) if name == "engine" else None
        if task == "P":
            conds["placebo_null"] = bool(summary["placebo"].get("null_holds"))
        if task == "G":
            conds["permutation_p<0.05"] = bool(summary["permutation"].get("p_value") is not None and summary["permutation"]["p_value"] < 0.05)
        conds["label_audit_passed"] = flag if task == "G" else None
        conds["data_permit_any_tier"] = bool(permit)
        checks = [v for v in conds.values() if v is not None]
        status = "VALIDATED" if (checks and all(checks)) else "SUGGESTIVE"
        if any(("skill>0" in k_) and v is False for k_, v in conds.items() if k_.split(":")[-1] == "skill>0"):
            status = "SUGGESTIVE / null"
        return {"status": status, "conditions": conds}
    for task in ("G", "P"):
        out["rules"][f"engine:{task}"] = one("engine", task)
        for t in permit:
            for iid in summary["tiers"][t][task]["items_vs_climatology"]:
                out["rules"][f"{iid}:{task}"] = one(iid, task)
    for task in ("G", "P"):
        r = out["rules"].get(f"engine:{task}", {})
        out[f"{task}_conditioning"] = f"{r.get('status', 'SUGGESTIVE')} (protocol §7; audit passed: {flag})"
    out["note"] = ("VALIDATED requires: skill > 0 vs climatology in both tiers where data permit, DM p < 0.05 after HLN, "
                   "SPA, all three regime blocks, placebo null, label-permutation p < 0.05 (G), and the Step 4 label audit. "
                   "Everything else is SUGGESTIVE; nulls are published as nulls.")
    return out


# ============================================================================ figures

def figures(summary, out_dir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fd = Path(out_dir) / "figures"; fd.mkdir(parents=True, exist_ok=True)
    made = []
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, task in zip(axes, ("G", "P")):
        for tier, ls in (("daily", "-"), ("monthly", "--")):
            lc = (summary["tiers"].get(tier) or {}).get(task, {}).get("learning_curve") or []
            if not lc:
                continue
            x = [pt["n"] for pt in lc]
            ax.plot(x, [pt["skill_engine_vs_clim"] for pt in lc], ls, label=f"{tier}: engine (Hedge) vs climatology")
            ax.plot(x, [pt["skill_frozen_vs_clim"] for pt in lc], ls, alpha=0.5, label=f"{tier}: frozen vs climatology")
        ax.axhline(0, color="k", lw=0.5); ax.set_title(f"Learning curve -- {task} ({'Brier' if task == 'G' else 'CRPS'} skill, cumulative)")
        ax.set_xlabel("scored reads, in order"); ax.set_ylabel("skill = 1 - S_engine/S_clim"); ax.legend(fontsize=7)
    fig.tight_layout(); fig.savefig(fd / "learning_curve.png", dpi=120); plt.close(fig); made.append("learning_curve.png")
    for tier in TIER_ORDER:
        blk = (summary["tiers"].get(tier) or {}).get("G", {}).get("murphy_engine") or {}
        if blk:
            fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))
            for ax, b in zip(axes, BRANCHES):
                m = blk.get(b)
                ax.plot([0, 1], [0, 1], "k--", lw=0.5)
                if m:
                    xs = [d["forecast_mean"] for d in m["diagram"]]; ys = [d["observed_freq"] for d in m["diagram"]]
                    ax.plot(xs, ys, "o-")
                    for d in m["diagram"]:
                        if d.get("band95"):
                            ax.plot([d["forecast_mean"]] * 2, d["band95"], color="gray", lw=1)
                    ax.set_title(f"{b}\nrel {m['reliability']:.3f} res {m['resolution']:.3f} n={m['n']}", fontsize=8)
                ax.set_xlim(0, 1); ax.set_ylim(0, 1)
            fig.suptitle(f"Reliability -- engine, {tier} tier (bars: stationary-bootstrap 95% band)")
            fig.tight_layout(); fig.savefig(fd / f"reliability_{tier}.png", dpi=120); plt.close(fig); made.append(f"reliability_{tier}.png")
        pit = (summary["tiers"].get(tier) or {}).get("P", {}).get("pit_engine")
        if pit:
            fig, ax = plt.subplots(figsize=(5, 3.5))
            ax.bar(np.arange(pit["bins"]) / pit["bins"], pit["counts"], width=1 / pit["bins"], align="edge")
            ax.axhline(pit["expected_per_bin"], color="k", lw=0.8)
            ax.set_title(f"PIT histogram -- engine, {tier} (n={pit['n']}, chi2={pit['chi2']:.1f})", fontsize=9)
            fig.tight_layout(); fig.savefig(fd / f"pit_{tier}.png", dpi=120); plt.close(fig); made.append(f"pit_{tier}.png")
    sc = summary.get("spec_curve", {}).get("rows") or []
    if sc:
        fig, ax = plt.subplots(figsize=(10, 3.5))
        for task, col in (("G", "C0"), ("P", "C1")):
            vals = sorted(r["skill"] for r in sc if r["task"] == task and r.get("skill") is not None and r["tier"] == "daily")
            if vals:
                ax.plot(range(len(vals)), vals, ".", color=col, label=f"{task} (daily), {len(vals)} specs")
        ax.axhline(0, color="k", lw=0.5); ax.set_xlabel("specification (sorted)"); ax.set_ylabel("skill vs climatology")
        ax.set_title("Specification curve -- engine skill across every registered threshold"); ax.legend(fontsize=8)
        fig.tight_layout(); fig.savefig(fd / "spec_curve.png", dpi=120); plt.close(fig); made.append("spec_curve.png")
    return made


# ============================================================================ the whole thing

def run(corpus=None, menu=None, out_dir=WF, params=None, fast=False, quiet=False, with_figures=True):
    if corpus is None:
        from _db import connect
        corpus = R.Corpus.from_db(connect(read_only=True))
    menu = menu or S.load_menu()
    p = dict(REGISTERED) | (FAST if fast else {}) | (params or {})
    out_dir = Path(out_dir)
    t0 = time.time()
    w = Walk(corpus, menu, out_dir=out_dir, params=p, quiet=quiet).run_reads()
    if not quiet:
        print(f"reads: {len(w.reads)} sealed, {time.time() - t0:.0f}s")
    summary = {"protocol": p["protocol"], "run_id": w.run_id, "generated_at": _now(), "registered": {k: v for k, v in p.items() if k != "protocol"},
               "menu": [m["id"] for m in menu["items"]], "tiers": {}}
    for tier in TIER_ORDER:
        if any(r["tier"] == tier for r in w.reads):
            summary["tiers"][tier] = summarize_tier(w.reads, w.scores, p, tier)
    # G jointly across tiers (the geopolitical branch model only)
    geo = [s for s in w.scores if s["burn_in_ok"] and s["outcome"]["branch"]]
    if geo:
        mb = _mean_block([s["date"] for s in geo], p["cluster_days"])
        summary["G_joint_across_tiers"] = _skill_block(_paired(geo, "G", "brier", "engine", "climatology"), "G", "brier", "engine", "climatology",
                                                       mb, p["n_boot"], max(int(round(mb)) - 1, 0))
    fam_p, fam_l = [], []
    for t in summary["tiers"].values():
        fam_p += t["family_p"]["p"]; fam_l += t["family_p"]["labels"]
    bh = INF.bh_fdr(fam_p, q=0.05)
    summary["fdr"] = {"q": 0.05, "family": [{"comparison": l, "p": round(pv, 5), "q_value": round(qv, 5), "survives": s_}
                                            for l, pv, qv, s_ in zip(fam_l, fam_p, bh["qvalues"], bh["survive"])]}
    summary["permutation"] = permutation_test(w.reads, w.scores, p)
    summary["regime_blocks"] = regime_blocks(w.reads, w.scores, p)
    summary["spec_curve"] = spec_curve(corpus, w.reads, w.scores, p)
    summary["placebo"] = placebo(corpus, menu, w.reads, w.scores, p)
    if not quiet:
        print(f"inference done, {time.time() - t0:.0f}s; leakage run...")
    import tempfile
    b = Walk(corpus, menu, out_dir=tempfile.mkdtemp(prefix="walk_leakage_"), params=p, break_filtration=True, quiet=True).run_reads()
    summary["leakage_test"] = leakage_test(w, b)
    summary["big_moves_knew"] = big_moves_knew(corpus, w.reads, w.scores)
    summary["verdict"] = verdict(summary, p)
    summary["limits"] = ["outcome labels corpus-derived until the Step 4 audit passes (audit flag in verdict)",
                         "situation fields not vintage-stamped: sr_* fields taken as coded (protocol §1 LIMITATION); state-panel fields, when present, are vintage-filtered",
                         "monthly tier n is small: describes, does not validate (§9)",
                         "flow side of P is a price proxy until 2026 (§9)",
                         "Big Moves windows use the registered full-history top-5% threshold (BIG_MOVES_REGISTRATION), not a point-in-time one",
                         "the registered skill vs climatology carries a SAMPLE-SIZE bias against a k-atom analog distribution (CRPS: +E|X-X'|/(2k); "
                         "Brier: +sum_b p_b(1-p_b)/k), so a null engine reads as negative skill vs climatology; the size-corrected scores "
                         "(Ferro 2014) are published in every tier's diagnostic_fair block and are NOT registered -- gates use §3's scores unchanged; "
                         "whether to amend §3 is Joe's call",
                         "the placebo null (§6) is judged against the size-matched random-analog reference (§4 baseline 3); the climatology-referenced "
                         "placebo skill and the size-corrected one are published beside it",
                         "Hedge losses use the registered scores, so within the menu the k=5 item is handicapped against k=12 by sample size alone",
                         "this summary.json replaces the PRE_REGISTRATION_V2 src/walk_forward.py summary at the same path; the ledger, story and "
                         "terminal readers of the old 'windows' shape show an empty engine board until PATH Step 9 rewires them"]
    summary["data_state"] = data_state(corpus)
    summary["seal_check"] = dict(zip(("ok", "n_records", "first_bad_line"), verify_file(out_dir / "reads.jsonl")))
    if with_figures:
        summary["figures"] = figures(summary, out_dir)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1, default=str))
    (out_dir / "big_moves_knew.json").write_text(json.dumps(summary["big_moves_knew"], indent=1, default=str))
    if not quiet:
        print(f"summary.json written ({time.time() - t0:.0f}s)")
    return summary, w


def _print(summary):
    for tier, t in summary["tiers"].items():
        print(f"\n=== {tier}: {t['n_scored_burn_in']} scored of {t['n_reads']} reads; permits validation: {t['permits_validation']}")
        for task in ("G", "P"):
            for ref, r in t[task]["engine_vs"].items():
                if r.get("skill") is not None:
                    print(f"  {task} engine vs {ref:<15} skill {r['skill']:+.4f}  CI {r['ci95'][0]:+.3f}..{r['ci95'][1]:+.3f}  DM/HLN p={r['dm_p']:.3f}  n={r['n']}")
            spa = t[task].get("spa", {})
            if "p_spa" in spa:
                print(f"  {task} SPA p={spa['p_spa']:.3f} (RC p={spa['p_rc']:.3f}), best={spa['best_model']}")
            fr = t[task].get("diagnostic_fair", {}).get("engine_vs_climatology", {})
            if fr.get("skill") is not None:
                print(f"  {task} [diagnostic, not registered] size-corrected engine vs climatology skill {fr['skill']:+.4f}  CI {fr['ci95'][0]:+.3f}..{fr['ci95'][1]:+.3f}  DM/HLN p={fr['dm_p']:.3f}")
        m = t["M"]["engine"]; print(f"  M engine precision {m['precision']} recall {m['recall']} n={m['n']} base {m['base_rate']}")
    pm = summary["permutation"]; print(f"\npermutation (G): skill {pm.get('observed_skill')} p={pm.get('p_value')}")
    pl = summary["placebo"]
    print(f"placebo (P) vs random analogs (size-matched): skill {pl.get('skill')} CI {pl.get('ci95')} null_holds={pl.get('null_holds')}")
    for k_ in ("vs_climatology", "fair_vs_climatology"):
        if pl.get(k_):
            print(f"placebo (P) {k_}: skill {pl[k_]['skill']:+.4f} CI {pl[k_]['ci95'][0]:+.3f}..{pl[k_]['ci95'][1]:+.3f}")
    print(f"leakage: {summary['leakage_test']['verdict']}")
    sc = summary["spec_curve"].get("skill_distribution"); print(f"spec curve: {sc}")
    print("\nverdict:")
    for k, v in summary["verdict"]["rules"].items():
        if k.startswith("engine"):
            print(f"  {k}: {v['status']}")
    print(f"  audit passed: {summary['verdict']['audit_passed']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true")
    a = ap.parse_args()
    s, _ = run(fast=a.fast)
    _print(s)
