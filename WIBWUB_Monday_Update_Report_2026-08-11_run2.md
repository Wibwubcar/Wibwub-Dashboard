# WIBWUB Weekly Update — 2026-08-11 (run 2)

Second automated run of "wibwub-monday-update" today. Unlike the earlier run (see `WIBWUB_Monday_Update_Report_2026-08-11.md`), TikTok Affiliate auth was available this time, so affiliate data was updated. Shipnity's export bug persisted, so Top Products was deliberately skipped rather than guessed.

## Task 1 — M5 protection check
Re-verified `M5` month-label array in `WIBWUB_Dashboard.html` and `WIBWUB_Mobile.html`. Still correct (8 Thai months through August). No fix needed.

## Task 2 — Shipnity purchase export (partial data, used month-to-date-minus-1)
Reproduced the same multi-page export bug documented in the earlier run today (only page 1 of multi-page exports survives; single-file exports hang indefinitely; the 500-rows/file slider only goes up to 1000, not enough to fit ~11 days of orders in one file). Also could not narrow the date picker to "today only" (Aug 11) — the "วันนี้" quick-select and manual day-clicks did not change the displayed range.

Rather than keep fighting the exporter, used the existing complete file `Data Shipnity/Data_10-08-2026.xlsx` (verified cumulative Aug 1–10, 11,619 rows) as the data source for Task 4, explicitly excluding today's partial Aug 11 activity to avoid time-of-day skew.

## Task 3 — TikTok Affiliate export (success)
`affiliate.tiktok.com/insights/transaction-analysis` session was authenticated this run. Exported a custom Aug 1–9 "Transaction Analysis — Creator List" report (took ~220s+ to generate, longer than the UI's stated 60–90s). Downloaded successfully to `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260801-20260809.xlsx` (4,989 rows, 22 columns) — no data loss, unlike Shipnity.

## Task 4 — Top Products update: SKIPPED (by design)
Computed a raw product-name revenue/quantity ranking from `Data_10-08-2026.xlsx`, but stopped short of writing it into `ALL_PRODUCTS` / `PROD_MO` (`WIBWUB_Mobile.html`) or the Top Products chart in `WIBWUB_Dashboard.html`. Two pieces of logic needed to do this safely were not available this run:

1. A reliable mapping from raw Shipnity SKU/product names (e.g. "Sugar (Sugar-500ml+Spray)", "Wool duster-ไม้ปัดขนแกะ") to the 15 polished display names used on the dashboards, including disambiguating multiple size variants of the same product line.
2. The derivation logic for `mk`/`mkq` ("🎯 งบตลาด" marketing-budget submetric) shown alongside each product — not present anywhere in this run's context.

Guessing either would risk writing wrong numbers into a live business dashboard, so per the "stop and log rather than guess" principle, this task was left undone this run. `ALL_PRODUCTS` and `PROD_MO` are unchanged.

**To unblock next run:** either re-supply the name-mapping table / mk-mkq formula (if they exist in an earlier task-file version or a script elsewhere), or explicitly approve a keyword/size-based best-effort mapping with `mk`/`mkq` carried forward unchanged from the prior month.

## Task 5 — Affiliate arrays update (done)
Parsed the Aug 1–9 Transaction Analysis file (`GMV จากครีเอเตอร์`, `การคืนเงิน`, `ค่าคอมมิชชั่นโดยประมาณ` columns). Cross-checked the formula against the existing dashboard's Aug 1–8 snapshot using the prior day's export as a reference (close match), confirming:
- `NET = GMV − Returns`
- Creator count = creators with GMV > 0

Aug 1–9 totals: GMV ฿484,852, Returns ฿10,430, NET ฿474,423, Commission ฿56,606, Creators 321.

Overwrote the last index only (no insert/rebuild) in:
- `WIBWUB_Affiliate_Dashboard.html`: `AF_MO[7]`, `AF_GMV[7]`, `AF_NET[7]`, `AF_COM[7]`, `AF_CR[7]` — label changed "ส.ค. (1-8)" → "ส.ค. (1-9)"
- `WIBWUB_Mobile.html`: `AFI_MONTHS[9]`, `AFI_GMV[9]`, `AFI_NET[9]`, `AFI_COMM[9]` — label changed "สค.69 (1-8)" → "สค.69 (1-9)"

## Task 6 — Cache bump / commit (partial)
Bumped `sw.js` cache version `wibwub-v637` → `wibwub-v638` (file saved).

Git commit was blocked: `.git/index.lock` was present and could not be removed (`Operation not permitted`) across three attempts with waits in between. This is consistent with the earlier same-day report's note that other concurrent scheduled tasks (Shopee zip exports, `push_now.command`, `auto_push.log`) touch this same repo — most likely one of those was mid-operation. Did not force past the lock to avoid corrupting a concurrent process's work. **No commit was made and no `push_now.command` was created this run** — the two edited files (`WIBWUB_Affiliate_Dashboard.html`, `WIBWUB_Mobile.html`) and `sw.js` remain as uncommitted changes on disk alongside other pre-existing uncommitted files from concurrent automations.

**To unblock next run:** commit `WIBWUB_Affiliate_Dashboard.html`, `WIBWUB_Mobile.html`, and `sw.js` (cache v638) once no other automation is mid-git-operation, then push.

## Summary of file changes this run
- `WIBWUB_Affiliate_Dashboard.html` — edited (AF_* arrays, index 7)
- `WIBWUB_Mobile.html` — edited (AFI_* arrays, index 9)
- `sw.js` — edited (cache version v637 → v638)
- `ALL_PRODUCTS` / `PROD_MO` / Top Products chart — **not** edited (see Task 4)
- No git commit / no push_now.command this run (see Task 6)
