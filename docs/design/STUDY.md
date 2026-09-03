# The desk — design study

*2026-09-03, session A. Written after building DESIGN.md Steps 0–4 (796f1ef, 27cbc10, 2440847,
7b9658d, ef164ed, 8faa0ad) and then measuring what was actually built. DESIGN.md was a hypothesis
written before anything existed; this study treats the build as data on it.*

*Every number in this document was executed and is reproducible from the path named beside it.
Nothing here is estimated or recalled.*

---

## 0. The evidence this study is arguing from

The design question changed because the results changed. These are the results, as of this date.

| what | value | receipt |
|---|---|---|
| corpus | 313 events, 1973-10-06 → 2026-06-17, 7 classes (17–57 each) | `data/oil.db` `events` |
| series | 772 series, 678,280 observations | `data/oil.db` `observations` |
| **escalation (G) vs climatology** | **−0.097 [−0.180, −0.018]**, DM *p*=0.022, n=150 | `data/walk_forward/summary.json` |
| escalation vs persistence | −0.600 [−1.228, −0.230], *p*=0.00023 | same |
| escalation vs random analogs | −0.021 [−0.098, 0.052], *p*=0.58 | same |
| **price (P) vs persistence** | **+0.128 [0.070, 0.185]**, *p*=3.3e-5, n=253 | same |
| price vs climatology | −0.071 [−0.136, −0.017], *p*=0.016 | same |
| price vs random analogs | −0.005 [−0.060, 0.049], *p*=0.85 | same |
| permutation *p* | 0.124 | same |
| monthly tier | n_scored **0**, `permits_validation: false` | same |
| G target audit | 30-row sheet, **1 done**, κ = null, `passed: false` | same |
| **events with NO situation field at t** | **262 of 313 (83.7%)** | `data/state/situation_knowable.json` |
| situation values kept at t | 60 of 786 (7.6%); 726 dropped as knowable-after-t | same |
| propagation cells transmitting | **15 of 371 (4.0%)**; 11 survive BH q=0.10 | `data/ripple/irf.json` |
| — by class | policy_response 7, infrastructure_attack 3, opec_decision 2, demand_shock 1, chokepoint 1, conflict_escalation 1, **sanctions 0** | same |
| big Brent moves with **no identified event** | **15 of 43 (34.9%)**, Wilson [0.224, 0.498] | `data/big_moves/brent.json` |
| ledger: record vs narrative | 19 of 36 vs 17 of 36; disagree on 34; record right on 18 of 34, Wilson [0.367, 0.685]; McNemar exact *p* = 0.864 | `data/ledger/resolutions.jsonl` |
| feed today (2026-07-28) | 2 material, 0 in line, 12 noise | `data/feed.json` |
| series gone dark | 40 of 772 last reported before 2025-09 | `data/oil.db` |
| — non-randomly | Iran's five JODI series all end 2018-07 (US secondary sanctions reimposed); UAE + Qatar end 2018-12; Russian crude stocks 2009; Kazakh 2014 | same |

Two of these have never appeared on any screen: **the vintage wall (262 of 313)** and **the dark-data
selection problem (40 series, non-randomly)**. Both are findings. Both are currently invisible.

---

## 1. Who is this for

### The decision

**Primary user: the skeptical technical reader deciding whether this project's method is sound.**
Concretely — a data journalist's editor, a quant lead, a researcher, an interviewer with a
technical background. Someone who gives it five to twenty minutes and whose actual question is
*"is this real work, or a dashboard?"*

### The argument against the alternatives

**Against the daily analyst.** This is not a taste question; it is settled by the numbers above. An
analyst adopts a tool when it beats the heuristic they already use. This engine is *worse than
climatology* on escalation (−0.097, interval excluding zero) and *worse than climatology* on price
(−0.071, interval excluding zero). It is indistinguishable from drawing random analogs on both
tasks. The one thing it beats is persistence on price (+0.128) — and "better than assuming
tomorrow equals today" is not a reason to open a terminal every morning. Designing for the daily
analyst means designing for a user the results say we cannot yet serve. The Feed makes that
promise implicitly today, and today's Feed is 2 material items out of 14.

