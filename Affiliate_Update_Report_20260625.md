# WIBWUB Affiliate Auto-Update — 25 มิ.ย. 2569

## สรุป: ไม่มีข้อมูลใหม่ให้ sync — และมีงานค้าง push ขึ้น GitHub

รอบนี้ **ไม่ได้ export/แก้ไข dashboard** เพราะ TikTok ยังไม่มีข้อมูลใหม่กว่าที่ dashboard มีอยู่แล้ว แต่พบ **การเปลี่ยนแปลงค้างที่ยังไม่ถูก push ขึ้น GitHub ตั้งแต่ 23 มิ.ย.**

---

### 1. ข้อมูล TikTok ตอนนี้ lag ถึงแค่ 21 มิ.ย. (เก่ากว่าที่มีใน dashboard)
เปิดหน้า Transaction Analysis และตั้ง date range แล้ว — ปฏิทินเลือกได้ถึง **21 มิ.ย. เท่านั้น** (22–27 มิ.ย. ถูก grey out, "อัปเดตเมื่อ 21 มิ.ย. 2026").

แต่ dashboard ปัจจุบันมีข้อมูลถึง **23 มิ.ย.** อยู่แล้ว → การ export ใหม่จะได้ข้อมูล **ที่เก่ากว่าและครบน้อยกว่า** จึงข้ามการ export เพื่อไม่ให้ตัวเลขถอยหลัง

### 2. สถานะ Dashboard (เป็นปัจจุบันถึง 23 มิ.ย. แล้ว)
- **WIBWUB_Mobile.html:** AFI_GMV[Jun]=฿437,951 · AFI_NET=฿429,851 · AFI_COMM=฿54,303
- **WIBWUB_Affiliate_Dashboard.html:** badge "1–23 มิ.ย. 2569 · อัปเดต 24 มิ.ย. 2569"
- ไฟล์ครบ 4 tab ในโฟลเดอร์ Data Affiliate/ ช่วง 1–23 มิ.ย.
- ข้อมูล creator file 23 มิ.ย. (อ้างอิง): GMV ฿436,626 · Net ฿429,316 · Comm ฿54,274 · 308 creators

### 3. ⚠️ งานค้างสำคัญ — ยังไม่ได้ push ขึ้น GitHub
commit ล่าสุดบน git คือ **23 มิ.ย. (sw v233)** แต่ working tree ถูกแก้ไปไกลแล้วและยังไม่ commit/push:
- `sw.js` : v233 → **v239** (ค้าง)
- `WIBWUB_Affiliate_Dashboard.html` (แก้ ~136 บรรทัด)
- `WIBWUB_Mobile.html`
- `Data Shipnity/Sales_Dashboard.html` (อยู่นอก push_now.command — ดูข้อ 5)

**ผู้ใช้ต้องดับเบิลคลิก `push_now.command` บนเครื่องจริง** เพื่อ commit + push (git push จาก sandbox ถูก block ด้วย proxy 403)

### 4. หมายเหตุที่ควรตรวจ (ไม่ได้แก้ในรอบนี้)
- ตัวเลข GMV เดือน มิ.ย. ไม่ตรงกันระหว่าง 2 ไฟล์: `AF_GMV[Jun]=฿375,789` (Affiliate Dashboard) แต่ Mobile = `฿437,951` แนะนำให้ตรวจว่าควรเป็นค่าใด ก่อน push — ไม่แก้อัตโนมัติเพราะ mapping ไม่ชัดและเสี่ยง corrupt
- `push_now.command` มี commit message อ้าง "sw v236 / 436.6K" ซึ่ง stale (เนื้อไฟล์ที่ push จริงถูกต้อง แต่ข้อความ commit เก่า)

### 5. push_now.command ไม่ครอบคลุม Sales_Dashboard
สคริปต์ add แค่ Affiliate Dashboard + Mobile + sw.js — `Data Shipnity/Sales_Dashboard.html` ที่แก้ค้างจะไม่ถูก push ด้วย ถ้าต้องการ push ด้วยให้เพิ่มไฟล์นั้นใน git add

### ข้อเสนอแนะ
ตั้ง schedule ให้รัน **วันละครั้งช่วงเช้าตรู่** ก็พอ และเพิ่มขั้นตอน auto-push (หรือเตือนให้ push) เพราะตอนนี้ data ถูกอัปเดตทุกวันแต่ไม่เคยขึ้น GitHub มาตั้งแต่ 23 มิ.ย.
