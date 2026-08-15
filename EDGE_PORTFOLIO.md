# EDGE PORTFOLIO — the pre-registered battery, scored

*Results of `src/edge_battery.py` (run 2026-07-30, corpus N=289). Registration frozen **before** this
run in `PRE_REGISTRATION.md` / git tag `edge-battery-preregistered-20260730`. This is the honest
scorecard — validated survivors **and** every null. The nulls are not a failure; they are the product.*

> **⚠ RED-TEAM-1 RE-TIER (R7, governing).** Under the single evidentiary bar
> (SAR-standardized + regime-block-robust CI excluding zero + permutation-FDR;
> see `EVALUATION.md` §0), the **entire prior validated set downgrades to
> SUGGESTIVE** — H1, copper_growth, palladium_supply, hy_credit_stress,
> severity_dose_response, CC2, CC5. On the raw-|CAR| metric below the numbers stand,
> but raw |CAR| is a volatility quantity (attack #1); on the standardized metric the
> validated set is **empty**. Receipts: `data/evidentiary_bar.json`,
> `docs/red_team_1.md`. The tables below are the *as-registered raw-metric* record,
> retained unedited; the bar in `EVALUATION.md` §0 governs tiering.

## Update — WS-S (2026-07-30): strengthened, family grew 10 → 12, a NEW edge validated
The capture-and-strengthen pass (dated `PRE_REGISTRATION.md` amendment) added two apt keyless
conditioners and fixed one real bug. Honest outcome, both directions:
- **NEW VALIDATED EDGE: `hy_credit_stress`** — +1.65% [+0.22, +3.94], perm_p 0.012, FDR-q 0.070,
  survives robustness. Un-capping credit (a HYG-drawdown proxy, since the keyless HY spread was capped
  at ~3y) turned a former **exclusion** into a real, tested, validated edge. **Validated set: 2**
  (`copper_growth`, `hy_credit_stress`).
- **A hyped anecdote correctly collapsed to null:** the clustering-bug fix (cluster *within* type) took
  `chokepoint_gt_sanction` from a **n=3 anecdote at +3.8%** to a **fairly-tested null (+0.35%)**. The fix
  removed a spurious-looking result — integrity working the other way.
- `gold_real_rate` null (real rates weren't gold's missing key); `severity_dose_response` +3.87% still
  null (CI touches zero). Family-wise FDR now over **12** hypotheses.

**UCDP amendment (2026-07-30b):** added `conflict_intensity_gold` (does gold ripple harder when
UCDP-verified background conflict intensity is high?). Pre-registered before results; **null** (+0.93%,
CI [−0.36, +2.87]). Gold's safe-haven bid doesn't measurably depend on trailing verified conflict
intensity — reported, not chased. Family-wise FDR now over **13** hypotheses; validated set unchanged
(copper_growth, hy_credit_stress).

*The original 10-family scorecard below is preserved for the record.*

## Headline (original 10-family run)
A **10-hypothesis family** of economically-distinct conditioned event-study tests, corrected
**family-wise** (BH-FDR q=0.10 **and** Bonferroni α=0.05). **One survives: `copper_growth`** (already
the second validated edge). **The new hypotheses added no new validated edge** — the battery fairly
tested a diverse set and refused to manufacture edges. The portfolio grew in **credibility**, not count.

## Decision rule (fixed in advance)
`validated` ⇔ 95% cluster-bootstrap CI excludes zero **and** amp in the pre-declared direction **and**
survives family BH-FDR (q=0.10) **and** survives leave-one-cluster-out. Windows/metric frozen to the
existing study (est t−130..t−11, event t−5..t+20, horizon +20d, state at t−1, |CAR| magnitude).

## The scorecard (family of 10, corrected together)

| hypothesis | class | amp | 95% CI | perm p | FDR q | verdict |
|---|---|---|---|---|---|---|
| **copper_growth** | prior | **+4.34%** | **[+0.97, +6.55]** | 0.0003 | 0.003 | ✅ **VALIDATED** |
| gold_safe_haven | prior | +1.36% | [−0.29, +2.80] | 0.037 | 0.095 | null¹ |
| palladium_supply | prior | +5.20% | [−0.16, +10.19] | 0.018 | 0.092 | null¹ |
| yields_inflation | new | +6.64 bps | [−3.38, +14.60] | 0.038 | 0.095 | null¹ |
| gold_weak_dollar | new | +1.47% | [−0.73, +3.28] | 0.065 | 0.130 | null |
| silver_growth | new | +2.39% | [−1.31, +6.03] | 0.092 | 0.153 | null |
| palladium_growth | new | +2.98% | [−2.00, +8.56] | 0.133 | 0.190 | null |
| severity_dose_response | new | +2.40% | [−3.19, +8.40] | 0.233 | 0.238 | null² |
| chokepoint_gt_sanction | new | +3.82% | [−7.38, +21.54] | 0.238 | 0.238 | null³ |
| silver_precious | prior | +1.63% | [−2.22, +4.88] | 0.178 | 0.222 | null |

**Reported alongside (NOT in the amplification FDR family):**
| edge | n | signal | verdict |
|---|---|---|---|
| under_priced_risk_oos | 14 | turbulence 0.929, Wilson [0.685, 0.987] vs 0.521 base (lower bound beats base) | **SUGGESTIVE** — never validated at this N |

FDR survivors on the permutation p-value: **4**. Bonferroni survivors: **1** (copper).

## Footnotes a quant should read
**¹ Survives FDR on the permutation p, but the bootstrap CI still spans zero.** Requiring *both* is the
conservative gate — these three (gold-as-safe-haven, palladium-under-stress, yields-under-inflation) are
**suggestive, not validated**. That double requirement is the machinery that stops a permutation-lucky
result from being called an edge. It is doing visible work here.

**² Severity dose-response** (high-sev 4–5, n=24 vs low-sev 1–2, n=19): directionally sensible (higher
coded severity → bigger ripple, +2.4%) but null. A soft *positive* signal that the codebook's severity
coding tracks reality, without clearing the bar.

**³ Chokepoint > sanction** is directionally large (+3.8%) but rests on only **3 clustered chokepoint
episodes** — that is anecdote, not statistics (CI [−7, +22]). Reported, not believed.

**Collinearity:** the conditioners (vix_pct, curve_2s10s, usd_z, be_level) have max pairwise |r| =
**0.30** over 4,862 common days — genuinely distinct economic drivers, **not "VIX in disguise."**

## Honest exclusions (declared, not force-fit)
- **natural gas** — weather/storage-driven; no clean market-state proxy.
- **wheat** — supply/weather-driven; no clean market-state proxy.
- **HY credit** — keyless FRED caps the HY spread (`fred.BAMLH0A0HYM2`) at ~3y, so no point-in-time
  credit-cycle state exists for pre-2024 events. Excluded rather than tested on an unfair window.

## What this means for the portfolio
The validated set is unchanged: **H1** (VIX-stress → oil, generalized to Brent, heating oil, 5Y
breakeven, S&P) plus **copper under a growth regime**. The battery's value is the **process**: a
pre-registered, family-wise-corrected, fully-reported test of a diverse hypothesis set. For a research
audience, *"I tested ten, one survives, three are suggestive, here is everything that didn't work"* is a
stronger claim than any single manufactured edge.

The one genuinely new *kind* of edge — **mispricing** (market error, not reaction magnitude) — is the
most promising suggestive signal and the natural next brick: it becomes a real test only as the corpus
(and the resolved gap ledger) grows. That is time, not code.

## Red-team-1 update (R6) — CC2 downgraded to SUGGESTIVE
The cross-chain edge **CC2 (supply → gasoline crack)** was `validated` (+2.96 $/bbl
[0.99, 5.21]). Under adversarial review it survives dropping its two
post-registration outliers alone (+1.83 [0.36, 3.31]) and month-of-year seasonal
adjustment alone (+2.17 [0.35, 4.25]), but **not both controls jointly**
(+1.16 [−0.22, +2.56], perm p=0.06 — CI includes zero). A robust edge should clear
both at once; CC2 does not, so it is now **SUGGESTIVE**. Receipts:
`data/cc2_seasonal.json`, `data/evidence/edge.CC2_supply_gasoline_crack.json`,
`docs/red_team_1.md`.

*Receipts: `data/edge_battery.json` · registration: `PRE_REGISTRATION.md` (tag
`edge-battery-preregistered-20260730`) · method: `METHOD.md`, `src/validate.py`.*
