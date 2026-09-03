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

### Amendment 3.1 (2026-09-02, approved by Joe; registered before the remaining two classes are coded) — the field is canon, and the precondition waits for all four classes
Joe approved §A3.2's precondition and CLASS_AUDIT §7.5's recommendation: a **`hostility`
field**, not new `events.type` values. Registered in `EVENTS_CODEBOOK.md`, amendment
2026-09-02, with the four values, the coding rules and the tie-breaks; the machine
identifiers stay the §A3.3 ones (`hostile`, `non_hostile`, `ambiguous`,
`hostile_unattributed`) and the codebook's hyphenated spellings are their display forms.
The `type` enum stays at seven values and nothing in `events` changes.

Two consequences, fixed here rather than left to whoever implements:
1. **The field is required on all four geopolitical types** (`conflict_escalation`,
   `infrastructure_attack`, `chokepoint_disruption`, `sanctions`) and is null-and-not-
   applicable on the other three, which never claimed to be hostile acts.
2. **The precondition is not implemented until all four are coded.** Implementing it while
   only two classes carry the field would exclude non-hostile events from two classes and
   silently keep them in the other two — a worse state than today, because the inconsistency
   would be invisible in the output. `src/engine/**` and `src/walk.py` are Session B's;
   the handoff carries this as a blocking condition with the outstanding count.

### Amendment 3.2 (2026-09-02, registered before `conflict_escalation` and `sanctions` are coded) — H1 for the other two classes: four cases the original wording does not decide
*A3.2's H1 was written from the two classes then audited, both of them about physical damage,
and its examples are all kinetic. Reading the other two geopolitical classes turned up four
kinds of event that H1's head clause and its example list answer differently. Deciding them
inside the audit would be choosing a definition with the events in view, so they are decided
here first. Nothing in `events` changes and no count has been computed under these rules.*

**The head clause governs; the list illustrates.** H1 is *"a deliberate act, directed
adversarially at a state, its people, its territory, its infrastructure, or at shipping"*.
The examples after the dash — attack, bombing, sabotage, mining, blockade, seizure, threat or
display of force — are the forms that arise in `infrastructure_attack` and
`chokepoint_disruption`. **They are not a closed list, and H1 does not require violence.**
The question the precondition asks is whether the event is an adversarial act between
identified parties, because that is what makes "did this escalate in the next 90 days" a
question with a subject. Four rules follow.

**(a) Non-kinetic state coercion satisfies H1.** An embargo, a sanction, an export ban aimed
at a named state, a secondary tariff, a trade blockade: a deliberate act directed
adversarially at an identified state. `sanctions` is one of the four geopolitical types
precisely because it is state-on-state coercion, and IES-90's question — did this dyad reach
force in W — is well posed for it.

**(b) Relief and settlement inside a live adversarial dyad satisfy H1, and are marked.**
A sanction lifted, a waiver granted, a deal signed, an embargo ended. The *act* is
de-escalatory, but the dyad is identified and adversarial, and both the level and the DEAL
flag are defined for it. Excluding them would delete precisely the events the DEAL flag
exists to measure, and would bias the corpus toward escalation by construction — a worse
error than the one this amendment corrects. Such rows carry **`de_escalatory = 1`** so the
direction of the act is never lost inside a `hostile` value.
Consequently `hostile` on this field means **"an adversarial act, or a dated act inside an
identified adversarial dyad"**. It does not mean violent, and no surface may render it as
"violent". The four values stay exactly as Joe approved them.

**(c) Domestic industrial and commercial action fails H1 → `non_hostile`.** A strike, a wage
dispute, a community road blockade, a mine occupation, and a producer's own export
restriction taken for domestic price, supply or industrial-policy reasons. The counterparty
is an employer, a mine operator or a domestic market — not an adversary. This is the same
tie-break 3 (`crime for private gain`) generalised: a coercive act with a commercial
counterparty is not an act of foreign policy. Where such a restriction **names a state** it
is (a), not (c).

**(d) Seizure of power and armed uprising satisfy H1.** A coup, a revolution, an insurgency
taking territory, a violently repressed national uprising: a deliberate act directed
adversarially at a state, by a party the record identifies at least as a class (the army, a
named movement, the security forces). A **political turning point inside** such a conflict
that is not itself an act of force — a ruler leaving the country — is `ambiguous`, by the
same logic as tie-break 2.

**One consequence to state plainly.** Under (a) and (b), essentially the whole `sanctions`
class stays G-scorable, and the precondition removes far less there than it does from the
two classes audited first. That is the correct result and not a weakening: sanctions were
never the events with no adversary. The events with no adversary are storms, groundings,
accidents, strikes and price-management export bans — and they are scattered across three of
the four geopolitical classes, which is the finding.

