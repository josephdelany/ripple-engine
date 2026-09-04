> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** Working record of the pre-1973 admission and vintage work. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../../SUBMISSION_STATUS.md).

# G-6 — OPEN_ITEMS 1.4, the era confound: can the three confounds be separated at n = 150?
*Computed by `src/g_era_confound.py` under `docs/g/G6_ERA_CONFOUND_REGISTRATION.md`, which was
committed first. Generated 2026-09-03T16:19:54+00:00.*

> **This is a DIAGNOSTIC. It gates nothing.** It re-judges no run, moves no threshold and changes
> no published verdict. `WALK_FORWARD_PROTOCOL.md` Amendment E.1 governs which score judges a v2
> run and this does not touch it.

## 0. The answer

- **Separable? **NO**** — criteria fired: `(b) < 2 off-diagonal cells with n >= 20`, `(c) every era interval contains the pooled skill`.
- No decomposition is published; the era table stands as a description with its intervals, and OPEN_ITEMS 1.4's question is answered 'the sample cannot separate them'.
- **S4, the size-correction test: FAILS** — registered-Brier era spread **0.4434**, fair-Brier era spread **0.4370**, ratio **0.985** against a threshold of 0.5.
  FAILS: the era gradient survives size correction; the artefact is not the whole story.

## 0b. Three things §4 of the registration got wrong, before anything else

- **The premise was false.** §4 derived its magnitude from a constant engine atom count of 5. `n_atoms_engine` ranges **4–21** and rises with era. That was a wrong statement about the inputs, not a prediction that failed.
- **The magnitude was far too large.** Measured differential inflation swings **0.0094** across the bins large enough to read (n ≥ 8) against the **0.068** registered. Direction supported, size not. (All-bins spread 0.0687 — dominated by the smallest bin, the same defect that sank S4; both are published.)
- **The statistic was excluded by G's own §7.** S4 was a spread over four bins, two with n = 2 and n = 10, which §7 says are description and not inference — and those two bins drove the failure. It is left failed rather than swapped, because replacing a test after seeing it fail is the move this project exists to prevent.

## 1. The baseline check — the published number, re-derived before anything was stratified

    published:  {"run_id": "walk_20260903T052633Z", "n": 100, "engine_mean": 0.7098438901199999, "ref_mean": 0.6549544740591895, "skill": -0.08380646019657534}
    recomputed: {"n": 100, "engine_mean": 0.7098438901199999, "ref_mean": 0.6549544740591895, "skill": -0.08380646019657534}
    agrees:     True

Run pinned to `walk_20260903T052633Z`. `scores.jsonl` in the tree holds `walk_20260903T052633Z` (313 rows) — see §5 of the handoff; the second run is excluded by `run_id` and reported, not acted on.

## 2. The era table, on both scores

### registered Brier (what the headline uses)

| era | n | clusters | skill | 95 % CI | min detectable @80 % | pool median (min–max) | base rate L0 | dyadic share | k engine | k clim |
|---|---|---|---|---|---|---|---|---|---|---|
| 1987-99 | 1 | 1 | **+0.2858** | — | — | 8 (8–8) | 0.125 | 1.0 | 7 | 8 |
| 2000-09 | 8 | 7 | **+0.0403** | [-0.256, +0.279] | 0.374 | 10 (8–14) | 0.215 | 0.5 | 8 | 10 |
| 2010-19 | 39 | 25 | **-0.1576** | [-0.275, -0.016] | 0.174 | 19 (8–27) | 0.402 | 0.1538 | 10 | 19 |
| 2020-26 | 52 | 26 | **-0.0515** | [-0.198, +0.078] | 0.202 | 33 (10–45) | 0.546 | 0.0192 | 12 | 33 |

### fair Brier (Ferro size-corrected, Amendment E)

| era | n | clusters | skill | 95 % CI | min detectable @80 % | pool median (min–max) | base rate L0 | dyadic share | k engine | k clim |
|---|---|---|---|---|---|---|---|---|---|---|
| 1987-99 | 1 | 1 | **+0.4107** | — | — | 8 (8–8) | 0.125 | 1.0 | 7 | 8 |
| 2000-09 | 8 | 7 | **+0.3764** | [+0.078, +0.639] | 0.395 | 10 (8–14) | 0.215 | 0.5 | 8 | 10 |
| 2010-19 | 39 | 25 | **-0.0262** | [-0.135, +0.120] | 0.175 | 19 (8–27) | 0.402 | 0.1538 | 10 | 19 |
| 2020-26 | 52 | 26 | **+0.0910** | [-0.035, +0.203] | 0.174 | 33 (10–45) | 0.546 | 0.0192 | 12 | 33 |

**Two of the four bins have n = 2 and n = 10.** Whatever those rows show is description, not
inference (§7), and no weight is placed on them here.

## 3. Why the two scores differ — the mechanism, registered before it was measured

§4: the fair-Brier era gradient is materially flatter than the registered-Brier one, because the engine's k-atom inflation is constant at S/5 while climatology's shrinks as S/pool, and pool grows with era. Registered magnitude: the artefact swings ~0.068 in absolute Brier, ~0.10 in skill, against an observed era spread of 0.126.

