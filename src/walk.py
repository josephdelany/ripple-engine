"""
walk.py -- PATH Step 8 / BUILD_V3 S6: the walk, per WALK_FORWARD_PROTOCOL.md (registered 2026-09-02).

Stand at each corpus event in order, read, SEAL the read, only then look up the outcome, score it,
and let the engine learn -- but only from outcomes that had closed by the next read. Then ask
whether the skill is real: DM/HLN against four baselines, stationary block bootstrap, Reality Check
/ SPA over the family, BH-FDR, VIX-matched placebo, label permutation, regime-block leave-out,
specification curve, simulation power, and the leakage test (a run with the filtration broken must
differ). Everything is published as computed; VALIDATED is decided by §7 of the protocol including
the Step 4 audit flag, which is false until data/audits/outcome_audit.json records a pass.

G target (OUTCOME_MAPPING.md Amendment 1 + 1.1, 2026-09-02): the IES-90 escalation level reached in (d, d+90]
(ordinal 0 none / 1 threat or display / 2 use of force / 3 war) from independent dated sources, plus the DEAL
flag; event_outcomes source='ies90'. Scored with the multi-category Brier (registered, §3; drives the gates and
Hedge), the log score (§3) and the ranked probability score over the ordinal levels (Joe, 2026-09-02); DEAL with
the binary Brier. sr_outcome_90 is retired: never a target, a feature, or analog evidence. A geopolitical event
with no covering source (no_independent_outcome) is read and P-scored but never G-scored and never G evidence.

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
from engine import persistence as PS    # noqa: E402
from engine import recalibrate as RC    # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WF = ROOT / "data" / "walk_forward"
AUDIT = ROOT / "data" / "audits" / "outcome_audit.json"
LEVELS = SC.LEVELS
LEVEL_MEANING = R.LEVEL_MEANING
GEO = set(R.GEO_TYPES)
TIER_ORDER = ("monthly", "daily")

REGISTERED = {
    "protocol": "WALK_FORWARD_PROTOCOL.md (2026-09-02)",
    "g_target": "IES-90 level in (d, d+90] + DEAL flag (OUTCOME_MAPPING.md Amendment 1 and later amendments; event_outcomes source='ies90'; "
                "the label registration the run saw is recorded in data_state.ies90_registration); sr_outcome_90 retired",
    "g_scores": {"gate_and_hedge": "brier (multi-category, §3)", "also": ["log (§3)", "rps (ranked probability score over the ordinal levels; Joe 2026-09-02)"],
                 "deal": "binary brier"},
    "g_baselines": ["climatology", "frozen", "random_analogs", "persistence"],   # §4 + Amendment B (G-persistence: the dyad's IES level over [t-90, t-1], 0.9/0.1 smoothed; fallback climatology, counted)
    "menu_cap": "12 weightings + the recalibrated item M13 (Amendment C)",
    "seeds": {"bootstrap_and_spa": 19900802, "permutation": 19900802, "placebo": 19900802, "reliability_bands": 7, "power": 19900802,
              "random_analogs": "int(sha256(event_id)[:8], 16) (+1 for P)"},                       # Amendment I
    "release_lags_days": dict(S.RELEASE_LAGS),                                                    # Amendment G
    "permutation_rule": "block permutation over the registered 35-day clusters decides §7 (Amendment F.2); the §6 i.i.d. within-class permutation is published beside it",
    "situation_fields": "actor/target/conflict_scope/tempo/asset_role from situation_state knowable_at rows with vintage <= as_of, else unknown (Amendment H); prior_dyad/propensity corpus-derived from dated prior events (H.1)",
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


CONTENT_EXCLUDE = ("hash", "sealed_at", "run_id", "content_hash")          # Amendment I: wall-clock and run identity


def content_view(record):
    """The record without its wall-clock stamps and run identity: what two runs on the same inputs must reproduce."""
    import copy
    v = copy.deepcopy({k: x for k, x in record.items() if k not in CONTENT_EXCLUDE})
    for it in v.get("items", []):
        if isinstance(it.get("recal"), dict):
            it["recal"].pop("fit_max_looked_up_at", None)
    return v


def content_hash(record):
    return hashlib.sha256(_canon(content_view(record)).encode()).hexdigest()


def content_digest(reads):
    """SHA-256 over the ordered content hashes of a run's reads (Amendment I)."""
    return hashlib.sha256("\n".join(r.get("content_hash") or content_hash(r) for r in reads).encode()).hexdigest()


def seal(record):
    """Content hash over the whole record (sealed_at included) -- any later change is detectable.
    content_hash (Amendment I) excludes the wall-clock stamps and the run id so two runs can be compared."""
    record["content_hash"] = content_hash(record)
    record["sealed_at"] = _now()
    record["hash"] = hashlib.sha256(_canon({k: v for k, v in record.items() if k != "hash"}).encode()).hexdigest()
    return record


def verify_seal(record):
    body = {k: v for k, v in record.items() if k != "hash"}
    return hashlib.sha256(_canon(body).encode()).hexdigest() == record.get("hash")


def _open_text(path):
    import gzip
    path = Path(path)
    return gzip.open(path, "rt", encoding="utf-8") if path.suffix == ".gz" else open(path, encoding="utf-8")


def verify_file(path):
    """Every line re-hashes to its own seal (plain or .gz). Returns (ok, n_checked, first_bad_line)."""
    n = 0
    for i, line in enumerate(_open_text(path)):
        if not line.strip():
            continue
        n += 1
        if not verify_seal(json.loads(line)):
            return False, n, i + 1
    return True, n, None


def archive_prior_runs(out_dir, keep_run_id):
    """Amendment D: every run other than `keep_run_id` is MOVED -- never edited, never dropped -- from the three
    sealed logs in the tree to runs/<run_id>/<name>.jsonl.gz (append mode, so a run archived in pieces keeps every
    row). Returns the manifest {run_id: {reads.jsonl: n, ..., reads_seal_ok, reads_records_in_archive}}."""
    import gzip
    out_dir = Path(out_dir)
    manifest = {}
    for name in ("reads.jsonl", "scores.jsonl", "weights.jsonl"):
        f = out_dir / name
        if not f.exists():
            continue
        keep, others = [], defaultdict(list)
        for line in open(f, encoding="utf-8"):
            if not line.strip():
                continue
            rid = json.loads(line).get("run_id")
            (keep if rid == keep_run_id else others[rid]).append(line if line.endswith("\n") else line + "\n")
        for rid, lines in others.items():
            d = out_dir / "runs" / str(rid)
            d.mkdir(parents=True, exist_ok=True)
            with gzip.open(d / (name + ".gz"), "at", encoding="utf-8") as g:
                g.writelines(lines)
            manifest.setdefault(rid, {})[name] = len(lines)
        if others:
            f.write_text("".join(keep), encoding="utf-8")
    for rid, m in manifest.items():
        gz = out_dir / "runs" / str(rid) / "reads.jsonl.gz"
        if gz.exists():
            ok, n, bad = verify_file(gz)
            m["reads_seal_ok"], m["reads_records_in_archive"], m["first_bad_line"] = ok, n, bad
    return manifest


# ============================================================================ the walk

