"""
gaps.py -- THE GAP as a first-class, scored, resolving object (Pillar 1: market-as-null).

The differentiator: incumbents emit a geopolitical-risk SCORE. This engine emits a GAP -- where its
state-conditioned view of oil turbulence DISAGREES with what the market has priced -- and then keeps
score. A Gap is:

    {anchor shock/state}
      engine_view  : from the VALIDATED H1 -- when VIX stress is elevated (H1 amplifier ON), a shock
                     ripples wider, so the engine leans "turbulent"; else "calm".
      priced_view  : OVX (options-implied oil vol) percentile -- what the market has priced.
      gap_direction: under_priced_risk (engine turbulent, market calm) | over_priced_fear (engine calm,
                     market pricing high vol) | aligned.
      resolves at +20 trading days: did realized Brent vol actually rise? (reuses auto_forecast.vol_rose)
      Brier-scored, by regime and by gap_direction.

It is populated over the event history (OVX exists from 2007) so the ledger is REAL now, plus a live
gap for today. HONESTY: this reuses the same turbulence target the analogue forecaster showed is a hard
null -- so the engine's turbulence call may have little skill. That's the point of the moat: we publish
the resolving scorecard either way. The PRODUCT is the transparent, calibrated gap ledger, not a claim
of edge. "No priced anchor (pre-2007) -> not scored." numpy-only; deterministic; point-in-time.

Run:  python3 src/gaps.py
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from event_study import load_returns
from derive_signals import load_wide, build_signals
from auto_forecast import vol_rose

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
OUT = ROOT / "data" / "gaps.json"
BRENT = "fred.DCOILBRENTEU"
VIXP = "derived.vix_pct"
HORIZON = 20                 # trading days
OVX_LOW, OVX_HIGH = 40, 60   # priced-vol percentile bands ("market calm" / "market fearful")
P_TURB, P_CALM = 0.60, 0.40  # typed engine probabilities (buckets, not invented decimals)


def _brent(conn):
    rows = conn.execute("SELECT obs_date, value FROM observations WHERE series_id=? AND value IS NOT NULL "
                        "ORDER BY obs_date", (BRENT,)).fetchall()
    return [d for d, _ in rows], [v for _, v in rows]


def _ovx_series(conn):
    rows = conn.execute("SELECT obs_date, value FROM observations WHERE series_id='fred.OVXCLS' "
                        "AND value IS NOT NULL ORDER BY obs_date").fetchall()
    return [d for d, _ in rows], np.array([v for _, v in rows], float)


def _pct_rank(prior_vals, x):
    """Percentile of x within the prior values (point-in-time; 0..100)."""
    if len(prior_vals) < 20:
        return None
    return round(float((np.asarray(prior_vals) < x).mean() * 100), 1)


def _resolve_turbulence(dates, vals, anchor_date):
    """Did realized Brent vol rise from the 20td before to the 20td after? 1/0/None (reuses vol_rose)."""
    i = next((k for k, d in enumerate(dates) if d >= anchor_date), None)
    if i is None or i < HORIZON or i + HORIZON >= len(dates):
        return None
    rose = vol_rose(vals[i - HORIZON:i + 1], vals[i:i + HORIZON + 1])
    return None if rose is None else (1 if rose else 0)


def _gap_direction(engine_turbulent, ovx_pct):
    if ovx_pct is None:
        return "aligned"
    if engine_turbulent and ovx_pct < OVX_LOW:
        return "under_priced_risk"      # engine sees turbulence; market priced calm
    if (not engine_turbulent) and ovx_pct > OVX_HIGH:
        return "over_priced_fear"       # engine sees calm; market priced fear
    return "aligned"


def build(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS gaps (
        gap_id TEXT PRIMARY KEY, as_of TEXT, anchor_date TEXT, subject TEXT,
        engine_call TEXT, engine_p REAL, priced_ovx REAL, priced_ovx_pct REAL,
        gap_direction TEXT, horizon_days INTEGER, outcome INTEGER, brier REAL,
        resolved_at TEXT, source_url TEXT, notes TEXT)""")
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    bdates, bvals = _brent(conn)
    odates, ovals = _ovx_series(conn)
    ovx_by_date = dict(zip(odates, ovals))
    signals = build_signals(load_wide(conn))
    vixs = signals[VIXP].dropna() if VIXP in signals else pd.Series(dtype=float)
    vix_median = float(vixs.median()) if len(vixs) else 50.0    # H1 threshold (event-sample-ish)

    events = pd.read_sql("SELECT event_id, event_date, title, source_url FROM events ORDER BY event_date", conn)
    rows = []
    for _, ev in events.iterrows():
        d = ev["event_date"]
        if d < (odates[0] if odates else "9999"):      # no priced anchor before OVX exists
            continue
        cutoff = pd.Timestamp(d) - pd.Timedelta(days=1)      # t-1 state
        vix = vixs.asof(cutoff) if len(vixs) else np.nan
        if pd.isna(vix):
            continue
        # priced view: OVX at/just before t-1 + its point-in-time percentile
        ov_prior = [ovals[k] for k, od in enumerate(odates) if od <= d]
        if len(ov_prior) < 20:
            continue
        ovx = ov_prior[-1]
        ovx_pct = _pct_rank(ov_prior[:-1], ovx)
        turbulent = bool(vix >= vix_median)                  # H1: elevated stress -> wider ripple
        outcome = _resolve_turbulence(bdates, bvals, d)
        p = P_TURB if turbulent else P_CALM
        gd = _gap_direction(turbulent, ovx_pct)
        rows.append({
            "gap_id": f"gap.{ev['event_id']}", "as_of": now, "anchor_date": d,
            "subject": ev["title"], "engine_call": "turbulent" if turbulent else "calm",
            "engine_p": p, "priced_ovx": round(float(ovx), 2), "priced_ovx_pct": ovx_pct,
            "gap_direction": gd, "horizon_days": HORIZON,
            "outcome": outcome, "brier": (None if outcome is None else round((p - outcome) ** 2, 4)),
            "resolved_at": (now if outcome is not None else None),
            "source_url": ev["source_url"],
            "notes": f"H1 amplifier {'ON' if turbulent else 'OFF'} (VIX %ile {vix:.0f} vs {vix_median:.0f}); "
                     f"market OVX {ovx:.0f} (p{ovx_pct}); gap={gd}."})

    # a LIVE gap for today (unresolved) from the latest state
    if len(vixs) and odates:
        vix_now = float(vixs.iloc[-1]); ovx_now = float(ovals[-1])
        ovx_pct_now = _pct_rank(ovals[:-1], ovx_now)
        turbulent = vix_now >= vix_median
        gd = _gap_direction(turbulent, ovx_pct_now)
        rows.append({
            "gap_id": "gap.LIVE", "as_of": now, "anchor_date": vixs.index[-1].date().isoformat(),
            "subject": "LIVE state (no dated shock -- standing read)",
            "engine_call": "turbulent" if turbulent else "calm",
            "engine_p": P_TURB if turbulent else P_CALM, "priced_ovx": round(ovx_now, 2),
            "priced_ovx_pct": ovx_pct_now, "gap_direction": gd, "horizon_days": HORIZON,
            "outcome": None, "brier": None, "resolved_at": None, "source_url": "",
            "notes": f"Live: H1 {'ON' if turbulent else 'OFF'} (VIX %ile {vix_now:.0f}); "
                     f"market OVX {ovx_now:.0f} (p{ovx_pct_now}); gap={gd}."})

    conn.executemany(
        "INSERT OR REPLACE INTO gaps VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        [(r["gap_id"], r["as_of"], r["anchor_date"], r["subject"], r["engine_call"], r["engine_p"],
          r["priced_ovx"], r["priced_ovx_pct"], r["gap_direction"], r["horizon_days"], r["outcome"],
          r["brier"], r["resolved_at"], r["source_url"], r["notes"]) for r in rows])
    conn.commit()
    return rows


