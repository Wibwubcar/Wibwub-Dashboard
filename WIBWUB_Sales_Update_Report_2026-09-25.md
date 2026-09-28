# WIBWUB Sales Sheet Update — 2026-09-25 (จันทร์+พฤหัส 09:30 run)

## STEP 0 protection check
`M5` / `MONTH_LABELS_FULL` / `MONTH_LABELS_SHORT` / `MP_MONTH_BOUNDS` and every `SH_/TK_/LZ_` data
array: **9 = 9** in both `WIBWUB_Dashboard.html` and `WIBWUB_Mobile.html` (ม.ค.–ก.ย. 2569, index 8 =
กันยายน). No mismatch, no month pushed blindly. ✅

## Sheets checked (row สุดท้ายของแต่ละเดือน — เดือน ก.ย. 2569)

Read via Google Drive MCP as full xlsx export (all tabs) and parsed with openpyxl to get the exact
last cumulative row per platform's "ยอดรายเดือน" sheet.

| Platform | Sheet's last modified (Drive) | Sheet's latest cumulative row | Dashboard's current values (index 8) | Result |
|---|---|---|---|---|
| Shopee | 2026-09-21 02:44 | `01-20/09/26` — ยอดขาย 4,802,418 / order 8,456 / cancel 5.4754% / fee 1,438,804.43 | Already 4,802,418 / 8,456 / 5.48 / 1,438,804.43 | **No change** |
| Lazada | 2026-09-21 02:47 | `01-20/09/26` — ยอดขาย 85,324.24 / ads 6,490 / fee 15,069.19 / coupon 1,980 / cost% 27.588% | Already 85,324.24 / 6,490 / 15,069.19 / 1,980 / 27.59 | **No change** |
| TikTok | 2026-09-24 07:48 | `01-23/09/26` — Rev 2,472,808.19 / Ads 26,233.92 (Afi-ads col) / Net 2,439,538.62 / Afi% 62.431% | Already matches exactly (TK_REV[8]=2,472,808.19) | **No change** |

`SH_REV`/`SH_ORD`/`SH_CANCEL_PCT`/`SH_FEE`, `LZ_REV`/`LZ_ADS`/`LZ_FEE`/`LZ_COUPON`/`LZ_COST_PCT`,
and `TK_REV` all match byte-for-byte between `WIBWUB_Dashboard.html` and `WIBWUB_Mobile.html`
(Mobile uses `SH_CANCEL` in place of `SH_CANCEL_PCT`, and doesn't carry `LZ_FEE`/`LZ_COUPON` at all
— that's the existing, intentional structure, not something this run touched).

**Note:** `SH_ADS[8]` (893,761.02) is intentionally not sourced from this sheet — it's maintained by
the separate Shopee Ads download job (per prior run notes) and was not touched or compared here.

## ⚠️ Flag: source sheets have been stuck for several days

- Shopee & Lazada's "ยอดรายเดือน" tabs have not been edited since **2026-09-21** — still sitting on
  the `01-20/09/26` row that was already synced 5 days ago (last actual update was in the
  2026-09-21 run2 pass). Today is the 25th, so ~5 days of September Shopee/Lazada sales are missing
  from the sheet itself (not just the dashboard).
- TikTok's sheet was touched on 2026-09-24 but its usable cumulative row still only reaches
  `01-23/09/26` — 2 days behind.
- This has now shown up as "no new data" across multiple consecutive scheduled runs (09-22, and now
  09-25). Whoever updates these sheets daily may have stopped, or the update habit has shifted to
  a different cadence — worth a nudge to the team.

## Files
No edits made to `WIBWUB_Dashboard.html`, `WIBWUB_Mobile.html`, or `sw.js` this run — `git status`
confirms these three are untouched by this run (unrelated staged changes from an earlier TikTok Ads
sync task remain pending in the repo, not modified or committed by this run).

## Date picker (STEP 3B)
Not touched — no new month was added (still ม.ค.–ก.ย., index 8).

## Git commit / push
**Skipped** — per the task's error-handling rule ("ข้อมูลเดือนนี้ไม่เปลี่ยนแปลงจากครั้งก่อน → log
'No new data' และ skip commit"). No sales-array changes to commit this run.

## Outcome
**No new data.** Sales dashboards remain current only through 20 ก.ย. (Shopee/Lazada) and 23 ก.ย.
(TikTok) 2569 — the source sheets themselves haven't been updated past those dates.
