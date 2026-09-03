# The crack-concentration finding, tested — and it does not survive

*Session B, 2026-09-03. `OIL_FINDINGS` §4 reports that geopolitical classes coincide with top-5 %
diesel-crack moves 1.9–2.5× more often than with top-5 % crude moves, labelled testable-but-untested.
It is now tested. **The descriptive ratio reproduces exactly. The inference does not survive.***

---

## 0. The answer first

| | pooled, all 7 classes | pooled, 4 geopolitical classes | per class |
|---|---|---|---|
| **exact McNemar** (pairs independent) | **p = 0.0024** | **p = 0.00002** | best raw p = 0.0347 |
| **cluster-robust** (35-day clusters) | **p = 0.658** | **p = 0.435** | best p = 0.227 |
| **BH-FDR across the 7-class family** | — | — | **0 of 7 survive**, on either p-value |

**Verdict: NOT SUPPORTED.** The effect that looks decisive at p = 0.00002 is an artefact of treating
127 discordant pairs as 127 independent observations. They sit in **30 clusters**. Corrected for that,
there is no detectable asymmetry.

---

## 1. The 44 vs 45 inconsistency, resolved before anything was tested

`infrastructure_attack` showed n = 44 against crude and n = 45 against the crack. Same events, different
denominator — so one of the two was wrong, or the samples were not the same events.

**Neither. It is a coverage artefact, and it is the whole problem in miniature.** The two series do not
start on the same day:

- `fred.DCOILBRENTEU` (Brent) first observation **1987-05-20**
- `derived.diesel_crack` first observation **1986-06-02**

Four `infrastructure_attack` events predate Brent (`abqaiq_arabian_1977`, `iran_oilworkers_strike_1978`,
`kharg_strikes_1985`, `iraq_kharg_1986`); only three predate the crack. The difference is exactly one
event — **`iraq_kharg_1986`, 1986-08-12** — which is scoreable against the crack and not against crude.
48 − 4 = 44; 48 − 3 = 45.

The eligibility rule was **verified, not assumed**: reconstructing "event_date within [series first,
series last]" reproduces **all fourteen published denominators exactly**, both assets, all seven classes.

**Consequence for the test.** McNemar requires the same units scored twice. `iraq_kharg_1986` is not,
so it leaves the paired sample. The paired window is the intersection of the two series,
**1987-05-20 … 2026-08-25**, giving **299 of 313 corpus events**.

---

## 2. The paired table

An event "hits" an asset if it appears in the `events` list of at least one registered Big Moves episode
for that asset. Built from `data/big_moves/{brent,diesel_crack}.json` at event level, not from the margins.

| class | n | crude hits | crack hits | ratio | both | crude-only | crack-only | discordant | **clusters** |
|---|---|---|---|---|---|---|---|---|---|
| chokepoint_disruption | 26 | 4 (15.4 %) | 10 (38.5 %) | **2.50×** | 2 | 2 | 8 | 10 | 8 |
| conflict_escalation | 50 | 12 (24.0 %) | 23 (46.0 %) | **1.92×** | 6 | 6 | 17 | 23 | 11 |
| infrastructure_attack | 44 | 6 (13.6 %) | 15 (34.1 %) | **2.50×** | 1 | 5 | 14 | 19 | **6** |
| sanctions | 55 | 8 (14.5 %) | 19 (34.5 %) | **2.38×** | 2 | 6 | 17 | 23 | 10 |
| opec_decision | 51 | 16 | 13 | 0.81× | 5 | 11 | 8 | 19 | 15 |
| policy_response | 56 | 18 | 20 | 1.11× | 6 | 12 | 14 | 26 | 9 |
| demand_shock | 17 | 6 | 5 | 0.83× | 2 | 4 | 3 | 7 | 6 |
| **POOLED (all)** | **299** | 70 | 105 | 1.50× | 24 | 46 | 81 | 127 | **30** |
| **POOLED (geopolitical)** | **175** | 30 | 67 | 2.23× | — | 19 | 56 | 75 | **23** |

