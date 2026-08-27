#!/usr/bin/env python3
"""
fastmoss_update.py — WIBWUB vs. competitor FastMoss snapshot updater.

WHY THIS SCRIPT EXISTS
-----------------------
fastmoss.com shop pages are heavily client-rendered (JavaScript SPA) and
login-gated, so they cannot be scraped with plain HTTP requests. Every run
requires an agent step (Claude in Chrome) to actually open the page and
read the numbers. This script is the *second half* of that process: once
the numbers have been read off the page for a given date, this script
merges them into the history file and regenerates the dashboard HTML so
the two never drift out of sync.

WORKFLOW (used by the scheduled task, and by any manual re-run):
  1. Navigate to each shop's FastMoss URL via Claude in Chrome.
  2. Read the cumulative header stats AND scroll to "แนวโน้มข้อมูล" (Data
     Trends) to read the genuine 28-day windowed stats. THESE ARE TWO
     DIFFERENT NUMBER SETS ON THE SAME PAGE — do not substitute one for
     the other (see note below).
  3. Write a snapshot JSON (see SNAPSHOT SCHEMA) to a temp file.
  4. Run: python3 fastmoss_update.py --snapshot /path/to/snapshot.json
  5. Run: node --check on the extracted <script> block (see validation
     note at bottom of this file) before trusting the output.
  6. git add + commit (this script does that part automatically).
  7. Remind the user to double-click push_now.command on their real Mac
     (git push from this sandbox always fails with a 403 proxy error —
     that is expected, not a bug).

IMPORTANT GOTCHA — cumulative vs. 28-day trend
------------------------------------------------
FastMoss shop pages show TWO distinct classes of numbers:
  (a) top profile/header stat cards = ALL-TIME CUMULATIVE totals
      (e.g. total orders ever, total videos ever posted by tagged
      creators, etc.)
  (b) the "แนวโน้มข้อมูล" (Data Trends) section further down the page,
      which has its own 7/28/90/180-day tab selector and an explicit
      date-range display (e.g. "2026-07-30 -> 2026-08-26").
Only (b) is a genuine 28-day trend. A prior run of this workflow
accidentally reported WIBWUB's cumulative header numbers (2.0k lives,
6.5k videos, 2.2k creators) as if they were 28-day figures, which would
have made WIBWUB vs. munwow comparisons apples-to-oranges. Always pull
trend28d fields from the Data Trends section, never from the header.

SNAPSHOT SCHEMA (what --snapshot should contain)
--------------------------------------------------
{
  "date": "YYYY-MM-DD",
  "shops": {
    "wibwub": {
      "cumulative": {"orders_total":.., "sales_total":.., "products_active":..,
                      "products_total":.., "country_rank":.., "category_rank":..,
                      "rating":.., "overall_good_pct":.., "quality_score":..,
                      "response_rate_24h":.., "shipping_rate_48h":..},
      "trend28d": {"range":"YYYY-MM-DD → YYYY-MM-DD", "orders":.., "sales":..,
                   "creators":.., "lives":.., "videos":.., "products_sold":..},
      "top_products": [{"name":.., "orders":.., "sales":..}, ...]   // top 5
    },
    "munwow": { ... same shape ... }
  }
}
Any shop key present in fastmoss_history.json's "shops" metadata block can
appear here (not just wibwub/munwow) — adding a third competitor later is
just adding a new entry to the "shops" metadata block plus its data here.

Re-running with the same "date" for a shop OVERWRITES that shop's entry
for that date (idempotent) rather than creating a duplicate — safe to
re-run if a scrape needs correcting.

MONTHLY DATA — history["monthly_history"] (added 2026-08-27)
--------------------------------------------------------------
In addition to the daily/weekly "history" snapshots above (used for the
all-time cumulative + 28-day trend comparison), there is a separate
"monthly_history" list that powers the Channel Performance Dashboard's
month-tab filtering. Each entry:
{
  "month": "YYYY-MM",
  "shops": {
    "wibwub": {
      "orders": ..,           # accurate calendar-month sum
      "sales": ..,            # accurate calendar-month sum
      "creators_new": ..,     # NEW creators added to FastMoss's all-time
      "videos_new": ..,       #   counter this month — NOT the same metric
      "lives_new": ..,        #   as trend28d.creators/videos/lives (which
                               #   is "active in a rolling 28-day window").
                               #   Never conflate the two in the UI.
      "days_in_period": ..,   # how many calendar days of data went into
                               #   this month's sum (useful for flagging a
                               #   still-in-progress current month)
      "cumulative_eom": {"date":.., "orders_total":.., "sales_total":..,
                         "creators_total":.., "videos_total":..,
                         "lives_total":..}   # end-of-month all-time totals
    },
    "munwow": { ... same shape ... }
  }
}
Note: there is deliberately NO "products_sold" field per month — FastMoss's
export has no daily/monthly breakdown for that metric, only the single
latest 28-day trend value (trend28d.products_sold). Do not fabricate a
monthly figure for it; keep showing the trend28d value with a caveat in
month-filtered views instead.

HOW TO REFRESH monthly_history (used by upsert_monthly_snapshot below):
  1. On FastMoss, open each shop's page, go to "แนวโน้มข้อมูล", select the
     "180 days" preset + "ดูตาราง" (table) view, and use the export icon to
     download the full daily delta table as xlsx (covers ~180 days back
     from today in one file — plenty to backfill/refresh recent months).
  2. Parse the daily delta columns (orders/sales are directly additive;
     creators/videos/lives use the "increase" columns, which are new-adds
     to the all-time counter, see note above) and group by calendar month.
  3. Build a snapshot dict shaped like MONTHLY_SNAPSHOT SCHEMA below and
     pass it via --monthly-snapshot.

MONTHLY_SNAPSHOT SCHEMA (what --monthly-snapshot should contain)
--------------------------------------------------------------
{
  "months": [
    {"month": "YYYY-MM", "shops": {"wibwub": {...}, "munwow": {...}}},
    ...
  ]
}
Each shop entry must match the monthly_history shop shape above. Re-running
with the same "month" for a shop OVERWRITES that shop's entry for that
month (idempotent upsert, same pattern as upsert_snapshot).
"""
import json
import re
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent
HISTORY_PATH = BASE / "fastmoss_history.json"
DASHBOARD_PATH = BASE / "WIBWUB_FastMoss_Competitor_Dashboard.html"

