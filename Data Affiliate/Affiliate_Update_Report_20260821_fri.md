# WIBWUB Affiliate Auto-Update — 2026-08-21 (ศุกร์)

**ช่วงข้อมูล:** 1/8/2026 – 18/8/2026
(TikTok ยัง greyed out วันที่ 19–21 — ข้อมูลล่าสุดที่ระบบยอมให้ดึงคือ 18 ส.ค.)

## ไฟล์ที่ดาวน์โหลด + ย้ายแล้ว
| Tab | ไฟล์ | ปลายทาง |
|---|---|---|
| ครีเอเตอร์ | Transaction_Analysis_Creator_List_20260801-20260818.xlsx | Data Affiliate/ครีเอเตอร์/ |
| สินค้า | Transaction_Analysis_Product_List_20260801-20260818.xlsx | Data Affiliate/สินค้า/ |
| วีดีโอ | Transaction_Analysis_Video_List_20260801-20260818.xlsx | Data Affiliate/วีดีโอ/ |
| ไลฟ์สตรีม | Transaction_Analysis_Live_List_20260801-20260818.xlsx | Data Affiliate/ไลฟ์สตรีม/ |

Downloads ถูก LaunchAgent (com.wibwub.download-mover) ย้ายให้อัตโนมัติเรียบร้อย

## STEP 4 — Affiliate arrays (AF_* / AFI_*)
คำนวณจากไฟล์ครีเอเตอร์: **GMV ฿960,112 | Net ฿940,905 | Comm ฿112,989 | Creators 515**

ค่าเหล่านี้ **ตรงกับที่มีอยู่แล้ว** ใน `AF_GMV/AF_NET/AF_COM/AF_CR` index สุดท้าย (label `"ส.ค. (1-18)"`)
และ `AFI_GMV/AFI_NET/AFI_COMM` (label `'สค.69 (1-18)'`) → **ไม่มีการแก้ไข** (no-op ที่ถูกต้อง เพราะข้อมูลยังหยุดที่ 18 ส.ค.)

หมายเหตุ: column layout ของไฟล์ครีเอเตอร์จริงคือ col1=GMV, col4=การคืนเงิน, col21=ค่าคอมมิชชั่น
(ไม่ใช่ col2/col3/col10 ตามที่ SKILL.md เขียนไว้) และมี header 2 แถว

## STEP 5 — PRODUCTS cr/vid
อ่านจาก col19 = ครีเอเตอร์ที่มียอดขายเฉลี่ยรายวัน, col13 = วิดีโอที่มียอดขายเฉลี่ยรายวัน

| สินค้า | cr | vid |
|---|---|---|
| WIBWUB Refresh Leather Wipes | 36 → **37** | 33 → **34** |
| WIBWUB Interior wipes | 22 | 22 |
| WIBWUB Sugar | 15 | 16 |
| WIBWUB CLEANER | 6 | 7 |
| WIBWUB Interior | 5 | 5 |
| WIBWUB Refresh | 4 → **3** | 4 |
| WIBWUB Visible | 2 | 2 |

ใช้ mapping แบบระบุชื่อในวงเล็บตรง ๆ แทน fuzzy keyword ของ SKILL.md เพราะ
"WIBWUB Refresh Leather Cleaner" จะไป match keyword `Leather` ก่อนแล้วเขียนทับ Leather Wipes ผิด

## STEP 5B — VIDEOS array
- parse ไฟล์วีดีโอ (inlineStr XML): 5,772 rows
- monthly schema: mar, apr, may, jun, jul, aug (มี `aug` อยู่แล้ว ไม่ต้อง extend)
- อัปเดตค่าเดือน ส.ค.: **92 รายการ**
- เพิ่มวีดีโอใหม่: **140 รายการ**
- รวมทั้งหมด: **6,167 entries** (เดิม 6,027)

## Verify
- `node eval` VIDEOS array → ผ่าน (6,167 entries)
- `node eval` PRODUCTS array → ผ่าน (7 entries, cr/vid ถูกต้อง)
- `git diff --stat` → 373 insertions / 233 deletions บนไฟล์ ~46K บรรทัด (ปกติ ไม่ใช่ rebuild ทั้งไฟล์)

## STEP 6
- sw.js: **v758 → v759**
- `push_now.command` พร้อมแล้ว

📌 **ดับเบิ้ลคลิก `push_now.command` เพื่อ push ขึ้น GitHub**
