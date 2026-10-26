#!/usr/bin/env python3
"""Export a Bing Webmaster baseline for the domain move (Sprint W1, T-W102; reused weekly in W6).

  BING_API_KEY=... python3 scripts/export_bing_baseline.py                  # https://l2cache.amvo.store/
  python3 scripts/export_bing_baseline.py --site https://l2cache.app/       # key read from .env

Bing returns about 6 months of weekly rows. Writes docs/baseline/bing-<site>-<date>-{pages,queries,traffic}.csv.
"""
import argparse
import collections
import csv
import datetime
import json
import os
import re
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://ssl.bing.com/webmaster/api.svc/json"


def api_key():
    key = os.environ.get("BING_API_KEY")
    env = os.path.join(ROOT, ".env")
    if not key and os.path.exists(env):
        for line in open(env, encoding="utf-8"):
            if line.startswith("BING_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
    if not key:
        raise SystemExit("Set BING_API_KEY in the environment or in .env")
    return key


def call(method, site, key):
    qs = urllib.parse.urlencode({"siteUrl": site, "apikey": key})
    with urllib.request.urlopen(f"{API}/{method}?{qs}") as resp:
        data = json.loads(resp.read())
    if "ErrorCode" in data:
        raise SystemExit(f"{method}: {data['Message']}")
    return data["d"]


def date_of(row):
    ms = int(re.search(r"\d+", row["Date"]).group())
    return datetime.date.fromtimestamp(ms / 1000)


def aggregate(rows, field):
    """Sum weekly rows per page/query; position is impression-weighted."""
    acc = collections.defaultdict(lambda: [0, 0, 0.0])
    for r in rows:
        a = acc[r[field]]
        a[0] += r["Clicks"]
        a[1] += r["Impressions"]
        a[2] += max(r["AvgImpressionPosition"], 0) * r["Impressions"]
    return sorted(((k, c, i, round(p / i, 1) if i else "") for k, (c, i, p) in acc.items()), key=lambda x: -x[2])


def write(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="https://l2cache.amvo.store/")
    args = ap.parse_args()
    key = api_key()
    out_dir = os.path.join(ROOT, "docs", "baseline")
    os.makedirs(out_dir, exist_ok=True)
    stem = f"bing-{args.site.replace('https://', '').strip('/')}-{datetime.date.today()}"

    pages = call("GetPageStats", args.site, key)
    queries = call("GetQueryStats", args.site, key)
    traffic = call("GetRankAndTrafficStats", args.site, key)

    write(os.path.join(out_dir, f"{stem}-pages.csv"), ["page", "clicks", "impressions", "position"], aggregate(pages, "Query"))
    write(os.path.join(out_dir, f"{stem}-queries.csv"), ["query", "clicks", "impressions", "position"], aggregate(queries, "Query"))
    write(os.path.join(out_dir, f"{stem}-traffic.csv"), ["date", "clicks", "impressions"],
          sorted((date_of(r), r["Clicks"], r["Impressions"]) for r in traffic))

    dates = [date_of(r) for r in pages + traffic]
    print(f"{args.site}  {min(dates)} → {max(dates)}")
    print(f"  pages {len(set(r['Query'] for r in pages))}  queries {len(set(r['Query'] for r in queries))}  "
          f"clicks {sum(r['Clicks'] for r in traffic)}  impressions {sum(r['Impressions'] for r in traffic)}")


if __name__ == "__main__":
    main()
