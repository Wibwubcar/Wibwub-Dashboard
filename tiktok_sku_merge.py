#!/usr/bin/env python3
"""
tiktok_sku_merge.py — merge TikTok Seller Center Compass SKU/variant-level
sales data into WIBWUB_Dashboard.html's embedded TK_PROD_SKU const (powers
the per-variant "↳ SKU" expandable rows under each product in the
"สินค้าที่ขายได้" section, TikTok Shop tab). Consumed by tkpRenderSkuRows(pid)
in the dashboard's JS.

IMPORTANT CAVEAT (documented, not a bug): unlike the product-level endpoint
(/api/v3/insights/seller/ttp/product/list, one row per day), the SKU-level
endpoint (/api/v2/insights/seller/ttp/product/sku/list) does NOT return a
per-day breakdown — a request for date range [start,end] returns ONE
aggregate number per SKU for the whole range (confirmed via direct testing:
single-day ranges, i.e. start===end, fail outright with
{code:98001021,"call downstream server error"}; the backend requires a
genuine multi-day span). So true daily SKU granularity is not obtainable
from this endpoint.

WORKAROUND used here: fetch data in ~7-day chunks, then evenly distribute
each chunk's aggregate gmv/orders/items_sold across every date in that
chunk (divide by day count). This keeps tkpRenderSkuRows' existing
sum-over-selected-dates logic correct when a user selects a whole chunk
(or the full backfilled range), and gives a reasonable smoothed estimate
for partial-week selections. If TikTok ever exposes true daily SKU data,
replace the even-split step with real per-day values.

INPUT
-----
A JSON file shaped like (as produced by the browser-side capture):
{
  "2026-08-01_2026-08-07": [
    {"pid": "...", "sid": "...", "prop": "500 ml", "gmv": 123.45, "orders": 5, "items_sold": 5},
    ...
  ],
  "2026-08-08_2026-08-14": [...],
  ...
}
Each top-level key is a "STARTDATE_ENDDATE" chunk whose values are the
RANGE-AGGREGATE (not daily) SKU stats for that chunk.

OUTPUT
------
Merges into WIBWUB_Dashboard.html's `const TK_PROD_SKU = {...};`, shaped:
{"YYYY-MM-DD": {pid: [{prop, sku_id, gmv, items_sold, orders}, ...]}}
(one entry per date in each chunk, values = chunk aggregate / day count)

USAGE
-----
    python3 tiktok_sku_merge.py /path/to/tk_sku_backfill.json
"""
import json
import re
import sys
import os
import subprocess
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
DASHBOARD = os.path.join(HERE, "WIBWUB_Dashboard.html")


def load_dashboard_tk_prod_sku(html):
    m = re.search(r"const TK_PROD_SKU = (\{.*?\});", html, re.S)
    if not m:
        raise RuntimeError("Could not find `const TK_PROD_SKU = {...};` in WIBWUB_Dashboard.html — "
                            "has the ตาม SKU section been removed or renamed?")
    return json.loads(m.group(1)) if m.group(1).strip() != "{}" else {}, m.span(1)


def dates_in_chunk(start, end):
    s = datetime.strptime(start, "%Y-%m-%d")
    e = datetime.strptime(end, "%Y-%m-%d")
    out = []
    d = s
    while d <= e:
        out.append(d.strftime("%Y-%m-%d"))
        d += timedelta(days=1)
    return out


def row_from_record(rec, n_days):
    r = lambda x: round(x / n_days, 2) if isinstance(x, (int, float)) else x
    return {
        "prop": rec.get("prop") or rec.get("sid", ""),
        "sku_id": rec.get("sid", ""),
        "gmv": r(rec.get("gmv", 0)),
        "items_sold": r(rec.get("items_sold", 0)),
        "orders": r(rec.get("orders", 0)),
    }


def merge(existing, chunks):
    daily = dict(existing)
    for chunk_key, records in chunks.items():
        start, end = chunk_key.split("_")
        ds = dates_in_chunk(start, end)
        n_days = len(ds)
        by_pid = {}
        for rec in records:
            pid = rec["pid"]
            by_pid.setdefault(pid, []).append(row_from_record(rec, n_days))
        for d in ds:
            daily[d] = by_pid
    return daily


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "tk_sku_backfill.json")
    if not os.path.exists(input_path):
        print(f"ERROR: input file not found: {input_path}")
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        chunks = json.load(f)

    with open(DASHBOARD, encoding="utf-8") as f:
        html = f.read()

    existing, span = load_dashboard_tk_prod_sku(html)
    merged = merge(existing, chunks)

    print(f"dates before: {len(existing)}, after: {len(merged)}, chunks merged: {sorted(chunks.keys())}")

    merged_json = json.dumps(merged, ensure_ascii=False, separators=(",", ":"))
    new_html = html[:span[0]] + merged_json + html[span[1]:]

    with open(DASHBOARD, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"Wrote {DASHBOARD} ({len(new_html)} bytes)")

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        subprocess.run(["git", "add", "WIBWUB_Dashboard.html"], cwd=HERE, check=True)
        subprocess.run(
            ["git", "-c", "user.name=WIBWUB Bot", "-c", "user.email=marketingwibwub@gmail.com",
             "commit", "-m", f"auto: backfill TikTok SKU-level sales data {ts}"],
            cwd=HERE, check=True,
        )
        print("Committed. Run push_now.command on your real machine to push (sandbox push always fails).")
    except subprocess.CalledProcessError as e:
        print(f"git commit skipped/failed (may be nothing to commit): {e}")


if __name__ == "__main__":
    main()
