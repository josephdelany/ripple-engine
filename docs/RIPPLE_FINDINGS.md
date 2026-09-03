# The ripple study — findings

*2026-09-02, session C. Written from `data/ripple/*.json` only. **No computation was run to
produce this document**: every estimate below was already in those files, and the only new
arithmetic is the pass-through ratios of §2, which divide two stored coefficients and carry
their delta-method interval — the script that did it is quoted in Appendix A so the division
can be checked. The design was sealed in `RIPPLE_REGISTRATION.md` at 15:42:38 and the estimator
first appeared at 15:59:32, seventeen minutes later (Appendix A). Verdict words are the
registered three: **TRANSMITTING / NULL / INSUFFICIENT**.*

**The one-sentence result.** Across 477 node×shock cells the chain is, with a handful of
exceptions at its two ends, silent: 21 cells transmit where between 1 and 24 would transmit if
nothing transmitted at all, and the registered expectation that some tightening class beats a
volatility-and-geopolitics-matched placebo at Brent fails.

---

## 0. The chain, named

    crude → refined products → cracks → gas / LNG → fertilizer → freight proxies → credit

with the physical system (refinery runs, stocks, imports, chokepoint transits) hanging off the
crude and product hops, and macro (breakevens, dollar, volatility, metals, equities) beside the
chain as cross-checks, never inside it. Every node, its series id and its transform are in
`RIPPLE_REGISTRATION.md` Table N. The shocks are the seven corpus event classes plus two pooled
sets: **tightening** (chokepoint ∪ infrastructure ∪ conflict) and **all**.

De-overlapped shock counts on the daily grid (35-calendar-day chain rule, Amendment A):
chokepoint 21, infrastructure 26, conflict 44, OPEC 50, sanctions 42, demand 16, policy 39;
tightening 68, all 103.

---

## 1. What transmits, what is null, what is insufficient

### 1.1 The tally

| verdict | cells |
|---|---|
| TRANSMITTING | 21 |
| NULL | 401 |
| INSUFFICIENT | 55 |
| **total** | **477** |
| of the NULL, FRAGILE (the two standard errors disagree on zero) | 0 |

**Read this against its base rate, not against zero.** A cell is TRANSMITTING only if the 95%
band excludes zero **and** the coefficient falls outside the central 95% of 500 placebo draws
matched on the volatility and geopolitical-risk state **and** the Newey–West band agrees. Under
a complete null the first condition alone fires on about 5% of cells and the second on about
5%, and the two are driven by the same coefficient so they are far from independent: the
expected count under no transmission anywhere is somewhere between **1 and 24 cells**. The
observed 21 sits inside that interval. Nothing in this section should be read as a discovery.

### 1.2 By hop — where the transmitting cells actually are

| hop | nodes | cells | TRANSMITTING | NULL | INSUFFICIENT |
|---|---|---|---|---|---|
| 0 crude | Brent, WTI, Brent–WTI spread, Pink Sheet crude | 36 | 4 | 32 | 0 |
| 1 products and cracks | heating oil, gasoline (Gulf, NYH), jet, propane, diesel crack, gasoline crack | 63 | 3 | 60 | 0 |
| 2 physical | refinery use, crude/distillate/gasoline stocks, crude imports, 7 chokepoint transits | 108 | 1 | 79 | 28 |
| 3 gas and LNG | Henry Hub, TTF, Pink Sheet gas US/EU, LNG Japan | 45 | **0** | 41 | 4 |
| 4 fertilizer | nitrogen PPI, urea, DAP, TSP, potash, coal | 54 | **0** | 54 | 0 |
| e freight and sector proxies | 5 tanker, 3 refiner, 3 fertilizer, 1 LNG equity | 108 | 7 | 84 | 17 |
| x macro | breakevens, dollar, volatility, credit proxy, palladium, platinum, S&P 500 | 63 | 6 | 51 | 6 |

**The shape of that table is the finding.** The transmitting cells sit at the two ends —
crude itself and the equity/macro nodes beside the chain — and thin out along it. The gas and
fertilizer hops, four and five steps down, produce **zero** transmitting cells out of 99. The
credit node produces zero. If a shock propagated down this chain in a way this design can see,
hops 3 and 4 are where it would show, and they are empty.

### 1.3 By shock class

| shock | TRANSMITTING | NULL | INSUFFICIENT |
|---|---|---|---|
| policy_response | 7 | 46 | 0 |
| tightening (pooled) | 5 | 48 | 0 |
| infrastructure_attack | 3 | 37 | 13 |
| opec_decision | 2 | 41 | 10 |
| all (pooled) | 1 | 52 | 0 |
| chokepoint_disruption | 1 | 44 | 8 |
| conflict_escalation | 1 | 52 | 0 |
| demand_shock | 1 | 30 | 22 |
| sanctions | **0** | 51 | 2 |

