const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

const htmlPath = require('node:path').join(__dirname, 'claude-session-viewer.html');
const html = fs.readFileSync(htmlPath, 'utf8');

const scriptMarker = '<!-- Script: Parser, Multi-Agent Indexer, IndexedDB Persistence & Workspace Logic -->';
const markerIndex = html.indexOf(scriptMarker);
const scriptStart = html.indexOf('<script>', markerIndex) + '<script>'.length;
const scriptEnd = html.indexOf('</script>', scriptStart);
assert(markerIndex >= 0 && scriptStart > 0 && scriptEnd > scriptStart, 'main viewer script must be discoverable');
new vm.Script(html.slice(scriptStart, scriptEnd), { filename: 'claude-session-viewer.inline.js' });

const agentStart = html.indexOf('function detectAgent');
const agentEnd = html.indexOf('// Drag and drop listeners', agentStart);
const parserStart = html.indexOf('function isSystemContextText');
const parserEnd = html.indexOf('function populateFilterDropdowns', parserStart);
const usageStart = html.indexOf('function summarizeMeasuredUsage');
const usageEnd = html.indexOf('function toggleProjectCollapse', usageStart);
const insightsStart = html.indexOf('function getSessionToolExecutions');
const insightsEnd = html.indexOf('function openInsightEvidence', insightsStart);
assert(agentStart >= 0 && agentEnd > agentStart, 'agent detector must be discoverable');
assert(parserStart >= 0 && parserEnd > parserStart, 'parser block must be discoverable');
assert(usageStart >= 0 && usageEnd > usageStart, 'usage formatter block must be discoverable');
assert(insightsStart >= 0 && insightsEnd > insightsStart, 'insights analyzer block must be discoverable');

const context = { console };
vm.createContext(context);
vm.runInContext(`
  const grokMetaCache = new Map();
  ${html.slice(agentStart, agentEnd)}
  ${html.slice(parserStart, parserEnd)}
  ${html.slice(usageStart, usageEnd)}
  ${html.slice(insightsStart, insightsEnd)}
  globalThis.analyticsApi = { parseFileIntoSessions, formatMeasuredUsage, buildActionInsights };
`, context, { filename: 'session-normalization-test-bundle.js' });

const { parseFileIntoSessions, formatMeasuredUsage, buildActionInsights } = context.analyticsApi;
const richTranscript = [
  JSON.stringify({
    type: 'user',
    sessionId: 'rich-session',
    cwd: '/repo',
    gitBranch: 'main',
    timestamp: '2026-09-30T00:00:00.000Z',
    message: { content: 'Fix the parser and verify it.' }
  }),
  JSON.stringify({
    type: 'assistant',
    timestamp: '2026-09-30T00:01:00.000Z',
    message: {
      model: 'claude-test-model',
      usage: {
        input_tokens: 100,
        output_tokens: 20,
        cache_read_input_tokens: 80,
        cache_creation_input_tokens: 10,
        cost_usd: 0.012
      },
      content: [
        { type: 'text', text: 'I will update the parser.' },
        { type: 'tool_use', id: 'tool-1', name: 'Edit', input: { file_path: '/repo/src/parser.js' } },
        { type: 'tool_use', id: 'tool-2', name: 'Edit', input: { file_path: '/repo/src/parser.js' } }
      ]
    }
  }),
  JSON.stringify({
    type: 'user',
    timestamp: '2026-09-30T00:02:00.000Z',
    message: { content: [{ type: 'tool_result', tool_use_id: 'tool-1', is_error: true, content: 'Edit failed' }] }
  })
].join('\n');

const rich = parseFileIntoSessions(richTranscript, {
  name: 'rich.jsonl',
  customRelativePath: '.claude/projects/demo/rich.jsonl',
  lastModified: Date.parse('2026-09-30T00:03:00.000Z')
}, 0)[0];

assert(rich, 'metadata-rich transcript should parse');
assert.equal(rich.model, 'claude-test-model');
assert.equal(rich.metrics.inputTokens, 100);
assert.equal(rich.metrics.outputTokens, 20);
assert.equal(rich.metrics.cacheReadTokens, 80);
assert.equal(rich.metrics.cacheCreationTokens, 10);
assert.equal(rich.metrics.totalTokens, 210);
assert.equal(rich.metrics.actualCost, 0.012);
assert.equal(rich.metrics.costBasis, 'source');
assert.equal(rich.metrics.startTimestamp, '2026-09-30T00:00:00.000Z');
assert.equal(rich.metrics.endTimestamp, '2026-09-30T00:02:00.000Z');
assert.equal(rich.metrics.durationMs, 120000);
assert.equal(rich.coverage.tokens, true);
assert.equal(rich.coverage.model, true);
assert.equal(rich.coverage.cost, true);
assert.equal(rich.filesTouched.length, 1);
assert.equal(rich.filesTouched[0].path, '/repo/src/parser.js');
assert.equal(rich.filesTouched[0].operation, 'edit');
assert.equal(rich.filesTouched[0].occurrences, 2);
assert.equal(rich.filesTouched[0].failed, true);
assert(rich.events.some(event => event.toolCallId === 'tool-1' && event.isError === true));
assert.equal(rich.metrics.toolExecutions, 2);
assert.equal(rich.metrics.failedToolExecutions, 1);
assert.equal(rich.coverage.toolStatus, 0.5);

