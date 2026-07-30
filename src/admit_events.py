"""
admit_events.py -- TIERED ADMISSION for LLM-extracted candidates (living-engine step 4).

After triage_candidates.py scores the candidates, this decides which LLM-extracted ones are corroborated
strongly enough to AUTO-ADMIT vs. which wait in Joe's review queue. It reads ONLY deterministic
corroboration receipts (data/state/corroboration_log.csv: confidence p, n_independent, source_urls) --
NEVER the worker's suggested numbers. It sets `joe_decision` in candidate_review.csv; the untouched
apply_review.py + load_events.py then do the actual admission (and re-apply the codebook gate), so canon
is only ever written through the one sanctioned, gated path.

AUTO-ADMIT tier (all required): triage recommendation == 'keep' AND an EXACT source_url match to a
corroboration receipt (fail-closed: no exact match -> review) AND confidence p >= 0.90 AND
n_independent >= 3. Auto-admits get a DETERMINISTIC provisional severity/surprise band (by event type,
not the LLM number) and a logged receipt; a human can veto before the next apply_review. Everything else
stays in the queue: FAST_REVIEW (keep + p>=0.75), REVIEW (keep), PARK (triage reject).

Run:  python3 src/admit_events.py
"""

import csv
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEW = ROOT / "data" / "candidate_review.csv"
CORROB_LOG = ROOT / "data" / "state" / "corroboration_log.csv"
ADMISSION_LOG = ROOT / "data" / "extract" / "admission_log.csv"

P_AUTO, N_AUTO, P_FAST = 0.90, 3, 0.75
# Conservative, provisional severity band by type (expected disruption; NOT the LLM's number). Joe can
# refine any auto-admitted event afterwards -- these are tagged provisional in the description.
SEV_BAND = {"chokepoint_disruption": 3, "infrastructure_attack": 3, "conflict_escalation": 3,
            "opec_decision": 3, "demand_shock": 3, "sanctions": 2, "policy_response": 2}
SURPRISE_DEFAULT = 3          # 'plausible but not consensus' -- the neutral middle, provisional


def _corrob_index():
    """source_url -> (confidence_p, n_independent) from the deterministic corroboration receipts."""
    idx = {}
    if not CORROB_LOG.exists():
        return idx
    for r in csv.DictReader(open(CORROB_LOG, newline="", encoding="utf-8")):
        try:
            p, n = float(r.get("confidence") or 0), int(r.get("n_independent") or 0)
        except ValueError:
            continue
        for u in (r.get("source_urls") or "").split("|"):
            u = u.strip()
            if u:
                prev = idx.get(u)
                if prev is None or p > prev[0]:
                    idx[u] = (p, n)
    return idx


def tier_for(row, corrob):
    """Return (tier, receipt) for one llm_extract candidate row."""
    rec = (row.get("recommendation") or "").strip().lower()
    if rec == "reject":
        return "PARK", None
    hit = corrob.get((row.get("source_url") or "").strip())      # EXACT url match, fail-closed
    if hit is None:
        return "REVIEW", None
    p, n = hit
    if rec == "keep" and p >= P_AUTO and n >= N_AUTO:
        return "AUTO_ADMIT", {"p": p, "n_independent": n}
    if rec == "keep" and p >= P_FAST:
        return "FAST_REVIEW", {"p": p, "n_independent": n}
    return "REVIEW", {"p": p, "n_independent": n}


def run():
    if not REVIEW.exists():
        return {"note": "no candidate_review.csv (run triage_candidates.py first)", "auto_admitted": 0}
    rows = list(csv.DictReader(open(REVIEW, newline="", encoding="utf-8")))
    if not rows:
        return {"auto_admitted": 0}
    fields = list(rows[0].keys())
    corrob = _corrob_index()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    admitted = []
    for r in rows:
        if r.get("candidate_source") != "llm_extract":
            continue
        if (r.get("joe_decision") or "").strip():          # already decided -> idempotent skip
            continue
        tier, receipt = tier_for(r, corrob)
        if tier == "AUTO_ADMIT":
            r["severity"] = str(SEV_BAND.get(r.get("type"), 2))     # deterministic provisional band
            r["surprise"] = str(SURPRISE_DEFAULT)
            r["joe_decision"] = "approve"
            r["rec_reason"] = (r.get("rec_reason", "") +
                               f" | AUTO-ADMIT p={receipt['p']:.2f} n_indep={receipt['n_independent']} "
                               f"(provisional sev={r['severity']} -- Joe can refine)").strip(" |")
            admitted.append({"event_id": r.get("event_id"), "source_url": r.get("source_url"),
                             "p": receipt["p"], "n_independent": receipt["n_independent"],
                             "provisional_severity": r["severity"], "admitted_at": now})
        else:
            r["rec_reason"] = (r.get("rec_reason", "") + f" | tier={tier}").strip(" |")
    with open(REVIEW, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    if admitted:
        first = not ADMISSION_LOG.exists()
        ADMISSION_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(ADMISSION_LOG, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["event_id", "source_url", "p", "n_independent",
                                              "provisional_severity", "admitted_at"])
            if first:
                w.writeheader()
            w.writerows(admitted)
    return {"auto_admitted": len(admitted),
            "pending_review": sum(1 for r in rows if r.get("candidate_source") == "llm_extract"
                                  and not (r.get("joe_decision") or "").strip())}


def main():
    res = run()
    print(f"admit_events: {res.get('auto_admitted', 0)} auto-admitted (approve set), "
          f"{res.get('pending_review', 0)} awaiting review. "
          f"Canon is still written only by apply_review.py + load_events.py (gate re-applied).")


if __name__ == "__main__":
    main()
