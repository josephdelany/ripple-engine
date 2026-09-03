# The physical half of the ripple study — Amendment C, as computed

*Run 2026-09-03T03:25:09+00:00, seed 19900802, runtime 130.6s. Registered in RIPPLE_REGISTRATION.md Amendment C before anything here was computed; every sample size the amendment fixed in advance reproduces exactly (below). Estimator imported from `src/ripple_lp.py`, not re-implemented.*

## 0. Coverage first — the physical record goes dark for the producers that matter

JODI: 106 series, window 2002-01-01 → 2026-06-01, 294 months. 21 production series carry ≥200 months (Amendment C.2 said 21).

| reporter | production ends | exports ends | stocks ends | intake ends | demand ends |
|---|---|---|---|---|---|
| United Arab Emirates | 2018-12-01 | 2018-12-01 | 2018-12-01 | 2018-12-01 | 2018-12-01 |
| Brazil | 2022-12-01 | 2022-12-01 | 2022-12-01 | 2022-12-01 | 2022-02-01 |
| India | 2026-03-01 | 2019-03-01 | 2026-03-01 | 2026-03-01 | 2026-03-01 |
| Iraq | 2024-03-01 | 2024-03-01 | 2024-03-01 | 2024-03-01 | 2024-03-01 |
| Iran | 2018-07-01 | 2018-07-01 | 2018-07-01 | 2018-07-01 | 2018-07-01 |
| Kazakhstan | 2026-05-01 | 2026-05-01 | 2014-03-01 | — | — |
| Mexico | 2026-05-01 | 2026-05-01 | 2026-05-01 | 2026-05-01 | 2026-05-01 |
| Qatar | 2018-12-01 | 2018-12-01 | 2018-12-01 | 2018-12-01 | 2018-12-01 |
| Russia | 2023-03-01 | 2021-12-01 | 2009-12-01 | 2023-03-01 | — |

**Months of crude production reported, by year.** A zero is a country that stopped reporting, not a country that stopped producing.

| reporter | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| United Arab Emirates | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Brazil | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 0 | 0 | 0 | 0 |
| Canada | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 6 |
| China | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 6 |
| Germany | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 6 |
| Algeria | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 11 | 12 | 12 | 11 | 12 | 12 | 12 | 9 | 12 | 12 | 12 | 12 | 11 | 12 | 6 |
| United Kingdom | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 6 |
| India | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 3 |
| Iraq | 0 | 0 | 0 | 0 | 0 | 12 | 12 | 12 | 12 | 12 | 12 | 11 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 3 | 0 | 0 |
| Iran | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 10 | 11 | 12 | 12 | 12 | 12 | 9 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Japan | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 6 |
| Korea | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 6 |
| Kuwait | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 11 | 11 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 6 |
| Kazakhstan | 12 | 12 | 12 | 9 | 12 | 12 | 12 | 12 | 0 | 0 | 0 | 11 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 5 |
| Mexico | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 5 |
| Nigeria | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 6 |
| Norway | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 6 |
| Qatar | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Russia | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 3 | 0 | 0 | 0 |
| Saudi Arabia | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 6 |
| United States | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 6 |
| Venezuela | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 6 |

### 0.1 The selection problem, in one table

For each producer: how many de-overlapped corpus events name it as actor or target, and how many of those fall while it was still reporting production. The gap is the part of the physical record that the geopolitics itself removed.

| producer | last production report | named events (de-overlapped) | within reporting span | lost |
|---|---|---|---|---|
| United States | 2026-06-01 | 23 | 22 | **1** |
| Iran | 2018-07-01 | 21 | 8 | **13** |
| Russia | 2023-03-01 | 20 | 14 | **6** |
| China | 2026-06-01 | 15 | 15 | **0** |
| Saudi Arabia | 2026-06-01 | 10 | 10 | **0** |
| Iraq | 2024-03-01 | 7 | 7 | **0** |
| Nigeria | 2026-06-01 | 7 | 7 | **0** |
| Venezuela | 2026-06-01 | 7 | 7 | **0** |
| India | 2026-03-01 | 4 | 4 | **0** |
| Kazakhstan | 2026-05-01 | 4 | 4 | **0** |
| United Arab Emirates | 2018-12-01 | 1 | 0 | **1** |
| Canada | 2026-06-01 | 1 | 1 | **0** |
| Japan | 2026-06-01 | 1 | 1 | **0** |
| Qatar | 2018-12-01 | 1 | 1 | **0** |

