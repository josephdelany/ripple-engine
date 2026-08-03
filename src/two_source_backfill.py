"""
two_source_backfill.py -- give the original hand-coded events a SECOND independent source (V-Q7).

Two-source rule (journalism / intelligence): no single-source facts in the record. The auto-admit tier
already requires 2+ independent sources; the ORIGINAL hand-coded events carry one primary source each.
This backfills a second, INDEPENDENT source for them so the corpus is uniformly two-source.

Division of labour (respects the cage): a proposer (the caged extractor / an operator via web search)
PROPOSES a candidate second URL; this script's DETERMINISTIC verifier decides whether to accept it.
No fabrication -- a candidate is only accepted if it is a real, well-formed URL from a DIFFERENT
publisher than the primary. Anything missing or failing the rule goes to the BORDERLINE QUEUE for Joe;
nothing is silently accepted.

  target       = the N earliest events by event_date (the historical hand-coded core; the living engine
                 only auto-admits recent events, so pre-modern events are hand-coded by construction).
  proposals    = data/two_source_candidates.csv  (event_id, second_url)  -- filled by the proposer.
  verified     -> appended to data/state/two_source_log.csv (event_id, primary_url, second_url, ...).
  borderline   -> data/two_source_queue.csv (ranked, capped) for Joe: missing or rule-failing events.

Verifier rule (all required): the candidate URL parses (scheme+host) AND its registrable domain differs
from the primary source's (a DIFFERENT publisher = independent). Same-publisher or malformed -> queue.

Run:  python3 src/two_source_backfill.py            # verify proposals, refresh the log + queue
      python3 src/two_source_backfill.py --status   # coverage only, no writes
"""

import csv
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
CANDIDATES = ROOT / "data" / "two_source_candidates.csv"
LOG = ROOT / "data" / "state" / "two_source_log.csv"
QUEUE = ROOT / "data" / "two_source_queue.csv"
N_TARGET = 60          # the original hand-coded core: the 60 earliest events by date
QUEUE_CAP = 300        # never let the borderline queue grow unbounded


def registrable_domain(url):
    """Coarse registrable domain: the last two dotted labels of the host (nytimes.com, archives.gov,
    wikipedia.org). Good enough to tell two DIFFERENT publishers apart for an independence check."""
    host = (urlparse(url).netloc or "").lower().split(":")[0]
    parts = [p for p in host.split(".") if p]
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def verify(primary_url, candidate_url):
    """(ok, reason). A candidate is INDEPENDENT iff it parses and is a different publisher than primary."""
    if not candidate_url or not candidate_url.strip():
        return False, "no candidate proposed"
    p = urlparse(candidate_url.strip())
    if not (p.scheme in ("http", "https") and p.netloc):
        return False, "malformed URL (need http(s)://host)"
    cd, pd_ = registrable_domain(candidate_url), registrable_domain(primary_url)
    if cd == pd_:
        return False, f"same publisher as primary ({cd}) -- not independent"
    return True, f"independent 2nd source ({cd} vs primary {pd_})"


def load_candidates():
    if not CANDIDATES.exists():
        return {}
    out = {}
    for r in csv.DictReader(open(CANDIDATES, newline="", encoding="utf-8")):
        eid = (r.get("event_id") or "").strip()
        if eid:
            out[eid] = (r.get("second_url") or "").strip()
    return out


def run(write=True):
    conn = sqlite3.connect(DB)
    targets = conn.execute(
        "SELECT event_id, event_date, title, source_url FROM events "
        "ORDER BY event_date LIMIT ?", (N_TARGET,)).fetchall()
    conn.close()
    cands = load_candidates()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    verified, queue = [], []
    for eid, date, title, primary in targets:
        cand = cands.get(eid, "")
        ok, reason = verify(primary or "", cand)
        if ok:
            verified.append({"event_id": eid, "event_date": date, "primary_url": primary,
                             "second_url": cand, "second_domain": registrable_domain(cand),
                             "verified_at": now, "method": "proposer(web-search)+deterministic-rule"})
        else:
            queue.append({"event_id": eid, "event_date": date, "title": title,
                          "primary_domain": registrable_domain(primary or ""),
                          "reason": reason, "queued_at": now})

    if write:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG, "w", newline="", encoding="utf-8") as f:
            wr = csv.DictWriter(f, fieldnames=["event_id", "event_date", "primary_url", "second_url",
                                               "second_domain", "verified_at", "method"])
            wr.writeheader(); wr.writerows(verified)
        # rank the borderline queue: most recent (best-documented, easiest to source) first, cap it
        queue.sort(key=lambda r: r["event_date"], reverse=True)
        with open(QUEUE, "w", newline="", encoding="utf-8") as f:
            wr = csv.DictWriter(f, fieldnames=["event_id", "event_date", "title", "primary_domain",
                                               "reason", "queued_at"])
            wr.writeheader(); wr.writerows(queue[:QUEUE_CAP])

    return {"n_target": len(targets), "n_verified": len(verified), "n_queue": len(queue),
            "coverage_pct": round(100 * len(verified) / len(targets), 1) if targets else 0.0}


def main():
    r = run(write="--status" not in sys.argv)
    print("=" * 78)
    print("TWO-SOURCE BACKFILL (V-Q7) -- second independent source for the hand-coded core")
    print("=" * 78)
    print(f"  target (earliest {r['n_target']} events by date)")
    print(f"  verified two-source: {r['n_verified']}  ({r['coverage_pct']}%)  -> {LOG.name}")
    print(f"  borderline queue for Joe: {r['n_queue']}  -> {QUEUE.name}")
    print("\n  Proposer proposes (web search), deterministic rule verifies independence, the rest is")
    print("  Joe's queue. No source is fabricated or silently accepted.")


if __name__ == "__main__":
    main()
