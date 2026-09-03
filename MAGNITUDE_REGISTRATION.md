# MAGNITUDE REGISTRATION — the shock-magnitude study, registered before computing

*2026-09-03, Session C. Written after `docs/RIPPLE_FINDINGS.md` (v2, prices) and
`docs/RIPPLE_PHYSICAL.md` (Amendment C, physical quantities), and **before any magnitude series
exists, any candidate is constructed, or any coefficient is computed**. The git timestamp is the
seal. Amendments are dated and appended, never edited in place. Everything in §11 is an
EXPECTATION to be tested; everything in §12 is an OUTCOME registered as admissible in advance,
including the outcomes that would end the programme.*

*Joe's brief of 2026-09-03 proposed a shape and asked me to argue with it rather than accept it.
§2 is where I disagree, and the disagreement changes the design substantially. §3 is a kill-test I
am adding that his brief did not contain and that should run before anything is built.*

---

## 0. The object, and why it exists

Twice now, with different outcome types, the same verdict:

| study | outcome | corpus dummies | an identified, magnitude-bearing shock, same code |
|---|---|---|---|
| v2 (`RIPPLE_FINDINGS.md` §4.1) | Brent, h = 5 | OPEC dummy **−3.159 [−7.439, +1.121]**, n = 47 | Känzig surprise **+1.727 [+0.919, +2.535]**, 128 days |
| Amendment C (`RIPPLE_PHYSICAL.md` §2.3) | JODI aggregate production, h = 0 | tightening dummy **−0.279 [−0.877, +0.318]**, n = 51 | B–H supply shock **+0.760 [+0.496, +1.023]**, 291 months |

A 0/1 dummy asserts only *something happened*. It weighs a coup and a communiqué identically. Both
studies named this the principal weakness and neither could fix it. **This document registers the
study that tries to, and registers in advance the conditions under which the honest answer is that
it cannot be fixed for a given class.**

**Scope.** This is a study of the *regressor*, not of the chain. It builds and validates candidate
magnitude series; it does not re-run the ripple study. Re-running the chain with a validated
magnitude is a later brief and needs its own registration. Session C owns `src/ripple_*`,
`src/magnitude_*`, `tests/test_magnitude_*`, `data/magnitude/**` and `docs/MAGNITUDE_*`.

---

## 1. The two existence proofs, and exactly what each proves

Joe's brief calls Känzig and Baumeister–Hamilton "existence proofs". They are, but not of the same
thing, and the difference is the whole design.

- **Känzig (2021)** identifies off the *futures price surprise* in a narrow window around OPEC
  announcements. Its magnitude is the size of the market's revision of belief.
- **Baumeister & Hamilton (2019)** identify a structural shock in a VAR whose variables include
  world oil *production*. Its magnitude is, to a first approximation, barrels.

Both recover cleanly with our estimator. They are proofs that **the estimator and both outcome
datasets work**, and that the failure is located in the regressor. That much of Joe's brief is
correct and is adopted.

---

## 2. Where I disagree with the proposed shape

### 2.1 The central objection: a Känzig-style analogue would be blind to the finding that motivated it

The brief proposes constructing "an equivalent" of Känzig for sanctions, chokepoint disruptions and
interstate escalation. Taken literally — a price-surprise magnitude in a window around each event —
this builds an instrument that **cannot see the result that made this study necessary**.

`RIPPLE_PHYSICAL.md` §4:

| episode | physical flow | Brent |
|---|---|---|
| Red Sea 2024 | Bab el-Mandeb **−56.6%**, Cape of Good Hope **+101.8%** | **−4.9%** |
| Hormuz 2026 | Hormuz **−92.3%**, Cape **+20.7%** | **+48.5%** |

A price-surprise magnitude scores the Red Sea closure at **approximately zero**, because Brent fell.
It would encode, as a measurement, precisely the blindness that the physical study exposed. It is
also **circular** when the outcome is a price: regressing Brent on a magnitude defined by Brent's
own move is not an estimate.

