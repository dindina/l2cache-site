#!/usr/bin/env python3
"""
Unified SEO Health & Ranking Monitor for L2Cache (Google Search Console + Bing Webmaster Tools + IndexNow)
"""

import json
import time
import urllib.request
import urllib.parse
import datetime
import os
import sys
import jwt

# Configuration
GSC_KEY_PATH = "/Users/dinesh/tech/astute-veld-398216-29207275aa29.json"
GSC_SITE_PROPERTY = "sc-domain:l2cache.amvo.store"
BING_API_KEY = "7d11b0d9c9aa45f49582910889750fc4"
BING_SITE_URL = "https://l2cache.amvo.store/"

def get_gsc_token():
    if not os.path.exists(GSC_KEY_PATH):
        return None
    with open(GSC_KEY_PATH) as f:
        key_data = json.load(f)
    client_email = key_data["client_email"]
    private_key = key_data["private_key"]
    token_uri = key_data.get("token_uri", "https://oauth2.googleapis.com/token")
    now = int(time.time())
    payload = {
        "iss": client_email,
        "scope": "https://www.googleapis.com/auth/webmasters https://www.googleapis.com/auth/webmasters.readonly",
        "aud": token_uri,
        "exp": now + 3600,
        "iat": now
    }
    signed_jwt = jwt.encode(payload, private_key, algorithm="RS256")
    token_req = urllib.request.Request(
        token_uri,
        data=urllib.parse.urlencode({
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": signed_jwt
        }).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    with urllib.request.urlopen(token_req) as resp:
        return json.loads(resp.read().decode()).get("access_token")

def check_bing():
    print("=" * 70)
    print("📊 BING WEBMASTER TOOLS HEALTH & STATS")
    print("=" * 70)
    
    # 1. Check Registered Site
    site_api = f"https://ssl.bing.com/webmaster/api.svc/json/GetUserSites?apikey={BING_API_KEY}"
    try:
        with urllib.request.urlopen(urllib.request.Request(site_api)) as resp:
            sites = json.loads(resp.read().decode()).get("d", [])
            print(f"✓ Connected to Bing Webmaster ({len(sites)} site registered)")
    except Exception as e:
        print(f"✗ Bing connection error: {e}")
        return

    # 2. Check Sitemaps
    sitemap_api = f"https://ssl.bing.com/webmaster/api.svc/json/GetFeeds?siteUrl={urllib.parse.quote(BING_SITE_URL)}&apikey={BING_API_KEY}"
    try:
        with urllib.request.urlopen(urllib.request.Request(sitemap_api)) as resp:
            feeds = json.loads(resp.read().decode()).get("d", [])
            for f in feeds:
                print(f"  - Sitemap: {f.get('Url')} | Status: {f.get('Status')} | Last Crawled: {f.get('LastCrawled', 'Pending')}")
    except Exception as e:
        print(f"✗ Sitemap check error: {e}")

    # 3. Check Submission Quotas
    quota_api = f"https://ssl.bing.com/webmaster/api.svc/json/GetUrlSubmissionQuota?siteUrl={urllib.parse.quote(BING_SITE_URL)}&apikey={BING_API_KEY}"
    try:
        with urllib.request.urlopen(urllib.request.Request(quota_api)) as resp:
            quota = json.loads(resp.read().decode()).get("d", {})
            print(f"  - Daily URL Quota Remaining: {quota.get('DailyQuota', 0)} | Monthly: {quota.get('MonthlyQuota', 0)}")
    except Exception as e:
        pass

    # 4. Search Query Performance
    query_api = f"https://ssl.bing.com/webmaster/api.svc/json/GetQueryStats?siteUrl={urllib.parse.quote(BING_SITE_URL)}&apikey={BING_API_KEY}"
    try:
        with urllib.request.urlopen(urllib.request.Request(query_api)) as resp:
            queries = json.loads(resp.read().decode()).get("d", [])
            if queries:
                print(f"\nTop Queries on Bing ({len(queries)}):")
                for q in queries[:10]:
                    print(f"  - \"{q.get('Query')}\" | Clicks: {q.get('Clicks', 0)} | Impressions: {q.get('Impressions', 0)} | Pos: {q.get('AvgPosition', 0):.1f}")
            else:
                print("  - Query stats: Accumulating initial ranking data from active crawls.")
    except Exception as e:
        pass
    print()

def check_gsc():
    print("=" * 70)
    print("📊 GOOGLE SEARCH CONSOLE HEALTH & STATS")
    print("=" * 70)
    token = get_gsc_token()
    if not token:
        print("✗ GSC credentials not available.")
        return
        
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    encoded_site = urllib.parse.quote(GSC_SITE_PROPERTY, safe="")
    
    # 1. Sitemaps
    sitemap_url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/sitemaps"
    try:
        with urllib.request.urlopen(urllib.request.Request(sitemap_url, headers=headers)) as resp:
            sitemaps = json.loads(resp.read().decode()).get("sitemap", [])
            print(f"✓ GSC Connected ({len(sitemaps)} sitemaps registered):")
            for sm in sitemaps:
                print(f"  - {sm.get('path')} | Submitted: {sm.get('lastSubmitted', '')[:10]} | Errors: {sm.get('errors', 0)}")
    except Exception as e:
        print(f"✗ GSC sitemap error: {e}")

    # 2. Performance (Last 30 days)
    today = datetime.date.today()
    start_date = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    analytics_url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/searchAnalytics/query"
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query", "page"],
        "rowLimit": 15
    }

    try:
        req = urllib.request.Request(analytics_url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req) as resp:
            rows = json.loads(resp.read().decode()).get("rows", [])
            print(f"\nTop Ranking Queries on Google ({len(rows)} detected):")
            print(f"  {'Query':<30} | {'Impressions':<11} | {'Clicks':<6} | {'Avg Pos':<7} | Landing Page")
            print("  " + "-" * 85)
            for r in rows:
                keys = r.get("keys", ["", ""])
                query = keys[0]
                page = keys[1].replace("https://l2cache.amvo.store", "")
                clicks = r.get("clicks", 0)
                impressions = r.get("impressions", 0)
                pos = f"{r.get('position', 0):.1f}"
                print(f"  {query[:30]:<30} | {impressions:<11} | {clicks:<6} | {pos:<7} | {page}")
    except Exception as e:
        print(f"✗ GSC Analytics error: {e}")
    print()

def main():
    print("\n🔍 RUNNING AUTOMATED SEO HEALTH & RANKING AUDIT...")
    print(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    check_bing()
    check_gsc()
    print("=" * 70)
    print("✅ SEO Health Audit Complete.")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