class Walk:
    def __init__(self, corpus, menu, out_dir=WF, run_id=None, params=None, break_filtration=False, quiet=False, break_recal=False):
        self.c = corpus
        self.menu = menu["items"]
        self.base = [m for m in self.menu if m.get("kind") != "recalibrated"]                      # the retrieval weightings (M01-M12)
        self.recal = next((m for m in self.menu if m.get("kind") == "recalibrated"), None)         # Amendment C: M13, last in the menu
        assert self.recal is None or self.menu[-1] is self.recal, "the recalibrated item must be the last menu item"
        self.N = len(self.menu)
        self.break_recal = break_recal                    # Amendment C.6: the recalibrator ignores close dates (leakage test only)
        self.out = Path(out_dir)
        self.out.mkdir(parents=True, exist_ok=True)
        self.p = dict(REGISTERED) | (params or {})
        self.broken = break_filtration
        self.quiet = quiet
        self.run_id = run_id or f"walk_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}" + ("_BROKEN" if break_filtration else "") + ("_RECALBROKEN" if break_recal else "")
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
        hist = []                                               # Amendment C: (g_closed_on, looked_up_at, frozen G, realized level) of this tier's scored reads
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
            for m in self.base:
                r = R.read(self.c, e, weighting=dict(m, k=self.p["k_max"]), with_propagation=False,
                           with_differencing=False, break_filtration=self.broken)
                n_pool = max(n_pool, r["filtration"]["n_pool"])
                if r["no_adequate_precedent"]:
                    items.append({"id": m["id"], "k": m["k"], "no_precedent": True, "ranked": [], "G": None, "D": None, "P": None, "M": None})
                    continue
                top = r["analogs"][: m["k"]]
                g = R.g_distribution(top) if e["type"] in GEO else None
                pdist = R.p_distribution(self.c, top, tier)
                mm = R.m_read(self.c, top, tier)
                g_atoms = [(a["event_id"], a["outcome"], a.get("deal")) for a in top if a.get("g_closed") and a.get("outcome") in LEVELS] if g else []
                items.append({"id": m["id"], "k": m["k"], "no_precedent": False,
                              "ranked": [[a["event_id"], a["similarity"], bool(a["g_closed"]), bool(a["p_closed"])] for a in r["analogs"]],
                              "G": (g["rates"] if g and g["n"] else None), "G_n": (g["n"] if g else 0),
                              "G_ids": [i for i, _, _ in g_atoms], "G_labels": [l for _, l, _ in g_atoms], "G_deals": [d for _, _, d in g_atoms],
                              "D": (g["deal"]["rate"] if g else None), "D_n": (g["deal"]["n"] if g else 0),
                              "P": (pdist["values"] if pdist["n"] else None), "P_ids": pdist.get("analog_ids", []),
                              "M": mm["call"]})
            pool = self.c.pool(self.c.vector(e["event_id"]) | {"tier": tier}, t, break_filtration=self.broken)
            g_pool = [c for c in pool if c["g_closed"]]
            p_pool = [c for c in pool if c["p_closed"]]
            clim_G = clim_D = None
            if e["type"] in GEO and g_pool:
                outs = [c["outcome"] for c in g_pool]
                clim_G = {b: outs.count(b) / len(outs) for b in LEVELS}
                deals = [c["deal"] for c in g_pool if c.get("deal") in (0, 1)]
                clim_D = {"rate": sum(deals) / len(deals), "n": len(deals)} if deals else None
            clim_P = [round(self.c.outcome(c["event_id"], H, tier)["chg_pct"], 3) for c in p_pool] or None
            # Amendment B: G-persistence -- the dyad's level over [t-90, t-1] (engine.persistence), else climatology, counted
            pers = self.c.persistence.get(e["event_id"]) if e["type"] in GEO else None
            if e["type"] in GEO:
                known = bool(pers and pers.get("level_pre") in LEVELS)
                pers_blk = {"P": [0.0], "G": (PS.smooth(pers["level_pre"]) if known else clim_G), "fallback": (not known),
                            "level_pre": (pers or {}).get("level_pre"), "covering_pre": (pers or {}).get("covering_pre", []),
                            "window_pre": (pers or {}).get("window_pre"), "basis_pre": (pers or {}).get("basis_pre")}
            else:
                pers_blk = {"P": [0.0], "G": None, "fallback": None}
            burn_in_ok = len(p_pool if e["type"] not in GEO else g_pool) >= self.p["burn_in"]
            # engine (Hedge mixture) and frozen (uniform mixture)
            nb = len(self.base)
            frozen = self._mix(items, np.full(nb, 1.0 / nb), np.full(nb, 1.0 / nb), tier)     # §4 baseline 4: uniform over M01-M12
            if self.recal is not None:                                                        # Amendment C: M13 from the frozen mixture + closed outcomes
                used = [h for h in hist if (self.break_recal or h[0] <= t)]
                rc = RC.Recalibrator().fit([h[2] for h in used], [h[3] for h in used])
                items.append(self._recal_item(rc, frozen, used))
            eng = self._mix(items, w["G"], w["P"], tier)
            rec = {"run_id": self.run_id, "tier": tier, "event_id": e["event_id"], "date": t, "as_of": t, "type": e["type"],
                   "horizon": H, "unit": R.TIERS[tier]["unit"], "n_pool": len(pool), "n_pool_g": len(g_pool), "n_pool_p": len(p_pool),
                   "burn_in_ok": bool(burn_in_ok), "filtration_broken": self.broken,
                   "weights": {"G": [round(float(x), 6) for x in w["G"]], "P": [round(float(x), 6) for x in w["P"]]},
                   "items": items, "engine": eng, "frozen": frozen,
                   "baselines": {"climatology": {"G": clim_G, "G_labels": [c["outcome"] for c in g_pool] if clim_G else [], "D": clim_D, "P": clim_P},
                                 "persistence": pers_blk,
                                 "random_analogs": {"k": self.menu[0]["k"], "draws": self.p["random_draws"],
                                                    "seed": int(hashlib.sha256(e["event_id"].encode()).hexdigest()[:8], 16),
                                                    "g_pool_ids": [c["event_id"] for c in g_pool], "p_pool_ids": [c["event_id"] for c in p_pool]}},
                   "state_unknown": self.c.vector(e["event_id"])["unknown"],
                   "state_market": {f: v_ for f, v_ in self.c.vector(e["event_id"])["fields"].items() if f in S.MARKET_SERIES or f in S.MOMENTUM},
                   "situation_known_at_t": self.c.vector(e["event_id"]).get("situation_known_at_t", []),
                   "situation_blanked": self.c.vector(e["event_id"]).get("situation_blanked", [])}
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
            if outcome["level"] and e["type"] in GEO and sc["items_loss"]["G"] is not None:
                pending.append((outcome["g_closed_on"], "G", sc["items_loss"]["G"]))
            if outcome["chg_pct"] is not None and sc["items_loss"]["P"] is not None:
                pending.append((outcome["closed_on"], "P", sc["items_loss"]["P"]))
            if self.recal is not None and outcome["level"] and rec["frozen"]["G"]:
                hist.append((outcome["g_closed_on"], outcome["looked_up_at"], rec["frozen"]["G"], outcome["level"]))
            if (i + 1) % 50 == 0:
                self.log(f"  {tier}: {i + 1}/{len(events)} reads ({time.time() - t0:.0f}s)")
        self.log(f"{tier}: {len(events)} reads sealed")

    def _recal_item(self, rc, frozen, used):
        """Amendment C: M13 = the frozen mixture's G through the recalibration map; P and M are the frozen mixture's."""
        fp = frozen.get("P")
        return {"id": self.recal["id"], "kind": "recalibrated", "k": None, "no_precedent": frozen["G"] is None and fp is None, "ranked": [],
                "G": (rc.apply(frozen["G"]) if frozen["G"] else None), "G_n": 0, "G_ids": [], "G_labels": [], "G_deals": [],
                "D": frozen.get("D"), "D_n": 0,
                "P": (fp["values"] if fp else None), "P_w": (fp["weights"] if fp else None), "P_ids": (fp["ids"] if fp else []), "M": frozen.get("M"),
                "recal": rc.state() | {"n_closed_used": len(used), "fit_max_closed_on": max((h[0] for h in used), default=None),
                                       "fit_max_looked_up_at": max((h[1] for h in used), default=None),
                                       "rule": "closed-by-t (g_closed_on <= as_of)" if not self.break_recal else "BROKEN: close dates ignored (leakage test)"}}

    def _mix(self, items, wG, wP, tier):
        G = SC.mixture_g([it["G"] for it in items], wG) if any(it["G"] for it in items) else None
        g_ids, g_labels, g_ws = SC.mixture_atoms([it.get("G_ids") or [] for it in items], [it.get("G_labels") or [] for it in items], wG)
        vals, ws, ids = SC.mixture_p([it["P"] for it in items], wP, [it.get("P_ids") or [] for it in items], atom_weights=[it.get("P_w") for it in items])
        mcalls = [(it["M"], w) for it, w in zip(items, wP) if it["M"]]
        dpairs = [(it["D"], w) for it, w in zip(items, wG) if it.get("D") is not None and w > 0]
        D = (sum(d * w for d, w in dpairs) / sum(w for _, w in dpairs)) if dpairs and sum(w for _, w in dpairs) > 0 else None
        M = None
        if mcalls:
            z = sum(w for _, w in mcalls)
            M = "MATERIAL" if z > 0 and sum(w for m, w in mcalls if m == "MATERIAL") / z >= 0.5 else "NOT_MATERIAL"
        out = {"G": ({b: round(v, 5) for b, v in G.items()} if G else None), "D": (round(D, 5) if D is not None else None), "M": M,
               "G_atoms": ({"ids": g_ids, "labels": g_labels, "weights": [round(x, 6) for x in g_ws]} if G else None),
               "P": ({"values": [round(v, 3) for v in vals], "weights": [round(x, 6) for x in ws], "ids": ids,
                      "p10": round(SC.weighted_quantile(vals, 0.10, ws), 2), "p50": round(SC.weighted_quantile(vals, 0.50, ws), 2),
                      "p90": round(SC.weighted_quantile(vals, 0.90, ws), 2), "n_atoms": len(vals)} if vals else None)}
        return out

    def _outcome(self, e, tier, H):
        o = self.c.outcome(e["event_id"], H, tier)
        lab = self.c.ies90.get(e["event_id"]) if e["type"] in GEO else None       # IES-90: absent -> no_independent_outcome, never guessed
        return {"level": (lab["level"] if lab else None), "level_meaning": (LEVEL_MEANING[lab["level"]] if lab else None),
                "deal": (lab["deal"] if lab else None), "no_independent_outcome": bool(e["type"] in GEO and not lab),
                "chg_pct": (None if o is None else o["chg_pct"]), "closed_on": (None if o is None else o["closed_on"]),
                "g_closed_on": str((pd.Timestamp(e["event_date"]) + pd.Timedelta(days=R.G_HORIZON_DAYS)).date()),
                "in_big_move": self.c.in_big_move(e["event_id"]), "looked_up_at": _now()}

    def _score_p(self, vals, y, ws=None):
        return {"crps": SC.crps(vals, y, ws), "pin10": SC.pinball(vals, y, 0.10, ws), "pin50": SC.pinball(vals, y, 0.50, ws),
                "pin90": SC.pinball(vals, y, 0.90, ws), "pit": SC.pit(vals, y, ws), "sign_ok": SC.sign_correct(vals, y, ws),
                "crps_fair": SC.crps_fair(vals, y, ws), "n_atoms": len(vals)}

    def _score_g(self, probs, lv, labels=None, weights=None):
        out = {"brier": SC.brier(probs, lv), "log": SC.log_score(probs, lv), "rps": SC.rps(probs, lv)}
        if labels:
            out["brier_fair"] = SC.brier_fair(labels, lv, weights); out["rps_fair"] = SC.rps_fair(labels, lv, weights); out["n_atoms"] = len(labels)
        return out

    def _score_d(self, rate, deal):
        return None if rate is None else {"brier": SC.brier_binary(rate, deal)}

    def _score(self, rec, outcome):
        br, y, tier = outcome["level"], outcome["chg_pct"], rec["tier"]
        clim = rec["baselines"]["climatology"]
        f = {}
        # G (IES-90 level) and D (DEAL flag, scored only when the realized flag is known)
        if br:
            for name in ("engine", "frozen"):
                src, at = rec[name]["G"], rec[name].get("G_atoms")
                f.setdefault(name, {})["G"] = self._score_g(src, br, at["labels"], at["weights"]) if src and at else (self._score_g(src, br) if src else None)
            f.setdefault("climatology", {})["G"] = self._score_g(clim["G"], br, clim.get("G_labels")) if clim["G"] else None
            pg = (rec["baselines"].get("persistence") or {}).get("G")
            f.setdefault("persistence", {})["G"] = (self._score_g(pg, br) | {"brier_fair": SC.brier(pg, br), "rps_fair": SC.rps(pg, br), "n_atoms": 1}) if pg else None
            for it in rec["items"]:
                f.setdefault(it["id"], {})["G"] = self._score_g(it["G"], br, it.get("G_labels")) if it["G"] else None
            rg = self._random_g(rec, br, outcome["deal"])
            f.setdefault("random_analogs", {})["G"] = rg.get("G") if rg else None
            if outcome["deal"] in (0, 1):
                for name in ("engine", "frozen"):
                    f.setdefault(name, {})["D"] = self._score_d(rec[name].get("D"), outcome["deal"])
                f.setdefault("climatology", {})["D"] = self._score_d((clim.get("D") or {}).get("rate"), outcome["deal"])
                for it in rec["items"]:
                    f.setdefault(it["id"], {})["D"] = self._score_d(it.get("D"), outcome["deal"])
                f.setdefault("random_analogs", {})["D"] = rg.get("D") if rg else None
        # P
        if y is not None:
            for name, src in (("engine", rec["engine"]["P"]), ("frozen", rec["frozen"]["P"])):
                f.setdefault(name, {})["P"] = self._score_p(src["values"], y, src["weights"]) if src else None
            f.setdefault("climatology", {})["P"] = self._score_p(clim["P"], y) if clim["P"] else None
            f.setdefault("persistence", {})["P"] = self._score_p([0.0], y)
            for it in rec["items"]:
                f.setdefault(it["id"], {})["P"] = self._score_p(it["P"], y, it.get("P_w")) if it["P"] else None
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

    def _random_g(self, rec, br, deal=None):
        b = rec["baselines"]["random_analogs"]
        ids = b["g_pool_ids"]
        if len(ids) < 1:
            return None
        rng = np.random.default_rng(b["seed"])
        vals, dvals = [], []
        for _ in range(b["draws"]):
            pick = rng.choice(len(ids), size=min(b["k"], len(ids)), replace=False)
            outs = [self.c.ies90[ids[i]]["level"] for i in pick]
            probs = {x: outs.count(x) / len(outs) for x in LEVELS}
            vals.append(self._score_g(probs, br, outs))
            deals = [self.c.ies90[ids[i]]["deal"] for i in pick if self.c.ies90[ids[i]]["deal"] in (0, 1)]
            if deal in (0, 1) and deals:
                dvals.append(SC.brier_binary(sum(deals) / len(deals), deal))
        return {"G": {k: float(np.mean([v[k] for v in vals])) for k in vals[0]},
                "D": ({"brier": float(np.mean(dvals))} if dvals else None)}

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
    rows = [(s["scores"][forecaster]["G"], s["outcome"]["level"], s) for s in scores
            if s["outcome"]["level"] and (s["scores"].get(forecaster) or {}).get("G")]
    if not rows:
        return out
    reads = [r[2] for r in rows]
    for b in LEVELS:
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


