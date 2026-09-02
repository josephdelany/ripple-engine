# Does the record predict? A pre-registered walk-forward test of history-conditioned reads of geopolitical shocks in the oil economy

**Joseph Delany** — Colby College, Department of History (Middle East focus)
Draft v0.1, 2026-09-02. Numbers from run `walk_20260902T182828Z`
(`data/walk_forward/summary.json`) unless a file is named. Every number in this
draft is traced in Appendix A to the file that produced it; none is typed from memory.
This draft will be re-issued when the next sealed run lands (Amendments B–D:
G-persistence baseline, walk-forward recalibration, run archive).

---

## Abstract

Analysts read a geopolitical shock by analogy: *this looks like 1990, or 2019, or
2022*. We ask whether that reading, made explicit and disciplined, has forecasting
value. We build a corpus of 313 dated geopolitical and policy shocks (1973–2026), a
world-state panel drawn from seventeen open academic and government datasets and
joined to each event under a vintage rule (the engine at date *t* sees only what was
knowable at *t*), and a state-conditioned analog engine that reads each event as a
frequency distribution over independently coded escalation outcomes (IES-90:
none / threat / force / war, from ICB, COW MID, COW War and UCDP) and over the
20-day Brent price path. We then forecast the past in sequence under a
pre-registered walk-forward protocol: reads are sealed by hash before the outcome
is looked up, scored with strictly proper rules, and compared to four baselines
under Diebold–Mariano, stationary-bootstrap, Reality-Check/SPA, label-permutation,
matched-placebo, regime-block and specification-curve tests. **The engine has no
skill beyond the base rate on either target** (escalation Brier skill −0.007,
95% CI [−0.084, +0.065], SPA *p* = 0.79; price CRPS skill −0.028, CI [−0.062,
+0.008]). It beats persistence on price (+0.163, *p* < 0.001) and is not reliably
better than random analogs. A label-permutation test nonetheless rejects the
hypothesis that the engine's analog selection is noise (*p* = 0.008): the Murphy
decomposition shows resolution on the *no-escalation* class and over-confidence
on the *force* and *war* classes, so what structure exists is destroyed by
miscalibration. Separately, a market-defined census of the largest Brent moves
since 1987 finds that 35% have no identifiable event in the corpus, that in half of
the attributed episodes every attributed event was knowable more than 20 trading
days before the move began, and that
geopolitical classes are *under*-represented inside big crude moves and
*over*-represented inside big diesel-crack moves. Two earlier positive headlines
(volatility-stress amplification; escalation skill +0.12 against self-coded
labels) did not survive, respectively, a matched placebo and independent labels;
both downgrades are in the record. We argue the null is informative: at the
horizons and sample sizes a human analyst actually works with, "history rhymes"
does not yet cash out as a calibrated forecast, and we state what would change
that verdict.

---

## 1. The question

A desk reading a geopolitical shock asks five things in order: is it priced, is the
narrative right, what is the tail, where does it travel, and how much should any of
this be trusted (`NORTH_STAR.md` §2). The second and third questions are answered,
in practice, by precedent. The claim that "history rhymes" is doing quantitative
work whenever an analyst says a strike on Abqaiq looks like 2019 and not like 1990.

This paper makes that claim testable. It asks: **given only what was knowable on
the day, does conditioning on the historical record produce a forecast of
escalation and of price that beats the base rate?** It answers with a
pre-registered, sealed, walk-forward test whose verdict is decided by a rule
written before any number was computed (`WALK_FORWARD_PROTOCOL.md` §7).

The contribution is threefold. First, a *market-defined* notion of significance:
instead of asking whether events we chose moved prices, we take the market's
largest moves and ask what was knowable while they happened (§4). Second, an
*independent* escalation outcome, after our own coded outcomes tested at chance
against three external datasets (§5). Third, the protocol itself, which we believe
is the strictest applied to an analog-forecasting system in this domain: hashes
before outcomes, four baselines, a leakage test that breaks the filtration to prove
it binds, and a verdict rule that the authors cannot override (§7).

## 2. Related work

