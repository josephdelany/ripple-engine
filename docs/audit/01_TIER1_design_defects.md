# Tier 1 — Design defects that determine the result

*These three are not limitations to disclose. Each one makes a headline result follow from the
design rather than from the phenomenon under study.*

---

## A1 — The price target is a raw return with no market model

**Where.** `src/engine/read.py:148–177`. `path()` returns `(seg / seg[0] - 1) * 100`; `outcome()`
takes `pct[h]` at exactly +20 trading days.

**What is missing.** No market model, no expected-return subtraction, no detrending, no risk
adjustment. A grep across the walk for `abnormal`, `market_model`, `expected_return`, `CAR` returns
nothing.

**Why it is fatal.** Event studies work in *abnormal* returns — realised minus expected — because
raw returns are dominated by the market-wide process. A 20-day Brent return is mostly the oil
market, which is close to a random walk. The event's contribution is a small share of that variance.

**Consequence.** The engine is being asked to forecast **the oil market**, not the event's effect.
Climatology — the pool of prior same-class raw returns — is approximately the unconditional
distribution of 20-day oil returns. Beating it requires forecasting oil. Nothing does that.

> **The price null follows from the target definition, before analogy enters the picture. The price
> result does not test what the paper says it tests.**

**Fix.** Either (a) state this plainly in the abstract and §8, or (b) re-run against an
abnormal-return target: estimate an expected-return model on a pre-event window and score the
residual. (b) makes the price arm a real test. Cost: 1 h to restate, 3–4 h to re-run.

---

## A2 — The candidate pool is class-filtered, so "worse than climatology" means something far narrower

**Where.** `src/engine/read.py:208` — `if e["type"] != target["type"] ... continue`. Climatology is
then computed from that same pool at `src/walk.py:262`.

**What this means.** Every candidate is the same event class as the target. The engine gets class
conditioning **for free**; so does climatology. The only thing under test is whether the **state
vector** adds anything *beyond class membership*.

**Measured scale of what remains:**

| quantity | value | source |
|---|---:|---|
| `k` retrieved | **8** | `menu.json` |
| median G pool (same class, prior, closed) | **18** | `reads.jsonl` |
| engine's share of the available pool at the median | **44%** | computed |
| reads where pool ≤ k — **no selection possible at all** | **26%** | computed |
| events with no situation field knowable at *t* | **262 of 313 (84%)** | `situation_knowable.json` |

**Consequence.** For a quarter of reads the similarity metric is inert by construction — "the eight
most similar events" is simply "all the events." For 84% of reads there is no structural state to
compute similarity on. What is actually tested is **reranking within a class, mostly on market
state, against pooling within that same class.**

> **The abstract claims a test of "formalised historical analogy." The design tests within-class
> reranking on a market state vector.**

**Fix.** Restate the headline with the four numbers above at the top of §8. Cost: 1.5 h.

---

## A3 — The escalation target is 83% a country-violence indicator, not a dyadic escalation measure

**Where.** `src/state/ies90.py:385–420`, `score_ged()`, rule `GED.location.ge250`. A level is
assigned from a **location** death count — violence anywhere in the affected country in the 90-day
window — whenever no dyadic record covers. "Dyadic beats location" applies only when a dyadic record
*exists*.

**Measured across the 132 labelled events** (`event_outcomes.basis`):

| basis | level 0 | 1 | 2 | 3 | total |
|---|---:|---:|---:|---:|---:|
| **dyadic** | 11 | 3 | 5 | 4 | **23** |
| **location** | 62 | 6 | 25 | 16 | **109** |

**83% of labels are location-based. Of the 59 non-zero labels — the entire signal — 47 are
location-based and only 12 are dyadically grounded.**

**Consequence, and it explains the whole escalation arm.** The target is not *"did the event's two
parties escalate against each other."* It is largely *"was there violence in the affected country in
the next 90 days."*

**The persistence corollary.** `src/engine/persistence.py:45–55` computes the baseline by calling
**the same `score_event`** on the window [t−90, t−1]. So persistence is *the same location-based
variable, lagged*. Country violence is heavily autocorrelated.

> **Persistence is not out-forecasting historical analogy. It is an AR(1) on country violence,
> competing against a retrieval engine on a target that is largely a country fixed effect.**

This mechanically explains `OPEN_ITEMS` 1.1, and it shows that the ICB/GED location artefact session
G identified in the grid panel is **present in the main corpus and dominates it**.

**Fix.** Restate the escalation target in the abstract and §5, reframe the persistence result as a
consequence, and report the dyadic-basis subset (n = 23, 12 non-zero) as the only part of the target
that measures what the paper describes. Cost: 1.5 h.
