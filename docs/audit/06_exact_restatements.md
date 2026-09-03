# Exact restatements

*Drop-in replacement text. Each block replaces a specific published claim.*

---

## 1. Abstract — the central claim

**Remove:** *"does formalised historical analogy contain out-of-sample predictive information about
geopolitical escalation and oil prices, once hindsight is removed?"* as a description of what was
tested.

**Replace with:**

> We test whether **reranking within an event class**, on a state vector that is largely
> macro-financial, beats **pooling within that same class** — for two outcomes: an escalation label
> that is 83% derived from country-level violence, and the raw 20-day return on Brent. Neither
> comparison favours retrieval. We are explicit that this is narrower than the question we set out
> to ask, and §§5, 8 and 12.4 set out why the wider version could not be tested on this record.

---

## 2. §5 — what IES-90 measures

**Insert at the head of the section:**

> **What this target measures in practice.** Of 132 labelled events, **109 (83%) carry a
> location basis** — the level was set by violence recorded anywhere in the affected country within
> the window — and 23 carry a dyadic basis, where a record matched both parties of the event's pair.
> Of the **59 non-zero labels, 47 are location-based and 12 are dyadically grounded.** The target is
> therefore closer to *"was there violence in this country in the next 90 days"* than to *"did these
> two parties escalate against each other."* Results below should be read accordingly, and the
> dyadic subset is reported separately.

---

## 3. §8 — the persistence result

**Replace:** *"A forecaster who knew nothing but the dyad's own recent history would have beaten
this engine decisively."*

**With:**

> Persistence is computed by calling the **same** scoring function on the prior 90-day window
> (`persistence.py:45`), so it is the same largely location-based variable, lagged. Given that 83%
> of labels are country-violence indicators, and that country violence is heavily autocorrelated,
> **the persistence baseline is close to an AR(1) on the target itself.** Its advantage is therefore
> only weak evidence about analogy, and we do not read it as such.

---

## 4. §8 — scope of the escalation comparison

**Insert before the first result:**

> **What the comparison is between.** The candidate pool is filtered to the same event class
> (`read.py:208`), and climatology is computed from that same pool. Both the engine and the baseline
> therefore receive class conditioning; only the state vector distinguishes them. The engine
> retrieves **k = 8** from a median pool of **18** — 44% of what is available — and in **26% of
> reads the pool is at or below k, so no selection occurs at all.** With **262 of 313 events
> carrying no situation field knowable at *t***, the comparison is best described as **within-class
> reranking on market state against within-class pooling.**

---

## 5. §8 — the price result

**Insert:**

> **What the price target is.** The outcome is the raw percentage change in Brent from the event
> date to +20 trading days (`read.py:148–177`). **There is no market model and no
> abnormal-return adjustment.** A 20-day Brent return is dominated by the oil market rather than by
> the event, and climatology is approximately the unconditional distribution of such returns.
> Beating it would require forecasting oil. **This result should therefore be read as a statement
> about forecasting raw returns, not about estimating event effects.**

---

## 6. `OIL_FINDINGS.md` §1 — pass-through

**Replace the header and opening.**

> ## 1. [TESTED — REPLICATION] At one month, light ends rise with crude and do not fall with it
>
> This reproduces a well-established result. Asymmetric transmission from crude to petroleum
> products is documented from Bacon (1991) — "rockets and feathers" — and Borenstein, Cameron &
> Gilbert (1997), with a large subsequent literature. **What is new here is only the setting:** spot
> rather than retail prices, on a 17-test family with BH-FDR correction.

---

## 7. `OIL_FINDINGS.md` §3 — anticipation

**Replace the section with:**

> ## 3. [WITHDRAWN PENDING TEST] Events and move onsets
>
> An earlier version reported a median 31-day lag and *"in half of attributed Brent episodes every
> event was public more than 20 trading days before the move began."* **That claim is withdrawn.**
> `big_moves.py:92` defines onset as the **price extreme, chosen ex post**, so it precedes
> everything in the episode by construction. Median episode duration is **76 days** and **every
> episode exceeds 20 days**; a uniform within-episode null produces **55% "anticipated"
> mechanically**, against **69%** observed. The excess is ≈2.5σ on a crude unclustered test and is
> not reported as a finding pending a clustered permutation against that null.

---

## 8. `OIL_FINDINGS.md` §5 — Red Sea / Hormuz

**Replace with:**

> ## 5. [CASE, n = 2 — CONFOUNDED] Reroutability and chokepoint closures
>
> Red Sea 2024: Bab el-Mandeb flow −56.6%, Cape reroutes +101.8%, Brent −4.9%. Hormuz 2026: flow
> −92.3%, reroute +20.7%, Brent +48.5%.
>
> **This comparison is confounded and is reported as an illustration only.** Brent fell **−14.8%
> during Q4 2023, before the Red Sea attacks began**, and **rose +9.5% across the attack window
> itself.** The −4.9% depends on the window chosen, against a strongly falling pre-trend driven by
> demand weakness and non-OPEC supply growth. There is no detrending and no counterfactual. The
> mechanism — that a reroutable closure is a freight event rather than a price event — is plausible
> and is **not established by this evidence.**

---

## 9. Resume and application material

**Replace** *"Established that geopolitical shocks land in refining margins rather than crude"* —
which is a descriptive rate that failed its McNemar test — **with:**

> Measured that dated event-occurrence flags carry no information about the size of a market
> response once the market's own revision in expectations is controlled for, on 44 days where both
> encodings are observable — and that the physical alternative is only 6% recoverable from public
> sources.

**And add, because it is the strongest defensible sentence available:**

> Audited my own instrument and found both outcome variables mis-specified relative to the claims
> made about them; restated the results accordingly rather than defending them.
