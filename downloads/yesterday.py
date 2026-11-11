"""What did I do yesterday? Rebuilt from files already on your Mac.

Reads git reflogs (no git commands), Claude Code transcripts and zsh history,
and prints counts only: no commit messages, prompts or commands.
Usage: python3 yesterday.py [projects folder]   (default: ~/Developer)
"""
import functools
import glob
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import date, datetime

ROOT = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/Developer")
activity = defaultdict(Counter)  # day -> Counter of "project: what"


def day_of(epoch):
    return datetime.fromtimestamp(epoch).date()


@functools.lru_cache(maxsize=None)
def repo_of(folder):
    """The repository a folder belongs to (nearest parent with a .git), so `app/docs` counts as `app`."""
    path = folder
    while path and path != os.path.dirname(path):
        if os.path.exists(os.path.join(path, ".git")):
            return os.path.basename(path)
        path = os.path.dirname(path)
    return os.path.basename(folder) or "?"


# 1. Git: every branch's reflog records commits, merges and new branches with a timestamp.
for git_dir in glob.glob(os.path.join(ROOT, "*", ".git")):
    project = os.path.basename(os.path.dirname(git_dir))
    for log in glob.glob(os.path.join(git_dir, "logs", "refs", "heads", "**"), recursive=True):
        if not os.path.isfile(log):
            continue
        for line in open(log, errors="replace"):
            head, _, message = line.partition("\t")
            parts = head.split()
            if len(parts) < 2:
                continue
            day = day_of(int(parts[-2]))
            if message.startswith(("commit", "commit (amend)", "commit (initial)")):
                activity[day][f"{project}: commits"] += 1
            elif message.startswith("merge"):
                activity[day][f"{project}: merges"] += 1
            elif message.startswith("branch: Created"):
                activity[day][f"{project}: new branches"] += 1

# 2. Claude Code: each transcript line has a timestamp; count sessions and prompts per day.
for path in glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")):
    sessions = set()
    for line in open(path, errors="replace"):
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        text = (row.get("message") or {}).get("content")
        # Typed prompts are plain strings; tool results and slash-command output are not.
        # Compaction summaries are stored as user messages too, but nobody typed them.
        if row.get("type") != "user" or not isinstance(text, str) or text.startswith("<"):
            continue
        if row.get("isMeta") or row.get("isCompactSummary") or text.startswith("[Request interrupted"):
            continue
        day = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")).astimezone().date()
        project = repo_of(row.get("cwd") or "")
        activity[day][f"{project}: agent prompts"] += 1
        if (day, project) not in sessions:
            sessions.add((day, project))
            activity[day][f"{project}: agent sessions"] += 1

# 3. zsh history (needs EXTENDED_HISTORY for timestamps): count commands per day.
history = os.path.expanduser("~/.zsh_history")
stamped = 0
if os.path.exists(history):
    for line in open(history, errors="replace"):
        if line.startswith(": ") and ":" in line[2:]:
            try:
                activity[day_of(int(line[2:].split(":", 1)[0]))]["terminal: commands"] += 1
                stamped += 1
            except ValueError:
                pass

past = sorted(d for d in activity if d < date.today())
if not past:
    sys.exit("No activity found before today.")
day = past[-1]
print(f"Your last working day: {day:%A, %B %d}\n")
for key, count in sorted(activity[day].items()):
    print(f"  {key:<40}{count:>5}")
if not stamped:
    print("\n  (Terminal skipped: your zsh history has no timestamps. Add `setopt EXTENDED_HISTORY` to ~/.zshrc.)")
