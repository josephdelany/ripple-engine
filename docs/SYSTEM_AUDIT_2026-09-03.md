> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** A working analysis or evidence record from the legacy engine. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../SUBMISSION_STATUS.md).

# System audit — full repository

*2026-09-03. Scope: 54,667 lines of source across `src/`, the walk-forward core, the retrieval and
scoring implementations, baseline construction, corpus admission, the outcome mapping, the test
suite (915 test functions, 2,689 assertions), and every published data artefact. Line references
are to the committed code.*

**The two most serious findings are in the core design and neither had been examined before. They
determine the headline result independently of anything about historical analogy.**

---

## TIER 1 — Design defects that determine the result

### A1. The price target is a raw return with no market model. The price null follows from this alone.

`src/engine/read.py:148–177`. `path()` returns `(seg / seg[0] - 1) * 100` — the percentage change in
Brent from the event date forward. `outcome()` takes `pct[h]`, the raw return at exactly +20 trading
days. **There is no market model, no expected-return subtraction, no detrending, no risk
adjustment.** A grep for `abnormal`, `market_model`, `expected_return` or `CAR` across the walk
returns nothing.

**Why this is fatal to the price arm.** The entire event-study literature works in *abnormal*
returns — actual minus expected — precisely because raw returns are dominated by the market-wide
process. A 20-day Brent return is mostly the oil market, and the oil market is close to a random
walk. The event's contribution is a small share of that variance.

**So the engine is being asked to forecast the oil market, not the event's effect.** Climatology —
the pool of prior same-class raw returns — is approximately the unconditional distribution of 20-day
oil returns. Beating it requires forecasting oil. **Nothing does that, and the null is essentially
guaranteed by the target definition.**

This is not a limitation to be disclosed. It means **the price result does not test what the paper
says it tests.**

### A2. The candidate pool is filtered to the same event class — so "worse than climatology" means something far narrower than claimed

`src/engine/read.py:208`: `if e["type"] != target["type"] ... continue`.

Every candidate is the **same class** as the target. Climatology (`walk.py:262`) is then computed
from that same pool. So:

- the engine gets class conditioning **for free**
- climatology gets it **too**
- the only thing under test is whether the **state vector** adds anything *beyond class membership*

**Measured scale of what remains.** `k` = 8. Median G pool = **18**. The engine therefore uses
**44%** of the available pool at the median, and **26% of reads have a pool at or below k — for
those, no selection occurs at all.** Add that **84% of events have no situation field knowable at
*t*** (60 kept of 786), and for most reads the "state" being compared is the market block plus
entities.

**The honest statement of the headline is therefore:** *reranking within an event class, mostly on
market state, does not beat pooling within that same class.* That is a real result. It is not
"formalised historical analogy contains no out-of-sample predictive information," which is what the
abstract claims.

### A3. The escalation target is 83% a country-violence indicator, not a dyadic escalation measure

`src/state/ies90.py:385–420`, `score_ged()`, rule `GED.location.ge250`. A level may be assigned from
a **location** death count — violence anywhere in the affected country within the 90-day window —
when no dyadic record covers. Amendment 2's "dyadic beats location" only applies when a dyadic
record *exists*.

**Measured across the 132 labelled events (`event_outcomes.basis`):**

| basis | level 0 | 1 | 2 | 3 | total |
|---|---:|---:|---:|---:|---:|
| **dyadic** | 11 | 3 | 5 | 4 | **23** |
| **location** | 62 | 6 | 25 | 16 | **109** |

**83% of all labels, and 47 of the 59 non-zero labels, are location-based.** The entire non-zero
signal of the escalation target rests on **12 dyadically-grounded events**.