**Against the ninety-second recruiter.** This audience is real — the project is a capstone and has
been shown to a news company. But optimising for it means optimising for impressiveness, and the
honest headline is *mostly null*. You cannot make "mostly null" impressive without overstating it,
and not overstating is the one property this project has that most projects don't. Designing for
the recruiter puts the interface in direct conflict with §6.

**Why the reviewer is the right primary.** This is the only audience for whom the actual results are
an **asset**. "The engine loses to climatology on escalation, here is the interval, here is the
registration that fixed the test before we ran it, here is the audit that has not passed yet" is a
strong signal to a reviewer and a weak one to nobody. The nulls are the product.

And the choice is not zero-sum in the direction people assume: **an artefact built for the reviewer
is also readable in ninety seconds, provided every screen opens with one sentence stating its
finding.** The converse fails — a recruiter-optimised artefact loses the reviewer in ten seconds,
permanently. So we buy the second audience by doing the first one properly. We do not buy the first
by doing the second.

### What this costs the other two

| audience | what they lose | mitigation |
|---|---|---|
| recruiter (90 s) | reads the word "null" repeatedly; no single wow number | the ten-second object is the **method** claim, not the result claim (§3); it is genuinely impressive and true |
| daily analyst | no watchlist, no alerting, no real-time driver; Feed demoted from product to proof-of-life | accept it. Re-open only if a tier ever clears `permits_validation` against climatology |
| reviewer | nothing | — |