Three literatures meet here. The **oil-shock literature** distinguishes supply,
aggregate-demand and precautionary-demand shocks (Kilian 2009; Baumeister &
Hamilton 2019) and identifies oil-supply news from dated announcements (Känzig
2021); it is about the macroeconomy's response to identified shocks, not about
forecasting the shocks' evolution. The **geopolitical-risk literature** builds
indices from news text (Caldara & Iacoviello 2022) and studies their asset-pricing
consequences; our world-state panel uses the GPR series as a feature and as a
placebo-matching variable. The **forecast-evaluation literature** supplies the
tools we register: strictly proper scoring rules (Brier 1950; Gneiting & Raftery
2007), the reliability–resolution decomposition (Murphy 1973), predictive-accuracy
tests with small-sample correction (Diebold & Mariano 1995; Harvey, Leybourne &
Newbold 1997), dependence-preserving resampling (Politis & Romano 1994), data-snooping
control across a model family (White 2000; Hansen 2005), false-discovery control
(Benjamini & Hochberg 1995), size-corrected scores for finite ensembles (Ferro
2014), online aggregation (Freund & Schapire 1997), and specification curves
(Simonsohn, Simmons & Nelson 2020). The prequential principle (Dawid 1984) — score
forecasts only against outcomes not yet seen — is the spine of the protocol.

The structured-analogy tradition in forecasting (Green & Armstrong 2007) and the
judgment literature (Tetlock & Gardner 2015) motivate the exercise: analysts use
analogs; the question is whether a disciplined machine version has skill. We know
of no prior work that tests analog reads of geopolitical shocks against
independently coded escalation outcomes under a sealed walk-forward protocol.

## 3. Data

**Event spine.** 313 events, 1973-10-06 to 2026-06-17, human-gated under a
codebook: sanctions 57, policy responses 57, conflict escalations 55, OPEC
decisions 52, infrastructure attacks 48, chokepoint disruptions 27, demand shocks
17 (`data/oil.db`, table `events`). 187 are geopolitical in the sense used for the
escalation target.

**This layer is the study's principal weakness, and we state its condition
precisely rather than in summary.** (i) *Provenance.* Each event carries a single
primary `source_url`; **0 of 313 record two independent sources**, so the
codebook's two-source admission rule is a standard for future admissions, not a
property of the present corpus. Per-field provenance is recorded in `sr_json`
under a sourced-or-unknown rule, but a substantial share of those field sources
are null or self-referential (`corpus:density`, `corpus:observed`), i.e. derived
from the corpus rather than from an external record. (ii) *Depth.* Event
descriptions have a median length of 148 characters — a sentence, not a case
narrative; some carry draft coding notes in the text. (iii) *Coverage.* The
distribution is heavily recent: 8 events in the 1970s, 11 in the 1980s, 16 in the
1990s, 43 in the 2000s, 85 in the 2010s, 150 in the 2020s. The "1973–2026 spine"
is in practice a dense 2010–2026 record with a thin historical tail, which is why
the 1990 read in Appendix B draws on seven precedents and the monthly tier cannot
be scored at all. (iv) *Selection.* Events were chosen by humans with hindsight;
the Big Moves census (§4) is the check on this and finds 35% of the largest Brent
moves have no corpus event at all.

Repair is registered and under way (`data/candidates/REGISTRATION.md`,
`DOSSIER_RULE.md`): 624 pre-1987 candidates drawn mechanically from ICB, COW MID,
COW War and UCDP are being turned into dossiers carrying two verified sources
each, with admission by the author alone. Until that lands, every result in this
paper should be read as conditional on a corpus whose historical arm is thin.

**Prices.** A daily spine from FRED (Brent from 1987-05-20, WTI from 1986-01-02,
products, cracks, gas), a monthly WTI spine from 1946 (FRED `WTISPLC`), and ~598
series in all.

