async function publish(article, config) {
  const apiKey = process.env.DEVTO_API_KEY;
  if (!apiKey) throw new Error('DEVTO_API_KEY not set in .env');

  const body = {
    article: {
      title:          article.title,
      body_markdown:  article.body_markdown,
      published:      config.published ?? false,
      description:    article.description || undefined,
      tags:           article.tags.slice(0, 4).map(t => String(t).toLowerCase().replace(/[^a-z0-9]/g, '')),
      series:         config.series || undefined,
      organization_id: config.organization_id || undefined,
      canonical_url:  article.canonical_url || undefined,
      main_image:     article.cover_image || undefined,
    },
  };

  // Strip undefined fields
  Object.keys(body.article).forEach(k => body.article[k] === undefined && delete body.article[k]);

  const res = await fetch('https://dev.to/api/articles', {
    method: 'POST',
    headers: { 'api-key': apiKey, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  const data = await res.json();
  if (!res.ok) throw new Error(data.error || data.message || JSON.stringify(data));

  return { url: data.url };
}

module.exports = { publish };
