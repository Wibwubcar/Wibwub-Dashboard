# TikTok Ads Download — 27 ก.ย. 2026 (เย็น, ~19:16)
📅 ช่วงข้อมูล: 01/09 – 27/09 (27 ก.ย. เป็นข้อมูลระหว่างวัน)

## ผลการดาวน์โหลด
- ✅ GMV Max: `Campaign overview data 20260901 - 20260927.xlsx` → data Ads/TikTok/GMV Max/
  Total row: spend 735,623.83 / orders 12,973 / revenue 2,760,484.75 / ROI 3.75 / CPA 56.70
  (ได้ไฟล์ 20260901-20260928 มาด้วยจากการกดซ้ำ — ข้อมูลเดียวกัน ส่วนต่าง spend 18 บาท; ใช้ไฟล์ -0927 ที่ใหม่กว่า)
- ✅ Business Ads: `WIBWUBCAR-Campaign Report-2026-09-01 to 2026-09-27.xlsx` → data Ads/TikTok/Business Ads/
  Total of 97 results: spend 23,505.40 / imp 314,614 / clicks 3,913 — ผลรวม 6 แคมเปญที่มี spend ตรงกับแถว Total ทุกค่า

## Dashboard update (WIBWUB_Ads_Dashboard.html)
- DATA_PERIODS.sep.tiktok: spend 759,129.23 / revenue 2,760,484.75 / orders 12,973 / ROAS 3.64 / CPA 58.52
- TK_BREAKDOWN.sep.gmvMax.total และ bizAds (total + 6 campaigns) อัปเดตแล้ว; gmvLive ไม่เปลี่ยน (0 = ยังไม่เก็บ)
- cover.tiktokPull, badge #ads-updated, .pb-sub (ก.ย. + ทั้งหมด) → TikTok ถึง 27 ก.ย.
- JS ผ่าน node --check; backup: WIBWUB_Ads_Dashboard.html.bak_20260927_tk_pm
- sw.js ไม่ได้ bump (ไฟล์นี้ไม่อยู่ใน FILES[] ของ sw.js)
- git commit 4353ef4 แล้ว — push ต้อง double-click `push_now.command`

## หมายเหตุ
1. คำสั่งใน task ใช้ปุ่ม "ดูรายงาน/View report" แต่ปุ่มนี้เปิด insights ไม่ใช่ export — ใช้ Campaigns > More > Export data แทน (ทำงานเมื่อคลิกผ่าน element ref)
2. ไฟล์ถูก LaunchAgent ย้ายจาก Downloads ไป `data Ads/TikTok/` (root) → cp เข้าโฟลเดอร์ย่อยแล้ว
3. ⚠️ git ทิ้ง `.git/HEAD.lock` และ tmp_obj ไว้ (sandbox ลบไม่ได้) — ถ้า git รอบถัดไปขึ้น "HEAD.lock exists" ให้ลบ `.git/HEAD.lock` ด้วยมือ
