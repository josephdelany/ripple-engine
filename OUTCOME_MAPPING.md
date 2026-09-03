# OUTCOME MAPPING — independent codings to the four branches (PATH Step 4, registered before code)
*2026-09-02. Fixes, before any join is run, how a corpus event is matched to ICB, MID and
UCDP, how each source's codes map to CONTAINED / LIMITED_RETALIATION / WIDENING /
RESOLUTION_BY_DEAL, which source takes precedence, how agreement with the corpus-derived
`sr_outcome_90` is scored, and what the audit decides. Amendments are dated and appended.
Nothing here changes any branch until Joe's audit is recorded (`data/audits/outcome_audit_60.csv`).*

## 1. What is being compared
- **Ours:** `events.sr_outcome_90` — the +90-day branch derived by `situation_record.py` from
  subsequent corpus events in the same dyad (corpus-derived, never source-audited; every
  surface says so).
- **Theirs:** professionally coded outcomes from datasets that never saw our corpus:
  ICB v16 (crisis level), COW Dyadic MID 4.03 (dispute level, to 2014), UCDP/PRIO v26.1
  (conflict-year, location country). Their constructs differ from ours (a crisis or dispute
  is an episode; ours is a 90-day window). The mapping states the construct it uses; κ is
  reported per source and pooled, and the audit — not the number — decides.

## 2. Matching a corpus event to an independent record (deterministic, in this order)
Let `d` = the event's `event_date`; `A` = the set of mapped `country.*` entities of the event
(actor/target from the situation record, plus every coded `event_entities` country); `P` =
the actor–target pairs among them (all pairs if roles are unknown).
- **ICB.** A crisis matches if `d ∈ [trigdate − 30 d, termdate]` and at least one crisis
  actor (ICB2 `cracid` → COW code) or one crisis dyad state (ICB Dyads `statea`/`stateb`)
  is in `A`. If several match, the one with the latest `trigdate ≤ d + 30 d`, else the
  nearest `trigdate`. Record `crisno`, `crisname`, `viol`, `sevviosy`, `forout`, `outesr`,
  `gpinv`, `globactm`, `trigdate`, `termdate`.
- **MID.** A dyadic dispute matches if its dyad is in `P` (or, when roles are unknown, both
  states are in `A`) and `d ∈ [start − 30 d, end + 90 d]`. Prefer the dispute whose start
  is nearest `d`. Record `disno`, `hihost`, `fatlev`, `outcome`, `settlmnt`, start/end.
- **UCDP.** For each location country in `A`: the conflict-year rows of year(`d`) and
  year(`d`)+1 (the +90-day window can cross a year end). Record max `intensity_level` in
  each year and the sum of `bd_best` where BRD exists (1989→).
- An event with no match in any source is flagged `no_independent_outcome` and counts as
  such in the report — never dropped, never guessed.

## 3. Mapping each source's codes to the four branches (total and deterministic)
**ICB (crisis level):**
| condition (evaluated top-down) | branch |
|---|---|
| `forout ∈ {1, 2}` (formal / semi-formal agreement) and `viol ≤ 2` | RESOLUTION_BY_DEAL |
| `viol = 4` (full-scale war) | WIDENING |
| `viol = 3` (serious clashes) | WIDENING if `outesr = 1` (escalation of tension) else LIMITED_RETALIATION |
| `viol = 2` (minor clashes) | LIMITED_RETALIATION |
| `viol = 1` (no violence) | CONTAINED |
| `viol` missing | no label from ICB |

**MID (dispute level):**
| condition | branch |
|---|---|
| `hihost = 5` (war) | WIDENING |
| `hihost = 4` (use of force) and `fatlev ≥ 3` (≥ 101 deaths) | WIDENING |
| `hihost = 4` | LIMITED_RETALIATION |
| `hihost ∈ {2, 3}` (threat / display) and `settlmnt = 1` (negotiated) | RESOLUTION_BY_DEAL |
| `hihost ∈ {1, 2, 3}` | CONTAINED |

