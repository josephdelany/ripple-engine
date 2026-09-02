"""
heartbeat.py -- is the engine actually alive, or quietly rotting?

WHY THIS EXISTS:
A refresh that "succeeds" but silently stops updating a series is worse than a
crash, because nobody notices. This is the smoke detector. It reads the canonical
database and, for every series, asks one blunt question: when did fresh data last
arrive, and is that overdue for how often this series is supposed to update?

  OK    -- up to date for its cadence
  STALE -- a new reading is overdue by more than 2x the cadence
  DEAD  -- overdue by more than 4x (something is broken, not just late)

Cadence comes from the series table (daily/weekly/monthly). For daily series we
count BUSINESS days, so a normal weekend never looks like staleness; weekly and
monthly series are judged on calendar days.

It also checks the things a dashboard can't see at a glance: how many events are
loaded, how many forecasts are still open, and whether the LAST refresh run had
any failed steps. It writes data/health_status.json (for the dashboard widget)
and prints a report. It EXITS NON-ZERO if anything is STALE/DEAD or the last
refresh failed -- so a scheduler or wrapper can tell that something needs a look.

Run:  python3 src/heartbeat.py
"""

import csv
import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
LOG = ROOT / "data" / "refresh_log.csv"
OUT = ROOT / "data" / "health_status.json"
NTFY_SERVER = os.environ.get("NTFY_SERVER", "https://ntfy.sh")
ALERT_SEEN = ROOT / "data" / "state" / "health_alert_seen.txt"


def push_health_alert(health):
    """Push a phone alert (ntfy) when DATA health is TROUBLE -- so the engine tells you when
    it's broken, not just news. Deduped by the trouble fingerprint so a durable break doesn't
    spam every run; cleared on recovery. No-op (dry-run print) if NTFY_TOPIC is unset."""
    prev = ALERT_SEEN.read_text().strip() if ALERT_SEEN.exists() else ""
    if health["overall"] != "TROUBLE":
        if prev:                                     # recovered -> reset so next break re-alerts
            ALERT_SEEN.write_text("")
        return
    bad = sorted(f"{r['series_id']}:{r['status']}" for r in health["series"]
                 if r["status"] not in ("OK", "CLOSED"))
    if health["last_refresh"].get("state") == "failures":
        bad.append("refresh:failures")
    fingerprint = ";".join(bad)
    if fingerprint == prev:                          # same trouble already alerted
        return
    ALERT_SEEN.parent.mkdir(parents=True, exist_ok=True)
    ALERT_SEEN.write_text(fingerprint)
    topic = os.environ.get("NTFY_TOPIC")
    if not topic:
        print(f"  [health alert dry-run] would push: {fingerprint or 'trouble'}")
        return
    try:
        import requests
        body = "Data health TROUBLE: " + (", ".join(bad[:6]) or "refresh failed")
        requests.post(f"{NTFY_SERVER}/{topic}", data=body.encode("utf-8"),
                      headers={"Title": "Ripple Engine: data health", "Priority": "high",
                               "Tags": "warning"}, timeout=15)
        print(f"  [health alert] pushed to ntfy ({len(bad)} issue(s)).")
    except Exception as e:
        print(f"  [health alert] push failed ({type(e).__name__}).")

CADENCE_DAYS = {"daily": 1, "weekly": 7, "monthly": 30,
                "quarterly": 91, "yearly": 365, "annual": 365}
STALE_MULT, DEAD_MULT = 2, 4

# Per-series publish-lag overrides: some feeds publish with an inherent lag (FRED daily series post
# 2-3 business days late; the GPR index and PortWatch transits lag several days), so "overdue" must be
# measured AFTER subtracting that known lag -- otherwise a perfectly-current feed reads STALE/DEAD.
# Loaded from data/series_cadence_overrides.json (glob or exact series_id -> {cadence_days, publish_lag_days}).
OVERRIDES_FILE = ROOT / "data" / "series_cadence_overrides.json"


def load_overrides():
    import json
    try:
        return json.loads(OVERRIDES_FILE.read_text()) if OVERRIDES_FILE.exists() else {}
    except (ValueError, OSError):
        return {}


