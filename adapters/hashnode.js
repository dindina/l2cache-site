async function publish(article, config) {
  const token = process.env.HASHNODE_TOKEN;
  if (!token) throw new Error('HASHNODE_TOKEN not set in .env');

  const publicationId = config.publication_id || process.env.HASHNODE_PUBLICATION_ID;
  if (!publicationId) throw new Error('publication_id not set in frontmatter or HASHNODE_PUBLICATION_ID in .env');

  const mutation = `
    mutation PublishPost($input: PublishPostInput!) {
      publishPost(input: $input) {
        post { id url }
      }
    }
  `;

  const input = {
    title:           article.title,
    contentMarkdown: article.body_markdown,
    publicationId,
    isDraft:         config.draft ?? true,
    tags:            article.tags.slice(0, 5).map(t => ({ name: String(t) })),
  };

  if (article.cover_image) {
    input.coverImageOptions = { coverImageURL: article.cover_image };
  }
  if (article.canonical_url) {
    input.originalArticleURL = article.canonical_url;
  }

  const res = await fetch('https://gql.hashnode.com', {
    method: 'POST',
    headers: { 'Authorization': token, 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: mutation, variables: { input } }),
  });

  const raw = await res.text();
  if (!res.ok || raw.trim().startsWith('<')) {
    throw new Error(`Hashnode returned HTTP ${res.status}. Response: ${raw.slice(0, 200)}`);
  }
  const data = JSON.parse(raw);
  if (data.errors) throw new Error(data.errors.map(e => e.message).join(', '));

  const post = data.data?.publishPost?.post;
  return { url: post?.url || 'saved as draft — check your Hashnode dashboard' };
}

module.exports = { publish };
