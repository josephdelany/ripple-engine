# TASK_BRIEF_11 — Quincy data enhancement: quiet set, policy_response type, pump pass-through

Read CLAUDE.md first. All guardrails apply. Context: this implements the
data enhancements behind the restraint-paper program (sanctions depth and
policy_response events arrive separately via Joe's candidate_review gate).

## Precondition
Joe must have approved batch 3 in candidate_review.csv (10 events: 6
sanctions + 4 policy_response) and run apply_review/load_events. If the
events table still lacks the policy_response type, STOP at part 1 and say
so. Part 2 and 3 can proceed regardless.

## Part 1 — codebook amendment: policy_response type
- Add `policy_response` as the 7th event type wherever types are validated
  (load_events.py etc.), with a comment: "Amendment 2026-07-23, approved by
  Joe with batch 3: deliberate government/agency market interventions (SPR/
  IEA releases). Severity = scale of intervention." Log the amendment as an
  addendum line in EVENTS_CODEBOOK.md (this is the ONLY permitted edit to
  that file, clearly dated, nothing else altered).
- Verify the four policy_response events flow through the full pipeline
  (event study, scenario card, cross-asset edges) like any other type.

## Part 2 — the quiet-comparison module
- `data/quiet_events.csv` (committed by this brief) holds 6 hand-sourced
  high-alarm/no-supply-channel events. They must NOT enter the events
  table — they are a comparison class, loaded into their own `quiet_events`
  table by a small loader (same schema as events).
- `src/quiet_compare.py` (import-only reuse): run the identical CAR
  machinery on the quiet set; output `data/quiet_comparison.txt`:
  per-event CAR+5/+20 (Brent, and 5Y bps via the cross-asset path), then
  the comparison: |CAR+20| distribution of quiet events vs. the clustered
  main corpus (means, medians, and a two-sided permutation p on the
  difference, seeded). Handle the flagged Fujairah/Gulf-of-Oman window
  overlap: report Fujairah's numbers but exclude it from the pooled
  comparison, stating why.
- Language rules: descriptive/exploratory only; no "confirms", no verdicts.
  This is the F4 selection-bias answer and the threat-inflation evidence
  base — the output must let the numbers speak.

## Part 3 — pass-through to the pump
- Add weekly US regular retail gasoline (FRED GASREGW, keyless) as a
  series via fetch_series.py's pattern; wire into refresh/heartbeat.
- Extend cross_asset.py's target list with gasoline (weekly cadence:
  measure CAR at +1/+2/+4 WEEKS from the last weekly reading before the
  event; label units and cadence clearly — do not pretend daily
  resolution).
- Regenerate edges + cross_asset_results.txt including the gasoline column.

## Standard
- Same clustering/windows/discipline; seeded and reproducible; teach-style
  comments; units everywhere; small-n shouted.
- Receipts: commit quiet_comparison.txt and updated cross_asset_results.txt;
  refresh N/N OK; forbidden analysis modules untouched (import-only;
  fetch_series/cross_asset/load_events wiring changes permitted as scoped
  above).

## Bounds
- No hypotheses registered, no verdicts, no amplifiers from any of this.
- Quiet events never enter the events table; policy_response events never
  enter the quiet table.
- No keys, no scraping (FRED keyless CSV only). Ports untouched.
- If Joe's batch-3 approval hasn't landed, do Parts 2-3 and report Part 1
  blocked.
