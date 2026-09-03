# The intended system, the built system, and the gap between them

*2026-09-03. Written because the two are not the same, and the difference is the most useful thing
this project has to say. Every layer below is checked against the code rather than described from
memory.*

---

## 1. The intended system

The design goal was a **learning instrument over the petro-product complex**, working forward
through history:

1. Start early in the record. Take an event, and the **environment surrounding it** — the
   conflict, the alliances and treaty obligations, the physical state of supply, the market state.
2. Observe the **response**: not just crude, but the whole chain — Brent and WTI, refined products,
   cracks, LNG, fertilizer, plastics, freight.
3. Learn the conditional: *under conditions x, y, z, this is what followed.*
4. Move forward to the next event. Read its environment. Say: *last time a, b and c held, this
   happened — but the environment now differs in these ways, so the expectation shifts thus.*
5. Observe what actually happened. **Readjust the weights and the focus.** Continue.
6. Repeat to the present, so the instrument is trained and refined by the whole record.
7. Use crude and Brent as **drivers** of the rest of the chain, learning the propagation.
8. At read time, combine the trained engine with **live circumstantial input**. If Ras Tanura were
   struck today: assess the physical damage, place it in context (an Iran conflict, these
   alliances, this treaty), consult what happened historically when refining capacity was struck,
   weight by how central that facility is to production, and produce a distribution over what
   follows.

That is a coherent design. The rest of this document establishes which of its layers exist.

---

## 2. What was built, layer by layer

| layer the vision needs | built? | what exists, exactly |
|---|---|---|
| **Historical event corpus with dates** | **yes** | 313 dated events, 1956–2026, human-gated under a codebook |
| **Forward-in-time sequential learning** | **yes** | walk-forward protocol: at each date the engine sees only what precedes it, forecasts, is sealed by hash, then scored. This is literally steps 4–6 |
| **Weight readjustment as it goes** | **yes** | Hedge online mixture (η = 0.25) over 13 registered menu items, re-weighted at every closed read |
| **Retrieval of similar prior situations** | **yes** | state-conditioned analog engine with a registered similarity metric and *k* = 12 |
| **Multi-product response, not just crude** | **yes** | 772 price/macro series; the propagation study spans **53 nodes** across crude → refined products → cracks → gas/LNG → fertilizer → freight → credit; the grid study scores six targets (Brent, WTI, diesel crack, gasoline crack, Henry Hub, propane) |
| **Crude as a driver of the rest of the chain** | **yes** | the propagation study is exactly this: local projections of each downstream node on the shock, hop by hop |
| **Alliances and treaty obligations** | **partial** | ATOP 5.1 as two binary dyad-year flags — `atop_defense_pact`, `atop_any_obligation` — **ending 2018.** A flag that an obligation exists, not a model of whether it is honoured |
| **Conflict history of the pair** | **yes** | `mid_count_10y` (to 2015), `icb_crisis_count` (to 2021) |
| **Market state** | **yes** | Brent 20-day vol, VIX percentile, COT percentile, OVX percentile |
| **Macro state** | **yes** | 2s10s curve, real rate, USD, credit stress |
| **Physical state** | **thin** | inventory sigma, diesel crack, Brent–WTI spread. **Three aggregate market-derived proxies** |
| **Facility-level capacity and criticality** | **NO** | nothing. No refinery, terminal or field register; no throughput; no "how central is Ras Tanura" |
| **Damage severity as a physical quantity** | **NO** | `severity` is an unsourced analyst ordinal, and Amendment C-1 now bars it from serving as a magnitude at all |
| **Outage duration** | **NO** | no outage register, no duration model, no historical shutdown lengths |
| **Barrels at risk** | **NO** | the magnitude study's Stage 0 verdict is literally *magnitude is belief, not barrels* — it could not construct a barrels measure for any non-OPEC class |

**The environment vector, in total, is 13 macro-financial fields and 4 dyad-level conflict/treaty
flags.** That is what "conditions x, y, z" resolves to in the built system.

---

## 3. What was therefore tested, and what was not

**Tested, rigorously, and it failed:** a **macro-conditioned** analog forecaster. It asks *was
volatility elevated, was the curve steep, was positioning stretched, had this pair fought
recently, is there a defence pact* — and retrieves prior events with similar answers.

**Never tested:** a **physically-conditioned** forecaster. The version that asks *how many barrels
of refining capacity are offline, for how long, at a facility of what criticality, in a country
whose ally holds what obligation* — because **none of those four quantities exists in the data.**

This distinction is the whole finding, and it cuts both ways:

- The project **cannot** claim the vision was tested and failed.
- Nor is the null empty. It establishes, with numbers, that **the version buildable from public
  panel data does not work**, and it locates the missing ingredient.

---

## 4. The measured reason the tested version failed — and it points at the same gap

Three independent results, computed under separate registrations, converge on one conclusion.

**(a) The conditions were mostly not knowable.** Enforcing a point-in-time rule showed **262 of
313 events have no situation field knowable on the day**, and 726 of 786 situation values were
knowable only *after* the event they describe. Step 3 of the vision — *learn the conditional* —
requires conditions. There were, for most events, none.

