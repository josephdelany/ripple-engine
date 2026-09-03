# Tier-1 A1, answered: the price loss was a target artefact — and one finding gets stronger

*Session B, 2026-09-03. Registered before computation in `GRID_STUDY_REGISTRATION.md` Part III
Amendment 2 (commit `caa345b`), with the three admissible outcomes and their meanings fixed in advance.
Computed on the grid price arm, run `data/grid/price/summary.json`, 175 registered candidates.*

---

## The claim under test

`docs/audit/01_TIER1_design_defects.md` A1: the price target is a raw return with no market model, so
climatology is approximately the unconditional distribution of 20-day oil returns, and

> *the price null follows from the target definition, before analogy enters the picture.*

If that is right, the paper's price section does not test what it says it tests. It had to be settled
before anything was rewritten around it.

## The test

The **same engine, the same analogs, the same baselines, the same 35-day cluster structure and the same
inference** — only the target changed. Expected return estimated on 250 trading days ending 21 trading days
before each read, so a read's own horizon can never enter its own benchmark; constant-mean model for crude
and gas, market model on Brent for the cracks (a crack is a margin, and its expected move *given crude* is
what must be removed); minimum 100 observations or the read is dropped and counted (246 cells dropped).

## The result

| fitted engine vs | RAW return | ABNORMAL return |
|---|---|---|
| **grid-climatology** | **−0.0706** (p < 0.0001) | **+0.0063** (p 0.70) |
| **random analogs** | +0.0102 (p 0.052) | **+0.0705** (p < 0.0001) |
| no-change | +0.1844 (p < 0.0001) | +0.2492 (p < 0.0001) |
| frozen (fitted vs fixed weights) | +0.0013 (p 0.82) | +0.0011 (p 0.94) |

**Multiplicity guards, on the abnormal arm's own family:** SPA (Hansen, benchmark grid-climatology,
models {fitted, frozen, random analogs, no-change}) **p = 0.466**. BH-FDR across the ten reported
comparisons: **2 of 10 survive** — `vs no_change` and `vs random_analogs`. No per-target comparison
survives.

## What this establishes, and what it does not

**1. A1 is upheld on its central claim, and a published result must be retracted.** The engine's decisive
*loss* to climatology — −0.0706 at p < 0.0001, which survives FDR on the raw arm — **disappears entirely**
once the market process is removed from the target. It becomes +0.0063 at p 0.70. That loss was a property
of the target definition, not of the engine. **The price section's "the engine is worse than the
unconditional distribution" cannot stand as written.**

**2. The engine does not beat climatology either.** +0.0063 is a tie, not a win, and SPA over the family
returns p 0.466 — under the guard, nothing beats climatology. The honest replacement claim is
**indistinguishable from climatology on abnormal returns**, which is a materially different statement from
both the published one and from a success.

**3. The finding that gets stronger, and it is the first positive result here that survives its own
correction.** On abnormal returns the engine beats **random analogs drawn from the same point-in-time pool**
by **+0.0705, p < 0.0001, surviving BH-FDR.** That is similarity retrieval carrying measurable information
about the response — the identical comparison that was null on the event panel (−0.021, p 0.58) and
borderline on the raw grid (+0.010, p 0.052, failing FDR). Same engine, same k, same pool; the difference
is that the target now contains the event's contribution rather than being dominated by the oil market.

> **Retrieval was never the weak part. The target was.**

**4. Fitting still does not beat fixed weights**, on either target (p 0.82 raw, p 0.94 abnormal). The
registered constants remain at the achievable optimum, and Part III §3.4's either-way finding is unchanged.

## What this does not license

- Not a claim of skill against climatology. SPA says no.
- Not a per-target claim. Nothing survives FDR per target, and `gasoline_crack` runs the *opposite* way
  (−0.058, p 0.030 raw) — a mixed sign set is not a story.
- Not transferable to the event walk without re-running it. This is the **grid** arm, unit = date. The event
  walk still scores raw returns (`src/engine/read.py:148–177`) and its price numbers still carry A1 in full.
  **The obvious next step is the same target change on the event walk**, which would test whether the
  published event-level price null is the same artefact.
- Nothing here is VALIDATED. §7's label audit is unpassed and this is a grid-arm result whose unit is a date.

## Provenance

Registered `caa345b` before any code. Both targets published side by side in
`data/grid/price/summary.json` (`fitted_vs` for raw, `abnormal_return_target` for abnormal) and the raw
result is **not withdrawn** — it is the number the paper reported and it stays on the record as what a
raw-return target produces. Model diagnostics, dropped-cell counts, SPA and FDR are in the same object.
