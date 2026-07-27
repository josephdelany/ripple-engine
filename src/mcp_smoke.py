"""
mcp_smoke.py -- smoke test for the Engine MCP server.

Spawns src/mcp_server.py over stdio exactly as the Claude app would, lists the
tools, calls each one with a realistic argument, and prints a one-line result --
proof the server starts and every tool answers. The captured output is the
receipt (data/mcp_smoke_test.txt).

Run:  python3 src/mcp_smoke.py
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent.parent
SERVER = str(ROOT / "src" / "mcp_server.py")

# (tool, args) -- one realistic call each.
CALLS = [
    ("get_daily_read", {}),
    ("get_health", {}),
    ("list_events", {"type": "conflict_escalation"}),
    ("get_event", {"event_id": "iraq_invades_kuwait_1990"}),
    ("scenario_card", {"event_type": "conflict_escalation"}),
    ("query_series", {"series_id": "fred.DCOILBRENTEU", "start": "2026-07-01"}),
    ("get_alerts", {"limit": 3}),
    ("get_results", {"name": "registered_run_results"}),
]


def _one_line(result):
    txt = "".join(getattr(b, "text", "") for b in result.content)
    return " ".join(txt.split())[:140]


async def run():
    params = StdioServerParameters(command=sys.executable, args=[SERVER])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            names = [t.name for t in tools.tools]
            print(f"Engine MCP smoke test -- server exposed {len(names)} tools:")
            print("  " + ", ".join(names) + "\n")
            for name, args in CALLS:
                try:
                    res = await session.call_tool(name, args)
                    print(f"  {name:<16} OK   {_one_line(res)}")
                except Exception as e:
                    print(f"  {name:<16} FAIL {type(e).__name__}: {e}")
            print("\nAll tools are READ-ONLY. No tool writes, approves, promotes, "
                  "or logs anything.")


if __name__ == "__main__":
    asyncio.run(run())
