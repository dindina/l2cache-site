#!/usr/bin/env python3
"""Export a Search Console baseline for the domain move (Sprint W1, T-W102; reused weekly in W6).

  python3 scripts/export_gsc_baseline.py                       # sc-domain:l2cache.amvo.store, last 16 months
  python3 scripts/export_gsc_baseline.py --site sc-domain:l2cache.app --days 28

Writes docs/baseline/gsc-<site>-<date>-pages.csv (complete per-page totals) and
docs/baseline/gsc-<site>-<date>-queries.csv (page x query x country; Google omits rare queries).
"""
import argparse
import csv
import datetime
import json
import os
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from fetch_gsc_stats import get_access_token  # noqa: E402  (reuses the service-account login)

PAGE_SIZE = 25000


def query_all(token, site, start, end, dimensions):
    url = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(site, safe='')}/searchAnalytics/query"
    rows, start_row = [], 0
    while True:
        body = {"startDate": start, "endDate": end, "dimensions": dimensions,
                "rowLimit": PAGE_SIZE, "startRow": start_row, "dataState": "final"}
        req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                     headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            batch = json.loads(resp.read()).get("rows", [])
        rows += batch
        if len(batch) < PAGE_SIZE:
            return rows
        start_row += PAGE_SIZE


def write(path, dimensions, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(dimensions + ["clicks", "impressions", "ctr", "position"])
        for r in sorted(rows, key=lambda r: -r["impressions"]):
            w.writerow(r["keys"] + [r["clicks"], r["impressions"], round(r["ctr"], 4), round(r["position"], 1)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="sc-domain:l2cache.amvo.store")
    ap.add_argument("--days", type=int, default=486, help="Search Console keeps about 16 months")
    args = ap.parse_args()

    end = datetime.date.today() - datetime.timedelta(days=3)  # final data lags ~2-3 days
    start = end - datetime.timedelta(days=args.days)
    token = get_access_token()
    out_dir = os.path.join(ROOT, "docs", "baseline")
    os.makedirs(out_dir, exist_ok=True)
    stem = f"gsc-{args.site.replace('sc-domain:', '').replace('https://', '').strip('/')}-{datetime.date.today()}"

    pages = query_all(token, args.site, str(start), str(end), ["page"])
    write(os.path.join(out_dir, f"{stem}-pages.csv"), ["page"], pages)
    queries = query_all(token, args.site, str(start), str(end), ["page", "query", "country"])
    write(os.path.join(out_dir, f"{stem}-queries.csv"), ["page", "query", "country"], queries)

    print(f"{args.site}  {start} → {end}")
    print(f"  pages:   {len(pages):>6} rows  clicks {sum(r['clicks'] for r in pages):>6.0f}  impressions {sum(r['impressions'] for r in pages):>8.0f}")
    print(f"  queries: {len(queries):>6} rows")


if __name__ == "__main__":
    main()
