"""Cold start report for Claude Code.

Reads your local transcripts (~/.claude/projects/*/*.jsonl) and reports every
time you came back to a session after its prompt cache had expired, and what
that cost. Only token counts and timestamps are read; no message text is printed.
"""
import glob
import json
import os
from collections import defaultdict
from datetime import datetime

# API list prices per million tokens: base input, cache read.
# Cache writes cost 2x base input on a 1-hour cache, 1.25x on a 5-minute one.
PRICES = {"fable-5-2": (8, 0.20), "fable-5-1": (10, 0.25), "opus-5-5": (4, 0.20), "sonnet-5-5": (2, 0.10), "haiku-4-5": (1, 0.10)}
DEFAULT_PRICE = (4, 0.20)
BUCKETS = [(0, "under 100k"), (100_000, "100-200k"), (200_000, "200-400k"), (400_000, "400-600k"), (600_000, "600k+")]


def price_for(model):
    return next((p for key, p in PRICES.items() if key in (model or "")), DEFAULT_PRICE)


def bucket(size):
    return [label for floor, label in BUCKETS if size >= floor][-1]


def gap_text(seconds):
    hours = seconds / 3600
    return f"{hours:.1f} h" if hours >= 1 else f"{seconds / 60:.0f} min"


def scan(path):
    """Returns (replies, total cost, cold starts) for one transcript."""
    last, last_ttl, seen = None, 300, set()
    replies, total, cold = 0, 0.0, []
    for line in open(path):
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        msg = row.get("message") or {}
        usage = msg.get("usage")
        if row.get("type") != "assistant" or not usage or msg.get("id") in seen:
            continue
        seen.add(msg.get("id"))
        written = usage.get("cache_creation_input_tokens", 0)
        read = usage.get("cache_read_input_tokens", 0)
        size = usage.get("input_tokens", 0) + written + read
        if size == 0:  # system or error replies carry no tokens
            continue
        replies += 1
        when = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")).astimezone()
        writes = usage.get("cache_creation") or {}
        ttl = 3600 if writes.get("ephemeral_1h_input_tokens", 0) > 0 else last_ttl
        base, read_price = price_for(msg.get("model"))
        write_price = base * (2 if ttl == 3600 else 1.25)
        total += (usage.get("input_tokens", 0) * base + written * write_price
                  + read * read_price + usage.get("output_tokens", 0) * base * 5) / 1e6
        if last and (when - last).total_seconds() > last_ttl:
            cold.append({
                "when": when, "size": size, "gap": (when - last).total_seconds(),
                "model": (msg.get("model") or "unknown").replace("claude-", ""),
                "times": (2 if last_ttl == 3600 else 1.25) * base / read_price,
                # What this reply paid to rewrite the cache, minus what a warm read would have cost.
                "extra": written * (write_price - read_price) / 1e6,
            })
        if writes.get("ephemeral_1h_input_tokens", 0) > 0:
            last_ttl = 3600
        elif writes.get("ephemeral_5m_input_tokens", 0) > 0:
            last_ttl = 300
        last = when
    return replies, total, cold


def main():
    sessions, all_cold, total_cost, total_replies = [], [], 0.0, 0
    for path in glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")):
        replies, cost, cold = scan(path)
        if not replies:
            continue
        project = os.path.basename(os.path.dirname(path)).split("-")[-1] or "?"
        session = os.path.basename(path)[:8]
        for c in cold:
            c["session"], c["project"] = session, project
        sessions.append((session, project, cold))
        all_cold += cold
        total_cost += cost
        total_replies += replies

    if not all_cold:
        print(f"Scanned {len(sessions)} sessions. No cold starts found.")
        return

    extra = sum(c["extra"] for c in all_cold)
    hit = [s for s in sessions if s[2]]
    first = min(c["when"] for c in all_cold)
    last = max(c["when"] for c in all_cold)

    print("COLD START REPORT  (Claude Code, estimated at API list prices)")
    print("=" * 66)
    print(f"Sessions scanned:        {len(sessions)}  ({total_replies:,} replies)")
    print(f"Cold starts:             {len(all_cold)}  in {len(hit)} sessions, {first:%b %d} to {last:%b %d}")
    print(f"  over 100k tokens:      {sum(c['size'] >= 100_000 for c in all_cold)}")
    print(f"Extra cost of cold starts: ${extra:,.2f}  ({extra / total_cost:.0%} of ${total_cost:,.2f} total)")

    print("\nBY SESSION SIZE AT THE COLD START")
    print(f"  {'size':<12}{'cold starts':>12}{'extra cost':>13}")
    for _, label in BUCKETS:
        rows = [c for c in all_cold if bucket(c["size"]) == label]
        if rows:
            print(f"  {label:<12}{len(rows):>12}{'$' + format(sum(c['extra'] for c in rows), ',.2f'):>13}")

    print("\nHOW LONG YOU WERE AWAY")
    for label, lo, hi in [("under 2 h (breaks, meetings)", 0, 7200),
                          ("2-8 h (lunch, afternoon)", 7200, 28800),
                          ("over 8 h (overnight)", 28800, float("inf"))]:
        rows = [c for c in all_cold if lo <= c["gap"] < hi]
        print(f"  {label:<30}{len(rows):>4} cold starts   ${sum(c['extra'] for c in rows):,.2f}")

    print("\nSESSIONS THAT COST THE MOST TO RE-WARM")
    hit.sort(key=lambda s: sum(c["extra"] for c in s[2]), reverse=True)
    for session, project, cold in hit[:5]:
        sizes = [c["size"] for c in cold]
        print(f"  {session}  {project:<14} {len(cold):>2} cold starts, "
              f"{min(sizes) // 1000}k -> {max(sizes) // 1000}k   ${sum(c['extra'] for c in cold):,.2f}")

    print("\nMOST EXPENSIVE COLD STARTS")
    for c in sorted(all_cold, key=lambda c: c["extra"], reverse=True)[:5]:
        print(f"  {c['when']:%b %d %H:%M}  {c['size'] // 1000:>4}k  away {gap_text(c['gap']):>7}  "
              f"{c['model']:<11} {c['times']:.0f}x a warm turn   ${c['extra']:.2f}")


if __name__ == "__main__":
    main()