**World-state panel.** Two layers (`WORLD_STATE_FRAMEWORK.md`): a panel with
vintage (`state_panel`) and a per-event dossier. Sources, each verified for
variables, coverage and licence in `WORLD_STATE_SOURCES.md`: ICB v16, COW NMC v7,
COW MID 5, COW War, ATOP 5.1, UCDP 26.1, CSP Polity5 / Coups / MEPV, V-Dem v16,
SIPRI, GPR and GPRH, EIA surplus capacity and NYMEX curves, Energy Institute
Statistical Review, Kilian's index of global real economic activity, UNGA ideal
points (Voeten), WDI, Archigos. Seventeen loaders populate 34 of 70 registered
fields (`data/state/status.json`); the remainder are listed as gaps with reasons.
**Vintage rule:** the engine at date *t* sees only rows whose vintage is ≤ *t*.
A registered limitation (protocol §1) is that the per-event situation fields
(`sr_*`) were not vintage-stamped in this run; Amendment A to the framework, now
registered, stamps them and drops any field with `knowable_at` > *t*.

**Outcomes.** §5.

## 4. Significance, defined by the market

Event studies choose the events. We invert this. A **Big Move** is a top-5% move
in the trailing 20- or 60-day window (daily tier) or the trailing 3- or 12-month
window (monthly tier); onset is the price extreme; the attribution window runs
from seven days before onset to the end of the move (31 days on the monthly tier);
an event whose date precedes onset by more than 20 days is marked ANTICIPATED
(`BIG_MOVES_REGISTRATION.md`, Amendments 1–3 dated and appended).

Results (`data/big_moves/*.json`):

| Asset | Episodes | No identified event | Attributed | …all events anticipated | …any event anticipated | Everyday base rate |
|---|---|---|---|---|---|---|
| Brent, daily, 1987– | 43 | 15 (35%) | 28 | 14 (50%) | 20 (71%) | 18.3% |
| WTI, daily, 1986– | 46 | 14 (30%) | 32 | 12 (38%) | 18 (56%) | 18.6% |
| Diesel crack, daily, 1986– | 36 | 7 (19%) | 29 | 7 (24%) | 23 (79%) | 16.8% |
| WTI, monthly, 1946– | 18 | 1 | — | — | — | 14.7% |

"Anticipated" is the registered flag for an attributed event whose date precedes
the move's onset by more than 20 trading days — i.e. the news was already public
when the market finally moved. Read with the first column, the picture is
uncomfortable for any event-driven reading of this market: on Brent, 15 of 43
largest moves have no event we can name, and in 14 of the 28 that do, every event
we can name was old news. Only 14 of 43 Brent episodes (33%) are moves where a
corpus event was both present and fresh; on WTI 20 of 46 (43%), on the diesel
crack 22 of 36 (61%). The product margin is the most event-driven series we
measure, and crude the least.

The everyday base rate is the share of days that fall inside any big-move window;
*P(big move | event class)* is compared to it as a ratio. On **Brent**, demand
shocks (1.61), OPEC decisions (1.61) and policy responses (1.85) sit inside big
moves more often than a random day, while infrastructure attacks (0.62),
sanctions (0.79) and chokepoint disruptions (0.84) sit inside them *less* often.
On the **diesel crack** every geopolitical class is over-represented: chokepoint
2.29, conflict 2.62, infrastructure 1.98, sanctions 2.06. Geopolitics moves
products more than it moves crude, on this record. Policy responses are endogenous
to big moves by construction and are excluded from the materiality gate
(`src/materiality.py`).

Two caveats are registered. The top-5% threshold is computed on full history, not
point-in-time (a look-ahead in the *definition* of significance, though not in any
forecast); and *n* per class is small (4–19 episodes), so ratios are reported with
their counts and no significance test is attached.

## 5. Outcomes: the label problem

The first version of this project coded each geopolitical event's outcome at
+90 days from its own corpus (CONTAINED / LIMITED_RETALIATION / WIDENING /
RESOLUTION_BY_DEAL). We tested those labels against three independent datasets
(`data/state/outcomes_kappa.json`; `OUTCOME_MAPPING.md`): Cohen's κ against ICB
was −0.001 (*n* = 43), against COW MID −0.234, against UCDP 0.104. Our labels were
at chance. Under the pre-stated rule (κ < 0.6 → the self-coded outcome is not a
target), `sr_outcome_90` was **retired** on 2026-09-02 (Amendment 1): not a target,
not a feature, not analog evidence.

