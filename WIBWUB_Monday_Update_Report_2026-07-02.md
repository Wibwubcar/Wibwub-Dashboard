# WIBWUB Weekly Update — พฤ. 2 ก.ค. 2026 (automated run)

## สรุป: ไม่มีข้อมูลใหม่ในขอบเขต task — ไม่ commit เพิ่ม | แก้ regression ที่ guardrail จะสร้าง (M5)

รอบนี้ทำงานร่วมกับ auto-update daemon ที่กำลังแก้ไฟล์เดียวกันอยู่ (working tree มี change ของ daemon ค้างอยู่: followers, sw.js v305, affiliate June 1–29 sync, push_now.command) จึงเลือกแนวทาง **minimal-touch + verify + report** เพื่อเลี่ยง race/regression ตามที่รายงาน 29 มิ.ย. เตือนไว้

---

## การตัดสินใจสำคัญ: ย้อน M5 กลับเป็น 6 เดือน (deviate จาก guardrail)

Guardrail script ใน SKILL สั่งให้ตั้ง `M5` = `required_months` = 7 (เพราะเดือนนี้ = ก.ค.) ผมรันแล้วมันเพิ่ม `"ก.ค."` เข้าไป **แต่ได้ย้อนกลับเป็น 6 เดือน** ด้วยเหตุผล:

- ทุก data array (`SH_REV`, `TK_REV`, `SH_ORD`, `TOTAL_REV` ฯลฯ) มี **6 element (ม.ค.–มิ.ย.)** เท่านั้น
- โค้ด chart/table ใช้ `M5.map((m,i)=>SH_REV[i]...)` ตรง ๆ → ถ้า M5 มี 7 label แต่ data มี 6 → index 6 = `undefined`/`NaN` → **แถบยอดขาย + ตารางเดือน ก.ค. จะเพี้ยน**
- commit วันนี้ `52bde2c` ("June arrays ครบ 6 เดือน") ตั้งใจคุมให้เป็น 6 เดือนอยู่แล้ว
- 3 รอบล่าสุด (30 มิ.ย., 1 ก.ค.) ก็คง M5 = 6 → ธรรมเนียมจริงคือ "เพิ่ม label เมื่อมีข้อมูลเดือนนั้นแล้วเท่านั้น"
- ข้อมูลยอดขาย ก.ค. มาจาก Google Sheets (นอกขอบเขต Monday task) และ ก.ค. เพิ่งผ่านไป 2 วัน → ยังไม่มีข้อมูล

ผลลัพธ์: `WIBWUB_Mobile.html` กลับมา **byte-identical กับ HEAD**; `WIBWUB_Dashboard.html` เหลือเฉพาะ change ของ daemon (follower 27.075→27.083)

---

## ผลตรวจแต่ละ STEP

### STEP 1 — Shipnity download ✅ มีอยู่แล้ว
`Data Shipnity/Data_กรกฎาคม.xlsx` ถูกดาวน์โหลดวันนี้แล้ว (2 ก.ค. 01:07, 1.1MB) — ไม่รัน Chrome ซ้ำ

### STEP 2 — Affiliate download ⏸️ ไม่มีข้อมูลใหม่
TikTok Affiliate data ยัง lag — รายงาน 1 ก.ค. ยืนยันว่าวันที่ 30 มิ.ย. ยัง greyed out และ ก.ค. ยังปิด (ข้อมูลถึงแค่ 29 มิ.ย.) ไฟล์ล่าสุด = `Transaction_Analysis_Creator_List_20260601-20260627.xlsx` การ export ซ้ำจะได้ตัวเลขเดิม จึงไม่โหลด (เลี่ยงชน daemon ที่กำลังแก้ Affiliate_Dashboard.html)

### STEP 3 — Top Products (Shipnity) ✅ current (daemon ดูแลสดกว่า)
`ALL_PRODUCTS` ใน Mobile: Wool Duster = **฿5,163,381** สูงกว่าค่ารอบ 29 มิ.ย. (฿5,156,807) → daemon อัปเดตสดด้วยข้อมูล ก.ค. แล้ว การ overwrite ด้วยผลคำนวณเก่ากว่าจะเป็นการถอยข้อมูล จึง **ไม่แก้** (aggregate เต็มไฟล์ใหญ่ทุกไฟล์ timeout — ไม่จำเป็นเพราะ dashboard สดอยู่แล้ว)

### STEP 4 — Affiliate arrays ✅ current ถึง 29 มิ.ย. (ล่าสุดที่มี)
`AFI_GMV/NET/COMM` ใน Mobile index 7 (= มิ.ย., เพราะ `AFI_MONTHS` เริ่มที่ พ.ย.68) = **607,557 / 598,495 / 75,273** ตรงกับ Creator List 1–29 มิ.ย. เป๊ะ daemon กำลัง sync `WIBWUB_Affiliate_Dashboard.html` จาก 1–28 → 1–29 (uncommitted) ให้ตรงกันอยู่แล้ว ยังไม่มี index ก.ค. เพราะข้อมูลยังไม่เปิด (ถ้าเพิ่มตอนนี้จะ premature)

> หมายเหตุ index: SKILL เขียนสูตร `month_idx = month-1` แต่ **ไม่ตรง** กับ `AFI_MONTHS` จริง (เริ่ม พ.ย.2025 → มิ.ย. = index 7, ก.ค. = index 8) อย่าใช้สูตร month-1 กับ AFI arrays

### STEP 5 — sw.js + commit ⏸️ ไม่ commit เพิ่ม
daemon bump `sw.js` เป็น **v305** และเขียน `push_now.command` ใหม่ (commit followers) ไว้แล้ว การ commit ทับตอนนี้จะพัน change ของ daemon + เสี่ยง race ตามที่รายงาน 29 มิ.ย. เตือน จึงไม่ commit (ตาม precedent เดิม)

---

## สถานะ repo ตอนจบ
- HEAD = `08dd087` (auto-update: Stock forecast 2026-07-02)
- working tree มีเฉพาะ change ของ **daemon** (ผมไม่เพิ่ม net change ใด ๆ):
  - `WIBWUB_Dashboard.html` — follower 27083 (daemon)
  - `WIBWUB_Affiliate_Dashboard.html` — sync มิ.ย. 1–29 (daemon)
  - `sw.js` — v305 (daemon)
  - `push_now.command` — followers commit (daemon)
- `WIBWUB_Mobile.html` — สะอาด ตรง HEAD

## ข้อเสนอแนะ
- ปล่อยให้ daemon/`push_now.command` จัดการ commit+push change ของมันเอง
- เมื่อข้อมูล 30 มิ.ย. เปิด (คาด 1–2 วัน) รันปิดยอด มิ.ย. เต็มเดือน 1–30 (→ AFI index 7)
- เมื่อ Google Sheets มียอดขาย ก.ค. แล้ว ค่อยเพิ่ม M5 = 7 พร้อม append element ที่ 7 ให้ทุก sales array
- root cause ควรแก้: guardrail M5 ไม่ควร "เพิ่ม label เดือนที่ยังไม่มี data array" — ควรผูกกับความยาว `SH_REV` แทน `today.month`
