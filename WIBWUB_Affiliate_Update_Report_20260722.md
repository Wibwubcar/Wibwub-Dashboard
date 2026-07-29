# WIBWUB Affiliate Update — วันพุธ 22 ก.ค. 2569 (automated run, wibwub-thursday-affiliate)

**สรุป: ดาวน์โหลดและอัปเดตข้อมูล Affiliate ครบ 4 ไฟล์ (ครีเอเตอร์/สินค้า/วิดีโอ/ไลฟ์สตรีม) ช่วง 1–20 ก.ค. 2569 เข้า `WIBWUB_Affiliate_Dashboard.html` และ `WIBWUB_Mobile.html` แล้ว, bump sw.js เป็น v439, อัปเดต `push_now.command` — ทุกอย่างแก้ไว้บนดิสก์แล้ว ยังไม่ push ขึ้น GitHub (ต้องดับเบิลคลิก push_now.command เอง)**

---

## ✅ สิ่งที่ทำสำเร็จ

### 1. ดาวน์โหลดไฟล์ export จาก TikTok Affiliate Center
ตั้งช่วงวันที่ 01/07/2026–20/07/2026 (ทั้งตัวกรองบนสุดและในส่วน "รายละเอียด") แล้ว export/ดาวน์โหลดครบ 4 ไฟล์ — ครีเอเตอร์ (497KB), สินค้า (19KB), วิดีโอ (1.76MB), ไลฟ์สตรีม (67KB) — LaunchAgent ย้ายเข้าโฟลเดอร์ `Data Affiliate/{ครีเอเตอร์,สินค้า,วีดีโอ,ไลฟ์สตรีม}/` ให้อัตโนมัติ

### 2. อัปเดตข้อมูลครีเอเตอร์ (ก.ค. 1-20)
- `WIBWUB_Affiliate_Dashboard.html`: overwrite ค่าสุดท้ายของ AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR เป็น "ก.ค. (1-20)" → GMV ฿1,027,426 · Net ฿1,011,992 · Comm ฿118,073 · ครีเอเตอร์ 576 ราย
- `WIBWUB_Mobile.html`: overwrite AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM ชุดเดียวกัน + อัปเดตการ์ด KPI hardcoded (`฿975K` → `฿1,027K`, `547 creators` → `576 creators`, label → `กค.69 (1-20)`)
- อัปเดต KPI strip 3 การ์ดใน dashboard (Affiliate GMV, Net GMV, ค่าคอมมิชชั่น) เป็นตัวเลขและ label ช่วงวันที่ใหม่

### 3. อัปเดต PRODUCTS[].vid (สินค้า)
Fuzzy-match ชื่อสินค้าทั้ง 7 รายการกับไฟล์ export สินค้า แล้วอัปเดตจำนวนวิดีโอ (คอลัมน์ "วิดีโอ" ตรงตัว) ของช่วง 1-20 ก.ค.:
Leather Wipes 141→107, Interior Wipes 75→56, Sugar 115→93, Cleaner 18→15, Interior 70→55, Refresh 29→26, Visible 12→11
(ตัวเลขลดลงทุกตัวเพราะไฟล์นี้ให้ข้อมูลเฉพาะช่วงที่เลือก ไม่ใช่ยอดสะสมตลอดกาลเหมือนฟิลด์ gmv/monthly)

### 4. ประมวลผลไฟล์วิดีโอ (inlineStr XML)
Parse ด้วย zipfile+regex ได้ 5,261 แถวข้อมูล (ผ่าน safety check ไม่ใช่ 0 แถว) → match ด้วย vid_id กับ `VIDEOS` array เดิม (769 รายการ) → อัปเดตยอด GMV เดือน ก.ค. (`monthly.jul`) และคำนวณ `gmv` รวมใหม่ให้ 68 รายการที่มีข้อมูลเปลี่ยนแปลง (8.8% ของทั้งหมด — ผ่าน safety check ไม่เกิน 50%) ตรวจสอบ syntax ผ่าน `node -e` แล้วว่าไฟล์ยัง valid

