"""Repeat error report for Claude Code.

Scans your local transcripts (~/.claude/projects/*/*.jsonl) for builds, tests and
scripts the agent ran that really failed, and reports how often the same error
came back in a later session. Only error names, masked compiler messages and
test names are printed, never your messages or commands.
"""
import glob
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime

# Programs that build, test or run code. A failure in their output is a real failure;
# the same text printed by cat, grep or sqlite3 is just something being read.
RUNNERS = {"xcodebuild", "swift", "swiftc", "python", "python3", "pytest", "node", "npm", "npx", "pnpm",
           "yarn", "bun", "tsc", "cargo", "go", "make", "gradle", "mvn", "dotnet", "ruby", "rspec", "jest", "vitest"}
SKIP = {"cd", "env", "command", "rtk", "time", "timeout", "nice", "sudo", "exec"}

# What identifies an error, by kind. Each pattern's first group is the key.
SIGNATURES = [
    re.compile(r"(?m)^(\w+(?:Error|Exception))\b(?::|$)"),                # Python: last line of a traceback
    re.compile(r"\berror (TS\d{4})\b"),                                    # TypeScript
    re.compile(r"(?m)^error\[(E\d{4})\]"),                                 # Rust
    re.compile(r"(?m)(?:Exception Type:\s+|Thread \d+: )(EXC_[A-Z_]+)"),   # crashes
    re.compile(r"(?m)^panic: (\w+)"),                                       # Go
    re.compile(r"(?m):\d+:\d+: (?:fatal )?error: (.{8,160})$"),           # compilers (message is masked)
    re.compile(r"✘ Test (?:\"[^\"]+\"|\w+\(\))"),                          # Swift Testing failures
    re.compile(r"Test Case '-\[\S+ (\w+)\]' failed"),                       # XCTest failures
    re.compile(r"(?m)^FAILED (\S+::\S+)"),                                 # pytest failures
]
COMPILER = SIGNATURES[5]
FAILED_RUN = re.compile(r"\*\* (?:BUILD|TEST) FAILED \*\*|Traceback \(most recent call last\)")


def template(message):
    """cannot find 'fooBar' in scope -> cannot find '…' in scope"""
    message = re.sub(r"(['\"`‘“]).*?(['\"`’”])", "'…'", message)
    message = re.sub(r"(?:/[\w.@+-]+)+", "<path>", message)
    message = re.sub(r"\b0x[0-9a-fA-F]+\b|\b\d+\b", "N", message)
    return re.sub(r"\s+", " ", message).strip()[:60]


def segments(command):
    """Each piece of a shell command with what follows it: 'end', '&&', '|' or 'other' (; || &)."""
    parts = re.split(r"(\|\||&&|\|&?|;|(?<![<>])&(?![>&])|\n)", command)
    out = []
    for text, sep in zip(parts[::2], parts[1::2] + [None]):
        follower = "end" if sep is None else "&&" if sep == "&&" else "|" if sep.startswith("|") and sep != "||" else "other"
        words = [w for w in text.split() if "=" not in w.split("/")[0]]
        while words and (os.path.basename(words[0]) in SKIP or words[0].isdigit()):
            words.pop(0)
        if words:
            out.append((os.path.basename(words[0]), follower))
    return out


def text_of(block):
    content = block.get("content")
    if isinstance(content, list):
        return " ".join(c.get("text", "") for c in content if isinstance(c, dict))
    return content if isinstance(content, str) else ""


def main():
    seen = defaultdict(list)  # error -> [(when, session)]
    failures, hidden, masked_by = 0, 0, Counter()
    for path in glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")):
        session = os.path.basename(path)[:8]
        commands, done = {}, set()
        for line in open(path):
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            content = (row.get("message") or {}).get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use" and block.get("name") == "Bash":
                    command = str((block.get("input") or {}).get("command", ""))
                    # Inline scripts (python3 - <<EOF, python3 -c) are the agent's own throwaway tooling:
                    # their tracebacks are slips in the script, not errors in your project.
                    inline = re.search(r"\bpython3? +(?:-c\b|-\s|-<<)", command)
                    commands[block.get("id")] = [s for s in segments(command) if not (inline and s[0].startswith("python"))]
                    continue
                use_id = block.get("tool_use_id")
                if block.get("type") != "tool_result" or use_id not in commands or use_id in done:
                    continue
                runs = [(exe, follower) for exe, follower in commands[use_id] if exe in RUNNERS]
                if not runs:
                    continue  # nothing was built, tested or run: any error text was only being read
                body = text_of(block)[:50_000]
                keys = set()
                for pattern in SIGNATURES:
                    for match in pattern.finditer(body):
                        found = match.group(1) if pattern.groups else match.group(0)
                        keys.add(template(found) if pattern is COMPILER else found[:60])
                if not keys and not FAILED_RUN.search(body):
                    continue
                done.add(use_id)
                failures += 1
                if not block.get("is_error"):
                    hidden += 1
                    masked_by[next((f for _, f in runs if f != "end"), "end")] += 1
                when = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")).astimezone()
                for key in keys:
                    seen[key].append((when, session))

    repeats = {}
    for key, hits in seen.items():
        sessions = {s for _, s in hits}
        if len(sessions) >= 2:
            days = (max(w for w, _ in hits) - min(w for w, _ in hits)).days
            repeats[key] = (len(sessions), len(hits), days)

    labels = {"|": "piped into another command", "other": "followed by ; || or &", "&&": "followed by &&", "end": "last command, still exit 0"}
    print("REPEAT ERROR REPORT  (Claude Code transcripts)")
    print("=" * 72)
    print(f"Builds, tests and scripts that failed: {failures}")
    print(f"  ...reported as success (exit 0):     {hidden}")
    for follower, n in masked_by.most_common():
        print(f"       {labels[follower]:<31}{n:>4}")
    print(f"Distinct errors:                       {len(seen)}")
    print(f"Came back in a later session:          {len(repeats)}")
    if repeats:
        spans = sorted(d for _, _, d in repeats.values())
        print(f"Days between first and last time:      median {spans[len(spans) // 2]}, longest {spans[-1]}")
        print("\nMOST REPEATED")
        for key, (n_sessions, n_hits, days) in sorted(repeats.items(), key=lambda kv: (-kv[1][0], -kv[1][1]))[:8]:
            print(f"  {key:<60} {n_sessions:>2} sessions {n_hits:>3}x  {days:>2} days")


if __name__ == "__main__":
    main()
