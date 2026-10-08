# TikTok Ads Download — 2 ต.ค. 2569 (รอบเย็น 19:13 ICT)
📅 ช่วงข้อมูล: 01/10 – 02/10/2026 (2 ต.ค. ยังเป็นข้อมูลระหว่างวัน)

✅ GMV Max: Campaign overview data 20261001 - 20261002.xlsx
   Total row: spend 72,502.62 / 1,239 orders / revenue 257,849.53 / ROI 3.56 / CPA 58.52
✅ Business Ads: WIBWUBCAR-Campaign Report-2026-10-01 to 2026-10-02.xlsx
   97 campaigns (2 with spend); sum == "Total of 97 results": spend 1,557.43 / imp 22,160 / clicks 430
   (C-Ads TOP CREATOR 969.54 · 18.09.26/Followerพี่เป๊ก 587.89)

Dashboard (WIBWUB_Ads_Dashboard.html) — commit a3287ea, sw v1375:
- DATA_PERIODS.oct.tiktok: spend 74,060.05 / rev 257,849.53 / orders 1,239 / ROAS 3.48 / CPA 59.77
- TK_BREAKDOWN.oct.gmvMax.total + bizAds updated; gmvLive = 0 (ยังไม่เก็บ)
- cover.tiktokPull, #ads-updated title, ต.ค. pb-sub fallback (TikTok ฿258K) updated
- node --check ผ่าน; backup: WIBWUB_Ads_Dashboard.html.bak_20261002_tk_pm

หมายเหตุ:
- GMV Max export button ต้องคลิกผ่าน JS (data-testid="export-button-index-...") — คลิกพิกัดจาก screenshot ไม่ติดเพราะ page zoom
- Business Ads: ปุ่ม "View report" เปิดเป็น AI summary panel แล้ว → ใช้ More → Export data แทน
- LaunchAgent ย้ายไฟล์จาก Downloads ไปไว้ที่ data Ads/TikTok/ (root) — copy เข้า subfolder แล้ว
- ⚠️ git ทิ้ง .git/HEAD.lock (sandbox ลบไม่ได้) — ถ้า push/commit ติด "HEAD.lock exists" ให้ลบไฟล์นี้บน Mac ก่อน
- push ต้อง double-click push_now.command บน Mac
