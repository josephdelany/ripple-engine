# STORIES HUB — the operating plan
<!-- Synthesized 2026-07-28 by a 9-agent workflow (mine Frontier Alpha -> frame -> judge ->
     synthesize), curated by Claude. Supersedes the daily-brief framing. This is the
     definitive next-steps document for turning the ripple-engine into Joe's living
     stories-intelligence hub. The core reframe: the GAP is the atom; the STORY is the view. -->

This is a strategy/planning document task. The chief-strategist verdict, mining catalogue, and repo assessment are all provided in context — I have what I need to write the definitive next-steps document. I'll return it directly as my final response (no file writing per instructions).

# THE MASSIVE PLAN — Joe's Stories-Intelligence Hub

*Built on the disciplined ripple-engine core. Mining the best of Frontier Alpha. $0, honest, buildable. The definitive next-steps document.*

---

## 1. THE CONCEPT

A **stories-intelligence hub** where the world is not a feed of headlines but a small set of **living stories** — persistent, named subgraphs of entities, causal chains, and priced beliefs that Joe tracks over time. Each story is organized around one falsifiable spine: **the Gap** — a timestamped, Brier-scored micro-prediction that says *the market is wrong here, this is why, and here is the ledger of my being right.* Stories are the human-readable explanation; Gaps are the load-bearing edge. The hub reads the world, flags where reality has moved while priced belief is stale, narrates the mechanism, invites Joe's own conviction against the engine's, and scores everyone honestly. It is an *anticipation-with-a-track-record* instrument, not a newsreader — and every claim on its surface has already been, or will be, scored.

---

## 2. THE CORE ABSTRACTION

**A GAP is the atom.** Everything else is a view onto, an explanation of, or a track-record over Gaps.

```
GAP = {
  reality_signal:   moved   (GDELT / PortWatch / FIRMS / EIA / GPR)
  priced_belief:    stale   (Polymarket / Kalshi / oil curve / COT)
  divergence:       typed   (pricing | positioning | attention | consensus | structural)
  opened_at:        real timestamp (event-triggered, never daily)
  engine_prob:      deterministic (analogue.py + divergence.py — never LLM)
  joe_prob:         Joe's bucketed conviction (graft from apprentice framing)
  lens_tag:         Joe's reasoning mode (free tag, not yet analyzed)
  lifecycle:        opened → {repricing | resolved | defeated}
  brier:            scored on resolution, for BOTH engine and Joe
  provenance:       source_url + retrieved_at on every input
}
```

A Gap **cannot exist without a priced belief to diverge from** — this enforces market-as-null structurally, not by convention.

**A STORY is the secondary object — the explanation a Gap points to.** A story is a persistent named subgraph: `{entities + edges + attached events + the LLM-authored prose read}`. Stories are the *click-through*, never the *front door*. When you open a Gap, the Story is the cast, the sourced causal chain, and the mechanism narrative behind it. Stories map cleanly onto the Narrative/Regime spec: the **regime** (VIX/EIA/COT state) is the weighting-world a story lives in; the **narrative** is the prose read; the **subgraph** is the propagation graph (`propagation.py` + 13 sourced chains).

**Portfolios and hypotheses:** A *portfolio* is a filtered set of open Gaps (two-sided: "Overpriced Fear" vs "Underpriced Risk"). A *hypothesis* is a Gap before it has a resolution — Joe logs one by recording `joe_prob` + a falsifiable resolution condition. Resolution scores the hypothesis. The ledger of resolved hypotheses **is** the portfolio artifact Joe hands an interviewer.

---

## 3. THE ARCHITECTURE

Five layers, each powered by modules that already exist:

| Layer | What it does | Current ripple module | Grafted Frontier Alpha IDEA (never code) |
|---|---|---|---|
| **SENSE** | Ingest reality + priced belief | `fetch_*.py` (Polymarket 185, GDELT, PortWatch, EIA, GPR, FIRMS, COT) | *Curated forward-catalyst calendar* (`catalyst_engine`) → scheduled-vs-surprise tag |
| **CORROBORATE** | Weight-of-evidence, dedup, source-tier | E3 corroboration scaffold, `derive_signals.py` | *Source-tier decaying battery* (`signal_accrual`); *both-channels-fire geometric-mean gate* (`macro_threat_detector` / SCE) |
| **REASON / ENGINES** | Deterministic divergence + analogue + propagation | `divergence.py`, `analogue.py`, `propagation.py`, `criticality.py`, `backtest_analogue.py` | *Shock→price-**band** with inventory-runway* (`supply_chain_model`) as prior only; *pattern+precedent records* (`pattern_memory`) |
| **STORIES SYNTHESIS** | Assemble Gaps into named stories; LLM writes prose | `reads/*.md`, `situation.py`, MCP server | *Named-pattern vocabulary* (PatternBoard: deep-value / regime-transition / crisis-alert); *MACRO→ENTITY→INSTRUMENT causal drill-down* (AlphaSynthesisPanel) |
| **SURFACE / QUERY** | Two-column gap board + Brier ledger; Claude queries | `backend.py` (32 endpoints), `mcp_server.py`, `the_brief.html` | *Signed mispricing gap as hero metric*; *regime ribbon*; *progressive disclosure in place*; *source-tier badges everywhere* |