def override_for(series_id, overrides):
    """Return (cadence_days_or_None, publish_lag_days) for a series, matching exact id first then a
    'prefix.*' glob (e.g. 'fred.*'). Longest matching prefix wins."""
    if series_id in overrides:
        o = overrides[series_id]
        return o.get("cadence_days"), o.get("publish_lag_days", 0)
    best = None
    for key, o in overrides.items():
        if key.endswith(".*") and series_id.startswith(key[:-1]):
            if best is None or len(key) > len(best[0]):
                best = (key, o)
    if best:
        return best[1].get("cadence_days"), best[1].get("publish_lag_days", 0)
    return None, 0


_ENDS_RE = re.compile(r"ends\s+(\d{4}-\d{2}-\d{2})")
# A dated terminal marker written by a fetcher: the source reported the contract closed, the source
# no longer returns it at all (delisted), or the series was superseded (retired). From that date on
# the series is terminal -- CLOSED, never a broken feed. (2026-09-02, data/integrity_report.txt)
_TERMINAL_RE = re.compile(r"(?:closed|delisted|retired)\s+(\d{4}-\d{2}-\d{2})")


def terminal_date(notes):
    """Return the date of a 'closed/delisted/retired YYYY-MM-DD' marker in notes, else None."""
    if not notes:
        return None
    m = _TERMINAL_RE.search(notes)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y-%m-%d").date()
    except ValueError:
        return None


def contract_end_date(notes):
    """A dated event-contract (e.g. a Polymarket market) records 'ends YYYY-MM-DD' in its notes.
    Return that date if present, else None. A contract whose end date is in the past has RESOLVED --
    it is terminal and will never update again, so it should read CLOSED, not STALE (a resolved
    contract is not a broken feed; flagging it STALE is a false alarm)."""
    if not notes:
        return None
    m = _ENDS_RE.search(notes)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y-%m-%d").date()
    except ValueError:
        return None


def business_days_between(d1, d2):
    """Count weekdays in (d1, d2] -- how many trading days have passed since d1."""
    if d2 <= d1:
        return 0
    days, cur = 0, d1
    while cur < d2:
        cur = cur.fromordinal(cur.toordinal() + 1)
        if cur.weekday() < 5:            # Mon-Fri
            days += 1
    return days


def classify(last_obs, frequency, today, cadence_override=None, publish_lag_days=0):
    """Return (status, elapsed, cadence_days) for one series. `cadence_override` forces the cadence
    (for a series whose declared frequency is missing/wrong); `publish_lag_days` is subtracted from
    elapsed so a feed's inherent publish lag doesn't read as overdue."""
    cadence = cadence_override or CADENCE_DAYS.get((frequency or "").lower(), 1)
    if last_obs is None:
        return "DEAD", None, cadence
    if (frequency or "").lower() == "daily":
        elapsed = business_days_between(last_obs, today)
    else:
        elapsed = (today - last_obs).days
    elapsed = max(0, elapsed - (publish_lag_days or 0))     # discount the feed's inherent publish lag
    ratio = elapsed / cadence
    if ratio > DEAD_MULT:
        return "DEAD", elapsed, cadence
    if ratio > STALE_MULT:
        return "STALE", elapsed, cadence
    return "OK", elapsed, cadence


def last_refresh_status():
    """Look at refresh_log.csv and report the most recent run's outcome."""
    if not LOG.exists():
        return {"state": "none", "detail": "no refresh has run yet"}
    rows = list(csv.DictReader(open(LOG, newline="", encoding="utf-8")))
    if not rows:
        return {"state": "none", "detail": "refresh log is empty"}
    last_ts = max(r["timestamp"] for r in rows)
    last_run = [r for r in rows if r["timestamp"] == last_ts]
    failed = [r["step"] for r in last_run if r["status"] != "OK"]
    return {
        "state": "failures" if failed else "ok",
        "run_id": last_ts,
        "steps": len(last_run),
        "failed_steps": failed,
        "detail": (f"{len(failed)} step(s) failed: {', '.join(failed)}"
                   if failed else f"all {len(last_run)} steps OK"),
    }


