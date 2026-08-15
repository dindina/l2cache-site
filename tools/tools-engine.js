// ===================================================
//  L2Cache Web Tools Engine: Privacy Interceptor & Pac-Man Engine
// ===================================================

let blockedCount = 0;
let opsCount = 0;
let bytesProcessed = 0;
let offlineMode = false;
let offlineStart = null;
let offlineTimerInterval = null;

// Intercept fetch
const origFetch = window.fetch;
window.fetch = async (...args) => {
  const url = String(args[0]?.url ?? args[0]);
  if (offlineMode) {
    logBlockedRequest(url, 'fetch');
    return new Response(null, { status: 0 });
  }
  if (!url.startsWith('https://fonts.googleapis.com') && !url.startsWith('https://fonts.gstatic.com')) {
    logBlockedRequest(url, 'fetch');
    return new Response(null, { status: 0 });
  }
  return origFetch(...args);
};

// Intercept XMLHttpRequest
const origOpen = XMLHttpRequest.prototype.open;
XMLHttpRequest.prototype.open = function(method, url) {
  logBlockedRequest(String(url), 'xhr');
};
XMLHttpRequest.prototype.send = function() {};

function logBlockedRequest(url, type) {
  blockedCount++;
  console.warn(`[L2Cache Privacy] Blocked ${type} request to: ${url}`);
}

function logLocalOp(description, byteCount) {
  opsCount++;
  bytesProcessed += byteCount;
}

// ── Airplane Mode Toggle ──
function toggleOfflineMode() {
  offlineMode = !offlineMode;
  const bar   = document.getElementById('offline-challenge-bar');
  const btn   = document.getElementById('offline-toggle-btn');
  const label = document.getElementById('btn-label');
  const icon  = document.getElementById('btn-icon');
  const pill  = document.getElementById('status-pill');
  const stext = document.getElementById('status-text');
  const timer = document.getElementById('offline-timer');

  if (offlineMode) {
    offlineStart = Date.now();
    if (bar) bar.classList.add('offline-active');
    if (btn) btn.classList.add('is-offline');
    if (icon) icon.textContent = '🔴';
    if (label) label.textContent = 'Restore Network';
    if (pill) pill.className = 'status-pill offline';
    if (stext) stext.textContent = 'AIRPLANE MODE';
    if (timer) timer.style.display = 'inline';

    offlineTimerInterval = setInterval(() => {
      const secs = Math.floor((Date.now() - offlineStart) / 1000);
      const display = secs >= 60 ? Math.floor(secs/60) + 'm ' + (secs % 60) + 's' : secs + 's';
      if (timer) timer.textContent = display;
    }, 1000);

    showToast('✈️ Airplane Mode ON — all tools run 100% offline in your browser.');
  } else {
    clearInterval(offlineTimerInterval);
    offlineStart = null;
    if (bar) bar.classList.remove('offline-active');
    if (btn) btn.classList.remove('is-offline');
    if (icon) icon.textContent = '✈️';
    if (label) label.textContent = 'Airplane Mode Challenge';
    if (pill) pill.className = 'status-pill online';
    if (stext) stext.textContent = 'NETWORK ON';
    if (timer) { timer.style.display = 'none'; timer.textContent = ''; }
    showToast('📶 Network restored.');
  }
}

// ── Pac-Man Transform Animation Engine ──
const PAC_PELLETS = {
  jwt:  ['header', '.', 'payload', '.', 'sig', 'exp', 'sub', 'aud'],
  json: ['"key"', '{ }', 'null', '[]', 'true', ':', ',', '...'],
  ts:   ['interface', 'type', 'string', 'number', 'z.infer', 'ZodSchema'],
  sql:  ['SELECT', 'FROM', 'WHERE', 'JOIN', 'GROUP BY', 'LIMIT'],
  csv:  ['| Header |', '| Data |', 'row_1', 'row_2', '---'],
  utm:  ['utm_source', '&fbclid', '&gclid', '?ref=', '&mc_eid']
};
const PAC_SCORE = { jwt: '+500', json: '+250', ts: '+400', sql: '+350', csv: '+200', utm: '+150' };

