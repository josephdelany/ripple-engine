# G-6 REGISTRATION — OPEN_ITEMS 1.4, the era confound: can era, pool size, base rate and label basis be separated at n = 150?
*2026-09-03, Session G. Registered BEFORE `src/g_era_confound.py` is written and BEFORE any
stratified number is computed (charter §2 rule 2). **This is a DIAGNOSTIC. It gates nothing.**
It re-judges no run, moves no threshold, changes no published verdict, and writes to no table.
Amendments are dated and appended.*

## 0. Standing, and a reassignment recorded rather than assumed

`OPEN_ITEMS.md` §1.4 names **B** as owner. Joe reassigned the item to Session G on 2026-09-03
("your panel work is the reason you are the right session for it"). G therefore writes only to
its own paths — `docs/g/**` and `src/g_era_confound.py` — reads `data/walk_forward/**` and never
writes there, and hands the result to B and to whoever owns `OPEN_ITEMS.md`. Nothing in
`src/walk*.py`, `data/walk_forward/**` or `data/grid/**` is touched.

## 1. The question, stated so it can come out "no"

Joe: *"What I want to know is whether the three confounds can be separated at all at this n, and
if they cannot, say so rather than reporting a decomposition the sample cannot support."*

So the deliverable is **not** a decomposition. It is a **verdict on identifiability**, with the
decomposition published only if the verdict permits it. §5 fixes the rule that decides, before
any of it is computed.

## 2. The run is PINNED, and why that is not a formality

`data/walk_forward/scores.jsonl` **currently contains two runs** — `walk_20260903T003422Z`
(313 rows) and `walk_20260903T052633Z` (313 rows) — while `summary.json` describes only the
first and is older on disk (23:23 against 01:28). `WALK_FORWARD_PROTOCOL.md` Amendment D says
the sealed logs in the tree hold **the current run only**, with earlier runs archived. Either
session B is mid-run and the archive step has not fired yet, or Amendment D's invariant is not
holding. **Either way, an analysis that read the file without filtering would silently mix two
runs.**

This diagnostic is computed on **`run_id == "walk_20260903T003422Z"` only** — the run
`summary.json` publishes and the run OPEN_ITEMS §1.4 quotes. The second run is excluded by
`run_id`, its presence is reported, and the fact is handed to B rather than acted on.

**Baseline check, before anything is stratified.** The pinned run must reproduce the published
G block exactly:

    n = 150 · engine_mean = 0.7687487109093333 · ref_mean = 0.7010597406851313
    skill = −0.09655235680492913          (summary.json tiers.daily.G.engine_vs.climatology)

If it does not reproduce to the seventh decimal, the diagnostic is void and says so. Everything
below is measured against a number this code has re-derived, not against one it was told.

## 3. The four variables, and where each comes from

| variable | definition | source, read not recalled |
|---|---|---|
| **era** | the four bins of OPEN_ITEMS §1.4: 1987–99, 2000–09, 2010–19, 2020–26 | the read's `date` |
| **pool size** | the point-in-time G pool the read was scored against | `reads.jsonl` `n_pool_g` |
| **base rate** | the level-0 share of that read's **own** pool, not an era average | `reads.jsonl` `baselines.climatology.G_labels` |
| **label basis** | whether the IES-90 level rests on a dyadic or a location reading | `event_outcomes` `field='basis'` (`ies90`), per event |

The bins are **taken from OPEN_ITEMS as registered**, not chosen by G. Their unevenness
(n = 2, 10, 51, 87) is the property under test and is not repaired by re-binning: re-cutting the
bins after seeing the skill is exactly the move this document exists to prevent.

## 4. S4 — the size-correction test, with its direction and its magnitude registered in advance

This is the mechanism G thinks is doing the work, and it is registered as a **falsifiable
prediction with a number** before the data is cut, so that being wrong about it is visible.

`WALK_FORWARD_PROTOCOL.md` Amendment E.3 registers that the Brier score of a **k-atom**
predictive distribution exceeds the population Brier by `Σ_b p_b(1−p_b) / k`. In this run:

- the **engine**'s distribution is built from its k analogs — `n_atoms = 5` on the read inspected;
- **climatology**'s distribution is the pool's own label frequencies — `n_atoms = the pool size`,
  which OPEN_ITEMS reports as median **8 → 10 → 18 → 36** across the four eras.

