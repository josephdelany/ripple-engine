> **WORKING NOTE — INTERNAL BUILD MATERIAL, NOT A CLAIM.** Internal planning and build material. Not part of the submitted product; see [`README.md`](../README.md).

# The Brief Standard — how the Intelligence Desk stays honest

This document is the methodology behind the Ripple Engine **Intelligence Desk**
(`/workbench`) and its **Analytical Brief** (`src/brief.py`). It exists so that a
sophisticated reader — an analyst, an editor, a head of state — can see *why* the
numbers are trustworthy, not just take them on faith. It was written to a standard
drawn from real institutional practice, researched and cited below.

The Desk does one thing that traditional narrative newsrooms (NYT, Al Jazeera) do
not, and traditional quant desks do not: it **fuses the story with the measured
history**, and it does so under hard honesty gates. It leads with the number, states
the uncertainty, ships the base rate, and refuses to fabricate.

---

## 1. What the research said "high-level" means

Four independent research streams (institutional research notes; geopolitical-risk
tradecraft; narrative-economics / event-study rigor; terminal-grade design) converged
on one picture. The load-bearing findings, with the primary sources:

**Structure — conclusion first (BLUF).** Institutional notes lead with the bottom
line, then evidence in descending importance (CFA Institute, *How to Write a Great
Research Report*; DNI ICD-203 key-judgments format). The Desk's brief opens with a
one-sentence **BOTTOM LINE** before any evidence.

