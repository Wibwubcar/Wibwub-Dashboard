# WIBWUB Weekly Update — วันพฤหัสบดี 23 ก.ค. 2569 (รันอัตโนมัติ, wibwub-monday-update)

---

## ✅ สิ่งที่ทำสำเร็จ

### 0. ตรวจสอบ M5 array (Protection check)
ตรวจแล้วถูกต้อง (7 รายการ ตรงเดือนกรกฎาคม) ทั้ง WIBWUB_Dashboard.html และ WIBWUB_Mobile.html — ไม่ต้องแก้

### 1. Export Shipnity + รีเฟรช Top Products
- Export ข้อมูล Shipnity เดือนปัจจุบัน (month-to-date) → `Data_23-07-2026.xlsx` → คัดลอกทับ `Data_กรกฎาคม.xlsx` (finalized month file)
- ยืนยันแล้วว่าไฟล์ยังเป็น product-level (มีคอลัมน์ 'สินค้า' จริง) — Mistake #10 ในเอกสาร SKILL (ไฟล์เปลี่ยนเป็น order-level ตั้งแต่ พ.ค. 2569) **ไม่กระทบไฟล์นี้**
- Parse ไฟล์ Shipnity ทั้ง 7 เดือน (ม.ค.–ก.ค.) ด้วย dedupe key (เลขออเดอร์, รหัสสินค้า, จำนวน) ตามสูตรมาตรฐาน
- เพิ่ม logic **แยกช่องทางการขาย** (Shopee/TikTok/Lazada/Facebook/Line Shopping/LINE OA/Website/Carcare/อื่นๆ) และตัดยอด "เบิกของ"/"สินค้าสำหรับทำการตลาด" ออกจากยอดขายจริง (ของแจก ไม่ใช่ยอดขาย) — ตัดออกรวม ฿441,117 ตลอด 7 เดือน
- อัปเดต `ALL_PRODUCTS` + `PROD_MO` (WIBWUB_Mobile.html) และตาราง/กราฟแท่ง/กราฟโดนัท Top 15 สินค้าขายดี พร้อม breakdown ช่องทาง (WIBWUB_Dashboard.html)
- **อันดับ 1 ยังเป็น Wool Duster ฿5.42M (8,490 ชิ้น)**
- ยอดขายรวมทั้งหมด = ฿52.82M / 205,282 ชิ้น (สะสม 7 เดือน ม.ค.–ก.ค. 2569)

### 2. TikTok Affiliate Creator List Export
- ตั้งช่วงวันที่กำหนดเอง 2026-07-01 ถึง 2026-07-22 (วันที่ 23 ยังเลือกไม่ได้ในปฏิทิน — cutoff ข้อมูลอยู่ที่ 22 ก.ค.)
- Export ค้างสถานะ "กำลังส่งออก" นานผิดปกติ (ยาวนานตลอดช่วงทำ STEP 3) แต่ **ไม่ได้ล้มเหลวถาวร** — หลังรีเฟรชหน้า พบว่า export เดิมเสร็จแล้วในพื้นหลัง โหลดไฟล์ `Creator_List_20260701-20260722_20260723023246.xlsx` (15,370 แถว, 24 คอลัมน์) เข้า `Data Affiliate/ครีเอเตอร์/` สำเร็จ

### 3. อัปเดต Affiliate arrays จากข้อมูลจริง (1-22 ก.ค.)
คำนวณจากไฟล์ Creator List จริงด้วย pandas (openpyxl read_only อ่านไฟล์นี้ผิดพลาด — dimension tag เพี้ยน ต้องใช้ pandas แทน):
- GMV จากแอฟฟิลิเอต = ฿1,135,114.37
- GMV คืนเงิน = ฿67,288.93 → Net GMV = ฿1,067,825.44
- ค่าคอมมิชชั่นโดยประมาณ = ฿130,721.64
- ครีเอเตอร์ที่มียอดขาย (GMV > 0) = 625 ราย จาก 15,370 รายทั้งหมด

**หมายเหตุสำคัญ**: คอลัมน์จริงในไฟล์ export ล่าสุด **ไม่ตรงกับที่ SKILL_update-wibwub_v2.md ระบุไว้** — เอกสารบอกว่า Returns=คอลัมน์ 2, Commission=คอลัมน์ 10 แต่ตรวจสอบจริงพบว่า Returns อยู่คอลัมน์ 20 ('GMV ของการคืนเงินจากแอฟฟิลิเอต') และ Commission อยู่คอลัมน์ 7 ('ค่าคอมมิชชั่นโดยประมาณ') — ใช้ชื่อคอลัมน์จริงยืนยันก่อนคำนวณ ไม่อิงตำแหน่งคอลัมน์จากเอกสารเก่าตรงๆ (ควรอัปเดตเอกสาร SKILL ในรอบถัดไป)

