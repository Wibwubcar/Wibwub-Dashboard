# WIBWUB Weekly Update — วันจันทร์ 20 ก.ค. 2569 (automated run, wibwub-monday-update)

**สรุป: พบและแก้บั๊กข้อมูล Affiliate ที่ถูกโปรแกรมอัตโนมัติตัวอื่นเขียนทับผิดเมื่อเช้านี้ (ค่าคอมมิชชั่นเหลือ ฿9 ทั้งเดือน) กลับเป็นค่าที่ถูกต้อง + รีเฟรช Top Products ด้วยไฟล์ Shipnity ฉบับสมบูรณ์ 1-20 ก.ค. — commit แล้วบนดิสก์ (4212ac5), ยังไม่ push**

---

## ✅ สิ่งที่ทำสำเร็จ

### 1. ตรวจสอบ M5 array (Protection check)
ตรวจแล้วถูกต้องอยู่แล้ว (7 รายการ ตรงกับเดือนกรกฎาคม) — ไม่ต้องแก้

### 2. พบและแก้บั๊ก **Affiliate GMV/Net/Comm/Creators corruption**
- Chrome export "Transaction Analysis" ของ TikTok ค้างที่สถานะกำลังประมวลผล (spinner) นานเกิน 130 วินาที ไม่มีไฟล์ตกลงมาเลย แม้ retry แล้ว
- ระหว่างตรวจสอบ พบว่า commit `d759265` (เช้านี้ 02:31 UTC) ได้ตั้งค่า Affiliate เดือน ก.ค. (1-19) ไว้ถูกต้องแล้ว: **GMV ฿974,988 · Net ฿915,161 · Comm ฿111,799 · ครีเอเตอร์ 13,945 ราย** (ตรงกับ `_report_2026-07-20.md` ที่มีอยู่แล้วในโฟลเดอร์ Data Affiliate)
- แต่ commit ถัดมา `1d89290` ("auto: update 2026-07-20 18:13" — จากบอทตัวอื่น ไม่ใช่งานนี้) เขียนทับค่าเหล่านี้ผิดเพี้ยน: **Comm เหลือแค่ ฿9** (เป็นไปไม่ได้สำหรับยอดขายทั้งเดือน ฿974,846), Net กลายเป็น ฿948,283 (สูงกว่า GMV−returns เดิม ผิดตรรกะ), ครีเอเตอร์เหลือ 547 ราย
- **แก้ไข**: คืนค่า `AF_GMV/AF_NET/AF_COM/AF_CR` ใน `WIBWUB_Affiliate_Dashboard.html` และ `AFI_GMV/AFI_NET/AFI_COMM` ใน `WIBWUB_Mobile.html` กลับเป็นค่าที่ถูกต้อง (974988 / 915161 / 111799 / 13945) — ไม่ได้แตะตาราง per-creator หรือ VIDEOS array เพราะไม่มีหลักฐานว่าเสีย

### 3. รีเฟรช Top Products จากไฟล์ Shipnity ฉบับสมบูรณ์
- Chrome download ของ Shipnity ก็มีปัญหาเช่นกัน (ตามที่บันทึกไว้ก่อนหน้า) แต่พบว่ามีไฟล์ `Data Shipnity/Data_20-07-2026.xlsx` ที่สมบูรณ์อยู่แล้ว (จากกระบวนการอื่นเมื่อ 01:47 น.) — 21,491 แถว ครอบคลุมออเดอร์ AL2685–AM8586 (1–20 ก.ค. เต็ม ไม่มีช่องว่าง)
- คำนวณยอดขาย ก.ค. MTD (1-20) ใหม่สำหรับสินค้าหลัก 15 รายการที่ระบบติดตาม (dedupe ด้วย date+order+qty+code) แล้วอัปเดต `PROD_MO[].mo[6]` และ `ALL_PRODUCTS` (v + ลำดับใหม่ตามยอดขาย) ใน `WIBWUB_Mobile.html`
- อัปเดตการ์ด KPI "สินค้าขายดีสุด" ใน `WIBWUB_Dashboard.html` (จำนวนชิ้น 8,634 ให้ตรงกับ ALL_PRODUCTS)
- ยอดขายรวม 15 สินค้าหลัก ก.ค. MTD = ฿3,505,097 จากยอดขายรวมทั้งหมด (141 สินค้า) ฿5,448,487 — สัดส่วนสมเหตุสมผล (~64%)

