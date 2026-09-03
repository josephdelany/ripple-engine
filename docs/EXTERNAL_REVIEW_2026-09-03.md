# External review — energy economics desk

*2026-09-03. Adversarial read of the full repository. Findings ranked by severity, with a
remediation plan. Nothing here is softened.*

---

## 0. What the project is trying to do, stated so the critique lands on the right target

The stated goal is to test whether historical precedent — the reasoning behind *"this resembles
1973"* — carries predictive information about geopolitical escalation and the petroleum complex,
under a strict point-in-time constraint. The intended instrument decomposes into hazard,
vulnerability, exposure and financial modules.

**The critique below is not that the question is bad. The question is good and under-examined.** It
is that several published claims do not survive scrutiny, and that the design constrains what the
central null can mean far more than the paper acknowledges.

---

## PART 1 — FATAL. These claims must be withdrawn or fundamentally restated.

### F1. The anticipation finding is mostly an artefact of the onset definition

**Claimed:** median 31-day lag from event to move onset; *"in half of attributed Brent episodes
every attributed event was already public more than 20 trading days before the move began."*

**The defect.** `src/big_moves.py:92` sets `onset = win.idxmin() if up else win.idxmax()` — **the
onset is the price extreme, selected ex post.** By construction it precedes everything else in the
episode. `anticipated` (line 185) then flags any event falling more than 20 days after that onset.

**Measured.** Median episode duration **76 days**; **100% of episodes exceed 20 days.** Under a
uniform null — an event landing anywhere inside its own episode by chance — **55% would be flagged
anticipated by construction.** Observed: **69%** of 77.

**Verdict.** There is an excess over the mechanical baseline (~2.5σ on a crude unclustered test),
but the headline is mostly definitional. **The claim as published is not supportable.** It needs a
clustered test against the uniform-within-episode null, and the honest restatement is *"a modest
excess over what the onset definition produces mechanically."*

### F2. The Red Sea / Hormuz contrast has no control and the pre-trend runs against it

**Claimed:** Bab el-Mandeb flow −56.6%, Cape reroutes +101.8%, Brent −4.9% — *"a reroutable closure
is a freight event, not a price event."*

**The defect.** Pulled from the project's own price table: Brent fell **−14.8% during Q4 2023,
before the attacks began** (91.2 → 77.7). Across the attack window itself, December 2023 to March
2024, Brent **rose +9.5%** (78.7 → 86.2).

**Verdict.** The −4.9% is a windowing choice against a strongly falling pre-trend driven by demand
weakness and non-OPEC supply growth. **There is no detrending, no counterfactual, and n = 2.** The
mechanism is plausible and may well be right; **the evidence presented does not establish it.**
Demote to an illustration with the pre-trend stated in the same breath, or test it properly on more
episodes with a control.

### F3. The pass-through asymmetry is a replication presented as a discovery

**Claimed:** *"the strongest and least expected result in the project."*

**The defect.** Asymmetric price transmission from crude to petroleum products is among the most
studied phenomena in energy economics. Bacon (1991) coined "rockets and feathers"; Borenstein,
Cameron and Gilbert (1997, *QJE*) is canonical; there is a large subsequent literature and multiple
meta-analyses.

**Verdict.** The result is real and survives FDR. It is **not** unexpected and **not** new.
Reposition as *"reproduces the known asymmetry on spot rather than retail; here is what differs in
my specification."* Presenting it as a discovery signals the literature was not searched.

---

## PART 2 — STRUCTURAL. These do not invalidate the null; they determine what it can mean.

### S1. For 84% of events there is no structural state to condition on — so "state-conditioned" overstates what was tested

`data/state/situation_knowable.json`: **60 field-values kept of 786; 262 of 313 events have no
situation field knowable at *t*.** For those events, similarity is computed on the market block,
class and entities.

**Consequence.** The paper's central null is not *"conditioning on the world state fails."* It is
**"market-state-and-class matching fails."** That is a narrower and much more defensible claim, and
the paper should make it in those words.

### S2. For 28% of reads, retrieval is not selecting anything

The engine retrieves *k* = 12. Pool sizes: median 21, **minimum 0**, and **28% of reads have a pool
smaller than 12** — 15% have five or fewer, 6% have one or none.

