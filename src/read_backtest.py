"""
read_backtest.py -- does conditioning the read on H1 actually help, walk-forward? (Step 2)

The registered study proved H1 IN-SAMPLE: across all events, |CAR+20| is ~+5pp bigger when
VIX stress was elevated. This asks the harder, accountability question a forecaster is judged
on: if, for each shock in turn, the engine had predicted the ripple MAGNITUDE using ONLY the
events before it, does knowing the H1 amplifier state reduce its error OUT-OF-SAMPLE?

Method (strict walk-forward, no lookahead):
  Replay the clustered events in date order. Before event i, using only events 1..i-1:
    - unconditional expectation = mean |CAR+20| of prior events.
    - H1-conditioned expectation = mean |CAR+20| of prior events in the SAME H1 bucket, where
      the bucket (ON/OFF) is set by whether that event's t-1 VIX %ile was >= the prior median.
  Resolve against event i's realized |CAR+20|; score error for both.
  If MAE(conditioned) < MAE(unconditional), H1 carries out-of-sample forecasting value -- the
  live-style confirmation of the in-sample edge. Stratified by regime (H1 ON vs OFF).

This is magnitude accountability (a resolving track record), NOT a new hypothesis test: it does
not touch the registered +5pp rule or any verdict. Reuses the exact clustering + event-study +
signal machinery (engine_read / robustness / event_study). Deterministic.

Run:  python3 src/read_backtest.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

# Reuse -- never fork -- the clustered-event builder and the primitives it stands on.
from engine_read import build_clustered_events
from event_study import load_returns, HORIZONS
from derive_signals import load_wide, build_signals

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "read_backtest.json"

MIN_PRIOR = 20          # need a prior base before an OOS read means anything
MIN_BUCKET = 4          # min prior events in a bucket to trust the conditioned expectation
VIX_KEY = "vix"         # the clustered-frame column for derived.vix_pct (see robustness.REGISTERED)


def run():
    conn = sqlite3.connect(DB)
    ret = load_returns(conn)
    signals = build_signals(load_wide(conn))
    events = pd.read_sql("SELECT event_id, event_date, type FROM events ORDER BY event_date", conn)
    conn.close()

    clustered = build_clustered_events(ret, signals, events)      # one row per episode
    clustered = clustered.sort_values("date").reset_index(drop=True)
    # magnitude we forecast: |CAR+20| in pp; and the H1 state variable at t-1
    clustered["mag"] = clustered["car20"].abs() * 100.0
    df = clustered[clustered["mag"].notna() & clustered[VIX_KEY].notna()].reset_index(drop=True)

    recs = []
    for i in range(len(df)):
        if i < MIN_PRIOR:
            continue
        prior = df.iloc[:i]
        cur = df.iloc[i]
        realized = float(cur["mag"])
        uncond = float(prior["mag"].mean())
        # walk-forward H1 bucket: threshold = median of PRIOR VIX %iles (no lookahead)
        med = float(prior[VIX_KEY].median())
        state = "ON" if cur[VIX_KEY] >= med else "OFF"
        same = prior[prior[VIX_KEY] >= med] if state == "ON" else prior[prior[VIX_KEY] < med]
        cond = float(same["mag"].mean()) if len(same) >= MIN_BUCKET else uncond
        recs.append({"event_id": cur["event_id"], "date": cur["date"], "h1_state": state,
                     "realized_mag_pp": round(realized, 2),
                     "expected_uncond_pp": round(uncond, 2),
                     "expected_cond_pp": round(cond, 2),
                     "err_uncond": round(realized - uncond, 2),
                     "err_cond": round(realized - cond, 2)})

    n = len(recs)
    report = {"what": "Walk-forward accountability: does conditioning the read on H1 reduce "
                      "magnitude error out-of-sample?",
              "n_scored": n, "min_prior": MIN_PRIOR,
              "note": "Magnitude accountability (resolving track record), not a hypothesis "
                      "re-test. |CAR+20| forecast from prior events only; H1 bucket set walk-forward."}
    if n:
        eu = np.array([r["err_uncond"] for r in recs])
        ec = np.array([r["err_cond"] for r in recs])
        mae_u, mae_c = float(np.abs(eu).mean()), float(np.abs(ec).mean())
        report.update({
            "mae_uncond_pp": round(mae_u, 3), "mae_cond_pp": round(mae_c, 3),
            "mae_improvement_pp": round(mae_u - mae_c, 3),   # >0 => H1 conditioning helps OOS
            "conditioning_helps": bool(mae_c < mae_u),
            # regime split: realized magnitude actually bigger when H1 was ON?
            "by_regime": {
                st: {"n": int(sum(1 for r in recs if r["h1_state"] == st)),
                     "mean_realized_pp": round(float(np.mean(
                         [r["realized_mag_pp"] for r in recs if r["h1_state"] == st])), 2)}
                for st in ("ON", "OFF") if any(r["h1_state"] == st for r in recs)},
            "records": recs,
        })
        on = report["by_regime"].get("ON", {}).get("mean_realized_pp")
        off = report["by_regime"].get("OFF", {}).get("mean_realized_pp")
        report["live_amplification_pp"] = (round(on - off, 2)
                                           if on is not None and off is not None else None)
    OUT.write_text(json.dumps(report, indent=2))
    return report


def main():
    r = run()
    print("=" * 74)
    print("READ BACKTEST -- does H1-conditioning help the read out-of-sample? (walk-forward)")
    print("=" * 74)
    if not r.get("n_scored"):
        print("  not enough events to score yet."); return
    print(f"  scored {r['n_scored']} events (after {r['min_prior']} priors)")
    print(f"  MAE unconditional {r['mae_uncond_pp']}pp  ->  H1-conditioned {r['mae_cond_pp']}pp "
          f"(improvement {r['mae_improvement_pp']:+}pp)")
    print(f"  conditioning helps OOS: {r['conditioning_helps']}")
    for st, s in r.get("by_regime", {}).items():
        print(f"    H1 {st:<3} n={s['n']:<3} mean realized |CAR+20| = {s['mean_realized_pp']}pp")
    if r.get("live_amplification_pp") is not None:
        print(f"  live-style amplification (ON minus OFF realized): "
              f"{r['live_amplification_pp']:+}pp")
    print(f"  {r['note']}")


if __name__ == "__main__":
    main()
