# WIBWUB Weekly Update — วันอังคาร 21 ก.ค. 2569 (รันอัตโนมัติ, wibwub-monday-update)

**สรุป: พบและแก้บั๊ก Affiliate data corruption ซ้ำเป็นครั้งที่ 3 (bot อื่นเขียนทับ AF_GMV/NET/COM/CR กลับไปเป็นค่าผิดอีกครั้ง) + รีเฟรช Top Products จาก Shipnity ฉบับใหม่ 1-21 ก.ค. — commit แล้ว (3b82a17), ยังไม่ push**

---

## ✅ สิ่งที่ทำสำเร็จ

### 0. ตรวจสอบ M5 array (Protection check)
ตรวจแล้วถูกต้องอยู่แล้ว (7 รายการ ตรงกับเดือนกรกฎาคม) ทั้งใน WIBWUB_Dashboard.html และ WIBWUB_Mobile.html — ไม่ต้องแก้

### 1. Export Shipnity สำเร็จ
Export จาก shipnity.com (มุมมอง "สินค้าในออเดอร์") สำเร็จ → `Data Shipnity/Data_21-07-2026.xlsx` (21,358,506 bytes) และคัดลอกทับ `Data Shipnity/Data_กรกฎาคม.xlsx` — ครอบคลุมออเดอร์ AL2689–AM999, วันที่ 1–21 ก.ค. (22,683 แถว)

### 2. พบและแก้บั๊ก **Affiliate GMV/Net/Comm/Creators corruption (ครั้งที่ 3)**
- ก่อนเริ่มงาน ตรวจพบว่า `AF_GMV/AF_NET/AF_COM/AF_CR` ใน WIBWUB_Affiliate_Dashboard.html และ `AFI_GMV/AFI_NET/AFI_COMM` ใน WIBWUB_Mobile.html ถูกเขียนทับผิดอีกครั้งโดย bot อื่น (ไม่ใช่ task นี้) หลังจากที่ถูกแก้ไปแล้วเมื่อ 20 ก.ค. (commit `4212ac5`)
- ค่าที่พบผิด: GMV=974,846 / NET=960,624 / COM=111,628 / **CR=547** ⚠️ (ตัวเลข creator=547 ตรงกับรูปแบบบั๊กที่เคยพบและยืนยันว่าผิดมาก่อนแล้วในรอบ 20 ก.ค.)
- นอกจากนี้ยังพบว่าการ์ด KPI "ครีเอเตอร์ที่มียอด" (บรรทัด kstrip) ค้างค่า 547 ไม่ตรงกับการ์ด GMV/Net/Comm ข้างเคียงที่ยังแสดงค่าถูกต้อง (฿975K/฿915K/฿112K) — ยืนยันว่าเป็นการเขียนทับ JS array เท่านั้น ไม่ได้แตะ static KPI div
- **แก้ไข**: คืนค่าที่ยืนยันถูกต้องแล้ว (GMV 974,988 / NET 915,161 / COM 111,799 / CR 13,945) กลับเข้าไปใน `AF_GMV/AF_NET/AF_COM/AF_CR`, `AFI_GMV/AFI_NET/AFI_COMM`, และการ์ด KPI ครีเอเตอร์ — ไม่มีข้อมูลใหม่กว่านี้ให้ใช้ (ดู step 2b ด้านล่าง)

### 2b. TikTok Affiliate Transaction Analysis export — ล้มเหลว (ค้างสถานะ)
- สั่ง export ช่วง 01/07/2026–19/07/2026 (ตัวเลือกวันที่ล่าสุดที่ระบบเปิดให้เลือกได้ — วันที่ 19 ก.ค. เป็น ceiling เดียวกับที่ระบบแสดง "อัปเดตเมื่อ: 19 ก.ค. 2026")
- รอ >3 นาที (เกิน worst-case เดิมที่เคยเจอ 60-130 วิ) สถานะยังค้างที่ "กำลังส่งออก" ไม่ขยับ
- เนื่องจาก data ceiling ของ TikTok ยังอยู่ที่ 19 ก.ค. เท่าเดิม (เท่ากับช่วงที่ข้อมูลที่ยืนยันแล้วครอบคลุมอยู่แล้ว) จึงไม่มีข้อมูลใหม่กว่านี้ที่จะได้จากการรอต่อ — ยกเลิกการรอและใช้ค่าที่ยืนยันแล้วแทน (ดู step 2)

