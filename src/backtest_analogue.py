"""
backtest_analogue.py -- point-in-time validation of the analogue engine (Stage 5, early).

The analogue forecaster claims a probability that oil will spike after a shock. Is that
claim any good? This runs the honest test: WALK-FORWARD, point-in-time.

For each of the 52 sourced historical events, we:
  1. rebuild the analogue library as it would have looked THEN -- only analogues dated
     strictly BEFORE the event (no lookahead),
  2. read the engine's implied P(Brent spikes >= 5% in 20 trading days) from those analogues,
  3. resolve it against what Brent ACTUALLY did in the 20 trading days after the event,
  4. score the whole set with Brier + a reliability curve.

Skill > 0 means the analogue base rate carries information beyond always predicting the base
rate. This is the pre-registered kind of gate from PHASE2_NORTH_STAR (OOS Brier < base-rate
Brier). It reuses the SAME forecaster code the live engine uses (src/analogue.py) -- so a
pass here is evidence the live forecast is trustworthy, and a fail is reported honestly.

Deterministic; no LLM. Run:  python3 src/backtest_analogue.py
"""

import csv
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import analogue                      # our own module (same dir) -- reuse the live forecaster

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
EVENTS = ROOT / "data" / "events.csv"
OUT = ROOT / "data" / "backtest_analogue.json"

SPIKE = 0.05
HORIZON_TD = 20
BRENT = "fred.DCOILBRENTEU"

# events.csv `type` -> analogue-library query (extends analogue.KIND_TO_QUERY).
TYPE_QUERY = dict(analogue.KIND_TO_QUERY)
TYPE_QUERY.setdefault("demand_shock", {"event_type": "commodity_supply",
                                       "archetype": "commodity_supply_shock"})
DEFAULT_Q = {"event_type": "geo", "archetype": "geopolitical_shock"}


def brent_series(conn):
    rows = conn.execute(
        "SELECT obs_date, value FROM observations WHERE series_id=? AND value IS NOT NULL "
        "ORDER BY obs_date", (BRENT,)).fetchall()
    return [d for d, _ in rows], [v for _, v in rows]


def resolve_spike(dates, vals, event_date):
    """Point-in-time resolution: did Brent spike >= 5% in the 20 trading days AFTER the first
    trading day on/after event_date? Returns 1/0, or None if not enough forward data."""
    i = next((k for k, d in enumerate(dates) if d >= event_date), None)
    if i is None or i + HORIZON_TD >= len(dates):
        return None
    return 1 if analogue_is_spike(vals[i], vals[i + 1:i + 1 + HORIZON_TD]) else 0


def analogue_is_spike(base, window):
    return bool(window) and (max(window) / base - 1) >= SPIKE


def reliability(records, edges=(0.0, 0.2, 0.4, 0.6, 0.8, 1.01)):
    """Bin forecasts by predicted probability; report mean predicted vs mean realised."""
    bins = []
    for lo, hi in zip(edges, edges[1:]):
        grp = [r for r in records if lo <= r["p"] < hi]
        if grp:
            bins.append({"range": f"{lo:.1f}-{min(hi,1.0):.1f}", "n": len(grp),
                         "mean_pred": round(sum(r["p"] for r in grp) / len(grp), 3),
                         "mean_outcome": round(sum(r["outcome"] for r in grp) / len(grp), 3)})
    return bins


def run():
    conn = sqlite3.connect(DB)
    dates, vals = brent_series(conn)
    conn.close()
    library = analogue.load_library()
    events = list(csv.DictReader(EVENTS.open()))

    records, skipped = [], 0
    for e in events:
        d = e["event_date"]
        pit = [o for o in library if (o.get("event_date") or "") < d]   # point-in-time
        if len(pit) < analogue.MIN_ANALOGUES:
            skipped += 1
            continue
        q = TYPE_QUERY.get(e.get("type"), DEFAULT_Q)
        matches = analogue.search_multi([q], pit)
        dist, _ = analogue.outcome_distribution(matches)
        oil = dist.get("wti") or dist.get("brent")
        if not oil or not oil.get("n"):
            skipped += 1
            continue
        p = round(oil["patterns"].get("overshoot", 0) / oil["n"], 3)
        outcome = resolve_spike(dates, vals, d)
        if outcome is None:
            skipped += 1
            continue
        records.append({"event_id": e["event_id"], "date": d, "type": e.get("type"),
                        "p": p, "outcome": outcome, "n_analogues": len(matches)})

    n = len(records)
    report = {"as_of": datetime.now(timezone.utc).date().isoformat(),
              "n_events": len(events), "n_scored": n, "n_skipped": skipped,
              "spike_threshold": SPIKE, "horizon_td": HORIZON_TD,
              "note": "Point-in-time walk-forward: analogue P(Brent +5% in 20td) vs realised, "
                      "prior-only analogues. Reuses src/analogue.py. Small N -- indicative."}
    if n:
        brier = round(sum((r["p"] - r["outcome"]) ** 2 for r in records) / n, 4)
        base = round(sum(r["outcome"] for r in records) / n, 3)
        base_brier = round(sum((base - r["outcome"]) ** 2 for r in records) / n, 4)
        report.update({"brier": brier, "base_rate": base, "base_rate_brier": base_brier,
                       "skill_vs_base": round(base_brier - brier, 4),
                       "reliability": reliability(records), "records": records})
    OUT.write_text(json.dumps(report, indent=2))
    return report


def main():
    r = run()
    if not r.get("n_scored"):
        print(f"backtest_analogue -- 0 scored ({r['n_skipped']} skipped for thin analogues / "
              "insufficient forward data).")
        return
    print(f"backtest_analogue -- scored {r['n_scored']}/{r['n_events']} events "
          f"({r['n_skipped']} skipped).")
    print(f"  Brier {r['brier']}  vs base-rate {r['base_rate_brier']}  "
          f"-> skill {r['skill_vs_base']:+}  (base rate of spikes {r['base_rate']})")
    print("  reliability (pred -> realised):")
    for b in r["reliability"]:
        print(f"    {b['range']}  n={b['n']:<3} pred {b['mean_pred']}  realised {b['mean_outcome']}")


if __name__ == "__main__":
    main()