**UCDP (conflict-year, location country):** let `i0` = max intensity in year(`d`)−1,
`i1` = max intensity across year(`d`) and year(`d`)+1 (0 when no conflict row).
| condition | branch |
|---|---|
| `i1 = 2` (war) and `i0 < 2` | WIDENING |
| `i1 = 2` and `i0 = 2` | LIMITED_RETALIATION (a war that continued) |
| `i1 = 1` | LIMITED_RETALIATION |
| `i1 = 0` | CONTAINED |
UCDP carries no negotiated-settlement code in the conflict-year file; RESOLUTION_BY_DEAL is
never assigned from UCDP (the Peace Agreements dataset is a later loader).

## 4. Precedence and the independent label
`independent_outcome` = ICB's branch when an ICB crisis matched; else MID's; else UCDP's;
else `no_independent_outcome`. The per-source labels are all stored
(`event_outcomes(event_id, source, field, value)`), so κ is computed per source as well as
for the precedence label.

## 5. Agreement
Cohen's unweighted κ over the four branches on events that carry both `sr_outcome_90`
(not "unknown") and an independent label; the 4×4 confusion table published beside it;
n stated. Computed by code, tested on a synthetic table with a hand-computed κ.
Decision rule (PATH Step 4): **if κ < 0.6 on the precedence label, our branches are replaced
by the independent ones** — after, and only after, the 60-event audit is recorded.

## 6. The audit sheet (Joe)
`data/audits/outcome_audit_60.csv`: the 60 disagreements (all of them if fewer), stratified
proportionally by event class and era (1946–86 / 1987→) with a fixed seed, one row each:
event, date, class, title, source URL, our branch, the independent branch and source, the
ICB/MID/UCDP codes behind it, and blank `joe_branch` / `joe_note` columns. Joe fills them
from sources. Nothing in `events` or the situation records changes in this step.

---

## Amendment 1 (2026-09-02) — `sr_outcome_90` retired as an outcome; IES-90 replaces it
*Registered before any code. Nothing in `events`, the situation records or any other
registered file changes. §1–§6 above stay as the record of what was tried; §5's decision
rule is superseded by this amendment.*

### A1.1 What the record shows
Step 4 ran as registered (`data/state/outcomes_kappa.json`, generated 2026-09-02T15:46Z):
κ = −0.001 against ICB (n 43), −0.234 against MID (n 15), 0.104 against UCDP (n 184),
0.061 on the precedence label (n 184); 114 disagreements, 60 in `outcome_audit_60.csv`.
Two defects, both structural, neither fixable by auditing rows:
1. **Our coder is biased to CONTAINED by corpus sparsity.** `sr_outcome_90` reads "no later
   corpus event in the dyad within 90 days" as CONTAINED (115 of 187). The corpus is a
   curated list of oil-relevant events, not a record of what happened next; absence of a
   corpus row is absence of evidence.
2. **§3's mappings answer a whole-episode question.** ICB `viol` is the crisis's peak
   violence over its whole life, MID `hihost` the dispute's, UCDP `intensity_level` the
   calendar year's. None is dated to the 90 days after `d`. The two sides of κ measured
   different things, so the audit sheet could not adjudicate them.
**Decision.** `sr_outcome_90` (and `sr_outcome_30`) are retired as outcomes. The columns
stay in `events` untouched; any surface that still shows them says "corpus-derived, retired
2026-09-02". The κ < 0.6 replacement rule is moot — there is no episode label to replace
with. The κ report and the 60-row sheet are kept for the record and are no longer a gate.

### A1.2 IES-90 — the Independent Escalation Scale over (d, d+90]
For a geopolitical event (types `conflict_escalation`, `infrastructure_attack`,
`chokepoint_disruption`, `sanctions`) with `event_date` = `d`, the window is
**W = (d, d+90]** (day precision; when `date_precision` is week/month, `d` is the recorded
date and the row says so). `A` and `P` are as in §2; `L` (location set) = the event's
`location` ∪ `target` role entities, else `A`.

**Level** (an ordinal reached *in W*, not a change from before W):