def _spa_block(sc, task, key, base_name, names, n_spa, mb):
    """White's RC / Hansen's SPA: does the best of `names` beat `base_name` on this score?"""
    base = _series(sc, task, base_name, key)
    cols = [_series(sc, task, name, key) for name in names]
    keep = [i for i in range(len(sc)) if base[i] is not None and all(c[i] is not None for c in cols)]
    if len(keep) < 10:
        return {"note": f"only {len(keep)} complete rows; SPA needs >= 10", "benchmark": base_name}
    d = np.array([[base[i] - c[i] for c in cols] for i in keep])
    spa = INF.spa(d, n_boot=n_spa, mean_block=mb)
    spa["best_model"] = names[spa["best_model"]]; spa["models"] = names; spa["benchmark"] = base_name
    return spa


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
    for task, key, refs in (("G", "brier", ("climatology", "frozen", "random_analogs", "persistence")),
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
                                  "engine_vs_persistence": _skill_block(_paired(sc, task, fk, "engine", "persistence"), task, fk, "engine", "persistence", mb, min(n_boot, 500), max(lag, 0)),   # Amendment F.4
                                  "note": "size-corrected (Ferro 2014) scores published beside the registered ones; gates use the registered scores only"}
        # secondary scores
        if task == "G":
            rows = _paired(sc, task, "log", "engine", "climatology")
            blk["log_score_vs_climatology"] = _skill_block(rows, task, "log", "engine", "climatology", mb, min(n_boot, 500), max(lag, 0))
            # the ranked probability score over the ordinal IES-90 levels (Joe, 2026-09-02): same comparisons, distance-aware
            blk["rps"] = {"score": "rps", "engine_vs": {ref: _skill_block(_paired(sc, task, "rps", "engine", ref), task, "rps", "engine", ref, mb, min(n_boot, 500), max(lag, 0))
                                                        for ref in refs},
                          "items_vs_climatology": {iid: _skill_block(_paired(sc, task, "rps", iid, "climatology"), task, "rps", iid, "climatology", mb, min(n_boot, 300), max(lag, 0))
                                                   for iid in item_ids},
                          "learning_curve": _learning_curve(sc, task, "rps"),
                          "spa": _spa_block(sc, task, "rps", "climatology", item_ids + ["engine", "frozen"], n_spa, mb)}   # Amendment F.3
            blk["diagnostic_fair"]["rps_engine_vs_climatology"] = _skill_block(_paired(sc, task, "rps_fair", "engine", "climatology"), task, "rps_fair", "engine", "climatology", mb, min(n_boot, 500), max(lag, 0))
            # the DEAL flag (binary Brier), scored only where the realized flag is known
            drows = _paired(sc, "D", "brier", "engine", "climatology")
            blk["deal"] = {"score": "binary brier", "n_scored": len(drows),
                           "engine_vs": {ref: _skill_block(_paired(sc, "D", "brier", "engine", ref), "D", "brier", "engine", ref, mb, min(n_boot, 500), max(lag, 0))
                                         for ref in ("climatology", "frozen", "random_analogs")},
                           "base_rate": (round(float(np.mean([s["outcome"]["deal"] for s in sc if s["outcome"]["deal"] in (0, 1)])), 4)
                                         if any(s["outcome"]["deal"] in (0, 1) for s in sc) else None)}
            blk["murphy_engine"] = _reliability(sc, "engine", p["reliability_bins"], n_boot, mb)
            blk["murphy_climatology"] = _reliability(sc, "climatology", p["reliability_bins"], n_boot, mb)
            rid = next((it["id"] for it in (reads[0]["items"] if reads else []) if it.get("kind") == "recalibrated"), None)
            if rid:                                                                    # Amendment C.5
                blk["murphy_M13"] = _reliability(sc, rid, p["reliability_bins"], n_boot, mb)
                by_hash = {r["hash"]: r for r in reads}
                states = [next(it["recal"] for it in by_hash[s_["read_hash"]]["items"] if it.get("kind") == "recalibrated") for s_ in sc if s_["read_hash"] in by_hash]
                blk["recalibration"] = {"item": rid, "n_scored_reads": len(states),
                                        "n_reads_recalibrated": sum(1 for st in states if any(v != "identity" for v in st["mode"].values())),
                                        "first_active_n_fit": next((st["n_fit"] for st in states if any(v != "identity" for v in st["mode"].values())), None),
                                        "final_mode": (states[-1]["mode"] if states else None), "final_n_fit": (states[-1]["n_fit"] if states else None)}
        else:
            for q in ("pin10", "pin50", "pin90"):
                rows = _paired(sc, task, q, "engine", "climatology")
                blk[f"{q}_vs_climatology"] = _skill_block(rows, task, q, "engine", "climatology", mb, min(n_boot, 500), max(lag, 0))
            sg = [v for v in _series(sc, "P", "engine", "sign_ok") if v is not None]
            blk["sign_accuracy_engine"] = {"n": len(sg), "rate": round(float(np.mean(sg)), 3) if sg else None}
            blk["pit_engine"] = _pit_hist(sc, "engine", p["pit_bins"])
            blk["pit_climatology"] = _pit_hist(sc, "climatology", p["pit_bins"])
        # Reality Check / SPA over the family {items, engine, frozen} vs climatology (§6); vs persistence beside it (Amendment B.4)
        blk["spa"] = _spa_block(sc, task, key, "climatology", item_ids + ["engine", "frozen"], n_spa, mb)
        if task == "G":
            blk["spa_vs_persistence"] = _spa_block(sc, task, key, "persistence", item_ids + ["engine", "frozen"], n_spa, mb)
            rd = [r for r in reads if r["tier"] == tier and r["burn_in_ok"] and r["type"] in GEO]
            blk["n_persistence_fallback"] = sum(1 for r in rd if (r["baselines"].get("persistence") or {}).get("fallback") is True)
            blk["n_persistence_known"] = sum(1 for r in rd if (r["baselines"].get("persistence") or {}).get("fallback") is False)
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
    geo = [(r, s) for r, s in zip(reads, scores) if r["type"] in GEO and s["outcome"]["level"] and s["burn_in_ok"]]
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
        lab[pos[r["event_id"]]] = LEVELS.index(s["outcome"]["level"])
    # analog labels come from the corpus: the reads carry each analog's id; fetch its label via the scores of that id
    # (every analog with g_closed was itself a corpus event with a branch label)
    known = {s["event_id"]: s["outcome"]["level"] for s in scores if s["outcome"]["level"]}
    for e, i in pos.items():
        if lab[i] < 0 and e in known:
            lab[i] = LEVELS.index(known[e])
    class_of = {r["event_id"]: r["type"] for r, _ in geo}
    for s in scores:
        class_of.setdefault(s["event_id"], s["type"])
    N = len(reads[0]["items"]); K = p["k_max"]
    recal_idx = next((j for j, it in enumerate(reads[0]["items"]) if it.get("kind") == "recalibrated"), None)
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
        if recal_idx is not None:                                            # Amendment C.4: M13 refitted from the permuted closed outcomes
            base_idx = [j for j in range(N) if j != recal_idx]
            hb = has[:, base_idx]
            fz = (item_f[:, base_idx, :] * hb[..., None]).sum(axis=1) / np.maximum(hb.sum(axis=1), 1)[:, None]
            hz = hb.any(axis=1)
            yt = labv[tgt]
            m13 = fz.copy()
            for t_ in range(T):
                u = np.where(C[t_] & hz & (yt >= 0))[0]
                if len(u) >= RC.MIN_N and hz[t_]:
                    m13[t_] = RC.fit_apply_arrays(fz[u], yt[u], fz[t_])
            item_f[:, recal_idx, :] = m13; has[:, recal_idx] = hz
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
    for _ in range(n_perm):                                              # §6: i.i.d. within class (registered)
        lp = lab.copy()
        for cls_, idxs in groups.items():
            idxs = np.array(idxs)
            lp[idxs] = lab[idxs][rng.permutation(len(idxs))]
        null.append(skill_for(lp)[0])
    null = np.array(null)
    # Amendment F.2: block permutation -- the registered 35-day clusters (same tier, gap <= cluster_days) are permuted as units
    clusters, cur = [], [0]
    for i in range(1, T):
        gap = (pd.Timestamp(str(dates[i])) - pd.Timestamp(str(dates[i - 1]))).days
        if tiers[i] == tiers[i - 1] and gap <= p["cluster_days"]:
            cur.append(i)
        else:
            clusters.append(cur); cur = [i]
    clusters.append(cur)
    rng_b = np.random.default_rng(seed + 1)
    null_b = []
    for _ in range(n_perm):
        order = rng_b.permutation(len(clusters))
        seq = [i for k_ in order for i in clusters[k_]]
        lp = lab.copy()
        for pos_i, src_i in enumerate(seq):
            lp[tgt[pos_i]] = lab[tgt[src_i]]
        null_b.append(skill_for(lp)[0])
    null_b = np.array(null_b)
    iid = {"p_value": INF.permutation_p(obs, null), "null_mean": float(null.mean()), "null_sd": float(null.std()), "null_p95": float(np.percentile(null, 95)),
           "rule": "§6 registered: labels shuffled i.i.d. within class"}
    block = {"p_value": INF.permutation_p(obs, null_b), "null_mean": float(null_b.mean()), "null_sd": float(null_b.std()), "null_p95": float(np.percentile(null_b, 95)),
             "n_clusters": len(clusters), "mean_cluster_size": round(T / len(clusters), 2),
             "rule": f"Amendment F.2: intact {p['cluster_days']}-day clusters permuted as units (class stratification dropped)"}
    return {"n_reads": T, "n_perm": n_perm, "observed_skill": float(obs), "engine_brier": float(ob_e), "climatology_brier": float(ob_c),
            "p_value": block["p_value"], "decides": "block (Amendment F.2)", "block": block, "iid": iid,
            "null_mean": block["null_mean"], "null_sd": block["null_sd"], "null_p95": block["null_p95"],
            "note": "recomputed from sealed analog ids; Hedge and M13 replayed with the closed-by-t rule; p_value is the block-permutation p, the i.i.d. p is beside it"}


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
    hist_r = []                                                   # Amendment C.4: (g_closed_on, frozen G, level) replayed
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
        br, y = s["outcome"]["level"], None
        oc = corpus.outcome(r["event_id"], H, tier) if r["event_id"] in corpus.by_id else None
        y = oc["chg_pct"] if oc else None
        # per-item forecasts at k and H from the sealed ranked ids
        gI, pI, pW, fg = [], [], [], None
        for it in r["items"]:
            if it.get("kind") == "recalibrated":
                continue                                          # appended below from the replayed frozen mixture
            g_ids = [a[0] for a in it["ranked"] if a[2]][:k]
            p_ids = [a[0] for a in it["ranked"] if a[3]][:k]
            outs = [corpus.ies90[i]["level"] for i in g_ids if i in corpus.ies90]
            gI.append({b: outs.count(b) / len(outs) for b in LEVELS} if outs else None)
            vals = [corpus.outcome(i, H, tier)["chg_pct"] for i in p_ids if corpus.outcome(i, H, tier)]
            pI.append(vals or None); pW.append(None)
        if any(it.get("kind") == "recalibrated" for it in r["items"]):
            nb = len(gI); uni = np.full(nb, 1.0 / nb)
            fg = SC.mixture_g(gI, uni)
            used = [h for h in hist_r if h[0] <= t]
            rc = RC.Recalibrator().fit([h[1] for h in used], [h[2] for h in used])
            gI.append(rc.apply(fg) if fg else None)
            fv, fw = SC.mixture_p(pI, uni)
            pI.append(fv); pW.append(fw)
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
            if fg is not None:
                hist_r.append((s["outcome"]["g_closed_on"], fg, br))
        if y is not None and cp and any(pI):
            wP = hedge["P"].weights()
            vals, ws = SC.mixture_p(pI, wP, atom_weights=pW)
            ec, cc = SC.crps(vals, y, ws), SC.crps(cp, y)
            P_rows.append((ec, cc))
            pending.append((oc["closed_on"], "P", [min((SC.crps(v, y, aw) if v else cc) / p["p_scale"], 1.0) for v, aw in zip(pI, pW)]))
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
    base = S.weighting_items(menu)
    uniform = np.full(len(base), 1.0 / len(base))
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
            vec_e = corpus.vector(e["event_id"])                        # Amendment H: the situation fields as knowable at the real event's date
            pseudo = {k_: v for k_, v in e.items() if k_ in ("type", "title")}
            pseudo |= {col: (vec_e["fields"].get(f) if vec_e["fields"].get(f) is not None else "unknown") for f, col in S.SR_MAP.items()}
            pseudo |= {"event_id": f"placebo:{e['event_id']}:{rep}", "event_date": str(pd_.date())}
            vals_items, ids_items = [], []
            for m in base:
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