Across all reporters: **122** named de-overlapped events, **101** of them inside the producer's reporting span — **21 lost**.

PortWatch: 7 chokepoints × 3 fields, 2799 calendar days (2019-01-01 → 2026-08-30), no missing days. Amendment C.3 fixed the window at 2,799 days.

## 1. Did the registered sample sizes reproduce?

| set | JODI registered | JODI computed | PortWatch registered | PortWatch computed |
|---|---|---|---|---|
| chokepoint_disruption | 21 | 21 | 14 | 14 |
| infrastructure_attack | 21 | 21 | 14 | 14 |
| conflict_escalation | 34 | 34 | 17 | 17 |
| opec_decision | 38 | 38 | 15 | 15 |
| sanctions | 36 | 36 | 19 | 19 |
| demand_shock | 13 | 13 | 9 | 9 |
| policy_response | 36 | 36 | 22 | 22 |
| all | 67 | 67 | 16 | 16 |
| tightening | 51 | 51 | 24 | 24 |

Every one matches, including the counterintuitive PortWatch fact that the pooled `all` set (16) is *smaller* than `tightening` (24). The seal holds.

## 2. JODI — the registered primary test barely exists

The primary is the producer the event itself names. Of 22 JODI reporters, these clear the registered minimum of 15 de-overlapped named events:

| producer | named (all) | tightening | clears n≥15? |
|---|---|---|---|
| United States | 23 | 4 | **yes** |
| Iran | 21 | 8 | **yes** |
| Russia | 20 | 11 | **yes** |
| China | 15 | 1 | **yes** |
| Saudi Arabia | 10 | 8 | no |
| Iraq | 7 | 6 | no |
| Nigeria | 7 | 5 | no |
| Venezuela | 7 | 0 | no |
| India | 4 | 0 | no |
| Kazakhstan | 4 | 1 | no |
| United Arab Emirates | 1 | 1 | no |
| Canada | 1 | 0 | no |

Estimable named-producer cells: **4**.

- `cn.crude_production` × all (n=15): +0.087% [-1.018, +1.192] — **NULL**
- `cn.refinery_intake` × all (n=15): -0.822% [-4.371, +2.728] — **NULL**
- `cn.crude_exports` × all (n=4): +3.675% [-90.173, +97.524] — **INSUFFICIENT**
- `cn.products_demand` × all (n=15): +0.404% [-3.477, +4.284] — **NULL**
- `ir.crude_production` × all (n=4): +3.504% [+0.236, +6.772] — **INSUFFICIENT**
- `ir.refinery_intake` × all (n=4): -0.552% [-6.306, +5.202] — **INSUFFICIENT**
- `ir.crude_stocks` × all (n=0): n/a — **INSUFFICIENT**
- `ir.crude_exports` × all (n=4): +8.936% [-2.530, +20.402] — **INSUFFICIENT**
- `ir.products_demand` × all (n=4): -0.808% [-3.847, +2.231] — **INSUFFICIENT**
- `ru.crude_production` × all (n=12): -1.799% [-4.770, +1.172] — **INSUFFICIENT**
- `ru.refinery_intake` × all (n=12): -1.467% [-4.840, +1.907] — **INSUFFICIENT**
- `ru.crude_stocks` × all (n=1): +7.095% [-6.405, +20.596] — **INSUFFICIENT**
- `ru.crude_exports` × all (n=6): +3.977% [-7.813, +15.767] — **INSUFFICIENT**
- `us.crude_production` × all (n=22): -0.076% [-3.115, +2.963] — **NULL**
- `us.refinery_intake` × all (n=22): -1.135% [-3.655, +1.384] — **NULL**
- `us.crude_stocks` × all (n=22): -0.795% [-2.743, +1.153] — **NULL**
- `us.crude_exports` × all (n=22): -4.661% [-16.467, +7.145] — **NULL**
- `us.products_demand` × all (n=22): -1.565% [-3.908, +0.777] — **NULL**

### 2.1 The pooled panel, balanced reporters only

10 reporters have a complete 294-month production record: Canada, China, Germany, United Kingdom, Japan, Nigeria, Norway, Saudi Arabia, United States, Venezuela.

Standard errors clustered by month (the shock has no cross-sectional variation, so this is the binding one). Headline h = 3 months.

