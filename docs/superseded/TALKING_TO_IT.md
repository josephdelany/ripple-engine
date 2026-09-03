# TALKING TO IT — how to text Claude and use the engine

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


Your primary interface is a conversation with Claude (Desktop, with the MCP server connected). You ask
in plain English; Claude calls the right read-only tool and hands you the engine's **raw material** —
tiered, receipted, honest. **The engine never writes your read. You do.**

## One-time setup (≈5 min, keyless)
1. `pip install mcp` (once).
2. In Claude Desktop → Settings → Developer → Edit config, add under `mcpServers`:
   ```json
   "ripple-engine": { "command": "python3",
     "args": ["/Users/default/Documents/Claude/Projects/News to Markets/ripple-engine/src/mcp_server.py"] }
   ```
3. Restart Claude Desktop. Ask *"list the ripple-engine tools"* to confirm. (Details: `ops/MCP.md`.)

## The cookbook — say this, get that
| You say | Tool that fires | What comes back |
|---|---|---|
| **"Orient me on the Middle East right now"** | `orient_on_topic("middle east")` | regime + validated edges + live gap + corroborated situations + coverage gaps + receipt ids — everything to start a read |
| "What should I watch on shipping / commodities / macro?" | `orient_on_topic("shipping")` | same, scoped to that domain |
| "Does VIX stress amplify gold?" | `test_hypothesis(state="derived.vix_pct", asset="yf.gold", sign="high")` | amplification + 95% CI + permutation p + HOLDS/no-effect verdict |
| "What can I test?" | `list_testables()` | the state variables, assets, event types, domains |
| "Show me the commodities lens" | `get_domain_lens("commodities")` | that domain's validated nodes + nulls + supply-chain + situations |
| "What's mispriced vs the market now?" | `get_gaps()` | the live gap + resolving scorecard (suggestive, small-N) |
| "Show me the edge portfolio" | `get_edge_portfolio()` | the pre-registered battery: validated + nulls, family-wise corrected |
| **"Show me the receipt for the copper edge"** | `get_evidence_pack("edge.copper_growth")` | the exact underlying episodes (events + dates + source URLs), CI, method, commit hashes |
| "Is the engine sound?" | `get_evaluation()` | placebo (must be null), surface consistency, calibration, robustness, miss-audit |
| "What did the engine just register?" | `get_new_events()` | auto-admitted live events + the corroboration that cleared each |
| "What's waiting for my review?" | `get_review_queue()` | LLM-extracted candidates awaiting your coding + the cage's rejects |
| "How is the engine's health?" | `get_health()` / (later) `engine_status` | freshness / coverage / last run |

## How to read what it hands you (the tiers)
Every number carries a tier. Treat them differently:
- **validated** — a claim you can stand behind (CI excludes 0 + multiple-testing corrected + robust). Cite it, with its receipt.
- **suggestive** — a lead, not a claim (small-N / in-sample). Say "suggestive" out loud.
- **null / insufficient** — reported, not hidden. Use them to say what the data *can't* yet support.
- **descriptive** — context (a percentile, an analogue). Never a forecast.

## The rules you inherit when you write from it
- The engine measures **consequence**, never whether an event will happen — the geopolitical judgment stays yours.
- **No naked numbers.** Every figure you publish should trace to a receipt (`get_evidence_pack`).
- **Believe the wide CIs.** Small-N intervals are honest; don't narrate past them.
- When the engine is **silent** (a coverage gap, a null), say so — that honesty is the credibility.

## The daily loop
1. Morning: the engine has refreshed itself (launchd) — or run `./go --refresh`.
2. Ask Claude *"orient me on <what you're writing about>"* → skim the raw material.
3. Pull the specific tests/analogues/receipts you need.
4. **Write your read, in your voice, from the receipts.** The engine is the bench; you are the analyst.
