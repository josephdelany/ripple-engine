# NORTH STAR — Ground News for the petro economy
*Agreed direction, 2026-09-01. Every build decision is tested against this file.
It sits above RIPPLE_ENGINE_V2_SPEC.md (the mechanism) and BUILD_V2.md (the order).*

## 1. The sentence
**The Ripple Engine is how a financier reads the news about oil, gas, and petro-
products: every story is read against fifty years of measured history and the
live market — each claim scored, every source kept honest, and the engine itself
kept score.**

Ground News tells you whether a story is left or right. This tells you whether a
story is *supported by the record*, whether the market has *already priced it*,
and how often *this kind of claim* — and *this source* — has turned out right.
Not opinion, not sentiment: measured frequencies with n, resolved later, scored.

## 1b. The use: significant things only
This is an instrument for navigating **significant developments** — shocks,
escalations, sanctions regimes, chokepoint threats, OPEC turns, regime shifts —
and the capital decisions they force: sizing or hedging a physical book (crude,
LNG, fertilizer, plastics), holding or cutting exposure through an escalation,
allocating over quarters. It is not for day trading, entries and exits, or
intraday anything. Consequences of that choice, binding on the build:
- **Horizons are weeks to quarters.** Claims resolve at +20/+60 trading days and
  +30/+90 calendar days for escalation. No intraday data, no tick feeds.
- **A materiality gate sits in front of the Feed.** A story reaches the front
  page only if its class historically moves markets more than ordinary
  volatility (the class-CI-clears-baseline-CI test already in `deconstruct.py`)
  or it maps to the situation taxonomy. Everything else goes to a NOISE shelf,
  visible but unranked. The tool ignores most oil news on purpose; that is a
  feature and it is written on the page.
- **Significance is the first field on every story:** MATERIAL / IN LINE /
  NOISE, measured, before any claim is read.
- **Intake stays continuous; attention does not.** The 15-minute watcher keeps
  running so nothing is missed; the front page changes only when something
  material clears the gate.
- **Users are an investment committee and its analysts**, not a screen trader.
  Every page must survive being read aloud in a meeting.

## 1c. Significance is defined by the market, not by us
We do not decide what a "large event" is by coding severity. We ask the record
the other way round: **find every time the market actually changed, then find
what did it.** That set — the Big Moves — defines significance.
- **Big Moves** = episodes in the top tail of measured change since 1987 (and
  1970 where monthly data exist): 20/60-day price moves in the top 5%, curve
  flips (backwardation ↔ contango), volatility-regime breaks, product-spread
  blowouts, and flow drops (production, transits) — per asset, not just Brent.
  Thresholds registered before computing.
- **Attribution.** Each Big Move is joined to the corpus event(s) knowable in
  its window, or marked NO IDENTIFIED EVENT (demand collapses and policy turns
  will dominate — 1986, 2008, 2014, 2020 — and most conflict headlines will be
  absent; that is the finding, published as computed).
- **Two-way base rates.** P(big move | event class) and P(event class | big
  move). The second is what tells a desk which *kinds* of things have ever
  changed this market; the first is what a story's class is worth.
- **The materiality gate is rebased on this.** A story is MATERIAL if its
  decomposed class belongs to the set that has produced Big Moves at a rate
  above the everyday base rate, with n. Not because we called it severe.
- **Big Moves is also the history spine's front door**: a 50-year timeline of
  every time the market changed and what did it, per asset. For a history
  major this is the page.

## 2. The center: the Story Page, as a desk reads it
A financier reading a petro story asks five things in order. The Story Page
answers them top to bottom. Nothing else is on it.

| Desk question | What the page shows | Where it comes from |
|---|---|---|
| **Is it priced?** | What the market has done since the story became knowable vs what analogs did over the same horizon; premium vs realized (flow side beside price side) | live series + ripple graph + analog set |
| **Is the story right?** | The story's checkable claims, verbatim, each with a verdict: SUPPORTED / MIXED / UNSUPPORTED / THIN (n<8) / NO PRECEDENT / UNCHECKABLE — and the numbers behind it | claim extractor (`src/deconstruct.py`, upgraded) + reference classes |
| **What's the tail?** | The conditioned branch table (contained / limited retaliation / widening / deal) with historical frequencies and n; the dated worst cases, always shown | Layer G (spec §4.2) |
| **Where does it travel?** | The propagation hops from the hit asset through the chain — price and flow separately, n on every hop | Layer P (spec §4.3) |
| **How much do I trust this?** | The engine's walk-forward score for this class + each cited source's resolved-claim record | the Ledger (§4) |

Then the analyst's notes and export. Every number one hop from its receipt.

