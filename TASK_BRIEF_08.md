# TASK_BRIEF_08 — GPR index: load + validate (NO conditioning yet)

Read CLAUDE.md first. All guardrails apply. Context: FRONTIER_AUDIT.md F4/F6.

## Outcome

1. **Fetch** `src/fetch_gpr.py`: download the Caldara-Iacoviello Geopolitical
   Risk index from the official site (matteoiacoviello.com/gpr.htm — the
   daily series file). Parse and upsert into `observations` as series
   `gpr.GPRD` (daily headline index; if the file also carries GPRD_ACT and
   GPRD_THREAT sub-indices, load those too as their own series ids). Register
   the series in `series` with source and cadence. Wire into refresh.py and
   heartbeat.py like every other series.
2. **Validate** `src/validate_gpr.py`: a read-only report answering "does our
   hand-built event list line up with the field-standard salience measure?"
   For each of the 42 events: GPR daily percentile (full-history) on the event
   date and the max within event_date ±3 days. Output
   `data/gpr_validation.txt`: table sorted by that percentile, plus a summary
   (median percentile across events; list of events sitting below the 50th —
   those are candidates for the salience-selection discussion, F4).
3. NO conditioning run. Do NOT split CARs by GPR state. That analysis is
   blocked until Joe registers a hypothesis (direction + rationale) in
   BRIEF_SKELETON.md-style form — pre-registration discipline (ba3d6fa
   precedent). Print a reminder line at the end of validate_gpr.py:
   "Conditioning blocked pending registered H4 (Joe)."

## Standard

- Exact source URL recorded in the series row and script header. If the
  download fails or the file format differs from expectations, STOP and
  report — do not scrape alternatives or hand-enter numbers.
- Point-in-time: GPR is subject to revisions; store as_of = fetch date.
- Teach-style comments (what the GPR index is, how it's built, why an
  external salience measure checks our selection bias).
- Receipts: commit data/gpr_validation.txt; show refresh.py 9/9 OK and
  heartbeat listing the new series.

## Bounds

- No conditioning, no new hypotheses, no verdicts — data + validation only.
- No events added or edited. No existing analysis modules modified
  (refresh/heartbeat wiring excepted).
- No API keys (GPR is a public file). Ports untouched.
