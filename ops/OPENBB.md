# Ops — OpenBB Workspace, set up right (+ Claude in the browser)

The engine feeds **OpenBB Workspace** (pro.openbb.co) through the local backend
(`src/backend.py`, port 5050). This is how to make it good — not a wall of tables —
and how to put **Claude right next to it in the browser**.

## 1. Connect the backend (once)
1. Run it: `python3 src/backend.py` (leave it in its own Terminal tab).
2. In OpenBB Workspace → **Apps / Connections** → add a custom backend →
   URL `http://127.0.0.1:5050`. Widgets appear under their names.
3. **After any change to `backend.py`, restart it** (`Ctrl+C`, re-run) — OpenBB only
   sees new widgets on reconnect/refresh. This is why new widgets "don't show" until
   you restart.

## 2. It's not just tables — use the right widget type
OpenBB supports far more than tables ([widget types](https://docs.openbb.co/workspace/developers/json-specs/widgets-json-reference)):
`table`, **`chart`** (Plotly), `chart-highcharts`, `metric` (big-number KPI),
`markdown`, `newsfeed`, `live_grid`, `html`, `iframe`, `omni`.

The engine now exposes (18 widgets):
- **Tables** — Corroborated Events, Market-Implied Odds, Chokepoint Transits,
  Attention, Supply Fundamentals (+ the original engine tables).
- **Charts (Plotly)** — Brent Crude, Chokepoint Tanker Flow, Attention Over Time.

**Adding a chart is easy** (no Plotly dependency needed): the endpoint returns a plain
`{"data": [...], "layout": {...}}` dict and the widget `type` is `"chart"`
([plotly docs](https://docs.openbb.co/workspace/developers/widget-types/plotly-charts)).
See `_line_fig()` in `backend.py` for the pattern — copy it for any new series.

## 3. Build a good dashboard
- **Group by question, not by feed:** a "Where do we stand" board (engine read +
  corroborated events + chokepoint chart + market odds), a "Physical" board
  (fundamentals + transits + Brent), a "Watchlist" board (the wire + attention).
- Resize/drag widgets; save as a named dashboard. You can keep several.
- Charts up top (fast read), tables below (detail).

## 4. Claude in the browser (this is the "AI next to the terminal")
**Claude for Chrome** is Anthropic's official browser extension — a Claude **sidebar
that sees the live page** (including behind the pro.openbb.co login) and can **act**
(click, type, navigate). It's on all **paid** plans (Pro/Max/Team/Enterprise).
([get started](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome) ·
[guide](https://almcorp.com/blog/claude-for-chrome-complete-guide/))

Install: Chrome Web Store → search "Claude" → **Add to Chrome** → sign in. Then, with
OpenBB open, the Claude sidebar can read your dashboards and help you interpret,
rearrange, and drive them — exactly the "Claude helps me use/design the terminal"
workflow. (It reads what's on screen; it doesn't need our backend to *see* the data.)

## 5. Make Claude the OpenBB copilot (advanced, later)
OpenBB's built-in copilot can be replaced with a **custom AI agent** via
**`openbb-pydantic-ai`** — write an agent that speaks native OpenBB and plug in
**Claude** as the model ([OpenBB × Pydantic AI](https://openbb.co/blog/building-ai-agents-for-openbb-workspace-with-pydantic-ai/)).
Combined with **Workspace MCP** ([intro](https://openbb.co/blog/introducing-workspace-mcp/))
and our own `src/mcp_server.py`, the in-terminal copilot becomes Claude reading the
ripple engine. This is a bigger build — do it once the widget layer feels right.

**AI-friendly widgets:** set `"raw": true` on a widget so the copilot gets clean JSON
while you see the chart — worth adding to the chart widgets when we wire the copilot.
