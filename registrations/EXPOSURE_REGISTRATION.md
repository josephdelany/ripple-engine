# EXPOSURE & VULNERABILITY — registration, written before any code

*2026-09-03. Committed before `src/exposure.py` and before any field is filled. Verdict words and
exclusion rules fixed here.*

## §0 What this is

`docs/VISION_AND_BUILD.md` established that the project's environment vector is 13 macro-financial
fields and 4 dyad flags, and that the missing layer is physical. `PHYSICAL_EXPOSURE_REGISTRATION.md`
registered the country-level exposure study. **This registration adds the layer that was designed
into the schema and never filled:** `events.sr_target_capacity` is populated for all 313 events with
the literal string `"unknown"`, and `sr_asset_role` is `"unknown"` for 271 of 313.

The project is hereby stated in the architecture it has always implied — the four modules of a
catastrophe model (NAIC; Casualty Actuarial Society), with the retrieval step being reference-class
forecasting in Flyvbjerg's sense:

| module | supplies | status |
|---|---|---|
| **Hazard** | the event catalogue and reference-class retrieval | built: 313 events, walk-forward, sealed reads |
| **Vulnerability** | capacity affected → duration of outage | **this registration** |
| **Exposure** | which asset, what capacity, what criticality | **this registration** (history) + intake schema (live) |
| **Financial** | volume-days lost → price and margin response across the complex | built: 53-node propagation |

## §1 Scope, stated so it cannot be overread

Exposure is populated **only for the 75 events whose class involves a physical asset** — 48
`infrastructure_attack` and 27 `chokepoint_disruption`. The other 238 events (sanctions, policy
response, OPEC decision, conflict escalation, demand shock) have no damaged facility and are
**out of scope by construction, not by omission**. Every result from this layer is a result about
75 events and is reported as such.

## §2 The schema — 6 required, 6 optional, and the rule that makes it defensible

Required (an event is `COMPLETE` only with all six):

| field | unit | note |
|---|---|---|
| `asset_name` | text | the specific refinery, terminal, field, pipeline or chokepoint |
| `asset_type` | enum | refinery · terminal · field · pipeline · chokepoint · processing · storage |
| `capacity_nameplate_kbd` | kb/d | the asset's capacity **at the time of the event**, not today |
| `capacity_affected_kbd` | kb/d | capacity taken offline by this event |
| `days_to_partial_restore` | days | to first material resumption |
| `days_to_full_restore` | days | to pre-event capacity; `ongoing` permitted with a stamp date |

Optional — filled only where a source volunteers them, never inferred: `operator`,
`country_iso3`, `export_share_pct`, `downstream_dependency`, `alt_routing_available`,
`prior_incidents_same_asset`.

Provenance, required on every filled numeric field: `source_url`, `source_publisher`,
`source_date`.

> **THE RULE. Every figure names a source and a date, or the field stays `unknown`.**
> No estimate, no interpolation, no "approximately", no inference from a neighbouring event. An
> event with six sourced fields is worth more than an event with eighteen where one is a guess,
> because the guess is invisible downstream. This is the failure that produced `severity` — an
> unsourced analyst ordinal that Amendment C-1 now bars from carrying magnitude — and it will not
> be repeated in the variable built to replace it.

**Vintage.** `capacity_nameplate_kbd` must be the figure as of the event date, from a source
published before or contemporaneous with it where one exists; where only a later source gives the
figure, `source_date` records that and the value is flagged `retrospective: true`. Capacity changes
slowly, so retrospective capacity is admissible **as a covariate** and inadmissible for any claim
about what was knowable at *t*. A test asserts the flag is carried.

## §3 The two-stage model, registered because the naive version leaks

Realised duration is an **outcome**, not a predictor. Regressing price on realised duration would
be leakage of the class Amendment H caught. Therefore:

- **Stage 1 (vulnerability).** `duration ~ capacity_affected + capacity_share + asset_type + context`.
  Fitted walk-forward: each event predicted from events strictly before it. Published with its *n*.
