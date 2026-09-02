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

## Amendment (2026-09-02) — Joe's Ruling 1 applied: the five amplification edges are retracted
*Registered before the code and before the table is touched. Session B, on Joe's authority
(`data/gates/ripple_2026-09-02.md`, Ruling 1, option (a)). Session C ran the re-test, registered it in
RIPPLE_REGISTRATION.md Amendment B BEFORE running it, and declined to edit a table that is not its file.
Nothing above is deleted; this amendment is appended.*

### What was retracted and why
`propagation_edges` carried five rows with `status = 'validated'`, kind `stress->node`
("geopolitical shock (VIX-stress regime)" → node, lag 20d). Session C's registered re-test — the
all-event shock restricted to days when `derived.vix_pct` at t−1 is at or above its median, h = 20,
against the VIX-and-GPR-matched placebo — returns NULL for every one of them:

| edge (`edge_id`) | old strength, CI | re-test β at h=20 | n | placebo pct | verdict |
|---|---|---|---|---|---|
| `amp.Brent oil` | +6.041 [+1.557, +10.087] | +0.614 % [−4.116, +5.345] | 40 | 55.0 | NULL |
| `amp.Heating oil` | +5.030 [+1.527, +9.230] | +2.008 % [−2.617, +6.633] | 35 | 87.8 | NULL |
| `amp.5Y breakeven` | +16.247 [+4.470, +31.022] | −0.061 pp [−0.237, +0.116] | 20 | 2.2 | NULL |
| `amp.S&P 500` | +1.894 [+0.342, +3.448] | −0.760 % [−2.769, +1.249] | 36 | 3.8 | NULL |
| `amp.Platinum` | +7.425 [+1.958, +14.647] | −1.286 % [−5.042, +2.469] | 25 | 4.2 | NULL |

Every re-test band covers zero by a wide margin, and three of the five have re-test point estimates of
the **opposite sign** to the strength that earned them `validated`.

### The rule, from this date
1. Those five `edge_id`s carry `status = 'retracted_h1_retest'`. The strength and CI columns keep the
   values as originally computed — the retraction is a status, not an erasure — and `mechanism` carries
   the pointer: `retracted 2026-09-02 by Joe's Ruling 1; re-test data/ripple/retraction_six.json;
   docs/red_team_1.md`.
2. **`src/propagation_graph.py` may not re-validate them.** The retraction is encoded in the code that
   writes the table (`RETRACTED_EDGE_IDS`), so a refresh cannot silently undo Joe's ruling. Lifting it
   needs a dated amendment here, not a re-run.
3. No surface calls them validated. `src/shock_tracer.py`'s transmission lane reads
   `status = 'validated'` and therefore stops showing them by construction.

### Palladium — recorded as computed, and not a finding
The re-test's sixth node, palladium, is the one that survives: **−5.807 % [−10.663, −0.951], n = 22,
placebo percentile 0.0, verdict TRANSMITTING**. It is recorded here and in
`data/ripple/retraction_six.json` as computed. It is **not** promoted anywhere, for three reasons
stated together, as Joe ruled:
- its `propagation_edges` row (`amp.Palladium`, strength +5.144 [−0.251, +10.108]) was **already
  `null`** before this amendment — it never held `validated` status, and it does not gain it now;
- palladium **is not on the oil chain** — the mechanism this engine exists to measure does not run
  through it;
- **one survivor out of six at this base rate is what noise looks like.** With six tests at a 5 %
  placebo threshold, the chance of at least one survivor under a complete null is about 26 %.
- the re-test's sign (−5.81 %) is opposite to the original row's (+5.14): the two estimates do not
  agree even in direction.
It is not to be surfaced as a finding on any page, in any export, or in the paper.

### EVALUATION.md
`EVALUATION.md` §0 already downgraded the entire prior validated set to SUGGESTIVE under the SAR bar
("under this bar the current validated set is empty"), so no claim there needs to be weakened further by
this amendment; the re-read is recorded in `data/gates/ruling1_applied_2026-09-02.md`. The table had been
lagging that document; this amendment makes the stored rows say what the published bar already said.
