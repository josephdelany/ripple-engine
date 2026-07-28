"""
auto_forecast.py -- the ENGINE's self-resolving track record (Stage 2: the calibration loop).

forecast_log.py records JOE's judgment calls. This records the ENGINE's: a concrete,
falsifiable, self-resolving forecast derived straight from the analogue engine, so the
engine is held accountable automatically, every run.

The forecast, per active situation:
    P(Brent spikes >= 5% within 20 trading days) = the analogue base rate for oil OVERSHOOT.
No fabrication -- the probability is read from analogue.json. It resolves ITSELF: 20 trading
days later, we check whether Brent actually rose >= 5% intra-window, set the outcome, and
score it with Brier. Over time this is the engine's calibration curve: does its analogue
base rate actually track reality?

One OPEN forecast per situation at a time (a clean rolling record, not a daily flood). Uses
the existing `forecasts` table, tagged market_source='analogue' so it never touches Joe's
manual log. Overlapping windows across situations are correlated -- flagged, not hidden.

Deterministic; no LLM. Run:  python3 src/auto_forecast.py
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
ANALOGUE = ROOT / "data" / "analogue.json"
OUT = ROOT / "data" / "forecast_calibration.json"

SPIKE = 0.05             # "spike" = Brent up >= 5% at some point in the window
HORIZON_TD = 20          # trading days
BRENT = "fred.DCOILBRENTEU"
TAG = "analogue"         # market_source tag marking engine forecasts


# ---- pure helpers (unit-tested) --------------------------------------------
def p_overshoot(fc):
    """Analogue-implied P(oil overshoot) for one situation: share of matched analogues whose
    oil (WTI, else Brent) pattern was 'overshoot'. None if the forecast carries no oil asset."""
    ka = fc.get("key_assets", {})
    a = ka.get("wti") or ka.get("brent")
    if not a:
        return None
    pats = a.get("patterns", {})
    n = a.get("n") or sum(pats.values())
    return round(pats.get("overshoot", 0) / n, 3) if n else None


def is_spike(base, window, thresh=SPIKE):
    """Did the series rise >= thresh at any point in the forward window?"""
    return bool(window) and (max(window) / base - 1) >= thresh


def brier(p, o):
    """Single-forecast Brier score (lower better; 0 perfect)."""
    return round((p - o) ** 2, 4)


# ---- DB ops ----------------------------------------------------------------
def _brent(conn):
    return conn.execute(
        "SELECT obs_date, value FROM observations WHERE series_id=? AND value IS NOT NULL "
        "ORDER BY obs_date", (BRENT,)).fetchall()


def log_today(conn, now):
    """Log one open forecast per active situation (skip if one is already open)."""
    if not ANALOGUE.exists():
        return 0
    forecasts = json.loads(ANALOGUE.read_text()).get("forecasts", [])
    logged = 0
    for fc in forecasts:
        p = p_overshoot(fc)
        if p is None:
            continue
        sit = fc.get("situation", "")
        q = f"Brent spikes >= {int(SPIKE*100)}% within {HORIZON_TD} trading days — {sit}"
        open_row = conn.execute(
            "SELECT 1 FROM forecasts WHERE question=? AND market_source=? AND "
            "resolved_at IS NULL", (q, TAG)).fetchone()
        if open_row:                                   # one open forecast per situation
            continue
        conn.execute(
            "INSERT INTO forecasts (made_at, question, horizon, my_prob, market_prob, "
            "market_source, notes) VALUES (?,?,?,?,?,?,?)",
            (now, q, f"{HORIZON_TD}td", p, None, TAG,
             f"analogue base rate; N={fc.get('n_analogues')}; "
             f"confidence {fc.get('confidence',{}).get('band','')}; anchor {now[:10]}"))
        logged += 1
    return logged


def resolve_matured(conn, now):
    """Resolve engine forecasts whose 20-trading-day window has fully elapsed."""
    series = _brent(conn)
    dates = [d for d, _ in series]
    vals = [v for _, v in series]
    pending = conn.execute(
        "SELECT forecast_id, made_at FROM forecasts WHERE resolved_at IS NULL AND "
        "market_source=?", (TAG,)).fetchall()
    resolved = 0
    for fid, made_at in pending:
        day = (made_at or "")[:10]
        i = next((k for k, d in enumerate(dates) if d >= day), None)
        if i is None or i + HORIZON_TD >= len(dates):     # not enough forward data yet
            continue
        outcome = 1 if is_spike(vals[i], vals[i + 1:i + 1 + HORIZON_TD]) else 0
        conn.execute("UPDATE forecasts SET outcome=?, resolved_at=? WHERE forecast_id=?",
                     (outcome, now, fid))
        resolved += 1
    return resolved


def calibration(conn):
    """Brier scoreboard over resolved engine forecasts, vs the base-rate benchmark."""
    rows = conn.execute(
        "SELECT my_prob, outcome FROM forecasts WHERE outcome IS NOT NULL AND "
        "market_source=?", (TAG,)).fetchall()
    n = len(rows)
    if not n:
        return {"n": 0, "note": "no engine forecasts resolved yet (need 20 trading days)."}
    ps = [r[0] for r in rows]
    os = [float(r[1]) for r in rows]
    mean_brier = round(sum(brier(p, o) for p, o in zip(ps, os)) / n, 4)
    base = round(sum(os) / n, 3)
    base_brier = round(sum(brier(base, o) for o in os) / n, 4)
    return {"n": n, "brier": mean_brier, "base_rate": base, "base_rate_brier": base_brier,
            "skill_vs_base": round(base_brier - mean_brier, 4),
            "note": "Engine analogue forecasts, self-resolved vs realised Brent. Skill>0 = "
                    "the analogue base rate beats always-predicting the base rate. Overlapping "
                    "windows are correlated (early, indicative)."}


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn = sqlite3.connect(DB)
    settled = resolve_matured(conn, now)      # settle matured first...
    logged = log_today(conn, now)             # ...then open new forecasts
    conn.commit()
    cal = calibration(conn)
    cal["as_of"] = now[:10]
    OUT.write_text(json.dumps(cal, indent=2))
    conn.close()
    print(f"auto_forecast -- logged {logged}, resolved {settled}. "
          + (f"Brier {cal['brier']} vs base {cal['base_rate_brier']} (n={cal['n']})."
             if cal.get("n") else cal["note"]))


if __name__ == "__main__":
    main()
