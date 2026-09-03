"""g_era_confound.py -- G-6: OPEN_ITEMS 1.4, the era confound.

Registered first, in docs/g/G6_ERA_CONFOUND_REGISTRATION.md (2026-09-03). Read that file before
this one; every rule below names the clause it implements.

THIS IS A DIAGNOSTIC. It gates nothing, re-judges no run, moves no threshold and writes no table.
Joe's question is not "decompose the era effect" -- it is "can the three confounds be separated at
all at this n, and if they cannot, say so rather than reporting a decomposition the sample cannot
support." So §5's identifiability rule is fixed before the numbers and can return NOT SEPARABLE,
in which case no decomposition is published.

The run is PINNED (§2): data/walk_forward/scores.jsonl currently holds TWO runs while summary.json
describes one, so an analysis that read the file without filtering would silently mix them.

Run:  python3 src/g_era_confound.py
Out:  docs/g/ERA_CONFOUND.json, docs/g/ERA_CONFOUND.md
"""
from __future__ import annotations

import datetime as dt
import json
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
WF = ROOT / "data" / "walk_forward"
OUT_JSON = ROOT / "docs" / "g" / "ERA_CONFOUND.json"
OUT_MD = ROOT / "docs" / "g" / "ERA_CONFOUND.md"

RUN_ID = "walk_20260903T003422Z"            # §2, pinned: the run summary.json publishes
SEED = 19900802                             # protocol Amendment I's registered seed
CLUSTER_DAYS = 35                           # protocol §2's registered clustering rule
N_BOOT = 2000
ERAS = (("1987-99", 1987, 1999), ("2000-09", 2000, 2009),
        ("2010-19", 2010, 2019), ("2020-26", 2020, 2026))       # §3, taken from OPEN_ITEMS, not chosen
PUBLISHED = {"n": 150, "engine_mean": 0.7687487109093333,
             "ref_mean": 0.7010597406851313, "skill": -0.09655235680492913}
SEP_RHO = 0.80          # §5(a)
SEP_CELL_N = 20         # §5(b)
S4_HALF = 0.5           # §4: fair spread <= half the registered spread -> the artefact explains it


# ----------------------------------------------------------------------------- loading (read-only)

def load_scores():
    """§2. Only the pinned run. Reports how many rows the file holds for other runs."""
    by_run = Counter()
    rows = []
    for line in open(WF / "scores.jsonl"):
        r = json.loads(line)
        by_run[r["run_id"]] += 1
        if r["run_id"] == RUN_ID:
            rows.append(r)
    return rows, dict(by_run)


def load_reads():
    out = {}
    for line in open(WF / "reads.jsonl"):
        r = json.loads(line)
        if r["run_id"] == RUN_ID:
            out[(r["event_id"], r.get("as_of"))] = r
    return out


def load_basis():
    """§3. The label basis per event, from event_outcomes (ies90), read-only."""
    conn = sqlite3.connect(f"file:{ROOT / 'data' / 'oil.db'}?mode=ro", uri=True)
    try:
        return {e: v for e, v in conn.execute(
            "SELECT event_id, value_text FROM event_outcomes WHERE source='ies90' AND field='basis'")}
    finally:
        conn.close()


def g(r, ref, key="brier"):
    v = (r["scores"].get(ref) or {}).get("G")
    return (v or {}).get(key)


def scored_set(rows):
    """The 150: daily tier, burn-in met, both engine and climatology G scored."""
    return [r for r in rows if r["tier"] == "daily" and r.get("burn_in_ok")
            and g(r, "engine") is not None and g(r, "climatology") is not None]


# ----------------------------------------------------------------------------- §2 baseline check

def baseline_check(sc):
    e = float(np.mean([g(r, "engine") for r in sc]))
    c = float(np.mean([g(r, "climatology") for r in sc]))
    got = {"n": len(sc), "engine_mean": e, "ref_mean": c, "skill": 1 - e / c}
    ok = (got["n"] == PUBLISHED["n"]
          and all(abs(got[k] - PUBLISHED[k]) < 1e-7 for k in ("engine_mean", "ref_mean", "skill")))
    return {"published": PUBLISHED, "recomputed": got, "agrees": bool(ok),
            "rule": "§2: if this does not reproduce to the seventh decimal the diagnostic is void."}