| flow | shock | n countries | n events | β(h=3) [95%] | verdict |
|---|---|---|---|---|---|
| crude_production | chokepoint_disruption | 10 | 20 | -0.383% [-2.350, +1.584] | NULL |
| crude_production | infrastructure_attack | 10 | 21 | -0.291% [-1.955, +1.372] | NULL |
| crude_production | conflict_escalation | 10 | 34 | -0.229% [-1.520, +1.061] | NULL |
| crude_production | opec_decision | 10 | 38 | +0.147% [-1.068, +1.362] | NULL |
| crude_production | sanctions | 10 | 35 | +0.180% [-1.284, +1.644] | NULL |
| crude_production | demand_shock | 10 | 13 | -3.789% [-6.856, -0.722] | INSUFFICIENT |
| crude_production | policy_response | 10 | 35 | +0.631% [-0.588, +1.849] | NULL |
| crude_production | all | 10 | 65 | +0.562% [-0.399, +1.523] | NULL |
| crude_production | tightening | 10 | 51 | +0.085% [-0.943, +1.113] | NULL |

### 2.2 The balanced aggregate

| node | shock | n | β(h=3) [95%] | placebo pct | verdict |
|---|---|---|---|---|---|
| agg_crude_production | chokepoint_disruption | 20 | -0.082% [-2.463, +2.299] | 23.2 | NULL |
| agg_crude_production | infrastructure_attack | 21 | -0.371% [-1.465, +0.722] | 22.2 | NULL |
| agg_crude_production | conflict_escalation | 34 | +0.273% [-0.666, +1.211] | 67.2 | NULL |
| agg_crude_production | opec_decision | 38 | +0.114% [-0.968, +1.196] | 76.2 | NULL |
| agg_crude_production | sanctions | 35 | +0.171% [-1.143, +1.484] | 79.6 | NULL |
| agg_crude_production | demand_shock | 13 | -3.123% [-6.431, +0.185] | — | INSUFFICIENT |
| agg_crude_production | policy_response | 35 | +0.632% [-0.325, +1.590] | 94.6 | NULL |
| agg_crude_production | all | 65 | +0.428% [-0.401, +1.258] | 84.6 | NULL |
| agg_crude_production | tightening | 51 | +0.012% [-0.886, +0.911] | 34.2 | NULL |
| agg_refinery_intake | chokepoint_disruption | 20 | +0.188% [-1.490, +1.866] | 26.0 | NULL |
| agg_refinery_intake | infrastructure_attack | 21 | +0.010% [-1.150, +1.170] | 34.4 | NULL |
| agg_refinery_intake | conflict_escalation | 34 | -0.964% [-2.521, +0.592] | 0.2 | NULL |
| agg_refinery_intake | opec_decision | 38 | -0.773% [-1.970, +0.424] | 3.8 | NULL |
| agg_refinery_intake | sanctions | 35 | -0.696% [-1.736, +0.345] | 4.6 | NULL |
| agg_refinery_intake | demand_shock | 13 | -1.536% [-3.914, +0.842] | — | INSUFFICIENT |
| agg_refinery_intake | policy_response | 35 | -0.283% [-1.387, +0.821] | 16.0 | NULL |
| agg_refinery_intake | all | 65 | -0.479% [-1.412, +0.455] | 4.6 | NULL |
| agg_refinery_intake | tightening | 51 | -0.511% [-1.608, +0.586] | 0.4 | NULL |
| agg_crude_exports | chokepoint_disruption | 20 | -0.019% [-3.201, +3.162] | 32.0 | NULL |
| agg_crude_exports | infrastructure_attack | 21 | -1.367% [-3.696, +0.963] | 13.6 | NULL |
| agg_crude_exports | conflict_escalation | 34 | +0.738% [-1.424, +2.900] | 79.6 | NULL |
| agg_crude_exports | opec_decision | 38 | -0.376% [-2.660, +1.908] | 63.4 | NULL |
| agg_crude_exports | sanctions | 35 | -0.060% [-2.258, +2.137] | 78.6 | NULL |
| agg_crude_exports | demand_shock | 13 | -3.133% [-7.311, +1.045] | — | INSUFFICIENT |
| agg_crude_exports | policy_response | 35 | +1.338% [-0.727, +3.402] | 97.8 | NULL |
| agg_crude_exports | all | 65 | +0.112% [-1.575, +1.799] | 74.0 | NULL |
| agg_crude_exports | tightening | 51 | -0.502% [-2.395, +1.391] | 24.4 | NULL |
| agg_products_demand | chokepoint_disruption | 20 | +0.169% [-2.355, +2.692] | 43.0 | NULL |
| agg_products_demand | infrastructure_attack | 21 | +0.231% [-1.121, +1.583] | 40.2 | NULL |
| agg_products_demand | conflict_escalation | 34 | -1.152% [-2.984, +0.679] | 0.4 | NULL |
| agg_products_demand | opec_decision | 38 | -1.230% [-2.943, +0.484] | 15.4 | NULL |
| agg_products_demand | sanctions | 35 | -0.762% [-1.897, +0.373] | 17.0 | NULL |
| agg_products_demand | demand_shock | 13 | -1.525% [-5.159, +2.108] | — | INSUFFICIENT |
| agg_products_demand | policy_response | 35 | -0.377% [-1.453, +0.700] | 17.8 | NULL |
| agg_products_demand | all | 65 | -0.493% [-1.630, +0.643] | 14.0 | NULL |
| agg_products_demand | tightening | 51 | -0.406% [-1.701, +0.890] | 5.0 | NULL |