**Per screen, what the choice costs:** Feed loses its claim to be a daily surface (cost: analyst).
Story gains provenance density that a recruiter will skim (cost: recruiter's attention, low). Ledger
and Walk get *more* prominent, which is the reviewer's gain and the recruiter's loss of a clean
narrative. Big moves is neutral — it serves all three.

---

## 2. Is the five-screen structure right?

### The charge against it

Feed / Story / Big moves / Ledger / Walk is an information architecture organised by **data source
and mechanism** — it mirrors the pipeline, not a reader's question. It was drawn in NORTH_STAR
before any result existed. Three specific failures now:

1. **The headline is in the last tab.** The walk verdicts are the project's actual findings and
   `Walk` is fifth. The landing screen is the Feed, whose content today is 2 material items.
2. **Two screens for one idea.** Ledger and Walk are both track record — claims-vs-record and
   engine-vs-baseline. A reviewer reads them as one question asked twice.
3. **The Feed implies a product.** A live-updating feed is the visual grammar of a monitoring tool.
   We do not have a monitoring tool; we have a study. The interface is making a claim the results
   don't support — which is a §6 violation committed by the navigation itself.

### The alternative I propose

**Four screens, ordered as an argument rather than as a data model:**

| # | screen | the reader's question | absorbs |
|---|---|---|---|
| 1 | **The result** | "What did you find?" | Walk verdicts + Ledger boards + the vintage wall + the propagation count |
| 2 | **How you'd catch us** | "How do I know you didn't cheat?" | registration, vintage discipline, sealed reads, placebo, permutation, the unfinished audit, dark data |
| 3 | **A case** | "Show me it working on one event" | Story |
| 4 | **The record** | "What is underneath it?" | Big moves + corpus + the live loop (Feed folded in as proof-of-life) |

The reordering is the whole point: screen 1 is the abstract, screen 2 is the methods section, screen
3 is the worked example, screen 4 is the data appendix.

### A genuinely different architecture, argued and rejected

**"The paper": abandon screens entirely.** Render the project as one scrolling registered report —
abstract, method, results, limitations, appendix — with live figures inline and no navigation at all.

*For:* it matches the actual epistemic object exactly; the primary audience reads papers; it kills
the "dashboard implies a product" problem at the root rather than by relabelling tabs; and it is
trivially legible in ninety seconds because papers have abstracts. The precedent (Registered
Reports, RPP, OSF) is strongest here of anywhere in this study.

*Against:* it destroys the demo. The single most persuasive artefact this project has is *stand at a
date, paste a headline, watch the engine read it point-in-time* — and a static document cannot show
that a system runs. The project's live claim is not "here are results" but "here is an engine that
grades itself continuously"; a paper asserts that, an instrument demonstrates it. It also makes the
Story's 53-cell propagation band and the analog fan unusable as explorable objects.

*Verdict:* **rejected as the whole IA, adopted as screen 1.** "The result" *is* the abstract of the
paper, and should read like one — prose and figures, not cards. That is the synthesis, and it is why
screen 1 is not merely "Walk renamed."

**A second alternative, rejected faster: "lead with the failures."** A front page titled *What we got
wrong*. Rejected as a pose. Self-flagellation is not calibration; it overstates in the other
direction and a reviewer reads it as performance. The verdict table with intervals is both more
honest and more impressive than an apology.

---

## 3. The one thing in ten seconds

**Currently: no screen delivers one.** Measured, not asserted — the rebuilt Story screen renders
exactly one Finding-tier element (§5), and the landing screen is a Feed with 2 material items.

The candidates:

- *(i) the result* — "oil's response to geopolitical shocks is mostly indistinguishable from noise."
  True, but it is a negative about the world, and a reader's first reaction is "then why build this."
- *(ii) the method* — "an engine that grades itself against four baselines and publishes when it
  loses." True, impressive, and it survives the results being null.
- *(iii) the vintage finding* — **262 of 313 events have no state field that was knowable at the
  time.** Novel, specific, and it is the *cause* of (i).

**The ten-second object should be (iii) framed by (ii)**, because (iii) explains (i) and is the
genuinely new contribution. Most published event studies condition on variables assembled after the
fact; this one refuses to, and the refusal is what empties the conditioning set. That is a finding
about the literature, not just about this corpus.

Proposed ten-second object, three numbers and one sentence:

> **Restricted to what was knowable at the time, the record goes quiet.**
> 262 of 313 events have no state to condition on · escalation forecasts do worse than the base
> rate (−0.097 [−0.180, −0.018]) · price beats persistence (+0.128 [0.070, 0.185])

**No screen shows the first number today.** `data/state/situation_knowable.json` is rendered
nowhere. That is the single largest gap this study found, and it is a content gap, not a styling one.

---

## 4. Precedents

*Honesty note, because this study is about honesty: six of these I opened directly. Three I could
only reach through search-result summaries because the sites return 403 to automated fetches. Eleven
named sources I could not open at all. Each is labelled. Nothing below is recalled from memory.*

### Opened directly

**FRED — series page for our own Brent series** (`fred.stlouisfed.org/series/DCOILBRENTEU`).
*Uncertainty:* none, deliberately — FRED publishes measurements, not estimates, so there is nothing
to bound. *Absence:* missing observations render as a literal `.` — a character, not a gap.
**Taken:** the provenance model wholesale. Units, frequency, "Updated: Sep 2, 2026 12:17 PM CDT",
next-release date, source attribution, and a suggested citation with DOI and retrieval date, all
above or beside the number. This is §6's "one click from its source" already solved by someone else.
**Rejected:** nothing, but note the inapplicability — a page with no estimates needs no interval
language, so FRED teaches provenance and teaches nothing about our hard problem.

**Our World in Data — grapher page** (`ourworldindata.org/grapher/share-of-population-in-extreme-poverty`).
*Uncertainty:* handled in prose and FAQ rather than in the mark — they explain survey
incomparability at length beside the chart. *Absence:* a **"breaks in data"** toggle that reveals
where a series stops being comparable, and honest disclosure that regional aggregates are
"extrapolated to the year of the data release."
**Taken:** finding-as-title above the chart, source line beneath it, always. And the breaks-in-data
idea, which is the closest thing in mainstream data journalism to our vintage wall.
**Rejected:** extrapolating across gaps, and making the breaks a *toggle*. Our equivalent must be
permanently on and cannot be dismissed — the wall is the finding.

**Center for Open Science — Registered Reports** (`cos.io/initiatives/registered-reports`).
*Uncertainty:* not a visual system; an institutional one. *Absence:* this is the only precedent here
whose entire purpose is to make a null publishable. In-principle acceptance "will not be revoked
based on the outcomes"; the format "eliminates the bias against negative results in publishing
because the results are not known at the time of review."
**Taken:** the licence for the whole design. A null is a *completed* result, not a missing one, and
the interface should render it with the same weight as a positive. Also the vocabulary — registered,
in-principle, results-blind — which we already use and should use more visibly.
**Rejected:** nothing.

**Trading Economics — Brent commodity page** (`tradingeconomics.com/commodity/brent-crude-oil`).
The most useful **rejection** in this study, because it is what a visitor expects a market page to
look like. Dense, competent, and — quoting the fetch — *"The page shows minimal uncertainty
quantification. Forecasts lack confidence intervals, standard deviations, or probability ranges."*
It states "Brent is expected to trade at 91.72 USD/BBL by the end of this quarter" with no bound at
all.
**Taken:** one thing only — model outputs are explicitly attributed ("according to Trading Economics
global macro models"), so a reader can tell a projection from a print.
**Rejected:** everything else, and specifically the shape of the page. This is the interface we must
not build, and it is the gravitational default.

**Retraction Watch Database — user guide** (`retractionwatch.com/retraction-watch-database-user-guide/`).
*Absence:* the strongest model here for our Ledger. It is **dual-entry** — the original article and
the notice withdrawing it are both records, both dated, both searchable, and the status change is
itself the object. It distinguishes full retraction from partial invalidation ("Correction" for
sections unfit for citation while the article stands) and carries a published reasons taxonomy.
**Taken:** the Ledger should be a dual-entry register of claims and their dated status changes, not
a scoreboard. A scoreboard has a score; a register has a history, and a history reads correctly at
n=1 where a score reads as failure. This directly addresses §3.3's "reads as broken."
**Rejected:** the blog-derived, organically-grown taxonomy — ours must be a closed published list
(it is: the verdict kinds in CLAIM_LEDGER_REGISTRATION.md).

**Philadelphia Fed — Survey of Professional Forecasters**
(`philadelphiafed.org/surveys-and-data/real-time-data-research/survey-of-professional-forecasters`).
*Uncertainty:* forecast dispersion files plus a separate error-statistics resource. The decisive
detail, from the search result and confirmed on the page's own linking: benchmark models are
estimated **"with real-time data from the Philadelphia Fed real-time data set, using the vintage of
data that the survey panelists would have had at the time."** That is charter §2 rule 5, practised
by a central bank since 1990. It is the citable institutional precedent for our vintage discipline
and we should name it.
**Taken:** the vintage discipline, and the existence of a published error table as a first-class
artefact. **Rejected: its placement.** Accuracy sits in a "Resources" section below the forecast
downloads — supplementary to the forecasts. We invert it: track record *above* forecast. The lesson
is that even the honest institutions bury the score, and we should not.

### Reached only through search summaries (site returned 403 to direct fetch)

**IPCC AR6 calibrated language.** A fixed published vocabulary binding words to numeric ranges —
*virtually certain* 99–100%, *very likely* 90–100%, *likely* 66–100%, *about as likely as not*
33–66%, *unlikely* 0–33%, *very unlikely* 0–10%, *exceptionally unlikely* 0–1% — plus a **separate
confidence axis** built from evidence (type, amount, quality, consistency) crossed with agreement.
**Taken:** the two-axis idea, which is the most important import in this study. *Strength of
evidence* and *agreement among sources* are different things, and our `NULL` / `INSUFFICIENT` split
is a crude one-axis version of it. A cell that is null on 200 events and a cell that is null on 16
are both "null" to us and should not be.
**Rejected:** the word-scale itself. Mapping our intervals onto "very likely" would add a layer of
interpretation between the reader and the number, which §1 exists to prevent.

**Metaculus — scoring and track record.** Baseline score (against chance) and Peer score (against
other forecasters) are shown *together*; the calibration curve is a first-class object showing, e.g.,
that your 80% forecasts resolved yes 65% of the time. Annulled questions "are not scored," and an
admin explains why in a thread anyone can read and challenge.
**Taken:** two references shown side by side rather than one — we have four baselines and should
show them as a set, never one at a time. And **visible annulment with a stated reason**, which is
exactly the defect I fixed in Step 4: 12 of 13 "pending" ledger claims are hypothetical and can never
resolve, and the screen was counting them as pending.
**Rejected:** medals and leaderboards — single-user project, no peer set.

**ECMWF ensemble meteograms** (Forecast User Guide §8.1.4, via Confluence search result). Box-and-
whisker plumes showing median, 25/75, 10/90, and min/max at successive lead times: a standard,
learnable encoding for a distribution evolving over time, and directly applicable to our analog fan.
The stated limitation matters more than the encoding: **"bi-modal distributions of forecast results
will not be shown by meteograms as box-and-whisker plots cannot do this, though bimodal
distributions can be apparent on plume diagrams."**
**Taken:** the plume, *not* the box plot — our analog distribution is frequently bimodal (contained
vs escalated) and a box plot would conceal precisely the structure the reader needs. Draw individual
analog paths.
Also from the same source: a newer ECMWF meteogram design uses **value-suppressing uncertainty
icons**, allocating a larger range of icons when uncertainty is low and a smaller range when high.

**Value-Suppressing Uncertainty Palettes** — Correll, Moritz & Heer, CHI 2018
(`dl.acm.org/doi/10.1145/3173574.3174216`; open implementation at `uwdata.github.io/vsup/`). VSUPs
"allocate larger ranges of a visual channel to data when uncertainty is low, and smaller ranges when
uncertainty is high," blending colours toward grey as certainty falls; a crowdsourced evaluation
found they lead people to weight uncertainty more heavily than conventional bivariate maps do.
**Taken:** the principled answer to our hardest rendering problem. The propagation band is 53 cells
per class of which 301 of 371 are null and 55 insufficient. A VSUP makes uncertain cells recede
*automatically as a function of their own uncertainty* rather than by the hand-tuned three-state
rule §2 currently specifies. This is the one place I would consider extending the registered absence
language.
**Rejected (for now):** it is a bivariate palette and must clear the §4 contrast floors in both
themes; that is a real cost and it is why this is a proposal, not a change.

**Reproducibility Project: Psychology** (via search; Science paper 403, OSF page is a JS shell).
Of 97 original findings reported significant, **35 (36.1%)** were significant on replication, and
81 of 97 (83.5%) were stronger in the original. The nuance the team published alongside the blunt
number: 77% of replication effect sizes fell within a prediction interval from the original.
**Taken:** publish the blunt fraction *and* the sophisticated reading in the same place, with both
numerators visible. Also the lesson about what happens if you don't — the coverage carried "only 36%
replicated" and nothing else.
**Rejected:** nothing; this is the closest thing to a template for reporting a corpus of mostly-null
results.

### Named in the brief but **not opened** — recorded so the gap is visible

`metaculus.com` track record and FAQ (403) · IPCC AR5/AR6 guidance PDFs (403) · ECMWF charts
(403, bot protection) · `ft.com` Visual & Data Journalism (blocked) · `science.org` RPP paper (403)
· OSF project `ezcuj` (JS shell, no content served) · IMF PortWatch (JS shell) · Good Judgment
(403) · EIA weekly petroleum dashboard (the URL now serves an archive index; EIA has discontinued
*This Week in Petroleum*) · Reuters Graphics · NYT Upshot.
Bloomberg and FactSet are behind paid terminals and were **not** consulted; §7 of DESIGN.md cites
Bloomberg as a precedent and that citation is, on the current evidence, unsourced. See the proposed
amendment A2.5.

---

## 5. What building it taught me — evidence on the spec

The spec was a hypothesis. Here is what measuring the built artefact says about it. Method:
`renderStory()` executed under jsdom against the real `/api/story?id=abqaiq_attack_2019` payload,
DOM queried per band; old screen taken from `git show 5882ca4:src/app.html` (pre-Step-0).

| | old (5882ca4) | new (Steps 0–4) |
|---|---|---|
| rendered characters | 9,023 | 13,195 |
| labelled bands | 0 | 6 |
| Finding-tier elements | 0 | **1** |
| Evidence-tier elements | 0 | **0** |
| Provenance-tier elements | 0 | **0** |
| interval marks | 0 | 53 |
| zero rules drawn | 0 | 53 |
| hatched (insufficient) | 0 | 13 |
| plain-words captions (`.cap`) | 0 | **0** |
| `data-verbatim` nodes | 0 | 2 |

Per band, the new screen:

| band | intervals | captions | tier classes | legacy `.dim`/`.mono` |
|---|---|---|---|---|
| 1 the read | 0 | 0 | 1 find | 0 / 0 |
| 2 is it priced? | 0 | 0 | **0** | 9 / 9 |
| 3 is the narrative right? | 0 | 0 | **0** | 5 / 3 |
| 4 what is the tail? | 0 | 0 | **0** | 17 / 15 |
| 5 where does it travel? | 53 | **0** | **0** | 109 / 0 |
| 6 how much to trust this | 0 | 0 | **0** | 6 / 13 |

### What the spec got right

- **The three tiers are the correct decomposition.** Where band 1 uses `.t-find`, the screen reads
  the way the spec intended, immediately and obviously.
- **"Colour carries the verdict, not the sign"** is right and load-bearing. It is what lets a null
  look composed.
- **Insufficient ≠ null, hatched not coloured** is right and was vindicated in Step 4: 10 of the
  Ledger's 12 source rows fall below n=8, and hatching them is the difference between an honest
  screen and one asserting that aljazeera.com is 100% accurate on 8 claims.
- **The zero rule on every chart** is right.
- **A1.2's split of the forbidden-word rule** (absolute for the desk's own strings, inventoried for
  verbatim quotation) is right and was necessary — without it the desk would have had to edit source
  titles to satisfy a lint.

### What the spec got wrong

1. **§1's tier rule is unenforceable as written.** "Nothing on any screen sits outside them" is a
   prohibition with no counting test. Result: the flagship screen has **one** tier-classed element
   and 149 legacy `.dim`/`.mono` ones, and every test passed throughout.
2. **§2's caption rule is satisfied in the data and lost in the DOM.** `story_read.travel()` returns
   a plain-words caption for all 53 cells. The renderer drops every one. `.cap` count on Story: **0**.
   A rule can be implemented in the backend and still be absent from the interface.
3. **The spec's own [T] tests test the stylesheet, not the interface.** `tests/test_design_spec.py`
   verifies that the palette, the contrast ratios and the vocabulary *exist in the source*. They do,
   and nothing uses them. The rules were implemented as CSS that no screen consumes.
4. **The only DOM test in the repo had been skipping in every run**, because jsdom was never
   installed and the test skips politely when it is missing. This is Amendment 1 A1.3's own
   complaint, one level deeper: A1.3 correctly diagnosed "a rule that can only be checked where the
   checker never runs is not a rule," moved the static rules somewhere they run — and left the DOM
   rules exactly where they were. I installed jsdom in Step 4; it immediately began testing.
5. **Band 4 violates §1 in the spec's own words.** It renders `Contained 17 of 23 74%` — a
   proportion with no interval, where §1 says such a number "appears with its interval or not at all."
6. **Band 6 violates §2.** It renders `−0.097 · 95% CI −0.180..−0.018` as text, where §2 requires
   "interval as a bar, estimate as a tick — not a number in a cell."
7. **Six labelled bands re-create the grid of boxes §4 forbids.** Each band has a numbered heading
   and a panel; the effect at real density is a template, which is the exact failure §0 names.
8. **§0 quotes results and they have already rotted.** It says "21 of 477 cells fired where 1–24
   were expected by chance." The current file gives 15 of 371 for the seven corpus classes (21 of
   553 across all shock sets). A registered spec that quotes results will always drift from them.