### 3. รีเฟรช Top Products จากไฟล์ Shipnity ฉบับใหม่ (1-21 ก.ค.)
- Parse `Data_กรกฎาคม.xlsx` (22,683 แถว, dedupe ด้วย วันที่สร้าง+เลขที่ออเดอร์+จำนวน+รหัสสินค้า)
- **Validate mapping ก่อนอัปเดต**: คำนวณยอดขายผ่านข้อมูลถึงวันที่ 19 ก.ค. เทียบกับ mo[6] เดิม (baseline ที่ยืนยันแล้วจากรอบก่อน) — พบว่าตรงกันภายใน 0.3-2% ทุก 15 สินค้า (ส่วนต่างเล็กน้อยสมเหตุสมผลจากออเดอร์ใหม่ที่เพิ่มเข้ามา) ยืนยันว่า code mapping ถูกต้อง รวมถึงยืนยันว่า "Reflex Ceramic Coating" = รวมโค้ด SRFX000003 (250ml) + SRFX110003 (500ml) ไม่รวม SRFX030003 (3L)
- อัปเดต `PROD_MO[].mo[6]` (ก.ค. MTD 1-21) และ `ALL_PRODUCTS` (v ใหม่ + จัดลำดับใหม่ตามยอดขาย) ใน `WIBWUB_Mobile.html`
- อัปเดตการ์ด KPI "สินค้าขายดีสุด" ใน `WIBWUB_Dashboard.html`: ฿5.40M → ฿5.41M (จำนวนชิ้น 8,634 คงเดิม — ยังไม่มี array ประวัติจำนวนชิ้นรายเดือนให้อัปเดตแม่นยำ)
- ยอดขายรวม 15 สินค้าหลัก ก.ค. MTD (1-21) = ฿3,694,416 จากยอดขายรวมทั้งหมด (141 สินค้า) ฿5,749,186 — สัดส่วน 64.3% (สอดคล้องกับสัดส่วน ~64% ของรอบก่อน)
- อันดับเปลี่ยนเล็กน้อย: Refresh Wipes และ Refresh สลับอันดับ 5-6, Mind Detailer แซง Quartz Shampoo ขึ้นอันดับ 14 (ส่วนต่างน้อยกว่า 0.1%)

### 4. Bump เวอร์ชัน + Commit
- `sw.js`: `wibwub-v434` → `wibwub-v435`
- iframe cache-bust ใน `WIBWUB_Dashboard.html`: `?v=265` → `?v=266`
- Commit `3b82a17`: 4 ไฟล์เท่านั้น (WIBWUB_Affiliate_Dashboard.html, WIBWUB_Dashboard.html, WIBWUB_Mobile.html, sw.js) — ไม่แตะไฟล์อื่นที่มีการเปลี่ยนแปลง/untracked จาก task อื่นในโฟลเดอร์เดียวกัน
- ตรวจ JS syntax ของทั้ง 3 ไฟล์ HTML ผ่าน node — ไม่มี syntax error
- `push_now.command` มีอยู่แล้วและถูกต้อง (clear lock files + push) ไม่ต้องแก้

---

## ⛔ สิ่งที่ทำไม่ได้ / ข้อจำกัด

1. **TikTok Affiliate Transaction Analysis export**: ค้างสถานะ "กำลังส่งออก" นานเกิน 3 นาที ไม่มีไฟล์ตกลงมา — ใช้ค่าที่ยืนยันแล้วจากประวัติแทน (data ceiling ยังอยู่ 19 ก.ค. เท่าเดิม ดังนั้นไม่เสียข้อมูลใหม่)
2. **จำนวนชิ้น (q) ของ Top Products**: อัปเดตเฉพาะยอดขาย (revenue) เหมือนรอบก่อน ไม่ได้อัปเดต q เนื่องจากไม่มี array ประวัติจำนวนชิ้นรายเดือนให้อ้างอิง
3. **กราฟ pr_top10 (Top 10 by channel)** ใน WIBWUB_Dashboard.html: ไม่ได้แตะ (เหมือนรอบก่อน) เพราะเป็นข้อมูลสะสมที่ต้องมีไฟล์ดิบทุกเดือน ม.ค.–มิ.ย. ครบถึงจะคำนวณใหม่ได้แม่นยำ

---

## 📊 สถานะ dashboard ปัจจุบัน (หลังแก้ไข)
- Affiliate ก.ค. (1-19): GMV ฿974,988 · Net ฿915,161 · Comm ฿111,799 · ครีเอเตอร์ 13,945 ราย
- Top Products ก.ค. MTD (1-21): อันดับ 1 Wool Duster ฿240,831 (สะสม ฿5,414,305) รองลงมา Sugar 500ml, Interior 500ml, Interior Wipe, Refresh Wipes, Refresh 500ml, Spot Clean, Perfect, Reflex, Tire&Trim, Sugar 3L, Martini, X-Glass, Mind Detailer, Quartz Shampoo
- sw.js = v435, commit `3b82a17` พร้อม push

## ▶️ ขั้นถัดไป (แนะนำ)
1. รัน `push_now.command` เพื่อ push ขึ้น GitHub
2. **สำคัญ (แจ้งซ้ำเป็นครั้งที่ 3)**: มีบอทอัตโนมัติตัวอื่น ("auto: update" — ไม่ใช่ wibwub-monday-update) เขียนทับข้อมูล Affiliate ผิดพลาดซ้ำแล้วซ้ำเล่าทุกสัปดาห์ (18/19 ก.ค.: PRODUCTS cr/vid, 20 ก.ค.: AF_COM=9, 21 ก.ค.: AF_CR=547 อีกครั้ง) ควรตรวจสอบ scope/ตัวแปรของสคริปต์นั้นอย่างเร่งด่วนก่อนที่ปัญหาจะเกิดซ้ำในรอบถัดไป
3. หาก TikTok export ยังค้างซ้ำอีกในสัปดาห์หน้า อาจพิจารณาลด date-range หรือ export เฉพาะบางส่วนแทนทั้งเดือน