| level | meaning |
|---|---|
| 0 | none — a covering source has no dated record in W |
| 1 | threat or display of force |
| 2 | use of force |
| 3 | war |

**DEAL flag**: a dated negotiated termination in W (1/0; null when neither ICB nor MID
covers W).

**Per-source rules — each source yields a dated level for W or nothing.** "Covers" means
the whole of W lies inside the source's period and the event has ≥ 1 mapped country.

| source | period (covers) | record counts when | level |
|---|---|---|---|
| **MIDI/MIDIP 5.0** (incident) | 1993-01-01 ≤ d and d+90 ≤ 2014-12-31 | incident participants (MIDIP `ccode` → `countries.py`) contain both members of a pair in P on opposite sides (`sidea` differs); if P is empty, ≥ 1 participant in A; incident dates [st, end] ∩ W ≠ ∅ (unknown day −9 → 1; unknown end → start) | max `hostlev`: 1→0, 2→1, 3→1, 4→2, 5→3 |
| **Dyadic MID 4.03** (dispute) | d+90 ≤ 2014-12-31 | dyad ∈ P (both states in A when P empty; either state when \|A\| = 1) and [start, end] ∩ W ≠ ∅ | start ∈ W → `hihost` 1→0, 2→1, 3→1, 4→2, 5→3; start ≤ d and `hihost` = 5 → 3 ("war ongoing"); start ≤ d and `hihost` ≤ 4 → **no level** (the force is undated inside W; the record is kept as detail) |
| **COW war dates** | = Dyadic MID `war = 1` rows | the war dyad's dispute dates are the COW war dates used; the standalone COW War v4 file is not loaded (register: pre-1946 tail only; corpus starts 1973) | as Dyadic MID `hihost` = 5 |
| **ICB v16** (crisis) | 1918-01-01 ≤ d and d+90 ≤ 2021-12-31 | crisis members (ICB2 `cracid`, Dyads `statea/stateb`) ∩ A ≠ ∅ | `trigdate` ∈ W → `viol` 1→1, 2→2, 3→2, 4→3; `trigdate` ≤ d < `termdate` and `viol` = 4 → 3 ("war ongoing"); otherwise **no level** |
| **UCDP GED 26.1** (events, location only) | 1989-01-01 ≤ d and d+90 ≤ 2025-12-31 | state-based events (`type_of_violence` = 1) with `date_start` ∈ W and `country` ∈ L (GED names → `countries.py` by the table in `ies90.py`; unmapped names are listed in the distribution file, never dropped silently) | D = Σ `best`: D ≥ 250 → 3 (UCDP's 1,000-deaths/yr war line pro-rated: 1000 × 90 / 365 = 246.6); 25 ≤ D < 250 → 2 (UCDP's own inclusion threshold, unprorated as a floor); D < 25 → 0. Also stored, never used for the level: D over (d−90, d] (`deaths_ged_pre90`) and the one-sided/non-state sum |

The cached GED (`data/cache/ucdp_ged_26.1.json`) carries only date, country, deaths and
type; there is no dyad field and no `UCDP_TOKEN` in this environment to re-pull one, so GED
is a **location** source: deaths in the country, not deaths between the event's actors. Every
GED-set level says so in its detail. This is the largest known weakness of IES-90 and is
why `deaths_ged_pre90` is stored beside it.

**Precedence.** `ies90_level` = max of the covering sources' levels. `level_source` = the
source(s) attaining that max (ties listed in the order MIDI, ICB, MID, GED). Level 0 is
asserted only when ≥ 1 source covers W and none records anything; when **no source covers
W** the event is `no_independent_outcome` (level null, never guessed). 2026 events are
therefore uncovered (GED ends 2025-12-31; MID 2014; ICB 2021).

**DEAL.** 1 if ICB `termdate` ∈ W with `forout` ∈ {1, 2}, or a Dyadic MID `end` ∈ W with
`settlmnt` = 1; 0 if ICB or MID covers W and neither fires; null otherwise.

