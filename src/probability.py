"""
probability.py -- the kNN probability function over the corpus (Step 4), falsification-first.

DECLARED BEFORE TESTING (the pre-commitment that makes this honest):
  TARGET:    P( |CAR+20| >= the historical median |CAR+20| | today's pre-event state )
             i.e. "will a shock landing in today's market state ripple BIGGER than a typical
             shock?" -- a binary with a ~0.5 base rate.
  MECHANISM: shocks that land in states resembling prior LARGE-ripple episodes (elevated VIX
             stress, tight inventories, wide spreads, stressed curve/dollar) should themselves
             ripple larger. This is the multivariate generalisation of H1 (which proved the VIX
             component alone). The kNN reads the k most similar prior states and predicts the
             share that were above-median magnitude.
  SIGNATURE: the 7 derived state variables at t-1 (point-in-time), standardised by PRIOR stats.

GATE (identical to the one that proved the analogue a null): strict walk-forward (each shock
forecast from prior events only), then CPCV dispersion + PBO + Diebold-Mariano + Brier-vs-base,
all via src/validate.py. Promoted ONLY if it beats the base rate out-of-sample with PBO<0.2.
The honest, likely outcome given H1 is a weak edge is: "some skill, but does it beat base rate
after correction?" -- reported either way, never tuned to pass. numpy-only; deterministic.

Run:  python3 src/probability.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

from event_study import load_returns, car_for_event, PRE
from derive_signals import load_wide, build_signals
import validate

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "probability_backtest.json"

# The state signature (the 7 conditioning variables; H1's VIX is one of them).
SIG_VARS = ["derived.vix_pct", "derived.inv_sigma", "derived.cot_pct", "derived.brent_vol20",
            "derived.brent_wti_spread_z", "derived.usd_z", "derived.curve_2s10s"]
K = 12                # neighbours
MIN_PRIOR = 30        # walk-forward warmup
MIN_FEATURES = 4      # require at least this many non-missing signature features to score


def build_library(conn):
    """Compute the per-event state signature (t-1) + realized |CAR+20|, and persist to the
    `library` table (created if absent). Additive; one row per event."""
    conn.execute("""CREATE TABLE IF NOT EXISTS library (
        event_id TEXT PRIMARY KEY, event_date TEXT, signature TEXT, mag_pp REAL)""")
    ret = load_returns(conn)
    signals = build_signals(load_wide(conn))
    events = pd.read_sql("SELECT event_id, event_date FROM events ORDER BY event_date", conn)
    rows = []
    for _, ev in events.iterrows():
        car = car_for_event(ret, ev["event_date"])
        if car is None:
            continue
        cutoff = pd.Timestamp(ev["event_date"]) - pd.Timedelta(days=1)   # t-1: no lookahead
        sig = {}
        for sid in SIG_VARS:
            if sid in signals:
                s = signals[sid].dropna()
                v = s.asof(cutoff) if len(s) else np.nan
                if pd.notna(v):
                    sig[sid] = float(v)
        rows.append((ev["event_id"], ev["event_date"], json.dumps(sig),
                     float(abs(car[PRE + 20]) * 100.0)))
    conn.executemany("INSERT OR REPLACE INTO library VALUES (?,?,?,?)", rows)
    conn.commit()
    return len(rows)


def _knn_prob(sig, prior, k):
    """P(above-median magnitude) from the k nearest prior states. `prior` is a list of dicts
    {sig, mag, above}. Features standardised by prior mean/std; distance over shared features."""
    feats = [f for f in SIG_VARS if f in sig]
    if len(feats) < MIN_FEATURES:
        return None
    # standardisation stats from prior events (walk-forward; no lookahead)
    stats = {}
    for f in feats:
        vals = [p["sig"][f] for p in prior if f in p["sig"]]
        if len(vals) >= 5:
            mu, sd = float(np.mean(vals)), float(np.std(vals))
            stats[f] = (mu, sd if sd > 1e-9 else 1.0)
    feats = [f for f in feats if f in stats]
    if len(feats) < MIN_FEATURES:
        return None
    q = np.array([(sig[f] - stats[f][0]) / stats[f][1] for f in feats])
    dists = []
    for p in prior:
        shared = [f for f in feats if f in p["sig"]]
        if len(shared) < MIN_FEATURES:
            continue
        pv = np.array([(p["sig"][f] - stats[f][0]) / stats[f][1] for f in shared])
        qv = np.array([q[feats.index(f)] for f in shared])
        dists.append((float(np.linalg.norm(qv - pv)), p["above"]))
    if len(dists) < k:
        return None
    dists.sort(key=lambda t: t[0])
    nn = dists[:k]
    return sum(a for _, a in nn) / k


def _load_events(conn, clustered):
    """The library as an event list; if clustered, collapse overlapping episodes (keep the first
    of each 35-day cluster) so correlated overlapping windows don't inflate the OOS gate."""
    lib = conn.execute(
        "SELECT event_id, event_date, signature, mag_pp FROM library ORDER BY event_date").fetchall()
    events = [{"event_id": r[0], "date": r[1], "sig": json.loads(r[2]), "mag": r[3]}
              for r in lib if r[3] is not None]
    if not clustered:
        return events
    from robustness import assign_clusters
    df = assign_clusters(pd.DataFrame([{"event_id": e["event_id"], "date": e["date"]}
                                       for e in events]))
    keep = set(df.groupby("cluster").first()["event_id"])
    return [e for e in events if e["event_id"] in keep]


