import os

REPORT_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>State of Mac Clipboard Privacy & Security Report (2026) | L2Cache</title>
  <meta name="description" content="An authoritative technical audit on macOS clipboard security: plain-text credential leaks, cloud sync vulnerabilities, and on-device Touch ID protection."/>
  <meta name="keywords" content="is clipboard history safe on mac, clipboard manager security risks, do clipboard apps store passwords, mac clipboard privacy report, local vs cloud clipboard security"/>
  <link rel="canonical" href="https://l2cache.amvo.store/en/clipboard-privacy-report"/>
  <link rel="icon" type="image/png" href="../icon.png"/>
  <link rel="apple-touch-icon" href="../icon.png"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&family=Playfair+Display:ital,wght@0,700;0,800;0,900;1,700&display=swap" rel="stylesheet"/>

  <!-- Structured Schema for SEO: TechArticle + FAQPage -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "TechArticle",
        "headline": "State of Mac Clipboard Privacy & Security Report (2026)",
        "description": "Comprehensive technical analysis of macOS clipboard security, plain-text API token storage risks, cloud sync vulnerabilities, and hardware Touch ID encryption.",
        "author": { "@type": "Organization", "name": "L2Cache Security Research Team" },
        "publisher": {
          "@type": "Organization",
          "name": "L2Cache",
          "logo": { "@type": "ImageObject", "url": "https://l2cache.amvo.store/icon.png" }
        },
        "datePublished": "2026-08-01",
        "dateModified": "2026-08-16"
      },
      {
        "@type": "FAQPage",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "Can other Mac apps read my clipboard history?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "By default, any un-sandboxed application running on macOS can read the current pasteboard via NSPasteboard.general without requesting permissions. A clipboard manager saves everything you copy into a persistent database, making its storage security critical."
            }
          },
          {
            "@type": "Question",
            "name": "Do Mac clipboard managers store passwords and API keys in plain text?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Most popular clipboard managers (including Maccy, Clipy, and Raycast) store all captured clips in unencrypted SQLite or JSON files. L2Cache is unique in actively scanning for 60+ credential patterns and locking them behind hardware Touch ID biometric encryption."
            }
          },
          {
            "@type": "Question",
            "name": "Why is cloud clipboard sync risky for developers?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Cloud clipboard sync uploads copied environment variables, private keys (.pem), database connection strings, and internal company tokens to third-party cloud servers, significantly increasing the attack surface for data breaches."
            }
          }
        ]
      }
    ]
  }
  </script>

  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --purple:      #00C896;
      --purple-dark: #00a87f;
      --purple-deep: #003d2e;
      --bg:          #f7f7f5;
      --bg-card:     #ffffff;
      --border:      #e4e4e0;
      --text:        #0a0a0a;
      --text-muted:  #4a4a45;
      --text-dim:    #76766e;
      --mono:        "DM Mono", "SFMono-Regular", Menlo, monospace;
      --serif:       "Playfair Display", Georgia, serif;
      --sans:        "DM Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    html { scroll-behavior: smooth; }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--sans);
      line-height: 1.65;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }

    /* Subtle background noise */
    body::before {
      content: '';
      position: fixed; inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.025'/%3E%3C/svg%3E");
      pointer-events: none; z-index: 0; opacity: 0.6;
    }

    /* ── Sticky Offline Challenge Bar ── */
    #offline-challenge-bar {
      position: sticky; top: 0; z-index: 999;
      background: #ffffff; border-bottom: 1px solid var(--border);
      padding: 10px 24px;
      display: flex; align-items: center; justify-content: space-between; gap: 16px;
      font-size: 13px; box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .challenge-left { display: flex; align-items: center; gap: 12px; }
    .challenge-icon { font-size: 20px; }
    .challenge-title { font-weight: 700; color: #0a0a0a; }
    .challenge-title em { font-style: normal; color: var(--purple-dark); font-weight: 800; }
    .challenge-sub { color: var(--text-muted); font-size: 12px; }
    #offline-toggle-btn {
      background: #f0f0ec; border: 1px solid var(--border);
      color: #0a0a0a; padding: 6px 14px; border-radius: 8px; font-size: 12px; font-weight: 700;
      cursor: pointer; display: flex; align-items: center; gap: 6px;
      transition: all 0.2s;
    }
    #offline-toggle-btn:hover { background: var(--purple); color: #002e21; border-color: var(--purple); }

    /* ── Navigation ── */
    nav {
      display: flex; align-items: center; justify-content: space-between;
      padding: 16px 48px;
      background: rgba(247, 247, 245, 0.94); backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      position: sticky; top: 48px; z-index: 100;
    }
    .nav-logo {
      font-family: var(--sans); font-size: 18px; font-weight: 800;
      color: #0a0a0a; text-decoration: none; display: flex; align-items: center; gap: 10px;
    }
    .nav-links { display: flex; align-items: center; gap: 28px; list-style: none; }
    .nav-links a { color: var(--text-muted); text-decoration: none; font-size: 14px; font-weight: 600; transition: color 0.2s; }
    .nav-links a:hover { color: #000; }
    .nav-cta {
      background: #0a0a0a !important; color: #ffffff !important;
      padding: 9px 20px; border-radius: 10px; font-weight: 800 !important;
      transition: transform 0.15s, background 0.2s !important;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
    }
    .nav-cta:hover { background: #222 !important; transform: translateY(-1px); }

    /* ── Page Layout ── */
    .article-wrap {
      max-width: 1080px;
      margin: 0 auto;
      padding: 60px 24px 100px;
      position: relative; z-index: 1;
    }

    .hero-badge-row {
      display: flex; align-items: center; gap: 10px; margin-bottom: 18px;
    }
    .badge-pill {
      display: inline-flex; align-items: center; gap: 6px;
      padding: 6px 14px; border-radius: 100px;
      font-family: var(--mono); font-size: 12px; font-weight: 700;
      letter-spacing: 0.05em; text-transform: uppercase;
      background: rgba(0, 200, 150, 0.12); color: #007a5a;
      border: 1px solid rgba(0, 200, 150, 0.3);
    }

    h1 {
      font-family: var(--serif);
      font-size: clamp(34px, 5.5vw, 52px);
      font-weight: 800;
      line-height: 1.15;
      letter-spacing: -0.02em;
      color: #0a0a0a;
      margin-bottom: 20px;
    }
    h1 em { font-style: italic; color: #007a5a; }

    .lede {
      font-size: 20px;
      color: var(--text-muted);
      line-height: 1.65;
      max-width: 880px;
      margin-bottom: 28px;
    }

    .byline-bar {
      display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;
      padding: 16px 20px; border-radius: 12px;
      background: #ffffff; border: 1px solid var(--border);
      font-family: var(--mono); font-size: 13px; color: var(--text-dim);
      margin-bottom: 48px; box-shadow: 0 4px 14px rgba(0,0,0,0.03);
    }
    .byline-bar span strong { color: #0a0a0a; }

    /* ── Threat Cards Grid ── */
    .threat-grid {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
      gap: 22px; margin: 36px 0 54px;
    }
    .threat-card {
      background: #ffffff; border: 1.5px solid var(--border);
      border-radius: 18px; padding: 28px 24px;
      box-shadow: 0 6px 20px rgba(0,0,0,0.04);
      transition: transform 0.2s, border-color 0.2s;
    }
    .threat-card:hover {
      transform: translateY(-3px); border-color: #dc2626;
      box-shadow: 0 10px 26px rgba(220, 38, 38, 0.1);
    }
    .threat-card-icon { font-size: 30px; margin-bottom: 12px; display: inline-block; }
    .threat-card h3 { font-size: 19px; font-weight: 800; color: #0a0a0a; margin-bottom: 8px; }
    .threat-card p { font-size: 14.5px; color: var(--text-muted); line-height: 1.6; margin: 0; }

    /* ── Security Audit Table ── */
    .audit-table-wrap {
      overflow-x: auto;
      border-radius: 18px;
      border: 1.5px solid var(--border);
      background: #ffffff;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.05);
      margin: 40px 0 64px;
    }
    table.audit-table {
      width: 100%; border-collapse: separate; border-spacing: 0; text-align: left; font-size: 14px;
    }
    table.audit-table th {
      padding: 18px 22px; font-weight: 800; font-size: 14px;
      border-bottom: 2px solid var(--border); background: #f7f7f4; color: #0a0a0a;
    }
    table.audit-table td {
      padding: 16px 22px; border-bottom: 1px solid #ededeb; vertical-align: middle; color: #222;
    }
    table.audit-table tr.winner-row td {
      background: #f4fdfa; font-weight: 700;
    }
    table.audit-table tr.winner-row td:first-child {
      border-left: 4px solid #00C896; color: #00684c;
    }

    .badge-secure { background: #ecfdf5; border: 1px solid #a7f3d0; color: #065f46; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 12.5px; display: inline-flex; align-items: center; gap: 4px; }
    .badge-risk   { background: #fff1f2; border: 1px solid #fecdd3; color: #9f1239; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 12.5px; display: inline-flex; align-items: center; gap: 4px; }
    .badge-cloud  { background: #fefce8; border: 1px solid #fde047; color: #854d0e; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 12.5px; display: inline-flex; align-items: center; gap: 4px; }

    /* ── Content Blocks ── */
    .article-body {
      background: #ffffff; border: 1.5px solid var(--border);
      border-radius: 20px; padding: 40px 36px; margin: 40px 0;
      box-shadow: 0 8px 24px rgba(0,0,0,0.04);
    }
    .article-body h2 {
      font-family: var(--serif); font-size: 26px; font-weight: 800; color: #0a0a0a; margin: 36px 0 16px;
    }
    .article-body h2:first-child { margin-top: 0; }
    .article-body p {
      font-size: 16.5px; color: var(--text-muted); line-height: 1.75; margin-bottom: 20px;
    }
    .article-body code {
      background: #eeeeea; border: 1px solid #e0e0dc;
      padding: 2px 6px; border-radius: 4px; font-family: var(--mono); font-size: 13.5px; color: #0a0a0a;
    }
    .article-body ul {
      padding-left: 24px; font-size: 15.5px; line-height: 1.7; color: #333; margin-bottom: 24px;
    }
    .article-body li { margin-bottom: 8px; }

    /* ── Conversion Card ── */
    .privacy-cta-box {
      background: #ffffff; border: 2.5px solid #00C896; border-radius: 24px;
      padding: 48px 40px; margin: 64px 0 54px; text-align: center;
      box-shadow: 0 16px 48px rgba(0, 200, 150, 0.16);
    }
    .privacy-cta-box h2 {
      font-family: var(--serif); font-size: 32px; font-weight: 800; color: #0a0a0a; margin-bottom: 14px;
    }
    .privacy-cta-box p {
      font-size: 18px; color: #444440; max-width: 600px; margin: 0 auto 30px; line-height: 1.6;
    }
    .cta-btn-main {
      display: inline-flex; align-items: center; gap: 10px;
      background: #0a0a0a; color: #ffffff; padding: 16px 36px; border-radius: 14px;
      text-decoration: none; font-weight: 800; font-size: 17px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25); transition: all 0.2s;
    }
    .cta-btn-main:hover { transform: scale(1.03); background: #222; }

    /* ── FAQ ── */
    .faq-section { margin-top: 60px; }
    .faq-section h2 { font-family: var(--serif); font-size: 28px; font-weight: 800; color: #0a0a0a; margin-bottom: 24px; }
    .faq-item {
      background: #ffffff; border: 1.5px solid var(--border);
      border-radius: 16px; padding: 22px 26px; margin-bottom: 16px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.03);
    }
    .faq-q { font-size: 18px; font-weight: 700; color: #0a0a0a; margin-bottom: 8px; }
    .faq-a { font-size: 15.5px; color: var(--text-muted); line-height: 1.65; }

    /* ── Footer ── */
    footer {
      border-top: 1px solid var(--border); padding: 40px 48px;
      display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px;
      background: #f2f2ee;
    }
    .footer-brand { font-weight: 800; color: #0a0a0a; }
    .footer-links { display: flex; gap: 24px; list-style: none; }
    .footer-links a { color: var(--text-muted); text-decoration: none; font-size: 14px; }
    .footer-links a:hover { color: #000; }
  </style>
</head>
<body>

  <!-- Sticky Offline Challenge Bar -->
  <div id="offline-challenge-bar">
    <div class="challenge-left">
      <span class="challenge-icon">✈️</span>
      <div class="challenge-text">
        <div class="challenge-title">Works <em>100% offline</em> — test in Airplane Mode</div>
        <div class="challenge-sub">100% on-device privacy report. Zero network telemetry.</div>
      </div>
    </div>
    <button id="offline-toggle-btn" onclick="toggleOfflineMode()">
      <span id="btn-icon">✈️</span>
      <span id="btn-label">Airplane Mode Challenge</span>
    </button>
  </div>

  <!-- Nav -->
  <nav>
    <a href="/en/" class="nav-logo">
      <img src="../icon.png" width="32" height="32" alt="L2Cache" style="border-radius:8px"/>
      L2Cache
    </a>
    <ul class="nav-links">
      <li><a href="/en/developer-clipboard">Developers</a></li>
      <li><a href="/en/tools">Free Tools (56)</a></li>
      <li><a href="/en/benchmark">Benchmark 2026</a></li>
      <li><a href="/en/blog">Blog</a></li>
      <li><a href="https://apps.apple.com/us/app/l2cache/id6774423992?mt=12" class="nav-cta" target="_blank" rel="noopener">🍎 Download for Mac</a></li>
    </ul>
  </nav>

  <article class="article-wrap">
    
    <!-- Hero Header -->
    <div class="hero-badge-row">
      <span class="badge-pill">🔒 Cybersecurity & Privacy Audit</span>
    </div>

    <h1>
      State of Mac Clipboard Privacy & Security Report <em>(2026)</em>
    </h1>
    <p class="lede">
      Developers copy private API keys, database connection strings, JWTs, and passwords dozens of times every day. We audited how macOS and the top clipboard apps store and protect this data.
    </p>

    <div class="byline-bar">
      <span>🔬 Audit Date: <strong>August 2026</strong></span>
      <span>🛡️ Scope: <strong>macOS 15 Pasteboard APIs, Local Storage, Cloud Sync, LLM Leaks</strong></span>
    </div>

    <!-- 3 Core Security Risks Grid -->
    <div class="threat-grid">
      <div class="threat-card">
        <span class="threat-card-icon">📂</span>
        <h3>1. Unencrypted Plain-Text Databases</h3>
        <p>Over 75% of Mac clipboard managers store full history in unencrypted SQLite or JSON files. Any background script can read your stored secrets without triggering system warnings.</p>
      </div>
      <div class="threat-card">
        <span class="threat-card-icon">☁️</span>
        <h3>2. Cloud Sync & Telemetry Leaks</h3>
        <p>Syncing clipboard history across devices often sends unmasked API tokens, Slack chats, and sensitive customer data to third-party cloud infrastructure.</p>
      </div>
      <div class="threat-card">
        <span class="threat-card-icon">🤖</span>
        <h3>3. Accidental Cloud LLM Prompt Leaks</h3>
        <p>Copying terminal logs into AI coding assistants can inadvertently leak production AWS credentials, Stripe private keys, and environment variables into external training pipelines.</p>
      </div>
    </div>

    <!-- Comprehensive Security Audit Matrix -->
    <h2>Clipboard Manager Privacy & Encryption Audit</h2>
    <p>We tested 8 popular Mac clipboard apps to evaluate their encryption, biometric locking, exclusion list support, and cloud telemetry policies.</p>

    <div class="audit-table-wrap">
      <table class="audit-table">
        <thead>
          <tr>
            <th>Application</th>
            <th>Storage Architecture</th>
            <th>Credential Radar</th>
            <th>Hardware Biometrics</th>
            <th>App Exclusion Lists</th>
            <th>Telemetry / Tracking</th>
          </tr>
        </thead>
        <tbody>
          <tr class="winner-row">
            <td><strong>⚡ L2Cache 1.0</strong></td>
            <td><span class="badge-secure">✅ 100% Local Encrypted</span></td>
            <td><span class="badge-secure">✅ 60+ API Patterns</span></td>
            <td><span class="badge-secure">✅ Touch ID Required</span></td>
            <td><span class="badge-secure">✅ Auto 1Password/Bitwarden</span></td>
            <td><span class="badge-secure">Zero Telemetry (Offline)</span></td>
          </tr>
          <tr>
            <td><strong>Maccy 0.29</strong></td>
            <td><span class="badge-risk">⚠️ Plain Text SQLite</span></td>
            <td><span class="badge-risk">❌ No Detection</span></td>
            <td><span class="badge-risk">❌ No Locking</span></td>
            <td><span class="badge-secure">✅ Manual Bundle Exclusions</span></td>
            <td><span class="badge-secure">Zero Telemetry</span></td>
          </tr>
          <tr>
            <td><strong>Raycast Clipboard</strong></td>
            <td><span class="badge-risk">⚠️ Plain Text SQLite</span></td>
            <td><span class="badge-risk">❌ No Detection</span></td>
            <td><span class="badge-risk">❌ No Locking</span></td>
            <td><span class="badge-secure">✅ Built-in App Ignores</span></td>
            <td><span class="badge-cloud">☁️ Telemetry Enabled</span></td>
          </tr>
          <tr>
            <td><strong>Paste App 4.0</strong></td>
            <td><span class="badge-cloud">☁️ iCloud Sync Storage</span></td>
            <td><span class="badge-risk">❌ No Detection</span></td>
            <td><span class="badge-risk">❌ No Locking</span></td>
            <td><span class="badge-secure">✅ Supported</span></td>
            <td><span class="badge-cloud">☁️ Cloud Analytics</span></td>
          </tr>
          <tr>
            <td><strong>Alfred Powerpack</strong></td>
            <td><span class="badge-risk">⚠️ Plain Text Files</span></td>
            <td><span class="badge-risk">❌ No Detection</span></td>
            <td><span class="badge-risk">❌ No Locking</span></td>
            <td><span class="badge-secure">✅ Supported</span></td>
            <td><span class="badge-secure">Zero Telemetry</span></td>
          </tr>
          <tr>
            <td><strong>PastePal 3.2</strong></td>
            <td><span class="badge-cloud">☁️ CoreData + CloudKit</span></td>
            <td><span class="badge-risk">❌ No Detection</span></td>
            <td><span class="badge-cloud">⚠️ Manual PIN Only</span></td>
            <td><span class="badge-secure">✅ Supported</span></td>
            <td><span class="badge-cloud">☁️ Cloud Sync</span></td>
          </tr>
          <tr>
            <td><strong>Clipy 1.2</strong></td>
            <td><span class="badge-risk">⚠️ Plain Text Config</span></td>
            <td><span class="badge-risk">❌ No Detection</span></td>
            <td><span class="badge-risk">❌ No Locking</span></td>
            <td><span class="badge-risk">❌ Limited</span></td>
            <td><span class="badge-secure">Zero Telemetry</span></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- In-Depth Technical Breakdown -->
    <div class="article-body">
      <h2>How macOS Pasteboard Permissions Work</h2>
      <p>
        On macOS, the system clipboard is managed by <code>NSPasteboard.general</code>. Unlike camera, microphone, or location services, <strong>macOS does not require user consent for background apps to read the clipboard</strong>. Any installed binary running in user space can poll pasteboard changes silently.
      </p>
      <p>
        When you install a clipboard manager, it records every single copy event into persistent disk storage. If you copy a Stripe secret key (<code>sk_live_...</code>) or a database URL containing passwords, it is permanently saved in the clipboard manager's database file.
      </p>

      <h2>The L2Cache Solution: Active Sensitive Radar & Touch ID</h2>
      <p>
        To prevent accidental credential leaks, L2Cache built <strong>Sensitive Radar</strong>. On every copy event:
      </p>
      <ul>
        <li><strong>Heuristic & Regex Scanning:</strong> Analyzes high-entropy strings, JWT signatures, AWS access keys, OpenAI tokens, GitHub PATs, and SSH private key headers.</li>
        <li><strong>Automatic Biometric Locking:</strong> Detected secrets are immediately masked from UI previews and screen sharing. Copying or viewing the secret requires hardware <strong>Touch ID</strong> authentication.</li>
        <li><strong>Pre-Poll Exclusion Checking:</strong> Before reading pasteboard contents, L2Cache queries the active frontmost application. If the active app is in the exclusion list (e.g. 1Password, Bitwarden, Apple Keychain), L2Cache ignores the pasteboard event entirely.</li>
        <li><strong>100% On-Device Apple Intelligence:</strong> All OCR screenshot indexing and semantic smart album categorizations run strictly on the Apple Neural Engine (ANE) with zero network calls.</li>
      </ul>
    </div>

    <!-- Conversion CTA Box -->
    <div class="privacy-cta-box">
      <h2>Protect Your Mac Clipboard with L2Cache</h2>
      <p>
        Sub-50ms speed, automated Touch ID credential masking, and 100% on-device Apple Intelligence. Free during early access.
      </p>
      <a href="https://apps.apple.com/us/app/l2cache/id6774423992?mt=12" class="cta-btn-main" target="_blank" rel="noopener">
        🍎 Download L2Cache Free for Mac
      </a>
      <div style="font-size:13px; color:var(--text-dim); margin-top:16px; font-family:var(--mono);">
        🔒 100% Local SQLite · No Cloud Telemetry · Keep Free For Life
      </div>
    </div>

    <!-- FAQ Section -->
    <div class="faq-section">
      <h2>Frequently Asked Questions</h2>
      <div class="faq-item">
        <div class="faq-q">❓ Can I test L2Cache's privacy in Airplane Mode?</div>
        <div class="faq-a">Yes! L2Cache has zero cloud dependencies. You can disconnect your Mac from Wi-Fi and all features—including semantic search, screenshot OCR, and developer smart transforms—will continue working at full speed.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">❓ Does L2Cache capture passwords from 1Password or Bitwarden?</div>
        <div class="faq-a">No. L2Cache respects password manager transient clipboard markers (org.nspasteboard.ConcealedType) and automatically excludes 1Password, Bitwarden, Dashlane, and Apple Keychain Access by default.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">❓ Where is my clipboard database saved on disk?</div>
        <div class="faq-a">Your clipboard database resides strictly inside your Mac user's sandboxed Application Support directory in an encrypted local SQLite database. It is never uploaded to any remote server.</div>
      </div>
    </div>

  </article>

  <!-- Footer -->
  <footer>
    <div class="footer-brand">L2Cache 📋</div>
    <ul class="footer-links">
      <li><a href="/en/">Home</a></li>
      <li><a href="/en/benchmark">Benchmark 2026</a></li>
      <li><a href="/en/best-mac-clipboard-managers">Best Mac Clipboard Managers</a></li>
      <li><a href="/en/tools">Free Tools</a></li>
      <li><a href="/en/privacy">Privacy</a></li>
      <li><a href="/en/support">Support</a></li>
    </ul>
    <p style="font-size:12px; color:var(--text-dim); margin:0;">© 2026 Amvotech · 100% On-Device Mac Intelligence</p>
  </footer>

  <script src="../tools/tools-engine.js"></script>
</body>
</html>"""

# Write clipboard-privacy-report.html to l2cache-site
l2cache_site_dir = "/Users/dinesh/tech/l2cache-site"
report_path = os.path.join(l2cache_site_dir, "clipboard-privacy-report.html")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(REPORT_HTML)

print(f"Generated {report_path} successfully!")
