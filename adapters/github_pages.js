async function publish(article, config) {
  const token = process.env.GITHUB_TOKEN;
  if (!token) throw new Error('GITHUB_TOKEN not set in .env');

  const repo   = config.repo   || process.env.GITHUB_REPO;
  const branch = config.branch || process.env.GITHUB_BRANCH || 'main';
  const engine = config.site_engine || process.env.GITHUB_SITE_ENGINE || 'jekyll';
  const isDraft = config.draft ?? true;

  if (!repo) throw new Error('github_pages.repo not set in frontmatter or GITHUB_REPO in .env');

  const today = new Date().toISOString().split('T')[0];
  const postsDir = isDraft
    ? '_drafts'
    : (config.posts_dir || process.env.GITHUB_POSTS_DIR || '_posts');

  const filename = engine === 'jekyll' && !isDraft
    ? `${today}-${article.slug}.md`
    : `${article.slug}.md`;

  const filePath = `${postsDir}/${filename}`;
  const jekyllFrontmatter = buildFrontmatter(article, engine, today);
  const fileContent = `${jekyllFrontmatter}\n${article.body_markdown}`;
  const encoded = Buffer.from(fileContent).toString('base64');

  // Check if file already exists (need SHA to update)
  const checkRes = await fetch(
    `https://api.github.com/repos/${repo}/contents/${filePath}?ref=${branch}`,
    { headers: { Authorization: `Bearer ${token}`, 'User-Agent': 'publisher-agent' } }
  );
  const existing = checkRes.ok ? await checkRes.json() : null;

  const body = {
    message: `${isDraft ? 'draft' : 'post'}: add ${article.slug}`,
    content: encoded,
    branch,
    ...(existing ? { sha: existing.sha } : {}),
  };

  const putRes = await fetch(
    `https://api.github.com/repos/${repo}/contents/${filePath}`,
    {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
        'User-Agent': 'publisher-agent',
      },
      body: JSON.stringify(body),
    }
  );

  const result = await putRes.json();
  if (!putRes.ok) throw new Error(result.message || JSON.stringify(result));

  return { url: `https://github.com/${repo}/blob/${branch}/${filePath}` };
}

function buildFrontmatter(article, engine, date) {
  if (engine === 'hugo') {
    return [
      '---',
      `title: "${article.title.replace(/"/g, '\\"')}"`,
      `date: ${date}`,
      `draft: true`,
      `description: "${article.description.replace(/"/g, '\\"')}"`,
      article.cover_image ? `image: "${article.cover_image}"` : '',
      `tags: [${article.tags.map(t => `"${t}"`).join(', ')}]`,
      '---',
    ].filter(Boolean).join('\n');
  }

  // Jekyll (default)
  return [
    '---',
    'layout: post',
    `title: "${article.title.replace(/"/g, '\\"')}"`,
    `date: ${date} 09:00:00 +0000`,
    `description: "${article.description.replace(/"/g, '\\"')}"`,
    article.cover_image ? `image: "${article.cover_image}"` : '',
    `tags: [${article.tags.join(', ')}]`,
    article.canonical_url ? `canonical_url: "${article.canonical_url}"` : '',
    '---',
  ].filter(Boolean).join('\n');
}

module.exports = { publish };
