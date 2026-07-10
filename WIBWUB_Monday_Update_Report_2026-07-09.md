# WIBWUB Weekly Dashboard Update — 9 กรกฎาคม 2026

## สรุปสิ่งที่ทำ

### 1. แก้บัคข้อมูล Affiliate เดือน ก.ค. ที่เสียหาย (สำคัญ)
รันก่อนหน้า (18:04 น. วันเดียวกัน) พาร์สไฟล์ TikTok Affiliate export ผิด ทำให้ค่าคอมมิชชั่นเดือน ก.ค. ถูกบันทึกผิดเป็น **1 บาท** แทนที่จะเป็นค่าจริง ตรวจพบและแก้ไขโดย export ไฟล์ "Transaction Analysis Creator List" (รูปแบบถูกต้อง 12 คอลัมน์) ใหม่ ช่วง 1-8 ก.ค. 2569 แล้วคำนวณใหม่:

| | ค่าเดิม (ผิด) | ค่าใหม่ (ถูกต้อง) |
|---|---|---|
| GMV | 319,359 | 356,665 |
| Net | 307,864 | 350,747 |
| Commission | **1** | **41,165** |
| Creators | 265 | 354 |

อัปเดตทั้งใน `WIBWUB_Affiliate_Dashboard.html` (AF_MO/GMV/NET/COM/CR) และ `WIBWUB_Mobile.html` (AFI_MONTHS/GMV/NET/COMM) ให้ตรงกัน

### 2. Export ข้อมูลใหม่
- Shipnity เดือน ก.ค. (month-to-date ถึงวันที่ 9): `Data Shipnity/Data_กรกฎาคม.xlsx`
- TikTok Affiliate Transaction Analysis (1-8 ก.ค.): `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260701-20260708.xlsx`

### 3. คำนวณ Top Products ใหม่
รวมข้อมูลจากไฟล์ Shipnity รายเดือน 7 ไฟล์ (ม.ค.–ก.ค. 2569, ตรวจสอบช่วงวันที่ครบทุกไฟล์แล้ว) dedup ด้วย (เลขที่ออเดอร์, รหัสสินค้า, จำนวน) เพื่อกันข้อมูลซ้ำ:

- ยอดขายรวม 7 เดือน: **฿49.87M** (จากเดิม ฿49.8M)
- สินค้าขายดีสุด: Wool Duster ฿5.27M · 8,256 ชิ้น (อันดับ 1 เหมือนเดิม)
- Interior Wipes ขยับจากอันดับ 5 → 4 (แซง Refresh 500ml เล็กน้อย)
- จำนวนชิ้นรวม: 190K ชิ้น

อัปเดต `ALL_PRODUCTS` + `PROD_MO` ใน `WIBWUB_Mobile.html` และตาราง/กราฟ Top Products (KPI, ตารางแยกช่องทาง 15 อันดับ, กราฟแท่ง pr_top10, กราฟโดนัท pr_channel) ใน `WIBWUB_Dashboard.html`

### 4. Cache version + Git
- Bump `sw.js`: `wibwub-v353` → `wibwub-v354`
- Commit `e936314`: 4 ไฟล์ (Affiliate Dashboard, Mobile, Dashboard, sw.js), +72/-72 บรรทัด
- สร้าง `push_now.command` ใหม่ — **ต้องดับเบิลคลิกเพื่อ push ขึ้น GitHub** (sandbox push เองไม่ได้)

## หมายเหตุ
- ขอบเขตงานนี้จำกัดเฉพาะ Affiliate + Top Products ตาม task ที่กำหนด ไม่ได้แตะ Ads/Social/Platform Analytics
- ไฟล์ Shipnity รายเดือนทั้ง 7 ไฟล์ยืนยันแล้วว่าเป็นข้อมูลระดับสินค้า (มีชื่อสินค้าจริง) ครบทั้งเดือน ไม่ใช่ snapshot บางส่วนตามที่เอกสารเก่าเคยระบุไว้
