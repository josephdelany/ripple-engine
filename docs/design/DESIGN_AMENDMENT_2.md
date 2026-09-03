# DESIGN.md — Amendment 2 (ADOPTED 2026-09-03)

*2026-09-03, session A. Registered under SESSION_CHARTER §2 rule 2 and DESIGN.md's own practice:
the spec changes by dated amendment, never by silent edit. **Nothing in DESIGN.md is edited by this
file.** Ruled on by Joe on 2026-09-03 and adopted; the adoption record and the ruling that differs
from the proposal are in §Adoption below. This document is registered BEFORE the code written under
it, including Appendix A, which fixes every generated sentence before any is written.*

*Basis: `docs/design/STUDY.md`, which measured the artefact built under Steps 0–4 against the spec
that specified it. Every claim of a defect below is a measurement, with the method stated in STUDY §5.*

---

## Why there is an amendment at all

DESIGN.md was written before the interface existed and before the results existed. Both now exist.
The spec is right about more than it is wrong about — the three tiers, the absence language, the
verdict-not-sign colour rule, and the insufficient/null distinction all survive contact with the
build and are **not** changed here. What changed is that four of its rules turned out to be
unenforceable as written, one of its screens is aimed at an audience we have now decided against,
and one finding it did not know about has become the most important thing the project has.

---

## A2.1 — The audience is registered

DESIGN.md §0 states the problem but never says who is reading. Every unresolved layout argument in
Steps 0–4 traced back to that gap.

**Proposed.** A new §0.1: *The desk is built for a skeptical technical reader deciding whether the
method is sound — five to twenty minutes, asking "is this real work?" Where the interests of a
ninety-second visitor and this reader conflict, this reader wins. The desk is not built for a daily
analyst, and no surface may imply a monitoring product.*

**Why.** The results decide it, not taste: the engine is worse than climatology on escalation
(−0.097 [−0.180, −0.018]) and on price (−0.071 [−0.136, −0.017]), and indistinguishable from random
analogs on both. There is no daily-analyst use case to design for. Full argument in STUDY §1.

---

## A2.2 — The tier rule becomes countable

**Defect.** §1 says "Nothing on any screen sits outside them." It is a prohibition with no counting
test, and it was not met. Measured on the rebuilt Story screen: **1** Finding element, **0**
Evidence elements, **0** Provenance elements, against 149 legacy `.dim`/`.mono` nodes. Bands 2, 3, 4
and 6 carry no tier class at all. Every test passed throughout.

**Proposed.** §1 gains an enforceable form:

> Every screen region renders **exactly one** Finding-tier element. Every number that is not inside a
> Finding element carries either `t-ev` or `t-prov`. A rendered screen containing a numeric string
> outside the three tier classes fails. **[T]** — and the test **counts** elements in the rendered
> DOM; it may not be satisfied by the classes existing in the stylesheet.

**Also.** §2's caption rule gains the same treatment: *the plain-words caption is rendered in the
DOM, not merely computed.* Measured: `story_read.travel()` returns a caption for all 53 cells and the
renderer drops every one. `.cap` count on Story is **0**.

---

## A2.3 — Captions name their reference

**Defect.** §2 fixes one caption: *"The interval crosses zero: no effect distinguishable from none at
this sample size."* That is correct where the reference is zero effect and wrong wherever it is not.
Step 4 hit this immediately: on the Ledger the reference is a coin flip, and the shared caption
asserted "no effect" about a board measuring whether the record beats being right half the time. It
had to be patched with a clarifying line beneath the board.

**Proposed.** The caption is parameterised by its reference, and the reference is always named:

| reference | caption |
|---|---|
| zero effect | "The interval crosses zero: no effect distinguishable from none at this sample size (n=…)." |
| a baseline | "The interval crosses zero: not distinguishable from `<baseline>` at this sample size (n=…)." |
| a coin flip | "The interval spans even odds: not distinguishable from being right half the time (n=…)." |
| a base rate | "The interval spans the everyday rate of `<r>%`: not distinguishable from an ordinary day (n=…)." |

Every chart states what its zero rule *is*. **[T]**

---

## A2.4 — A rule must be checked where commits are gated

