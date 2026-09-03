"""
abnormal_price.py -- WALK_FORWARD_PROTOCOL.md Amendment O (2026-09-03): the event walk's price target,
recomputed as an abnormal return, from the SEALED run.

Answers docs/audit/01_TIER1_design_defects.md A1 on the walk the paper actually reports. The grid arm
already found (docs/ABNORMAL_RETURN_RESULT.md) that its decisive loss to climatology was a property of the
raw-return target; the event walk still scores raw returns, so the same test has to run here.

WHY THIS NEEDS NO RE-RUN. Every sealed read carries the IDENTITIES of the analogs that form its P forecast
(items[*].P_ids, engine.P.ids) and its point-in-time climatology pool. Retrieval is label-free and was
already performed. So the target is changed by substituting each analog's outcome with its abnormal
counterpart and re-scoring. Which analogs were retrieved, their weights, the Hedge weights and the cluster
structure are held EXACTLY as sealed.

Run:  python3 src/engine/abnormal_price.py
"""
from __future__ import annotations

import json
import sqlite3
import sys
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
DB = ROOT / "data" / "oil.db"

EST_WINDOW = 250      # O.2
EST_GAP = 21
EST_MIN = 100
DAILY_SERIES = "fred.DCOILBRENTEU"     # the daily tier's price series
HORIZON_TD = 20


def _rows(name, run_id):
    return [r for r in (json.loads(l) for l in (WF / name).open(encoding="utf-8") if l.strip())
            if r["run_id"] == run_id]


def abnormal_map(dates_by_event):
    """O.2: AR = chg_pct - 20 * alpha * 100, alpha the mean daily log return on the 250 trading days ending
    21 before the event. Constant-mean model (Brown & Warner 1985): the daily tier's target IS crude, so
    there is no exogenous oil-market factor distinct from the asset. Returns {event_id: alpha} and drops."""
    conn = sqlite3.connect(DB)
    s = pd.read_sql("select obs_date, value from observations where series_id=? and value is not null "
                    "order by obs_date", conn, params=[DAILY_SERIES])
    s["obs_date"] = pd.to_datetime(s["obs_date"])
    idx = s["obs_date"].to_numpy()
    lv = np.log(s["value"].to_numpy(float))
    dlv = np.diff(lv, prepend=np.nan)
    alpha, dropped = {}, 0
    for eid, d in dates_by_event.items():
        pos = int(np.searchsorted(idx, np.datetime64(pd.Timestamp(d)), side="left"))
        e1, e0 = pos - EST_GAP, pos - EST_GAP - EST_WINDOW
        if e0 < 1:
            dropped += 1
            continue
        seg = dlv[e0:e1]
        m = np.isfinite(seg)
        if m.sum() < EST_MIN:
            dropped += 1
            continue
        alpha[eid] = float(seg[m].mean())
    return alpha, dropped


