#!/usr/bin/env node
// Offline checks for api/waitlist.js with a stubbed fetch. Run: node scripts/test_waitlist_api.js
const assert = require("assert");
const handler = require("../api/waitlist.js");

const VALID = {
  email: "  Sam@Example.com ",
  name: "Sam",
  company: "Acme",
  team_size: "6–15",
  os: ["macos", "wsl", "macos", "bogus"],
  agents: ["claude-code", "codex", "nope"],
  wanted: ["team-updates", "seat-advisor", "secret-alerts", "free-pony"],
  pain: "cold restarts",
  consent: true,
  website: "",
  source: "utm_source=email",
};

function call(body, { method = "POST", env = {}, fetchImpl } = {}) {
  const calls = [];
  const logs = [];
  global.fetch = fetchImpl || (async (url, init) => { calls.push({ url, init }); return { ok: true, status: 201 }; });
  const origError = console.error;
  console.error = (...a) => logs.push(a.join(" "));
  process.env.SUPABASE_URL = "SUPABASE_URL" in env ? env.SUPABASE_URL : "https://proj.supabase.co/";
  delete process.env.SUPABASE_SECRET_KEY;
  process.env.SUPABASE_SERVICE_ROLE_KEY = "KEY" in env ? env.KEY : "eyJhbGciOi.test";
  if (env.SECRET) process.env.SUPABASE_SECRET_KEY = env.SECRET;
  const res = {
    statusCode: 0, headers: {}, payload: null,
    status(c) { this.statusCode = c; return this; },
    setHeader(k, v) { this.headers[k] = v; },
    json(p) { this.payload = p; return this; },
  };
  const req = { method, body, headers: { "user-agent": "test-agent" } };
  return Promise.resolve(handler(req, res)).then(() => { console.error = origError; return { res, calls, logs }; });
}

const tests = {
  async "GET is rejected"() {
    const { res } = await call(VALID, { method: "GET" });
    assert.strictEqual(res.statusCode, 405);
  },
  async "malformed JSON string is a 400"() {
    const { res, calls } = await call("{not json");
    assert.strictEqual(res.statusCode, 400);
    assert.strictEqual(calls.length, 0);
  },
  async "honeypot pretends success and stores nothing"() {
    const { res, calls } = await call({ ...VALID, website: "http://spam" });
    assert.strictEqual(res.statusCode, 200);
    assert.strictEqual(calls.length, 0);
  },
  async "bad email, team size, consent are 400s"() {
    for (const patch of [{ email: "nope" }, { team_size: "7" }, { consent: "true" }]) {
      const { res, calls } = await call({ ...VALID, ...patch });
      assert.strictEqual(res.statusCode, 400, JSON.stringify(patch));
      assert.ok(res.payload.error);
      assert.strictEqual(calls.length, 0);
    }
  },
  async "only email, team size and consent are required"() {
    const { res, calls } = await call({ email: "a@b.co", team_size: "2–5", consent: true });
    assert.strictEqual(res.statusCode, 200);
    const row = JSON.parse(calls[0].init.body);
    assert.deepStrictEqual([row.os, row.agents, row.wanted, row.name], [[], [], [], null]);
  },
  async "proactive-alerts is an allowed wanted value"() {
    const { calls } = await call({ ...VALID, wanted: ["proactive-alerts"] });
    assert.deepStrictEqual(JSON.parse(calls[0].init.body).wanted, ["proactive-alerts"]);
  },
  async "team-skills is an allowed wanted value"() {
    const { calls } = await call({ ...VALID, wanted: ["team-skills"] });
    assert.deepStrictEqual(JSON.parse(calls[0].init.body).wanted, ["team-skills"]);
  },
  async "wanted is optional"() {
    const { res, calls } = await call({ ...VALID, wanted: undefined });
    assert.strictEqual(res.statusCode, 200);
    assert.deepStrictEqual(JSON.parse(calls[0].init.body).wanted, []);
  },
  async "missing env is a 500 without calling Supabase"() {
    const { res, calls } = await call(VALID, { env: { KEY: "" } });
    assert.strictEqual(res.statusCode, 500);
    assert.strictEqual(calls.length, 0);
  },
  async "valid signup inserts a cleaned row"() {
    const { res, calls } = await call(JSON.stringify(VALID));
    assert.strictEqual(res.statusCode, 200);
    assert.strictEqual(calls.length, 1);
    const { url, init } = calls[0];
    assert.strictEqual(url, "https://proj.supabase.co/rest/v1/teams_waitlist?on_conflict=email");
    assert.strictEqual(init.headers.Prefer, "resolution=ignore-duplicates,return=minimal");
    assert.strictEqual(init.headers.Authorization, "Bearer eyJhbGciOi.test");
    const row = JSON.parse(init.body);
    assert.strictEqual(row.email, "sam@example.com");
    assert.deepStrictEqual(row.os, ["macos", "wsl"]);
    assert.deepStrictEqual(row.agents, ["claude-code", "codex"]);
    assert.deepStrictEqual(row.wanted, ["team-updates", "seat-advisor", "secret-alerts"]);
    assert.strictEqual(row.user_agent, "test-agent");
    assert.strictEqual(row.website, undefined);
  },
  async "new sb_secret keys are sent as apikey only"() {
    const { calls } = await call(VALID, { env: { KEY: "sb_secret_abc" } });
    assert.strictEqual(calls[0].init.headers.apikey, "sb_secret_abc");
    assert.strictEqual(calls[0].init.headers.Authorization, undefined);
  },
  async "SUPABASE_SECRET_KEY is used when set"() {
    const { calls } = await call(VALID, { env: { KEY: "", SECRET: "sb_secret_new" } });
    assert.strictEqual(calls[0].init.headers.apikey, "sb_secret_new");
  },
  async "Supabase error is a 502 and logs no personal data"() {
    const { res, logs } = await call(VALID, { fetchImpl: async () => ({ ok: false, status: 401, json: async () => ({ code: "PGRST301" }) }) });
    assert.strictEqual(res.statusCode, 502);
    assert.ok(logs.some((l) => l.includes("401") && l.includes("PGRST301")));
    assert.ok(logs.every((l) => !l.includes("example.com") && !l.includes("Sam")));
  },
  async "network failure is a 502"() {
    const { res } = await call(VALID, { fetchImpl: async () => { throw new TypeError("fetch failed"); } });
    assert.strictEqual(res.statusCode, 502);
  },
};

(async () => {
  let failed = 0;
  for (const [name, fn] of Object.entries(tests)) {
    try { await fn(); console.log(`ok   ${name}`); }
    catch (e) { failed++; console.log(`FAIL ${name}\n     ${e.message}`); }
  }
  console.log(failed ? `${failed} failed` : `all ${Object.keys(tests).length} passed`);
  process.exit(failed ? 1 : 0);
})();