function withPacman(trackId, pacmanId, outputId, pelletType, result) {
  const track  = document.getElementById(trackId);
  const pacman = document.getElementById(pacmanId);
  const output = document.getElementById(outputId);
  if (!track || !pacman) {
    if (output) {
      output.textContent = result;
      output.className = result.startsWith('❌') ? 'tool-output-view error' : 'tool-output-view';
    }
    return;
  }

  // Clear previous elements
  [...track.querySelectorAll('.pac-pellet,.pac-score,.pac-burst-star')].forEach(el => el.remove());
  if (output) {
    output.textContent = '';
    output.className = 'tool-output-view';
  }

  const labels = PAC_PELLETS[pelletType] || ['...'];
  const trackW = track.offsetWidth || 380;
  const pelletGap = Math.max(48, (trackW - 70) / labels.length);
  const pellets = [];

  labels.forEach((label, i) => {
    const el = document.createElement('span');
    el.className = 'pac-pellet';
    el.textContent = label;
    const leftPx = 45 + i * pelletGap;
    el.style.left = leftPx + 'px';
    track.appendChild(el);
    pellets.push({ el, leftPx });
  });

  track.classList.add('running');

  const DURATION = 1100;
  const startLeft = -34;
  const endLeft = trackW + 10;
  const startTime = performance.now();
  let lastEaten = -1;

  function step(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / DURATION, 1);
    const ease = progress < 0.5 ? 2 * progress * progress : -1 + (4 - 2 * progress) * progress;
    const curLeft = startLeft + (endLeft - startLeft) * ease;

    pacman.style.left = curLeft + 'px';

    pellets.forEach((p, idx) => {
      if (curLeft > p.leftPx - 6 && idx > lastEaten) {
        lastEaten = idx;
        p.el.classList.add('eaten');
        spawnScore(track, p.leftPx, PAC_SCORE[pelletType] || '+100');
      }
    });

    if (progress < 1) {
      requestAnimationFrame(step);
    } else {
      spawnBurst(track, trackW - 20, '✦');
      setTimeout(() => {
        track.classList.remove('running');
        pacman.style.left = '-34px';
        if (output && result !== null && result !== undefined) {
          typewriterReveal(output, result, result.startsWith('❌') ? 'tool-output-view error' : 'tool-output-view');
        }
      }, 350);
    }
  }

  requestAnimationFrame(step);
}

function spawnScore(parent, leftPx, text) {
  const el = document.createElement('span');
  el.className = 'pac-score';
  el.textContent = text;
  el.style.left = (leftPx - 10) + 'px';
  el.style.top = '4px';
  parent.appendChild(el);
  setTimeout(() => el.remove(), 600);
}

function spawnBurst(parent, leftPx, emoji) {
  for (let i = 0; i < 4; i++) {
    const el = document.createElement('span');
    el.className = 'pac-burst-star';
    el.textContent = emoji;
    el.style.right = (parent.offsetWidth - leftPx + (i - 1.5) * 12) + 'px';
    el.style.animationDelay = (i * 60) + 'ms';
    parent.appendChild(el);
    setTimeout(() => el.remove(), 800);
  }
}

function typewriterReveal(el, text, className) {
  el.className = className;
  el.textContent = '';
  const charDelay = Math.min(14, Math.max(1, 600 / (text.length || 1)));
  let i = 0;
  function typeNext() {
    if (i < text.length) {
      el.textContent += text[i++];
      setTimeout(typeNext, charDelay);
    }
  }
  typeNext();
}

// ── Copy to Clipboard & Toast ──
let toastTimer;
function showToast(msg) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2600);
}

function copyOutput(id) {
  const el = document.getElementById(id);
  if (!el) return;
  const text = el.textContent || el.value;
  if (!text || text.startsWith('//')) return;
  navigator.clipboard.writeText(text).then(() => {
    showToast('✅ Copied to clipboard! (Automate on Mac with L2Cache)');
  });
}