def leakage_test(sealed: Walk, broken: Walk, recal_broken: Walk = None, audit=None):
    """§1: the walk with the filtration broken must differ from the sealed run, or the result is void.
    Amendment C.6: a recalibrator fitted with the closed-by-t rule broken must change M13 on >= 1 read."""
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
    out = {"reads_differ": hs != hb, "scores": diffs, "n_reads_with_different_analogs": analog_diff}
    if recal_broken is not None:
        def m13(r):
            return next((it["G"] for it in r["items"] if it.get("kind") == "recalibrated"), None)
        n_diff = sum(1 for rs, rb in zip(sealed.reads, recal_broken.reads) if m13(rs) != m13(rb))
        same_base = all([it["ranked"] for it in rs["items"] if it.get("kind") != "recalibrated"] ==
                        [it["ranked"] for it in rb["items"] if it.get("kind") != "recalibrated"] for rs, rb in zip(sealed.reads, recal_broken.reads))
        n_pending = sum(1 for r in recal_broken.reads for it in r["items"] if it.get("kind") == "recalibrated"
                        and it["recal"]["fit_max_closed_on"] and it["recal"]["fit_max_closed_on"] > r["as_of"])
        r_ok = n_diff > 0 and same_base
        out["recalibration_rule"] = {"n_reads_with_different_M13": n_diff, "base_items_identical": same_base,
                                     "n_broken_reads_that_used_an_unclosed_outcome": n_pending, "asserted": r_ok}
        ok = ok and r_ok
    if audit is not None:                                                    # Amendment F.1
        out["filtration_audit_clean"] = bool(audit.get("clean"))
        ok = ok and bool(audit.get("clean"))
    out |= {"asserted": ok, "verdict": "filtration is binding" if ok else ("VOID: the filtration audit found a violation" if audit is not None and not audit.get("clean") else "VOID: a broken rule changed nothing")}
    return out