9. **§2's caption asserts the wrong thing wherever the reference is not zero-effect.** "The interval
   crosses zero: no effect distinguishable from none" is correct for a local projection and wrong for
   the Ledger, where the reference is a coin flip. Step 4 had to add a clarifying line beneath the
   board to stop the shared caption from misdescribing it.

9b. **A look-ahead value is on the Story screen right now.** Session G reported
   (`data/handoffs/G_to_A_2026-09-03_knowable_at_rule_e.md` §3) that `sr_conflict_scope` counts
   same-dyad events at `abs(days) <= 120` — symmetric, so contaminated by the future. I verified
   the consequence end to end on 2026-09-03: `conflict_scope` renders in the Story DOM as a
   *likeness* justifying an analog match — the screen offers a future-contaminated field as evidence
   that a 1977 event resembles a 2019 one. That is charter §2 rule 5 violated on a surface I own.
   It needs a ruling (G proposes dating the field at `event_date + 120`), not a silent patch, and it
   is listed as an open question rather than fixed here.

10. **§3.5 specifies a column with no data behind it.** It requires `anticipated` to become "a
    visible column rather than an inline tag." There is no `anticipated` key in
    `data/big_moves/brent.json`; all 43 episodes carry it as null. The spec cannot be implemented as
    written until `big_moves.py` computes the field or §3.5 is amended.