// ===================================================
//  Standalone Converter Code Exporter & Downloader
// ===================================================

const TOOL_STANDALONE_SNIPPETS = {
  'json-unescaper': {
    title: 'JSON String Unescaper & Log Cleaner',
    js: `// Standalone JavaScript JSON String Unescaper
function unescapeJSONString(raw) {
  let text = raw.trim();
  if ((text.startsWith('"') && text.endsWith('"')) || (text.startsWith("'") && text.endsWith("'"))) {
    try { text = JSON.parse(text); } catch(e) { text = text.slice(1, -1); }
  }
  return text.replace(/\\\\"/g, '"').replace(/\\\\n/g, '\\n').replace(/\\\\t/g, '\\t').replace(/\\\\\\\\/g, '\\\\');
}`,
    py: `# Standalone Python JSON Log Unescaper
import json

def unescape_json(raw_str: str) -> str:
    cleaned = raw_str.strip()
    if cleaned.startswith('"') and cleaned.endswith('"'):
        try:
            return json.loads(cleaned)
        except Exception:
            pass
    return cleaned.replace('\\\\"', '"').replace('\\\\n', '\\n').replace('\\\\t', '\\t')`
  },

  'json-to-yaml': {
    title: 'JSON to YAML Serializer',
    js: `// Standalone JavaScript JSON to YAML Serializer
function jsonToYaml(obj, indent = 0) {
  const spaces = '  '.repeat(indent);
  if (obj === null || obj === undefined) return 'null';
  if (typeof obj !== 'object') return String(obj);
  if (Array.isArray(obj)) return obj.map(i => \`\${spaces}- \${jsonToYaml(i, indent + 1).trimStart()}\`).join('\\n');
  return Object.entries(obj).map(([k, v]) => \`\${spaces}\${k}: \${jsonToYaml(v, indent + 1).trimStart()}\`).join('\\n');
}`,
    py: `# Standalone Python JSON to YAML Converter
import json, yaml

def json_to_yaml(json_str: str) -> str:
    data = json.loads(json_str)
    return yaml.dump(data, default_flow_style=False, sort_keys=False)`
  },

  'sql-to-json': {
    title: 'SQL DDL to Mock Data JSON Generator',
    js: `// Standalone JavaScript SQL DDL to Mock JSON Generator
function ddlToMockJson(tableName, columns, count = 3) {
  const records = [];
  for (let i = 0; i < count; i++) {
    const row = {};
    columns.forEach(c => { row[c] = \`\${c}_\${i+1}\`; });
    records.push(row);
  }
  return JSON.stringify(records, null, 2);
}`,
    py: `# Standalone Python SQL DDL Mock Generator
import json

def ddl_to_mock(cols: list, count: int = 3) -> str:
    records = [{c: f"{c}_{i+1}" for c in cols} for i in range(count)]
    return json.dumps(records, indent=2)`
  },

  'schemaforge': {
    title: 'SchemaForge AST Multi-Target Model Generator',
    js: `// Standalone JavaScript JSON to Swift & TypeScript Model Generator
function generateSwiftAndTS(jsonObj, structName = 'DataModel') {
  const swiftProps = [];
  const tsProps = [];

  for (const [k, v] of Object.entries(jsonObj)) {
    const isNum = typeof v === 'number';
    const isBool = typeof v === 'boolean';
    const isArr = Array.isArray(v);
    const isStr = typeof v === 'string';

    const swiftType = isStr ? 'String' : (isNum ? (Number.isInteger(v) ? 'Int' : 'Double') : (isBool ? 'Bool' : 'Any'));
    const tsType = isStr ? 'string' : (isNum ? 'number' : (isBool ? 'boolean' : 'any'));

    swiftProps.push(\`  let \${k}: \${swiftType}\`);
    tsProps.push(\`  \${k}: \${tsType};\`);
  }

  return {
    swift: \`struct \${structName}: Codable {\n\${swiftProps.join('\\n')}\n}\`,
    ts: \`export interface \${structName} {\n\${tsProps.join('\\n')}\n}\`
  };
}`,
    py: `# Standalone Python JSON to Pydantic Model Generator
import json

def json_to_pydantic(json_str: str, class_name: str = "DataModel") -> str:
    data = json.loads(json_str)
    lines = ["from pydantic import BaseModel", "", f"class {class_name}(BaseModel):"]
    for k, v in data.items():
        t = "str" if isinstance(v, str) else ("int" if isinstance(v, int) else ("float" if isinstance(v, float) else "bool"))
        lines.append(f"    {k}: {t}")
    return "\\n".join(lines)`
  },

  'sql-query-converter': {
    title: 'SQL CRUD Query Transformer (SELECT ⇄ INSERT ⇄ UPDATE ⇄ DELETE)',
    js: `// Standalone JavaScript SQL Query Transformer
function convertSelectToInsert(tableName, columns, values) {
  const colList = columns.join(', ');
  const valList = values.map(v => typeof v === 'number' ? v : \`'\${v}'\`).join(', ');
  return \`INSERT INTO \${tableName} (\${colList}) VALUES (\${valList});\`;
}

function convertSelectToUpdate(tableName, columns, values, whereClause = 'WHERE id = 1') {
  const setPairs = columns.map((c, i) => \`\${c} = '\${values[i] || ''}'\`).join(', ');
  return \`UPDATE \${tableName} SET \${setPairs} \${whereClause};\`;
}`,
    py: `# Standalone Python SQL Query Builder
def build_crud_queries(table: str, cols: list, vals: list, where: str = "WHERE id = 1"):
    col_str = ", ".join(cols)
    val_str = ", ".join(f"'{v}'" if isinstance(v, str) else str(v) for v in vals)
    set_str = ", ".join(f"{c} = '{v}'" for c, v in zip(cols, vals))
    
    return {
        "insert": f"INSERT INTO {table} ({col_str}) VALUES ({val_str});",
        "update": f"UPDATE {table} SET {set_str} {where};",
        "delete": f"DELETE FROM {table} {where};"
    }`
  },

  'universal-data-converter': {
    title: 'Universal Multi-Format Serializer (JSON ⇄ YAML ⇄ XML ⇄ CSV)',
    js: `// Standalone JavaScript Universal Multi-Format Converter
function convertObject(obj) {
  return {
    json: JSON.stringify(obj, null, 2),
    yaml: objToYaml(obj),
    xml: objToXml(obj),
    csv: objToCsv(obj)
  };
}`,
    py: `# Standalone Python Universal Multi-Format Converter
import json, yaml, csv, io
import xml.etree.ElementTree as ET

def convert_all(data):
    json_str = json.dumps(data, indent=2)
    yaml_str = yaml.dump(data, default_flow_style=False)
    return {"json": json_str, "yaml": yaml_str}`
  },

  'regexlens': {
    title: 'RegexLens AST Tokenizer & ReDoS Checker',
    js: `// Standalone JavaScript Regex AST Tokenizer & ReDoS Detector
function analyzeRegex(pattern) {
  const redosRisks = [
    /\\([^\\)]*[\\+\\*]\\)[\\+\\*]/,
    /\\([^\\)]*\\|[\\)]*\\)[\\+\\*]/
  ];
  const hasReDoS = redosRisks.some(r => r.test(pattern));

  return {
    pattern,
    hasReDoS,
    length: pattern.length,
    status: hasReDoS ? 'DANGER: ReDoS Catastrophic Backtracking' : 'SAFE'
  };
}`,
    py: `# Standalone Python Regex AST & ReDoS Analyzer
import re

def analyze_regex(pattern: str) -> dict:
    redos_rules = [
        r'\\([^\\)]*[\\+\\*]\\)[\\+\\*]',
        r'\\([^\\)]*\\|[\\)]*\\)[\\+\\*]'
    ]
    has_redos = any(re.search(r, pattern) for r in redos_rules)
    return {
        "pattern": pattern,
        "is_safe": not has_redos,
        "risk_level": "HIGH" if has_redos else "LOW"
    }`
  },

  'pasteguard': {
    title: 'PasteGuard Secret Scrubber & Redactor',
    js: `// Standalone JavaScript Secret Scrubber for AI Prompts
function sanitizeSecretsForAI(rawCode) {
  const rules = [
    { re: /sk-[a-zA-Z0-9_-]{20,}/g, mock: 'sk-proj-SAMPLE_MOCK_KEY' },
    { re: /AKIA[0-9A-Z]{16}/g, mock: 'AKIA_MOCK_AWS_ACCESS_KEY_SAFE' },
    { re: /sk_live_[0-9a-zA-Z]{24,}/g, mock: 'sk_test_SAMPLE_MOCK_STRIPE_KEY' },
    { re: /gh[pousr]_[0-9a-zA-Z]{36}/g, mock: 'ghp_SAMPLE_MOCK_GITHUB_TOKEN' },
    { re: /(postgres|postgresql|mysql|mongodb):\\/\\/[^:\\s]+:[^@\\s]+@[^\\s"']+/gi, mock: 'postgresql://mock_user:mock_pass@localhost:5432/mock_db' }
  ];

  let clean = rawCode;
  rules.forEach(({ re, mock }) => {
    clean = clean.replace(re, mock);
  });
  return clean;
}`,
    py: `# Standalone Python Secret Scrubber for AI Prompts
import re

def sanitize_for_ai(raw_text: str) -> str:
    rules = [
        (r'sk-[a-zA-Z0-9_-]{20,}', 'sk-proj-SAMPLE_MOCK_KEY'),
        (r'AKIA[0-9A-Z]{16}', 'AKIA_MOCK_AWS_ACCESS_KEY_SAFE'),
        (r'sk_live_[0-9a-zA-Z]{24,}', 'sk_test_SAMPLE_MOCK_STRIPE_KEY'),
        (r'gh[pousr]_[0-9a-zA-Z]{36}', 'ghp_SAMPLE_MOCK_GITHUB_TOKEN'),
        (r'(postgres|postgresql|mysql|mongodb)://[^:\s]+:[^@\s]+@[^\s"\']+', 'postgresql://mock_user:mock_pass@localhost:5432/mock_db')
    ]
    cleaned = raw_text
    for pattern, mock in rules:
        cleaned = re.sub(pattern, mock, cleaned)
    return cleaned`
  },

  'pdf-password-protect': {
    title: 'PDF Password Encryption Engine',
    js: `// Standalone Node.js / Browser script to password protect a PDF
// Uses pdf-lib + standard PDF encryption (RC4-128 / AES)
const fs = require('fs');
const { PDFDocument } = require('pdf-lib');
const { encryptPDF } = require('@pdfsmaller/pdf-encrypt-lite');

async function lockPDF(inputPath, outputPath, password) {
  const inputBytes = fs.readFileSync(inputPath);
  const encryptedBytes = await encryptPDF(new Uint8Array(inputBytes), password);
  fs.writeFileSync(outputPath, Buffer.from(encryptedBytes));
  console.log(\`Successfully encrypted \${outputPath} with password: \${password}\`);
}

// Usage:
// lockPDF('confidential.pdf', 'confidential-protected.pdf', 'MySecretPassword123');`,
    py: `# Standalone Python script to password protect a PDF
# Requires: pip install pypdf
from pypdf import PdfReader, PdfWriter

def protect_pdf(input_path: str, output_path: str, user_password: str):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # 128-bit AES / RC4 standard PDF encryption
    writer.encrypt(user_password=user_password, owner_pwd=None, use_128bit=True)

    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"🔒 Encrypted {output_path} successfully.")

if __name__ == "__main__":
    protect_pdf("document.pdf", "document-protected.pdf", "secret_pass_123")`
  },

  'json-diff': {
    title: 'Semantic JSON Diff Engine',
    js: `// Standalone JS Recursive Semantic JSON Diff Function
function semanticJSONDiff(obj1, obj2, path = '') {
  const diffs = [];

  if (obj1 === undefined && obj2 !== undefined) {
    return [{ type: 'add', path, val: obj2 }];
  }
  if (obj1 !== undefined && obj2 === undefined) {
    return [{ type: 'del', path, val: obj1 }];
  }
  if (typeof obj1 !== typeof obj2) {
    return [{ type: 'mod', path, from: obj1, to: obj2, note: 'Type changed' }];
  }
  if (typeof obj1 !== 'object' || obj1 === null || obj2 === null) {
    if (obj1 !== obj2) {
      return [{ type: 'mod', path, from: obj1, to: obj2 }];
    }
    return [];
  }

  if (Array.isArray(obj1) && Array.isArray(obj2)) {
    const maxLen = Math.max(obj1.length, obj2.length);
    for (let i = 0; i < maxLen; i++) {
      diffs.push(...semanticJSONDiff(obj1[i], obj2[i], \`\${path}[\${i}]\`));
    }
    return diffs;
  }

  const allKeys = new Set([...Object.keys(obj1), ...Object.keys(obj2)]);
  for (const key of allKeys) {
    const nextPath = path ? \`\${path}.\${key}\` : key;
    diffs.push(...semanticJSONDiff(obj1[key], obj2[key], nextPath));
  }
  return diffs;
}

// Example:
const a = { name: "Alice", role: "dev", tags: ["js"] };
const b = { name: "Alice", role: "lead", tags: ["js", "swift"], id: 101 };
console.log(semanticJSONDiff(a, b));`,
    py: `# Standalone Python Semantic Deep Diff
import json
from typing import Any, List, Dict

def diff_json(v1: Any, v2: Any, path: str = "") -> List[Dict[str, Any]]:
    diffs = []
    if type(v1) != type(v2):
        return [{"type": "TYPE_MOD", "path": path, "from": v1, "to": v2}]
    if isinstance(v1, dict):
        all_keys = set(v1.keys()) | set(v2.keys())
        for k in sorted(all_keys):
            p = f"{path}.{k}" if path else k
            if k not in v1:
                diffs.append({"type": "ADD", "path": p, "val": v2[k]})
            elif k not in v2:
                diffs.append({"type": "DEL", "path": p, "val": v1[k]})
            else:
                diffs.extend(diff_json(v1[k], v2[k], p))
    elif isinstance(v1, list):
        max_l = max(len(v1), len(v2))
        for i in range(max_l):
            p = f"{path}[{i}]"
            if i >= len(v1):
                diffs.append({"type": "ADD", "path": p, "val": v2[i]})
            elif i >= len(v2):
                diffs.append({"type": "DEL", "path": p, "val": v1[i]})
            else:
                diffs.extend(diff_json(v1[i], v2[i], p))
    else:
        if v1 != v2:
            diffs.append({"type": "MOD", "path": path, "from": v1, "to": v2})
    return diffs

# Example:
d1 = {"user": "Alice", "active": True}
d2 = {"user": "Alice", "active": False, "role": "admin"}
print(diff_json(d1, d2))`
  },

  'jwt-decoder': {
    title: 'Offline JWT Decoder & Claim Inspector',
    js: `// Standalone JWT Decoder with UTF-8 support (Zero external dependencies)
function decodeJWT(jwtString) {
  const parts = jwtString.trim().split('.');
  if (parts.length !== 3) throw new Error('Invalid JWT format (expected 3 parts)');

  const decodeB64Url = (str) => {
    let b64 = str.replace(/-/g, '+').replace(/_/g, '/');
    while (b64.length % 4) b64 += '=';
    const binary = atob(b64);
    const bytes = Uint8Array.from(binary, c => c.charCodeAt(0));
    return JSON.parse(new TextDecoder().decode(bytes));
  };

  const header = decodeB64Url(parts[0]);
  const payload = decodeB64Url(parts[1]);
  const isExpired = payload.exp ? (Date.now() >= payload.exp * 1000) : false;

  return { header, payload, isExpired, signature: parts[2] };
}

// Example:
// console.log(decodeJWT('eyJhbGciOi...'));`,
    py: `# Standalone Python JWT Payload Decoder (Without PyJWT dependency)
import base64, json, time

def decode_jwt(token: str) -> dict:
    parts = token.strip().split('.')
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")

    def b64url_decode(s: str) -> dict:
        s += '=' * (-len(s) % 4)
        data = base64.urlsafe_b64decode(s.encode('utf-8'))
        return json.loads(data.decode('utf-8'))

    header = b64url_decode(parts[0])
    payload = b64url_decode(parts[1])
    is_expired = (time.time() > payload.get('exp', float('inf'))) if 'exp' in payload else False

    return {"header": header, "payload": payload, "is_expired": is_expired}`
  },

  'sql-formatter': {
    title: 'SQL Query Prettifier Engine',
    js: `// Standalone SQL Formatter Regex Engine
function formatSQL(sql) {
  const keywords = [
    'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'JOIN', 'LEFT JOIN', 'RIGHT JOIN', 
    'INNER JOIN', 'OUTER JOIN', 'ON', 'GROUP BY', 'HAVING', 'ORDER BY', 'LIMIT', 
    'OFFSET', 'INSERT INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE FROM', 'UNION ALL', 'UNION'
  ];
  
  let formatted = sql.replace(/\\s+/g, ' ').trim();
  keywords.forEach(kw => {
    const re = new RegExp(\`\\\\b\${kw}\\\\b\`, 'gi');
    formatted = formatted.replace(re, \`\\n\${kw.toUpperCase()}\`);
  });
  
  return formatted.trim();
}`,
    py: `# Standalone Python SQL Formatter
# Requires: pip install sqlparse
import sqlparse

def prettify_sql(sql_query: str) -> str:
    return sqlparse.format(
        sql_query,
        reindent=True,
        keyword_case='upper',
        identifier_case='lower'
    )`
  },

  'regex-tester': {
    title: 'Regex Match & Explanation Engine',
    js: `// Standalone JS Regex Matcher with Group Extraction
function testRegex(pattern, flags, testString) {
  try {
    const re = new RegExp(pattern, flags);
    const matches = [...testString.matchAll(re)];
    return matches.map(m => ({
      match: m[0],
      index: m.index,
      groups: m.slice(1)
    }));
  } catch (err) {
    return { error: err.message };
  }
}`,
    py: `# Standalone Python Regex Matcher
import re

def test_pattern(pattern: str, test_string: str, flags: int = 0):
    matches = []
    for m in re.finditer(pattern, test_string, flags):
        matches.append({
            "match": m.group(0),
            "start": m.start(),
            "end": m.end(),
            "groups": m.groups()
        })
    return matches`
  },

  'curl-converter': {
    title: 'cURL Command to Code Converter',
    js: `// Standalone cURL to Fetch parser
function curlToFetch(curlCommand) {
  const urlMatch = curlCommand.match(/curl\\s+['"]?([^'\\s]+)['"]?/);
  const url = urlMatch ? urlMatch[1] : '';
  const methodMatch = curlCommand.match(/-X\\s+([A-Z]+)/i);
  const method = methodMatch ? methodMatch[1].toUpperCase() : 'GET';
  
  return \`fetch('\${url}', {\\n  method: '\${method}',\\n  headers: { 'Content-Type': 'application/json' }\\n}).then(res => res.json());\`;
}`,
    py: `# Standalone Python cURL to Requests
import re

def curl_to_requests(curl_cmd: str) -> str:
    url = re.search(r"curl\\s+['\"]?([^'\"\\s]+)", curl_cmd)
    target_url = url.group(1) if url else ""
    return f"import requests\\nresponse = requests.get('{target_url}')\\nprint(response.json())"`
  }
};

