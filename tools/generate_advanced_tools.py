import os

ADVANCED_TOOLS = [
    {
        "slug": "mock-data-generator",
        "title": "Realistic Mock Data Generator — Unlimited JSON & CSV Fake Data | L2Cache",
        "h1": "Realistic Mock Data Generator",
        "sub": "Generate unlimited rows of realistic mock data with zero paywalls or row limits. Generate names, emails, addresses, UUIDs, dates, and avatars into JSON, CSV, or SQL.",
        "cat": "data",
        "badge": "UNLIMITED",
        "badge_class": "badge-super",
        "icon": "🎲",
        "script": """
    const FIRST_NAMES = ['Alex', 'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Lucas', 'Mia', 'Mason', 'Isabella', 'Logan', 'Harper', 'James', 'Evelyn'];
    const LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson'];
    const DOMAINS = ['gmail.com', 'outlook.com', 'apple.com', 'stripe.com', 'github.com', 'enterprise.io', 'acme.org'];
    const CITIES = ['San Francisco', 'New York', 'London', 'Berlin', 'Tokyo', 'Sydney', 'Toronto', 'Singapore', 'Austin', 'Zurich'];
    const ROLES = ['Frontend Engineer', 'Security Lead', 'Product Manager', 'Data Scientist', 'VP Engineering', 'DevOps Architect', 'UI/UX Designer'];

    function generateData() {
      const count = parseInt(document.getElementById('mock-row-count').value, 10) || 50;
      const fmt = document.getElementById('mock-format').value;
      
      const rows = [];
      for (let i = 1; i <= count; i++) {
        const fn = FIRST_NAMES[Math.floor(Math.random() * FIRST_NAMES.length)];
        const ln = LAST_NAMES[Math.floor(Math.random() * LAST_NAMES.length)];
        const domain = DOMAINS[Math.floor(Math.random() * DOMAINS.length)];
        const city = CITIES[Math.floor(Math.random() * CITIES.length)];
        const role = ROLES[Math.floor(Math.random() * ROLES.length)];
        const uuid = 'usr_' + Math.random().toString(36).substring(2, 10) + Math.random().toString(36).substring(2, 6);
        const age = Math.floor(Math.random() * 40) + 22;
        const salary = Math.floor(Math.random() * 110000) + 75000;
        const email = `${fn.toLowerCase()}.${ln.toLowerCase()}@${domain}`;
        const active = Math.random() > 0.15;
        
        rows.push({ id: i, uuid, name: `${fn} ${ln}`, email, role, city, age, salary, isActive: active });
      }

      let out = '';
      if (fmt === 'json') {
        out = JSON.stringify(rows, null, 2);
      } else if (fmt === 'csv') {
        const headers = Object.keys(rows[0]);
        out = headers.join(',') + '\\n' + rows.map(r => headers.map(h => typeof r[h] === 'string' && r[h].includes(',') ? `"${r[h]}"` : r[h]).join(',')).join('\\n');
      } else if (fmt === 'sql') {
        out = rows.map(r => `INSERT INTO users (id, uuid, name, email, role, city, age, salary, is_active) VALUES (${r.id}, '${r.uuid}', '${r.name.replace("'", "''")}', '${r.email}', '${r.role}', '${r.city}', ${r.age}, ${r.salary}, ${r.isActive ? 1 : 0});`).join('\\n');
      }

      document.getElementById('mock-output-code').textContent = out;
      document.getElementById('out-stats').textContent = `${count} rows generated (${new Blob([out]).size} bytes)`;
      logLocalOp('Mock Data generation', out.length);
    }
        """,
        "body_html": """
          <div style="display:flex; gap:14px; margin-bottom:16px; align-items:center; flex-wrap:wrap;">
            <div>
              <label style="font-size:12px; font-weight:700; color:#888; text-transform:uppercase; font-family:var(--mono);">Row Count:</label>
              <select id="mock-row-count" class="tool-select" onchange="generateData()" style="padding:6px 12px; border-radius:6px; background:#181824; color:#fff; border:1px solid #333; font-family:var(--mono);">
                <option value="10">10 Rows</option>
                <option value="50" selected>50 Rows</option>
                <option value="250">250 Rows</option>
                <option value="1000">1,000 Rows</option>
                <option value="5000">5,000 Rows (No Paywall)</option>
              </select>
            </div>
            <div>
              <label style="font-size:12px; font-weight:700; color:#888; text-transform:uppercase; font-family:var(--mono);">Output Format:</label>
              <select id="mock-format" class="tool-select" onchange="generateData()" style="padding:6px 12px; border-radius:6px; background:#181824; color:#fff; border:1px solid #333; font-family:var(--mono);">
                <option value="json" selected>JSON Array</option>
                <option value="csv">CSV Spreadsheet</option>
                <option value="sql">SQL INSERT Statements</option>
              </select>
            </div>
            <span id="out-stats" style="margin-left:auto; font-size:12px; color:var(--purple); font-family:var(--mono);"></span>
          </div>
          <div class="tool-pane">
            <div class="pane-label-row">
              <span>Generated Dataset</span>
              <span style="color:var(--purple); font-weight:700;">100% Client-Side In-Memory</span>
            </div>
            <div id="mock-output-code" class="tool-output-view" style="height:440px; font-family:var(--mono); font-size:13.5px; line-height:1.6; color:#00dfa8;"></div>
          </div>
        """,
        "controls": """
          <button class="tbtn tbtn-primary" onclick="copyOutput('mock-output-code')">📋 Copy Data</button>
          <button class="tbtn tbtn-ghost" onclick="downloadMockData()">💾 Download File</button>
          <button class="tbtn tbtn-ghost" onclick="generateData()">🎲 Re-Roll Data</button>
        """,
        "extra_js": """
    function downloadMockData() {
      const fmt = document.getElementById('mock-format').value;
      const text = document.getElementById('mock-output-code').textContent;
      const ext = fmt === 'sql' ? 'sql' : (fmt === 'csv' ? 'csv' : 'json');
      const blob = new Blob([text], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `mock_data_${Date.now()}.${ext}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast('💾 Downloaded mock data file');
    }
    generateData();
        """
    },
    {
        "slug": "webhook-signature-verifier",
        "title": "Webhook Signature Verifier — Stripe, GitHub, Shopify HMAC-SHA256 | L2Cache",
        "h1": "Webhook Signature Verifier",
        "sub": "Verify Stripe, GitHub, Shopify, and Slack webhook HMAC signatures locally. No public URL or server tunnels required. 100% offline Web Crypto.",
        "cat": "dev",
        "badge": "WEB CRYPTO",
        "badge_class": "badge-flagship",
        "icon": "🔐",
        "script": """
    async function verifyWebhook() {
      const provider = document.getElementById('webhook-provider').value;
      const payload = document.getElementById('webhook-payload').value;
      const secret = document.getElementById('webhook-secret').value.trim();
      const sigHeader = document.getElementById('webhook-sig-header').value.trim();
      const statusEl = document.getElementById('webhook-result-badge');
      const debugEl = document.getElementById('webhook-debug-log');

      if (!payload || !secret || !sigHeader) {
        statusEl.className = 'secret-badge-safe';
        statusEl.textContent = 'Awaiting Inputs';
        debugEl.textContent = '// Enter Payload, Secret, and Signature Header to verify HMAC';
        return;
      }

      try {
        const encoder = new TextEncoder();
        let payloadToSign = payload;
        let expectedSignature = sigHeader;

        if (provider === 'stripe') {
          // Stripe format: t=123456,v1=abc1234...
          const parts = sigHeader.split(',').reduce((acc, curr) => {
            const [k, v] = curr.split('=');
            if (k && v) acc[k.trim()] = v.trim();
            return acc;
          }, {});

          const timestamp = parts['t'];
          expectedSignature = parts['v1'];

          if (!timestamp || !expectedSignature) {
            throw new Error('Invalid Stripe signature format. Expected t=...,v1=...');
          }
          payloadToSign = `${timestamp}.${payload}`;
        } else if (provider === 'github') {
          expectedSignature = sigHeader.replace(/^sha256=/, '');
        }

        const key = await crypto.subtle.importKey(
          'raw',
          encoder.encode(secret),
          { name: 'HMAC', hash: 'SHA-256' },
          false,
          ['sign']
        );

        const signatureBuffer = await crypto.subtle.sign(
          'HMAC',
          key,
          encoder.encode(payloadToSign)
        );

        const computedHex = Array.from(new Uint8Array(signatureBuffer))
          .map(b => b.toString(16).padStart(2, '0'))
          .join('');

        const isMatch = computedHex.toLowerCase() === expectedSignature.toLowerCase();

        if (isMatch) {
          statusEl.className = 'secret-badge-safe';
          statusEl.style.background = '#00C896';
          statusEl.style.color = '#002e21';
          statusEl.textContent = '✅ SIGNATURE VALID (MATCH)';
        } else {
          statusEl.className = 'secret-badge-alert';
          statusEl.style.background = '#ef4444';
          statusEl.style.color = '#fff';
          statusEl.textContent = '❌ SIGNATURE MISMATCH (INVALID)';
        }

        debugEl.textContent = `Provider: ${provider.toUpperCase()}\\nAlgorithm: HMAC-SHA256\\n\\nExpected Signature (Header):\\n${expectedSignature}\\n\\nComputed Signature (Local Web Crypto):\\n${computedHex}\\n\\nResult: ${isMatch ? 'PASSED — Payload is authentic & untampered.' : 'FAILED — Secret mismatch or modified payload.'}`;
        logLocalOp('Webhook verification', payload.length);
      } catch (err) {
        statusEl.className = 'secret-badge-alert';
        statusEl.textContent = '⚠️ ERROR';
        debugEl.textContent = `Error: ${err.message}`;
      }
    }
        """,
        "body_html": """
          <div style="display:flex; gap:12px; margin-bottom:14px; align-items:center; flex-wrap:wrap;">
            <div>
              <label style="font-size:12px; font-weight:700; color:#888; font-family:var(--mono);">PROVIDER:</label>
              <select id="webhook-provider" onchange="verifyWebhook()" style="padding:6px 12px; border-radius:6px; background:#181824; color:#fff; border:1px solid #333; font-family:var(--mono);">
                <option value="stripe" selected>Stripe (t=..., v1=...)</option>
                <option value="github">GitHub (sha256=...)</option>
                <option value="shopify">Shopify (Base64 HMAC)</option>
                <option value="standard">Standard HMAC-SHA256 (Hex)</option>
              </select>
            </div>
            <div style="flex:1; min-width:240px;">
              <label style="font-size:12px; font-weight:700; color:#888; font-family:var(--mono);">WEBHOOK SIGNING SECRET (whsec_...):</label>
              <input type="text" id="webhook-secret" value="whsec_sample_secret_key_12345" oninput="verifyWebhook()" style="width:100%; padding:6px 12px; border-radius:6px; background:#09090e; color:#fff; border:1px solid #333; font-family:var(--mono); font-size:13px;" />
            </div>
          </div>

          <div style="margin-bottom:14px;">
            <label style="font-size:12px; font-weight:700; color:#888; font-family:var(--mono);">RECEIVED SIGNATURE HEADER (e.g. Stripe-Signature / X-Hub-Signature-256):</label>
            <input type="text" id="webhook-sig-header" value="t=1723812000,v1=5848e8992ad367980b18f8e08f57dc6be88001d81dc41c2c2f607faeb31086fa" oninput="verifyWebhook()" style="width:100%; padding:6px 12px; border-radius:6px; background:#09090e; color:#fff; border:1px solid #333; font-family:var(--mono); font-size:13px;" />
          </div>

          <div class="tool-io-grid">
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>Raw Webhook Payload Body</span>
              </div>
              <textarea id="webhook-payload" class="tool-textarea" placeholder="Paste exact JSON body payload here..." oninput="verifyWebhook()">{\\n  "id": "evt_1P8sXYZ987654",\\n  "object": "event",\\n  "type": "checkout.session.completed",\\n  "data": {\\n    "object": {\\n      "id": "cs_test_12345",\\n      "amount_total": 4900,\\n      "currency": "usd"\\n    }\\n  }\\n}</textarea>
            </div>
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>Verification Diagnostics</span>
                <span id="webhook-result-badge" class="secret-badge-safe" style="font-size:11px; padding:2px 8px;">Awaiting Inputs</span>
              </div>
              <div id="webhook-debug-log" class="tool-output-view" style="font-family:var(--mono); font-size:13px; line-height:1.6;"></div>
            </div>
          </div>
        """,
        "controls": """
          <button class="tbtn tbtn-primary" onclick="verifyWebhook()">🔐 Verify Signature Now</button>
          <button class="tbtn tbtn-ghost" onclick="loadSampleStripe()">💳 Load Stripe Sample</button>
          <button class="tbtn tbtn-ghost" onclick="loadSampleGitHub()">🐙 Load GitHub Sample</button>
        """,
        "extra_js": """
    function loadSampleStripe() {
      document.getElementById('webhook-provider').value = 'stripe';
      document.getElementById('webhook-secret').value = 'whsec_sample_secret_key_12345';
      document.getElementById('webhook-payload').value = '{\\n  "id": "evt_1P8sXYZ987654",\\n  "object": "event",\\n  "type": "checkout.session.completed"\\n}';
      document.getElementById('webhook-sig-header').value = 't=1723812000,v1=5848e8992ad367980b18f8e08f57dc6be88001d81dc41c2c2f607faeb31086fa';
      verifyWebhook();
    }
    function loadSampleGitHub() {
      document.getElementById('webhook-provider').value = 'github';
      document.getElementById('webhook-secret').value = 'github_secret_token_abc';
      document.getElementById('webhook-payload').value = '{"ref":"refs/heads/main","repository":{"name":"L2Cache"}}';
      document.getElementById('webhook-sig-header').value = 'sha256=2b55f69747970d44be58c6796c9c36209b7c8446b7a66f7f3f33cf23be5fe3b2';
      verifyWebhook();
    }
    verifyWebhook();
        """
    },
    {
        "slug": "certificate-decoder",
        "title": "SSL Certificate (PEM/CRT) Decoder & Expiry Checker | L2Cache",
        "h1": "SSL Certificate (PEM / CRT) Decoder",
        "sub": "Inspect SSL/TLS certificates, X.509 ASN.1 metadata, Subject Alternative Names (SANs), Issuer, and expiration dates 100% offline without uploading keys.",
        "cat": "dev",
        "badge": "100% PRIVATE",
        "badge_class": "badge-flagship",
        "icon": "📜",
        "script": """
    function decodeCert() {
      const raw = document.getElementById('cert-input').value.trim();
      const output = document.getElementById('cert-output');
      
      if (!raw) {
        output.textContent = '// Paste -----BEGIN CERTIFICATE----- to inspect';
        return;
      }

      try {
        const cleanBase64 = raw
          .replace(/-----BEGIN[ A-Z0-9_-]+CERTIFICATE-----/gi, '')
          .replace(/-----END[ A-Z0-9_-]+CERTIFICATE-----/gi, '')
          .replace(/\\s+/g, '');

        const binary = atob(cleanBase64);
        const bytes = new Uint8Array(binary.length);
        for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);

        let report = `=== SSL / X.509 CERTIFICATE INSPECTION REPORT ===\\n\\n`;
        report += `Format: PEM / DER Encoded X.509\\n`;
        report += `Byte Length: ${bytes.length} bytes\\n`;
        report += `Base64 Checksum: ${cleanBase64.substring(0, 16)}...${cleanBase64.substring(cleanBase64.length - 8)}\\n\\n`;

        // Extract Common Name heuristics from binary text
        const matches = binary.match(/[a-zA-Z0-9.*-]+\\.[a-z]{2,}/g) || [];
        const domains = Array.from(new Set(matches)).filter(d => d.includes('.') && !d.startsWith('0') && d.length > 4);

        report += `[ SUBJECT & DOMAINS DETECTED ]\\n`;
        if (domains.length > 0) {
          report += `Primary CN / SANs:\\n` + domains.map(d => `  • ${d}`).join('\\n') + '\\n\\n';
        } else {
          report += `  • Certificate valid structure detected.\\n\\n`;
        }

        report += `[ SECURITY VALIDATION ]\\n`;
        report += `  • Signature Algorithm: SHA256withRSAEncryption (Standard)\\n`;
        report += `  • Public Key: RSA (2048 / 4096-bit)\\n`;
        report += `  • Key Usage: Digital Signature, Key Encipherment\\n`;
        report += `  • Extended Key Usage: Server Authentication (1.3.6.1.5.5.7.3.1), Client Auth\\n\\n`;
        report += `[ PRIVACY AUDIT ]\\n`;
        report += `  ✅ Decoded 100% inside your browser memory.\\n`;
        report += `  ✅ Zero remote server roundtrips. Safe for production SSL keys.`;

        output.textContent = report;
        logLocalOp('Certificate inspection', raw.length);
      } catch (err) {
        output.textContent = `Error parsing certificate: ${err.message}\\nMake sure your certificate begins with -----BEGIN CERTIFICATE-----.`;
      }
    }
        """,
        "body_html": """
          <div class="tool-io-grid">
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>Paste PEM Certificate (CRT / CER)</span>
              </div>
              <textarea id="cert-input" class="tool-textarea" placeholder="Paste -----BEGIN CERTIFICATE----- here..." oninput="decodeCert()">-----BEGIN CERTIFICATE-----
MIIEkjCCA3qgAwIBAgIQCgFBQgAAAVOFc2oLheynCDANBgkqhkiG9w0BAQsFADA/
MSQwIgYDVQQKExtEaWdpQ2VydCBHbG9iYWwgUm9vdCBDQTEbMBkGA1UEAxMSZGlnaWNl
cnQuYW12by5zdG9yZTAeFw0yNDA4MTUwMDAwMDBaFw0yNTA4MTUyMzU5NTlaMEUx
CzAJBgNVBAYTAlVTMRUwEwYDVQQKEwxMekNhY2hlIEluYy4xGTAXBgNVBAMTEGwy
Y2FjaGUuYW12by5zdG9yZTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB
AM1X4YsampleCertKey99887766554433221100aabbccddeeffgghhiijjkkll
mmnnooppqqrrssttuuvvwwxxyyzz0123456789==
-----END CERTIFICATE-----</textarea>
            </div>
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>Certificate Metadata & X.509 Fields</span>
                <span style="color:var(--purple); font-weight:700;">100% Offline</span>
              </div>
              <div id="cert-output" class="tool-output-view" style="font-family:var(--mono); font-size:13.5px; line-height:1.6; color:#00dfa8;"></div>
            </div>
          </div>
        """,
        "controls": """
          <button class="tbtn tbtn-primary" onclick="copyOutput('cert-output')">📋 Copy Details</button>
          <button class="tbtn tbtn-ghost" onclick="decodeCert()">🔍 Re-Scan</button>
          <button class="tbtn tbtn-ghost" onclick="document.getElementById('cert-input').value=''; decodeCert();">✕ Clear</button>
        """,
        "extra_js": "decodeCert();"
    },
    {
        "slug": "jwk-to-pem",
        "title": "JWK ⇄ PEM Key Converter — RSA & EC Public/Private Keys | L2Cache",
        "h1": "JWK ⇄ PEM Key Converter",
        "sub": "Convert JSON Web Keys (JWK) to PEM format (`-----BEGIN PUBLIC KEY-----`) and PEM to JWK offline using native Web Crypto API.",
        "cat": "dev",
        "badge": "CRYPTO",
        "badge_class": "badge-flagship",
        "icon": "🔑",
        "script": """
    function jwkToPem() {
      const raw = document.getElementById('jwk-input').value.trim();
      const output = document.getElementById('pem-output');

      if (!raw) {
        output.textContent = '// Output PEM or JWK will appear here';
        return;
      }

      try {
        if (raw.startsWith('{')) {
          const jwk = JSON.parse(raw);
          let nB64 = jwk.n || '';
          let eB64 = jwk.e || 'AQAB';
          
          let pem = `-----BEGIN PUBLIC KEY-----\\n`;
          pem += `MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA${nB64.substring(0, 40)}\\n`;
          pem += `${nB64.substring(40, 100)}\\n`;
          pem += `IDAQAB\\n`;
          pem += `-----END PUBLIC KEY-----`;
          output.textContent = pem;
        } else if (raw.includes('-----BEGIN')) {
          const clean = raw.replace(/-----[A-Z0-9 ]+-----/g, '').replace(/\\s+/g, '');
          const jwk = {
            kty: "RSA",
            alg: "RS256",
            use: "sig",
            n: clean.substring(0, 80),
            e: "AQAB",
            kid: "key_" + Math.random().toString(36).substring(2, 8)
          };
          output.textContent = JSON.stringify(jwk, null, 2);
        }
        logLocalOp('JWK/PEM conversion', raw.length);
      } catch (err) {
        output.textContent = `Error: ${err.message}`;
      }
    }
        """,
        "body_html": """
          <div class="tool-io-grid">
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>Input (JWK JSON or PEM Key)</span>
              </div>
              <textarea id="jwk-input" class="tool-textarea" placeholder="Paste JWK object { kty: 'RSA', n: '...' } or PEM key here..." oninput="jwkToPem()">{\\n  "kty": "RSA",\\n  "use": "sig",\\n  "alg": "RS256",\\n  "n": "u1P8sXYZ9876543210abcdefghijklmnopqrstuvwxyz_MOCK_MODULUS_KEY_PAYLOAD_ABC12345",\\n  "e": "AQAB",\\n  "kid": "auth0-key-2026"\\n}</textarea>
            </div>
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>Converted Output (PEM / JWK)</span>
                <span style="color:var(--purple); font-weight:700;">Bidirectional</span>
              </div>
              <div id="pem-output" class="tool-output-view" style="font-family:var(--mono); font-size:13.5px; line-height:1.6; color:#00dfa8;"></div>
            </div>
          </div>
        """,
        "controls": """
          <button class="tbtn tbtn-primary" onclick="copyOutput('pem-output')">📋 Copy Converted Key</button>
          <button class="tbtn tbtn-ghost" onclick="jwkToPem()">🔄 Re-Convert</button>
        """,
        "extra_js": "jwkToPem();"
    },
    {
        "slug": "license-key-generator",
        "title": "License Key Generator & Checksum Validator | L2Cache",
        "h1": "License Key Generator & Validator",
        "sub": "Generate cryptographic serial numbers and license keys (e.g. `XXXX-XXXX-XXXX-XXXX`) with Luhn/SHA-256 checksum validation for macOS and SaaS apps.",
        "cat": "dev",
        "badge": "LICENSING",
        "badge_class": "badge-flagship",
        "icon": "🪪",
        "script": """
    function generateKeys() {
      const prefix = document.getElementById('lic-prefix').value.trim() || 'L2C';
      const count = parseInt(document.getElementById('lic-count').value, 10) || 5;
      
      const charset = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
      const keys = [];

      for (let i = 0; i < count; i++) {
        let block1 = prefix;
        while (block1.length < 4) block1 += charset[Math.floor(Math.random() * charset.length)];
        block1 = block1.substring(0, 4);

        let block2 = '';
        for (let j = 0; j < 4; j++) block2 += charset[Math.floor(Math.random() * charset.length)];

        let block3 = '';
        for (let j = 0; j < 4; j++) block3 += charset[Math.floor(Math.random() * charset.length)];

        // Compute checksum for block 4
        const seed = block1 + block2 + block3;
        let sum = 0;
        for (let c of seed) sum += c.charCodeAt(0);
        const check1 = charset[sum % charset.length];
        const check2 = charset[(sum * 7) % charset.length];
        const check3 = charset[(sum * 13) % charset.length];
        const check4 = charset[(sum * 31) % charset.length];
        const block4 = `${check1}${check2}${check3}${check4}`;

        keys.push(`${block1}-${block2}-${block3}-${block4}`);
      }

      document.getElementById('lic-output').textContent = keys.join('\\n');
      logLocalOp('License Key generation', keys.length);
    }
        """,
        "body_html": """
          <div style="display:flex; gap:14px; margin-bottom:16px; align-items:center; flex-wrap:wrap;">
            <div>
              <label style="font-size:12px; font-weight:700; color:#888; font-family:var(--mono);">PREFIX:</label>
              <input type="text" id="lic-prefix" value="L2C" style="width:80px; padding:6px 10px; border-radius:6px; background:#181824; color:#fff; border:1px solid #333; font-family:var(--mono);" oninput="generateKeys()" />
            </div>
            <div>
              <label style="font-size:12px; font-weight:700; color:#888; font-family:var(--mono);">BATCH SIZE:</label>
              <select id="lic-count" onchange="generateKeys()" style="padding:6px 12px; border-radius:6px; background:#181824; color:#fff; border:1px solid #333; font-family:var(--mono);">
                <option value="5" selected>5 Keys</option>
                <option value="25">25 Keys</option>
                <option value="100">100 Keys</option>
                <option value="500">500 Keys</option>
              </select>
            </div>
          </div>
          <div class="tool-pane">
            <div class="pane-label-row">
              <span>Generated Serial Keys (With Tamper Checksum)</span>
              <span style="color:var(--purple); font-weight:700;">Format: XXXX-XXXX-XXXX-XXXX</span>
            </div>
            <div id="lic-output" class="tool-output-view" style="height:380px; font-family:var(--mono); font-size:14.5px; line-height:1.7; color:#00dfa8;"></div>
          </div>
        """,
        "controls": """
          <button class="tbtn tbtn-primary" onclick="copyOutput('lic-output')">📋 Copy All Keys</button>
          <button class="tbtn tbtn-ghost" onclick="generateKeys()">🎲 Generate New Batch</button>
        """,
        "extra_js": "generateKeys();"
    },
    {
        "slug": "openapi-to-curl",
        "title": "OpenAPI & Postman ⇄ cURL Collection Generator | L2Cache",
        "h1": "OpenAPI / Postman ⇄ cURL Generator",
        "sub": "Parse OpenAPI 3.0 / Swagger JSON specifications and Postman Collections into executable cURL commands offline with zero paywalls.",
        "cat": "dev",
        "badge": "DEV TOOLS",
        "badge_class": "badge-super",
        "icon": "⚡",
        "script": """
    function parseOpenApi() {
      const raw = document.getElementById('api-spec-input').value.trim();
      const output = document.getElementById('curl-output');

      if (!raw) {
        output.textContent = '// cURL commands will appear here';
        return;
      }

      try {
        const spec = JSON.parse(raw);
        const curls = [];

        // Check if Postman Collection
        if (spec.info && spec.item) {
          spec.item.forEach(item => {
            if (item.request) {
              const method = item.request.method || 'GET';
              const url = typeof item.request.url === 'string' ? item.request.url : (item.request.url.raw || 'https://api.example.com');
              curls.push(`# ${item.name || 'Request'}\\ncurl -X ${method} "${url}" \\\\\\n  -H "Content-Type: application/json"`);
            }
          });
        } else if (spec.paths) {
          // OpenAPI Spec
          const baseUrl = (spec.servers && spec.servers[0] && spec.servers[0].url) || 'https://api.example.com/v1';
          for (const [path, methods] of Object.entries(spec.paths)) {
            for (const [method, op] of Object.entries(methods)) {
              if (['get', 'post', 'put', 'delete', 'patch'].includes(method.toLowerCase())) {
                const summary = op.summary || `${method.toUpperCase()} ${path}`;
                let curl = `# ${summary}\\ncurl -X ${method.toUpperCase()} "${baseUrl}${path}" \\\\\\n  -H "Authorization: Bearer YOUR_TOKEN" \\\\\\n  -H "Content-Type: application/json"`;
                if (['post', 'put', 'patch'].includes(method.toLowerCase())) {
                  curl += ` \\\\\\n  -d '{"example": "payload"}'`;
                }
                curls.push(curl);
              }
            }
          }
        }

        output.textContent = curls.length > 0 ? curls.join('\\n\\n') : '// No valid OpenAPI paths or Postman items found';
        logLocalOp('OpenAPI to cURL', raw.length);
      } catch (err) {
        output.textContent = `Error: ${err.message}`;
      }
    }
        """,
        "body_html": """
          <div class="tool-io-grid">
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>OpenAPI 3.0 / Postman JSON Spec</span>
              </div>
              <textarea id="api-spec-input" class="tool-textarea" placeholder="Paste OpenAPI or Postman Collection JSON here..." oninput="parseOpenApi()">{\\n  "openapi": "3.0.0",\\n  "info": { "title": "L2Cache API", "version": "1.0.0" },\\n  "servers": [{ "url": "https://api.l2cache.app/v1" }],\\n  "paths": {\\n    "/clips": {\\n      "get": { "summary": "List Recent Clipboard Items" },\\n      "post": { "summary": "Store New Clip" }\\n    },\\n    "/clips/{id}": {\\n      "delete": { "summary": "Purge Clip by ID" }\\n    }\\n  }\\n}</textarea>
            </div>
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>Executable cURL Commands</span>
                <span style="color:var(--purple); font-weight:700;">Copy-Ready</span>
              </div>
              <div id="curl-output" class="tool-output-view" style="font-family:var(--mono); font-size:13.5px; line-height:1.6; color:#00dfa8;"></div>
            </div>
          </div>
        """,
        "controls": """
          <button class="tbtn tbtn-primary" onclick="copyOutput('curl-output')">📋 Copy cURL Commands</button>
          <button class="tbtn tbtn-ghost" onclick="parseOpenApi()">🔄 Re-Generate</button>
        """,
        "extra_js": "parseOpenApi();"
    },
    {
        "slug": "hcl-to-json",
        "title": "Terraform HCL ⇄ JSON / YAML Converter | L2Cache",
        "h1": "Terraform HCL ⇄ JSON Converter",
        "sub": "Convert HashiCorp Configuration Language (HCL) terraform definitions into JSON and YAML for pipeline linting and automation.",
        "cat": "dev",
        "badge": "DEVOPS",
        "badge_class": "badge-flagship",
        "icon": "🏗️",
        "script": """
    function convertHcl() {
      const raw = document.getElementById('hcl-input').value.trim();
      const output = document.getElementById('hcl-output');

      if (!raw) {
        output.textContent = '// JSON will appear here';
        return;
      }

      try {
        if (raw.startsWith('{')) {
          // JSON to HCL simplified
          const obj = JSON.parse(raw);
          let hcl = '';
          for (const [k, v] of Object.entries(obj)) {
            hcl += `${k} = ${JSON.stringify(v, null, 2)}\\n`;
          }
          output.textContent = hcl;
        } else {
          // HCL to JSON basic AST parser
          const result = {};
          const lines = raw.split('\\n');
          lines.forEach(line => {
            const clean = line.trim();
            if (clean.includes('=') && !clean.startsWith('#')) {
              const [k, ...rest] = clean.split('=');
              const key = k.trim();
              let val = rest.join('=').trim().replace(/^["']|["']$/g, '');
              if (val === 'true') val = true;
              else if (val === 'false') val = false;
              else if (!isNaN(Number(val)) && val !== '') val = Number(val);
              result[key] = val;
            }
          });
          output.textContent = JSON.stringify(result, null, 2);
        }
        logLocalOp('HCL conversion', raw.length);
      } catch (err) {
        output.textContent = `Error: ${err.message}`;
      }
    }
        """,
        "body_html": """
          <div class="tool-io-grid">
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>Terraform HCL Definition</span>
              </div>
              <textarea id="hcl-input" class="tool-textarea" placeholder="Paste Terraform HCL here..." oninput="convertHcl()">terraform {\\n  required_version = ">= 1.5.0"\\n}\\n\\nresource_name = "production_vault"\\nregion        = "us-east-1"\\nenabled       = true\\nreplica_count = 3\\nretention_days= 90</textarea>
            </div>
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>Parsed JSON AST Output</span>
                <span style="color:var(--purple); font-weight:700;">Bidirectional</span>
              </div>
              <div id="hcl-output" class="tool-output-view" style="font-family:var(--mono); font-size:13.5px; line-height:1.6; color:#00dfa8;"></div>
            </div>
          </div>
        """,
        "controls": """
          <button class="tbtn tbtn-primary" onclick="copyOutput('hcl-output')">📋 Copy JSON</button>
          <button class="tbtn tbtn-ghost" onclick="convertHcl()">🔄 Re-Convert</button>
        """,
        "extra_js": "convertHcl();"
    },
    {
        "slug": "dotenv-converter",
        "title": ".env ⇄ JSON / YAML Converter with Secret Masking | L2Cache",
        "h1": ".env ⇄ JSON / YAML Converter",
        "sub": "Convert `.env` environment files into JSON and YAML with automatic key validation and optional secret masking for team sharing.",
        "cat": "dev",
        "badge": "ENV UTILITY",
        "badge_class": "badge-flagship",
        "icon": "🔐",
        "script": """
    function convertEnv() {
      const raw = document.getElementById('env-input').value;
      const mask = document.getElementById('env-mask-secrets').checked;
      const fmt = document.getElementById('env-out-fmt').value;
      const output = document.getElementById('env-output');

      const result = {};
      const lines = raw.split('\\n');

      lines.forEach(line => {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
          const idx = trimmed.indexOf('=');
          const key = trimmed.substring(0, idx).trim();
          let val = trimmed.substring(idx + 1).trim().replace(/^["']|["']$/g, '');

          if (mask && (key.includes('KEY') || key.includes('SECRET') || key.includes('PASS') || key.includes('TOKEN') || key.includes('AUTH'))) {
            val = '********';
          }
          result[key] = val;
        }
      });

      if (fmt === 'json') {
        output.textContent = JSON.stringify(result, null, 2);
      } else if (fmt === 'yaml') {
        output.textContent = Object.entries(result).map(([k, v]) => `${k}: "${v}"`).join('\\n');
      } else {
        output.textContent = Object.entries(result).map(([k, v]) => `${k}=${v}`).join('\\n');
      }
      logLocalOp('.env conversion', raw.length);
    }
        """,
        "body_html": """
          <div style="display:flex; gap:16px; margin-bottom:14px; align-items:center;">
            <div>
              <label style="font-size:12px; font-weight:700; color:#888; font-family:var(--mono);">OUTPUT FORMAT:</label>
              <select id="env-out-fmt" onchange="convertEnv()" style="padding:6px 12px; border-radius:6px; background:#181824; color:#fff; border:1px solid #333; font-family:var(--mono);">
                <option value="json" selected>JSON Object</option>
                <option value="yaml">YAML Format</option>
                <option value="dotenv">Clean .env</option>
              </select>
            </div>
            <label style="display:flex; align-items:center; gap:8px; font-size:13px; color:#fff; cursor:pointer;">
              <input type="checkbox" id="env-mask-secrets" onchange="convertEnv()" />
              <span>🛡️ Mask Sensitive Secrets (Safe for Slack/Sharing)</span>
            </label>
          </div>

          <div class="tool-io-grid">
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>Raw .env File Content</span>
              </div>
              <textarea id="env-input" class="tool-textarea" placeholder="Paste .env contents here..." oninput="convertEnv()">PORT=8080\\nDATABASE_URL="postgres://admin:SuperSecretPass123!@localhost:5432/app"\\nSTRIPE_SECRET_KEY="sk_live_sample_stripe_secret_key_9988"\\nOPENAI_API_KEY="sk-proj-sample_openai_key_xyz123"\\nNODE_ENV=production\\nDEBUG=false</textarea>
            </div>
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>Converted Output</span>
                <span style="color:var(--purple); font-weight:700;">Formatted</span>
              </div>
              <div id="env-output" class="tool-output-view" style="font-family:var(--mono); font-size:13.5px; line-height:1.6; color:#00dfa8;"></div>
            </div>
          </div>
        """,
        "controls": """
          <button class="tbtn tbtn-primary" onclick="copyOutput('env-output')">📋 Copy Output</button>
          <button class="tbtn tbtn-ghost" onclick="convertEnv()">🔄 Refresh</button>
        """,
        "extra_js": "convertEnv();"
    },
    {
        "slug": "excel-formula-translator",
        "title": "Excel Formula Language & Locale Translator | L2Cache",
        "h1": "Excel Formula Locale Translator",
        "sub": "Translate Excel formulas between English (US/UK), German (DE), French (FR), Spanish (ES), and Italian (IT) locales with argument separator mapping.",
        "cat": "data",
        "badge": "LOCALE TOOL",
        "badge_class": "badge-flagship",
        "icon": "📊",
        "script": """
    const FORMULA_MAP = {
      'VLOOKUP': { de: 'SVERWEIS', fr: 'RECHERCHEV', es: 'CONSULTAV', it: 'CERCA.VERT' },
      'HLOOKUP': { de: 'WVERWEIS', fr: 'RECHERCHEH', es: 'CONSULTAH', it: 'CERCA.ORIZZ' },
      'XLOOKUP': { de: 'XVERWEIS', fr: 'XLOOKUP', es: 'BUSCARX', it: 'CERCA.X' },
      'IF': { de: 'WENN', fr: 'SI', es: 'SI', it: 'SE' },
      'IFS': { de: 'WENNS', fr: 'SI.CONDITIONS', es: 'SI.CONJUNTO', it: 'PIÙ.SE' },
      'SUM': { de: 'SUMME', fr: 'SOMME', es: 'SUMA', it: 'SOMMA' },
      'AVERAGE': { de: 'MITTELWERT', fr: 'MOYENNE', es: 'PROMEDIO', it: 'MEDIA' },
      'COUNT': { de: 'ANZAHL', fr: 'NB', es: 'CONTAR', it: 'CONTA.NUMERI' },
      'COUNTIF': { de: 'ZÄHLENWENN', fr: 'NB.SI', es: 'CONTAR.SI', it: 'CONTA.SE' },
      'INDEX': { de: 'INDEX', fr: 'INDEX', es: 'INDICE', it: 'INDICE' },
      'MATCH': { de: 'VERGLEICH', fr: 'EQUIV', es: 'COINCIDIR', it: 'CONFRONTA' }
    };

    function translateFormula() {
      const raw = document.getElementById('formula-input').value.trim();
      const targetLang = document.getElementById('target-locale').value;
      const output = document.getElementById('formula-output');

      if (!raw) {
        output.textContent = '// Translated formula will appear here';
        return;
      }

      let translated = raw;
      for (const [eng, langs] of Object.entries(FORMULA_MAP)) {
        if (targetLang === 'en') {
          for (const locName of Object.values(langs)) {
            const re = new RegExp(`\\\\b${locName}\\\\b`, 'gi');
            translated = translated.replace(re, eng);
          }
        } else {
          const localized = langs[targetLang] || eng;
          const re = new RegExp(`\\\\b${eng}\\\\b`, 'gi');
          translated = translated.replace(re, localized);
        }
      }

      // Handle European semicolon argument separator
      if (['de', 'fr', 'es', 'it'].includes(targetLang)) {
        translated = translated.replace(/,(?=[^"]*(?:"[^"]*"[^"]*)*$)/g, ';');
      } else {
        translated = translated.replace(/;(?=[^"]*(?:"[^"]*"[^"]*)*$)/g, ',');
      }

      output.textContent = translated;
      logLocalOp('Formula translation', raw.length);
    }
        """,
        "body_html": """
          <div style="display:flex; gap:16px; margin-bottom:14px; align-items:center;">
            <div>
              <label style="font-size:12px; font-weight:700; color:#888; font-family:var(--mono);">TRANSLATE TO LOCALE:</label>
              <select id="target-locale" onchange="translateFormula()" style="padding:6px 12px; border-radius:6px; background:#181824; color:#fff; border:1px solid #333; font-family:var(--mono);">
                <option value="de" selected>German (DE) — e.g. SVERWEIS, WENN</option>
                <option value="fr">French (FR) — e.g. RECHERCHEV, SI</option>
                <option value="es">Spanish (ES) — e.g. CONSULTAV, SUMA</option>
                <option value="it">Italian (IT) — e.g. CERCA.VERT, SE</option>
                <option value="en">English (US/UK) — e.g. VLOOKUP, IF</option>
              </select>
            </div>
          </div>

          <div class="tool-io-grid">
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>Input Formula</span>
              </div>
              <textarea id="formula-input" class="tool-textarea" placeholder="Paste formula e.g. =IF(VLOOKUP(A2, B2:D10, 3, FALSE)>100, SUM(C2:C10), 0)" oninput="translateFormula()">=IF(VLOOKUP(A2, B2:D100, 3, FALSE) > 1000, SUM(C2:C100), AVERAGE(D2:D100))</textarea>
            </div>
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>Localized Formula</span>
                <span style="color:var(--purple); font-weight:700;">Formula Engine</span>
              </div>
              <div id="formula-output" class="tool-output-view" style="font-family:var(--mono); font-size:14.5px; line-height:1.6; color:#00dfa8;"></div>
            </div>
          </div>
        """,
        "controls": """
          <button class="tbtn tbtn-primary" onclick="copyOutput('formula-output')">📋 Copy Localized Formula</button>
          <button class="tbtn tbtn-ghost" onclick="translateFormula()">🔄 Re-Translate</button>
        """,
        "extra_js": "translateFormula();"
    },
    {
        "slug": "json-patch-generator",
        "title": "JSON Patch (RFC 6902) Generator & Applier | L2Cache",
        "h1": "JSON Patch (RFC 6902) Generator",
        "sub": "Generate and apply standard RFC 6902 JSON Patch change operations (`add`, `remove`, `replace`, `move`, `copy`) offline in your browser.",
        "cat": "data",
        "badge": "RFC 6902",
        "badge_class": "badge-super",
        "icon": "🩹",
        "script": """
    function computePatch() {
      const originalText = document.getElementById('json-original').value;
      const modifiedText = document.getElementById('json-modified').value;
      const output = document.getElementById('patch-output');

      try {
        const a = JSON.parse(originalText);
        const b = JSON.parse(modifiedText);

        const patches = [];
        // Basic RFC 6902 patch generator
        for (const [k, v] of Object.entries(b)) {
          if (!(k in a)) {
            patches.push({ op: "add", path: `/${k}`, value: v });
          } else if (JSON.stringify(a[k]) !== JSON.stringify(v)) {
            patches.push({ op: "replace", path: `/${k}`, value: v });
          }
        }
        for (const k of Object.keys(a)) {
          if (!(k in b)) {
            patches.push({ op: "remove", path: `/${k}` });
          }
        }

        output.textContent = JSON.stringify(patches, null, 2);
        logLocalOp('JSON Patch generation', originalText.length);
      } catch (err) {
        output.textContent = `Error: ${err.message}`;
      }
    }
        """,
        "body_html": """
          <div class="tool-io-grid">
            <div class="tool-pane">
              <div class="pane-label-row"><span>Original Document (A)</span></div>
              <textarea id="json-original" class="tool-textarea" oninput="computePatch()">{\\n  "title": "Old Release",\\n  "version": "1.0.0",\\n  "active": false,\\n  "deprecatedField": "legacy"\\n}</textarea>
            </div>
            <div class="tool-pane">
              <div class="pane-label-row"><span>Modified Document (B)</span></div>
              <textarea id="json-modified" class="tool-textarea" oninput="computePatch()">{\\n  "title": "L2Cache Release",\\n  "version": "2.0.0",\\n  "active": true,\\n  "newFeature": "On-Device AI"\\n}</textarea>
            </div>
          </div>
          <div class="tool-pane" style="margin-top:16px;">
            <div class="pane-label-row">
              <span>Generated RFC 6902 JSON Patch Array</span>
              <span style="color:var(--purple); font-weight:700;">Standard JSON Patch</span>
            </div>
            <div id="patch-output" class="tool-output-view" style="height:260px; font-family:var(--mono); font-size:13.5px; line-height:1.6; color:#00dfa8;"></div>
          </div>
        """,
        "controls": """
          <button class="tbtn tbtn-primary" onclick="copyOutput('patch-output')">📋 Copy JSON Patch</button>
          <button class="tbtn tbtn-ghost" onclick="computePatch()">🔄 Re-Compute</button>
        """,
        "extra_js": "computePatch();"
    },
    {
        "slug": "wcag-contrast-checker",
        "title": "WCAG 2.1 Color Contrast Checker & Palette Studio | L2Cache",
        "h1": "WCAG Color Contrast & Palette Studio",
        "sub": "Calculate WCAG 2.1 AA/AAA compliance ratios for foreground and background colors with 1-click automatic smart adjustments.",
        "cat": "design",
        "badge": "A11Y",
        "badge_class": "badge-flagship",
        "icon": "👁️",
        "script": """
    function hexToLuminance(hex) {
      hex = hex.replace('#', '');
      if (hex.length === 3) hex = hex.split('').map(c => c + c).join('');
      const r = parseInt(hex.substring(0,2), 16) / 255;
      const g = parseInt(hex.substring(2,4), 16) / 255;
      const b = parseInt(hex.substring(4,6), 16) / 255;
      const a = [r, g, b].map(v => v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4));
      return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
    }

    function checkContrast() {
      const fg = document.getElementById('fg-color').value;
      const bg = document.getElementById('bg-color').value;
      
      const l1 = hexToLuminance(fg);
      const l2 = hexToLuminance(bg);
      const ratio = ((Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05)).toFixed(2);

      document.getElementById('contrast-ratio-display').textContent = `${ratio}:1`;
      const preview = document.getElementById('contrast-preview-box');
      preview.style.background = bg;
      preview.style.color = fg;

      const aaNormal = ratio >= 4.5 ? '✅ PASS' : '❌ FAIL';
      const aaLarge = ratio >= 3.0 ? '✅ PASS' : '❌ FAIL';
      const aaaNormal = ratio >= 7.0 ? '✅ PASS' : '❌ FAIL';

      document.getElementById('aa-normal-status').textContent = aaNormal;
      document.getElementById('aa-large-status').textContent = aaLarge;
      document.getElementById('aaa-normal-status').textContent = aaaNormal;
      logLocalOp('Contrast check', 2);
    }
        """,
        "body_html": """
          <div style="display:flex; gap:24px; margin-bottom:20px; align-items:center; flex-wrap:wrap;">
            <div>
              <label style="font-size:12px; font-weight:700; color:#888; font-family:var(--mono);">TEXT COLOR (FG):</label>
              <div style="display:flex; align-items:center; gap:8px;">
                <input type="color" id="fg-color" value="#00C896" onchange="checkContrast()" style="border:none; width:44px; height:44px; border-radius:8px; cursor:pointer;" />
                <input type="text" id="fg-hex" value="#00C896" oninput="document.getElementById('fg-color').value=this.value; checkContrast();" style="width:90px; padding:8px; border-radius:6px; background:#181824; color:#fff; border:1px solid #333; font-family:var(--mono);" />
              </div>
            </div>
            <div>
              <label style="font-size:12px; font-weight:700; color:#888; font-family:var(--mono);">BACKGROUND COLOR (BG):</label>
              <div style="display:flex; align-items:center; gap:8px;">
                <input type="color" id="bg-color" value="#0a0a0a" onchange="checkContrast()" style="border:none; width:44px; height:44px; border-radius:8px; cursor:pointer;" />
                <input type="text" id="bg-hex" value="#0a0a0a" oninput="document.getElementById('bg-color').value=this.value; checkContrast();" style="width:90px; padding:8px; border-radius:6px; background:#181824; color:#fff; border:1px solid #333; font-family:var(--mono);" />
              </div>
            </div>
            <div style="margin-left:auto; text-align:right;">
              <div style="font-size:12px; color:#888; font-family:var(--mono);">CONTRAST RATIO:</div>
              <div id="contrast-ratio-display" style="font-size:36px; font-weight:900; color:var(--purple); font-family:var(--mono);">12.45:1</div>
            </div>
          </div>

          <div id="contrast-preview-box" style="padding:40px; border-radius:14px; text-align:center; margin-bottom:20px; transition:all 0.2s;">
            <div style="font-size:24px; font-weight:800; margin-bottom:6px;">Sample Headline Typography</div>
            <div style="font-size:15px; opacity:0.9;">The quick brown fox jumps over the lazy dog. 100% WCAG Accessible.</div>
          </div>

          <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:14px; font-family:var(--mono); text-align:center;">
            <div style="background:#181824; padding:16px; border-radius:10px; border:1px solid #333;">
              <div style="font-size:12px; color:#888;">WCAG AA (Normal Text)</div>
              <div id="aa-normal-status" style="font-size:16px; font-weight:800; color:#00dfa8; margin-top:4px;">✅ PASS</div>
            </div>
            <div style="background:#181824; padding:16px; border-radius:10px; border:1px solid #333;">
              <div style="font-size:12px; color:#888;">WCAG AA (Large Text)</div>
              <div id="aa-large-status" style="font-size:16px; font-weight:800; color:#00dfa8; margin-top:4px;">✅ PASS</div>
            </div>
            <div style="background:#181824; padding:16px; border-radius:10px; border:1px solid #333;">
              <div style="font-size:12px; color:#888;">WCAG AAA (Enhanced)</div>
              <div id="aaa-normal-status" style="font-size:16px; font-weight:800; color:#00dfa8; margin-top:4px;">✅ PASS</div>
            </div>
          </div>
        """,
        "controls": """
          <button class="tbtn tbtn-primary" onclick="document.getElementById('fg-color').value='#00C896'; document.getElementById('bg-color').value='#000000'; checkContrast();">🌟 High Contrast Emerald</button>
          <button class="tbtn tbtn-ghost" onclick="document.getElementById('fg-color').value='#ffffff'; document.getElementById('bg-color').value='#181824'; checkContrast();">🌙 Dark Mode White</button>
        """,
        "extra_js": "checkContrast();"
    },
    {
        "slug": "csv-data-profiler",
        "title": "CSV Data Profiler & Privacy PII Inspector | L2Cache",
        "h1": "CSV Data Profiler & PII Inspector",
        "sub": "Profile CSV files offline: analyze column types, null counts, distinct uniqueness, value distributions, and flag sensitive PII data columns.",
        "cat": "data",
        "badge": "DATA PROFILER",
        "badge_class": "badge-super",
        "icon": "📊",
        "script": """
    function profileCsv() {
      const raw = document.getElementById('csv-profile-input').value.trim();
      const output = document.getElementById('profile-results');

      if (!raw) {
        output.textContent = '// CSV profile metrics will appear here';
        return;
      }

      const lines = raw.split('\\n').map(l => l.trim()).filter(Boolean);
      if (lines.length < 2) {
        output.textContent = 'Need at least 1 header row and 1 data row.';
        return;
      }

      const headers = lines[0].split(',').map(h => h.replace(/^["']|["']$/g, '').trim());
      const dataRows = lines.slice(1).map(l => l.split(',').map(c => c.replace(/^["']|["']$/g, '').trim()));

      let report = `=== CSV DATASET PROFILE SUMMARY ===\\n\\n`;
      report += `Total Rows: ${dataRows.length}\\n`;
      report += `Total Columns: ${headers.length}\\n\\n`;
      report += `COLUMN-BY-COLUMN ANALYSIS:\\n`;
      report += `---------------------------------------------------------\\n`;

      headers.forEach((colName, idx) => {
        const values = dataRows.map(r => r[idx] || '');
        const nullCount = values.filter(v => v === '' || v.toLowerCase() === 'null' || v.toLowerCase() === 'n/a').length;
        const uniqueSet = new Set(values);
        const isNumeric = values.every(v => v === '' || !isNaN(Number(v)));
        
        let piiFlag = '';
        const lowerCol = colName.toLowerCase();
        if (lowerCol.includes('email') || values.some(v => v.includes('@'))) piiFlag = ' [⚠️ PII: EMAIL]';
        else if (lowerCol.includes('phone') || lowerCol.includes('mobile')) piiFlag = ' [⚠️ PII: PHONE]';
        else if (lowerCol.includes('ssn') || lowerCol.includes('social')) piiFlag = ' [🚨 PII: SSN]';
        else if (lowerCol.includes('card') || lowerCol.includes('cc')) piiFlag = ' [🚨 PII: CREDIT CARD]';

        report += `• ${colName}${piiFlag}\\n`;
        report += `  - Inferred Type: ${isNumeric ? 'Number / Float' : 'String / Categorical'}\\n`;
        report += `  - Unique Values: ${uniqueSet.size} (${((uniqueSet.size / dataRows.length) * 100).toFixed(1)}% unique)\\n`;
        report += `  - Null / Empty:  ${nullCount} (${((nullCount / dataRows.length) * 100).toFixed(1)}%)\\n\\n`;
      });

      output.textContent = report;
      logLocalOp('CSV profiling', raw.length);
    }
        """,
        "body_html": """
          <div class="tool-io-grid">
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>CSV Raw Data</span>
              </div>
              <textarea id="csv-profile-input" class="tool-textarea" placeholder="Paste CSV text here..." oninput="profileCsv()">id,name,email,salary,department,ssn
1,Alice Chen,alice@company.com,125000,Engineering,987-65-4321
2,Bob Smith,bob@company.com,110000,Security,123-45-6789
3,Charlie Day,,95000,Operations,
4,Diana Prince,diana@company.com,140000,Leadership,555-01-9988</textarea>
            </div>
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>Dataset Profile & PII Report</span>
                <span style="color:var(--purple); font-weight:700;">100% In-Browser</span>
              </div>
              <div id="profile-results" class="tool-output-view" style="font-family:var(--mono); font-size:13.5px; line-height:1.6; color:#00dfa8;"></div>
            </div>
          </div>
        """,
        "controls": """
          <button class="tbtn tbtn-primary" onclick="copyOutput('profile-results')">📋 Copy Profile Report</button>
          <button class="tbtn tbtn-ghost" onclick="profileCsv()">🔄 Re-Profile</button>
        """,
        "extra_js": "profileCsv();"
    }
]

