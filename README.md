# Historical analogy in geopolitical and oil-market forecasting

**Can historical precedent be turned into a systematic, point-in-time forecasting tool for
geopolitical shocks and oil markets?**

Joseph Delany · Colby College · 2026
**[One page](docs/BRIEF.md)** · **[Full paper](docs/PAPER_DRAFT.md)** ·
**[Propagation study](docs/RIPPLE_FINDINGS.md)** · **[What to read first](INDEX.md)** ·
**[Adversarial audit of this project](docs/ADVERSARIAL_AUDIT.md)** · **[Open items](OPEN_ITEMS.md)**

---

## The question

Analysts reason by precedent. *This confrontation looks like 1990, not like 2019.* The
reasoning is everywhere in geopolitical risk work and it is almost never tested, because
testing it requires something awkward: you have to ask not just whether history contains
patterns, but whether those patterns were **available to an analyst at the time**.

That distinction is the whole project. A political-risk index published in 2024 describes
2018 accurately — and tells you nothing an analyst could have used in 2018. A forecasting
system that quietly consumes such a variable is not reasoning from history; it is
reasoning from hindsight, and it will look skilful for the wrong reason.

So: does formalised historical analogy contain out-of-sample predictive information about
geopolitical escalation and oil prices, once hindsight is removed?

**Three conditions have to hold for it to.** The state you compute similarity on must be
*knowable at the forecast date*, not merely recorded for it. The pool of prior cases must be
*dense* enough that "most similar precedent" means something. And the target must carry
information *beyond its own recent history*. Failure of any one is enough to sink the method, and
none of them is about whether history rhymes — the first is a claim about archives, the second
about sample size, the third about the outcome variable. **All three fail on this record, and the
paper measures by how much** ([§1.1](docs/PAPER_DRAFT.md), §13.1).

## The data

**313** dated geopolitical and policy shocks, 1973–2026, human-gated under a codebook.
**27** academic and government sources — Correlates of War, ICB, UCDP, ATOP, Polity,
V-Dem, SIPRI, Archigos, UNGA ideal points, GPR, EIA, CFTC, World Bank, IMF, FRED, Energy
Institute, Kilian — assembled into a world-state panel of 352k rows. **772** price and
macro series back to 1946.

Escalation outcomes are computed from **ICB, COW MID, COW War and UCDP**, never from our
own corpus — after our own coded outcomes were tested against those datasets and scored
κ ≈ 0, at which point they were retired.

## The method

```
     event at t
         │
         ▼
  ┌──────────────────┐
  │  VINTAGE FILTER  │   only information demonstrably available on date t
  └──────────────────┘
         │
         ▼
   world-state vector  ──▶  similar prior events  ──▶  outcome distribution
                                                              │
                                                              ▼
                                                     forecast, SEALED (hashed)
                                                              │
                                            ┌─────────────────┴──────────────┐
                                            ▼                                ▼
                                   observed outcome at t+90        four baselines:
                                            │                      climatology, persistence,
                                            ▼                      random analogues, frozen
                                    proper scoring rules
```

Pre-registered; amendments dated and appended, never edits; every result published as
computed.

## Three results

*Run `walk_20260903T052633Z`, on the escalation target as rebuilt under Amendment 4
(184 labelled events → 132; 100 scored).*

| | |
|---:|:---|
| **−0.084** | escalation Brier skill vs the base rate (95% CI −0.175 … **+0.004**, *p* = 0.076). Worse than climatology — but at *n* = 100 the interval **crosses zero**, so not distinguishably so. |
| **−0.304** | escalation skill vs **persistence**. The dyad's own last 90 days score 0.545 against the engine's 0.710 (*p* = 0.025). On the **ordinal** score the same gap is −0.175 at *p* = 0.26 — not distinguishable from zero. A registered follow-up found this gap was the *estimand*, not the analogies — see below. |
| **+0.134** | price CRPS skill vs persistence (95% CI +0.076 … +0.193, *p* < 0.001). The one comparison the analogue engine wins, and the only sign stable across every run. |

On **price** the engine *is* significantly worse than the base rate (−0.074, CI −0.140 … −0.021,
*p* = 0.011). On **escalation**, at this sample size, it is not.