### Amendment 3.3 (2026-09-02, ruled by Joe) — `ambiguous` is terminal, and the diagnostic publishes both ways
*Closes the last gate this audit left open. Nothing in `events` changes and no count moves.*

**1. `ambiguous` is a terminal value, not a pending decision.** Where the record does not
settle whether an event was an adversarial act, `ambiguous` **is the answer** — the same
status as an `unknown` state field or a `low` confidence, and governed by the same rule
(SESSION_CHARTER §2.1, sourced-or-unknown). Adjudicating the thirteen anyway would supply a
fact the evidence lacks, which is the failure mode this project's whole registration
discipline exists to stop; it would also mean a target definition being settled by judgement
after the results were in view.
- **No session re-codes an `ambiguous` event to clear it**, and no surface, checklist, gate
  report or handoff lists them as outstanding. `ambiguous` is not a Joe gate.
- The **only** thing that moves an event out of `ambiguous` is **new evidence in the record**:
  a source that settles the cause, or a Session E patch that unbundles a row holding two acts
  (three of the thirteen are of that kind). The move is then a normal re-coding under the
  registered rule, published with the evidence that caused it — never a decision to stop
  having an awkward value.
- `ambiguous` remains **not G-scorable** (§A3.3 unchanged): it returns
  `no_independent_outcome` and is counted.

**2. Every diagnostic of the G target publishes the level-0 share with and without the
`ambiguous` events.** Because the value is terminal, whether to count those events can never
be settled by evidence, so both bounds are reported as a matter of course — in
`data/spine/CLASS_AUDIT.md` §6, in `data/walk_forward/summary.json` when B implements the
precondition, and on any surface that reports a G outcome distribution. The registered rule
excludes `ambiguous`, so the share **under Amendment 3** is the one that drops only
`non_hostile`; the also-without-`ambiguous` figure is published beside it as the other bound,
never instead of it. A single-figure report of this target is incomplete, and the audit's test
asserts both figures are present.

---

## Amendment 4 (2026-09-02, registered before any count is computed under it) — the ongoing-conflict rule reaches COW War and UCDP GED, and "no level" stops meaning "level 0"
*Session K, under the ownership carve-out in SESSION_CHARTER §1. Applies to IES-90
(Amendments 1, 1.1, 2) and is orthogonal to Amendment 3 (F's hostility precondition asks
whether the **event** is a hostile act; this asks whether the **record** can date an
escalation inside W — an event can fail either, and the two exclusions are counted
separately and never merged). Nothing in `events` changes; no class is re-coded; no
published run is altered. This text was committed **before** the code that implements it
and before any count under it was computed.*

### A4.1 The defect, verified

Red team 2 finding 3 (`docs/red_team_2.md`:64–83, Tier A5) says most level-3 "war" labels
are wars that were already on before the event. Session K re-derived it rather than taking
it on faith. Everything below was executed today against `event_outcomes` (source `ies90`)
and the GED 26.1 cache; the scripts are in the session log and the receipts are the SQL and
the `detail` column itself.

**The scale as built.** 187 geopolitical events, 184 with a level, 3 `no_independent_outcome`.
Levels: **0 → 76, 1 → 6, 2 → 48, 3 → 54.**

**(i) The false threes — confirmed.** All 54 level-3 labels come from COW War (15), UCDP GED
(38) or both (1) — exactly the two sources Amendment 1.1's "ongoing → no level" carve-out
was written for ICB and Dyadic MID and never extended to. Of the 54, **34 carry a stored
`deaths_ged_pre90` ≥ 250** (the remaining 10 with the field below the line, 10 more pre-dating
GED coverage entirely). Of the 38 GED-set level 3, **31** have stored `deaths_ged_pre90` ≥ 250.
Of the 16 COW-war-set level 3, **14** sit inside a war spell that started on or before `d`
— Desert Storm 1991 is scored 3 from the Gulf War spell that began 1990-08-02, five and a
half months before the event, while ICB crisis 393 and MID dispute 3957 both correctly
returned *"ongoing at d, violence undated in W (no level)"* for the same war. One rule said
"no level" and another said "war", about the same fact, in the same row.

**(ii) A correction to the field the finding rests on.** `deaths_ged_pre90` is summed over
`[d−89, d]` — **inclusive of the event day itself** (`ies90.py` `score_ged`, the one place
the field is written and the only place it is used). For an event whose own day is the
violent one, the "before" figure is mostly the event. Recomputed strictly before `d`:

| event | `deaths_ged_pre90` as stored | strictly before `d` | on `d` itself |
|---|---:|---:|---:|
| `russia_invades_ukraine_2022` | 20,473 | **79** | 20,394 |
| `israel_hamas_war_2023` | 3,835 | **28** | 3,807 |
| `israel_iran_war_2025` | 959 | **4** | 955 |
| `me_rough_rider_2025` | 537 | **173** | 364 |

So the two headline examples of "a war that was already running" are the opposite: they are
war *onsets*, and the level 3 on them is correct. The count of GED-set level 3 with ≥ 250
deaths genuinely before the event is **27 of 38, not 31**; over all 54 it is **34 as stored
and lower strictly before**. The defect is real and large; the specific arithmetic in the
brief and in red team 2 §A5 overstates it for four events, and this amendment records that
rather than repeating it.

**(iii) The false zeros — the same defect, opposite sign, not previously reported.**
Amendment 1.1 made an ongoing ICB crisis or MID dispute yield *no level*. But `score_event`
takes `max(..., default=0)`, so an event whose only records are undated-for-W falls through
to **level 0 = "none — a covering source has no dated record in W"**. That statement is
false: the source has a record, and cannot date it. **18 events are scored 0 this way**,
including the two most consequential geopolitical oil events of their decade:

- `abqaiq_attack_2019` → level 0, from ICB crisis 496 ABQAIQ OIL STRIKE and crisis 474
  HOUTHI REBELLION, both "ongoing at d".
- `soleimani_strike_2020` → level 0, `level_source = icb`, `rule_fired = NONE.covered` —
  while GED recorded **177 state-based deaths in Iran/Oman/UAE inside W against 0 in the
  pre-window**. Amendment 2's dyadic precedence handed the level to ICB, ICB could not date
  it, and the fresh location evidence was discarded. `level_source = icb` on a row where ICB
  set nothing is itself incoherent.

**(iv) Why this is one defect and not three.** A level-3 that reports a war already running,
and a level-0 that reports "none" while a war is running, are the same confusion: **the
scale conflates "the source records nothing in W" with "the source records something it
cannot place in W".** Both readings are then a function of the *pre-existing conflict state*
— which is precisely what the persistence baseline encodes. The target and the baseline
therefore share variance by construction, and the published
"persistence beats the engine for escalation" (skill −0.469, run 193022Z −0.467) is partly a
statement about that construction rather than about historical analogy. That is the
consequence; this amendment fixes the cause.

### A4.2 The rule

**Windows.** `W = (d, d+90] = [d+1, d+90]` (unchanged). **`B = [d−90, d−1]`**, the 90 days
strictly before the event. **Day `d` belongs to the event and lies in neither window.** No
new constant is introduced: `B` is the scale's own 90 days, run backwards.

**Undated-for-W.** A source record is *undated-for-W* when it overlaps `W` but cannot place
the level it would assert inside `W`. Three cases, one predicate:

| source | undated-for-W when | rule id |
|---|---|---|
| **ICB**, **Dyadic MID** | ongoing at `d` — unchanged from Amendment 1.1, now given a rule id instead of a null | `ICB.<kind>.ongoing`, `MID.<kind>.ongoing` |
| **COW War** (inter and intra) | the spell overlapping `W` also covers the whole of `B` (start ≤ `d−90` **and** end ≥ `d−1`) | `WAR.inter.continuation`, `WAR.intra.continuation` |
| **UCDP GED** | the level over `B` reaches the level over `W`: `ged_level(D(B)) ≥ ged_level(D(W))` — the same registered ladder (250 → 3, 25 → 2), applied to the baseline | `GED.location.continuation` |
| **MIDI/MIDIP** | the incident covers the whole of `B` (for uniformity; incidents are days long and this is expected never to fire) | `MIDI.continuation` |

The COW and GED tests ask the same question in the vocabulary each source has: *was the
state this record asserts for W already the state across the whole of the preceding 90 days?*
A spell has no intensity, so for COW the test is coverage; GED is a count, so for GED it is
the same threshold on the baseline. Neither test invents a number.

**What the level is.** For an event, on the basis Amendment 2 selects, let `D` be the records
yielding a dated level and `U` the records that are undated-for-W:

1. `D ≠ ∅` → `level` = max over `D`. Unchanged.
2. **`D = ∅` and `U ≠ ∅` → `no_independent_outcome` = 1, `level` null,
   `rule_fired = UNDATED.continuation`.** The event is excluded from G-scoring and counted.
   **This is what replaces an ongoing-war level.**
3. `D = ∅`, `U = ∅`, ≥ 1 source covers `W` → `level` = 0. A true zero: a covering source has
   a dated view of `W` and records nothing in it.
4. No source covers `W` → `no_independent_outcome`, `rule_fired = UNCOVERED`. Unchanged.