## 3. The Ground News mapping (what we borrow, what we replace)
| Ground News | Ripple Engine | Why ours is stronger |
|---|---|---|
| Story page aggregating outlets | Story page aggregating **claims** about one development | Claims are checkable; outlets are not |
| Bias bar (L/C/R) | **The Record bar**: distribution of what happened after analogs (e.g. Brent +20d: up 9 / flat 8 / down 5, n=22) | Measured, not labeled |
| Factuality rating, imported from third parties (CJR's central critique) | **Track record, measured in-house**: per source and per claim type, from claims we logged and resolved | We generate the rating; nobody sells this for petro |
| Blindspot (covered by one side only) | Two blindspots: **LOUD/QUIET** — big coverage, record says little moves (the quiet set is the seed); **QUIET/LOUD** — thin coverage, record says this class moves markets | Attention vs record is the financier's blindspot, not left vs right |
| Coverage comparison | Claim comparison: outlet A "soaring", outlet B "muted", beside the record and the market | Resolves the disagreement with data |

## 4. The Ledger — the part that compounds
Every checkable claim the engine reads becomes a logged forecast with a horizon
(+5/+20/+60 trading days; +30/+90 calendar days for escalation claims). At the
horizon it resolves from data, never by hand. Three scoreboards grow from it:
1. **Engine vs base rate** — walk-forward G-/P-scores per class (spec §5).
2. **Record vs narrative** — for each resolved story: was the record's read or
   the story's claim closer to what happened? One number a buyer understands.
3. **Sources** — per outlet / analyst / claim type: resolved-true rate with n.
   (Hamilton College scored 472 pundit predictions at coin-toss accuracy; no
   one has done it for oil coverage. This is the moat, and it takes months to
   fill — say so on the page.)
Seed at launch: the 313 corpus events each carry a `source_url` — the narrative
at the time. Claim-extract those articles point-in-time and resolve them against
the measured CARs already in the DB → a "record vs narrative" pilot on day one.

## 5. "Probability" under our rules
We never invent an occurrence probability. We show **reference-class
frequencies**: "13 of 22 (59%) infrastructure attacks on export terminals since
1987 had Brent higher at +20d." The percentage is a count, conditioned and
labeled with its class and n; conditioned subsets flagged when thin. This is the
outside view (Kahneman/Flyvbjerg) and it is exactly what a desk wants from us.

## 6. Ready for anything (live news is unprecedented by nature)
No what-if console. Instead the engine is built so any input gets an honest read:
- **Decompose, don't label.** Unprecedented whole, precedented parts: asset
  role, actor class, chokepoint, output chain. Kharg-with-helium has no analog;
  "export terminal struck by state actor during active campaign" has several.
- **Hierarchical reference classes.** Dyad → asset role → event type → all
  shocks. Fall back one level at a time, flag each fallback on the page.
- **NO PRECEDENT is a first-class page state** — it still shows what the market
  is doing and what is structurally downstream, with no historical magnitudes.
- **Open-set intake.** Unclassifiable items go to a human queue, never forced
  into a type. Intake ≠ corpus (gates unchanged).
Once this holds, a what-if is just a hypothetical claim typed into the same
door ("if Hormuz closes for 30 days") — the extractor already tags hypotheticals.

## 7. The surface (four screens, Ground-News shaped)
1. **Feed** — a market-state strip on top (each asset vs its 50-year
   distribution; "today rhymes with…" analog regimes), then today's material
   stories ranked by the gap between narrative and record, each with its
   significance chip, Record bar, LOUD/QUIET flag, sources. NOISE shelf
   collapsed at the bottom.
2. **Story Page** — §2, top to bottom: significance and why → priced? (price
   path since knowable over the analog fan: median, IQR band, dated tails as
   thin lines; flow series beside) → claims (verbatim rows, verdict chip, Record
   bar, n, "resolves on …") → branches (four-column frequency table, then the
   differencing table) → travels (chain diagram, price/flow per hop) → trust
   (engine class score, source records). Right rail: notes and export. Also the
   paste/URL door.
3. **Big Moves** — the 50-year timeline of every time the market changed and
   what did it; filter by asset and move type; click → event → analogs.
4. **Ledger** — the three scoreboards; record-vs-narrative by year; sources.
Visual language: one recurring glyph, the **Record bar** (a strip showing the
outcome distribution after analogs, tails as dated ticks), used everywhere a
frequency appears; every number carries its n; dark, dense, readable aloud.
Terminal / Trace / Backtest remain deep views. The Desk becomes the Story Page.

## 8. Critical risks (thought through, not hand-waved)
- **Claim extraction is the weak joint.** Articles hedge ("could send oil
  soaring"). Rule: extractive and verbatim only; a claim is checkable only if it
  resolves to asset + direction/magnitude/flow/escalation + horizon; everything
  else is UNCHECKABLE and shown as such. Measure extractor agreement on a small
  human sample; publish the number.
- **The record usually says "muted."** GPR literature: large geopolitical
  spikes are not systematically followed by higher prices; our own H1 died the
  same way. The tool will say UNSUPPORTED to most alarm. That is the product —
  but the page must always carry dispersion and the dated tails (1990, 2022,
  2026) so "muted" never reads as "safe."
- **Empty ledger at launch.** Source scores need months; engine scores exist
  now (walk-forward) and the corpus-article pilot (§4) gives a day-one number.
  Never backfill by hand.
- **Point-in-time or nothing.** Verdicts are stamped with what was knowable;
  outcomes at horizon; nothing edited. Same discipline as the frozen record.
- **Coverage volume needs a source.** LOUD/QUIET requires an attention series
  (GDELT counts, pageviews — already tracked as reference tier, never causal).
- **No edge claim.** The buyer gets a disciplined outside view with a score,
  not a signal. R8 wording stands.

## 9. Gap between today and the north star
Built: extractive claims + magnitude verdicts (`deconstruct.py`), Desk paste
door, Question view, corpus 313, watcher, backtest console, integrity regime.
Missing, in build order: claim typing + horizon + logging/resolution (the
Ledger) · conditioning fields + Layer G · Layer P per branch · feed ranking by
narrative-vs-record gap with attention series · walk-forward stamps · Story
Page/Feed/Ledger surfaces · corpus-article pilot · deep history to 1970.
