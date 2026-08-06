# WIBWUB Sales Sheet Update — 2026-08-06 09:30

## Result: no new sales data — but found and fixed a re-introduced M5 array bug

## Sheet check (last cumulative row per platform, ยอดประจำปี tables)

| แหล่ง | เดือนล่าสุดที่มีข้อมูล | ยอดขาย | Ads | ค่าธรรมเนียม/คอมมิชชั่น | order |
|---|---|---|---|---|---|
| Shopee | 01-31/07/26 | 5,923,704 | 942,122.40 | 1,774,741.72 | 10,511 (cancel 5.34%) |
| Lazada | 01-31/07/26 | 95,770.98 | 9,710 | 16,914.09 | cost% 30.99 |
| TikTok | 01-31/07/26 | 2,089,005.47 | 508,456.37 | 613,482.79 | — |

**No August 2026 row exists in any of the 3 sheets** — confirmed directly for Shopee/Lazada, and for
TikTok via a subagent that opened the workbook and searched every tab for any `/08/26` date pattern
(zero matches). July 31 remains the latest closed month everywhere.

## Bug found (STEP 0)

`M5` in both `WIBWUB_Dashboard.html` and `WIBWUB_Mobile.html` had **8 elements** (`ม.ค.`…`ก.ค.`, plus a
stray `ส.ค.`), while `SH_REV`/`TK_REV`/`LZ_REV`/`MONTH_LABELS_FULL`/`MONTH_LABELS_SHORT`/`MP_MONTH_BOUNDS`
all had 7. This is the exact bug class the STEP 0 protection rule exists to catch — a previous run (after
the 2026-08-03 fix noted in the 08-04 report) re-added the "ส.ค." label to `M5` without adding real August
data anywhere else.

Since no sheet has August data yet, the fix was to **remove the stray "ส.ค." from `M5`** in both files
(not add August data elsewhere) — restoring all arrays to 7 matching elements. Verified all related arrays
(`M5`, `SH_REV`, `TK_REV`, `LZ_REV`, `FB_REV`, `LINE_REV`, `WEB_REV`, `SH_ORD`, `TK_ORD`, `LZ_ORD`,
`FB_ORD`, `LINE_ORD`, `MONTH_LABELS_FULL`, `MONTH_LABELS_SHORT`) now all report count=7 in both files.

Also confirmed: index 6 (July) already equals the sheet totals above exactly, `rangeEnd=6`, and header
already reads "ม.ค. – ก.ค. 2569" — no further array/KPI/date-picker edits needed.

## Committed

- Bumped `sw.js` cache version v571 → v572
- Committed `WIBWUB_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js` as `4bd3c2a`
- Created `push_now.command` — **run this to push to the live site** (sandbox can't push directly, HTTP 403 via proxy)

## Summary
- Shopee, Lazada, TikTok: still no August 2026 data as of today (Aug 6).
- Fixed a recurring M5/data-array length mismatch bug before it could break the latest-month chart.
- Next run should watch for this same M5 bug recurring, and re-check once August entries appear in the sheets.
