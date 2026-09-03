# Interval audit — where the grid file's defect lives, and where it does not
*Session B, 2026-09-03. Commissioned after B found and corrected the defect in its own published file
(`a7fbae9`). **Read-only: nothing was re-run and nothing was fixed.** The scope comes first so the response
can be chosen — a published erratum if it is widespread, a targeted fix if it is not.*

## The defect being hunted

**The unit of dependence used by an interval is not the unit of dependence in the data.** Two forms:

- **(A) Stacking.** Several correlated series are flattened into one vector and resampled with a block
  length measured in time. Adjacent entries are then not neighbours in time, and the interval is computed as
  though correlated observations were independent. This is what B did in the grid price arm.
- **(B) Replication.** Several correlated rows per underlying unit (reps, horizons, nodes) are treated as
  independent draws.

Both inflate precision. Neither moves a point estimate.

## The answer, in one line

**It is not widespread. Two files carry it, one of which is already corrected. Every other interval in the
project uses the right unit — because the event-study modules de-overlap into clusters before they
bootstrap, and the walk uses the stationary block bootstrap at its own measured block length.**

## The table

| # | file · comparison | unit of dependence USED | unit that SHOULD be used | conclusion changes? |
|---|---|---|---|---|
| **1** | `data/grid/price/summary.json` · every interval | flattened cell, **10,857**, block length measured in dates | **grid date, 413** | **YES — already corrected in `a7fbae9`.** fitted vs random analogs p **0.0104 → 0.0524**, CI [+0.0022,+0.0184] → [−0.0004,+0.0212], no longer survives FDR; Ferro diagnostic p 0.076 → 0.128; fitted vs frozen p 0.642 → 0.820 (null either way) |
| **2** | `data/walk_forward/summary.json` · `placebo.*` (`walk.py:1033`) | **pseudo-read, 411, i.i.d.** (`mean_block=1.0, lag=0`) | **source event, 82** — the 411 rows are 82 events × **5 reps**, and the reps are matched on the *same* VIX-percentile decile of the *same* source event | **PROBABLY YES.** `vs_random_analogs` skill −0.0473, CI [−0.0828, −0.0082], `null_holds: false`. √(411/82) ≈ 2.24; widening by that gives ≈ [−0.13, +0.04], **covering zero**, and dm_p 0.019 → ≈0.19. **`null_holds` would flip false → true.** `vs_climatology` (p 9e-7) survives any plausible widening; `fair_vs_climatology` already covers zero. |
| 3 | `src/brief.py` · `horizons[].ci90`, class-median CIs | event, i.i.d. (`arrs` is **not** de-overlapped) | de-overlapped cluster | Intervals are too narrow. The brief **already discloses** the overlap in prose (line 315: *"the effective sample is below the…"*) but attaches **no number** to it. Qualitative caveat, quantitative gap. |
| 4 | `src/walk.py:_replay` · P-tier `mean_block` | the **first `len(rows)` dates of `scores`**, not the P rows' own dates | the P rows' dates | Minor. Mis-estimates the HAC lag on some spec-curve rows. The spec curve publishes **no interval** (see below), so **no published conclusion depends on it.** |
| 5 | `propagation_graph.py`, `local_projections.py`, `cross_chain.py`, `edge_battery.py`, `evidentiary_bar.py`, `frozen_lens.py`, `placebo_vixmatched.py`, `supply_chain.py`, `research.py` | **cluster** — every one calls `assign_clusters(...)` then `groupby("cluster").first()` before bootstrapping | same | **NO — correct.** |
| 6 | `walk.py:_skill_block`, `_reliability`, `_spa_block`; `engine/delta_experiment.py:_block`; `engine/diagnostic_hostile.py` | **read**, stationary block bootstrap at the tier's **measured** mean block (daily 2.32; Δ-experiment 1.95) | same | **NO — correct.** |
| 7 | `src/ripple_lp.py` | **one regression per horizon**, Newey–West at bandwidth h, lag-augmented, clustered, BH across the family | same | **NO — correct, and it is the textbook treatment of exactly the horizon-stacking trap B fell into.** |

## Three premises in the brief, checked

- **"The delta experiment pools 150 reads across dyads and horizons."** It does not. `delta_experiment_reads.json`
  is **150 rows, 150 unique events** — one read per event, one 90-day window, one primary dyad each, sorted by
  date, bootstrapped at the measured block 1.95 over 57 clusters. There is no dyad axis and no horizon axis to
  stack. **No defect.**
- **"The specification curve has 162 settings."** Correct — `n_specs: 162`. But it publishes a *distribution*
  (min −0.150, median −0.075, max −0.041, share positive 0.000) and **no interval**, which is what §6
  registered. 162 overlapping specifications are not 162 independent tests and are not presented as such.
  **No defect.**
- **"The propagation study has 477 cells across nodes that are obviously correlated."** The correlation is
  real, but each cell's interval is computed on **cluster-collapsed** CARs, so the *unit* is right; and
  `propagation_graph.py:206` applies **BH-FDR across the family** and gates `status = "validated"` on
  surviving it. `backbone_validated: 0`. **No defect of this class.**

## What this means for the response

**An erratum is not warranted; one targeted correction is.** Finding 1 is corrected and its erratum is
already written into paper §14.1. Finding 2 is one number in one block and should be re-run under a
source-event cluster bootstrap — **and it runs in the engine's favour**, which is the reason to be careful
about it rather than quick: correcting it *removes* a published mark against the engine (`null_holds: false`
is currently evidence that the placebo null fails). That is exactly the direction in which a correction
deserves the most scrutiny, and it is why this audit stops at the table rather than proceeding to the fix.

Findings 3 and 4 are disclosure and hygiene, not conclusions.

**Blocked on two things before any re-run:** `src/walk.py` is frozen until K's rebuild lands (Joe's ruling,
tag `record-pre-amendment-4`), and the placebo lives inside the walk. So finding 2 cannot be corrected
without re-running the walk anyway — which means it should be folded into the post-rebuild re-run rather
than done separately. B proposes exactly that, and no separate placebo run.

## The general lesson, since it caught the person auditing for it

Every module that got this right did so by **collapsing to the unit of dependence before computing anything**
— `assign_clusters(...).groupby("cluster").first()` — rather than by choosing a clever block length
afterwards. The two that got it wrong both computed on a stacked vector and tried to repair it with a block
parameter. The first discipline is checkable by reading one line; the second is not.