Rule 2 is evaluated **on the basis Amendment 2 already chose**. Where the basis is dyadic and
every dyadic record is undated-for-W, the event is `no_independent_outcome` even though
location records exist — A2.1 already ruled that location evidence does not answer the dyadic
question. The location reading is not lost: it stays in `level_location`, so the alternative
can be read off the published counts without a re-run, the same device A3.2 uses for
`hostile_unattributed`. Under this rule `soleimani_strike_2020` becomes
`no_independent_outcome` with `level_location = 2`, not level 0 and not level 2.

### A4.3 What replaces an ongoing-war level, and why — decided before the number

Joe's brief put two options: `no_independent_outcome`, or a level for the **change** in
intensity. The answer is **`no_independent_outcome` for the G target** (§A4.2 rule 2), and
the change published beside it as a separate, separately-named measure (§A4.4) — never
inside `level`. Four reasons, all of which hold whichever way the resulting numbers fall.

1. **Level 0 would be a fabricated zero.** The obvious cheap fix — extend "ongoing → no
   level" verbatim and let `max(default=0)` do the rest — turns 34-odd wartime events into
   "no escalation recorded". That is not a gap, it is a false statement, and it is the same
   error as the false threes with the sign reversed. Whatever replaces the level, it cannot
   be 0.
2. **The target is undefined for these events, not zero and not unknown-but-estimable.**
   When the only thing the sources say is "a war that was already running was still running",
   they answer no question about what *this event* did. That is the identical situation
   Amendment 3 legislated for non-hostile events, and it takes the identical value, for the
   identical reason: *"a statement that the G question does not apply to this event, not that
   the event is doubtful"* (§A3.2). One project, one answer for "the target does not exist
   here".
3. **A change-level inside `level` would put two measurands in one column.** Levels 0–3 are
   defined as *states reached in W* ("none / threat or display / use of force / war").
   A level derived from an increment is a different quantity. A `level = 3` meaning "MIDI
   recorded hostility level 5 between the pair" and a `level = 3` meaning "deaths rose 250
   over baseline" are not the same number, and every score, κ, RPS and Brier computed over
   the column would be computed over a mixture. A1.4 already says in terms: *"It is not a
   change score."* Making it half a change score is worse than either.
4. **Choosing change thresholds now would be choosing them with the outcome in view.**
   Session K has already seen `deaths_ged_pre90` and `deaths_ged_90` for all 54 level-3 rows
   — they are published in the brief, in red team 2 and in §A4.1 above. Any *new* cut point
   for an increment would be picked by someone who has seen the increments. The rule in
   §A4.2 introduces no new number: it reuses the 90-day window and the 250/25 ladder that
   were registered before any of this was visible. That is the only version of this
   amendment that is honestly pre-registered.