### 4. Bump เวอร์ชัน + Commit
- `sw.js`: `wibwub-v425` → `wibwub-v426`
- iframe cache-bust ใน `WIBWUB_Dashboard.html`: `?v=263` → `?v=264`
- Commit `4212ac5`: 4 ไฟล์ (WIBWUB_Affiliate_Dashboard.html, WIBWUB_Dashboard.html, WIBWUB_Mobile.html, sw.js)
- ตรวจ JS syntax ของทั้ง 3 ไฟล์ HTML ผ่าน node — ไม่มี syntax error
- `push_now.command` มีอยู่แล้วและถูกต้อง (clear lock files + push) ไม่ต้องแก้

---

## ⛔ สิ่งที่ทำไม่ได้ / ข้อจำกัด

1. **TikTok Affiliate Transaction Analysis export**: ค้างที่สถานะ async processing นานเกิน 130 วินาที (เกินเวลาที่คาดไว้ 60-90 วิ) ไม่มีไฟล์ตกลงมา แม้ retry แล้ว — ใช้ค่าที่ยืนยันแล้วจากประวัติ git แทนการดาวน์โหลดใหม่
2. **จำนวนชิ้น (q) ของ Top Products**: อัปเดตเฉพาะยอดขาย (revenue) ไม่ได้อัปเดต q เนื่องจากไม่มี array ประวัติจำนวนชิ้นรายเดือนให้อ้างอิง การประมาณจำนวนชิ้นที่เพิ่มขึ้นเฉพาะสัปดาห์นี้แบบแม่นยำทำไม่ได้โดยไม่เดา — ทิ้งไว้ตามเดิม
3. **กราฟ pr_top10 (Top 10 by channel)** ใน WIBWUB_Dashboard.html: ไม่ได้แตะ เพราะเป็นข้อมูลสะสม ม.ค.–ก.ค. แยกตามช่องทางขาย ซึ่งต้องมีไฟล์ดิบของเดือน ม.ค.–มิ.ย. ครบทุกเดือนถึงจะคำนวณใหม่ได้แม่นยำ — มีเฉพาะไฟล์ ก.ค. ในรอบนี้

---

## 📊 สถานะ dashboard ปัจจุบัน (หลังแก้ไข)
- Affiliate ก.ค. (1-19): GMV ฿974,988 · Net ฿915,161 · Comm ฿111,799 · ครีเอเตอร์ 13,945 ราย
- Top Products ก.ค. MTD (1-20): อันดับ 1 Wool Duster ฿227,825 (สะสม ฿5,401,299) รองลงมา Sugar 500ml, Interior 500ml, Interior Wipe, Refresh 500ml, Refresh Wipes, Spot Clean, Perfect, Reflex, Tire&Trim, Sugar 3L, Martini, X-Glass, Quartz Shampoo, Mind Detailer
- sw.js = v426, commit `4212ac5` พร้อม push

## ▶️ ขั้นถัดไป (แนะนำ)
1. รัน `push_now.command` เพื่อ push ขึ้น GitHub
2. **สำคัญ**: มีบอทอัตโนมัติตัวอื่น ("auto: update" — ไม่ใช่ wibwub-monday-update) เขียนทับข้อมูล Affiliate ผิดพลาดระหว่างวันซ้ำแล้วซ้ำเล่า ควรตรวจสอบว่าสคริปต์นั้นใช้ชื่อตัวแปรถูกต้องหรือไม่ (ปัญหาเดิมที่เคยพบ: gmvD/netD/commD ไม่มีอยู่จริง) ก่อนที่จะเขียนทับค่าที่ถูกต้องซ้ำอีกในรอบถัดไป
3. หาก TikTok export ยังค้างซ้ำอีกในสัปดาห์หน้า อาจพิจารณาลด date-range หรือ export เฉพาะบางส่วนแทนทั้งเดือน
