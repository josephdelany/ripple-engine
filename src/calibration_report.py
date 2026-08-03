"""
calibration_report.py -- the quarterly out-of-sample calibration report (VISION_ROADMAP V-Q4).

The forecast log is the engine's PERMANENT out-of-sample test: every scored call is a bet against
reality that cannot be tuned after the fact. This turns the resolved ledger into a standing calibration
report -- Brier, skill vs base rate, and a reliability table -- broken out BY QUARTER (bucketed on when
the call was MADE, anchor_date, not when it happened to be resolved), so drift is visible over time.

Source: the resolved gap ledger (gaps with outcome + engine_p), the same ledger evaluate.py calibrates
on -- here time-sliced. (The forecasts table is the newer log; it is included automatically once its
rows resolve.) A quarter with few calls is labelled thin, not hidden. numpy only; free/local.

Writes data/calibration_report.json + data/calibration_report.txt. A compact summary is folded into
data/evaluation.json by evaluate.py (headline artifact of every phase, per the standing rule).

Run:  python3 src/calibration_report.py
"""

import json
import sqlite3
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
JSON = ROOT / "data" / "calibration_report.json"
TXT = ROOT / "data" / "calibration_report.txt"
THIN = 8            # a quarter with < THIN resolved calls is labelled thin (shown, not trusted)


def _quarter(date_str):
    y, m = int(date_str[:4]), int(date_str[5:7])
    return f"{y}Q{(m - 1) // 3 + 1}"


def _brier(p, y):
    p, y = np.asarray(p, float), np.asarray(y, float)
    return float(np.mean((p - y) ** 2))


def _scores(p, y):
    """Brier, base-rate Brier, skill, n for a set of (prob, outcome)."""
    p, y = np.asarray(p, float), np.asarray(y, float)
    if len(p) == 0:
        return None
    obar = float(np.mean(y))
    brier = _brier(p, y)
    base = float(np.mean((obar - y) ** 2))
    return {"n": int(len(p)), "base_rate": round(obar, 3), "brier": round(brier, 4),
            "base_rate_brier": round(base, 4), "skill_vs_base": round(base - brier, 4)}


def _reliability(p, y, edges=(0, 0.2, 0.4, 0.6, 0.8, 1.01)):
    p, y = np.asarray(p, float), np.asarray(y, float)
    bins = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (p >= lo) & (p < hi)
        if m.sum() == 0:
            continue
        bins.append({"band": f"{lo:.1f}-{min(hi,1.0):.1f}", "n": int(m.sum()),
                     "mean_forecast": round(float(p[m].mean()), 3),
                     "observed": round(float(y[m].mean()), 3)})
    return bins


def run():
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT anchor_date, engine_p, outcome FROM gaps "
        "WHERE outcome IS NOT NULL AND engine_p IS NOT NULL AND anchor_date IS NOT NULL "
        "ORDER BY anchor_date").fetchall()
    conn.close()
    if not rows:
        return {"ran": False, "reason": "no resolved forecasts with anchor dates yet"}

    p = [float(r[1]) for r in rows]
    y = [float(r[2]) for r in rows]
    overall = _scores(p, y)
    overall["reliability"] = _reliability(p, y)

    # quarterly buckets on the date the call was MADE
    by_q = {}
    for (adate, ep, out) in rows:
        by_q.setdefault(_quarter(adate), {"p": [], "y": []})
        by_q[_quarter(adate)]["p"].append(float(ep)); by_q[_quarter(adate)]["y"].append(float(out))
    quarters = []
    for q in sorted(by_q):
        s = _scores(by_q[q]["p"], by_q[q]["y"])
        s["quarter"] = q; s["thin"] = s["n"] < THIN
        quarters.append(s)

    return {"ran": True, "overall": overall, "quarters": quarters,
            "n_quarters": len(quarters),
            "span": f"{rows[0][0][:7]}..{rows[-1][0][:7]}"}


def write_txt(r):
    L = []
    w = L.append
    w("=" * 84)
    w("QUARTERLY CALIBRATION REPORT -- the forecast log as a standing out-of-sample test (V-Q4)")
    w("=" * 84)
    if not r.get("ran"):
        w(f"  not yet: {r.get('reason')}")
        TXT.write_text("\n".join(L) + "\n"); return "\n".join(L)
    o = r["overall"]
    w(f"  OVERALL (n={o['n']}, {r['span']}): Brier {o['brier']} vs base {o['base_rate_brier']} "
      f"-> skill {o['skill_vs_base']:+.4f}  (base rate {o['base_rate']})")
    w(f"  {'skill > 0 = better than always guessing the base rate.' }")
    w("")
    w("  Reliability (forecast band -> observed frequency):")
    w(f"    {'band':<10}{'n':>5}{'mean p':>9}{'observed':>10}")
    for b in o["reliability"]:
        w(f"    {b['band']:<10}{b['n']:>5}{b['mean_forecast']:>9}{b['observed']:>10}")
    w("")
    w("  By quarter (bucketed on when the call was MADE; 'thin' = few calls, shown not trusted):")
    w(f"    {'quarter':<9}{'n':>4}{'Brier':>8}{'skill':>9}  flag")
    for q in r["quarters"]:
        w(f"    {q['quarter']:<9}{q['n']:>4}{q['brier']:>8.3f}{q['skill_vs_base']:>+9.4f}"
          f"  {'thin' if q['thin'] else ''}")
    w("")
    w("  Published as computed; a quarter's small-n reads as indicative, not a verdict.")
    TXT.write_text("\n".join(L) + "\n")
    return "\n".join(L)


def main():
    r = run()
    JSON.write_text(json.dumps(r, indent=2))
    print(write_txt(r))
    print(f"\nWrote {JSON} and {TXT}")


if __name__ == "__main__":
    main()
