# WIBWUB Affiliate Auto-Update — รายงานสรุป

**วันที่รัน:** 2 ก.ค. 2569 (2026-07-02) · รันอัตโนมัติ (scheduled task)

## สถานการณ์ข้อมูล
- ข้อมูลเดือน ก.ค. **ยังไม่มี** — วันที่ในปฏิทิน TikTok Affiliate Center ของเดือน ก.ค. ยัง grey out ทั้งหมด (ข้อมูลถึง 30 มิ.ย. เท่านั้น)
- จึงตัดสินใจทำ **final full-month sync ของเดือน มิ.ย. (1–30)** แทนการเขียนค่า 0 ให้เดือน ก.ค.
- รอบก่อนหน้า (1 ก.ค.) ค้างที่ช่วง 1–29 มิ.ย.

## ไฟล์ที่ดาวน์โหลด + ย้าย (ช่วง 20260601–20260630)
- ครีเอเตอร์ → `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260601-20260630.xlsx`
- สินค้า → `Data Affiliate/สินค้า/Transaction_Analysis_Product_List_20260601-20260630.xlsx`
- วีดีโอ → `Data Affiliate/วีดีโอ/Transaction_Analysis_Video_List_20260601-20260630.xlsx`
- ไลฟ์สตรีม → `Data Affiliate/ไลฟ์สตรีม/Transaction_Analysis_Live_List_20260601-20260630.xlsx`

หมายเหตุ: สำเนาต้นฉบับยังอยู่ใน Downloads เพราะ mount เป็น read-only (ลบไม่ได้) — พฤติกรรมเดียวกับรอบก่อน

## ตัวเลข มิ.ย. 2569 — สรุปสุดท้าย (1–30)
| KPI | เดิม (1–29) | ใหม่ (1–30) |
|---|---|---|
| Affiliate GMV | ฿607,557 (฿0.61M) | **฿642,490 (฿0.64M)** |
| Net GMV | ฿598,495 (฿0.60M) | **฿632,313 (฿0.63M)** |
| Commission | ฿75,273 (฿75K) | **฿79,284 (฿79K)** · avg 12.3% |
| Returns | ฿9.1K | **฿10.2K** |
| Active creators (GMV ≥ ฿1K) | 83 | **87** |
| Creators มียอด | 383 | **398** |
| Orders | 2,745 | **3,103** · AOV ฿207 |

## ไฟล์ที่แก้ไข
1. **WIBWUB_Affiliate_Dashboard.html**
   - AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR (index 5 = มิ.ย.) → ค่า 1–30 · label "มิ.ย. (1-30)"
   - PRODUCTS array (แก้เฉพาะ cr/vid): Leather Wipes 15/22 · Interior Wipes 17/118 · Sugar 11/225 · Cleaner 7/74 · Interior 4/200 · Refresh 3/41 · Visible 2/24 (ไม่เปลี่ยน)
   - KPI strip + badge + note → ค่า 1–30, อัปเดต 2 ก.ค. 2569
   - Products table header sub-label "มิ.ย.1-20" → "มิ.ย.1-30"
2. **WIBWUB_Mobile.html**
   - AFI_GMV/AFI_NET/AFI_COMM (index 7 = มิ.ย.) → 642490 / 632313 / 79284
   - Affiliate GMV รวม card ฿2.94M → **฿2.97M**
3. **sw.js** — cache version wibwub-v305 → **v306**
4. **push_now.command** — ปรับให้ commit ไฟล์ affiliate รอบนี้

## Backups
- `WIBWUB_Affiliate_Dashboard.html.bak_20260702_025410_run`
- `WIBWUB_Mobile.html.bak_20260702_025410_run`

## ขั้นตอนถัดไป (ต้องรันเอง)
เปิด `push_now.command` เพื่อ commit + push ขึ้น GitHub Pages (PWA จะอัปเดตอัตโนมัติจาก cache v306)
