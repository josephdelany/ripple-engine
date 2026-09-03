# Stage 0: the kill-test — **MAGNITUDE IS BELIEF, NOT BARRELS**

*2026-09-03, Session C. `MAGNITUDE_REGISTRATION.md` §3, sealed at `8cb9d3d`, with the decision rule's
`">>"` quantified and committed at `de70b04` **before** the estimator was run and with no result file
in the tree. Computed by `src/magnitude_stage0.py`, which imports its estimator from
`src/ripple_lp.py` and its frames from `src/ripple_physical.py`. Numbers:
`data/magnitude/stage0.json`.*

## The answer

Of the three outcomes §3 registered in advance, the rule returns the **middle** one — not the one I
predicted.

> **MAGNITUDE IS BELIEF, NOT BARRELS.** Build M-B only, and only as the §2.1 comparator.
> *(§12 outcome 3.)*

The study is **not** killed and it is **not** cleared to proceed as briefed. It is narrowed to the
one thing it can honestly do.

## The shared subsample, which is Stage 0's entire contribution

**44 days** are both a corpus `opec_decision` event (52 day-precision) and a Känzig announcement day
(169). On those same days, four regressors differ only in what they say:

| | A dummy | B magnitude | C both | D severity ordinal |
|---|---|---|---|---|
| regressor | 1 | Känzig surprise | 1 *and* surprise | corpus severity 1–5 |

v2 §4.1 already published Känzig +1.727 against the OPEC dummy −3.159 at h = 5 on Brent, but on
**different samples** (128 announcement days versus 47 de-overlapped corpus events), so that
comparison confounded the regressor with the sample. This one does not.

## Price — magnitude wins, exactly as registered

Brent, headline h = 5, n = 35 in the estimation sample.

| spec | β [95%] | \|z\| | band excludes zero |
|---|---|---|---|
| **A** dummy | −1.572 [−5.423, +2.279] | 0.80 | no |
| **B** magnitude | **+2.230 [+0.809, +3.651]** | **3.08** | **yes** |
| **C** dummy, with magnitude present | −0.483 [−3.056, +2.090] | 0.37 | **no** |
| **C** magnitude, with dummy present | **+2.208 [+0.866, +3.549]** | **3.23** | **yes** |
| **D** severity ordinal | −0.996 [−2.638, +0.646] | 1.19 | no |

Both registered conditions hold. **B beats A** (B's band excludes zero, A's does not), and in **spec
C the dummy collapses to −0.48 with a band covering zero while the magnitude is untouched.** On the
same 44 days, the 0/1 indicator carries no information the continuous surprise does not already have.

**And the free ordinal baseline fails too.** §5 registered `events.severity` as the zero-cost
comparator, "because a magnitude series that cannot beat an ordinal severity code is not worth
building". Severity does not beat the dummy, let alone the surprise. A 1–5 analyst code is not a
substitute for a measured surprise — which also disposes of the cheapest possible route to Stage 1.

## Quantity — magnitude does nothing, and the dummy's one hit is a timing artefact

JODI balanced-aggregate production, 10 continuous reporters, headline **h = 0** (the horizon
`RIPPLE_PHYSICAL.md` §2.3 showed quantity responses actually live at), n = 35 months.

| spec | β [95%] | \|z\| | band excludes zero |
|---|---|---|---|
| **A** dummy | **+0.881 [+0.151, +1.611]** | 2.37 | **yes** |
| **B** magnitude | +0.073 [−0.093, +0.238] | 0.86 | no |
| **C** dummy, with magnitude present | +0.936 [+0.224, +1.649] | 2.58 | yes |
| **C** magnitude, with dummy present | +0.102 [−0.040, +0.245] | 1.41 | no |
| **D** severity ordinal | +0.238 [−0.010, +0.485] | 1.88 | no |

**B does not beat A. It is beaten by A.** That is the whole reason the verdict is outcome 3 rather
than outcome 1.

### The dummy's hit does not survive scrutiny, and I looked because it is a positive result

This is the one band excluding zero on a physical quantity in the entire Stage 0 table, and it
belongs to the *indicator*, not the measured shock. It even clears the registered state-matched
placebo (99.2nd percentile). It is still not a response, for three reasons found by looking:

1. **It exists at h = 0 and nowhere else.** h = 1: +0.561 [−0.401, +1.523]. h = 2 onward: all
   negative and all covering zero. A one-period contemporaneous blip, not a path.
2. **Production is already falling into the announcement.**

   | | mean Δlog production |
   |---|---|
   | into the month *before* the announcement | **−0.549%** |
   | into the announcement month | **+0.674%** |
   | all 293 months | +0.065% |

   The h = 0 coefficient is the **rebound leg of a V centred on the announcement**. OPEC meets at the
   trough. This is the quantity analogue of v2 §4.3, where Brent is already +1.663% in the week
   *before* an OPEC decision and the class is flagged ANTICIPATED-IN-PRICE.
3. **At monthly resolution the announcement and the production month are the same month**, so the
   ordering within it is not identified. Känzig's entire design exists because OPEC decisions respond
   to market conditions.

**And the magnitude shows none of it.** That is the tell. If the dummy marked *what OPEC decided*, the
surprise would carry it too. The dummy marks *when OPEC meets* — a timing feature correlated with
production conditions — and the surprise carries the news content. The dummy's apparent advantage on
quantity is the artefact; the magnitude's silence is the honest reading.

## What this does and does not license

**Licensed** (§12 outcome 3): build **M-B**, the belief magnitude, and use it *only* against physical
outcomes, where §2.1 registered it as answering a real question — *did the market's revision of belief
predict the barrels?* Red Sea 2024 is the registered case where the answer should be no.

**Not licensed:** building M-Q — quantity magnitudes for sanctions, chokepoint disruptions or
interstate escalation — on the strength of Stage 0. The evidence for magnitude is entirely on the
price side, and the price side is where M-B is **circular by construction** (§2.1). Stage 0 has
demonstrated that a magnitude-bearing regressor beats a dummy *at predicting a price*, which is close
to demonstrating that a price surprise predicts prices.

**What Stage 0 did not settle: R2.** §13 warned of exactly this. Stage 0 runs on `opec_decision` — the
class *least* affected by R2, correlating r = 0.431 with |Känzig|, while the tightening classes
correlate **r = −0.023** with the identified supply shock over 614 months. A pass here does **not**
license assuming our sanctions, chokepoint and conflict events are supply shocks at all. The
near-orthogonality stands untouched, and "a magnitude attached to a non-shock is still a non-shock"
remains the live risk.

## Expectations, scored in the registered vocabulary

| | registered in advance | result |
|---|---|---|
| **E-1** | Stage 0 returns "magnitude is the binding constraint" on Brent; Känzig beats the dummy on the shared subsample and the dummy carries no residual information in spec C | **PARTLY CONSISTENT.** Every price sub-claim holds exactly. The overall verdict does not, because the production arm failed. |
| **E-2** | Stage 0 is INDETERMINATE on production; the OPEC magnitude should not move JODI production even at h = 0, because announcements are anticipated (R3) and offset (R4) | **CONSISTENT** — and the reason given in advance is supported: the anticipation diagnostic finds production falling into the month before the announcement. |

## What happens next

Not Stage 1 as briefed. The narrowed programme:

1. **M-B is buildable and is worth building** — but as the §2.1 comparator only, tested against
   physical outcomes, never against a price.
2. **M-Q for the non-OPEC classes remains unjustified by evidence.** Stage 0 was the cheap way to find
   that out and it found it out.
3. **R2 is now the binding question**, not magnitude. Whether our tightening events are supply shocks
   at all is prior to how heavily to weight them, and it needs its own registration.

## Provenance

Run 2026-09-03, seed 19900802. Rule sealed `de70b04` before the run; registration sealed `8cb9d3d`.
Every number above is in `data/magnitude/stage0.json`: `intersection`, `price.specs`, `quantity.specs`,
`decision`, `quantity_dummy_scrutiny`, `expectations`. Tests: `tests/test_magnitude_stage0.py`.
The anticipation diagnostic and the expectation scoring were **added after** the rule returned its
answer and are labelled as such in the code; neither feeds the decision rule, which is computed from
the headline coefficients alone.