**Registered ruling.** Two magnitude concepts are separated, named, and never mixed in one column
(INV-5 in spirit):

| | **M-B — belief magnitude** | **M-Q — quantity magnitude** |
|---|---|---|
| what it measures | the market's revision, from asset prices in a window | barrels at risk, or barrels actually lost |
| built from | futures/spot surprise around the event | capacity, throughput, production, export volumes |
| legitimate outcome | **physical quantities only** | prices and quantities both |
| illegitimate outcome | **any price** (circular) | transit counts, where M-Q is *measured from* transits (circular) |
| Känzig is | this | not this |
| B–H is | not this | approximately this |

**M-Q is the object this study needs.** M-B is built only as a *comparator*, and only ever tested
against physical outcomes, where it answers a genuinely interesting question the dummies cannot:
**did the market's revision of belief predict the barrels?** Red Sea 2024 is the registered case
where the prediction is that it did not.

### 2.2 The calibration target as stated is wrong, and would reject good series

The brief says a candidate "should move production by something in that neighbourhood" of B–H's
+0.760 [+0.496, +1.023]. Two objections.

1. **Wrong unit.** B–H is a *global* shock and its coefficient is a global-aggregate response. A
   sanctions event on one country should not move global production by 1.32% (one SD) unless that
   country is large. Matching the level would be evidence of a *confound*, not of validity. The
   calibration must be an **elasticity**: coefficient per unit of barrels-at-risk, i.e. does a shock
   putting *x*% of world supply at risk move measured production by an amount consistent with *x*
   after offset?
2. **Wrong panel.** The balanced JODI panel deliberately **excludes every reporter that went dark**
   (`RIPPLE_PHYSICAL.md` §2.2) — Iran, Russia, Iraq, UAE, Qatar. A sanctions shock's direct effect
   is on the target's production, and the target is not in the panel. The target's own loss is
   structurally invisible.

**Registered consequence — the offset channel is the primary test for sanctions.** What *is*
visible in the balanced panel is the **replacement**: if barrels are removed from a sanctioned
producer, the non-sanctioned producers in the panel (Saudi Arabia and the United States are both in
it) should raise output. Registered directional prediction, stated before anything is built: a
sanctions shock of magnitude M-Q **lowers the target's own production** (where the target still
reports) **and raises balanced-panel production**, with the panel coefficient smaller in absolute
value than the target's. A 0/1 dummy can make no such paired directional prediction; this is the
first thing magnitude buys that is not just extra precision.

### 2.3 Magnitude may not be the binding constraint, and the design must be able to say so

The brief assumes the defect is missing magnitude. Three rival explanations are already in the
evidence and are registered here as live alternatives, to be discriminated rather than assumed away:

| # | rival explanation | evidence already in hand |
|---|---|---|
| **R1** | **no magnitude** (the brief's hypothesis) | §0's two rows |
| **R2** | **the events are not supply shocks** | `RIPPLE_FINDINGS.md` §4.2: correlation of our monthly tightening count with the B–H identified supply shock is **r = −0.023 over 614 months** — very nearly orthogonal |
| **R3** | **anticipation** — the event date is the wrong date | §4.3: Brent is already **+1.663% (se 0.803, n = 49)** in the five days *before* an OPEC decision, flagged ANTICIPATED-IN-PRICE |
| **R4** | **offset** — the true production effect is small because spare capacity absorbs it | Kilian's own conclusion that unanticipated supply disruptions have only small effects on the real price |

**R2 is the one that would end the programme, and it is currently the best-supported.** A magnitude
attached to an event that is not a supply shock is still not a supply shock. Registered
consequence: §3's kill-test runs first and is designed to separate R1 from R2 at low cost.

### 2.4 The class where magnitude is easiest to build is the class whose correct outcome we cannot buy

If a reroutable closure is a freight event (§9), the correct outcome for chokepoint disruptions is a
**tanker freight rate**. `RIPPLE_SOURCES.md` §6 and `docs/DATA_LICENCES.md` record that Baltic BDTI
and BCTI are **licensed, not free, and not obtained** — a standing GAP, and the $0-forever constraint
disqualifies buying them. The tanker equities are labelled equity proxies and must never be read as
freight.

Registered now, before it can be discovered as a disappointment: **chokepoint disruptions are the
class where M-Q is most cleanly measurable (PortWatch publishes `capacity_tanker` in metric tons/day,
already loaded, 2,799 days) and the class whose theoretically correct outcome is unavailable at $0.**
A free route-level tanker rate is registered as a search target in §4; if none is found, the class is
tested on prices and physical transits only, and the freight channel is reported as unmeasured.

---

## 3. STAGE 0 — the kill-test, which runs first and gates everything else

**This is not in Joe's brief and I am adding it, because it can end or justify the programme using
data already in `data/oil.db`, before a single new series is constructed.**

For exactly one class — `opec_decision` — we already possess both a dummy and a validated
magnitude on the same events. So the value of magnitude is directly measurable there, and it is an
upper bound on what magnitude can buy elsewhere: OPEC announcements are the *easiest* case (scheduled,
identifiable, with a liquid instrument in a narrow window).

**Registered design.** On the intersection sample — the days that are both a corpus `opec_decision`
event and a Känzig announcement day — estimate, with the ripple estimator unchanged:

- **A. dummy only:** the 0/1 corpus dummy.
- **B. magnitude only:** Känzig's continuous surprise.
- **C. both:** dummy + magnitude, to see whether the dummy retains any information once magnitude
  is present.

Outcomes: Brent (h = 0…60, headline 5) and JODI balanced-aggregate production (h = 0…12, headline
**0**, per `RIPPLE_PHYSICAL.md` §2.3's finding that quantity responses live at h = 0–1).

**Registered decision rule, fixed now.**

| Stage 0 result | registered verdict | consequence |
|---|---|---|
| B ≫ A, and in C the dummy's coefficient is indistinguishable from zero | **MAGNITUDE IS THE BINDING CONSTRAINT** | proceed to Stage 1 for all classes |
| B ≈ A (magnitude adds little on the easiest class) | **MAGNITUDE IS NOT THE BINDING CONSTRAINT** | do **not** build magnitude for the hard classes; the defect is R2/R3, and the next brief is event *identification*, not event *weighting* |
| B > A on price but not on production | **MAGNITUDE IS BELIEF, NOT BARRELS** | build M-B only, and only as the §2.1 comparator |

**Registered prior, so the result cannot be reinterpreted afterwards.** From v2 §4.1 the point
estimates already published are: Känzig +1.727 [+0.919, +2.535] versus the OPEC dummy −3.159
[−7.439, +1.121], both at h = 5 on Brent. Those two numbers are *not* the Stage 0 test — they are
estimated on different samples (128 announcement days versus 47 de-overlapped corpus events) and are
not a like-for-like comparison. Stage 0's contribution is the **shared subsample**, which removes
that confound. I expect Stage 0 to return "magnitude is the binding constraint" on price and I am
genuinely unsure on production; that expectation is recorded so that a contrary result is a
disconfirmation and not a surprise to be explained away.

---

## 4. STAGE 1 — per-class construction, with the constructibility verdict fixed in advance

Only if Stage 0 permits. For each class, the source, the unit, and **what would have to be true for
the series to count as constructed** — all fixed now.

| class | proposed M-Q source | unit | status of the source, today |
|---|---|---|---|
| `chokepoint_disruption` | PortWatch `capacity_tanker` (metric tons/day) at the named chokepoint; EIA World Oil Transit Chokepoints for pre-2019 normal throughput | share of world seaborne crude at risk | **loaded** (2,799 days, 7 chokepoints); EIA to be checked |
| `sanctions` | GSDB R5 (obtained, local-only, non-redistributable) for scope/type/date; target's JODI crude exports and production for barrels | target's exports as share of world supply | GSDB **obtained**, not yet parsed; JODI loaded |
| `infrastructure_attack` | nameplate capacity of the struck asset (refinery kb/d, terminal, pipeline), coded per event from the event's own sources | capacity struck, kb/d | **not built**; requires per-event coding against sources |
| `conflict_escalation` | belligerents' combined production/exports from JODI + the corpus's own actor/target fields | belligerent supply at risk | partially derivable; **weakest case** |
| `opec_decision` | Känzig (M-B) already; announced quota change in kb/d as M-Q | kb/d of announced quota change | Känzig loaded; quota changes **not built** |
| `demand_shock` | registered INSUFFICIENT in advance (n = 13 monthly, 9 daily) | — | not attempted |
| `policy_response` | announced SPR release volumes, kb/d, where the event is a release | kb/d released | not built |

**Registered constructibility criteria.** A class is:

- **CONSTRUCTIBLE** if a magnitude can be assigned from a *source document or a measured series* to
  **≥ 80%** of the class's de-overlapped events in the study window, with **≥ 3 distinct non-modal
  values** and a within-class coefficient of variation **≥ 0.5**.
- **PARTIAL** if ≥ 50% and < 80% coverage, or if it meets coverage but fails the dispersion test.
- **NOT CONSTRUCTIBLE** otherwise.

Coverage and dispersion are properties of the constructed series and are computed **before any
outcome regression touches it**. A NOT CONSTRUCTIBLE verdict is a registered, publishable result
(§12), not a failure to be worked around: the criteria are fixed here precisely so that "we could
not build it" cannot become an excuse invented after a disappointing estimate.

**Registered prohibition.** No magnitude may be assigned by a language model reading an event
description and producing a number. Every magnitude value carries a source and a vintage, as
everything in this repo does (charter §2 rule 1). Where no source gives a number, the value is
missing and the event is uncovered — never imputed.

---

## 5. The free ordinal magnitude we already have, and the claim it already supports

`events.severity` (1–5) is populated for 305 of 313 events and is **unused by the ripple study**. It
is nearly orthogonal to class — between-class SD of the class means is **0.13** against a
within-class SD of **0.75–1.00** — so it does carry within-class information. It is registered as a
**zero-cost baseline comparator** in Stage 0, because a magnitude series that cannot beat an ordinal
severity code is not worth building.

**Two disclosures, both of which bound how it may be read.**

1. **It is a mixed measured/inferred column.** `src/admit_events.py` assigns auto-admitted events a
   *deterministic provisional band by event type* (`SEV_BAND`: 3 for chokepoint/infrastructure/
   conflict/OPEC/demand, 2 for sanctions/policy). **102 of 313 events sit exactly on their class's
   auto value** — an upper bound on how many are class-imputed rather than judged. Storing a measured
   and an inferred value in one column is what INV-5 forbids. Registered consequence: severity is
   used **only** with the auto-band events flagged, and every severity result is reported twice —
   all events, and hand-coded events only.
2. **There is already a VALIDATED claim in this repo asserting the thing this study is testing.**
   `data/edge_battery.json` carries `severity_dose_response` — "high-severity (4–5) events ripple
   harder into oil than low-severity (1–2)" — as **validated**: amp **+5.079 [+1.003, +9.364]**,
   n = 116 (76 high, 40 low), permutation p = 0.0303, survives FDR at q = 0.10, **fails Bonferroni**
   (adjusted 0.394).

**Registered re-test, in the pattern of `RIPPLE_REGISTRATION.md` Amendment B.** That claim was
validated by the `edge_battery` gate, which is the same family of gate whose defect v2 §3 documented
and on which five of six `propagation_edges` were retracted: **it never looks at a non-event day**,
so a world in which nothing transmits but severe events cluster in volatile periods passes it. Before
any new magnitude series is built, `severity_dose_response` is re-tested under the ripple discipline
— VIX+GPR-matched placebo, EHW and Newey–West bands, the registered three verdict words — and the
outcome is registered now:

- **RETAINED** if TRANSMITTING under that discipline.
- **RETRACTED** if NULL.
- **INSUFFICIENT** if below n = 15 after de-overlapping.

The `edge_battery.json` file is **not edited by this brief**; the status is reported for the owning
session to act on, exactly as Amendment B did.

---

## 6. Outcomes, and the freight gap

Registered outcome set, unchanged from the two prior studies except where noted:

1. **Prices** — Brent, WTI, product cracks (v2 Table N). Legitimate for M-Q; **forbidden for M-B**.
2. **Physical quantities** — JODI production/exports (balanced panel and named producer), PortWatch
   transits. Legitimate for both, with the circularity carve-out: where M-Q for a chokepoint event is
   *measured from* that chokepoint's transits, transit outcomes at that chokepoint are excluded and
   only the price and the reroute counter-node are read.
3. **Freight** — **GAP**. BDTI/BCTI licensed and not obtained; equity proxies are not freight.
   Registered search target: any free, route-level, publicly redistributable tanker rate. If none is
   found within the Stage 1 pass, the freight channel is reported as **unmeasured**, and §9's
   proposition is tested on the flow/price contrast alone.

**Headline horizons.** Prices h = 5 (daily), quantities **h = 0 and h = 1** (monthly). This is a
change from Amendment C's h = 3 and it is registered with its reason: `RIPPLE_PHYSICAL.md` §2.3
showed that even for an identified shock the production response lives at h = 0–1 and is gone by
h = 2, while the price response runs to h = 12. Amendment C's h = 3 was registered where a physical
response has already decayed. The full registered horizon set is unchanged.

---

## 7. Estimator, samples and vocabulary — all carried over unchanged

Lag-augmented local projections, EHW (Montiel Olea & Plagborg-Møller) primary and Newey–West(h)
diagnostic, VIX+GPR-matched placebo × 500, Benjamini–Hochberg at q = 0.10 within a node's family,
minimum **n = 15** de-overlapped events, 35-calendar-day chain rule, seed 19900802. Verdict
vocabulary is the registered three: **TRANSMITTING / NULL / INSUFFICIENT**; the nine-expectation
vocabulary is **CONSISTENT / INCONSISTENT / INDETERMINATE**. Code imports from `src/ripple_lp.py`
and does not re-implement, as `src/ripple_physical.py` does and a test asserts.

**A continuous regressor changes one thing and it is registered now.** With a 0/1 dummy, `n_events`
is the count of ones. With a continuous magnitude the effective sample is not a count, so the
minimum-n rule is applied as: **the number of events with a non-zero, non-missing magnitude must be
≥ 15**, and that number is reported on every row. Cells are additionally flagged where a **single
event contributes more than 25% of the regressor's total variance**, because one large event with a
large magnitude is a case study, not an estimate.

---

## 8. Samples, fixed in advance where they can be

Daily price sample 1990-01-09 → 2026-08-25 (the VIX control binds, per Amendment A). JODI monthly
2002-01 → 2026-06, 294 months. PortWatch daily 2019-01-01 → 2026-08-30, 2,799 calendar days.
De-overlapped event counts within each window are those already published and reconciled in
`RIPPLE_PHYSICAL.md` §1 and are not restated here. **Per-class magnitude-covered n cannot be fixed in
advance**, because coverage is what Stage 1 determines; it is reported for every class before any
outcome regression is run, and §4's thresholds are applied to it.

---

## 9. The proposition Joe asked to be stated, registered as a testable claim

> **A reroutable closure is a freight event, not a price event. A price-only study sees it and
> concludes that nothing happened.**

The evidence, from `docs/RIPPLE_PHYSICAL.md` §4: Red Sea 2024 cut Bab el-Mandeb tanker transits
**−56.6%** and raised Cape of Good Hope transits **+101.8%**, with Brent **−4.9%**. Hormuz 2026 cut
transits **−92.3%** with Cape only **+20.7%**, and Brent **+48.5%**. The difference is that there is
no reroute out of the Gulf.

This is a claim about **study design across this literature**, not about our corpus: any event study
that measures oil-supply disruption by the price response will score a reroutable closure at
approximately zero, however large the physical disruption. It is stated here because it is the
strongest sentence either ripple study produced and it should not live only in a handoff note.

**It is currently supported by n = 2 episodes and is therefore a proposition, not a finding.**
Registered as testable, with the test fixed now: across the PortWatch window, classify each
de-overlapped chokepoint event by whether a **reroute counter-node rose** while the named chokepoint
fell, and test whether the price response is systematically smaller for the reroutable group. The
registered honest outcome is that **n will be too small** — §3.1 of the physical report already shows
every named-chokepoint cell below the minimum — in which case the proposition is published as a
**two-case demonstration with its n stated**, and the search moves to whether it can be tested on
external chokepoint-closure datasets rather than on this corpus. That outcome is registered as
admissible now so that reporting it later is not a retreat.

---

## 10. Multiple testing

Every candidate magnitude series tested against every outcome is a family. BH at q = 0.10 within
each (outcome node × class) family, as in v2 §2.9. The Stage 0 kill-test is **three specifications on
one class and two outcomes** and is small enough to read directly; its base rate is stated with its
result. Stage 1's family size cannot be fixed in advance because it depends on how many classes turn
out CONSTRUCTIBLE; the **base-rate range under a complete null is computed and printed beside every
tally**, as `RIPPLE_PHYSICAL.md` §2.5 does, and no tally is reported without it.

---

## 11. Expectations, stated in advance

- **E-1** Stage 0 returns "magnitude is the binding constraint" on Brent: Känzig's continuous
  surprise beats the OPEC dummy on the shared subsample, and the dummy carries no residual
  information in spec C.
- **E-2** Stage 0 is **INDETERMINATE on production**. I do not expect the OPEC magnitude to move
  JODI aggregate production detectably even at h = 0, because OPEC quota announcements are
  anticipated (R3) and offset (R4).
- **E-3** `chokepoint_disruption` is the only class that returns **CONSTRUCTIBLE** on the first pass,
  because PortWatch measures the flow loss directly.
- **E-4** `sanctions` returns **PARTIAL**: GSDB gives dates and scope for most events but barrels
  only where the target still reported to JODI, and §0 of the physical report shows the targets are
  exactly the reporters that went dark.
- **E-5** `conflict_escalation` returns **NOT CONSTRUCTIBLE**. There is no source that assigns
  barrels-at-risk to an escalation without an analyst's judgement, and §4 forbids that judgement
  being a model's.
- **E-6** `severity_dose_response` is **RETRACTED** under the ripple discipline — it fails Bonferroni
  already, and its gate is the one v2 §3 showed cannot distinguish transmission from volatile
  periods.
- **E-7** Where M-Q and M-B are both constructed for the same class, they are **weakly correlated**,
  and Red Sea 2024 is the extreme case: large M-Q, near-zero M-B.
- **E-8** No magnitude series moves balanced-panel production by anything approaching one SD of the
  B–H shock (1.32% at h = 0), because the panel excludes the sanctioned producers and the offset
  channel is second-order.

---

## 12. Outcomes registered as admissible in advance

So that none of them is a retreat when reported:

1. **Magnitude fixes it.** Stage 0 passes, Stage 1 builds ≥ 1 CONSTRUCTIBLE series, and re-running
   the chain with it produces TRANSMITTING cells that the dummy missed. Requires its own registration.
2. **Magnitude is not the binding constraint.** Stage 0 returns B ≈ A. The programme **stops here**
   and the next brief is event identification (R2) or event timing (R3), not event weighting. This is
   a publishable result and the registration says so before the test is run.
3. **Magnitude is belief, not barrels.** Stage 0 splits by outcome. M-B is built as a comparator
   only, and the M-B/M-Q divergence becomes the object of study.
4. **Some classes are NOT CONSTRUCTIBLE.** Published per class against §4's fixed criteria, with the
   coverage and dispersion numbers that produced the verdict.
5. **Everything is NOT CONSTRUCTIBLE.** Admissible. The result would be that this corpus's
   non-OPEC classes cannot be given magnitude from free sources, which bounds what any $0 study of
   this kind can achieve and is worth stating plainly.

---

## 13. Known limits, stated now

1. **R2 is unresolved and may be fatal.** r = −0.023 between our tightening count and the identified
   supply shock. If our events are not supply shocks, weighting them changes nothing. Stage 0 is
   designed to detect this cheaply but is run on OPEC, the class *least* affected by R2 (r = 0.431
   with |Känzig|), so a Stage 0 pass does **not** license assuming R2 is absent for the other classes.
2. **The go-dark selection is unfixed and unfixable** (`RIPPLE_PHYSICAL.md` §0). Magnitude does not
   restore Iran's post-2018 production record.
3. **Freight is a gap** (§2.4, §6), and it is the correct outcome for the class most likely to be
   CONSTRUCTIBLE.
4. **`severity` is a mixed measured/inferred column** (§5), with up to 102 of 313 values class-imputed.
5. **A continuous regressor is more fragile to one large event than a dummy is**; §7's 25%-of-variance
   flag mitigates but does not remove this.
6. **The corpus is 313 events.** Magnitude improves precision per event; it does not add events.
7. **GSDB R5 is non-redistributable** (`docs/DATA_LICENCES.md`): any sanctions magnitude built from
   it is local-only and a fresh clone cannot rebuild it, exactly as JODI already is.
8. **§9's proposition rests on two episodes**, one of which is still in progress.

---

## 14. What is NOT registered here

No re-run of the ripple chain with a magnitude series (that is a later brief and needs its own
registration). No change to the v2 or Amendment C nodes, the estimator, the placebo construction,
the minimum n, the verdict vocabulary or the BH rule. No edit to `events`, `propagation_edges` or
`data/edge_battery.json`. No new outcome family. No purchase of any licensed data, now or ever
(`CLAUDE.md`: $0 recurring, forever).

**No estimate in this document has been computed.** Every coefficient, band and correlation is
quoted from `docs/RIPPLE_FINDINGS.md`, `docs/RIPPLE_PHYSICAL.md`, `data/edge_battery.json` or
`src/admit_events.py`, cited at the point of use. The only arithmetic performed *for* this document
is §5's severity dispersion, which is four counts over the `events` table and no regression. It is
reproduced in full by:

```python
import sqlite3, pandas as pd
SEV_BAND = {"chokepoint_disruption": 3, "infrastructure_attack": 3, "conflict_escalation": 3,
            "opec_decision": 3, "demand_shock": 3, "sanctions": 2, "policy_response": 2}
e = pd.read_sql("SELECT type, severity FROM events", sqlite3.connect("data/oil.db"))
e["sev"] = pd.to_numeric(e.severity, errors="coerce")
print(e.sev.notna().sum())                              # 305 of 313 populated
print((e.sev == e.type.map(SEV_BAND)).sum())            # 102 on the auto band
g = e.groupby("type").sev.agg(["mean", "std"])
print(g["std"].min(), g["std"].max(), g["mean"].std())  # 0.75, 1.00 within; 0.13 between
```

Running it is the receipt; no output file is written, because writing one before Stage 0 would be
the first computed artefact of a study this document exists to precede.
