# WIBWUB Sales Sheet Update — 2026-09-27 19:33 ICT (evening re-check)

## STEP 0 protection check
`M5` / data arrays: 9 = 9 in both `WIBWUB_Dashboard.html` and `WIBWUB_Mobile.html` (ม.ค.–ก.ย. 2569,
index 8 = กันยายน). No mismatch, no month pushed blindly. ✅

## Sheets checked (Google Drive modifiedTime)

| Platform | fileId | modifiedTime (Drive) | Days stale |
|---|---|---|---|
| Shopee (ส่งเสริมการขาย Shopee) | 19P7945wP4mQI0zzWA3qgFsEFOd1VQOLctLfSM0TJMos | 2026-09-21T02:44:53Z | 6 days |
| TikTok (ส่งเสริมการขายTIKTOK.xlsx) | 1k22c3PGY6aQjygAX6df_rQLR8aTzL-iz | 2026-09-24T07:48:51Z | 3 days |
| Lazada (ส่งเสริมการขาย Lazada) | 1x8bbjZxgoQe6bT4s1_S8W2A9EONsI4bl4d4znwq9t7E | 2026-09-21T02:47:44Z | 6 days |

Verified via full xlsx export + openpyxl (Shopee, TikTok) and NL read (Lazada — xlsx export timed
out on the 12.5MB file), last row of "ยอดรายเดือน" tab, all unchanged vs. this morning's 09:30 run
and vs. what's already live in WIBWUB_Dashboard.html / WIBWUB_Mobile.html:
- Shopee last row `01-20/09/26`: revenue 4,802,418 / fee 1,438,804.43 / orders 8,456 / cancel% 5.48
- TikTok last row `01-23/09/26`: net revenue 2,472,808.19 / ads 2,439,538.62
- Lazada last row (Sep, ~day 20): revenue 85,324.24 / ads 6,490 / fee 15,069.19 / coupon 1,980 / cost% 27.59

All match SH_REV[8]/SH_FEE[8]/SH_ORD[8]/SH_CANCEL_PCT[8]/TK_REV[8]/LZ_REV[8]/LZ_ADS[8]/LZ_FEE[8]/
LZ_COUPON[8]/LZ_COST_PCT[8] already in both dashboard files byte-for-byte.

## Outcome
**No new data — skipped commit.** No files edited, no git commit made, sw.js not bumped.

## ⚠️ Recurring flag — source sheets stale for 6+ days (unresolved, 4th consecutive run)
Flagged in the 2026-09-25, 2026-09-26, and 2026-09-27 09:30 run reports already — still not
resolved as of this evening re-check. Shopee & Lazada sheets haven't been touched since
**21 กันยายน** (6 days), TikTok since **24 กันยายน** (3 days). The dashboard's September sales
figures have been frozen on ~20/23 กันยายน cumulative numbers all week while real sales have kept
happening — the gap between what the dashboard shows and actual September performance is now
substantial and growing daily. This needs a human to check with whoever normally updates these
sheets (Shopee/Lazada/TikTok ops team), not another automated retry.