**Likelihood ≠ confidence, and never fabricate precision.** Intelligence tradecraft
(ICD-203; Sherman Kent's *Words of Estimative Probability*) separates *how probable*
from *how good the evidence is*, and binds probability words to fixed bands rather
than inventing "63%". The Desk keeps **confidence** (evidence quality: sample size +
corroboration) explicitly separate from any statement of magnitude, and — crucially —
**emits no occurrence probability at all** for whether an event happens.

**The killing statistic (the prior for everything).** Cutler, Poterba & Summers
(1989), *What Moves Stock Prices?* (NBER w2538): macro news explains **at most ~⅓** of
return variance, and "large market moves often occur on days without any identifiable
major news." So the honest default is humility: a headline is a weak, noisy cause.

**Association, never causation.** MacKinlay (1997) — a significant cumulative abnormal
return is an *association around an event under a joint hypothesis*, not proof of
cause. Even Shiller's *Narrative Economics* (NBER w23075), whose whole thesis is that
narratives move markets, writes "we can give no final proof of causality." If Shiller
hedges, the Desk hedges.

**Base rates, magnitude vs probability, small-N, selection, clustering, confounders.**
From the event-study and news-index literature (Baker-Bloom-Davis EPU 2016;
Caldara-Iacoviello GPR 2022; Kilian 2009, *Not All Oil Price Shocks Are Alike*; the
ASA statement on p-values): every conditional statistic ships with its base rate;
magnitude and probability are separate numbers; small samples force caveats or silence;
a hand-curated event corpus is selected on the outcome and therefore an **upper bound**;
overlapping events mean effective N < nominal N; and an oil move must name its
confounders (demand, OPEC+, inventories, the dollar, the risk premium).

**Design — Tufte, not decoration.** Terminal-grade credibility comes from a high
data-ink ratio: tonal (luminance-layered) surfaces not decorated cards, tabular
figures, two-font discipline (sans for prose, mono for numbers), semantic colour only
and direction double-encoded, direct labels not legends, inline sparklines / CAR
curves / small multiples, and a print/PDF mode for presentation. (Tufte, *data-ink* &
*sparklines*; Bloomberg terminal UX; FT/Economist/Datawrapper style guides.)

Full source lists live in the research appendix of this project's build log; the
citations above are the primary, verified ones.

---

## 2. The honesty gates, and where they are enforced

Every gate below is enforced in code (`src/brief.py`) and covered by a test
(`tests/test_brief.py`), so it cannot silently rot.

| # | Gate | Enforcement |
|---|------|-------------|
| G1 | **BLUF** — conclusion first | `bottom_line()` renders the lead sentence before any section. |
| G2 | **Association, not causation** — no causal verbs in prose | `test_br2` bans "causes/caused/drives/will move/guarantees"; templates say "associated with". |
| G3 | **Magnitude, not probability** — no occurrence probability | The engine emits expected \|CAR+20\|; `test_br3` asserts the discipline line and that no quant field names a probability. |
| G4 | **Every conditional stat ships its base rate** | `quant_read()` computes a NULL baseline (|CAR+20| on random ordinary windows) and reports the class's position vs it (lift), not a naked number. |
| G5 | **Bootstrap CIs, not parametric t** | `bootstrap_ci()` — percentile bootstrap on small, heavy-tailed, clustered returns; fixed seed → reproducible. |
| G6 | **Small-N gates drive the mode** | `sample_gate()`: n≥30 full · 10–29 caveat · 4–9 cases-only · <4 documented gap (never a fabricated rate). |
| G7 | **Selection / survivorship disclosure** | Stated on every brief: the hand-curated corpus makes the measured move an **upper bound**. |
| G8 | **Clustering disclosure** | Stated: overlapping events mean effective N < nominal N; CIs are, if anything, optimistic. |
| G9 | **Oil confounder panel** | Named every time: demand, OPEC+, inventories, the dollar, the risk premium (Kilian). |
| G10 | **Confidence ≠ likelihood** | `confidence_tier()` reports evidence quality only, explicitly "NOT the probability of any outcome." |
| G11 | **Real events only, sourced** | `precedent()` returns corpus events with `source_url`; `test_br4` asserts every analogue is a real `event_id`. |
| G12 | **Reproducible** | Fixed seeds → same story yields the same brief (`test_br6`). numpy executes the arithmetic; the model never eyeballs it. |
| G13 | **What-would-change-it** | Observable, falsifiable invalidation criteria on every brief (`what_would_change()`). |
| G14 | **Provenance & as-of** | Every figure carries a source and a data-as-of; prediction-market prices are labelled risk-neutral context, never a statistic. |

---

## 3. The anatomy of a brief

`build_brief(story)` assembles, in order:

1. **Bottom line (BLUF)** — the one honest sentence: association + median move + 90% CI
   + where it sits vs ordinary moves + today's amplifier + the priced gap.
2. **The quant read** — median/mean \|CAR+20\| with range, IQR, bootstrap 90% CI; the
   null-baseline lift; the multi-horizon CAR path (+1/+5/+10/+20) and its curve (t=0
   rule, ±1 SE band); the cross-asset reaction (oil / gas / USD / gold / equities /
   yields, % and bps on **separate** scales); the small-N gate and disclosures.
3. **Verified precedent** — nearest real corpus analogues with dates, measured moves,
   shared-entity count (a type-only match is shown as the weak precedent it is), sources.
4. **Market state now** — Brent level + move (sparkline), priced oil vol (OVX) percentile,
   GPR percentile + posture, flagged chokepoints — each with an as-of.
5. **Priced vs our view (the gap)** — the source-aware transmission read (supply/demand
   channel; does the real move confirm it?), the engine-vs-market gap (under-priced risk
   / over-priced fear), what prediction markets price (context), and the resolving,
   Brier-scored track record (published honestly, small-N and all).
6. **Synthesis** — the fusion paragraph, in the honest phrasings above.
7. **What would change this view** — observable, falsifiable markers.
8. **Receipts, confidence, discipline** — provenance, the confidence tier (evidence
   quality), and the standing discipline line.

Everything **reuses** the validated engine (`triage`, `event_study`, `cross_asset`, and
the committed pipeline artifacts). No new statistical claim is minted at the surface;
the brief is an honest *presentation* layer over measurements the engine already made.

---

## 4. What this is not

It is **not** a forecast of whether an event will happen — it never estimates that.
It is **not** a claim that the news caused the move. It is **not** a trade signal.
It is a disciplined answer to one question: *when events like this happened before, how
did oil actually behave, how sure can we be, and how does that sit against what the
market has already priced?* — with every number one hop from a stored computation, and
every limit stated out loud.