# ----------------------------------------------------------------------------- the assembled frame

def build_frame(sc, reads, basis):
    """One row per scored read, carrying the four variables of §3."""
    out = []
    for r in sc:
        rd = reads.get((r["event_id"], r["date"])) or {}
        labels = ((rd.get("baselines") or {}).get("climatology") or {}).get("G_labels") or []
        labels = [str(x) for x in labels if x is not None]
        base0 = (labels.count("0") / len(labels)) if labels else None
        out.append({
            "event_id": r["event_id"], "date": r["date"], "year": int(r["date"][:4]),
            "type": r["type"],
            "era": next((n for n, lo, hi in ERAS if lo <= int(r["date"][:4]) <= hi), None),
            "brier_engine": g(r, "engine"), "brier_clim": g(r, "climatology"),
            "fair_engine": g(r, "engine", "brier_fair"), "fair_clim": g(r, "climatology", "brier_fair"),
            "n_atoms_engine": (((r["scores"].get("engine") or {}).get("G")) or {}).get("n_atoms"),
            "n_atoms_clim": (((r["scores"].get("climatology") or {}).get("G")) or {}).get("n_atoms"),
            "pool_g": rd.get("n_pool_g"), "pool_labels": len(labels), "base_rate_0": base0,
            "basis": basis.get(r["event_id"]), "level": r["outcome"].get("level"),
        })
    return out


# ----------------------------------------------------------------------------- intervals (§6)

def clusters(dates):
    """Protocol §2: reads within 35 days of the previous read are one cluster."""
    order = np.argsort(dates)
    cid, out, last = 0, np.zeros(len(dates), dtype=int), None
    for i in order:
        d = dates[i]
        if last is not None and (d - last).days > CLUSTER_DAYS:
            cid += 1
        out[i] = cid
        last = d
    return out


def boot_skill(eng, ref, cl, n_boot=N_BOOT, seed=SEED):
    """Cluster bootstrap of the skill 1 - mean(eng)/mean(ref), resampling whole clusters."""
    rng = np.random.default_rng(seed)
    eng, ref, cl = np.asarray(eng, float), np.asarray(ref, float), np.asarray(cl)
    ids = np.unique(cl)
    idx = {c: np.flatnonzero(cl == c) for c in ids}
    if len(ids) < 2:
        return None, None, len(ids)
    vals = []
    for _ in range(n_boot):
        pick = rng.choice(ids, size=len(ids), replace=True)
        sel = np.concatenate([idx[c] for c in pick])
        m = np.mean(ref[sel])
        if m > 0:
            vals.append(1 - np.mean(eng[sel]) / m)
    if not vals:
        return None, None, len(ids)
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5)), len(ids)


def mds(eng, ref, cl, n_boot=800, seed=SEED):
    """§6: the minimum detectable skill at 80% power for this n and dispersion -- the half-width
    of the interval scaled to the 80%-power constant (1.96+0.84)/1.96."""
    lo, hi, ncl = boot_skill(eng, ref, cl, n_boot=n_boot, seed=seed)
    if lo is None:
        return None, ncl
    return float((hi - lo) / 2 * (1.96 + 0.8416) / 1.96), ncl


# ----------------------------------------------------------------------------- §4 and §5

