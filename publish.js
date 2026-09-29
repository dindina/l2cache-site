require('dotenv').config();
const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

const ADAPTERS = {
  devto:        './adapters/devto.js',
  hashnode:     './adapters/hashnode.js',
  github_pages: './adapters/github_pages.js',
  linkedin:     './adapters/linkedin.js',
  twitter_x:    './adapters/twitter_x.js',
};

async function publish(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  const { data: fm, content } = matter(raw);

  if (!fm.title) throw new Error('Article missing required frontmatter: title');
  if (!fm.publish_to) throw new Error('Article missing required frontmatter: publish_to');

  const isDryRun = process.argv.includes('--dry-run');
  const onlyFlag = process.argv.find(a => a.startsWith('--only='));
  const skipFlag = process.argv.find(a => a.startsWith('--skip='));
  const only = onlyFlag ? onlyFlag.split('=')[1].split(',') : null;
  const skip = skipFlag ? skipFlag.split('=')[1].split(',') : [];

  const article = {
    title:        fm.title,
    description:  fm.description || '',
    tags:         fm.tags || [],
    body_markdown: content.trim(),
    cover_image:  fm.cover_image || '',
    canonical_url: fm.canonical_url || '',
    slug: path.basename(filePath, '.md').replace(/_/g, '-'),
  };

  const globalDraft = process.env.DEFAULT_DRAFT !== 'false';

  console.log(`\n📄 Publishing: ${article.title}`);
  console.log(`   Slug: ${article.slug}`);
  if (isDryRun) console.log('   Mode: DRY RUN (no API calls)\n');
  else console.log('   Mode: LIVE (draft on each platform)\n');

  const tasks = Object.entries(fm.publish_to)
    .filter(([platform, config]) => {
      if (!config || !config.enabled) return false;
      if (only && !only.includes(platform)) return false;
      if (skip.includes(platform)) return false;
      if (!ADAPTERS[platform]) { console.warn(`⚠️  No adapter for "${platform}" — skipping`); return false; }
      return true;
    })
    .map(async ([platform, config]) => {
      if (isDryRun) {
        console.log(`🔍 [dry-run] ${platform}: would publish "${article.title}"`);
        return { platform, success: true, url: '(dry-run)' };
      }
      try {
        const mergedConfig = { draft: globalDraft, published: !globalDraft, ...config };
        const adapter = require(ADAPTERS[platform]);
        const result = await adapter.publish(article, mergedConfig);
        console.log(`✅ ${platform}: ${result.url}`);
        return { platform, success: true, ...result };
      } catch (err) {
        console.error(`❌ ${platform}: ${err.message}`);
        return { platform, success: false, error: err.message };
      }
    });

  const results = await Promise.all(tasks);

  console.log('\n── Summary ─────────────────────────────────');
  results.forEach(r => {
    const icon = r.success ? '✅' : '❌';
    const detail = r.success ? (r.url || 'ok') : r.error;
    console.log(`${icon} ${r.platform.padEnd(14)} ${detail}`);
  });
  console.log('─────────────────────────────────────────────\n');

  return results;
}

const filePath = process.argv.find(a => a.endsWith('.md'));
if (!filePath) {
  console.error('Usage: node publish.js <article.md> [--dry-run] [--only=devto,hashnode] [--skip=github_pages]');
  process.exit(1);
}

publish(path.resolve(filePath)).then(results => {
  if (results.some(r => !r.success)) process.exit(1);
}).catch(err => {
  console.error('Fatal:', err.message);
  process.exit(1);
});
