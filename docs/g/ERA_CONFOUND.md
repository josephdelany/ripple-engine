# G-6 — OPEN_ITEMS 1.4, the era confound: can the three confounds be separated at n = 150?
*Computed by `src/g_era_confound.py` under `docs/g/G6_ERA_CONFOUND_REGISTRATION.md`, which was
committed first. Generated 2026-09-03T05:39:10+00:00.*

> **This is a DIAGNOSTIC. It gates nothing.** It re-judges no run, moves no threshold and changes
> no published verdict. `WALK_FORWARD_PROTOCOL.md` Amendment E.1 governs which score judges a v2
> run and this does not touch it.

## 0. The answer

- **Separable? **NO**** — criteria fired: `(a) |rho(era, pool)| >= 0.80`, `(c) every era interval contains the pooled skill`.
- No decomposition is published; the era table stands as a description with its intervals, and OPEN_ITEMS 1.4's question is answered 'the sample cannot separate them'.
- **S4, the size-correction test: FAILS** — registered-Brier era spread **0.1845**, fair-Brier era spread **0.3512**, ratio **1.904** against a threshold of 0.5.
  FAILS: the era gradient survives size correction; the artefact is not the whole story.

## 0b. Three things §4 of the registration got wrong, before anything else

- **The premise was false.** §4 derived its magnitude from a constant engine atom count of 5. `n_atoms_engine` ranges **5–22** and rises with era. That was a wrong statement about the inputs, not a prediction that failed.
- **The magnitude was ~5× too large.** Measured differential inflation swings **0.0159** across eras against the **0.068** registered. Direction supported, size not.
- **The statistic was excluded by G's own §7.** S4 was a spread over four bins, two with n = 2 and n = 10, which §7 says are description and not inference — and those two bins drove the failure. It is left failed rather than swapped, because replacing a test after seeing it fail is the move this project exists to prevent.

## 1. The baseline check — the published number, re-derived before anything was stratified

    published:  {"n": 150, "engine_mean": 0.7687487109093333, "ref_mean": 0.7010597406851313, "skill": -0.09655235680492913}
    recomputed: {"n": 150, "engine_mean": 0.7687487109093333, "ref_mean": 0.7010597406851313, "skill": -0.09655235680492913}
    agrees:     True

Run pinned to `walk_20260903T003422Z`. `scores.jsonl` in the tree holds `walk_20260903T003422Z` (313 rows), `walk_20260903T052633Z` (313 rows) — see §5 of the handoff; the second run is excluded by `run_id` and reported, not acted on.

## 2. The era table, on both scores

### registered Brier (what the headline uses)

| era | n | clusters | skill | 95 % CI | min detectable @80 % | pool median (min–max) | base rate L0 | dyadic share | k engine | k clim |
|---|---|---|---|---|---|---|---|---|---|---|
| 1987-99 | 2 | 2 | **+0.0086** | [-1.171, +0.209] | 0.987 | 8 (8–9) | 0.236 | 1.0 | 6 | 8 |
| 2000-09 | 10 | 8 | **+0.0675** | [-0.194, +0.255] | 0.319 | 10 (8–15) | 0.295 | 0.5 | 8 | 10 |
| 2010-19 | 51 | 28 | **-0.1035** | [-0.285, -0.001] | 0.195 | 18 (8–31) | 0.377 | 0.1707 | 11 | 18 |
| 2020-26 | 87 | 20 | **-0.1169** | [-0.216, -0.035] | 0.133 | 36 (14–56) | 0.454 | 0.0192 | 14 | 36 |

### fair Brier (Ferro size-corrected, Amendment E)

| era | n | clusters | skill | 95 % CI | min detectable @80 % | pool median (min–max) | base rate L0 | dyadic share | k engine | k clim |
|---|---|---|---|---|---|---|---|---|---|---|
| 1987-99 | 2 | 2 | **+0.1275** | [-1.175, +0.280] | 1.040 | 8 (8–9) | 0.236 | 1.0 | 6 | 8 |
| 2000-09 | 10 | 8 | **+0.3347** | [+0.101, +0.538] | 0.304 | 10 (8–15) | 0.295 | 0.5 | 8 | 10 |
| 2010-19 | 51 | 28 | **+0.0124** | [-0.139, +0.124] | 0.188 | 18 (8–31) | 0.377 | 0.1707 | 11 | 18 |
| 2020-26 | 87 | 20 | **-0.0165** | [-0.122, +0.074] | 0.142 | 36 (14–56) | 0.454 | 0.0192 | 14 | 36 |

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
| `era_index~pool_g` | +0.848 |
| `era_index~base_rate_0` | +0.436 |
| `era_index~dyadic` | +0.424 |
| `era_index~date_ordinal` | +1.000 |
| `pool_g~base_rate_0` | +0.356 |
| `pool_g~dyadic` | +0.356 |
| `pool_g~date_ordinal` | +0.848 |
| `base_rate_0~dyadic` | +0.239 |
| `base_rate_0~date_ordinal` | +0.436 |
| `dyadic~date_ordinal` | +0.424 |

