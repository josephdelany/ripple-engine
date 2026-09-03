# B → Cowork, 2026-09-03 — section 14.1: CORRECTED numbers, and one claim that must be pulled

**The numbers I gave you for 14.1 were computed with a defective interval. The point estimates stand; two
p-values move materially and one claim has to be restated.** Everything below is from the corrected run in
`data/grid/price/summary.json` and every interval now resamples **whole grid dates**.

## 1. What was wrong

The first cut flattened the T × A × H score array to one 10,857-cell vector and resampled it with a block
length measured in **dates**. Adjacent entries in that flat vector are *different targets at the same date* —
Brent and WTI 20-day returns correlate **0.906** — so a block of two in flattened index space is not a block
in time. Every interval was computed as though there were ~10,857 quasi-independent observations, where this
study's own arithmetic (`data/grid/power_arithmetic.json`) says the effective n is **1,979**.

This is the exact failure the grid study exists to prevent, committed in my own inference rather than in my
counting. A test now asserts the invariant — every published block carries `n_dates` and `n_cells`, and only
`n_dates` is inferential.

## 2. The corrected table for 14.1

n_dates 413 (n_cells 10,857). Registered CRPS is the gate score.

| comparison | skill | 95 % CI | DM p | survives BH-FDR (19 tests, q 0.05) |
|---|---|---|---|---|
| **fitted vs frozen** | +0.0013 | −0.0104 … +0.0128 | **0.820** | no |
| fitted vs grid-climatology | **−0.0706** | −0.0826 … −0.0587 | <0.0001 | **yes** |
| fitted vs no-change | +0.1844 | +0.1721 … +0.1963 | <0.0001 | **yes** |
| **fitted vs random analogs** | **+0.0102** | **−0.0004 … +0.0212** | **0.0524** | **no** (q 0.062) |
| frozen vs random analogs | +0.0095 | −0.0011 … +0.0211 | 0.082 | no (q 0.092) |

**SPA (Hansen), benchmark grid-climatology, models {fitted, frozen, random analogs, no-change}: p = 0.703**,
best model `fitted` with a mean gain of **−0.0105**. Nothing beats climatology, and the registered guard says
so directly. The SPA and the FDR were both **missing from my first cut** — §3.2 inherits §6 unchanged, which
includes them — and are now computed.

**Ferro size-corrected diagnostic:** +0.0085, CI −0.0027 … +0.0198, **p 0.128** (I previously reported 0.076;
that too was the flattened interval). **PIT:** fitted `[1751, 778, 819, 842, 1192, 1334, 835, 814, 815, 1532]`
against climatology's near-flat `[1178, 983, 1061, 1056, 1067, 1140, 1088, 1090, 1105, 1095]`.

## 3. What changes in the three things you put in 14.1

**(a) Fitting does not beat the registered constants — UNCHANGED, and slightly stronger.** +0.0013, CI
−0.0104 … +0.0128, p **0.820** (I reported 0.642). At n_eff 1,979 with the fit legitimate by the pre-declared
floor, this remains a real either-way test that fell toward *the constants were already at the achievable
optimum*. Keep the 15-selections-across-414-reads trajectory beside it.

**(b) The climatology loss — UNCHANGED.** −0.0706, survives FDR, on all six targets and all five horizons.
Gate decides; the Ferro correction and the PIT sit beside it, unpromoted. One correction to the diagnostic's
own strength: the size-corrected comparison is **not** significant (p 0.128), so the honest reading is
*the engine is indistinguishable from climatology once the small-k penalty is removed*, not *it wins*.

**(c) The random-analogs finding — MUST BE RESTATED.** +0.0102 at **p 0.0524**, interval touching zero, and
**it does not survive the multiplicity correction** (q 0.062, rank 16 of 19). It is not "measurable work".

## 4. On the scoping of finding 4 — the direction holds, the strength does not

Joe's joint statement was: *pooling-not-similarity is an escalation result at n = 150; on price at n_eff
2,000 the similarity metric does measurable work; retrieval is underpowered and over-sharp, not worthless.*

**The direction survives and the scoping is right.** The contrast is real — the event panel could not
separate retrieval from random analogs (−0.021, p 0.58) and the grid comes within a whisker of doing so
(+0.010, p 0.052). Suggested wording, which is narrower than the draft and I think stronger for it:

> On the event panel, retrieval was indistinguishable from random draws from the same pool (−0.021,
> p 0.58) and interchangeable with the base rate inside the pool (§11.3). On the grid price panel, at an
> effective n roughly thirteen times larger, the same comparison reaches +0.010 with p 0.052 and an
> interval touching zero — at the edge of detectability, and not surviving correction for the nineteen
> comparisons reported alongside it. The pattern is **consistent with** retrieval carrying a small real
> signal that the event panel was too small to see; it does not establish one.

**Two cautions on the mechanism.** The two panels differ in unit (event vs date), target (escalation vs
price), score (Brier vs CRPS) **and** n. Attributing the difference to power alone picks one of four changes.
And the PIT says the forecast is over-sharp on the grid too, so "underpowered and over-sharp" is well
supported as a description of the *forecast*, while "underpowered" as the explanation for the *event panel's*
null remains an inference rather than a measurement.

## 5. Standing

Nothing here re-judges an event-triggered number (`GRID_STUDY_REGISTRATION` §0.2). The unit is `date`; the
event panel's unit is `event`; the two are never pooled. `src/walk.py` remains frozen until K's rebuild
lands, and this arm never reads `event_outcomes`.
