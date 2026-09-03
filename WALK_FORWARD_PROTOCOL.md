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

## Amendment E (2026-09-02) — protocol v3, prospective only: the size-corrected scores become the gate
*Registered before any v3 run; Joe's decision (Brief 2, B-7), dated 2026-09-02. Session B records it.*
- **E.1 Scope.** For every run on the v2 corpus (the 313 events as of 2026-09-02, and any run before
  the pre-1987 corpus is admitted through Joe's sheet, PATH Step 5) §3's registered Brier (G), log score
  and CRPS (P) remain the scores that drive §5's Hedge losses, the FDR family and the §7 gates. Nothing
  about run `walk_20260902T182828Z` or its successors on this corpus is re-judged by this amendment.
- **E.2 The v3 gate.** From the first run after the pre-1987 corpus is admitted (the run's
  `data_state` will say so: `n_events` above the v2 count and `corpus_version: v3`), the **size-corrected
  scores** — Ferro (2014) fair Brier, fair RPS (over the ordinal levels) and fair CRPS, in the weighted
  form of Amendment A.5 with c = Σw²/(1−Σw²) — become the PRIMARY scores: they drive the Hedge losses,
  the FDR family, the SPA family and the §7 conditions. The registered §3 scores are published beside
  them in every block, always, and the placebo (A.4) keeps its size-matched reference.
- **E.3 Reason.** The registered scores of a k-atom analog distribution exceed the population score by
  E|X−X′|/(2k) (CRPS) and Σ_b p_b(1−p_b)/k (Brier; likewise each cumulative term of the RPS), so under the
  null the engine reads as negative skill against a ~10k-atom climatology by sample size alone
  (derived and reproduced by simulation in `tests/test_walk.py`; stated in every summary's `limits`).
  A gate that a null engine cannot pass and a skilled small-k engine cannot pass either is not a gate.
  Adopting the corrected scores prospectively, at the corpus change, keeps every v2 number as judged.
- **E.4 Hedge losses under E.2.** The fair Brier and fair CRPS can be slightly negative for weighted
  mixtures; Hedge losses are clamped to [0, 1] after scaling as today (stated).

## Amendment F (2026-09-02) — the filtration audit, block permutation, and two missing corrections
*Registered before the code (Brief 2, B-8), answering docs/red_team_2/D2_leakage_hunt.md finding 1 and
D3_multiplicity.md findings 1, 3 and 5. Session B.*
- **F.1 The leakage test was structurally blind** (D2 finding 1): comparing the sealed run with a
  maximally broken run detects the presence of a large leak, never the absence of a small one inside
  the sealed path. Two deliberate leaks (an unclosed-window analog admitted; a same-day market
  observation visible to standardization) passed it. From this amendment every run carries a
  **filtration audit** computed inside the sealed run by an independent code path (raw dates, never
  the functions being audited): for every sealed read and every analog it carries, `event_date <
  as_of`; for every analog flagged `g_closed`, `event_date + 90 days ≤ as_of`; for every analog flagged
  `p_closed`, its price window's closing observation date ≤ `as_of`; for every market field of the
  read's state vector, the date of the observation used `< as_of` (and `< as_of − lag` where Amendment
  G applies). Counts and the first violation are published in `summary.json.filtration_audit`; a single
  violation voids the run (`leakage_test.asserted` false). `tests/test_walk_filtration_audit.py`
  re-applies D's two leaks by monkeypatching the sealed path and asserts the audit catches each.
- **F.2 Block permutation** (D3 finding 2 / §5): the registered §6 label permutation shuffles labels
  i.i.d. within class, ignoring §2's 35-day clustering; the label sequence is autocorrelated
  (D3: lag-1 +0.17). Added beside it, and reported as `permutation.block`: the same statistic under
  a permutation that shuffles **intact clusters** (reads within 35 days of the previous read form one
  cluster; clusters are permuted as units within the tier, class stratification dropped), 1,000 draws.
  Both p-values are published; §7's `permutation_p<0.05` condition uses the **block** p-value from
  this amendment on, since it respects the registered dependence rule; the i.i.d. p stays beside it.
- **F.3 RPS item family** (D3 finding 3): the SPA test is also run over the RPS item family
  (`G.rps.spa`, benchmark climatology), so a post-hoc "best RPS item" is guarded as the Brier one is.
- **F.4 Persistence, size-corrected** (D3 finding 1): `diagnostic_fair.engine_vs_persistence` is
  published for P (and G), so "beats persistence" carries its size-corrected effect size beside it. A
  point forecast has no within-forecast spread, so its fair CRPS equals its registered CRPS; the
  engine's fair CRPS is lower than its registered one — the correction can only raise the engine's
  measured advantage over persistence, never lower it.
- **F.5 Item status wording** (D3 finding 5): every item's `verdict.rules` status carries its DM
  p-value and the family SPA p-value in the string, so no item reads as "SUGGESTIVE" without them.

## Amendment G (2026-09-02) — release lags applied in the engine for two market fields
*Registered before the code (Brief 2, B-8; D2 finding 3). §1 promises "otherwise the release lag is
applied"; the observations table carries `as_of = obs_date` for `derived.cot_pct` and
`derived.inv_sigma`.* The engine's information set now applies a registered lag when reading these
fields at t: `cot_pct` (CFTC Commitments of Traders: positions as of Tuesday, released Friday) **3
calendar days**; `inv_sigma` (EIA Weekly Petroleum Status Report: week ending Friday, released the
following Wednesday) **5 calendar days**. An observation dated d is visible at t only if d + lag < t;
the standardization window obeys the same rule. Holidays that delay a release are not modelled
(stated). `summary.json.registered.release_lags` records the map; the filtration audit (F.1) checks it.

## Amendment H (2026-09-02) — the situation fields' knowable-at rule, implemented
*Registered before the code (Brief 2, B-8; D2 finding 4; WORLD_STATE_FRAMEWORK.md Amendment A, session
A).* §1's LIMITATION promised that a situation field whose source postdates t is set to "unknown" for
that read. Session A now stamps every `sr_*` field with `knowable_at` in `situation_state` (entity
`situation`, `vintage = knowable_at`). From this amendment the engine's situation block takes each of
its seven fields (`actor`, `target`, `conflict_scope`, `tempo`, `prior_dyad`, `asset_role`,
`propensity`) from those rows **with vintage ≤ as_of**, and sets a field with no such row to unknown —
for the target and for every candidate alike. The share of fields blanked and the number of events
with no situation field at t are published in `data_state` (session A's count at registration:
262 of 313 events have none). A read whose target has no known situation field is retrieved on the
market block alone, as the distance rule already provides. This will weaken the situation-weighted
items; that is the point-in-time engine, published as computed.

## Amendment I (2026-09-02) — determinism and the content digest
*Registered before the code (Brief 2, B-9).* Every random draw in the walk is seeded from a registered
seed: bootstrap and SPA 19900802, permutation 19900802, placebo 19900802, reliability bands 7, power
simulations 19900802, random-analog draws from SHA-256 of the event id; the seeds are listed in
`summary.json.registered.seeds`. Each sealed read carries `content_hash`: SHA-256 of the record with
`hash`, `sealed_at`, `run_id` and `content_hash` removed (`tests/test_reproduce.py`'s convention), and
`summary.json.determinism.content_digest` is the SHA-256 of the ordered content hashes of the run in
the tree. Two consecutive runs on the same inputs must produce the same digest; `tests/test_walk_determinism.py`
asserts it on the synthetic corpus, and `python3 src/walk.py --digest` prints the digest of the run in
the tree so `make reproduce` can compare a clone's run to the committed one by digest.

## Amendment J (2026-09-02) — the v3 register: what changes when the pre-1987 corpus is admitted
*Registered prospectively, on Joe's instruction (Brief 3, B-11). **Nothing here is computed and nothing here
re-judges any v2 run.** Session B. The three items take effect together, on the first run whose
`data_state.corpus_version` is `v3` — the first run after Joe admits a batch from
`data/candidates/pre1987_candidates.csv` (PATH Step 5). Every v2 run keeps §3 as its gate (Amendment E.1).*

### J.1 The gate — already registered in Amendment E, restated here as the v3 index
Amendment E (2026-09-02) registers the Ferro size-corrected Brier, RPS and CRPS as the PRIMARY scores from
the first v3 run: they drive the Hedge losses, the FDR family, the SPA family and §7. The registered §3
scores are published beside them in every block, always. E.1 is unchanged: no v2 run is re-judged.

### J.2 The materiality threshold, made point-in-time
The read-time materiality call (`read.m_read`, and the `in_big_move` flag on every analog) uses the
registered full-history top-5 % threshold of `BIG_MOVES_REGISTRATION`. A read at t therefore uses a
threshold informed by moves after t. Session D named this (`docs/red_team_2/D2_leakage_hunt.md` finding 2/7);
session B measured it rather than assuming: recomputing `big_moves.episodes_for` on history truncated at each
`as_of`, the threshold moves between 0.165 (1996) and 0.229 (1992) against the full-sample 0.212, and **2 of
the 41 registered episodes with ≥ 500 prior observations would not clear the threshold computed from history
before their own onset** (`data/handoffs/B_response_to_D.md`).

From the first v3 run: the M call at read time uses the top-5 % threshold of the asset's **own history
strictly before `as_of`**, with a minimum of 500 prior observations; below that the read returns
`M = None` with reason `no_threshold_at_t`, never a call from a full-sample number. The Big Moves *label*
used for scoring M stays the registered full-history one (it is an outcome, not an input, and the walk's
filtration governs inputs); both are published, and the filtration audit (F.1) gains a `materiality_threshold`
check that the threshold used by a read was derived only from observations dated before `as_of`.

### J.3 A new estimand: the CHANGE in escalation level, not the level
**Why.** In the published run `walk_20260902T210135Z`, G-persistence — a point mass on the dyad's IES-90
level over [t−90, t−1], 0.9/0.1 smoothed (Amendment B) — beats the engine on the registered Brier by
**0.480 to 0.769** (skill −0.600, DM p 0.002) and on RPS by 0.380 to 0.681 (skill −0.791). Escalation levels
persist; the engine's state vector contains no field for the dyad's own current level, so it forecasts the
level from scratch while persistence starts from the answer. **Any model that does not start from
persistence starts behind.** This amendment registers the estimand that tests whether the analog machinery
adds anything *on top of* persistence, which is the question the level target cannot answer.

**The target.** For a geopolitical read at t with pre-window level L⁻ (Amendment B.1, the persistence level;
`no_independent_outcome` at either end excludes the read, counted) and realized IES-90 level L over
(d, d+90], the target is **ΔIES = L − L⁻**, an ordered categorical on {−3, −2, −1, 0, +1, +2, +3}.

**The forecast.** For each retrieved analog a, its own change Δ_a = L_a − L⁻_a, computed by exactly the same
rule at the analog's own date. The engine's Δ forecast is the frequency distribution of Δ_a over the analogs
(the menu mixture as today, Hedge over the same items). The implied level forecast is that distribution
shifted by the target's L⁻ and clipped into 0..3, with the clipped mass accumulating at the boundary; both
the Δ forecast and the implied level forecast are sealed in the read.

**The scores.** Multi-category Brier and RPS over the seven ordered Δ categories (RPS's distance-awareness is
the point: a Δ miss of one level must cost less than a miss of three), plus the size-corrected forms of
both (E.2). The implied level forecast is *also* scored on the v2 level scores, so the two estimands are
comparable on one axis.

**The baselines** (§4, as adapted): (1) Δ-climatology, the unconditional Δ distribution of the class's prior
closed reads; (2) **no-change**, a point mass on Δ = 0 — which is exactly G-persistence expressed in this
estimand, and is the baseline to beat; (3) random analogs, k drawn at random from the class; (4) the frozen
menu mixture.

**The gate.** §7 unchanged in form, with the size-corrected scores primary (E.2) and the **no-change**
baseline added to the conditions: a Δ result is VALIDATED only if it also beats no-change with DM p < 0.05
after HLN. Beating Δ-climatology while losing to no-change is published as what it is — the engine
rediscovering persistence.

**Not computed here.** No Δ is computed, no code is written by this amendment, and no v2 number changes. The
first v3 run publishes the Δ blocks beside the level blocks, as computed, whatever they say.

## Amendment K (2026-09-03) — the hostility diagnostic on the sealed run (gates nothing)
*Registered BEFORE the numbers are computed, on Joe's instruction. Session B. This amendment adds a
DIAGNOSTIC, in the same standing as the Ferro size-corrected scores of Amendment A.5: it is published beside
the registered numbers, it is published whichever way it comes out, and **it cannot move any verdict.**
§3 and §7 are untouched. `data/walk_forward/reads.jsonl` is not re-scored (OUTCOME_MAPPING Amendment 3
§A3.5); nothing about run `walk_20260903T003422Z` is re-judged.*

### K.1 Why this is not a post-hoc subset
The exclusion set is session F's `hostility` field, defined in OUTCOME_MAPPING.md Amendment 3 §A3.3 and
coded for all 187 events of the four geopolitical classes **before any count under it was computed**
(`data/spine/CLASS_AUDIT.md`; F's blocking condition "do not implement until all four classes are coded"
was cleared at 0 of 4 outstanding). `non_hostile` and `ambiguous` return `no_independent_outcome` under
A3.3 — the G target is *undefined* for those reads, not merely unfavourable. Removing reads whose target is
undefined is a repair of the estimand, not a search over subsets; and because the field was registered and
coded first, the subset could not have been chosen once its effect on the score was known.

### K.2 What is computed
On the daily tier of the published run, restricted to the **G-scorable** reads — `hostility` in
{`hostile`, `hostile_unattributed`} — of the sealed scored set:
- the engine's, frozen's and persistence's G forecasts are taken **as sealed**; nothing is re-read and no
  analog is re-retrieved;
- **climatology is re-estimated on the reduced distribution.** Each sealed read carries its own
  point-in-time G pool (`baselines.random_analogs.g_pool_ids`) and that pool's labels
  (`baselines.climatology.G_labels`), index-aligned. For the diagnostic, pool members that are not
  G-scorable are dropped and the climatology forecast is the level frequency over what remains. This is the
  point of the exercise: the baseline the engine is scored against moves, not only the engine's score;
- **random analogs are re-drawn from the reduced pool**, same k and same per-event seed as the sealed run;
- scores: multi-category Brier and RPS over the IES-90 levels, engine against each of the four baselines,
  with the stationary-bootstrap interval and the DM/HLN test, using the tier's measured mean block and HAC
  lag recomputed on the retained dates.

### K.3 Publication
`summary.json` gains `tiers.daily.G.diagnostic_hostile`, carrying its own `computed_at`, the sealed
`run_id` it was derived from, `registered: false`, the retained and dropped counts by hostility value, the
level-0 share before and after, and every comparison. It is written by `src/engine/diagnostic_hostile.py`
from the sealed files, never by re-scoring, and a short section is added to
`data/handoffs/B_run_delta_spine.md` answering one question: does the engine's negative skill widen, narrow
or hold when the reads whose target is undefined are removed?

### K.4 The limit, stated with the number
n falls from 150 to the retained count, so every interval widens; the registered `min_tier_n` of 30 is still
met but the comparison is materially less powerful than the one it sits beside (measured minimum detectable
skill at the published n = 150 is already 0.127). This is a diagnostic on a sealed run, not a new run, and
it is not the run the paper reports. Whatever it shows, `engine:G` stays SUGGESTIVE / null under §7.

## Amendment L (2026-09-03) — the incremental-information experiment: ΔIES on the v2 corpus
*Registered BEFORE any number under it is computed. Session B, on Joe's instruction of 2026-09-03, and
independently arrived at by an external reviewer the same day. This amendment moves the Δ estimand of
Amendment J.3 forward from the v3 trigger onto the **existing 150 scored daily-tier G reads** of the sealed
run `walk_20260903T003422Z`. It is computed from the sealed files by the discipline of Amendment K —
nothing is re-read, no analog is re-retrieved, no weight is re-fitted except the one object named in L.6 —
and it does **not** re-judge any v2 number and does **not** change the status of `engine:G` under §7.*

### L.0 Why the estimand changes
The strongest result in the published run is that **G-persistence beats the engine**: registered
multi-category Brier 0.4805 to 0.7687 (skill −0.600, DM/HLN p 0.0002, n 150), RPS 0.3798 to 0.6813
(skill −0.791). Escalation levels persist and the engine's state vector carries no field for the dyad's
own current level, so the level estimand asks the engine to **replace** the dyad's recent history rather
than **improve** on it. The question that estimand cannot answer, and this one can:

> **Does the analogue distribution carry information about escalation beyond what the dyad's own last
> 90 days already say?**

### L.1 The target
For a scored daily-tier G read of event e at `as_of` = t with pre-window level L⁻ (Amendment B.1: the
dyad's IES level over W⁻ = [t−90, t−1], as sealed in `baselines.persistence.level_pre`) and realized
IES-90 level L over (d, d+90]:

    ΔIES = L − L⁻,   an ordered categorical on {−3, −2, −1, 0, +1, +2, +3}.

**Exclusions, each counted and published:** `outcome.no_independent_outcome` true; `persistence.fallback`
true (L⁻ not knowable, B.3); a read carrying no analog with a knowable Δ (L.2). Only the daily tier is
computed: the monthly tier has 0 scored G reads.

### L.2 The forecast — the analogue distribution, re-anchored
For each analog a carried by a menu item at this read (`items[*].G_ids`, index-aligned with
`items[*].G_labels`, both already filtered by the walk to analogs whose branch window closed by t):

    Δ_a = L_a − L⁻_a

where L_a is the sealed analog label and **L⁻_a is that analog's own pre-window level, taken from the
analog's own sealed read** (`baselines.persistence.level_pre`, computed on [d_a−90, d_a−1] and therefore
strictly before d_a < t). An analog whose own read has `persistence.fallback` true contributes no Δ and is
dropped from that item's distribution, counted as `n_analog_delta_dropped`. Structural check made before
this amendment was written and reported here as a fact about the data, not a result: **0 of the 10,885
analog slots carried by the 150 scored reads lack L⁻_a.**

An item's Δ forecast is the frequency distribution of its Δ_a. An item with no Δ atom **abstains** and is
charged the Δ-climatology forecast for that read — the registered abstain rule, unchanged.

**The Δ engine (`analogue`) is the mixture over M01–M12 of their Δ distributions, weighted by the sealed
run's Hedge G weights for those twelve items, renormalized to sum 1.** No retrieval is repeated and no
Hedge weight is re-fitted: the Δ experiment is a **pure re-anchoring of the sealed run**. M13 is excluded
and the reason is stated: it is a recalibration of the level mixture, not an analog retrieval, and carries
no analogs to vote on Δ.

**Feasibility (clipping, as J.3 registered).** Given L⁻, the feasible Δ are exactly {−L⁻, …, 3−L⁻}. Every
forecast in this amendment is clipped to that set: mass on an infeasible Δ moves to the nearest feasible Δ
(equivalently, the implied level forecast is clipped into 0..3 with mass accumulating at the boundary).

**A consequence, registered so that it cannot be presented later as a finding.** After clipping, the map
Δ ↔ level (ℓ = Δ + L⁻) is a bijection on the four feasible categories, so the 7-category Δ Brier and RPS
of any clipped forecast are **numerically identical** to the 4-level Brier and RPS of its implied level
forecast. The Δ framing therefore changes the **forecast** (the analogs vote on change, not on level) and
the **baseline** (no-change ≡ G-persistence); it does not change the score axis. `assert_delta_level_identity`
in the code checks this on every read. It follows that `no-change` in Δ space scores exactly what
`persistence` scored in level space, and that the two estimands are directly comparable.

### L.3 The baselines
1. **no-change** — a point mass on Δ = 0 with Amendment B.2's smoothing (0.9 on Δ = 0, 0.1 spread equally
   over the adjacent feasible Δ; a boundary L⁻ gives its one neighbour the whole 0.1). This is
   G-persistence expressed in this estimand and **it is the baseline to beat**.
2. **analogue alone** — L.2's mixture, unshrunk.
3. **Δ-climatology** — the unconditional Δ distribution of the read's own point-in-time G pool
   (`baselines.random_analogs.g_pool_ids` with the aligned `baselines.climatology.G_labels`, each member's
   Δ formed with its own L⁻), clipped. The honest bar (§4 baseline 1).
4. **random analogs** — k drawn from that same pool at the sealed k, seed and number of draws, scored on Δ
   (§4 baseline 3): isolates whether *similarity retrieval* adds anything in this estimand.
5. **frozen** — the equal-weight mixture over M01–M12's Δ distributions (§4 baseline 4).

### L.4 The combination — stated before any number is seen
The object of the experiment is the **combination** of the dyad's own history with the analogue
distribution. Three combination rules are registered; no other is admissible under this amendment.

- **C1 (PRIMARY), the registered weight.** Linear pool `0.5 · no-change + 0.5 · analogue`, clipped. λ = 0.5
  is **fixed, registered, and not fitted to anything.** It is the primary because it cannot be gamed.
- **C2, the walk-forward weight.** Linear pool `λ_i · no-change + (1 − λ_i) · analogue` where λ_i is chosen
  at read i from the registered grid **{0.0, 0.1, …, 1.0}** as the value minimising the cumulative
  registered Δ-Brier of the pool over the reads j in the scored set whose branch window had **closed by**
  `as_of_i` (`g_closed_on ≤ as_of_i`) — the walk's closed-by-t rule, exactly Amendment C.2's. Fewer than
  **40** such reads: λ_i = 0.5. Ties resolve to the **larger** λ (conservative: favours persistence). The
  λ trajectory and the terminal λ* are published.
- **C3, Hedge over the two.** The registered §5 update rule (exponentially-weighted average forecaster,
  η = 0.25, loss = Δ-Brier / g_scale 2.0) over the two forecasters {no-change, analogue}, weights from past
  **closed** reads only, initialised uniform. The weight trajectory is published.

λ in C2 is the only quantity fitted anywhere in this amendment, and it is fitted walk-forward on closed
reads only, on a grid registered here before it was computed.

### L.5 The scores
Amendment E.1 holds: this is a run on the **v2 corpus**, so the registered §3 scores gate.
- **Gate score:** registered multi-category **Brier** over the seven ordered Δ categories.
- **Beside it, always:** **RPS** over the same ordered categories (a Δ miss of one level must cost less
  than a miss of three — this is why the ordinal score matters here), log score, and the **Ferro
  size-corrected** fair Brier and fair RPS as DIAGNOSTIC (A.5 / E.1), never as a gate.
- The implied level forecast is also scored on the v2 level scores; by L.2's identity these agree exactly,
  and disagreement is a defect, not a finding.

### L.6 Inference — the full registered draws
Stationary block bootstrap **2,000** draws on the skill, mean block measured from the registered 35-day
clustering on the retained dates; **Diebold–Mariano with the Harvey–Leybourne–Newbold** correction and HAC
lag = round(mean block) − 1; **SPA (Hansen 2005) 1,000** draws over the combination family {C1, C2, C3}
with **no-change as the benchmark**, so the best of the three is guarded; **Benjamini–Hochberg FDR** across
every comparison this amendment reports. Two permutations, **1,000** draws each, seed 19900802:
- **(i) label permutation, block form (F.2)** — the realized level L is permuted across intact 35-day
  clusters and Δ recomputed as L_perm − L⁻ with each read's **own** L⁻ (feasible by construction). This is
  the §7-form condition, per F.2.
- **(ii) forecast permutation** — the analogue Δ distributions are permuted across intact clusters,
  re-clipped to each receiving read's own feasible set, C1 recomposed, skill vs no-change recomputed. Null:
  *the analogue distribution retrieved for this read carries no more information than one retrieved for a
  different read.* Published beside (i); it does not gate.
Measured **minimum detectable skill** at 80 % power at the retained n is published beside every result, so
a null reads as "not detectable at this n," not "no effect." No placebo is run (the placebo tests P-side
event selection, which this estimand does not touch); stated, not omitted silently.

### L.7 The gate — four registered verdicts, decided before the numbers exist
Let skill = 1 − Brier(C1) / Brier(no-change) on the retained set.

- **INCREMENTAL** — skill > 0 **and** DM/HLN p < 0.05 **and** the 95 % bootstrap CI excludes 0 **and** SPA
  p < 0.05 over the C-family against no-change **and** block label-permutation p < 0.05.
  *Reading: historical analogy carries information beyond the dyad's own last 90 days.*
- **INCREMENTAL-UNDER-FITTED-WEIGHT** — C1 fails the above, **but** C2 beats no-change with DM/HLN p < 0.05
  and a CI excluding 0, **and** C2's terminal λ* < 0.5. *Reading: the analogue carries information, but only
  at a weight the equal pool does not use.* Strictly weaker than INCREMENTAL and never reported as it.
- **DEGRADES** — no-change beats C1 with DM/HLN p < 0.05 and a CI excluding 0, **and** C2's terminal
  λ* ≥ 0.9. *Reading: the analogue actively degrades a good baseline — the fitted weight runs away from it
  too.*
- **NO ADDITION** — anything else, including the case where C1 loses but C2's λ* < 0.9. That case is
  reported as NO ADDITION with the explicit note that **the loss is attributable to the registered equal
  weight, not to the analogue's content** — a fixed 50/50 pool losing is not evidence that analogy degrades.
  Published with the measured MDS at the retained n.

**All four are publishable and none is preferred.** §7 is untouched: nothing in this amendment can make
anything VALIDATED — the §7 label audit is 1 of 30 rows in — and `engine:G` on the level estimand keeps the
status the published run gave it whatever this experiment says.

### L.8 Expected failure modes, registered in advance
1. **Near-degenerate target.** If Δ = 0 on most reads, no-change is near-unbeatable and the experiment is
   underpowered by construction. The marginal Δ distribution and the Δ = 0 share are published beside the
   result, and if that share exceeds 0.90 the estimand is declared near-degenerate in the same breath as
   the verdict.
2. **Fixed-weight conservatism.** A 50/50 linear pool of a sharp point mass and a diffuse analogue
   distribution is worse than the sharp one whenever the analogue is weak — *even if the analogue carries
   some information*. This is exactly why C2 and C3 are registered beside C1 and why DEGRADES additionally
   requires λ* ≥ 0.9.
3. **The small-atom penalty runs against the analogue.** The analogue side is a k ≤ 12-atom empirical
   distribution and no-change is a point mass; the registered Brier charges the analogue Σp(1−p)/k that it
   cannot charge a point mass (E.3). The direction of that bias is known and stated: it works **against**
   the analogue. The Ferro fair scores are published beside for this reason and the gate still stays on the
   registered score (E.1).
4. **Shared-L⁻ error.** L⁻ enters the target, the baseline and the analogue anchor at once. A coverage
   error in L⁻ inflates the target's error and **cancels** in no-change, mechanically favouring the
   baseline. Sensitivity, registered: the whole comparison repeated on reads with ≥ 2 sources in
   `covering_pre`.
5. **Analog-side L⁻ noise.** Δ_a inherits the coverage of the analog's own W⁻. The distribution of
   `covering_pre` sizes across analog slots is published.
6. **Undefined targets.** `no_independent_outcome` is excluded (L.1); the Amendment K hostility set
   (`non_hostile`, `ambiguous`, whose G target is undefined under OUTCOME_MAPPING A3.3) is published as a
   registered secondary restriction, not as a chosen subset.
7. **Power.** n = 150 before exclusions; the measured MDS on the level target at n = 150 was **0.127**. A
   null here means "not detectable at this n."
8. **The identity of L.2 is not a bug.** If the analogue re-anchoring changes nothing, C1 vs no-change
   reproduces the level-estimand persistence comparison. That is the NO ADDITION branch, published as such.

### L.9 Publication
`src/engine/delta_experiment.py`, written from the sealed files only, produces
`data/walk_forward/delta_experiment.json` and `summary.json → tiers.daily.G.experiment_delta`
(`registered: true`, `amendment: L`, `derived_from_run`, `gates: engine:G unchanged`). Tests carrying the
amendment id live in `tests/test_delta_experiment.py`. The numbers go to Cowork in
`data/handoffs/B_to_Cowork_2026-09-03_delta_experiment.md`, **as computed**, whichever of the four
verdicts holds.

## Amendment M (2026-09-03) — pooling or similarity? the three-pool control on Amendment L (gates nothing)
*Registered BEFORE the numbers, and registered **post hoc**: this control was motivated by Amendment L's
result, which is stated here rather than concealed. It therefore takes DIAGNOSTIC standing, exactly as
Amendment K does — published beside the registered numbers, published whichever way it comes out, and it
**cannot move any verdict**. L.7's NO ADDITION stands whatever M shows. §3 and §7 are untouched, nothing is
re-scored, and no v2 number is re-judged. Session B.*

### M.1 Why
Amendment L found that the registered equal pool C1 (½ no-change + ½ analogue) scores 0.4643 against
no-change's 0.4805 — a gain that does not clear any of L.7's conditions — while the **Δ-climatology**
baseline alone scores 0.4635, better than the retrieved analogue's 0.4799 and marginally better than C1
itself. That leaves L's headline number ambiguous between two readings which the registered comparisons
cannot separate:

- **pooling** — any second distribution, pooled with a 0.9-sharp point mass, buys the same shrinkage; or
- **similarity** — the *retrieved* analogues specifically carry something the unconditional distribution does not.

L's registered baselines answer this for the components in isolation (analogue 0.4799 vs random analogs
0.4824 vs Δ-climatology 0.4635) but not **inside the pool**, which is the object L was built to test.