Sanctions — 42 de-overlapped events, the second-largest class — move nothing anywhere in the
chain at any registered horizon.

### 1.4 Every transmitting cell, with n and band

Units: % for log nodes, USD/bbl for cracks, log(1+n) for transits. "placebo" is the
coefficient's percentile in the matched pseudo-event distribution; "BH" is survival of the
Benjamini–Hochberg control at q = 0.10 within that node's nine-shock family.

| hop | node | shock | h | β [95%] | n | placebo | BH |
|---|---|---|---|---|---|---|---|
| 0 | Brent | demand_shock | 5 | −6.852 [−13.249, −0.456] | 16 | 0.0 | no |
| 0 | Brent | policy_response | 5 | −3.528 [−6.186, −0.871] | 36 | 0.0 | **yes** |
| 0 | WTI | policy_response | 5 | −3.717 [−6.947, −0.486] | 27 | 0.0 | no |
| 0 | WTI | tightening | 5 | +2.308 [+0.100, +4.515] | 47 | 99.6 | no |
| 1 | diesel crack | tightening | 20 | +2.805 [+0.163, +5.447] | 47 | 100.0 | no |
| 1 | gasoline crack | infrastructure_attack | 20 | +2.509 [+0.163, +4.855] | 20 | 98.8 | no |
| 1 | jet fuel, Gulf | infrastructure_attack | 20 | +4.404 [+0.196, +8.613] | 20 | 99.0 | no |
| 2 | Cape of Good Hope transits | conflict_escalation | 5 | +20.659 [+8.772, +32.547] | 16 | 100.0 | **yes** |
| e | CF Industries | policy_response | 5 | −2.987 [−5.128, −0.846] | 26 | 1.4 | **yes** |
| e | DHT Holdings | opec_decision | 5 | +5.319 [+1.038, +9.601] | 25 | 100.0 | no |
| e | Cheniere | tightening | 5 | +3.152 [+0.216, +6.087] | 45 | 99.4 | no |
| e | Nutrien | tightening | 5 | +2.293 [+0.796, +3.791] | 23 | 100.0 | **yes** |
| e | Phillips 66 | tightening | 5 | +1.708 [+0.141, +3.275] | 32 | 99.4 | no |
| e | Teekay Tankers | chokepoint_disruption | 5 | −3.882 [−7.595, −0.169] | 17 | 0.4 | no |
| e | Teekay Tankers | infrastructure_attack | 5 | +3.169 [+0.545, +5.792] | 15 | 98.8 | no |
| x | palladium | opec_decision | 20 | −4.026 [−7.158, −0.894] | 30 | 0.0 | **yes** |
| x | palladium | policy_response | 20 | −3.415 [−6.467, −0.362] | 26 | 0.2 | **yes** |
| x | palladium | all | 20 | −3.688 [−6.360, −1.015] | 51 | 0.0 | **yes** |
| x | S&P 500 | policy_response | 20 | −2.199 [−3.996, −0.403] | 30 | 0.0 | no |
| x | broad dollar | policy_response | 20 | +0.669 [+0.080, +1.259] | 26 | 99.6 | no |
| x | volatility index | policy_response | 20 | +7.064 [+0.903, +13.226] | 33 | 99.4 | no |

Seven of the 21 survive the false-discovery control. **Teekay Tankers appears twice with
opposite signs** — down 3.9% after a chokepoint disruption, up 3.2% after an infrastructure
attack — which is a useful reminder of what a table of 477 cells looks like when the underlying
truth is mostly nothing.

### 1.5 The chain itself, cell by cell, for the two pooled shocks

Every one of these is NULL unless marked. This is the table the study was built to produce.