def filtration_audit(corpus, reads):
    """Amendment F.1: inside the sealed run, by an independent path (raw dates and a mask-based lookup, never the
    functions that built the read): every analog dated before as_of; every g_closed analog's window closed (date + 90
    <= as_of); every p_closed analog's closing price observation dated <= as_of; every market value in the read's state
    equal to the last observation dated < as_of - lag; the persistence window ending before as_of."""
    counts = defaultdict(int); n_checks = defaultdict(int); first = None
    def viol(kind, r, detail):
        nonlocal first
        counts[kind] += 1
        if first is None:
            first = {"kind": kind, "event_id": r["event_id"], "as_of": r["as_of"], "detail": detail}
    for r in reads:
        as_of = r["as_of"]; tier = r["tier"]; H = r["horizon"]
        s = corpus.prices.get(tier)
        seen = set()
        for it in r["items"]:
            for a in it.get("ranked", []):
                aid, g_cl, p_cl = a[0], bool(a[2]), bool(a[3])
                if aid in seen:
                    continue
                seen.add(aid)
                e = corpus.by_id.get(aid)
                if e is None:
                    viol("analog_unknown", r, aid); continue
                n_checks["analog_date"] += 1
                if not (e["event_date"] < as_of):
                    viol("analog_date", r, f"{aid} dated {e['event_date']}")
                if g_cl:
                    n_checks["g_window"] += 1
                    if str((pd.Timestamp(e["event_date"]) + pd.Timedelta(days=R.G_HORIZON_DAYS)).date()) > as_of:
                        viol("g_window", r, f"{aid} +90d window open at {as_of}")
                if p_cl and s is not None:
                    n_checks["p_window"] += 1
                    pos = int(s.index.searchsorted(pd.Timestamp(e["event_date"])))
                    if pos + H >= len(s) or str(s.index[pos + H].date()) > as_of:
                        viol("p_window", r, f"{aid} +{H} price window open at {as_of}")
        for f, val in (r.get("state_market") or {}).items():
            if val is None:
                continue
            n_checks["market_value"] += 1
            iv, d = corpus.info.independent_value_before(f, as_of)
            if iv is not None and abs(float(val) - iv) <= 1e-9:
                continue
            # a market field may also come from session A's state bridge (situation_state), which carries its own
            # obs_date and vintage; that path is admissible only if BOTH are at or before as_of (checked here, not assumed)
            pr = [x for x in (corpus.panel.get(r["event_id"]) or []) if x.get("field") == f and x.get("value") is not None
                  and abs(float(x["value"]) - float(val)) <= 1e-9]
            ok = [x for x in pr if (x.get("vintage") and str(x["vintage"]) <= as_of) and (x.get("obs_date") and str(x["obs_date"]) <= as_of)]
            if ok:
                n_checks["market_value_from_panel"] += 1
                continue
            if pr:
                viol("market_value_panel_dates", r, f"{f}: panel row value {val} with obs_date {pr[0].get('obs_date')} / vintage {pr[0].get('vintage')} vs as_of {as_of}")
            else:
                viol("market_value", r, f"{f}: read used {val}, last value dated < as_of - lag is {iv} ({d}), and no panel row carries it")
        pw = (r["baselines"].get("persistence") or {}).get("window_pre")
        if pw:
            n_checks["persistence_window"] += 1
            if not (pw[1] < as_of):
                viol("persistence_window", r, f"window {pw} not before {as_of}")
    n_viol = int(sum(counts.values()))
    return {"n_reads": len(reads), "checks": dict(n_checks), "violations": dict(counts), "n_violations": n_viol, "first_violation": first,
            "release_lags_days": dict(S.RELEASE_LAGS), "clean": n_viol == 0,
            "note": "Amendment F.1: independent recomputation inside the sealed run; one violation voids the run (leakage_test.asserted false)"}


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
                               "realized_chg_pct": s["outcome"]["chg_pct"], "realized_level": s["outcome"]["level"], "realized_deal": s["outcome"]["deal"]}
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
    labelled = [e for e in geo if e["event_id"] in corpus.ies90]
    with_deal = sum(1 for e in labelled if corpus.ies90[e["event_id"]]["deal"] in (0, 1))
    lv = [corpus.ies90[e["event_id"]]["level"] for e in labelled]
    try:                                   # which OUTCOME_MAPPING amendment produced the rows this run read (session A's file)
        dist = json.load(open(ROOT / "data" / "state" / "ies90_distribution.json"))
        reg = {"registration": dist.get("registration"), "generated_at": dist.get("generated_at")}
    except Exception:
        reg = {"registration": None, "note": "data/state/ies90_distribution.json absent"}
    out = {"n_events": n, "n_geo": len(geo), "n_with_any_situation_field": coded,
           "g_target": "IES-90 (event_outcomes source='ies90'); sr_outcome_90 retired 2026-09-02", "ies90_registration": reg,
           "n_geo_with_ies90_level": len(labelled), "n_geo_no_independent_outcome": len(geo) - len(labelled),
           "share_geo_labelled": round(len(labelled) / len(geo), 3) if geo else None,
           "ies90_level_counts": {l: lv.count(l) for l in LEVELS}, "n_geo_with_deal_flag": with_deal,
           "panel_events_with_rows": len(corpus.panel), "codebook_fields": len(corpus.schema_extra)}
    vecs = [corpus.vector(e["event_id"]) for e in corpus.events]
    out["situation_knowable"] = {"rule": "Amendment H: actor/target/conflict_scope/tempo/asset_role from situation_state knowable_at rows (vintage <= as_of)",
                                 "n_events_with_a_situation_field_at_t": sum(1 for v in vecs if v.get("situation_known_at_t")),
                                 "n_events_with_none": sum(1 for v in vecs if not v.get("situation_known_at_t")),
                                 "fields_blanked": sum(len(v.get("situation_blanked", [])) for v in vecs),
                                 "fields_known_at_t": sum(len(v.get("situation_known_at_t", [])) for v in vecs)}
    if geo and coded < 0.5 * n:
        out["warning_situation"] = ("situation record largely absent: similarity runs on the market block only. "
                                    "Re-run src/situation_record.py (writes the events table; Joe's call) and then src/walk.py.")
    if geo and len(labelled) < 0.5 * len(geo):
        out["warning_labels"] = "IES-90 levels largely absent: G is not scorable. Run python3 src/state/ies90.py (session A) and then src/walk.py."
    return out