Its replacement, **IES-90**, is computed — not coded by us — from dated records:
the maximum escalation level in (d, d+90] on the dyad, with 0 none / 1 threat or
display of force / 2 use of force / 3 war, plus a DEAL flag, from MID incidents and
disputes, UCDP GED and dyadic data, ICB crisis dates and COW war dates. Amendment 2
sets dyadic precedence and a chokepoint-to-littoral map used for location only.
Coverage: 184 of 187 geopolitical events labelled (98.4%); 3 have no independent
covering source and are never escalation evidence. Level counts: 0 → 76, 1 → 6,
2 → 48, 3 → 54; 95 carry a deal flag. A 30-event audit sheet
(`data/audits/ies90_audit_30.csv`) awaits the author's row-by-row check against
the source records; the protocol's verdict rule treats the audit as a gate, so no
verdict can rise above SUGGESTIVE until it is recorded.

## 6. The engine

The engine is deliberately simple. Each event at *t* has a state vector assembled
from the panel (vintage ≤ *t*) in five blocks — physical, market, actors, dyads,
system. Similarity is block-wise weighted distance (`src/engine/similarity.py`);
analogs are the *k* ≤ 12 prior events above a registered threshold (0.4). A read is
the analog outcome frequency distribution over IES-90 levels with *n* (Layer G),
the analog 20-day Brent path distribution (Layer P), a materiality flag from the
Big Moves gate (Layer M), propagation through the measured event×node reaction
table, and a then-vs-now differencing of the state vector. "No adequate precedent"
is a first-class answer and is charged the climatology loss when scored. Twelve
registered weightings (`data/walk_forward/menu.json`) form the model family; an
online Hedge mixture over them (η = 0.25) is the "engine", and the same mixture
with weights frozen at burn-in is the "frozen" baseline. The engine returns
frequencies with *n*, never probabilities of occurrence.

## 7. The walk-forward protocol

`WALK_FORWARD_PROTOCOL.md`, registered 2026-09-02 before the first run, with
Amendments A–D dated and appended after. Anchored expanding window; burn-in 8
events; each read is sealed by SHA-256 over its canonical payload and its
`sealed_at` timestamp precedes the outcome's `looked_up_at` (asserted per read;
`seal_check.ok = true`, 1,565 records). Scores: multi-category Brier (gate and
Hedge loss), log score, ranked probability score over the ordinal levels, binary
Brier for DEAL; CRPS, pinball at 10/50/90 and PIT for price. Baselines:
climatology (expanding base rate), persistence (price; escalation added by
Amendment B), random analogs (size-matched, 25 draws), frozen engine. Inference:
Diebold–Mariano with the HLN correction and HAC lag from the measured dependence
(cluster 35 days, mean block 2.32), stationary block bootstrap (2,000), White's
Reality Check and Hansen's SPA over the 14-model family (1,000), Benjamini–Hochberg
at *q* = 0.05 over all comparisons, label permutation within class (1,000),
VIX-matched placebo (5 replicates, 30-day exclusion), regime-block leave-out
(2008, 2020, 2026), a 162-cell specification curve (burn-in × *k* × horizon ×
cluster × big-move quantile), and a leakage test that deliberately breaks the
filtration and asserts the reads and scores change.

**Verdict rule (§7).** VALIDATED requires, in every tier where data permit
(*n* ≥ 30): skill > 0 vs climatology, DM *p* < 0.05 after HLN, SPA *p* < 0.05, skill
> 0 in all three regime blocks, a null placebo, label-permutation *p* < 0.05
(escalation), and the author's label audit recorded as passed. Anything else is
SUGGESTIVE; nulls are published as nulls. The word VALIDATED appears on no surface
of the software unless this rule produced it (acceptance check D6).

## 8. Results

Daily tier: 299 reads, 253 scored after burn-in (price), 150 with an escalation
label. The monthly tier has 14 reads and 0 scored beyond burn-in; it describes and
cannot validate (§11).

