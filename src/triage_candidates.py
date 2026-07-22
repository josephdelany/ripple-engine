"""
triage_candidates.py -- MECHANICAL triage of the candidate pile. No LLM. No facts.

WHAT THIS IS (and what it is deliberately NOT):
Reviewing hundreds of candidates by hand is slow, so this tool pre-sorts them and
attaches a keep/reject RECOMMENDATION. But it never asks a model what an event
"was", never summarises the news, never invents a claim. Every signal it uses is
mechanical and checkable:

  (a) price-window fit -- is there enough surrounding price data to even run an
      event study on that date? (mirrors event_study.py's own guard exactly:
      >=130 trading days before and 20 after; no CAR is computed here.)
  (b) episode clustering -- is it within 35 days of an event already in events.csv
      (same episode, already represented), or within 35 days of a STRONGER
      candidate (so this weaker one is a duplicate of that episode)?
  (c) producer involvement -- does an actor match the harvester's own major-
      producer / OPEC filter?
  (d) salience -- GDELT mention count, parsed from the harvester's own note.

The recommendation is a SUGGESTION to speed Joe's eye. The only fact he needs to
check is one he can click: the source_url. Joe's judgment stays in the loop.

Output: data/candidate_review.csv, sorted best-first, with an empty joe_decision
column for Joe to fill (approve/reject), then feed to apply_review.py.

Run:  python3 src/triage_candidates.py
"""

import bisect
import csv
import re
import sqlite3
from datetime import datetime
from pathlib import Path

from harvest_gdelt import PRODUCERS   # reuse the exact producer set the harvester filtered on

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
CANDIDATES = ROOT / "data" / "candidate_events.csv"
EVENTS = ROOT / "data" / "events.csv"
OUT = ROOT / "data" / "candidate_review.csv"

BRENT_SERIES = "fred.DCOILBRENTEU"      # the series event_study.py runs on
EST_BEFORE = 130                        # trading days needed before (event_study EST_START)
POST_AFTER = 20                         # trading days needed after (event_study POST)
CLUSTER_DAYS = 35                       # same window robustness.py collapses episodes on

PRODUCER_NAMES = set(PRODUCERS.values())
MANUAL_SALIENCE = 10 ** 9               # hand-sourced seeds outrank any GDELT count

CAND_FIELDS = ["event_id", "event_date", "date_precision", "type", "title",
               "description", "severity", "surprise", "confidence", "source_url",
               "entities", "status", "candidate_source"]
# recommendation + reason first, then all candidate fields, then the empty
# joe_decision column Joe fills in last.
OUT_FIELDS = ["recommendation", "rec_reason", "salience_mentions"] + CAND_FIELDS + ["joe_decision"]


def load_price_dates():
    """Sorted list of Brent trading-day dates -- the spine of the price-window check."""
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT obs_date FROM observations WHERE series_id=? ORDER BY obs_date",
        (BRENT_SERIES,)).fetchall()
    conn.close()
    return [datetime.strptime(r[0][:10], "%Y-%m-%d").date() for r in rows]


def price_window_ok(evdate, pdates):
    """Exactly event_study.py's guard: first trading day on/after the event needs
    >=EST_BEFORE days before it and >POST_AFTER days after it. Returns (ok, pos, n)."""
    pos = bisect.bisect_left(pdates, evdate)     # index of first trading day >= evdate
    n = len(pdates)
    ok = pos >= EST_BEFORE and pos + POST_AFTER < n
    return ok, pos, n


def parse_salience(row):
    """Mechanical salience: GDELT 'total mentions' parsed from the harvester's own
    note (never a judgment). Manual seeds get a sentinel so they always rank top."""
    if row.get("candidate_source") == "manual":
        return MANUAL_SALIENCE
    m = re.search(r"(\d+)\s+total", row.get("description", ""))
    if m:
        return int(m.group(1))
    m = re.search(r"peak\s+(\d+)", row.get("description", ""))
    return int(m.group(1)) if m else 0


def involves_producer(row):
    """(c): does an actor match the major-producer/OPEC filter? Mechanical string check."""
    blob = (row.get("entities", "") + " " + row.get("title", "")).lower()
    if "opec" in blob:
        return "OPEC"
    for nm in PRODUCER_NAMES:
        if f"country.{nm}" in blob:
            return nm
    return None


def parse_date(s):
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def strength(cand):
    """Total order for 'stronger candidate': higher salience, then earlier date,
    then smaller id. Guarantees exactly one winner per cluster neighbourhood."""
    d = cand["_date"]
    return (cand["_salience"], -d.toordinal(), cand["event_id"])


