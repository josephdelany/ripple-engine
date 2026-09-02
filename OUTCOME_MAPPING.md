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
