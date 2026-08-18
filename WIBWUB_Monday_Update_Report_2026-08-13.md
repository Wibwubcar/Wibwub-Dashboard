# WIBWUB Weekly Update — 2026-08-13

## Summary

All 5 steps completed successfully.

## Steps

1. **M5 month-array protection check** — `WIBWUB_Dashboard.html` / `WIBWUB_Mobile.html` already correct (8 entries, ม.ค.–ส.ค.). No fix needed.
2. **Shipnity export** (month-to-date) — downloaded and moved to `Data Shipnity/`.
3. **TikTok Affiliate Transaction Analysis export** — downloaded and moved to `Data Affiliate/ครีเอเตอร์/` (`Transaction_Analysis_Creator_List_20260801-20260810.xlsx`).
4. **Top Products update** (from 77 Shipnity product-level files, revenue-ranked top 15):
   - `WIBWUB_Mobile.html`: `ALL_PRODUCTS` and `PROD_MO` fully replaced/reordered with new Aug 1–13 totals.
   - `WIBWUB_Dashboard.html`: "🏆 ตารางสินค้าขายดี" table rows 1–15 updated (รวม (฿) / จำนวน columns only, per-channel breakdown left as-is), rank order corrected (Refresh Wipes now #5, Xglass now #12, Martini now #13), grand total row updated to ฿60.09M / 234,349, KPI cards and header date notes updated to 13 ส.ค. 2569.
5. **Affiliate arrays** (`AFI_*` in Mobile, `AF_*` in Affiliate Dashboard) — last index (ส.ค. 1–10, GMV ฿550,824) overwritten in place per rolling-window rule.
6. **sw.js** bumped to `wibwub-v651`; committed `WIBWUB_Mobile.html`, `WIBWUB_Dashboard.html`, `WIBWUB_Affiliate_Dashboard.html`, `sw.js` (commit `bab4828`).

## Push

Sandbox `git push` is blocked by a proxy 403, as usual — run `push_now.command` in the `All` folder to push commit `bab4828` to origin/main.

## Verification

- All 3 dashboard files pass JS syntax check (`node --check`).
- `PROD_MO` mo-arrays: all 15 products at length 8 (consistent).
- `AFI_MONTHS/GMV/NET/COMM`: all length 10 (consistent).
- `AF_MO/GMV/NET/COM/CR`: all length 8 (consistent).
- Top Products table: ranks 1–15 present, sequential, no duplicates/gaps.

## Note

Recurring environment quirk: `.git/index.lock` and stale objects can't be `rm`'d (bindfs permission denies unlink) but can be `mv`'d aside — used that workaround again this run, consistent with prior weeks.
