# WIBWUB Weekly Update — 3 ก.ย. 2026

สรุปการรันอัตโนมัติ `wibwub-monday-update`

---

## ผลลัพธ์โดยรวม

| Step | สถานะ | หมายเหตุ |
|---|---|---|
| 0. M5 protection | ✅ ผ่าน (ไม่แก้ไข) | `len(M5) == len(SH_REV) == 8` ทั้ง Dashboard และ Mobile |
| 1. Shipnity export | ✅ ดาวน์โหลดใหม่ | `Data Shipnity/Data_03-09-2026.xlsx` (2.49 MB, 2,712 แถว) |
| 2. TikTok Affiliate export | ✅ ตรวจสอบแล้ว | TikTok ยังไม่ปล่อยข้อมูล ก.ย. — ใช้ไฟล์ ส.ค. เดิม |
| 3. Top Products | ⏸️ ตั้งใจไม่แก้ | เหตุผลด้านล่าง |
| 4. Affiliate arrays | ✅ **แก้ไขแล้ว** | ตัวเลข ส.ค. คลาดเคลื่อน — เขียนทับ index สุดท้าย |
| 5. sw.js + commit | ✅ v960 → **v961**, commit `bcc3c61` | รอ push ด้วยมือ |

---

## STEP 1 — Shipnity (ยอดขาย ก.ย. MTD)

ดาวน์โหลดผ่าน Claude Chrome จาก `shipnity.com/data/c/purchase` ระดับสินค้าในออเดอร์, ส่งออกเป็น "ไฟล์เดียว" (.xlsx)

**ยอดขาย ก.ย. 2026 (1–3 ก.ย.) รวม ฿784,516** (2,705 แถวหลัง dedup)

| วันที่ | ยอดขาย |
|---|---|
| 01/09 | ฿375,966 |
| 02/09 | ฿313,550 |
| 03/09 | ฿95,000 (ไม่เต็มวัน) |

**แยกช่องทาง:** Shopee ฿450,587 · TikTok ฿215,659 · Facebook ฿54,357 · Carcare ฿36,240 · Line Shopping ฿21,512 · Lazada ฿4,768 · การตลาด ฿1,328 · Makro pro ฿65

**Top 10 SKU (ก.ย. MTD):**

1. Sugar 500ml — ฿90,227 (259)
2. Refresh Wipes — ฿80,474 (985)
3. Interior 500ml — ฿41,111 (117)
4. Interior Wipes — ฿38,571 (498)
5. Wool Duster — ฿29,842 (48)
6. Spot 500ml — ฿29,274 (74)
7. Anna Nano Diamond — ฿28,640 (16)
8. Refresh 500ml — ฿22,324 (63)
9. Tire & Trim Gel — ฿21,209 (44)
10. Xglass 100ml — ฿20,435 (54)

---

## STEP 4 — แก้ไข Affiliate arrays (การเปลี่ยนแปลงหลักของรอบนี้)

เปิด TikTok Affiliate → Transaction Analysis ยืนยันสด: ปฏิทิน 09/2026 ยัง disabled ทั้งเดือน และ "อัปเดตเมื่อ" ยังเป็น **31 ส.ค. 2026** → ไม่มีข้อมูล ก.ย. ให้ append

แต่เมื่อคำนวณใหม่จาก `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260801-20260831.xlsx` พบว่าค่าที่อยู่ในแดชบอร์ด**ต่ำกว่าไฟล์ต้นทาง**:

| ค่า | เดิมในแดชบอร์ด | ไฟล์ต้นทาง | ส่วนต่าง |
|---|---|---|---|
| GMV | 1,730,666 | **1,730,879** | −213 |
| NET | 1,701,769 | **1,701,979** | −210 |
| Commission | 198,783 | **199,254** | −471 |
| Creators | 853 | 853 | ✅ |

Label `"ส.ค. (1-31)"` / `'สค.69 (1-31)'` **เป็นตัวสุดท้ายของ array อยู่แล้ว** → เข้าเงื่อนไข case 3 ของ runbook: เขียนทับเฉพาะ index สุดท้าย ไม่ append ไม่เปลี่ยนความยาว

**ไฟล์ที่แก้:**
- `WIBWUB_Affiliate_Dashboard.html` บรรทัด 12043–12045 → `AF_GMV` / `AF_NET` / `AF_COM` (`AF_CR` ไม่แตะ)
- `WIBWUB_Mobile.html` บรรทัด 880–882 → `AFI_GMV` / `AFI_NET` / `AFI_COMM`

