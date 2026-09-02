# WALK-FORWARD PROTOCOL — the self-enforcing backtest, registered before running
*2026-09-02. This document fixes what is tested, how it is scored, what it is
compared against, how the engine is allowed to learn, and which tests of the test
must pass — before any number is computed. Amendments are dated and appended.
Plain-English glosses follow each technical term; the terms are the ones the
forecasting-evaluation literature uses, so the results can be read by anyone
trained in it.*

## 0. What is being tested (the object)
At each date t the engine issues a **read** R_t for a development: (G) a
probability distribution over the four escalation branches at +90 days; (P) a
predictive distribution over the price outcome at +20 trading days (and +3
months on the monthly tier), given as the empirical distribution of analog
paths; (M) a materiality call. The question is not "does it make money." It is
the forecaster's question: **do the engine's distributions have skill — are they
sharper than the naive alternative while remaining calibrated — and does that
skill hold out of sample, in sequence, through fifty years?**

## 1. Information discipline (the filtration)
*Gloss: the engine at date t may use only what a person could have known by t.*
- Corpus: events with `event_date` (first knowability) < t. No event enters an
  earlier read, ever.
- Prices and series: observations dated ≤ t; macro series use ALFRED vintages
  where they exist (already in the DB), otherwise the release lag is applied.
- Situation fields: the coded record as it stood at t. LIMITATION, stated: the
  current situation fields are not vintage-stamped; until each field carries a
  source date, fields whose source postdates t are set to "unknown" for that
  read (conservative), and the share of fields blanked is reported.
- Outcome labels: the +90d branch label is corpus-derived. Before any G-skill
  is called more than SUGGESTIVE, a 60-event stratified sample of labels is
  audited against sources by a human and Cohen's κ ≥ 0.6 is required
  (*gloss: two coders agree well beyond chance*).
- Leakage guard: the walk is run twice, once with the filtration enforced and
  once with it deliberately broken (future events visible). The two runs must
  differ; if they do not, the filtration is not doing anything and the result
  is void.

## 2. Sequential design
*Gloss: stand at each shock in order, read, seal, advance, score.*
- **Anchored expanding-window, rolling-origin evaluation** (Tashman 2000): the
  training set grows; nothing is ever re-fitted on the test point.
- Unit of evaluation: every corpus event after a burn-in (the first date at which
  the class of the event has ≥ 8 prior members; earlier events are read but
  scored only as "no adequate precedent" cases).
- Each read is **sealed**: written to `data/walk_forward/reads.jsonl` with a
  content hash and timestamp before the outcome is looked up. The file is
  append-only.
- Two tiers, never pooled: monthly (1946–1987, WTI spliced; horizons in months)
  and daily (1987–2026, Brent; horizons in trading days). Results are reported
  per tier and, for the geopolitical branch model only, jointly.

## 3. Scoring (strictly proper scoring rules)
*Gloss: a "proper" score is one a forecaster cannot game — the best expected
score comes only from reporting honest probabilities (Gneiting & Raftery 2007).*
- G (branches, categorical): **Brier score** (multi-category) and **log score**.
  Brier is decomposed (Murphy 1973) into **reliability** (are 30% calls right
  30% of the time?), **resolution** (do the calls vary usefully across
  situations?) and **uncertainty** (how hard the problem is). Reliability
  diagrams with block-bootstrap bands.
- P (price distribution): **CRPS** — continuous ranked probability score
  (*gloss: how far the whole predicted distribution sits from the realized
  value; generalizes absolute error to distributions*). Secondary: **pinball
  loss** at the 10/50/90 quantiles; sign accuracy; **PIT histogram** for
  calibration (*gloss: realized values should fall uniformly across the
  predicted distribution*).
- M (materiality): precision/recall of MATERIAL against membership of a Big
  Moves window, per tier.
- **Skill score** = 1 − S_engine / S_reference; positive means the engine beats
  the reference.