**§4's descriptive claim reproduces exactly**: the four geopolitical classes run 1.92×–2.50×, and the
three non-geopolitical classes do not (0.81×–1.11×). The pattern §4 describes is really in the data.

---

## 3. Why the exact test overstates it

McNemar's exact binomial asks: of the discordant pairs, is the split 50/50? It assumes **each discordant
pair is an independent draw.** These are not. The registered 35-day clustering rule (`robustness.assign_clusters`)
puts the 299 paired events into 92 clusters, and the discordant pairs into far fewer:

- pooled: **127 discordant pairs in 30 clusters** — 4.2 pairs per cluster
- geopolitical: **75 discordant pairs in 23 clusters**
- `infrastructure_attack`: **19 discordant pairs in 6 clusters** — a single crack episode containing
  several corpus events contributes many "crack-only" pairs *at once*, and they are one observation of
  the world, not fourteen.

**The cluster-robust test.** Under the null of symmetry, each discordant pair is equally likely to be
crude-only or crack-only; the correct randomisation flips **whole clusters** rather than individual pairs.
20,000 draws, seed 19900802, statistic |crack-only − crude-only|:

| | exact | cluster-robust |
|---|---|---|
| pooled, all classes | 0.00242 | **0.65757** |
| pooled, geopolitical | 0.00002 | **0.43548** |
| chokepoint_disruption | 0.10938 | 0.22739 |
| conflict_escalation | 0.03469 | 0.50242 |
| sanctions | 0.03469 | 0.50427 |
| infrastructure_attack | 0.06357 | 0.84586 |
| opec_decision | 0.64761 | 0.67167 |
| policy_response | 0.84502 | 0.91650 |
| demand_shock | 1.00000 | 1.00000 |

A p-value moving from 0.00002 to 0.435 is not a marginal adjustment. It says the entire apparent
significance came from counting one clustered episode many times.

**BH-FDR across the seven-class family, q = 0.05: 0 of 7 survive**, on either p-value. Under the exact
p's the best q is 0.121 (conflict_escalation, sanctions); under the cluster-robust p's every q is 1.000.

---

## 4. What may and may not be said

**May be said.** Geopolitical classes coincide with large diesel-crack moves about 2.2× as often as with
large crude moves (30 vs 67 hits over 175 events), and non-geopolitical classes show no such gap. This is
a **description of the corpus**, reported with its n.

**May not be said.** That the difference is statistically established. It is not, at this n, with these
events, at their true unit of dependence. §4 should carry the ratio and the cluster-robust p, and should
not be quoted as a tested asymmetry.

**Not a null of the phenomenon.** 23 discordant clusters cannot detect much; this is "not detectable at
this n", not "no effect". Distinguishing them needs more independent episodes, which means the corpus,
not the estimator.

**What would settle it.** Move to the date grid rather than the event corpus. `data/grid/power_arithmetic.json`
puts a month-end grid at n_eff ≈ 1,979 against the event panel's 249, with the crack among the six
registered targets — the same question asked where the units are not clustered into 30 blocks.

---

## 5. Reproduction

Paired table built from `data/big_moves/{brent,diesel_crack}.json` `episodes[].events[].id`, joined to
`events` in `data/oil.db`, restricted to the intersection window, clustered by `robustness.assign_clusters`
at the registered 35 days. Exact binomial by `math.comb`; cluster randomisation 20,000 draws at the
registered seed 19900802; BH-FDR by `engine.inference.bh_fdr` at q = 0.05.

## 6. The pattern this makes three times

The grid price arm reported p = 0.010 on 10,857 flattened cells that were 413 dates; corrected, 0.052.
The walk's placebo reported an interval on 411 pseudo-reads that were 190 source events. This finding
reported p = 0.00002 on 127 discordant pairs that are 30 clusters. Three different studies, three
different authors, one error: **the number of rows was mistaken for the number of independent
observations.** The instrument that catches it is cheap — count the clusters before computing the p —
and it belongs in the review checklist rather than in a third post-mortem.
