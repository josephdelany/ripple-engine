# Instrument demonstration — 2026 Hormuz closure

> A single frozen historical read, shown to explain the instrument—not selected as proof of average performance.

**Target:** 2026-03-04 · `chokepoint_disruption` · Iran declares the Strait of Hormuz closed

**Seal:** `fe9c98a498897489a3e771fcf9a3c11b2d375bf9147e3e03aa0b987e1392be40` (verified before the outcome is attached)

The read compares the same 293 closed prior events. Structural weighting uses strictly available market/state fields (effective weight n 249.6); surface weighting uses event class only (effective weight n 33.8).

## Structural state

Forecast abnormal-return distribution: p25 -7.75%, median -0.36%, p75 +5.75% (weighted mean -2.15%).

| weight | date | class | historical case | +20d abnormal return |
|---:|---|---|---|---:|
| 0.007 | 2025-06-22 | `conflict_escalation` | US strikes Iranian nuclear sites Fordow Natanz and Isfahan | -7.24% |
| 0.007 | 2003-01-12 | `opec_decision` | OPEC raises quota 6.5% amid Venezuela strike | +4.88% |
| 0.007 | 2022-03-04 | `policy_response` | Hungary bans all grain exports | -11.75% |
| 0.007 | 2010-08-05 | `policy_response` | Russia announces temporary grain export ban | -12.82% |
| 0.007 | 2019-01-28 | `sanctions` | US sanctions on PDVSA | +6.04% |

## Surface class

Forecast abnormal-return distribution: p25 -4.82%, median -0.71%, p75 +4.65% (weighted mean -2.16%).

| weight | date | class | historical case | +20d abnormal return |
|---:|---|---|---|---:|
| 0.036 | 2025-11-14 | `chokepoint_disruption` | Ukrainian drone strike halts oil loadings at Novorossiysk Sheskharis terminal | +1.41% |
| 0.036 | 2025-08-18 | `chokepoint_disruption` | Ukrainian strike halts Druzhba pipeline oil flow to Hungary and Slovakia | +4.65% |
| 0.036 | 2023-11-19 | `chokepoint_disruption` | Houthis seize Galaxy Leader car carrier in Red Sea | -3.10% |
| 0.036 | 2023-12-01 | `chokepoint_disruption` | Houthi attacks disrupt Red Sea shipping | -4.82% |
| 0.036 | 2023-12-15 | `chokepoint_disruption` | Houthi drone strike triggers Red Sea shipping diversions | +3.42% |

## Resolution

Realized +20-day abnormal Brent return: **+36.66%**.

CRPS: structural **31.918**, surface **33.130**, uniform pooling **31.383** (lower is better). The **structural** arm scored better on this case.

This one read demonstrates mechanics and auditability. The project-level conclusion comes from all 264 inferential dates in `data/structural_surface/summary.json`, not from this example.