**Consequence.** For nearly a third of reads "the twelve most similar events" is simply "all
available events." **The similarity metric is inert on those reads by construction.** A null on the
value of similarity cannot be cleanly interpreted when a third of the sample never exercised it.
This belongs in the limitations at the top, not buried.

### S3. The state vector is macro-financial, not fundamental

The "physical" block is three fields — inventory sigma, the diesel crack, the Brent–WTI spread —
**all derived from prices.** Absent: OECD days of cover, non-OPEC supply growth, demand growth,
floating storage, rig counts, spare capacity (which exists in the database but not in the retrieval
blocks).

**Consequence.** An energy economist's first four variables are all missing. With 772 series
available this was a design choice, not a data constraint. Restated honestly, the finding is
*"conditioning on the financial state does not predict oil"* — modest, true, and survivable.

### S4. The reference class spans regimes that are not comparable

8 events precede 1983 (no NYMEX crude futures). 78 precede 2010 (pre-shale). **150 of 313 fall in
the 2020s alone.** Retrieving a 1979 analog for a 2024 event assumes price formation is stable
across the introduction of futures markets, the SPR, financialisation and shale. **Nothing in the
design tests this**, and it is at least as plausible an explanation of the null as §1.1's three
conditions.

### S5. The escalation target is the wrong question for the stated goal

The bulk of the apparatus estimates IES-90 escalation levels — a political-science construct. If
the question is petroleum-complex response, escalation is at best an instrument. The price arm,
which is the economic question, is comparatively thin.

### S6. `policy_response` is a 57-event grab bag

The second-largest class, analytically heterogeneous. Large heterogeneous classes absorb noise and
dilute real effects.

---

## PART 3 — WHAT SURVIVES

- **The vintage finding.** 262 of 313 with no knowable state, and the disappearance of apparent
  skill once enforced. Sound, central, and untouched by this review.
- **Flags versus magnitude on the 44 shared days.** Same days, same events, only the regressor
  changes. A clean design and the right kind of evidence.
- **The bound at |*r*| ≤ 0.10.** Stating what is ruled out rather than what was found.
- **The exposure measurement: 5 COMPLETE of 80.** Genuinely useful to anyone scoping a supply-risk
  build, with the failure modes documented.
- **The specification curve, negative in all 162 settings.**
- **The integrity apparatus.** Four retractions, three audits, a suite that refuses to report green
  when it has not run, registrations verifiable by commit order. This is unusual and it is real.

---

## PART 4 — REMEDIATION PLAN

**Most of these cannot be fixed by more computation. They are fixed by restating the claim
correctly — and the correctly stated claim is stronger than the current one.**

| # | action | owner | cost |
|---|---|---|---|
| **R1** | Withdraw F1 and F2 as findings; restate F3 as replication. Correction-of-record in place. | docs | 1 h |
| **R2** | Add the operational definition of "similar" to §6: what the engine compares on, for how many events. | docs | 30 m |
| **R3** | Publish the pool-size distribution as a first-class limitation, with the 28% figure. | docs | 30 m |
| **R4** | Rename the central claim throughout: **market-state-and-class matching**, not state-conditioned analogy. | docs | 45 m |
| **R5** | Add regime comparability (S4) to limitations with the pre-1983 / pre-2010 counts. | docs | 20 m |
| **R6** | Reorder every findings surface by what survives review. Vintage first. | docs | 45 m |
| **R7** | Cite Bacon 1991 and Borenstein–Cameron–Gilbert 1997; search the event-study anticipation literature before republishing F1. | docs | 45 m |
| **R8** | Test F1 properly: clustered permutation against the uniform-within-episode null. | analysis | 1–2 h |
| **R9** | The 30-row label audit. | author | 3 h |

**R1 through R7 are presentational and take about four hours.** They convert a project that would be
taken apart in a room into one that pre-empts its own criticism. **R8 is the only new analysis
worth running today**, and it decides whether F1 becomes a real finding or stays withdrawn.

**The restated headline, after remediation:**

> Market-state-and-class matching over a 70-year corpus does not predict escalation or petroleum
> prices out of sample under a point-in-time constraint. The richer structural version could not be
> tested, and the project measures why: 84% of events carry no knowable structural state, 28% of
> reads have no selection to perform, and the physical layer is 6% recoverable from public sources.

That is defensible, it is interesting, and it is what the evidence supports.