const codexTranscript = [
  JSON.stringify({ type: 'session_meta', payload: { id: 'codex-session', cwd: '/repo', model: 'gpt-test-model' } }),
  JSON.stringify({ type: 'event_msg', payload: { type: 'user_message', message: 'Inspect the cache.' } }),
  JSON.stringify({ type: 'event_msg', payload: { type: 'agent_message', message: 'Inspection complete.' } }),
  JSON.stringify({
    type: 'event_msg',
    payload: {
      type: 'token_count',
      info: {
        total_token_usage: {
          input_tokens: 250,
          output_tokens: 50,
          cached_input_tokens: 100,
          reasoning_tokens: 15,
          total_tokens: 300
        }
      }
    }
  })
].join('\n');
const codex = parseFileIntoSessions(codexTranscript, {
  name: 'rollout.jsonl',
  customRelativePath: '.codex/sessions/demo/rollout.jsonl',
  lastModified: Date.parse('2026-09-30T00:03:00.000Z')
}, 1)[0];

assert(codex, 'Codex transcript should parse');
assert.equal(codex.model, 'gpt-test-model');
assert.equal(codex.metrics.inputTokens, 250);
assert.equal(codex.metrics.outputTokens, 50);
assert.equal(codex.metrics.cacheReadTokens, 100);
assert.equal(codex.metrics.reasoningTokens, 15);
assert.equal(codex.metrics.totalTokens, 300);
assert.equal(codex.metrics.actualCost, null);
assert.equal(codex.coverage.tokens, true);

const codexToolTranscript = [
  JSON.stringify({ type: 'event_msg', payload: { type: 'user_message', message: 'Apply the patch.' } }),
  JSON.stringify({
    type: 'response_item',
    payload: {
      type: 'custom_tool_call',
      call_id: 'codex-tool-1',
      name: 'apply_patch',
      input: '*** Begin Patch\n*** Update File: src/cache.js\n*** End Patch'
    }
  }),
  JSON.stringify({
    type: 'response_item',
    payload: { type: 'custom_tool_call_output', call_id: 'codex-tool-1', output: 'Patch failed', status: 'failed' }
  })
].join('\n');
const codexTool = parseFileIntoSessions(codexToolTranscript, {
  name: 'rollout-tools.jsonl',
  customRelativePath: '.codex/sessions/demo/rollout-tools.jsonl',
  lastModified: Date.parse('2026-09-30T00:03:00.000Z')
}, 2)[0];

assert(codexTool, 'Codex tool transcript should parse');
assert.equal(codexTool.metrics.toolExecutions, 1);
assert.equal(codexTool.metrics.failedToolExecutions, 1);
assert.equal(codexTool.filesTouched.length, 1);
assert.equal(codexTool.filesTouched[0].path, 'src/cache.js');
assert.equal(codexTool.filesTouched[0].failed, true);

const cumulativeCostTranscript = [
  JSON.stringify({ type: 'USER_INPUT', content: 'Measure the run.' }),
  JSON.stringify({ type: 'PLANNER_RESPONSE', content: 'First step.', usage: { input_tokens: 10, total_cost_usd: 0.01 } }),
  JSON.stringify({ type: 'PLANNER_RESPONSE', content: 'Second step.', usage: { input_tokens: 10, total_cost_usd: 0.02 } })
].join('\n');
const cumulativeCost = parseFileIntoSessions(cumulativeCostTranscript, {
  name: 'cost.jsonl',
  customRelativePath: '.claude/projects/demo/cost.jsonl',
  lastModified: Date.parse('2026-09-30T00:03:00.000Z')
}, 3)[0];
assert.equal(cumulativeCost.metrics.actualCost, 0.02);

const sparseTranscript = [
  JSON.stringify({ type: 'USER_INPUT', content: 'Explain this function.' }),
  JSON.stringify({ type: 'PLANNER_RESPONSE', content: 'Here is the explanation.' })
].join('\n');
const sparse = parseFileIntoSessions(sparseTranscript, {
  name: 'sparse.jsonl',
  customRelativePath: '.claude/projects/demo/sparse.jsonl',
  lastModified: Date.parse('2026-09-30T00:03:00.000Z')
}, 4)[0];

assert(sparse, 'metadata-poor transcript should remain usable');
assert.equal(sparse.metrics.inputTokens, null);
assert.equal(sparse.metrics.outputTokens, null);
assert.equal(sparse.metrics.totalTokens, null);
assert.equal(sparse.metrics.actualCost, null);
assert.equal(sparse.metrics.costBasis, 'unavailable');
assert.equal(sparse.coverage.tokens, false);
assert.equal(sparse.coverage.model, false);
assert.equal(sparse.coverage.timestamps, 0);
assert.deepEqual(Array.from(sparse.filesTouched), []);
assert.equal(formatMeasuredUsage([sparse]), 'usage unavailable');
assert(!formatMeasuredUsage([sparse]).includes('$0.00'));

const actionInsights = buildActionInsights([rich, codexTool, sparse]);
assert(actionInsights.some(insight => insight.type === 'verification' && insight.sessionIds.includes(rich.id)), 'changed files without a successful check should be actionable');
assert(actionInsights.some(insight => insight.type === 'coverage'), 'missing token metadata should create a coverage action');

const repeatedFailureSession = {
  ...sparse,
  id: 99,
  title: 'Repeated build failure',
  metrics: { ...sparse.metrics, failedToolExecutions: 2 },
  events: [0, 1].map(index => ({
    index,
    role: 'tool',
    type: 'COMMAND_EXECUTION',
    content: 'npm test',
    isError: true,
    toolStatus: 'error',
    toolCalls: [{ name: 'exec', arguments: { command: 'npm test', exit_code: 1 } }]
  }))
};
assert(buildActionInsights([repeatedFailureSession]).some(insight => insight.type === 'failure'), 'repeated identical failures should be detected');

assert(html.includes("const PARSER_SCHEMA_VERSION = 'v2026_09_30_analytics_v11';"), 'parser cache schema must invalidate v10 records');
console.log('Session normalization verification passed.');
