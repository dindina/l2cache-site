"""Estimate your hours per project per day from Claude Code transcripts.

Uses the same rules as L2Cache's timesheet: each moment of activity owns the time
until the next one; a gap over 15 minutes is idle and earns 5 minutes; agent
activity counts only within 15 minutes of something you typed. Reads timestamps
and folder names only, never message text.
"""
import functools
import glob
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta

IDLE_GAP = 15 * 60
CREDIT = 5 * 60
DAYS = 14


def is_your_prompt(row):
    # Compaction summaries are written as user messages but nobody typed them.
    if row.get("type") != "user" or row.get("isMeta") or row.get("isCompactSummary"):
        return False
    content = (row.get("message") or {}).get("content")
    if isinstance(content, str):
        return True
    return isinstance(content, list) and not any(
        isinstance(b, dict) and b.get("type") == "tool_result" for b in content)


@functools.lru_cache(maxsize=None)
def project_name(folder):
    """The repository a folder belongs to (its nearest parent with a .git), like L2Cache's projects."""
    path = folder
    while path and path != os.path.dirname(path):
        if os.path.exists(os.path.join(path, ".git")):
            return os.path.basename(path)
        path = os.path.dirname(path)
    return os.path.basename(folder) or "?"


def points():
    since = datetime.now().astimezone() - timedelta(days=DAYS)
    for path in glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")):
        for line in open(path):
            try:
                row = json.loads(line)
                when = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")).astimezone()
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
            if when < since or row.get("type") not in ("user", "assistant"):
                continue
            project = project_name(row.get("cwd") or "")
            yield when, project, is_your_prompt(row)


def main():
    pts = sorted(points())
    anchors = [w for w, _, you in pts if you]
    present = []
    j = 0
    for when, project, you in pts:
        while j + 1 < len(anchors) and anchors[j + 1] <= when:
            j += 1
        near = any(0 <= k < len(anchors) and abs((anchors[k] - when).total_seconds()) <= IDLE_GAP
                   for k in (j, j + 1))
        if you or near:
            present.append((when, project))
    hours = defaultdict(float)
    for i, (when, project) in enumerate(present):
        gap = (present[i + 1][0] - when).total_seconds() if i + 1 < len(present) else IDLE_GAP + 1
        hours[(when.date(), project)] += gap if gap <= IDLE_GAP else CREDIT
    alone = sum(1 for _, _, you in pts) - len(present)
    # First to last activity each day: the "I was at it from 9 to 6" number.
    first, last = {}, {}
    for when, _ in present:
        first.setdefault(when.date(), when)
        last[when.date()] = when

    days = sorted({d for d, _ in hours})
    projects = sorted({p for _, p in hours})
    names = {p: (f"Project {chr(65 + i)}" if "--mask" in sys.argv else p) for i, p in enumerate(projects)}
    q = lambda s: round(s / 900) / 4
    print(f"ESTIMATED HOURS, LAST {DAYS} DAYS (from Claude Code activity)")
    print(f"{'day':<12}" + "".join(f"{names[p][:12]:>13}" for p in projects) + f"{'total':>9}{'span':>9}")
    for d in days:
        row = [q(hours.get((d, p), 0)) for p in projects]
        print(f"{d:%a %b %d}  " + "".join(f"{h:>13.2f}" for h in row) + f"{sum(row):>9.2f}{q((last[d] - first[d]).total_seconds()):>9.2f}")
    total = sum(q(hours.get((d, p), 0)) for d in days for p in projects)
    span = sum(q((last[d] - first[d]).total_seconds()) for d in days)
    print(f"\nEstimated time: {total:.2f} h over {len(days)} days. First-to-last span: {span:.2f} h.")
    print(f"Agent activity left out because you weren't there (15+ min from your last input): {alone:,} events.")


if __name__ == "__main__":
    main()
