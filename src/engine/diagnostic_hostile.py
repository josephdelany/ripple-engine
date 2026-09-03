"""
diagnostic_hostile.py -- WALK_FORWARD_PROTOCOL.md Amendment K (2026-09-03): the hostility diagnostic.

Recomputes the daily-tier G comparisons on the G-SCORABLE reads only -- hostility in {hostile,
hostile_unattributed} per OUTCOME_MAPPING.md Amendment 3 A3.3, coded by session F in data/spine/CLASS_AUDIT.md
before any count under it. non_hostile and ambiguous return no_independent_outcome, so the G target is
UNDEFINED for those reads.

Reads the SEALED files and never re-scores (A3.5): the engine's, frozen's and persistence's forecasts are
taken as sealed; CLIMATOLOGY IS RE-ESTIMATED on the reduced pool (each read's own point-in-time
g_pool_ids with its aligned G_labels, minus the pool members that are not G-scorable); random analogs are
re-drawn from the reduced pool at the same k and per-event seed.

Gates nothing (K.1). Writes summary.json -> tiers.daily.G.diagnostic_hostile.

Run:  python3 src/engine/diagnostic_hostile.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from engine import scoring as SC          # noqa: E402
from engine import inference as INF       # noqa: E402
import walk as W                          # noqa: E402

WF = ROOT / "data" / "walk_forward"
AUDIT = ROOT / "data" / "spine" / "CLASS_AUDIT.md"
SCORABLE = ("hostile", "hostile_unattributed")
NOT_SCORABLE = ("non_hostile", "ambiguous")
# the section-3 row of CLASS_AUDIT.md, as tests/test_hostility.py parses it (session F's format)
ROW = re.compile(r"^\|\s*`(?P<eid>[a-z0-9_]+)`\s*\|\s*(?P<date>\d{4}-\d{2}-\d{2})\s*\|\s*"
                 r"\*\*(?P<hostility>\w+)\*\*(?P<flags>[^|]*)\|")


def hostility_map(path=AUDIT):
    """{event_id: hostility} from session F's hand coding. The audit is the register; this only reads it."""
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line.strip())
        if m:
            out[m.group("eid")] = m.group("hostility")
    return out


def _rows(name, run_id):
    return [r for r in (json.loads(l) for l in (WF / name).open(encoding="utf-8") if l.strip())
            if r["run_id"] == run_id]


def _reduced_climatology(read, keep):
    """Amendment K.2: the read's own point-in-time pool, minus members that are not G-scorable."""
    ids = read["baselines"]["random_analogs"]["g_pool_ids"]
    labs = read["baselines"]["climatology"]["G_labels"] or []
    if len(ids) != len(labs):
        return None, []
    pairs = [(i, l) for i, l in zip(ids, labs) if keep(i)]
    if not pairs:
        return None, []
    kept = [l for _, l in pairs]
    return {b: kept.count(b) / len(kept) for b in SC.LEVELS}, kept


def _reduced_random(read, keep, level_of):
    """Random analogs re-drawn from the reduced pool: same k, same per-event seed, same number of draws."""
    b = read["baselines"]["random_analogs"]
    ids = [i for i in b["g_pool_ids"] if keep(i) and level_of(i) in SC.LEVELS]
    if not ids:
        return None
    rng = np.random.default_rng(b["seed"])
    draws = []
    for _ in range(b["draws"]):
        pick = rng.choice(len(ids), size=min(b["k"], len(ids)), replace=False)
        outs = [level_of(ids[i]) for i in pick]
        draws.append({x: outs.count(x) / len(outs) for x in SC.LEVELS})
    return draws


