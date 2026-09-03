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
- ~~Not transferable to the event walk without re-running it.~~ **Now tested there too — see §2 below. It does
  not transfer, and the reason is the more interesting result.**
- Nothing here is VALIDATED. §7's label audit is unpassed and this is a grid-arm result whose unit is a date.

## Provenance

Registered `caa345b` before any code. Both targets published side by side in
`data/grid/price/summary.json` (`fitted_vs` for raw, `abnormal_return_target` for abnormal) and the raw
result is **not withdrawn** — it is the number the paper reported and it stays on the record as what a
raw-return target produces. Model diagnostics, dropped-cell counts, SPA and FDR are in the same object.


---

# 2. The same test on the EVENT walk — and it gives the opposite answer

*Amendment O, registered `2151a71` before the code, computed from the sealed run `walk_20260903T052633Z`
with no re-run: the analogs' identities and weights, the Hedge weights and the cluster structure are held
exactly as sealed, and only each analog's outcome value is replaced by its abnormal counterpart.
n = 246 scored; 17 events dropped for a short estimation window, 47 analog atoms dropped, all counted.*

| engine vs | RAW skill | RAW p | ABNORMAL skill | ABNORMAL p |
|---|---|---|---|---|
| **climatology** | −0.0738 | 0.011 | **−0.0588** | **0.033** |
| persistence | +0.1337 | <0.0001 | +0.1488 | <0.0001 |
| random analogs | −0.0066 | 0.807 | +0.0060 | 0.817 |
| frozen | +0.0105 | <0.0001 | +0.0102 | <0.0001 |

**SPA (benchmark climatology): p = 0.533.** BH-FDR: 3 of 4 survive — `vs_persistence`, `vs_frozen`,
`vs_climatology`. `vs_random_analogs` does not.

## The event walk lands on Amendment O's FIRST branch, not the grid's

**The loss to climatology narrows but persists and stays significant** (−0.074 → −0.059, p 0.033, surviving
FDR). So on the walk the paper actually reports, **A1 is a real limitation but it is _not_ the cause of the
price null.** The published price number stands, with the caveat that a quarter of the measured loss was
target definition.

**And retrieval still does not beat random analogs here** (+0.006, p 0.82) — where on the grid, on the same
corrected target, it beat them by +0.0705 at p < 0.0001, surviving FDR.

## Why the two arms disagree — a hypothesis the numbers support, not a demonstrated mechanism

The two arms differ in exactly one structural way that bears on this: **the event walk's climatology pool is
class-filtered and the grid's is not.** `src/engine/read.py:208` restricts every candidate to the target's
own event class, and climatology is then computed from that same pool — which is Tier-1 **A2**. So on the
event walk, climatology already carries class conditioning for free; on the grid, climatology is the pool of
all prior grid dates and carries none.

That predicts precisely what is observed: removing the market process from the target (A1) helps the engine
against a *weak, unconditional* climatology and not against a *strong, class-conditioned* one. It also
explains why beating random analogs — which are drawn from the same pool as climatology — separates on the
grid and not on the walk.

**Stated as a hypothesis.** It is consistent with both arms and with A2's documented mechanism, and it is
falsifiable: re-run the event walk with the class filter removed and the two arms should converge.

> ## RETRACTED 2026-09-03 — the hypothesis above is WRONG, and it was tested rather than left standing
>
> Amendment P (registered `a69bd15` **before** the run, with this outcome named in advance as P.3's third
> branch) removed the class filter and re-ran the walk. **The arms did not converge. The engine got
> dramatically worse on every comparison.**
>
> | | class-filtered | unfiltered |
> |---|---|---|
> | G Brier vs climatology | −0.084 (p 0.076) | **−0.369 (p < 0.0001)** |
> | G Brier vs random analogs | −0.016 (p 0.73) | **−0.252 (p 0.0003)** |
> | G Brier vs persistence | −0.304 (p 0.025) | **−0.635 (p < 0.0001)** |
> | P CRPS vs climatology | −0.074 (p 0.011) | **−0.114 (p < 0.0001)** |
> | P CRPS vs random analogs | −0.007 (p 0.81) | −0.013 (p 0.55) |
>
> **The correct reading is P.3's third branch: class membership carries real information that the state
> vector cannot recover.** Given a free choice over all prior history, the similarity metric selects *worse*
> precedents than when it is confined to the event's own class. The class filter was not inflating the
> baseline — it was doing genuine work that the 13 macro-financial fields and 4 dyad flags cannot reproduce.
>
> *Caveat, stated because it weakens the comparison:* the read sets are not identical (G n 100 → 123, P
> n 246 → 296), because an unfiltered pool clears the burn-in for events a class-filtered pool cannot. The
> direction is far too large to be an artefact of that, but the magnitudes are not strictly paired.
>
> **Why this matters for the central finding, and it strengthens it.** The registered experiment
> (`data/structural_surface/summary.json`) shows structural weighting beats surface-class weighting *within
> the same candidate pool*. This result shows that *removing* the class boundary altogether is worse than
> keeping it. Together they say something sharper than either alone:
>
> > **Event class is a useful coarse filter and a bad fine-grained weight.** Use it to bound which history
> > is admissible; do not use it to decide which of the admissible cases matters most. That is precisely the
> > distinction between the two arms of the central experiment, and both halves of it are now measured.

## What the paper must now say about price

1. **The grid arm's loss to climatology was a target artefact and must be retracted** (§1).
2. **The event arm's loss is not.** It survives the correction at p 0.033 and FDR, and it is the number the
   paper reports. It stands, with the size of the target effect stated: about a quarter of it.
3. **Retrieval beats random analogs on the grid and not on the walk**, on the same corrected target. The
   difference is a property of the *baseline*, not of the retrieval, and A2 is the candidate explanation.
4. **Nothing beats climatology under SPA on either arm** (grid p 0.466, walk p 0.533). No positive price
   claim against climatology is available from either.