**Defect.** Amendment 1 A1.3 diagnosed this correctly — *"A rule that can only be checked where the
checker never runs is not a rule"* — and then fixed only half of it. It moved the static rules into
`tests/test_design_spec.py`, which runs everywhere, and left the DOM rules in jsdom tests that
**skipped in every run**, because jsdom was never installed. The repo's only rendering test had been
silently passing by not executing. It was installed in Step 4 and began finding things immediately.

**Proposed.** §4 or a new §8:

> jsdom is a required development dependency (`npm install --prefix tools jsdom`; `tools/node_modules`
> is gitignored). In the environment that gates a commit, a **skipped** render test is a **failed**
> render test. Every rule marked **[T]** names the file and test that enforces it, and a **[T]** with
> no named test is not in the spec.

---

## A2.5 — The spec may not quote results, and one citation is withdrawn

**Defect 1.** §0 quotes "21 of 477 cells fired where 1–24 were expected by chance." The current file
gives 15 of 371 for the seven corpus classes (21 of 553 across all shock sets). A registered spec
that quotes results drifts from them silently and then misinforms the person implementing it.

**Proposed.** The spec names files and rules, never values. Where a number is needed to make a rule
concrete it is written as a path: "see `data/ripple/irf.json`, `meta` and the verdict counts."

**Defect 2.** §7 cites Bloomberg Terminal as a precedent and takes a design principle from it.
Bloomberg and FactSet are behind paid terminals; I could not consult either, and STUDY §4 records
that. On present evidence that citation is unsourced.

**Proposed.** §7 is marked as *consulted* versus *asserted from reputation*, and the Bloomberg claim
is either sourced or withdrawn. The principle it carries — that a strict luminance ladder does the
work boxes do badly — is independently supported and can stand on its own without the attribution.

---

## A2.6 — The vintage wall gets a screen, and the record bar gets a field

**The finding the spec did not know about.** `data/state/situation_knowable.json`: 726 of 786
situation field-values were knowable only *after* the event they describe. **262 of 313 events have
no state field at t at all.** This is rendered nowhere in the interface.

It is the project's most novel result. It is the *cause* of the null escalation skill, and it is a
finding about the literature — most published event studies condition on variables assembled after
the fact — not merely about this corpus.

**Proposed.**
- §5's record bar gains a named field: `STATE@t  60 of 786 knowable`, on every screen.
- A new §3.6 registers the vintage wall as a first-class region, and §3.1's Story gains a
  *"What was knowable"* band that states the absence in prose where a story has no field at t.
- The absence wording is registered here so it is identical everywhere: *"No situation field for this
  event was knowable at t, so the engine read it on class and entities alone."* **[T]**

---

## A2.6b — The record bar's verdicts carry §2 colour, and the colour is read from the interval

**Defect, found when run `walk_20260903T052633Z` replaced `walk_20260903T003422Z`.** §5 says the record
bar's "two verdicts [are] in Evidence tier **with their colour from §2**". They were rendered as plain
text with no colour at all, so the bar could not distinguish the three states §2 registers.

It stopped being cosmetic with this run. Escalation against climatology moved from
skill −0.097, CI [−0.180, −0.018] — **excluding zero**, the amber "engine worse" state — to
skill −0.084, CI [−0.175, **+0.004**], *p* 0.076 — **crossing zero**, the neutral state. Price against
climatology stayed at −0.074, CI [−0.140, −0.021], *p* 0.011, which still excludes zero and stays amber.
A bar that colours neither cannot show that one of the two verdicts changed state, and a bar that coloured
by the sign of the estimate would have shown both as amber and been wrong about escalation.

**Registered.** The record bar's verdict fields take their colour from the **interval**, through the same
`verdictOf()` the forest rows use: crosses zero → neutral grey; excludes zero and worse → amber; excludes
zero and better → green. Never from the point estimate, never from the *p*-value, and never from the status
string's wording. **[T]**

