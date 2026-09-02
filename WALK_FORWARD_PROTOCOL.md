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