### A1.3 Outputs
- `event_outcomes` rows with `source = 'ies90'`: `level`, `deal`, `level_midi`, `level_mid`,
  `level_icb`, `level_ged` (present only when the source covers W), `deaths_ged_90`,
  `deaths_ged_pre90`, `deaths_ged_other_90`, `covering` (text), `level_source` (text),
  `no_independent_outcome` (1.0 when uncovered); `detail` lists the source records (ids,
  dates, codes) that produced the level. Rows of other sources are untouched.
- `data/state/ies90_distribution.json`: level by decade, level by class, DEAL by decade,
  `no_independent_outcome` by decade, coverage by source, unmapped GED names, and — for the
  record only — the cross-table of IES-90 against the retired `sr_outcome_90`.
- `data/audits/ies90_audit_30.csv`: 30 events with a level, stratified by level × decade
  (largest remainder, seed 20260902), each event row followed by the source rows that
  produced its level, with blank `joe_check` / `joe_note`. Joe checks the source rows
  against the sources; he does not code.
- `data/state/outcomes_kappa.json` and `data/audits/outcome_audit_60.csv` stay as the record.

### A1.4 What IES-90 does not claim
It is not attribution: a level from GED is violence in the location, from ICB a crisis the
country was in. It is not a change score. It is not available after 2025-12-31, or between
2015 and 2021 from anything but ICB and GED, or after 2021 from anything but GED. Those
gaps are published, not filled.

### Amendment 1.1 (2026-09-02, before the IES-90 code is committed) — dated war, not episode peak
A first run of the A1.2 rules on the corpus showed the "war ongoing at d" clauses re-importing
the whole-episode defect: ICB codes the Gulf crisis `viol` = 4 from 1990-08-02, but the war
began 1991-01-17; Dyadic MID's `hihost` = 5 likewise dates the dispute, not the war. A
crisis or dispute that merely *starts* in W has the same problem — `viol`/`hihost` is its
later peak. Three rules change; nothing else in A1.2 does.
1. **COW War v4 is loaded** (keyless; `data/state/raw/cow_war/`): Inter-State War v4.0
   (1816–2007-12-31) and Intra-State War v4.1 (1816–2014-12-31), each with dated spells
   (`Start*1..End*1`, and `*2` when present; unknown month/day −9 → 1; an end coded as
   ongoing → the period end). A war spell overlapping W gives **level 3**: inter-state when
   the participants contain both members of a pair in P on opposite sides (`Side`), or when
   P is empty any participant in A; intra-state when a state party (`CcodeA`/`CcodeB`) ∈ L.
   The A1.2 shortcut "COW war dates = Dyadic MID `war` = 1 rows" is withdrawn.
2. **ICB** asserts a level only where it can date it: a crisis **wholly inside W**
   (`trigdate` ≥ d+1 and `termdate` ≤ d+90) → `viol` 1→1, 2→2, 3→2, 4→3; a crisis
   **triggered in W that ends after W** → level 1 (the onset — a perceived threat — is
   dated; `viol` is recorded as the undated peak); a crisis **ongoing at d** → no level (the
   record is kept as detail). The DEAL rule is unchanged (`termdate` ∈ W and `forout` ∈ {1, 2}).
3. **Dyadic MID** the same way: a dispute wholly inside W → `hihost` 2→1, 3→1, 4→2, 5→3; a
   dispute starting in W and ending after → level 1 (a MID begins with a militarized action,
   at least a threat); ongoing at d → no level. Rows are de-duplicated to one per
   (dispute, dyad) — the file carries both directions and one row per dispute-year — taking
   the max `hihost` and the last year's `settlmnt`/end. The DEAL rule is unchanged.
Coverage now: MIDI 1993–2014, COW war 1816–2007 (inter) / 1816–2014 (intra), ICB 1918–2021,
MID 1816–2014, GED 1989–2025. Tie order for `level_source`: MIDI, war, ICB, MID, GED.
The first run also showed **24 of 27 uncovered events carry no `country.*` entity at all**
(chokepoint- or facility-only codings: Bab el-Mandeb, Hormuz, Suez, pipelines). They stay
`no_independent_outcome`; a chokepoint → littoral-state map is a candidate Amendment 2, not
made here.

