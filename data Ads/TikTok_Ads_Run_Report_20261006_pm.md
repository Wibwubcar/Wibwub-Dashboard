# TikTok Ads Download — 6 ต.ค. 2569 (รอบเย็น 19:15 ICT)
📅 ช่วงข้อมูล: 01/10 – 06/10/2026 (6 ต.ค. ข้อมูลระหว่างวันถึง ~19:00)

✅ GMV Max: Campaign overview data 20261001 - 20261007.xlsx (แถว 7 ต.ค. = 0)
   Total row: spend 272,188.43 / 4,707 orders / revenue 980,452.69 / ROI 3.60 / CPA 57.83
✅ Business Ads: WIBWUBCAR-Campaign Report-2026-10-01 to 2026-10-06.xlsx (ดึงจาก More → Export data)
   98 campaigns (3 with spend); sum == "Total of 98 results": spend 5,095.87 / imp 79,060 / clicks 1,460
   (C-Ads TOP CREATOR 3,158.93 · 18.09.26/Followerพี่เป๊ก 1,796.27 · 06.10.26/แบรนด์ไทย 140.67 — ใหม่)

Dashboard — commit 0aa6011, sw v1451:
- DATA_PERIODS.oct.tiktok: spend 277,284.30 / rev 980,452.69 / orders 4,707 / ROAS 3.54 / CPA 58.91
- TK_BREAKDOWN.oct.gmvMax.total + bizAds updated; gmvLive = 0 (ยังไม่เก็บ)
- cover.tiktokPull, #ads-updated title, ต.ค. pb-sub (TikTok ฿980K), all-period pb-sub (TikTok ฿15.73M)
- node --check ผ่าน; backup: WIBWUB_Ads_Dashboard.html.bak_20261006_tk_pm

หมายเหตุ:
- ⚠️ .git/HEAD.lock ค้าง (sandbox ลบไม่ได้) → ลบบน Mac ก่อน commit ครั้งถัดไป; push ต้อง double-click push_now.command
- LaunchAgent ย้ายไฟล์ Business Ads ไป data Ads/TikTok/ (root) → copy เข้า subfolder แล้ว
- ปุ่ม "View report" ตอนนี้เปิด panel สรุป AI ไม่ใช่ download — ใช้ More → Export data แทน