def compute(run_id=None):
    summary = json.loads((WF / "summary.json").read_text())
    run_id = run_id or summary["run_id"]
    reads = {r["event_id"]: r for r in _rows("reads.jsonl", run_id)}
    scores = _rows("scores.jsonl", run_id)
    host = hostility_map()
    # the published scored G set: exactly summary.json tiers.daily.G.engine_vs.climatology.n
    sel = [s for s in scores if s["tier"] == "daily" and s.get("burn_in_ok")
           and (s["scores"].get("engine") or {}).get("G") and (s["scores"].get("climatology") or {}).get("G")]
    level_of = {s["event_id"]: s["outcome"]["level"] for s in scores if s["outcome"].get("level")}
    # a pool member is G-scorable when F coded it scorable; an event F did not code (a non-geopolitical
    # class) never appears in a G pool, so an unknown id is kept only if it carries a level.
    keep = lambda eid: host.get(eid, "hostile") in SCORABLE
    retained = [s for s in sel if keep(s["event_id"])]
    dropped = [s for s in sel if not keep(s["event_id"])]

    rows = {}                                   # forecaster -> list of (brier, rps) aligned with `retained`
    dates, kept_n, clim_n = [], [], []
    for s in retained:
        r = reads.get(s["event_id"])
        lv = s["outcome"]["level"]
        clim, kept = _reduced_climatology(r, keep) if r else (None, [])
        rnd = _reduced_random(r, keep, lambda i: level_of.get(i)) if r else None
        if clim is None:
            continue
        dates.append(s["date"]); kept_n.append(len(kept)); clim_n.append(len(r["baselines"]["climatology"]["G_labels"] or []))
        rows.setdefault("engine", []).append((SC.brier(r["engine"]["G"], lv), SC.rps(r["engine"]["G"], lv)))
        rows.setdefault("frozen", []).append((SC.brier(r["frozen"]["G"], lv), SC.rps(r["frozen"]["G"], lv)))
        pg = (r["baselines"].get("persistence") or {}).get("G")
        rows.setdefault("persistence", []).append((SC.brier(pg, lv), SC.rps(pg, lv)) if pg else (None, None))
        rows.setdefault("climatology", []).append((SC.brier(clim, lv), SC.rps(clim, lv)))
        rows.setdefault("random_analogs", []).append(
            (float(np.mean([SC.brier(d, lv) for d in rnd])), float(np.mean([SC.rps(d, lv) for d in rnd]))) if rnd else (None, None))

    mb = W._mean_block(dates, W.REGISTERED["cluster_days"])
    lag = max(int(round(mb)) - 1, 0)

    def block(ref, idx):
        pairs = [(a[idx], b[idx]) for a, b in zip(rows["engine"], rows[ref]) if a[idx] is not None and b[idx] is not None]
        if len(pairs) < 3:
            return {"n": len(pairs), "skill": None}
        e = np.array([p[0] for p in pairs]); c = np.array([p[1] for p in pairs])
        ci = INF.bootstrap_ci(lambda ix: None if c[ix].mean() == 0 else 1 - e[ix].mean() / c[ix].mean(),
                              len(pairs), n_boot=W.REGISTERED["n_boot"], mean_block=mb)
        dm = INF.dm_test(e, c, h=1, lag=lag)
        return {"n": len(pairs), "engine_mean": float(e.mean()), "ref_mean": float(c.mean()),
                "skill": ci["estimate"], "ci95": [ci["lo"], ci["hi"]], "dm_hln": dm.get("dm_hln"),
                "dm_p": dm.get("p_value"), "ref": ref}

    lv0 = lambda rs: (sum(1 for s in rs if s["outcome"]["level"] == "0"), len(rs))
    k_all, n_all = lv0(sel); k_ret, n_ret = lv0(retained)
    out = {
        "registered": False,
        "what": "the daily-tier G comparisons on the G-scorable reads only (hostility in hostile / "
                "hostile_unattributed); climatology re-estimated on the reduced pool, random analogs re-drawn "
                "from it; engine, frozen and persistence forecasts taken AS SEALED",
        "amendment": "WALK_FORWARD_PROTOCOL.md Amendment K (2026-09-03); exclusion set OUTCOME_MAPPING.md "
                     "Amendment 3 A3.3, coded in data/spine/CLASS_AUDIT.md before any count under it",
        "gates": "nothing -- §3 and §7 are untouched and every verdict is unchanged",
        "derived_from_run": run_id, "computed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "n_published": len(sel), "n_retained": len(retained), "n_dropped": len(dropped),
        "dropped_by_hostility": dict(Counter(host.get(s["event_id"], "uncoded") for s in dropped)),
        "retained_by_hostility": dict(Counter(host.get(s["event_id"], "uncoded") for s in retained)),
        "level0_share_published": {"k": k_all, "n": n_all, "pct": round(100 * k_all / n_all, 1)},
        "level0_share_retained": {"k": k_ret, "n": n_ret, "pct": round(100 * k_ret / n_ret, 1)},
        "climatology_pool": {"mean_size_published": round(float(np.mean(clim_n)), 1),
                             "mean_size_reduced": round(float(np.mean(kept_n)), 1),
                             "note": "the baseline moves, not only the engine's score -- Amendment K.2"},
        "dependence": {"cluster_days": W.REGISTERED["cluster_days"], "mean_block": round(mb, 2), "hac_lag": lag},
        "brier": {ref: block(ref, 0) for ref in ("climatology", "frozen", "random_analogs", "persistence")},
        "rps": {ref: block(ref, 1) for ref in ("climatology", "frozen", "random_analogs", "persistence")},
        "limit": (f"n falls from {len(sel)} to {len(retained)}, so every interval widens; min_tier_n "
                  f"{W.REGISTERED['min_tier_n']} is still met but the measured minimum detectable skill at the "
                  "published n = 150 was already 0.127. A diagnostic on a SEALED run, not a new run, and not "
                  "the run the paper reports."),
    }
    return out, summary


def main():
    out, summary = compute()
    summary["tiers"]["daily"]["G"]["diagnostic_hostile"] = out
    (WF / "summary.json").write_text(json.dumps(summary, indent=1, default=str))
    print(json.dumps({k: v for k, v in out.items() if k not in ("what", "amendment", "limit", "gates")}, indent=1))


if __name__ == "__main__":
    main()
