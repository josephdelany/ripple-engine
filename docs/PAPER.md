# When event labels hurt historical analogy

## A registered comparison of structural and surface matching in geopolitical oil events

Joseph Delany · Colby College · 2026

## Abstract

Analysts often select historical precedents from visible event labels: a closure is compared with other closures, or a sanction with other sanctions. The stronger claim behind analogical inference is that cases should correspond across the state in which events occur. I test that distinction directly. On 313 dated geopolitical and oil-policy events, two walk-forward forecasters use the same eligible prior cases and forecast Brent’s 20-trading-day abnormal return; they differ only in whether cases are weighted by a point-in-time state vector or by event-class identity. That vector turns out to be narrow — four market fields reach every comparison, two leadership fields reach half, and one dyadic field reaches three — so what is tested is a market-and-leadership state against event labels, not full structural correspondence. Structural weighting records mean CRPS 8.341 against 8.784 for surface matching (paired difference −0.444; 95% stationary-bootstrap interval [−0.613, −0.269]; DM *p*=8.65×10⁻⁷; 264 dates). But uniform pooling scores 8.390, and structure does not distinguishably beat it (difference −0.049; interval [−0.112, +0.012]; *p*=0.140). Surface matching is significantly worse than pooling. The evidence supports a narrow conclusion: class labels sharply down-weight cross-class precedents and can damage forecasts; it does not establish production forecasting skill for the structural instrument. An availability audit also shows why the stronger test remains difficult: only 671 of 11,029 panel-derived state rows satisfy the registered point-in-time rule.

## 1. Research question

When an analyst says that a contemporary shock resembles a famous precedent, is that inference or pattern matching? Historical work establishes that policymakers use analogies and that poorly chosen precedents can distort decisions (May 1973; Jervis 1976; Khong 1992). Surface analogy selects cases because their event labels agree. Structural analogy compares the wider state: geopolitical alignment, conflict conditions, market conditions, and other variables observable at the forecast date.

The instrument is the experiment. Its state vector defines “structure”; its distance rule defines correspondence; its candidate pool defines which precedents are admissible; its vintage rule defines what could have been known; its outcome defines “what followed”; and its baselines define “adds information.” The [registered protocol](../registrations/STRUCTURAL_SURFACE_EXPERIMENT.md) fixes those choices.

## 2. Data and estimand

The input bundle contains 313 events, 29,458 daily market observations across three series (Brent 9,963; WTI 10,231; VIX 9,264), and 11,089 state observations. It is committed as CSV with hashes in `data/structural_surface/input/bundle_manifest.json`.

The bundle is where reproducibility stops, and the boundary is worth stating precisely. `make reproduce-central` rebuilds every frozen artifact from those CSVs alone, with no database, network access or credentials, and requires SHA-256 equality. The CSVs themselves cannot be re-derived and checked: they were exported from a gitignored 242 MB database whose recorded hash no longer matches the file present here, and 4,717 of the 11,089 state rows (42.5%) originate in Stata and Excel distributions that must be obtained by hand, with others key-gated or request-gated. Every row carries its own source, observation date, vintage, release date and retrospective flag, so an individual row can be audited against the dataset it names. This is auditability by receipt, not reproduction by pipeline. `src/bundle_provenance.py` checks both halves on demand and reports the upstream database as reproduced, diverged or absent rather than silently; [`docs/audit/PROVENANCE_BOUNDARY.md`](audit/PROVENANCE_BOUNDARY.md) records the full accounting.

The primary outcome is cumulative abnormal Brent log return over exactly 20 daily returns, from the last close before the event through the nineteenth trading observation on or after it. Expected return is a constant mean estimated from up to 250 trading days ending 21 trading days before the event, with at least 100 observations required. This makes the outcome an event-window deviation from the prior market process rather than the raw movement of oil (`src/structural_surface_experiment.py`, function `abnormal_outcome`).

At each forecast date, both arms receive every prior, outcome-closed event with a usable target and at least three common strict state fields. There is no same-class eligibility filter. A state observation is eligible only when its observation date, vintage, and release date do not exceed the event date and it is not retrospective (`src/structural_surface_experiment.py:103–112`, function `strict_panel_rows`). Holding support fixed isolates weighting from candidate selection.

