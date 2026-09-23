---
title: How to Inspect, Search, and Resume Claude Code & OpenAI Codex Sessions (Free In-Browser Tool)
published: true
description: Stop losing terminal prompts and tool executions. Inspect Claude Code and Codex JSONL sessions with zero-upload local privacy in your browser.
tags: ai, webdev, macos, programming
canonical_url: https://l2cache.amvo.store/en/tools/claude-session-viewer
cover_image: https://l2cache.amvo.store/screenshots/agent-history1.jpg
---

If you use CLI coding agents like **Claude Code** (`claude`) or **OpenAI Codex** (`codex`), you already know the superpower they give you: they write code, run shell commands, debug failing tests, and refactor multi-file architectures right inside your terminal.

But as you work on multiple branches, repositories, and projects throughout the day, a major friction point emerges:

> **"Where did that exact prompt, architectural explanation, or bash command go from 3 hours ago?"**

Both Claude Code and Codex record transcripts locally on your machine:
- **Claude Code:** Stored in `~/.claude/projects/<project>/transcript.jsonl`
- **OpenAI Codex:** Stored in `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`

---

## 💻 The Built-in CLI Options (And Where They Fall Short)

Both tools provide built-in terminal flags to resume past work:

### 1. Claude Code
- **Interactive Picker:** `claude --resume` (or `claude -r`) lists recent sessions in your current directory.
- **Direct Resume:** `claude --resume <session-id>` jumps directly into a specific conversation.

### 2. OpenAI Codex
- **Resume Command:** `codex resume <session-id>` or `codex --resume` picks up where you left off.

### ⚠️ Why the Default CLI Flags Fall Short:
While `--resume` is great if you just closed a terminal 5 minutes ago, it struggles as your history grows:
1. **No Full-Text Search Across Turns:** You only get truncated single-line summaries. You cannot search: *"Which session had that Docker compose volume fix?"* or *"What was the exact curl command we used yesterday?"*.
2. **Siloed by Directory:** `claude --resume` only shows sessions for the current folder. If you worked across 6 microservices or multiple branches, finding a past solution means `cd`-ing into every folder.
3. **Massive JSONL Files:** Opening the raw 25MB `.jsonl` transcript in VS Code or Vim will lag your editor and makes reading nested tool envelopes nearly impossible.

---

## 🛠️ The Solution: Claude & Codex Session Viewer (100% In-Browser & Local)

To solve this, we built a free, privacy-first web tool: **[Claude & Codex Session Viewer](https://l2cache.amvo.store/en/tools/claude-session-viewer)**.

![Claude & Codex Session History](https://l2cache.amvo.store/screenshots/agent-history1.jpg)

### ✨ What It Does:
1. **📂 Single-Click Folder Linking:** Use the native Web File System Access API to link your `~/.claude` or `~/.codex/sessions` directory once.
2. **⚡ Real-time Smart Filtering:** Filter instantly by agent (`Claude`, `Codex`), Git branch, project name, or search query.
3. **🔍 Instant Full-Text Search:** Query across all past human prompts, model responses, and executed tool calls.
4. **💬 Clean Chat UI:** Renders prompts, assistant replies, Markdown formatting, code syntax blocks, and tool executions (`Bash`, `file_edit`, `custom_tool_call`).
5. **🛡️ 100% Private (Zero Cloud Uploads):** All parsing and search indexing happens entirely on your machine via client-side JavaScript. No session files, API keys, or proprietary code ever leave your browser.

---

## 🔬 How the JSONL Parsing Works Under the Hood

Parsing session transcripts from multiple CLI agents requires dealing with diverse payload envelope architectures:

### 1. Claude Code Envelopes
Claude records user turns and assistant responses as discrete JSON objects:

```json
{"type":"user","message":{"role":"user","content":"fix the memory leak in auth worker"},"sessionId":"019fef5f..."}
{"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"I analyzed the heap snapshot..."},{"type":"tool_use","name":"Bash","input":{"command":"npm test"}}]},"sessionId":"019fef5f..."}
```

### 2. OpenAI Codex Rollout Envelopes
Codex wraps session lifecycles into a 2-pass envelope system with `session_meta`, `turn_context`, and `event_msg`:

```json
{"type":"session_meta","payload":{"session_id":"019fef5f...","cwd":"/Users/dev/app","git":{"branch":"main"}}}
{"type":"event_msg","payload":{"type":"item_completed","item":{"type":"UserMessage","content":"review the auth PR"}}}
{"type":"event_msg","payload":{"type":"item_completed","item":{"type":"CommandExecution","command":"cargo test","exit_code":0}}}
```

Our parser runs a **2-pass indexing engine**:
- **Pass 1:** Pre-scans for session metadata, repository working directory (`cwd`), Git branch, token usage, and tool error statuses.
- **Pass 2:** Reconstructs the chronological conversation timeline, mapping tool calls and outputs to clean visual timeline cards.

---

## 🚀 How to Try It in 10 Seconds

You don't need to install anything or sign up for an account:

1. Open the **[Claude & Codex Session Viewer](https://l2cache.amvo.store/en/tools/claude-session-viewer)** in any modern browser (Chrome, Edge, Safari, Arc).
2. Click **"Link Claude Folder"** and select `~/.claude` (or drag and drop any `.jsonl` file).
3. Search your past prompts, copy code snippets, or inspect exact tool outputs.

---

## 💡 Want Automated Background Tracking on Mac?

If you prefer not having to manually drag files and want instant `⌥ + Space` search across all your clipboard history, screenshots (with on-device Apple Vision OCR), and AI coding sessions right from your macOS menu bar:

![L2Cache Session Timeline & Token Metrics](https://l2cache.amvo.store/screenshots/agent-history2.jpg)

👉 Check out **[L2Cache for macOS ($4.99 Lifetime)](https://l2cache.amvo.store)**.

Happy coding! If you have suggestions or formats you'd like supported (like Gemini CLI or Cursor transcripts), leave a comment below!