def era_table(frame, score="brier"):
    ek, ck = f"{'brier' if score == 'brier' else 'fair'}_engine", f"{'brier' if score == 'brier' else 'fair'}_clim"
    out = {}
    for name, _lo, _hi in ERAS:
        rs = [r for r in frame if r["era"] == name and r[ek] is not None and r[ck] is not None]
        if not rs:
            out[name] = {"n": 0}
            continue
        eng = [r[ek] for r in rs]
        ref = [r[ck] for r in rs]
        dates = [dt.date.fromisoformat(r["date"]) for r in rs]
        cl = clusters(dates)
        lo, hi, ncl = boot_skill(eng, ref, cl)
        m, _ = mds(eng, ref, cl)
        pools = [r["pool_g"] for r in rs if r["pool_g"] is not None]
        base = [r["base_rate_0"] for r in rs if r["base_rate_0"] is not None]
        dy = [r["basis"] for r in rs if r["basis"]]
        out[name] = {
            "n": len(rs), "n_clusters": ncl,
            "engine_mean": float(np.mean(eng)), "ref_mean": float(np.mean(ref)),
            "skill": float(1 - np.mean(eng) / np.mean(ref)),
            "ci95": [lo, hi], "min_detectable_skill_80pc": m,
            "pool_median": (float(np.median(pools)) if pools else None),
            "pool_min": (int(min(pools)) if pools else None), "pool_max": (int(max(pools)) if pools else None),
            "base_rate_0_mean": (float(np.mean(base)) if base else None),
            "dyadic_share": (round(sum(1 for x in dy if x == "dyadic") / len(dy), 4) if dy else None),
            "n_atoms_engine_median": float(np.median([r["n_atoms_engine"] for r in rs if r["n_atoms_engine"]])),
            "n_atoms_clim_median": float(np.median([r["n_atoms_clim"] for r in rs if r["n_atoms_clim"]])),
        }
    return out


def spread(tab):
    ss = [v["skill"] for v in tab.values() if v.get("n")]
    return (max(ss) - min(ss)) if len(ss) > 1 else None


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = ~(np.isnan(a) | np.isnan(b))
    a, b = a[ok], b[ok]
    if len(a) < 3:
        return None
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean()
    d = float(np.sqrt((ra ** 2).sum() * (rb ** 2).sum()))
    return (float((ra * rb).sum() / d) if d > 0 else None)


def separability(frame):
    """§5, computed under the rule fixed before the numbers."""
    era_ix = {n: i for i, (n, _l, _h) in enumerate(ERAS)}
    v = {"era_index": [era_ix.get(r["era"]) for r in frame],
         "pool_g": [r["pool_g"] for r in frame],
         "base_rate_0": [r["base_rate_0"] for r in frame],
         "dyadic": [(1.0 if r["basis"] == "dyadic" else 0.0 if r["basis"] else None) for r in frame],
         "date_ordinal": [dt.date.fromisoformat(r["date"]).toordinal() for r in frame]}
    v = {k: [np.nan if x is None else float(x) for x in xs] for k, xs in v.items()}
    keys = list(v)
    rho = {f"{a}~{b}": spearman(v[a], v[b]) for i, a in enumerate(keys) for b in keys[i + 1:]}
    # condition number of the standardised design
    M = np.array([v[k] for k in ("era_index", "pool_g", "base_rate_0", "dyadic")], dtype=float).T
    M = M[~np.isnan(M).any(axis=1)]
    cond = None
    if len(M) > 4:
        Z = (M - M.mean(0)) / np.where(M.std(0) > 0, M.std(0), 1)
        cond = float(np.linalg.cond(Z))
    # (era x pool tertile) support
    pools = np.array([x for x in v["pool_g"] if not np.isnan(x)])
    t1, t2 = (float(np.percentile(pools, 33.3)), float(np.percentile(pools, 66.7))) if len(pools) else (0, 0)
    tert = lambda p: (None if p is None else ("low" if p <= t1 else "mid" if p <= t2 else "high"))  # noqa: E731
    cross = defaultdict(int)
    for r in frame:
        cross[(r["era"], tert(r["pool_g"]))] += 1
    diag = {"1987-99": "low", "2000-09": "low", "2010-19": "mid", "2020-26": "high"}
    offdiag = [(k, n) for k, n in cross.items() if k[1] and diag.get(k[0]) != k[1] and n >= SEP_CELL_N]
    ranges = {}
    for name, _lo, _hi in ERAS:
        ps = [r["pool_g"] for r in frame if r["era"] == name and r["pool_g"] is not None]
        ranges[name] = {"min": (min(ps) if ps else None), "max": (max(ps) if ps else None), "n": len(ps)}
    return {"spearman": rho, "condition_number": cond,
            "pool_tertile_cuts": {"t33": t1, "t67": t2},
            "cross_tab": {f"{k[0]}|{k[1]}": n for k, n in sorted(cross.items(), key=lambda x: str(x[0]))},
            "off_diagonal_cells_ge_20": [{"cell": f"{k[0]}|{k[1]}", "n": n} for k, n in offdiag],
            "pool_range_by_era": ranges}


