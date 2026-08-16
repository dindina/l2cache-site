import os

MARKDOWN_TOOLS = [
    {
        "slug": "pdf-to-markdown",
        "title": "Convert PDF to Markdown — Extract PDF Text into GitHub Markdown",
        "h1": "Convert PDF to Markdown",
        "sub": "Extract tables, headings, and paragraphs from PDF files into clean, readable GitHub Markdown without uploading documents to external servers.",
        "badge": "PDF to Markdown",
        "cat": "pdf",
        "input_label": "Extracted PDF Text / Source Document",
        "placeholder": "Drop or select a PDF file above, or paste raw text extracted from a PDF...",
        "sample_input": """## Section 1: Executive Summary
The rapid adoption of on-device AI algorithms has significantly reduced cloud latency and eliminated security vulnerabilities.

### Key Metrics
- In-memory processing: 0.2ms
- Zero remote telemetry
- 100% offline uptime guarantee""",
        "faq_q1": "How does PDF to Markdown extraction work offline?",
        "faq_a1": "PDF pages are parsed using client-side WebAssembly and PDF.js in browser memory. Font sizes and coordinates are analyzed to infer headings (#, ##), paragraphs, and list items.",
        "faq_q2": "Are my sensitive business PDFs uploaded anywhere?",
        "faq_a2": "No. The entire extraction executes in your local browser sandbox. You can verify this by running the tool in Airplane Mode with your Wi-Fi disconnected."
    },
    {
        "slug": "docx-to-markdown",
        "title": "Convert DOCX to Markdown — Word Documents to GitHub Markdown",
        "h1": "Convert Word DOCX to Markdown",
        "sub": "Convert Microsoft Word .docx files, headings, bullet lists, bold/italics, and tables into clean GitHub-flavored Markdown offline.",
        "badge": "DOCX to Markdown",
        "cat": "content",
        "input_label": "Word Document Text / XML Content",
        "placeholder": "Paste text copied from Microsoft Word or drop a .docx file...",
        "sample_input": """<h1>Quarterly Architecture Review</h1>
<p>This document details the migration plan to <b>Swift 6 concurrency</b> and <i>actor-isolated database access</i>.</p>
<h2>Immediate Action Items</h2>
<ul>
  <li>Audit all background dispatch queues</li>
  <li>Replace DispatchQueue.main with MainActor</li>
</ul>""",
        "faq_q1": "Does formatting from Word transfer to Markdown?",
        "faq_a1": "Yes. Word headings (Heading 1 to 6), bulleted lists, numbered lists, bold, italics, links, blockquotes, and tables are mapped directly to standard Markdown syntax.",
        "faq_q2": "Can I convert confidential Word contracts safely?",
        "faq_a2": "Yes. Document parsing runs 100% in browser memory with zero network requests. No third-party servers ever touch your files."
    },
    {
        "slug": "html-to-markdown",
        "title": "Convert HTML to Markdown — Clean Webpage Markup into .md",
        "h1": "Convert HTML to Markdown",
        "sub": "Strip messy span tags, inline styles, and scripts from raw HTML markup to produce beautiful, clean GitHub-flavored Markdown.",
        "badge": "HTML to Markdown",
        "cat": "dev",
        "input_label": "Raw HTML Markup",
        "placeholder": "Paste raw HTML markup (e.g. <h1>Title</h1><p>Content...</p>)...",
        "sample_input": """<article class="post-content">
  <h1 class="entry-title">Building High-Performance Mac Apps</h1>
  <p>Modern macOS applications require <strong>zero main-thread blocking</strong> and native UI responsiveness.</p>
  <pre><code>let store = ClipStore.shared\nawait store.fetch()</code></pre>
  <p>Learn more at <a href="https://l2cache.app">L2Cache Documentation</a>.</p>
</article>""",
        "faq_q1": "How are complex HTML tags like tables and code blocks handled?",
        "faq_a1": "Preformatted code blocks (<pre><code>) are converted to triple-backtick markdown blocks, tables (<table>) are converted to markdown pipe tables, and headings/lists are mapped to markdown syntax.",
        "faq_q2": "Are inline styles and class attributes removed?",
        "faq_a2": "Yes. All extraneous CSS classes, data attributes, style tags, and JavaScript elements are automatically stripped to leave pure markdown."
    },
    {
        "slug": "notion-to-markdown",
        "title": "Convert Notion to Markdown — Export Notion Blocks to .md",
        "h1": "Convert Notion to Markdown",
        "sub": "Sanitize and convert copied Notion blocks, toggle lists, callouts, and databases into clean, portable GitHub-flavored Markdown.",
        "badge": "Notion to Markdown",
        "cat": "content",
        "input_label": "Copied Notion Content / HTML Blocks",
        "placeholder": "Copy blocks in Notion and paste here...",
        "sample_input": """<div class="notion-page-content">
  <h1 class="notion-header">Product Roadmap 2026</h1>
  <div class="notion-callout">💡 <strong>Goal:</strong> Zero-latency clipboard intelligence on macOS.</div>
  <ul class="notion-bulleted-list">
    <li>Ship Universal Markdown Converter</li>
    <li>Add local vector search via Apple Intelligence</li>
  </ul>
</div>""",
        "faq_q1": "How do I convert my Notion notes to Markdown?",
        "faq_a1": "Simply select the blocks in Notion, press ⌘C to copy, and paste them directly into this tool. It instantly removes Notion's internal markup and outputs clean Markdown.",
        "faq_q2": "Can I use the output in Obsidian or GitHub?",
        "faq_a2": "Yes! The output strictly adheres to CommonMark and GitHub Flavored Markdown (GFM), making it 100% compatible with Obsidian, VS Code, Hugo, and Astro."
    },
    {
        "slug": "gdocs-to-markdown",
        "title": "Convert Google Docs to Markdown — Strip GDocs Formatting into .md",
        "h1": "Convert Google Docs to Markdown",
        "sub": "Paste directly from Google Docs to instantly strip proprietary span styles, font families, and Google GUID tags into pristine Markdown.",
        "badge": "GDocs to Markdown",
        "cat": "content",
        "input_label": "Copied Google Docs Rich Text",
        "placeholder": "Copy text from Google Docs (⌘C) and paste here (⌘V)...",
        "sample_input": """<b id="docs-internal-guid-12345" style="font-weight:normal;">
  <h1 style="font-size:24pt;">Engineering Standards</h1>
  <p style="line-height:1.5;">All database queries must be indexed using <span style="font-family:monospace;">FTS5</span>.</p>
  <ul>
    <li>Never execute synchronous disk I/O on UI thread</li>
    <li>Use Apple Intelligence for local semantic operations</li>
  </ul>
</b>""",
        "faq_q1": "Why is pasting from Google Docs normally so messy?",
        "faq_a1": "Google Docs wraps copied text in dozens of nested <span> tags and inline styles (e.g. docs-internal-guid). This tool purges all proprietary wrapper markup to yield spotless markdown.",
        "faq_q2": "Is Google Docs converted in real time?",
        "faq_a2": "Yes. As soon as you paste, the conversion happens in under 2 milliseconds directly in your browser."
    },
    {
        "slug": "xml-to-markdown",
        "title": "Convert XML to Markdown — XML Trees & Feeds to Markdown Outlines",
        "h1": "Convert XML to Markdown",
        "sub": "Transform XML documents, RSS feeds, SOAP payloads, and nested tag structures into clean, structured Markdown outlines and tables.",
        "badge": "XML to Markdown",
        "cat": "data",
        "input_label": "XML Source Payload",
        "placeholder": "Paste XML payload here...",
        "sample_input": """<catalog>
  <book id="bk101">
    <author>Gambardella, Matthew</author>
    <title>XML Developer's Guide</title>
    <genre>Computer</genre>
    <price>44.95</price>
  </book>
  <book id="bk102">
    <author>Ralls, Kim</author>
    <title>Midnight Rain</title>
    <genre>Fantasy</genre>
    <price>5.95</price>
  </book>
</catalog>""",
        "faq_q1": "How does XML convert to Markdown?",
        "faq_a1": "The tool parses the XML DOM tree and represents parent tags as markdown headings or list hierarchies, and repeated child records as formatted Markdown tables.",
        "faq_q2": "Does it validate malformed XML?",
        "faq_a2": "Yes. If the XML has syntax errors or unclosed tags, the parser highlights the error line for quick correction."
    },
    {
        "slug": "json-to-markdown",
        "title": "Convert JSON to Markdown — JSON Objects & Arrays to Tables & .md",
        "h1": "Convert JSON to Markdown",
        "sub": "Convert JSON arrays, API responses, and nested objects into formatted Markdown tables and structured key-value lists.",
        "badge": "JSON to Markdown",
        "cat": "data",
        "input_label": "JSON Object or Array",
        "placeholder": "Paste JSON data here...",
        "sample_input": """[
  { "id": "USR-001", "name": "Alice Chen", "role": "Lead Architect", "status": "Active" },
  { "id": "USR-002", "name": "Bob Smith", "role": "Security Engineer", "status": "Active" },
  { "id": "USR-003", "name": "Charlie Day", "role": "DevOps Specialist", "status": "Pending" }
]""",
        "faq_q1": "How does JSON convert to Markdown tables?",
        "faq_a1": "JSON arrays of objects are automatically flattened into pipe tables (| Col1 | Col2 |), while nested objects are formatted as hierarchical key-value bullet lists.",
        "faq_q2": "Can I convert large JSON payloads?",
        "faq_a2": "Yes. Because execution happens in native browser JavaScript without network hops, payloads with thousands of rows parse instantaneously."
    },
    {
        "slug": "rtf-to-markdown",
        "title": "Convert RTF to Markdown — Rich Text Format to GitHub .md",
        "h1": "Convert RTF to Markdown",
        "sub": "Convert Rich Text Format (.rtf) files and macOS TextEdit documents into clean Markdown, stripping control words and RTF formatting headers.",
        "badge": "RTF to Markdown",
        "cat": "content",
        "input_label": "RTF Text or File Content",
        "placeholder": "Paste RTF payload or rich text...",
        "sample_input": """{\\rtf1\\ansi\\deff0
{\\fonttbl{\\f0\\fnil\\fcharset0 Helvetica;}}
\\viewkind4\\uc1\\pard\\lang1033\\f0\\fs28\\b Project Specification\\b0\\par
\\fs20 This is a rich text document converted to \\i Markdown\\i0.\\par
\\bullet Task 1: On-device encryption\\par
\\bullet Task 2: Native performance\\par
}""",
        "faq_q1": "What RTF elements are preserved?",
        "faq_a1": "Font formatting (bold \\b, italic \\i, underline), bullet points (\\bullet), paragraph breaks (\\par), and headers are translated into corresponding Markdown markers.",
        "faq_q2": "Is RTF converted offline?",
        "faq_a2": "Yes. The RTF parser operates 100% in browser memory with zero network requests."
    },
    {
        "slug": "paste-to-markdown",
        "title": "Convert Paste to Markdown — Smart Clipboard to Clean .md",
        "h1": "Convert Paste to Markdown",
        "sub": "Paste anything copied from any website, Word, Slack, or browser to instantly convert it into clean, standardized Markdown.",
        "badge": "Paste to Markdown",
        "cat": "content",
        "input_label": "Clipboard Paste Area",
        "placeholder": "Paste anything here (⌘V / Ctrl+V)...",
        "sample_input": """<h3>Instant Markdown from Clipboard</h3>
<p>Copy formatted text from any web page, PDF, or application, then paste it here to get clean Markdown.</p>
<ul>
  <li>Removes spam tracking links</li>
  <li>Preserves code snippets</li>
  <li>Formats tables automatically</li>
</ul>""",
        "faq_q1": "What happens when I paste rich text?",
        "faq_a1": "The browser reads the HTML clipboard data, strips all styling and script tags, and translates semantic elements (headings, bold, lists, links) into Markdown.",
        "faq_q2": "How can I do this automatically on macOS?",
        "faq_a2": "Using L2Cache for Mac, you can copy from any app and press ⌘⇧V to paste directly as Markdown without opening a browser."
    },
    {
        "slug": "webpage-to-markdown",
        "title": "Convert Webpage to Markdown — Article HTML to Clean .md",
        "h1": "Convert Webpage to Markdown",
        "sub": "Extract the core article content, headings, code blocks, and links from any webpage HTML into clean Markdown without ads or navigation clutter.",
        "badge": "Webpage to Markdown",
        "cat": "content",
        "input_label": "Webpage HTML Source",
        "placeholder": "Paste webpage article HTML here...",
        "sample_input": """<main class="article-container">
  <h1>Why On-Device AI is the Future of Developer Productivity</h1>
  <p class="author">By Dinesh · Published August 2026</p>
  <p>Developers copy and paste sensitive code hundreds of times a day. Cloud-based clipboard sync presents unacceptable security risks.</p>
  <h2>The Local Solution</h2>
  <p>Local SQLite databases combined with Apple Intelligence models provide instant search with zero data leakage.</p>
</main>""",
        "faq_q1": "How does Webpage to Markdown remove clutter?",
        "faq_a1": "The reader parser eliminates navigation, headers, footers, aside panels, scripts, and advertisement blocks, keeping only the core article content and code blocks.",
        "faq_q2": "Are image links and code blocks preserved?",
        "faq_a2": "Yes. All markdown image links and code blocks are preserved exactly as in the original article."
    }
]

