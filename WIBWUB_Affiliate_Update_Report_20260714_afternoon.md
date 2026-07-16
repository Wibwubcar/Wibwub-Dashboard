# WIBWUB Affiliate Auto-Update Report — 14 กรกฎาคม 2026 (รอบบ่าย)

## สรุปสิ่งที่อัปเดต

### 1. ตรวจสอบข้อมูลบน TikTok Affiliate Center
ปฏิทินเลือกวันที่บนหน้า "การวิเคราะห์ครีเอเตอร์" ยืนยันว่ายังไม่มีข้อมูลเกิน 12 ก.ค. 2569 (วันที่ 13+ ถูกล็อกไว้) ข้อมูล Video/Live List ที่มีอยู่แล้วในคลัง (`Data Affiliate/วีดีโอ/` และ `.../ไลฟ์สตรีม/`, exported 14 ก.ค. 02:59–03:03) จึงเป็นปัจจุบันที่สุดแล้ว ไม่ต้อง export ใหม่

### 2. Export สินค้าใหม่ (ListProducts)
Export ผ่านปุ่ม "ส่งออก" ที่ตารางสินค้าในหน้า product-performance สำเร็จ: `ListProducts_2026-07-01-2026-07-13_ALLPlan_20260714024302.xlsx` (70 SKU) ย้ายเข้า `Data Affiliate/สินค้า/` แล้ว

### 3. คำนวณยอด Creator ใหม่ (ยืนยันด้วยไฟล์ Creator_List 1-12 ก.ค. ที่มีอยู่แล้ว — ตรงกับ KPI สดบนเว็บ 359 ครีเอเตอร์)
| | ค่าเดิมในไฟล์สด (ก่อนแก้) | ค่าที่ถูกต้อง (คำนวณจากไฟล์) |
|---|---|---|
| GMV | 575,217 | 575,302 |
| Net | 559,906 | 545,087 |
| Commission | 0 | 66,167 |
| Creators | 359 | 359 |

พบว่าค่า Net และ Commission ในไฟล์สดคลาดเคลื่อนจากรอบก่อนหน้า (Commission เป็น 0 ทั้งที่มีข้อมูลจริง) จึงแก้ไขให้ตรงกับผลคำนวณจากไฟล์ Creator_List ล่าสุด — อัปเดตทั้งใน `WIBWUB_Affiliate_Dashboard.html` (AF_GMV/AF_NET/AF_COM/AF_CR ดัชนีสุดท้าย "ก.ค. (1-12)") และ `WIBWUB_Mobile.html` (AFI_GMV/AFI_NET/AFI_COMM ดัชนีสุดท้าย)

### 4. อัปเดต PRODUCTS (cr/vid) จากไฟล์ ListProducts ใหม่
| สินค้า | cr เดิม→ใหม่ | vid เดิม→ใหม่ |
|---|---|---|
| Leather Wipes | 134→150 | 61→71 |
| Interior Wipes | 106→113 | 44→48 |
| Sugar | 60→62 | 60→68 |
| Cleaner | 35→36 | 10→10 |
| Interior | 28→28 | 38→41 |
| Refresh | 26→26 | 13→17 |
| Visible | 9→9 | 5→6 |

(field อื่น เช่น gmv/units/monthly/ret ไม่ถูกแตะ — นอกสโคป)

### 5. Cache version + Git
- Bump `sw.js`: `wibwub-v379` → `wibwub-v380`
- แก้ `push_now.command` กลับให้มี `git add -A` + `git commit` + `git push` ครบ (ไฟล์บนดิสก์ถูกย่อเหลือแค่ push เมื่อไม่ทราบสาเหตุ — คืนค่าให้ตรงกับเวอร์ชันที่คอมมิตไว้แล้ว)
- Commit `68892e7`: 3 ไฟล์ (Affiliate Dashboard, Mobile, sw.js), +14/-14 บรรทัด
- **ต้องดับเบิลคลิก `push_now.command` เพื่อ push ขึ้น GitHub** (sandbox push เองไม่ได้ ติด proxy)

## หมายเหตุ
- ตัวเลข "ผ่าน 398 creators" ในแท็บสินค้า (บรรทัด `สินค้าที่ Active`) เป็นข้อความ hardcode เก่าที่ยังไม่อัปเดต — ไม่ได้แก้เพราะอยู่นอกสโคปที่กำหนด (cr/vid array เท่านั้น) รอผู้ใช้ยืนยันก่อนแก้
- Creator/Product/Video/Live ทั้ง 4 หมวดยังคงอยู่ที่ช่วง 1-12/1-13 ก.ค. เพราะ TikTok ยังไม่ปล่อยข้อมูลเกินวันที่นี้