Condition number of the standardised design: **3.3**.

Pool-size range by era — if these do not overlap, era and pool size are the same variable in this
sample and no n repairs it:

| era | n | pool min | pool max |
|---|---|---|---|
| 1987-99 | 2 | 8 | 9 |
| 2000-09 | 10 | 8 | 15 |
| 2010-19 | 51 | 8 | 31 |
| 2020-26 | 87 | 14 | 56 |

(era × pool tertile) support — separation needs cells **off** the diagonal:

| cell | n |
|---|---|
| `1987-99|low` | 2 |
| `2000-09|low` | 10 |
| `2010-19|low` | 31 |
| `2010-19|mid` | 20 |
| `2020-26|high` | 48 |
| `2020-26|low` | 10 |
| `2020-26|mid` | 29 |

Off-diagonal cells with n ≥ 20: **2** ([{'cell': '2010-19|low', 'n': 31}, {'cell': '2020-26|mid', 'n': 29}]).

## 5. The verdict, under the rule fixed before the numbers

```
{
 "separable": false,
 "criteria_fired": [
  "(a) |rho(era, pool)| >= 0.80",
  "(c) every era interval contains the pooled skill"
 ],
 "rho_era_pool": 0.848003911284946,
 "off_diagonal_cells": 2,
 "era_ci_contains_pooled": {
  "1987-99": true,
  "2000-09": true,
  "2010-19": true,
  "2020-26": true
 },
 "pooled_skill": -0.09655235680492913,
 "rule": "G6_REGISTRATION \u00a75, fixed before the numbers. NOT SEPARABLE if any of (a), (b), (c). If NOT SEPARABLE, no decomposition is published.",
 "consequence": "No decomposition is published; the era table stands as a description with its intervals, and OPEN_ITEMS 1.4's question is answered 'the sample cannot separate them'."
}
```

## 5b. The post-hoc diagnostics (Amendment 1 A1.5; they gate nothing)

**D1 — the identity that collapses two confounds into one.** `n_atoms_clim == n_pool_g` on **150 of 150** reads, exactly. Climatology's atom count IS the pool size. The 'pool-size confound' and the 'size artefact' are one variable under two names, not two of OPEN_ITEMS 1.4's three confounds.

**D2 — the differential inflation, measured by era.**

| era | n | k engine | k clim | S_e/k_e − S_c/k_c |
|---|---|---|---|---|
| 1987-99 | 2 | 6.5 | 8.5 | +0.0259 |
| 2000-09 | 10 | 8.0 | 10.5 | +0.0242 |
| 2010-19 | 51 | 11.0 | 18.0 | +0.0319 |
| 2020-26 | 87 | 14.0 | 36.0 | +0.0401 |

§4 assumed k_engine constant at 5; it ranges 5-22 and rises with era, so the differential inflation swings ~0.014, not 0.068 -- about a tenth of the era gradient, not most of it. Direction supported, magnitude not.

**D3 — the two bins that carry the sample** (§7's caveat applied, not a post-hoc cut). A level statement, never a spread:

| era | n | registered skill | fair skill | shift |
|---|---|---|---|---|
| 2010-19 | 51 | -0.1035 | +0.0124 | +0.1158 |
| 2020-26 | 87 | -0.1169 | -0.0165 | +0.1005 |

**D4 — the level shift under correction.** Engine mean -0.1121, climatology -0.0303 — the engine benefits **3.7×** more. S/k is not Ferro's correction; the level effect is larger.

> **Already published by session B, and confirmed here rather than discovered:** summary.json tiers.daily.G.diagnostic_fair.engine_vs_climatology: n 150, skill +0.021, CI [-0.067, +0.111], DM p 0.635, registered: false. G confirms this number and did not discover it.


## 6. What this cannot do

- It cannot establish that the engine has skill. A confounded negative is not a positive.
- It cannot re-judge run `walk_20260903T003422Z` or any other; Amendment E.1 governs.
- It cannot separate label basis from era where the cross-tab has no off-diagonal support, and the daily tier begins in 1987 — OPEN_ITEMS's '100 % dyadic in 1946–73' is a monthly-tier fact quoted for context, not a fact about these 150 reads.
- It is computed on 150 reads across four bins, two of which have n = 2 and n = 10.