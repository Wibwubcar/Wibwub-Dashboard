# WIBWUB Affiliate Auto-Update — Report

**Run date:** 23 มิ.ย. 2569 (2026-06-23) · Scheduled task `wibwub-thursday-affiliate`
**Data range:** 1–22 มิ.ย. 2026 (current month → latest available date)
**Shop:** TikTok Affiliate Center (shop_id 7494549095358892612, TH)

## Files exported & filed
4 transaction-analysis files for 20260601–20260622 are in their subfolders under `Data Affiliate/`:
- ครีเอเตอร์ → `Transaction_Analysis_Creator_List_20260601-20260622 (1).xlsx`
- สินค้า → `Transaction_Analysis_Product_List_20260601-20260622 (1).xlsx`
- วีดีโอ → `Transaction_Analysis_Video_List_20260601-20260622.xlsx`
- ไลฟ์สตรีม → `Transaction_Analysis_Live_List_20260601-20260622.xlsx`

## June (1–22) creator aggregates — verified from the export
- Total GMV: **฿413,513**
- Net GMV (after returns): **฿406,204**
- Commission: **฿51,145**
- Creators with GMV > 0: **297** · Active (GMV ≥ ฿1K): **60** · total rows 554

## Dashboard edits applied
- `WIBWUB_Mobile.html` — `AFI_GMV/AFI_NET/AFI_COMM` June (index 7) = **413513 / 406204 / 51145**; home KPI card **฿2.75M · 297 creators · มิย.69** (cumulative GMV + current creator count)
- `WIBWUB_Affiliate_Dashboard.html` — CREATORS data + note refreshed to **60 active (GMV ≥ ฿1K), Total GMV ฿413.5K — มิ.ย. 1–22, 2026**; header badge **1–20 → 1–22 มิ.ย. 2569 · อัปเดต 23 มิ.ย.** (badge was the one item left stale by the mid-day commit; fixed this run)
- `sw.js` cache version **wibwub-v233 → wibwub-v234** (so the live PWA picks up the badge fix)
- `push_now.command` commit message refreshed (sw v234)

## Already in sync (no change needed)
The bulk of this 1–22 dataset was already applied and committed earlier today (commit `a651969`, 12:07). On arrival the AFI arrays, mobile KPI, CREATORS array, and most PRODUCTS values already matched the export — so this run only reconciled the remaining stale header badge and bumped the cache.

## Notes / caveats (transparency)
1. **PRODUCTS cr/vid and GMV are cumulative multi-month totals**, not June-only (e.g. Leather Wipes gmv ฿571K vs June ฿~). They were left as the committed cumulative values rather than overwritten with single-month figures from the export, which would have understated them.
2. **Top-of-page / home KPIs are cumulative** (Affiliate GMV ฿2.75M). Intentionally not replaced with June's ฿413.5K; only the creator count (297) and month label track the latest export.
3. **SKILL array names partially stale.** The Affiliate Dashboard has no `gmvD/netD/commD/crD` arrays; edits were mapped to the real structures (`CREATORS`, `PRODUCTS`, mobile `AFI_*`).
4. **Source files in Downloads not deleted.** The Downloads mount blocks `rm`, so exports were copied into `Data Affiliate/` rather than moved; harmless duplicates remain in Downloads.

## Next step (manual)
Run `push_now.command` to commit & push (Affiliate dashboard, Mobile, sw.js) so the live PWA refreshes to cache **v234**.
