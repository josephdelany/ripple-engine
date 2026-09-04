> **ARCHIVED — HISTORICAL RECORD, NOT A CURRENT CLAIM.** A working analysis or evidence record from the legacy engine. Preserved for audit; current release status is in [`SUBMISSION_STATUS.md`](../SUBMISSION_STATUS.md).

# Adversarial audit — every flaw, what it costs, and what closes it

*2026-09-03. Written against the project rather than for it. Each item states the flaw, the
question a hostile reviewer would ask, the honest answer, and the fix with its real cost.
Severity is about **exposure in a viva or interview**, not about scientific interest.*

**Read this before any interview.** An auditor who has already found their own worst problems is
in a different position from one who is discovered.

---

## 0. First, correct one thing about the evidence

The project does **not** have thin data. It has:

| | |
|---|---|
| corpus | 313 dated events, 1956–2026 |
| state panel | 27 sources, ~352k rows |
| price/macro series | 772, back to 1946 |
| grid study | 10,857 scored cells over 413 dates |
| dyad-date panel | 15,740 cells, n_eff 9,733 |
| propagation study | 477 node×shock cells |
| market census | 44 largest Brent episodes |

What is thin is one specific thing: **scored forecasts on the primary estimand — 100
escalation reads and 246 price reads.** Everything else is either a companion study answering a
different question, or input data. **Never say "the evidence is weak." Say "the primary test has
100 scored reads, and I measured what that can and cannot detect."** The first sounds like a
confession; the second is a finding.

---

## 1. Power — the real ceiling. **Severity: HIGH, unfixable**

**The flaw.** 100 scored escalation reads. The project's own power block puts the minimum
detectable Brier skill at **0.137**; the observed effect is −0.084. Detecting a true +0.05 would
need roughly 1,200 reads.

**What they ask.** *"So your test couldn't have found the effect you were looking for?"*

**The honest answer.** Correct, and I measured that rather than assuming it. The paper reports
the minimum detectable effect beside every headline. The null is therefore *uninformative about
small effects and informative about large ones* — I can rule out that formalised analogy has a
large, exploitable edge on this corpus; I cannot rule out a small one.

**How it screws you.** Only if you overclaim. If you say "I showed analogy doesn't work," a sharp
interviewer produces the power number and you lose the room. If you say it first, you own it.

**The fix.** None available. Backward expansion is *measured* shut (six pre-1974 records built to
full sourcing standard buy **zero** scored reads; pre-1973 monthly WTI has 16 distinct values in
324 months). Forward expansion works for price (grid: n_eff 1,979) but the escalation labels die
at 2014 because only MID/MIDI/COW War record *sides*. **This is a documented ceiling, not an
oversight — and being able to prove a ceiling is itself a result.**

---

## 2. The outcome variable has never been validated by a human. **Severity: HIGH, fixable in 3h**

**The flaw.** The IES-90 label audit stands at **1 of 30 rows**, and that one row was answered
while the tool was displaying the engine's own answer above the prompt — so it is contaminated
and has been marked superseded. Inter-coder κ = 0.8307 (0.7383 excluding rows whose event_id
telegraphs the class), **but both coders were AI**, which measures whether the codebook is legible,
not whether it is right.

**What they ask.** *"How do you know your escalation labels are correct?"*

**The honest answer today.** I don't, independently. The labels come from ICB, COW MID, COW War
and UCDP rather than my own coding — which removes *my* bias — but the mapping from those source
fields to a 0–3 level is mine and has not been checked by a human against the records.

**How it screws you.** This is the single most likely question in the first five minutes, and
right now there is no good answer. It also blocks `VALIDATED` project-wide by your own protocol.

**The fix.** Thirty rows, blind, rested. The tool is now correctly blinded (the engine's level
renders behind `[reveal]` *after* your answer). Three hours. **This is the highest-value
outstanding item in the entire project.**

---

## 3. No theoretical frame. **Severity: HIGH, fixable in one writing session**

**The flaw.** The paper tests whether analogy predicts. It never states the conditions under
which it *should*. It is an empirical exercise without a model.

**What they ask.** *"Why would you expect this to work in the first place? What would have had to
be true?"*

**The honest answer, and it is already in your results — you just haven't named it.** Analogical
forecasting requires three conditions, and this project found each one failing:

1. **The state must be observable at *t*.** 262 of 313 events have no situation field knowable on
   the day. *(§8, Amendment H)*
2. **The analog pool must be dense enough in state space.** Median pool 8 in 1987–99 against 36
   in 2020–26; every monthly class sits below burn-in. *(§9, G-1/G-2)*
3. **The target must not be dominated by its own autocorrelation.** Persistence beats the engine,
   and 73% of the change target is zeros. *(§8, §11)*

**Those three conditions are a theory of when analogical forecasting works.** Stated in §1 and
returned to in §13, they convert a pile of negative results into a structured account: *this class
of method must fail when any of three conditions breaks, and here is each one breaking, measured.*

**How it screws you without it.** "I built a thing and it didn't work" is an undergraduate
project. "I derived the conditions under which this class of method must fail, and demonstrated
each" is research. Same evidence, different standing.

**The fix.** 2–3 pages. No computation. **Do this second, after the audit.**

---

## 4. Your own field is under-cited. **Severity: MEDIUM, fixable in an hour**

**The flaw.** The econometrics is deep (Kilian, Baumeister–Hamilton, Känzig, Caldara–Iacoviello,
Brier, Gneiting–Raftery, Murphy, Diebold–Mariano, HLN, Politis–Romano, White, Hansen,
Benjamini–Hochberg, Ferro, Simonsohn, Dawid). The political science on *analogical reasoning
itself* is two citations: Green & Armstrong, Tetlock.

**What they ask.** *"Have you read Khong?"*

**Missing and canonical.** Yuen Foong Khong, *Analogies at War* (1992) — the standard work on
analogical reasoning in foreign-policy decisions, and directly your thesis. Ernest May, *"Lessons"
of the Past* (1973). Robert Jervis, *Perception and Misperception in International Politics*
(1976).

**How it screws you.** You are a history major writing about how analysts reason from precedent.
Not knowing the canonical work in your own field is worse than any statistical gap, because it
suggests the framing was reverse-engineered from the method.

**The fix.** An hour of reading, a paragraph in §2, one sentence in §1 connecting Khong's
descriptive claim (analysts *do* reason by analogy, often badly) to your normative test (does it
carry information when done systematically). Cheapest high-value item on this list.

---

## 5. The corpus is yours. **Severity: MEDIUM, disclosed**

**The flaw.** 313 events selected by you under a codebook you wrote. 0 of 313 have two
independent source domains; provenance is 11.9% external URL, 25.0% corpus-derived, 63.1% null.
28 post-2000 records have no citable domain and cannot be repaired by any route tested.

**What they ask.** *"You picked the events. How do we know the selection isn't doing the work?"*

**The honest answer, and it is a strong one.** I tested it from the other direction. The Big Moves
census inverts the event study — take the *market's* largest moves rather than my chosen events —
and **14 of 44 largest Brent episodes have no identifiable event in my corpus at all**, while in
half the attributed episodes every attributed event was already public more than 20 trading days
before the move began. So the corpus demonstrably misses things the market reacted to, and I
published that rather than discovering it in review.

**How it screws you.** Only if you haven't rehearsed the Big Moves answer. With it, this becomes a
strength.

**The fix.** None needed. Rehearse it.

---

## 6. The same statistical defect appeared three times in one day. **Severity: MEDIUM**

**The flaw.** A resampling unit correct for one comparison, inherited by a neighbour with a
different grouping variable: the grid price arm (10,857 cells treated as independent; *p* 0.010 →
0.052), the placebo block (411 pseudo-reads that are 190 source events), and the severity
dose-response (clustering by event type in a test grouped by severity — 36 overlapping episodes
counted as independent).

**What they ask.** *"If it happened three times, why should I believe the rest?"*

**The honest answer.** Because I audited all of them rather than assuming. `docs/INTERVAL_AUDIT_2026-09-03.md`
walks every estimator in the project, names the unit each uses and the unit it should use, and
finds the remainder correct — the event-study modules de-overlap into clusters before
bootstrapping, and `ripple_lp.py` uses Newey–West at bandwidth *h*, lag-augmented and clustered,
which is the textbook treatment of exactly this trap. Every instance inflated precision, none moved
a point estimate, and **each was found by the session that had published it, checking its own
result.**

**How it screws you.** If you present the audit, it's a strength. If they find one you missed, it
is fatal to the integrity story that is your main selling point.