DATA_MARKER_START = "const FASTMOSS_DATA = "
DATA_MARKER_END = ";\n/*FASTMOSS_DATA_END*/"


def load_history():
    with open(HISTORY_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_history(data):
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def upsert_snapshot(history, snapshot):
    date = snapshot["date"]
    entry = None
    for h in history["history"]:
        if h["date"] == date:
            entry = h
            break
    if entry is None:
        entry = {"date": date, "shops": {}}
        history["history"].append(entry)
        history["history"].sort(key=lambda h: h["date"])
    for shop_key, shop_data in snapshot["shops"].items():
        if shop_key not in history["shops"]:
            raise ValueError(
                f"Unknown shop key '{shop_key}' — add it to the top-level "
                f"'shops' metadata block in fastmoss_history.json first "
                f"(name, fastmoss_id, url, category, price_range, "
                f"listed_since, color)."
            )
        entry["shops"][shop_key] = shop_data
    return history


def upsert_monthly_snapshot(history, monthly_snapshot):
    """Merge a --monthly-snapshot payload into history['monthly_history'].

    Mirrors upsert_snapshot()'s idempotent-upsert-by-key pattern, but keyed
    by "month" (YYYY-MM) instead of "date", and stored in a separate list
    so it never collides with the daily/weekly 'history' snapshots.
    """
    history.setdefault("monthly_history", [])
    for month_data in monthly_snapshot["months"]:
        month = month_data["month"]
        entry = None
        for h in history["monthly_history"]:
            if h["month"] == month:
                entry = h
                break
        if entry is None:
            entry = {"month": month, "shops": {}}
            history["monthly_history"].append(entry)
            history["monthly_history"].sort(key=lambda h: h["month"])
        for shop_key, shop_data in month_data["shops"].items():
            if shop_key not in history["shops"]:
                raise ValueError(
                    f"Unknown shop key '{shop_key}' — add it to the top-level "
                    f"'shops' metadata block in fastmoss_history.json first "
                    f"(name, fastmoss_id, url, category, price_range, "
                    f"listed_since, color)."
                )
            entry["shops"][shop_key] = shop_data
    return history


def regen_html(history):
    html = DASHBOARD_PATH.read_text(encoding="utf-8")
    payload = json.dumps(history, ensure_ascii=False, indent=2)
    pattern = re.compile(
        re.escape(DATA_MARKER_START) + r".*?" + re.escape(DATA_MARKER_END),
        re.DOTALL,
    )
    new_block = DATA_MARKER_START + payload + DATA_MARKER_END
    if not pattern.search(html):
        raise RuntimeError(
            "Could not find FASTMOSS_DATA marker block in dashboard HTML — "
            "has the template changed? Look for 'const FASTMOSS_DATA = ' "
            "and '/*FASTMOSS_DATA_END*/' in the <script> section."
        )
    html = pattern.sub(new_block, html, count=1)
    # Bump the "last generated" footer timestamp so the dashboard visibly
    # reflects when it was last regenerated.
    now_label = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = re.sub(
        r'(<span id="gen-ts">).*?(</span>)',
        lambda m: m.group(1) + now_label + m.group(2),
        html,
        count=1,
    )
    DASHBOARD_PATH.write_text(html, encoding="utf-8")


def git_commit():
    subprocess.run(["git", "add", str(DASHBOARD_PATH), str(HISTORY_PATH)], cwd=BASE, check=False)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    subprocess.run(
        [
            "git",
            "-c", "user.name=WIBWUB Bot",
            "-c", "user.email=marketingwibwub@gmail.com",
            "commit",
            "-m", f"auto: update FastMoss competitor snapshot {ts}",
        ],
        cwd=BASE,
        check=False,
    )
    # Sandbox git push always fails (proxy 403) — that's expected. The real
    # push happens via push_now.command on the user's own machine.
    subprocess.run(["git", "push", "origin", "main"], cwd=BASE, check=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", help="Path to a snapshot JSON to merge in")
    ap.add_argument(
        "--monthly-snapshot",
        help="Path to a MONTHLY_SNAPSHOT JSON (see module docstring) to merge "
        "into history['monthly_history']. Can be combined with --snapshot "
        "in the same run.",
    )
    ap.add_argument(
        "--regen-only",
        action="store_true",
        help="Skip merging a new snapshot, just rebuild the HTML from the "
        "existing fastmoss_history.json (useful after hand-editing the JSON)",
    )
    ap.add_argument(
        "--no-commit",
        action="store_true",
        help="Skip the git add/commit/push step",
    )
    args = ap.parse_args()

    history = load_history()

    if not args.regen_only:
        if not args.snapshot and not args.monthly_snapshot:
            raise SystemExit(
                "Provide --snapshot <path> and/or --monthly-snapshot <path>, "
                "or use --regen-only"
            )
        if args.snapshot:
            with open(args.snapshot, encoding="utf-8") as f:
                snapshot = json.load(f)
            history = upsert_snapshot(history, snapshot)
        if args.monthly_snapshot:
            with open(args.monthly_snapshot, encoding="utf-8") as f:
                monthly_snapshot = json.load(f)
            history = upsert_monthly_snapshot(history, monthly_snapshot)
        save_history(history)

    regen_html(history)
    print(f"Regenerated {DASHBOARD_PATH.name} from {HISTORY_PATH.name}")

    if not args.no_commit:
        git_commit()
        print("Committed. Remember: double-click push_now.command on your Mac to actually push.")


if __name__ == "__main__":
    main()
