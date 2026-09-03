# Does the record predict? A pre-registered walk-forward test of history-conditioned reads of geopolitical shocks in the oil economy

**Joseph Delany** — Colby College, Department of History (Middle East focus)
Draft v1.0, 2026-09-03. Numbers from run `walk_20260903T003422Z`
(`data/walk_forward/summary.json`) unless a file is named. Every number in this
draft is traced in Appendix A to the file that produced it; none is typed from memory.

This is the final version of the day's work. It supersedes v0.3 (run 210135Z), v0.2
(193022Z) and v0.1 (182828Z); every superseded number survives in git history and in
`data/handoffs/B_run_delta.md`, none is deleted. Four runs, each stricter than the
last, each published as computed — that sequence is itself the result.

The decisive change was Amendment H, which enforced the vintage rule on the per-event
situation fields and moved the headline from *parity with the base rate* to
*significantly worse than the base rate* (§8). The run reported here re-ran everything
on a corpus whose sourcing had since been repaired — 66 field changes across nineteen
pre-1990 records and the 1990s pass — and **not one forecast number moved**. The
content digest is identical for the third independent run. That is a negative control
worth stating: the results were never resting on the weak citations the repair fixed,
because the repair touched only provenance columns the engine does not read (verified
by diffing the live corpus against the sealed reads: zero date changes, zero type
changes, zero label changes; `data/gates/negative_control_spine_2026-09-03.md`).

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
matched-placebo, regime-block and specification-curve tests.

**The engine is significantly *worse* than the base rate on both targets**
(escalation Brier skill −0.097, 95% CI [−0.180, −0.018], DM *p* = 0.022; price
CRPS skill −0.071, CI [−0.136, −0.017], *p* = 0.016), and the reason is the
central finding of this study. Earlier runs of the same code showed parity with
climatology (−0.005 and −0.030). Those runs took the per-event situation fields as
coded rather than as knowable: the codings existed, but their dates did not
establish that an analyst could have had them on the day. When the vintage rule is
enforced on those fields as well — a registered amendment, applied after the
earlier numbers were published — **262 of 313 events turn out to have no situation
field knowable at *t***, retrieval falls back to the market block alone, and the
engine's apparent parity disappears. The state conditioning that gave the engine
its edge was, to a first approximation, hindsight.

Three further results are consistent with that. A naive persistence rule — the
dyad's own maximum escalation level over the preceding 90 days — beats the engine
decisively (Brier 0.480 vs 0.769; skill −0.600, *p* = 0.0002). A registered
walk-forward recalibration, which we had predicted in writing would rescue the
engine by fixing miscalibration, instead made it worse (−0.700, *p* < 0.001): that
hypothesis is **falsified**. And a label-permutation test that had rejected "the
engine is noise" at *p* = 0.002 before the vintage amendment no longer rejects
(*p* = 0.124): the structure it had detected was in the retrospective codings, not
in the retrieval. The specification curve is negative in **all 162** registered
settings. The engine's one surviving win is against persistence on price (+0.129,
*p* < 0.001). A companion propagation study, registered and placebo-controlled, finds
the same silence on the transmission side: across 477 node×shock cells only 21
transmit, against 1–24 expected under no transmission at all, with **zero of 99** at
the gas/LNG and fertilizer hops — while the same estimator recovers Känzig's (2021)
published oil-supply-news shock cleanly at every horizon, so the nulls are not an
instrument failure (§11). Separately, a market-defined census of the largest Brent moves
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

**This layer was the study's principal weakness, it was measured rather than
described, and it was repaired in part on the same day.** We report both states,
because the repair is itself evidence about what a historical corpus of this kind
can and cannot be made to carry.

