# The Desk — front-end specification

*Written as if handing it to a studio to build exactly as intended. It is opinionated on
purpose. Everything here obeys the house rules: local, $0, keyless, and it never fabricates
a fact or a number.*

## The one-line brief
Build the screen where I turn today's news into published, numbers-backed analysis: I see
the real articles, the engine's quantitative read sits beside each one, I write my take, and
I export it — without leaving the page, and without the tool ever inventing a fact or a figure.

## Who I am at this screen
An analyst who publishes market commentary (Substack, notes to a principal). Every morning I
must: scan what happened, know what history and the market say about it, form a view, and write
it with receipts. News desks (NYT, Al Jazeera) give me the story; quant desks give me the
numbers; nobody fuses them. This screen is that fusion — and the fusion *is* the product.

## The daily loop (four moves)
1. **SCAN** — today's oil-relevant articles, each already pre-read by the engine.
2. **OPEN** — pick one (or paste/search one); see the source and the engine read side by side.
3. **SYNTHESIZE** — write my take beside the numbers; pull the figures in.
4. **PUBLISH** — export a clean, sourced draft.

## How articles get in — the answer to the sourcing question
Three intake modes, unified into one "Sources" column. All three operate on **real articles**;
none does a paid/keyed live web search.

- **TODAY (the feed).** Real articles the engine already ingests every cycle from real outlets
  (Al Jazeera, BBC, UN, Reuters-style energy wires: oilprice, gCaptain, FreightWaves, EIA),
  filtered to oil-relevant and ranked by materiality. Each row: source, time, event-type,
  one-line engine read, read/unread. This is "wake up and scan."
- **SEARCH.** Search the **ingested article archive** (the watcher's durable feed — thousands of
  real items) by words / entity / date / source. Instant, $0, because it searches what has
  already been aggregated, not the live web. Returns real articles with working links.
- **PASTE / URL.** A box for any headline, paragraph, or article URL. A URL is fetched (keyless)
  and read.

> Decision: **not** a live web-search platform (that needs a paid news API and breaks $0/keyless).
> The engine already aggregates free RSS; "search" searches that archive. It is the honest,
> zero-cost version of what you asked for, and it is instant.

## What you see when you open an article — and the honest answer on "AI summaries"
The center shows the STORY and the READ, side by side.

**THE STORY** — real headline, source, timestamp, a **"read the original ↗"** link to the actual
page, and a **SOURCE EXTRACT**: the article's own lede plus the sentences that mention the
entities the engine matched. It is *extractive* — real sentences lifted verbatim from the real
article, labelled "from the source" — never a machine paraphrase.

**Why not a generative "AI summary":** the engine's entire credibility is that it does not make
things up. A generative summary can hallucinate a detail that isn't in the article — the single
fastest way to lose a serious reader (and the exact "AI slop" we're defined against). So the
article summary is a truthful excerpt with a click-through to the source, and the **"AI analysis"
is the engine READ** — the deterministic, receipted brief, which is the real intelligence. If a
true generative summary is wanted later, it is a deliberate decision requiring a free model
endpoint and an ADR accepting the fabrication trade-off; the seam is left for it, but it is not
the default, and I recommend against it for a head-of-state audience.

**THE READ** — the brief: bottom line, the significant charts, precedent, market state, the
engine-vs-market gap, synthesis, decision read, receipts.

## The graphs — every chart earns a decision (the significance rule)
No chart that doesn't change a decision. Decorative sparklines are cut. The set:

1. **THE RIPPLE** — the CAR curve: how Brent actually moved over the 20 days around events of
   this class, with its dispersion band. The core measurement; the hero.
2. **IS THIS BIGGER THAN NORMAL?** — the magnitude-vs-baseline view: this class's typical move
   marked on the distribution of *ordinary* 20-day moves. It answers the one question that
   decides whether the story matters at all — material signal, or everyday churn. (New.)
3. **WHERE ELSE IT HITS** — cross-asset bars: the same shock measured in gas, the dollar, gold,
   equities, rates (% and bps on separate scales).
4. **PRECEDENT DISPERSION** — the individual real analog events plotted by their measured move,
   so the range and the outliers are visible, not hidden inside an average.

## Screen anatomy (three columns, terminal-grade)
- **MASTHEAD** — identity, date + data-as-of (with a stale flag), live regime chips (market
  stress, geopolitical risk, engine-vs-market gap), and a global command box (paste/search).
- **LEFT — SOURCES** — tabs Today / Search / Paste; a dense, scannable list of real articles.
- **CENTER — THE BRIEF** — the story (excerpt + link) above the read (charts + analysis).
- **RIGHT — NOTES & DRAFT** — the writing pane, "insert brief," export to sourced markdown.

## Interaction & feel
- Instant: click an article → brief in <1s; search is live-as-you-type.
- Keyboard: `j`/`k` move through the feed, `Enter` opens, `/` focuses search, `⌘P` prints.
- States: skeletons while loading; honest empty/error; never a broken half-screen.
- Print/PDF: a clean, ink-on-paper research note for presenting.
- Local, $0, keyless, deterministic, no fabrication — on every screen.

## Non-negotiables (so a future change can't quietly break the product)
- Every number one hop from a stored computation; every article a real, linked source.
- The article "summary" is a verbatim extract, never generated prose.
- Expected magnitude, never an occurrence probability; association, never cause.
- A story that doesn't classify is a documented gap, not a fabricated read.
