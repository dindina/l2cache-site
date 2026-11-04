const memories = {
  agent: {
    kind: 'CODEX SESSION',
    time: '09:12',
    title: 'Mapped the migration path',
    body: 'The session connected the schema change to three migration tests and left a concrete verification command.',
    code: 'xcodebuild test -only-testing:DatabaseMigrationTests',
    links: ['L2Cache', 'feature/recovery-index', 'L2-184']
  },
  terminal: {
    kind: 'TERMINAL · EXIT 65',
    time: '09:46',
    title: 'The first verification failed',
    body: 'The failure stayed attached to the branch, working directory, and agent session that produced it.',
    code: 'DatabaseMigrationTests · testLegacyMarkerDecode failed',
    links: ['12 tests', '1 failure', '~/L2Cache']
  },
  ticket: {
    kind: 'TICKET L2-184',
    time: '10:03',
    title: 'Found the compatibility edge',
    body: 'An older store used a recovery marker that the new indexed decoder did not recognise.',
    code: 'accept legacy marker → normalize → persist indexed form',
    links: ['Compatibility', 'Migration', 'Needs test']
  },
  commit: {
    kind: 'GIT COMMIT',
    time: '10:41',
    title: 'Preserved the old read path',
    body: 'The fix kept existing user data readable while making every new write use the indexed representation.',
    code: 'f34a12c migration: decode legacy recovery marker',
    links: ['3 files', '+41 −8', 'feature/recovery-index']
  },
  success: {
    kind: 'RECOVERY POINT #42',
    time: '10:49',
    title: 'Focused suite passed',
    body: 'L2Cache snapshotted the result, branch evidence, open loops, and exact state to resume in 1 click.',
    code: 'DatabaseMigrationTests · 12 passed · 0 failed',
    links: ['Verified', 'Ready for review', 'Resume']
  },
  mcp: {
    kind: 'MCP TOOL · GET_RECOVERY_POINT',
    time: '10:52',
    title: 'Agent restored context autonomously',
    body: 'Claude Code called built-in l2cache-mcp to query recovery point #42 before composing the PR summary.',
    code: 'l2cache-mcp get_recovery_point(project: \"L2Cache\")',
    links: ['l2cache-mcp', 'Sub-2ms', 'Auto-injected']
  }
};

const events = [...document.querySelectorAll('.event')];
const setMemory = (key, index) => {
  const m = memories[key];
  if (!m) return;
  document.querySelector('#memory-kind').textContent = m.kind;
  document.querySelector('#memory-time').textContent = m.time;
  document.querySelector('#memory-title').textContent = m.title;
  document.querySelector('#memory-body').textContent = m.body;
  document.querySelector('#memory-code').innerHTML = '<span>context</span> ' + m.code;
  document.querySelector('.memory-links').innerHTML = m.links.map(x => '<span>' + x + '</span>').join('');
  events.forEach((e, i) => {
    e.classList.toggle('active', i === index);
    e.setAttribute('aria-pressed', i === index ? 'true' : 'false');
  });
  const count = events.length;
  document.querySelector('#thread-progress').style.height = (15 + (index / (count - 1)) * 80) + '%';
};

events.forEach((event, index) => {
  event.addEventListener('click', () => setMemory(event.dataset.event, index));
});

// Command-K searches
const searches = {
  migration: [
    ['Terminal', 'Focused migration suite failed', 'DatabaseMigrationTests reported the legacy marker mismatch.', '09:46'],
    ['Ticket', 'L2-184 · compatibility edge', 'Older stores encoded the recovery marker differently.', '10:03'],
    ['Codex', 'Restore continuity after index migration', 'The session linked the failure to the old decoder.', '09:12']
  ],
  decision: [
    ['Decision', 'Keep recovery decoding backward-compatible', 'Preserve existing stores; use the indexed form for new writes.', 'Today'],
    ['Git', 'f34a12c · decode legacy marker', 'Three files changed on feature/recovery-index.', '10:41'],
    ['Ticket', 'L2-184 · acceptance note', 'Existing histories must remain readable after upgrade.', '10:03']
  ],
  resume: [
    ['Next action', 'Open review with compatibility note', 'Focused tests pass and the branch is ahead by three commits.', 'Ready'],
    ['Recovery point', 'Migration verified locally', '12 tests passed with no failures.', '10:49'],
    ['MCP Server', 'l2cache-mcp served recovery point', 'Instant context injection for coding agents in 1.8ms.', '10:52']
  ],
  mcp: [
    ['MCP Tool', 'get_recovery_point(L2Cache)', 'Returns branch state, open loops, and test proof.', '10:52'],
    ['MCP Tool', 'search_screenshots(schema)', 'Found database ER diagram in TablePlus capture.', 'Yesterday'],
    ['MCP Tool', 'get_recent_clips(limit: 5)', 'Served 5 recent code snippets to Google Antigravity.', 'Just now']
  ]
};