## 4. References the engine must beat (baselines)
1. **Climatology**: the unconditional class base rate (G) / the class's
   unconditional outcome distribution (P). This is the honest bar.
2. **Persistence / no-change** for P.
3. **Random analogs**: the same k analogs drawn at random from the class,
   which isolates whether *similarity retrieval* adds anything.
4. **The frozen engine**: the engine with its initial weights, never updated —
   isolates whether *learning* (§5) adds anything.

## 5. The learning loop (how the engine is allowed to get better)
*Gloss: after each outcome is known, and only then, the engine may adjust — but
only within a small, pre-declared menu, so it cannot fit itself to the past.*
- Adjustable: the similarity weights over the situation fields (currently
  uniform), the retrieval threshold, and k. The menu is a **finite, registered
  set** of candidate weightings (≤ 12), listed in `data/walk_forward/menu.json`
  before the run.
- Update rule: **exponentially-weighted average forecaster** (Hedge; Cesa-Bianchi
  & Lugosi 2006) over the menu, weights updated from cumulative *past sealed*
  scores only. This carries a proven regret bound (*gloss: over time it does
  nearly as well as the best single menu item, and cannot be fooled into
  chasing noise for long*).
- Weights at every step are logged; the **learning curve** (cumulative skill vs
  time) is a published figure. Whether learning helps is itself a tested
  hypothesis (§4 baseline 4), not an assumption.

## 6. Inference (is the skill real?)
- **Diebold–Mariano test** of the engine vs each baseline on the sequence of
  score differentials, with the **Harvey–Leybourne–Newbold** small-sample
  correction and HAC variance for overlapping horizons (*gloss: a t-test built
  for forecast comparisons that respects that neighboring reads overlap*).
- Dependence: reads within 35 days are one cluster (registered clustering
  rule); **stationary block bootstrap** (Politis–Romano) for all intervals.
- **Reality Check / SPA** (White 2000; Hansen 2005): because several
  conditioners, horizons and assets are tried, the "best" one is tested against
  the null that *none* beats the baseline — the standard guard against
  data-snooping (*gloss: with enough tries something looks good by luck; this
  test prices that in*). Benjamini–Hochberg FDR across the family of reported
  comparisons.
- **Placebo**: VIX/vol-matched pseudo-events at non-event dates (already built);
  engine skill on placebos must be indistinguishable from zero.
- **Label permutation** (G): outcome labels shuffled within class, 1,000 times,
  gives the null distribution of skill; the observed skill's rank is the
  permutation p-value.
- **Regime-block leave-out**: 2008, 2020, 2026 removed as whole blocks; skill
  must survive each.
- **Specification curve**: every registered threshold (top-5%, n ≥ 8, k, 35-day
  clustering, horizons) varied across its pre-declared range; the distribution
  of skill across specifications is published, not the best one.
- **Power**: simulation-based minimum detectable skill at 80% power for the
  actual n per class and tier, reported beside every result so that a null is
  read as "not detectable at this n," not "no effect."

## 7. Promotion rule (what may be called what)
- A conditioner or the learning loop is **VALIDATED** only if: skill > 0 against
  climatology in *both* tiers where data permit, DM p < 0.05 after HLN, survives
  SPA and all three regime blocks, placebo null, label-permutation p < 0.05,
  and the label audit (§1) has passed. Otherwise **SUGGESTIVE**. Nulls are
  published as nulls.
- No occurrence probabilities are ever emitted; every published rate is a
  frequency with its n.

## 8. Outputs (all published as computed)
`data/walk_forward/reads.jsonl` (sealed reads), `scores.jsonl`, `weights.jsonl`
(the learning trajectory), `summary.json` (skill by tier/class/horizon with
intervals, DM and SPA p-values, power), figures: learning curve, reliability
diagrams, PIT histograms, specification curve, "what the engine knew at each
Big Move" table. The Ledger's engine board reads from `summary.json`.

