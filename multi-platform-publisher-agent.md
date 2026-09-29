# Multi-Platform Article Publisher Agent

A plugin-based agent that reads a single Markdown file and publishes it to multiple content platforms simultaneously. New platforms are added by implementing a one-file adapter.

---

## Table of Contents

1. [Article Frontmatter Spec](#1-article-frontmatter-spec)
2. [Agent Architecture](#2-agent-architecture)
3. [Platform Adapters](#3-platform-adapters)
   - [Dev.to](#31-devto)
   - [Hashnode](#32-hashnode)
   - [GitHub Pages (GitHub.io)](#33-github-pages-githubio)
   - [LinkedIn (future)](#34-linkedin)
   - [X.com / Twitter (future)](#35-xcom--twitter)
   - [Medium — Deprecated](#36-medium--deprecated)
4. [Environment Variables](#4-environment-variables)
5. [CLI Usage](#5-cli-usage)
6. [Agent Workflow](#6-agent-workflow)
7. [Adding a New Platform](#7-adding-a-new-platform)
8. [Error Handling & Retry Policy](#8-error-handling--retry-policy)
9. [Full Example Article](#9-full-example-article)
10. [Roadmap](#10-roadmap)

---

## 1. Article Frontmatter Spec

Every article is a standard `.md` file. The YAML frontmatter block at the top controls where and how it gets published.

```yaml
---
# ── Core metadata ────────────────────────────────────────────────────
title: "Your Article Title"
description: "One-sentence summary shown as subtitle / meta description."
tags: [javascript, webdev, tutorial, productivity]       # max 4 for Dev.to
canonical_url: "https://yourblog.com/slug"               # optional: your authoritative URL

# ── Publishing targets ───────────────────────────────────────────────
publish_to:
  devto:
    enabled: true
    published: false            # false = draft ✅ | true = live
    series: ""                  # optional series name
    organization_id: null       # optional org to post under

  hashnode:
    enabled: true
    publication_id: ""          # required — your Hashnode publication/blog id
    draft: true                 # true = draft ✅ | false = live

  github_pages:
    enabled: true
    repo: "username/username.github.io"
    branch: "main"
    posts_dir: "_posts"         # Jekyll default; change for Hugo/Astro
    site_engine: "jekyll"       # "jekyll" | "hugo" | "astro" | "nextjs"
    draft: true                 # true = commit to _drafts/ folder ✅
    commit_message: "draft: add new article"

  linkedin:
    enabled: false              # not yet implemented — set true when ready
    visibility: "PUBLIC"        # "PUBLIC" | "CONNECTIONS"
    article_type: "long_form"   # "long_form" | "post" (post = short status update)
    draft: true

  twitter_x:
    enabled: false              # not yet implemented
    thread_mode: false          # true = split into a thread

  # medium: REMOVED — Medium shut down public API in 2024, no new tokens issued.

# ── Cover image ──────────────────────────────────────────────────────
cover_image: "https://example.com/cover.png"   # used by Dev.to, Hashnode, Medium

# ── Scheduling (optional) ────────────────────────────────────────────
scheduled_at: ""               # ISO 8601 — e.g. "2026-10-01T09:00:00Z"
                               # empty = publish immediately
---
```

> **Rule**: anything not in `publish_to` is ignored. Add a new key to enable a new platform.

---

## 2. Agent Architecture

```
article.md
    │
    ▼
┌─────────────────────────────────────────┐
│             Parser & Validator          │  parse frontmatter, validate required fields
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│           Content Transformer           │  convert MD → HTML, handle images, inline code
└────────────────────┬────────────────────┘
                     │
          ┌──────────┼──────────┐──────────┐
          ▼          ▼          ▼          ▼
    ┌──────────┐ ┌──────┐ ┌────────┐ ┌──────────┐
    │  Medium  │ │Dev.to│ │Hashnode│ │  GitHub  │  ... adapter per platform
    │ Adapter  │ │Adptr │ │ Adptr  │ │  Adapter │
    └────┬─────┘ └──┬───┘ └───┬────┘ └────┬─────┘
         │          │         │            │
         ▼          ▼         ▼            ▼
    Platform     Platform  Platform    Platform
    API call     API call  API call    git push
         │          │         │            │
         └──────────┴────┬────┴────────────┘
                         ▼
              ┌─────────────────────┐
              │    Result Reporter  │  print success/fail URLs per platform
              └─────────────────────┘
```

**Design principles:**
- Each adapter is a self-contained module: `adapters/<platform>.js`
- Adapters receive a normalized `Article` object — not the raw markdown
- All API credentials come from environment variables only
- Failures in one adapter never block other adapters (parallel execution, isolated errors)

---

## 3. Platform Adapters

### 3.1 Dev.to

**API**: REST — `https://dev.to/api`  
**Auth**: API key header `api-key: <key>`  
**Docs**: https://developers.forem.com/api

#### Getting credentials
1. Go to **Dev.to → Settings → Account → DEV Community API Keys**
2. Generate key and set `DEVTO_API_KEY=<key>`

#### API call

```
POST /api/articles
```

#### Request body

```json
{
  "article": {
    "title": "Article Title",
    "body_markdown": "<full markdown string>",
    "published": false,          // always false = draft
    "tags": ["tag1", "tag2"],
    "series": "My Series",
    "canonical_url": "https://...",
    "main_image": "https://example.com/cover.png",
    "organization_id": null
  }
}
```

#### Response

```json
{
  "id": 12345,
  "url": "https://dev.to/user/article-title-abc1"
}
```

---

### 3.2 Hashnode

**API**: GraphQL — `https://gql.hashnode.com`  
**Auth**: Bearer token header  
**Docs**: https://apidocs.hashnode.com

#### Getting credentials
1. Go to **Hashnode → Account Settings → Developer → Personal Access Tokens**
2. Generate token and set `HASHNODE_TOKEN=<token>`
3. Find `publication_id` from your Hashnode blog settings URL

#### GraphQL mutation

```graphql
mutation PublishPost($input: PublishPostInput!) {
  publishPost(input: $input) {
    post {
      id
      url
    }
  }
}
```

#### Variables

```json
{
  "input": {
    "title": "Article Title",
    "contentMarkdown": "<full markdown string>",
    "tags": [{ "name": "tag1" }, { "name": "tag2" }],
    "coverImageOptions": {
      "coverImageURL": "https://example.com/cover.png"
    },
    "originalArticleURL": "https://...",
    "publicationId": "<your-publication-id>",
    "isDraft": true              // always true = draft
  }
}
```

---

### 3.3 GitHub Pages (GitHub.io)

**API**: GitHub REST API — `https://api.github.com`  
**Auth**: Personal Access Token (PAT) with `repo` scope  
**Docs**: https://docs.github.com/en/rest/repos/contents

This adapter **does not call a publishing API** — it commits the markdown file into your GitHub Pages repository. Jekyll/Hugo/Astro then builds and deploys it automatically via GitHub Actions.

#### Getting credentials
1. Go to **GitHub → Settings → Developer settings → Personal access tokens**
2. Generate token with `repo` scope and set `GITHUB_TOKEN=<token>`

#### File naming

| Engine | Format | Example |
|--------|--------|---------|
| Jekyll | `YYYY-MM-DD-slug.md` | `2026-09-28-my-article.md` |
| Hugo | `slug.md` in `content/posts/` | `my-article.md` |
| Astro | `slug.md` in `src/content/blog/` | `my-article.md` |

#### API flow

```
1. GET /repos/{owner}/{repo}/contents/{path}
   → to check if file exists (get SHA for update)

2. PUT /repos/{owner}/{repo}/contents/{path}
   body: {
     "message": "post: add my-article",
     "content": "<base64-encoded markdown>",
     "sha": "<sha if updating>",
     "branch": "main"
   }
```

The adapter prepends the correct Jekyll/Hugo/Astro frontmatter automatically based on `site_engine`.

**Jekyll frontmatter example injected by adapter:**
```yaml
---
layout: post
title: "Article Title"
date: 2026-09-28 09:00:00 +0000
tags: [tag1, tag2]
description: "One-sentence summary"
image: https://example.com/cover.png
---
```

---

### 3.4 LinkedIn

**API**: REST — `https://api.linkedin.com/v2`  
**Auth**: OAuth 2.0 (3-legged)  
**Docs**: https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin

> Status: adapter stub ready, OAuth flow pending.

#### Setup (when enabled)
1. Create a LinkedIn app at **LinkedIn Developer Portal**
2. Request `w_member_social` permission
3. Complete OAuth2 flow → set `LINKEDIN_ACCESS_TOKEN=<token>`
4. Get your `person URN` from `GET /v2/me` → set `LINKEDIN_PERSON_URN=urn:li:person:ABC`

#### API call

```
POST /v2/ugcPosts
```

#### Request body (long-form article)

```json
{
  "author": "urn:li:person:ABC",
  "lifecycleState": "PUBLISHED",
  "specificContent": {
    "com.linkedin.ugc.ShareContent": {
      "shareCommentary": {
        "text": "Check out my new article: Article Title\n\n#tag1 #tag2"
      },
      "shareMediaCategory": "ARTICLE",
      "media": [
        {
          "status": "READY",
          "originalUrl": "https://yourblog.com/slug",
          "title": { "text": "Article Title" },
          "description": { "text": "One-sentence summary" }
        }
      ]
    }
  },
  "visibility": {
    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
  }
}
```

---

### 3.5 X.com / Twitter

**API**: Twitter API v2 — `https://api.twitter.com/2`  
**Auth**: OAuth 2.0 PKCE or Bearer token  
**Docs**: https://developer.twitter.com/en/docs/twitter-api

> Status: adapter stub ready, OAuth flow pending.

#### Setup (when enabled)
1. Create app at **developer.twitter.com**
2. Enable OAuth 2.0, request `tweet.write` scope
3. Set `TWITTER_ACCESS_TOKEN=<token>` and `TWITTER_ACCESS_TOKEN_SECRET=<secret>`

#### Post a tweet linking the article

```
POST /2/tweets
body: {
  "text": "📝 New post: Article Title\n\nhttps://yourblog.com/slug\n\n#tag1 #tag2"
}
```

#### Thread mode (when `thread_mode: true`)

Split the article into 280-char chunks and post as a reply chain:

```
POST /2/tweets  → first tweet (returns id)
POST /2/tweets  → { "text": "...", "reply": { "in_reply_to_tweet_id": "<first_id>" } }
...
```

---

### 3.6 Medium — Deprecated

> ⚠️ **Medium shut down their public API in 2024.** No new integration tokens are issued.  
> Existing tokens were revoked. The adapter has been removed from this agent.

**Workaround options:**
- Import via RSS: Medium can pull from your RSS feed automatically (Settings → Import a story)
- Manual copy-paste: paste the article into Medium editor after publishing elsewhere
- Third-party tools like [Zapier](https://zapier.com) offer limited Medium automation via unofficial methods

---

## 4. Environment Variables

Set these in a `.env` file (never commit it):

```bash
# Medium
MEDIUM_TOKEN=your_medium_integration_token

# Dev.to
DEVTO_API_KEY=your_devto_api_key

# Hashnode
HASHNODE_TOKEN=your_hashnode_personal_access_token

# GitHub Pages
GITHUB_TOKEN=your_github_pat_with_repo_scope
GITHUB_REPO=username/username.github.io   # overrides frontmatter if set

# LinkedIn (future)
LINKEDIN_ACCESS_TOKEN=your_linkedin_oauth2_token
LINKEDIN_PERSON_URN=urn:li:person:XXXXXXXX

# Twitter / X.com (future)
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_token_secret
```

---

## 5. CLI Usage

```bash
# Install
npm install

# Publish a single article (respects frontmatter publish_to flags)
node publish.js article.md

# Dry-run: validate + show what would be posted, no API calls
node publish.js --dry-run article.md

# Publish to specific platforms only (overrides frontmatter)
node publish.js --only devto,hashnode article.md

# Skip specific platforms
node publish.js --skip medium article.md

# Publish all .md files in a directory
node publish.js posts/

# Watch mode: republish on file save
node publish.js --watch article.md
```

---

## 6. Agent Workflow

```
publish.js article.md
│
├── 1. Read & parse article.md
│      ├── Extract YAML frontmatter
│      ├── Extract markdown body
│      └── Validate required fields (title, publish_to)
│
├── 2. Content transformation
│      ├── Resolve relative image URLs → absolute
│      ├── Convert markdown → HTML (for platforms needing HTML)
│      └── Generate slug from title (kebab-case)
│
├── 3. Check scheduled_at
│      └── If future timestamp → queue and exit; else continue
│
├── 4. For each enabled platform (run in parallel):
│      ├── Load adapter: require(`./adapters/${platform}.js`)
│      ├── Authenticate (validate token exists)
│      ├── Map Article → platform-specific payload
│      ├── POST to platform API
│      └── Return { platform, success, url, error }
│
└── 5. Report results
       ├── ✅ medium    → https://medium.com/@user/title-abc
       ├── ✅ devto     → https://dev.to/user/title-1234
       ├── ✅ hashnode  → https://user.hashnode.dev/title
       ├── ✅ github    → committed to username/username.github.io
       └── ❌ linkedin  → not enabled
```

---

## 7. Adding a New Platform

1. **Create** `adapters/myplatform.js`:

```javascript
// adapters/myplatform.js
export async function publish(article, config) {
  // article = {
  //   title, description, tags, body_markdown, body_html,
  //   cover_image, canonical_url, slug
  // }
  // config = values from frontmatter publish_to.myplatform
  //        + process.env.MYPLATFORM_TOKEN etc.

  const token = process.env.MYPLATFORM_TOKEN;
  if (!token) throw new Error("MYPLATFORM_TOKEN not set");

  const response = await fetch("https://api.myplatform.com/posts", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      title: article.title,
      content: article.body_markdown,
      tags: article.tags,
      draft: config.draft ?? true,
    }),
  });

  const data = await response.json();
  if (!response.ok) throw new Error(data.message || "Publish failed");

  return { url: data.url };
}
```

2. **Register** in `publish.js`:

```javascript
const ADAPTERS = {
  medium:       "./adapters/medium.js",
  devto:        "./adapters/devto.js",
  hashnode:     "./adapters/hashnode.js",
  github_pages: "./adapters/github_pages.js",
  linkedin:     "./adapters/linkedin.js",
  twitter_x:   "./adapters/twitter_x.js",
  myplatform:  "./adapters/myplatform.js",   // ← add this line
};
```

3. **Add** `MYPLATFORM_TOKEN` to `.env` and to the frontmatter spec.

That's it. The orchestrator auto-discovers and runs it.

---

## 8. Error Handling & Retry Policy

| Scenario | Behavior |
|----------|----------|
| Missing API token | Skip platform, log warning, continue others |
| Rate limit (429) | Retry with exponential backoff: 1s → 2s → 4s (max 3 retries) |
| Auth failure (401) | Fail fast, log "check your token", no retry |
| Network timeout | Retry up to 3 times, then skip |
| Partial failure | Report per-platform; exit code 1 if any platform failed |
| Dry-run mode | Log payload only, no API calls, always exit 0 |

---

## 9. Full Example Article

Save this as `my-article.md` and run `node publish.js my-article.md`:

```markdown
---
title: "5 JavaScript Tricks That Will Surprise You"
description: "Lesser-known JS patterns that can make your code cleaner and faster."
tags: [javascript, webdev, programming, tips]
canonical_url: "https://yourblog.com/5-js-tricks"
cover_image: "https://yourblog.com/images/js-tricks.png"

publish_to:
  medium:
    enabled: true
    status: "draft"
    notify_followers: false

  devto:
    enabled: true
    published: false

  hashnode:
    enabled: true
    publication_id: "your-hashnode-pub-id-here"
    draft: false

  github_pages:
    enabled: true
    repo: "yourname/yourname.github.io"
    branch: "main"
    posts_dir: "_posts"
    site_engine: "jekyll"
---

## Introduction

JavaScript has some hidden patterns that most developers never use...

## Trick 1: Nullish Coalescing Assignment

```js
let user = { name: null };
user.name ??= "Anonymous";
console.log(user.name); // "Anonymous"
```

## Trick 2: ...
```

---

## 10. Roadmap

| Platform | Status |
|----------|--------|
| Dev.to | ✅ Adapter complete — draft mode default |
| Hashnode | ✅ Adapter complete — draft mode default |
| GitHub Pages (Jekyll) | ✅ Adapter complete — commits to `_drafts/` |
| GitHub Pages (Hugo) | ✅ Adapter complete — draft mode default |
| GitHub Pages (Astro) | 🔧 In progress |
| LinkedIn | 🔲 Stub ready — OAuth pending |
| X.com / Twitter | 🔲 Stub ready — OAuth pending |
| Substack | 🔲 Planned (no public API yet; email import workaround) |
| Ghost | 🔲 Planned — Admin API available |
| WordPress | 🔲 Planned — REST API available |
| Notion | 🔲 Planned — useful for drafts/review workflow |
| Medium | ❌ Removed — API shut down in 2024 |

---

*Generated for [l2cache.amvo.store](https://l2cache.amvo.store) · Multi-Platform Publisher v1.0*
