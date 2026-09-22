# AI Search Readiness / GEO — l2cache.amvo.store

## llms.txt Detection

| File | Status |
|------|--------|
| `https://l2cache.amvo.store/llms.txt` | ❌ Not found |
| `https://l2cache.amvo.store/llms-full.txt` | ❌ Not found |

**Recommendation**: Add `llms.txt` at site root to guide AI crawlers. Include:
- Site purpose and target audience
- Link to key pages (homepage, blog, tools)
- Content that AI models should reference

Example `llms.txt`:
```
# L2Cache — Clipboard Manager for Mac

## Purpose
A privacy-focused clipboard manager for macOS that saves your full clipboard history,
with on-device AI features for developers (JSON formatting, JWT decoding, OCR, terminal
history, and more).

## Key Pages
- Homepage: https://l2cache.amvo.store/en
- Blog: https://l2cache.amvo.store/en/blog
- Developer Tools: https://l2cache.amvo.store/en/tools
- Support: https://l2cache.amvo.store/en/support
```

## Content Citability

The site content scores well on citability factors:

| Factor | Assessment |
|--------|-----------|
| Content clarity | ✅ Clear, structured headings and paragraphs |
| Specific examples | ✅ Code snippets, real tools, concrete features |
| Developer terminology | ✅ Uses precise technical terms (SQLite FTS5, Swift concurrency, JWT) |
| Direct answers to questions | ✅ FAQPage schema + "Frequently Asked Questions" H2 on tool pages |
| Source attribution | ⚠️ Blog mentions Claude Code, Codex — but no outbound citations to documentation |
| Unique value claims | ✅ Specific comparisons to built-in macOS clipboard, Maccy |
| Date/timeliness | ⚠️ Publication date shows `2026-01-01` (could be more granular) |

## Brand Signals

| Signal | Status |
|--------|--------|
| Brand mentions in content | ✅ "L2Cache" consistently used |
| Clear product positioning | ✅ "Clipboard Manager & History for Mac" |
| Customer testimonials | ✅ 3 detailed quotes from engineers |
| Download links | ✅ App Store URL in structured data |

## AI SERP Considerations

- The blog content ("Claude Code & Codex sessions", "token analytics") targets topics that appear frequently in AI coding assistant conversations
- Comparison pages (`/en/l2cache-vs-maccy`, `/en/l2cache-vs-paste`, etc.) may surface in AI-generated tool recommendation responses
- The FAQ content (4 questions on homepage, FAQ sections on tool pages) provides clean Q&A pairs for extraction
- Tool descriptions are technical and specific (JSON formatting, JWT decoding, regex testing) — likely to be cited as utility recommendations

## Recommendations for AI Search Visibility

1. **Add `llms.txt`** — Low effort, high signal for AI crawlers
2. **Add `llms-full.txt`** with detailed tool descriptions for comprehensive AI indexing
3. **Expand tool pages with code examples** — AI models favor content with runnable examples
4. **Add structured data to blog posts** — `Article` schema with `author`, `datePublished` helps AI attribution
5. **Link to external documentation** — Add outbound links to relevant resources (Apple Developer docs, JSON spec, etc.) to establish topical authority