So the engine's inflation is roughly constant at `S/5` while climatology's shrinks as `S/pool`.
**The engine's handicap relative to climatology therefore grows monotonically with pool size, and
pool size grows with era — which produces a declining measured skill across eras under exactly
zero change in true skill.**

**Registered magnitude.** With both raw scores near 0.7, the differential inflation is about
`0.7/5 − 0.7/8 = 0.053` in the earliest era and `0.7/5 − 0.7/36 = 0.121` in the latest — a swing
of ≈ **0.068 in absolute Brier**, or ≈ **0.10 in skill** on a reference near 0.70. The observed
era spread is `+0.009 → −0.117`, i.e. **0.126**. So the prediction registered here is that the
size artefact alone is of the **same order as the entire observed era gradient**.

**The test.** Both scores are already sealed: `brier` (registered) and `brier_fair` (Ferro
size-corrected, Amendment A.5/E). The era table is computed on **both**. The registered
prediction is that the fair-Brier era gradient is **materially flatter** than the registered-Brier
one. Fixed now, before the numbers:

> **S4 passes** (the artefact is doing most of the work) if the era spread in fair-Brier skill is
> **≤ half** the era spread in registered-Brier skill.
> **S4 fails** (the era effect survives size correction) if the fair spread is **> half** the
> registered spread.
> Either way the result is published, and **neither outcome changes any verdict** — Amendment E.1
> already rules that the registered scores govern every v2 run, and this diagnostic does not
> touch that.

## 5. S3 — separability, and the rule that decides it, fixed before it is run

Three things are computed:

1. **Collinearity.** Pairwise Spearman ρ among (date-ordinal, pool size, pool base rate, dyadic
   label share) over the 150 scored reads, plus the condition number of the standardised design.
2. **Support.** The (era × pool-size tertile) cross-tab, with cell counts. Two variables can be
   separated only where the sample has cells **off the diagonal**: if every read in the early era
   has a small pool and every read in the late era has a large one, era and pool size are the same
   variable in this sample and no n repairs it.
3. **Overlap.** The min–max pool-size range within each era, and whether the ranges intersect.

**The registered decision rule.** The diagnostic returns **NOT SEPARABLE** if **any** of:

- **(a)** |Spearman ρ| between era-index and pool size ≥ **0.80**; or
- **(b)** the (era × pool-tertile) cross-tab has **fewer than two off-diagonal cells with n ≥ 20**; or
- **(c)** every era's 95 % interval on skill contains the pooled skill of −0.0966.

If NOT SEPARABLE, **no decomposition is published** — the era table is published as a description
with its intervals, and the answer to OPEN_ITEMS §1.4 is that the sample cannot answer it.
If SEPARABLE on all three, the decomposition is published with the caveats §7 lists.

## 6. S5 — power, so a null is read as "not detectable at this n"

Per era, the minimum detectable Brier skill at 80 % power for that era's own n and observed score
dispersion, by the protocol §6 convention, published beside every era's point estimate. Intervals
are **stationary block bootstrap** (Politis–Romano), the protocol's registered estimator, at the
registered seed 19900802, with the tier's registered 35-day clustering rule — reads within 35 days
are one cluster, so the era intervals respect the same dependence rule the headline does.

## 7. What this diagnostic cannot do, registered before it is read

- It **cannot** establish that the engine has skill. A confounded negative is not a positive.
- It **cannot** re-judge run `walk_20260903T003422Z` or any other. Amendment E.1 governs.
- It **cannot** separate label basis from era **at all** if §5(b) fails on that pair too; the
  daily tier begins in 1987 and OPEN_ITEMS's "100 % dyadic in 1946–73" is a monthly-tier fact
  quoted for context, not a fact about the 150 reads under test.
- It is computed on **150 reads across four bins, two of which have n = 2 and n = 10.** Whatever
  it finds about those two bins is description, not inference, and is labelled as such in the
  output rather than in a footnote.

## 8. Outputs

`docs/g/ERA_CONFOUND.json`, `docs/g/ERA_CONFOUND.md`, `src/g_era_confound.py` (reads `oil.db` and
`data/walk_forward/**` **read-only**, writes no table), `tests/test_g_era_confound.py`, and a
handoff to B and to the owner of `OPEN_ITEMS.md`.
