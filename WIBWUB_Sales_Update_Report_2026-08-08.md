# WIBWUB Sales Sheet Update — 2026-08-08

## สรุป
- อ่าน Google Sheets ทั้ง 3 sheet (Shopee, TikTok, Lazada) เรียบร้อย
- **ไม่มีเดือนใหม่ให้เพิ่ม** — เดือนสิงหาคม 2026 มีข้อมูลใน Sheet ทั้ง 3 platform เพียงบางส่วน (row ล่าสุด `01-05/08/26`, ยังไม่ใช่ยอดสะสมสิ้นเดือน) จึงยังไม่ push เข้า dashboard ตามกฎ
- ข้อมูลเดือนกรกฎาคม (ก.ค.) ในทั้ง 2 ไฟล์ตรงกับ Sheet ต้นทางทุกค่าอยู่แล้ว (SH_REV, TK_REV, LZ_REV เดือน ก.ค. = 5,923,704 / 2,089,005.47 / 95,770.98 ตรงกับแถวสุดท้าย `01-31/07/26` ของแต่ละ Sheet) — ไม่ต้องแก้ค่า

## 🐛 พบและแก้บั๊ก
STEP 0 ตรวจพบว่า array `M5` ในทั้ง `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html` มี 8 ช่อง (รวม "ส.ค." ที่ถูกใส่มาก่อนหน้านี้แบบไม่มีข้อมูลจริงรองรับ) ในขณะที่ `SH_REV`/`TK_REV`/`LZ_REV`/`MONTH_LABELS_FULL`/`MONTH_LABELS_SHORT`/`MP_MONTH_BOUNDS` มีแค่ 7 ช่อง (ถึง ก.ค.) — ตรงกับรูปแบบบั๊กที่เคยเกิดเมื่อ 2026-08-03 ที่ SKILL ระบุไว้ว่าอันตราย เพราะทำให้กราฟเดือนล่าสุด (index 7) อ่านค่า `undefined` จาก data array ที่มีแค่ index 0-6

**แก้ไข:** เนื่องจาก Sheet ต้นทางยังไม่มีข้อมูลสิงหาคมแบบเต็มเดือน จึงลบ `"ส.ค."` ออกจาก `M5` ในทั้ง 2 ไฟล์ ให้กลับมาเป็น 7 ช่องตรงกับ data array ทั้งหมด — ไม่ได้แตะ data array ใดๆ เลย

## ไฟล์ที่แก้
- `WIBWUB_Dashboard.html` — M5 array (8→7 ช่อง)
- `WIBWUB_Mobile.html` — M5 array (8→7 ช่อง)
- `sw.js` — bump cache v600 → v601

## Git
- Commit `eda6ba5` สร้างแล้ว (local) — **รอ user กด `push_now.command` เพื่อ push ขึ้น GitHub** (sandbox ติด proxy push เองไม่ได้)

## หมายเหตุอื่นๆ ที่ไม่เกี่ยวกับงานนี้ (ไม่ได้แตะ)
พบว่ามีไฟล์อื่นที่ modified อยู่จาก process อื่น (Shipnity top products, Affiliate GMV, Followers zip, auto_push.log) — ไม่เกี่ยวกับ scope งาน Sales Update นี้ ไม่ได้ commit ไปด้วย