| hop | node | shock=all | shock=tightening |
|---|---|---|---|
| crude | Brent (h=5) | +0.150 [−1.695, +1.995] n=82 | +1.990 [−0.403, +4.382] n=53 |
| crude | WTI (h=5) | +0.114 [−1.884, +2.113] n=68 | **+2.308 [+0.100, +4.515] n=47 — TRANSMITTING** |
| products | heating oil NYH (h=20) | +1.958 [−0.998, +4.913] n=70 | +3.210 [−0.696, +7.116] n=48 |
| products | gasoline Gulf (h=20) | −0.259 [−4.586, +4.069] n=70 | +2.834 [−1.404, +7.072] n=48 |
| products | gasoline NYH (h=20) | −0.317 [−3.983, +3.348] n=70 | +1.686 [−2.201, +5.574] n=48 |
| products | jet Gulf (h=20) | +1.631 [−1.977, +5.238] n=70 | +2.784 [−1.077, +6.644] n=48 |
| products | propane (h=20) | +0.539 [−3.141, +4.218] n=67 | +1.928 [−1.432, +5.288] n=46 |
| cracks | diesel crack (h=20) | +1.526 [−0.038, +3.089] n=70 | **+2.805 [+0.163, +5.447] n=47 — TRANSMITTING** |
| cracks | gasoline crack (h=20) | −0.268 [−2.538, +2.002] n=70 | +1.341 [−0.574, +3.256] n=47 |
| gas | Henry Hub (h=20) | +0.295 [−4.470, +5.060] n=66 | −2.852 [−7.904, +2.199] n=45 |
| gas | US gas, monthly (h=3m) | −5.762 [−12.128, +0.604] n=94 | −3.217 [−11.476, +5.042] n=61 |
| gas | Europe gas, monthly (h=3m) | +1.285 [−4.330, +6.900] n=94 | −1.577 [−9.918, +6.764] n=61 |
| LNG | Japan LNG, monthly (h=3m) | +0.657 [−2.586, +3.900] n=94 | +1.252 [−2.479, +4.984] n=61 |
| fertilizer | nitrogen PPI (h=3m) | −1.079 [−3.997, +1.838] n=94 | +1.961 [−1.148, +5.069] n=61 |
| fertilizer | urea (h=3m) | +0.490 [−5.831, +6.811] n=94 | +4.031 [−2.696, +10.758] n=61 |
| fertilizer | DAP (h=3m) | +0.011 [−4.417, +4.439] n=94 | +1.305 [−3.029, +5.639] n=61 |
| fertilizer | TSP (h=3m) | −2.576 [−6.891, +1.739] n=94 | +0.966 [−3.536, +5.469] n=61 |
| fertilizer | potash (h=3m) | +3.332 [−0.438, +7.102] n=94 | +4.770 [−1.769, +11.308] n=61 |
| freight proxy | Frontline (h=5) | −0.915 [−4.571, +2.740] n=54 | +1.064 [−0.759, +2.887] n=44 |
| freight proxy | Scorpio (h=5) | −1.637 [−3.683, +0.409] n=35 | +1.415 [−1.247, +4.077] n=36 |
| freight proxy | DHT (h=5) | +0.817 [−1.150, +2.784] n=47 | +1.409 [−0.361, +3.180] n=41 |
| freight proxy | Teekay (h=5) | +1.365 [−1.000, +3.730] n=43 | +1.256 [−0.846, +3.357] n=39 |
| freight proxy | Intl Seaways (h=5) | −0.394 [−3.039, +2.251] n=19 | +2.287 [−0.026, +4.600] n=25 |
| credit | high-yield ETF proxy (h=20) | −0.296 [−1.535, +0.943] n=45 | +0.254 [−0.408, +0.916] n=40 |
| physical | crude stocks ex-SPR (h=4w) | −0.161 [−0.942, +0.620] n=87 | +0.244 [−0.554, +1.041] n=56 |
| physical | refinery utilization (h=4w) | +0.156 [−0.831, +1.143] n=86 | +0.245 [−0.764, +1.253] n=55 |
| physical | distillate stocks (h=4w) | +0.273 [−1.088, +1.633] n=87 | −0.110 [−1.766, +1.546] n=56 |
| physical | gasoline stocks (h=4w) | +0.207 [−0.681, +1.095] n=87 | +0.528 [−0.641, +1.697] n=56 |
| physical | crude imports (h=4w) | +1.110 [−0.641, +2.861] n=87 | +0.370 [−1.576, +2.317] n=56 |

Note the pattern in the tightening column: almost every product and fertilizer node is
positive and almost none excludes zero. That is what a real but small effect looks like, and it
is also what noise with a shared regressor looks like. This design cannot separate them at
n ≈ 50, and §6 says what would.

### 1.6 The regime split (gas, Ramberg–Parsons break)

Registered in §2.7: pre 2009-02-06 versus post 2009-02-13, estimated only at n ≥ 15.

| node | window | shock | h | β [95%] | n | usable? |
|---|---|---|---|---|---|---|
| Henry Hub | pre-shale | tightening | 20d | −10.731 [−17.041, −4.421] | **8** | **no — below the registered minimum of 15** |
| Henry Hub | pre-shale | all | 20d | −1.535 [−7.965, +4.895] | 26 | yes, NULL |
| Henry Hub | post-shale | tightening | 20d | −1.009 [−6.855, +4.837] | 37 | yes, NULL |
| Henry Hub | post-shale | all | 20d | +1.432 [−5.141, +8.006] | 40 | yes, NULL |
| US gas, monthly | pre-shale | tightening | 3m | −15.214 [−25.565, −4.862] | 19 | yes — band excludes zero, **sign is negative** |
| US gas, monthly | post-shale | tightening | 3m | +4.715 [−6.318, +15.748] | 42 | yes, NULL |