### What I only learned by building

- **53 forest rows in a column is not readable.** The propagation band is correct, honest, complete
  — and it is a 53-row stack that no one will read. The content is right and the *form* is wrong.
  This is what pushed me toward a grid and toward VSUP.
- **The absence language works better than I expected on the Ledger and worse than expected on
  Story.** On the Ledger it turned three boards reading zero into a stated null with an interval. On
  Story it is invisible, because the bands that most need it (priced, tail, trust) never adopted it.
- **The honest screen is often the *simpler* one.** Step 4's biggest improvement was not visual: it
  was discovering that 12 of 13 "pending" claims can never resolve, and saying so. No amount of
  styling would have fixed a number that was wrong.
- **Provenance is cheap and I under-used it.** Adding the receipt path to the Ledger's Provenance
  line cost one line and is the thing a reviewer checks first.

---

## 6. Three directions for the Story screen

Genuinely different objects, not three skins. Each assumes the same data contract.

### Direction A — "The verdict card" (subtractive)

One screen-height object: a single finding sentence, one chart (price against the analog fan), and
a strip of four verdict chips — priced · narrative · tail · travel — each linking to a detail view.
No bands on the landing view. Everything else is one click away.

*For:* delivers the ten-second object trivially; destroys the template feel; makes "one finding per
screen region" true by construction; the only direction that works on a phone.
*Against:* **hides the density that constitutes the credibility.** A reviewer's question is "did you
cheat," and the answer to that question is evidence, which this direction puts behind clicks. It
also breaks §6's "no number without its file reachable in one click" by spending the click on
navigation instead of provenance. Risks reading as thin — the failure mode where a project with 678k
observations looks like a landing page.

