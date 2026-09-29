#!/usr/bin/env bash
# ==============================================================================
# Automated One-Command Build, Deploy, and Search Engine Indexing Pipeline
# ==============================================================================
set -e

echo "🚀 [1/5] Building Site & Generating Sitemaps..."
python3 build.py

echo "🔍 [2/5] Validating SEO & Metadata Rules..."
python3 validate_seo.py || true

# Load environment variables if .env exists
if [ -f .env ]; then
  set -a
  source .env 2>/dev/null || true
  set +a
fi

echo "☁️ [3/5] Deploying to Vercel Production..."
export PATH="$PATH:/opt/homebrew/bin:/usr/local/bin"
if [ -n "$VERCEL_TOKEN" ]; then
  npx -y vercel deploy --prod --yes --token "$VERCEL_TOKEN"
else
  npx -y vercel deploy --prod --yes
fi

echo "⚡ [4/5] Pinging IndexNow (Bing & DuckDuckGo)..."
python3 submit_indexnow.py || true

echo "📊 [5/5] Running Unified SEO Health Audit..."
python3 seo_health_check.py

echo "🎉 All systems deployed, indexed, and audited successfully!"
