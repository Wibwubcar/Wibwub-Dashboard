# TikTok Ads Download — 7 ต.ค. 2569 (รอบเช้า ~08:15 ICT)
📅 ช่วงข้อมูล: 01/10 – 07/10/2026 (7 ต.ค. = ข้อมูลช่วงเช้าเท่านั้น)

✅ GMV Max: Campaign overview data 20261001 - 20261007.xlsx
   Total row: spend 286,481.09 / 4,937 orders / revenue 1,031,781.99 / ROI 3.60 / CPA 58.03 (7 ต.ค. = 4,814.18)
✅ Business Ads: WIBWUBCAR-Campaign Report-2026-10-01 to 2026-10-07.xlsx (More → Export data)
   98 campaigns (3 with spend); sum == "Total of 98 results": spend 5,431.05 / imp 92,182 / clicks 1,538
   (C-Ads TOP CREATOR 3,392.90 · 18.09.26/Followerพี่เป๊ก 1,796.27 · 06.10.26/แบรนด์ไทย 241.88)

Dashboard:
- DATA_PERIODS.oct.tiktok: spend 291,912.14 / rev 1,031,781.99 / orders 4,937 / ROAS 3.53 / CPA 59.13
- ⚠️ A parallel run of this same schedule had already applied these numbers + tiktokDay=7 + pb-sub labels (commit f39498e, sw v1461).
  This run only fixed the stale cover.tiktokPull (was "6 ต.ค. 19:15") → commit a15336f, sw v1462. node --check passed.

หมายเหตุ:
- ⚠️ .git/HEAD.lock still stuck (sandbox can't delete it). Delete it on the Mac, then double-click push_now.command to push.
- The LaunchAgent auto-moved both files straight into the GMV Max/ and Business Ads/ subfolders.
- The schedule appears to fire twice (duplicate sessions); check for a duplicate scheduled task.
