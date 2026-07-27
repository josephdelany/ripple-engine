# The Engine MCP — let Claude query the engine

This exposes the engine to **Claude Desktop** (and Cowork) as a read-only MCP
server, so an analysis chat can pull real numbers from the database directly — no
screenshots, no copy-paste. It is launched by the Claude app over stdio; it opens
no network port and every tool is read-only.

## Install (you paste this — I do not touch Claude's config)

1. Open Claude Desktop's config file:
   `~/Library/Application Support/Claude/claude_desktop_config.json`
   (create it if it doesn't exist).
2. Add this server under `mcpServers` (merge with anything already there):

```json
{
  "mcpServers": {
    "ripple-engine": {
      "command": "/usr/local/bin/python3",
      "args": ["/Users/default/Documents/Claude/Projects/News to Markets/ripple-engine/src/mcp_server.py"]
    }
  }
}
```

   (If `which python3` shows a different path than `/usr/local/bin/python3`, use
   that instead.)
3. **Fully quit and reopen Claude Desktop** (MCP servers load at launch).

## Verify the tools appeared
In a Claude Desktop chat, open the tools/attachments menu — you should see the
`ripple-engine` server with ten tools: `get_daily_read`, `get_health`,
`list_events`, `get_event`, `scenario_card`, `query_series`, `get_alerts`,
`list_situations`, `get_situation`, `get_results`. Ask e.g. *"use get_daily_read"*
— it returns today's engine read; *"get_situation for the Israel-Iran war"* returns
the running dossier (timeline + priced-state) so the terminal reads the memory.

To check the server runs at all outside the app:
```bash
python3 src/mcp_smoke.py        # lists the 8 tools and calls each one
```

## Uninstall
Remove the `ripple-engine` block from `claude_desktop_config.json` (or the whole
`mcpServers` object if it's the only one) and restart Claude Desktop.

## What it can and cannot do
- **Read-only, always.** The database is opened in SQLite read-only mode; there is
  no raw-SQL passthrough (parameterized queries only). No tool writes, approves,
  promotes an alert, logs a forecast, or changes anything. The human gate is
  untouched.
- Each tool's description carries the engine's caveats (small n, exploratory/failed
  hypotheses, and that the engine measures market *consequences* of events and
  never forecasts whether events occur) so Claude repeats them in conversation.