const questions = {
  migration: 'Where did the migration fail?',
  decision: 'Why did we keep the legacy decoder?',
  resume: 'What should I do next?',
  mcp: 'What can AI agents query via MCP?'
};

const renderResults = key => {
  document.querySelector('#query-text').textContent = questions[key] || '';
  document.querySelector('#query-results').innerHTML = (searches[key] || []).map(([kind, title, body, time]) => '    <article class=\"result\">      <small>' + kind.toUpperCase() + '</small>      <div><b>' + title + '</b><p>' + body + '</p></div>      <time>' + time + '</time>    </article>  ').join('');
};

document.querySelectorAll('.query-chips button').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.query-chips button').forEach(b => b.classList.toggle('active', b === button));
    renderResults(button.dataset.query);
  });
});
renderResults('migration');

// Interactive Agent Sessions
const agentSessions = {
  northstar: {
    agent: 'Codex',
    branch: 'feature/recovery-index',
    time: '34 min',
    title: 'Restore session continuity after the index migration',
    quote: '“Run the focused migration suite, then add the compatibility note to L2-184.”',
    stats: '14 messages · 3 commands · 1 decision'
  },
  orion: {
    agent: 'Google Antigravity',
    branch: 'main',
    time: '18 min',
    title: 'Track subagents & intercept file diffs across tasks',
    quote: '“Captured 4 subagent trajectories, 2 bash commands, and 1 recovery snapshot with zero lag.”',
    stats: '22 turns · 4 tool calls · 1 recovery point'
  },
  maple: {
    agent: 'Claude Code',
    branch: 'release/2.0',
    time: 'Yesterday',
    title: 'Verify SQLite WAL concurrency under connection pressure',
    quote: '“All 48 tests passed. Saved 2,480 prompt cache tokens through local session replay.”',
    stats: '8 commands · 2 diffs · $0.06 saved'
  },
  relay: {
    agent: 'GitHub Copilot',
    branch: 'fix/tokens',
    time: 'Tuesday',
    title: 'Shell command suggestion & multi-line explanation',
    quote: '“Explained xattr removal flags and preserved Gatekeeper quarantine avoidance rules.”',
    stats: '6 suggestions · 2 shell runs'
  }
};

document.querySelectorAll('.agent-list button').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.agent-list button').forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    const s = agentSessions[btn.dataset.session];
    if (!s) return;
    const detail = document.querySelector('.agent-transcript');
    detail.querySelector('.tag').textContent = s.agent;
    detail.querySelector('div span:nth-child(2)').textContent = s.branch;
    detail.querySelector('time').textContent = s.time;
    detail.querySelector('h3').textContent = s.title;
    detail.querySelector('blockquote').textContent = s.quote;
    detail.querySelector('.transcript-footer span:first-child').textContent = s.stats;
  });
});

