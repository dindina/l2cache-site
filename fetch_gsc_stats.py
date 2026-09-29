#!/usr/bin/env python3
"""
Fetch live performance metrics & top queries from Google Search Console using the Service Account.
"""

import json
import time
import urllib.request
import urllib.parse
import datetime
import os
import sys
import jwt

CREDENTIALS_PATH = "/Users/dinesh/tech/astute-veld-398216-29207275aa29.json"
SITE_PROPERTY = "sc-domain:l2cache.amvo.store"

def get_access_token():
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"Error: Credentials file not found at {CREDENTIALS_PATH}")
        sys.exit(1)
        
    with open(CREDENTIALS_PATH) as f:
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

def query_gsc(days=30, row_limit=50):
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    encoded_site = urllib.parse.quote(SITE_PROPERTY, safe="")
    
    today = datetime.date.today()
    start_date = (today - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/searchAnalytics/query"
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query", "page"],
        "rowLimit": row_limit
    }

    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            rows = data.get("rows", [])
            print(f"=== GOOGLE SEARCH CONSOLE PERFORMANCE ({start_date} to {end_date}) ===")
            print(f"Total Ranking Queries: {len(rows)}\n")
            print(f"{'Query':<35} | {'Impressions':<11} | {'Clicks':<6} | {'CTR':<6} | {'Avg Pos':<7} | Landing Page")
            print("-" * 120)
            for r in rows:
                keys = r.get("keys", ["", ""])
                query = keys[0]
                page = keys[1].replace("https://l2cache.amvo.store", "")
                clicks = r.get("clicks", 0)
                impressions = r.get("impressions", 0)
                ctr = f"{r.get('ctr', 0) * 100:.1f}%"
                pos = f"{r.get('position', 0):.1f}"
                print(f"{query[:35]:<35} | {impressions:<11} | {clicks:<6} | {ctr:<6} | {pos:<7} | {page}")
    except Exception as e:
        print("GSC query failed:", e)

if __name__ == "__main__":
    query_gsc()
