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
