// POST /api/waitlist — L2Cache for Teams waitlist signups (teams/script.js).
// Writes one row to Supabase `teams_waitlist` (supabase/teams_waitlist.sql) through the REST API.
// Env (Vercel → Settings → Environment Variables): SUPABASE_URL and SUPABASE_SECRET_KEY
// (sb_secret_…; the legacy service_role key also works, as SUPABASE_SERVICE_ROLE_KEY).
// The key stays server-side; the table has RLS on with no policies, so browsers can't reach it.

const TEAM_SIZES = ["1", "2–5", "6–15", "16–50", "50+"];
const OS = ["macos", "windows", "wsl", "linux"];
const AGENTS = ["claude-code", "codex", "cursor", "copilot", "gemini-cli", "other"];
const WANTED = ["team-updates", "proactive-alerts", "usage-report", "seat-advisor", "quota-forecast", "secret-alerts", "safety-inventory", "pr-recaps", "client-reports", "team-memory", "team-skills"];
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function text(value, max) {
  return typeof value === "string" ? value.trim().slice(0, max) : "";
}

function pick(values, allowed) {
  if (!Array.isArray(values)) return [];
  return [...new Set(values.filter((v) => allowed.includes(v)))];
}

// Returns { row } or { error } with a message the form can show as is.
function validate(body) {
  const email = text(body.email, 254).toLowerCase();
  if (!EMAIL.test(email)) return { error: "Please enter a valid work email." };
  if (!TEAM_SIZES.includes(body.team_size)) return { error: "Please choose how many developers use coding agents." };
  // Everything except email, team size and consent is optional, to keep signing up quick.
  const os = pick(body.os, OS);
  const agents = pick(body.agents, AGENTS);
  if (body.consent !== true) return { error: "Please tick the box so we can email you about early access." };
  return {
    row: {
      email,
      name: text(body.name, 120) || null,
      company: text(body.company, 120) || null,
      team_size: body.team_size,
      os,
      agents,
      wanted: pick(body.wanted, WANTED),
      pain: text(body.pain, 500) || null,
      consent: true,
      source: text(body.source, 300) || null,
    },
  };
}

function parse(req) {
  if (req.body && typeof req.body === "object") return req.body;
  try {
    return JSON.parse(req.body || "{}");
  } catch {
    return null;
  }
}

async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed." });
  }
  const body = parse(req);
  if (!body) return res.status(400).json({ error: "Something went wrong. Please try again." });

  // Honeypot: real visitors never fill the hidden field. Answer as if it worked.
  if (text(body.website, 200)) return res.status(200).json({ ok: true });

  const { row, error } = validate(body);
  if (error) return res.status(400).json({ error });

  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) {
    console.error("waitlist: SUPABASE_URL or SUPABASE_SECRET_KEY is not set");
    return res.status(500).json({ error: "Signups are paused for a moment. Please try again later." });
  }

  row.user_agent = text(req.headers["user-agent"], 300) || null;
  const headers = {
    apikey: key,
    "Content-Type": "application/json",
    // A repeat email is ignored, not an error, so the form never reveals who has signed up.
    Prefer: "resolution=ignore-duplicates,return=minimal",
  };
  // Legacy service_role keys are JWTs and also go in Authorization; new sb_secret_ keys use apikey only.
  if (key.startsWith("eyJ")) headers.Authorization = `Bearer ${key}`;

  try {
    const response = await fetch(`${url.replace(/\/$/, "")}/rest/v1/teams_waitlist?on_conflict=email`, {
      method: "POST",
      headers,
      body: JSON.stringify(row),
    });
    if (!response.ok) {
      // Log the status and Supabase's error code only — never the signup's details.
      const detail = await response.json().catch(() => ({}));
      console.error(`waitlist: insert failed ${response.status} ${detail.code || ""}`);
      return res.status(502).json({ error: "Something went wrong. Please try again, or email support@amvo.store." });
    }
  } catch (err) {
    console.error(`waitlist: insert request failed ${err.name}`);
    return res.status(502).json({ error: "Something went wrong. Please try again, or email support@amvo.store." });
  }
  return res.status(200).json({ ok: true });
}

module.exports = handler;
module.exports.validate = validate;