**Escalation (G), Brier vs climatology:** engine 0.706, climatology 0.701, skill
**−0.007**, 95% CI [−0.084, +0.065], DM *p* = 0.85. Log score skill −0.035
(CI [−0.112, +0.045]). Vs frozen: −0.003 (learning adds nothing). Vs random
analogs: +0.062, CI [−0.008, +0.130], *p* = 0.068. SPA over the family: best model
M07 (uniform, *k* = 12), *p*_RC = 0.88, *p*_SPA = 0.79. DEAL (binary, *n* = 66,
base rate 6%): −0.218, CI covers zero. Per class, none significant (chokepoint
+0.017, conflict −0.065, infrastructure +0.018, sanctions +0.019).

**Ranked probability score** (published, not a gate): vs climatology +0.072,
CI [−0.008, +0.151], *p* = 0.076; vs random analogs +0.140, CI [+0.061, +0.219],
*p* < 0.001. Ordering information is present; the registered multi-category Brier
does not reward it.

**Price (P), CRPS vs climatology:** skill **−0.028**, CI [−0.062, +0.008],
*p* = 0.14. Vs persistence: **+0.163**, CI [+0.121, +0.210], *p* < 0.001 — the
only comparison that survives FDR at *q* = 0.05 for the engine. Vs random analogs
+0.035 (*p* = 0.053); vs frozen +0.001. Pinball: 10th percentile −0.039, median
+0.004, 90th percentile −0.073 (CI [−0.149, −0.017]) — the upper tail is too wide.
PIT: engine χ² = 16.9 on 9 df (first bin 41 vs 25.3 expected), climatology 13.3.
Sign accuracy 0.498. SPA *p* = 0.94.

**Materiality (M):** engine precision 0.337, recall 0.544, base rate 0.225
(*n* = 253); identical for the frozen mixture.

**Verdict as computed:** `engine:G` SUGGESTIVE / null; `engine:P` SUGGESTIVE /
null; no menu item reaches VALIDATED.

## 9. Robustness

**Regime blocks.** Dropping 2008 (9 reads): G −0.013, P −0.028. Dropping 2020 (19
reads): G −0.014, P −0.011. Dropping 2026 (3 reads): G −0.007, P −0.027. Nothing
turns positive.

**Specification curve.** 162 registered settings: skill median −0.023, IQR
[−0.041, −0.007], max +0.015, share positive 16.7%. The null is not a choice of
settings.

**Placebo — unresolved, and we do not claim it as passed.** VIX-matched
pseudo-events (411 reads, 5 replicates). Against the size-matched random-analog
reference the placebo skill is −0.024, CI [−0.053, +0.007], covering zero; against
climatology it is −0.081, CI [−0.112, −0.048], not covering zero; the Ferro
size-corrected version is −0.008, covering zero. Which of these is *the* placebo
test is not settled: the registered protocol §6 requires placebo skill
indistinguishable from zero without naming a reference, and every other skill
number in this paper uses climatology; the size-matched reference is defined only
in a proposed amendment that the author has not ratified, and part of that
amendment's text describes code written before it. We therefore record the placebo
condition as **UNRESOLVED** and let no conclusion rest on it. Our reading of the
three numbers is that the climatology-referenced result reflects the finite-*k*
score bias of §11 (the size-corrected version covers zero) rather than a signal in
matched non-events — but that is an argument, not a registered test, and it is the
author's call to ratify, amend or withdraw. Raised in `docs/red_team_2.md`
finding 1; this paragraph replaces a prior version that read "the placebo is null,
as required".

**Label permutation.** With labels shuffled within class and Hedge replayed under
the closed-by-*t* rule, the null distribution of skill has mean −0.061, SD 0.025,
95th percentile −0.018; the observed +0.0005 has *p* = 0.008. The engine's analog
selection carries information about the labels.

**Multiplicity.** 32 comparisons under BH at *q* = 0.05: the engine survives only
vs persistence on price. Two menu items survive on price vs climatology (M02
situation-only *q* = 0.024; M06 *k* = 5 *q* < 0.001); neither is the registered
engine, neither passes SPA, and we report them as what a specification search
would have found.