- **Stage 2 (financial).** Price and margin response regressed on **predicted volume-days lost**
  from Stage 1 — never on realised duration.
- A test asserts no Stage 2 regressor derives from an outcome observed at or after the event.

## §4 The live read — the deliverable

`read(exposure) → distribution`. Given a supplied exposure conforming to §2, retrieve comparable
historical cases **by exposure similarity**, and return the duration distribution and the
price/margin distribution across the complex, each with its *n* and its reference class named. This
is the operator-supplied exposure module of a catastrophe model, and it is what makes the project an
instrument rather than a study.

**Registered constraint:** the read returns **historical frequencies with their *n*, never an
occurrence probability**, per the project's standing rule. A read with fewer than 5 comparable cases
returns `no adequate precedent` as a first-class state.

## §5 Verdict words, fixed now

- **VULNERABILITY MODELLED** iff Stage 1 beats a class-mean baseline out of sample on duration.
- **PHYSICAL MAGNITUDE CARRIES** iff Stage 2 with predicted volume-days beats the class dummy, with
  the dummy's coefficient moving toward zero when both are present.
- **NO ADDITION** is a permitted outcome for either stage and is **not** a failure of the study.
- Coverage is reported before any estimate: how many of 75 reached `COMPLETE`, and the exclusion
  table for the rest. **If fewer than 30 reach `COMPLETE`, Stage 1 is reported as descriptive only
  and no verdict is issued** — registered now so it cannot be waived later.

---

## Amendment 1 (2026-09-03) — the expanded reference class: cause becomes a covariate, not a filter
*Appended by **Session G on Joe's instruction of 2026-09-03**, before any accident-caused row is
filled. §§0–5 above are Cowork's and are unchanged; this amendment adds a class and a covariate and
changes no verdict word, no gate and no threshold. Amendments are dated and appended, never edited.*

### A1.1 Why the class expands, and why it is not a rescue of the gate

The attack-caused attempt closed at **8 `COMPLETE` of 75** against §5's registered gate of 30. **The
gate holds and Stage 1 is descriptive only.** Nothing in this amendment changes that, and no
accident-caused row counts toward the 30: §5's gate is about *the corpus*, and the corpus is the 75.

The reason to expand is the estimand, not the count. §3's Stage 1 asks
`duration ~ capacity_affected + capacity_share + asset_type + context`. **For that question the
cause of damage is a covariate, not a membership test.** A refinery with 200 kb/d offline faces
substantially the same restoration engineering whether the unit was lost to a fire, a hurricane or
a drone: the same crude unit, the same procurement, the same turnaround crews. If cause matters to
duration, that is a *finding* the model should be allowed to produce, and it cannot produce it while
cause is a filter.

### A1.2 The new field, declared before any row is filled

Every row in the expanded class carries:

| field | values |
|---|---|
| `cause` | `attack` · `hurricane` · `fire_explosion` · `technical` · `labour` · `other` |
| `cause_source` | the same per-field provenance object as every other value |

`cause` is a **declared covariate in Stage 1** and is **never** a selection criterion. Registered
consequence: any Stage 1 result must be published both with and without `cause` as a regressor, so
the reader can see what conditioning on it does.

### A1.3 What does not change

The six required fields, the six optional, **the absolute sourcing rule** (every figure names a
source and a date or the field stays `unknown`; no estimate, no interpolation, no "approximately",
no inference from a neighbouring event), the `retrospective` flag and its meaning, and §5's verdict
words. Accident-caused rows are held to the identical standard — **the point of the exercise is
lost if they are held to a lower one.**

### A1.4 The contrast is the deliverable, and it is registered as such before it is measured

The expanded class exists to be **compared**, not merely added. Registered now:

> **The completion rate is reported for each cause class side by side, on the same six required
> fields, and the difference is reported whichever way it comes out.**

The prediction Joe put on the record, and it is falsifiable: **accident-caused outages are publicly
measurable and attack-caused outages are not** — because EIA tracked accidents weekly in consistent
units with confirmed rather than forecast restoration dates, and because no belligerent contests the
figures. If the accident class completes at a rate close to the attack class's 8/75, the prediction
is wrong and that is published.

