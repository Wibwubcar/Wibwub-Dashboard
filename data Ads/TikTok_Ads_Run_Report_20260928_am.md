# TikTok Ads Download — 28 ก.ย. 2026 (เช้า, ~08:14)
📅 ช่วงข้อมูล: 01/09 – 28/09 (28 ก.ย. เป็นข้อมูลระหว่างวัน ~08:13)

## ผลการดาวน์โหลด
- ✅ GMV Max: `Campaign overview data 20260901 - 20260928.xlsx` → data Ads/TikTok/GMV Max/
  Total row: spend 747,356.07 / orders 13,188 / revenue 2,802,177.94 / ROI 3.75 / CPA 56.67
- ✅ Business Ads: `WIBWUBCAR-Campaign Report-2026-09-01 to 2026-09-28.xlsx` → data Ads/TikTok/Business Ads/
  Total of 97 results: spend 24,076.68 / imp 319,820 / clicks 3,993 — ผลรวม 6 แคมเปญที่มี spend ตรงกับแถว Total ทุกค่า

## Dashboard update (WIBWUB_Ads_Dashboard.html)
- DATA_PERIODS.sep.tiktok: spend 771,432.75 / revenue 2,802,177.94 / orders 13,188 / ROAS 3.63 / CPA 58.50
- TK_BREAKDOWN.sep.gmvMax.total และ bizAds (total + 6 แคมเปญ) อัปเดตแล้ว; gmvLive ไม่เปลี่ยน (0 = ยังไม่เก็บ)
- cover.tiktokDay → 28, tiktokPull, badge #ads-updated (fallback + title), .pb-sub (ก.ย. + ทั้งหมด: TikTok ฿14.34M)
- JS ผ่าน node --check; backup: WIBWUB_Ads_Dashboard.html.bak_20260928_tk_am
- sw.js ไม่ได้ bump (ไฟล์นี้ไม่อยู่ใน FILES[] ของ sw.js)

## หมายเหตุ
1. Schedule Shopee (08:15) แก้ไฟล์ dashboard พร้อมกัน — รอให้เสร็จ (08:16:00) แล้วค่อยแก้ทับบนเวอร์ชันล่าสุด ไม่มีข้อมูล Shopee หาย
2. ⚠️ **ยังไม่ได้ git commit** — `.git/HEAD.lock`, `.git/index.lock`, `.git/next-index-7.lock` ค้างจาก commit ของ Shopee (5c36943, 08:16) และ sandbox ลบไม่ได้ → ลบ 3 ไฟล์นี้ด้วยมือ แล้วรัน `git add "data Ads/WIBWUB_Ads_Dashboard.html" && git commit -m "auto-update: TikTok Ads 1-28 ก.ย."` จากนั้น double-click `push_now.command`
3. ปุ่ม export GMV Max ต้องคลิก 2 ครั้ง (ครั้งแรกโดนแบนเนอร์ layout shift); Business Ads ใช้ Campaigns > More > Export data (element ref)
4. LaunchAgent ย้ายไฟล์จาก Downloads ไป `data Ads/TikTok/` (root) → cp เข้าโฟลเดอร์ย่อยแล้ว

## Resolution (run 2, ~09:2x, same schedule window)
- ✅ git commit completed: removed stale `.git/index.lock` (after granting delete permission on the connected folder — sandbox could not `rm` it before), staged only `data Ads/WIBWUB_Ads_Dashboard.html` + `sw.js`, ran `node --check` (OK), bumped sw.js `wibwub-v1284→v1285` (harmless even if this file isn't in sw.js's FILES[] cache list).
- The commit ended up bundled into `e971364 auto: update TikTok product sales data 2026-09-28 09:01:50` (another scheduled task committed while our files were staged in the shared index) rather than its own commit — data is correct and safely in history, just not under its own commit message this time.
- Verified `origin/main` includes it: pushed as part of `68215fd..021b4b6` (auto_push.log, 09:24). No data loss.
- Re-downloaded GMV Max + Business Ads xlsx independently in this run and confirmed Total rows match exactly what's now live in the dashboard (spend 747,356.07 / orders 13,188 / revenue 2,802,177.94 GMV Max; spend 24,076.68 / imp 319,820 / clicks 3,993 Business Ads).