---

## Amendment 2 (2026-09-02, registered before the rebuild) — dyadic precedence, littoral map as location, rule-fired column
*Applies to IES-90 (Amendment 1 + 1.1). Nothing in `events` changes. Field names the walk
reads (`level`, `deal`, `no_independent_outcome`) are unchanged.*

### A2.1 Dyadic precedence
A source record is **dyadic** when it was matched through a pair in P: a MIDI incident with both
members on opposite sides, a COW inter-state war with both members on opposite sides, a Dyadic MID
row whose dyad ∈ P, an ICB crisis with ≥ 2 members of the pair among its actors. A record is
**location** when it was matched through a single country or a location set: GED (always), COW
intra-state (always), and any MIDI / MID / COW inter-state / ICB record matched because P was
empty (single-country events) or through one member only.
- If **any dyadic-capable source covers W and P is non-empty**, `ies90_level` = max over the
  *dyadic* records; `basis = 'dyadic'`. Location records are still stored (`level_location`)
  and shown in the audit, but do not set the level. A dyadic-covered event with no dyadic record
  in W is level 0 on the dyadic basis, whatever the location sources say.
- Otherwise (P empty, or no dyadic-capable source covers W) `ies90_level` = max over the
  location records; `basis = 'location'`. Every location-basis level says so on every surface.
- `covering` is split into `covering_dyadic` and `covering_location`. `no_independent_outcome`
  is unchanged: no source of either kind covers W.
Why: a location source answers "was there violence in the country", not "did this dyad
escalate"; under Amendment 1 a 2024 sanctions event on Russia read as war from GED deaths in
Ukraine. Dyadic evidence, where it exists, is the question being asked.

### A2.2 Littoral map — location only
A chokepoint or facility entity on the event adds its littoral or host states to **L only**
(never to A or P), so GED and COW intra-state can cover events coded without a country. The map
is fixed here and checked by a test; states not in `countries.py` are named but not mapped:
| entity | L gains | not mapped (no `country.*` id) |
|---|---|---|
| `chokepoint.hormuz` | iran, uae, omn | — |
| `chokepoint.bab_el_mandeb` | yemen | Djibouti, Eritrea |
| `chokepoint.suez`, `chokepoint.suez_canal` | egypt | — |
| `chokepoint.gibraltar_strait` | gbr | Spain, Morocco |
| `chokepoint.malacca` | indonesia | Malaysia, Singapore |
| `chokepoint.taiwan_strait` | taiwan, china | — |
| `chokepoint.libya_es_sider` | libya | — |
| `chokepoint.kirkuk_ceyhan_pipeline` | iraq, turkey | — |
| `chokepoint.druzhba_pipeline` | russia, ukraine, hungary | Belarus, Poland, Slovakia, Czechia |
| `chokepoint.cpc_novorossiysk` | russia, kazakhstan | — |
A level reached only through the littoral map is location-basis by construction and its detail
names the entity that supplied L.

### A2.3 Rule-fired column
Every `ies90` level row carries `rule_fired` (value_text): the identifier of the registered rule
that set the level — `MIDI.pair.overlap`, `MIDI.single.overlap`, `WAR.inter.pair`,
`WAR.inter.single`, `WAR.intra.location`, `ICB.pair.wholly`, `ICB.pair.onset`, `ICB.single.wholly`,
`ICB.single.onset`, `MID.pair.wholly`, `MID.pair.onset`, `MID.single.wholly`, `MID.single.onset`,
`GED.location.ge250`, `GED.location.ge25`, `NONE.covered` (a covering source, nothing in W) —
with ties listed in the A1.1 order. The audit sheet gets the same column on every source row,
plus `basis`. `UNCOVERED` is written on `no_independent_outcome` rows.
Outputs: `event_outcomes` source='ies90' fields `basis`, `rule_fired`, `level_location`,
`covering_dyadic`, `covering_location` (alongside the Amendment 1 fields);
`data/state/ies90_distribution.json` adds level × basis and rule_fired counts;
`data/audits/ies90_audit_30.csv` is regenerated with `basis` and `rule_fired` columns.

