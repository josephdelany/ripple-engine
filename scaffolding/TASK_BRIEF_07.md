# TASK_BRIEF_07 — Standardized ripples + honest inference

Read CLAUDE.md first. All guardrails apply. Purpose: close the two
methodological holes a sharp referee would attack first (see
../FRONTIER_AUDIT.md F1 and F2).

## Outcome

A new module `src/inference.py` (import-only reuse of event_study/robustness;
do not modify them) that:

1. **Standardized CARs (the vol-clustering defense).** For each event,
   divide CAR+20 by the standard deviation of daily returns over that event's
   own estimation window (t-130..t-11), scaled by sqrt(window length), so each
   ripple becomes "how many normal-period sigmas was this move." Then re-run
   the H1/H2/H3 high/low median splits on |standardized CAR| — baseline,
   clustered, no-outlier — exactly mirroring robustness.py's structure.

2. **Permutation inference.** For each hypothesis, on the clustered sample:
   hold the |CAR| values fixed, shuffle the state-variable labels across
   events 10,000 times (seeded, reproducible), and report the fraction of
   shuffles producing amplification >= the observed one. That fraction is the
   permutation p-value. Report it plainly; do NOT relabel verdicts — the
   pre-registered +5pp rule stands as registered, this is an ADDITIONAL lens.

3. **Output** `data/inference_results.txt` with three blocks per hypothesis:
   raw amplification (as robustness.py computes), standardized amplification,
   permutation p — each with n. A final plain-English summary block stating,
   for H1 specifically, whether the VIX result survives standardization.

## Standard

- Same clustering, same registered variables and directions, same samples as
  robustness.py — any divergence is a bug, not a choice.
- Seeded RNG; two runs must produce identical output.
- Teach-style comments: explain WHY standardization defeats the
  vol-clustering critique, in plain English, in the module docstring.
- Receipt: commit data/inference_results.txt; state clearly in the commit
  message that this is a post-registration robustness lens, not a new
  hypothesis.

## Bounds

- No new hypotheses, no new state variables, no data fetching, no events.
- Do not modify event_study.py / robustness.py / conditioned_study.py /
  derive_signals.py.
- No widget changes this brief (keep the diff small and auditable).
- Ports untouched. If a number can't be computed honestly, print that.
