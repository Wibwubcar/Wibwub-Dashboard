# ⚠️ WIBWUB Weekly Update (wibwub-monday-update) — 26 ก.ย. 2569 (เสาร์) — BLOCKED

## สถานะ: หยุดหลัง STEP 1–2 — ดาวน์โหลดไฟล์ทั้ง Shipnity และ Affiliate ไม่สำเร็จ

## Protection check (ก่อน STEP 1)
- `M5` array ใน `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html` มี 9 เดือน ตรงกับเดือนปัจจุบัน (กันยายน = เดือนที่ 9) — ไม่ต้องแก้ไข

## STEP 1: Shipnity export — ⚠️ export UI แสดง 100% แต่ไฟล์ไม่ลงจริง
- เปิด Shipnity → ประวัติ → ตั้งช่วงวันที่ 1–26 ก.ย. 2569 สำเร็จ
- กด "ส่งออกข้อมูล" เลือก "ไฟล์เดียว" (.xlsx) → progress bar ขึ้นจาก 0% ถึง **100%** สำเร็จ (ใช้เวลา ~100 วินาทีต่อครั้ง)
- ลองทำซ้ำ **2 รอบเต็ม** (แต่ละรอบถึง 100%) และลองคลิกปุ่ม/ไอคอนดาวน์โหลดที่ปรากฏในหน้าต่าง Export หลายจุด (ไอคอนไฟล์, ปุ่มวงกลมข้างชื่อไฟล์, ปุ่ม X) รวมถึงลองสั่ง `.click()` ตรงบน element ผ่าน JS
- ตรวจสอบ `$HOME/mnt/Downloads/` ก่อน/หลังทุกครั้ง (ทั้งด้วย `ls -lt` และ `find -newermt`) — **ไม่มีไฟล์ .xlsx ใหม่ลงมาเลยแม้แต่ไฟล์เดียว** ตลอดการทดสอบ (~10+ นาที)
- ตรวจสอบ network requests (fetch/XHR) และ `performance.getEntriesByType('resource')` บนแท็บ — พบเฉพาะการ poll ผ่าน `/api/graphql` (สำหรับ progress %) ไม่มี request ใดที่ดึงตัวไฟล์ xlsx จริงเลย และไม่มี `<a>` tag ที่มี href/download attribute ของไฟล์ผลลัพธ์ในหน้า DOM
- สรุป: ต่างจากรอบก่อนหน้า (ดู `Monday_Update_Report_20260919_BLOCKED.md` ที่เคย export สำเร็จและเห็นสถานะ "Download completed") รอบนี้ progress bar ขึ้น 100% แต่ไม่มีการส่งไฟล์จริงมาที่เบราว์เซอร์เลย — คาดว่าเป็นปัญหาฝั่ง Shipnity (อาจเป็น mechanism ใหม่ที่ต้องใช้ native save dialog ซึ่ง browser-automation เข้าไม่ถึง หรือ backend generate ไฟล์ไม่สำเร็จ)

## STEP 2: Affiliate (Transaction Analysis) export — ❌ HTTP 503 ซ้ำรอยปัญหาเดิม
- หน้า `transaction-analysis` (URL เดิม) ถูก redirect ไปหน้า "ผลการดำเนินงาน" (Performance) ใหม่ — มี deprecation banner ตามที่คาด, ทำงานต่อในหน้าใหม่ได้ปกติ
- ตั้งช่วงวันที่แบบกำหนดเอง: 01/09/2026 – 23/09/2026 (23 = วันล่าสุดที่มีข้อมูล, วันที่ 24–26 ถูก grey ไว้ในปฏิทิน) สำเร็จ
- กด "ส่งออก" บนแท็บครีเอเตอร์สำเร็จหลายครั้ง (ระบบสร้างรายงานใหม่ในพาเนล "รายงานที่ส่งออก" สถานะเปลี่ยนจาก "กำลังส่งออก" เป็นพร้อมดาวน์โหลดได้)
- เมื่อกด **"ดาวน์โหลด"** (ทั้งรายงานที่เพิ่งสร้างใหม่ 3-4 ชุด และรายงานเก่าที่มีอยู่แล้ว) ระบบตอบกลับ **HTTP 503 Service Unavailable** ทุกครั้งที่ endpoint:
  ```
  GET /api/v1/oec/affiliate/compass/export_task/export?...&task_id=...
  ```
  (ยืนยันด้วย network request log ตรง ๆ ไม่ใช่การเดา)
- นี่คือ**ปัญหาเดิมที่เคยเจอมาก่อน** เมื่อ 20 ก.ย. 2569 (ดู `Affiliate_Update_Report_20260920_thu_BLOCKED.md`) — เป็นปัญหาฝั่ง TikTok server ไม่ใช่ปัญหาการตั้งค่าฝั่งเรา

## ผลกระทบ
- ไม่มีไฟล์ Shipnity หรือ Affiliate ใหม่เข้า `Data Shipnity/` หรือ `Data Affiliate/`
- **ไม่มีการแก้ไขไฟล์ dashboard ใดๆ** (`WIBWUB_Dashboard.html`, `WIBWUB_Mobile.html`, `WIBWUB_Affiliate_Dashboard.html`) — ข้อมูลเดิมยังคงอยู่ครบถ้วน ไม่มีความเสี่ยงข้อมูลเสียหาย
- ไม่มีการ bump `sw.js` และไม่มีการ `git add`/`git commit`/สร้าง `push_now.command` ในรอบนี้

## ข้อเสนอแนะสำหรับรอบถัดไป
1. ลองรันใหม่อีกครั้งในอีก 1-2 ชั่วโมง — ทั้งสองปัญหามีลักษณะเป็น service-side ชั่วคราว
2. ถ้า Shipnity ยังโชว์ 100% แต่ไม่ยอมดาวน์โหลดไฟล์อีก ควรตรวจสอบด้วยตนเองผ่านเบราว์เซอร์ปกติว่า UI การส่งออกเปลี่ยนไปหรือไม่ (เช่น อาจต้องกด "Save As" ผ่าน native dialog ซึ่ง automation เข้าไม่ถึง)
3. Affiliate 503 เกิดซ้ำเป็นครั้งที่ 2 ในรอบ 1 สัปดาห์ — ถ้ายังเป็นต่อเนื่องเกิน 24-48 ชม. ควรพิจารณาแจ้ง TikTok Shop support

## ไฟล์ที่แก้ไข
ไม่มี (no-op run เนื่องจากบล็อกตั้งแต่ขั้นตอนดาวน์โหลดทั้งสองแหล่งข้อมูล)