**(b) The event flag has no magnitude.** On the **44 days that are both a corpus OPEC event and a
Känzig announcement day** — same days, four regressors — the 0/1 flag's band **covers zero**
(−1.572) while a continuous measure of the same events **excludes** it (+2.230), and the flag
**collapses to −0.483** once the continuous measure is present. Our own `severity` ordinal fails
too. Step 8 — *assess how bad the damage is* — is the missing variable, stated in the negative.

**(c) A physical disruption need not be a price event, and the reverse.** Red Sea 2024: Bab
el-Mandeb flow **−56.6%**, Cape reroutes **+101.8%**, Brent **−4.9%**. Hormuz 2026: flow
**−92.3%**, reroute only **+20.7%**, Brent **+48.5%**. **A reroutable closure is a freight event;
an unreroutable one is a price event.** Nothing in a macro state vector distinguishes them. Only
physical geography does.

**All three say the same thing: the engine was reasoning about the environment without the
physical layer that makes the environment predictive.**

---

## 5. The positive results that do exist, and they are multi-product

The nulls are on the forecasting engine. These are not nulls, and none is Brent-only.

**Geopolitical shocks land in refining margins, not in crude flat price.** Of the events in each
class, the share coinciding with a top-5% move in that asset:

| event class | big **crude** move | big **diesel-crack** move | ratio |
|---|---|---|---|
| chokepoint disruption | 4/26 (15%) | **10/26 (38%)** | **2.5×** |
| infrastructure attack | 6/44 (14%) | **15/45 (33%)** | **2.4×** |
| sanctions | 8/55 (15%) | **19/55 (35%)** | **2.4×** |
| conflict escalation | 12/50 (24%) | **23/50 (46%)** | **1.9×** |
| OPEC decision | 17/51 (31%) | 13/51 (25%) | 0.8× |
| demand shock | 6/17 (35%) | 5/17 (29%) | 0.8× |

**Every military and geopolitical class is roughly 2–2.5× more likely to coincide with a large
refining-margin move than a large crude move — and the market/policy classes invert.** These are
conditional frequencies on our own corpus, not forecasts, and selection applies; they stand
regardless.

**The chain does not transmit as assumed.** Across **477 node×shock cells** spanning the whole
complex, 21 transmit against 1–24 expected under no transmission at all — while the same estimator
recovers Känzig's published oil-supply-news shock cleanly (Brent **+0.851 at h = 0** rising to
**+2.37 at h = 20**, every horizon excluding zero) and the Baumeister–Hamilton supply shock moves
physical production **+0.760 [+0.496, +1.023]**. So the instrument works and real shocks move real
quantities; what does not travel is the corpus event.

**Events move oil. This project's own replications prove it.** What fails is forecasting the
*size* of the response from a flag saying an event occurred.

---

## 6. What the untested version would require

Concretely, and in order of how much each would buy:

1. **A facility register with capacity and criticality** — refineries, terminals, fields, pipelines,
   with throughput and share of national/global capacity. This is the single missing keystone: it
   turns "Ras Tanura was struck" into "*n* barrels/day at risk, *x*% of Saudi export capacity."
2. **An outage register** — historical disruptions with capacity affected and duration restored.
   This is what makes "shutdowns like this last about this long" a measured statement.
3. **Damage severity as a physical quantity**, sourced per event, replacing an analyst ordinal that
   is now barred from carrying magnitude.
4. **Alliance behaviour, not alliance existence** — ATOP says an obligation exists; the vision needs
   the base rate of obligations being honoured, conditional on circumstance. ATOP also stops in 2018.
5. **A magnitude series for non-OPEC classes** — registered as the next study, and the prior
   question is sharper still: the tightening classes correlate **r = −0.023** with the identified
   supply shock over 614 months, so whether they are shocks at all comes before how to weight them.

Items 1 and 2 are the ones that would change the answer. Both are largely commercial data.

---

## 7. What this licenses saying

**Defensible:**

- I designed a learning instrument over the petro-product complex and built the whole apparatus —
  sequential walk-forward, sealed reads, online re-weighting, multi-product propagation across 53
  nodes and 772 series.
- I tested the version that public panel data supports, and it does not beat simple baselines.
- I identified the reason, three ways independently: the conditioning state was mostly not knowable
  at the time; the event flag carries no magnitude; and physical disruption and price response come
  apart in a way no macro state vector can see.
- Along the way I found that **geopolitical shocks land in refining margins rather than crude**, and
  that a **reroutable closure is a freight event rather than a price event** — both multi-product,
  both positive, both actionable.
- The missing layer is physical: barrels at risk, facility criticality, outage duration. That is a
  data-acquisition problem, not a modelling one, and it is now specified rather than assumed.

**Not defensible, and not claimed:**

- That the intended system was built. The physical layer does not exist.
- That historical analogy fails. The conditions under which it could work (§1.1 of the paper) were
  never met on this record.
- That geopolitical events do not move oil. They do, and this project measured it.

**The honest one-sentence version:** *I built the full apparatus for a history-trained,
multi-product petro forecasting instrument, tested the version public data supports, found it does
not beat simple baselines, and established that the missing ingredient is physical — capacity at
risk, facility criticality and outage duration — with three independent measurements pointing at
that same gap.*