The eye is drawn to the −10.7% pre-shale Henry Hub cell. **It has eight events and the
registration forbids reading it**; it is printed here only so that nobody rediscovers it later
and thinks it was hidden. The monthly US gas cell at n = 19 does clear the minimum and does
exclude zero, but its sign is *negative* — gas **falling** 15% over three months after a
tightening event, the opposite of the expectation in E-4 — and it did not survive as a
TRANSMITTING cell because the regime runs carry no placebo. Treat it as a lead for v3, not a
result.

---

## 2. Pass-through, hop to hop

### 2.1 The ratios are not identified, and here is the proof

The natural summary of a chain is "how much of crude's move arrives at the next hop", i.e.
β(product)/β(crude) at the same shock and horizon. **That ratio cannot be computed here,
because the denominator is null everywhere.** Brent's own response at the headline horizon has
a band covering zero for both pooled shocks, so the ratio is a number divided by something
indistinguishable from zero. The delta-method intervals below say so themselves.

| shock | numerator | β(num) | β(Brent) | ratio | 95% (delta) | denominator excludes zero? |
|---|---|---|---|---|---|---|
| all | heating oil / Brent, h=20 | +1.958 | +0.168 | +11.69 | [−196.7, +220.1] | **no** |
| all | gasoline Gulf / Brent | −0.259 | +0.168 | −1.54 | [−39.2, +36.1] | **no** |
| all | jet Gulf / Brent | +1.631 | +0.168 | +9.74 | [−164.5, +184.0] | **no** |
| all | propane / Brent | +0.539 | +0.168 | +3.22 | [−58.0, +64.4] | **no** |
| all | Henry Hub / Brent | +0.295 | +0.168 | +1.76 | [−40.5, +44.0] | **no** |
| tightening | heating oil / Brent, h=20 | +3.210 | +1.656 | +1.94 | [−3.06, +6.94] | **no** |
| tightening | gasoline Gulf / Brent | +2.834 | +1.656 | +1.71 | [−2.95, +6.37] | **no** |
| tightening | gasoline NYH / Brent | +1.686 | +1.656 | +1.02 | [−2.28, +4.32] | **no** |
| tightening | jet Gulf / Brent | +2.784 | +1.656 | +1.68 | [−2.80, +6.16] | **no** |
| tightening | propane / Brent | +1.928 | +1.656 | +1.16 | [−2.17, +4.50] | **no** |
| tightening | Henry Hub / Brent | −2.852 | +1.656 | −1.72 | [−6.69, +3.24] | **no** |
| all | urea / Pink Sheet crude, h=3m | +0.490 | −3.788 | −0.13 | [−1.81, +1.55] | **no** |
| all | DAP / crude, h=3m | +0.011 | −3.788 | −0.00 | [−1.17, +1.17] | **no** |
| tightening | urea / crude, h=3m | +4.031 | +1.526 | +2.64 | [−9.33, +14.61] | **no** |
| tightening | nitrogen PPI / crude, h=3m | +1.961 | +1.526 | +1.28 | [−4.50, +7.07] | **no** |

Two disclosures about that arithmetic. **First**, the delta method needs the covariance between
numerator and denominator; the two coefficients come from separate regressions and no
covariance is stored, so independence is assumed. Both are driven by the same events and are
positively correlated, which means the true interval is *narrower* than shown — the intervals
above are conservative, and they are still uninformative. **Second**, a ratio whose denominator
straddles zero is the classical Fieller problem: its confidence set is not an interval at all
and the delta method understates the pathology. The right reading of this table is not "the
pass-through ratio is 1.9" but "**the pass-through ratio is not estimable from this sample**".

What *is* interpretable is the level response at each hop, and that is §1.5.

### 2.2 Rockets and feathers: fires in 6 of 15 spot tests, with the signs pointing both ways

The registered test (§2.6) enters positive and negative crude changes together — never
censored, per Kilian and Vigfusson — and asks whether the cumulative response differs.
W = β⁺ − β⁻; a positive W means increases pass through faster.

