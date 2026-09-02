# B_run_delta — every number that moved, run 182828Z → 193022Z (Brief 2, B-5)

Both runs: full registered draws, daily tier, IES-90 target under OUTCOME_MAPPING Amendment 2 rows
(computed 2026-09-02T18:25Z). What changed between them is the code of Brief B-1..B-4 (protocol Amendments
B, C, D): G-persistence as the fourth G baseline, M13 in the menu (Hedge over 13 items, M13 refitted inside
the permutation and spec-curve replays), and the sealed-run archive. Same corpus, same seeds. Numbers are
from `data/walk_forward/summary.json` of each run (182828Z's summary is archived in
`data/walk_forward/runs/walk_20260902T182828Z/`; its figures were quoted in `release_check_2026-09-02.md`).

## D4 status
**Closed on the published file.** `tiers.daily.G.engine_vs` now carries four references
(climatology, frozen, random_analogs, persistence); `G.spa_vs_persistence` and `n_persistence_fallback`
(2 of 153 geopolitical reads fell back to climatology) are published. P had four already.
`acceptance_v2 --dod` D4 reads on this file.

## Registered scores (daily tier, engine = Hedge mixture)

| comparison | 182828Z | 193022Z | moved by |
|---|---|---|---|
| G Brier vs climatology, skill | −0.0070 (CI −0.084..+0.065, DM p 0.847) | −0.0053 (CI −0.083..+0.067, p 0.884) | +0.0017 |
| G Brier vs frozen | −0.0026 (p 0.131) | −0.0024 (CI −0.006..+0.001, p 0.167) | +0.0002 |
| G Brier vs random analogs | +0.0622 (CI −0.008..+0.130, p 0.068) | +0.0638 (CI −0.006..+0.131, p 0.063) | +0.0016 |
| **G Brier vs persistence** | — (not computed) | **−0.4669 (CI −1.031..−0.133, p 0.002)** | new |
| G SPA (family vs climatology) | p 0.793, best M07 | p 0.743 (RC 0.906), best M07 | −0.050 |
| G SPA vs persistence | — | p 0.567, best M07 | new |
| G RPS vs climatology | +0.0718 (CI −0.008..+0.151, p 0.076) | +0.0757 (CI −0.006..+0.156, p 0.064) | +0.0039 |
| G RPS vs random analogs | +0.1398 (CI +0.061..+0.219, p 0.001) | +0.1435 (CI +0.064..+0.223, p <0.001) | +0.0037 |
| G RPS vs persistence | — | −0.6343 (CI −1.347..−0.217, p 0.001) | new |
| DEAL binary Brier vs climatology (n 66) | −0.2179 (CI −0.857..+0.072) | −0.2185 (CI −0.861..+0.074) | −0.0006 |
| P CRPS vs climatology | −0.0279 (CI −0.062..+0.008, p 0.136) | −0.0297 (CI −0.064..+0.006, p 0.111) | −0.0018 |
| P CRPS vs persistence | +0.1632 (CI +0.121..+0.210, p <0.001) | +0.1617 (CI +0.120..+0.208, p <0.001) | −0.0015 |
| P CRPS vs random analogs | +0.0350 (CI −0.002..+0.077, p 0.053) | +0.0333 (CI −0.003..+0.075, p 0.063) | −0.0017 |
| P CRPS vs frozen | +0.0013 (p 0.051) | +0.0014 (CI +0.000..+0.003, p 0.022) | +0.0001 |
| P SPA | p 0.937, best M07 | p 0.937 (RC 0.991), best M07 | 0 |
| M precision / recall (n 253, base 0.225) | 0.337 / 0.544 | 0.337 / 0.544 | 0 |

The engine's own G and P numbers move by thousandths: the thirteenth item enters the Hedge mixture with
weight 1/13 and is driven to 3.6e-05 by its losses, so the engine is the twelve-item engine plus noise.

## Tests of the test