**Leakage.** Breaking the filtration changes 313 reads' analogs and moves the
sealed G score from 0.706 to 0.619 and P from 7.92 to 8.04; the test asserts the
difference. The filtration binds.

**Learning curve.** Cumulative Brier skill vs climatology is negative through
2020, first turns positive on 2021-03-07, drifts between −0.01 and +0.04 through
2022–2023 and ends at −0.007 at *n* = 150 (`figures/learning_curve.png`; the
cumulative RPS skill follows the same path and ends at +0.072). The frozen mixture
tracks the online engine within 0.007 at every point, so whatever movement there is
comes from the sample, not from Hedge learning.

## 10. Why the permutation test rejects while skill is null

The two results are not in tension; the Murphy decomposition says why. For the
*no-escalation* class the engine has resolution 0.038 against the climatology's
0.0004 with reliability 0.002 — it sorts the quiet cases. For *force* and *war* its
reliability terms are 0.042 and 0.035: in the 0.4–1.0 forecast bins it observes
0–36% frequencies (reliability diagrams, `figures/reliability_daily.png`). The
engine knows something about which situations stay quiet and is over-confident
about which ones burn. Miscalibration of that size is enough to erase the
resolution in a Brier score, while a permutation test — which only asks whether
the analog assignment is exchangeable with a random one — still rejects.

This is a testable diagnosis. Amendment C registers M13, the same mixture with
walk-forward recalibration (per-class isotonic regression, Platt below *n* = 40,
identity until 40 closed reads, fitted only on reads whose outcomes were looked up
before *t*). If the diagnosis is right, M13's Brier skill will be positive and its
reliability terms near zero; if it is wrong, M13 will not move. The result will be
published either way in the next issue of this draft.

## 11. Limitations

