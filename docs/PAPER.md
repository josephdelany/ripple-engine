# When historical analogy helps—and when the label hurts

## A registered comparison of structural and surface matching in geopolitical oil events

Joseph Delany · Colby College · 2026

## Abstract

Analysts often select historical precedents from visible event labels: a closure is compared with other closures, or a sanction with other sanctions. The stronger claim behind analogical inference is that cases should correspond across the state in which events occur. I test that distinction directly. On 313 dated geopolitical and oil-policy events, two walk-forward forecasters use the same eligible prior cases and forecast Brent’s 20-trading-day abnormal return; they differ only in whether cases are weighted by a point-in-time structural state vector or by event-class identity. Structural weighting records mean CRPS 8.337 against 8.782 for surface matching (paired difference −0.446; 95% stationary-bootstrap interval [−0.623, −0.271]; DM *p*=1.57×10⁻⁶; 264 dates). But uniform pooling scores 8.392, and structure does not distinguishably beat it (difference −0.055; interval [−0.115, +0.006]; *p*=0.090). Surface matching is significantly worse than pooling. The evidence supports a narrow conclusion: class labels discard useful cross-class precedents and can damage forecasts; it does not establish production forecasting skill for the structural instrument. An availability audit also shows why the stronger test remains difficult: only 671 of 11,029 panel-derived state rows satisfy the registered point-in-time rule.

## 1. Research question

When an analyst says that a contemporary shock resembles a famous precedent, is that inference or pattern matching? Surface analogy selects cases because their event labels agree. Structural analogy compares the wider state: geopolitical alignment, conflict conditions, market conditions, and other variables observable at the forecast date.

The instrument is the experiment. Its state vector defines “structure”; its distance rule defines correspondence; its candidate pool defines which precedents are admissible; its vintage rule defines what could have been known; its outcome defines “what followed”; and its baselines define “adds information.” The [registered protocol](../registrations/STRUCTURAL_SURFACE_EXPERIMENT.md) fixes those choices.

## 2. Data and estimand

The input bundle contains 313 events, 29,458 Brent observations, and 11,089 state observations. It is committed as CSV with hashes in `data/structural_surface/input/bundle_manifest.json`.

The primary outcome is cumulative abnormal Brent log return from the event date through 20 trading days. Expected return is a constant mean estimated from up to 250 trading days ending 21 trading days before the event, with at least 100 observations required. This makes the outcome an event-window deviation from the prior market process rather than the raw movement of oil (`src/structural_surface_experiment.py:242`).

At each forecast date, both arms receive every prior, outcome-closed event with a usable target and at least three common strict state fields. There is no same-class eligibility filter. A state observation is eligible only when its observation date, vintage, and release date do not exceed the event date and it is not retrospective (`src/structural_surface_experiment.py:161`). Holding support fixed isolates weighting from candidate selection.

## 3. Competing analogy rules

Surface distance is zero when two events share a class and one otherwise. Structural distance is the equal-block average of normalized field distances over fields jointly available to the pair. Both become weights through the same kernel, `exp(−d/0.25)`. The forecast is the weighted empirical distribution of prior abnormal returns.

The primary score is weighted CRPS. Each forecast is serialized and sealed by SHA-256 before its target is attached. Inference is paired by date: Diebold–Mariano with Newey–West variance and a stationary-bootstrap interval. Uniform weighting on identical support is a registered diagnostic separating useful similarity from pooling.

## 4. Primary result

There are 264 scored dates; 24 events have an unusable target and 25 lack the minimum pool of eight prior cases. Structural weighting scores 8.3366 and surface weighting 8.7824. Their paired difference is −0.4458, with interval [−0.6231, −0.2712] and *p*=1.57×10⁻⁶. Under the registered rule, structure beats surface.

The uniform diagnostic determines the interpretation. Pooling scores 8.3917. Structure is better by 0.0551 CRPS, but [−0.1152, +0.0057] crosses zero and *p*=0.0896. Surface is worse than uniform by 0.3906, [0.2158, 0.5720], *p*=3.31×10⁻⁵. Median effective sample size is 130.2 under structure and 28.7 under surface.

Thus structural comparison preserves information class matching throws away. The experiment does not establish that structural weighting extracts reliable 20-day signal beyond the historical pool itself.

Five- and ten-day outcomes were non-verdict diagnostics. At five days structure beats surface (−0.1767; *p*=0.0280) and uniform (−0.0687; *p*=0.0172). At ten days it beats surface (−0.1896; *p*=0.0456) but not uniform. They are not the headline.

## 5. What the audit changed

The earlier price walk forecast raw 20-day Brent returns (`src/engine/read.py:148`). That mixes event response with the ordinary market process. Target-only corrections give different answers in two legacy designs: the grid loss to climatology disappears, while the event-walk loss narrows but remains. This shows target construction matters and the designs are not interchangeable; neither replaces the direct experiment. The side-by-side record is `docs/ABNORMAL_RETURN_RESULT.md`.

The earlier event walk admitted only same-class candidates (`src/engine/read.py:208`) and built climatology from that conditioned pool (`src/walk.py:262` in the audited version). It tested within-class reranking, not structural versus surface analogy. The central experiment removes that filter and holds support fixed.

The original “knowable at *t*” conclusion was not an availability test. Situation fields without a dated URL inherited their 2026 coding date (`src/situation_vintage.py:279` in the audited version), so they failed mechanically. The defensible statement is that availability could not be demonstrated. In the rebuilt input, only 671 of 11,029 panel-derived rows satisfy observation/vintage/release/non-retrospective rules. At least one strict panel field is available for 227 events, with median six usable fields among them. This is a feasibility and metadata finding, not proof that analysts lacked the information.

Legacy escalation labels often used violence anywhere in the affected country rather than dyadic escalation (`src/state/ies90.py:385`), while persistence lagged that measure (`src/engine/persistence.py:45`). Those results do not answer whether the event parties escalated and are not evidence for the present claim.

## 6. Significance and limitations

The consequential result is the primary comparison together with its uniform control: surface class matching can make an analyst worse than retaining the eligible reference class. That argues against event type as an eligibility gate and for testing similarity systems against unrestricted pooling on identical support.

This is not a rescue of the original engine. Structure has not shown 20-day skill beyond pooling. The catalogue is curated, not a probability sample; coverage varies by era; strict state availability is sparse; missingness may encode time and source coverage; the equal-block metric and bandwidth are design choices; and abnormal returns do not remove every concurrent cause. Dependence-aware inference cannot repair catalogue selection or measurement error.

The next serious analysis is prospective collection of time-stamped states and forecasts under this frozen protocol. Until then, the honest headline remains comparative: structure beats surface matching, while pooling remains competitive.

## 7. Reproduction

Run `make reproduce-central`. It uses the committed input bundle, rebuilds central outputs in isolation, and verifies byte-for-byte hashes against `data/structural_surface/manifest.json`. The scientific artifacts are `reads.jsonl`, `scores.jsonl`, and `summary.json`. Tests enforce filtration, equal support, seal-before-outcome order, scoring, and deterministic reproduction.

The six-week system and retractions remain in repository history and the audit record, but are not additional validated findings. Tag `closure-core-frozen-2026-09-03` is the pre-closure recovery point.
