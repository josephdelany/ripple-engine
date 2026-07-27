"""
notify.py -- push high-signal alerts to your phone via ntfy (free, no account).

This is the "taps you on the shoulder" step. After the watcher runs, it pushes a
notification ONLY when both conditions hold:
  1. a NEW alert is high-signal (its heuristic type is a supply-relevant one), and
  2. the market is PRIMED (at least one amplifier, H1 VIX or H2 inventories, is ON).
That pairing is the whole point -- a chokepoint headline matters far more when the
market is already stressed/tight. Quiet-market noise stays off your phone.

It is idempotent across runs via a small committed ledger (data/state/notified.csv),
so you are never pinged twice for the same story. It sends nothing unless NTFY_TOPIC
is set (otherwise it's a dry run that just prints what it WOULD send), and it never
forecasts -- the push is a sourced headline + today's amplifier context, nothing more.

Env:
  NTFY_TOPIC   your chosen ntfy topic (e.g. ripple-joe-8f3k). Unset -> dry run.
  NTFY_SERVER  default https://ntfy.sh

Run:  python3 src/notify.py
"""

import csv
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
ALERT_QUEUE = ROOT / "data" / "alert_queue.csv"
ENGINE_READ = ROOT / "data" / "engine_read.json"
LEDGER = ROOT / "data" / "state" / "notified.csv"

# Supply-relevant heuristic types worth a push (the rest stay on the dashboard).
HOT_TYPES = {"chokepoint_disruption", "conflict_escalation",
             "infrastructure_attack", "sanctions"}
RECENCY_DAYS = 3          # don't ping about stale headlines
MAX_PER_RUN = 8           # never burst-spam the phone


def amplifiers_on(engine_read):
    """(is_primed, label) from engine_read.json -- H1/H2 amplifiers that are ON."""
    hyp = (engine_read or {}).get("hypotheses", {})
    on = [h for h in ("H1", "H2") if hyp.get(h, {}).get("amplifier") == "ON"]
    return (bool(on), " ".join(on))


def select_to_notify(alerts, notified, amps_on, now, recency_days=RECENCY_DAYS):
    """Pure selection: which alerts to push. High-signal + primed + fresh + unseen.
    Returns [] if the market is not primed (amps_on False)."""
    if not amps_on:
        return []
    cutoff = now - timedelta(days=recency_days)
    out = []
    for a in alerts:
        url = (a.get("url") or "").strip()
        if not url or url in notified:
            continue
        if a.get("heuristic_type") not in HOT_TYPES:
            continue
        try:
            ts = datetime.fromisoformat((a.get("timestamp_utc") or "").replace("Z", "+00:00"))
        except ValueError:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if ts < cutoff:
            continue
        out.append(a)
    return out[:MAX_PER_RUN]


def load_notified():
    if not LEDGER.exists():
        return set()
    with open(LEDGER, newline="", encoding="utf-8") as f:
        return {r["url"] for r in csv.DictReader(f) if r.get("url")}


def record_notified(rows, now_iso):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    new = not LEDGER.exists()
    with open(LEDGER, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["url", "sent_at"])
        for a in rows:
            w.writerow([a.get("url", ""), now_iso])


def push(alert, amp_label, topic, server):
    """POST one notification to ntfy. Returns True on success."""
    title = f"Ripple: {alert.get('heuristic_type', 'alert')} (amps {amp_label} ON)"
    body = f"{alert.get('headline', '')}\n{alert.get('source', '')}"
    try:
        r = requests.post(f"{server}/{topic}", data=body.encode("utf-8"),
                          headers={"Title": title, "Tags": "warning",
                                   "Click": alert.get("url", "")}, timeout=15)
        return r.status_code < 300
    except requests.RequestException as e:
        print(f"  ntfy push failed ({type(e).__name__})")
        return False


def main():
    alerts = list(csv.DictReader(open(ALERT_QUEUE, newline="", encoding="utf-8"))) \
        if ALERT_QUEUE.exists() else []
    er = json.loads(ENGINE_READ.read_text()) if ENGINE_READ.exists() else {}
    amps_on, amp_label = amplifiers_on(er)
    now = datetime.now(timezone.utc)
    picks = select_to_notify(alerts, load_notified(), amps_on, now)

    topic = os.environ.get("NTFY_TOPIC")
    server = os.environ.get("NTFY_SERVER", "https://ntfy.sh")
    if not picks:
        print(f"notify -- nothing to push (amplifiers "
              f"{'ON: ' + amp_label if amps_on else 'OFF'}).")
        return
    if not topic:
        print(f"notify -- DRY RUN (set NTFY_TOPIC to send). Would push {len(picks)}:")
        for a in picks:
            print(f"    [{a.get('heuristic_type')}] {a.get('headline', '')[:70]}")
        return
    sent = [a for a in picks if push(a, amp_label, topic, server)]
    record_notified(sent, now.isoformat(timespec="seconds"))
    print(f"notify -- pushed {len(sent)}/{len(picks)} high-signal alerts to "
          f"ntfy topic '{topic}' (amps {amp_label} ON).")


if __name__ == "__main__":
    main()