| leg | node | h | β⁺ | β⁻ | W | p | fires at 5%? |
|---|---|---|---|---|---|---|---|
| daily spot | heating oil NYH | 5 | +0.442 | +0.718 | **−0.277** | 0.041 | yes, **negative** |
| daily spot | heating oil NYH | 10 | +0.457 | +0.673 | −0.216 | 0.283 | no |
| daily spot | heating oil NYH | 20 | +0.534 | +0.664 | −0.130 | 0.570 | no |
| daily spot | gasoline Gulf | 5 | +0.633 | +0.609 | +0.023 | 0.909 | no |
| daily spot | gasoline Gulf | 10 | +0.802 | +0.497 | +0.305 | 0.375 | no |
| daily spot | gasoline Gulf | 20 | +1.258 | +0.173 | **+1.085** | 0.001 | yes, positive |
| daily spot | gasoline NYH | 5 | +0.594 | +0.556 | +0.038 | 0.858 | no |
| daily spot | gasoline NYH | 10 | +0.718 | +0.436 | +0.282 | 0.366 | no |
| daily spot | gasoline NYH | 20 | +1.136 | +0.215 | **+0.921** | 0.005 | yes, positive |
| daily spot | jet Gulf | 5 | +0.493 | +0.769 | **−0.276** | 0.034 | yes, **negative** |
| daily spot | jet Gulf | 10 | +0.536 | +0.776 | −0.240 | 0.322 | no |
| daily spot | jet Gulf | 20 | +0.798 | +0.649 | +0.149 | 0.665 | no |
| daily spot | propane | 5 | +0.621 | +0.369 | +0.252 | 0.060 | no |
| daily spot | propane | 10 | +0.700 | +0.279 | **+0.420** | 0.022 | yes, positive |
| daily spot | propane | 20 | +1.050 | −0.015 | **+1.065** | <0.001 | yes, positive |
| weekly retail | US regular retail | 4w | +0.379 | +0.473 | −0.094 | 0.296 | **no** |
| weekly retail | US regular retail | 8w | +0.441 | +0.554 | −0.113 | 0.405 | **no** |

Six of fifteen spot tests reject at 5% where 0.75 would by chance, so this is not pure noise.
But three features cut against reading it as rockets and feathers:

1. **The signs conflict.** At h=5 heating oil and jet reject with a *negative* W — decreases
   passing through faster, feathers and rockets the wrong way round. At h=20 gasoline and
   propane reject with a positive W. The same commodity flips sign across horizons.
2. **The leg where the literature puts the asymmetry is the one leg that shows none.**
   Borenstein, Cameron and Gilbert located it at the wholesale-to-retail step and found the
   crude-to-wholesale step symmetric ("0.13¢ over the five weeks and statistically
   insignificant"). Our retail leg does not reject at either horizon, and our spot legs do. The
   pattern is the inverse of the mechanism story it would be borrowed from.
3. **The test is slope-based**, and Kilian and Vigfusson's whole point is that slope tests are
   "not informative about the degree of asymmetry of the response functions". The registration
   says this at §2.6 and it is repeated here because it is the difference between a finding and
   an artefact. The impulse-response-based symmetry test is deferred to v3.

Registered expectation E-3 predicted no asymmetry at the spot hop and asymmetry at retail. The
result is **INDETERMINATE**, and closer to inverted than confirmed.

---

## 3. The five retracted amplification edges, and the palladium survivor

`propagation_edges` carried six rows labelled `validated` — "geopolitical shock (VIX-stress
regime)" → node, 20-day lag. Amendment B registered the re-test before it ran: the all-event
shock restricted to days whose volatility percentile at t−1 is at or above its median (the
"stress regime" the edges claim), h = 20, against the matched placebo.

| edge | β at h=20 | n | placebo pct | verdict | ruling |
|---|---|---|---|---|---|
| Brent oil | +0.614% [−4.116, +5.345] | 40 | 55.0 | NULL | **RETRACTED** |
| Heating oil | +2.008% [−2.617, +6.633] | 35 | 87.8 | NULL | **RETRACTED** |
| 5Y breakeven | −0.061pp [−0.237, +0.116] | 20 | 2.2 | NULL | **RETRACTED** |
| S&P 500 | −0.760% [−2.769, +1.249] | 36 | 3.8 | NULL | **RETRACTED** |
| Platinum | −1.286% [−5.042, +2.469] | 25 | 4.2 | NULL | **RETRACTED** |
| Palladium | −5.807% [−10.663, −0.951] | 22 | 0.0 | TRANSMITTING | retained |

Joe ruled on 2026-09-02: retract the five. Another session implemented it in
`src/propagation_graph.py` as a *status*, not an erasure — strength and interval keep their
computed values.

**Palladium, framed as the ruling requires and as it will be framed anywhere it appears.** The
re-test result is published above exactly as computed. In the same breath: palladium is **not
on the oil chain**. It is a macro cross-check node and no mechanism in this study predicts a
crude shock reaching it. And **one survivor out of six re-tested edges is what noise looks like
at this base rate** — at a 5% threshold there is roughly a 26% chance of at least one hit among
six under a complete null. There is a further wrinkle that makes it worse rather than better:
the re-tested coefficient is **−5.807 while the edge it was testing is +5.144**, so the survivor
does not even agree in sign with the claim it was meant to confirm. **This is not a finding and
must not be surfaced as one.** It is published because the re-test was registered before it ran,
and every result of a registered test is published, including the awkward one.