**Consequence, and it explains the whole escalation arm.** The target is not *"did the event's two
parties escalate against each other"* — it is largely *"was there violence in the affected country
in the next 90 days."* Country violence is enormously autocorrelated, which is why a persistence
rule beats the engine: persistence is not out-forecasting analogy, **it is exploiting the fact that
the target is a country fixed effect.** This also mechanically explains OPEN_ITEMS 1.1 ("the target
is substantially a persistence variable"), and it shows that the ICB/GED location artefact session G
found in the grid panel **is present in the main corpus too, and dominates it.**

**The paper describes IES-90 as an escalation measure for the event's dyad. In operation it is not.**

---

## TIER 2 — Published claims that do not survive

### B1. The anticipation finding is mostly definitional
`big_moves.py:92` sets `onset` to the **price extreme, chosen ex post**; line 185 flags
`anticipated` when an event falls >20 days after it. Median episode = **76 days**; **100% exceed 20
days**. A uniform within-episode null yields **55% anticipated by construction** against **69%**
observed. Excess ≈2.5σ unclustered. **Withdraw as published; restate as a modest excess, or test it
properly (R8).**

### B2. Red Sea / Hormuz has no control and the pre-trend runs against it
Brent fell **−14.8% in Q4 2023 before the attacks**, then **rose +9.5% across the attack window**.
The published −4.9% is a windowing choice, at *n* = 2, with no detrending. **Demote to illustration
with the pre-trend in the same sentence.**

### B3. Pass-through asymmetry is a replication presented as a discovery
Bacon (1991); Borenstein, Cameron & Gilbert (1997, *QJE*); a large subsequent literature.
**Reposition as replication on spot rather than retail.**

### B4. The model family lacks diversity, which weakens Hedge, SPA and the Reality Check

`data/walk_forward/menu.json`. Of twelve similarity items: **M02, M04 and M10 weight the `situation`
block, which is empty for 84% of events** — they are substantially inert. M01/M06/M07 differ only in
*k* (8, 5, 12). M08/M09 differ only in the retrieval threshold (0.30, 0.50).

**Consequence.** Hedge over near-redundant experts converges to uniform — the sampled sealed read
shows all thirteen weights at exactly 0.076923 = 1/13. SPA and White's Reality Check across a family
of near-identical models have little power to detect a winner. And "fitting does not beat frozen"
(+0.0013, *p* = 0.820 in the grid study) is partly a statement about a family with little to choose
between.

### B5. Vintage is enforced on the situation block but `as_of` equals the observation date elsewhere

In `observations`, `as_of` equals `obs_date` for the revision-prone EIA series (stocks, refinery
utilisation). **EIA weekly inventories are first published several days after the week they
describe and are subsequently revised.** Stamping the observation date as the knowable date assumes
the value was available on the day it describes.

`inv_sigma` — in `MARKET_SERIES`, and one of only three fields in the "physical" block — derives
from those stocks. **So the block the paper leans on after Amendment H emptied the situation block
carries a mild look-ahead of its own.** Smaller than A1–A3, but it undercuts the claim that the
market block is the clean one.

---

## TIER 3 — Structural limits on interpretation

| # | finding | evidence |
|---|---|---|
| **C1** | State vector is macro-financial, not fundamental — no days-of-cover, supply growth, demand growth, floating storage. The "physical" block is 3 price-derived fields. | `grid/price/summary.json` `registered.blocks`; 772 series available |
| **C2** | Reference class spans incommensurable regimes: 8 events pre-1983 (no crude futures), 78 pre-2010 (pre-shale), **150 of 313 in the 2020s** | `oil.db` `events` |
| **C3** | Escalation (IES-90) is a political-science target, not the economic question, yet carries most of the apparatus | paper §§5, 8, 11 |
| **C4** | `policy_response` is a 57-event heterogeneous class — the second largest | `oil.db` `events` |
| **C5** | Only 4 of 7 classes are G-scorable (`similarity.py:46`), so escalation results describe a subset without saying so prominently | `GEO_TYPES` |
| **C6** | 106 skip/xfail markers across the suite | `tests/` |

---

## What is genuinely strong — and this is not consolation

- **The scoring implementations are correct.** CRPS is the proper `E|X−y| − ½E|X−X′|` with a sound
  O(n log n) formulation; Brier is the multi-category form; RPS follows Epstein (1969);
  `skill = 1 − engine/ref` is the standard skill score. I checked these first because an error here
  would invalidate every number in the project. There is none.
- **The test suite is real.** 915 test functions, 2,689 assertions, and **zero tests without an
  assertion**. That is better discipline than most production codebases.
- **The filtration is honest.** Baselines draw from the *same* filtration-constrained pool as the
  engine (`walk.py:255–296`); the random-analog baseline is not advantaged. The leakage test
  deliberately breaks the filtration and demonstrates the scores move.
- **Sourced-or-unknown is enforced in code**, not just asserted — `_outcome()` returns
  `no_independent_outcome` rather than guessing a level.
- **The vintage finding stands.** 262 of 313 with no knowable state. I attacked it and could not
  move it.
- **The 44-day flags-versus-magnitude design is clean.** Same days, same events, one regressor
  changes.
- **Reproducibility to a content digest, four self-retractions, three audits.** Unusual and real.

---

## Remediation plan, reordered by what actually matters

| # | action | why | cost |
|---|---|---|---|
| **R0a** | **Restate the escalation target.** It is 83% location-based; the non-zero signal rests on 12 dyadic events. Say so in the abstract and §5, and reframe the persistence result as a consequence of it. | A3 — the escalation arm measures something other than what it claims | 1.5 h |
| **R0** | **Restate the price result.** It tests forecasting of *raw* 20-day returns, not event effects. Either say so plainly in the abstract and §8, or re-run against an abnormal-return target with a pre-event estimation window. | A1 — the largest single defect | 1 h to restate · 3–4 h to re-run |
| **R1** | **Restate the escalation headline** as *within-class reranking vs within-class pooling*, with k=8, median pool 18, 26% no-selection, 84% no-state, all stated at the top of §8. | A2 — the abstract currently overclaims scope | 1.5 h |
| **R2** | Withdraw B1 and B2; reposition B3 as replication. Corrections of record. | published claims that fail | 1 h |
| **R3** | State C1 and C2 in limitations with their counts. | pre-empts the two obvious attacks | 45 m |
| **R4** | Reorder all findings surfaces by what survives. | currently ranked backwards | 45 m |
| **R5** | Cite Bacon 1991, Borenstein–Cameron–Gilbert 1997; search the event-study anticipation literature. | literature gaps | 45 m |
| **R6** | Clustered permutation of B1 against the uniform-within-episode null. | decides whether B1 returns | 1–2 h |
| **R7** | The 30-row label audit. | the only human validation gate | 3 h |

**R0 and R1 are the whole game.** They are not cosmetic: they change what the paper claims to have
tested from something the design could not test into something it did. Everything else is
housekeeping by comparison.

**The defensible restatement, after R0 and R1:**

> Within-class reranking on a mostly macro-financial state vector does not beat within-class pooling
> for escalation, and does not beat the unconditional distribution of raw 20-day returns for price.
> The structural version could not be tested: 84% of events carry no knowable structural state, 26%
> of reads admit no selection, and the physical layer is 6% recoverable from public sources.

Narrower than the current abstract by a wide margin, and unlike the current abstract, it is what the
evidence supports.