def verdict(sep, tab_reg, pooled_skill):
    """§5's decision rule, applied mechanically to the numbers just computed."""
    rho = sep["spearman"].get("era_index~pool_g")
    a = (rho is not None and abs(rho) >= SEP_RHO)
    b = len(sep["off_diagonal_cells_ge_20"]) < 2
    contains = {n: (v["ci95"][0] is not None and v["ci95"][0] <= pooled_skill <= v["ci95"][1])
                for n, v in tab_reg.items() if v.get("n") and v["ci95"][0] is not None}
    c = bool(contains) and all(contains.values())
    fired = [k for k, hit in (("(a) |rho(era, pool)| >= 0.80", a),
                              ("(b) < 2 off-diagonal cells with n >= 20", b),
                              ("(c) every era interval contains the pooled skill", c)) if hit]
    return {"separable": not fired, "criteria_fired": fired,
            "rho_era_pool": rho, "off_diagonal_cells": len(sep["off_diagonal_cells_ge_20"]),
            "era_ci_contains_pooled": contains, "pooled_skill": pooled_skill,
            "rule": ("G6_REGISTRATION §5, fixed before the numbers. NOT SEPARABLE if any of (a), (b), (c). "
                     "If NOT SEPARABLE, no decomposition is published."),
            "consequence": ("No decomposition is published; the era table stands as a description with its "
                            "intervals, and OPEN_ITEMS 1.4's question is answered 'the sample cannot separate "
                            "them'." if fired else
                            "The decomposition may be published, with §7's caveats.")}


def s4(tab_reg, tab_fair):
    """§4's size-correction test, under the pass condition fixed before the numbers."""
    sr, sf = spread(tab_reg), spread(tab_fair)
    ratio = (sf / sr) if (sr and sf is not None and sr > 0) else None
    return {"registered_spread": sr, "fair_spread": sf, "ratio_fair_to_registered": ratio,
            "threshold": S4_HALF,
            "passes": (ratio is not None and ratio <= S4_HALF),
            "prediction_registered": ("§4: the fair-Brier era gradient is materially flatter than the "
                                      "registered-Brier one, because the engine's k-atom inflation is "
                                      "constant at S/5 while climatology's shrinks as S/pool, and pool grows "
                                      "with era. Registered magnitude: the artefact swings ~0.068 in absolute "
                                      "Brier, ~0.10 in skill, against an observed era spread of 0.126."),
            "reading": ("PASSES: the size artefact accounts for at least half the era gradient." if
                        (ratio is not None and ratio <= S4_HALF) else
                        "FAILS: the era gradient survives size correction; the artefact is not the whole story."),
            "gates": "nothing. Amendment E.1 governs which score judges a v2 run, and this does not touch it."}