**Everything stays $0.** SQLite + sqlite-vec (installed) + numpy/pandas. LLM = Joe's subscription, extraction+synthesis prose ONLY, never scoring. The single new dependency: a free local **embedder** (`sentence-transformers` pip add) to light up analogue retrieval and subgraph semantic matching. That is the one flagged decision.

---

## 4. THE OPERATING MODEL

**Joe's day-in-the-life:**

1. **Notification** (real event-trigger only — "a Gap opened," never a fake daily tempo). Reality moved on a tracked subgraph and priced belief hasn't caught up.
2. **Open the hub.** Two-column board: *Overpriced Fear* | *Underpriced Risk*, sorted by divergence magnitude. Regime ribbon at top: `REGIME: high-VIX | inventories tight | COT crowded long`.
3. **The read.** Click a Gap → the Story. Three things, in order: **system impact** (the causal chain, MACRO→ENTITY→INSTRUMENT, sourced), **what markets miss** (the priced belief that's stale + why), **what's next** (the falsifiable call + resolution window from `transmission_windows.json`).
4. **Query.** Joe asks Claude (via MCP): *"closest historical analogue to this subgraph — what did oil/SPX/yields do?"* Grounded, cited, caveated answer from the 511-shock memory.
5. **Log a hypothesis.** Joe records his own bucketed conviction (`joe_prob`) beside `engine_prob`, tags his reasoning lens, sets the resolution condition. One row. Both get scored on resolution.

**Autonomy + division of labor:**
- **Deterministic engine (Python):** all scoring, divergence math, analogue kNN, Brier — the unfabricatable spine. Runs headless on a GitHub-Actions refresh loop.
- **Caged LLM (subscription):** extraction of typed observations + synthesis prose for the Story read. Never touches a number that becomes a score.
- **Joe (judgment):** conviction, hypothesis logging, story naming, gated network growth.
- **The driver (orchestration):** the workflow that fans out sense→corroborate→reason→synthesis and writes surface JSON.

---

## 5. THE ROADMAP

Staged $0 sprints, each shippable, each with a definition-of-done that **makes a Gap better** — not a new widget.

**Sprint 0 — Finish the registered run.** Load VIX + EIA + COT together, run H1–H3 once, record the verdict. *DoD: the pre-registered result exists and is honestly reported (pass or null). Nothing new wires in until this is done.*

**Sprint 1 — Promote the Gap to a first-class DB row.** `gaps` table with the full lifecycle schema (§2). `divergence.py` output stops being a paragraph, becomes a tracked object. *DoD: a Gap can be opened, persisted, and queried with provenance.*

**Sprint 2 — The resolver + Brier ledger.** Resolution conditions, point-in-time scoring, `engine_prob` scored on resolution. *DoD: a resolved Gap carries a real Brier score; the ledger renders.*

**Sprint 3 — Retrodiction drills (the honesty bootstrap).** Seed the ledger with masked historical cases from the 511-shock library, scored point-in-time, for the engine. *DoD: a non-empty track record exists on day one, before live Gaps age.*

**Sprint 4 — Joe's conviction column.** `joe_prob` + `lens_tag` on every Gap; same resolver scores both. *DoD: the ledger shows Joe-vs-engine, both Brier-scored.*

**Sprint 5 — The two-column surface.** Overpriced Fear | Underpriced Risk board + regime ribbon + source-tier badges + progressive-disclosure drill into the Story. *DoD: Joe can open→read→query→log without page churn.*

**Sprint 6 — The embedder + analogue retrieval.** `sentence-transformers` add; populate sqlite-vec; "closest subgraph analogue" query via MCP. *DoD: a Gap carries its cited historical analogue with honest "no good analogue" fallback.*

**Sprint 7 — Stories as tracked subgraphs.** Named persistent subgraphs that light up as observations hit their nodes. *DoD: a Gap's Story shows its subgraph and its recent activity — as drill-down, not front door.*

---

## 6. THE CREATIVE LEAPS

1. **Stories as evolving subgraphs.** Consensus tracks headlines as discrete; you track the connected structure over time, so you see a subgraph *lighting up* (fresh observations hitting its nodes) before it's a headline. A query pattern over `entities`+`edges`+`event_entities`, not new infrastructure.

2. **Causal-chain diffs over time.** Snapshot each Story's chain at open; on every refresh, diff it. *"Three days ago this chain ran chokepoint→tanker-rates→Brent; today ammonia→food priced in too."* The diff — what got added to the transmission path — is itself a signal, and it's free.

3. **The self-scoring hypothesis engine.** The engine proposes a Gap *and its own `engine_prob`*, then the resolver grades it. Not an LLM guessing decimals — deterministic analogue math making a falsifiable call and eating the score. Over time the ledger reveals *which divergence types the engine is actually good at.*

4. **Cross-story contagion.** When two Stories share an entity or edge, a Gap opening in one raises a watch-flag on the other. Borrow the SIR *framing* from Frontier Alpha's Contagion Network — **framing only, never its invented 0.30/0.25 edge weights.** Let resolved Gaps eventually calibrate whether contagion flags earn their keep.

5. **Joe's calibration mirror.** `joe_prob` vs `engine_prob`, both scored, reveals where Joe beats the machine and where he should defer — a learning loop that is also the strongest job artifact: *"here is my scored record of being right about mispricings, built on a disciplined engine."*

---

## 7. ANTI-SPRAWL GUARDRAILS

**The discipline:** *Nothing surfaces as edge until it is scored. The Gap ledger earning trust IS the roadmap.* No naked numbers, buckets not decimals, real timestamps only, every input carries `source_url` + `retrieved_at`.

**The kill-list — we will NOT build:**

- **"Story births" / dormant-subgraph anticipation.** An engine inventing new stories from graph activity while the predictive spine scores −0.16 — the exact old failure mode (confident narrative on unproven math). Cut entirely until Gaps beat base rate.
- **Lens-decomposed calibration analytics.** "Does Joe's game-theory brain beat his probability brain" needs dozens of resolved bets per lens — a year of data. Record the lens as a free tag; build nothing on it until n justifies it.
- **The full narrative-terminal UX.** No 22-page Bloomberg cosplay, no P&L/VaR trading desk Joe doesn't use, no cast-panel theater. Ship the two-column board + Brier ledger. Earn the terminal.
- **Any fake liveness.** No "3 gaps opened today" unless 3 gaps opened. Fake tempo is the fastest way to make an honest engine lie.
- **Hardcoded transmission coefficients.** Take `supply_chain_model`'s band+runway *structure* as a prior; let the event-study estimate the number. Never ship the 0.8/1.5.
- **LLM-in-the-scoring-path.** Ever. Extraction and prose only.
- **Parallel DBs / new tables without approval.** One `data/oil.db`. New data = new rows via small adapters.

**The one-line test for every proposed feature:** *Does this make a Gap open more honestly, resolve more truthfully, or score more usefully?* If not, it is Frontier Alpha 2. Don't build it.
---

## Appendix — chief-strategist verdict (the reasoning behind the pick)

I'll judge these on their merits without needing to inspect the repo — the framings themselves carry the decision, and the CLAUDE.md constraints are the scoring rubric. Here is my ruthless verdict.

---

# VERDICT: Framing 2 (Mispricing-First / Gap Engine) is the PRIMARY

It is the only framing whose hero object *is* the thing the disciplined core already computes, and the only one that survives all three tests without special pleading.

## Why 2 wins on the three tests

**(1) VALUE to Joe.** The analyst job is won by one demonstrable skill: *"here is where the market is wrong, here is why, and here is my scored record of being right about it."* Framing 2 makes that the literal product surface. A Gap is a falsifiable, timestamped, Brier-scored micro-prediction — that IS a portfolio artifact you hand an interviewer. Framing 1 (stories) produces a beautiful narrative terminal but its deliverable is *prose about subgraphs*, which reads as opinion, not edge. Framing 3 (apprentice) produces the best *learning* artifact but the weakest *job* artifact — "a mirror of my own reasoning" is a diary, not proof of an ahead-of-consensus read.

**(2) ACHIEVABILITY at $0 on the ripple core.** This is decisive. The Gap is `divergence.py` output — it already exists in the disciplined core. Framing 2 is the *smallest diff from what's built*: promote the gap from a paragraph to a first-class, lifecycle-tracked DB row. Framings 1 and 3 both require net-new heavy machinery (a Story object graph with "story births"; a reasoning-lens-decomposed calibration system needing retrodiction drills) that is exactly the kind of speculative build the CLAUDE.md anti-sprawl rule and the "predecessor died of sprawl" warning forbid.

**(3) TRUTH to Joe.** Event-driven, not daily: a Gap opens when reality moves — inherently event-triggered, and Framing 2 is explicit about "real timestamps only, no fake liveness." Honest/calibrated: Framing 2 is the *only* one whose novel leap IS the calibration mechanism — "a Brier-scored ledger of the engine's disconnect-calls." It doesn't bolt honesty on; honesty is the product. Critically, all three framings name the *same* fatal risk (analogue skill −0.16, calibration n=0), but only Framing 2 makes confronting that risk the load-bearing feature rather than a mitigation footnote. That is the correct relationship to your worst number.

## The one abstraction that organizes everything

**The GAP as a pre-registered, lifecycle-tracked, Brier-scored micro-prediction.**

`{reality_signal moved} − {priced_belief stale} → typed divergence → opens → {repricing | resolved | defeated} → scored.`

Everything else is a view onto, an explanation of, or a track-record over Gaps. This abstraction is right because it is simultaneously the hero metric, the falsifiable unit, the calibration atom, and the job-portfolio artifact — one object doing all four jobs. It also enforces the market-as-null discipline structurally: a Gap cannot exist without a priced belief to diverge from.

---

## GRAFT from the others (the best product is a hybrid)

**From Framing 1 — the STORY as the explanation layer, demoted to secondary.** Framing 2 already concedes this ("A STORY is the secondary object... the causal explanation a Gap points to"). Keep it exactly there: a Story is the click-through subgraph that *explains* a Gap — the cast, the sourced chain, the LLM-authored prose read. Do NOT let it be the entry point. Graft the "subgraph lights up" visual as the *drill-down*, not the *front door*.

**From Framing 3 — Joe's estimate versus the engine's, on the resolved Gap.** This is the single highest-value graft. When a Gap opens, let Joe record his own bucketed conviction alongside `engine_prob`, and score *both* on resolution. This turns the Gap ledger from "the engine's track record" into "Joe's track record built on the engine's substrate" — which is a far stronger job artifact and learning loop, at near-zero marginal build cost (one column, same resolver). It converts the apprentice's whole value proposition into two fields on the object you were already building.

**From Framing 3 — retrodiction drills to bootstrap calibration.** Steal this as the *answer to Framing 2's own biggest risk*. n=0 calibration and slow-aging forecasts mean the live ledger is empty for months. Seeding the record with masked historical cases from the 511-shock library — for both engine and Joe — is the honest way to have a track record before live Gaps resolve. This is the mitigation Framing 2 lacked and Framing 3 supplied.

---

## Do NOT build (anti-sprawl kill-list)

- **"Story births" / dormant-subgraph anticipation (Framing 1's novel leap).** This is the most seductive and most dangerous item — an engine proposing new stories from graph activity, while the predictive spine scores −0.16. It manufactures confident narrative on unproven math: the exact old failure mode. Cut it entirely until Gaps beat base rate.
- **Reasoning-lens decomposition of calibration (Framing 3's novel leap).** "Does his game-theory brain beat his probability brain" needs *dozens of resolved bets per lens* — a year-plus of data, by Framing 3's own admission. Building the decomposition machinery now is scaffolding for data that doesn't exist. Record the lens as a tag on each Gap (free), but do not build the decomposed analytics until n justifies it.
- **The full "portfolio of live narratives" terminal UX (Framing 1).** Regime ribbons, cast panels, story-as-position metaphor — this is a lot of surface for a system whose core claim isn't validated. Ship the two-column gap board (Overpriced Fear / Underpriced Risk) and the Brier ledger first. Earn the terminal.
- **Any daily-liveness affordance.** No "3 gaps opened today" unless 3 gaps actually opened. Fake tempo is the fastest way to make an honest engine lie.

---

## One-line summary for Joe

Build the **Gap** as a first-class, Brier-scored, lifecycle-tracked micro-prediction (Framing 2); make **Stories** the click-through explanation and **your own conviction vs. the engine's** two extra fields on every Gap (grafts from 1 and 3); seed the ledger with **retrodiction drills** so it has a track record on day one; and refuse to build **story-births** or **lens-decomposed calibration** until resolved Gaps prove the spine beats base rate. The gap ledger earning trust *is* the roadmap — nothing surfaces as edge until it's scored.