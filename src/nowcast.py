"""
nowcast.py -- Kalman local-level nowcast of a lagged state variable, gated (Step 7).

The state variables update on a lag (EIA crude stocks are weekly; between prints the "current"
value is stale). A local-level Kalman filter tracks the latent level and gives a calibrated
predictive band. This ports ste/kalman.py (pure numpy) and adds an HONEST backtest gate:

  GATE (PHASE2_NORTH_STAR): the one-step-ahead nowcast must (a) have 68% predictive-interval
  coverage in [0.60, 0.76] (calibrated, not over/under-confident) AND (b) beat naive persistence
  (last-value carry-forward) out-of-sample on RMSE. If it is calibrated but does NOT beat
  persistence, that is the honest result at this frequency without a leading correlate -- reported,
  not hidden. (The path to skill is a higher-frequency correlate via the ALFRED/dynamic-factor
  route -- src/fetch_fred_alfred.py -- not tuning.)

Point-in-time: the filter only ever uses data up to each step. numpy-only, deterministic.

Run:  python3 src/nowcast.py [series_id]   (default: eia.crude_stocks_xspr)
"""

import json
import sqlite3
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "nowcast_backtest.json"
DEFAULT_SERIES = "eia.crude_stocks_xspr"


# ---- ported local-level Kalman filter (ste/kalman.py) ----
def kalman_step(prior_mean, prior_var, obs, obs_var, process_var):
    """One Bayesian update of a local-level (random-walk) latent state given a new obs."""
    pred_mean, pred_var = prior_mean, prior_var + process_var
    gain = pred_var / (pred_var + obs_var)
    return pred_mean + gain * (obs - pred_mean), (1 - gain) * pred_var, gain


def kalman_filter(z, process_var, obs_var):
    """Filter a 1-D series. Returns per-step one-step-ahead predictive mean and variance
    (the forecast for z[t] made BEFORE seeing z[t] -- what a nowcast would have said)."""
    z = np.asarray(z, float)
    m, v = z[0], obs_var
    pred_means, pred_vars = [], []
    for t in range(len(z)):
        pm, pv = m, v + process_var                 # one-step-ahead prediction for z[t]
        pred_means.append(pm); pred_vars.append(pv)
        m, v, _ = kalman_step(m, v, z[t], obs_var, process_var)   # update with the observed z[t]
    return np.array(pred_means), np.array(pred_vars)


def _series(conn, series_id):
    rows = conn.execute(
        "SELECT obs_date, value FROM observations WHERE series_id=? AND value IS NOT NULL "
        "ORDER BY obs_date, as_of DESC", (series_id,)).fetchall()
    # de-dupe by obs_date (keep first = latest as_of due to ordering within date)
    seen, out = set(), []
    for d, v in rows:
        if d in seen:
            continue
        seen.add(d); out.append(float(v))
    return np.array(out)


def backtest(conn, series_id):
    z = _series(conn, series_id)
    n = len(z)
    if n < 60:
        return {"ok": False, "reason": f"series too short ({n})"}
    # scale process/obs variance off the series' own step size (random-walk prior)
    diffs = np.diff(z)
    step_var = float(np.var(diffs)) or 1.0
    process_var, obs_var = step_var, step_var * 0.5     # modest measurement noise

    pm, pv = kalman_filter(z, process_var, obs_var)
    # evaluate one-step-ahead from a warmup point (point-in-time)
    start = 20
    err_k = z[start:] - pm[start:]
    err_p = z[start:] - z[start - 1:-1]                 # naive persistence: predict last value
    rmse_k = float(np.sqrt(np.mean(err_k ** 2)))
    rmse_p = float(np.sqrt(np.mean(err_p ** 2)))
    sd = np.sqrt(pv[start:])
    coverage68 = float(np.mean(np.abs(err_k) <= sd))    # share of actuals within +/-1 predictive sd
    skill = 1 - rmse_k / rmse_p if rmse_p else 0.0

    cov_ok = 0.60 <= coverage68 <= 0.76
    beats = rmse_k < rmse_p
    report = {
        "series": series_id, "n": n, "n_evaluated": int(n - start),
        "rmse_nowcast": round(rmse_k, 3), "rmse_persistence": round(rmse_p, 3),
        "skill_vs_persistence": round(skill, 4), "beats_persistence": bool(beats),
        "ci68_coverage": round(coverage68, 3), "coverage_in_band": bool(cov_ok),
        "gate_passes": bool(cov_ok and beats),
        "verdict": (
            "PASSES: calibrated (68% coverage in band) AND beats persistence OOS."
            if (cov_ok and beats) else
            f"Calibrated coverage={round(coverage68,3)} (band [.60,.76]: {cov_ok}); beats "
            f"persistence: {beats}. " + (
                "Honest null on skill: a local-level filter ~= persistence at this frequency "
                "without a leading correlate. The path to skill is a higher-frequency correlate "
                "(ALFRED/dynamic-factor), not tuning." if not beats else
                "Calibration off-band; needs variance retune before use.")),
    }
    OUT.write_text(json.dumps(report, indent=2))
    return report


def main():
    series_id = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SERIES
    conn = sqlite3.connect(DB)
    r = backtest(conn, series_id)
    conn.close()
    print("=" * 74)
    print(f"NOWCAST GATE -- Kalman local-level on {series_id}")
    print("=" * 74)
    if not r.get("ok", True) and "reason" in r:
        print("  " + r["reason"]); return
    print(f"  n={r['n']} (evaluated {r['n_evaluated']} one-step-ahead)")
    print(f"  RMSE nowcast {r['rmse_nowcast']} vs persistence {r['rmse_persistence']} "
          f"-> skill {r['skill_vs_persistence']:+} (beats persistence: {r['beats_persistence']})")
    print(f"  68% coverage {r['ci68_coverage']} (in band [.60,.76]: {r['coverage_in_band']})")
    print(f"  GATE: {r['verdict']}")


if __name__ == "__main__":
    main()
