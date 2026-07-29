"""
resolve_reads.py -- close out logged reads and score the engine's calibration (Wire 4).

For every pending read (resolved_at IS NULL) whose event window has fully elapsed,
compute the REALIZED abnormal return of the anchor series at the read's horizon
(the same constant-mean CAR the engine uses everywhere, via event_study), and
record the error = realized - expected. Then print the running calibration: how
far off the engine's magnitude expectations have been, overall and by event type.

This is the loop that makes the system LEARN -- "last three times it overshot."
It is magnitude accountability, not a probability and not a forecast of occurrence.
Resolution needs the full event-study window (POST=20 trading days) of price data
after the anchor, so a read settles ~20 trading days after it is logged.

Run:  python3 src/resolve_reads.py
"""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from cross_asset import asset_returns
from event_study import car_for_event, PRE

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"


def resolve_pending(conn, now=None):
    """Resolve every read whose window has elapsed. Returns rows resolved."""
    now = now or datetime.now(timezone.utc).isoformat(timespec="seconds")
    pending = conn.execute(
        "SELECT read_id, kind, anchor_date, anchor_series, horizon_days, "
        "expected_car FROM reads WHERE resolved_at IS NULL").fetchall()
    resolved = 0
    ret_cache = {}
    for rid, kind, anchor_date, series, horizon, expected in pending:
        if series not in ret_cache:
            ret_cache[series] = asset_returns(conn, series, "price")
        ret = ret_cache[series]
        if ret is None:
            continue
        car = car_for_event(ret, anchor_date)
        if car is None or PRE + horizon >= len(car):
            continue                       # window not fully elapsed yet -> pending
        realized = float(car[PRE + horizon]) * 100.0
        error = realized - expected
        conn.execute(
            "UPDATE reads SET resolved_at=?, realized_car=?, error=? WHERE read_id=?",
            (now, round(realized, 3), round(error, 3), rid))
        resolved += 1
    conn.commit()
    return resolved


def _h1_state(amp_context):
    """Parse the H1 amplifier state that was recorded when the read was logged
    (amp_context looks like 'H1:ON H2:ON H3:FAILED'). Returns 'ON'/'OFF'/None."""
    for tok in (amp_context or "").split():
        if tok.startswith("H1:"):
            s = tok.split(":", 1)[1]
            return s if s in ("ON", "OFF") else None
    return None


def calibration(conn):
    """Summary stats over all resolved reads: n, bias (mean error), MAE -- overall, by event
    kind, and stratified by the H1 amplifier state at log time (the live, forward-accruing
    counterpart to read_backtest.py: were realized ripples bigger when H1 was ON?)."""
    rows = conn.execute(
        "SELECT kind, expected_car, realized_car, error, amp_context FROM reads "
        "WHERE resolved_at IS NOT NULL").fetchall()
    out = {"n": len(rows), "overall": None, "by_kind": {}, "by_h1": {}}
    if not rows:
        return out
    errs = np.array([r[3] for r in rows], dtype=float)
    out["overall"] = {"bias_pp": round(float(errs.mean()), 2),
                      "mae_pp": round(float(np.abs(errs).mean()), 2)}
    kinds, h1 = {}, {}
    for kind, _exp, realized, err, amp in rows:
        kinds.setdefault(kind, []).append(err)
        st = _h1_state(amp)
        if st is not None and realized is not None:
            h1.setdefault(st, []).append(abs(float(realized)))   # realized magnitude by regime
    for kind, es in kinds.items():
        a = np.array(es, dtype=float)
        out["by_kind"][kind] = {"n": len(es), "bias_pp": round(float(a.mean()), 2),
                                "mae_pp": round(float(np.abs(a).mean()), 2)}
    for st, mags in h1.items():
        a = np.array(mags, dtype=float)
        out["by_h1"][st] = {"n": len(mags), "mean_realized_abs_pp": round(float(a.mean()), 2)}
    return out


def main():
    conn = sqlite3.connect(DB)
    n = resolve_pending(conn)
    cal = calibration(conn)
    pending = conn.execute(
        "SELECT COUNT(*) FROM reads WHERE resolved_at IS NULL").fetchone()[0]
    conn.close()
    print(f"resolve_reads -- resolved {n} this run; {pending} still pending; "
          f"{cal['n']} resolved total.")
    if cal["overall"]:
        o = cal["overall"]
        print(f"  calibration (realized - expected): bias {o['bias_pp']:+.2f}pp, "
              f"MAE {o['mae_pp']:.2f}pp")
        for kind, s in sorted(cal["by_kind"].items()):
            print(f"    {kind:<22} n={s['n']:<3} bias {s['bias_pp']:+.2f}pp  "
                  f"MAE {s['mae_pp']:.2f}pp")
    else:
        print("  no resolved reads yet -- log some with log_read.py and wait for "
              "the window to elapse.")


if __name__ == "__main__":
    main()
