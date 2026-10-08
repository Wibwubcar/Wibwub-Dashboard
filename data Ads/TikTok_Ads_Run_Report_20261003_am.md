# TikTok Ads Download — 3 ต.ค. 2569 (รอบเช้า 08:12 ICT)
📅 ช่วงข้อมูล: 01/10 – 03/10/2026 (3 ต.ค. ข้อมูลระหว่างวันถึง ~08:00)

✅ GMV Max: Campaign overview data 20261001 - 20261004.xlsx (ชื่อไฟล์ถึง 4 ต.ค. แต่แถว 4 ต.ค. = 0)
   Total row: spend 88,898.84 / 1,526 orders / revenue 317,974.44 / ROI 3.58 / CPA 58.26
✅ Business Ads: WIBWUBCAR-Campaign Report-2026-10-01 to 2026-10-03.xlsx
   97 campaigns (2 with spend); sum == "Total of 97 results": spend 2,005.93 / imp 26,641 / clicks 519
   (C-Ads TOP CREATOR 1,188.69 · 18.09.26/Followerพี่เป๊ก 817.24)

Dashboard — commit 8e773db, sw v1380:
- DATA_PERIODS.oct.tiktok: spend 90,904.77 / rev 317,974.44 / orders 1,526 / ROAS 3.50 / CPA 59.57
- TK_BREAKDOWN.oct.gmvMax.total + bizAds updated; gmvLive = 0 (ยังไม่เก็บ)
- cover.tiktokDay=3, tiktokPull, #ads-updated title, ต.ค. pb-sub (TikTok ฿318K), all-period pb-sub (TikTok ฿14.97M ถึง 3 ต.ค.)
- node --check ผ่าน; backup: WIBWUB_Ads_Dashboard.html.bak_20261003_tk_am

หมายเหตุ:
- ⚠️ การแก้ all-period pb-sub (ครั้งที่ 2) ยังไม่ได้ commit — .git/HEAD.lock ค้าง (sandbox ลบไม่ได้) → ลบ HEAD.lock บน Mac แล้ว commit/push
- push ต้อง double-click push_now.command บน Mac
- LaunchAgent ย้ายไฟล์ไป data Ads/TikTok/ (root) แล้ว — copy เข้า subfolder เรียบร้อย