**The cost, stated plainly.** This removes a large share of the G target's n, and it removes
it non-randomly: the events it removes are disproportionately the big wartime oil shocks.
After this amendment the G target is defined on *events that did not occur inside a conflict
already running at the same level* — a narrower claim than "escalation", and every surface
and the paper must say so rather than quietly reporting a smaller n. **The loss is not a cost
to be minimised** (§A3.4's words, and they apply again): every read removed was a read against
a label that reported the neighbourhood rather than the event. Whether the removal makes the
engine look better or worse against persistence and climatology is **not** a consideration in
adopting the rule and must not become one.

### A4.4 The change measure, published beside and never inside

Where GED covers `W`, three fields are stored and none of them is `level`:

- `deaths_ged_pre90` — **redefined** to `B = [d−90, d−1]`, strictly before `d`. The old
  `[d−89, d]` definition is withdrawn; §A4.1(ii) is the reason and the four affected events
  are named there.
- `deaths_ged_on_d` — **new**: `D` over `[d, d]`, so the day-`d` mass that used to hide
  inside the "before" figure is visible on its own and can never silently move between
  windows again.
- `delta_level` — **new**: `ged_level(max(0, D(W) − D(B)))`, by the same registered ladder,
  with `delta_basis = 'location'` and `deaths_ged_delta` stored beside it.

`delta_level` is **a published diagnostic, not the G target.** No surface may render it as
IES-90, no score is computed against it under this amendment, and promoting it would need a
further amendment registered before that score exists. It is written now, and handed to
Session B now, for one reason: B is running the persistence-conditional experiment, and the
question "does the engine beat persistence once the target stops encoding the pre-existing
state?" has two defensible operationalisations — drop the contaminated events (§A4.2) or
measure the increment (this section). Registering both before either is computed is what
stops the choice being made afterwards, by whoever likes the answer better. Both are to be
published as computed, side by side.

### A4.5 Expected effect on n and on the level distribution — the prediction, written first

Registered before the implementing code was run. Point estimate with an interval; being
wrong here is informative and is reported as such in §A4.7.

| quantity | as built | predicted after Amendment 4 | reasoning |
|---|---:|---|---|
| level 3 | 54 | **~15** (14–24) | 27 of 38 GED-set have `D(B) ≥ 250` strictly before `d`; ~11–13 of 16 COW spells cover all of `B`; the onsets (Yom Kippur, Kuwait 1990, Iraq 2003, Ukraine 2022, Gaza 2023, Israel–Iran 2025) survive |
| level 2 | 48 | **~34** (30–42) | 26 of 37 GED-set level 2 have a baseline at or above the 25 line; a few level-3 continuations fall here when another record still dates something |
| level 1 | 6 | **~6** (5–8) | ICB/MID onset rules unchanged |
| level 0 | 76 | **~58** (55–62) | the 18 false zeros of §A4.1(iii) leave, and few arrive |
| `no_independent_outcome` | 3 | **~62** (50–75) | the sum of the above, less events that retain a dated level from a second source |
| events with a level (pre-Amendment-3) | 184 | **~122** (110–135) | ≈ a third of the G target's n |

**Direction on the persistence baseline.** The shared variance between the target and the
persistence predictor should fall, and the engine-vs-persistence skill (−0.469 at 182828Z,
−0.467 at 193022Z) should move **toward zero**. It may not reach it. **If persistence still
beats the engine on the de-contaminated target, that is a real result and it is published as
one** — the point of the amendment is to make the comparison mean something, not to win it.
The test is Session B's; §A4.6 hands B what it needs to run it.

### A4.6 What Session K computes, and what it does not touch

The counts in §A4.7 are computed with `ies90.run(conn, write=False)`: every level, source,
rule and count, **without writing a row to `event_outcomes`**. Session B holds the
persistence-conditional experiment open against the table as it stands; rewriting the target
underneath a running experiment is exactly the move SESSION_CHARTER §2 rule 2 and the seal
exist to prevent. The rebuild of the `ies90` rows is therefore a **separate, announced step**
that Joe schedules with B, not a side effect of this amendment. Until it runs,
`event_outcomes` holds the pre-Amendment-4 labels and every published run remains reproducible
against them.

### A4.7 No retroactive application

**This amendment cannot be applied to any published run retroactively**, on the same terms as
§A3.5, which is incorporated here by reference and not restated. The sealed reads were made
against the target as it stood. Specifically:

- Runs 182828Z and 193022Z stand as published, with their n, their scores, and the
  engine-vs-persistence skill of −0.469 / −0.467 unchanged.
- Every surface reporting a G result from a pre-amendment run carries: *"scored before
  Amendment 4; the escalation label on N of these events reports a conflict already running
  at the event date, or reports 'none' where a covering source could not date one"*, with N
  and the receipt path from §A4.8.
- The amendment governs **the next run**, and that run is reported separately — never pooled
  with a pre-amendment run, never presented as a correction to its numbers.
- The paper states the defect, the affected counts, the direction, and the fact that the
  post-amendment G target is defined on a narrower population — rather than showing a
  corrected result.
- The prediction in §A4.5 is scored against the computed counts in the same document, as
  written, whether or not it was right.

### A4.8 Outputs and receipts

- `data/state/ies90_amendment4_counts.json` — the level distribution before and after, by
  level, by source, by rule fired, by basis and by decade; the continuation counts per source;
  the `delta_level` distribution; and the §A4.5 prediction scored against the outcome. Written
  by `ies90.py` in no-write mode; contains no row that is not derived from a covering source.
- `event_outcomes` (source `ies90`) gains `deaths_ged_on_d`, `deaths_ged_delta`, `delta_level`,
  `delta_basis`; `deaths_ged_pre90` is redefined per §A4.4; `rule_fired` gains the six rule
  ids of §A4.2 — **all of these on the next rebuild, not now** (§A4.6).
- `data/state/ies90_distribution.json` gains an `amendment_4` block on that rebuild.
- `tests/test_ies90_continuation.py` — the rules of §A4.2 as unit tests, named for this
  amendment, including the two cases that must not regress: a war onset at `d` keeps level 3,
  and an event whose only records are undated-for-W is never level 0.
- `data/handoffs/K_to_B_2026-09-02_ongoing_war.md` and
  `data/handoffs/K_to_Cowork_2026-09-02_ongoing_war.md` — the counts, for the
  persistence-conditional experiment and for the paper.

### A4.9 What this amendment does not fix

Named so that no one reads the fix as larger than it is.

- **GED is still a location source.** A2.1 and A1.2 already say so; the continuation test is
  computed on the same location deaths and inherits the same weakness. `delta_level` narrows
  it (an increment in the location is closer to an event effect than a level in the location)
  but does not close it. Only a dyadic GED pull would, and there is no `UCDP_TOKEN` in this
  environment.
- **It does not make the target a change score**, and A1.4 still stands. It removes the
  events where the state reading is inherited; it does not re-express the ones that remain.
- **It does not address Amendment 3's precondition**, which is Session F's and still awaits
  all four classes being coded (A3.1 §2). An event can be dropped by either rule; the two
  exclusion counts are reported separately and never merged into one "excluded" figure.
- **It does not touch the P target**, which does not presuppose an adversary and is unaffected.
- **It does not re-score anything.** No score, skill, CI or p-value in this repository moves
  because of this text.
- **It does not reach an undated record on the basis Amendment 2 did not choose**, and that
  leaves a residual of the §A4.1(iii) shape. §A4.2 rule 2 is evaluated on the chosen basis, so
  a dyadically-covered event whose *only* undated records are location-basis still falls to
  rule 3 and is published as level 0. `iran_sanctions_reimposed_2018` is the case found while
  testing: ICB covers, no Iran–USA crisis is recorded in W (a genuine dated zero on the dyadic
  question), while the ICB records that did match Iran singly — the Houthi Rebellion and North
  Korea Nuclear VII — are "ongoing at d" and set nothing. The level 0 is defensible under
  A2.1 (the dyad did not escalate; an unrelated ongoing crisis elsewhere does not make that
  question unanswerable), and `level_source` on such a row lists the covering sources rather
  than setters, which is registered A2.3 behaviour and reads worse than it is. It is recorded
  here as a residual and not fixed, because fixing it would mean letting location evidence
  speak on a dyadic event — the thing Amendment 2 exists to prevent.

### A4.10 The counts, computed (appended 2026-09-02, after §A4.1–§A4.9 were committed)

Computed by `python3 src/state/ies90.py --counts` — a `write=False` run, per §A4.6. Receipts:
`data/state/ies90_amendment4_counts.json` and
`data/state/ies90_amendment4_persistence_overlap.json`. **No row of `event_outcomes` was
written and no published run moved.**

**The distribution.**

| level | before | after | |
|---|---:|---:|---|
| 0 — none | 76 | **73** | |
| 1 — threat or display | 6 | **9** | |
| 2 — use of force | 48 | **30** | |
| 3 — war | 54 | **20** | |
| `no_independent_outcome` | 3 | **55** | 3 uncovered (as before) + **52 undated-for-W** |
| **events with a level** | **184** | **132** | **52 removed, 28 % of the G target's n** |

**59 of 187 labels change.** 3 → `no_independent_outcome` 27; 2 → `no_independent_outcome` 22;
3 → 2 four; 3 → 1 three; 0 → `no_independent_outcome` three.

**The 20 surviving level 3, by the rule that set them:** `GED.location.ge250` 11,
`WAR.inter.pair` 3, `WAR.intra.location` 3, `WAR.inter.single` 2,
`MIDI.pair.overlap`+`WAR.inter.pair` 1. By source: GED 11, COW War 8, MIDI+War 1.

**Continuation records found, by rule:** `GED.location.continuation` 58,
`MID.single.ongoing` 51, `ICB.single.ongoing` 38, `MID.pair.ongoing` 14,
`ICB.pair.ongoing` 12, `WAR.intra.continuation` 8, `WAR.inter.continuation` 6,
`MIDI.continuation` 1 (the MIDI case was predicted never to fire; it fires once).

**`delta_level` (§A4.4 diagnostic, not the target):** 0 → 119, 2 → 28, 3 → 21, not
applicable (GED does not cover) → 19.

**The behaviour that matters, checked event by event.** The war *onsets* keep level 3 —
`yom_kippur_war_1973`, `iraq_invades_kuwait_1990`, `iraq_war_begins_2003`,
`russia_invades_ukraine_2022`, `israel_hamas_war_2023` are all unchanged. The
*continuations* leave: `rus_ryazan_strike_2025a` (6,927 GED deaths in B, 2,116 in W) and 26
others go from "war" to `no_independent_outcome`. `desert_storm_air_campaign_1991` moves
3 → 1, not to `no_independent_outcome`: the Gulf War spell is a continuation, but MID
dispute 3974 *starts* inside W, and A1.1's onset rule dates that at level 1. That is the
rule working: an onset inside W is dated evidence, and it outranks nothing.
`soleimani_strike_2020` moves 0 → `no_independent_outcome` — the false zero is gone.

**`abqaiq_attack_2019` does not move, and that is correct.** It stays level 0, because GED
covered Saudi Arabia across W and recorded 1 death: a source with a dated view of W that
found nothing in it. Rule 3, a true zero. It appeared in §A4.1(iii) as one of the 18
suspicious zeros; on the rule it turns out only 3 of those 18 were false zeros, and the
other 15 had a genuine dated zero beside the undated record. §A4.1(iii) overstated that
count and this paragraph corrects it.

**What the other option would have kept — the price of §A4.3, in numbers.** Of the 52
events that leave the G target, `delta_level` (§A4.4) is 0 on 28, 2 on 13, 3 on 8, and not
applicable on 3. **So the change measure would have carried a non-zero level on 21 of the
52.** Those 21 are events where UCDP records a genuine *increase* in violence over the
baseline — the strongest case against §A4.3's choice, and it is stated here rather than left
for a reader to find. The choice stands on the four reasons in §A4.3, none of which is
"it keeps more n"; and because `delta_level` is registered and published, the 21 are not
lost — they are available to anyone scoring the change target, exactly as §A4.4 intends.

**The §A4.5 prediction, scored. Four of six inside the interval; two misses, both mine.**

| quantity | predicted | interval | observed | |
|---|---:|---|---:|---|
| level 3 | 15 | 14–24 | **20** | inside |
| level 2 | 34 | 30–42 | **30** | inside |
| level 1 | 6 | 5–8 | **9** | **outside, +3** |
| level 0 | 58 | 55–62 | **73** | **outside, +15** |
| `no_independent_outcome` | 62 | 50–75 | **55** | inside |
| events with a level | 122 | 110–135 | **132** | inside |

Both misses come from the same bad assumption: I predicted the 18 events of §A4.1(iii)
would nearly all leave, and only 3 did (see the Abqaiq paragraph), which held level 0 up at
73 instead of 58. The three-too-many at level 1 are the 3 → 1 moves like Desert Storm, which
I did not think of at all — I predicted continuations would fall out of the sample, not that
some would land on a dated onset one rung down. The rule is not adjusted to fit the
prediction, and the prediction is not edited to fit the rule.

### A4.11 Does the target still share its variance with the persistence baseline? — measured

The question Joe's brief ends on. WALK_FORWARD_PROTOCOL Amendment B.1 defines the
G-persistence forecast as **the same function on a shifted window**:
`ies90.score_event(t − 91, A, P, L, sources)`. So Amendment 4 changes the *baseline* as well
as the target, and both were recomputed under both rule sets — the pre-amendment code taken
from git at `c74ccd6`, the post-amendment code as committed. A read at `t = d`; the walk's
own reads use its `as_of` and its filters, so these are corpus-level diagnostics and **not**
the walk's numbers. Receipt: `data/state/ies90_amendment4_persistence_overlap.json`.

| | before | after |
|---|---:|---:|
| n with both target and persistence | 184 | 120 |
| exact agreement (target level == persistence level) | **75.0 %** | **73.3 %** |
| Spearman ρ | **0.800** | **0.638** |
| ρ² — shared rank variance | **0.640** | **0.407** |
| Cramér's V | 0.563 | 0.502 |

The headline drop (0.640 → 0.407) is confounded: the two rows are different samples. Holding
the sample fixed at the 120 events scorable under **both** rules:

| same 120 events | old rules | Amendment 4 |
|---|---:|---:|
| Spearman ρ | 0.696 | **0.638** |
| ρ² | 0.484 | **0.407** |
| exact agreement | 75.8 % | **73.3 %** |

**The answer, stated as it comes out: yes, it still shares its variance — less, and not by
much on a like-for-like sample.** Of the 0.23 fall in ρ², about **0.08 is the rule** and the
rest is the sample: the events Amendment 4 removes were the ones where target and
persistence agreed most, so removing them lowers the correlation partly by selection.
**41 % of the target's rank variance is still shared with the persistence forecast**, and
73 % of labels are still exactly what persistence would have said.

That residual is not a defect and this amendment does not try to remove it. Conflict is
autocorrelated; a persistence forecast of a conflict scale *should* be good, and a baseline
that is genuinely hard to beat is the point of having one. What Amendment 4 removes is the
part that was true **by construction** — a label inherited from the pre-window because the
rule could not date anything inside the window. What remains is a real property of the
world. The published "persistence beats the engine for escalation" (−0.469 / −0.467) was
therefore **partly** mechanical and is not *only* mechanical: after the fix the engine still
has to beat a strong, legitimate baseline, and whether it does is Session B's to run and
publish, either way.

**One consequence Session B must price before running it.** Because B.1 reuses this
function, the persistence forecast itself now returns `no_independent_outcome` far more
often: **B.3's climatology fallback goes from 2 reads to 58** (of 187 corpus events; the
walk's scored subset will differ). "Engine vs persistence" after Amendment 4 is therefore
partly "engine vs climatology", `n_persistence_fallback` must be published beside the
comparison as B.4 requires, and the comparison is materially less powerful than the one that
produced −0.469. That is a fact about the experiment, not an argument against the amendment.

### A4.12 One implementation consequence, recorded rather than worked around

`src/engine/persistence.py` calls `ies90.score_event` **live** — WALK_FORWARD_PROTOCOL
Amendment B.1 says "called, never copied", and that is what the code does. So committing the
Amendment 4 code changes the **G-persistence baseline immediately**, while the labels in
`event_outcomes` stay pre-amendment until the rebuild that §A4.6 defers. Between those two
points a walk run would score a pre-amendment target against a post-amendment baseline —
an invalid comparison that does not announce itself, because `walk.py` takes
`data_state.ies90_registration` from `data/state/ies90_distribution.json`, which Session K
did not regenerate.

This is **not** a defect introduced by the amendment; it is a coupling the amendment makes
visible, and the honest response is to name it rather than to add a switch that lets the
registered rule be turned off. **The two coherent states are: everything pre-Amendment-4
(`src/state/ies90.py` at `c74ccd6`), or everything post (the `ies90` rows rebuilt).** Which
one holds, and when the rebuild happens, is Joe's decision with Session B, and it is carried
in `data/handoffs/K_to_B_2026-09-02_ongoing_war.md` §0 with the one-line check that
distinguishes them. Session K does not choose it, and does not half-apply the amendment to
avoid having to ask.

### Amendment 4.1 (2026-09-03, registered before the code, after the Amendment 4 rebuild exposed the defect) — an audit in progress survives a target rebuild

*Session K. Amends A1.3's audit-sheet rule only. No level, window, source, precedence or
threshold changes; no published run is touched; nothing enters `events`.*

**The defect, found by the rebuild itself.** `data/audits/ies90_audit_30.csv` is drawn as 30
events **stratified by level × decade over the pool that has a level** (A1.3, seed 20260902).
Amendment 4 moved 52 events out of that pool, so the strata quotas moved and the draw
returned a different sample: **19 of the 30 rows changed, and the one row Joe had already
answered (`iran_iraq_war_1980`) left the sheet** — not because its label changed (it is still
level 3) but because the 1980s × level-3 quota did. `tests/test_audit_ies90.py::
test_joes_answered_row_survives_the_regeneration` caught it, which is what it is for.

Joe's answer itself was never at risk: it lives in `data/audits/outcome_audit.json`, which
this session did not touch, and the pre-rebuild sheet is in git at `213209e`. What was at
risk is worse than a lost answer — **the sheet Joe is working through can be reshuffled
under him by any target amendment**, so the §7 label-audit gate (κ ≥ 0.6, *every* row
answered) can never be completed while the target is still moving. Reverting the sheet was
rejected as the fix: a pre-rebuild sheet shows `ies90_level` values that no longer exist in
`event_outcomes`, so Joe would be checking the engine against labels the engine no longer
holds. That is a false artifact, and a worse failure than a reshuffle.

**The rule.** The sheet is drawn as A1.3 registers it, with one clause added before it:

1. **Every event already carrying an answer in `data/audits/outcome_audit.json` is retained
   on the sheet**, in date order, and the stratified largest-remainder draw fills the
   remaining `30 − n_answered` seats from the rest of the pool. The seed, the strata and the
   largest-remainder rule are unchanged; the draw is still deterministic.
2. **An answered event that Amendment 4 removed from the pool is still retained**, carrying
   `ies90_level` blank, `rule_fired = UNDATED.continuation` or `UNCOVERED`, and
   `pinned_reason = answered_before_rebuild; no longer G-scorable`. Joe's answer is a record
   of what he checked and does not silently vanish because the target moved. Such a row is
   **excluded from κ** and the exclusion is counted, because there is no engine level to
   agree or disagree with — never dropped silently, never counted as agreement.
3. The sheet gains a `pinned` column (`1` for a retained answered row, `0` for a drawn one)
   so the two kinds are never confused, and the audit tool can tell a resumed row from a new
   one.

**Why this and not a bigger fix.** The alternative — freezing the sheet permanently at its
first draw — would mean the audit never covers the target actually in use, which is the
opposite failure. Retaining answers and redrawing the rest keeps both properties: the audit
covers the live target, and work already done is never thrown away.

**Expected effect, stated before running it:** one row is currently answered, so 1 seat is
pinned and 29 are drawn; the sheet stays 30 rows; `iran_iraq_war_1980` returns; the other 29
are drawn by the unchanged rule and most will differ from the pre-rebuild sheet, because the
pool genuinely changed. κ is unaffected — 1 answered row, κ still null, `passed` still false.
