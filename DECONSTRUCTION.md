# The Read — article deconstruction, quant-engine ruled

The flagship. Paste a news story (URL or text) and the engine breaks it into its claims and
answers **each** with measured evidence — never a generated opinion. The quant engine rules;
no LLM, no fabrication, $0.

## Why this shape (the decision, recorded)
The ask was "read an article, see what's true, weigh op-eds against all the data." An LLM that
*declares* what's true is the slop this project is defined against — and a local LLM won't run on
the target Mac, while a hosted one breaks "$0/keyless forever." So the honest, powerful version:
**extract every claim, bind each to the engine's measured record, and let the numbers render the
verdict.** That is what "see the truth of the article" means when you cannot fabricate.

## The pipeline (`src/deconstruct.py`)
1. **Extract** the article body (real-paragraph scrape from `<article>`/`<p>`, nav/boilerplate filtered).
2. **Fact vs op-ed** — transparent markers (first-person density, opinion phrases). An op-ed is
   evaluated against the data, not taken on the writer's authority.
3. **Pull the claims** — verbatim sentences that carry an entity, an event, a figure, or an
   assertive verb. Extractive; no paraphrase. Hypothetical clauses ("Iran *could* close Hormuz")
   are flagged and answered "if it occurs" — the base rate is for events that happened.
4. **Bind each claim to the quant engine** (reusing `brief.py`): the class's historical base-rate
   20-day oil move (median, IQR, 90% CI, n, percentile of ordinary moves), the nearest verified
   precedent, cross-asset reaction.
5. **Verdict by the numbers** — "materially larger than normal" is claimed **only** when the class
   median's 90% CI clears the everyday baseline; otherwise the typical move is called in line — and
   the fat tail is **always** cited (never "ordinary" next to a 51% precedent). Small samples flagged.
6. **The historical record** — every coded corpus event of the dominant class, entity-matched first,
   each with its measured move + source: "what history says," with numbers.
7. **Public mood** — measured sentiment (GDELT tone, geopolitical-risk percentile, attention,
   conflict-media), shown only when the article has a real class (else it would overclaim).

## The honesty gates (enforced + tested, `tests/test_deconstruct.py`)
- Verdicts are measured-only; no causal/opinion language; every stat cites history + n.
- Expected magnitude, never an occurrence probability; association, not cause.
- Dominant class = the article's actual topic (salience), not a priority-ordered side-mention.
- The mood block never renders on a non-geopolitical article.
- A hypothetical clause is answered "if it occurs", not as an event.
- The historical table states "the N most relevant of TOTAL" — never a count that contradicts the rows.

## The experience (`/workbench`, "The Read")
Opens on a calm welcome (paste a story, or pick one of today's). Reading view: the data's verdict on
the central claim up top, then each claim with its measured verdict (stance dot + legend), an
expandable evidence panel, the collapsible historical record, the public-mood card, and a drill into
the full quant brief. Serif reading type, generous spacing, progressive disclosure.

## Honest limits
Keyword classification can mislabel (shown transparently, per-claim, so it's challengeable). URL
fetch fails on JS-only/paywalled pages (degrades to "read the original"). The engine's "history" is
measured market outcomes over the coded corpus — not a treaties/alliances encyclopedia. Political-
bias labels are a documented gap (licensing wall — see NEWS_LAYER.md).
