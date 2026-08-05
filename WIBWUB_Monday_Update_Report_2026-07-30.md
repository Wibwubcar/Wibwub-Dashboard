# WIBWUB Weekly Update — 30 กรกฎาคม 2569 (2026-07-30)

Automated run of the `wibwub-monday-update` scheduled task. Summary below.

## 1. Shipnity sales data — ✅ done

- Downloaded fresh month-to-date export (`Data_30-07-2026.xlsx`, July 1–30) into `Data Shipnity/`.
- Recomputed Top 15 products (`ALL_PRODUCTS`/`PROD_MO` in `WIBWUB_Mobile.html`, Top Products KPI/table in `WIBWUB_Dashboard.html`) using `ราคา × จำนวน` per line item, dedup on `(รหัสสินค้า, เลขที่ออเดอร์, วันที่สร้าง, ราคา, จำนวน)`.
- Since `PROD_MO` only stores revenue (not qty) historically, both revenue and quantity were reconstructed exactly (not estimated) by diffing two consecutive snapshots (`Data_28-07-2026.xlsx` vs `Data_30-07-2026.xlsx`) per SKU — unit prices aren't constant per SKU, so estimating qty from revenue was ruled out.
- Validated: reconstructed old (Jul 1–28) totals matched already-committed `PROD_MO[6]` values almost exactly (≤1 baht rounding), and all 15 products showed small, uniform 0.03%–1.88% growth over the 2 extra days — no anomalies.
- New Top 15 total: Wool Duster now ฿5.54M/8,658 pcs (was ฿5.51M/8,610 pcs); full updated figures in both files.
- Scope: only "รวม (฿)"/"จำนวน" columns and the best-seller KPI were updated. Grand-total KPI (still ฿54.64M/212,160 pcs), per-channel breakdown columns, and the "รวมทั้งหมด" footer row were left untouched (still stale at 26 ก.ค.) — same as prior runs, no reliable exact baseline available to recompute those safely.

## 2. TikTok Affiliate data — ⚠️ blocked, no data lost

- TikTok's export/download endpoint (`GET .../export_task/export?...task_id=...`) is in a confirmed, ongoing system-wide **503 outage**, now in its 2nd+ day.
- Confirmed independently by a sister scheduled task (`wibwub-thursday-affiliate`) that ran the same morning: 503s across creator/product tabs, 3 different task_ids, verified via network inspection — not a UI or session-specific issue.
- No data lost: TikTok's affiliate analytics lag date hadn't advanced past what's already committed (through 26–27 ก.ค.), so nothing new was available to pull anyway.
- Skipped without further retries per task guidance ("log and stop" rather than repeatedly retrying a confirmed outage).

## 3. Cache version — ✅ done

- `sw.js` bumped `wibwub-v501` → `wibwub-v502`.

## 4. Git commit — ✅ done

- Encountered `.git/index.lock` contention from a concurrent automation (same pattern as the 28 ก.ค. run — other same-day automated commits were landing in real time, e.g. TikTok followers, stock forecast). Backed off and retried rather than forcing the lock.
- Lock cleared on its own after ~2 minutes; commit succeeded cleanly:
  `09b6776 — auto-update: Monday update 2026-07-30 — Top Products from Shipnity Jul(1-30) full-month export; sw.js v501->v502`
  (3 files changed, 50 insertions / 50 deletions — `WIBWUB_Mobile.html`, `WIBWUB_Dashboard.html`, `sw.js`).
- `push_now.command` was already up to date (push-only script) from a prior automation — left as-is, no changes needed.
- **Note**: push itself was not executed (sandboxed environment cannot push to the remote); the user's `push_now.command` will push this commit along with any others already queued.

## Files changed (committed)
- `WIBWUB_Mobile.html` — `ALL_PRODUCTS`, `PROD_MO`
- `WIBWUB_Dashboard.html` — Top Products KPI card, table, footnote
- `sw.js` — cache version v501 → v502