let currentModalToolId = 'json-diff';
let currentModalLang = 'js';

function ensureCodeExportModal() {
  let modal = document.getElementById('code-export-modal');
  if (modal) return modal;

  modal = document.createElement('div');
  modal.id = 'code-export-modal';
  modal.className = 'code-modal-overlay';
  modal.innerHTML = `
    <div class="code-modal-box">
      <div class="code-modal-header">
        <div class="code-modal-title-wrap">
          <span style="font-size: 18px;">💻</span>
          <span class="code-modal-title" id="code-modal-title">Standalone Transform Script</span>
          <span class="code-modal-badge">ZERO SERVER DEPS</span>
        </div>
        <button class="code-modal-close-btn" onclick="closeCodeModal()">✕</button>
      </div>

      <div class="code-lang-tabs">
        <button class="code-lang-btn active" id="tab-btn-js" onclick="switchCodeLang('js')">🟨 JavaScript / Node</button>
        <button class="code-lang-btn" id="tab-btn-py" onclick="switchCodeLang('py')">🐍 Python</button>
      </div>

      <div class="code-modal-body">
        <pre class="code-pre-box"><code id="code-modal-snippet"></code></pre>
      </div>

      <div class="code-modal-footer">
        <span class="code-modal-note">⚡ Run locally in your scripts, microservices, or CI/CD pipelines.</span>
        <div class="code-modal-actions">
          <button class="tbtn tbtn-primary" onclick="copyModalCode()">📋 Copy Code</button>
          <button class="tbtn tbtn-ghost" onclick="downloadModalCode()">💾 Download Script</button>
        </div>
      </div>
    </div>
  `;

  document.body.appendChild(modal);

  // Close on backdrop click or Escape key
  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeCodeModal();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeCodeModal();
  });

  return modal;
}