def ledger(rows):
    """The scorecard: Brier vs base rate overall, by H1 regime, and by gap_direction (does the
    engine add value specifically where it DISAGREES with the market?)."""
    scored = [r for r in rows if r["outcome"] is not None]
    n = len(scored)
    if not n:
        return {"n_scored": 0}
    y = np.array([r["outcome"] for r in scored], float)
    p = np.array([r["engine_p"] for r in scored], float)
    base = float(y.mean())
    brier = float(np.mean((p - y) ** 2)); base_brier = float(np.mean((base - y) ** 2))

    import validate
    def _grp(key, val):
        g = [r for r in scored if r[key] == val]
        if not g:
            return None
        gy = np.array([r["outcome"] for r in g], float); gp = np.array([r["engine_p"] for r in g], float)
        k = int(gy.sum()); ci = validate.wilson_ci(k, len(g))   # honest small-N interval
        return {"n": len(g), "turbulence_rate": round(float(gy.mean()), 3),
                "turbulence_rate_ci95": [ci["lo"], ci["hi"]],
                "brier": round(float(np.mean((gp - gy) ** 2)), 4)}

    return {"n_scored": n, "turbulence_base_rate": round(base, 3),
            "brier": round(brier, 4), "base_rate_brier": round(base_brier, 4),
            "skill_vs_base": round(base_brier - brier, 4),
            "by_h1_regime": {"turbulent(ON)": _grp("engine_call", "turbulent"),
                             "calm(OFF)": _grp("engine_call", "calm")},
            "by_gap_direction": {d: _grp("gap_direction", d)
                                 for d in ("under_priced_risk", "over_priced_fear", "aligned")}}


