"""Which MCP tools do your Claude Code agents actually call, and how much comes back?

Reads ~/.claude/projects/*/*.jsonl. Prints tool names and sizes only, never message text.
Usage: python3 mcp_usage.py [server]   e.g. `python3 mcp_usage.py l2cache` for one server's tools.
"""
import glob
import json
import os
import sys
from collections import defaultdict

calls, sizes, pending, total = defaultdict(int), defaultdict(list), {}, 0
for path in glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")):
    for line in open(path):
        try:
            content = (json.loads(line).get("message") or {}).get("content")
        except json.JSONDecodeError:
            continue
        for block in content if isinstance(content, list) else []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use":
                total += 1
                if block.get("name", "").startswith("mcp__"):
                    calls[block["name"]] += 1
                    pending[block.get("id")] = block["name"]
            elif block.get("type") == "tool_result" and block.get("tool_use_id") in pending:
                result = block.get("content")
                text = "".join(b.get("text", "") for b in result if isinstance(b, dict)) if isinstance(result, list) else str(result)
                sizes[pending[block["tool_use_id"]]].append(len(text) // 4)  # ~4 characters per token

mcp = sum(calls.values())
print(f"{total:,} tool calls, {mcp} to MCP servers ({mcp / max(total, 1):.1%})\n")

servers = defaultdict(lambda: [0, []])
for name, n in calls.items():
    server = name.split("__")[1]
    servers[server][0] += n
    servers[server][1] += sizes[name]
print(f"{'MCP server':<28}{'calls':>7}{'median tokens back':>20}")
for server, (n, s) in sorted(servers.items(), key=lambda kv: -kv[1][0]):
    s = sorted(s) or [0]
    print(f"{server:<28}{n:>7}{s[len(s) // 2]:>20}")

only = sys.argv[1] if len(sys.argv) > 1 else None
tools = {name: n for name, n in calls.items() if only is None or name.split("__")[1] == only}
print(f"\n{'Tool' + (f' ({only})' if only else ''):<34}{'calls':>6}{'median':>8}{'90th pct':>10}{'empty':>7}")
for name, n in sorted(tools.items(), key=lambda kv: -kv[1])[:15]:
    s = sorted(sizes[name]) or [0]
    empty = sum(t <= 10 for t in s)  # 10 tokens or fewer: nothing found
    print(f"{name.split('__', 2)[2][:33]:<34}{n:>6}{s[len(s) // 2]:>8}{s[int(len(s) * 0.9)]:>10}{empty:>7}")