function openCodeExportModal(toolId) {
  const id = toolId || detectToolId();
  currentModalToolId = id;
  const modal = ensureCodeExportModal();
  
  const snippetData = TOOL_STANDALONE_SNIPPETS[id] || {
    title: 'Standalone Client Transform',
    js: '// JavaScript implementation snippet\\nconsole.log("Run directly in browser or Node.js");',
    py: '# Python implementation snippet\\nprint("Run directly with Python 3.9+")'
  };

  document.getElementById('code-modal-title').textContent = snippetData.title || 'Standalone Transform Script';
  switchCodeLang('js');
  modal.classList.add('open');
}

function closeCodeModal() {
  const modal = document.getElementById('code-export-modal');
  if (modal) modal.classList.remove('open');
}

function switchCodeLang(lang) {
  currentModalLang = lang;
  document.getElementById('tab-btn-js').classList.toggle('active', lang === 'js');
  document.getElementById('tab-btn-py').classList.toggle('active', lang === 'py');

  const snippetData = TOOL_STANDALONE_SNIPPETS[currentModalToolId] || {};
  const code = snippetData[lang] || `// No snippet available for ${lang}`;
  document.getElementById('code-modal-snippet').textContent = code;
}

function copyModalCode() {
  const snippetData = TOOL_STANDALONE_SNIPPETS[currentModalToolId] || {};
  const code = snippetData[currentModalLang] || '';
  navigator.clipboard.writeText(code).then(() => {
    showToast(`✅ Copied ${currentModalLang.toUpperCase()} standalone code!`);
  });
}

function downloadModalCode() {
  const snippetData = TOOL_STANDALONE_SNIPPETS[currentModalToolId] || {};
  const code = snippetData[currentModalLang] || '';
  const ext = currentModalLang === 'js' ? 'js' : 'py';
  const filename = `${currentModalToolId}-transform.${ext}`;

  const blob = new Blob([code], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast(`💾 Downloaded ${filename}`);
}

function detectToolId() {
  const path = window.location.pathname;
  const match = path.match(/([a-z0-9-]+)\.html$/i) || path.match(/\/([a-z0-9-]+)$/i);
  return match ? match[1] : 'json-diff';
}

// Auto-inject "💻 Get Code" button on tool headers if present
document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('.tool-header-bar');
  if (header && !header.querySelector('.tbtn-code-export')) {
    const btn = document.createElement('button');
    btn.className = 'tbtn-code-export';
    btn.innerHTML = '💻 Get Code / Script';
    btn.onclick = () => openCodeExportModal(detectToolId());
    header.appendChild(btn);
  }
});