## 3. Competing analogy rules

Surface distance is zero when two events share a class and one otherwise. Structural distance is the equal-block average of normalized field distances over fields jointly available to the pair. Both become weights through the same kernel, `exp(−d/0.25)`. The forecast is the weighted empirical distribution of prior abnormal returns.

### What the structural vector actually contains

The rule above admits any field the pair share. The registered eligibility filter is strict enough that
few survive, and the paper's earlier description of a "structural state" was therefore broader than the
computation. Recomputed from the frozen reads over all 41,997 target–candidate comparisons in the 264
scored dates:

| field | block | comparisons | share |
|---|---|---:|---:|
| `market:wti_chg20` | market | 41,997 | 100.00% |
| `market:brent_chg20` | market | 41,982 | 99.96% |
| `market:brent_vol20` | market | 41,982 | 99.96% |
| `market:vix_close` | market | 41,322 | 98.39% |
| `panel:leader_change_last_365d` | actors | 21,082 | 50.20% |
| `panel:leader_tenure_days` | actors | 21,082 | 50.20% |
| `panel:mid_last_date` | dyads | 3 | 0.01% |

No other field, and no fourth block, ever enters a distance. 20,915 comparisons (49.8%) use market fields
only, 73 of the 264 dates are entirely market-only, and the whole experiment contains six distinct field
combinations. `tests/test_paper_field_composition.py` recomputes these from the ledger and fails if this
table drifts from it.

Two readings of that are both wrong. It is not a full-state comparison: alignment, regime, capability and
conflict variables are present in the catalogue and absent from the arithmetic. But neither is it merely a
market model, because the distance averages *blocks* rather than fields. On the half of comparisons that
carry the two leadership fields, the `actors` block takes half the distance weight while four market
fields share the other half — so leadership is weighted heavily exactly where it exists. The accurate
description is a market-state comparison on half the comparisons and a market-and-leadership comparison,
equally weighted between the two, on the other half.


The primary score is weighted CRPS, a strictly proper score for predictive distributions (Gneiting and Raftery 2007). Each forecast is serialized and sealed by SHA-256 before its target is attached. Inference is paired by date using the Diebold–Mariano comparison with a finite-sample correction (Diebold and Mariano 1995; Harvey, Leybourne, and Newbold 1997), Newey–West variance, and a stationary-bootstrap interval (Politis and Romano 1994). Uniform weighting on identical support is a registered diagnostic separating useful similarity from pooling.

## 4. Primary result

There are 264 scored dates; 24 events have an unusable target and 25 lack the minimum pool of eight prior cases. Structural weighting scores 8.3407 and surface weighting 8.7842. Their paired difference is −0.4435, with interval [−0.6130, −0.2687] and *p*=8.65×10⁻⁷. Under the registered rule, structure beats surface.

The uniform diagnostic determines the interpretation. Pooling scores 8.3900. Structure is better by 0.0493 CRPS, but [−0.1120, +0.0121] crosses zero and *p*=0.1400. Surface is worse than uniform by 0.3942, [0.2224, 0.5698], *p*=1.43×10⁻⁵. Median effective sample size is 130.2 under structure and 28.7 under surface.

Thus structural comparison preserves information class matching throws away. The experiment does not establish that structural weighting extracts reliable 20-day signal beyond the historical pool itself.

Five- and ten-day outcomes were non-verdict diagnostics. Neither distinguishes structure from surface or uniform after the exact-horizon correction. They are not the headline.

## 5. What the audit changed

The earlier price walk forecast raw 20-day Brent returns (`src/engine/read.py:153–181`, methods `path` and `outcome`). That mixes event response with the ordinary market process. Target-only corrections gave different answers in two legacy designs, showing that target construction matters and those designs are not interchangeable. Neither replaces the direct experiment, and neither supplies an additional headline here.

The earlier event walk admitted only same-class candidates (`src/engine/read.py:205–214`, method `pool`) and built climatology from that conditioned pool (`src/walk.py:257–266`). It tested within-class reranking, not structural versus surface analogy. The central experiment removes that filter and holds support fixed.

