# DESIGN.md — Amendment 2 (PROPOSED, not adopted)

*2026-09-03, session A. Registered as a proposal under SESSION_CHARTER §2 rule 2 and DESIGN.md's own
practice: the spec changes by dated amendment, never by silent edit. **Nothing in DESIGN.md is
edited by this file.** It requires Joe's approval before any code is written under it.*

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

## A2.9 — VSUP: flagged, NOT proposed for adoption

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

## Adoption

This amendment is a proposal. If Joe adopts it, it is committed **before** the code written under
it, per charter §2 rule 2, and DESIGN.md gains a pointer to it — its body is not rewritten. If it is
rejected in whole or in part, the rejection is recorded here with the reason and the build continues
under DESIGN.md as it stands.

**Open questions for Joe, in the order they block work:**

1. **A2.1** — is the skeptical reviewer the primary user? Everything else follows from this.
2. **A2.7** — five screens to four? This is the largest single change and it reorders finished work.
3. **A2.8** — does Story become prose? This has the highest fabrication risk of anything proposed and
   is the one I would most understand you refusing.
4. **A2.6** — the vintage wall needs a home whatever else is decided; it is currently invisible.
