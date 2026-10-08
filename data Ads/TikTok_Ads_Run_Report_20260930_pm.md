# TikTok Ads Download — 30 ก.ย. 2569 (รอบค่ำ 22:05 ICT)
📅 ช่วงข้อมูล: 01/09 – 30/09/2026 (30 ก.ย. = ข้อมูลระหว่างวัน)

✅ GMV Max: Campaign overview data 20260901 - 20260930.xlsx
   Total row: spend 861,356.34 / 14,994 orders / revenue 3,194,796.03 / ROI 3.71 / CPA 57.45
   (30 ก.ย. บางส่วน 42,111.77 / 653 / 146,139.36)
✅ Business Ads: WIBWUBCAR-Campaign Report-2026-09-01 to 2026-09-30.xlsx (ไฟล์ 22:03 ที่มีอยู่แล้วใน data Ads/TikTok/)
   97 campaigns (6 with spend); sum == Total row: spend 26,409.04 / imp 352,172 / clicks 4,585

Dashboard updated:
- DATA_PERIODS.sep.tiktok: spend 887,765.38 / revenue 3,194,796.03 / orders 14,994 / ROAS 3.60 / CPA 59.21
- TK_BREAKDOWN.sep.gmvMax.total + bizAds.total/campaigns
- cover.tiktokPull → 22:05, #ads-updated badge + title, .pb-sub (sep TikTok ฿3.19M; all TikTok ฿14.74M)
- node --check OK, sw.js v1341 → v1342, git commit 9e5f081 (backup .bak_20260930_tk_pm)

หมายเหตุ:
- Session OK. GMV Max download clicked via export icon; LaunchAgent moved file to data Ads/TikTok/, copied into GMV Max/.
- Business Ads not re-downloaded: a fresh 22:03 export (1 min before this run) was already in data Ads/TikTok/; copied into Business Ads/.
- Business Ads column layout is [0]=name,[4]=spend,[7]=imp,[8]=clicks (task file's [2]/[3]/[7] is outdated).
- git left .git/HEAD.lock (sandbox can't unlink) — remove on the Mac before push_now.command.
- Push pending: double-click push_now.command.