The original “knowable at *t*” conclusion was not an availability test. Situation fields without a dated URL inherited their 2026 coding date (`src/situation_vintage.py:279` in the audited version), so they failed mechanically. The defensible statement is that availability could not be demonstrated. In the rebuilt input, only 671 of 11,029 panel-derived rows satisfy observation/vintage/release/non-retrospective rules. At least one strict panel field is available for 227 events, with median six usable fields among them. This is a feasibility and metadata finding, not proof that analysts lacked the information.

Legacy escalation labels often used violence anywhere in the affected country rather than dyadic escalation (`src/state/ies90.py:385`), while persistence lagged that measure (`src/engine/persistence.py:45`). Those results do not answer whether the event parties escalated and are not evidence for the present claim.

## 6. Significance and limitations

The consequential result is the primary comparison together with its uniform control: surface class matching can make an analyst worse than retaining the eligible reference class. That argues against event type as an eligibility gate and for testing similarity systems against unrestricted pooling on identical support.

This is not a rescue of the original engine, and it is not yet an answer to the question in §1. The registered comparison was designed to test whether correspondence across the wider state beats correspondence of labels. What it could execute was a comparison between a market-and-leadership state and labels, because that is all the strict availability rule left standing. The stronger test is therefore not failed here; it is untested, and no result in §4 should be read as evidence about the geopolitical variables that never entered a distance. A registered component and concentration ablation ([`registrations/STRUCTURAL_COMPONENT_ABLATION.md`](../registrations/STRUCTURAL_COMPONENT_ABLATION.md)) separates the remaining possibilities — market conditioning, leadership information, or the breadth of the reference class — on this same frozen support. A further caution follows from the table in §3: with only six distinct field combinations, and one of the three blocks reaching three comparisons out of 41,997, the design has far less independent structural variation than 41,997 comparisons suggests. Structure has not shown 20-day skill beyond pooling. The catalogue is curated, not a probability sample; coverage varies by era; strict state availability is sparse; missingness may encode time and source coverage; the equal-block metric and bandwidth are design choices; and abnormal returns do not remove every concurrent cause. Dependence-aware inference cannot repair catalogue selection or measurement error.

The next serious analysis is prospective collection of time-stamped states and forecasts under this frozen protocol. Until then, the honest headline remains comparative: structure beats surface matching, while pooling remains competitive.

## 7. Reproduction

Run `make reproduce-central`. It uses the committed input bundle, rebuilds central outputs in isolation, and verifies byte-for-byte hashes against `data/structural_surface/manifest.json`. The scientific artifacts are `reads.jsonl`, `scores.jsonl`, and `summary.json`. Tests enforce filtration, equal support, seal-before-outcome order, scoring, and deterministic reproduction.

The six-week system and retractions remain in repository history and the audit record, but are not additional validated findings. Tag `closure-core-frozen-2026-09-03` is the pre-closure recovery point.

## References

- Diebold, F. X., and R. S. Mariano. 1995. “Comparing Predictive Accuracy.” *Journal of Business & Economic Statistics* 13(3): 253–263.
- Gneiting, T., and A. E. Raftery. 2007. “Strictly Proper Scoring Rules, Prediction, and Estimation.” *Journal of the American Statistical Association* 102(477): 359–378.
- Harvey, D., S. Leybourne, and P. Newbold. 1997. “Testing the Equality of Prediction Mean Squared Errors.” *International Journal of Forecasting* 13(2): 281–291.
- Jervis, R. 1976. *Perception and Misperception in International Politics*. Princeton University Press.
- Khong, Y. F. 1992. *Analogies at War: Korea, Munich, Dien Bien Phu, and the Vietnam Decisions of 1965*. Princeton University Press.
- May, E. R. 1973. *“Lessons” of the Past: The Use and Misuse of History in American Foreign Policy*. Oxford University Press.
- Politis, D. N., and J. P. Romano. 1994. “The Stationary Bootstrap.” *Journal of the American Statistical Association* 89(428): 1303–1313.