## 9. Known limits, stated in advance
n ≈ 300 daily-tier events and 14 monthly-tier events: the monthly tier can
describe, not validate. Outcome labels are corpus-derived until audited.
Situation fields are not yet vintage-stamped. Flow history begins 2026; the
flow side of P is a price proxy until then. None of these are hidden by the
scores; each is a labelled column in the summary.

## References
Tashman (2000) *Int. J. Forecasting*; Gneiting & Raftery (2007) *JASA*; Murphy
(1973) *J. Appl. Meteor.*; Diebold & Mariano (1995) *JBES*; Harvey, Leybourne &
Newbold (1997) *Int. J. Forecasting*; White (2000) *Econometrica*; Hansen (2005)
*JBES*; Politis & Romano (1994) *JASA*; Cesa-Bianchi & Lugosi (2006)
*Prediction, Learning, and Games*; Benjamini & Hochberg (1995) *JRSS-B*;
Tetlock & Gardner (2015) *Superforecasting*; Green & Armstrong (2007) *Int. J.
Forecasting*.

## Amendment B (2026-09-02) — G-persistence, the fourth G baseline (§4)
*Registered before the code (Brief B-1). §4 lists persistence for P only, so the G tier carried three
baselines and PATH §3 D4 read PARTIAL. Dated and appended; §0–§9 unchanged. Session B.*

- **B.1 Definition.** For a read of event e at `as_of` = t, the G-persistence forecast is a point mass
  on the IES level the event's **primary dyad** had reached over the 90 days ending the day before t,
  W⁻ = [t−90, t−1]: the same sources and rules as the label (OUTCOME_MAPPING.md Amendment 1, 1.1 and
  2 — dyadic precedence, littoral map as location), evaluated on W⁻ instead of (d, d+90]. Concretely
  `ies90.score_event(t − 91 days, A, P, L, sources)` with A, P, L derived exactly as for the label. Only
  records dated ≤ t−1 enter; a crisis, dispute or war still ongoing at t contributes by its dated
  onset only (the A1.1 rules applied to W⁻). Each source is held in its single published vintage — no
  vintages exist for these datasets — stated here as the same limitation the labels carry.
- **B.2 Smoothing.** Probability 0.9 on L⁻ and 0.1 spread equally over its adjacent levels (L⁻ ± 1
  within 0..3); a boundary level (0 or 3) has one neighbour, which takes the whole 0.1.
- **B.3 Fallback.** A level is knowable only when ≥ 1 source covers W⁻ under the coverage rule. When
  none does, the persistence forecast for that read is the climatology forecast, and the read is
  counted: `n_persistence_fallback` per tier is published beside the block.
- **B.4 Publication.** `tiers.*.G.engine_vs.persistence` (Brier; log and RPS beside it) with the
  stationary-bootstrap interval and the DM/HLN test like the other baselines, and an SPA block with
  persistence as the benchmark (`G.spa_vs_persistence`) beside the registered climatology-benchmark
  SPA. The persistence forecast is sealed in every read (`baselines.persistence.G`, with `level_pre`,
  `covering_pre` and `fallback`). It enters the FDR family. With this, G carries four baselines and D4
  is judged on the published file.
- **B.5 Test.** `tests/test_walk_baselines.py`: on a synthetic corpus the persistence level for a read
  at t never uses a record dated ≥ t (a record injected at t or later leaves the forecast unchanged;
  one injected inside W⁻ changes it); the smoothing sums to 1; the fallback is counted.

