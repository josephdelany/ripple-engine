# Gulf Risk Vision — the north star

A research instrument for **Middle Eastern / Gulf geopolitical risk** — from war to
financial markets — that senses, corroborates, prices, and explains, to give an
**ahead-of-consensus** read. Free/local brain, OpenBB cockpit, Claude analyst.

## What it answers, continuously
1. **What's happening?** — multi-source sensing (news, ships, satellite fire, conflict, attention, social).
2. **Is it real?** — corroboration: independent modalities converging (news + physical flow + thermal).
3. **What's it worth?** — transmission: how a shock ripples into oil, Gulf equities, FX pegs, sovereign spreads, safe havens.
4. **What does history say, and what's already priced?** — base rates vs. prediction-market odds. **The gap is the edge.**

The differentiator vs. a Bloomberg terminal or a consensus desk: it fuses **ground-truth
OSINT + market-priced probability + historical base rates + a calibrated track record** —
and it explains its reasoning, is reproducible, and is yours.

## The three layers (keep them distinct — this is what keeps it coherent)
| Layer | Role | Where it lives |
|---|---|---|
| **The Brain** | ingest → enrich → corroborate → calibrate → intelligence | the ripple engine (free, local, GitHub Actions) |
| **The Cockpit** | charts, dashboards, interaction, native market data, copilot | OpenBB Workspace |
| **The Analyst** | read the brain, write the read, answer why, draft the brief | Claude (MCP + Chrome) |

OpenBB is the **instrument panel, not the aircraft.** If OpenBB vanished the engine still
runs, notifies, and publishes. The rigor (event-study, pre-registration, corroboration,
no naked numbers, human gate) stays in the engine. OpenBB + Claude are presentation +
judgement ON TOP of it. Free/local core, always; OpenBB Pro + Claude are the paid
*surfaces you already have* — the intelligence stays $0 and yours.

## Organizing principle: SITUATION-centric, not asset-centric
Gulf risk is a **portfolio of live situations** (Israel–Iran war, Houthi/Red Sea, Iran
nuclear, Saudi domestic, OPEC+), each with its own arc, actors, and market channels. Each
is a **Situation Memory dossier** carrying timeline, corroboration, priced odds, and
market transmission. The cockpit is a **situation switcher** — pick a situation, the whole
dashboard re-reads for it. This is what makes it *ours*, not a generic terminal.

## The transmission surface (war → markets)
A single shock reads across every channel at once, conditioned on state + corroborated:
- **Oil complex** — Brent/WTI, crack, chokepoint flow, fundamentals (have).
- **The peg-break tail** — USD/SAR, USD/AED forwards (under-watched fear signal).
- **Sovereign stress** — Saudi/Qatar/Bahrain CDS + bond spreads (contagion channel).
- **Regional equities** — Tadawul, ADX/DFM, defense names, gold/safe-havens.
That cross-asset ripple IS the product.

## Using OpenBB's full power (not static tables)
- **Parameterized widgets** — a **Situation selector** dropdown that drives the dashboard. *(The cockpit move.)*
- **Metric widgets** — a top **risk-gauge row** (escalation, Hormuz status, amplifiers, market-implied P, top corroboration).
- **Markdown widgets** — the **"Where We Stand" dossier rendered as prose**, not a table.
- **Charts (Plotly/Highcharts)** — the visual layer (have: Brent, transits, attention).
- **Newsfeed** — the live wire.
- **Widget grouping** — one selection updates linked widgets.
- **Pluggable copilot** — via `openbb-pydantic-ai` + Workspace MCP + `src/mcp_server.py`, the
  in-terminal copilot becomes Claude reading the engine; **Claude for Chrome** is Claude
  beside the terminal seeing the rendered page ($0, subscription).

## Why it's a RESEARCH tool (not an alert box)
Every number carries its **mechanism, base rate, history, and confidence** — so you don't
just see "Hormuz elevated," you see *why it matters, what it's done before, how sure we
are.* The engine enforces this; OpenBB surfaces it; Claude explains it.

## Roadmap
- **Phase 1 — DONE:** oil-ripple engine · 7 modalities · corroboration · calibration · a real OpenBB app (apps.json, 3 tabs).
- **Phase 2 — the cockpit (building now):** Situation selector (parameterized widgets) · risk-gauge metric row · dossier-as-markdown · AI-readable widgets.
- **Phase 3 — the full surface:** broaden transmission to Gulf equities / FX pegs / sovereign CDS · add situations (Nuclear, Succession, OPEC+).
- **Phase 4 — the analyst loop:** the daily Gulf brief (synthesizer) · calibrated track record surfaced · ahead-of-consensus "gap" alerts.

## One-sentence version
*The ripple engine is a Gulf-risk brain that senses, corroborates, and prices geopolitical
shocks; OpenBB is its cockpit; Claude is its analyst — together, an ahead-of-consensus
research instrument for everything from a Hormuz incident to a peg-break scare.*
