# Red Team 1 — adversarial review + remediation record

*This file is the frozen record of the first external adversarial review of the
ripple engine, and the disposition of every attack. Per `RED_TEAM_1_RESPONSE.md`,
it is committed **before** any recomputation — the order is itself integrity
evidence. Numbers are filled in as each slice (R1–R9) lands; every result is
published as computed, including downgrades.*

**Reviewer stance:** skeptical senior quantitative researcher, instructed to
attack. **Disposition philosophy:** the review is high quality; most attacks are
**CONCEDED** and answered with *computation, not argument*. The frozen registered
record (`BRIEF_SKELETON.md`, `REGISTERED_SAMPLE.md`, `PRE_REGISTRATION.md`
n=20 / N=289) is **never edited**; all new analyses are **additive lenses** with
receipts. Claim/wording changes happen only **after** numbers land, with Joe's
sign-off.

---

## Part 1 — the reviewer's full text (verbatim)

**Estimand first.** The headline claim (`hyp.H1`) is: *"Geopolitical shocks ripple
harder into Brent oil when VIX stress is elevated,"* amp **+5.56pp**, CI
**[0.94, 9.65]**. Almost every attack converges on one thing: **the project has not
shown this is a causal amplification rather than mechanical volatility clustering
in a selected, endogenous event set.**

### A. The headline is probably heteroskedasticity, not "amplification"

**1.** The metric is a volatility measure and it is split by a volatility index.
`_car_mags` (`research.py:101`) returns `abs(car[PRE+horizon])` from a
**constant-mean** abnormal-return model. |CAR| over 20 days is, mechanically,
|20-day return − 20·mean|. VIX *is* expected volatility. High-VIX windows have
larger absolute returns for essentially every asset on every date, by
construction. Splitting an **unstandardized** magnitude at the VIX median and
finding the high side bigger is close to tautological. The field's standard fix —
Boehmer-Musumeci-Poulsen (1991) standardized abnormal returns — is exactly what
the headline does **not** use. `FRONTIER_AUDIT` F1 names this; `validate.py:398`
shows a standardized-sigma variant exists, but the advertised 5.56pp is the
un-standardized one. Until the headline is the SAR-standardized number, the result
is not credible.

**2.** The "placebo" cannot discriminate the confound. `permutation_p`
(`validate.py:192`) and the EVALUATION §1 placebo shuffle the state↔magnitude
pairing; the null is "no association between VIX-state and magnitude." But the
heteroskedasticity story *also* implies a real association (high VIX ⟺ high
realized vol ⟺ high |CAR|). Both the causal hypothesis and the artifact predict
the permutation rejects. So "placebo null" is necessary, not sufficient, and it is
presented as the soundness proof. The correct negative control is pseudo-events
drawn from VIX-matched dates (or SAR-standardized returns), not label-shuffling.

### B. The "high-stress" bin isn't geopolitical shocks — it's crises and endogenous OPEC reactions

**3.** The largest |CAR| in the high-VIX bin (`hyp.H1.json`): Lehman 33.6
(state 94.8), OPEC-extend-June-2020 35.98 (COVID, state 90.8), OPEC-Oran-2008 31.1
(state 96), OPEC-emergency-cut-2008 28.6 (state 99.7), Iraq-war 33.9, BTC-pipeline
26.4, 9/11 25.5, Iran-strike-2026 50.67. The high bin ≈ {1998 Asia/Russia crisis,
2008 GFC, 2020 COVID, 2026 Iran}. That is "oil's absolute moves are huge during
financial crises," not "geopolitical shocks rippling harder."

**4.** Reverse causality. OPEC-emergency-cut-2008, OPEC-Oran-2008,
OPEC-extend-June-2020 are the biggest high-bin |CAR|s and they are **responses to
the price collapse**, not causes of it. Codebook rule #4 ("not a price move
itself") does not catch an endogenous policy reaction. OPEC decisions are ~40% of
the corpus and dominate the tail.

**5.** "Geopolitical shock" is stretched to include Lehman, the Thai baht float,
Korea's IMF bailout, the 2001 recession onset, IMF growth downgrades, steel
tariffs, Nigeria's fuel-subsidy removal, Indonesia's ore ban, Philippine nickel
closures, Kazatomprom uranium cuts, Marikana. Half the corpus is macro-financial
or non-oil-commodity. Restrict to genuinely geopolitical types and re-run.

