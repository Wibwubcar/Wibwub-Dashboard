# WIBWUB Weekly Update — 28 กรกฎาคม 2569 (2026-07-28)

Automated run of the `wibwub-monday-update` scheduled task. Summary below.

## 1. Shipnity sales data — ✅ done

- Downloaded fresh month-to-date export (`Data_28-07-2026.xlsx`, 28,786 rows, July 1–28) into `Data Shipnity/`, and copied to the canonical `Data_กรกฎาคม.xlsx`.
- Recomputed the Top 15 products (`ALL_PRODUCTS` and `PROD_MO` in `WIBWUB_Mobile.html`, and the Top Products KPI cards/table in `WIBWUB_Dashboard.html`) using `ราคา × จำนวน` per line item with dedup on `(รหัสสินค้า, เลขที่ออเดอร์, วันที่สร้าง, ราคา, จำนวน)`.
- Validated against the prior Jul(1–27) baseline: all 15 products showed 0.03%–3.9% growth for the single extra day — no anomalies.
- Quantity (`q`) was updated precisely by computing the July 27→28 delta directly from the full dataset (not estimated) and adding it to the existing cumulative totals.
- New grand total: **฿54.64M / 212,160 pcs** (was ฿54.54M / 211,985 pcs).
- Ranking order of the 15 products is unchanged.
- Note: the per-channel breakdown columns in the `WIBWUB_Dashboard.html` table (Shopee/TikTok/Lazada/etc.) still reflect data through 26 ก.ค. only — this was already the case before this run and requires a separate channel-level recomputation that wasn't in scope today. The table footnote was updated to reflect this.

### Caught during processing: SKU mapping bug
Initially mapped both `SRFX000003` (Reflex 250ml) and `SRFX110003` (Reflex 500ml) to the single "Reflex Ceramic Coating" line, which produced a false +124% jump. Confirmed via per-SKU breakdown that `SRFX110003` is a separate, untracked variant and excluded it. Corrected figures show a sane +2.6% for Reflex.

## 2. TikTok Affiliate data — ⚠️ blocked, no data lost

- The Transaction Analysis export attempted 5+ times (fresh export + retrying already-queued ones, including a full page reload). Every attempt failed.
- Root cause confirmed via network inspection: the actual download endpoint (`GET .../export_task/export?...task_id=...`) returned **503 Service Unavailable** consistently across different task IDs — a genuine TikTok-side outage, not a UI issue.
- No data was actually lost: TikTok's affiliate analytics only update through a fixed lag date ("อัปเดตเมื่อ: 26 ก.ค. 2026") regardless of when the export is run, and the already-committed data in `WIBWUB_Affiliate_Dashboard.html` / `WIBWUB_Mobile.html` already covers that full range (Jul 1–26). Nothing to update this run.

## 3. Cache version — ✅ done

- `sw.js` bumped `wibwub-v482` → `wibwub-v483` (v482 had already been committed by a separate automation earlier today).

## 4. Git commit — ⚠️ staged, but not committed

- All three files (`WIBWUB_Mobile.html`, `WIBWUB_Dashboard.html`, `sw.js`) are edited, saved to disk, and successfully **staged** (`git add` succeeded) — diffs are sane (51 insertions / 51 deletions across the three files, all attributable to the changes above).
- `git commit` itself could not complete: `.git/index.lock` was held almost continuously across ~10 retry attempts over several minutes by what appears to be a **different automation running concurrently** against the same repo (the lock kept reappearing with a fresh timestamp right after being cleared, and recent commit history shows other same-day automated commits landing in real time, e.g. `0d50355`, `9eab647`, `b4b358b`). Forcibly removing an active lock risked corrupting that other process's commit, so I backed off rather than force it. Ran `git fsck` to confirm the repo itself is not corrupted — clean aside from unrelated pre-existing dangling objects.
- **Current state**: changes are staged in the index (`git status` shows `M` for all three files) but HEAD is unchanged. **Action needed**: once the concurrent automation finishes, simply run `git commit -m "auto-update: Monday update 2026-07-28 — Top Products from Shipnity Jul(1-28) full-month export; sw.js v483"` (no need to re-add) to finish the commit. `push_now.command` was left as-is since it's push-only and unaffected by this.

## Files changed (uncommitted)
- `WIBWUB_Mobile.html` — `ALL_PRODUCTS`, `PROD_MO`
- `WIBWUB_Dashboard.html` — Top Products KPI cards, table, footnote
- `sw.js` — cache version v482 → v483
