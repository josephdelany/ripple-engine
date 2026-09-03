# B → Cowork, 2026-09-03 — the walk IS re-run: `walk_20260903T052633Z`

**The waiting sentence can change.** The rebuild has landed in the database *and* the walk has now been
re-run on it. Every number in sections 8–11 moves; several move enough to change what the section says.
Full registered draws, filtration audit clean (0 violations over 15,241 checks), leakage binding.

## 1. The headline table, same axis

| | old target (`…003422Z`) | **new target (`…052633Z`)** | p old → new |
|---|---|---|---|
| **G n_scored** | 150 | **100** | — |
| G Brier vs climatology | −0.0966 | **−0.0838** | 0.0225 → **0.0758** |
| G Brier vs frozen | +0.0074 | **+0.0372** | 0.0294 → **0.0006** |
| G Brier vs random analogs | −0.0212 | −0.0156 | 0.583 → 0.730 |
| G Brier vs persistence | −0.6000 | **−0.3035** | 0.0002 → 0.0248 |
| **G RPS vs persistence** | −0.7906 | **−0.1748** | <0.0001 → **0.2596** |
| G RPS vs climatology | −0.0127 | −0.0031 | 0.770 → 0.954 |
| P CRPS vs climatology | −0.0705 | −0.0738 | 0.016 → 0.011 |
| P CRPS vs persistence | +0.1285 | +0.1337 | <0.0001 |
| P CRPS vs frozen | +0.0070 | +0.0105 | 0.0001 |
| block permutation p | 0.1239 | **0.0500** | — |
| SPA (G) | 0.645 | 0.341 | — |
| spec curve median / share positive | −0.0754 / 0.000 | −0.0769 / **0.000** | — |
| power: G MDS at n | 0.1268 (n 150) | **0.1365 (n 100)** | — |

Verdicts unchanged in kind: `engine:G` **SUGGESTIVE / null** (−0.0838, DM p 0.076, SPA 0.341);
`engine:P` **SUGGESTIVE / null** (−0.0738, DM p 0.011, SPA 0.964). §7's label audit is still unpassed, so
nothing can be VALIDATED regardless.

## 2. Two sentences in the paper that must change, not just their numbers

1. **"Persistence beats the engine decisively" is no longer decisive on the ordinal score.** G RPS vs
   persistence goes −0.7906 → **−0.1748 at p 0.2596**. On Brier it survives (−0.3035, p 0.0248) but at half
   its former size. The finding is now *persistence beats the engine on Brier; on RPS the gap is not
   distinguishable from zero at n = 100.* Amendment L's motivation — that the level estimand is mis-anchored —
   rests on the Brier number and still stands, but the RPS figure should not be quoted as it was.
2. **The block permutation p is 0.0500, which is NOT below the registered 0.05.** §7's condition is strict.
   It must not be written as "p = 0.05, significant" or rounded. It is a knife-edge and reads as one.

## 3. The placebo: a registered prediction that failed

Amendment N (registered `56ca1db`, **before** the code) predicted the source-event cluster bootstrap would
widen the interval ≈2.24× and flip `null_holds` false → true. **It did not.** Measured widening **1.28×**;
corrected interval **[−0.1187, −0.0201]**, still excluding zero, p 0.0111. **`null_holds` stays false — the
placebo null still fails.**

The reason is B's arithmetic error, and it belongs in the record: the cluster count was derived by
*division* (411 rows ÷ 5 registered reps = 82 events) rather than measured. The placebo loop skips a source
event when its VIX decile has no matched candidate, so the real panel is **416 rows over 190 source events —
2.19 reps per event, not 5**. The largest possible widening was √(416/190) = 1.48. The registration was
wrong in its arithmetic and right in its procedure: the number was written down first, so the failure is
visible rather than absorbed.

**The decomposition (Amendment N.6), because this run carried two changes:**

| comparison | target delta (B−A) | estimator delta (C−B) |
|---|---|---|
| vs random analogs | **−0.0222** | +0.0020 |
| vs climatology | **−0.0187** | +0.0023 |
| fair vs climatology | **−0.0312** | −0.0017 |

**The rebuilt target moved the placebo an order of magnitude more than the estimator did, and moved it
against the engine.** Both estimators are published in the same object permanently, so the correction is
auditable without a re-run; per-read rows are now sealed to `placebo_rows.jsonl`.

## 4. Nothing was inherited — tested, not asserted

Compared event by event against the archived old reads, all 313: outcome label moved on **59**, L⁻ on **62**,
the pool's `climatology.G_labels` on **151**, item analog labels on **140**. Persistence fallback **2 → 50**;
`n_persistence_known` **151 → 96**. Content digest changed. This was the most likely place for something
silently stale and there is nothing stale in it.

## 5. The Amendment L/M delta experiment is re-run (N.7)

| | old | new |
|---|---|---|
| derived from | `…003422Z` | `…052633Z` |
| n_retained | 150 | **89** (11 excluded, persistence fallback) |
| ΔIES share zero | 0.7333 | 0.7303 |
| C1 vs no-change | +0.0336 (p 0.181) | +0.0505 (p 0.243) |
| analogue alone vs no-change | +0.0012 (p 0.980) | −0.0246 (p 0.764) |
| MDS at n | 0.0666 | **0.1167** |
| **verdict** | NO ADDITION | **NO ADDITION** |
| Amendment M, C1 vs C0 | −0.0037 (p 0.766) | +0.0169 (p 0.439) |

The verdict is unchanged and the reading is unchanged: no separation between pooling with the retrieved
analogues and pooling with the base rate. Note the MDS nearly doubled — at n = 89 this test can only see a
skill of 0.117 or larger, so the null is weaker evidence than it was, not stronger.

## 6. What is NOT re-run

`data/grid/price/**` is unaffected — the grid price arm never reads `event_outcomes` and its unit is a date.
`data/grid/power_arithmetic.json`'s **event-triggered G baseline** (n_eff 148.5) was computed from the old
sealed run and now belongs to the old target; its P baseline (249.1) is unaffected. That file's conclusions
do not depend on the G baseline, but the number should carry the old run id if it is quoted.
