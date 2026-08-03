"""
status.py -- one verdict: is the engine healthy AND complete right now? (GREEN / AMBER / RED)

Composes the sub-signals the human, the cockpit, and the conversational layer all want in one glance:
data freshness (heartbeat), coverage (coverage_report), the last run (last_run.json), the review-queue
depth, backups (+ whether restore is tested), and the evaluation's framework-sound flag. No new data
pulls -- pure assembly of committed artifacts. Writes data/engine_status.json.

  GREEN  -- fresh, covered, last run OK, framework sound.
  AMBER  -- a coverage gap / review backlog / lag-artifact staleness / no last-run record yet.
  RED    -- a real DEAD feed-through (data broken), last run crashed, or the framework check failed.

Run:  python3 src/status.py
"""

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "engine_status.json"


def _rj(name):
    p = DATA / name
    try:
        return json.loads(p.read_text()) if p.exists() else {}
    except (ValueError, OSError):
        return {}


def run():
    health = _rj("health_status.json")
    cov = _rj("coverage_report.json")
    last = _rj("last_run.json")
    ev = _rj("evaluation.json")

    # freshness: heartbeat's overall (post lag-overrides, real breaks still trip)
    series = health.get("series", [])
    dead = [s for s in series if s.get("status") == "DEAD"]
    stale = [s for s in series if s.get("status") == "STALE"]
    fresh_ok = not dead
    fresh_amber = bool(stale) and not dead

    # coverage
    undercov = cov.get("undercovered_domains", [])
    dead_feeds = cov.get("n_dead_feeds", 0)

    # review queue depth
    n_pending = 0
    review = DATA / "candidate_review.csv"
    if review.exists():
        for r in csv.DictReader(open(review, newline="", encoding="utf-8")):
            if r.get("candidate_source") == "llm_extract" and not (r.get("joe_decision") or "").strip():
                n_pending += 1

    # backups + restore-tested marker (restore_tested true only if the test file exists in the suite)
    backups = sorted((DATA / "backups").glob("oil_*.db.gz")) if (DATA / "backups").exists() else []
    restore_tested = (ROOT / "tests" / "test_restore.py").exists()

    # last run
    last_verdict = last.get("verdict")
    last_crashed = bool(last.get("failed_steps"))

    framework_sound = (ev.get("overall", {}) or {}).get("framework_sound")

    # V2.3 auto-admission audit: open flags block a domain -> surface as AMBER until Joe clears
    audit_flags = {}
    af = DATA / "audit_flags.json"
    if af.exists():
        try:
            audit_flags = json.loads(af.read_text())
        except (ValueError, OSError):
            audit_flags = {}
    blocked_types = sorted(audit_flags)

    # roll up
    red = bool(dead or last_crashed or framework_sound is False)
    amber = bool(undercov or dead_feeds or fresh_amber or n_pending >= 15
                 or last_verdict is None or framework_sound is None or blocked_types)
    verdict = "RED" if red else ("AMBER" if amber else "GREEN")

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "verdict": verdict,
        "freshness": {"overall": health.get("overall"), "n_dead": len(dead), "n_stale": len(stale),
                      "dead_series": [s["series_id"] for s in dead][:10]},
        "coverage": {"undercovered_domains": undercov, "n_dead_feeds": dead_feeds},
        "review_queue": {"n_pending": n_pending},
        "last_run": {"verdict": last_verdict, "failed_steps": last.get("failed_steps", []),
                     "run_id": last.get("run_id")},
        "backups": {"count": len(backups), "newest": backups[-1].name if backups else None,
                    "restore_tested": restore_tested},
        "evaluation": {"framework_sound": framework_sound},
        "audit": {"blocked_types": blocked_types},
        "reasons": _reasons(dead, stale, undercov, dead_feeds, n_pending, last_verdict, last_crashed,
                            framework_sound, blocked_types),
    }
    OUT.write_text(json.dumps(report, indent=2, default=str))
    return report


def _reasons(dead, stale, undercov, dead_feeds, n_pending, last_verdict, last_crashed, fw,
             blocked_types=()):
    r = []
    if blocked_types:
        r.append(f"AMBER: auto-admission blocked in {list(blocked_types)} (open audit flag -- clear it)")
    if dead:
        r.append(f"RED: {len(dead)} DEAD series (data broken)")
    if last_crashed:
        r.append("RED: last run crashed")
    if fw is False:
        r.append("RED: framework soundness check FAILED")
    if undercov:
        r.append(f"AMBER: undercovered domains {undercov}")
    if dead_feeds:
        r.append(f"AMBER: {dead_feeds} dead feed(s)")
    if stale and not dead:
        r.append(f"AMBER: {len(stale)} STALE series")
    if n_pending >= 15:
        r.append(f"AMBER: {n_pending} events awaiting review")
    if last_verdict is None:
        r.append("AMBER: no last-run record yet (run daily.py)")
    if fw is None:
        r.append("AMBER: evaluation not yet run")
    return r or ["GREEN: fresh, covered, last run OK, framework sound"]


def main():
    r = run()
    print("=" * 60)
    print(f"  ENGINE STATUS: {r['verdict']}")
    print("=" * 60)
    for reason in r["reasons"]:
        print("   " + reason)
    print(f"\n  freshness overall={r['freshness']['overall']} | coverage undercovered="
          f"{r['coverage']['undercovered_domains'] or 'none'} | review pending={r['review_queue']['n_pending']}")
    print(f"  backups={r['backups']['count']} (restore_tested={r['backups']['restore_tested']}) | "
          f"framework_sound={r['evaluation']['framework_sound']}")
    print(f"  wrote {OUT}")


if __name__ == "__main__":
    main()