**How, and why it is not a new set of colour rules.** My first implementation gave the bar its own
`.v-worse` / `.v-better` text-colour rules. `tests/test_design_spec.py` rejected it, correctly and for the
right reason: §2 registers **one** absence language "so it is used identically everywhere", and that file
records that the propagation band already "carried a private `.ib`/`.v-*` implementation of the same idea"
and was made to consume the shared component. A second set of verdict colours is a second language.

So the bar draws the **same `interval()` mark** as every other verdict on the desk — a 54×11 span with its
tick and its zero rule — and the colour arrives through §2's own component. There are still exactly two
amber/green declarations in the stylesheet, which is what the §2 test counts.
`tests/test_record_bar.py::test_a26b_the_bar_reuses_the_shared_component_and_does_not_invent_a_second_language`
pins it so the shortcut cannot come back.

---

## A2.7 — Five screens become four, ordered as an argument

**Defect.** Feed / Story / Big moves / Ledger / Walk mirrors the pipeline, not a reader's question.
Consequences: the headline results sit in the last tab; Ledger and Walk ask one question twice; and
the Feed's grammar implies a monitoring product we do not have and cannot support — which is §6
violated by the navigation itself.

**Proposed.** `The result` · `How you'd catch us` · `A case` · `The record`. Feed folds into *The
record* as proof-of-operation. Ledger folds into *The result*. Rationale and the rejected
alternative (a single scrolling registered report, rejected as the whole IA and adopted as the
landing screen) in STUDY §2.

---

## A2.8 — Story becomes a narrative spine, not six numbered bands

**Defect.** Six labelled bands, each a titled panel, re-create the "grid of boxes" §4 forbids — the
cheapest possible hierarchy, reading as a template. More seriously, a panel cannot state *nothing*
gracefully, and *nothing* is the majority case: 262 of 313 events have no state at t, 37 of 53 cells
are null for a typical class, and Abqaiq's branch band has `applicable: true, n: null`.

**Proposed.** §3.1's six bands become a prose spine — *Question · What was knowable at t · What the
registered rule predicted · What happened · What we got wrong* — with instrument-grade figures
inline. Prose can say "nothing" without looking broken; a panel cannot.

**Guard, because generated prose is where fabrication lives.** Every generated sentence is
template-bound to named fields, the templates are registered in this amendment's appendix before any
are written, and the render test inventories every sentence against its source fields. No sentence
may contain a number that is not read from a named path. **[T]**

---

## A2.9 — VSUP: flagged, NOT adopted (ruled 2026-09-03)

The propagation band is 53 cells per class, of which 301 of 371 are null and 55 insufficient. Built
as 53 stacked forest rows it is correct, complete, honest, and unreadable. Value-Suppressing
Uncertainty Palettes (Correll, Moritz & Heer, CHI 2018) are the principled fix: allocate a larger
range of the visual channel where uncertainty is low, desaturating toward grey as it rises.

**Not proposed yet**, because it is a bivariate palette and §4's contrast floors (Finding ≥ 12:1,
Evidence ≥ 7:1, Provenance ≥ 4.5:1) must be cleared by every cell in both themes, and that has not
been measured. Recorded here so the option is registered before anyone is tempted to reach for it
mid-build. If adopted it extends §2 rather than replacing it: the three verdict states remain, and
VSUP governs only the saturation within them.

---

## What is NOT changed

The absence language of §2 stands unaltered — three states, the zero rule on every chart, interval
as a bar and estimate as a tick, insufficient hatched and never coloured, a caption in plain words.
STUDY §5 found it works wherever it was actually applied, and is simply missing where it was not.
Amendment 1 (A1.1–A1.6 and A1.1–A1.4) stands in full.

---

## Adoption — ruled by Joe, 2026-09-03

| item | ruling |
|---|---|
| **A2.1** | **RULED, and NOT as proposed.** See below. |
| **A2.2** | adopted as proposed |
| **A2.3** | adopted as proposed |
| **A2.4** | adopted as proposed |
| **A2.5** | adopted as proposed |
| **A2.6** | **ADOPTED** — record-bar field, the §3.6 region, and the registered absence wording, all as proposed |
| **A2.7** | **ADOPTED** — four screens; Feed folds into *The record* as proof-of-operation, Ledger folds into *The result* |
| **A2.8** | **ADOPTED, CONDITIONAL.** The condition is non-negotiable and is stated below |
| **A2.9** | **NOT adopted**, as recorded. VSUP is not reached for until a bivariate palette has been measured against §4's contrast floors |