### 2.3 Does the machinery see an identified shock in this data?

Node: `agg_crude_production (10 balanced reporters)`. Expected sign on production: + (a positive B-H supply shock is more production).

| shock series | on aggregate production, h=3 | on the crude price, h=3 | months |
|---|---|---|---|
| bh_supply_shock | +0.200% [-0.236, +0.637] | -4.646% [-7.074, -2.217] | 291 |
| kanzig_news_shock_monthly | +0.462% [-0.335, +1.259] | +10.935% [+6.193, +15.678] | 288 |

### 2.4 The exploratory family (every reporter × flow × shock)

A disclosed post-hoc screen (degenerate if >10% of in-window observations are zero, or the SD of the monthly 100*log change exceeds 25) marks 21 of 106 series as degenerate — Germany reports zero crude exports in most months, Korea's crude 'production' is a rounding error. The screen is computed from the series alone, never from a coefficient, and both tallies are published.

| verdict | all cells | cells on non-degenerate series |
|---|---|---|
| TRANSMITTING | 22 | 21 |
| NULL | 655 | 575 |
| INSUFFICIENT | 277 | 169 |
| **total** | **954** | **765** |
| expected TRANSMITTING under a complete null | 2.4–47.7 | 1.9–38.2 |
| surviving BH q=0.10 within the node's family | 24 | — |

**The monthly placebo is thin.** Pool 108 months across 58 state buckets; on average 26.4 buckets per cell fall back to VIX-decile-only matching. A monthly TRANSMITTING verdict therefore rests mainly on the two standard-error bands. **v2 ran no monthly placebo at all**, which made TRANSMITTING unreachable for every monthly node by construction — a defect in the v2 study, recorded here rather than quietly fixed.

| node | shock | n | β(h=3) [95%] | placebo pct | BH |
|---|---|---|---|---|---|
| ae.refinery_intake | opec_decision | 22 | -13.998% [-25.574, -2.421] | 0.0 | **yes** |
| ae.refinery_intake | all | 49 | -10.316% [-18.416, -2.216] | 0.0 | **yes** |
| br.crude_stocks | chokepoint_disruption | 15 | +13.807% [+6.142, +21.472] | 100.0 | **yes** |
| ca.products_demand | policy_response | 35 | -2.286% [-4.362, -0.211] | 0.2 | no |
| cn.refinery_intake | conflict_escalation | 34 | -3.147% [-6.253, -0.042] | 0.2 | no |
| de.refinery_intake | policy_response | 35 | -2.573% [-4.854, -0.293] | 0.0 | no |
| dz.products_demand | tightening | 45 | -3.632% [-6.117, -1.147] | 0.6 | **yes** |
| gb.products_demand | infrastructure_attack | 21 | +2.225% [+0.279, +4.171] | 99.4 | no |
| in.refinery_intake | chokepoint_disruption | 20 | -3.638% [-6.980, -0.296] | 0.2 | no |
| in.refinery_intake | opec_decision | 38 | -3.814% [-6.802, -0.825] | 1.4 | no |
| jp.products_demand | conflict_escalation | 34 | -2.904% [-5.354, -0.455] | 2.4 | no |
| kr.products_demand | conflict_escalation | 34 | -2.446% [-4.295, -0.597] | 0.2 | **yes** |
| kw.products_demand | all | 60 | -7.424% [-12.571, -2.277] | 0.0 | **yes** |
| ng.crude_production | chokepoint_disruption | 20 | -4.651% [-8.535, -0.767] | 1.2 | no |
| ng.refinery_intake | conflict_escalation | 28 | +47.059% [+10.939, +83.178] | 97.8 | **yes** |  ← degenerate series
| no.products_demand | tightening | 51 | -6.802% [-11.039, -2.565] | 0.6 | **yes** |
| qa.crude_exports | conflict_escalation | 16 | -5.708% [-10.490, -0.926] | 0.0 | **yes** |
| qa.crude_production | conflict_escalation | 16 | -3.483% [-6.104, -0.861] | 0.0 | **yes** |
| qa.crude_production | tightening | 27 | -2.537% [-4.562, -0.511] | 0.0 | **yes** |
| ru.refinery_intake | opec_decision | 32 | -2.298% [-3.704, -0.892] | 0.6 | **yes** |
| us.crude_production | conflict_escalation | 34 | +1.522% [+0.026, +3.018] | 100.0 | no |
| us.refinery_intake | opec_decision | 38 | -2.288% [-4.169, -0.407] | 0.8 | no |

