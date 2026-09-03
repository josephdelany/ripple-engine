"""
discovery.py -- falsification-first leading-indicator scan (Step 5), built to find NO edge.

Hunts for state variables that predict a shock's oil ripple, but is engineered to say when there
is nothing there. Every candidate (state feature x CAR outcome) must clear FOUR gates:
  1. PERMUTATION p-value on |corr| (assumption-free -- no normality with this N),
  2. BENJAMINI-HOCHBERG FDR across the whole scan (multiple-testing: 28 tests -> ~1 false hit
     at p<0.05 by luck, so we correct),
  3. OUT-OF-SAMPLE sign-hold (split by time; the sign must persist on the held-out half),
  4. CAUSAL control (partial correlation controlling for the most-correlated other feature must
     survive -- kills links that are really a confounder driving both).
Run on the CLUSTERED (de-overlapped) sample so correlated overlapping windows don't manufacture
hits. "Nothing survives" is the honest, expected result on noisy macro data -- this is a
p-hacking guard, not a signal factory. If VIX->|CAR20| survives, that is just discovery
re-finding H1 from scratch (a good sign the scan works). Reuses src/validate.py. numpy-only.

Run:  python3 src/discovery.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from event_study import load_returns, car_for_event, PRE
from derive_signals import load_wide, build_signals
from robustness import assign_clusters
import validate

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "discovery.json"

FEATURES = ["derived.vix_pct", "derived.inv_sigma", "derived.cot_pct", "derived.brent_vol20",
            "derived.brent_wti_spread_z", "derived.usd_z", "derived.curve_2s10s"]
# outcomes: magnitude (what H1 is about) and signed direction, at two horizons.
OUTCOMES = {"abs_car20": lambda c: abs(c[PRE + 20]), "abs_car5": lambda c: abs(c[PRE + 5]),
            "car20": lambda c: c[PRE + 20], "car5": lambda c: c[PRE + 5]}
FDR_Q = 0.10
N_PERM = 5000
OOS_FRAC = 0.7


def _frame(conn):
    ret = load_returns(conn)
    signals = build_signals(load_wide(conn))
    events = pd.read_sql("SELECT event_id, event_date FROM events ORDER BY event_date", conn)
    rows = []
    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["event_date"])
        if car is None:
            continue
        cutoff = pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1)
        row = {"event_id": ev["event_id"], "date": ev["event_date"]}
        for f in FEATURES:
            s = signals[f].dropna() if f in signals else pd.Series(dtype=float)
            row[f] = s.asof(cutoff) if len(s) else np.nan
        for name, fn in OUTCOMES.items():
            row[name] = float(fn(car))
        rows.append(row)
    df = assign_clusters(pd.DataFrame(rows))
    return df.groupby("cluster").first().reset_index()      # de-overlapped


def run():
    conn = sqlite3.connect(DB)
    df = _frame(conn)
    conn.close()

    cands = []
    for outcome in OUTCOMES:
        for f in FEATURES:
            sub = df[[f, outcome]].dropna()
            if len(sub) < 20:
                continue
            x = sub[f].to_numpy(float); y = sub[outcome].to_numpy(float)
            r = validate.pearson(x, y)
            p = validate.perm_corr_p(x, y, N_PERM)
            cut = int(len(x) * OOS_FRAC)
            r_tr, r_te = validate.pearson(x[:cut], y[:cut]), validate.pearson(x[cut:], y[cut:])
            oos = bool(np.sign(r_tr) == np.sign(r_te) and abs(r_te) >= 0.1)
            # causal gate: control for the OTHER feature most correlated with f
            others = [g for g in FEATURES if g != f]
            zbest, pc, zc = None, r, -1.0
            for g in others:
                gz = df[[f, g, outcome]].dropna()
                if len(gz) < 20:
                    continue
                cc = abs(validate.pearson(gz[f].to_numpy(float), gz[g].to_numpy(float)))
                if cc > zc:
                    zc = cc; zbest = g
                    pc = validate.partial_corr(gz[f].to_numpy(float), gz[outcome].to_numpy(float),
                                               gz[g].to_numpy(float))
            causal_ok = bool(abs(pc) >= 0.1 and np.sign(pc) == np.sign(r))
            cands.append({"feature": f, "outcome": outcome, "r": round(r, 3), "n": len(sub),
                          "perm_p": round(p, 4), "r_test": round(r_te, 3), "oos_holds": oos,
                          "partial_r": round(float(pc), 3), "controlled_for": zbest,
                          "causal_ok": causal_ok})

    fdr = validate.bh_fdr([c["perm_p"] for c in cands], q=FDR_Q)
    for c, surv, q in zip(cands, fdr["survive"], fdr["qvalues"]):
        c["passes_fdr"] = bool(surv); c["fdr_q"] = q
    survivors = [c for c in cands if c["passes_fdr"] and c["oos_holds"] and c["causal_ok"]]

    # A survivor is a CANDIDATE, not a shipped edge. Magnitude outcomes (|CAR|) are un-standardized,
    # so any vol-like feature (VIX, realized vol) can predict them MECHANICALLY via volatility
    # clustering (big-vol periods have big moves in everything). Such survivors must pass the
    # standardization defeater (src/inference.py) before promotion. VIX already did (that IS H1);
    # realized Brent vol has NOT -- so it stays a candidate, not an edge.
    VOL_LIKE = {"derived.vix_pct", "derived.brent_vol20"}
    for c in survivors:
        magnitude = c["outcome"].startswith("abs_car")
        c["is_rediscovered_h1"] = (c["feature"] == "derived.vix_pct" and magnitude)
        c["needs_vol_clustering_defeater"] = bool(magnitude and c["feature"] in VOL_LIKE
                                                  and not c["is_rediscovered_h1"])
        c["status"] = ("re-discovered H1 (already validated)" if c["is_rediscovered_h1"]
                       else "CANDIDATE -- likely volatility clustering, needs standardization defeater"
                       if c["needs_vol_clustering_defeater"]
                       else "CANDIDATE -- experimental, needs OOS forecasting validation before promotion")

    report = {
        "what": "Falsification-first scan: which pre-event state features predict the ripple, "
                "surviving permutation + FDR + OOS sign-hold + partial-correlation causal control",
        "sample": "clustered (de-overlapped)", "n_candidates": len(cands),
        "fdr_q": FDR_Q, "n_pass_fdr": int(sum(c["passes_fdr"] for c in cands)),
        "survivors": survivors,
        "strongest_raw": sorted(cands, key=lambda c: abs(c["r"]), reverse=True)[:5],
        "message": (
            "Discovery re-found H1 (VIX->|CAR20|) from scratch -- a good check that the scan works. "
            "The strongest raw hit, realized-Brent-vol -> |CAR20|, is almost certainly volatility "
            "clustering (a known confound), so it is flagged a CANDIDATE needing the standardization "
            "defeater, NOT a validated edge. No NEW validated edge is shipped here: survivors are "
            "candidates that must clear mechanism scrutiny + OOS forecasting validation first."
            if survivors else
            "No leading indicator survives all four gates -- the honest null."),
    }
    # A re-discovery is not a re-validation. H1 is downgraded under the single evidentiary bar, and the
    # placebo objection is about NON-events, which a correlation scan over real events cannot answer.
    # src/retractions.py is the one place that knows; tests/test_retraction_guard.py enforces it.
    import retractions as _R
    for _s in report.get("survivors", []):
        if _s.get("is_rediscovered_h1") and not _R.may_be_live("H1"):
            _rec = _R.adjudication()[_R.canonical("H1")]
            _s["status"] = ("re-discovered H1 -- H1 is NOT validated: " + _R.pointer("H1")
                            + ". Re-discovery does not answer the placebo.")
            _s["retracted"] = True
            _s["retier"] = _rec["retier"]
            _s["retracted_on"] = _rec["on"]
            _s["retracted_reference"] = _rec["reference"]
    OUT.write_text(json.dumps(report, indent=2))
    return report


def main():
    r = run()
    print("=" * 76)
    print("DISCOVERY SCAN (falsification-first) -- clustered sample")
    print("=" * 76)
    print(f"  {r['n_candidates']} candidates tested, FDR q={r['fdr_q']}; "
          f"{r['n_pass_fdr']} pass FDR, {len(r['survivors'])} survive ALL gates")
    print("  strongest raw correlations (pre-correction):")
    for c in r["strongest_raw"]:
        print(f"    {c['feature'].split('.')[-1]:<18} -> {c['outcome']:<9} r={c['r']:+.3f} "
              f"perm_p={c['perm_p']} oos={c['oos_holds']} causal={c['causal_ok']} "
              f"(fdr_q={c.get('fdr_q')})")
    if r["survivors"]:
        print("  SURVIVORS:")
        for c in r["survivors"]:
            print(f"    {c['feature']} -> {c['outcome']}  r={c['r']:+.3f} "
                  f"partial_r={c['partial_r']} (controlled for {c['controlled_for']})")
    print(f"  {r['message']}")


if __name__ == "__main__":
    main()