### Direction B — "The registered report" (documentary)

The Story renders as a short paper about one event, top to bottom: **Question · What was knowable at
t · What the registered rule predicted · What happened · What we got wrong.** Prose with inline
figures and inline provenance; no panels, no numbered bands.

*For:* matches the epistemic object exactly, and matches the primary audience's reading habits. The
strongest precedent support in this study (Registered Reports, RPP). Decisively: **prose can say
"nothing" without looking broken.** "No state field for this event was knowable at t, so the engine
read it on class and entities alone" is a sentence; the same fact as an empty panel reads as a bug.
Given that this is true for 262 of 313 events, the format that handles absence gracefully is not a
stylistic preference — it is the majority case.
*Against:* generated prose is exactly where fabrication risk lives; every sentence must be
template-bound to a named field and inventoried, which is real work and a real hazard. Harder to
scan. Makes the engine look like a document rather than a running system — and "it runs" is part of
the claim.

### Direction C — "The instrument" (additive)

A fixed multi-pane instrument: persistent left rail (event selector), top status strip (the record
bar), 3–4 panes that all re-key when the event changes. Hierarchy from the luminance ladder alone,
no boxes. The propagation band becomes a **VSUP heat grid** — 7 hops × node, colour suppressed by
uncertainty — instead of 53 stacked rows.

