# Open items — the complete register

*2026-09-03. Everything outstanding, in one place, ranked by whether it changes a published
sentence. Sources: `docs/red_team_2.md`, the session handoffs in `data/handoffs/`,
`data/acceptance_dod.json`, an external review of the paper, and Cowork's own audits.
Anything not listed here is done or explicitly out of scope.*

---

## Tier 1 — changes what a published number means

**1.1 The escalation target was substantially a persistence variable — registered,
fixed, and awaiting a rebuild.** *(red team 2 finding 3; verified, **partly corrected**, and
repaired by K, `c74ccd6` + `0a206b2`.)*

*The correction, to our own brief.* The finding as I briefed it overstated itself for four
events. `deaths_ged_pre90` is summed over `[d−89, d]` — **inclusive of the event day** — so
for an event whose own day is the violent one, the "before" figure is mostly the event.
Strictly before *d*: Ukraine 2022 is **79**, not 20,473; Israel–Hamas 2023 is **28**, not
3,835; Israel–Iran 2025 is **4**, not 959. Those are war *onsets* and their level 3 is
correct. The count of GED-set level 3 with ≥250 deaths genuinely before the event is **27 of
38, not 31**. The 34-of-54 headline count and the source split reproduced exactly; the
specific examples did not, and `OUTCOME_MAPPING.md` §(ii) records that rather than repeating
it.

*The defect is still real and still large.* Amendment 4 extends the "ongoing → no level"
rule to COW War and UCDP GED, and stops `max(default=0)` silently reading "no covering
record" as level 0 — the same defect with the sign reversed, not previously reported. The
effect on the target is severe: **184 events with a level → 132 (−28%)**, level 3 **54 → 20**,
level 2 **48 → 30**, `no_independent_outcome` **3 → 55**, 59 of 187 labels moving.
Persistence's share of the target's rank variance falls ρ² **0.640 → 0.407**; holding the
sample fixed at the 120 events scorable under both rules, 0.484 → 0.407, so about a third of
the fall is the rule and the rest is selection. **41% of the target's rank variance and 73%
of its labels are still what persistence would say** — partly mechanical, not only
mechanical, and the engine still has a legitimate baseline to beat.

**1.1a — RULED 2026-09-03: tag, rebuild, re-run.** Joe's ruling: tag the sealed record
first (done — `record-pre-amendment-4` at `18561e2`, so the published numbers stay citable
after the target changes under them), then rebuild `event_outcomes` under Amendment 4 and
re-run the walk. §8–§11 and the delta experiment are all on the pre-amendment target and the
paper owes a sentence saying so. Owner **K** (rebuild), **B** (re-run), **Cowork** (the
sentence). *The state that made this blocking:* The tree is in an **incoherent state**:
`event_outcomes` in `data/oil.db` still carries the pre-amendment 76/6/48/54 = 184, while
`src/state/ies90.py` is post-amendment, and `src/engine/persistence.py` calls
`ies90.score_event` **live** (Amendment B.1: "called, never copied"). **Any walk run right
now scores a pre-amendment target against a post-amendment baseline, and does not announce
it.** Two coherent states only: revert `ies90.py` to `c74ccd6`, or rebuild the `event_outcomes`
level rows. K declined to choose and did not add a switch to dodge asking, which was right.
Note that every published number — §8, §11, the delta experiment — is on the **pre**-amendment
target, so a rebuild means those numbers describe a target that no longer exists and a re-run
is owed. That is the record working, but it must be stated, not absorbed.

**1.2 The Big Moves clustering constants are unregistered.** *(finding 2.)*
`BIG_MOVES_REGISTRATION.md` registers clustering within 60 **trading** days and no merge
step; `src/big_moves.py` clusters at 90 **calendar** days and merges same-sign clusters
within 60. No amendment covers either, and both constants landed in the same commit as the
registration, so git cannot show registered-before-computed. Owner **Joe** (ruling: amend
with the honest history, or re-run under the registered rule), then **B**.

