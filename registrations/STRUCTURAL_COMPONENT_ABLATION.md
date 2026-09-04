# Structural-component and concentration ablation — registration

**Registered 2026-09-03 before implementation or inspection of any result from this analysis.**

## Purpose

The frozen structural-versus-surface experiment establishes that its registered structural arm
beats its registered event-class arm, but it does not beat uniform pooling. Its realized arms also
have very different concentration: median effective sample size is about 130 under structural
weighting and 29 under surface weighting. The frozen reads show that the usable structural distance
is dominated by market fields and, when available, an actor block. This analysis determines whether
the registered result is evidence about state information, event labels, or concentration.

This is an explanatory analysis of the already-frozen experiment. It cannot alter the original
scores or registration and may only narrow their interpretation.

## Frozen sample, support, outcome, and inference

Use `data/structural_surface/reads.jsonl` and `scores.jsonl` exactly as committed at release commit
`1705713b801d7ffc48d7cc39adb5a802b613157c`. Use all 264 scored dates, the candidate IDs and abnormal
20-return atoms already sealed for each date, and the attached primary outcome. No candidate,
target, field, date, or outcome may be added or removed.

Score every arm by the same weighted empirical CRPS. Compare paired date-level losses using the
same `paired_block` procedure, stationary-bootstrap settings, DM implementation, seed, and decision
thresholds as the frozen experiment. Report mean loss, paired difference, 95% interval, DM p-value,
median effective sample size, and the number of dates for every comparison.

## Frozen arms

1. **Uniform:** equal weight over the frozen candidate pool.
2. **Registered structural:** reuse the sealed registered structural weights without modification.
3. **Market-only:** for each candidate use the stored `market` block distance. Apply the registered
   `exp(-d/0.25)` kernel. The frozen support guarantees that every admitted pair has a market block;
   otherwise the analysis must stop rather than change support.
4. **Market-plus-actors:** use the equal-block mean of stored market and actor distances when the
   actor block exists, and market distance alone otherwise. This reconstructs the effective content
   of the registered structural arm. Any other block is retained only in the registered arm and
   counted explicitly.
5. **Registered surface:** reuse the sealed event-class weights without modification.
6. **Concentration-matched surface:** retain the binary same-class/cross-class distance but choose a
   separate nonnegative cross-class weight ratio for each date so that its effective sample size is
   as close as numerically possible to the registered structural arm's effective sample size. The
   ratio is chosen from candidate class counts and the sealed structural effective sample size only;
   outcomes and losses are forbidden. If the target effective size is outside the binary arm's
   attainable range, use the nearest boundary and count the date as unattainable.

## Registered questions and interpretation

The primary explanatory comparison is concentration-matched surface minus uniform. Secondary
comparisons are registered structural minus market-only, market-plus-actors minus market-only,
registered structural minus concentration-matched surface, and registered surface minus
concentration-matched surface.

- Event labels carry harmful information only if concentration-matched surface is worse than
  uniform with a 95% interval excluding zero and DM p < 0.05.
- The non-market state adds information only if registered structural beats market-only with a 95%
  interval excluding zero and DM p < 0.05.
- If registered surface is worse than its concentration-matched version but the matched version is
  not worse than uniform, the defensible finding is excessive class concentration, not harmful
  label information.
- If neither state increment nor matched label arm is distinguishable from uniform, the headline is
  that broad pooling beats the registered concentrated surface rule; “structural information” is
  withdrawn from the résumé claim.

No subgroup, alternative horizon, bandwidth, or target can change these interpretations.

## Required field-use audit

Publish across all frozen target-candidate comparisons: fields used, block combinations, fraction
using market only, fraction containing actors, fraction containing dyads or any other block, and the
number of forecast dates whose comparisons are all market-only. These are descriptive properties of
the registered structural arm, not hypothesis tests.

## Outputs and tests

Write only under `data/structural_surface/ablation/`: `scores.jsonl`, `summary.json`, and
`manifest.json`. The manifest must hash both frozen input ledgers and all outputs and record this
registration commit and the later implementation/execution commits separately.

Tests must independently reconstruct weights and CRPS for fixed examples; prove identical support
and atoms across arms; prove the matched ratio never reads outcomes; verify attainable effective
sample size numerically; reproduce the published field-use counts directly from frozen reads; and
reproduce all outputs byte-for-byte from a clean checkout.

## Amendment 1 — common-concentration comparison (2026-09-03, before implementation)

The binary-only matching rule above controls concentration for the surface arm but does not fully
isolate representation in the market-versus-combined-state contrast. Supersede the primary analysis
with a common feasible effective sample size for all three non-uniform representations.

For each frozen read and each distance vector—market, market-plus-available-panel, and surface—find
the minimum attainable effective sample size as temperature tends to zero, including ties. Set the
common target `K_t` to the maximum of (a) the sealed registered structural effective sample size and
(b) those three minima. `K_t` cannot exceed the common pool size. For each representation, choose a
temperature by deterministic bisection using distances and `K_t` only, never outcomes, so its
effective sample size matches `K_t` within `1e-8`; a constant-distance arm is uniform and forces
`K_t` to the pool size. Record temperatures, achieved effective sizes, boundary cases, and dates
where surface distance is constant.

The two primary explanatory contrasts are:

1. ESS-matched market minus ESS-matched surface: market-state representation versus event class.
2. ESS-matched combined state minus ESS-matched market: incremental non-market information.

Apply Holm's step-down correction across their two DM p-values at family alpha 0.05. Always publish
unadjusted p-values, Holm-adjusted p-values, intervals, and effect sizes. The original registered
structural, surface, and uniform arms remain descriptive anchors. The earlier binary-only
surface-versus-uniform interpretation is secondary and cannot override these two matched contrasts.
