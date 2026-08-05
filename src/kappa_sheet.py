"""
kappa_sheet.py -- the BLIND inter-coder reliability sheet (FINAL_PLAN F2.2 / BULLETPROOF Q5, machine side).

The last conventional credential the corpus lacks is a quantified inter-coder reliability number: would a
SECOND independent coder, reading the same sources, assign the same codes? This builds the blind sheet:
it samples 20 corpus events (seeded -> reproducible), and serves Joe each event's TITLE + SOURCE URLs
with the existing codes HIDDEN. Joe codes type / severity / surprise / date from the sources alone; the
companion kappa_report.py then computes Cohen's kappa per field against the corpus codes.

Outputs:
  data/kappa_blind_sheet.md   -- what JOE reads + codes (no existing codes shown).
  data/kappa_responses.csv    -- the blank form Joe fills (row_id, type, severity, surprise, date).
  data/kappa_key.csv          -- the HIDDEN key (row_id -> event_id + the corpus codes). Joe must NOT
                                 open this while coding; kappa_report.py reads it afterwards.

Run:  python3 src/kappa_sheet.py          # (re)generate the sheet (idempotent; seeded sample)
"""

import csv
import random
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "oil.db"
TWO_SOURCE = ROOT / "data" / "state" / "two_source_log.csv"
SHEET = ROOT / "data" / "kappa_blind_sheet.md"
RESP = ROOT / "data" / "kappa_responses.csv"
KEY = ROOT / "data" / "kappa_key.csv"
N_SAMPLE = 20
SEED = 20260805        # fixed -> the same 20 events every run (reproducible; declared, not fished)


def _second_sources():
    idx = {}
    if TWO_SOURCE.exists():
        for r in csv.DictReader(open(TWO_SOURCE, newline="", encoding="utf-8")):
            if r.get("event_id") and r.get("second_url"):
                idx[r["event_id"]] = r["second_url"]
    return idx


def run():
    conn = sqlite3.connect(DB)
    events = conn.execute(
        "SELECT event_id, event_date, type, title, severity, surprise, source_url "
        "FROM events ORDER BY event_id").fetchall()
    conn.close()
    rng = random.Random(SEED)
    sample = rng.sample(events, min(N_SAMPLE, len(events)))
    sample.sort(key=lambda e: e[0])                        # stable presentation order
    second = _second_sources()

    # blind sheet (Joe reads this) -- NO type/severity/surprise/date shown.
    L = ["# Blind coding sheet -- inter-coder reliability (F2.2 / Q5)", "",
         f"Code these {len(sample)} events **from the sources**, WITHOUT looking at the corpus codes",
         "(do not open `data/kappa_key.csv`). For each row, read the source(s), then in",
         "`data/kappa_responses.csv` fill: **type** (one of: chokepoint_disruption, opec_decision,",
         "sanctions, conflict_escalation, infrastructure_attack, demand_shock, policy_response),",
         "**severity** 1-5 (by expected disruption, NOT the price reaction), **surprise** 1-5 (how",
         "unexpected the day before), **date** (YYYY-MM-DD, the first day the market could know).",
         "The title is a locator only -- severity/surprise/exact-date must come from the sources.", "",
         "| row | event (title) | sources |", "|---|---|---|"]
    for i, (eid, d, typ, title, sev, sur, url) in enumerate(sample, 1):
        srcs = url + ((" · " + second[eid]) if eid in second else "")
        L.append(f"| {i} | {title} | {srcs} |")
    SHEET.write_text("\n".join(L) + "\n")

    # blank response form for Joe
    with open(RESP, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["row_id", "type", "severity", "surprise", "date"])
        for i in range(1, len(sample) + 1):
            w.writerow([i, "", "", "", ""])

    # hidden key (corpus codes) -- for kappa_report.py, NOT for Joe to consult while coding
    with open(KEY, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["row_id", "event_id", "type", "severity", "surprise", "date"])
        for i, (eid, d, typ, title, sev, sur, url) in enumerate(sample, 1):
            w.writerow([i, eid, typ, sev, sur, d])
    return len(sample)


def main():
    n = run()
    print(f"kappa sheet: {n} events sampled (seed {SEED}).")
    print(f"  Joe reads + codes:  {SHEET.name}  ->  fills  {RESP.name}")
    print(f"  hidden key (do not peek while coding):  {KEY.name}")
    print("  Then run: python3 src/kappa_report.py")


if __name__ == "__main__":
    main()
