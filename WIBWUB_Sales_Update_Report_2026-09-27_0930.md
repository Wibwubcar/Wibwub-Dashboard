# WIBWUB Sales Sheet Update — 2026-09-27 (scheduled run, จันทร์+พฤหัส 09:30)

## STEP 0 protection check
`M5` / data arrays: 9 = 9 in both `WIBWUB_Dashboard.html` and `WIBWUB_Mobile.html` (ม.ค.–ก.ย. 2569,
index 8 = กันยายน). No mismatch, no month pushed blindly. ✅

## Sheets checked (Google Drive modifiedTime, compared against last synced run)

| Platform | fileId | modifiedTime (Drive) | Same as last sync (2026-09-26 run)? |
|---|---|---|---|
| Shopee (ส่งเสริมการขาย Shopee) | 19P7945wP4mQI0zzWA3qgFsEFOd1VQOLctLfSM0TJMos | 2026-09-21T02:44:53Z | Yes — unchanged |
| TikTok (ส่งเสริมการขายTIKTOK.xlsx) | 1k22c3PGY6aQjygAX6df_rQLR8aTzL-iz | 2026-09-24T07:48:51Z | Yes — unchanged |
| Lazada (ส่งเสริมการขาย Lazada) | 1x8bbjZxgoQe6bT4s1_S8W2A9EONsI4bl4d4znwq9t7E | 2026-09-21T02:47:44Z | Yes — unchanged |

Verified directly against the "ยอดรายเดือน" tab last row of each workbook (full xlsx export +
openpyxl for Shopee/TikTok; full NL read for Lazada — all three unchanged since yesterday):
- Shopee last row `01-20/09/26`: revenue 4,802,418 / fee 1,438,804.43 / orders 8,456 / cancel% 5.48
- TikTok last row `01-23/09/26`: net revenue 2,472,808.19
- Lazada last row (Sep, day ~20): revenue 85,324.24 / ads 6,490 / fee 15,069.19 / coupon 1,980 / cost% 27.59

All match `SH_REV[8]`, `SH_FEE[8]`, `SH_ORD[8]`, `SH_CANCEL_PCT[8]`, `TK_REV[8]`, `LZ_REV[8]`,
`LZ_ADS[8]`, `LZ_FEE[8]`, `LZ_COUPON[8]`, `LZ_COST_PCT[8]` already in both
`WIBWUB_Dashboard.html` and `WIBWUB_Mobile.html` byte-for-byte.

## Outcome
**No new data — skipped commit**, per task rule ("ข้อมูลเดือนนี้ไม่เปลี่ยนแปลงจากครั้งก่อน → log
'No new data' และ skip commit"). No files edited, no git commit made, sw.js not bumped.

## ⚠️ Recurring flag — source sheets stale for 6+ days (unresolved, 3rd consecutive run)
- Shopee & Lazada "ยอดรายเดือน" sheets: last edited **2026-09-21** — now **6 days** with no update.
- TikTok sheet: last edited **2026-09-24** — now **3 days** behind.
- Flagged in the 2026-09-25 and 2026-09-26 run reports too, still not resolved. Whoever normally
  updates these three sheets daily appears to have stopped for a week — the WIBWUB Dashboard/Mobile
  sales pages have been stuck on the 20/23 กันยายน cumulative numbers since then, missing ~1 week
  of actual September sales.