*For:* solves the 53-row problem properly; genuinely professional; the only direction that would
serve an analyst if we ever earn one; density is honest when the hierarchy is earned.
*Against:* highest build cost by a distance. Density without earned hierarchy is precisely the
failure §0 diagnoses, and this direction has the least margin for getting it wrong. The VSUP palette
must clear §4's contrast floors in both themes. And a ninety-second visitor sees a wall.

### Recommendation

**Direction B for the spine, Direction C for the figures.** The Story reads as a short registered
report, and its figures are instrument-grade — including the propagation grid, which is the one place
C's density is unambiguously correct. This hybrid is not a compromise between A and C; it is the only
combination in which the 262-of-313 absence case reads as a finding rather than as an empty screen.

**A is rejected.** Subtractive design is the wrong instinct for an audience whose question is
whether we cheated. Putting evidence behind a click is the opposite of what the primary user wants,
and the ten-second problem is better solved by a finding sentence at the top of a dense screen than
by removing the density.

---

## 7. What this study contradicts in DESIGN.md

Written up as a dated amendment for approval, not applied: **`docs/design/DESIGN_AMENDMENT_2.md`**.
In summary it proposes registering the audience (§1 of this study), making the tier rule countable
rather than prohibitive, making the caption reference-aware, requiring the DOM tests to be
non-skippable where commits are gated, forbidding result numbers in the spec text, adding a screen
for the vintage wall, and replacing the six-band Story layout with the narrative spine.

