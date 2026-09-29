#!/usr/bin/env python3
"""
Submit site URLs to IndexNow for immediate indexing on Microsoft Bing, DuckDuckGo, Seznam, and Yandex.
"""

import urllib.request
import json
import xml.etree.ElementTree as ET
import os
import sys

INDEXNOW_KEY = "f429f476aace450d98d63642289564df"

SITES = [
    {
        "host": "l2cache.amvo.store",
        "sitemap": "out/l2cache/sitemap.xml" if os.path.exists("out/l2cache/sitemap.xml") else "sitemap.xml",
        "key_location": f"https://l2cache.amvo.store/{INDEXNOW_KEY}.txt"
    },
    {
        "host": "hingejoy.amvo.store",
        "sitemap": "out/hingejoy/sitemap.xml" if os.path.exists("out/hingejoy/sitemap.xml") else "hingejoy/sitemap.xml",
        "key_location": f"https://hingejoy.amvo.store/{INDEXNOW_KEY}.txt"
    }
]

ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow"
]

def extract_urls_from_sitemap(sitemap_file):
    if not os.path.exists(sitemap_file):
        print(f"Error: Sitemap not found at {sitemap_file}")
        return []
    
    tree = ET.parse(sitemap_file)
    root = tree.getroot()
    
    # Handle XML namespaces
    namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = []
    
    for url_tag in root.findall('ns:url', namespaces):
        loc = url_tag.find('ns:loc', namespaces)
        if loc is not None and loc.text:
            urls.append(loc.text.strip())
            
    # Fallback if no namespace matched
    if not urls:
        for loc in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            if loc.text:
                urls.append(loc.text.strip())
                
    return urls

def submit_to_indexnow(host, key_location, urls):
    if not urls:
        print(f"No URLs to submit for {host}.")
        return False
        
    print(f"\nSubmitting {len(urls)} URLs to IndexNow for {host}...")
    
    payload = {
        "host": host,
        "key": INDEXNOW_KEY,
        "keyLocation": key_location,
        "urlList": urls
    }
    
    data = json.dumps(payload).encode('utf-8')
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "AmvoStore-IndexNow-Bot/1.0"
    }
    
    success = True
    for endpoint in ENDPOINTS:
        req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req) as response:
                status = response.status
                print(f"✓ [{host}] Submitted to {endpoint} (HTTP {status})")
        except urllib.error.HTTPError as e:
            print(f"✗ [{host}] HTTP Error {e.code} on {endpoint}: {e.read().decode('utf-8', errors='ignore')}")
            success = False
        except Exception as e:
            print(f"✗ [{host}] Request failed for {endpoint}: {e}")
            success = False
            
    return success

if __name__ == "__main__":
    if len(sys.argv) > 1:
        custom_sitemap = sys.argv[1]
        urls = extract_urls_from_sitemap(custom_sitemap)
        host = "hingejoy.amvo.store" if "hingejoy" in custom_sitemap else "l2cache.amvo.store"
        key_loc = f"https://{host}/{INDEXNOW_KEY}.txt"
        submit_to_indexnow(host, key_loc, urls)
    else:
        for site_info in SITES:
            urls = extract_urls_from_sitemap(site_info["sitemap"])
            print(f"Loaded {len(urls)} URLs from {site_info['sitemap']} ({site_info['host']})")
            for u in urls[:5]:
                print(f"  - {u}")
            if len(urls) > 5:
                print(f"  ... and {len(urls) - 5} more")
            submit_to_indexnow(site_info["host"], site_info["key_location"], urls)