**Why the two gates disagreed at all**, since this will recur otherwise: the engine's own gate
is `ci_excludes_zero and amp > 0 and survives_FDR`, where `amp` is high-volatility events minus
low-volatility events. It never looks at a non-event day, so a world in which nothing transmits
but volatile periods have larger moves passes it. The re-test compares against non-event days
matched on the same volatility *and* geopolitical-risk state. This is the defect
`src/placebo_vixmatched.py` was written to fix and which the repo already conceded as red-team
attack #2 ("it cannot tell them apart").

---

## 4. External checks against published shock series

These were registered as documented sanity checks, never as gates (§2.8). They are the most
informative part of this document, because they separate two very different possible reasons
for §1's silence: a broken estimator, or weak shocks.

### 4.1 Känzig's oil supply news surprise — the estimator works

Our local projection of Brent on Känzig's daily principal-component surprise, over 128 OPEC
announcement days, using the same code that produced every null in §1:

| h (trading days) | β (% Brent per unit surprise) | 95% | excludes zero? |
|---|---|---|---|
| 0 | +0.851 | [+0.650, +1.052] | yes |
| 1 | +1.633 | [+1.013, +2.253] | yes |
| 2 | +1.665 | [+1.044, +2.286] | yes |
| 5 | +1.727 | [+0.919, +2.535] | yes |
| 10 | +1.904 | [+0.621, +3.188] | yes |
| 20 | +2.374 | [+0.997, +3.750] | yes |
| 40 | +2.236 | [+0.732, +3.739] | yes |
| 60 | +1.607 | [+0.387, +2.827] | yes |

**Every horizon excludes zero, with the sign, the shape and the persistence Känzig reports.**
The estimator recovers a published identified shock cleanly. So the nulls in §1 are not the
machinery failing to see an effect that is there.

Beside it, our own OPEC dummy on the same asset at the same horizon: **−3.159 [−7.439, +1.121],
n = 47, band covers zero.** Same node, same horizon, same code; a magnitude-bearing shock finds
the effect and an unsigned dummy does not. That is the single most useful comparison in the
study, and it points at the shock design, not the estimator.

### 4.2 Baumeister–Hamilton structural shocks — agreement on their series, disagreement with our classes

| check | result |
|---|---|
| B–H supply shock → Pink Sheet crude, h=3 months | **−4.718 [−6.373, −3.064]**, n=494, excludes zero at every horizon 0–12 |
| B–H inventory-demand shock → crude, h=3 months | +0.126 [−1.671, +1.923], covers zero at every horizon |
| correlation, our monthly OPEC-event count vs abs(Känzig monthly surprise) | **r = 0.431**, n = 513 months |
| correlation, our monthly tightening count vs B–H supply shock | **r = −0.023**, n = 614 months |

Read together these say something specific. Our OPEC dates line up with Känzig's announcement
surprises (r = 0.43), which they should, being largely the same meetings. But **our tightening
classes have essentially no relationship with the identified structural supply shock** (r =
−0.02 over 614 months). The events the corpus calls chokepoint disruptions, infrastructure
attacks and conflict escalations are not, in aggregate, the months in which the oil market
experienced identified supply shocks. That is consistent with Kilian's own conclusion that
"unanticipated oil supply disruptions have only a small positive effect on the real price of
oil" and that major episodes were driven by demand, and it is a more likely explanation of §1
than any defect in the estimator.

### 4.3 One class fails the anticipation check

