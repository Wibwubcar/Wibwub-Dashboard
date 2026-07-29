# WIBWUB Monday Update — 2026-07-27 (autonomous run, retry #2)

## Summary

- **Top Products (ภาพรวมธุรกิจ)**: updated successfully this run, using a clean Shipnity product-level export and an incremental-delta method (see below). This closes the gap left open by the earlier same-day run (`WIBWUB_Monday_Update_Report_2026-07-27.md`), which had skipped this step.
- **Affiliate (WIBWUB_Affiliate_Dashboard.html / Mobile)**: left untouched again. TikTok's Affiliate Center Creator Analysis export is confirmed (13th documented attempt, across runs) to only produce a single-row `Core_Stats` aggregate, never a per-creator list — a real platform limitation, not a fluke. No changes made.
- **M5 month-label array**: verified OK (7 entries, matches July = month 7), no fix needed.
- **sw.js**: cache version bumped `wibwub-v478` → `wibwub-v479`.
- **Committed**: `WIBWUB_Mobile.html`, `WIBWUB_Dashboard.html`, `sw.js` → commit `32088a8`. `push_now.command` regenerated → commit `98dc8c9`. **Not yet pushed** — sandbox proxy blocks direct push/fetch (`403 from proxy`, confirmed again this run); please double-click `push_now.command` to push to `origin/main`.

## Top Products — what was done

1. Confirmed `Data Shipnity/Data_27-07-2026.xlsx` (auto-placed by the `com.wibwub.download-mover` LaunchAgent after the Chrome export completed) is genuine **product-level** data: has `รหัสสินค้า` (SKU) and `สินค้า` (product name) columns, 28,414 rows, dates 01/07–27/07/2026.
2. Validated methodology: raw `สินค้า`-name aggregation (sum of price×qty) for Jul 1–26 reconciles with the dashboard's existing published canonical `PROD_MO`/`ALL_PRODUCTS` figures within 0.04%–1.5% for all 15 top products — close enough to trust for computing a one-day delta.
3. Computed the Jul 27 delta per product (revenue + qty) from the raw export and added it on top of the existing trusted Jul 1–26 baseline, rather than re-deriving the full canonical mapping from scratch (avoids the SKU-mapping risk that caused the earlier run to skip this).
4. Updated `WIBWUB_Mobile.html`: `ALL_PRODUCTS` (`v`, `q`) and `PROD_MO` (`mo[6]`, Jul) for 14 of 15 products (Refresh Wipes had zero Jul 27 sales, left unchanged). `mk`/`mkq` (marketing budget) fields left unchanged — not derivable from this export.
5. Updated `WIBWUB_Dashboard.html`: KPI cards (`฿54.32M`→`฿54.54M`, date range → 27 ก.ค., qty `8,591`→`8,606`, `210K`→`212K`), each of the 15 product table rows' "รวม (฿)"/"จำนวน" columns, and the "รวมทั้งหมด" grand-total row (`฿54.32M`/`211,099` → `฿54.54M`/`211,985`) — using the true whole-catalog delta (all products, not just top 15) for the grand total.

**Deliberately NOT updated** (documented in-file via a footnote): the per-channel breakdown columns (Shopee/TikTok/Lazada/Facebook/etc.) in the product table, the `pr_top10` bar chart, and the `pr_channel` doughnut chart — these are asterisked in the dashboard as "15 สินค้าขายดีที่สุดเท่านั้น" (top-15-only) and require channel-level attribution that wasn't recomputed this run for risk/complexity reasons. They still reflect data through 26 ก.ค.

## Affiliate — why still no update

Same conclusion as the earlier run today: TikTok Affiliate Center's "Creator Analysis" export only returns `Core_Stats_...` (single aggregate row), never a per-creator list needed for `AF_CR`. Checked the export-history panel (13 entries) — all Core_Stats. This is a platform limitation, not transient. Left `AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR` and `AFI_*` untouched; they remain correct through 25 ก.ค. from an earlier run.

Note: `WIBWUB_Affiliate_Dashboard.html` shows as modified in `git status` from a **different, concurrent** automation process — not from this run. Deliberately excluded from this run's commit since the changes weren't reviewed/understood here.

## Git / push

- Commit `32088a8`: `WIBWUB_Mobile.html`, `WIBWUB_Dashboard.html`, `sw.js` (Top Products delta + sw.js v479).
- Commit `98dc8c9`: regenerated `push_now.command` to be **push-only** (no `git add`/`git commit` inside it) — the previous version of the script would have blindly committed `WIBWUB_Affiliate_Dashboard.html` under a stale message, which risked committing another process's unreviewed changes. It now just clears stale locks and runs `git push origin main`.
- Confirmed via `git fetch origin main` that the sandbox cannot reach GitHub directly (`403 from proxy`) — push must be done by the user via `push_now.command`.
- Excluded from this run's commits (belong to other concurrent automations, left as-is): `WIBWUB_Affiliate_Dashboard.html`, `build_snapshot_tmp.py`, `data content/Followers_wibwubcar.zip`, `scripts/auto_push.log`, various untracked report `.md`/data export files.

## Action needed

Double-click `push_now.command` in the `All` folder to push commits `32088a8` and `98dc8c9` (and any other already-committed work from concurrent runs) to `origin/main`.

## Recommendations (carried over)

1. Investigate TikTok Affiliate Center for any export option that still returns one row per creator — the current default doesn't support `AF_CR`.
2. Consider staggering scheduled tasks (Monday update, stock forecast, thursday-affiliate, sales-from-sheets, TikTok followers) — several are landing in the same window and stepping on each other's git state / Downloads folder.
3. Next run: continue using the incremental-delta method validated here for Top Products; consider extending it to per-channel breakdowns if a reliable channel-aggregation approach is worked out.