**6.** Selection on salience (`FRONTIER_AUDIT` F4). Hand-curated events enter
because someone remembered them, and memorable events are disproportionately the
ones that moved markets — selection on the outcome. The GDELT harvest that would
populate quiet non-movers is quarantined to the reference tier and never enters
the causal corpus.

### C. Dependence understated; robustness weaker than advertised

**7.** 35-day same-type clustering (`edge_battery.py:121-128`) treats the six
distinct 2008 events (Jan SA-power → Dec Oran, all >35d apart) as six independent
episodes inside one oil collapse. The cluster bootstrap and leave-one-cluster-out
over-count effective N. Drop 2008 / 2020 / 2026 as **regime blocks** and report.

**8.** CI barely clears zero (lower bound 0.94pp on 5.56) and leans on
post-registration outliers: the 2026 Iran events (|CAR| 50.67, 21.74) were added
after registration (pack N=296 vs registered N=289). Winsorize or drop 2026 and
publish.

### D. Registration integrity is half theater

**9.** The advertised 5.56pp is recomputed on the growing corpus (N=296), not the
frozen registered N=289 — the pack says so. The genuinely frozen/OOS estimate is
the temporal holdout: **2.921pp on 2019+**, roughly half, and its CI is not
published. Lead with the frozen number.

**10.** In-sample median split (`validate.py:170,200` `np.median(states)`) uses the
whole sample, including future events, to label an event "high VIX" — lookahead in
the conditioner. The OOS section freezes a pre-2019 threshold; the headline does
not.

### E. The product has no forecasting skill

**11.** Calibration: Brier **0.2466** vs base **0.2495** → skill **0.0029** over
n=247, 67 quarters. A 1.2% relative improvement — indistinguishable from zero. The
engine only emits 0.4 or 0.6 (resolution 0.0042). NORTH_STAR's premise is
"understand a market shift before consensus prices it"; the calibration says it
cannot.

**12.** The miss-audit (EVALUATION §5) refutes H1's mechanism OOS: worst-scored
gaps are all *"regime_misread — engine saw turbulence (high VIX); calm realised,"*
and they are the same high-VIX events that drive H1 (OPEC-emergency-cut-2008,
SA-power-2008, Iran-CISADA). In-sample amplification + out-of-sample anti-signal =
overfit to volatility clustering.

### F. Cross-chain edges: same disease, weaker

**13.** CC2 (gasoline crack, +2.96 $/bbl, n=37) has signs all over the place:
underlying CARs include −5.92, −6.85, −6.17 alongside +10.97, +16.64 and a lone
+29.01 (hormuz_closure_2026, post-registration, ~10× the median). Nearly half are
negative against the predicted "+". Drop hormuz_2026 and venezuela_blackout_2019
and the CI [0.99, 5.21] likely crosses zero.

**14.** No seasonality control in a 1987–2026 gasoline-crack study; the crack has a
strong summer-driving-season signature the constant-mean model does not remove.

### G. Multiple-comparison accounting bends toward winners

**15.** The weakest edge (mispricing, n=14, in-sample direction) is conveniently
"reported alongside, NOT in the FDR family." Every framing choice protects the
survivors.

**16.** Inconsistent bar: gold/palladium survive FDR-on-permutation-p but are
(correctly) not called validated because the bootstrap CI spans zero — yet
permutation-p is the primary support for H1. Apply one bar to H1 too.

### H. Smaller but real

**17.** Receipts don't reconcile: corpus 289/291/293/296, tests 131/147/150/151,
evidence packs 9/11/13 across docs. A reviewer cannot tell which N produced which
number.

**18.** Pre-1990 "VIX": CC2 starts 1987 and H1's percentile state needs a VIX/VXO
splice pre-1990 — note the instrument break and confirm the percentile reference
is not full-sample (lookahead).

**19.** "$0/keyless / no-fabrication" is a provenance guarantee, not a correctness
one; it is repeatedly invoked as if it were scientific virtue.