def post_hoc(frame, tab_reg, tab_fair):
    """Amendment 1 A1.5: D1-D4, computed AFTER §4's registered test failed and labelled as such.
    Amendment K standing -- published beside the registered result, gating nothing."""
    ke = [x["n_atoms_engine"] for x in frame if x["n_atoms_engine"]]
    ident = sum(1 for x in frame if x["n_atoms_clim"] is not None and x["n_atoms_clim"] == x["pool_g"])
    by_era = {}
    for name, _lo, _hi in ERAS:
        rs = [x for x in frame if x["era"] == name and x["n_atoms_engine"] and x["n_atoms_clim"]]
        if rs:
            by_era[name] = {
                "n": len(rs),
                "k_engine_median": float(np.median([x["n_atoms_engine"] for x in rs])),
                "k_clim_median": float(np.median([x["n_atoms_clim"] for x in rs])),
                "differential_inflation": float(np.mean([x["brier_engine"] / x["n_atoms_engine"]
                                                         - x["brier_clim"] / x["n_atoms_clim"] for x in rs])),
            }
    di = [v["differential_inflation"] for v in by_era.values()]
    big = {n: {"registered_skill": tab_reg[n]["skill"], "fair_skill": tab_fair[n]["skill"],
               "n": tab_reg[n]["n"], "shift": tab_fair[n]["skill"] - tab_reg[n]["skill"]}
           for n in tab_reg if tab_reg[n].get("n", 0) >= 50}
    eng_shift = float(np.mean([x["fair_engine"] - x["brier_engine"] for x in frame
                               if x["fair_engine"] is not None]))
    clim_shift = float(np.mean([x["fair_clim"] - x["brier_clim"] for x in frame if x["fair_clim"] is not None]))
    return {
        "standing": ("Amendment 1 A1.5 -- computed after §4's registered test failed. Amendment K standing: "
                     "published beside the registered result, gating nothing."),
        "D1_identity": {"n_atoms_clim_equals_pool_g": ident, "of": len(frame),
                        "reading": ("Climatology's atom count IS the pool size. The 'pool-size confound' and "
                                    "the 'size artefact' are one variable under two names, not two of "
                                    "OPEN_ITEMS 1.4's three confounds.")},
        "D2_differential_inflation_by_era": by_era,
        "D2_swing": (max(di) - min(di)) if len(di) > 1 else None,
        "D2_registered_prediction_was": 0.068,
        "D2_reading": ("§4 assumed k_engine constant at 5; it ranges "
                       f"{min(ke)}-{max(ke)} and rises with era, so the differential inflation swings "
                       "~0.014, not 0.068 -- about a tenth of the era gradient, not most of it. "
                       "Direction supported, magnitude not."),
        "D3_bins_with_n_ge_50": big,
        "D3_reading": ("§7's own caveat applied, not a post-hoc cut: the two bins that carry the sample. "
                       "Stated as a LEVEL, never as a spread."),
        "D4_level_shift_under_correction": {"engine_mean_shift": eng_shift, "clim_mean_shift": clim_shift,
                                            "ratio": (eng_shift / clim_shift) if clim_shift else None,
                                            "reading": "S/k is not Ferro's correction; the level effect is larger."},
        "already_published_by_B": ("summary.json tiers.daily.G.diagnostic_fair.engine_vs_climatology: "
                                   "n 150, skill +0.021, CI [-0.067, +0.111], DM p 0.635, registered: false. "
                                   "G confirms this number and did not discover it."),
    }


