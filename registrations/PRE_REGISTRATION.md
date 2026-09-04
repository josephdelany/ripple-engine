> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** A registration for a superseded study, kept so its pre-commitments stay auditable. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../SUBMISSION_STATUS.md).

# PRE-REGISTRATION — the edge battery

**Frozen:** 2026-07-30, at corpus N=289 events (1987–2025).
**Discipline:** this document + the `HYPOTHESES`/`CONDITIONING` tuples in `src/edge_battery.py` are
committed and git-tagged **before** `data/edge_battery.json` (the results) exists. The mechanism for
each test is declared here, in advance. Nothing below was chosen after seeing a result.

This follows the convention of `REGISTERED_SAMPLE.md` (the frozen n=20 sample) and the module-docstring
pre-registration already used in `src/domain_conditioning.py` (copper-under-growth).

## Why a battery, and why family-wise correction
The portfolio today is one mechanism (H1: VIX-stress amplifies the oil ripple, generalized to four
assets) plus one apt-conditioned second edge (copper under a growth regime). To grow it **without
p-hacking**, we declare a fixed set of economically-distinct hypotheses up front, run each through the
**same gate** (clustered median split → cluster-bootstrap 95% CI → 10k-permutation p), and **correct
across the whole family** (BH-FDR q=0.10 **and** Bonferroni α=0.05), reporting **every** verdict.

Expected outcome: **most of the battery is null.** That is not failure — the honest scorecard (with its
nulls) is the deliverable. The count of new edges is not the success metric; the discipline is.

## The decision rule (fixed, binding)
A hypothesis is **`validated`** iff **all** of:
1. the 95% cluster-bootstrap CI **excludes zero**, and
2. the amplification points in the **pre-declared direction** (amp > 0 as defined), and
3. it **survives BH-FDR at q=0.10** across the full family, and
4. it **survives leave-one-cluster-out** (the sign never flips when any single episode is dropped).

Bonferroni survival is reported too (stricter), but FDR is the gate. Windows and metric are **frozen**
to the existing study: estimation t−130..t−11, event t−5..t+20, horizon **+20 trading days**, median
split on the state read at **t−1** (point-in-time, no lookahead), |CAR| magnitude in the asset's unit.

## The family (10 amplification hypotheses, corrected together)

**Prior (already run in `domain_conditioning.py`; folded in for honest multiple-comparisons counting):**
| # | name | conditioner | asset | dir | mechanism |
|---|------|-------------|-------|-----|-----------|
| P1 | gold_safe_haven | derived.vix_pct | yf.gold | high | gold as safe haven under stress |
| P2 | silver_precious | derived.vix_pct | yf.silver | high | silver shares gold's stress channel |
| P3 | copper_growth | derived.curve_2s10s | yf.copper | high | copper is a growth metal (steep curve) |
| P4 | palladium_supply | derived.vix_pct | yf.palladium | high | palladium supply-concentrated → stress |

**New — Class 1 (apt conditioners for assets that were null under generic VIX-stress):**
| # | name | conditioner | asset | dir | mechanism |
|---|------|-------------|-------|-----|-----------|
| 1 | silver_growth | derived.curve_2s10s | yf.silver | high | silver is precious+**industrial** → growth metal |
| 2 | palladium_growth | derived.curve_2s10s | yf.palladium | high | autocatalyst/industrial → growth regime |
| 3 | gold_weak_dollar | derived.usd_z | yf.gold | low | gold rises as USD weakens; amplifies when USD already soft |
| 4 | yields_inflation | derived.be_level | fred.DGS10 | high | oil shock → nominal yields more when inflation regime hot |

**New — Class 2 (event-type heterogeneity of the oil edge; two-group tests on |CAR+20| in Brent):**
| # | name | comparison | mechanism |
|---|------|------------|-----------|
| 5 | chokepoint_gt_sanction | chokepoint_disruption vs sanctions | physical route shocks ripple harder than financial ones |
| 6 | severity_dose_response | severity 4–5 vs 1–2 | higher coded severity ripples harder (validates the coding) |

`derived.be_level` (10Y breakeven percentile, 5y) and `derived.usd_z` are added to `derive_signals.py`
with pre-declared mechanisms.

## Reported alongside, NOT in the FDR family
**`under_priced_risk_oos`** (Class 3, the mispricing edge) — when the engine flags under-priced risk
(H1 ON while OVX prices calm), does realized +20d turbulence follow? This is a **forecast-skill** test,
not an amplification, so it is **not** folded into the amplification FDR. It is **small-N (~14)** and its
direction is defined in-sample, so it is reported with a **Wilson CI vs the base rate** and labeled
**SUGGESTIVE — never `validated`** at this N. It becomes a real test only as the corpus grows.

## Honest exclusions (declared, not force-fit)
- **natural gas** — weather/storage-driven; no clean market-state proxy in the engine.
- **wheat** — supply/weather-driven; no clean market-state proxy (already excluded upstream).
- **HY credit** — keyless FRED caps the HY spread (`fred.BAMLH0A0HYM2`) at ~3y of history, so a
  point-in-time credit-cycle state cannot be built for events before 2024. Excluded rather than tested
  on an unfairly short window.