## 3. PortWatch — the registered primary test is INSUFFICIENT at every chokepoint

| chokepoint | named events (de-overlapped, 2019+) | clears n≥15? |
|---|---|---|
| Strait of Hormuz | 8 | **no** |
| Bab el-Mandeb | 5 | **no** |
| Suez Canal | 1 | **no** |
| Cape of Good Hope | 0 | **no** |
| Malacca Strait | 0 | **no** |
| Panama Canal | 0 | **no** |
| Bosporus | 0 | **no** |

The registration forbids reading a cell below n = 15. Every named-chokepoint cell is below it, so the registered primary test returns **INSUFFICIENT everywhere** — a fact about the corpus, knowable without estimating anything.

### 3.1 The secondary: per-class shocks on all seven chokepoints

| verdict | cells |
|---|---|
| TRANSMITTING | 0 |
| NULL | 105 |
| INSUFFICIENT | 63 |
| **total** | **168** |
| surviving BH q=0.10 | 3 |

### 3.2 The reroute counter-node

| shock | Bab el-Mandeb β(h=5) | Cape of Good Hope β(h=5) | reading |
|---|---|---|---|
| chokepoint_disruption | +2.130 | +3.294 | common time trend, not a reroute |
| infrastructure_attack | -1.810 | +0.158 | consistent with a reroute |
| conflict_escalation | -5.298 | +4.033 | consistent with a reroute |
| opec_decision | +0.902 | -1.950 | opposite signs but the wrong way round |
| sanctions | -7.840 | -4.919 | common time trend, not a reroute |
| demand_shock | +9.461 | -15.526 | opposite signs but the wrong way round |
| policy_response | +2.056 | -8.164 | opposite signs but the wrong way round |
| tightening | -0.739 | +7.109 | consistent with a reroute |

### 3.3 Leave-one-episode-out (C.3, mandatory)

**Dropping red_sea_2024** (2023-12-01 → 2024-12-31, 397 days).

**Dropping hormuz_2026** (2026-03-01 → 2026-08-30, 183 days).

Cluster jackknife over 35 (node × shock) cells: **10** change sign when a single de-overlapped event is removed.

## 4. The two episodes, described and not estimated

| episode | node | pre | post | change |
|---|---|---|---|---|
| Red Sea 2024 | Bab el-Mandeb tankers/day | 26.32 | 11.42 | **-56.6%** |
| Red Sea 2024 | Cape of Good Hope tankers/day | 9.5 | 19.18 | **+101.8%** |
| Red Sea 2024 | Brent, $/bbl | 84.69 | 80.56 | — |
| Hormuz 2026 | Hormuz tankers/day | 40.36 | 3.09 | **-92.3%** |
| Hormuz 2026 | Cape of Good Hope tankers/day | 16.63 | 20.07 | **+20.7%** |
| Hormuz 2026 | Brent, $/bbl | 66.03 | 98.06 | — |

n = 1 each. No estimator in this study can speak to a single episode; these are levels.

Brent, monthly mean, against Hormuz tanker transits:

| month | Brent $/bbl | Hormuz tankers/day |
|---|---|---|
| 2025-12 | 62.54 | 30.42 |
| 2026-01 | 66.6 | 31.13 |
| 2026-02 | 70.89 | 43.46 |
| 2026-03 | 103.13 | 0.94 |
| 2026-04 | 117.29 | 2.6 |
| 2026-05 | 107.14 | 1.71 |
| 2026-06 | 85.4 | 5.67 |
| 2026-07 | 83.76 | 5.74 |
| 2026-08 | 91.4 | 1.77 |