### M.2 What is computed
Three pools at the **identical registered weight λ = 0.5**, differing only in the second component, so the
weight cannot explain any difference between them:

| pool | second component | isolates |
|---|---|---|
| **C1** (from L.4, unchanged) | the retrieved analogue mixture, k ≤ 12 atoms | similarity + atom count |
| **C0r** | random analogs from the read's own point-in-time G pool, same k, same sealed seed and draws | atom count alone |
| **C0** | the read's own point-in-time Δ-climatology, the whole pool | pooling alone |

Reported: each pool against no-change (skill, stationary-bootstrap CI at the registered 2,000 draws, DM/HLN
at the tier's measured HAC lag) and — the comparison the amendment exists for — **C1 against C0 and C1
against C0r, paired on the same reads**, on the registered Brier and on RPS.

### M.3 How it is read, stated before the numbers exist
- **C1 ≈ C0** → the gain is **pooling**. The retrieved analogues are interchangeable with the unconditional
  Δ distribution and similarity retrieval contributes nothing inside the pool.
- **C1 > C0** → the gain is **similarity**: retrieval carries something the unconditional distribution does
  not, *even though* L.7 says the gain does not clear its conditions. This would be reported as a
  diagnostic direction, never as a result that changes L's verdict.
- **C1 < C0** → retrieval **costs** the pool: the engine would do better pooling persistence with the class
  base rate than with its own analogues.
- **C0r vs C0** prices the small-atom penalty of E.3 inside the pool with content held fixed (the same pool,
  the same draws, k atoms against all of them), so a C1 < C0 gap can be attributed to atom count or to
  content rather than left ambiguous.

All four readings are publishable and none is preferred.

### M.4 Publication
`data/walk_forward/delta_experiment.json → diagnostic_pools`, carrying `registered_post_hoc: true`,
`gates: nothing`, and the sentence that this control was motivated by L's own result. Test:
`tests/test_delta_experiment.py::test_M2_*`.
