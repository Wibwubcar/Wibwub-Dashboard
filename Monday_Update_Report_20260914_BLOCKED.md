# ⚠️ WIBWUB Weekly Update (wibwub-monday-update) — 14 ก.ย. 2569 (จันทร์) — BLOCKED

## สถานะ: หยุดตั้งแต่ STEP 1 — Chrome extension ไม่ connected

`list_connected_browsers` คืนค่าว่างเปล่า และ `select_browser` ด้วย deviceId เดิม
(`b75a6bb0-5b78-4e44-92a8-75224f1ce4ee`) ก็ error ว่าไม่มี browser นี้ connected อยู่
→ ไม่สามารถเปิด Shipnity (`data/c/purchase`) หรือ TikTok Affiliate Transaction Analysis
เพื่อตั้งช่วงวันที่/export/ดาวน์โหลดไฟล์ได้เลยในรอบนี้ ตามกฎ error handling ของ skill
("Chrome ไม่ connected → log และหยุด") จึงไม่ได้ทำ STEP 2 เป็นต้นไป

รันตอน 02:14 น. — น่าจะเป็นเพราะเครื่อง Mac sleep หรือ Chrome ปิดอยู่ในช่วงเวลานี้
(รูปแบบเดิมกับ blocker ครั้งก่อน ๆ ในสัปดาห์นี้: 11, 13 (x2) ก.ย.)

## สิ่งที่ทำได้ในรอบนี้ (ไม่ต้องพึ่ง Chrome)

- ✅ Protection check ผ่าน: `M5` array ใน `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html`
  มี 9 เดือน (ม.ค.–ก.ย.) ตรงกับเดือนปัจจุบัน — ไม่ต้องแก้ไข
- ตรวจไฟล์ข้อมูลดิบที่มีอยู่แล้ว — ไม่มีไฟล์ใหม่กว่าที่เคยประมวลผลไปแล้ว:
  - Shipnity: ไฟล์ล่าสุดคือ `Data Shipnity/Data_11-09-2026.xlsx` (11 ก.ย.) — ตรงกับ label
    "อัปเดตล่าสุด 11 ก.ย. 2569" ที่ Top Products บน `WIBWUB_Dashboard.html` แสดงอยู่แล้ว (ประมวลผลไปแล้ว)
  - Affiliate: ไฟล์ Transaction Analysis ล่าสุดคือ `Transaction_Analysis_Creator_List_20260901-20260906.xlsx`
    (คลุมถึง 6 ก.ย.) — แดชบอร์ดปัจจุบันแสดง `AF_MO`/`AFI_MONTHS` ล่าสุดเป็น "ก.ย. (1-8)"
    (อัปเดตจากรอบอื่นก่อนหน้านี้แล้ว ดู commit `2e40ee4` เช้านี้ 09:04 ซึ่งแก้ไข
    `WIBWUB_Affiliate_Dashboard.html` และ `WIBWUB_TikTok_Dashboard_v7.html`)
  - **สรุป: ไม่มีไฟล์ export ใหม่ที่ยังไม่ได้ประมวลผลรออยู่ และไม่มีข้อมูลใหม่กว่านี้ให้ดึงโดยไม่มี Chrome**
- ไม่ได้แตะไฟล์ dashboard (`WIBWUB_Dashboard.html`, `WIBWUB_Mobile.html`, `WIBWUB_Affiliate_Dashboard.html`),
  `sw.js` (ปัจจุบัน `wibwub-v1093`), หรือทำ git commit ใด ๆ ในรอบนี้ เพราะไม่มีข้อมูลใหม่จริงให้ใส่

## ที่ต้องทำ (ต้องมีคนที่เครื่อง Mac)

1. เปิด Chrome บน Mac และตรวจว่า extension "Claude in Chrome" ยัง enable/login/connect อยู่จริง —
   ปัญหานี้เกิดซ้ำหลายรอบติดกันแล้ว โดยเฉพาะรอบที่รันตอนดึก/เช้ามืด (เครื่องอาจ sleep หรือ Chrome ปิดอยู่)
2. เมื่อ Chrome connected แล้ว ให้รัน schedule นี้ใหม่อีกครั้งเพื่อดึงข้อมูลถึงวันที่ล่าสุด
   ทั้ง Shipnity (12–14 ก.ย.) และ TikTok Affiliate Transaction Analysis (9–14 ก.ย.) ที่ยังค้างอยู่
