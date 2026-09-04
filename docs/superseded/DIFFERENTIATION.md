> **SUPERSEDED — NOT A CURRENT CLAIM.** Superseded design and status material for the legacy engine. The authoritative documents are [`README.md`](../../README.md) and [`PAPER.md`](../PAPER.md).

# DIFFERENTIATION — where this engine sits, and why it's not another risk score

> **SUPERSEDED — 2026-09-03.** This document dates from the project's v1 period (July
> 2026) and describes a "validated" portfolio that no longer exists. Every claim it calls
> validated has since been retracted or downgraded, each by a test registered before it
> ran: **H1** — geopolitical shocks amplifying ~5pp harder under volatility stress — did
> not survive a VIX-matched placebo (`docs/red_team_1.md`); **five of the six**
> stress-amplification propagation edges were retracted under a pre-registered re-test
> (`data/ripple/retraction_six.json`); the propagation chain is silent, with 21 of 477
> cells transmitting against 1–24 expected by chance (`docs/RIPPLE_FINDINGS.md`); and the
> walk-forward engine is significantly **worse** than the base rate on both targets once
> the vintage rule binds (`docs/PAPER_DRAFT.md` §8).
>
> Nothing below has been edited. This project annotates its record; it does not rewrite
> it. For the current state read `README.md`, `docs/PAPER_DRAFT.md` and `EDGE_PORTFOLIO.md`.


*The honest landscape, the whitespace, and the moat. Written to be handed to a quant.*

---

## 1. The field (who already does geopolitics → markets, and how)

| Player | What it is | How it works |
|---|---|---|
| **GPR Index** — Caldara & Iacoviello (Federal Reserve) | The canonical academic geopolitical-risk measure | Newspaper-text **count** of adverse-event articles, monthly/daily, split into Threats vs Acts |
| **GeoQuant** (acquired by **Fitch**, 2022) | Commercial political-risk data | ML over ~3,000 articles/day + structural data → a **0–100 risk score** per country, 146 countries |
| **RavenPack** | News-analytics feed for quants | NLP sentiment/event tags on news; **~70% of top quant funds** consume it for event-driven signals |
| **BlackRock Geopolitical Risk Dashboard** | Buy-side risk monitor | Market-attention + analyst scoring of macro geopolitical risks |
| **Predata / Dataminr / Kensho** | Attention / early-warning / NLP | Web-attention nowcasting, real-time event detection, NLP over filings/news |

**The shared shape:** they measure **attention** (how much the world is talking about a risk) and emit a **score**. That's the product.

## 2. Their flaws — documented, not my opinion

1. **Attention ≠ consequence.** The attention score "depends heavily on media and analyst coverage, which can be driven by noise as much as by substance… sudden news spikes [do] not necessarily reflect real changes in underlying probability." A spike in coverage is not a spike in *priced consequence*.
2. **Conflated event definitions.** Existing indicators have "unclear definitions… that conflate very different events ranging from wars to economic crises to climate change" — poorly suited for clean empirical analysis.
3. **Black-box scores.** GeoQuant's 0–100 is an ML output; you cannot trace *why*, cannot see the mechanism, cannot see what it rejects.
4. **Crowding / alpha decay.** Once ~70% of top funds run the same RavenPack feed, "the edge disappears." Widely-used signals decay by construction; the advantage is in *novel combination*, not the raw feed.
5. **Shallow / hidden calibration.** "The fact that a model is calibrated says little about the potential impact"; and political-risk strategies have shown a "picking up pennies in front of a steamroller" payoff that discourages active portfolio use.
6. **No honest nulls.** None of them publish what they *couldn't* validate. The failures are invisible — which is exactly where over-confidence hides.

*(Sources: Caldara-Iacoviello / Fed IFDP 1222 & AER 2022; ECB Economic Bulletin 2023 & CEPR on geopolitical oil shocks; CB Insights / Fitch on GeoQuant; RavenPack; BlackRock dashboard critique; academic notes on risk-score calibration limits.)*

**Important honesty:** the academic literature (ECB, CEPR, and GPR-based studies) has **already established the core finding** — geopolitical shocks move oil, and hit harder in some market regimes. So the *idea* is not novel. What's missing from the *products* is the honest, calibrated, consequence-and-gap layer.

## 3. The whitespace (what nobody ships)

A shock lands. The incumbent tells you *"geopolitical risk is elevated (score 74)."* It does **not** tell you:
- **the consequence** — how oil (or gas, or the peg) has historically rippled *given a shock like this, in a market state like today's*, with a confidence interval;
- **versus what's already priced** — is the market *under-* or *over-*reacting? (the gap);
- **how sure, and why** — the receipts: the sourced events, the mechanism, the out-of-sample validation, the multiple-testing correction;
- **a scored track record** — were its past gap calls right? (a public, regime-stratified Brier);
- **what it can't stand behind** — the standing list of hypotheses it *rejected*.

That gap-shaped, glass-box, calibration-first space is open — and it's precisely what a black-box attention-score *structurally cannot* occupy.

## 4. The moat — four pillars this engine is built on

1. **Consequence conditioned on state, vs the priced gap (market-as-null).** The engine's validated core (H1): geopolitical shocks ripple ~5pp harder into oil when VIX stress is elevated (CI excludes zero, survives Bonferroni, confirmed walk-forward). It then compares that consequence to what the market has priced and surfaces the **gap** — not a risk score.
2. **Cross-modal corroboration.** Confidence comes from *convergence* across **news + physical ship-transits (PortWatch) + thermal fires (FIRMS) + prediction-market odds** — physical confirmation, not text attention alone. This directly answers flaw #1.
3. **A live, resolving, calibrated track record.** Every read/gap is logged, resolves at horizon, and is Brier-scored by regime. The engine publishes its own accuracy — including where it's wrong.
4. **Glass-box + honest nulls.** Every number traces to a sourced event and a stated mechanism; every claim carries its CI, FDR, and PBO; and the signal registry openly lists **1 live edge and 6 rejected nulls**, status *derived from the evidence, not asserted*.

**The strategy in one sentence:** *don't out-scale the incumbents (impossible solo/$0) — out-honest and out-explain them on the axis they're structurally weakest on.*

## 5. Honest self-assessment (say this before they have to)

**What it is:** a rigorous, reproducible, point-in-time research engine with **one** validated edge and a full anti-overfitting harness (pre-registration, purged CV, PBO, Diebold-Mariano, FDR, walk-forward). The methodology is at graduate/professional level; parts (purged CV, PBO, pre-registration, the *caught false discovery*) exceed typical academic work.

**What it is NOT:** production alpha. It's small-N (~90 clustered episodes), largely single-asset (oil), and the one edge is modest and weakens under volatility-standardization. It won't match GeoQuant/RavenPack on coverage, data scale, or latency.

**Where it genuinely wins:** honesty, explainability, calibrated consequence, and the priced gap — the things allocators and intelligence clients increasingly demand and the black boxes can't provide. It is the *glass-box* the black boxes can't be.

## 6. The positioning line

> "Everyone else scores geopolitical **attention**. This scores the **consequence versus what the market already priced** — the gap — and keeps a public, calibrated record of those calls, with every number traceable and a standing list of what it couldn't validate. It's the glass-box the black boxes can't be."

---

*This document is the engine's north star: every feature we add must make a claim **open more honestly, resolve more truthfully, or score more usefully** — otherwise it's just another score, and the world has enough of those.*