---

## Amendment 3 (2026-09-02, registered before any count is computed under it) — the hostility precondition on the G target
*Session F. Applies to IES-90 (Amendments 1, 1.1, 2). Nothing in `events` changes; no
class is re-coded; no published run is altered. This amendment states a rule and the
grounds for it. **Session B implements it in v3**, not here — the numbers in §A3.6 below
were computed after this text was committed, and are reported as an impact estimate, not
as a re-scored run.*

### A3.1 The defect
IES-90 asks a source what escalation was recorded in W = (d, d+90] near an event. It never
asks whether the event was a **hostile act at all**. The four geopolitical classes
(`conflict_escalation`, `infrastructure_attack`, `chokepoint_disruption`, `sanctions`) are
assumed hostile by their names, and the assumption is false: `infrastructure_attack` and
`chokepoint_disruption` are coded in EVENTS_CODEBOOK by *what was disrupted*, not by *who
did it or whether anyone did*. A refinery fire, a grounded ship, a storm, a blackout, a
pipeline contaminated to cover an oil theft, a strike, and a mine collapse are all in
those two classes today.

For such an event the G target is not merely noisy — it is **undefined**. There is no dyad,
no actor, and no escalation of anything. What IES-90 returns is whatever violence the
covering sources happened to record in the country during the following 90 days: a location
reading of the neighbourhood, attached to an event that has no adversary. Two examples from
the record: `iran_oilworkers_strike_1978` (an oil-workers' strike) is scored **level 3 —
war**, from the Iranian Revolution's intra-state war spell overlapping W;
`druzhba_contamination_2019` (contamination injected at a Samara collection point to cover
the theft of on-spec crude) is scored **level 2 — use of force**, from GED deaths in Russia
in that window. Neither number is about the event.

This is the same failure Amendment 2 identified for the dyadic/location distinction, one
level down: Amendment 2 fixed *which* record may set a level; this fixes *whether the event
has a level to set*.

### A3.2 The precondition (the rule)
**An event is G-scorable only where the record shows a hostile act.** Formally, for an event
in the geopolitical classes, IES-90 is computed only if both hold:

- **(H1) Hostile act.** The event record (title, description, sources) shows a *deliberate
  act, directed adversarially* at a state, its people, its territory, its infrastructure, or
  at shipping — armed attack, bombing, sabotage of an adversary's asset, mining, armed
  blockade, forcible seizure or interdiction of a vessel, or an explicit threat or display
  of force.
- **(H2) Identified party.** The record names the acting party at least to the level of an
  actor *class* that a covering source could carry: a state, a named armed group or
  movement, or a party the covering record itself names. A perpetrator that is *disputed
  between named candidates* satisfies H2 (the act is hostile on every candidate account);
  a perpetrator that is *simply unknown* does not.

An event failing H1 returns **`no_independent_outcome`** and is excluded from G-scoring and
counted — exactly as the three non-geopolitical classes (`opec_decision`, `demand_shock`,
`policy_response`) already are, and by the same logic: the target is not defined for them.
An event satisfying H1 but failing H2 is scored as now and carries
`hostility = 'hostile_unattributed'` on every surface, so the alternative reading (excluding
it too) can be read off the published counts without a re-run. **Failing the precondition is
not a data-quality flag and never becomes one**: it is a statement that the G question does
not apply to this event, not that the event is doubtful.

### A3.3 Coding the precondition (deterministic, from the record only)
Every event in the geopolitical classes carries a `hostility` value, assigned by reading the
record — never by keyword, and never from the outcome:

| value | rule | G-scorable |
|---|---|---|
| `hostile` | H1 and H2 hold | yes |
| `hostile_unattributed` | H1 holds, H2 fails (deliberate hostile act, no party named anywhere in the record) | yes, flagged |
| `non_hostile` | H1 fails: the cause the record gives is an accident, a natural hazard, a technical or industrial failure, a labour action, a commercial or legal action, or a crime committed for private gain rather than against an adversary | **no** — `no_independent_outcome` |
| `ambiguous` | the record is genuinely contested between hostile and non-hostile, or the act is coercive but not adversarial (a defensive or precautionary state decision, a protective deployment) | **no** — `no_independent_outcome`, listed by name |

Three tie-breaks, fixed here so they are not chosen later against a result:
1. **A hostile act with a contested perpetrator is `hostile`, not `ambiguous`**, when every
   candidate account is a hostile act (e.g. a bombing claimed by one party and attributed by
   others to a second). It is `ambiguous` when one of the live accounts is an accident.
2. **A defensive or precautionary response to someone else's hostile act is not itself a
   hostile act.** The antecedent attack is the hostile event; a suspension of sailings, a
   protective escort, or a shutdown ordered by the operator is not.
3. **Crime for private gain is `non_hostile`** however deliberate, unless the record shows it
   was directed at an adversary as an adversary.

The coding is published in full, event by event with its evidence, in
`data/spine/CLASS_AUDIT.md`, and is checked by `tests/test_hostility.py`. It is a *reading of
the existing record*: no event's class, description, entities or sources change, and nothing
enters the `events` table.

### A3.4 Expected effect on n
Applying the precondition **reduces n for G and never increases it.** In the two classes
audited under this amendment (75 events), 9 are `non_hostile` and 5 are `ambiguous`, so at
most 14 of 75 leave G-scoring; the equivalent audit of `conflict_escalation` and `sanctions`
is not yet done and may remove a few more. (Those two counts come from the audit that
*grounds* this amendment — the defect in §A3.1 was found by reading the records before the
rule was written, and the rule was written to fit the defect, not the other way round. No
**score** was computed under the rule before this text was committed; the walk numbers in
§A3.6 came after.) The G walk's scored n falls by the number of
those events that clear the walk's own filters (daily tier, burn-in, both engine and
climatology scored); the measured figure is in §A3.6. n for P is **unaffected** — a price
response to a storm or a grounding is a real price response, and the P target does not
presuppose an adversary. Nothing else in IES-90 changes: no window, no source, no
precedence rule, no level mapping.

