# GATE — the drop rule I registered drops the escalation panel. Joe rules; I do not amend it myself.

*Session B, 2026-09-03. Blocking only the G arm of the grid study. The P arm is unblocked and proceeds
(charter §4.3: write the gate report and move on).*

## What happened

`GRID_STUDY_REGISTRATION.md` §2.7 was registered before any number was computed, in commit `7afcb2c`. It
declares two independent DROP conditions for a multiplier:

- realisation ratio **R_m < 0.10** → DROP
- **Δn_eff < 30** effective units → DROP

Applied mechanically to the computed arithmetic, multiplier 4 (escalation at dyad-date) is **DROPPED**:

| grid | n_nominal cells | n_eff | R_m | Δn_eff vs the event-triggered G panel | decision |
|---|---|---|---|---|---|
| month-end | 321,678 | **4,056** | **0.0126** | **+3,908** | DROP (R < 0.10) |
| week-end | 1,398,768 | **4,217** | **0.0030** | **+4,069** | DROP (R < 0.10) |

The event-triggered G panel's own effective n, computed on the same definition from the sealed
differentials of `walk_20260903T003422Z`, is **148.5**. So the rule drops a multiplier that would multiply
the escalation evidence by roughly **27×** in effective units — because its *ratio* is low, and its ratio is
low precisely because its nominal count is enormous.

## Why this is a defect in my rule, not in the multiplier

The rule was written to serve Joe's instruction: *"If a multiplier buys less than it appears to, say so and
drop it."* That sentence contains two different tests, and I collapsed them into one:

- **"buys almost nothing"** — a real reason to drop. Complexity with no return.
- **"buys much less than it appears"** — a real reason to *say so*. It is not, by itself, a reason to drop
  something that still buys a great deal.

A ratio test punishes a multiplier for having a large denominator. Multiplier 4 has 321,678 nominal cells
and delivers 4,056 effective ones; multiplier 2 (targets) has 5 nominal columns and delivers 1.85 effective
ones. The second passes at R = 0.37 and the first fails at R = 0.013, yet the first contributes about four
times more effective evidence than the entire price panel's grid multiplier. The rule as written prefers
small honest multipliers to large inflated ones **even when the large one is worth more after the inflation
is removed**.

## Why I am not fixing it myself

I noticed this defect *because* it dropped a multiplier I expected to keep. A rule rewritten at that moment,
by the person whose result it inconvenienced, is indistinguishable from a rescue — and this project's whole
method is that registrations bind after they stop being convenient. So the computed file
(`data/grid/power_arithmetic.json`) records **DROP**, as registered, and Part III of the study is written
without the G arm until you rule.

## The ruling I need

**Option A — the rule stands.** Multiplier 4 is dropped. The grid study has a price arm only. The escalation
question stays on the 150 event-triggered reads, where Amendment L already showed we cannot detect a skill
below 0.067. *Cost: the escalation side of the engine never gets the n it needs.*

**Option B — amend §2.7 to separate the two tests**, dated and disclosed as post-hoc-motivated (the standing
Amendment K and Amendment M carry):
- **DROP** iff Δn_eff < 30 effective units (the absolute test — "buys almost nothing").
- **DISCLOSE** iff R_m < 0.33 — the multiplier is kept but permanently labelled marginal, with R_m printed
  beside every number it contributes to, in every surface.
Under B, multiplier 4 is kept and carries `R = 0.013` forever, which is a louder disclosure than the drop
would have been. *Cost: a rule amended after seeing the number it decided, with that fact on the record.*

**Option C — something else you specify.**

### Recommendation — revised the same day, against my own earlier one

**I first recommended B. I now recommend A**, on evidence that landed after I wrote it: session G's
dyad-date probe (`data/grid/PROBE.md`, commit `b31a24e`), which tested the same panel against `ies90.py`'s
own rules rather than by inference. Three of its findings bear directly:

1. **After 2014 every non-zero dyad-date cell is an artefact.** MID, MIDI and COW War are the only sources
   that record which *side* a state was on, and all three stop covering the grid at 2014-10-02. ICB records
   crisis **actors**, so on a mechanically supplied pair allies read as adversaries — at 2018-01-31 the dyad
   `country.gbr|country.usa` scores **IES level 3** from one Syria crisis, and all six of 2018's level-3
   dyads are pairwise combinations of {GBR, Russia, Syria, USA}: one episode counted six times. GED is a
   location death count replicated across every dyad containing that country: all 21 of 2024's non-zero
   cells are Iran paired with Saudi Arabia, the UAE and the USA — one country's deaths, three times.
2. **The contamination is not confined to the post-2014 tail.** I re-ran my own arithmetic with a
   sided-evidence-only variant (MID alone, to 2014-10-02). Informative cells fall from **10,442 to 8,437**
   at month-end: about a fifth of what my published `mid_family_2014` panel counted as information is ICB
   co-actor artefact.
3. **Every cell is retrospective**, so under `WORLD_STATE_CODEBOOK.md` Amendment 1 it can describe and never
   validate — and, as G puts it, *density does not fix that, because the problem is not n.* Multiplier 4
   cannot buy the thing the study wants most.

So the rule that dropped multiplier 4 reached the right destination by faulty reasoning. I still think the
ratio test is the wrong test and would write it differently today; that is a separate question from whether
this particular multiplier should be in this particular study, and the answer to the second is now no.

**What I would do instead, and am not doing without your word:** build the sided-evidence dyad-date panel
for **1987–2014** as its own descriptive study, which is roughly where session G's probe also lands. It is a
real object — 1998 alone yields 295 defined-ΔIES cells against the corpus's 14 monthly-tier events — but it
is a *description of a closed period*, not a panel a live engine can read from, and it belongs in its own
registration with that stated on the front page rather than as a multiplier inside a study whose price arm
runs to 2026.

## Two things that are true whichever you choose

**1. The escalation panel's n_eff is a ceiling, not an estimate — and on this panel it is barely even that.**
Removing the ICB contamination *raised* the computed n_eff (month-end 4,056 → 5,962) while *lowering* the
informative cells (10,442 → 8,437), because n_eff on a 97 %-zero panel is driven by the zeros' dependence
structure and not by the information. That is a warning about the measure, and I am not going to invent a
better one after seeing the number. Read the informative-cell count, not the n_eff.

The level panel is **96.75 % zeros** (311,236 of 321,678 covered cells at level 0; 2,321 at 1, 7,331 at 2,
790 at 3). A forecaster and its
climatology both get a level-0 cell right, so those cells carry no power to *discriminate* between them.
The 4,056 figure counts them. The genuinely informative cells number **10,442** (month-end), of which
about a fifth are ICB co-actor artefact, leaving **8,437** on sided evidence. Under
Amendment L's finding that the right escalation target is ΔIES rather than the level, the moving share is
smaller again. Whatever you rule, the G arm's real power is below 4,056 and the file says so.

**2. The coverage wall is hard and is not affected by this ruling.** A dyad-resolved IES label ends **2014**
for the MID family, is carried by ICB alone to 2021, and does not exist after 2021 — UCDP GED reaches 2025
but resolves a *location*, not a dyad. The grid's escalation arm therefore cannot be scored on the last
twelve years at all, whichever rule applies. (Also, for the record: the brief's "Dyadic MID 4.03 is 59,076
panel rows" does not match the file in this tree, which has **10,358** dyad-year rows. No file in
`data/state/raw/` has 59,076 rows.)

## What proceeds while this is open

The price arm: multipliers 1, 2 and 3 all survive §2.7 and Part III is written for them. Its arithmetic,
for the record and for your decision:

| | event-triggered | grid, month-end | grid, week-end |
|---|---|---|---|
| n nominal | 253 | 12,691 (**50×**) | 55,220 (**218×**) |
| **n effective** | **249** | **1,979 (7.9×)** | **2,895 (11.6×)** |
| minimum detectable Brier skill | 0.085 | **0.029** | **0.027** |

Fifty times the rows buys **7.9 times** the power. That is the arithmetic you asked to see before anything
was built, and it is the reason the ratio disclosure matters more than the drop.
