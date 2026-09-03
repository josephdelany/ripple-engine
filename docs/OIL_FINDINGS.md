# What this project found about oil

*2026-09-03. The market findings, separated from the forecasting result. Every figure traced to a
named file.*

> **Evidence grade, stated first, because "finding" is doing too much work otherwise.** Each result
> below is tagged:
>
> - **[TESTED]** — a hypothesis test with an interval, surviving multiple-testing correction where
>   a family exists.
> - **[DESCRIPTIVE]** — a measured count or rate with no significance test. Real, checkable, and
>   *not* an established effect.
> - **[NULL]** — a test run and not rejected.
> - **[CASE]** — a comparison of two or three episodes. Illustrative, not inferential.
>
> A reader with an econometrics background will ask which is which within a minute. Do not present
> a DESCRIPTIVE result as though it were TESTED.

---

## 1. [TESTED] At one month, light ends rise with crude and do not fall with it

The strongest result in the project, and it had gone unreported. **Corrected for multiplicity across
the 17-test family by Benjamini–Hochberg**; only the results below survive at *q* < 0.05.

**At one month (h = 20), light ends rise with crude and do not fall with it.**

| product | β to crude **up** | β to crude **down** | W | *p* | **BH *q*** |
|---|---:|---:|---:|---:|---:|
| **propane** | **+1.050** | **−0.015** | +1.065 | <0.0001 | **<0.0001 ✓** |
| gasoline, Gulf | +1.258 | +0.173 | +1.085 | 0.0011 | **0.0094 ✓** |
| gasoline, NYH | +1.136 | +0.215 | +0.921 | 0.0047 | **0.0266 ✓** |
| propane (h = 10) | +0.700 | +0.279 | +0.420 | 0.0220 | 0.0935 ✗ |

**Propane tracks crude up roughly one-for-one and is statistically flat on the way down.** This is
the classic "rockets and feathers" pattern, measured here on spot rather than retail, and strongly
significant across three light-end products.

**At one week the point estimates reverse for middle distillates — but this DOES NOT survive
correction and must not be presented as a finding.**

| product | β up | β down | W | *p* | **BH *q*** |
|---|---:|---:|---:|---:|---:|
| jet, Gulf | +0.493 | +0.769 | −0.276 | 0.0342 | **0.1150 ✗** |
| heating oil, NYH | +0.442 | +0.718 | −0.277 | 0.0406 | **0.1150 ✗** |

> **Correction of record.** An earlier version of this document reported the asymmetry as
> "reversing by horizon and product class" and presented these two rows as a finding. Across the
> 17-test family the reversal does **not** survive Benjamini–Hochberg (*q* = 0.115 for both).
> Uncorrected, seven of 17 tests clear *p* < 0.10, which is roughly what testing 17 things produces.
> **The defensible claim is the one-month light-end asymmetry only.** The one-week reversal is
> suggestive and unestablished, and is retained here as a hypothesis rather than a result.

**Why it matters.** Anyone hedging a product exposure with crude is carrying an asymmetry that
changes sign depending on which product and which horizon. A propane position hedged with crude at
a one-month horizon is protected on the way up and unhedged on the way down.

*Registered caveat, carried from the source file: this is a slope-based symmetry test, and per
Kilian & Vigfusson (2011) such tests are informative about slopes rather than about the shape of the
underlying nonlinear response. Both signs enter together; nothing is censored.*
`data/ripple/passthrough.json`

---

## 2. [DESCRIPTIVE] Roughly a third of the largest moves have no identifiable cause

| asset | episodes | with **no** identifiable corpus event |
|---|---:|---:|
| Brent | 44 | **14 (32%)** |
| WTI | 48 | **14 (29%)** |
| diesel crack | 37 | **8 (22%)** |

Taking the market's largest moves rather than our chosen events — so this inverts the usual event
study and is immune to corpus selection. **The diesel crack is the most explicable of the three**,
which is consistent with §4 below.
`data/big_moves/{brent,wti,diesel_crack}.json`

---

## 3. [DESCRIPTIVE] The market prices a geopolitical event about a month before the "event"

| asset | median lag | 75th pct | max | episodes where **every** attributed event was already public | **any** |
|---|---:|---:|---:|---:|---:|
| Brent | **31 days** | 54 | 85 | 15 of 30 (**50%**) | 22 of 30 (73%) |
| WTI | **35 days** | 59 | 90 | 13 of 34 (38%) | 20 of 34 (59%) |
| diesel crack | **34 days** | 57 | 85 | 9 of 29 (31%) | **25 of 29 (86%)** |

**The event date is not when the market moves.** In half of the attributed Brent episodes, *every*
attributed event was already public more than 20 trading days before the move began. Any study that
dates a shock to the event and measures a window around it is measuring a response the market had
largely already made.
`data/big_moves/*.json` · `events[].lag_days`, `events[].anticipated`

---

## 4. [DESCRIPTIVE — testable, not yet tested] Geopolitical shocks land in refining margins, not crude

Share of events in each class coinciding with a top-5% move in that asset:

| event class | big **crude** move | big **diesel-crack** move | ratio |
|---|---:|---:|---:|
| chokepoint disruption | 4/26 (15%) | **10/26 (38%)** | **2.5×** |
| infrastructure attack | 6/44 (14%) | **15/45 (33%)** | **2.4×** |
| sanctions | 8/55 (15%) | **19/55 (35%)** | **2.4×** |
| conflict escalation | 12/50 (24%) | **23/50 (46%)** | **1.9×** |
| OPEC decision | 17/51 (31%) | 13/51 (25%) | 0.8× |
| demand shock | 6/17 (35%) | 5/17 (29%) | 0.8× |