## Amendment C (2026-09-02) — M13, the engine with walk-forward recalibration (§5 menu, 13th item)
*Registered before the code (Brief B-2). Motivation from the published run `walk_20260902T182828Z`
(daily tier, 150 scored G reads): the label permutation rejects noise (p = 0.008) while the Brier
skill vs climatology is null (−0.007). Murphy's decomposition says why: on level 0 the engine's
resolution is 0.0376 against climatology's 0.0004 (it separates cases), but on levels 2 and 3 its
reliability is 0.0420 and 0.0351 (climatology 0.0198 / 0.0224) — overconfident on force and war: in
the 0.4–1.0 forecast bins for level 2 the observed frequency is 0.32 / 0.00 / 0.00 (n 25 / 1 / 3) and
for level 3 it is 0.25 / 0.36 / 0.25 (n 36 / 14 / 4). Resolution the engine has; calibration it has
not. M13 tests whether calibration learned strictly from the past recovers the skill. Dated and
appended; the menu grows to 13 (the ≤ 12 cap of §5 is amended to ≤ 13 by this item and no other).*

- **C.1 Base forecast.** The frozen mixture: equal weights over M01–M12 at the same read (the
  registered §4 baseline 4). M13 is a function of the twelve items' reads at t and of past closed
  outcomes only. The frozen baseline itself stays the uniform mixture over M01–M12.
- **C.2 Recalibration.** Per IES level l, a monotone map g_l: [0,1] → [0,1] applied to the frozen
  mixture's probability of l, then the four mapped probabilities renormalized to sum 1. The map is
  fitted, expanding, on the frozen mixture's own earlier reads in the same tier whose branch window
  had **closed by t** — the walk's closed-by-t rule (`g_closed_on ≤ as_of`), which in the sequential
  walk is exactly the set of reads whose outcome was looked up before this read was sealed; the
  sealed `looked_up_at` and `sealed_at` stamps are asserted to satisfy this. Let n be the number of
  such reads. n < 40: identity (M13 = the frozen mixture). n ≥ 40: for level l, isotonic regression
  (pool-adjacent-violators on (p, 1[level = l]), evaluated by linear interpolation between block
  centres, clamped to [0,1]) when the level has ≥ 40 positive cases among the n reads; otherwise
  Platt scaling (σ(a·logit(p) + b), maximum likelihood by Newton's method, p clipped to [0.01, 0.99]).
- **C.3 P and M.** M13's price distribution and materiality call are the frozen mixture's, unchanged.
  Its Hedge losses are computed like any item's; Hedge runs over thirteen items.
- **C.4 Replays.** The specification curve and the label permutation refit the recalibrator
  sequentially from the replayed (respectively permuted) closed outcomes under the same rule, so M13's
  permutation p-value and its spec-curve rows are as computed, never copied.
- **C.5 Publication.** M13 is scored like any item (`items_vs_climatology.M13_recalibrated`, DM/HLN,
  the SPA family, regime blocks, permutation) and additionally reported as a forecaster in the
  reliability figures `figures/reliability_G_<level>.png` (engine, climatology, M13; the 95 % bands
  of `murphy_*.diagram`). §7 alone decides its status; nothing in this amendment changes §7.
- **C.6 Test.** The leakage test is extended: the recalibrator never sees a score whose
  `g_closed_on` > `as_of` or whose `looked_up_at` ≥ the read's `sealed_at`; a recalibrator fitted with
  that rule broken must produce a different M13 forecast on at least one read (asserted).

## Amendment D (2026-09-02) — the sealed-run archive (§2, §8)
*Registered before the code (Brief B-4). `reads.jsonl` grows by ~5 MB per run.* The three sealed logs
in the tree (`reads.jsonl`, `scores.jsonl`, `weights.jsonl`) hold the current run only. When a run
completes, every earlier run's rows are moved — never edited, never dropped — to
`data/walk_forward/runs/<run_id>/{reads,scores,weights}.jsonl.gz` (git-ignored, kept on disk; each
archive still verifies by `walk.verify_file`). `summary.json.data_state.archived_runs` lists the
archived run_ids with their record counts and seal checks. "Append-only" (§2) holds within each run's
file; the leakage test and the seal check are computed on the run in the tree.