อัปเดตเฉพาะ**ตำแหน่งเดือนปัจจุบัน** (ก.ค.) เปลี่ยน label จาก `"(1-21)"` → `"(1-22)"` — ไม่แตะค่าประวัติเดือน มี.ค.-มิ.ย. เลย:
- `AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR` ใน WIBWUB_Affiliate_Dashboard.html
- `AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM` ใน WIBWUB_Mobile.html
- นอกจากนี้ยังอัปเดตการ์ด KPI แบบ static text ("kstrip" ใน Affiliate Dashboard และ "mks-grid" ใน Mobile) ให้ตรงกับตัวเลขใหม่ — พบว่าการ์ดเหล่านี้ยังค้างอยู่ที่ "(1-21)" จากรอบก่อนหน้า ไม่ตรงกับ array จริง จึงแก้ให้สอดคล้องกันในรอบนี้

### 4. Bump เวอร์ชัน + Commit
- `sw.js`: `wibwub-v448` → `wibwub-v449`
- Commit `4485e49`: **4 ไฟล์เท่านั้น** (WIBWUB_Affiliate_Dashboard.html, WIBWUB_Dashboard.html, WIBWUB_Mobile.html, sw.js) — ไม่แตะไฟล์ untracked/modified อื่นจาก task อื่นในโฟลเดอร์เดียวกัน (เช่น build_snapshot_tmp.py, ไฟล์ zip ต่างๆ, scripts/auto_push.log)
- เจอ `.git/index.lock` ค้าง (ปกติของ mount นี้) — ใช้วิธี rename (mv) แทน rm ตามที่เคยได้ผลมาก่อน แล้ว commit ผ่านปกติ
- ตรวจ diff แล้วยืนยันว่าค่าประวัติของทั้ง AF_* และ AFI_* (ม.ค.–มิ.ย.) ไม่ถูกเขียนทับ (เปลี่ยนเฉพาะ element สุดท้าย)
- `push_now.command` มีอยู่แล้ว ปรับให้ commit เฉพาะ 4 ไฟล์ที่ถูกต้อง (เดิมไม่รวม WIBWUB_Dashboard.html) และ suppress error กรณีไม่มีอะไรให้ commit ซ้ำ

---

## ⛔ สิ่งที่ทำไม่ได้ / ข้อจำกัด

1. ยังไม่ push commit `4485e49` ขึ้น GitHub (sandbox push ตรงไม่ได้ ต้องรันจากเครื่อง — กด `push_now.command`)
2. จำนวนชิ้น (q) ของ Top Products อัปเดตเฉพาะยอดขาย ไม่ได้อัปเดต q รายเดือน (เหมือนทุกรอบก่อนหน้า — ไม่มี array ประวัติจำนวนชิ้นให้อ้างอิง)
3. ไม่ได้อัปเดต creator-level arrays (`CREATORS`, `KOLS_DATA`) ที่มีข้อมูล insight ต่อครีเอเตอร์รายตัว — เป็นข้อมูลที่ต้องคัดสรร/เขียน insight เอง ไม่ใช่ตัวเลขสรุปที่คำนวณอัตโนมัติได้ตรงไปตรงมา จึงปล่อยไว้ตามเดิมเพื่อความปลอดภัย
4. คอลัมน์จริงในไฟล์ Creator List ไม่ตรงกับเอกสาร SKILL_update-wibwub_v2.md (ดูหมายเหตุด้านบน) — แนะนำให้แก้เอกสารในรอบถัดไปเพื่อป้องกันความผิดพลาดซ้ำ

---

## 📊 สถานะ dashboard ปัจจุบัน (หลังแก้ไข)
- Top Products สะสม 7 เดือน (ม.ค.–ก.ค. 2569): Wool Duster ฿5.42M (8,490 ชิ้น) อันดับ 1, ยอดขายรวมทั้งหมด ฿52.82M / 205,282 ชิ้น
- Affiliate ก.ค. (1-22): GMV ฿1,135,114 · Net ฿1,067,825 · Commission ฿130,722 · ครีเอเตอร์ที่มียอด 625 ราย
- sw.js = v449, commit `4485e49` พร้อม push

## ▶️ ขั้นถัดไป (แนะนำ)
1. รัน `push_now.command` เพื่อ push commit `4485e49` ขึ้น GitHub
2. อัปเดต SKILL_update-wibwub_v2.md ให้ตรงกับคอลัมน์จริงของไฟล์ Creator List ปัจจุบัน (Returns=คอลัมน์ 20, Commission=คอลัมน์ 7) เพื่อป้องกัน task ในอนาคตอ่านผิดคอลัมน์
3. มีบอทอัตโนมัติหลายตัวทำงานบน repo เดียวกัน เห็น `.git/index.lock`/`tmp_obj` ค้างเป็นระยะ (ปกติของ mount นี้ แก้ด้วยการ rename แทน rm) — ควรพิจารณาจัด schedule ให้ไม่ทับเวลากันเพื่อลดความเสี่ยง race condition
