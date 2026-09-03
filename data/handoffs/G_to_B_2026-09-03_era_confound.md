# G → B (and to whoever owns OPEN_ITEMS.md), 2026-09-03 — item 1.4: the sample cannot separate the confounds, and one of them is not a separate confound at all

Item **1.4** is registered to B in `OPEN_ITEMS.md`; Joe reassigned it to G on 2026-09-03. Registered
first in `docs/g/G6_ERA_CONFOUND_REGISTRATION.md` (+ Amendment 1), computed by
`src/g_era_confound.py`, published at `docs/g/ERA_CONFOUND.{json,md}`. **Diagnostic only — it gates
nothing, re-judges no run and writes no table.** `data/walk_forward/**` was read, never written.

## 1. The answer to the question Joe actually asked

> *"Whether the three confounds can be separated at all at this n, and if they cannot, say so rather
> than reporting a decomposition the sample cannot support."*

**They cannot. NOT SEPARABLE**, under the rule fixed before the numbers (§5). Two of the three
criteria fired:

- **(a)** Spearman ρ(era index, pool size) = **+0.848**, against a registered bar of 0.80.
- **(c)** **Every** era's 95 % cluster-bootstrap interval contains the pooled skill of −0.0966.

Criterion (b) did **not** fire — there are 2 off-diagonal (era × pool-tertile) cells with n ≥ 20
(`2010-19|low` n=31, `2020-26|mid` n=29) — and the condition number of the standardised design is
only **3.3**. So the honest statement is narrower than "the design is degenerate": the era pattern
is **not distinguishable from the pooled result at this n**, and era and pool size are nearly the
same variable. **No decomposition is published**, per §5.

## 2. The finding that changes the shape of item 1.4

**`n_atoms_clim == n_pool_g` on 150 of 150 reads, exactly.** Climatology's atom count *is* the pool
size, because climatology is the pool's own label frequencies.

So of the three confounds OPEN_ITEMS 1.4 lists — pool size, base rate, label basis — **"pool size"
and "the k-atom size artefact" are one variable under two names.** Correcting for either corrects
for the other. Item 1.4 is not three confounds plus a size correction; it is:

| | ρ with era |
|---|---|
| pool size ≡ climatology's k | **+0.848** |
| base rate (level-0 share of the read's own pool) | +0.436 |
| label basis (dyadic) | +0.424 |

Base rate and label basis move with era **far more weakly** than pool size does. If 1.4 is to be
worked further, it is a **pool-size** problem with two minor passengers, not a three-way tie.

The label-basis premise does hold on the daily tier, for the record: dyadic share by era runs
**100 % (n=2) → 50 % → 12 % → 2 %**, and reads with *no* basis recorded rise to 35 of 87 by 2020–26.

## 3. The era table, as description (no decomposition, per §5)

| era | n | registered skill | 95 % CI | min detectable @80 % | pool median | k clim | base rate L0 | dyadic |
|---|---|---|---|---|---|---|---|---|
| 1987–99 | 2 | +0.0086 | — | — | 8.5 | 8.5 | — | 1.00 |
| 2000–09 | 10 | +0.0675 | wide | — | 10.5 | 10.5 | — | 0.50 |
| 2010–19 | 51 | −0.1035 | contains −0.097 | — | 18.0 | 18.0 | — | 0.12 |
| 2020–26 | 87 | −0.1169 | contains −0.097 | — | 36.0 | 36.0 | — | 0.02 |

Full numbers in `ERA_CONFOUND.json`. **Two of the four bins have n = 2 and n = 10** and are
description, not inference — that was registered in §7 before the numbers, and it matters below.

## 4. Three things G's own registration got wrong, reported rather than quietly fixed

§4 of the registration predicted, with a number, that the size artefact would explain most of the
era gradient. **The registered test S4 FAILED and is left failed** — its threshold was not moved and
the statistic was not re-cut. Why it failed:

1. **The premise was false.** §4 derived everything from a constant engine atom count of 5, read off
   one inspected row. `n_atoms_engine` actually ranges **5–22** and rises with era (median 6.5 → 14).
   That was a wrong statement about the inputs, not a prediction that failed; one more read would
   have caught it.
2. **The magnitude was ~5× too large.** Because both atom counts grow together, the measured
   differential inflation `S_e/k_e − S_c/k_c` swings **0.016** across eras against the **0.068**
   registered — roughly a tenth of the era gradient, not most of it. Direction supported, size not.
3. **The statistic was one G's own §7 excludes.** S4 was a spread across four bins; the two bins with
   n = 2 and n = 10 read +0.128 and +0.335 under fair Brier and drove the failure single-handed.

## 5. What the size correction does do, on the bins that carry the sample

Applying §7's registered caveat (not a post-hoc cut), the two bins with n ≥ 50:

| era | n | registered skill | fair skill | shift |
|---|---|---|---|---|
| 2010–19 | 51 | −0.1035 | **+0.0124** | +0.116 |
| 2020–26 | 87 | −0.1169 | **−0.0165** | +0.100 |

Pooled, the correction moves the engine's mean by **−0.112** and climatology's by **−0.030** — the
engine benefits **3.7×** more, which is what finite-k theory predicts when `k_engine < k_clim`
throughout (6.5 vs 8.5 … 14 vs 36).

**This is your number, not G's.** `summary.json` already publishes
`tiers.daily.G.diagnostic_fair.engine_vs_climatology`: n 150, skill **+0.021**, CI [−0.067, +0.111],
DM p 0.635, `registered: false`. G confirms it and did not discover it. **Amendment E.1 governs**:
the registered scores judge every v2 run, and nothing here touches that.

The careful statement, and G will not go further than it: the published −0.097 is **consistent with**
being substantially a finite-k artefact, and this diagnostic **cannot demonstrate** that, because era,
pool size and k are not separately identified in these 150 reads. That is item 1.4's answer.

## 6. Two things for you specifically

- **`data/walk_forward/scores.jsonl` currently holds two runs** — `walk_20260903T003422Z` (313 rows)
  and `walk_20260903T052633Z` (313 rows) — while `summary.json` describes the first and is older on
  disk (23:23 vs 01:28). Amendment D says the sealed logs hold the current run only, with earlier runs
  archived. Either you are mid-run and the archive step has not fired, or the invariant is not
  holding. G pinned by `run_id`, reported it, and did not act on it. **Anything that reads that file
  without filtering is currently mixing two runs**, and the second gives n=100, skill −0.084.
- **If 1.4 is worked further**, the lever is pool size, and the cleanest design G can see is to hold
  `k_clim` fixed by construction — score climatology on a fixed-size subsample of the pool — so that
  era varies while k does not. At n = 150 that will not have power either, but it would at least be
  identified, which the present design is not.
