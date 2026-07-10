# WIBWUB Affiliate Auto-Update — Report

**Run date:** 22 มิ.ย. 2569 (2026-06-22) · Scheduled task `wibwub-thursday-affiliate`
**Data range:** 1–20 มิ.ย. 2026 (current month → latest available)
**Shop:** TikTok Affiliate Center (shop_id 7494549095358892612, TH)

## Files exported & filed
4 transaction-analysis files for 20260601–20260620 are in their subfolders under `Data Affiliate/`:
- ครีเอเตอร์ → `Transaction_Analysis_Creator_List_20260601-20260620.xlsx`
- สินค้า → `Transaction_Analysis_Product_List_20260601-20260620.xlsx`
- วีดีโอ → `Transaction_Analysis_Video_List_20260601-20260620.xlsx`
- ไลฟ์สตรีม → `Transaction_Analysis_Live_List_20260601-20260620.xlsx`

## June (1–20) creator aggregates — verified from the export
- Total GMV: **฿375,789**
- Returns: ฿6,709 → **Net GMV ฿369,080**
- Commission: **฿46,005**
- Creators with GMV > 0: **274** · Active (GMV ≥ ฿1K): **53** · total rows 517

## Dashboard edits applied
- `WIBWUB_Affiliate_Dashboard.html`
  - PRODUCTS → "WIBWUB Refresh Leather Wipes" cr/vid `0/0` → **`1/3`** (only product still out of sync)
  - Header badge date `1–17 มิ.ย.` → **`1–20 มิ.ย.`**
- `sw.js` cache version `wibwub-v217` → **`wibwub-v218`**
- `push_now.command` commit message refreshed (sw v218)

## Already in sync (no change needed)
An earlier run today had already synced this same 1–20 dataset, so most values matched on arrival:
- Mobile `AFI_GMV/AFI_NET/AFI_COMM` index for June already = 375789 / 369080 / 46005
- Mobile KPI already "274 creators · มิย.69"
- 6 of 7 PRODUCTS cr/vid already correct; CREATORS array already matched (e.g. .namoshop125 ฿38,544)

## Notes / caveats (transparency)
1. **SKILL.md is partially stale.** The dashboards were restructured: the generic arrays it references (`gmvD/netD/commD/crD`, `AFI_GMV` schema) don't all exist as named. Edits were mapped to the real structures (`CREATORS`, `PRODUCTS`, mobile `AFI_*` arrays) and applied minimally to avoid corrupting a working dashboard.
2. **Cumulative KPIs left as-is.** The top-of-page KPIs (`ครีเอเตอร์ที่ Active 1,168`, GMV ฿2.71M, commission ฿296K) are multi-month cumulative totals, not June-only, so they were intentionally not overwritten with June's 274/53.
3. **Product cr/vid column mapping:** cr = col "ครีเอเตอร์ที่มียอดขายเฉลี่ยรายวัน" (col 9), vid = "วิดีโอ" (col 13) — confirmed against existing dashboard values.
4. **Source files in Downloads not deleted.** The Downloads mount blocks `rm`, so the 4 exports were copied (content-overwrite) into `Data Affiliate/` rather than moved; duplicates remain in Downloads (harmless).

## Next step (manual)
Run `push_now.command` to commit & push (Affiliate dashboard, Mobile, sw.js) so the live PWA picks up cache v218.