### A2.1 as ruled — and the disagreement, recorded

I proposed the **skeptical technical reader** (five to twenty minutes, auditing the method). Joe ruled
for the **ninety-second reader** — a recruiter or professor who opens the link once, does not return,
and must reach the finding *and the integrity record* fast. Not the daily operator.

Recorded per CLAUDE.md `<push_back>`: the argument was made, the ruling went the other way, and the
build follows the ruling. The registered text of §0.1 is therefore:

> *The desk is built for a reader who opens the link once, spends about ninety seconds, and does not
> return. They must reach the finding and the integrity record fast. Where the interests of that
> reader and a longer audit conflict, the ninety-second reader wins. The desk is not built for a
> daily operator, and no surface may imply a monitoring product.*

**What actually changes versus my proposal.** Less than it appears, and this is why I record it rather
than contest it. Both readings demand the same things — a finding sentence at the top of every screen,
the integrity record reachable rather than buried, and no surface implying a product. The ruling
changes *emphasis*: the landing screen is optimised for a single visit rather than for an audit, and
"How you'd catch us" must be reachable in one click rather than read in order. Where the two conflict
during the build, the ninety-second reader wins and the conflict is noted at the point it arises.

**One instruction carried verbatim into the build**, from the ruling: *the null is the finding, not an
apology for one. It gets Finding-tier weight, not a hedge.* This is registered as a rule, not a
preference: **a null result is rendered at Finding tier. No hedging verb, no apologetic clause, and no
softening adverb may attach to it. [T]**

### A2.8's condition, as ruled

Adopted **only** with all three of these, in this order:

1. Every generated sentence is registered in **Appendix A below, before any of them is written.**
2. Every generated sentence is bound to named source fields — no number may appear in a sentence that
   was not read from a declared path.
3. The render test that inventories each rendered sentence against its declared source paths **exists
   and passes before the first sentence renders**. *If the test does not exist, the prose does not ship.*

---

## Appendix A — the registered sentence set

*Registered 2026-09-03, before any of these sentences was written. This is the complete set of
sentences the desk generates about itself. A sentence not in this table may not be rendered; adding
one is an amendment to this appendix, dated, before the code.*

**Mechanism.** Each sentence is emitted by `say(id, payload)` into a node carrying
`data-sentence="<id>"` and `data-fields="<comma-separated source paths>"`. Slots are resolved from the
API payload by the declared path and by nothing else. Free text between slots is fixed here and may
not be computed. Numbers are formatted by the shared helpers only.

**The enforcement.** `tests/test_sentences.py` renders every screen under jsdom, collects every
`[data-sentence]` node, and for each one: (a) asserts its id is in this appendix; (b) re-resolves its
declared paths from the same payload; (c) asserts every numeric token in the rendered sentence is
derivable from those resolved values; (d) asserts the fixed text matches this appendix's template with
the slots removed. A numeric token that is not derivable is a **failure**, not a warning. **[T]**

### A.1 — The result (landing screen)

| id | template | slots → source paths | when |
|---|---|---|---|
| `res.lede` | *"Restricted to what was knowable at the time, the record goes quiet."* | — (no slots; fixed text) | always |
| `res.vintage` | *"For {events_no_field} of {events} events the engine has no state to condition on at all."* | `vintage.events_with_no_situation_field_at_t`, `vintage.events` | always |
| `res.vintage.detail` | *"{dropped} of {total} situation field-values became knowable after the event they describe. {kept} survive."* | `vintage.dropped_after_t`, `vintage.total_values`, `vintage.kept` | always |
| `res.walk` | *"The engine forecasts escalation {g_word} than climatology and prices {p_word} than persistence."* | `walk.G.climatology.skill` → {g_word} ∈ {better, worse, no differently}; `walk.P.persistence.skill` → {p_word}; word chosen by the interval's relation to zero, never by the point estimate | when both intervals exist |
| `res.walk.null` | *"Against random analogs the interval crosses zero on both tasks: no effect distinguishable from none at this sample size (n={n_g}, n={n_p})."* | `walk.G.random_analogs.n`, `walk.P.random_analogs.n` | when both cross zero |
| `res.travel` | *"{k} of {n} registered pass-through cells transmit."* | `travel.transmitting`, `travel.cells` | always |
| `res.travel.none` | *"{cls} transmits nowhere: {n} registered cells, none of them transmitting."* | `travel.by_class[cls]`, `travel.cells_per_class` | when a class has 0 |
| `res.ledger` | *"At {n} resolved claims the record and the narrative are not distinguishable."* | `ledger.with_record_call` | when the paired interval crosses even odds |
| `res.ledger.sep` | *"On {n} resolved claims the {who} is right more often."* | `ledger.with_record_call`; {who} from the sign of the paired interval | when it excludes even odds |
| `res.ledger.empty` | *"No claim has reached its horizon yet."* | — | when `ledger.with_record_call` is 0 |