The `k engine` and `k clim` columns above are the atom counts the correction acts on. The engine's
is fixed by its analog count; climatology's is the pool, and the pool grows with time. That is the
whole mechanism, and it is visible in the table without any modelling.

## 4. Separability (§5)

| pair | Spearman ρ |
|---|---|
| `era_index~pool_g` | +0.718 |
| `era_index~base_rate_0` | +0.637 |
| `era_index~dyadic` | +0.519 |
| `era_index~date_ordinal` | +1.000 |
| `pool_g~base_rate_0` | +0.034 |
| `pool_g~dyadic` | +0.410 |
| `pool_g~date_ordinal` | +0.718 |
| `base_rate_0~dyadic` | +0.250 |
| `base_rate_0~date_ordinal` | +0.637 |
| `dyadic~date_ordinal` | +0.519 |

Condition number of the standardised design: **3.5**.

Pool-size range by era — if these do not overlap, era and pool size are the same variable in this
sample and no n repairs it:

| era | n | pool min | pool max |
|---|---|---|---|
| 1987-99 | 1 | 8 | 8 |
| 2000-09 | 8 | 8 | 14 |
| 2010-19 | 39 | 8 | 27 |
| 2020-26 | 52 | 10 | 45 |

(era × pool tertile) support — separation needs cells **off** the diagonal:

| cell | n |
|---|---|
| `1987-99|low` | 1 |
| `2000-09|low` | 8 |
| `2010-19|low` | 14 |
| `2010-19|mid` | 25 |
| `2020-26|high` | 31 |
| `2020-26|low` | 11 |
| `2020-26|mid` | 10 |

Off-diagonal cells with n ≥ 20: **0** (none).

## 5. The verdict, under the rule fixed before the numbers

```
{
 "separable": false,
 "criteria_fired": [
  "(b) < 2 off-diagonal cells with n >= 20",
  "(c) every era interval contains the pooled skill"
 ],
 "rho_era_pool": 0.7175277527752776,
 "off_diagonal_cells": 0,
 "era_ci_contains_pooled": {
  "2000-09": true,
  "2010-19": true,
  "2020-26": true
 },
 "pooled_skill": -0.08380646019657534,
 "rule": "G6_REGISTRATION \u00a75, fixed before the numbers. NOT SEPARABLE if any of (a), (b), (c). If NOT SEPARABLE, no decomposition is published.",
 "consequence": "No decomposition is published; the era table stands as a description with its intervals, and OPEN_ITEMS 1.4's question is answered 'the sample cannot separate them'."
}
```

## 5b. The post-hoc diagnostics (Amendment 1 A1.5; they gate nothing)

**D1 — the identity that collapses two confounds into one.** `n_atoms_clim == n_pool_g` on **100 of 100** reads, exactly. Climatology's atom count IS the pool size. The 'pool-size confound' and the 'size artefact' are one variable under two names, not two of OPEN_ITEMS 1.4's three confounds.

**D2 — the differential inflation, measured by era.**

| era | n | k engine | k clim | S_e/k_e − S_c/k_c |
|---|---|---|---|---|
| 1987-99 | 1 | 7.0 | 8.0 | -0.0273 |
| 2000-09 | 8 | 7.5 | 10.0 | +0.0320 |
| 2010-19 | 39 | 10.0 | 19.0 | +0.0401 |
| 2020-26 | 52 | 12.5 | 33.0 | +0.0414 |

§4 assumed k_engine constant at 5; it ranges 4-21 and rises with era, so the differential inflation across the bins large enough to read (n >= 8) swings 0.0094 against the 0.068 registered -- a small fraction of the era gradient, not most of it. Direction supported, magnitude not.

> A spread over era bins is dominated by the smallest bins -- the same defect that sank the registered S4 statistic (A1.3). The all-bins figure is reported and the n >= 8 figure is the one the reading uses. On the superseded run the all-bins swing was 0.016; on this run it is inflated by a single-read bin.

**D3 — the two bins that carry the sample** (§7's caveat applied, not a post-hoc cut). A level statement, never a spread:

| era | n | registered skill | fair skill | shift |
|---|---|---|---|---|
| 2020-26 | 52 | -0.0515 | +0.0910 | +0.1425 |

**D4 — the level shift under correction.** Engine mean -0.1350, climatology -0.0362 — the engine benefits **3.7×** more. S/k is not Ferro's correction; the level effect is larger.

> **Already published by session B, and confirmed here rather than discovered:** summary.json tiers.daily.G.diagnostic_fair.engine_vs_climatology: n 150, skill +0.021, CI [-0.067, +0.111], DM p 0.635, registered: false. G confirms this number and did not discover it.


## 6. What this cannot do

- It cannot establish that the engine has skill. A confounded negative is not a positive.
- It cannot re-judge run `walk_20260903T052633Z` or any other; Amendment E.1 governs.
- It cannot separate label basis from era where the cross-tab has no off-diagonal support, and the daily tier begins in 1987 — OPEN_ITEMS's '100 % dyadic in 1946–73' is a monthly-tier fact quoted for context, not a fact about these 150 reads.
- It is computed on 150 reads across four bins, two of which have n = 2 and n = 10.