The absence language itself **survives**. Nothing in this study argues against it; §5 shows it works
where it was actually applied and is simply absent where it wasn't.

---

## 8. Sources

Opened directly: [FRED DCOILBRENTEU](https://fred.stlouisfed.org/series/DCOILBRENTEU) ·
[Our World in Data grapher](https://ourworldindata.org/grapher/share-of-population-in-extreme-poverty) ·
[COS Registered Reports](https://www.cos.io/initiatives/registered-reports) ·
[Trading Economics Brent](https://tradingeconomics.com/commodity/brent-crude-oil) ·
[Retraction Watch Database user guide](https://retractionwatch.com/retraction-watch-database-user-guide/) ·
[Philadelphia Fed SPF](https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/survey-of-professional-forecasters)

Reached through search summaries only (direct fetch returned 403):
[Metaculus scores FAQ](https://www.metaculus.com/help/scores-faq/) ·
[IPCC AR6 WG1](https://www.ipcc.ch/report/ar6/wg1/) and
[IPCC uncertainty guidance note](https://www.ipcc.ch/site/assets/uploads/2018/03/inf09_p32_draft_Guidance_notes_LA_Consistent_Treatment_of_Uncertainties.pdf) ·
[ECMWF Forecast User Guide §8.1.4 Meteograms](https://confluence.ecmwf.int/display/FUG/Section+8.1.4+Meteograms) ·
[Value-Suppressing Uncertainty Palettes (CHI 2018)](https://dl.acm.org/doi/10.1145/3173574.3174216) and
[implementation](https://uwdata.github.io/vsup/) ·
[Reproducibility Project: Psychology summary](https://ppw.kuleuven.be/okp/_pdf/Nosek2015ETROP.pdf)

Not opened, listed so the gap is visible: Metaculus track record page, ECMWF charts, FT Visual &
Data Journalism, Science.org RPP paper, OSF ezcuj, IMF PortWatch, Good Judgment, EIA weekly
dashboard, Reuters Graphics, NYT Upshot, Bloomberg, FactSet.
