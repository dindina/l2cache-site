#!/usr/bin/env node
// Replays vercel.json routing offline for every row of docs/LEGACY_URL_INVENTORY.csv (Sprint W4/W5).
//
//   node scripts/check_routes.js            # after `python3 build.py`
//   node scripts/check_routes.js --verbose  # print every route
//
// Model of Vercel's order: cleanUrls (.html → clean, 308), trailingSlash:false (308), then the
// first matching redirect (host-aware via has/missing), then the filesystem under out/l2cache.
// Fails on: a final 404, more hops than allowed, a destination other than the inventory's
// proposed path, or any loop.
const fs = require("fs");
const path = require("path");
const { match, compile } = require("path-to-regexp");

const ROOT = path.join(__dirname, "..");
const OUT = path.join(ROOT, "out", "l2cache");
const NEW_HOST = "l2cache.app";
const OLD_HOST = "l2cache.amvo.store";
const LOCALE_HOMES = ["de", "es", "fr", "it", "ja", "ko", "pt-BR", "vi", "zh-Hans"];
const vercel = JSON.parse(fs.readFileSync(path.join(ROOT, "vercel.json"), "utf8"));
const verbose = process.argv.includes("--verbose");

function hostMatches(conds, host) {
  return (conds || []).every((c) => c.type !== "host" || c.value === host);
}

function redirectFor(host, p) {
  for (const r of vercel.redirects) {
    if (r.has && !hostMatches(r.has, host)) continue;
    if (r.missing && r.missing.some((c) => c.type === "host" && c.value === host)) continue;
    // Vercel matches case-sensitively: live, /zh-hans/support is not caught by the zh-Hans rule.
    const m = match(r.source, { decode: decodeURIComponent, sensitive: true })(p);
    if (!m) continue;
    let dest = r.destination;
    let destHost = host;
    const abs = dest.match(/^https:\/\/([^/]+)(\/.*)?$/);
    if (abs) { destHost = abs[1]; dest = abs[2] || "/"; }
    const toPath = compile(dest, { encode: (x) => x, validate: false });
    return { host: destHost, path: toPath(m.params), status: r.permanent === false ? 307 : 308, rule: r.source };
  }
  return null;
}

function serves(p) {
  const rel = decodeURIComponent(p).replace(/^\//, "");
  const candidates = rel === "" ? ["index.html"] : [rel, `${rel}.html`, path.join(rel, "index.html")];
  return candidates.some((c) => { const f = path.join(OUT, c); return fs.existsSync(f) && fs.statSync(f).isFile(); });
}

function resolve(host, p) {
  const hops = [];
  const seen = new Set();
  for (;;) {
    const key = `${host}${p}`;
    if (seen.has(key)) return { hops, status: "loop", host, path: p };
    seen.add(key);
    let next = null;
    if (vercel.cleanUrls && p.endsWith(".html")) {
      next = { host, path: p.replace(/\/index\.html$/, "").replace(/\.html$/, "") || "/", status: 308, rule: "cleanUrls" };
    } else if (vercel.trailingSlash === false && p.length > 1 && p.endsWith("/")) {
      next = { host, path: p.replace(/\/+$/, ""), status: 308, rule: "trailingSlash" };
    } else {
      next = redirectFor(host, p);
    }
    if (!next) return { hops, status: serves(p) ? 200 : 404, host, path: p };
    hops.push(next);
    host = next.host;
    p = next.path;
  }
}

function rows() {
  const text = fs.readFileSync(path.join(ROOT, "docs", "LEGACY_URL_INVENTORY.csv"), "utf8").trim().split("\n");
  const parse = (line) => line.match(/("([^"]|"")*"|[^,]*)(,|$)/g).map((c) => c.replace(/,$/, "").replace(/^"|"$/g, ""));
  const header = parse(text[0]);
  return text.slice(1).map((l) => Object.fromEntries(parse(l).map((v, i) => [header[i], v])));
}

// Expand template rows ({lang}) into the URLs the installed app actually sends.
function expand(row) {
  if (!row.current_path.includes("{lang}")) return [row.current_path];
  const sent = ["en", "de", "fr", "es", "it", "ja", "ko", "pt-br", "vi", "zh-hans", "ta", "pt-BR", "zh-Hans"];
  return sent.map((l) => row.current_path.replace("{lang}", l));
}

let failures = 0;
let checked = 0;
const report = (ok, line) => { if (!ok) failures++; if (!ok || verbose) console.log(`${ok ? "  ok " : "FAIL "} ${line}`); };

for (const row of rows()) {
  for (const oldPath of expand(row)) {
    checked++;
    const r = resolve(OLD_HOST, oldPath);
    const final = `${r.host}${r.path}`;
    const chain = r.hops.map((h) => `${h.status} ${h.host === OLD_HOST ? "" : h.host}${h.path}`).join(" → ");
    const pre = r.hops.filter((h) => h.rule === "cleanUrls" || h.rule === "trailingSlash").length;
    const isLocaleHome = LOCALE_HOMES.includes(oldPath.replace(/^\//, ""));
    const isTemplate = row.current_path.includes("{lang}");
    let ok = r.status === 200 && r.host === NEW_HOST;
    // One hop to the new domain; a cleanUrls/trailing-slash hop in front is allowed for .html app links.
    // Localized homepages take a second, temporary hop to / until Sprint W3 publishes them.
    const allowed = 1 + pre + (isLocaleHome ? 1 : 0) + (isTemplate ? 1 : 0);
    if (r.hops.length > allowed) ok = false;
    const proposed = row.proposed_path || "";
    if (!isTemplate && !isLocaleHome && proposed.startsWith("/") && !proposed.includes(" ") && r.path !== proposed) ok = false;
    report(ok, `${oldPath}  →  ${final} [${r.status}] (${r.hops.length} hop${r.hops.length === 1 ? "" : "s"}: ${chain || "none"})`);
  }
}

// Every page the build publishes must be served directly on the new domain, with no redirect.
const published = [];
(function walk(dir) {
  for (const name of fs.readdirSync(dir)) {
    const f = path.join(dir, name);
    if (fs.statSync(f).isDirectory()) walk(f);
    else if (name.endsWith(".html")) published.push("/" + path.relative(OUT, f).replace(/(^|\/)index\.html$/, "").replace(/\.html$/, ""));
  }
})(OUT);
// /tools/* is a duplicate copy that redirects to /en/tools/* by design (inventory action REDIRECT).
for (const p of published.filter((x) => !x.startsWith("/tools"))) {
  checked++;
  const url = p === "/" ? "/" : p.replace(/\/$/, "");
  const r = resolve(NEW_HOST, url);
  report(r.status === 200 && r.hops.length === 0, `${NEW_HOST}${url} [${r.status}] ${r.hops.length ? "redirects: " + r.hops.map((h) => h.path).join(" → ") : "served directly"}`);
}

console.log(`\n${checked} routes checked, ${failures} failure(s).`);
process.exit(failures ? 1 : 0);
