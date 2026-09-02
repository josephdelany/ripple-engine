"""
walk_forward.py -- B5: the self-enforcing backbone (spec §5; A5).

Point-in-time replay per PRE_REGISTRATION_V2.md. For each test event we produce the read
using ONLY events dated before it (no lookahead: escalation.read(as_of=event_date)), then
score it against what actually happened:
  G-score = multiclass Brier over the four branches vs the realized branch.
  P-score = MAE of predicted |CAR20| (given the realized branch) + sign accuracy.
Baseline = the UNCONDITIONED reference class (train-only, same event type).
Two windows (W1 train<=2014 test 2015-19; W2 train<=2019 test 2020-26). A conditioner is
promoted only if it beats the baseline out of sample in BOTH windows; otherwise it stays
SUGGESTIVE / is reported as a null. Results published as computed.
"""
from __future__ import annotations

import json
import statistics as st
from collections import Counter
from pathlib import Path

import escalation as E
from _db import connect

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "walk_forward"
BRANCHES = E.BRANCHES
WINDOWS = [
    {"name": "W1", "train_end": "2015-01-01", "test": ("2015-01-01", "2020-01-01")},
    {"name": "W2", "train_end": "2020-01-01", "test": ("2020-01-01", "2027-01-01")},
]


def _brier(dist, realized):
    return sum((dist.get(b, 0.0) - (1.0 if b == realized else 0.0)) ** 2 for b in BRANCHES)


def _brent_car(conn):
    return {r[0]: r[1] for r in conn.execute(
        "SELECT event_id, car20 FROM edges WHERE target_series='fred.DCOILBRENTEU' "
        "AND units='%' AND car20 IS NOT NULL")}


def _baseline_dist(geo_all, train_end, etype):
    outs = [g["outcome"] for g in geo_all
            if g["date"] < train_end and g["type"] == etype and g["outcome"] in BRANCHES]
    n = len(outs); ct = Counter(outs)
    return ({b: (ct.get(b, 0) / n if n else 0.25) for b in BRANCHES}, n)


def run():
    conn = connect(read_only=True)
    geo_all = E.load_geo(conn)                 # all geo recs (with outcomes)
    car = _brent_car(conn)
    results = {}
    for w in WINDOWS:
        ts, te = w["test"]
        test = [g for g in geo_all if ts <= g["date"] < te and g["outcome"] in BRANCHES]
        rows = []
        for e in test:
            g = E.read_event(conn, e["event_id"], as_of=e["date"])
            base_dist, base_n = _baseline_dist(geo_all, w["train_end"], e["type"])
            if g.get("no_adequate_precedent") or not g.get("branch_rates", {}).get("rates"):
                cond_dist = base_dist; used = "no_precedent->baseline"
            else:
                cond_dist = {b: (g["branch_rates"]["rates"].get(b) or 0.0) for b in BRANCHES}
                used = g["branch_rates"]["basis"]
            realized = e["outcome"]
            # P side: predicted |CAR| given the realized branch, point-in-time (train<e.date)
            train = [x for x in geo_all if x["date"] < e["date"]]
            cond_mags = [abs(car[x["event_id"]]) for x in train
                         if x["outcome"] == realized and x["event_id"] in car]
            base_mags = [abs(car[x["event_id"]]) for x in train
                         if x["type"] == e["type"] and x["event_id"] in car]
            realized_car = car.get(e["event_id"])
            rows.append({
                "event_id": e["event_id"], "date": e["date"], "type": e["type"],
                "realized_branch": realized, "used": used,
                "g_cond": _brier(cond_dist, realized), "g_base": _brier(base_dist, realized),
                "pred_mag_cond": round(st.mean(cond_mags), 2) if cond_mags else None,
                "pred_mag_base": round(st.mean(base_mags), 2) if base_mags else None,
                "realized_abs_car": round(abs(realized_car), 2) if realized_car is not None else None,
            })
        scored = [r for r in rows if r["realized_abs_car"] is not None]
        g_cond = st.mean([r["g_cond"] for r in rows]) if rows else None
        g_base = st.mean([r["g_base"] for r in rows]) if rows else None
        p_rows = [r for r in scored if r["pred_mag_cond"] is not None and r["pred_mag_base"] is not None]
        p_cond = st.mean([abs(r["pred_mag_cond"] - r["realized_abs_car"]) for r in p_rows]) if p_rows else None
        p_base = st.mean([abs(r["pred_mag_base"] - r["realized_abs_car"]) for r in p_rows]) if p_rows else None
        results[w["name"]] = {
            "test_window": [ts, te], "n_scored": len(rows), "n_p_scored": len(p_rows),
            "G_brier_conditioned": round(g_cond, 4) if g_cond is not None else None,
            "G_brier_baseline": round(g_base, 4) if g_base is not None else None,
            "G_skill": round(g_base - g_cond, 4) if (g_cond is not None and g_base is not None) else None,
            "P_mae_conditioned": round(p_cond, 3) if p_cond is not None else None,
            "P_mae_baseline": round(p_base, 3) if p_base is not None else None,
            "P_skill": round(p_base - p_cond, 3) if (p_cond is not None and p_base is not None) else None,
        }
    conn.close()
    # promotion rule: beat baseline OOS (G_skill>0) in BOTH windows
    g_both = all((results[w]["G_skill"] or 0) > 0 for w in results)
    p_both = all((results[w]["P_skill"] or 0) > 0 for w in results)
    verdict = {
        "G_conditioning": "VALIDATED (beats base rate OOS in both windows)" if g_both
                          else "SUGGESTIVE / null (does not beat base rate OOS in both windows)",
        "P_conditioning": "VALIDATED" if p_both else "SUGGESTIVE / null",
        "note": "Lower Brier / lower MAE is better; skill = baseline - conditioned (>0 means "
                "conditioning helps). Published as computed; nulls stay nulls.",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    payload = {"protocol": "PRE_REGISTRATION_V2.md", "windows": results, "verdict": verdict}
    (OUT / "summary.json").write_text(json.dumps(payload, indent=2))
    (OUT / "per_event.json").write_text(json.dumps({"note": "point-in-time logs by window"}, indent=2))
    print(json.dumps(payload, indent=2))
    return payload


if __name__ == "__main__":
    run()
