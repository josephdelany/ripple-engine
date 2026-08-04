"""
backfill.py -- run the registered admission rule over the candidate pool (VISION_ROADMAP V2.2).

Applies src/admission_rule.py (the codebook-registered 5-gate rule) to every pending candidate in
data/candidate_events.csv and routes each honestly:
  * AUTO_ADMIT (all 5 gates pass) -> reported for admission via the sanctioned path (rare here: the
    pool is single-source GDELT, which fails gate G1 by construction).
  * BORDERLINE (any gate fails) -> data/borderline_queue.csv for Joe: RANKED (triage 'keep' first,
    then most-recent), CAPPED, and EXPIRING (the cap drops the lowest-ranked stale ones -- never a
    silent admit), each tagged with the gates it failed.

Publishes a gate-failure histogram so the pool's shape is visible (e.g. "600 fail G1: single-source").
Does NOT write canon. numpy-free; deterministic.

Run:  python3 src/backfill.py
"""

import csv
import json
import sqlite3
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import admission_rule as AR

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
CANDIDATES = ROOT / "data" / "candidate_events.csv"
REVIEW = ROOT / "data" / "candidate_review.csv"
QUEUE = ROOT / "data" / "borderline_queue.csv"
FLAGS = ROOT / "data" / "audit_flags.json"          # V2.3: audit-blocked event types
QUEUE_CAP = 300


def _blocked_types():
    """Event types with an open audit flag -> auto-admission blocked until Joe clears them."""
    if not FLAGS.exists():
        return set()
    try:
        return set(json.loads(FLAGS.read_text()).keys())
    except (ValueError, OSError):
        return set()


def _review_index():
    """event_id -> (recommendation, salience) from triage, for ranking the queue."""
    idx = {}
    if REVIEW.exists():
        for r in csv.DictReader(open(REVIEW, newline="", encoding="utf-8")):
            try:
                sal = int(r.get("salience_mentions") or 0)
            except ValueError:
                sal = 0
            idx[(r.get("event_id") or "").strip()] = ((r.get("recommendation") or "").strip().lower(), sal)
    return idx


def run():
    conn = sqlite3.connect(DB)
    existing = conn.execute("SELECT event_date, type FROM events").fetchall()
    have = {r[0] for r in conn.execute("SELECT event_id FROM events")}
    conn.close()
    today = datetime.now(timezone.utc).date()
    review = _review_index()

    cands = [r for r in csv.DictReader(open(CANDIDATES, newline="", encoding="utf-8"))
             if r.get("status") == "candidate" and (r.get("event_id") or "").strip() not in have] \
        if CANDIDATES.exists() else []

    blocked = _blocked_types()
    auto, borderline, gate_fail = [], [], Counter()
    for r in cands:
        res = AR.evaluate(r, existing, today)
        if res["verdict"] == "AUTO_ADMIT" and r.get("type") in blocked:
            res = {"verdict": "BORDERLINE", "gates": res["gates"],
                   "reasons": [f"audit-blocked domain '{r.get('type')}' (open flag; Joe must clear)"]}
        if res["verdict"] == "AUTO_ADMIT":
            auto.append(r)
        else:
            for g, ok in res["gates"].items():
                if not ok:
                    gate_fail[g] += 1
            rec, sal = review.get((r.get("event_id") or "").strip(), ("", 0))
            borderline.append({"event_id": r.get("event_id"), "event_date": r.get("event_date"),
                               "type": r.get("type"), "title": (r.get("title") or "")[:120],
                               "triage": rec, "salience": sal,
                               "failed_gates": "; ".join(res["reasons"]),
                               "queued_at": today.isoformat()})

    # PRESERVE genuine manually-added borderline entries (real 2-source events held on G5, e.g. Wagner/
    # Angola/Keystone) -- they are NOT in the candidate pool, so don't let the rewrite drop them.
    cand_ids = {(r.get("event_id") or "").strip() for r in cands}
    fresh_ids = {r["event_id"] for r in borderline}
    manual = []
    if QUEUE.exists():
        for r in csv.DictReader(open(QUEUE, newline="", encoding="utf-8")):
            eid = (r.get("event_id") or "").strip()
            if eid and eid not in cand_ids and eid not in fresh_ids and eid not in have:
                manual.append(r)

    # rank: triage 'keep' first, then higher salience, then most-recent event_date. Cap (expire the tail).
    borderline.sort(key=lambda r: (r["triage"] != "keep", -r["salience"], r["event_date"]), reverse=False)
    # manual (real) entries always kept, ahead of the GDELT-derived pool (which is capped/expiring)
    kept, dropped = manual + borderline[:QUEUE_CAP], borderline[QUEUE_CAP:]
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    with open(QUEUE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["event_id", "event_date", "type", "title", "triage",
                                          "salience", "failed_gates", "queued_at"])
        w.writeheader(); w.writerows(kept)
    return {"n_candidates": len(cands), "auto_admit": len(auto),
            "borderline": len(borderline), "queued": len(kept), "expired": len(dropped),
            "gate_fail": dict(gate_fail), "auto_ids": [a.get("event_id") for a in auto]}


def main():
    r = run()
    print("=" * 78)
    print("BACKFILL -- registered admission rule over the candidate pool (V2.2)")
    print("=" * 78)
    print(f"  pending candidates:  {r['n_candidates']}")
    print(f"  AUTO_ADMIT:          {r['auto_admit']}"
          + (f"  {r['auto_ids']}" if r['auto_admit'] else "  (none -- pool is single-source, fails G1)"))
    print(f"  BORDERLINE -> queue: {r['queued']} kept, {r['expired']} expired past cap {QUEUE_CAP}")
    print("  gate-failure histogram (how many candidates each gate rejects):")
    for g in ("G1_two_independent_sources", "G2_date_precision_day", "G3_clean_entity_match",
              "G4_passes_cage", "G5_not_cluster_duplicate"):
        print(f"    {g:32} {r['gate_fail'].get(g, 0)}")
    print(f"\n  Wrote {QUEUE}. Canon unchanged -- borderline is Joe's; auto-admit only under the rule.")


if __name__ == "__main__":
    main()
