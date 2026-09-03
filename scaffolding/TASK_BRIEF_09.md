# TASK_BRIEF_09 — H5: GPR conditioning (exploratory, two-sided)

Read CLAUDE.md first. All guardrails apply.

## Precondition (verify before writing any code)

`../BRIEF_SKELETON.md` must contain the registered H5 block (GPR
conditioning, EXPLORATORY, two-sided, registered 2026-07-23) in a commit
whose timestamp precedes this run. If the registration is not committed,
STOP and say so — do not run the analysis against an uncommitted
registration.

## Outcome

Extend the analysis with the H5 exploratory conditioning run, mirroring the
established pipeline exactly:

1. `src/h5_gpr.py` (import-only reuse of event_study / robustness /
   inference logic — no forks): for each of the 42 events, GPR daily
   percentile (full-history, computed point-in-time style at t−1). High/low
   split at the event-sample median of that percentile. Report |CAR+20|
   amplification: baseline, clustered, no-outlier — raw AND standardized
   (per inference.py's sigma_for_event) — plus a TWO-SIDED permutation p
   (10,000 shuffles, seeded) on the clustered sample.
2. Output `data/h5_results.txt`. Language rules, enforced in the output
   templates: the words "holds", "fails", "confirms", "predicted" must NOT
   appear. Allowed framing: "exploratory result", "direction observed",
   "hypothesis-generating". The file must open with a header stating H5 is
   exploratory and two-sided per the registration.
3. Add the H5 row to the engine-read/scenario context ONLY as descriptive
   context (e.g. "GPR percentile today: X"), NOT as an amplifier — H5 has
   no registered direction, so it can never set an amplifier flag. Enforce
   this the same way H3's FAILED fence is enforced.

## Standard

- Same clustering, same samples, same event set as robustness/inference.
- Seeded, byte-reproducible across two runs.
- Teach-style comments: explain what an exploratory (vs confirmatory)
  analysis is and why the two-sided p is the honest choice here.
- Receipts: commit data/h5_results.txt; commit message must say
  "exploratory, two-sided, per registered H5".

## Bounds

- H5 can NEVER become an amplifier flag in engine_read/scenario.
- No other hypotheses touched; no verdict language anywhere.
- Do not modify event_study.py / robustness.py / conditioned_study.py /
  inference.py / derive_signals.py.
- No new data, no events, no keys. Ports untouched. If something can't be
  computed honestly, print that instead.
