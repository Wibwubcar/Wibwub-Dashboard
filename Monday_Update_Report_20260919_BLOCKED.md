# ⚠️ WIBWUB Weekly Update (wibwub-monday-update) — 19 ก.ย. 2569 (เสาร์) — BLOCKED

## สถานะ: หยุดหลัง STEP 2 — ตรวจพบ automation อีกตัวกำลังแก้ไฟล์ชุดเดียวกันอยู่พร้อมกัน

ระหว่างทำ STEP 1–2 (ดาวน์โหลด Shipnity + TikTok Affiliate export) พบหลักฐานชัดเจนว่ามี
automated process อื่นกำลังทำงานกับไฟล์ repo ชุดเดียวกันอยู่ ณ เวลาเดียวกัน (real-time):

- `Data Shipnity/Data_19-09-2026.xlsx` ถูกสร้างใหม่โดยกระบวนการอื่นเมื่อ 05:40 UTC (ก่อนที่ผมจะ copy ไฟล์ของตัวเองเข้าไป)
- `WIBWUB_Mobile.html` และ `WIBWUB_Dashboard.html` ถูกแก้ไขเมื่อ 05:39 UTC — ตรงกับไฟล์ที่ STEP 3
  ของ skill นี้ต้องแก้ไข (Top Products / ALL_PRODUCTS)
- `Data Affiliate/ครีเอเตอร์/` มีไฟล์ใหม่ถูกเขียนเข้ามาเรื่อย ๆ ระหว่างที่ตรวจสอบ (05:23, 05:33, 05:39 UTC)
- พบ `.git/index.lock` ค้างอยู่ช่วงสั้น ๆ แล้วหายไปพร้อมกับมี commit ใหม่โผล่ขึ้นมาเอง 3 ครั้งติดกันโดยที่ผมไม่ได้สั่ง:
  `69b0e8b` (Shopee Ads sync), `637a654` (Shopee Live), `f82c5e0` (TikTok sales from Sheets)
- ล่าสุด `git status` แสดงว่า `WIBWUB_Mobile.html` ถูก `git add` (staged) ไว้แล้วโดยกระบวนการอื่น — ยังไม่ทันถูก commit

ไฟล์ที่ต้องแก้ใน STEP 3 (Top Products), STEP 5 (sw.js version bump + commit) เป็นไฟล์เดียวกับที่
กระบวนการอื่นกำลังแก้/stage/commit อยู่พอดี ถ้าผมอ่านค่าปัจจุบันมาแก้ต่อแล้ว commit ทับ มีความเสี่ยงสูงที่จะ:
1. เขียนทับการเปลี่ยนแปลงที่อีกกระบวนการเพิ่งทำไป (lost update)
2. ชน `.git/index.lock` กลางอากาศระหว่าง commit ทำให้ repo state ผิดพลาด
3. ได้ค่า Top Products/Affiliate ที่ไม่ตรงกัน เพราะข้อมูลต้นทางถูกแก้ไปแล้วระหว่างที่ผมกำลังคำนวณ

ตามกฎ error-handling ("stop-and-log ถ้าไม่แน่ใจ") และ pattern ที่เคยใช้มาก่อน (ดู
`Monday_Update_Report_20260913_BLOCKED.md`) จึงหยุดการทำงานที่ STEP 2 ไม่ไปแตะไฟล์ dashboard/sw.js/git ต่อ

## สิ่งที่ทำไปแล้วในรอบนี้

- ✅ Protection check: `M5` array ใน `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html` มี 9 เดือน
  ตรงกับเดือนปัจจุบัน (กันยายน) — ไม่ต้องแก้ไข
- เปิด Shipnity ตั้งช่วงวันที่ 1–30 ก.ย. 2569 และสั่ง export `Data_19-09-2026.xlsx` สำเร็จ (ยืนยันสถานะ
  "Download completed" ในหน้า Shipnity) — **ไม่ได้ copy ไฟล์ทับเข้า `Data Shipnity/` เพราะกระบวนการอื่น
  เพิ่งสร้างไฟล์ชื่อเดียวกันที่สดกว่าไว้แล้ว (05:40 UTC)**
- เปิด TikTok Affiliate Transaction Analysis ตั้งช่วง 01–16 ก.ย. 2569 (16 ก.ย. คือวันล่าสุดที่มีข้อมูล
  อัปเดต) และสั่ง export เข้าคิวไว้ — **ไม่ได้ดาวน์โหลด/copy เข้า `Data Affiliate/` เพราะกระบวนการอื่นกำลัง
  เขียนไฟล์ใหม่เข้าโฟลเดอร์ย่อยเดียวกันอยู่ระหว่างที่ตรวจสอบ**
- ไม่ได้แตะ `WIBWUB_Dashboard.html`, `WIBWUB_Mobile.html`, `WIBWUB_Affiliate_Dashboard.html`, `sw.js`
  และไม่ได้ทำ `git add`/`git commit` ใด ๆ ในรอบนี้

## สิ่งที่ต้องทำ

1. รอให้ automation อีกตัวที่กำลังรันอยู่ตอนนี้ทำงานจนเสร็จและ commit เรียบร้อยก่อน (ดู git log ว่ามี
   commit ใหม่ที่ครอบคลุม Top Products / Affiliate arrays / sw.js version หรือยัง)
2. ถ้า commit ล่าสุดยังไม่ครอบคลุมข้อมูล Shipnity/Affiliate ถึงวันที่ 19 ก.ย. ให้รัน schedule
   `wibwub-monday-update` นี้ใหม่อีกครั้ง (ควรเว้นระยะจาก schedule อื่น ๆ ที่แก้ไฟล์เดียวกัน เพื่อลด
   โอกาสชนกันแบบนี้ซ้ำ)
3. แนะนำให้ตรวจสอบว่ามี scheduled task ตั้งเวลาซ้อนกันหลายตัวที่แก้ `WIBWUB_Mobile.html` /
   `WIBWUB_Dashboard.html` / `sw.js` พร้อมกันหรือไม่ (เช่น update-wibwub, fastmoss, procurement-dashboard
   ฯลฯ) เพื่อจัดตารางไม่ให้ทับเวลากันอีกในอนาคต