1. **Sample size and power.** 150 labelled escalation reads and 253 price reads.
   The bootstrap CI on escalation skill spans ±0.07; a true skill of +0.05 would
   not be detected. The monthly tier (14 reads) cannot validate at all until the
   pre-1987 corpus is admitted (624 candidate records 1946–1986 are on the
   author's admission sheet, `data/candidates/pre1987_candidates.csv`).
2. **Score bias against finite analog sets.** The registered Brier and CRPS charge
   a *k*-atom distribution an extra Σ *p_b*(1−*p_b*)/*k* and E|X−X′|/(2*k*)
   respectively, so a genuinely null engine reads *negative* against climatology.
   Ferro's (2014) size-corrected scores are published beside every registered one
   (fair Brier skill +0.057, CI [−0.019, +0.129]; fair CRPS +0.027, CI [−0.009,
   +0.078]; fair RPS +0.139, CI [+0.058, +0.222]). Gates use the registered scores
   unchanged; the decision whether to register the fair scores prospectively for
   v3 is the author's and is not made retroactively.
3. **Labels.** IES-90's UCDP-GED component is location-based (deaths in the
   country, not between the actors); this is stated on every affected row. The
   30-event audit is pending.
4. **Vintage.** The situation fields were taken as coded in this run (protocol §1);
   Amendment A stamps them and will drop most of them at *t* under the current
   coding. The next run will report the count.
5. **Corpus selection.** Events were chosen by humans with hindsight of which
   episodes mattered; the Big Moves census exists precisely to expose this, and
   finds 35% of big Brent moves have no corpus event.
6. **Big Moves look-ahead.** The top-5% threshold uses full history.
7. **"Ripple".** The propagation layer is a descriptive event×node reaction table;
   measured impulse responses with lags (local projections on the event dates) are
   registered as the next build (`RIPPLE_REGISTRATION.md`, forthcoming) and are not
   claimed here.

## 12. What would change the verdict

VALIDATED requires all of: positive registered skill with DM and SPA *p* < 0.05 on
both tiers where *n* ≥ 30; skill > 0 in all three regime blocks; a null placebo;
permutation *p* < 0.05; and the recorded label audit. On the present record the
permutation and placebo conditions are met and every skill condition fails. The
nearest path is the calibration hypothesis of §10 (M13) plus the sample-size
relief of a completed pre-1987 corpus; both are registered and neither is
guaranteed. A null that survives them would be, in our view, the more interesting
result: it would say that at 20-day and 90-day horizons the record does not rhyme
loudly enough to hear above the base rate.

## 13. The integrity record

Pre-registration files with git timestamps (`BRIEF_SKELETON.md`,
`PRE_REGISTRATION_V2.md`, `BIG_MOVES_REGISTRATION.md`,
`CLAIM_LEDGER_REGISTRATION.md`, `OUTCOME_MAPPING.md`, `WALK_FORWARD_PROTOCOL.md`),
every amendment dated and appended. An external adversarial review
(`docs/red_team_1.md`) whose attacks were conceded and answered by computation:
the original headline (H1, stress amplification of +5.56pp) reproduced exactly and
then fell inside a VIX-matched pseudo-event band; every previously "validated"
claim was downgraded to SUGGESTIVE under one retroactive bar. A second headline
(escalation skill +0.12, *p* < 0.001) was scored against self-coded labels and did
not survive independent ones. Both downgrades were published before any
recomputation. Nothing enters the corpus without a human; licence-restricted panels
are held locally and never committed; no field is fabricated — every value is
sourced or "unknown". 322 tests; `python3 src/acceptance_v2.py --dod` prints the
definition-of-done with evidence paths.

---

## References

Baumeister, C., & Hamilton, J. D. (2019). Structural interpretation of vector
autoregressions with incomplete identification: Revisiting the role of oil supply
and demand shocks. *American Economic Review*, 109(5), 1873–1910.

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate.
*Journal of the Royal Statistical Society B*, 57(1), 289–300.

Brecher, M., & Wilkenfeld, J. *International Crisis Behavior Project*, v16.

Brier, G. W. (1950). Verification of forecasts expressed in terms of probability.
*Monthly Weather Review*, 78(1), 1–3.

Caldara, D., & Iacoviello, M. (2022). Measuring geopolitical risk. *American
Economic Review*, 112(4), 1194–1225.

Dawid, A. P. (1984). Present position and potential developments: Some personal
views. Statistical theory: The prequential approach. *Journal of the Royal
Statistical Society A*, 147(2), 278–292.

Diebold, F. X., & Mariano, R. S. (1995). Comparing predictive accuracy. *Journal of
Business & Economic Statistics*, 13(3), 253–263.

Ferro, C. A. T. (2014). Fair scores for ensemble forecasts. *Quarterly Journal of
the Royal Meteorological Society*, 140(683), 1917–1923.

Freund, Y., & Schapire, R. E. (1997). A decision-theoretic generalization of
on-line learning and an application to boosting. *Journal of Computer and System
Sciences*, 55(1), 119–139.

Gneiting, T., & Raftery, A. E. (2007). Strictly proper scoring rules, prediction,
and estimation. *Journal of the American Statistical Association*, 102(477),
359–378.

Green, K. C., & Armstrong, J. S. (2007). Structured analogies for forecasting.
*International Journal of Forecasting*, 23(3), 365–376.

Hansen, P. R. (2005). A test for superior predictive ability. *Journal of Business
& Economic Statistics*, 23(4), 365–380.

Harvey, D., Leybourne, S., & Newbold, P. (1997). Testing the equality of prediction
mean squared errors. *International Journal of Forecasting*, 13(2), 281–291.

Känzig, D. R. (2021). The macroeconomic effects of oil supply news: Evidence from
OPEC announcements. *American Economic Review*, 111(4), 1092–1125.

Kilian, L. (2009). Not all oil price shocks are alike: Disentangling demand and
supply shocks in the crude oil market. *American Economic Review*, 99(3),
1053–1069.

Murphy, A. H. (1973). A new vector partition of the probability score. *Journal of
Applied Meteorology*, 12(4), 595–600.

Palmer, G., et al. (2022). The MID5 dataset, 2011–2014. *Conflict Management and
Peace Science*, 39(4), 470–482.

Politis, D. N., & Romano, J. P. (1994). The stationary bootstrap. *Journal of the
American Statistical Association*, 89(428), 1303–1313.

Simonsohn, U., Simmons, J. P., & Nelson, L. D. (2020). Specification curve
analysis. *Nature Human Behaviour*, 4, 1208–1214.

Tetlock, P. E., & Gardner, D. (2015). *Superforecasting: The Art and Science of
Prediction*. Crown.

White, H. (2000). A reality check for data snooping. *Econometrica*, 68(5),
1097–1126.

Datasets: Correlates of War (NMC v7, MID 5, War); ATOP 5.1; UCDP 26.1 (GED and
dyadic); Center for Systemic Peace (Polity5, Coups, MEPV); V-Dem v16; SIPRI; GPR
(Caldara & Iacoviello); EIA; Energy Institute Statistical Review; Kilian index;
Voeten UNGA ideal points; World Bank WDI; Archigos; FRED. Verified register:
`WORLD_STATE_SOURCES.md`.

---

## Appendix A — provenance of every number in this draft

| Number | Path in `data/walk_forward/summary.json` unless noted |
|---|---|
| 313 events; class counts; 1973-10-06 … 2026-06-17 | `oil.db` `events` |
| 187 geo; 184 labelled; 3 uncovered; level counts 76/6/48/54; 95 deal | `data_state` |
| 34 of 70 fields; 17 loaders | `data/state/status.json`; `data/acceptance_dod.json` D2 |
| κ −0.001 / −0.234 / 0.104 | `data/state/outcomes_kappa.json` |
| Big Moves table and ratios | `data/big_moves/{brent,wti,diesel_crack,wti_monthly}.json` |
| 299 / 253 / 150 reads; cluster 35, mean block 2.32 | `tiers.daily.{n_reads,n_scored_burn_in,dependence}`; `tiers.daily.G.engine_vs.climatology.n` |
| G Brier −0.007 [−0.084, +0.065] p 0.85 | `tiers.daily.G.engine_vs.climatology` |
| G log −0.035 | `tiers.daily.G.log_score_vs_climatology` |
| G vs frozen −0.003; vs random +0.062 p 0.068 | `tiers.daily.G.engine_vs.{frozen,random_analogs}` |
| SPA: M07, p_RC 0.88, p_SPA 0.79 | `tiers.daily.G.spa` |
| DEAL −0.218, n 66, base 0.061 | `tiers.daily.G.deal` |
| Per-class skills | `tiers.daily.G.per_class` |
| RPS +0.072 p 0.076; vs random +0.140 p < 0.001 | `tiers.daily.G.rps.engine_vs` |
| P CRPS −0.028 [−0.062, +0.008] p 0.14; persistence +0.163; random +0.035; frozen +0.001 | `tiers.daily.P.engine_vs` |
| Pinball 10/50/90; PIT counts and χ²; sign 0.498; P SPA 0.94 | `tiers.daily.P.{pin*,pit_*,sign_accuracy_engine,spa}` |
| M precision 0.337 recall 0.544 base 0.225 | `tiers.daily.M.engine` |
| Regime blocks | `regime_blocks` |
| Spec curve 162; median −0.023; 16.7% positive | `spec_curve.skill_distribution` |
| Placebo −0.024 [−0.053, +0.007]; −0.081; fair −0.008 | `placebo.{vs_random_analogs,vs_climatology,fair_vs_climatology}` |
| Permutation: mean −0.061, SD 0.025, p95 −0.018, p 0.008 | `permutation` |
| FDR survivors | `fdr.family` |
| Leakage: 313 reads; 0.706→0.619; 7.92→8.04 | `leakage_test` |
| Seal: ok, 1,565 records | `seal_check` |
| Murphy terms | `tiers.daily.G.murphy_engine`, `murphy_climatology` |
| Fair scores | `tiers.daily.G.diagnostic_fair`, `tiers.daily.P.diagnostic_fair` |
| Monthly 14 / 0 / min 30 | `tiers.monthly` |
| Verdict statuses | `verdict.rules` |
| H1 +5.56pp; placebo band; downgrade | `docs/red_team_1.md` Part 2 |
| 624 candidates | `data/candidates/pre1987_candidates.csv` (rows − header) |
| 322 tests | `data/acceptance_dod.json` D1 |