## The finding

An earlier run of the same code showed **parity** with the base rate (−0.005). Those runs
took the per-event state fields as *coded* rather than as *knowable*. Enforcing the vintage
rule on them revealed that **262 of 313 events have no state field demonstrably available
on the day** — and the apparent signal disappeared with it.

A second registered amendment then rebuilt the *target*: the "ongoing conflict → no level" rule
was extended to COW War and UCDP GED, and a missing covering record stopped silently reading as
level 0. That took the escalation target from 184 labelled events to **132** (100 scored) and
moved 59 of 187 labels. **Both amendments made the result smaller and less certain, and both
were committed before the code that implemented them.**

> The analogical structure the engine appeared to find was, to a first approximation,
> hindsight.

![The vintage rule, and what it cost](docs/figures/fig1_vintage.png)

*Left: the corpus split by whether any state field was knowable at t
(`data/state/situation_knowable.json`). Right: escalation Brier skill vs climatology before
and after Amendment H (`data/walk_forward/summary.json` ·
`tiers.daily.G.engine_vs.climatology`; the before-run from `STATE_OF_THE_ENGINE.md` §5 and
`data/handoffs/B_run_delta.md`). Drawn by `src/figures_paper.py`.*

Two explanations for the null were then registered in writing and tested. **Both were
falsified.** Walk-forward recalibration made escalation worse (−0.700). The
label-permutation test that had rejected "the engine is noise" at *p* = 0.002 before the
vintage amendment now sits at ***p* = 0.0500** — exactly on the registered threshold, over
1,000 permutations whose resolution is 0.001. Reported as a knife-edge, read as nothing.

### The baselines, in full

![Escalation: what each rule actually scores](docs/figures/fig2_escalation_baselines.png)

*Brier score, lower is better. Source: `data/walk_forward/summary.json` ·
`tiers.daily.G.engine_vs.*` and `tiers.daily.G.items_vs_climatology.M13_recalibrated`.
Drawn by `src/figures_paper.py`.*

![Price: CRPS skill against each of the four baselines](docs/figures/fig3_price_baselines.png)

*CRPS skill with 95% intervals; grey where the interval crosses zero. Source:
`data/walk_forward/summary.json` · `tiers.daily.P.engine_vs.*`. Drawn by
`src/figures_paper.py`.*

## The follow-up that repaired the question — and did not rescue the answer

The −0.304 above asks the engine to forecast the escalation *level* from scratch, while
persistence starts from the answer. Re-anchoring the identical sealed reads on the
**change** — same twelve items, same sealed weights, same analogs, nothing re-retrieved —
moves the mixture from **0.682 to 0.506** against persistence's 0.494. Most of the deficit
was a missing anchor.

Asked the fair question — *does analogy add anything once the dyad's own recent state is
known?* — the registered verdict is **NO ADDITION**: +0.034 Brier skill, DM *p* = 0.181,
permutation *p* = 0.124, nothing surviving FDR, against a measured minimum detectable skill
of 0.067. Not "no effect": *not detectable at n = 150*.

And a registered control separates the two things that pooling can be doing. Substituting
the class's unconditional change distribution for the retrieved analogues scores **0.4626
against 0.4643** — paired difference −0.004, *p* = 0.766. **The gain is pooling, not
similarity.** The retrieval step, which is the whole idea of the engine, is
interchangeable with the base rate.

## Two companion results from the same infrastructure

**Market attribution.** Inverting the usual event study — taking the market's largest moves
rather than our chosen events — **14 of 44 largest Brent moves have no identifiable event
in the corpus**, and in 14 of the 28 attributed episodes *every* attributed event was
already public more than 20 trading days before the move began. Geopolitical classes are
under-represented inside big **crude** moves and 2–3× over-represented inside big
**diesel-crack** moves: shocks express themselves in refining margins more than in crude.