def _score(events):
    """Walk-forward predictions over an event list (no lookahead). Returns the records."""
    recs = []
    for i in range(len(events)):
        if i < MIN_PRIOR:
            continue
        prior_raw = events[:i]
        med = float(np.median([p["mag"] for p in prior_raw]))          # prior-median (point-in-time)
        prior = [{"sig": p["sig"], "mag": p["mag"], "above": 1 if p["mag"] >= med else 0}
                 for p in prior_raw]
        cur = events[i]
        p = _knn_prob(cur["sig"], prior, K)
        if p is None:
            continue
        outcome = 1 if cur["mag"] >= med else 0
        recs.append({"event_id": cur["event_id"], "date": cur["date"], "p": round(p, 3),
                     "outcome": outcome})
    return recs


def _gate(recs):
    """Score a set of walk-forward records: Brier vs base + the anti-overfitting gate."""
    n = len(recs)
    if not n:
        return {"n_scored": 0}
    pr = np.array([r["p"] for r in recs]); y = np.array([r["outcome"] for r in recs], float)
    base = float(y.mean())
    brier = float(np.mean((pr - y) ** 2)); base_brier = float(np.mean((base - y) ** 2))
    lams = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25]
    perf = np.column_stack([-((base + lam * (pr - base)) - y) ** 2 for lam in lams])
    pbo = validate.pbo_cscv(perf, S=8)
    dm = validate.diebold_mariano((pr - y) ** 2, (base - y) ** 2, h=1)
    skills = []
    for tr, te in validate.cpcv_splits(n, k_folds=6, k_test=2, embargo=1):
        if len(tr) < 4 or len(te) < 2:
            continue
        b = y[tr].mean()
        skills.append(np.mean((b - y[te]) ** 2) - np.mean((pr[te] - y[te]) ** 2))
    skills = np.array(skills)
    passes = (brier < base_brier and pbo.get("pbo", 1) <= 0.2
              and dm.get("significant_5pct") and dm.get("better") == "A"
              and len(skills) and (skills > 0).mean() >= 0.5)
    return {"n_scored": n, "base_rate": round(base, 3), "brier": round(brier, 4),
            "base_rate_brier": round(base_brier, 4), "skill_vs_base": round(base_brier - brier, 4),
            "cpcv_skill_mean": round(float(skills.mean()), 4) if len(skills) else None,
            "cpcv_share_positive": round(float((skills > 0).mean()), 3) if len(skills) else None,
            "pbo": pbo, "diebold_mariano": dm, "gate_passes": bool(passes)}


def backtest(conn):
    """Run the walk-forward gate on BOTH the clustered (de-overlapped, primary/honest) and the
    all-events samples. The clustered result is the one that governs the verdict, because CPCV/DM
    assume independent observations and overlapping event windows would inflate the score."""
    clustered = _gate(_score(_load_events(conn, clustered=True)))
    allev = _gate(_score(_load_events(conn, clustered=False)))
    passes = bool(clustered.get("gate_passes"))
    report = {
        "what": "kNN P(|CAR+20| >= historical median) from the pre-event state signature",
        "declared_before_testing": True, "k": K, "signature_vars": SIG_VARS,
        "primary_sample": "clustered (de-overlapped -- the honest test)",
        "clustered": clustered, "all_events": allev,
        "gate_passes": passes,
        "verdict": ("PASSES the OOS gate on the de-overlapped sample -- a genuine EXPERIMENTAL "
                    "signal (the multivariate state predicts ripple magnitude beyond base rate). "
                    "Consistent with H1 being real. Stays experimental until it also beats H1 alone."
                    if passes else
                    "DOES NOT PASS on the de-overlapped sample -- reported as a null. Any all-events "
                    "'skill' was inflated by overlapping/clustered episodes, not a real edge."),
    }
    OUT.write_text(json.dumps(report, indent=2))
    return report


def main():
    conn = sqlite3.connect(DB)
    nlib = build_library(conn)
    r = backtest(conn)
    conn.close()
    print("=" * 76)
    print("PROBABILITY FUNCTION (kNN over the state signature) -- OOS gate")
    print("=" * 76)
    print(f"  library: {nlib} events")
    for lbl, g in (("CLUSTERED (primary/honest)", r["clustered"]), ("all events", r["all_events"])):
        if g.get("n_scored"):
            print(f"  [{lbl}] n={g['n_scored']}  base {g['base_rate']}  Brier {g['brier']} vs "
                  f"{g['base_rate_brier']} -> skill {g['skill_vs_base']:+}  | CPCV skill "
                  f"{g['cpcv_skill_mean']} (paths>0 {g['cpcv_share_positive']})  PBO "
                  f"{g['pbo'].get('pbo')}  DM p {g['diebold_mariano'].get('p_value')}  "
                  f"pass={g['gate_passes']}")
    print(f"  GATE (governed by clustered): {r['verdict']}")


if __name__ == "__main__":
    main()