// Interactive MCP Tool Playground
const mcpResponses = {
  clips: {
    cmd: 'l2cache-mcp://tools/get_recent_clips(limit: 5)',
    json: '{\\n  \"clips\": [\\n    {\\n      \"id\": \"c92b-8a1e\",\\n      \"type\": \"json\",\\n      \"title\": \"Stripe Webhook Payload\",\\n      \"content\": \"{\\\\\\\"event\\\\\\\": \\\\\\\"invoice.payment_succeeded\\\\\\\", \\\\\\\"amount\\\\\\\": 2900}\",\\n      \"time\": \"32s ago\"\\n    },\\n    {\\n      \"id\": \"48ef-7102\",\\n      \"type\": \"command\",\\n      \"title\": \"Docker compose migration\",\\n      \"content\": \"docker compose exec app bundle exec rake db:migrate\",\\n      \"time\": \"2m ago\"\\n    }\\n  ]\\n}'
  },
  recovery: {
    cmd: 'l2cache-mcp://tools/get_recovery_point?project=L2Cache',
    json: '{\\n  \"project\": \"L2Cache\",\\n  \"recovery_point_id\": \"rec_7b1c4a9\",\\n  \"git_branch\": \"feature/recovery-index\",\\n  \"open_loops\": [\\n    \"Verify backward compatibility with legacy recovery markers\"\\n  ],\\n  \"last_failed_command\": \"xcodebuild test (exit 65)\",\\n  \"last_successful_fix\": \"f34a12c migration: decode legacy recovery marker\",\\n  \"tests\": \"12 passed, 0 failed\"\\n}'
  },
  screenshots: {
    cmd: 'l2cache-mcp://tools/search_screenshots?query=schema',
    json: '{\\n  \"matches\": [\\n    {\\n      \"id\": \"scr_8192\",\\n      \"timestamp\": \"2026-10-21T09:14:00Z\",\\n      \"ocr_snippet\": \"CREATE TABLE clip_store (id UUID, mcp_token_cache TEXT...)\",\\n      \"confidence\": 0.98,\\n      \"source_app\": \"TablePlus\"\\n    }\\n  ]\\n}'
  },
  folders: {
    cmd: 'l2cache-mcp://tools/search_memory_folders?tag=api-keys',
    json: '{\\n  \"folder\": \"Production Configs\",\\n  \"items_count\": 8,\\n  \"tags\": [\"api-keys\", \"stripe\", \"aws\"],\\n  \"is_encrypted_keychain\": true\\n}'
  }
};

document.querySelectorAll('.mcp-chips button').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.mcp-chips button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const data = mcpResponses[btn.dataset.tool];
    if (!data) return;
    document.querySelector('#mcp-cmd-text').textContent = data.cmd;
    document.querySelector('#mcp-json-box').textContent = data.json;
  });
});

// Developer Tools Tab Switcher
document.querySelectorAll('.tool-tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tool-tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.tool-panel').forEach(p => p.classList.remove('active'));
    const target = document.getElementById(btn.dataset.panel);
    if (target) target.classList.add('active');
  });
});


// Hero Above-The-Fold Feature Stage Switcher
const heroViews = ['today', 'mcp', 'agents', 'tools', 'terminal'];
let currentHeroViewIdx = 0;
let heroAutoCycle = true;

const setHeroView = viewKey => {
  document.querySelectorAll('.hero-pill-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.view === viewKey);
  });
  document.querySelectorAll('.app-sidebar .sidebar-item').forEach(item => {
    item.classList.toggle('selected', item.dataset.view === viewKey);
  });
  document.querySelectorAll('.hero-view-panel').forEach(panel => {
    panel.classList.toggle('active', panel.id === 'hero-view-' + viewKey);
  });
  currentHeroViewIdx = heroViews.indexOf(viewKey);
};

document.querySelectorAll('.hero-pill-btn, .app-sidebar .sidebar-item').forEach(el => {
  el.addEventListener('click', () => {
    heroAutoCycle = false; // pause auto cycle when user manually clicks
    setHeroView(el.dataset.view);
  });
});

// Auto-cycle through top features on the first screen every 7s if untouched
setInterval(() => {
  if (!heroAutoCycle) return;
  currentHeroViewIdx = (currentHeroViewIdx + 1) % heroViews.length;
  setHeroView(heroViews[currentHeroViewIdx]);
}, 7000);


// Screenshot Zoom Lightbox
const heroWindow = document.querySelector('.hero-full-app-window');
const lightbox = document.getElementById('screenshot-lightbox');
if (heroWindow && lightbox) {
  heroWindow.addEventListener('click', () => {
    lightbox.classList.add('active');
  });
  lightbox.addEventListener('click', () => {
    lightbox.classList.remove('active');
  });
  window.addEventListener('keydown', e => {
    if (e.key === 'Escape') lightbox.classList.remove('active');
  });
}