The registered exogeneity diagnostic (Ramey's third criterion) measures Brent's own move over
the five days *before* each shock:

| shock | pre-window mean | se | n | flag |
|---|---|---|---|---|
| opec_decision | **+1.663%** | 0.803 | 49 | **ANTICIPATED-IN-PRICE** |
| demand_shock | −4.744% | 2.797 | 16 | flat |
| infrastructure_attack | +0.687% | 0.990 | 22 | flat |
| conflict_escalation | +0.507% | 1.096 | 40 | flat |
| policy_response | +0.478% | 0.965 | 38 | flat |
| chokepoint_disruption | +0.375% | 1.417 | 20 | flat |
| sanctions | +0.341% | 0.893 | 40 | flat |
| all | +0.622% | 0.685 | 91 | flat |
| tightening | +0.295% | 0.818 | 59 | flat |

Brent is already up 1.7% in the week before an OPEC decision. Whatever the OPEC dummy measures,
part of it was in the price beforehand — as Känzig's whole design anticipates, which is why he
uses a surprise rather than a date.

---

## 5. Limits

Stated at full strength, because several of them bound what any of the above can mean.

1. **The shocks carry no magnitude.** A dummy weights a coup and a communiqué identically. §4.1
   shows a magnitude-bearing shock on the same node with the same code finding a clean effect
   where the dummy finds nothing. This is the study's principal weakness and the first thing v3
   should fix.
2. **Baltic tanker indices are a gap, not a series.** BDTI and BCTI are licensed and not free.
   Nothing in this repo is a freight rate. The tanker equities are **labelled equity proxies**
   in their series names, are controlled for the S&P 500, and remain confounded by everything
   else that moves an equity. Never read them as freight.
3. **The equity proxies are proxies.** Same for the refiner, fertilizer and LNG names. Seven of
   the 21 transmitting cells are equity proxies; none of them is evidence about a physical
   ripple.
4. **JODI-Oil has no licence page.** "Freely available" was read as access, not rights, so the
   106 series loaded are refresh-only and never redistributed. A fresh clone cannot rebuild them
   offline. They are also **structurally missing the OPEC core after 2018**: Iran, the UAE and
   Qatar stopped publishing production volumes in 2018, Brazil in 2022, Russia in March 2023,
   Iraq in March 2024, while all six continue publishing the barrels-per-tonne conversion
   factor that a careless loader would mistake for a volume.
5. **UCDP GED is location-based**, coding events to the place a fatality occurred rather than to
   an actor's intent or a market-relevant asset. The engine's `derived.conflict_intensity_pct`
   rests on it. **The ripple study does not use it** — the controls are the volatility index and
   the geopolitical-risk threat index, and no GED series appears in `src/ripple_lp.py`. The
   limit is recorded because it bounds the corpus and the wider engine, not this estimate.
6. **The daily sample starts 1990-01-09**, not 1987, because the volatility control begins in
   1990 and the regression needs five days of it. Events before that date cannot enter a daily
   regression.
7. **The chokepoint transit nodes begin in 2019** and are INSUFFICIENT by construction: 28 of
   the 55 insufficient cells are transit nodes. The one transmitting transit cell (Cape of Good
   Hope, +20.7% after conflict escalations, n=16) sits barely above the minimum and covers the
   Red Sea rerouting period, when almost any conflict date would coincide with traffic moving
   around Africa. It is a description of that episode, not an estimate of a general response.
8. **Multiple testing.** 477 cells. The Benjamini–Hochberg control at q = 0.10 runs within each
   node's nine-shock family, not across the whole table; only seven cells survive even that.
9. **The pass-through ratios are not estimable** (§2.1), so no hop-to-hop transmission
   coefficient is reported.
10. **The monthly nodes see event counts per month**, collapsing 313 events into 294 months of
    which 67 contain any event. A monthly coefficient is "per event in the month", not per
    event.
11. **Regime cells carry no placebo**, so no regime result can reach TRANSMITTING; §1.6 is
    descriptive.
12. **Two coefficients are not a chain.** Even where a product node moves, nothing here
    establishes that it moved *because* crude moved; §2.1's failure means the study cannot
    attribute a product response to its own crude hop.

---

## 6. What would change the answer

Not a plan, a statement of what the nulls are consistent with. The tightening column of §1.5 is
positive at nearly every product and fertilizer node and excludes zero at almost none. At
n ≈ 50 with unsigned dummies, an effect of the size the literature would predict is not
separable from zero by this design. The three things that would separate it, in order of
expected value: a magnitude-bearing shock series for the non-OPEC classes (§4.1 shows what that
buys); more events, which is what the corpus expansion work is for; and the two new data
targets registered as `RIPPLE_REGISTRATION.md` **Amendment C** — JODI country production and
PortWatch chokepoint transits — which move the study from price-only to physical-quantity
outcomes. Amendment C states what each adds and the n each would have. **Nothing in Amendment C
has been computed.**

---

## Appendix A — provenance of every number

Run `2026-09-02T23:32:21Z`, seed 19900802, 9,963 trading days, 500 placebo draws per headline
cell, runtime 42 s. Paths are inside `data/ripple/` unless another file is named. The run is
deterministic: two runs on this seed produced byte-identical `rows` (checked, commit 338fae7).

| Numbers | Path |
|---|---|
| the 21 / 401 / 55 tally, fragile count, cells | `irf.json` `rows[]` where `spec="total"` and `verdict` is set |
| verdict counts by hop and by class (§1.2, §1.3) | same rows, grouped on `hop` and `shock` |
| every transmitting cell, its band, n, placebo percentile, BH flag (§1.4) | `irf.json` rows with `verdict="TRANSMITTING"`; `irf[]` entry at `headline_h`; `placebo.percentile`; `bh_q10_reject` |
| the chain table (§1.5) | `irf.json` rows, `shock` ∈ {all, tightening}, `spec="total"`, entry at `headline_h` |
| de-overlapped shock counts | `irf.json` `meta.shock_counts_daily_deoverlapped` |
| regime cells (§1.6) | `regimes.json` `henry_hub_daily[]`, `gas_monthly[]`, `sample` = `pre_2009-02-06` / `post_2009-02-13` |
| pass-through ratios and delta intervals (§2.1) | computed in this document from `irf.json` betas and `se_ehw`; script in Appendix B |
| asymmetry tests (§2.2) | `passthrough.json` `daily_spot[]`, `weekly_retail[]` |
| the six edges, their re-test and rulings (§3) | `retraction_six.json` `status`; `rows[]` `sample="vix_ge_median"` |
| palladium's +5.144 edge value and the 26% figure | `src/propagation_graph.py` `PALLADIUM_NOTE`; the edge value from `data/cross_asset_conditioned.json` |
| Känzig IRF, 128 announcement days (§4.1) | `external_checks.json` `kanzig_daily_pc_on_brent.irf[]` |
| our OPEC dummy at h=5 | `irf.json` node `brent`, shock `opec_decision`, `irf[h=5]` |
| B–H supply and inventory IRFs, both correlations (§4.2) | `external_checks.json` `bh_supply_shock_on_pinksheet_crude`, `bh_inventory_demand_shock_on_pinksheet_crude`, `corr_opec_count_vs_abs_kanzig_monthly`, `corr_tightening_count_vs_bh_supply_shock` |
| exogeneity / anticipation table (§4.3) | `exogeneity.json` |
| JODI coverage and the OPEC-core dropout (§5.4) | `RIPPLE_SOURCES.md` §5 load receipt |
| the seal timestamps | `git log -- RIPPLE_REGISTRATION.md` (cbf4fdc 15:42:38) and `git log --diff-filter=A -- src/ripple_lp.py` (4c989b0 15:59:32) |
| the base-rate range 1–24 | `data/ripple/SUMMARY.md` tally note; 0.25% and 5% of 477 |

## Appendix B — the only arithmetic performed in this document

The §2.1 ratios. For R = a/b with independent a and b,
Var(R) ≈ Var(a)/b² + a²·Var(b)/b⁴, and the interval is R ± 1.959964·√Var(R).

```python
a = irf[num][h]; b = irf[den][h]                 # both from data/ripple/irf.json
R  = a["beta"] / b["beta"]
var = a["se_ehw"]**2 / b["beta"]**2 + a["beta"]**2 * b["se_ehw"]**2 / b["beta"]**4
lo, hi = R - 1.959964*var**0.5, R + 1.959964*var**0.5
den_significant = (b["ehw_covers_zero"] is False)  # False for every pair in the table
```

No estimate, band, verdict or placebo percentile in this document was recomputed. The files
were read as committed.

---

## Erratum — 2026-09-03, from the Amendment C run (`docs/RIPPLE_PHYSICAL.md`)

*Appended, never edited in place. Every table above stands as computed on 2026-09-02; the two
corrections below are additions to how those tables must be read, both found by running Amendment C's
physical-quantity study with the same estimator on a larger sample.*

**E-1. §1.4's Cape of Good Hope cell does not survive the full physical record.** The table reports
`Cape of Good Hope transits × conflict_escalation, h=5, +20.659 [+8.772, +32.547], n=16`, BH
survivor — the only TRANSMITTING cell at hop 2 and one of seven BH survivors in the study. It was
estimated on the Brent **trading-day** index, which discards weekends; tanker transits happen at
weekends. Re-estimated on the registered Amendment C sample (all 2,799 calendar days, 2019-01-01 →
2026-08-30, de-overlapped within the window) the same cell is **+4.03 [−6.89, +14.96]** — covering
zero. It covers zero on the calendar index at **every one of nine horizons**, including h = 7, the
calendar-day equivalent of trading-day h = 5 (which spans 7.2 calendar days on average). On the
trading-day index it excludes zero at exactly one horizon of six, the registered headline.
**Its verdict on the full record is NULL.** Two further transit cells flip the same way
(`bab_el_mandeb × tightening`, `suez × chokepoint_disruption`). §5.7 above already hedged this cell
as "a description of that episode"; the hedge was right and insufficient.

Consequence for §1.2 and §1.4: hop 2 has **zero** transmitting cells, not one, and the study has
**six** BH survivors at hop 2 and below, not seven. The one-sentence result — that the chain is
silent except at its two ends — is strengthened, not weakened, by this correction.

**E-2. No monthly cell in this study could have transmitted.** Every monthly node was run with
`do_placebo=False`, and Amendment B's TRANSMITTING verdict *requires* the placebo. So the monthly
nodes were NULL-or-INSUFFICIENT **by construction**, and §1.2's "hop 4 fertilizer: 0 transmitting of
54" is arithmetic about a flag, not a finding about fertilizer. Hop 3 is affected for 3 of its 5
nodes (the monthly gas and LNG nodes; Henry Hub and TTF are daily and were scored properly).
`src/ripple_physical.py` implements the registered placebo construction on the monthly grid; it is
weak there (108 pool months, 58 state buckets, heavy fallback to VIX-only matching) and that
weakness is reported. **§1.2's hop-3 and hop-4 rows should be read as "not scored", not as "scored
and empty".**

Neither erratum changes a coefficient, a band, an n, or a placebo percentile in any table above.
