import os
import json

# Upgraded Comparison Template with Rich Interactive Table, High-Contrast Fonts & Badges
UPGRADED_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{{seo_title}} | L2Cache</title>
  <meta name="description" content="{{seo_description}}"/>
  <link rel="canonical" href="{{canonical_url}}"/>
  <link rel="icon" type="image/png" href="../icon.png"/>
  <link rel="apple-touch-icon" href="../icon.png"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet"/>

  <!-- Structured Schema for SEO -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "{{seo_title}}",
    "description": "{{seo_description}}",
    "author": { "@type": "Organization", "name": "L2Cache Labs" },
    "publisher": {
      "@type": "Organization",
      "name": "L2Cache",
      "logo": { "@type": "ImageObject", "url": "https://l2cache.amvo.store/icon.png" }
    },
    "image": "https://l2cache.amvo.store/icon.png",
    "mainEntityOfPage": "{{canonical_url}}",
    "datePublished": "2026-08-01",
    "dateModified": "2026-08-16"
  }
  </script>

  {{faq_schema_json}}

  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --brand:       #00C896;
      --brand-glow:  rgba(0, 200, 150, 0.22);
      --brand-bg:    rgba(0, 200, 150, 0.08);
      --brand-border:rgba(0, 200, 150, 0.35);
      --bg:          #08090d;
      --bg-card:     #111218;
      --bg-card-alt: #161822;
      --border:      rgba(255, 255, 255, 0.12);
      --text:        #f8fafc;
      --text-sub:    #94a3b8;
      --text-dim:    #64748b;
      --loss-bg:     rgba(244, 63, 94, 0.08);
      --loss-border: rgba(244, 63, 94, 0.25);
      --loss-text:   #fb7185;
      --font-sans:   'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-mono:   'JetBrains Mono', monospace;
    }

    html { scroll-behavior: smooth; }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      line-height: 1.65;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }

    /* Ambient Background Glow */
    .ambient-glow {
      position: fixed; top: 0; left: 50%; transform: translateX(-50%);
      width: 1000px; height: 450px;
      background: radial-gradient(50% 50% at 50% 0%, rgba(0, 200, 150, 0.14) 0%, rgba(8, 9, 13, 0) 100%);
      pointer-events: none; z-index: 0;
    }

    /* ── Sticky Offline Challenge Bar ── */
    #offline-challenge-bar {
      position: sticky; top: 0; z-index: 999;
      background: #0d1117; border-bottom: 1px solid var(--border);
      padding: 10px 24px;
      display: flex; align-items: center; justify-content: space-between; gap: 16px;
      font-size: 13px;
    }
    .challenge-left { display: flex; align-items: center; gap: 12px; }
    .challenge-icon { font-size: 20px; }
    .challenge-title { font-weight: 700; color: #fff; }
    .challenge-title em { font-style: normal; color: var(--brand); }
    .challenge-sub { color: var(--text-sub); font-size: 12px; }
    #offline-toggle-btn {
      background: rgba(255,255,255,0.08); border: 1px solid var(--border);
      color: #fff; padding: 6px 14px; border-radius: 8px; font-size: 12px; font-weight: 700;
      cursor: pointer; display: flex; align-items: center; gap: 6px;
      transition: all 0.2s;
    }
    #offline-toggle-btn:hover { background: var(--brand); color: #002e21; }

    /* ── Navigation ── */
    nav {
      display: flex; align-items: center; justify-content: space-between;
      padding: 18px 48px;
      background: rgba(8, 9, 13, 0.75); backdrop-filter: blur(24px);
      border-bottom: 1px solid var(--border);
      position: sticky; top: 48px; z-index: 100;
    }
    .nav-logo {
      font-family: var(--font-sans); font-size: 18px; font-weight: 800;
      color: #ffffff; text-decoration: none; display: flex; align-items: center; gap: 10px;
    }
    .nav-links { display: flex; align-items: center; gap: 28px; list-style: none; }
    .nav-links a { color: var(--text-sub); text-decoration: none; font-size: 14px; font-weight: 600; transition: color 0.2s; }
    .nav-links a:hover { color: #fff; }
    .nav-cta {
      background: var(--brand) !important; color: #002e21 !important;
      padding: 9px 20px; border-radius: 10px; font-weight: 800 !important;
      transition: transform 0.15s, box-shadow 0.2s !important;
      box-shadow: 0 4px 18px rgba(0, 200, 150, 0.3);
    }
    .nav-cta:hover { transform: translateY(-1px); box-shadow: 0 6px 24px rgba(0, 200, 150, 0.45); }

    /* ── Page Layout ── */
    .article-wrap {
      max-width: 1080px;
      margin: 0 auto;
      padding: 60px 24px 100px;
      position: relative; z-index: 1;
    }

    .hero-badge-row {
      display: flex; align-items: center; gap: 10px; margin-bottom: 20px;
    }
    .badge-pill {
      display: inline-flex; align-items: center; gap: 6px;
      padding: 6px 14px; border-radius: 100px;
      font-family: var(--font-mono); font-size: 12px; font-weight: 700;
      letter-spacing: 0.05em; text-transform: uppercase;
      background: rgba(0, 200, 150, 0.12); color: var(--brand);
      border: 1px solid var(--brand-border);
    }
    .badge-versus {
      font-family: var(--font-mono); font-size: 12px; font-weight: 700;
      color: var(--text-dim); text-transform: uppercase;
    }

    h1 {
      font-size: clamp(34px, 5.5vw, 54px);
      font-weight: 800;
      line-height: 1.15;
      letter-spacing: -0.025em;
      color: #ffffff;
      margin-bottom: 20px;
    }
    h1 span.hl {
      background: linear-gradient(135deg, #ffffff 30%, var(--brand) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    h1 em.comp-hl {
      font-style: normal;
      color: #fca5a5;
    }

    .lede {
      font-size: 20px;
      color: var(--text-sub);
      line-height: 1.6;
      max-width: 860px;
      margin-bottom: 28px;
    }

    .byline-bar {
      display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;
      padding: 16px 20px; border-radius: 12px;
      background: rgba(255,255,255,0.03); border: 1px solid var(--border);
      font-family: var(--font-mono); font-size: 13px; color: var(--text-dim);
      margin-bottom: 48px;
    }
    .byline-bar span strong { color: var(--text); }

    /* ── SHIFT BANNER: 3 Reasons to Switch ── */
    .switch-cards-grid {
      display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 20px; margin: 36px 0 54px;
    }
    .switch-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 26px 24px;
      position: relative; overflow: hidden;
      transition: transform 0.2s, border-color 0.2s;
    }
    .switch-card:hover {
      transform: translateY(-3px);
      border-color: var(--brand-border);
    }
    .switch-card-icon {
      font-size: 28px; margin-bottom: 14px; display: inline-block;
    }
    .switch-card h3 {
      font-size: 18px; font-weight: 800; color: #ffffff; margin-bottom: 8px;
    }
    .switch-card p {
      font-size: 14px; color: var(--text-sub); line-height: 1.6; margin: 0;
    }

    /* ── RICH COMPARISON TABLE ── */
    .table-header-ctrls {
      display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;
      margin-bottom: 18px;
    }
    .table-title-area h2 {
      font-size: 26px; font-weight: 800; color: #ffffff; letter-spacing: -0.01em;
    }
    .table-filter-pills {
      display: flex; gap: 8px; flex-wrap: wrap;
    }
    .tfilter-btn {
      background: var(--bg-card); border: 1px solid var(--border);
      color: var(--text-sub); padding: 8px 16px; border-radius: 100px;
      font-size: 13px; font-weight: 700; cursor: pointer;
      transition: all 0.18s;
    }
    .tfilter-btn:hover { border-color: var(--brand); color: #fff; }
    .tfilter-btn.active {
      background: var(--brand); color: #002e21; border-color: var(--brand); font-weight: 800;
      box-shadow: 0 4px 14px rgba(0, 200, 150, 0.35);
    }

    .matrix-table-wrap {
      overflow-x: auto;
      border-radius: 20px;
      border: 1px solid var(--border);
      background: var(--bg-card);
      box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);
      margin-bottom: 60px;
    }

    table.matrix-table {
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      text-align: left;
      font-size: 14.5px;
    }

    table.matrix-table th {
      padding: 20px 24px;
      font-weight: 800;
      font-size: 15px;
      letter-spacing: -0.01em;
      border-bottom: 2px solid var(--border);
      background: #151720;
    }
    table.matrix-table th.col-feature { width: 34%; color: #94a3b8; }
    table.matrix-table th.col-l2cache {
      width: 33%;
      background: rgba(0, 200, 150, 0.12);
      border-left: 2px solid var(--brand);
      border-right: 2px solid var(--brand-border);
      color: #00dfa8;
      font-size: 16px;
    }
    table.matrix-table th.col-comp {
      width: 33%;
      color: #cbd5e1;
    }

    table.matrix-table td {
      padding: 18px 24px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.07);
      vertical-align: middle;
      line-height: 1.55;
    }
    table.matrix-table tr:hover td {
      background: rgba(255, 255, 255, 0.02);
    }

    /* Winner L2Cache Column Highlight */
    table.matrix-table td.col-l2-win {
      background: rgba(0, 200, 150, 0.05);
      border-left: 2px solid var(--brand-border);
      border-right: 2px solid var(--brand-border);
      font-weight: 700;
      color: #ffffff;
    }
    table.matrix-table tr:hover td.col-l2-win {
      background: rgba(0, 200, 150, 0.09);
    }
    table.matrix-table tr:last-child td { border-bottom: none; }

    /* Badge & Smiley Styles */
    .rich-badge {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 6px 13px;
      border-radius: 8px;
      font-size: 13.5px;
      font-weight: 700;
      line-height: 1.35;
    }
    .badge-win-emerald {
      background: rgba(0, 200, 150, 0.14);
      border: 1px solid rgba(0, 200, 150, 0.4);
      color: #34d399;
    }
    .badge-win-gold {
      background: rgba(234, 179, 8, 0.14);
      border: 1px solid rgba(234, 179, 8, 0.35);
      color: #facc15;
    }
    .badge-loss-red {
      background: rgba(244, 63, 94, 0.1);
      border: 1px solid rgba(244, 63, 94, 0.25);
      color: #fda4af;
    }
    .badge-neutral {
      background: rgba(148, 163, 184, 0.1);
      border: 1px solid rgba(148, 163, 184, 0.2);
      color: #cbd5e1;
    }

    /* ── ADVANTAGES SECTION ── */
    .advantage-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 32px 30px;
      margin-bottom: 24px;
      transition: all 0.2s;
    }
    .advantage-card:hover {
      border-color: rgba(0, 200, 150, 0.4);
      box-shadow: 0 8px 30px rgba(0, 200, 150, 0.1);
    }
    .advantage-header {
      display: flex; align-items: center; gap: 14px; margin-bottom: 14px;
    }
    .advantage-icon-box {
      width: 44px; height: 44px; border-radius: 12px;
      background: rgba(0, 200, 150, 0.12); border: 1px solid var(--brand-border);
      display: flex; align-items: center; justify-content: center;
      font-size: 22px; flex-shrink: 0;
    }
    .advantage-header h3 {
      font-size: 21px; font-weight: 800; color: #ffffff;
    }
    .advantage-card p {
      font-size: 16px; color: var(--text-sub); line-height: 1.7; margin: 0;
    }

    /* ── CONVERSION CTA BOX ── */
    .shift-cta-box {
      background: linear-gradient(135deg, #111a1d 0%, #0d1e1c 50%, #0a2520 100%);
      border: 2px solid var(--brand);
      border-radius: 24px;
      padding: 48px 40px;
      margin: 64px 0 54px;
      text-align: center;
      box-shadow: 0 20px 60px rgba(0, 200, 150, 0.2);
      position: relative; overflow: hidden;
    }
    .shift-cta-box h2 {
      font-size: 32px; font-weight: 900; color: #ffffff; margin-bottom: 14px;
    }
    .shift-cta-box p {
      font-size: 18px; color: #cbd5e1; max-width: 580px; margin: 0 auto 30px;
    }
    .cta-download-btn {
      display: inline-flex; align-items: center; gap: 10px;
      background: var(--brand); color: #002e21;
      padding: 16px 36px; border-radius: 14px;
      text-decoration: none; font-weight: 900; font-size: 17px;
      box-shadow: 0 8px 30px rgba(0, 200, 150, 0.4);
      transition: all 0.2s;
    }
    .cta-download-btn:hover {
      transform: scale(1.03);
      box-shadow: 0 12px 36px rgba(0, 200, 150, 0.6);
      background: #00dfa8;
    }
    .cta-guarantee-note {
      font-size: 13px; color: var(--text-dim); margin-top: 18px; font-family: var(--font-mono);
    }

    /* ── FAQ SECTION ── */
    .faq-section { margin-top: 60px; }
    .faq-section h2 { font-size: 28px; font-weight: 800; color: #fff; margin-bottom: 24px; }
    .faq-item {
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 16px; padding: 22px 26px; margin-bottom: 16px;
    }
    .faq-q { font-size: 18px; font-weight: 700; color: #ffffff; margin-bottom: 8px; }
    .faq-a { font-size: 15px; color: var(--text-sub); line-height: 1.65; }

    /* ── Footer ── */
    footer {
      border-top: 1px solid var(--border);
      padding: 40px 48px;
      display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px;
      background: #050608;
    }
    .footer-brand { font-weight: 800; color: #fff; }
    .footer-links { display: flex; gap: 24px; list-style: none; }
    .footer-links a { color: var(--text-sub); text-decoration: none; font-size: 14px; transition: color 0.2s; }
    .footer-links a:hover { color: #fff; }

    @media (max-width: 768px) {
      nav { padding: 14px 20px; }
      .nav-links { display: none; }
      .article-wrap { padding: 40px 16px 80px; }
      table.matrix-table { font-size: 13px; }
      table.matrix-table th, table.matrix-table td { padding: 14px 16px; }
      .shift-cta-box { padding: 32px 20px; }
    }
  </style>
</head>
<body>

  <div class="ambient-glow"></div>

  <!-- Sticky Offline Challenge Bar -->
  <div id="offline-challenge-bar">
    <div class="challenge-left">
      <span class="challenge-icon">✈️</span>
      <div class="challenge-text">
        <div class="challenge-title">Works <em>100% offline</em> — test in Airplane Mode</div>
        <div class="challenge-sub">100% on-device privacy guarantee. No cloud telemetry.</div>
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
      <span class="badge-pill">⚡ Side-by-Side Comparison</span>
      <span class="badge-versus">L2Cache vs. {{competitor_name}}</span>
    </div>

    <h1>
      <span class="hl">L2Cache</span> vs. <em class="comp-hl">{{competitor_name}}</em>
    </h1>
    <p class="lede">{{intro_paragraph}}</p>

    <div class="byline-bar">
      <span>🔬 Tested & Published: <strong>August 2026 (macOS 15 Sequoia / Sonoma)</strong></span>
      <span>⚡ Performance: <strong>Apple Silicon Native (M-Series)</strong></span>
    </div>

    <!-- Shift Highlights: 3 Reasons to Switch -->
    <div class="switch-cards-grid">
      <div class="switch-card">
        <span class="switch-card-icon">🧠</span>
        <h3>On-Device Apple Intelligence</h3>
        <p>Search semantic concepts ('that docker error') and extract text from screenshot images via native OCR without cloud round-trips.</p>
      </div>
      <div class="switch-card">
        <span class="switch-card-icon">🛡️</span>
        <h3>Touch ID Credential Radar</h3>
        <p>Automatically scans and masks API keys (OpenAI, AWS, Stripe) and passwords behind hardware Touch ID biometric authentication.</p>
      </div>
      <div class="switch-card">
        <span class="switch-card-icon">🎁</span>
        <h3>Zero Subscription Fees</h3>
        <p>100% free during early access. Everyone who installs today keeps all features, OCR, and AI updates permanently free for life.</p>
      </div>
    </div>

    <!-- Comparison Table Header & Filter Tabs -->
    <div class="table-header-ctrls">
      <div class="table-title-area">
        <h2>⚔️ Comprehensive Feature Matrix</h2>
      </div>
      <div class="table-filter-pills">
        <button class="tfilter-btn active" onclick="filterMatrix('all', this)">🌟 All Features</button>
        <button class="tfilter-btn" onclick="filterMatrix('ai', this)">🧠 AI & OCR</button>
        <button class="tfilter-btn" onclick="filterMatrix('security', this)">🛡️ Privacy & Speed</button>
        <button class="tfilter-btn" onclick="filterMatrix('pricing', this)">💰 Pricing</button>
      </div>
    </div>

    <!-- Matrix Table Container -->
    <div class="matrix-table-wrap">
      <table class="matrix-table" id="comparison-table">
        <thead>
          <tr>
            <th class="col-feature">Capability & Feature</th>
            <th class="col-l2cache">⚡ L2Cache (Modern Native)</th>
            <th class="col-comp">📦 {{competitor_name}}</th>
          </tr>
        </thead>
        <tbody>
          {{comparison_table_rows}}
        </tbody>
      </table>
    </div>

    <!-- Key Differences Cards -->
    <h2 style="font-size: 28px; font-weight: 800; color: #fff; margin: 48px 0 24px;">💡 Deep-Dive: Why Developers Shift to L2Cache</h2>
    {{l2cache_advantages_html}}

    <!-- High-Impact Shift CTA Card -->
    <div class="shift-cta-box">
      <h2>Ready to Upgrade Your Mac Clipboard?</h2>
      <p>
        Experience sub-50ms panel activation, on-device Apple Intelligence OCR search, and Touch ID key security. Free during early access.
      </p>
      <a href="https://apps.apple.com/us/app/l2cache/id6774423992?mt=12" class="cta-download-btn" target="_blank" rel="noopener">
        🍎 Download L2Cache Free on Mac App Store
      </a>
      <div class="cta-guarantee-note">
        ✨ macOS 13+ · Universal Binary (M1/M2/M3/M4 & Intel) · Zero Credit Card Required
      </div>
    </div>

    <!-- FAQ Section -->
    <div class="faq-section">
      <h2>Frequently Asked Questions</h2>
      {{faq_html}}
    </div>

  </article>

  <!-- Footer -->
  <footer>
    <div class="footer-brand">L2Cache 📋</div>
    <ul class="footer-links">
      <li><a href="/en/">Home</a></li>
      <li><a href="/en/benchmark">Benchmark 2026</a></li>
      <li><a href="/en/tools">Free Tools</a></li>
      <li><a href="/en/privacy">Privacy</a></li>
      <li><a href="/en/support">Support</a></li>
    </ul>
    <p style="font-size:12px; color:var(--text-dim); margin:0;">© 2026 Amvotech · 100% On-Device Mac Intelligence</p>
  </footer>

  <script src="../tools/tools-engine.js"></script>
  <script>
    function filterMatrix(category, btn) {
      document.querySelectorAll('.tfilter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const rows = document.querySelectorAll('#comparison-table tbody tr');
      rows.forEach(r => {
        const cat = r.getAttribute('data-cat') || 'all';
        if (category === 'all' || cat.includes(category)) {
          r.style.display = '';
        } else {
          r.style.display = 'none';
        }
      });
    }
  </script>
</body>
</html>"""

# Write updated template to l2cache-site
template_path = "/Users/dinesh/tech/l2cache-site/comparison-template.html"
with open(template_path, "w", encoding="utf-8") as f:
    f.write(UPGRADED_TEMPLATE)

print("Wrote upgraded comparison-template.html!")