def main():
    today = datetime.now(timezone.utc).date()
    conn = sqlite3.connect(DB)

    series = conn.execute(
        "SELECT s.series_id, s.frequency, MAX(o.obs_date), s.notes "
        "FROM series s LEFT JOIN observations o ON o.series_id = s.series_id "
        "GROUP BY s.series_id ORDER BY s.series_id").fetchall()

    overrides = load_overrides()
    reports = []
    for sid, freq, last, notes in series:
        last_date = datetime.strptime(last[:10], "%Y-%m-%d").date() if last else None
        cad_over, lag = override_for(sid, overrides)
        status, elapsed, cadence = classify(last_date, freq, today, cad_over, lag)
        # A dated contract past its end date that has ALSO stopped updating (STALE/DEAD) has
        # resolved: mark it CLOSED, not a broken feed. But if it's still getting fresh snapshots
        # (classify -> OK), it's genuinely live (Polymarket keeps some past-dated markets open) --
        # leave it OK. The fresh-obs signal wins over the nominal end date.
        end_date = contract_end_date(notes)
        if status in ("STALE", "DEAD") and end_date is not None and end_date < today:
            status, elapsed, cadence = "CLOSED", None, None
        term = terminal_date(notes)
        if status in ("STALE", "DEAD") and term is not None and term <= today:
            status, elapsed, cadence = "CLOSED", None, None
        reports.append({
            "series_id": sid,
            "frequency": freq,
            "last_obs": last[:10] if last else None,
            "elapsed": elapsed,
            "cadence_days": cadence,
            "status": status,
        })

    events_count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    forecasts_pending = conn.execute(
        "SELECT COUNT(*) FROM forecasts WHERE outcome IS NULL").fetchone()[0]
    conn.close()

    refresh = last_refresh_status()

    # Overall status = worst series status, or trouble if last refresh failed.
    # CLOSED (resolved contracts) ranks below OK -- it is never trouble.
    order = {"CLOSED": -1, "OK": 0, "STALE": 1, "DEAD": 2}
    worst = max((r["status"] for r in reports), key=lambda s: order[s], default="OK")
    trouble = worst in ("STALE", "DEAD") or refresh["state"] == "failures"
    overall = "TROUBLE" if trouble else "OK"

    health = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "overall": overall,
        "series": reports,
        "events_count": events_count,
        "forecasts_pending": forecasts_pending,
        "last_refresh": refresh,
    }
    OUT.write_text(json.dumps(health, indent=2))
    push_health_alert(health)                        # ping the phone if data is broken

    # --- Human-readable report ---
    print("=" * 72)
    print(f"RIPPLE ENGINE HEALTH  --  {health['generated_at']}   [{overall}]")
    print("=" * 72)
    print(f"  {'series':<26}{'freq':<8}{'last obs':<12}{'overdue':<10}status")
    print("  " + "-" * 68)
    for r in sorted(reports, key=lambda r: order[r["status"]], reverse=True):
        overdue = "-" if r["elapsed"] is None else f"{r['elapsed']}/{r['cadence_days']*DEAD_MULT}"
        flag = "" if r["status"] == "OK" else "  <--"
        print(f"  {r['series_id']:<26}{str(r['frequency']):<8}"
              f"{str(r['last_obs']):<12}{overdue:<10}{r['status']}{flag}")
    print("  " + "-" * 68)
    print(f"  events loaded:      {events_count}")
    print(f"  forecasts pending:  {forecasts_pending}")
    print(f"  last refresh:       {refresh['detail']}"
          + (f"  ({refresh['run_id']})" if refresh.get("run_id") else ""))
    print(f"\n  Wrote {OUT}")

    counts = {s: sum(1 for r in reports if r["status"] == s) for s in ("OK", "STALE", "DEAD", "CLOSED")}
    print(f"  Series: {counts['OK']} OK, {counts['STALE']} STALE, {counts['DEAD']} DEAD, "
          f"{counts['CLOSED']} CLOSED (resolved contracts)")
    if trouble:
        print("\n  STATUS: TROUBLE -- something is stale/dead or the last refresh failed.")
        print("  ('overdue' column = business days (daily) or calendar days since last "
              "obs / the DEAD threshold.)")
        sys.exit(1)
    print("\n  STATUS: OK -- everything is current.")
    sys.exit(0)


if __name__ == "__main__":
    main()