**The fix.** Done. Know the audit exists and what it concluded.

---

## 7. Live awkward numbers you must not be caught rounding

| number | why it is awkward | the required phrasing |
|---|---|---|
| block permutation ***p* = 0.0500** | exactly on the registered 0.05, over 1,000 permutations whose resolution is 0.001 | "a knife-edge; I read nothing from it in either direction" — **never** "significant" |
| placebo `null_holds: false` | the placebo null **fails** under both the original and the corrected estimator | "the engine loses to matched non-events as well as to real ones; no verdict leans on the placebo" |
| Amendment N's prediction | registered a 2.24× widening and a flip to `null_holds: true`; measured 1.28×, no flip | "the registration was wrong in its arithmetic and right in its procedure — the number was written down first, so the failure is visible" |
| the pooling control flipped sign | −0.004 on the old target, +0.017 on the new | "a non-significant point estimate flipped across a target rebuild; the rule turns on indistinguishability, not sign, so the conclusion held — and the instability is itself a fact about how little n=89 resolves" |
| headline weakened twice | parity → −0.097 → −0.084 (n.s.) | "both amendments were registered before the code that implemented them, and both made my result *smaller*" |

**How these screw you.** Any one of them, quoted at you when you didn't raise it first, makes you
look like you were hoping nobody checked. **Raise all five yourself.**

---

## 8. Four retractions — a strength or a wound, depending entirely on framing

H1 stress amplification · the calibration hypothesis · the permutation-structure claim ·
`severity_dose_response`. Plus five of six propagation edges.

**The wrong framing:** "I kept getting things wrong." **The right framing:** "The apparatus caught
four of my own positive findings and I published all four retractions. Three were found by the
component that had produced the finding, re-examining its own result." Most published work in this
area retracts nothing, not because it is more careful but because nothing re-checks it.

---

## 9. Repository hygiene — low severity, but it is what a curious reviewer trips over

| item | status |
|---|---|
| `EVALUATION.md` asserted two **retracted** findings as current status | **bannered**; generator (`src/evaluate.py`) still unfixed — it will regenerate wrong |
| three demo pages cited hashes that no longer resolve; the 2026 page described an escalation read the current target **excludes** | **bannered** with current hashes; regeneration owed |
| figures and citation inventory stale after the re-run | guards correctly **red**; regeneration owed |
| `test_hostility.py::test_section_6_impact_recomputes_from_the_sealed_scores` | **failing** |
| 70 markdown files at the repo root | `INDEX.md` mitigates; a wanderer can still mistake a registration for a claim |
| the suite had three silent-skip modes today | fixed: a locked DB now raises, and >25% unexplained skips fails the run |

**How it screws you.** A reviewer who opens a root-level file called EVALUATION and reads a
retracted claim as your current verdict will not trust anything else. That one is handled; finish
the rest.

---

## 10. AI authorship — prepare this answer, do not improvise it

**What they ask.** *"Did you write this?"*

**The answer.** I directed it and I own every registered decision. The implementation was
AI-assisted across parallel sessions, and the reason that is defensible is the apparatus I built
to make it auditable: amendments committed before the code they govern, sealed reads hashed before
outcomes are looked up, a citation guard that fails when prose drifts from its source, an interval
audit, a filtration audit, and a suite that refuses to report green when it hasn't run. The
sessions caught each other's errors and mine.

**Do not** claim you hand-wrote the code. **Do** claim you built the review discipline — that is
the harder and more transferable skill, and for a consulting firm it is more interesting than the
finding.

---

## The order of work

| # | item | cost | why this order |
|---|---|---|---|
| 1 | **30-row label audit**, blind and rested | 3 h | closes the highest-exposure question; unblocks your own protocol |
| 2 | **Theory frame** — the three conditions, §1 + §13 | 2–3 h | largest standing upgrade, no computation |
| 3 | **Khong / May / Jervis** in §2 and §1 | 1 h | cheapest credibility gain; it is your own field |
| 4 | Rehearse §7's five awkward numbers aloud | 30 min | these decide the room |
| 5 | Regenerate figures, inventory, demos; fix `evaluate.py` | session work | hygiene |

**Items 1–4 are yours and take about seven hours.** After them, I would stop hedging about whether
this is defensible at a high level.