**Addition, 2026-09-03, registered before the code.** Joe's brief of this date: *"The 90-second landing
screen should state the three conditions from paper §1.1 — that is now the project's frame and the desk
should lead with it."* PAPER_DRAFT §1.1 registers C1 observability, C2 density, C3 non-degeneracy, and
reports that all three fail on this corpus. The landing screen leads with them.

| id | template | slots → source paths | when |
|---|---|---|---|
| `res.frame` | *"A state-conditioned analog forecaster needs three things. On this record none of them holds, and each failure is measured."* | — (fixed) | always |
| `res.c1` | *"Observability. {a} of {b} events have no state that was knowable at the forecast date."* | `vintage.events_with_no_situation_field_at_t`, `vintage.events` | always |
| `res.c2` | *"Density. The monthly tier scores {a} of its {b} reads: every class sits below the registered burn-in of {c}."* | `walk.monthly_scored`, `walk.monthly_reads`, `walk.burn_in` | always |
| `res.c3` | *"Non-degeneracy. Persistence beats the engine on Brier by {a}, and {b}% of the change target is exactly zero."* | `walk.G.persistence.skill_abs`, `delta.share_zero_pct` | always |
| `res.frame.close` | *"Each is a property of the record, not of the reasoning."* | — (fixed, §1.1's own words) | always |

**What C2 does NOT say, and why.** §1.1's table also gives *"median analog pool 8 in 1987–99 against 36 in
2020–26"*. That comparison exists in the paper's prose and in **no machine-readable file in the repo** — I
looked. §6 forbids a number whose file is not reachable in one click, so the desk states the half of C2 that
is sourced (`data/walk_forward/summary.json`: monthly `n_scored_burn_in` 0 of `n_reads` 14, against
`registered.burn_in` 8) and stays silent on the era comparison until something computes it to a file. The
sourced half is the operative one: it is why the historical arm scores nothing.

### A.2 — How you'd catch us

| id | template | slots → source paths | when |
|---|---|---|---|
| `catch.vintage` | *"{dropped} of {total} field-values were dropped because they became knowable after the event."* | `vintage.dropped_after_t`, `vintage.total_values` | always |
| `catch.audit` | *"The {n_rows}-event label audit stands at {n_done} done; κ is not computable and the audit has not passed."* | `record.audit.n_rows`, `record.audit.n_done` | when `record.audit.passed` is false |
| `catch.audit.passed` | *"The {n_rows}-event label audit passed at κ = {kappa}."* | `record.audit.n_rows`, `record.audit.kappa` | when passed is true |
| `catch.placebo` | *"Every cell is tested against {n} state-matched placebo pseudo-events."* | `travel.n_placebo` | always |
| `catch.dark` | *"{n} of {total} series stopped reporting before {cutoff}."* | `dark.n_stale`, `dark.n_series`, `dark.cutoff` | when `dark.n_stale` > 0 |

### A.3 — A case (Story spine)

| id | template | slots → source paths | when |
|---|---|---|---|
| `case.knowable.none` | *"No situation field for this event was knowable at t, so the engine read it on class and entities alone."* | — (fixed; the registered A2.6 wording) | when the event has 0 fields at t |
| `case.knowable.some` | *"{k} situation field{s} for this event {was} knowable at t; the rest were dropped."* | `story.state_at_t.kept` | when > 0 |
| `case.priced` | *"The realized path sits {pct}% {dir} the analog median at +{h} trading days, on {n} conditioned analogs."* | `story.priced.now_vs_median_abs`, `story.priced.horizon_td`, `story.priced.fan.n` | when a fan exists |
| `case.priced.none` | *"No comparable set: an unclassified story has no reference class."* | — | when `story.priced.fan` is null |
| `case.claims` | *"{n} {claim|claims} extracted, {c} checkable, {u} uncheckable."* | `story.n_claims`, `story.n_checkable`, `story.n_uncheckable` | always |
| `case.tail.none` | *"Nothing in the record precedes this event, so the engine has no reference class."* | — | when `no_adequate_precedent` and 0 analogs |
| `case.tail.thin` | *"The closest precedent scores {sim} against a retrieval threshold of {thr}, so no reference class is formed."* | `story.branches.max_similarity`, `story.branches.threshold` | when `no_adequate_precedent` and analogs exist |
| `case.tail` | *"{k} of {n} analogs were contained at +{h} days."* | `story.branches.subset_counts.counts.CONTAINED`, `story.branches.subset_counts.n`, `story.branches.horizon_days` | when precedent is adequate |
| `case.travel` | *"{k} of {n} registered cells transmit for this class."* | `story.propagation.counts.TRANSMITTING`, `story.propagation.counts.cells` | when available |
| `case.travel.none` | *"No cell transmits for this class: all {n} registered cells are null or insufficient."* | `story.propagation.counts.cells` | when k = 0 |
| `case.wrong` | *"This page is read against a target whose own label audit stands at {a} of {b}."* | `story.trust.audit.n_done`, `story.trust.audit.n_rows` | always — A2.2 requires band 6 to carry a Finding, and the audit is the honest one |

**Correction, 2026-09-03, same day, before any sentence rendered.** A.3 first registered `case.q` for
the story title. That was a mis-registration: a corpus title is **verbatim quoted material**, governed by
Amendment 1 A1.2 (rendered in a `data-verbatim` node and inventoried, never edited by the desk), not by
this appendix, which governs only sentences the desk **writes itself**. `tests/test_sentences.py` caught
the drift on its first run — the registry and the appendix must name the same set — and the row is removed
rather than implemented. The title still renders; it renders through `verbatim()`.

**Correction 2, 2026-09-03.** A.5's ban caught `res.vintage.detail` and `catch.vintage`, both of which
read "knowable **only** after the event". In those sentences "only" is precise rather than apologetic — it
means *not until*. The sentences were reworded to "became knowable after the event"; **the rule was not
relaxed**. Narrowing A.5 to let the token through would have been weakening a gate on first contact to make
it pass, which is the one move this project does not make. The reworded sentences say the same thing and
lose nothing.

### A.4 — The record

| id | template | slots → source paths | when |
|---|---|---|---|
| `rec.noevent` | *"{k} of the {n} biggest Brent moves since {first} have no identified event at all."* | `big.no_identified_event`, `big.n_episodes`, `big.first` | always |
| `rec.corpus` | *"{n} events, {from} to {to}, in {c} classes."* | `record.n_events`, corpus date range, class count | always |
| `rec.feed` | *"The live loop ran on {day}: {m} material, {i} in line, {x} noise."* | `feed.day`, `feed.counts.*` | when a feed exists |

### A.5 — Words that may never appear in a generated sentence

In addition to §6's banned list (`predicts`, `validated`, `signal`, `confirms`), no generated sentence
may contain a hedging or apologetic construction attached to a null: *only, merely, unfortunately,
sadly, admittedly, disappointing, weak, fails to, we had hoped, although, despite*. A null is stated
flatly. **[T]** — enforced in `tests/test_sentences.py` against every `[data-sentence]` node.

---

## Closing

DESIGN.md's body is not rewritten. It gains a pointer to this file. Everything built after this
commit is built under DESIGN.md as amended by Amendment 1 and this amendment, and Appendix A is
binding on every sentence the desk writes about itself.