def main():
    rows = list(csv.DictReader(open(CANDIDATES, newline="", encoding="utf-8")))
    pending = [r for r in rows if r.get("status") == "candidate"]
    if not pending:
        print("No candidates pending review. Nothing to triage.")
        return

    pdates = load_price_dates()
    if not pdates:
        print("No Brent price data found -- cannot do the price-window check. Aborting.")
        return

    # Existing events (already in the dataset) -- their dates anchor the (b) check.
    existing = []
    for r in csv.DictReader(open(EVENTS, newline="", encoding="utf-8")):
        d = parse_date(r.get("event_date", ""))
        if d:
            existing.append((d, r["event_id"]))

    # Pre-compute per-candidate mechanical facts.
    for c in pending:
        c["_date"] = parse_date(c["event_date"])
        c["_salience"] = parse_salience(c)
        c["_producer"] = involves_producer(c)

    def nearest_existing(d):
        for ed, eid in existing:
            if abs((d - ed).days) <= CLUSTER_DAYS:
                return eid, ed
        return None

    def stronger_neighbor(c):
        best = None
        for o in pending:
            if o is c or o["_date"] is None:
                continue
            if abs((o["_date"] - c["_date"]).days) <= CLUSTER_DAYS and strength(o) > strength(c):
                if best is None or strength(o) > strength(best):
                    best = o
        return best

    # Build the recommendation for each candidate (deterministic cascade).
    for c in pending:
        d = c["_date"]
        if d is None:
            c["_rec"], c["_reason"] = "reject", "unparseable event_date"
            continue
        ok, pos, n = price_window_ok(d, pdates)
        if not ok:
            c["_rec"] = "reject"
            c["_reason"] = (f"outside usable price window "
                            f"(need {EST_BEFORE}d before & {POST_AFTER}d after; "
                            f"have {pos} before, {n - pos} on/after)")
            continue
        ne = nearest_existing(d)
        if ne:
            c["_rec"] = "reject"
            c["_reason"] = f"within {CLUSTER_DAYS}d of existing event {ne[0]} ({ne[1]}) - same episode"
            continue
        sn = stronger_neighbor(c)
        if sn is not None:
            sal = "seed" if sn["_salience"] >= MANUAL_SALIENCE else f"{sn['_salience']} mentions"
            c["_rec"] = "reject"
            c["_reason"] = (f"duplicate episode: within {CLUSTER_DAYS}d of stronger "
                            f"candidate {sn['event_id']} ({sal})")
            continue
        # KEEP -- assemble the positive mechanical reason.
        if c["candidate_source"] == "manual":
            base = "hand-sourced seed; in price window"
        else:
            base = f"in price window; salience {c['_salience']} mentions"
        prod = f"; producer {c['_producer']}" if c["_producer"] else "; no major-producer actor (macro/risk channel)"
        c["_rec"], c["_reason"] = "keep", base + prod

    # Sort best-first: keeps before rejects, then by salience desc, then date.
    pending.sort(key=lambda c: (0 if c["_rec"] == "keep" else 1,
                                -c["_salience"],
                                c["_date"].toordinal() if c["_date"] else 0))

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OUT_FIELDS)
        w.writeheader()
        for c in pending:
            out = {k: c.get(k, "") for k in CAND_FIELDS}
            out["recommendation"] = c["_rec"]
            out["rec_reason"] = c["_reason"]
            out["salience_mentions"] = "seed" if c["_salience"] >= MANUAL_SALIENCE else c["_salience"]
            out["joe_decision"] = ""      # Joe fills this: approve / reject
            w.writerow(out)

    keeps = sum(1 for c in pending if c["_rec"] == "keep")
    print("=" * 66)
    print("TRIAGE COMPLETE (mechanical only -- no facts asserted, no LLM used)")
    print("=" * 66)
    print(f"  Candidates triaged:      {len(pending)}")
    print(f"  Recommended KEEP:        {keeps}")
    print(f"  Recommended REJECT:      {len(pending) - keeps}")
    print(f"  Wrote:                   {OUT}")
    print("\n  Reject reasons breakdown:")
    reasons = {}
    for c in pending:
        if c["_rec"] == "reject":
            tag = c["_reason"].split("(")[0].split(" - ")[0].strip()[:48]
            reasons[tag] = reasons.get(tag, 0) + 1
    for tag, n in sorted(reasons.items(), key=lambda x: -x[1]):
        print(f"    {n:>4}  {tag}")
    print("\n  Next: open the sheet, fill joe_decision (approve/reject), then run")
    print("        python3 src/apply_review.py")


if __name__ == "__main__":
    main()
