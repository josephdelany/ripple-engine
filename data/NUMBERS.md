# NUMBERS.md — the single reconciliation table (red-team-1, R9)

*Every public number, the **N it was computed on**, the **commit**, and the **receipt**.
Built to answer attack #17 ("a reviewer cannot tell which N produced which number").
This file is the source of truth for counts and headline figures; if any other doc
disagrees, this file wins and that doc is the bug.*

## Corpus counts — there are two legitimate N's, always labelled
| N | meaning | frozen? | where used |
|---|---|---|---|
| **289** | the **registered corpus**, frozen 2026-07-30 at git tag `edge-battery-preregistered-20260730` | YES — never recomputed | registration; R5 tier-1 frozen number |
| **296** | the **current** corpus (289 + 7 post-registration additions) | no — grows | tracking numbers, current packs |
| ~~291~~ | intermediate snapshot (V3 cross-chain amendment, 2026-08-03) | — | historical only; not a current number |
| ~~293~~ | intermediate snapshot (post-sweep, DATA_DICTIONARY/STATE) | — | **STALE** → corrected to 296 in R9 |

The 7 post-registration additions (289→296): `iran_israel_us_strike_2026`,
`hormuz_closure_2026`, `us_iran_hormuz_mou_2026`, `ecuador_leaves_opec_2019`,
`gabon_coup_2023`, `nigeria_fuel_subsidy_removed_2023`, `uschina_phase1_2020`.
List frozen in `data/registered_corpus_289.txt`.

## Other counts (current)
| thing | count | note |
|---|---|---|
| tests (pytest collect) | **151** | 131 pre-V0 → 147 post-V0 → 151 with red-team-1 lenses |
| evidence packs | **13** | 6 claim packs (`edge.*`,`hyp.H1`) + 7 node packs (`node.*`) in `data/evidence/` |
| FDR family (amplification) | 13 hypotheses | `PRE_REGISTRATION.md`; `edge_battery.json` |

## H1 — every published number (VIX-stress → Brent |CAR/SCAR +20|)
| number | value | N / n | commit | receipt |
|---|---|---|---|---|
| registered-sample headline (immutable) | **+10.3pp** raw | n=20 sample | reg. 2026-07-21 | `registered_run_results.txt` |
| frozen registered-corpus, raw | +5.00pp [0.86, 8.95] | N=289 | `9c9f476` (R5) | `h1_frozen_threshold.json` |
| frozen registered-corpus, **SAR** | **+0.158σ [−0.247, 0.523]** incl.0 | N=289 | `9c9f476` (R5) | `h1_frozen_threshold.json` |
| out-of-sample 2019+, raw (frozen thr) | +2.92pp [−12.34, 18.92] | n=16 | `9c9f476` (R5) | `h1_frozen_threshold.json` |
| out-of-sample 2019+, **SAR** | +0.60σ [−0.32, 1.62] incl.0 | n=16 | `9c9f476` (R5) | `h1_frozen_threshold.json` |
| current tracking, raw (headline surfaces) | **+5.5615pp [0.9436, 9.6525]** p=0.005 | N=296 (87 ep) | `e2baaa2` (R1) | `h1_sar.json`, `validation_claims.json` |
| current tracking, **SAR** (the metric) | **+0.2524σ [−0.2151, 0.651]** p=0.119 incl.0 | N=296 (87 ep) | `e2baaa2` (R1) | `h1_sar.json` |
| VIX-matched non-event placebo (raw) | pseudo +3.04pp [−0.08, 6.43]; real inside band | N=296 | `5abe7b5` (R2) | `placebo_vixmatched.json` |
| regime-block SAR (drop 2008/2020/2026/all) | all include zero | N=296 | `fcc2ca2` (R3) | `h1_regimeblock.json` |

**Convention note (a latent inconsistency, now documented).** Two median-split
conventions coexist in the code: `validate.py` uses `state >= median` (gives the
canonical **+5.5615pp** raw current number that every surface publishes);
`spec_curve.py`/`frozen_lens.py` use `state > median` (gives +6.07pp on the same
data). Both yield the same conclusion (raw excludes zero, SAR does not). The
**published H1 raw current number is +5.5615pp** (`validate` convention, `h1_sar.json`).

## Cross-chain CC2 — gasoline crack ($/bbl, signed CAR+10)
| number | value | n | commit | receipt |
|---|---|---|---|---|
| baseline (registered) | +2.96 [0.99, 5.21] p=0.003 | 37 | cross_chain | `edge.CC2_supply_gasoline_crack.json` |
| ex both outliers | +1.83 [0.36, 3.31] | 35 | `99104e2` (R6) | `cc2_seasonal.json` |
| seasonally adjusted | +2.17 [0.35, 4.25] | 37 | `99104e2` (R6) | `cc2_seasonal.json` |
| **seasonal + ex both** (strictest) | **+1.16 [−0.22, 2.56]** p=0.06 incl.0 | 35 | `99104e2` (R6) | `cc2_seasonal.json` |

## Amplification family under the one bar (R7, SAR) — receipt `evidentiary_bar.json`
| edge | SAR full | regime-robust? | re-tier |
|---|---|---|---|
| H1 | +0.25 [−0.22, 0.65] | no (null every cut) | SUGGESTIVE |
| copper_growth | +0.47 [0.09, 0.74] (FDR ✓) | no (drop-2008 [−0.06, 0.59]) | SUGGESTIVE (closest) |
| palladium_supply | +0.12 [−0.28, 0.54] | no | SUGGESTIVE |
| hy_credit_stress | +0.30 [−0.23, 0.91] | no | SUGGESTIVE |
| severity_dose_response | +0.18 [−0.26, 0.67] | no | SUGGESTIVE |

## Calibration (forecast skill) — receipt `evaluation.json`
Brier **0.2466** vs base **0.2495** → skill **0.0029**, resolution 0.0042, over **n=247**
resolved gaps (67 quarters). No demonstrated forecast edge.

## Attack #18 — pre-1990 VIX/VXO splice + percentile window
**Resolved: no splice exists and none is needed; the percentile window is point-in-time.**
- `derived.vix_pct` = `VIXCLS.rolling(1260, min_periods=252).rank(pct=True)*100`
  (`src/derive_signals.py:149-151`) — a **trailing ~5-year rolling rank**, NOT a
  full-sample rank. **No lookahead** in the conditioner (the percentile at date *t*
  uses only data up to *t*).
- `fred.VIXCLS` earliest observation: **1990-01-02**. With a 252-obs minimum, the
  first usable VIX state is ~Jan 1991; H1's **first episode is 1991-01-17**
  (`desert_storm_air_campaign_1991`). The one 1990 event (`iraq_invades_kuwait_1990`)
  carries VIX state **n/a** and is correctly excluded. **So no H1 event uses pre-1990
  (indeed pre-1991) VIX**, and there is no VXO splice — it would change nothing.
- CC2 (gasoline crack, from 1987) uses **no VIX conditioner** at all (it is a supply-
  event → crack test), so the pre-1990 VIX question does not touch it either.

*Reconciliation slice R9. Docs corrected: `DATA_DICTIONARY.md` (293→296),
`STATE_OF_THE_ENGINE.md` (current-count pointer added).*