def _knowable_limit():
    """WORLD_STATE_FRAMEWORK.md Amendment A (session A, 2026-09-02): the situation fields now carry knowable_at; the
    walk still reads events.sr_* as coded (protocol §1 LIMITATION). Quote session A's counts as computed, never restate them."""
    try:
        d = json.load(open(ROOT / "data" / "state" / "situation_knowable.json"))
        return (f"situation fields are read as coded (protocol §1 LIMITATION); by WORLD_STATE_FRAMEWORK.md Amendment A "
                f"(data/state/situation_knowable.json, {d.get('generated_at')}) only the fields whose source carries its own date are knowable at t: "
                f"{json.dumps({k: v for k, v in d.items() if isinstance(v, (int, float, str)) and k != 'generated_at'})[:600]}")
    except Exception:
        return "situation fields are read as coded (protocol §1 LIMITATION); data/state/situation_knowable.json absent -- the knowable-at count is not available to this run"


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
        detail = []
        for t in permit:                                                     # Amendment F.5: no status without its p-values
            blk = summary["tiers"][t][task]
            row = blk["engine_vs"]["climatology"] if name == "engine" else blk["items_vs_climatology"].get(name, {})
            spa = blk.get("spa", {})
            detail.append(f"{t}: skill {row.get('skill'):+.4f}, DM p {row.get('dm_p'):.3f}, family SPA p {spa.get('p_spa'):.3f}" if row.get("skill") is not None and row.get("dm_p") is not None and spa.get("p_spa") is not None else f"{t}: no scored comparison")
        return {"status": status + " (" + "; ".join(detail) + ")" if detail else status, "status_code": status, "conditions": conds}
    for task in ("G", "P"):
        out["rules"][f"engine:{task}"] = one("engine", task)
        for t in permit:
            for iid in summary["tiers"][t][task]["items_vs_climatology"]:
                out["rules"][f"{iid}:{task}"] = one(iid, task)
    for task in ("G", "P"):
        r = out["rules"].get(f"engine:{task}", {})
        out[f"{task}_conditioning"] = f"{r.get('status_code', 'SUGGESTIVE')} (protocol §7; audit passed: {flag})"
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
            for ax, b in zip(axes, LEVELS):
                m = blk.get(b)
                ax.plot([0, 1], [0, 1], "k--", lw=0.5)
                if m:
                    xs = [d["forecast_mean"] for d in m["diagram"]]; ys = [d["observed_freq"] for d in m["diagram"]]
                    ax.plot(xs, ys, "o-")
                    for d in m["diagram"]:
                        if d.get("band95"):
                            ax.plot([d["forecast_mean"]] * 2, d["band95"], color="gray", lw=1)
                    ax.set_title(f"level {b}: {LEVEL_MEANING[b]}\nrel {m['reliability']:.3f} res {m['resolution']:.3f} n={m['n']}", fontsize=8)
                ax.set_xlim(0, 1); ax.set_ylim(0, 1)
            fig.suptitle(f"Reliability -- engine, {tier} tier (bars: stationary-bootstrap 95% band)")
            fig.tight_layout(); fig.savefig(fd / f"reliability_{tier}.png", dpi=120); plt.close(fig); made.append(f"reliability_{tier}.png")
        blkG = (summary["tiers"].get(tier) or {}).get("G", {})
        if blkG.get("murphy_engine"):
            for b in LEVELS:
                series = [(name, (blkG.get(key) or {}).get(b)) for name, key in (("engine", "murphy_engine"), ("climatology", "murphy_climatology"), ("M13 recalibrated", "murphy_M13"))]
                if not any(m for _, m in series):
                    continue
                fig, ax = plt.subplots(figsize=(5, 4))
                ax.plot([0, 1], [0, 1], "k--", lw=0.5)
                for off, (name, m) in zip((-0.01, 0.0, 0.01), series):
                    if not m:
                        continue
                    xs = [d["forecast_mean"] + off for d in m["diagram"]]; ys = [d["observed_freq"] for d in m["diagram"]]
                    ax.plot(xs, ys, "o-", ms=4, label=f"{name} (rel {m['reliability']:.3f}, res {m['resolution']:.3f})")
                    for d, x in zip(m["diagram"], xs):
                        if d.get("band95"):
                            ax.plot([x, x], d["band95"], color="gray", lw=0.8, alpha=0.7)
                ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_xlabel("forecast probability"); ax.set_ylabel("observed frequency")
                ax.set_title(f"Reliability -- level {b} ({LEVEL_MEANING[b]}), {tier} tier; bars: stationary-bootstrap 95% band", fontsize=8); ax.legend(fontsize=7)
                fig.tight_layout(); fig.savefig(fd / f"reliability_G_{b}.png", dpi=120); plt.close(fig); made.append(f"reliability_G_{b}.png")
        pit = (summary["tiers"].get(tier) or {}).get("P", {}).get("pit_engine")
        if pit:
            fig, ax = plt.subplots(figsize=(5, 3.5))
            ax.bar(np.arange(pit["bins"]) / pit["bins"], pit["counts"], width=1 / pit["bins"], align="edge")
            ax.axhline(pit["expected_per_bin"], color="k", lw=0.8)
            ax.set_title(f"PIT histogram -- engine, {tier} (n={pit['n']}, chi2={pit['chi2']:.1f})", fontsize=9)
            fig.tight_layout(); fig.savefig(fd / f"pit_{tier}.png", dpi=120); plt.close(fig); made.append(f"pit_{tier}.png")
    pw = summary.get("power") or {}
    if any(isinstance(v, dict) and v.get("by_n") for v in pw.values()):
        fig, axes = plt.subplots(1, 2, figsize=(11, 4))
        for task, col in (("G", "C0"), ("P", "C1")):
            blk = pw.get(task) or {}
            for n, b in (blk.get("by_n") or {}).items():
                xs = [c[0] for c in b["curve"]]; ys = [c[1] for c in b["curve"]]
                axes[0].plot(xs, ys, "o-", color=col, label=f"{task} ({blk.get('score')}), n={n}: MDS {b.get('mds_skill')}")
            sc_ = (blk.get("n_required_for_skill") or {}).get("scan") or []
            if sc_:
                axes[1].plot([c[0] for c in sc_], [c[1] for c in sc_], "o-", color=col, label=f"{task}: skill +{blk['n_required_for_skill']['skill']} -> n {blk['n_required_for_skill'].get('n')}")
        for ax in axes:
            ax.axhline(0.8, color="k", lw=0.6, ls="--"); ax.set_ylim(0, 1.02); ax.legend(fontsize=7)
        axes[0].set_xlabel("skill vs climatology"); axes[0].set_ylabel("power (DM/HLN, alpha .05)"); axes[0].set_title("Power at the measured n (stationary block bootstrap of the sealed differentials)", fontsize=8)
        axes[1].set_xlabel("n scored reads"); axes[1].set_xscale("log"); axes[1].set_title("n required to detect +0.05 skill at 80% power", fontsize=8)
        fig.tight_layout(); fig.savefig(fd / "power.png", dpi=120); plt.close(fig); made.append("power.png")
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
    geo = [s for s in w.scores if s["burn_in_ok"] and s["outcome"]["level"]]
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
    b2 = Walk(corpus, menu, out_dir=tempfile.mkdtemp(prefix="walk_recal_leak_"), params=p, break_recal=True, quiet=True).run_reads() if w.recal else None
    summary["filtration_audit"] = filtration_audit(corpus, w.reads)
    summary["leakage_test"] = leakage_test(w, b, b2, summary["filtration_audit"])
    # Brief 2 B-6: power under the measured block dependence, from the sealed differential series (engine - climatology)
    summary["power"] = {}
    dt = summary["tiers"].get("daily")
    if dt:
        sc_d = [s_ for s_ in w.scores if s_["tier"] == "daily" and s_["burn_in_ok"]]
        for task, key in (("G", "brier"), ("P", "crps")):
            rows = _paired(sc_d, task, key, "engine", "climatology")
            if len(rows) >= 10:
                d = np.array([r_[1] - r_[2] for r_ in rows]); ref_mean = float(np.mean([r_[2] for r_ in rows]))
                summary["power"][task] = INF.power_block(d, dt["dependence"]["mean_block"], dt["dependence"]["hac_lag"], ref_mean, n_list=[len(rows)],
                                                         n_sims=(100 if fast else 400)) | {"score": key, "n_measured": len(rows), "tier": "daily"}
    summary["big_moves_knew"] = big_moves_knew(corpus, w.reads, w.scores)
    summary["verdict"] = verdict(summary, p)
    summary["limits"] = [f"G target is IES-90 (OUTCOME_MAPPING.md Amendment 1 and later; registration in data_state): independent dated sources; "
                         f"{sum(1 for e in corpus.events if e['type'] in GEO and e['event_id'] not in corpus.ies90)} geopolitical events without a covering "
                         "source are unscorable on G (no_independent_outcome) and are never G evidence; the 30-event IES-90 audit is the §7 label audit "
                         "-- audit flag false until data/audits/outcome_audit.json records a pass",
                         "sr_outcome_90 / sr_outcome_30 retired 2026-09-02: not a target, not a feature, not analog evidence",
                         "IES-90 GED levels are location-based (deaths in the country, not between the actors): stated in every such row's detail",
                         "the gates use the registered multi-category Brier; the ranked probability score over the ordinal levels is published in "
                         "every tier's G.rps block and is not (yet) registered as a gate",
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
                         "M13 (Amendment C) carries no analog atoms, so the size-corrected diagnostic of the engine mixture is computed from the twelve "
                         "weighting items' atoms only (M13's share is left out of that diagnostic, never of the registered scores)",
                         "G-persistence (Amendment B) is evaluated on each source's single published vintage, as the labels are",
                         _knowable_limit(),
                         "this summary.json replaces the PRE_REGISTRATION_V2 src/walk_forward.py summary at the same path; the ledger, story and "
                         "terminal readers of the old 'windows' shape show an empty engine board until PATH Step 9 rewires them"]
    summary["data_state"] = data_state(corpus)
    summary["data_state"]["archived_runs"] = archive_prior_runs(out_dir, w.run_id)        # Amendment D: prior runs -> runs/<run_id>/*.jsonl.gz
    summary["data_state"]["archive_dir"] = "data/walk_forward/runs/<run_id>/ (git-ignored; each archive re-verifies by walk.verify_file)"
    summary["seal_check"] = dict(zip(("ok", "n_records", "first_bad_line"), verify_file(out_dir / "reads.jsonl")))
    summary["seal_check"]["run_in_tree"] = w.run_id
    summary["determinism"] = {"content_digest": content_digest(w.reads), "n_reads": len(w.reads), "seeds": p["seeds"],
                              "rule": "Amendment I: SHA-256 over the ordered content hashes (records without hash/sealed_at/run_id/fit_max_looked_up_at); two runs on the same inputs must agree; python3 src/walk.py --digest prints the digest of the run in the tree"}
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
            if task == "G":
                for ref, r in t[task].get("rps", {}).get("engine_vs", {}).items():
                    if r.get("skill") is not None:
                        print(f"  G (RPS) engine vs {ref:<15} skill {r['skill']:+.4f}  CI {r['ci95'][0]:+.3f}..{r['ci95'][1]:+.3f}  DM/HLN p={r['dm_p']:.3f}  n={r['n']}")
                d = t[task].get("deal", {}); dr = d.get("engine_vs", {}).get("climatology", {})
                if dr.get("skill") is not None:
                    print(f"  DEAL (binary Brier) engine vs climatology skill {dr['skill']:+.4f}  CI {dr['ci95'][0]:+.3f}..{dr['ci95'][1]:+.3f}  n={dr['n']}  base rate {d.get('base_rate')}")
            if task == "G":
                rc_ = t[task].get("recalibration") or {}
                m13 = (t[task].get("items_vs_climatology") or {}).get(rc_.get("item") or "", {})
                if m13.get("skill") is not None:
                    print(f"  M13 recalibrated vs climatology  skill {m13['skill']:+.4f}  CI {m13['ci95'][0]:+.3f}..{m13['ci95'][1]:+.3f}  DM/HLN p={m13['dm_p']:.3f}  n={m13['n']}  "
                          f"(recalibrated on {rc_.get('n_reads_recalibrated')} of {rc_.get('n_scored_reads')} reads; final mode {rc_.get('final_mode')})")
                print(f"  G persistence fallback: {t[task].get('n_persistence_fallback')} of {t[task].get('n_persistence_fallback', 0) + t[task].get('n_persistence_known', 0)} geopolitical reads")
            fr = t[task].get("diagnostic_fair", {}).get("engine_vs_climatology", {})
            if fr.get("skill") is not None:
                print(f"  {task} [diagnostic, not registered] size-corrected engine vs climatology skill {fr['skill']:+.4f}  CI {fr['ci95'][0]:+.3f}..{fr['ci95'][1]:+.3f}  DM/HLN p={fr['dm_p']:.3f}")
        m = t["M"]["engine"]; print(f"  M engine precision {m['precision']} recall {m['recall']} n={m['n']} base {m['base_rate']}")
    pm = summary["permutation"]; print(f"\npermutation (G): skill {pm.get('observed_skill')} block p={pm.get('p_value')} (iid p={(pm.get('iid') or {}).get('p_value')})")
    fa = summary.get("filtration_audit") or {}; print(f"filtration audit: {fa.get('n_violations')} violations over {sum((fa.get('checks') or {}).values())} checks -> {'clean' if fa.get('clean') else 'VOID'}")
    for task, blk in (summary.get("power") or {}).items():
        for n, b in (blk.get("by_n") or {}).items():
            print(f"power {task}: minimum detectable skill at 80% for n={n}: {b.get('mds_skill')}; n required for +0.05: {(blk.get('n_required_for_skill') or {}).get('n')}")
    print(f"content digest: {(summary.get('determinism') or {}).get('content_digest')}")
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
    ap.add_argument("--digest", action="store_true", help="print the content digest of the run in data/walk_forward/reads.jsonl (Amendment I) and exit")
    a = ap.parse_args()
    if a.digest:
        rows = [json.loads(l) for l in open(WF / "reads.jsonl", encoding="utf-8") if l.strip()]
        print(json.dumps({"run_ids": sorted({r_["run_id"] for r_ in rows}), "n_reads": len(rows), "content_digest": content_digest(rows)}))
        sys.exit(0)
    s, _ = run(fast=a.fast)
    _print(s)
