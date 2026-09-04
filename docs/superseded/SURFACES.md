> **SUPERSEDED — NOT A CURRENT CLAIM.** Superseded design and status material for the legacy engine. The authoritative documents are [`README.md`](../../README.md) and [`PAPER.md`](../PAPER.md).

# SURFACES — how an analyst actually uses the engine

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


Four ways in, one engine underneath. All read the same validated artifacts; none writes your analysis.

## 1. The research bench (interrogate it) — `src/research.py`
Pull deterministic, receipted answers. `test` a hypothesis, `query` history, scan `gaps`, list `vars`.
See `RESEARCH_BENCH.md`. This is the "test my own thinking" surface.

## 2. Natural language (ask it) — the MCP server, `src/mcp_server.py`
Claude (Desktop/Cowork) queries the engine directly, read-only. Tools:
`get_daily_read`, `get_sowhat`, `get_propagation_graph`, `get_gaps`, `test_hypothesis`,
`scenario_card`, `list_events`/`get_event`, `list_situations`/`get_situation`, `query_series`,
`get_results`. Ask "does VIX stress amplify diesel?" and it runs the gate — no terminal.

## 3. The cockpit (watch it) — OpenBB Workspace via `src/backend.py` (port 5050)
Widgets: **The So-What Wire** (event→consequence→decision), **Propagation Graph** (validated
edges + traps), **Gap Board** (market-as-null), **Ripple Map** (does the edge generalize?),
**Corroboration** (confirmation not headlines), **Track Record**, **Signal Registry**,
**H1 — The Validated Edge**. Every number click-through-sourced.

## 4. The daily read (glance at it) — `src/digest.py` → `data/digest.html`
A calm, offline daily brief: today's read, the validated edge, the gap, the wire — formatted, not
generated.

## The docs that make it credible
- `METHOD.md` — the full framework, stage by stage, each with its honesty guard (the citable one).
- `DIFFERENTIATION.md` — where it sits vs GPR/GeoQuant/RavenPack/Everstream, and the moat.
- `RESEARCH_BENCH.md` — how to interrogate it and add your own data.
- `REGISTERED_SAMPLE.md` — the frozen pre-registration.

## The rule underneath all four
Only **validated** things are claims; **nulls and traps are shown, not hidden**; every number is
**sourced and point-in-time**; the engine measures **consequence**, never whether an event will
occur; and the **qualitative judgment stays yours**. That's the glass box the black boxes can't be.