### Verdict (reviewer)
The engineering and process are real (pre-registration ordering, honest nulls,
receipts, cage) — credible as a *build*. That does not transfer to the scientific
claims. H1 is not established; it is consistent with volatility clustering in a
salience-selected, partly-endogenous event set, and the negative control does not
rule that out. Cross-chain edges are outlier-driven. The forecasting product has
no measurable skill. **Credible as a build; not yet credible as a result.**

---

## Part 2 — disposition table

Legend: **CONCEDE** = accept and answer with computation. **CONCEDE\*** = accept as
a mitigation that cannot be fully solved without a different corpus, documented as
a standing limitation. No attack is CONTESTED — the remediation posture is
concede-and-compute.

| # | attack (short) | disp. | slice | action | receipt path |
|---|---|---|---|---|---|
| 1 | unstandardized \|CAR\| = vol clustering | CONCEDE | R1 | SAR headline; raw → secondary | `data/evidence/hyp.H1.json`, `data/h1_sar.json` |
| 2 | placebo can't test the confound | CONCEDE | R2 | VIX-matched pseudo-event placebo | `data/placebo_vixmatched.json` |
| 3 | high bin = crises not geopolitics | CONCEDE | R4 | subset re-run (geopolitical-only) | `data/h1_subsets.json` |
| 4 | reverse-causal endogenous OPEC cuts | CONCEDE | R4 | `endogenous_response` flag (Joe reviews) | codebook + `data/h1_subsets.json` |
| 5 | elastic "geopolitical" event set | CONCEDE | R4 | claim-matched subset | `data/h1_subsets.json` |
| 6 | selection on salience | CONCEDE\* | R4 | documented limitation; GDELT-tier note | `data/red_team_1.md`, R4 note |
| 7 | 35-day clustering understates dependence | CONCEDE | R3 | regime-block leave-out | `data/h1_regimeblock.json` |
| 8 | CI leans on post-reg outliers | CONCEDE | R3 | winsorized + drop-2026 CIs | `data/h1_regimeblock.json` |
| 9 | advertised N≠registered N | CONCEDE | R5 | frozen-number-leads headline block | pack + README |
| 10 | in-sample median split lookahead | CONCEDE | R5 | frozen-threshold split variant | `data/h1_frozen_threshold.json` |
| 11 | no forecasting skill | CONCEDE | R8 | calibration reframed near-baseline [Joe] | `EVALUATION.md`, NORTH_STAR/README |
| 12 | miss-audit refutes mechanism OOS | CONCEDE | R8 | regime_misread cited in H1 pack | `data/evidence/hyp.H1.json` |
| 13 | CC2 outlier-driven | CONCEDE | R6 | outlier-drop CI | `data/evidence/edge.CC2_supply_gasoline_crack.json` |
| 14 | no seasonality control | CONCEDE | R6 | month-of-year seasonal adj. | CC2 pack + `data/cc2_seasonal.json` |
| 15 | weakest edge outside FDR family | CONCEDE | R7 | one honest paragraph | `EVALUATION.md` |
| 16 | inconsistent evidentiary bar | CONCEDE | R7 | one bar, applied retroactively | `EVALUATION.md`, packs |
| 17 | receipts don't reconcile | CONCEDE | R9 | `data/NUMBERS.md` single source | `data/NUMBERS.md` |
| 18 | pre-1990 VIX/VXO splice | CONCEDE | R9 | verify splice + percentile window | H1 pack, `data/NUMBERS.md` |
| 19 | provenance ≠ correctness | CONCEDE | R8 | reframed as integrity property [Joe] | README, NORTH_STAR |

### Final numbers (filled as slices land)
- R1 SAR H1: _pending_
- R2 VIX-matched placebo: _pending_
- R3 regime-block CIs: _pending_
- R4 subset re-runs: _pending_
- R5 frozen/OOS/current block: _pending_
- R6 CC2 outlier-drop + seasonal: _pending_
- R7 retroactive bar outcomes: _pending_
- R8 purpose reframe (Joe sign-off): _pending_
- R9 reconciliation: _pending_

### Sign-off gates (stop for Joe)
1. **R4(i)** — Joe reviews the `endogenous_response` flag list before it drives any claim change.
2. **R8** — purpose-reframe wording.
3. **Final** — exact new headline wording.
