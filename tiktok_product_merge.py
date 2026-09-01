#!/usr/bin/env python3
"""
tiktok_product_merge.py — merge newly-scraped TikTok Seller Center Compass
product-level daily data into WIBWUB_Dashboard.html's embedded TK_PROD_DATA
const (powers the "สินค้าที่ขายได้" section on the TikTok Shop tab).

INPUT
-----
A JSON file (path passed as argv[1], defaults to tiktok_product_daily_new.json
in the same folder as this script) shaped like:

{
  "2026-09-01": [
    {
      "pid": "1731731059674744388",
      "name": "ทิชชู่เปียก... (WIBWUB Refresh Leather Wipes)",
      "gmv": 30218.36,
      "orders": 285,
      "sku_orders": 285,
      "items_sold": 288,
      "self_live": 303.51,
      "self_video": 172.2,
      "affiliate": 28370.93,
      "affiliate_live": 0,
      "affiliate_video": 26562.83,
      "product_card": 1371.72
    },
    ...
  ],
  "2026-09-02": [ ... ]
}

This is the exact schema produced by the browser-side capture of the
`/api/v3/insights/seller/ttp/product/list` endpoint (no anti-bot signature
required for this endpoint, unlike the SKU/variant-level v2 endpoint).

WHAT THIS SCRIPT DOES
----------------------
1. Loads the existing `const TK_PROD_DATA = {...};` object out of
   WIBWUB_Dashboard.html (dates / names / daily).
2. Merges in the new date(s): appends any new dates to `dates` (kept sorted),
   adds any new product ids to `names`, and adds/overwrites `daily[date]`
   rows for each date present in the input file.
3. Re-serializes TK_PROD_DATA compactly (same array-based row format used by
   the dashboard's tkpAggregate()/tkpRender() JS, i.e.
   [pid, gmv, orders, sku_orders, items_sold, self_live, self_video,
    affiliate, affiliate_live, affiliate_video, product_card]) and writes it
   back into the HTML file via a regex replace of the `const TK_PROD_DATA = ...;`
   statement — mirrors the `_replace_const()` pattern used by update_stock.py
   for the Procurement Dashboard's PRODUCTS/HIST_* consts.
4. Never deletes existing dates — this script is additive/overwrite-per-date
   only, so re-running it for a date you already have simply refreshes that
   date's numbers (useful if TikTok's own reporting is revised a day or two
   later, which does happen).

USAGE
-----
    python3 tiktok_product_merge.py /path/to/tiktok_product_daily_new.json

After running, validate with `node --check` on the dashboard's <script>
blocks (see the checklist at the bottom of this file's companion skill),
then commit WIBWUB_Dashboard.html and remind the user to run push_now.command
on their real machine (git push from this sandbox always fails — proxy 403).
"""
import json
import re
import sys
import os
import subprocess
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DASHBOARD = os.path.join(HERE, "WIBWUB_Dashboard.html")


def load_dashboard_tk_prod_data(html):
    m = re.search(r"const TK_PROD_DATA = (\{.*?\});\n", html, re.S)
    if not m:
        raise RuntimeError("Could not find `const TK_PROD_DATA = {...};` in WIBWUB_Dashboard.html — "
                            "has the สินค้าที่ขายได้ section been removed or renamed?")
    return json.loads(m.group(1)), m.span(1)


def row_from_record(rec):
    r = lambda x: round(x, 2) if isinstance(x, float) else x
    return [
        rec["pid"],
        r(rec.get("gmv", 0)),
        rec.get("orders", 0),
        rec.get("sku_orders", 0),
        rec.get("items_sold", 0),
        r(rec.get("self_live", 0)),
        r(rec.get("self_video", 0)),
        r(rec.get("affiliate", 0)),
        r(rec.get("affiliate_live", 0)),
        r(rec.get("affiliate_video", 0)),
        r(rec.get("product_card", 0)),
    ]


def merge(existing, new_data):
    dates = set(existing["dates"])
    names = dict(existing["names"])
    daily = dict(existing["daily"])

    for date, records in new_data.items():
        dates.add(date)
        rows = []
        for rec in records:
            pid = rec["pid"]
            if rec.get("name"):
                names[pid] = rec["name"]
            rows.append(row_from_record(rec))
        daily[date] = rows

    return {
        "dates": sorted(dates),
        "names": names,
        "daily": daily,
    }


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "tiktok_product_daily_new.json")
    if not os.path.exists(input_path):
        print(f"ERROR: input file not found: {input_path}")
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        new_data = json.load(f)

    with open(DASHBOARD, encoding="utf-8") as f:
        html = f.read()

    existing, span = load_dashboard_tk_prod_data(html)
    merged = merge(existing, new_data)

    before_dates = len(existing["dates"])
    after_dates = len(merged["dates"])
    print(f"dates before: {before_dates}, after: {after_dates}, new/updated: {sorted(new_data.keys())}")

    merged_json = json.dumps(merged, ensure_ascii=False, separators=(",", ":"))
    new_html = html[:span[0]] + merged_json + html[span[1]:]

    with open(DASHBOARD, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"Wrote {DASHBOARD} ({len(new_html)} bytes)")

    # Auto-commit (dashboard file only — mirrors update_stock.py convention)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        subprocess.run(["git", "add", "WIBWUB_Dashboard.html"], cwd=HERE, check=True)
        subprocess.run(
            ["git", "-c", f"user.name=WIBWUB Bot", "-c", "user.email=marketingwibwub@gmail.com",
             "commit", "-m", f"auto: update TikTok product sales data {ts}"],
            cwd=HERE, check=True,
        )
        print("Committed. Run push_now.command on your real machine to push (sandbox push always fails).")
    except subprocess.CalledProcessError as e:
        print(f"git commit skipped/failed (may be nothing to commit): {e}")


if __name__ == "__main__":
    main()