*As the published runs saw it* (`data/spine/AUDIT.md`, first commit): each event
carried a single primary `source_url` and **0 of 313 recorded two independent
source domains**, so the codebook's own two-source admission rule was a standard
the corpus had never met. Of the field-source slots in `sr_json`, 11.9% carried an
external URL, 25.0% were corpus-derived and therefore could not corroborate the
corpus, and 63.1% were null. Descriptions had a median length of 148 characters —
a sentence, not a case narrative — and 49 still carried drafting scaffolding.
Thirty-one records cited an encyclopaedia as their only source, which the
codebook's inclusion rule does not admit. Coverage was heavily recent: 8 events in
the 1970s, 11 in the 1980s, 16 in the 1990s, against 43, 85 and 150 in the decades
after. The "1973–2026 spine" was in practice a dense 2010–2026 record with a thin
historical tail — which is why the 1990 read in Appendix B draws on seven
precedents and the monthly tier cannot be scored at all.

*After the pre-2000 repair* (four dossier patches, 66 field changes, each applied
in one transaction on the author's line): **22 of 313 events now carry two
independent source domains** — 7 of 8 in the 1970s, 5 of 11 in the 1980s, 10 of 16
in the 1990s. Bare site-root citations fell from 9 to 3, encyclopaedia-only from 31
to 28, drafting scaffolding from 49 to 39. Every pre-2000 record now has a dossier
citing primary documents: FRUS minutes of the Washington Special Actions Group of
17 and 19 October 1973, a CIA Office of Economic Research memorandum of 19 October
1973, Brzezinski's memorandum of 4 November 1979 written the day the Tehran embassy
was seized, Executive Order 12170, Reagan's report to Congress on Operation Praying
Mantis, and the UNIIMOG mission history among them.

*What could not be repaired, and why* — three distinct reasons, each measured:

1. **Declassification.** Four records cannot reach a primary source because the
   volumes are unpublished: FRUS 1969–76 Volume X (Iran 1977–79) and the
   Reagan-era Gulf volumes XX and XXI are marked "Being Cleared". The
   declassification queue, not our effort, is the binding constraint on that decade.
2. **Archive reach.** Twenty-eight records still have no citable domain, all
   post-2000. Eight primary-document routes were probed live; **zero of 27
   post-2000 encyclopaedia-only records could be replaced by a primary document
   through any of them** (`data/spine/archive_reach_2026-09-02.md`). Between 2000
   and 2016 no free route reaches: the State Department volumes have ended, UK
   files are not yet open under the twenty-year rule, the free press index begins
   in 2017, and the Federal Register covers only US federal action. That window is
   the entire gap.
3. **Genuine absence.** The June 1998 OPEC production cut defeated roughly twenty
   documented routes individually; its dossier recommends leaving the source field
   unset rather than retaining an encyclopaedia citation.

The corpus the published runs used is the *before* state. Every result in this
paper is conditional on it, and the repair — which post-dates the runs — is
reported here so that a reader can see both what was wrong and how much of it
proved fixable.

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
`seal_check.ok = true`, 313 records for the run in the tree; earlier runs are
archived under Amendment D and re-verified there). Scores: multi-category Brier (gate and
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
cannot validate (§12).

**The vintage amendment, and what it did.** This run is the first in which the
per-event situation fields are filtered by their own `knowable_at` (Amendment H;
registered before the code, `WORLD_STATE_FRAMEWORK.md` Amendment A). Under that
rule **262 of 313 events have no situation field knowable at *t*** — the codings
exist, but nothing establishes an analyst could have held them on the day — so
retrieval for those events runs on the market block alone. Everything below is
after that filter. The same code on the same corpus, one run earlier, produced
escalation skill −0.005 and price −0.030 (`data/handoffs/B_run_delta.md`, run
210135Z). The
difference between those two runs is the difference between conditioning on the
world as recorded and conditioning on the world as knowable.

**Escalation (G), Brier vs climatology:** engine 0.769, climatology 0.701, skill
**−0.097**, 95% CI [−0.180, −0.018], DM *p* = 0.022 — the engine is significantly
*worse* than the base rate, and this comparison survives Benjamini–Hochberg. Vs
random analogs: −0.021 (*p* = 0.58) — indistinguishable from drawing analogs at
random. Vs frozen: +0.007 (*p* = 0.029), i.e. Hedge learning is marginally *worse*
than freezing the weights. SPA over the 15-model family: *p*_RC = 1.00,
*p*_SPA = 0.65; no member of the family beats climatology.

**Escalation persists, and the engine does not exploit it.** The registered fourth
baseline (Amendment B) is G-persistence: a Laplace-smoothed point mass on the
dyad's own maximum IES level over the preceding 90 days, from the same independent
sources under the same vintage rule, falling back to climatology where no dyad
level is knowable (2 of 150 reads). It scores **0.480** against the engine's 0.769
— skill −0.600, CI [−1.031, −0.230], DM *p* = 0.0002, surviving FDR; on the ranked
probability score −0.791 (*p* < 0.001). Escalation is strongly autocorrelated at 90
days, and averaging over state-similar analogs from other dyads destroys that
information. A forecaster who knew nothing but the dyad's own recent history would
have beaten this engine decisively.

**Ranked probability score** (published, not a gate): vs climatology −0.013
(*p* = 0.77), vs random analogs +0.062 (*p* = 0.14), vs persistence −0.791. The
ordering advantage over random analogs that v0.2 reported (+0.144, *p* < 0.001)
does not survive the vintage rule either.

**Price (P), CRPS vs climatology:** skill **−0.071**, CI [−0.136, −0.017],
*p* = 0.016 — also significantly worse than the base rate, also surviving FDR. Vs
random analogs −0.005 (*p* = 0.85). Vs frozen +0.007 (*p* < 0.001). Vs persistence
**+0.129**, CI [+0.070, +0.185], *p* < 0.001 — the engine's one surviving win, and
the one result that has held its sign across all three runs.

**Materiality (M):** precision 0.337, recall 0.544 against a base rate of 0.225
(*n* = 253).

**Verdict as computed:** `engine:G` and `engine:P` both SUGGESTIVE / null under
protocol §7 — the rule cannot return anything stronger, and on this run the failure
is not "no better than" but "significantly worse than" the base rate. We report
that distinction rather than hide behind the shared label.

## 9. Robustness

**Regime blocks.** Dropping 2008: G −0.108, P −0.071. Dropping 2020: G −0.099,
P −0.081. Dropping 2026: G −0.097, P −0.071. The negative result is not one crisis.

**Specification curve.** 162 registered settings (burn-in × *k* × horizon ×
cluster × big-move quantile): skill min −0.150, median −0.075, max −0.041,
**share positive 0.0**. Not one of the 162 defensible ways of running this test
produces a positive escalation skill. In v0.2, before the vintage amendment, 22%
were positive.

**Power (simulated from the sealed score series under the measured block
dependence, 400 replications).** Minimum detectable skill at 80% power is 0.127 on
escalation (*n* = 150) and 0.085 on price (*n* = 253); detecting +0.05 on either
would need roughly 1,200 scored reads. This cuts both ways and we state both: the
study could not have detected a small positive edge, and the significantly negative
results reported above are larger than that detection floor.

**Placebo.** VIX-matched pseudo-events, 5 replicates: against the size-matched
random-analog reference the placebo skill is −0.047, CI [−0.083, −0.008], which
does *not* cover zero; against climatology −0.106, CI [−0.142, −0.063]; the Ferro
size-corrected version is +0.017, CI covering zero. In v0.2 the size-matched
placebo covered zero and we recorded the condition as unresolved pending the
author's ratification of the reference (`docs/red_team_2.md` finding 1). It now
fails under two of three references, so the condition is not merely unresolved but
unmet on the registered reading, and no verdict may lean on it. The engine loses to
matched non-events as well as to real ones — consistent with an engine whose
retrieval, stripped of retrospective state, is worse than not retrieving at all.

**Label permutation.** With labels shuffled within class and Hedge and M13 replayed
under the closed-by-*t* rule, the null distribution of skill has mean −0.101,
SD 0.029, 95th percentile −0.053; the observed −0.066 gives block *p* = 0.124
(i.i.d. *p* = 0.092). **The test no longer rejects.** In v0.2 it rejected at
*p* = 0.002 with an observed +0.013, and we wrote there that "the engine finds
structure in the labels but not enough to forecast with". That sentence is
withdrawn: the structure it was detecting lived in situation fields coded after
the fact, and it does not survive the point-in-time rule.

**Multiplicity.** 34 comparisons under BH at *q* = 0.05; 31 survive — but almost
all of them are the engine and its menu items *losing* to climatology or to
persistence. The engine's only surviving win is price against persistence. This is
the mirror image of a data-snooping problem: the family is overwhelmingly
significant in the wrong direction.

**Leakage and filtration.** The registered leakage test breaks the filtration and
confirms the reads and scores change (G 0.769 → 0.638). Beyond it, this run adds a
standing filtration audit over every read: 15,784 checks across analog dates,
market values, persistence windows and both outcome windows, **0 violations**. An
earlier firing of that audit (run 200654Z) was investigated and found to be a
conservative path rather than a leak — session A's panel bridge supplies a market
value dated 4–7 days *before* the event — and that run remains sealed and archived,
marked VOID as computed rather than deleted.

**Determinism.** Two independent full runs reproduce the same content digest
(`2a90ff4a…`) with every seed registered; `make reproduce` rebuilds from seeds and
`tests/test_reproduce.py` asserts the hashes match.

**Learning curve.** The frozen mixture beats the online engine on both targets
(+0.007 each, *p* = 0.029 and *p* < 0.001). Hedge learning over the registered
menu does not merely fail to help; it costs.

## 10. Two registered hypotheses, both falsified

This project has now put two written explanations of its own null to the test and
lost both. We report them together because the pattern matters more than either.

**Hypothesis 1: miscalibration is hiding real resolution.** In v0.1 the Murphy
decomposition showed the engine sorting the quiet cases (resolution 0.033 on the
*no-escalation* class against climatology's 0.0004) while being over-confident on
*force* and *war* (reliability 0.042 and 0.034). We predicted in writing that
fixing the calibration would surface the resolution, and registered M13 — the same
mixture with walk-forward recalibration, per-class isotonic by pool-adjacent-
violators, Platt below *n* = 40, identity until 40 closed reads, fitted only on
reads whose outcomes were looked up before *t*. **Falsified.** On the v0.2 run M13
scored −0.590 against climatology; on this run −0.700, CI [−0.940, −0.457],
*p* < 0.001, with reliability terms *higher* than the engine's. Recalibrating on a
few dozen closed observations across four classes — one of which, *threat*, has six
events in the entire labelled sample — injects far more estimation noise than the
miscalibration it removes.

**Hypothesis 2: the permutation test proves the retrieval finds something real.**
In v0.2 we wrote that the engine "finds structure in the labels but not enough to
forecast with", on the strength of a label-permutation *p* of 0.002. **Falsified by
Amendment H.** Once the situation fields are filtered to what was knowable at *t*,
the same test gives *p* = 0.124 and the observed skill is −0.066. The structure was
in the retrospective codings.

What survives both falsifications is the diagnosis that replaced them, and it is
simpler than either: with 262 of 313 events carrying no knowable situation field,
this engine spends most of its reads retrieving on the market block alone, which
is a worse conditioning set than the unconditional base rate. The failure is not
in the scoring, the calibration, or the learning rule. It is that the state vector
the design depends on did not exist, in knowable form, for most of the record.

That is a finding about historical data availability, not about the market. It is
also the finding that the vintage rule was written to be able to catch, and the
reason it was registered before any number was computed.

## 11. The propagation study, in brief

The engine's second claim is not about forecasting at all: that a shock arriving at
crude *travels* — into refined products, cracks, gas and LNG, fertilizer, freight and
credit. That claim was, until this version, supported only by a descriptive table of
event-window reactions. It has now been tested properly and is reported in full in
`docs/RIPPLE_FINDINGS.md`; the result belongs here because it bears on the same
question.

**Design,** registered at 15:42:38 with the estimator's first line committed at
15:59:32 (`RIPPLE_REGISTRATION.md`): local projections (Jordà 2005) of each chain node
on the corpus event dates as identified shocks, horizons 0–60 trading days, HAC and
stationary-bootstrap bands, de-overlapped shocks under a 35-day chain rule, and a
placebo of 500 draws matched on the volatility and geopolitical-risk state. A cell is
TRANSMITTING only if its 95% band excludes zero, its coefficient falls outside the
central 95% of the matched placebo, and the Newey–West band agrees.

**Result. Across 477 node×shock cells, 21 transmit, 401 are null and 55 are
insufficient — where between 1 and 24 cells would transmit if nothing transmitted
anywhere.** The observed count sits inside its own null interval. The registered
expectation, that some tightening class beats the matched placebo at Brent, fails.

The shape is more informative than the tally. Transmitting cells sit at the two *ends*
— crude itself (4 of 36) and the equity and macro nodes beside the chain (13 of 171) —
and vanish along it: **zero of 99 cells transmit at the gas/LNG and fertilizer hops**,
four and five steps down. Pass-through ratios cannot be computed at all, because the
denominator is null: Brent's own response at the headline horizon covers zero, so every
hop-to-hop ratio is a number divided by something indistinguishable from zero, and the
delta-method intervals say so ([−196.7, +220.1] for heating oil on the pooled shock).

**This is not the machinery failing to see an effect.** The same code, on Känzig's
(2021) published daily oil-supply-news surprise over 128 OPEC announcement days,
recovers his result cleanly — β on Brent of +0.85 at h = 0 rising to +2.37 at h = 20,
every horizon excluding zero, with his sign, shape and persistence. The estimator finds
an identified shock when one is there.

**And five of six prior "validated" edges were retracted.** The stress-amplification
edges inherited from the first version of this project (geopolitical shock under
elevated VIX → node, +20 days) were re-tested under a re-test registered before it ran.
Brent, heating oil, 5Y breakeven, S&P 500 and platinum all returned NULL with bands
covering zero by wide margins; only palladium survived, which is not on the oil chain
and is what one survivor in six looks like at this base rate. The retraction is in
`data/ripple/retraction_six.json` and the five rows are flipped in the database.

Taken with §8, the two halves of this project now say the same thing in different
languages: conditioning on the historical record does not forecast escalation or price
better than the base rate, and geopolitical shocks do not measurably propagate down the
petroleum chain beyond crude itself at these horizons and sample sizes.

## 12. Limitations

1. **Sample size, and the size of the gap.** 150 labelled escalation reads and 253
   price reads. Simulation under the measured block dependence puts the minimum
   detectable skill at 80% power at 0.127 (escalation) and 0.085 (price); detecting
   +0.05 on either would take roughly **1,200 scored reads — about eight times the
   present corpus**. This study can therefore report that the engine is
   significantly worse than the base rate, and cannot rule out a small positive
   edge that a much larger record would reveal.
2. **The state vector is mostly missing at read time.** 262 of 313 events have no
   situation field knowable at *t* (§8). The design's premise — condition on the
   world as it stood — is only partly exercised by the data available to exercise it.
   This is the study's largest internal threat and its clearest finding at once.
3. **The escalation target is asked of events to which it does not apply.** An
   independent audit of all 187 events in the four geopolitical classes, coded under a
   hostility rule registered before any count was taken (`data/spine/CLASS_AUDIT.md`;
   `OUTCOME_MAPPING.md` Amendments 3, 3.1, 3.2), finds **33 (18%) are not G-scorable**:
   20 non-hostile, 13 ambiguous. Among the scored reads the figure is **27 of 150
   (18%)**. The failures are not marginal — an ICC arbitration award and a labour
   strike carry *use of force* and *war* respectively, off location-matched deaths with
   no adversary; eight Chilean and Peruvian mining strikes sit in `conflict_escalation`;
   a DRC cobalt suspension carries level 3. Because climatology is estimated from this
   distribution, the affected reads move the base rate the engine is scored *against*,
   not merely its own score: the level-0 share falls from 42.0% to 36.8% excluding the
   non-hostile reads and to 32.5% excluding the ambiguous as well. A diagnostic on the
   G-scorable subset is published beside the registered figures; the registered figures
   themselves are not re-scored, because the reads are sealed and the rule post-dates
   them. Ambiguous rows are left ambiguous under the sourced-or-unknown rule rather
   than adjudicated to tidy the table.
4. **Score bias against finite analog sets.** The registered Brier and CRPS charge a
   *k*-atom distribution an extra Σ*p_b*(1−*p_b*)/*k* and E|X−X′|/(2*k*); Ferro's
   size-corrected scores are published beside every registered one (fair Brier skill
   +0.021, fair RPS +0.119). Gates use the registered scores unchanged; whether to
   register the corrected scores prospectively for v3 is the author's decision and
   is not made retroactively.
5. **The corpus.** §3 documents it: one source per event, none with two independent
   ones, 31 records citing an encyclopaedia their own codebook would not admit, 49
   still carrying drafting scaffolding, and a historical arm of 8 / 11 / 16 events
   for the 1970s / 1980s / 1990s. An engine reasoning by analogy is bounded by the
   analogies available; in 1990 it had seven.
6. **Labels.** IES-90's UCDP-GED component is location-based (deaths in the country,
   not between the actors), stated on every affected row. The 30-event label audit
   is pending and is a §7 gate; no verdict can rise above SUGGESTIVE without it.
7. **Big Moves look-ahead.** The top-5% threshold uses full history, and 2 of 41
   episodes would not clear their own point-in-time threshold — registered for v3,
   not silently fixed.
8. **The monthly tier.** 14 reads, 0 scored; it describes and cannot validate.
9. **The corpus's classes conflate acts with incidents.** Beyond the scoring
   consequence in item 3, the codebook's `infrastructure_attack` and
   `chokepoint_disruption` types mix hostile acts with accidents, and
   `conflict_escalation` and `sanctions` mix state coercion with labour disputes and
   producer price management. A `hostility` field now records this without renaming
   classes — renaming after seeing results would rewrite every published per-class
   number. The correct class placements are registered for v3, applied prospectively
   only.

## 13. What would change the verdict

VALIDATED requires all of: positive registered skill with DM and SPA *p* < 0.05 on
both tiers where *n* ≥ 30; skill > 0 in all three regime blocks; a null placebo;
permutation *p* < 0.05; and the recorded label audit. On this run every skill
condition fails in the wrong direction, the placebo condition is unmet, the
permutation no longer rejects, and the label audit is outstanding. The verdict rule
returns SUGGESTIVE / null, and we state plainly that the honest description is
worse than that: *significantly worse than the base rate, point-in-time.*

Both of our own explanations for the earlier null have now been falsified (§10), so
we are careful about offering a third. What the record supports is three concrete,
registrable routes, in descending order of what they would teach:

1. **Start from persistence.** The single most robust result here is that a rule
   using only the dyad's own recent escalation beats a state-conditioned analog
   engine by 0.29 in Brier. The natural next estimand is the *change* from that
   baseline, with the analog distribution asked to improve on persistence rather
   than to replace it. Registered for v3; not computed.
2. **Make the state vector exist.** Amendment H's finding is that most events have
   no knowable state. Either the situation fields are re-derived from sources that
   carry real publication dates, or the design is conditioning on something the past
   did not contain. This is historical work, not modelling work.
3. **Sample size.** 1,200 scored reads is the target; the 624 pre-1987 candidates
   and the corpus repair are the only route to it, and both are underway with
   admission reserved to the author.

If a null survives all three, the conclusion is not that history is uninformative —
persistence *is* history — but that the specific analogical move this project
formalised, "find state-similar precedents and average their outcomes", is the wrong
way to use it at these horizons. On the present evidence that is the finding we would
defend.

## 14. The integrity record

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

Run `walk_20260903T003422Z` (numerically identical to 210135Z; see the negative
control note at the head of this draft). Paths are in `data/walk_forward/summary.json` unless
another file is named. Regenerate the whole run with `make reproduce`; two
independent runs reproduce content digest `2a90ff4a…`.

| Number | Path |
|---|---|
| 313 events; class counts; 1973-10-06 … 2026-06-17 | `oil.db` `events` |
| spine audit: 0 of 313 with two source domains; 11.9% / 25.0% / 63.1% field provenance; 49 with draft text; 31 encyclopaedia-only; 9 bare eia.gov root; median 148 chars | `data/spine/AUDIT.md` (`src/spine_audit.py`) |
| 187 geo; 184 labelled; 3 uncovered; levels 76/6/48/54; 95 deal; 126 uncovered = the three non-geopolitical classes | `data_state` |
| κ −0.001 / −0.234 / 0.104 | `data/state/outcomes_kappa.json` |
| 262 of 313 with no situation field at *t* | `WALK_FORWARD_PROTOCOL.md` Amendment H; `data/state/situation_knowable.json` |
| Big Moves episodes, no-event, anticipation, base rates | `data/big_moves/{brent,wti,diesel_crack,wti_monthly}.json` |
| 299 reads / 253 scored / 150 labelled; cluster 35, block 2.32 | `tiers.daily.*` |
| G Brier −0.097 [−0.180, −0.018] p 0.022; means 0.769 / 0.701 | `tiers.daily.G.engine_vs.climatology` |
| G vs persistence −0.600 [−1.031, −0.230] p 0.0002; ref mean 0.480; 2 fallbacks | `tiers.daily.G.engine_vs.persistence`, `n_persistence_fallback` |
| G vs random −0.021 p 0.58; vs frozen +0.007 p 0.029 | `tiers.daily.G.engine_vs.{random_analogs,frozen}` |
| G SPA: 15 models, p_RC 1.00, p_SPA 0.65 | `tiers.daily.G.spa` |
| G RPS: clim −0.013, random +0.062, persistence −0.791 | `tiers.daily.G.rps.engine_vs` |
| P CRPS −0.071 [−0.136, −0.017] p 0.016; persistence +0.129; random −0.005; frozen +0.007 | `tiers.daily.P.engine_vs` |
| M precision 0.337 / recall 0.544 / base 0.225 | `tiers.daily.M.engine` |
| M13 −0.700 [−0.940, −0.457] p < 0.001; reliability by class | `tiers.daily.G.items_vs_climatology.M13_recalibrated`, `.murphy_M13` |
| Power: G 0.127 @80%, P 0.085 @80%, n≈1,200 for +0.05 | `tiers.daily.power` |
| Spec curve 162; min −0.150, median −0.075, max −0.041; 0% positive | `spec_curve.skill_distribution` |
| Placebo −0.047 [−0.083, −0.008]; clim −0.106; fair +0.017 | `placebo.*` |
| Permutation: observed −0.066, mean −0.101, SD 0.029, block p 0.124, iid 0.092 | `permutation` |
| FDR: 34 comparisons, 31 survive, almost all losses | `fdr.family` |
| Filtration audit: 15,784 checks, 0 violations | `filtration_audit` |
| Leakage: G 0.769 → 0.638; P 8.25 → 8.01 | `leakage_test` |
| Determinism: digest `2a90ff4a…`, seeds registered | `data_state.determinism` |
| Regime blocks 2008 / 2020 / 2026 | `regime_blocks` |
| Fair scores: Brier +0.021, RPS +0.119, CRPS diagnostic | `tiers.daily.{G,P}.diagnostic_fair` |
| Verdict statuses | `verdict.rules` |
| H1 +5.56pp and its placebo downgrade | `docs/red_team_1.md` |
| Five of six amplification edges retracted under a registered re-test | `data/ripple/retraction_six.json`, `data/gates/ripple_2026-09-02.md` |
| 624 pre-1987 candidates; 473 post-1987 candidates | `data/candidates/*.csv` |
| test count at the run | `data/acceptance_dod.json` D1 |
