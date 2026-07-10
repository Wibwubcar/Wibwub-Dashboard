# WIBWUB Weekly Update — วันจันทร์ 29 มิ.ย. 2026 (automated run)

## สรุป: ข้อมูลในขอบเขตของ task อัปเดตครบแล้ว — ไม่มี commit ใหม่ที่จำเป็น
## ⚠️ พบ regression สำคัญนอกขอบเขต task: ยอดขายเดือน มิ.ย. ถูกตัดออกจาก sales arrays (รายละเอียดด้านล่าง)

---

## ขั้นตอนที่ตรวจสอบ

### STEP 1–2: ดาวน์โหลดข้อมูล (ไม่ต้องโหลดใหม่)
ไฟล์ล่าสุดมีอยู่แล้วครบ จึงไม่รัน Chrome download (ลดความเสี่ยง navigate ค้างในรอบ unattended):
- Shipnity: `Data_29-06-2026.xlsx` (ครอบคลุม 01–29 มิ.ย., วันนี้)
- Affiliate: `Transaction_Analysis_Creator_List_20260601-20260627.xlsx` (ถึง 27 มิ.ย. = ข้อมูล settle ล่าสุดที่มี)

### STEP 3: Top Products (Shipnity) — ✅ current แล้ว ไม่ต้องแก้
Aggregate จากไฟล์ product-level เดือนละ 1 ไฟล์ (ม.ค.–มิ.ย., dedup ตาม order key):
- เดือน 1–5: ตรงกับค่าใน dashboard ทุกตัว (100%)
- เดือน 6 (มิ.ย.): ค่าใน dashboard สูงกว่าผลคำนวณใหม่เล็กน้อย (~0.05%) → dashboard สดเท่ากันหรือใหม่กว่า snapshot ล่าสุดที่มี จึง**ไม่ overwrite** (จะเป็นการถอยข้อมูล)
- Top 1: Wool Duster ฿5,156,807 (dashboard) เทียบ ฿5,154,322 (คำนวณใหม่)

### STEP 4: Affiliate arrays — ✅ current แล้ว ไม่ต้องแก้
คำนวณจาก Creator List (ถึง 27 มิ.ย.) ตรงกับค่าที่ commit ไว้แล้วทุกตัว:
- GMV = ฿550,142 · NET = ฿542,744 · COMM = ฿68,304 · Creators = 355
- `AFI_GMV/NET/COMM` ใน Mobile (index 7) = ค่าเดียวกันเป๊ะ → ไม่มี delta

### STEP 5: sw.js + commit — ไม่ทำ
ไม่มีข้อมูลในขอบเขต task ที่เปลี่ยน → การ bump sw.js + commit ใหม่ไม่จำเป็น (sw ปัจจุบัน = v279, ตรงกับ HEAD)

---

## ⚠️ Regression สำคัญที่พบ (อยู่นอกขอบเขต Monday task — ฝากตรวจสอบ)

**ยอดขายเดือน มิ.ย. ถูกลบออกจาก sales arrays ทั้ง Mobile + Dashboard และถูก commit ไปแล้ว**

- Parent commit `62ae147` (ถูกต้อง): มี 6 เดือน รวม มิ.ย.
  `SH_REV = [...,5581064,5225845]` · `M5 = [...,"พ.ค.","มิ.ย."]`
- HEAD ปัจจุบัน `3c220cc` (regression): เหลือ 5 เดือน ตัด มิ.ย. ออก
  `SH_REV = [...,5581064]` · `M5 = [...,"พ.ค."]`
- `3c220cc` ใช้ commit message ซ้ำกับ `62ae147` แบบคำต่อคำ → เกิดจาก auto-commit daemon
  (`com.wibwub.autopush` / `com.wibwub.update`) ที่รันระหว่าง session ไม่ใช่การแก้โดยตั้งใจ

**arrays ที่โดนตัด มิ.ย. (ค่าจริงเดือน มิ.ย. ที่ควรคืน — จาก `62ae147`):**
- `SH_REV` มิ.ย. = 5225845 · `TK_REV` = 1079305 · `LZ_REV` = 109721
- `SH_ORD` = 8220 · `TK_ORD` = 2752 · `SH_CANCEL_PCT` = 5.16
- `TK_ADSSPEND` = 231695 · `TK_FEECOMM` = 272152

**ทำไมไม่แก้ในรอบนี้:** (1) นอกขอบเขต Monday task — sales arrays มาจาก Google Sheets ที่ task นี้ไม่ได้ดึง; (2) มี auto-daemon churn ไฟล์เดิมอยู่ ถ้าคืน มิ.ย. แล้ว daemon อาจตัดซ้ำ (race) ควรแก้ที่ root cause ของ daemon (logic "trim arrays ให้เท่า labels" — skill error #7)

**วิธีคืนข้อมูลถ้าต้องการ:**
```bash
cd ".../Digital Marketing/claude/All"
git show 62ae147:WIBWUB_Dashboard.html > /tmp/x && cat /tmp/x > WIBWUB_Dashboard.html
git show 62ae147:WIBWUB_Mobile.html    > /tmp/x && cat /tmp/x > WIBWUB_Mobile.html
```
(แล้วแก้ logic ใน auto-update daemon ไม่ให้ตัด มิ.ย. ออกอีก)

---

## สถานะ repo ตอนจบ
- Working tree สะอาด (ตรงกับ HEAD `3c220cc`)
- ไฟล์ที่ผมเขียนทับด้วย `git show HEAD:` = byte-identical กับ commit → ไม่มีไฟล์เสีย
- Backup ของ working-tree เดิมที่เก็บไว้: `outputs/regressed_worktree_backup/`
