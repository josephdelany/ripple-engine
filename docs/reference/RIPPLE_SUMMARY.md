> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** A summary of withdrawn ripple results. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../../SUBMISSION_STATUS.md).

# RIPPLE SUMMARY — computed once, as registered

*2026-09-02T23:32:21+00:00. Registration RIPPLE_REGISTRATION.md (sealed cbf4fdc; Amendments A, B). Numbers below are read from data/ripple/*.json written by src/ripple_lp.py in this run. Vocabulary: node×shock verdicts are TRANSMITTING / NULL / INSUFFICIENT; the nine expectations are CONSISTENT / INCONSISTENT / INDETERMINATE. Nothing was re-run or re-labelled after reading.*

## Tally (primary spec, headline horizon, verdict-bearing shocks)
| verdict | count |
|---|---|
| TRANSMITTING | 21 |
| NULL | 401 |
| INSUFFICIENT | 55 |
| of the NULL, FRAGILE (EHW and Newey–West disagree) | 0 |
| node×shock cells | 477 |

Base rate: 21/477 = 4.4% of cells transmit. Under the null every cell has a 5% chance of an EHW band excluding zero, a further 5% chance of a placebo percentile outside the central 95%, and the two are not independent (both are driven by the same β); the expected count under no transmission anywhere is therefore between 1 and 24 cells. Read the tally against that range, not against zero.

### Transmitting cells
- hop 0 **brent** ← demand_shock at h=5: -6.852% [95% -13.249, -0.456] n=16; placebo percentile 0.0 (pseudo 95% band [-2.0338, 3.4418]); BH q=.10 not rejected
- hop 0 **brent** ← policy_response at h=5: -3.528% [95% -6.186, -0.871] n=36; placebo percentile 0.0 (pseudo 95% band [-1.4269, 1.9925]); BH q=.10 reject
- hop 0 **wti** ← policy_response at h=5: -3.717% [95% -6.947, -0.486] n=27; placebo percentile 0.0 (pseudo 95% band [-1.8484, 2.0623]); BH q=.10 not rejected
- hop 0 **wti** ← tightening at h=5: +2.308% [95% +0.100, +4.515] n=47; placebo percentile 99.6 (pseudo 95% band [-1.1305, 1.5466]); BH q=.10 not rejected
- hop 1 **diesel_crack** ← tightening at h=20: +2.805 [95% +0.163, +5.447] n=47; placebo percentile 100.0 (pseudo 95% band [-1.0287, 1.1516]); BH q=.10 not rejected
- hop 1 **gasoline_crack** ← infrastructure_attack at h=20: +2.509 [95% +0.163, +4.855] n=20; placebo percentile 98.8 (pseudo 95% band [-1.1055, 1.9991]); BH q=.10 not rejected
- hop 1 **jet_gulf** ← infrastructure_attack at h=20: +4.404% [95% +0.196, +8.613] n=20; placebo percentile 99.0 (pseudo 95% band [-3.845, 4.0065]); BH q=.10 not rejected
- hop 2 **transit_cape_of_good_hope** ← conflict_escalation at h=5: +20.659% [95% +8.772, +32.547] n=16; placebo percentile 100.0 (pseudo 95% band [-16.7505, 12.5325]); BH q=.10 reject
- hop e **eq_cf** ← policy_response at h=5: -2.987% [95% -5.128, -0.846] n=26; placebo percentile 1.4 (pseudo 95% band [-2.7255, 1.7222]); BH q=.10 reject
- hop e **eq_dht** ← opec_decision at h=5: +5.319% [95% +1.038, +9.601] n=25; placebo percentile 100.0 (pseudo 95% band [-3.5794, 0.7777]); BH q=.10 not rejected
- hop e **eq_lng** ← tightening at h=5: +3.152% [95% +0.216, +6.087] n=45; placebo percentile 99.4 (pseudo 95% band [-5.6805, 1.7666]); BH q=.10 not rejected
- hop e **eq_ntr** ← tightening at h=5: +2.293% [95% +0.796, +3.791] n=23; placebo percentile 100.0 (pseudo 95% band [-2.7633, 0.7071]); BH q=.10 reject
- hop e **eq_psx** ← tightening at h=5: +1.708% [95% +0.141, +3.275] n=32; placebo percentile 99.4 (pseudo 95% band [-1.1086, 1.5034]); BH q=.10 not rejected
- hop e **eq_tnk** ← chokepoint_disruption at h=5: -3.882% [95% -7.595, -0.169] n=17; placebo percentile 0.4 (pseudo 95% band [-2.6566, 2.5756]); BH q=.10 not rejected
- hop e **eq_tnk** ← infrastructure_attack at h=5: +3.169% [95% +0.545, +5.792] n=15; placebo percentile 98.8 (pseudo 95% band [-2.9153, 2.8766]); BH q=.10 not rejected
- hop x **palladium** ← opec_decision at h=20: -4.026% [95% -7.158, -0.894] n=30; placebo percentile 0.0 (pseudo 95% band [-0.9231, 5.699]); BH q=.10 reject
- hop x **palladium** ← policy_response at h=20: -3.415% [95% -6.467, -0.362] n=26; placebo percentile 0.2 (pseudo 95% band [-1.7721, 4.7589]); BH q=.10 reject
- hop x **palladium** ← all at h=20: -3.688% [95% -6.360, -1.015] n=51; placebo percentile 0.0 (pseudo 95% band [-0.6572, 3.914]); BH q=.10 reject
- hop x **sp500** ← policy_response at h=20: -2.199% [95% -3.996, -0.403] n=30; placebo percentile 0.0 (pseudo 95% band [-1.2491, 1.7166]); BH q=.10 not rejected
- hop x **usd_broad** ← policy_response at h=20: +0.669% [95% +0.080, +1.259] n=26; placebo percentile 99.6 (pseudo 95% band [-0.7127, 0.3666]); BH q=.10 not rejected
- hop x **vix** ← policy_response at h=20: +7.064% [95% +0.903, +13.226] n=33; placebo percentile 99.4 (pseudo 95% band [-9.4129, 4.5517]); BH q=.10 not rejected

## Retraction check of the six `validated` propagation edges (Amendment B)
| edge (node) | β at h=20, all-shock, VIX≥median | n | placebo pct | verdict | status |
|---|---|---|---|---|---|
| Brent oil (brent) | +0.614% [95% -4.116, +5.345] n=40 | 40 | 55.0 | NULL | **RETRACTED** |
| Heating oil (heating_oil_nyh) | +2.008% [95% -2.617, +6.633] n=35 | 35 | 87.8 | NULL | **RETRACTED** |
| 5Y breakeven (t5yie) | -0.061 [95% -0.237, +0.116] n=20 | 20 | 2.2 | NULL | **RETRACTED** |
| Palladium (palladium) | -5.807% [95% -10.663, -0.951] n=22 | 22 | 0.0 | TRANSMITTING | **RETAINED** |
| S&P 500 (sp500) | -0.760% [95% -2.769, +1.249] n=36 | 36 | 3.8 | NULL | **RETRACTED** |
| Platinum (platinum) | -1.286% [95% -5.042, +2.469] n=25 | 25 | 4.2 | NULL | **RETRACTED** |

**Palladium, stated as Joe's Ruling 1 requires.** The re-test result is published above as computed: -5.807% [95% -10.663, -0.951] n=22, placebo percentile 0.0, verdict TRANSMITTING. In the same breath: palladium is **not on the oil chain** — it is a macro cross-check node, and no mechanism in this study predicts a crude shock reaching it. And one survivor out of six re-tested edges is exactly what this base rate produces by chance: at a 5% band and a 5% placebo tail, one hit in six is consistent with noise. **This is not a finding and must not be surfaced as one.** It is published because the re-test was registered before it ran and every result of a registered test is published, including the awkward one.

## The nine expectations (§6)
**E-1 (crude, h=5).**
- Brent ← chokepoint_disruption: +0.319% [95% -2.497, +3.134] n=19 → INDETERMINATE
- Brent ← infrastructure_attack: +1.003% [95% -1.535, +3.540] n=22 → INDETERMINATE
- Brent ← conflict_escalation: +2.045% [95% -1.275, +5.365] n=35 → INDETERMINATE
- Brent ← demand_shock: -6.852% [95% -13.249, -0.456] n=16 → CONSISTENT
**E-2 (pass-through completeness, h=20, shock = all).**
- heating_oil_nyh: +1.958% [95% -0.998, +4.913] n=70 vs Brent +0.168% [95% -2.808, +3.143] n=82 → INDETERMINATE (crude band covers zero)
- gasoline_gulf: -0.259% [95% -4.586, +4.069] n=70 vs Brent +0.168% [95% -2.808, +3.143] n=82 → INDETERMINATE (crude band covers zero)
- diesel_crack (USD/bbl): +1.526 [95% -0.038, +3.089] n=70 → CONSISTENT (transitory: band covers zero)
- gasoline_crack (USD/bbl): -0.268 [95% -2.538, +2.002] n=70 → CONSISTENT (transitory: band covers zero)
**E-3 (asymmetry at the crude→product hop, §2.6).**
- daily spot legs: 6 of 15 (node, h) tests reject symmetry at 5% → INDETERMINATE (some rejections)
  - heating_oil_nyh h=5: β⁺ +0.442 β⁻ +0.718 W -0.277 (p=0.0406)
  - heating_oil_nyh h=10: β⁺ +0.457 β⁻ +0.673 W -0.216 (p=0.283)
  - heating_oil_nyh h=20: β⁺ +0.534 β⁻ +0.664 W -0.130 (p=0.5702)
  - gasoline_gulf h=5: β⁺ +0.633 β⁻ +0.609 W +0.023 (p=0.9089)
  - gasoline_gulf h=10: β⁺ +0.802 β⁻ +0.497 W +0.305 (p=0.3752)
  - gasoline_gulf h=20: β⁺ +1.258 β⁻ +0.173 W +1.085 (p=0.0011)
  - gasoline_nyh h=5: β⁺ +0.594 β⁻ +0.556 W +0.038 (p=0.8575)
  - gasoline_nyh h=10: β⁺ +0.718 β⁻ +0.436 W +0.282 (p=0.3662)
  - gasoline_nyh h=20: β⁺ +1.136 β⁻ +0.215 W +0.921 (p=0.0047)
  - jet_gulf h=5: β⁺ +0.493 β⁻ +0.769 W -0.276 (p=0.0342)
  - jet_gulf h=10: β⁺ +0.536 β⁻ +0.776 W -0.240 (p=0.322)
  - jet_gulf h=20: β⁺ +0.798 β⁻ +0.649 W +0.149 (p=0.6654)
  - propane h=5: β⁺ +0.621 β⁻ +0.369 W +0.252 (p=0.0603)
  - propane h=10: β⁺ +0.700 β⁻ +0.279 W +0.420 (p=0.022)
  - propane h=20: β⁺ +1.050 β⁻ -0.015 W +1.065 (p=0.0)
- retail weekly h=4w: β⁺ +0.379 β⁻ +0.473 W -0.094 (p=0.2958) → INDETERMINATE
- retail weekly h=8w: β⁺ +0.441 β⁻ +0.554 W -0.113 (p=0.4054) → INDETERMINATE
**E-4 (gas regime, Henry Hub ← tightening/all, h=20; pre ≤ 2009-02-06 vs post ≥ 2009-02-13).**
- tightening: pre -10.731% [95% -17.041, -4.421] n=8 | post -1.009% [95% -6.855, +4.837] n=37 → INSUFFICIENT (a regime has n<15; registered 2.7 minimum)
- all: pre -1.535% [95% -7.965, +4.895] n=26 | post +1.432% [95% -5.141, +8.006] n=40 → INDETERMINATE
**E-5 (fertilizer lag, monthly ← tightening count).**
- m_urea: peak |β| at h=2 (+4.921% [95% -0.626, +10.469] n=61); h=0 +0.773% [95% -1.787, +3.332] n=61 → INDETERMINATE
- m_dap: peak |β| at h=12 (-5.701% [95% -15.066, +3.664] n=59); h=0 +0.996% [95% -0.555, +2.546] n=61 → INDETERMINATE
**E-6 (physical, weekly h=4 ← tightening).**
- crude stocks ex-SPR: +0.244% [95% -0.554, +1.041] n=56 → CONSISTENT (no significant fall)
- refinery utilization (pp): +0.245pp [95% -0.764, +1.253] n=55 → CONSISTENT (band covers zero)
**E-7 (OPEC, external).**
- Brent ← Känzig daily PC, h=5: +1.727% [95% +0.919, +2.535] n=118 → CONSISTENT
- Brent ← opec_decision dummy, h=5: -3.159% [95% -7.439, +1.121] n=47 → CONSISTENT (indeterminate as expected)
**E-8 (placebo).**
- Brent h=5 classes beyond the VIX+GPR state: none → INCONSISTENT
**E-9 (equity proxies, h=5, S&P-controlled).**
- eq_fro ← chokepoint_disruption: -1.528% [95% -4.755, +1.698] n=18 → INDETERMINATE
- eq_dht ← chokepoint_disruption: -1.537% [95% -4.475, +1.401] n=17 → INDETERMINATE
- eq_tnk ← chokepoint_disruption: -3.882% [95% -7.595, -0.169] n=17 → INCONSISTENT
- eq_insw ← chokepoint_disruption: -0.999% [95% -4.238, +2.240] n=15 → INDETERMINATE
- eq_stng ← chokepoint_disruption: -2.463% [95% -6.410, +1.484] n=17 → INDETERMINATE

## Exogeneity diagnostic (Brent pre-window t−6…t−1, by shock set)
- chokepoint_disruption: +0.375% (se 1.417) n=20 
- infrastructure_attack: +0.687% (se 0.99) n=22 
- conflict_escalation: +0.507% (se 1.096) n=40 
- opec_decision: +1.663% (se 0.803) n=49 ANTICIPATED-IN-PRICE
- sanctions: +0.341% (se 0.893) n=40 
- demand_shock: -4.744% (se 2.797) n=16 
- policy_response: +0.478% (se 0.965) n=38 
- all: +0.622% (se 0.685) n=91 
- tightening: +0.295% (se 0.818) n=59 

## External checks (§2.8)
- corr(opec_decision monthly count, |Känzig monthly surprise|) = 0.431 over 513 months
- corr(tightening monthly count, B-H supply shock) = -0.023 over 614 months (B-H supply shock: negative = production down)
- Pink Sheet crude ← bh_supply_shock, h=3 months: -4.718% [95% -6.373, -3.064] n=494
- Pink Sheet crude ← bh_inventory_demand_shock, h=3 months: +0.126% [95% -1.671, +1.923] n=494

## Limits that apply to every number above
Dummies carry no magnitude; the daily sample starts 1990-01-09 (VIX control); PortWatch nodes are 2019→ and INSUFFICIENT by construction; equity proxies are S&P-controlled but otherwise confounded; monthly nodes see counts per month. See RIPPLE_REGISTRATION.md §7.

## Who moved first (C-6, descriptive, no test)

*125 Big Move episodes (brent, wti, diesel_crack daily tiers). Rule: first day the node's cumulative move since the close before onset exceeds 2.0× its own trailing-60-day one-day sigma. A low bar at long horizons by construction; the ORDER is the information, not the crossing.*

Brent vs the first product to cross: crude first in 13, product first in 90, same day in 18, of n=121 episodes where both crossed.

| node | hop | episodes crossed | median rank | median day | first-mover count |
|---|---|---|---|---|---|
| diesel_crack | products/cracks | 115 | 8.0 | 3 | 18 |
| eq_vlo | equity proxy | 117 | 10.0 | 5 | 4 |
| gasoline_gulf | products/cracks | 121 | 10.0 | 4 | 2 |
| brent | crude | 121 | 10.0 | 5 | 14 |
| heating_oil_nyh | products/cracks | 119 | 10.0 | 4 | 0 |
| gasoline_nyh | products/cracks | 121 | 11.0 | 4 | 2 |
| jet_gulf | products/cracks | 115 | 11.0 | 4 | 3 |
| gasoline_crack | products/cracks | 111 | 12.0 | 4 | 11 |
| wti | crude | 119 | 12.0 | 3 | 1 |
| sp500 | macro | 112 | 12.0 | 3 | 0 |
| platinum | macro | 84 | 12.0 | 4 | 1 |
| palladium | macro | 89 | 12.0 | 4 | 2 |
| propane | products/cracks | 106 | 12.5 | 4 | 4 |
| eq_mos | equity proxy | 116 | 13.0 | 5 | 7 |
| henry_hub | gas | 100 | 13.0 | 4 | 3 |
| eq_fro | equity proxy | 88 | 13.0 | 4 | 6 |
| eq_stng | equity proxy | 61 | 13.0 | 4 | 3 |
| eq_dht | equity proxy | 76 | 13.5 | 4 | 4 |
| brent_wti_spread | crude | 112 | 14.0 | 7 | 17 |
| eq_lng | equity proxy | 106 | 14.0 | 5 | 7 |
| t5yie | macro | 81 | 14.0 | 4 | 0 |
| hyg_proxy | macro | 74 | 14.0 | 4 | 0 |
| eq_tnk | equity proxy | 74 | 14.5 | 4 | 1 |
| eq_cf | equity proxy | 74 | 15.0 | 5 | 2 |
| usd_broad | macro | 76 | 15.0 | 4 | 0 |
| eq_mpc | equity proxy | 58 | 15.0 | 4 | 2 |
| transit_bab_el_mandeb | transits | 16 | 15.0 | 2 | 1 |
| vix | macro | 110 | 15.5 | 4 | 1 |
| ttf | gas | 36 | 16.5 | 4 | 1 |
| eq_psx | equity proxy | 55 | 17.0 | 5 | 2 |
| eq_ntr | equity proxy | 38 | 17.0 | 4 | 0 |
| eq_insw | equity proxy | 39 | 18.0 | 5 | 0 |
| transit_hormuz | transits | 30 | 25.0 | 8 | 1 |
| transit_bosporus | transits | 26 | 28.5 | 14 | 0 |
| transit_cape_of_good_hope | transits | 20 | 29.0 | 12 | 1 |
| transit_suez | transits | 22 | 30.0 | 20 | 0 |
| transit_panama | transits | 19 | 30.0 | 15 | 0 |
| transit_malacca | transits | 16 | 32.0 | 24 | 0 |

Per-episode order tables: data/ripple/big_move_order.json (one row per node with day, cumulative move, sigma).
Nodes that never crossed inside an episode are listed there under never_crossed; equity proxies are labelled.
