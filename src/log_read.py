"""
log_read.py -- log one of the engine's conditional reads into the record (Wire 4).

A "read" records what the engine EXPECTS, so it can later be scored against what
actually happened. You endorse a read manually (you are in the loop); the engine
does not auto-log. It captures the base-rate magnitude expectation for an event
type at a horizon, anchored to today's price -- NOT a probability, and NOT a claim
that the event will occur. resolve_reads.py later fills in the realized move and
the error.

Example:
  python3 src/log_read.py --kind chokepoint_disruption --situation \
      situation.israel_iran_war_2025
  python3 src/log_read.py --kind conflict_escalation --horizon 5

The expected CAR comes from engine_read.json's clustered base rates (the same
numbers the dossier shows). Horizon must be one the engine reports: 1, 5, 10, 20.
"""

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
ENGINE_READ = ROOT / "data" / "engine_read.json"
BRENT = "fred.DCOILBRENTEU"
CAR_FIELD = {1: "car1", 5: "car5", 10: "car10", 20: "car20"}


def latest_obs(conn, series_id):
    """(obs_date, value) of the most recent observation, or (None, None)."""
    row = conn.execute(
        "SELECT obs_date, value FROM observations WHERE series_id=? "
        "ORDER BY obs_date DESC, as_of DESC LIMIT 1", (series_id,)).fetchone()
    return (row[0], row[1]) if row else (None, None)


def main():
    ap = argparse.ArgumentParser(description="Log an engine read into the record.")
    ap.add_argument("--kind", required=True, help="event type (e.g. chokepoint_disruption)")
    ap.add_argument("--situation", default=None, help="optional situation_id link")
    ap.add_argument("--horizon", type=int, default=20, choices=[1, 5, 10, 20])
    ap.add_argument("--notes", default="")
    args = ap.parse_args()

    if not ENGINE_READ.exists():
        raise SystemExit("engine_read.json not found -- run engine_read.py first.")
    er = json.loads(ENGINE_READ.read_text())
    base = {b["type"]: b for b in er.get("base_rates", [])}
    if args.kind not in base:
        raise SystemExit(f"no base rate for kind '{args.kind}'. Known: "
                         f"{sorted(base)}")
    expected = base[args.kind][CAR_FIELD[args.horizon]]
    n = base[args.kind].get("n")

    conn = sqlite3.connect(DB)
    anchor_date, anchor_value = latest_obs(conn, BRENT)
    if anchor_date is None:
        raise SystemExit("no Brent observations to anchor the read.")
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    amp = [f"{h}:{er['hypotheses'][h].get('amplifier')}"
           for h in ("H1", "H2", "H3") if h in er.get("hypotheses", {})]
    conn.execute(
        "INSERT INTO reads (made_at, situation_id, kind, anchor_date, "
        "anchor_series, anchor_value, horizon_days, expected_car, basis, "
        "amp_context, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (now, args.situation, args.kind, anchor_date, BRENT, anchor_value,
         args.horizon, expected,
         f"clustered base rate n={n} from engine_read {er.get('as_of')}",
         " ".join(amp), args.notes))
    conn.commit()
    rid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    print(f"Logged read #{rid}: {args.kind} CAR+{args.horizon} expected "
          f"{expected:+.1f}% (Brent ${anchor_value:.2f} @ {anchor_date}, "
          f"amps {' '.join(amp)}). Pending resolution in ~{args.horizon} "
          f"trading days.")


if __name__ == "__main__":
    main()
