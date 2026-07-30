"""
coverage.py -- is the engine actually WATCHING all six domains, or are there blind spots?

The living engine only captures what the watcher sees. This reports, per analyst domain, how much the
corpus + the live alert stream cover it, and flags UNDERCOVERED domains and DEAD feeds -- so a coverage
hole is visible, not silent. Deterministic; reuses research.DOMAINS. Writes data/coverage_report.json.

Run:  python3 src/coverage.py            # full (checks each RSS feed resolves; network)
      python3 src/coverage.py --no-net   # skip the feed-health check (offline)
"""

import csv
import json
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import research

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
FEEDS = ROOT / "data" / "watch_feeds.txt"
ALERTS = ROOT / "data" / "alert_queue.csv"
OUT = ROOT / "data" / "coverage_report.json"


def _feeds():
    out = []
    if not FEEDS.exists():
        return out
    for line in FEEDS.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) == 2 and parts[1].startswith("http"):
            out.append((parts[0], parts[1]))
    return out


def _feed_health(feeds):
    """Resolve each feed; report entry count. A feed with 0 entries (or that errors) is flagged DEAD."""
    try:
        import feedparser
    except Exception:
        return [{"feed": n, "url": u, "entries": None, "status": "unknown (no feedparser)"} for n, u in feeds]
    rows = []
    for name, url in feeds:
        try:
            d = feedparser.parse(url)
            n = len(d.entries)
            rows.append({"feed": name, "url": url, "entries": n,
                         "status": "ok" if n > 0 else "DEAD (0 entries)"})
        except Exception as e:                     # noqa: BLE001
            rows.append({"feed": name, "url": url, "entries": 0, "status": f"DEAD ({type(e).__name__})"})
    return rows


def run(check_net=True):
    conn = sqlite3.connect(DB)
    # recent alerts (30d) as a proxy for live capture
    recent = []
    if ALERTS.exists():
        cutoff = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        for a in csv.DictReader(open(ALERTS, newline="", encoding="utf-8")):
            if (a.get("timestamp_utc") or "") >= cutoff:
                recent.append(a)

    domains = []
    for dname, d in research.DOMAINS.items():
        types = sorted(d.get("event_types", []))
        n_events, last = 0, None
        for t in types:
            r = conn.execute("SELECT COUNT(*), MAX(event_date) FROM events WHERE type=?", (t,)).fetchone()
            n_events += r[0]
            if r[1] and (last is None or r[1] > last):
                last = r[1]
        # recent alerts whose heuristic_type is one of this domain's types
        n_alerts = sum(1 for a in recent if a.get("heuristic_type") in types)
        # structured series available to this domain (its validated/candidate ripple labels)
        n_nodes = len(d.get("labels", []))
        undercovered = (n_events < 10) or (n_alerts == 0 and bool(types))
        domains.append({"domain": dname, "event_types": types, "n_events": n_events,
                        "last_event": last, "n_alerts_30d": n_alerts, "n_nodes": n_nodes,
                        "status": "UNDERCOVERED" if undercovered else "ok"})
    conn.close()

    feeds = _feeds()
    feed_health = _feed_health(feeds) if check_net else \
        [{"feed": n, "url": u, "entries": None, "status": "unchecked (--no-net)"} for n, u in feeds]
    dead = [f for f in feed_health if str(f["status"]).startswith("DEAD")]

    report = {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "n_feeds": len(feeds), "n_dead_feeds": len(dead),
              "undercovered_domains": [d["domain"] for d in domains if d["status"] == "UNDERCOVERED"],
              "domains": domains, "feeds": feed_health,
              "note": "Coverage = corpus depth + live-alert flow per domain. UNDERCOVERED = <10 corpus "
                      "events OR no alerts in 30d. DEAD feed = resolves to 0 entries; prune or replace."}
    OUT.write_text(json.dumps(report, indent=2))
    return report


def main():
    r = run(check_net="--no-net" not in sys.argv)
    print("=" * 78)
    print("COVERAGE -- are all six domains actually watched?")
    print("=" * 78)
    print(f"  {'domain':<14}{'events':>7}{'last event':>13}{'alerts30d':>11}  status")
    for d in r["domains"]:
        print(f"  {d['domain']:<14}{d['n_events']:>7}{str(d['last_event']):>13}"
              f"{d['n_alerts_30d']:>11}  {d['status']}")
    print(f"\n  feeds: {r['n_feeds']} ({r['n_dead_feeds']} dead)")
    for f in r["feeds"]:
        if str(f["status"]).startswith("DEAD"):
            print(f"    DEAD  {f['feed']:<14} {f['url']}")
    if r["undercovered_domains"]:
        print(f"  UNDERCOVERED: {', '.join(r['undercovered_domains'])} -- add feeds/events there.")
    print(f"\n  wrote {OUT}")


if __name__ == "__main__":
    main()
