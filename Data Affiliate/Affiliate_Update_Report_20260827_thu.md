# ✅ WIBWUB Affiliate Update — 2026-08-27 (พฤหัส)

📅 ช่วงข้อมูล: **1/8/2026 – 24/8/2026**
(วันที่ 25–27 ยัง greyed out ในปฏิทิน TikTok — ระบบอัปเดตข้อมูลถึง 24 ส.ค. 2026 0:00 GMT+7 เท่านั้น)

## 📁 ไฟล์ที่ดาวน์โหลดและย้ายแล้ว
| Tab | ไฟล์ | ปลายทาง |
|---|---|---|
| ครีเอเตอร์ | Transaction_Analysis_Creator_List_20260801-20260824.xlsx | Data Affiliate/ครีเอเตอร์/ |
| สินค้า | Transaction_Analysis_Product_List_20260801-20260824.xlsx | Data Affiliate/สินค้า/ |
| วีดีโอ | Transaction_Analysis_Video_List_20260801-20260824.xlsx | Data Affiliate/วีดีโอ/ |
| ไลฟ์สตรีม | Transaction_Analysis_Live_List_20260801-20260824.xlsx | Data Affiliate/ไลฟ์สตรีม/ |

LaunchAgent `com.wibwub.download-mover` ย้ายไฟล์ออกจาก Downloads และเปลี่ยนชื่อให้อัตโนมัติเรียบร้อย

## 📊 ตัวเลข (ส.ค. 1-24)
| Metric | ค่าเดิม | ค่าใหม่ |
|---|---|---|
| GMV | ฿1,313,831 | **฿1,313,998** |
| Net GMV | ฿1,291,673 | **฿1,291,840** |
| Commission | ฿150,935 | **฿151,291** |
| Creators (GMV>0) | 670 | **670** |

Refund รวม ฿22,159 · ครีเอเตอร์ในไฟล์ทั้งหมด 7,206 แถว

## ✍️ ไฟล์ที่แก้ไข
- **WIBWUB_Affiliate_Dashboard.html** — `AF_GMV`, `AF_NET`, `AF_COM`, `AF_CR` (index สุดท้าย = label "ส.ค. (1-24)" ตรงกับเดือนที่ประมวลผล → overwrite ไม่ append)
- **WIBWUB_Mobile.html** — `AFI_GMV`, `AFI_NET`, `AFI_COMM` (index สุดท้าย = "สค.69 (1-24)")
- **sw.js** — v846 → **v847**
- **push_now.command** — เขียนใหม่แล้ว

## 🎬 VIDEOS array
- parse ไฟล์วีดีโอได้ 6,456 แถว · entry เดิมใน array 6,810 รายการ (parse ครบ 100% ไม่มี mismatch)
- อัปเดตค่าเดือน ส.ค.: **0 รายการ** (ข้อมูลช่วง 1-24 ส.ค. เท่าเดิมกับรอบก่อน)
- เพิ่มคลิปใหม่: **6 รายการ** (creator `jeewon445` / WIBWUB Interior wipes, GMV 0)
- รวมทั้งหมด **6,816 รายการ** — ตรวจด้วย `node eval` ผ่าน ไม่ throw

## 🛒 PRODUCTS cr/vid
ตรวจแล้วทุกค่า **ตรงกับไฟล์ export อยู่แล้ว ไม่ต้องแก้**:

| สินค้า | cr | vid |
|---|---|---|
| Refresh Leather Wipes | 40 | 37 |
| Interior wipes | 23 | 22 |
| Sugar | 14 | 15 |
| CLEANER | 5 | 6 |
| Interior | 5 | 5 |
| Visible | 2 | 2 |
| Refresh | 4 | 4 (ไม่มี SKU ตรงในไฟล์ — คงค่าเดิม) |

## ⚠️ หมายเหตุ/การตัดสินใจในรอบนี้ (autonomous)
1. **คอลัมน์ในไฟล์ครีเอเตอร์ไม่ตรงกับที่ SKILL.md ระบุ** — SKILL บอก returns=col2, commission=col10 แต่ไฟล์จริงคือ **returns=col4 (การคืนเงิน), commission=col21 (ค่าคอมมิชชั่นโดยประมาณ)** และ header กินไป **2 แถว** (ไม่ใช่ 1) → ใช้คอลัมน์จริง ผลลัพธ์สอดคล้องกับค่าที่ dashboard เก็บไว้เดิม แนะนำแก้ SKILL.md
2. **PRODUCTS cr/vid** — ไฟล์มีหลาย SKU ที่ match keyword เดียวกัน (เช่น Leather 3 SKU) เลือกใช้ **SKU ที่ GMV สูงสุด** ตามธรรมเนียมข้อมูลเดิมใน array แทนการรวมยอด
3. **STEP 3 pattern matching ใน SKILL.md ใช้ไม่ได้** — ไฟล์ที่ Chrome โหลดมาชื่อเป็น hash (เช่น `413145afe….xlsx`) ไม่ใช่ `Transaction_Analysis_*` แต่ LaunchAgent จัดการเปลี่ยนชื่อ+ย้ายให้เองอยู่แล้ว

## 📌 ขั้นตอนถัดไป
ดับเบิ้ลคลิก **push_now.command** เพื่อ push ขึ้น GitHub
(git diff: Affiliate +18 / Mobile +6 / sw.js +2 บรรทัด — อยู่ในเกณฑ์ปกติ ไม่มีสัญญาณเขียนทับผิดพลาด)
