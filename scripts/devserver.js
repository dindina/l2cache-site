const http = require("http");
const fs = require("fs");
const path = require("path");

const SITE = path.join(process.env.HOME, "tech/l2cache-site");
const OUT = path.join(SITE, "out/teams");

process.env.SUPABASE_URL = process.env.SUPABASE_URL || "https://stub.supabase.co";
process.env.SUPABASE_SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY || "sb_secret_stub";

const inserted = [];
global.fetch = async (url, init) => {
  if (init && init.body) {
    try { inserted.push(JSON.parse(init.body)); } catch (e) { inserted.push(init.body); }
  }
  return { ok: true, status: 201, json: async () => ({}) };
};

const handler = require(path.join(SITE, "api/waitlist.js"));

const types = {
  ".html": "text/html",
  ".css": "text/css",
  ".js": "text/javascript",
  ".png": "image/png",
  ".webp": "image/webp",
  ".jpg": "image/jpeg",
  ".xml": "application/xml",
  ".txt": "text/plain",
  ".svg": "image/svg+xml"
};

const server = http.createServer((req, res) => {
  const u = new URL(req.url, "http://localhost:8766");
  
  if (u.pathname === "/__inserted") {
    res.setHeader("content-type", "application/json");
    return res.end(JSON.stringify(inserted));
  }
  
  if (u.pathname === "/api/waitlist") {
    let b = "";
    req.on("data", c => b += c);
    req.on("end", () => {
      const r = {
        statusCode: 200,
        status(c) { this.statusCode = c; return this; },
        setHeader(k, v) { res.setHeader(k, v); },
        json(p) {
          res.statusCode = this.statusCode;
          res.setHeader("content-type", "application/json");
          res.end(JSON.stringify(p));
        }
      };
      handler({ method: req.method, body: b, headers: req.headers }, r);
    });
    return;
  }
  
  let f = path.join(OUT, u.pathname);
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) {
    f = path.join(f, "index.html");
  }
  if (!fs.existsSync(f) && fs.existsSync(f + ".html")) {
    f += ".html";
  }
  if (!fs.existsSync(f)) {
    res.statusCode = 404;
    return res.end("Not Found");
  }
  res.setHeader("content-type", types[path.extname(f)] || "application/octet-stream");
  fs.createReadStream(f).pipe(res);
});

server.listen(8766, () => {
  console.log("Teams local dev server running on http://localhost:8766/");
});

