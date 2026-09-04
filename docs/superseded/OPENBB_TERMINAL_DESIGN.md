> **SUPERSEDED — NOT A CURRENT CLAIM.** Superseded design and status material for the legacy engine. The authoritative documents are [`README.md`](../../README.md) and [`PAPER.md`](../PAPER.md).

# OpenBB Terminal — product design spec (Gulf Risk)

A final-product-quality OpenBB Workspace terminal for **Gulf geopolitical-risk research**,
built on the ripple engine's data, designed to professional standards *and* to teach a
learner-operator. This is the spec we build against. Design research + OpenBB mechanics
are cited in the commit that added this file.

## Design contract (the non-negotiables)
- **"Overview first, zoom & filter, then details on demand"** (Shneiderman). One glanceable
  overview tab; deep-dives behind it. **Never more than 2 disclosure levels.**
- **The Situation tab passes the 5-second test** — the main read is grasped in ~5s, no
  scrolling, no legend. Top-left = the North Star (reading gravity).
- **≤ 6 widgets on the overview**, 5–7 on deep-dives. Overflow goes to drill-downs, not clutter.
- **No naked numbers / no false precision** — typed buckets, ranges, and fans; match decimals
  to real reliability. "No good analogue / new regime" is a valid, displayable state.
- **Status = colour + sign/arrow + label** (never colour alone — ~8% of men are red-green CVD).
  Semantic axis is **blue↔orange**, not red/green, with sign+arrow redundancy.
- **Every panel answers ONE question**, carries a plain-language header, and a "what this means" line.
- **Surface divergences, never forecast.** Confidence shown honestly (fans/ranges), not decimals.

## Visual system (the professional look)
- **Dark near-black** `#121212` (never pure black — halation). Offer a light toggle later.
- **Semantic colour:** blue = elevated/risk-on, orange/amber = stress, muted green = benign;
  desaturated on the dark field; always paired with sign/arrow/label. Cap the palette at ~6.
- **Typography:** `tabular-nums` on every numeric column (digits align for scanning). One type
  scale; headers front-loaded and skimmable.
- **Charts over tables where a trend matters** (Plotly); **bullet graphs, not gauges** (Few);
  **sparklines-in-cells** for row-level trend; **variance/paired-track charts** for divergence;
  **fan charts** for probabilistic paths.

## Interactivity model — the cockpit
A single **Situation selector** drives the whole board. Mechanics (OpenBB, verified):
- A `type:"endpoint"` dropdown param `situation` on every situation-scoped widget, options from
  a `/situations` endpoint.
- In `apps.json`, one app-level group `{"name":"Situation","type":"endpointParam","paramName":"situation"}`
  and `"groups":["Situation"]` on each widget's layout entry → **pick a situation, the whole tab
  re-reads for it.**
- A global **filter header** (date range, region, actor) carried across tabs (ACLED pattern).
- Table **cell-click grouping** (`renderFn:"cellOnClick"`, `groupBy`) so clicking a chokepoint or
  event drives the linked widgets.

---

## Information architecture (5 tabs, widget-by-widget)

Each widget lists: **[OpenBB type] · engine source · the one question it answers.**

### TAB 0 — SITUATION  (overview · 5-second-readable · ≤6 widgets)
1. **Gulf Risk State** — top-left, largest. `[metric→bullet]` · a new deterministic composite
   (GPR %ile + amplifiers + top-corroboration + divergence, tagged heuristic index) · *"How
   hot is the Gulf right now, vs its own history?"* Plain label ("Elevated · deteriorating").
2. **Direction & horizon** — `[metric]` · attention/divergence trend · *"Getting better or worse,
   over what window?"* (deteriorating / stable / improving + 1–4wk).
3. **The Divergence** (the hero) — `[chart: variance/paired]` · `divergence.json` · *"Where does
   what the engine SEES disagree with what the market PRICES?"* The wedge is the object.
4. **Transmission snapshot** — `[table + sparklines]` · Brent/VIX/chokepoint-flow · *"What's moving,
   which way?"* small-multiple sparklines + arrow + vs-prior.
5. **What changed / top reads** — `[table, columnColor by confidence]` · corroboration + movers ·
   *"What's new and most-confirmed since I last looked?"*
