# TikTok Ads Download — 2026-10-08 (รอบเย็น 19:42 ICT)
📅 ช่วงข้อมูล: 01/10 – 08/10/2026 (8 ต.ค. บางส่วน ~19:40)

✅ GMV Max: Campaign overview data 20261001 - 20261008.xlsx
   Total row: spend 356,411.38 / orders 5,975 / revenue 1,292,724.76 / ROI 3.63 / CPA 59.65
✅ Business Ads: WIBWUBCAR-Campaign Report-2026-10-01 to 2026-10-08.xlsx
   sum(3 campaigns) == Total of 98 results: spend 6,636.08 / imp 135,762 / clicks 2,065

Dashboard: DATA_PERIODS.oct.tiktok → spend 363,047.46 / rev 1,292,724.76 / orders 5,975 / ROAS 3.56 / CPA 60.76;
TK_BREAKDOWN.oct gmvMax + bizAds updated; tiktokPull, #ads-updated title, oct pb-sub fallback updated.
node --check OK; sw.js wibwub-v1503 → v1504; commit 0fc28a0 (push pending: double-click push_now.command).

หมายเหตุ:
- LaunchAgent moved downloads to data Ads/TikTok/ (root) before the Downloads check; copied from there into GMV Max/ and Business Ads/.
- GMV Max export button clicked twice (first click showed no file within ~20s); a duplicate file may appear.
- Business Ads export: "View report" opens AI summary panel, not export — used More → Export data instead.
- Business Ads xlsx has no Campaign ID column; columns are spend=4, imp=7, clicks=8 (task notes say 2/3/7 — outdated).
- git: a concurrent git process was running; leftover .git/HEAD.lock / next-index-10.lock / index.lock could not be removed from the sandbox — may need manual removal before push.