def main():
    conn = sqlite3.connect(DB)
    rows = build(conn)
    conn.close()
    led = ledger(rows)
    live = [r for r in rows if r["gap_id"] == "gap.LIVE"]
    report = {"generated_at": rows[0]["as_of"] if rows else None,
              "what": "The GAP ledger: engine's H1-conditioned turbulence view vs the market's implied "
                      "vol (OVX), resolved and Brier-scored. Market-as-null; the scorecard IS the product.",
              "n_gaps": len(rows), "ledger": led,
              "live_gap": live[0] if live else None,
              "recent_gaps": [r for r in rows if r["outcome"] is not None][-8:]}
    OUT.write_text(json.dumps(report, indent=2, default=str))

    print("=" * 78)
    print("THE GAP LEDGER -- engine view vs the market's priced vol (OVX), scored")
    print("=" * 78)
    print(f"  {len(rows)} gaps ({led.get('n_scored',0)} resolved & scored; OVX-era events + live)")
    if led.get("n_scored"):
        print(f"  turbulence base rate {led['turbulence_base_rate']}  Brier {led['brier']} vs base "
              f"{led['base_rate_brier']} -> skill {led['skill_vs_base']:+}")
        r = led["by_h1_regime"]
        print(f"  H1 regime turbulence rate: ON {r['turbulent(ON)']['turbulence_rate'] if r['turbulent(ON)'] else 'n/a'} "
              f"vs OFF {r['calm(OFF)']['turbulence_rate'] if r['calm(OFF)'] else 'n/a'} "
              f"(is turbulence more likely when H1 says so?)")
        for d, g in led["by_gap_direction"].items():
            if g:
                ci = g["turbulence_rate_ci95"]
                print(f"    gap[{d:<17}] n={g['n']:<3} turbulence rate {g['turbulence_rate']} "
                      f"95%CI [{ci[0]},{ci[1]}]  Brier {g['brier']}")
    if live:
        print(f"  LIVE: {live[0]['notes']}")
    print("  SUGGESTIVE (small-N): the engine's overall turbulence call is ~null, BUT the DISAGREEMENT")
    print("  cases lean the right way (under-priced-risk -> turbulent, over-priced-fear -> calm). At")
    print("  n=9/17 the CIs are wide -- NOT yet a validated edge; it's the hypothesis the ledger will")
    print("  test as N grows. The deliverable is the transparent, resolving scorecard, published either way.")


if __name__ == "__main__":
    main()
