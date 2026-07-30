# USAGE — how to run and use the engine day to day

Everything is local and free. You interrogate it; it never writes your analysis.

## Quickstart (one command)

```
./go              # rebuild the reads, open the daily digest, start the cockpit on :5050
./go --refresh    # also pull fresh free data first, then the above
./go --build      # just refresh the reads + digest (no server) — good for a cron job
```

`./go` refreshes every read (state, gaps, propagation, supply-chain, apt-conditioning, so-what),
opens `data/digest.html`, and starts the cockpit backend. Ctrl+C stops it.

## The daily loop

1. **`./go --refresh`** in the morning → the digest opens with today's read.
2. **Skim the digest** (browser): today's state, the validated edge, the gap, the so-what wire.
3. **Open the cockpit** (OpenBB Workspace, one-time connect) for the full widgets, or ask **Claude**
   (MCP) / run the **bench** when you want to test a specific thesis.
4. **Write** your Substack/memo from the receipts (numbers + CIs + source links). In your voice.

## The four ways to interact

| You want to… | Do this | Where |
|---|---|---|
| Glance at the state | open `data/digest.html` | browser |
| Watch the full cockpit | `./go` → connect `http://127.0.0.1:5050` in **OpenBB Workspace** | browser |
| Ask in plain English | connect the **MCP server** in Claude Desktop, then ask ("does VIX stress amplify gold?", "what's the gap?", "commodities lens") | Claude Desktop |
| Test a specific thesis | `python3 src/research.py test --state derived.vix_pct --asset yf.copper --sign high` (see `RESEARCH_BENCH.md`) | terminal |

Bench cheatsheet: `research.py vars` (what you can test) · `test` (a hypothesis) · `query` (history) ·
`gaps` (what's mispriced) · `lens --domain commodities` (your domain view).

## One-time setup (≈10 min, once)

- **OpenBB cockpit:** run `./go` (starts the backend on :5050) → in OpenBB Workspace (free, browser)
  → Apps → Connect backend → URL `http://127.0.0.1:5050`. The widgets appear.
- **Claude MCP:** add `python3 <repo>/src/mcp_server.py` as an MCP server in Claude Desktop's config
  (needs `pip install mcp` on this machine). Then Claude can query the engine directly, read-only.
- **Deps:** `pip3 install -r requirements.txt` (numpy/pandas/requests/yfinance/… — no keys needed).

## What to trust (the honest tiering)

- **Claims** = only what the engine marks **validated** (H1 + the energy/safe-haven/inflation/equity
  ripple map; copper under a growth regime). Each carries a CI + FDR.
- **Not claims** = everything labelled **null / trap / insufficient / suggestive** — shown, not hidden
  (e.g. the supply-chain producer→commodity edges are honest nulls; the gap "disagreement" finding is
  suggestive small-N).
- The engine measures **consequence**, never whether an event will occur; the **qualitative judgment
  stays yours**.

See also: `SURFACES.md` (the surfaces), `METHOD.md` (the framework), `RESEARCH_BENCH.md` (the bench),
`DIFFERENTIATION.md` (where it sits vs the incumbents).
