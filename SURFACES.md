# SURFACES — how an analyst actually uses the engine

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
