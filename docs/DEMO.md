# Instrument demonstration — 2026 Hormuz closure

> A single frozen historical read, shown to explain the instrument—not selected as proof of average performance.

**Target:** 2026-03-04 · `chokepoint_disruption` · Iran declares the Strait of Hormuz closed

**Seal:** `49d2206c8da24f1ef0cf391f86b240eb17cdba68ba435f1d809cb9f552a8428b` (verified before the outcome is attached)

The read compares the same 293 closed prior events. Structural weighting uses strictly available market/state fields (effective weight n 249.6); surface weighting uses event class only (effective weight n 33.8).

## Structural state

Forecast abnormal-return distribution: p25 -8.04%, median -0.37%, p75 +5.72% (weighted mean -2.22%).

| weight | date | class | historical case | +20d abnormal return |
|---:|---|---|---|---:|
| 0.007 | 2025-06-22 | `conflict_escalation` | US strikes Iranian nuclear sites Fordow Natanz and Isfahan | -8.44% |
| 0.007 | 2003-01-12 | `opec_decision` | OPEC raises quota 6.5% amid Venezuela strike | +4.14% |
| 0.007 | 2022-03-04 | `policy_response` | Hungary bans all grain exports | -10.66% |
| 0.007 | 2010-08-05 | `policy_response` | Russia announces temporary grain export ban | -12.02% |
| 0.007 | 2019-01-28 | `sanctions` | US sanctions on PDVSA | +10.45% |

## Surface class

Forecast abnormal-return distribution: p25 -6.16%, median -1.52%, p75 +5.02% (weighted mean -2.32%).

| weight | date | class | historical case | +20d abnormal return |
|---:|---|---|---|---:|
| 0.036 | 2025-11-14 | `chokepoint_disruption` | Ukrainian drone strike halts oil loadings at Novorossiysk Sheskharis terminal | +1.02% |
| 0.036 | 2025-08-18 | `chokepoint_disruption` | Ukrainian strike halts Druzhba pipeline oil flow to Hungary and Slovakia | +2.02% |
| 0.036 | 2023-11-19 | `chokepoint_disruption` | Houthis seize Galaxy Leader car carrier in Red Sea | -5.73% |
| 0.036 | 2023-12-01 | `chokepoint_disruption` | Houthi attacks disrupt Red Sea shipping | -6.05% |
| 0.036 | 2023-12-15 | `chokepoint_disruption` | Houthi drone strike triggers Red Sea shipping diversions | +5.02% |

## Resolution

Realized +20-day abnormal Brent return: **+42.46%**.

CRPS: structural **37.876**, surface **38.971**, uniform pooling **37.309** (lower is better). **Structural** beat the other analogy arm; **uniform pooling** scored best overall.

This one read demonstrates mechanics and auditability. The project-level conclusion comes from all 264 inferential dates in `data/structural_surface/summary.json`, not from this example.