The loss is not a cost to be minimised. Every read removed was a read against a target that
did not exist for that event, and a share of them were level 0 by construction — an event
with no adversary is unlikely to have a dyadic record in W. Removing them therefore moves
the base rate. Whether that makes the engine look better or worse against climatology is
**not** a consideration in adopting the rule and must not become one; both figures are
published in §A3.6 as computed.

### A3.5 No retroactive application
**This amendment cannot be applied to any published run retroactively.** The sealed reads in
`data/walk_forward/reads.jsonl` were made against the target as it stood, and the scores in
`scores.jsonl` and `summary.json` are the record of that. A run is not re-scored under a
later target definition: doing so would break the seal (WALK_FORWARD_PROTOCOL §7) and would
let a definition be chosen after its effect on the score is known — the exact move
SESSION_CHARTER §2 rule 2 exists to prevent.

Therefore:
- The published run stands as published, with its n and its scores unchanged.
- Every surface reporting G results from a pre-amendment run carries the note: *"scored
  before Amendment 3; includes N non-hostile events for which the G target is undefined"*,
  with N and the receipt path from §A3.6.
- The precondition takes effect for **runs made after B implements it in v3**, and those
  runs are reported separately from the pre-amendment run — never pooled with it, and never
  presented as a correction to its numbers.
- The paper's limitations section states the defect, the affected count, and the direction
  of the effect on the level-0 share (§A3.6), rather than showing a corrected result.

### A3.6 Impact on the published run — measured, reported, not applied
Computed after this amendment was committed, over the 150 daily-tier scored G reads of run
`walk_20260902T210135Z` (`data/walk_forward/summary.json`, `/tiers/daily/G`). Numbers are in
`data/spine/CLASS_AUDIT.md` §5 with their receipt; they change nothing in the run.
