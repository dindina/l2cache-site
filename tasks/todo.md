# Session Insights Dashboard

## Milestone 1: Analytics Data Foundation

### Scope

- [x] Preserve canonical event timestamps, model metadata, and token usage while parsing supported session formats.
- [x] Normalize tool call identity, result status, exit code, duration, file paths, and file operation type when the source log provides them.
- [x] Add a backward-compatible `metrics` and `coverage` object to each session.
- [x] Replace fabricated fallback dollar costs with measured cost or an explicit “usage unavailable” state.
- [x] Bump the parser cache schema so stale IndexedDB records are rebuilt safely.
- [x] Keep the current project tree, grid, transcript, search, filters, and provider support working.

### Acceptance

- [x] Existing sample sessions still load and render.
- [x] A transcript containing usage/model/timestamps exposes those values in the normalized session record.
- [x] A transcript without analytics metadata remains usable and reports missing coverage without invented token or cost values.
- [x] File arguments from supported tool calls produce deduplicated normalized file operations.
- [x] Failed tool results retain an error/status signal that later insights can consume.
- [x] Focused parser checks cover both metadata-rich and metadata-poor transcripts.

### Explicit non-goals for this milestone

- No insights dashboard UI yet.
- No hotspot scoring, prompt coaching, or workflow recommendations yet.
- No external pricing service or dependency.
- No attempt to infer token counts when the source does not provide them.

## Review

- Added canonical per-event analytics enrichment and session-level `model`, `metrics`, `coverage`, and `filesTouched` records.
- Preserved explicit source costs only; project summaries now disclose measured coverage or show `usage unavailable`.
- Kept stale cached indexes available while requiring refresh or re-import for the new analytics schema.
- Added dependency-free verification for Claude usage, Anthropic cache tokens, Codex cumulative usage, tool/result correlation, failed patches, cumulative cost, and sparse logs.
- Verified with `rtk proxy node tools/verify-session-normalization.js`, `rtk npm run build`, `rtk git diff --check`, and a browser smoke test of the sample project tree.

## Milestone 2: Action Inbox

### Scope

- [x] Add an Insights view alongside Project Tree, Grid Tiles, and Full History.
- [x] Rank repeated failures, missing verification, frequently revisited files, repeated edits, and analytics coverage gaps.
- [x] Show evidence, impact, confidence, and one concrete action for every recommendation.
- [x] Respect the existing project, branch, agent, and search scope.
- [x] Support opening relevant sessions, copying a follow-up prompt, and dismissing a recommendation.

### Acceptance

- [x] Sample data renders the Action Inbox without breaking existing views.
- [x] Recommendations are derived only from observable session data.
- [x] Empty and filtered states explain why no recommendations are shown.
- [x] Existing parser verification and site build continue to pass.

### Review

- Added a scoped Action Inbox with summary coverage, ranked evidence cards, confidence labels, and plain-language impact.
- Added evidence navigation, follow-up prompt copying, and session-local dismissal.
- Added focused checks for repeated failures, missing verification, and incomplete analytics coverage.
- Verified the parser/insight harness, full site build, diff whitespace, built dashboard rendering, and evidence navigation.
