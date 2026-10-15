# Phase 1 — Coding-Agent Capability Matrix

**Status:** Initial implementation audit  
**Date:** 15 October 2026  
**Purpose:** Prevent the new website from implying identical support across every coding agent

## Legend

- **Verified:** Direct implementation path found.
- **Partial:** A shared UI/data path exists, but completeness depends on the provider's source format or requires runtime verification.
- **Not implemented:** The current implementation explicitly excludes the provider.
- **Verify:** Related code exists, but the end-to-end capability has not yet been proven.

## Matrix

| Capability | Claude Code | Codex | GitHub Copilot | Grok Build | Google Antigravity |
|---|---|---|---|---|---|
| Historical session import | Verified | Verified | Verified | Verified | Verified |
| Prompts/responses/commands capture from history | Partial | Partial | Partial | Partial | Partial |
| Provider filtering in session browser | Verified | Verified | Verified | Verified | Verified |
| Resume command generation | Verified | Verified | Verified | Verified | Verified |
| Live capture/hooks | Verified | Verified | Verified | Verified | Not implemented |
| Session handoff injection | Verified | Verified | Verified | Verified | Not implemented |
| Plans browser | Verified | Not implemented | Not implemented | Not implemented | Verified |
| Installed-skill catalogue | Verified | Verified | Not implemented | Not implemented | Not implemented |
| Skill invocation/usage extraction | Verified | Verified | Not implemented | Not implemented | Not implemented |
| MCP/rules/hooks inspection | Partial | Partial | Partial | Verify | Partial |
| Token/model/duration analytics surface | Partial | Partial | Partial | Partial | Partial |
| Project/Git association | Partial | Partial | Partial | Partial | Partial |

## Evidence Summary

### Historical import

`AgentHistoryService.adapter(for:)` maps every `AgentProvider` case to a dedicated adapter:

- `ClaudeHistoryAdapter`
- `CodexHistoryAdapter`
- `CopilotHistoryAdapter`
- `GrokHistoryAdapter`
- `AntigravityHistoryAdapter`

This verifies that all five providers have an intended local-history import path. It does not by itself prove identical transcript fidelity.

### Capture categories

Settings expose prompts, assistant responses, and executed-command capture categories. The app explicitly excludes hidden reasoning, raw tool output, environment snapshots, and file contents. Marketing copy should say “supported session activity,” not “every detail” or “complete raw transcripts,” until fixture tests establish provider parity.

### Resume

`AgentResumeCommand` generates provider-specific commands for all five providers:

- `claude --resume`
- `codex resume`
- `copilot --resume`
- `grok --resume`
- `agy resume`

Runtime availability still depends on the corresponding CLI and session being present.

### Live continuity

The Coding Agents settings expose `AgentContinuityRow` for Claude Code, Codex, GitHub Copilot, and Grok Build. Antigravity returns `false` for connection state and has no row. The website must not imply live hooks or handoff injection for Antigravity.

### Plans

`HomePlansView` currently scans Claude Code plan storage and Google Antigravity plan/brain storage. No Codex, Copilot, or Grok plan source is implemented in this view.

### Skills

The installed-skill catalogue scans Claude and Codex/`.agents` roots. Skill invocation extraction handles Claude and Codex and explicitly returns an empty result for Copilot, Grok, and Antigravity.

### Rules, MCP, and hooks

The rules surface has explicit parsing/representation for Claude, Codex, Antigravity, and Copilot plus shared provider presentation for Grok. The exact artifacts displayed for each provider require fixture-level verification before individual landing pages describe this capability.

### Analytics

The Insights model and provider UI represent all five providers. Richness depends on what each history adapter can extract. Claude and Codex have explicit token/cache/duration parsing. Other providers share normalized analytics structures, but metric availability must be demonstrated with real fixtures before publishing head-to-head or cost claims.

## Safe Homepage Representation

The homepage may accurately say:

> Bring local session history from Claude Code, Codex, GitHub Copilot, Grok Build, and Google Antigravity into one searchable view. Available details and live-continuity features vary by agent.

For a shorter provider strip, label it **Session history from** rather than **Full integration with**.

## Copy That Is Currently Blocked

- “Full support for every coding agent.”
- “Live session capture across all five agents.”
- “Resume any session with one click” without the installed-CLI qualification.
- “All plans, skills, rules, and MCP servers across every agent.”
- Cross-provider cost or performance comparisons without verified fixtures and methodology.
- “Complete transcripts” or “everything your agent did.”

## Verification Required Before Copy Lock

1. Import one representative fixture for every provider.
2. Record prompts, responses, commands, timestamps, paths, branches, models, tokens, cache tokens, and duration recovered from each.
3. Exercise every generated resume command against its current CLI.
4. Connect and disconnect all four hook-capable providers.
5. Verify handoff injection and safe uninstall for each hook format.
6. Confirm Plans behaviour for Claude and Antigravity.
7. Confirm skill catalogue and usage counts for Claude and Codex.
8. Capture the exact MCP/rules/hooks inventory shown for each provider.
9. Approve the final logo-strip label and per-provider landing-page claims.