## Collinearity check
The conditioners (vix_pct, curve_2s10s, usd_z, be_level) are pairwise-correlated on their common dates
and the max |r| reported, to demonstrate the panel is **not "the VIX effect in disguise"** but distinct
economic drivers.

## Amendment 2026-07-30 (WS-S — capture more + strengthen)
Declared **before** the amended battery is run (register-then-run preserved; git history proves it).
Rationale: give economically-apt, keyless conditioners a fair, pre-registered test — and fix a real
clustering bug — rather than leave cells unfairly excluded/underpowered. Mechanisms fixed here in
advance; the family-wise FDR denominator grows to include these; the mispricing edge stays out of the
amplification FDR; genuine nulls stay null.

**New conditioners** (added to `derive_signals.MECHANISMS`, keyless):
- `derived.credit_stress` — HY credit-cycle stress (HYG drawdown-from-252d-high percentile, 2007+).
- `derived.real_rate` — 10Y TIPS real-yield percentile (`fred.DFII10`, 2003+).
- `derived.ovx_pct` — oil implied-vol (OVX) percentile (`fred.OVXCLS`, 2007+). [registered; available]

**New pre-declared hypotheses** (added to the family; direction fixed here before results):
| name | conditioner | asset | dir | mechanism |
|---|---|---|---|---|
| gold_real_rate | derived.real_rate | yf.gold | low | gold is a real-rate asset → amplifies when real rates are low |
| hy_credit_stress | derived.credit_stress | yf.hyg | high | a shock widens HY credit more when credit is already stressed (un-caps the excluded credit test) |

**Correctness fix (declared):** `edge_battery._oil_type_frame` now clusters **within event type** for the
two-group tests (`chokepoint_gt_sanction`, `severity_dose_response`). Clustering all types together
cannibalised the chokepoint arm (n=3 despite 24 raw events); within-type clustering earns those tests a
fair episode count. This is a bug fix, not a specification change to the hypotheses.

**Also planned under WS-S** (dated amendments filed as each is added, before its result): new priceable
nodes (platinum `PL=F`, freight `BDRY/STNG/FRO`, ags `ZC=F/ZS=F`, miners `COPX/GDX`, FX) tested through
the same generalization gate; and codebook-gated event backfill to give underpowered producer/chokepoint
cells a fair test. All re-runs re-report honestly; nulls that stay null are reported.

## Amendment 2026-07-30b (UCDP verified-conflict conditioner)
Declared **before** the amended battery is run (register-then-run; git proves it). Adds the gold-standard
UCDP conflict feed as a pre-registered conditioner. Family-wise FDR denominator grows to include it;
genuine null stays null.

**New conditioner** (added to `derive_signals.MECHANISMS`, $0/free-token):
- `derived.conflict_intensity_pct` — global UCDP monthly-fatalities percentile (5y). Point-in-time:
  monthly, forward-filled to daily, read at t−1 (the last *completed* month; a shock's day never sees
  its own month's not-yet-complete total).

**New pre-declared hypothesis:**
| name | conditioner | asset | dir | mechanism |
|---|---|---|---|---|
| conflict_intensity_gold | derived.conflict_intensity_pct | yf.gold | high | gold ripples harder into the safe-haven bid when background verified conflict intensity is already high |

Expectation stated up front: this may well be **null** (gold's safe-haven bid may not depend on trailing
conflict intensity) — reported honestly either way.

## Amendment 2026-08-03 (V3 — the cross-chain battery)
Declared **before** the battery is run (register-then-run; git proves `src/cross_chain.py` predates
`data/cross_chain.json`). A SEPARATE family from the oil edge battery: does the V1 value chain transmit
under a decision rule fixed in advance? Directions are fixed here; tested on the grown corpus (N=291).

**Registered family (directions fixed):**
| id | test | direction | mechanism |
|---|---|---|---|
| CC1 | supply events (chokepoint ∪ infrastructure) → diesel crack, CAR+10 | **+** (widens) | refined product tightens faster than crude |
| CC2 | supply events → gasoline crack, CAR+10 | **+** (widens) | same, motor-fuel channel |
| CC3 | sanctions events → copper, CAR+20 | **−** (down) | trade friction is growth-negative for the industrial metal |
| CC4 | fertilizer PPI → wheat, monthly pass-through β | **+** | fertilizer cost lifts crop prices |
| CC5 | fertilizer PPI → corn, monthly pass-through β | **+** | same |

**Decision rule (fixed):** VALIDATED iff the 95% bootstrap CI excludes zero *in the predicted direction*
**and** it survives family-wise **BH-FDR (q=0.10)**. Bonferroni (α=0.05) and the **raw** perm-p are
reported alongside every verdict — breadth never manufactures a discovery. A **placebo** (shuffled event
dates) must send the family null. Expectation stated up front: **most are expected null** (chain_view
showed cracks strong-contemporaneous, fertilizer→food weak); nulls are reported as results.

---
*Results (after running `python3 src/edge_battery.py` / `src/cross_chain.py`) live in
`data/edge_battery.json` / `data/cross_chain.json`. The original battery section above is frozen;
amendments are dated and appended.*