6. **Where We Stand** — `[markdown, Situation dropdown]` · the dossier prose · *"In plain English,
   where are we?"* (built).

### TAB 1 — TRANSMISSION  (analytical · shock → oil → markets)
- **Oil-path fan chart** `[chart]` — base-rate CAR distribution as an asymmetric fan (BoE) · *"If a
  shock lands, what's the range, not the point?"*
- **Propagation heatmap** `[table, columnColor / heatmap]` · cross-asset CAR by event type ·
  *"Which assets move, how much?"*
- **Priced vs. history** `[bullet graphs]` · engine base rate vs market-implied · *"Is the market
  above or below what history says?"*
- **Chokepoint flow** `[chart]` (built) + **Brent** `[chart]` (built).

### TAB 2 — EVENTS & THE WIRE  (operational · details on demand)
- **Corroborated events** `[table, columnColor + confidence sparkline]` · corroboration · sortable.
- **The wire** `[newsfeed]` · alert_queue · *"What's breaking?"* (proper feed, not a table).
- **Event database** `[table]` (built) · the coded, sourced corpus.
- **Situation timeline** `[table]` · the dossier atoms, sourced.

### TAB 3 — STATE & CALIBRATION  (the honest scorecard)
- **Market state @ t−1** `[bullet graphs]` · VIX/inventories/COT vs historical band, point-in-time.
- **Calibration** `[chart]` · reads ledger + corroboration calibration · *"Has the engine been
  right? Where is it over/under-confident?"* (reliability curve, Brier).
- **Amplifier / regime** `[metric]` · H1/H2 ON-OFF + decision-rule status, reported honestly.

### TAB 4 — LEARN & METHOD  (the teachable spine)
- **Read this first** `[markdown]` · a guided walk-through of today's situation.
- **Glossary** `[markdown]` + tooltips-on-hover everywhere (VIX, backwardation, COT, fan chart).
- **Methodology cards** `[markdown]` · how each signal/index is built (state the rule); what
  "no analogue" means; the discipline (buckets not decimals, human gate).
- **The vision** `[markdown]` · GULF_RISK_VISION.md rendered.

---

## Widget upgrade catalog (make the existing ones pro)
- **Metric tiles:** add `delta` (sign/arrow) everywhere; label clearly.
- **Tables:** `columnColor` conditional coloring (confidence, flags), `sparkline` trend columns,
  `formatterFn`/`prefix` for `$`/`%`, `tabular-nums`, pinned key columns, `hoverCard` for detail.
- **Charts:** theme via the passed `theme` param; toolbar config; consistent palette.
- **The wire:** convert the alert table → `newsfeed` widget.
- **raw=true** on chart/html widgets so the copilot can read them.

## Staged build plan
- **Phase A — Foundation & polish** (the pro look): the 5-tab IA in `apps.json`; the **global
  Situation selector** (groups); convert widgets to correct types (metrics w/ arrows, tables w/
  columnColor + sparklines + tabular nums); dark-theme + blue↔orange consistency. *This is where
  it starts to feel like a product.*
- **Phase B — Hero widgets:** the Gulf Risk State composite (bullet), the Divergence variance card,
  the Transmission sparkline panel, the newsfeed wire.
- **Phase C — Depth & teach:** propagation heatmap, calibration tracker, the LEARN tab (glossary-on-
  hover, methodology cards, "what this means").
- **Phase D — AI copilot** *(optional, flagged):* wire Claude as the in-terminal copilot via
  `openbb-pydantic-ai` + Workspace MCP + `raw=true`. **This calls the Anthropic API from the copilot
  backend — a PAID dependency, deliberately outside the free/local engine core.** Do only with
  explicit approval; Claude-for-Chrome (subscription, $0) covers most of this need first.

## Honest notes
- The engine's data is real; some *precise* stats (base rates n=3, corroboration weights) are
  informed-but-uncalibrated — the terminal shows them as buckets/ranges with caveats, per the contract.
- Fan charts / calibration curves need a bit more engine output (distribution, resolved reads) —
  they land in Phase B/C as that data accretes.
- Build order optimizes for *you learning it*: Phase A makes it legible and navigable first.