**Every military and geopolitical class concentrates in the crack; the market and policy classes
invert.** A crude-only view of geopolitical risk is watching the wrong instrument.

**What this is not, yet.** These are frequencies, not a test. Because the denominators match per
class, these are *the same events scored against two assets* — paired binary data, for which
McNemar's test on the discordant pairs is the correct instrument. That requires the event-level
table rather than these margins and **has not been run**. Until it is, this is a striking rate
difference and not an established effect. (One inconsistency to resolve when it is run:
`infrastructure_attack` shows 44 against crude and 45 against the crack.)
`data/big_moves/summary.json` · `p_big_given_class`

---

## 5. [CASE, n = 2] A chokepoint closure is a price event only if the ships cannot go around

| | flow | reroute | Brent |
|---|---:|---:|---:|
| **Red Sea 2024** (Bab el-Mandeb) | **−56.6%** | Cape of Good Hope **+101.8%** | **−4.9%** |
| **Hormuz 2026** | **−92.3%** | **+20.7%** | **+48.5%** |

There is no reroute out of the Gulf. **A reroutable closure is a freight event; an unreroutable one
is a price event** — and a price-only study looks at the Red Sea and concludes nothing happened.
`data/ripple/physical.json` · `docs/RIPPLE_PHYSICAL.md` §4

---

## 6. [TESTED] Event-occurrence flags carry no information about the size of a response

On the **44 days that are both a corpus OPEC event and a Känzig (2021) announcement** — same days,
four regressors differing only in what they say about those days:

| regressor, Brent h = 5 | β | band |
|---|---:|---|
| the 0/1 event flag | −1.572 | [−5.423, +2.279] — **covers zero** |
| a continuous measure of the same events | **+2.230** | [+0.809, +3.651] — **excludes zero** |
| both together | flag **−0.483** | magnitude holds +2.208 |
| our own hand-coded severity ordinal | −0.996 | covers zero |

Two OPEC announcements both get a "1" whether one repriced the curve or was fully anticipated. **The
flag discards the only thing that varies**, and this applies to any product built on dated event
dummies.
`data/ripple/stage0.json` · paper §12.3

---

## 7. [TESTED — as a bound, not an effect] "Geopolitical oil risk" classes are near-orthogonal to identified supply shocks

The tightening classes — sanctions, chokepoint disruption, conflict escalation — correlate
**r = −0.023** with the identified oil-supply shock over **614 months**.

**Stated precisely, because "no relationship" overclaims.** The Fisher-*z* 95% interval is
**[−0.102, +0.056]**, which contains zero — so no relationship is *established*. What the sample
size does buy is a **bound**: it rules out any correlation with |r| greater than about **0.10**,
i.e. more than **1% shared variance**. That is the useful form of the claim — not "they are
unrelated" but "any relationship is smaller than 1% of variance." The prior question is therefore
not how heavily to weight these events but **whether they are supply shocks at all**.
`MAGNITUDE_REGISTRATION.md` §13.1

---

## 8. [TESTED] Real supply shocks do move real quantities — the instrument works

Run through this project's own estimator: Känzig's oil-supply news shock moves Brent **+0.851
(SE 0.103) at h = 0, rising to +2.37 at h = 20**, every horizon excluding zero. The
Baumeister–Hamilton identified supply shock moves JODI physical production **+0.760 [+0.496,
+1.023]**.

**Events move oil.** The failures above are about *encoding and measurement*, not about causation.
`data/ripple/external_checks.json`

---

## 9. [NULL] The chain does not transmit the way the industry narrative assumes

Across **477 node×shock cells** spanning crude → refined products → cracks → gas/LNG → fertilizer →
freight → credit, **21 transmit against 1–24 expected under no transmission at all.** The observed
count sits inside its own null interval. Transmitting cells cluster at the two *ends* — crude itself
and the equity/macro nodes beside the chain — and vanish along it.
`data/ripple/irf.json` · paper §12

---

## 10. [DESCRIPTIVE] The physical record goes dark exactly where it matters most

JODI reporting ends: **Iran 2018-07** — the month US secondary sanctions were reimposed — **UAE and
Qatar 2018-12, Russia 2023-03, Iraq 2024-03.** Of 122 de-overlapped events naming a producer,
**21 fall after that producer stopped reporting.** The missingness is caused by the treatment, and
no weighting fixes it.
`docs/RIPPLE_PHYSICAL.md` §1

---

## How these fit together

Findings 2, 3 and 6 say the same thing from three directions: **the event, as normally dated and
encoded, is not the thing that moves the market.** A third of big moves have no event; half of the
attributed ones were priced a month early; and the flag that marks an event carries no magnitude.

Findings 4 and 5 say where the response actually lands: **in refining margins rather than crude, and
in freight rather than price when the disruption is reroutable.**

Findings 7 and 10 say why this is hard to fix: the event classes are near-orthogonal to identified
supply shocks, and the physical record goes dark precisely for the producers under sanction.

Finding 8 is the control that keeps all of it honest — **the estimator recovers real shocks
cleanly**, so the nulls are about the events and the encoding, not about the machinery.

And finding 1 stands apart: an asymmetry in crude-to-product pass-through that reverses between
light ends and middle distillates, and between one week and one month.
