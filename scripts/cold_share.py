#!/usr/bin/env python3
"""Share of Claude Code tokens and cost spent on cold-cache reloads, last N days. Read-only.

    python3 scripts/cold_share.py [days]   # default 30; reads ~/.claude/projects locally
"""
import json, os, sys, glob
from collections import defaultdict
from datetime import datetime, timezone, timedelta

DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 30
ROOT = os.path.expanduser("~/.claude/projects")
SINCE = datetime.now(timezone.utc) - timedelta(days=DAYS)
# Relative to the model's base input price (Anthropic's published multipliers).
W = {"input": 1.0, "read": 0.1, "w5": 1.25, "w1h": 2.0, "output": 5.0}
SIZE_THRESHOLD = 50_000  # the guard's default minimum context

def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

seen = set()
streams = defaultdict(list)  # (file, sidechain) -> [(time, usage, model, project)]
for path in glob.glob(os.path.join(ROOT, "**", "*.jsonl"), recursive=True):
    if os.path.getmtime(path) < SINCE.timestamp():
        continue
    project = os.path.relpath(path, ROOT).split(os.sep)[0].replace("-Users-dinesh-tech-", "")
    with open(path, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            if '"usage"' not in line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            m = d.get("message") or {}
            u = m.get("usage")
            if not isinstance(u, dict) or "timestamp" not in d:
                continue
            key = (m.get("id"), d.get("requestId"))
            if key in seen:
                continue
            seen.add(key)
            t = ts(d["timestamp"])
            if t < SINCE:
                continue
            streams[(path, bool(d.get("isSidechain")))].append((t, u, m.get("model") or "?", project))

tot = defaultdict(float)
by_model = defaultdict(lambda: defaultdict(float))
cold = defaultdict(float)
cold_by_session = defaultdict(lambda: defaultdict(float))
requests = 0

def parts(u):
    cc = u.get("cache_creation") or {}
    w1h = cc.get("ephemeral_1h_input_tokens", 0) or 0
    w5 = cc.get("ephemeral_5m_input_tokens", 0) or 0
    total_w = u.get("cache_creation_input_tokens", 0) or 0
    if w1h + w5 == 0:
        w5 = total_w  # older lines without the split: assume 5m
    return {"input": u.get("input_tokens", 0) or 0, "read": u.get("cache_read_input_tokens", 0) or 0,
            "w5": w5, "w1h": w1h, "output": u.get("output_tokens", 0) or 0}

def units(p):
    return sum(p[k] * W[k] for k in W)

for (path, side), rows in streams.items():
    rows.sort(key=lambda r: r[0])
    prev_t, prev_ttl = None, None
    for t, u, model, project in rows:
        p = parts(u)
        requests += 1
        for k in W:
            tot[k] += p[k]
            by_model[model][k] += p[k]
        ctx = p["input"] + p["read"] + p["w5"] + p["w1h"]
        if prev_t is not None and (t - prev_t).total_seconds() > prev_ttl and (p["w5"] + p["w1h"]) > 0:
            wtok = p["w5"] + p["w1h"]
            wunits = p["w5"] * W["w5"] + p["w1h"] * W["w1h"]
            cls = "1h" if prev_ttl > 300 else "5m"
            big = ctx >= SIZE_THRESHOLD
            for tag in ("all", cls) + (("big",) if big else ()):
                cold[tag + "_n"] += 1
                cold[tag + "_tok"] += wtok
                cold[tag + "_units"] += wunits
                # what the same context would have cost warm (read instead of write)
                cold[tag + "_warm_units"] += wtok * W["read"]
            s = cold_by_session[(project, os.path.basename(path)[:8], side)]
            s["n"] += 1; s["tok"] += wtok; s["units"] += wunits; s["peak"] = max(s["peak"], ctx)
        # TTL comes from the latest write; a read refreshes the clock but keeps the TTL.
        if p["w1h"] > 0:
            prev_ttl = 3600
        elif p["w5"] > 0 or prev_ttl is None:
            prev_ttl = 300
        prev_t = t

T = sum(tot[k] for k in W)
U = units(tot)
print(f"Window: last {DAYS} days · {requests:,} billed requests · {len(streams)} streams · Claude Code only")
print(f"Tokens: {T/1e6:,.1f}M  (read {tot['read']/T:.1%} · write5m {tot['w5']/T:.1%} · write1h {tot['w1h']/T:.1%} · input {tot['input']/T:.1%} · output {tot['output']/T:.1%})")
print(f"Cost units (input-price tokens): {U/1e6:,.1f}M  (read {tot['read']*W['read']/U:.1%} · writes {(tot['w5']*W['w5']+tot['w1h']*W['w1h'])/U:.1%} · input {tot['input']/U:.1%} · output {tot['output']*W['output']/U:.1%})")
for tag, label in (("all", "All cold reloads"), ("1h", "  after a 1h cache expired"), ("5m", "  after a 5m cache expired"), ("big", f"  context ≥ {SIZE_THRESHOLD//1000}k (guard range)")):
    n = cold[tag + "_n"]
    if not n:
        print(f"{label}: none"); continue
    print(f"{label}: {int(n)} turns · {cold[tag+'_tok']/1e6:.1f}M tokens = {cold[tag+'_tok']/T:.1%} of tokens · "
          f"{cold[tag+'_units']/U:.1%} of cost · avoidable vs warm: {(cold[tag+'_units']-cold[tag+'_warm_units'])/U:.1%} of cost")
print("Models:", ", ".join(f"{m} {sum(v.values())/T:.0%}" for m, v in sorted(by_model.items(), key=lambda x: -sum(x[1].values()))[:4]))
print("Top cold sessions (project · session · thread · cold turns · reload tokens · share of all cost · peak ctx):")
for (proj, sid, side), s in sorted(cold_by_session.items(), key=lambda x: -x[1]["units"])[:5]:
    print(f"  {proj} · {sid} · {'subagent' if side else 'main'} · {int(s['n'])} · {s['tok']/1e6:.2f}M · {s['units']/U:.1%} · {s['peak']/1e3:.0f}k")
