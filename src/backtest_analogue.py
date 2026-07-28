"""
backtest_analogue.py -- point-in-time validation of the analogue engine (Stage 5, early).

RE-SPEC (2026-07-28): the first target (P of a +5% Brent spike) was falsified here (skill
-0.25). This validates the re-specified target from auto_forecast.py:

    P(oil TURBULENCE) = P(realised Brent vol RISES in the 20 trading days after a shock),
    forecast by the share of prior analogues whose oil pattern was NON-clean.

The test is honest and point-in-time. For each of the 52 sourced events:
  1. rebuild the analogue library as it looked THEN (only analogues dated before the event),
  2. read the engine's P(turbulence) from those analogues,
  3. resolve vs realised Brent: was forward-20d vol > pre-event-20d vol?
  4. score Brier + reliability, and report skill vs the base rate.

Skill > 0 means the analogue non-clean share carries information (the PHASE2_NORTH_STAR gate:
OOS Brier < base-rate Brier). Reuses src/analogue.py, so a pass reflects the LIVE forecaster.
A fail is reported, not buried. Deterministic; no LLM. Run: python3 src/backtest_analogue.py
"""

import csv
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import analogue
from auto_forecast import p_turbulence, vol_rose      # reuse the live forecaster + resolver

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
EVENTS = ROOT / "data" / "events.csv"
OUT = ROOT / "data" / "backtest_analogue.json"

HORIZON_TD = 20
BRENT = "fred.DCOILBRENTEU"

TYPE_QUERY = dict(analogue.KIND_TO_QUERY)
TYPE_QUERY.setdefault("demand_shock", {"event_type": "commodity_supply",
                                       "archetype": "commodity_supply_shock"})
DEFAULT_Q = {"event_type": "geo", "archetype": "geopolitical_shock"}


def brent_series(conn):
    rows = conn.execute(
        "SELECT obs_date, value FROM observations WHERE series_id=? AND value IS NOT NULL "
        "ORDER BY obs_date", (BRENT,)).fetchall()
    return [d for d, _ in rows], [v for _, v in rows]


def resolve_turbulence(dates, vals, event_date):
    """Point-in-time: did realised vol rise from the 20td before to the 20td after? None if
    not enough data on either side."""
    i = next((k for k, d in enumerate(dates) if d >= event_date), None)
    if i is None or i < HORIZON_TD or i + HORIZON_TD >= len(dates):
        return None
    rose = vol_rose(vals[i - HORIZON_TD:i + 1], vals[i:i + HORIZON_TD + 1])
    return None if rose is None else (1 if rose else 0)


def reliability(records, edges=(0.0, 0.2, 0.4, 0.6, 0.8, 1.01)):
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
        pit = [o for o in library if (o.get("event_date") or "") < d]
        if len(pit) < analogue.MIN_ANALOGUES:
            skipped += 1
            continue
        q = TYPE_QUERY.get(e.get("type"), DEFAULT_Q)
        matches = analogue.search_multi([q], pit)
        dist, _ = analogue.outcome_distribution(matches)
        fc = {"key_assets": {k: dist[k] for k in ("wti", "brent") if k in dist}}
        p = p_turbulence(fc)
        outcome = resolve_turbulence(dates, vals, d)
        if p is None or outcome is None:
            skipped += 1
            continue
        records.append({"event_id": e["event_id"], "date": d, "type": e.get("type"),
                        "p": p, "outcome": outcome, "n_analogues": len(matches)})

    n = len(records)
    report = {"as_of": datetime.now(timezone.utc).date().isoformat(),
              "n_events": len(events), "n_scored": n, "n_skipped": skipped,
              "target": "P(realised Brent vol rises over 20 trading days)", "horizon_td": HORIZON_TD,
              "note": "Point-in-time walk-forward: analogue non-clean share vs whether realised "
                      "Brent vol rose. Prior-only analogues; reuses src/analogue.py. Small N."}
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
        print(f"backtest_analogue -- 0 scored ({r['n_skipped']} skipped).")
        return
    print(f"backtest_analogue -- target: {r['target']}")
    print(f"  scored {r['n_scored']}/{r['n_events']} ({r['n_skipped']} skipped).")
    print(f"  Brier {r['brier']}  vs base-rate {r['base_rate_brier']}  "
          f"-> skill {r['skill_vs_base']:+}  (base rate {r['base_rate']})")
    for b in r["reliability"]:
        print(f"    {b['range']}  n={b['n']:<3} pred {b['mean_pred']}  realised {b['mean_outcome']}")


if __name__ == "__main__":
    main()