**ยืนยันหลังแก้:** AF_* ยาว 8 ทุกตัว, AFI_* ยาว 10 ทุกตัว, เดือนก่อนหน้าไม่ถูกแตะ, ไม่พบตัวเลขเก่าค้างที่อื่นในไฟล์ .html ใดๆ

---

## รายการที่ตั้งใจไม่ทำ

**STEP 0 — ไม่รันสคริปต์ป้องกัน M5**
สคริปต์ใน runbook ใช้ `required_months = today.month` ซึ่งจะยืด `M5` เป็น 9 ช่อง ขณะที่ `SH_REV`/`TK_REV`/`LZ_REV` และอีก ~20 array ยังยาว 8 → ทุกกราฟจะได้ `undefined` ที่ index 8 การรัน 1, 2 ก.ย. (เช้า/บ่าย) ตัดสินใจแบบเดียวกัน และในไฟล์เองมีคอมเมนต์กำกับไว้ว่า "ก.ย. จะเพิ่มเมื่อ sales sync มีข้อมูลเดือน ก.ย."

**STEP 3 — ไม่อัปเดต Top Products**
`ALL_PRODUCTS` / `PROD_MO` / `PROD_MO_LBL` ผูกกับหน้าต่าง 8 เดือนของ `M5` การเพิ่ม ก.ย. จะทำให้ยาวไม่เท่ากัน และตอนนี้ ก.ย. มีข้อมูลแค่ 3 วัน (03/09 ไม่เต็มวัน) เฉพาะ Shipnity ช่องทางอื่นยังไม่ sync จะทำเมื่อเดือน ก.ย. ถูก append เข้า M5 พร้อมกันทั้งชุด

---

## ⚠️ สิ่งที่ต้องทำด้วยมือ

**1. Push ขึ้น GitHub** — sandbox push ไม่ได้ (proxy HTTP 403) รัน `push_now.command` (อัปเดตให้แล้ว: เคลียร์ lock ครบขึ้น + แสดง commit ที่รอ push ก่อน)

รอ push: `bcc3c61`

**2. ไฟล์ค้างใน .git ที่ sandbox ลบไม่ได้** — มี `tmp_obj_*` หลายสิบไฟล์ใน `.git/objects/`, `HEAD.lock`, `objects/maintenance.lock` (Operation not permitted) รอบนี้ commit ผ่านได้ แต่ `push_now.command` เวอร์ชันใหม่จะเคลียร์ให้ตอนรัน

---

## 🔧 ข้อบกพร่องใน runbook ที่ควรแก้

**STEP 0** — เปลี่ยนเงื่อนไขจาก `required_months = today.month` เป็น `required_months = len(SH_REV)` เพราะ M5 ต้อง sync กับ data arrays ไม่ใช่กับปฏิทิน สคริปต์ปัจจุบันถ้ารันตรงๆ จะทำแดชบอร์ดพัง — ถูกข้ามมา 4 รอบติดแล้ว

**STEP 4** — สองจุด:
- `DATA_DIR` ต้องชี้ไปที่ `Data Affiliate/ครีเอเตอร์/` (LaunchAgent `wibwub_auto_move.sh` ย้ายไฟล์ creator list เข้าโฟลเดอร์ย่อยนี้) ปัจจุบันชี้ที่ `Data Affiliate/` จะเจอแต่ไฟล์เก่าตกค้าง
- ไฟล์ export เปลี่ยนจาก 12 → 22 คอลัมน์ และมี **header 2 แถว** index เดิมผิดหมด ควรอ้างด้วย**ชื่อคอลัมน์**: `GMV จากครีเอเตอร์` (col 1), `การคืนเงิน` (col 4, เดิมใช้ col 2), `ค่าคอมมิชชั่นโดยประมาณ` (col 21, เดิมใช้ col 10 → ได้ 0) และต้อง `.iloc[2:]` เพื่อข้าม header ทั้งสองแถว

**STEP 1–2 (path)** — runbook hard-code `/sessions/hopeful-serene-fermi/mnt/` ซึ่งเป็น session เก่า ควรเขียนเป็น path บน macOS แล้วให้ผู้รันแปลงเอง

---

*รันเมื่อ 3 ก.ย. 2026 · commit `bcc3c61` · sw.js `wibwub-v961`*