def compute(run_id=None):
    summary = json.loads((WF / "summary.json").read_text())
    run_id = run_id or summary["run_id"]
    reads = {r["event_id"]: r for r in _rows("reads.jsonl", run_id)}
    scores = _rows("scores.jsonl", run_id)
    by_id = {s["event_id"]: s for s in scores}

    dates = {s["event_id"]: s["date"] for s in scores}
    alpha, n_dropped = abnormal_map(dates)

    # raw outcome per event, and its abnormal counterpart
    raw = {s["event_id"]: (s["outcome"] or {}).get("chg_pct") for s in scores}
    AR = {e: (v - HORIZON_TD * alpha[e] * 100.0)
          for e, v in raw.items() if v is not None and e in alpha}

    sel = [s for s in scores if s["tier"] == "daily" and s.get("burn_in_ok")
           and (s["scores"].get("engine") or {}).get("P") and s["event_id"] in AR]
    sel.sort(key=lambda s: (s["date"], s["event_id"]))

    rows, dates_kept, n_atom_dropped = [], [], 0
    for s in sel:
        r = reads[s["event_id"]]
        y = AR[s["event_id"]]
        ep = (r["engine"] or {}).get("P") or {}
        ids, wts = ep.get("ids") or [], ep.get("weights") or []
        atoms = [(AR[i], w) for i, w in zip(ids, wts) if i in AR]
        n_atom_dropped += len(ids) - len(atoms)
        if not atoms:
            continue
        pool_ids = (r["baselines"]["random_analogs"] or {}).get("p_pool_ids") or []
        pool = [AR[i] for i in pool_ids if i in AR]
        if len(pool) < 3:
            continue
        v = np.array([a for a, _ in atoms]); w = np.array([b for _, b in atoms], float)
        eng = SC.crps(v, y, w)
        clim = SC.crps(np.array(pool), y)
        pers = SC.crps(np.array([0.0]), y)          # no-change is zero in either space (O.3)
        b = r["baselines"]["random_analogs"]
        rng = np.random.default_rng(b["seed"] + 1)
        k = min(b["k"], len(pool))
        rnd = float(np.mean([SC.crps(np.array([pool[i] for i in rng.choice(len(pool), k, replace=False)]), y)
                             for _ in range(b["draws"])]))
        fz = (r["frozen"] or {}).get("P") or {}
        fids, fwts = fz.get("ids") or [], fz.get("weights") or []
        fat = [(AR[i], wq) for i, wq in zip(fids, fwts) if i in AR]
        frz = SC.crps(np.array([a for a, _ in fat]), y, np.array([b_ for _, b_ in fat], float)) if fat else np.nan
        rows.append({"event_id": s["event_id"], "date": s["date"], "y_ar": y, "y_raw": raw[s["event_id"]],
                     "engine": eng, "climatology": clim, "persistence": pers, "random_analogs": rnd,
                     "frozen": frz, "n_atoms": len(atoms)})
        dates_kept.append(s["date"])

    if len(rows) < W.REGISTERED["min_tier_n"]:
        return {"note": f"only {len(rows)} scorable reads", "n": len(rows)}

    mb = W._mean_block(dates_kept, W.REGISTERED["cluster_days"])
    lag = max(int(round(mb)) - 1, 0)
    e = np.array([r["engine"] for r in rows])

    def block(ref):
        c = np.array([r[ref] for r in rows], float)
        m = np.isfinite(e) & np.isfinite(c)
        x, y_ = e[m], c[m]
        ci = INF.bootstrap_ci(lambda ix: None if y_[ix].mean() == 0 else 1 - x[ix].mean() / y_[ix].mean(),
                              len(x), n_boot=W.REGISTERED["n_boot"], mean_block=mb)
        dm = INF.dm_test(x, y_, h=1, lag=lag)
        return {"n": int(len(x)), "engine_mean": float(x.mean()), "ref_mean": float(y_.mean()),
                "skill": ci["estimate"], "ci95": [ci["lo"], ci["hi"]],
                "dm_hln": dm.get("dm_hln"), "dm_p": dm.get("p_value"), "ref": ref, "score": "crps"}

    vs = {ref: block(ref) for ref in ("climatology", "persistence", "random_analogs", "frozen")}

    fam = ["engine", "frozen", "random_analogs", "persistence"]
    base = np.array([r["climatology"] for r in rows], float)
    d = np.column_stack([base - np.array([r[f] for r in rows], float) for f in fam])
    ok = np.all(np.isfinite(d), axis=1)
    spa = INF.spa(d[ok], n_boot=W.REGISTERED["n_spa_boot"], mean_block=mb)
    spa["best_model"] = fam[spa["best_model"]]; spa["models"] = fam; spa["benchmark"] = "climatology"

    nm = [f"vs_{k}" for k, v in vs.items() if v.get("dm_p") is not None]
    ps = [v["dm_p"] for v in vs.values() if v.get("dm_p") is not None]
    bh = INF.bh_fdr(ps, q=0.05)

    pub = summary["tiers"]["daily"]["P"]["engine_vs"]
    return {
        "amendment": "WALK_FORWARD_PROTOCOL.md Amendment O (2026-09-03), registered in commit 2151a71 "
                     "before this module existed; answers docs/audit/01_TIER1_design_defects.md A1",
        "registered": True, "standing": "DIAGNOSTIC -- published beside the registered raw-return numbers, "
                                        "which are NOT withdrawn; cannot move a §7 verdict",
        "derived_from_run": run_id, "no_rerun": "retrieval, analog identities, weights, Hedge weights and "
                                                "the cluster structure are held exactly as sealed (O.1)",
        "computed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model": {"form": "constant_mean (Brown & Warner 1985)", "series": DAILY_SERIES,
                  "estimation_window_td": EST_WINDOW, "gap_td": EST_GAP, "min_obs": EST_MIN,
                  "n_events_without_a_model": n_dropped, "n_analog_atoms_dropped": n_atom_dropped},
        "n_scored": len(rows), "n_published_raw": pub["climatology"]["n"],
        "dependence": {"mean_block": round(mb, 2), "hac_lag": lag},
        "raw_vs_abnormal": {ref: {"raw_skill": (pub.get(ref) or {}).get("skill"),
                                  "raw_dm_p": (pub.get(ref) or {}).get("dm_p"),
                                  "abnormal_skill": vs[ref]["skill"], "abnormal_dm_p": vs[ref]["dm_p"]}
                            for ref in vs},
        "engine_vs": vs, "spa": spa,
        "fdr": {"names": nm, "p": ps, "bh": bh,
                "note": "§6 BH-FDR across this diagnostic's own family; a comparison that does not survive "
                        "is not a finding, on this arm exactly as on the raw one"},
    }


def main():
    out = compute()
    summary = json.loads((WF / "summary.json").read_text())
    summary["tiers"]["daily"]["P"]["diagnostic_abnormal"] = out
    (WF / "summary.json").write_text(json.dumps(summary, indent=1, default=str))
    print(json.dumps({k: out[k] for k in ("n_scored", "n_published_raw", "model", "raw_vs_abnormal", "spa",
                                          "fdr") if k in out}, indent=1, default=str)[:3000])


if __name__ == "__main__":
    main()
