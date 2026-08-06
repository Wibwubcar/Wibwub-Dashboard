# WIBWUB Weekly Update (wibwub-monday-update) — 2026-08-06

รันแบบอัตโนมัติ ไม่มีผู้ใช้ควบคุมระหว่างรัน (scheduled task)

## ✅ สรุปผล

| งาน | สถานะ |
|---|---|
| ตรวจ/แก้ M5 (label เดือน) ให้ตรงกับ array ยอดขาย | ✅ พบบั๊กและแก้แล้ว |
| Export Shipnity | ✅ (ใช้ไฟล์เต็มเดือนที่มีอยู่แล้วจากรอบก่อนหน้าวันนี้) |
| Export TikTok Affiliate (Transaction Analysis) | ✅ ดาวน์โหลดสำเร็จ |
| อัปเดต Top Products จาก Shipnity | ✅ ตรวจสอบแล้ว ถูกต้อง (ทำไว้แล้วโดยรอบก่อนหน้าวันนี้) |
| อัปเดต Affiliate arrays (AF_*/AFI_*) | ✅ ตรวจสอบแล้ว ถูกต้อง (ทำไว้แล้วโดยรอบก่อนหน้าวันนี้) |
| Bump sw.js cache version | ✅ v587 |
| Git commit + push | ✅ สำเร็จ (commit `220dd73`, sync กับ origin/main แล้ว) |

## 🐛 บั๊กที่พบและแก้ไข: M5 array length mismatch

ระหว่างขั้นตอนตรวจสอบ M5 (label เดือนภาษาไทยที่ใช้เป็น labels ของกราฟทั้งหมดใน `WIBWUB_Dashboard.html`/`WIBWUB_Mobile.html`) พบว่าถูกขยายเป็น 8 ช่อง (เพิ่ม "ส.ค.") ในรอบก่อนหน้าของวันนี้ แต่ array ข้อมูลยอดขายที่จับคู่กัน (SH_REV, TK_REV, LZ_REV และอีก ~20 array) ยังมีแค่ 7 ช่อง (ม.ค.–ก.ค.) เพราะยังไม่มีข้อมูล Shopee/TikTok-shop/Lazada เดือน ส.ค. จาก Google Sheets (นอกขอบเขตงานนี้)

ผลกระทบถ้าไม่แก้: กราฟที่ใช้ `labels:M5` (มีประมาณ 18 กราฟ) จะเพี้ยน/เลื่อนไม่ตรงเดือน และ `setMonthRange(0, M5.length-1)` จะอ้างอิง index เกินขอบเขตของ array อื่น

**แก้โดย**: ย้อน M5 กลับเป็น 7 ช่อง (ม.ค.–ก.ค.) ใน `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html` ให้ตรงกับ array ยอดขายที่มีอยู่จริง — ไม่ได้ไปดึงข้อมูล ส.ค. เดือนสด (Shopee/Lazada/TikTok-shop) มาเติม เพราะอยู่นอกขอบเขตงานนี้

## ตรวจสอบข้อมูลที่มีอยู่แล้ว (validate ซ้ำ ไม่ได้แก้ไข)

- **Affiliate**: ดาวน์โหลด `Transaction_Analysis_Creator_List_20260801-20260804.xlsx` ใหม่ (3,412 แถว) และรวมยอดเอง → GMV=202,794 / NET=197,668 / COMM=23,194 / ครีเอเตอร์ที่มียอด=172 — ตรงกับค่าที่มีอยู่แล้วใน `AF_GMV`/`AFI_GMV` ทุกประการ ไม่ต้องแก้ไขเพิ่ม
- **Top Products**: เทียบกับไฟล์ Shipnity เต็มเดือน `Data_06-08-2026.xlsx` (5,095 แถว) — สินค้าหลัก (Sugar, Interior ฯลฯ) ตรงกับค่าใน `ALL_PRODUCTS`/`PROD_MO` เป๊ะ ยืนยันว่าอัปเดตไว้ถูกต้องแล้ว

## Git commit/push

พบปัญหาชั่วคราวระหว่าง commit จาก sandbox (`.git/index.lock` ลบไม่ได้ เพราะสิทธิ์ file-delete ของ workspace ยังไม่ได้เปิด) — หลังขอสิทธิ์ลบไฟล์แล้ว พบว่ามีกระบวนการอัตโนมัติอีกตัวบนเครื่อง (คาดว่าเป็น `push_now.command`/LaunchAgent) ได้ commit+push การเปลี่ยนแปลงทั้งหมดไปแล้วที่ commit `220dd73` ("Auto-update affiliate data 2026-08-06") ซึ่งรวมไฟล์ทั้งหมดที่แก้ในรอบนี้ (`WIBWUB_Mobile.html`, `WIBWUB_Affiliate_Dashboard.html`, `sw.js`) เรียบร้อย — `git status` ยืนยัน local HEAD ตรงกับ `origin/main` แล้ว **ไม่ต้องดำเนินการเพิ่มเติม**

## ⚠️ รายการที่ควรตรวจสอบเพิ่มเติม (ไม่เร่งด่วน)

- ยอดขาย Shopee/TikTok-shop/Lazada เดือน ส.ค. (Google Sheets) ยังไม่ถูกดึงเข้า dashboard — จะเป็นงานของรอบถัดไปที่ครอบคลุม sales sync เต็มรูปแบบ