**Propagation.** A registered, placebo-controlled local-projection study of crude →
products → cracks → gas/LNG → fertilizer → freight → credit: **21 of 477 cells transmit,
against 1–24 expected under no transmission at all**. The same estimator recovers Känzig's
(2021) published oil-supply-news shock cleanly at every horizon — the silence is not an
instrument failure. **A follow-up study on physical outcomes issues two errata against that
result** and they are published beside it, not folded into it: the study's one transmitting
*physical* cell (Cape of Good Hope transits) was estimated on a Brent trading-day index that
discards weekends, and tanker transits happen at weekends — on the full calendar record it
covers zero at all nine horizons, so that hop has **zero** transmitting cells, not one. And
the monthly hops ran with no placebo, so "zero of 54 at fertilizer" was arithmetic about a
flag rather than a finding about fertilizer. The physical study also found the record goes
dark where it matters: Iran stops reporting production in **2018-07**, the month secondary
sanctions were reimposed.

## What this does not claim

Not that historical analogy fails. The narrower, defensible claim: **this implementation,
under a strict point-in-time information constraint, did not outperform simple baselines
for escalation** — on a corpus whose historical arm is thin (8 events in the 1970s) and
whose state vector is mostly unavailable at read time. Measured power puts the minimum
detectable escalation skill at **0.137**; detecting +0.05 would need roughly 1,200
scored reads against **100** today.

## Research integrity

Pre-registration with git timestamps · dated amendments, never edits · independent outcome
labels after our own scored κ ≈ 0 · sealed reads hashed before outcomes are looked up ·
four baselines · Diebold–Mariano, stationary bootstrap, Reality Check / SPA, permutation,
matched placebo, regime blocks, a 162-cell specification curve · a filtration audit of
**15,241** point-in-time checks with zero violations · two independent runs reproducing the
same content digest · two adversarial reviews · **four published retractions of the
project's own earlier positive findings.**

## Run it

```
./go                      # refresh, rebuild, open http://127.0.0.1:5050/app
make reproduce            # rebuild summary.json from source, full registered draws
pytest -q                 # 447 passed, 15 skipped
```

The desk: Feed (market state, gated stream), Story (any development read in a desk's
order), Big moves, Walk (open any sealed read and its score), Ledger (claims that resolve
from data).

## Where it is going

`PATH.md` is the route. The change-estimand experiment that this section used to
name as next has been run, and its answer is above.

### Update: the density route has a first answer

The grid ran. 476 month-end dates 1987–2026, six price targets, five horizons, **10,857 scored
cells** — and an *effective* sample of **1,979** against 249 for the event panel, because
nominal counts are never reported as effective ones here. Thirteen times the evidence, and
enough that fitting parameters becomes legitimate rather than overfitting.

**Fitting did not help.** With the block weights and metric scale fitted by nested
walk-forward cross-validation, the fitted model beats the frozen registered constants by
**+0.001 CRPS skill, *p* = 0.820** — a registered either-way test that fell on the side of
*the constants were already at the achievable optimum*. The fitted weights never converge:
15 distinct selections across 414 reads, the modal one taking 24.9%.

**And one thing moved, to the edge of detectability.** At n = 150 the engine could not
separate from randomly drawn analogs at all. On the grid the point estimate turns positive
and the interval only just includes zero: **+0.010, CI [−0.0004, +0.021], *p* = 0.052**, not
surviving the study's own multiplicity correction. That is *consistent with* retrieval
carrying a small real signal the event panel was too small to see — it does not establish one.
The PIT histogram independently shows the forecast is too sharp, which is a measured fact
where "underpowered" remains an inference.

All inference resamples whole grid dates: **413 dates** is the inferential *n*, and the 10,857
cells are a cell count, never an *n*.

The open problem is *n*: 150 scored escalation reads against a measured requirement of
~1,200. The registered route was backwards — expand the pre-1987 corpus — and that route is
now measured shut: six pre-1974 records built to the full sourcing standard buy **zero**
scored reads, and the four that matter most are unscoreable on both branches, because
monthly WTI before 1973 carries 16 distinct values in 324 months. The remaining route is
forwards in density: make the unit of observation a **date** rather than an event, scoring
on a periodic grid across multiple horizons and price targets, with escalation labels at
the dyad-date level. That is a different question, registered as a new study — and it also
removes the selection problem the Big Moves census exposes, since scoring only on chosen
events never tests the engine on the days the market actually moved.
