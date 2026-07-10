# WIBWUB Sales Sheet Update — พฤ. 2 ก.ค. 2026 09:30 (automated)

## สรุป: ไม่มีข้อมูลยอดขาย ก.ค. 2569 ใหม่ → ไม่ commit, ไม่แตะ arrays

### STEP 1 — อ่าน Google Sheets (Shopee / TikTok / Lazada) ✅
อ่านครบทั้ง 3 sheet ผ่าน Google Drive MCP แล้ว แต่ tab ที่ read_file_content คืนมาคือ
tab "Reports Campaign 2025" (ข้อมูลรายแคมเปญปี 2025 เท่านั้น ถึง พ.ย. 2025) —
**ไม่มี row ยอดสะสมรายเดือนของปี 2569 (2026)** ในผลที่อ่านได้ (MCP ไม่รองรับเลือก gid tab เฉพาะ)

ที่สำคัญกว่านั้น: **ก.ค. 2569 เพิ่งผ่านไป 2 วัน** พนักงานยังไม่ได้ปิดยอดรายเดือน
(รอบอัปเดตจริงคือ จ./พฤ.) จึงยังไม่มียอดสะสม ก.ค. ให้ลงไม่ว่าจะอ่าน tab ไหน

### STEP 2 — Map เข้า arrays ⏸️ ไม่มีค่าให้ map
ตรวจ arrays ปัจจุบันใน `WIBWUB_Dashboard.html`: ทุก array มี **6 element (ม.ค.–มิ.ย.) ครบและ length ตรงกันหมด**
(`M5, SH_REV, TK_REV, LZ_REV, SH_ORD, SH_CANCEL_PCT, SH_ADS, SH_FEE, TK_ADS, LZ_ADS, LZ_FEE, LZ_COUPON, LZ_COST_PCT` = 6 ทั้งหมด)
June ปิดครบแล้วที่ commit `52bde2c` / `3e85350` ไม่มีข้อมูลใหม่มา override

### STEP 2b — M5 guardrail: **จงใจคง M5 = 6 (ไม่ดันเป็น 7)**
Guardrail ใน SKILL สั่งให้ตั้ง M5 = required_months = 7 (เพราะเดือนนี้ ก.ค.)
แต่ **ไม่ทำ** เพราะ data array ทุกตัวยังมี 6 element — chart/table ใช้ `M5.map((m,i)=>SH_REV[i])`
ถ้า M5 = 7 label แต่ data = 6 → index 6 = NaN → แถบ/ตาราง ก.ค. เพี้ยน
ตรงกับ precedent ทุกรอบล่าสุด (30 มิ.ย., 1 ก.ค., และรอบ 02:44 วันนี้): เพิ่ม label เฉพาะเมื่อมี data เดือนนั้นแล้ว

### STEP 3 — KPI text ⏸️ ไม่แก้ (ไม่มีค่าใหม่)

### STEP 4 — sw.js + commit ⏸️ ไม่ commit
ตามกฎ task: "ข้อมูลเดือนนี้ไม่เปลี่ยนแปลง → log 'No new data' และ skip commit"
ไม่ bump sw.js, ไม่สร้าง push_now.command ใหม่ (working tree มี change ของ auto-update daemon ค้างอยู่ — เลี่ยง race)

---

## สถานะ repo
- HEAD = `3e85350` (auto-update: 2 ก.ค. — Affiliate มิ.ย. ครบ 1-30 + TK Followers 27.083K)
- `WIBWUB_Dashboard.html` / `WIBWUB_Mobile.html` — arrays ยอดขายสะอาด ครบ 6 เดือน ไม่มี net change จากรอบนี้
- working tree: มีเฉพาะ change ของ daemon (`push_now.command`) — ไม่แตะ

## เมื่อไหร่จะมีข้อมูล ก.ค.
เมื่อพนักงานอัปเดต row ปิดยอด ก.ค. ใน Google Sheets (คาดรอบ จ./พฤ. ถัดไป)
ค่อย append element ที่ 7 ให้ทุก sales array **พร้อมกัน** แล้วจึงตั้ง M5 = 7
