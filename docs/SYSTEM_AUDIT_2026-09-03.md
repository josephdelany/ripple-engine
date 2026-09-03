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