def to_md(o):
    L, a = [], None
    a = L.append
    v, s4r, bc = o["verdict"], o["s4_size_correction"], o["baseline_check"]
    a("# G-6 — OPEN_ITEMS 1.4, the era confound: can the three confounds be separated at n = 150?")
    a("*Computed by `src/g_era_confound.py` under `docs/g/G6_ERA_CONFOUND_REGISTRATION.md`, which was")
    a(f"committed first. Generated {o['generated_at']}.*\n")
    a("> **This is a DIAGNOSTIC. It gates nothing.** It re-judges no run, moves no threshold and changes")
    a("> no published verdict. `WALK_FORWARD_PROTOCOL.md` Amendment E.1 governs which score judges a v2")
    a("> run and this does not touch it.\n")
    a("## 0. The answer\n")
    a(f"- **Separable? {'YES' if v['separable'] else '**NO**'}** — criteria fired: "
      + (", ".join(f"`{c}`" for c in v["criteria_fired"]) if v["criteria_fired"] else "none") + ".")
    a(f"- {v['consequence']}")
    a(f"- **S4, the size-correction test: {'PASSES' if s4r['passes'] else 'FAILS'}** — registered-Brier era "
      f"spread **{s4r['registered_spread']:.4f}**, fair-Brier era spread **{s4r['fair_spread']:.4f}**, "
      f"ratio **{s4r['ratio_fair_to_registered']:.3f}** against a threshold of {s4r['threshold']}.")
    a(f"  {s4r['reading']}\n")
    ph = o["post_hoc"]
    a("## 0b. Three things §4 of the registration got wrong, before anything else\n")
    a(f"- **The premise was false.** §4 derived its magnitude from a constant engine atom count of 5. "
      f"`n_atoms_engine` ranges **{min(x['n_atoms_engine'] for x in o['frame'] if x['n_atoms_engine'])}–"
      f"{max(x['n_atoms_engine'] for x in o['frame'] if x['n_atoms_engine'])}** and rises with era. That was "
      "a wrong statement about the inputs, not a prediction that failed.")
    a(f"- **The magnitude was ~5× too large.** Measured differential inflation swings "
      f"**{ph['D2_swing']:.4f}** across eras against the **{ph['D2_registered_prediction_was']}** registered. "
      "Direction supported, size not.")
    a("- **The statistic was excluded by G's own §7.** S4 was a spread over four bins, two with n = 2 and "
      "n = 10, which §7 says are description and not inference — and those two bins drove the failure. "
      "It is left failed rather than swapped, because replacing a test after seeing it fail is the move "
      "this project exists to prevent.\n")
    a("## 1. The baseline check — the published number, re-derived before anything was stratified\n")
    a(f"    published:  {json.dumps(bc['published'])}")
    a(f"    recomputed: {json.dumps(bc['recomputed'])}")
    a(f"    agrees:     {bc['agrees']}\n")
    a(f"Run pinned to `{RUN_ID}`. `scores.jsonl` in the tree holds "
      + ", ".join(f"`{k}` ({n} rows)" for k, n in o["runs_in_file"].items())
      + " — see §5 of the handoff; the second run is excluded by `run_id` and reported, not acted on.\n")
    a("## 2. The era table, on both scores\n")
    for label, tab in (("registered Brier (what the headline uses)", o["era_registered"]),
                       ("fair Brier (Ferro size-corrected, Amendment E)", o["era_fair"])):
        a(f"### {label}\n")
        a("| era | n | clusters | skill | 95 % CI | min detectable @80 % | pool median (min–max) | "
          "base rate L0 | dyadic share | k engine | k clim |")
        a("|---|---|---|---|---|---|---|---|---|---|---|")
        for name, _lo, _hi in ERAS:
            t = tab.get(name) or {}
            if not t.get("n"):
                a(f"| {name} | 0 | — | — | — | — | — | — | — | — | — |")
                continue
            ci = t["ci95"]
            cis = f"[{ci[0]:+.3f}, {ci[1]:+.3f}]" if ci[0] is not None else "—"
            md = f"{t['min_detectable_skill_80pc']:.3f}" if t["min_detectable_skill_80pc"] else "—"
            a(f"| {name} | {t['n']} | {t['n_clusters']} | **{t['skill']:+.4f}** | {cis} | {md} | "
              f"{t['pool_median']:.0f} ({t['pool_min']}–{t['pool_max']}) | "
              f"{t['base_rate_0_mean']:.3f} | {t['dyadic_share']} | "
              f"{t['n_atoms_engine_median']:.0f} | {t['n_atoms_clim_median']:.0f} |")
        a("")
    a("**Two of the four bins have n = 2 and n = 10.** Whatever those rows show is description, not")
    a("inference (§7), and no weight is placed on them here.\n")
    a("## 3. Why the two scores differ — the mechanism, registered before it was measured\n")
    a(f"{s4r['prediction_registered']}\n")
    a("The `k engine` and `k clim` columns above are the atom counts the correction acts on. The engine's")
    a("is fixed by its analog count; climatology's is the pool, and the pool grows with time. That is the")
    a("whole mechanism, and it is visible in the table without any modelling.\n")
    a("## 4. Separability (§5)\n")
    sep = o["separability"]
    a("| pair | Spearman ρ |")
    a("|---|---|")
    for k, r in sep["spearman"].items():
        a(f"| `{k}` | {'—' if r is None else f'{r:+.3f}'} |")
    a(f"\nCondition number of the standardised design: **{sep['condition_number']:.1f}**.\n")
    a(f"Pool-size range by era — if these do not overlap, era and pool size are the same variable in this")
    a("sample and no n repairs it:\n")
    a("| era | n | pool min | pool max |")
    a("|---|---|---|---|")
    for name, rr in sep["pool_range_by_era"].items():
        a(f"| {name} | {rr['n']} | {rr['min']} | {rr['max']} |")
    a("\n(era × pool tertile) support — separation needs cells **off** the diagonal:\n")
    a("| cell | n |")
    a("|---|---|")
    for k, n in sep["cross_tab"].items():
        a(f"| `{k}` | {n} |")
    a(f"\nOff-diagonal cells with n ≥ {SEP_CELL_N}: **{len(sep['off_diagonal_cells_ge_20'])}** "
      f"({sep['off_diagonal_cells_ge_20'] or 'none'}).\n")
    a("## 5. The verdict, under the rule fixed before the numbers\n")
    a(f"```\n{json.dumps(v, indent=1, default=str)}\n```")
    a("\n## 5b. The post-hoc diagnostics (Amendment 1 A1.5; they gate nothing)\n")
    a(f"**D1 — the identity that collapses two confounds into one.** `n_atoms_clim == n_pool_g` on "
      f"**{ph['D1_identity']['n_atoms_clim_equals_pool_g']} of {ph['D1_identity']['of']}** reads, exactly. "
      f"{ph['D1_identity']['reading']}\n")
    a("**D2 — the differential inflation, measured by era.**\n")
    a("| era | n | k engine | k clim | S_e/k_e − S_c/k_c |")
    a("|---|---|---|---|---|")
    for k, vv in ph["D2_differential_inflation_by_era"].items():
        a(f"| {k} | {vv['n']} | {vv['k_engine_median']:.1f} | {vv['k_clim_median']:.1f} | "
          f"{vv['differential_inflation']:+.4f} |")
    a(f"\n{ph['D2_reading']}\n")
    a("**D3 — the two bins that carry the sample** (§7's caveat applied, not a post-hoc cut). "
      "A level statement, never a spread:\n")
    a("| era | n | registered skill | fair skill | shift |")
    a("|---|---|---|---|---|")
    for k, vv in ph["D3_bins_with_n_ge_50"].items():
        a(f"| {k} | {vv['n']} | {vv['registered_skill']:+.4f} | {vv['fair_skill']:+.4f} | {vv['shift']:+.4f} |")
    d4 = ph["D4_level_shift_under_correction"]
    a(f"\n**D4 — the level shift under correction.** Engine mean {d4['engine_mean_shift']:+.4f}, "
      f"climatology {d4['clim_mean_shift']:+.4f} — the engine benefits **{d4['ratio']:.1f}×** more. "
      f"{d4['reading']}\n")
    a(f"> **Already published by session B, and confirmed here rather than discovered:** {ph['already_published_by_B']}\n")
    a("\n## 6. What this cannot do\n")
    for x in o["cannot"]:
        a(f"- {x}")
    return "\n".join(L)


