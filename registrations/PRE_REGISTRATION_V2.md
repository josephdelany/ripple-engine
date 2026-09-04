> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** A registration for a superseded study, kept so its pre-commitments stay auditable. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../SUBMISSION_STATUS.md).

# Walk-forward pre-registration (v2) — REGISTERED before building the engine

Per RIPPLE_ENGINE_V2_SPEC §5. Committed **before** Layer G/P are built or scored, so the
protocol cannot be chosen to fit a result (register-then-run; git timestamp is the seal). The
existing frozen v1 registered record (`PRE_REGISTRATION.md`, `BRIEF_SKELETON.md`) is untouched.

## The one honest question
Does conditioning the read on the Situation Record (geopolitical + market state) beat the
**unconditioned reference class** — out of sample? Everything below is fixed so the answer is
earned, not tuned.

## Point-in-time law
At replay date *t*, the engine may use ONLY information knowable at *t*: features, similarity
weights, retrieval library, thresholds, and branch rates are all computed from data with
`event_date < t` (and observation `as_of <= t`). No lookahead in any component. A read at *t*
for an event at *t* forecasts its +30/+90d branch (Layer G) and its CAR sign/magnitude given
the realized branch (Layer P).

## Evaluation windows (two, fixed now)
- **W1:** train on events with `event_date <= 2014-12-31`; test 2015-01-01 … 2019-12-31.
- **W2:** train on events with `event_date <= 2019-12-31`; test 2020-01-01 … 2026-12-31.
Both are scored and published now. (Deep-history tier, B6, enlarges the *training* pools with
pre-1989 escalation precedents; the test windows above are unchanged.)

## Scores
- **G-score** — multi-class Brier over the four branches: mean of Σ_k (p_k − 1{realized=k})²
  across scored test situations. Lower is better.
- **P-score** — given the *realized* branch: MAE of the predicted CAR magnitude (percentage
  points) plus sign-accuracy (fraction with correct direction). Reported as a pair.
- Every scored situation writes a per-item log (features as-of t, predicted branch
  distribution, predicted magnitude, realized branch, realized CAR) → fully reproducible.

## Baseline (what conditioning must beat)
The **unconditioned reference class**: the parent-class branch frequencies (all events of the
same event *type*, train-only) for G; the class-mean |CAR| and modal sign for P. A conditioner
adds value only if it lowers the score versus this baseline on held-out data.

## Promotion rule (enforced in code, B5)
A conditioner (any geopolitical field used to form a subset) is labeled **SUGGESTIVE** by
default. It is promoted to **VALIDATED** only if it beats the baseline out of sample on its
score in **both** W1 and W2. Otherwise it stays SUGGESTIVE or is reported as a **null**. Nulls
are published as nulls. Weights/labels move only on out-of-sample evidence.

## Thin-conditioning guard
A conditioned subset is used for branch rates only at **n ≥ 8**; below that the engine falls
back to the parent class and flags "thin conditioning." When max analog similarity is below the
retrieval threshold, the output is **NO ADEQUATE PRECEDENT** (a first-class result, unit-tested).

## Publication
Both windows' G- and P-scores, per class, versus baseline, are written to `data/walk_forward/`
and surfaced on the Backtest console. Every Desk card is stamped with its class's walk-forward
score. Results are shown whatever they are; no result is suppressed or tuned post hoc
(INV: never weaken a test to pass).
