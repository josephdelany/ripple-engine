"""
auto_forecast.py -- the ENGINE's self-resolving track record (Stage 2: the calibration loop).

forecast_log.py records JOE's judgment calls. This records the ENGINE's: a concrete,
falsifiable, self-resolving forecast derived straight from the analogue engine.

RE-SPEC (2026-07-28): the first target -- P(Brent +5% spike) -- was falsified by the
backtest (skill -0.25): the analogue "overshoot" label does not mean a +5% up-move. This
is the re-specified, mechanism-honest target:

    P(oil TURBULENCE) = P(realised Brent volatility RISES in the 20 trading days after the
    shock), forecast by the share of the nearest analogues whose oil pattern was NON-clean
    (overshoot / confounded / bifurcated / slow / directional_error) -- i.e. "turbulent
    absorption" -> turbulent aftermath. Clean_absorption analogues => the market shrugged.

No fabrication: the probability is read from analogue.json. It resolves ITSELF -- 20 trading
days later we compare realised forward vol to the pre-event vol. Over time this is the
engine's calibration curve. Whether it actually calibrates is decided by backtest_analogue.py
and reported honestly either way.

One OPEN forecast per situation at a time. Uses the `forecasts` table, tagged
market_source='analogue'. Deterministic; no LLM. Run:  python3 src/auto_forecast.py
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
ANALOGUE = ROOT / "data" / "analogue.json"
OUT = ROOT / "data" / "forecast_calibration.json"

HORIZON_TD = 20          # trading days
BRENT = "fred.DCOILBRENTEU"
TAG = "analogue"


# ---- pure helpers (unit-tested) --------------------------------------------
def p_turbulence(fc):
    """Analogue-implied P(turbulent aftermath) for one situation: share of matched analogues
    whose oil (WTI, else Brent) pattern was NOT clean_absorption. None if no oil asset."""
    ka = fc.get("key_assets", {})
    a = ka.get("wti") or ka.get("brent")
    if not a:
        return None
    pats = a.get("patterns", {})
    n = a.get("n") or sum(pats.values())
    if not n:
        return None
    clean = pats.get("clean_absorption", 0)
    return round((n - clean) / n, 3)


def realized_vol(prices):
    """Sample stdev of simple daily returns over a price window. None if too short."""
    if len(prices) < 3:
        return None
    rets = [prices[i] / prices[i - 1] - 1 for i in range(1, len(prices)) if prices[i - 1]]
    if len(rets) < 2:
        return None
    m = sum(rets) / len(rets)
    return (sum((r - m) ** 2 for r in rets) / (len(rets) - 1)) ** 0.5


def vol_rose(pre_prices, post_prices):
    """Did realised volatility rise from the pre-event window to the post-event window?"""
    a, b = realized_vol(pre_prices), realized_vol(post_prices)
    if a is None or b is None:
        return None
    return b > a


def brier(p, o):
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
        p = p_turbulence(fc)
        if p is None:
            continue
        sit = fc.get("situation", "")
        q = f"Oil turbulence (realised vol rises) within {HORIZON_TD} trading days — {sit}"
        if conn.execute("SELECT 1 FROM forecasts WHERE question=? AND market_source=? AND "
                        "resolved_at IS NULL", (q, TAG)).fetchone():
            continue
        conn.execute(
            "INSERT INTO forecasts (made_at, question, horizon, my_prob, market_prob, "
            "market_source, notes) VALUES (?,?,?,?,?,?,?)",
            (now, q, f"{HORIZON_TD}td", p, None, TAG,
             f"analogue non-clean share; N={fc.get('n_analogues')}; "
             f"confidence {fc.get('confidence',{}).get('band','')}; anchor {now[:10]}"))
        logged += 1
    return logged


def resolve_matured(conn, now):
    """Resolve forecasts whose 20-trading-day post-window has fully elapsed."""
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
        if i is None or i < HORIZON_TD or i + HORIZON_TD >= len(dates):
            continue                                       # need 20 td both sides
        rose = vol_rose(vals[i - HORIZON_TD:i + 1], vals[i:i + HORIZON_TD + 1])
        if rose is None:
            continue
        conn.execute("UPDATE forecasts SET outcome=?, resolved_at=? WHERE forecast_id=?",
                     (1 if rose else 0, now, fid))
        resolved += 1
    return resolved


def calibration(conn):
    rows = conn.execute(
        "SELECT my_prob, outcome FROM forecasts WHERE outcome IS NOT NULL AND "
        "market_source=?", (TAG,)).fetchall()
    n = len(rows)
    if not n:
        return {"n": 0, "note": "no engine forecasts resolved yet (need 20 trading days)."}
    ps, os = [r[0] for r in rows], [float(r[1]) for r in rows]
    mean_brier = round(sum(brier(p, o) for p, o in zip(ps, os)) / n, 4)
    base = round(sum(os) / n, 3)
    base_brier = round(sum(brier(base, o) for o in os) / n, 4)
    return {"n": n, "brier": mean_brier, "base_rate": base, "base_rate_brier": base_brier,
            "skill_vs_base": round(base_brier - mean_brier, 4),
            "note": "Engine analogue turbulence forecasts, self-resolved vs realised Brent "
                    "vol. Skill>0 = the analogue non-clean share beats the base rate."}


def main():
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn = sqlite3.connect(DB)
    settled = resolve_matured(conn, now)
    logged = log_today(conn, now)
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
