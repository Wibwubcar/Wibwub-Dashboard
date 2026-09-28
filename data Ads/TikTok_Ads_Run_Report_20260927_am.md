# TikTok Ads Download — 27 ก.ย. 2026 (เช้า)

## ผลการดาวน์โหลด
- ✅ GMV Max: `Campaign overview data 20260901 - 20260928.xlsx` → data Ads/TikTok/GMV Max/
  Total row: spend 718,492.24 / orders 12,643 / revenue 2,700,254.05 / ROI 3.76 / CPA 56.83
- ✅ Business Ads: `WIBWUBCAR-Campaign Report-2026-09-01 to 2026-09-27.xlsx` → data Ads/TikTok/Business Ads/
  Total of 97 results: spend 23,059.46 / imp 309,404 / clicks 3,813 (6 spend>0 campaigns verified against Total row)

## Dashboard update
- WIBWUB_Ads_Dashboard.html: DATA_PERIODS.sep.tiktok, TK_BREAKDOWN.sep.gmvMax, TK_BREAKDOWN.sep.bizAds, cover.tiktokDay/tiktokPull ทั้งหมดอัปเดตแล้ว (spend รวม 741,551.70, ROAS 3.64, CPA 58.65)
- JS validated ok (node --check)
- Backup saved: WIBWUB_Ads_Dashboard.html.bak_20260927_tk

## หมายเหตุ/ปัญหาที่พบ
1. **ปุ่ม Export ทั้งสองจุด (GMV Max download icon และ Campaigns > More > Export data) เป็น async task ที่ popup-block ภายใต้ automation** — ทั้งสองปุ่มยิง request สำเร็จ (task_status: SUCCESS) แต่ browser ไม่เปิดหน้าดาวน์โหลดให้อัตโนมัติเพราะ transient user-activation หมดอายุระหว่าง round-trip ของ download_task/query ต้อง retry หลายรอบกว่าจะสำเร็จ (สังเกต pattern เดียวกันทั้งสองไฟล์)
2. **ไฟล์ที่ดาวน์โหลดสำเร็จไม่ได้ไปอยู่ใน mounted "Downloads" folder** แต่ไปอยู่ที่ `data Ads/TikTok/` (root) โดยตรง — เข้าใจว่า Chrome จำโฟลเดอร์ Save-As ล่าสุดของไฟล์ประเภทนี้ไว้ ต้อง `mv` เข้าโฟลเดอร์ย่อยเองหลังดาวน์โหลด
3. **sw.js cache version ไม่ได้ bump เพิ่ม** — WIBWUB_Ads_Dashboard.html ไม่ได้อยู่ใน FILES[] ของ service worker (มีแค่ Mobile PWA files) จึงไม่จำเป็นต้อง bump สำหรับการเปลี่ยนแปลงนี้ ปล่อย sw.js ไว้ตามที่ scheduled shopee run ตั้งไว้ (v1270) เพื่อไม่ชนกับงานที่ค้าง stage อยู่
4. **⚠️ Git commit ยังไม่ได้ทำ**: พบ `.git/index.lock` ค้างอยู่ในโฟลเดอร์ (0 bytes, สร้างระหว่าง run นี้) และ sandbox ไม่มีสิทธิ์ลบไฟล์ในโฟลเดอร์ที่เชื่อมต่อ (ต้องขอ delete permission จาก user ก่อน) — ไม่สามารถ `git add`/`git commit` ได้ในรอบนี้ นอกจากนี้ยังพบว่ามี staged changes ค้างอยู่จาก process อื่น (WIBWUB_Dashboard.html + sw.js v1270, จาก shopee sync รอบ 08:30) ที่ยังไม่ commit — ควรตรวจสอบและ commit ทั้งหมดรวมกันในรอบถัดไป (การเปลี่ยนแปลงของไฟล์นี้ยังอยู่ใน working tree ปกติ ไม่ได้หาย)