| block | 182828Z | 193022Z |
|---|---|---|
| label permutation (G, i.i.d. within class), observed skill / p | +0.0005 / 0.008 | +0.0133 / 0.002 |
| placebo, size-matched (null_holds) | −0.024 (CI −0.053..+0.007), true | −0.018 (CI −0.048..+0.011), true |
| placebo vs climatology | −0.081 (CI −0.112..−0.048) | −0.075 (CI −0.106..−0.043) |
| placebo, size-corrected vs climatology | −0.008 (CI −0.043..+0.028) | −0.001 (CI −0.036..+0.032) |
| spec curve (54 specs): min / median / max / share positive | −0.098 / −0.023 / +0.015 / 0.17 | −0.105 / −0.017 / +0.023 / 0.22 |
| leakage test | filtration binding | filtration binding; recalibration rule also asserted (M13 differs on the break_recal run) |
| FDR family size / BH survivors | 31 / 3 | 34 / 8 (see below) |
| verdict | G null, P null | G null, P null; M13 SUGGESTIVE / null |
| seal check | 1565 records, 5 runs in the tree | 313 in the tree (run 193022Z); 6 prior runs archived, each re-verified (192906Z is the run I aborted to add a limits line: 313 reads archived, its weights rows were lost to the kill — recorded, not dropped) |

The permutation observed skill moved from +0.0005 to +0.0133 because the replay now includes M13 (its
recalibrator is refitted from the permuted labels inside `skill_for`); the null distribution moved with
it. The i.i.d. permutation ignores the 35-day clustering (D3 finding); the block permutation of Amendment
F.2 is in the next run.

## M13 (Amendment C), as computed

| | value |
|---|---|
| M13 Brier vs climatology | **−0.5898** (CI −0.834..−0.357, DM p 3e-8, n 150) |
| M13 RPS vs climatology | −0.1900 (DM p 0.004) |
| reads recalibrated / scored | 214 / 253; first active at n_fit 40; final n_fit 172 |
| final modes by level | 0 isotonic, 1 Platt, 2 isotonic, 3 isotonic |
| final Hedge weight (G) | 3.6e-05 (the twelve weightings: 0.030–0.128) |
| status (§7) | SUGGESTIVE / null |

Reliability terms (Murphy decomposition, per level: reliability / resolution):

| level | engine | M13 | climatology |
|---|---|---|---|
| 0 | 0.0021 / 0.0333 | 0.1026 / 0.0207 | 0.0063 / 0.0004 |
| 1 | 0.0006 / 0.0005 | 0.2703 / 0.0009 | 0.0000 / 0.0000 |
| 2 | 0.0420 / 0.0026 | 0.0723 / 0.0034 | 0.0198 / 0.0017 |
| 3 | 0.0344 / 0.0081 | 0.0339 / 0.0173 | 0.0224 / 0.0248 |

Reading: the recalibration made calibration **worse** on levels 0, 1 and 2 (reliability up 50× on level 0,
from 0.002 to 0.103) and only kept level 3's. The expanding isotonic fit on 40–170 reads is a step
function that swings with each new closed outcome; the Platt fit on level 1 has six positives in the whole
corpus to learn from. The Hedge loop saw the losses and removed M13 from the mixture within the first
active reads. The hypothesis of Amendment C — that calibration learned strictly from the past recovers
the skill the permutation test hints at — is **not supported as registered**. Figures:
`figures/reliability_G_<level>.png` (engine vs climatology vs M13, 95 % bands).

## G-persistence (Amendment B), as computed

Persistence — 0.9 on the dyad's IES level over [t−90, t−1], 0.1 on the neighbours — **beats the engine**
on Brier (engine skill vs persistence −0.467) and on RPS (−0.634), and beats every menu item (SPA vs
persistence p 0.567, best item M07). Two of 153 geopolitical reads fell back to climatology. Escalation
levels persist over 90 days; the analog engine does not use the target's own recent history (its state
vector has no "current dyad level" field). That is the finding the fourth baseline exists to produce.

## FDR family (34 comparisons; BH q 0.05)

Survivors: `G:engine_vs_persistence` (negative: persistence wins), `G:M03_market_only_vs_climatology`,
`G:M13_recalibrated_vs_climatology` (negative), `P:engine_vs_persistence` (positive), and four P items vs
climatology (M02, M03, M06, M09). "Survives" is two-sided: three of the eight are the engine or an item
being *worse*.

## What is unchanged
Corpus (313 events, 184 IES-90 levels, 3 uncovered, 95 DEAL flags), menu M01–M12, seeds, burn-in, tiers.
Nothing about run 182828Z is re-judged (Amendment E.1).
