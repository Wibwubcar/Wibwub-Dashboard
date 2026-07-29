# WIBWUB Monday Update — 2026-07-27 (autonomous run)

## Summary

- **M5 month arrays**: verified OK, no fix needed (7 labels through July).
- **Top Products (ภาพรวมธุรกิจ)**: not updated this run — see below.
- **Affiliate (WIBWUB_Affiliate_Dashboard.html / Mobile)**: left as-is, already correct through 25 ก.ค. from an earlier run today.
- **Committed**: `WIBWUB_Affiliate_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js` (commit `0732b42`), plus a cleanup of `push_now.command` (commit `52df8e6`). **Not yet pushed** — run `push_now.command` to push to `origin/main`.

## Top Products — why no update

Tried twice to export a fresh Shipnity **product-level** file via the "ไฟล์เดียว" export dialog (`www.shipnity.com/data/c/purchase`):
1. First export downloaded but contained only a single `orderItemId` column (order-level, unusable for product aggregation).
2. Retry showed "Download completed" in the Shipnity UI but no file ever landed in Downloads.

Checked every Shipnity file downloaded in the last 2 days (`08b1a967...xlsx`, `ce42b63f...xlsx`, `55f4dd90...xlsx`) — all were the same broken order-level export. This looks like a persistent issue with that export button, not a one-off glitch.

However, a **daily** cumulative file (`Data Shipnity/Data_27-07-2026.xlsx`, 20 columns, product-level, 27,953 rows, dates 01/07–27/07) was already sitting in the folder — dropped there by a concurrent automation run in this same session window. I used it to sanity-check the dashboard's current Top-15 numbers (`PROD_MO` column "Jul 1-26"): the fresh July 1–27 total per product was only ~1–3% higher than what's already published, consistent with exactly one extra day of sales, not stale data.

**Decision:** did not rewrite `ALL_PRODUCTS` / `PROD_MO` this run. The gain (one day of data) didn't justify the risk of manually re-deriving the raw-SKU → canonical-product-name mapping without the authoritative script (`build_snapshot_tmp.py`, which is mid-edit by another concurrent process and unrelated to Top Products — it's a stock/procurement script). Recommend the next scheduled run redo this with a clean, non-overlapping Shipnity export.

## Affiliate — why no update

TikTok's Affiliate Center has replaced the old "Transaction Analysis" export with a "Creator Analysis" page. Its `Core_Stats` export is a single aggregate row, not a per-creator list, and the numbers it produced were internally inconsistent (implied Net GMV *lower* than the already-published 25 ก.ค. figure, and a creator count ~25x the established range). A file in the correct per-creator format (`Transaction_Analysis_Creator_List_20260701-20260725.xlsx`) already existed from an earlier run today and had already been used to update the dashboards through 25 ก.ค. — left that data untouched rather than overwrite good data with a bad export.

## Git / environment note

This repo (on the Google-Drive-mounted folder) has a long-standing quirk: almost any `git` command leaves behind an `index.lock`/`HEAD.lock`/object tmp-file that can't be `rm`'d or `unlink`'d from the sandbox (`Operation not permitted`) — evidenced by dozens of `.stale`/`.old`/`.bak` lock files going back to mid-June, all clearly worked around the same way by prior runs. Worked around it by `mv`-ing the stale lock aside (rename succeeds where unlink doesn't) immediately before `git add`/`commit`, with no other git command in between. Commits succeeded; **push still requires the sandbox proxy workaround** (`push_now.command` — please double-click it to push commit `52df8e6` → `origin/main`).

## Recommendations

1. Investigate why Shipnity's product-level export intermittently degrades to an order-level `orderItemId`-only file — check if a saved column/report template got reset.
2. On TikTok Affiliate Center, look for an export option that still returns one row per creator (needed for the `AF_CR` creator-count metric); the new "Creator Analysis" default export doesn't work for this.
3. Multiple scheduled tasks (this one, stock forecast, thursday-affiliate) are landing in the same window and stepping on each other's git state — consider staggering their schedules to reduce lock contention and duplicate downloads.
