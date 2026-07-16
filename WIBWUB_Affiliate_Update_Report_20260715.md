# WIBWUB Affiliate Auto-Update Report — 15 กรกฎาคม 2026 (Scheduled Task)

## สรุปสิ่งที่อัปเดต

### 1. Export ข้อมูลจาก TikTok Affiliate Center
ดาวน์โหลดครบ 4 ไฟล์จากหน้า Transaction Analysis (ช่วง 1-13 ก.ค. — TikTok ยังไม่ปล่อยข้อมูลเกินวันที่ 13):
- ครีเอเตอร์: `Transaction_Analysis_Creator_List_20260701-20260713.xlsx`
- สินค้า (archival): `Transaction_Analysis_Product_List_20260701-20260713.xlsx`
- วีดีโอ: `Transaction_Analysis_Video_List_20260701-20260713.xlsx`
- ไลฟ์สตรีม: `Transaction_Analysis_Live_List_20260701-20260713.xlsx`

ทั้ง 4 ไฟล์ถูก LaunchAgent ย้ายเข้า `Data Affiliate/` โฟลเดอร์ที่ถูกต้องอัตโนมัติแล้ว

### 2. Export สินค้าใหม่ (ListProducts) — ใช้สำหรับ cr/vid
`ListProducts_2026-07-01-2026-07-14_ALLPlan_20260715025548.xlsx` (ช่วง 1-14 ก.ค. — หน้า product-performance มีข้อมูลใหม่กว่าอีก 1 วัน)

### 3. อัปเดตยอด Creator (AF_GMV/AF_NET/AF_COM/AF_CR)
ตรวจสอบผ่าน git history พบว่าการรันรอบก่อนหน้าในวันเดียวกัน (commit `f11d8ef`) ได้อัปเดตค่านี้ถูกต้องแล้วทั้งใน `WIBWUB_Affiliate_Dashboard.html` และ `WIBWUB_Mobile.html` (label "ก.ค. (1-13)" / GMV 619,016 / NET 609,646 / COM 71,180 / CR 381) — ไม่ต้องแก้ซ้ำ

### 4. อัปเดต PRODUCTS (cr/vid) จากไฟล์ ListProducts ใหม่ (1-14 ก.ค.)
| สินค้า | cr เดิม→ใหม่ | vid เดิม→ใหม่ |
|---|---|---|
| Leather Wipes | 150→160 | 71→84 |
| Interior Wipes | 113→119 | 48→51 |
| Sugar | 62→65 | 68→74 |
| Cleaner | 36→37 | 10→11 |
| Interior | 28→30 | 41→43 |
| Refresh | 26→29 | 17→21 |
| Visible | 9→9 | 6→7 |

(field อื่น เช่น gmv/units/monthly/ret ไม่ถูกแตะ — นอกสโคป)

### 5. Cache version + Git
- Bump `sw.js`: `wibwub-v384` → `wibwub-v385`
- คืนค่า `push_now.command` ที่ถูกย่อ (ขาด `git add -A` + `git commit`) ให้กลับมาครบ add+commit+push อีกครั้ง (ปัญหาเดิมซ้ำจากรอบบ่ายเมื่อวาน)
- `git add` ไฟล์ที่แก้ (Affiliate Dashboard + sw.js) สำเร็จ แต่ **commit ใน sandbox ทำไม่ได้** เพราะ `.git/index.lock` ค้างอยู่และลบไม่ได้ (Operation not permitted บน mounted path นี้) — ไฟล์ยังอยู่ใน staging area รอ commit
- **ต้องดับเบิลคลิก `push_now.command` เพื่อ commit+push ขึ้น GitHub** (สคริปต์จะ `rm -f .git/index.lock` ด้วยสิทธิ์เครื่องจริงก่อน ซึ่งน่าจะลบ lock ที่ค้างได้สำเร็จ ต่างจาก sandbox)

## หมายเหตุ
- ไฟล์ export บางไฟล์ในโฟลเดอร์มีชื่อซ้ำ/สำรองจากการรันหลายรอบในวันเดียวกัน (เช่น ครีเอเตอร์รอบเช้าที่ export job ค้างสถานะ "กำลังส่งออก" ไม่สำเร็จ ถูกข้ามเพราะไฟล์ที่ถูกต้องมีอยู่แล้วจากการ export ซ้ำที่สำเร็จ)
- ไฟล์ `Core_Stats_20260701-20260714_20260715023550.xlsx` ในโฟลเดอร์ครีเอเตอร์ถูกเปลี่ยนชื่อเป็น `_WRONG_FORMAT_ignore_...` เพราะเป็นรูปแบบรายงานผิด ไม่ใช่ Creator List ที่ใช้จริง
- ตัวเลข "ผ่าน 398 creators" hardcode เก่าในแท็บสินค้ายังไม่แก้ตามที่บันทึกไว้จากรอบก่อน — อยู่นอกสโคป
- **ปัญหาใหม่ที่พบวันนี้**: sandbox ไม่สามารถลบไฟล์ `.git/index.lock` ได้ (Permission denied) แม้เป็นเจ้าของไฟล์เดียวกัน — อาจเป็นข้อจำกัดของ mounted cloud path จาก sandbox ฝั่งนี้ ต้องพึ่ง `push_now.command`/เครื่องจริงในการ commit+push รอบนี้