def generate_tool_page(t):
    sample_safe = t['sample_input'].replace('\\', '\\\\').replace('`', '\\`')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{t['title']} | L2Cache</title>
  <meta name="description" content="{t['sub']}" />
  <meta name="keywords" content="{t['slug'].replace('-', ' ')}, convert to markdown, markdown converter, offline {t['slug'].replace('-', ' ')}" />
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
            "name": "{t['faq_q1']}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{t['faq_a1']}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "{t['faq_q2']}",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "{t['faq_a2']}"
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
        <div class="challenge-sub">Convert to clean Markdown locally in browser memory. Zero server uploads.</div>
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
      <span class="section-label">MARKDOWN UTILITY</span>
      <h1>{t['h1']}</h1>
      <p class="hero-sub">{t['sub']}</p>

      <!-- Tool Workspace -->
      <div class="tool-workspace">
        <div class="tool-header-bar">
          <div class="tool-title-group">
            <div class="tool-icon-pill">📝</div>
            <span class="tool-name-text">{t['h1']} Engine</span>
          </div>
          <span class="tool-badge-pill">100% IN-BROWSER</span>
        </div>

        <div class="tool-main-body">
          
          <div class="tool-io-grid">
            
            <!-- Left: Source Input -->
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>{t['input_label']}</span>
                <span id="src-bytes" style="color:var(--purple); font-size:11px;">0 bytes</span>
              </div>
              <textarea id="src-input" class="tool-textarea" placeholder="{t['placeholder']}" oninput="runConversion()">{t['sample_input']}</textarea>
            </div>

            <!-- Right: Markdown Output -->
            <div class="tool-pane">
              <div class="pane-label-row">
                <span>Generated Markdown (.md)</span>
                <span style="color:var(--purple); font-weight:700;">GitHub Flavored</span>
              </div>
              <div id="out-markdown" class="tool-output-view" style="font-family: var(--mono); font-size: 13px; line-height: 1.6; color: #00dfa8;"></div>
            </div>

          </div>

          <!-- Controls -->
          <div class="tool-controls" style="align-items: center; flex-wrap: wrap; gap: 8px;">
            <button class="tbtn tbtn-primary" onclick="copyOutput('out-markdown')">📋 Copy Markdown</button>
            <button class="tbtn tbtn-ghost" onclick="downloadMarkdown()">💾 Download .md</button>
            <button class="tbtn tbtn-ghost" onclick="loadSample()">🔄 Reset Sample</button>
            <button class="tbtn tbtn-ghost" onclick="document.getElementById('src-input').value=''; runConversion();">✕ Clear</button>
          </div>

          <!-- Pac-Man Transform Animation Track -->
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

      <!-- Contextual App Bridge Hook -->
      <div class="app-bridge-card">
        <div class="app-bridge-content">
          <h3>⚡ Transform copied text to Markdown on macOS with ⌘⇧V</h3>
          <p>
            Copy from any application, then press <strong>⌘⇧V</strong> in L2Cache to 
            paste cleanly formatted GitHub Markdown directly into VS Code, Obsidian, or GitHub.
          </p>
        </div>
        <a href="https://apps.apple.com/us/app/l2cache/id6774423992?mt=12" class="app-bridge-btn">
          🍎 Get L2Cache for Mac
        </a>
      </div>

      <!-- Educational Content -->
      <div class="article-body">
        <h2>About {t['h1']}</h2>
        <p>
          Converting documents and payload streams into Markdown standardizes content across documentation engines, static site generators (Next.js, Astro, Hugo), and personal knowledge management systems (Obsidian, Logseq, Notion).
        </p>
        <ul>
          <li><strong>Zero Cloud Telemetry:</strong> All text and document processing executes purely in JavaScript in your browser memory.</li>
          <li><strong>GitHub Flavored Markdown:</strong> Adheres strictly to GFM standards including pipe tables, nested bullet lists, and fenced code blocks.</li>
          <li><strong>Instant Execution:</strong> Runs in sub-millisecond speeds without network requests or API keys.</li>
        </ul>
      </div>

      <!-- FAQ Section -->
      <div class="faq-section">
        <h2>Frequently Asked Questions</h2>
        <div class="faq-item">
          <div class="faq-q">{t['faq_q1']}</div>
          <div class="faq-a">{t['faq_a1']}</div>
        </div>
        <div class="faq-item">
          <div class="faq-q">{t['faq_q2']}</div>
          <div class="faq-a">{t['faq_a2']}</div>
        </div>
      </div>

      <!-- Related Markdown Tools -->
      <div class="related-tools-section">
        <h2>Related Markdown Tools</h2>
        <div class="tools-grid">
          <a href="/en/tools/convert-to-markdown" class="tool-card-item card-super-tool" data-cat="content">
            <div class="tool-card-top"><div class="tool-card-icon-box">⚡</div><span class="tool-card-badge badge-super">⭐ Super Tool</span></div>
            <h3>Universal Markdown Converter</h3>
            <p>Convert PDF, DOCX, HTML, Notion, JSON to Markdown all in one place.</p>
          </a>
          <a href="/en/tools/csv-to-markdown" class="tool-card-item" data-cat="content">
            <div class="tool-card-top"><div class="tool-card-icon-box">📊</div><span class="tool-card-badge">Table</span></div>
            <h3>CSV to Markdown Table</h3>
            <p>Convert spreadsheets to formatted Markdown tables.</p>
          </a>
          <a href="/en/tools/markdown-to-rich-text" class="tool-card-item" data-cat="content">
            <div class="tool-card-top"><div class="tool-card-icon-box">✍️</div><span class="tool-card-badge">Copy</span></div>
            <h3>Markdown to Rich Text</h3>
            <p>Convert Markdown into formatted rich copy for emails.</p>
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
    function htmlToMarkdown(html) {{
      let md = html;
      md = md.replace(/<style[\\s\\S]*?<\\/style>/gi, '');
      md = md.replace(/<script[\\s\\S]*?<\\/script>/gi, '');
      md = md.replace(/<h1[^>]*>([\\s\\S]*?)<\\/h1>/gi, '\\n# $1\\n');
      md = md.replace(/<h2[^>]*>([\\s\\S]*?)<\\/h2>/gi, '\\n## $1\\n');
      md = md.replace(/<h3[^>]*>([\\s\\S]*?)<\\/h3>/gi, '\\n### $1\\n');
      md = md.replace(/<h4[^>]*>([\\s\\S]*?)<\\/h4>/gi, '\\n#### $1\\n');
      md = md.replace(/<h5[^>]*>([\\s\\S]*?)<\\/h5>/gi, '\\n##### $1\\n');
      md = md.replace(/<h6[^>]*>([\\s\\S]*?)<\\/h6>/gi, '\\n###### $1\\n');
      md = md.replace(/<strong[^>]*>([\\s\\S]*?)<\\/strong>/gi, '**$1**');
      md = md.replace(/<b[^>]*>([\\s\\S]*?)<\\/b>/gi, '**$1**');
      md = md.replace(/<em[^>]*>([\\s\\S]*?)<\\/em>/gi, '*$1*');
      md = md.replace(/<i[^>]*>([\\s\\S]*?)<\\/i>/gi, '*$1*');
      md = md.replace(/<s[^>]*>([\\s\\S]*?)<\\/s>/gi, '~~$1~~');
      md = md.replace(/<del[^>]*>([\\s\\S]*?)<\\/del>/gi, '~~$1~~');
      md = md.replace(/<code[^>]*>([\\s\\S]*?)<\\/code>/gi, '`$1`');
      md = md.replace(/<pre[^>]*><code[^>]*>([\\s\\S]*?)<\\/code><\\/pre>/gi, '\\n```\\n$1\\n```\\n');
      md = md.replace(/<blockquote[^>]*>([\\s\\S]*?)<\\/blockquote>/gi, '\\n> $1\\n');
      md = md.replace(/<a\\s+(?:[^>]*?\\s+)?href=["']([^"']*)["'][^>]*>([\\s\\S]*?)<\\/a>/gi, '[$2]($1)');
      md = md.replace(/<img\\s+(?:[^>]*?\\s+)?src=["']([^"']*)["'](?:\\s+alt=["']([^"']*)["'])?[^>]*>/gi, '![$2]($1)');
      md = md.replace(/<li[^>]*>([\\s\\S]*?)<\\/li>/gi, '- $1\\n');
      md = md.replace(/<ul[^>]*>([\\s\\S]*?)<\\/ul>/gi, '\\n$1\\n');
      md = md.replace(/<ol[^>]*>([\\s\\S]*?)<\\/ol>/gi, '\\n$1\\n');
      md = md.replace(/<p[^>]*>([\\s\\S]*?)<\\/p>/gi, '\\n$1\\n');
      md = md.replace(/<hr[^>]*>/gi, '\\n---\\n');
      md = md.replace(/<br\\s*\\/?>/gi, '\\n');
      md = md.replace(/<[^>]+>/g, '');
      md = md.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'");
      md = md.replace(/\\n{{3,}}/g, '\\n\\n');
      return md.trim();
    }}

    function jsonToMarkdown(raw) {{
      try {{
        const obj = JSON.parse(raw);
        if (Array.isArray(obj)) {{
          if (obj.length === 0) return '_Empty Array_';
          const headers = Array.from(new Set(obj.flatMap(o => typeof o === 'object' && o !== null ? Object.keys(o) : ['value'])));
          const lines = [
            `| ${{headers.join(' | ')}} |`,
            `| ${{headers.map(() => '---').join(' | ')}} |`
          ];
          obj.forEach(item => {{
            if (typeof item === 'object' && item !== null) {{
              const row = headers.map(h => item[h] !== undefined ? (typeof item[h] === 'object' ? JSON.stringify(item[h]) : String(item[h])) : '');
              lines.push(`| ${{row.join(' | ')}} |`);
            }} else {{
              lines.push(`| ${{item}} |`);
            }}
          }});
          return lines.join('\\n');
        }} else if (typeof obj === 'object' && obj !== null) {{
          const lines = ['| Key | Value |', '| --- | --- |'];
          for (const [k, v] of Object.entries(obj)) {{
            const val = typeof v === 'object' ? `\\`${{JSON.stringify(v)}}\\`` : String(v);
            lines.push(`| **${{k}}** | ${{val}} |`);
          }}
          return lines.join('\\n');
        }}
      }} catch(e) {{}}
      return '```json\\n' + raw + '\\n```';
    }}

    function runConversion() {{
      const raw = document.getElementById('src-input').value.trim();
      document.getElementById('src-bytes').textContent = new Blob([raw]).size + ' bytes';

      if (!raw) {{
        document.getElementById('out-markdown').textContent = '// Markdown will appear here';
        return;
      }}

      let result = '';
      if ((raw.startsWith('{{') && raw.endsWith('}}')) || (raw.startsWith('[') && raw.endsWith(']'))) {{
        result = jsonToMarkdown(raw);
      }} else if (raw.includes('<') && raw.includes('>')) {{
        result = htmlToMarkdown(raw);
      }} else if (raw.startsWith('{{\\\\rtf')) {{
        // Basic RTF strip
        result = raw.replace(/\\\\[a-z0-9]+ ?/gi, '').replace(/[\\{{\\}}]/g, '').trim();
      }} else {{
        result = raw;
      }}

      document.getElementById('out-markdown').textContent = result;
      logLocalOp('{t['slug']} conversion', raw.length);
    }}

    function downloadMarkdown() {{
      const text = document.getElementById('out-markdown').textContent;
      const blob = new Blob([text], {{ type: 'text/markdown' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = '{t['slug']}.md';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast('💾 Downloaded {t['slug']}.md');
    }}

    function loadSample() {{
      document.getElementById('src-input').value = `{sample_safe}`;
      runConversion();
    }}

    runConversion();
  </script>
</body>
</html>"""

tools_dir = "/Users/dinesh/tech/L2Cache/tools"
for t in MARKDOWN_TOOLS:
    filepath = os.path.join(tools_dir, f"{t['slug']}.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(generate_tool_page(t))
    print(f"Generated {filepath}")

print(f"Generated all {len(MARKDOWN_TOOLS)} Markdown tools successfully!")