### 5. Bump เวอร์ชัน + สคริปต์ push
- `sw.js`: `wibwub-v438` → `wibwub-v439`
- อัปเดต `push_now.command` ให้ทำ `git add` + `git commit` + `git push` ครบ (ของเดิมมีแค่ push อย่างเดียว ไม่ commit ให้)
- ตรวจ JS syntax ของทั้ง `WIBWUB_Affiliate_Dashboard.html` และ `WIBWUB_Mobile.html` ผ่าน node แล้ว ไม่มี error

---

## ⛔ สิ่งที่ทำไม่ได้ / ต้องตรวจสอบเพิ่ม (ambiguous — ไม่แตะเพื่อความปลอดภัย)

1. **การ์ด "ครีเอเตอร์ที่มียอด" (13,945)** ใน dashboard บรรทัด ~270: ตัวเลขนี้ไม่ตรงกับจำนวนครีเอเตอร์ (576), จำนวนออเดอร์รวม (6,762), หรือจำนวนหน่วยขาย (7,047) จากไฟล์ครีเอเตอร์ — ไม่ทราบที่มาที่แน่ชัด จึงปล่อยค่าเดิมไว้ ไม่แก้
2. **PRODUCTS[].cr (จำนวนครีเอเตอร์ต่อสินค้า)**: ไฟล์ export สินค้าไม่มีคอลัมน์ "จำนวนครีเอเตอร์รวม" ตรงๆ มีแค่ "ครีเอเตอร์ที่มียอดขายเฉลี่ยรายวัน" (1-34 ราย) ซึ่งสเกลต่างจากค่าเดิมในระบบ (11-239 ราย) มาก ไม่กล้าเดาแล้วเขียนทับ — ปล่อยค่าเดิมไว้ทั้ง 7 รายการ
3. **การ์ด "สินค้าที่ Active" subtitle "ผ่าน 514 creators"** (บรรทัด 337): เกี่ยวโยงกับ ambiguity ข้อ 2 — ปล่อยไว้เช่นกัน
4. **ไฟล์ค้างใน Downloads**: `View Report-2026-07-01-2026-07-22.xlsx` (~30KB) เป็นไฟล์ export สินค้าชุดก่อนที่ไม่ตรง pattern ของ LaunchAgent เลยไม่ถูกย้าย — ไม่ได้ลบให้ (รอการยืนยัน)
5. พบว่าไฟล์อื่นในโฟลเดอร์ (`build_snapshot_tmp.py`, `Data Shipnity/stock/stock_snapshot.json`, `data content/Followers_wibwubcar.zip`, `scripts/auto_push.log`) มีการเปลี่ยนแปลงอยู่ก่อนแล้วจากงานอัตโนมัติอื่น (ไม่ใช่งานนี้) — ไม่ได้แตะต้อง

---

## 📊 สถานะ dashboard ปัจจุบัน (หลังแก้ไข)
- Affiliate ก.ค. (1-20): GMV ฿1,027,426 · Net ฿1,011,992 · Comm ฿118,073 · ครีเอเตอร์ 576 ราย
- VIDEOS array: 769 รายการ (68 อัปเดตยอด ก.ค., 3 รายการไม่มีข้อมูลใหม่ในไฟล์นี้)
- sw.js = v439, ยังไม่ commit/push

## ▶️ ขั้นถัดไป (แนะนำ)
1. ดับเบิลคลิก `push_now.command` เพื่อ commit + push ขึ้น GitHub
2. ตรวจสอบที่มาของตัวเลข 13,945 และ 514 creators โดยตรงจากหน้า TikTok Affiliate Center UI (อาจเป็นยอดสะสมตลอดกาลจากหน้า Overview คนละหน้ากับไฟล์ export ที่ใช้อยู่)
3. พิจารณาลบไฟล์ `View Report-2026-07-01-2026-07-22.xlsx` ใน Downloads ถ้าไม่ได้ใช้แล้ว