**Stated limitation, before the numbers.** The two classes differ in more than cause: the accident
set is predominantly **US** assets under **EIA and CSB** reporting mandates, and the attack set is
predominantly **not**. A completion gap therefore measures *cause confounded with reporting regime*,
and cannot separate them. That is stated here so the finding is not overread as cause alone. The
honest claim available from this design is about **the information environment**, not about
belligerents' behaviour in isolation.

### A1.5 Where it is written

`data/exposure/blocks/G_accident.json`, same schema, same per-field `provenance` model, plus
`cause`. It is a **separate file from the six corpus blocks** so that no accident row can be
mistaken for a corpus event or counted toward §5's gate.

---

## Amendment 2 (2026-09-03) — the accident block is re-run as a TEST OF ARCHITECTURE.md's central claim
*Appended by **Session G on Joe's instruction of 2026-09-03**, before any row of the re-run is filled.
Amendment 1's `cause` covariate stands unchanged. §§0–5 are Cowork's and are untouched. No row in this
block counts toward §5's gate of 30, which remains unmet at 5 and keeps Stage 1 descriptive only.*

### A2.1 What is being tested, and that it can come out against the claim

`ARCHITECTURE.md` now asserts that conflict-caused disruptions are unmeasurable for five specific
reasons — contested fields, incompatible units, forecast-not-confirmed restoration, closed archives,
category mismatch — and reports a **6 %** completion rate as the measurement of it.

**That claim is only load-bearing if accident-caused outages are measurable.** If accidents come back
at the same rate, the finding is different and much smaller: restoration data is not published for
anyone, and belligerent opacity explains nothing. Joe's instruction is explicit — *"If accidents also
come back low, say so plainly — I will rewrite the claim rather than defend it."* Registered
accordingly: **this amendment is written so the block can falsify the document that commissioned it.**

### A2.2 The target n is part of the test, not an aspiration

Joe set the target at **40–60 accident events**, on the stated expectation that EIA published weekly
capacity offline and confirmed restoration through Katrina, Rita, Ike, Harvey and Ida. Registered
before the retrieval concludes:

> **If the block cannot reach the target n at the registered sourcing standard, the shortfall is
> itself a measurement and is reported as one — with every route tested and the reason each failed.**
> Reaching a smaller n by relaxing the standard is forbidden, and reaching it by estimating any field
> is forbidden. A block of 8 honest rows falsifies the availability premise more cleanly than 50
> padded ones would confirm it.

### A2.3 The `retrospective` key is mandatory on every filled numeric

The original block template carried no `retrospective` key. That is a specification defect — Joe's,
stated as his — and it is why four events across blocks A–F are `INVALID` under
`src/exposure_schema.py`, which correctly refuses a numeric whose source postdates its event without
the flag. **Every numeric in this block carries `retrospective` explicitly**, and the validator's
verdict on this block is published rather than the block's own self-declared status.

Session G's own first pass failed this: `pes_philadelphia_fire_2019` carried
`retrospective: false` on a capacity from a source dated twelve days after the fire, with a note
arguing the source was "contemporaneous with the outage week". That was rationalisation, the
validator caught it, and it is corrected in this re-run rather than defended.

### A2.4 Same standard, no exceptions

Six required fields, six optional, the absolute sourcing rule, per-field provenance. Aggregate
regional figures are **never** written into an asset's `capacity_affected_kbd`; they are recorded in
`capacity_units_note` with their quote. A route that returns aggregate data is recorded as tested and
**not** as a partial success.

### A2.5 The deliverable

The side-by-side completion rate, accident against attack, **on the same schema and the same
standard, computed by `src/exposure_schema.py` and not by this session's own count** — because a
session marking its own work complete is not evidence, which is that validator's stated design
principle. Both the COMPLETE rate and the per-field rate are reported, because Amendment 1 already
found they say different things.