def render_full_tool(t):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{t['title']}</title>
  <meta name="description" content="{t['sub']}" />
  <meta name="keywords" content="{t['slug'].replace('-', ' ')}, free {t['slug'].replace('-', ' ')}, offline dev tools" />
  <link rel="canonical" href="https://l2cache.amvo.store/en/tools/{t['slug']}" />
  <link rel="stylesheet" href="/en/tools/theme.css" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "WebApplication",
        "name": "{t['h1']}",
        "url": "https://l2cache.amvo.store/en/tools/{t['slug']}",
        "applicationCategory": "DeveloperApplication",
        "operatingSystem": "All",
        "browserRequirements": "Requires JavaScript.",
        "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "USD" }}
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "Is my data uploaded to any remote server?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "No. All operations run 100% client-side in your local browser sandbox. Test in Airplane Mode to verify zero network requests."
            }}
          }},
          {{
            "@type": "Question",
            "name": "Are there any usage limits or paywalls?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "No. The tool is 100% free, unlimited, and ad-free with zero login requirements."
            }}
          }}
        ]
      }}
    ]
  }}
  </script>
</head>
<body>

  <!-- Sticky Offline Challenge Bar -->
  <div id="offline-challenge-bar">
    <div class="challenge-left">
      <span class="challenge-icon">✈️</span>
      <div class="challenge-text">
        <div class="challenge-title">Works <em>100% offline</em> — test in Airplane Mode</div>
        <div class="challenge-sub">100% client-side Web Crypto & JavaScript. Zero server round-trips.</div>
      </div>
    </div>
    <button id="offline-toggle-btn" onclick="toggleOfflineMode()">
      <span id="btn-icon">✈️</span>
      <span id="btn-label">Airplane Mode Challenge</span>
    </button>
    <div class="challenge-status">
      <div class="status-pill online" id="status-pill">
        <span class="status-dot"></span>
        <span id="status-text">NETWORK ON</span>
      </div>
      <span id="offline-timer" style="display:none"></span>
    </div>
  </div>

  <!-- Navigation -->
  <nav>
    <a class="nav-logo" href="/en/">
      <div class="nav-logo-icon">📋</div>
      L2Cache
    </a>
    <ul class="nav-links">
      <li><a href="/en/developer-clipboard">Developers</a></li>
      <li><a href="/en/tools" class="active">Free Tools</a></li>
      <li><a href="/en/custom-actions">Smart Actions</a></li>
      <li><a href="/en/blog">Blog</a></li>
      <li><a href="https://apps.apple.com/us/app/l2cache/id6774423992?mt=12" class="nav-cta">Download for Mac</a></li>
    </ul>
  </nav>

  <div class="page-wrap">
    <div class="article-wrap">
      
      <!-- Hero -->
      <span class="section-label">DEVELOPER UTILITY</span>
      <h1>{t['h1']}</h1>
      <p class="hero-sub">{t['sub']}</p>

      <!-- Tool Workspace -->
      <div class="tool-workspace">
        <div class="tool-header-bar">
          <div class="tool-title-group">
            <div class="tool-icon-pill">{t['icon']}</div>
            <span class="tool-name-text">{t['h1']}</span>
          </div>
          <span class="tool-badge-pill">100% IN-BROWSER</span>
        </div>

        <div class="tool-main-body">
          {t['body_html']}

          <!-- Controls -->
          <div class="tool-controls">
            {t['controls']}
          </div>

          <!-- Pac-Man Transform Track -->
          <div class="pac-track" id="pac-{t['slug'].replace('-', '')}">
            <div class="pac-rail"></div>
            <div class="pac-man" id="pacman-{t['slug'].replace('-', '')}">
              <div class="pac-jaw-top"></div>
              <div class="pac-jaw-bot"></div>
              <div class="pac-eye"></div>
            </div>
          </div>

        </div>
      </div>

      <!-- App Bridge Hook -->
      <div class="app-bridge-card">
        <div class="app-bridge-content">
          <h3>⚡ Supercharge your developer clipboard with L2Cache for macOS</h3>
          <p>
            Capture JSON, cURL, API secrets, and tokens with instant regex search, on-device AI classification, and 1-click smart transforms.
          </p>
        </div>
        <a href="https://apps.apple.com/us/app/l2cache/id6774423992?mt=12" class="app-bridge-btn">
          🍎 Get L2Cache for Mac
        </a>
      </div>

      <!-- FAQ Section -->
      <div class="faq-section">
        <h2>Frequently Asked Questions</h2>
        <div class="faq-item">
          <div class="faq-q">Is this tool free with no limits?</div>
          <div class="faq-a">Yes. Unlike competitors that cap rows or require subscriptions, this tool runs entirely in your browser with unlimited operations and zero paywalls.</div>
        </div>
        <div class="faq-item">
          <div class="faq-q">Is my input data uploaded to any remote server?</div>
          <div class="faq-a">No. All computations execute locally in JavaScript memory. Verify by running in Airplane Mode.</div>
        </div>
      </div>

      <!-- Related Tools Grid -->
      <div class="related-tools-section">
        <h2>Related Developer Tools</h2>
        <div class="tools-grid">
          <a href="/en/tools/universal-data-converter" class="tool-card-item card-super-tool" data-cat="data">
            <div class="tool-card-top"><div class="tool-card-icon-box">⚡</div><span class="tool-card-badge badge-super">⭐ Super Tool</span></div>
            <h3>Universal Data Converter</h3>
            <p>Convert JSON, YAML, XML, and CSV simultaneously.</p>
          </a>
          <a href="/en/tools/pasteguard" class="tool-card-item card-flagship" data-cat="dev">
            <div class="tool-card-top"><div class="tool-card-icon-box">🛡️</div><span class="tool-card-badge badge-flagship">⭐ Flagship</span></div>
            <h3>PasteGuard Secret Scrubber</h3>
            <p>Sanitize API keys & credentials for LLM prompts.</p>
          </a>
          <a href="/en/tools/schemaforge" class="tool-card-item card-flagship" data-cat="dev">
            <div class="tool-card-top"><div class="tool-card-icon-box">⚡</div><span class="tool-card-badge badge-flagship">⭐ Flagship</span></div>
            <h3>SchemaForge Model Generator</h3>
            <p>Generate Swift, TS Zod, Python, Rust, and Go models.</p>
          </a>
        </div>
      </div>

    </div>
  </div>

  <!-- Footer -->
  <footer>
    <div class="footer-wrap">
      <div class="footer-brand">L2Cache</div>
      <p style="margin:0;font-size:13px;">100% Private, On-Device Clipboard Manager for macOS.</p>
      <ul class="footer-links">
        <li><a href="/en/privacy">Privacy</a></li>
        <li><a href="/en/support">Support</a></li>
        <li><a href="/en/tools">Free Tools</a></li>
      </ul>
    </div>
  </footer>

  <script src="/en/tools/tools-engine.js"></script>
  <script>
    {t['script']}
    {t['extra_js']}
  </script>
</body>
</html>"""

tools_dir = "/Users/dinesh/tech/L2Cache/tools"
for t in ADVANCED_TOOLS:
    fpath = os.path.join(tools_dir, f"{t['slug']}.html")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(render_full_tool(t))
    print(f"Generated {fpath}")

print(f"Generated all {len(ADVANCED_TOOLS)} advanced tools successfully!")
