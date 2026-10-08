# TikTok Ads Download — 30 ก.ย. 2569 (รอบเช้า 08:13 ICT)
📅 ช่วงข้อมูล: 01/09 – 30/09/2026 (30 ก.ย. = ข้อมูลระหว่างวัน)

✅ GMV Max: Campaign overview data 20260901 - 20260930.xlsx
   Total row: spend 828,652.63 / 14,498 orders / revenue 3,085,863.98 / ROI 3.72 / CPA 57.16
   (29 ก.ย. ปิดวัน 47,696.26 / 735 / 161,236.78; 30 ก.ย. บางส่วน 9,408.06 / 157 / 36,995.13)
✅ Business Ads: WIBWUBCAR-Campaign Report-2026-09-01 to 2026-09-30.xlsx
   97 campaigns (6 with spend); sum = Total row: spend 25,973.63 / imp 345,476 / clicks 4,430

Dashboard (WIBWUB_Ads_Dashboard.html) updated:
- DATA_PERIODS.sep.tiktok: spend 854,626.26 / revenue 3,085,863.98 / orders 14,498 / ROAS 3.61 / CPA 58.95
- TK_BREAKDOWN.sep.gmvMax.total + bizAds.total/campaigns
- cover.tiktokDay 29→30, tiktokPull, #ads-updated badge (static text: Shopee ถึง 29 · TikTok ถึง 30), .pb-sub (sep: TikTok ฿3.09M; all: TikTok ฿14.63M)
- node --check OK, sw.js v1325 → v1326, git commit e3d6a39 (backup: .bak_20260930_tk_am)

หมายเหตุ:
- Session OK. LaunchAgent moved both files to data Ads/TikTok/; GMV Max file was already in GMV Max/, Business Ads file moved into Business Ads/.
- "View report" now opens an AI summary panel, not a download — the export came from More > Export data.
- gmvLive not pulled (stays 0 = not collected; already included in GMV Max Overview).
- ⚠️ .git/index.lock left behind (sandbox can't delete). Remove it on the Mac before push_now.command: rm "…/All/.git/index.lock"
- Push pending: double-click push_now.command.