**1.3 The placebo condition is unresolved — and its interval is computed on the wrong unit.**
*(finding 1; second defect found by B's interval audit, 2026-09-03.)* The size-matched
reference the placebo passes under exists only in an unratified amendment; against climatology
it fails. Recorded as UNRESOLVED in README and paper §9.

**The new fact.** `placebo.*` in `summary.json` (`walk.py:1033`) bootstraps **411 pseudo-reads
as i.i.d.** (`mean_block=1.0, lag=0`). They are not: the 411 rows are **82 source events × 5
reps**, and the reps are matched on the *same* VIX-percentile decile of the *same* event.
Correcting to a source-event cluster widens by ≈ √(411/82) ≈ 2.24: `vs_random_analogs` skill
−0.0473, CI [−0.0828, −0.0082] → ≈ [−0.13, +0.04], **covering zero**, and DM *p* 0.019 → ≈ 0.19.
**`null_holds` would flip false → true.** `vs_climatology` (*p* = 9e-7) survives any plausible
widening; `fair_vs_climatology` already covers zero.

**RULED 2026-09-03: fix it, with the direction registered before the computation.** The
correction runs *in the engine's favour* — it removes a published mark against us, since
`null_holds: false` is currently evidence that the placebo null fails. That is the direction in
which a correction deserves the most scrutiny, and B stopped at the audit table rather than
proceeding to the fix for exactly that reason. A defect is a defect whichever way it cuts, and
declining to fix errors that favour us would be the same bias as fixing only those that hurt.
So: register the expected direction, the estimator and the exact re-run **before computing** —
the Amendment M pattern — then run it and publish as computed. The registration is what makes
this credible rather than convenient. Owner **B** (register, then re-run), **Cowork** (§9 and
README).

**1.7 The interval audit, and what it found.** *(B, `docs/INTERVAL_AUDIT_2026-09-03.md`,
read-only — nothing re-run, nothing fixed.)* Commissioned after B found the defect in its own
published grid file. **The defect is not widespread: two files carry it, one already
corrected.** Every other interval is computed on the right unit, because the event-study
modules de-overlap into clusters before bootstrapping (`propagation_graph`,
`local_projections`, `cross_chain`, `edge_battery`, `evidentiary_bar`, `frozen_lens`,
`placebo_vixmatched`, `supply_chain`, `research`) and the walk uses the stationary block
bootstrap at its own measured block. `ripple_lp.py` is explicitly correct — Newey–West at
bandwidth *h*, lag-augmented, clustered, BH across the family, which is the textbook treatment
of the horizon-stacking trap. **All three premises Cowork gave B were wrong, each in the
engine's favour, and B checked rather than accepted them:** the delta experiment does not stack
dyads or horizons (150 rows, 150 unique events); the 162-cell specification curve publishes a
distribution and no interval; and the propagation study's cells are cluster-collapsed with
BH-FDR gating `status = validated`. Two residual hygiene items, neither touching a published
conclusion: `brief.py` intervals are not de-overlapped (disclosed in prose, no number attached),
and `walk.py:_replay` mis-estimates the P-tier block on some spec-curve rows that publish no
interval. **Verdict: a published erratum is not warranted; one targeted correction is (1.3).**

**1.2 RULED 2026-09-03 — re-run under the registered rule, publish both.** The Big Moves
clustering constants go back to the registered 60-trading-day, no-merge rule as the primary
result; the as-computed 90-calendar-day merged version is published beside it; and an amendment
names the honest history, that both constants landed in the same commit as the registration so
git cannot demonstrate registered-before-computed. Expect the episode count and every ratio
built on it to move, including the "15 of 43" that README and BRIEF both carry. Owner **B**
or **C** (re-run), **Cowork** (the four surfaces).

**1.4 The escalation result is confounded three ways by era.** Skill by era: 1987–99
+0.009 (n=2, median pool 8), 2000–09 +0.068 (n=10, pool 10), 2010–19 −0.103 (n=51, pool
18), 2020–26 −0.117 (n=87, pool 36). Pool size, base rate (0.751 → 0.659) and label basis
(100% dyadic in 1946–73 → 7% by 2015–26) all move together, and the recent era dominates
the sample. Owner **B** — stratified diagnostic, registered first, gating nothing.

**1.5 A VALIDATED claim in `edge_battery.json` asserts what a new study would test, and its
gate is the discredited one.** *(Found by C while registering the magnitude study,
2026-09-03.)* `severity_dose_response` is carried as **VALIDATED** — the proposition that
event severity produces a dose-response in outcomes. That is exactly what
`MAGNITUDE_REGISTRATION.md` sets out to test, and it was validated by the same gate that never
looks at a non-event day: the gate on which five propagation edges were retracted. A live
VALIDATED assertion resting on a discredited gate is the highest-severity kind of stale claim
this project can carry, because it is machine-readable and other surfaces read it. C has
pre-registered its re-test with the verdict words fixed in advance. Owner **C** (re-test),
**Cowork** (ensure no published surface quotes it meanwhile). *Same class of defect as the
`v2.0` tag asserting "escalation conditioning validated OOS".*

**1.6 `events.severity` mixes measured and inferred values in one column.** *(Same source.)*
A free ordinal magnitude, populated for 305 of 313 events and unused by the engine — but
**102 of 313 values are auto-assigned by class** in `admit_events.py`. Measured and inferred
in a single column is what INV-5 forbids, and the field is a candidate input to the magnitude
study, so it must be split before anything reads it. Owner **C**.

## Tier 2 — the target and the corpus

**2.1 The event taxonomy conflates acts with incidents.** 33 of 187 geopolitical-class
events are not G-scorable (20 non-hostile, 13 ambiguous). A `hostility` field now records
this; the correct four-way taxonomy (interstate military / interstate coercion /
energy-geopolitical / non-state-domestic) is registered **prospectively only**. Owner
**Joe** (whether v3 re-codes), **F** (already registered).

**2.2 The historical corpus is thin — and the backward route is now measured shut.**
*(G-1, G-2, closed 2026-09-03.)* 8 events in the 1970s, 11 in the 1980s, 16 in the 1990s,
against 150 after 2010. G built six pre-1974 records to the full sourcing standard and
measured what admitting them buys: **zero scored reads**, because burn-in is per class at 8
and every monthly class is below it — the tier goes 14 → 20 and stays at 0 of the 30 it
needs. The four most consequential (Libya 1970, Tehran 1971, Tripoli 1971, IPC 1972) are
unscoreable on **both** branches: `opec_decision` is absent from `GEO_TYPES`
(`similarity.py:46`), and their price target is monthly WTI, measured at 16 distinct values
across the 324 months to 1972 with 83.5% of 3-month changes exactly zero. **Consequence:**
expanding backwards cannot reach the ~1,200 reads the power block requires, at any amount of
archival effort. This is a finding, published in paper §14. The remaining route to *n* is the
date-grid study (2.5). Residual for **Joe**: whether the codebook gains a class for a
concession or ownership change — four records currently sit in `opec_decision` by elimination.

**2.5a DELIVERED — the dyad-date panel exists, with its limits structural.** *(G, 2026-09-03.)*
**15,740 dyad-date cells, n_eff 9,733** (two-way cluster on date × dyad; block estimator
13,554), of which **1,160 informative**, over 333 month-ends 1987-01-31 … 2014-09-30 on 156
dyads. Per ruling 4.5 nothing scores a forecasting engine on it; it is a descriptive object.
Its three limits are written as properties of the construction rather than caveats: never
reaches the present, never carries VALIDATED (every cell `retrospective = 1`), never scores
onset (R-ACT admits a dyad only after a recorded clash, so skill here would be skill at
continuation and de-escalation only). VR-3 held on an independent path — 15,740 cells, 0
violations — and removes 861 dyad-dates that plain R-ACT would have selected on a record still
running at *t*.

**The degeneracy tripwire fired 21 times, and where it fired is a finding.** The panel is inside
the registered 0.95 share-zero bar overall (ΔIES 0.9191, L 0.9034) but breaches it in **1989 and
1991–1995**, across all four series — the Gulf War shadow years. Three independent measures
agree on that block: 44.7% of the rows, 17.6% of the signal, and individually degenerate by the
registered bar. Slices stay in and the bar stays at 0.95, as registered.

**The effective-count pairing is now structural, and this is the pattern the rest of the project
should adopt.** The nominal count no longer exists as a scalar anywhere in the panel's outputs:
`size.cells`, `dIES.n_defined` and `strict_subset.cells` are objects
(`{nominal, n_eff_two_way, n_eff_block, informative}`), so a programmatic reader gets the pair or
a `KeyError`. A generated citation line — written by the code from the computed numbers, with no
version of it lacking the effective count — leads every file. One writer (`finalize` →
`write_panel`) applies the pairing before writing, so no code path can publish a nominal without
an effective. A test requires an effective figure within 300 characters of every nominal
occurrence, and a test *of that test* proves it fires. It caught two bare counts the moment it
existed, including one in G's own reconciliation table. The headline is the **two-way** figure
because it covers both axes of a dyad-date panel — and G noted explicitly that it is also the
*smaller* of the two, so the choice cannot be read as having been made for that reason.
*This is the schema-level answer to the defect Cowork committed tonight and B committed in the
grid file: it moves the guarantee from discipline to structure.*

**2.5 *n* is the binding constraint; the date grid is the only remaining route, and
G-4 measured its ceiling.** *(Probe reported 2026-09-03; scope RULED: build 1987–2014.)*
G's one-year probes found the grid is viable but bounded, and the boundary is a property of
the sources, not of our effort: **after 2014 every non-zero ΔIES cell is an artefact** (1998:
23 of 29 non-zero cells rest on opposed-side evidence; 2018: **0 of 43**; 2024: **0 of 21**).
Two mechanisms, both verified against `ies90.py` rather than inferred — ICB records crisis
*actors*, not sides, so at 2018-01-31 the dyad `gbr|usa` scores IES level 3 from ICB crisis
489, the UK and the US recorded as at war with each other, and all six of 2018's level-3
dyads are pairwise combinations of {GBR, Russia, Syria, USA}: one episode counted six times.
GED is a *location* count replicated across every dyad containing that country. MID, MIDI and
COW War are the only sided sources, and `covers()` needs d+90 ≤ coverage end, so all three
stop at **2014-10-02**. Density per grid date is 29–31 active dyad-dates (1998) falling to
10–12 (2024); ΔIES share-zero is 90.2% / 85.3% / 54.4% — inside the registered 95%
non-degeneracy bar, but not comfortably. The strict release-date vintage rule kills every
cell (0 of 357), which is why `WORLD_STATE_CODEBOOK` Amendment 1 already rejects
release-date-as-vintage as a definition error; under the project's actual convention 86.8% /
88.4% / 44.4% survive. G's own added check (VR-3) found a real leak: 39 of 335 cells in 2018
admitted on a record still running at *t* — selection on the future.
**Ruling:** build the panel for **1987–2014**, on the VR-3 active set, with the evidence-basis
bucket beside every result, and register three limits up front — it can never reach the
present, never carry VALIDATED (every cell is `retrospective=1`), and never score onset
(R-ACT makes it a recurrence panel by construction). Owner **G** (panel), **B** (walk).
*Original framing:*
150 scored escalation reads against ~1,200 required; §11's power block puts the requirement
higher still at the skill actually observed. Registered as a **new study, new estimand** —
the unit of observation becomes a date, not an event: a periodic grid (468 month-ends or
2,028 week-ends, 1987–2026), multiple horizons, multiple price targets, and escalation
labels at the **dyad-date** level rather than bounded by our 313 chosen events. Also removes
the event-selection problem the Big Moves census exposes. Owner **B** (the walk), **G** (the
dyad-date label panel and its vintage stamp — the bottleneck, and the number that decides
whether the route works at all).

**2.3 The state vector is empty once vintage binds.** 726 of 786 situation values dropped
as not-knowable. G-3 derived `knowable_at` from dossier document dates and recovered
**60 → 83** kept at *t*, and established that `conflict_scope` can never be knowable at *t*
at all. Delivered (`situation_vintage.py`); the residual emptiness is a documented finding,
not an open task.

**2.4 Post-2000 sourcing cannot be repaired by any reachable route.** 28 records have no
citable domain; 0 of 27 post-2000 encyclopaedia-only records could be replaced through
eight probed routes, because between 2000 and 2016 no free archive reaches. Documented,
not fixable. Owner — none; it is a finding.

## Tier 3 — loops that have never completed

**3.1 ~~The claim ledger has never resolved a claim end to end.~~** **Closed** (H,
`0c97285`): 51 claims resolved from data at their horizon, and the 93% uncheckable rate was
found to be a property of the reading matter, not a defect in the reader.

**3.2 The reader's gold set is machine-graded.** 100 headlines coded by session A, reader
scores 84% against them, labelled unaudited and gated by nothing. Owner **H** (inter-coder
κ + `audit_reader.py`), then **Joe**.

**3.3 The challenge loop has 2 entries.** Owner **H**.

## Tier 4 — Joe's gates, which no session can close

**4.1 The IES-90 label audit.** 1 of 30 rows. D3a stays FAIL until 30 are graded and κ is
computed. Note item 1.1 may change what some rows should say — worth waiting for A's
amendment before grading the rest.

**4.2 The 13 ambiguous class rows.** Ruled terminal; no action, recorded.

**4.3 Rulings outstanding:** the Big Moves constants (1.2), the placebo reference (1.3),
whether v3 re-codes the taxonomy (2.1), pre-1987 admissions (2.2) — and, opened by G-2,
whether `EVENTS_CODEBOOK.md` gains a class for a concession or ownership change, since four
pre-1974 records currently sit in `opec_decision` by elimination. Also E's five proposed
coding gaps (`docs/spine/CODEBOOK_AMENDMENT_PROPOSED.md`), which live in the adjacent
repository and cannot be applied from here.

**4.5 RULED 2026-09-03 — the multiplier-4 drop stands.** B's registered §2.7 drop rule is
applied as written; the grid study has a **price arm only**. The escalation question stays on
the event-triggered reads. Recorded reasoning, which B and Cowork reached independently: the
dyad-date panel is 96.75% zeros, its coverage wall is hard at 2014-10-02 for every sided
source, and every cell is `retrospective=1`, so under `WORLD_STATE_CODEBOOK` Amendment 1 it
can describe and never validate. Density does not fix that, because the problem is not *n*.
B's own note stands on the record: the ratio test is the wrong test and would be written
differently today, and that is a separate question from whether this multiplier belongs in
this study. The gate report is `data/gates/grid_multiplier4_2026-09-03.md`.

**4.6 RULED 2026-09-03 — the desk's audience is the 90-second reader.** A recruiter or
professor who opens the link once, does not return, and must reach the finding and the
integrity record fast. A2.6, A2.7 and A2.8 are to be re-derived from that ruling by session A
and re-proposed, rather than ruled separately on their old framing.

**4.4 `launchd` access** so the daily loop runs unattended — needed for D7's ledger days.

## Tier 5 — packaging

| deliverable | status |
|---|---|
| One-page brief | done — `docs/BRIEF.md` |
| README for a ten-second reader | done |
| Spoken versions and term glosses | done — `docs/EXPLAIN.md` |
| Resume bullets | done, corrected to 27 datasets |
| Three flagship charts | in flight — session I |
| Paper restructured to lead with the three findings | **not started** — Cowork |
| Technical appendix | partial — Appendix A plus the registrations |
| Propagation as a companion piece | partial — standalone at `docs/RIPPLE_FINDINGS.md`, still summarised in paper §11 |

## Tier 6 — housekeeping

**6.1 `acceptance_v2 --dod` reports D1 FAIL on a green suite** — substring bug, tests
`"failed" not in summary` and the line reads "1 xfailed". Owner **A**, one line.

**6.2 Eleven `TASK_BRIEF_*.md` and other scaffolding are tracked** at the repo root.
Bannered where they carry claims; not yet moved. Owner **Cowork**, low priority.

**6.3 D7:** tag `v3.0`, and either seven distinct Ledger days or a dated PATH amendment
re-scoping that plan line. Owner **Joe**.

---

## What is *not* an open item

The null itself. Three registered claims have been falsified and published — H1's
stress amplification, the calibration hypothesis, and the permutation-structure claim — and
five of six propagation edges retracted. Those are the record working, not defects in it.
