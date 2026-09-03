# Structural versus surface historical analogy — central experiment registration

**Registered 2026-09-03 before implementation or inspection of any result from this design.**

## 1. Question and estimand

The project's research question and instrument test are the same experiment:

> At a dated petroleum-relevant event, does weighting closed historical cases by the state that was
> actually available at the time forecast what follows better than weighting the same cases by the
> event's surface class?

The estimand is the paired difference in proper-score loss,

    d_t = loss(structural, t) - loss(surface, t).

Negative `d_t` favours structural analogy. The two arms may differ only in their similarity
function. They share reads, candidate rows, closure rules, targets, atom weights after similarity,
scores, and inference.

## 2. Primary sample and target

The primary unit is a day-precision corpus event with a usable daily Brent price at `t-1`, a closed
20-trading-day window, and enough prior observations for the expected-return model. Multiple corpus
events on one date are one inferential date; their forecasts are computed separately and their loss
differences are averaged before inference.

The primary target is Brent abnormal cumulative log return from the last trading close strictly
before the event through trading day `+20`:

    AR(t,20) = 100 * ([log P(t+20) - log P(t-1)] - 20 * alpha_hat_t).

`alpha_hat_t` is the mean daily Brent log return over 250 trading observations ending 21 trading
days before `t`, with at least 100 usable observations. A read failing that minimum is excluded and
counted. There is no raw-return fallback.

This constant-mean benchmark is fixed before results because the repository has no registered
exogenous oil factor distinct from Brent. Raw returns are published only as a diagnostic and never
substituted for the primary target.

Secondary price endpoints use the same rule at horizons 5 and 10. They cannot change the primary
verdict.

## 3. One information set and candidate universe

For target date `t`, a historical event is eligible for both arms only when:

1. its event date is strictly before `t`;
2. its own `+20` target window closed before `t`;
3. it and the target have at least three common strictly point-in-time structural fields; and
4. it is not the target event.

Event class is **not** an eligibility filter. All seven event classes enter the same historical
universe. A read with fewer than eight eligible candidates abstains; both arms abstain together.

The strictly point-in-time structural field set contains:

- market observations only when `obs_date < t` and stored `as_of <= t`; and
- `state_panel` rows only when `obs_date <= t`, `vintage <= t`, `release <= t`, and
  `retrospective = 0`.

Situation-record `sr_*` fields are excluded from the registered experiment because their current
`knowable_at` values mostly fall back to coding dates rather than demonstrated publication dates.
Event class, title, description, event entities, severity, surprise, and outcomes are never
structural fields.

For a candidate dated `c`, its state is reconstructed at `c`, under the same availability rules;
later revisions are invisible. Numeric standardisation at target `t` uses observations available
strictly before `t` only. Fields unknown on either side are omitted and counted. Block distances are
means over comparable fields and the total is the equal-weighted mean over represented blocks.

## 4. The two frozen arms

Both arms assign positive weights over the identical eligible candidates using

    weight_i = exp(-distance_i / 0.25), normalised to sum to one.

No `k`, threshold, learned weight, Hedge update, or post-result tuning is used.

### 4.1 Surface arm

Surface distance is exactly:

- `0` when candidate and target have the same registered event class;
- `1` otherwise.

This operationalises the project's surface comparison: class membership is the comparison, with no
world-state information. Cross-class cases remain in the common support at their registered kernel
weight rather than being made ineligible.

### 4.2 Structural arm

Structural distance is the existing block-wise state distance after enforcing section 3, with all
represented blocks weighted equally. Event class is not a field and cannot affect this distance.

## 5. Forecast distribution and scores

Each forecast is the weighted empirical distribution of eligible candidates' abnormal returns.
The primary loss is weighted empirical CRPS:

    sum_i w_i |x_i-y| - 0.5 * sum_i sum_j w_i w_j |x_i-x_j|.

Tests must reproduce this formula by hand on fixed examples, including unequal weights. Every read
publishes its candidate IDs, both distance vectors, both weight vectors, target, closure date, field
counts, and reasons for exclusion or abstention.

## 6. Sealing, inference, and verdict

For each read, the complete two-arm forecast object is canonical-JSON encoded and SHA-256 hashed
before the target outcome is attached. A test must fail after tampering with any candidate, distance,
weight, or forecast atom.

Inference operates on date-collapsed paired losses. The primary estimate is mean `d_t`; uncertainty
uses the repository's stationary bootstrap with the existing event-walk block-length rule and a
two-sided paired Diebold-Mariano test. The report always gives the estimate, 95% interval, p-value,
number of event reads, number of inferential dates, abstentions, eligible-pool distribution, and
effective weight count `1/sum(w^2)` for each arm.

The frozen verdict is:

- **STRUCTURE ADDS INFORMATION** only if mean `d_t < 0`, its 95% interval excludes zero, and paired
  DM `p < 0.05`;
- **SURFACE PERFORMS BETTER** only if mean `d_t > 0`, its 95% interval excludes zero, and paired DM
  `p < 0.05`;
- **NOT DISTINGUISHABLE ON THIS RECORD** otherwise;
- **INSUFFICIENT** if fewer than 30 inferential dates remain.

No secondary endpoint can promote or reverse this verdict.

## 7. Required comparators and diagnostics

Uniform pooling over the same candidates is reported as a non-verdict comparator. Raw-return
re-scoring, horizons 5 and 10, per-era estimates, per-class estimates, and alternative kernel widths
are diagnostics only. They are labelled exploratory and cannot become the headline.

The report must separately publish how many reads and candidates are lost to actual release/as-of
discipline. Missingness is a result about feasibility, not evidence for or against analogy.

## 8. Secondary escalation feasibility arm

Escalation is not part of the primary verdict. A later secondary run may use only outcomes whose
source and mapping identify the event dyad and whose measurement window lies inside `(t, t+90]`.
Location-only and annual `y+1` mappings are excluded. It must use the same surface/structural design
and is **INSUFFICIENT** below 30 inferential dates. Its result may not be pooled with price.

## 9. Frozen outputs

Implementation will write new artifacts under `data/structural_surface/`; it will not overwrite the
existing walk or grid records. Required files are `reads.jsonl`, `scores.jsonl`, `summary.json`, and
`manifest.json`, with input hashes and the implementation commit recorded in the manifest.

## Amendment 1 — deterministic state reduction (2026-09-03, before implementation)

`situation_state` can contain the same registered field for more than one event-relevant entity.
The event-level vector reduces those rows as follows: one numeric value is the arithmetic mean of
the available entity values; one categorical value is the sorted, `|`-joined set of available text
values. The entity identifier itself is not included, because actor/target identity is a surface
description and would make fields incomparable across cases. Global and single-entity fields pass
through unchanged. The output records the contributing entity count for every reduced field.

The market portion is limited to four directly observed series whose historical prints are held in
the database: prior-close Brent and WTI 20-day changes, prior 20-day Brent volatility, and the prior
VIX close. They are reconstructed from observations satisfying both `obs_date < event_date` and
stored `as_of <= event_date`; no `derived.*` row is trusted as an availability receipt. This fixed
set prevents a derived series whose loader copied `obs_date` into `as_of` from laundering revised
information into the experiment.