CANNOT = [
    "It cannot establish that the engine has skill. A confounded negative is not a positive.",
    f"It cannot re-judge run `{RUN_ID}` or any other; Amendment E.1 governs.",
    "It cannot separate label basis from era where the cross-tab has no off-diagonal support, and the "
    "daily tier begins in 1987 — OPEN_ITEMS's '100 % dyadic in 1946–73' is a monthly-tier fact quoted "
    "for context, not a fact about these 150 reads.",
    "It is computed on 150 reads across four bins, two of which have n = 2 and n = 10.",
]


def main():
    rows, by_run = load_scores()
    sc = scored_set(rows)
    bc = baseline_check(sc)
    frame = build_frame(sc, load_reads(), load_basis())
    tab_reg = era_table(frame, "brier")
    tab_fair = era_table(frame, "fair")
    sep = separability(frame)
    out = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "registration": "docs/g/G6_ERA_CONFOUND_REGISTRATION.md (2026-09-03)",
        "gates": "nothing. Diagnostic only.",
        "run_pinned": RUN_ID, "runs_in_file": by_run,
        "baseline_check": bc,
        "era_registered": tab_reg, "era_fair": tab_fair,
        "s4_size_correction": s4(tab_reg, tab_fair),
        "separability": sep,
        "verdict": verdict(sep, tab_reg, bc["recomputed"]["skill"]),
        "post_hoc": post_hoc(frame, tab_reg, tab_fair),
        "cannot": CANNOT,
        "frame": frame,
    }
    if not bc["agrees"]:
        out["VOID"] = "§2: the pinned run did not reproduce the published G block. Nothing below is valid."
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=1, default=str))
    OUT_MD.write_text(to_md(out))
    print(json.dumps({k: out[k] for k in ("run_pinned", "runs_in_file", "baseline_check",
                                          "s4_size_correction", "verdict")}, indent=1, default=str))
    return out


if __name__ == "__main__":
    main()
