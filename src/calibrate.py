"""
calibrate.py -- the honest quant validation of the analogue forecaster (#2's math).

The raw analogue signal is UNCALIBRATED (backtest: Brier 0.40 vs base-rate 0.24, skill
-0.16; overconfident at the tails). A quant does not ship that. The legitimate question is:
does a proper CALIBRATION MAP, fit OUT-OF-SAMPLE, rescue it?

Method (no black-box, no overfit): LEAVE-ONE-OUT isotonic regression (pool-adjacent-
violators). For each event, fit a monotone map raw_signal -> probability on the OTHER 41
events, predict the held-out one, then score. If the leave-one-out-calibrated Brier beats
the base-rate Brier, the signal carries information; if not, it does not -- and we say so.

This is the discipline the plan demands: nothing is an edge until it survives OOS scoring.
Deterministic; hand-rolled isotonic (no sklearn). Run:  python3 src/calibrate.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BT = ROOT / "data" / "backtest_analogue.json"
OUT = ROOT / "data" / "calibration.json"


def isotonic(xs, ys):
    """Pool-adjacent-violators: monotone non-decreasing fit of ys ordered by xs.
    Returns (sorted_x, fitted_y) as a step function."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    sx = [xs[i] for i in order]
    blocks = [[ys[i], 1] for i in order]          # [mean, weight]
    i = 0
    while i < len(blocks) - 1:
        if blocks[i][0] > blocks[i + 1][0] + 1e-12:
            m = (blocks[i][0] * blocks[i][1] + blocks[i + 1][0] * blocks[i + 1][1]) / (
                blocks[i][1] + blocks[i + 1][1])
            blocks[i] = [m, blocks[i][1] + blocks[i + 1][1]]
            del blocks[i + 1]
            if i:
                i -= 1
        else:
            i += 1
    # expand block means back to per-point, aligned to sorted x
    fit, k = [], 0
    for b in blocks:
        fit.extend([b[0]] * b[1])
    return sx, fit


def predict(sx, fit, x):
    """Step/linear read of the isotonic fit at x (clamped to [0,1])."""
    if x <= sx[0]:
        return min(1.0, max(0.0, fit[0]))
    if x >= sx[-1]:
        return min(1.0, max(0.0, fit[-1]))
    for i in range(len(sx) - 1):
        if sx[i] <= x <= sx[i + 1]:
            span = sx[i + 1] - sx[i]
            t = (x - sx[i]) / span if span else 0
            return min(1.0, max(0.0, fit[i] + t * (fit[i + 1] - fit[i])))
    return min(1.0, max(0.0, fit[-1]))


def brier(p, o):
    return (p - o) ** 2


def run():
    if not BT.exists():
        return {"error": "run src/backtest_analogue.py first"}
    recs = json.loads(BT.read_text()).get("records", [])
    n = len(recs)
    if n < 10:
        return {"error": f"too few records ({n}) to validate"}
    ps = [r["p"] for r in recs]
    os = [float(r["outcome"]) for r in recs]
    base = sum(os) / n

    # raw (uncalibrated) Brier + the always-base-rate benchmark
    raw_brier = round(sum(brier(p, o) for p, o in zip(ps, os)) / n, 4)
    base_brier = round(sum(brier(base, o) for o in os) / n, 4)

    # LEAVE-ONE-OUT isotonic calibration -- the honest OOS test
    cal_preds = []
    for i in range(n):
        xs = [ps[j] for j in range(n) if j != i]
        ys = [os[j] for j in range(n) if j != i]
        sx, fit = isotonic(xs, ys)
        cal_preds.append(predict(sx, fit, ps[i]))
    cal_brier = round(sum(brier(p, o) for p, o in zip(cal_preds, os)) / n, 4)

    report = {
        "n": n, "base_rate": round(base, 3),
        "raw_brier": raw_brier, "base_rate_brier": base_brier,
        "calibrated_brier_loo": cal_brier,
        "raw_skill": round(base_brier - raw_brier, 4),
        "calibrated_skill_loo": round(base_brier - cal_brier, 4),
        "verdict": None,
    }
    s = report["calibrated_skill_loo"]
    if s > 0.01:
        report["verdict"] = ("CARRIES INFORMATION: leave-one-out-calibrated Brier beats the "
                             "base rate. The analogue signal has (weak) OOS skill once calibrated.")
    else:
        report["verdict"] = ("NO OOS EDGE at this N: even a leave-one-out isotonic calibration "
                             "does not beat always-predicting the base rate. The signal is not "
                             "yet a validated edge -- more N (the corpus) is the honest fix, not "
                             "tuning. Report the null; do not ship it as an edge.")
    OUT.write_text(json.dumps(report, indent=2))
    return report


def main():
    r = run()
    if "error" in r:
        print(f"calibrate -- {r['error']}")
        return
    print(f"calibrate -- analogue forecaster, N={r['n']}, base rate {r['base_rate']}")
    print(f"  raw Brier          {r['raw_brier']}  (skill {r['raw_skill']:+})")
    print(f"  base-rate Brier    {r['base_rate_brier']}")
    print(f"  LOO-calibrated     {r['calibrated_brier_loo']}  (skill {r['calibrated_skill_loo']:+})")
    print(f"  VERDICT: {r['verdict']}")


if __name__ == "__main__":
    main()
