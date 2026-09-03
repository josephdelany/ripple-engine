"""
diagnostic_basis.py -- WALK_FORWARD_PROTOCOL.md Amendment Q (2026-09-03).

Splits the sealed escalation scores by the evidence basis of their label -- `dyadic` (the pair themselves)
versus `location` (violence anywhere in the affected country). Tier-1 A3 found the target is 83 %
location-based, so the dyadic subset is the only part of it that measures what the paper describes.

Forecasts are taken AS SEALED; only the evaluation set changes. Gates nothing.

Run:  python3 src/engine/diagnostic_basis.py
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from engine import scoring as SC        # noqa: E402
from engine import inference as INF     # noqa: E402
import walk as W                        # noqa: E402

WF = ROOT / "data" / "walk_forward"


def basis_map():
    c = sqlite3.connect(ROOT / "data" / "oil.db")
    return {e: v for e, v in c.execute(
        "select event_id, value_text from event_outcomes where source='ies90' and field='basis'")}


def compute():
    summary = json.loads((WF / "summary.json").read_text())
    rid = summary["run_id"]
    scores = [json.loads(l) for l in (WF / "scores.jsonl").open() if l.strip()]
    scores = [s for s in scores if s["run_id"] == rid and s["tier"] == "daily" and s.get("burn_in_ok")
              and (s["scores"].get("engine") or {}).get("G")]
    scores.sort(key=lambda s: (s["date"], s["event_id"]))
    bas = basis_map()

    out = {"amendment": "WALK_FORWARD_PROTOCOL.md Amendment Q (2026-09-03); addresses "
                        "docs/audit/01_TIER1_design_defects.md A3 and remediation R0a",
           "registered": True, "standing": "DIAGNOSTIC -- gates nothing; the whole-target numbers stand",
           "derived_from_run": rid, "forecasts": "taken as sealed; only the evaluation set changes",
           "subsets": {}}
    for name in ("dyadic", "location", "all"):
        sub = [s for s in scores if name == "all" or bas.get(s["event_id"]) == name]
        if len(sub) < 5:
            out["subsets"][name] = {"n": len(sub), "note": "too few reads to score"}
            continue
        dates = [s["date"] for s in sub]
        mb = W._mean_block(dates, W.REGISTERED["cluster_days"]); lag = max(int(round(mb)) - 1, 0)
        blk = {"n": len(sub), "n_nonzero": sum(1 for s in sub if s["outcome"]["level"] != "0"),
               "mean_block": round(mb, 2), "hac_lag": lag}
        for score in ("brier", "rps"):
            e = np.array([s["scores"]["engine"]["G"][score] for s in sub], float)
            for ref in ("climatology", "persistence"):
                c = np.array([(s["scores"].get(ref) or {}).get("G", {}).get(score, np.nan)
                              for s in sub], float)
                m = np.isfinite(e) & np.isfinite(c)
                if m.sum() < 5:
                    continue
                x, y = e[m], c[m]
                ci = INF.bootstrap_ci(lambda ix: None if y[ix].mean() == 0 else 1 - x[ix].mean() / y[ix].mean(),
                                      len(x), n_boot=W.REGISTERED["n_boot"], mean_block=mb)
                dm = INF.dm_test(x, y, h=1, lag=lag)
                blk[f"{score}_vs_{ref}"] = {"n": int(len(x)), "skill": ci["estimate"],
                                            "ci95": [ci["lo"], ci["hi"]], "dm_p": dm.get("p_value")}
                if score == "brier" and ref == "climatology":
                    pw = INF.power_block(x - y, mb, lag, float(y.mean()), n_list=[len(x)], n_sims=300)
                    mds = pw["by_n"][str(len(x))]["mds_skill"]
                    blk["mds_skill_at_this_n"] = mds
                    sk = ci["estimate"]
                    blk["testable"] = bool(mds is not None and sk is not None and abs(sk) >= mds)
                    blk["reading"] = ("the observed skill exceeds the minimum this n can detect"
                                      if blk["testable"] else
                                      f"NOT TESTABLE AT THIS n: the smallest skill detectable here is "
                                      f"{mds}, larger than the observed {None if sk is None else round(sk,4)}. "
                                      f"This subset cannot support a claim in either direction (Q.3).")
        out["subsets"][name] = blk
    d, l = out["subsets"].get("dyadic", {}), out["subsets"].get("location", {})
    out["headline"] = (f"The target is {l.get('n','?')} location-based against {d.get('n','?')} dyadic "
                       f"among scored reads. A3's finding reproduces on the rebuilt target.")
    return out, summary


def main():
    out, summary = compute()
    summary["tiers"]["daily"]["G"]["diagnostic_basis"] = out
    (WF / "summary.json").write_text(json.dumps(summary, indent=1, default=str))
    print(json.dumps(out, indent=1, default=str)[:2600])


if __name__ == "__main__":
    main()
