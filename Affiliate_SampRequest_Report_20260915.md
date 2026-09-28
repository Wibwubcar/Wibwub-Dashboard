# ✅ WIBWUB Affiliate — sync "คำขอสินค้า" 15 ก.ย. 2026

**เดือน ก.ย. 2569 (1-15 ก.ย.):**
- คำขอทั้งหมด: **237** (เดิม 185 ก่อนหน้า — เพิ่มใหม่ 52 แถว)
- อนุมัติ: **104**
- ปฏิเสธ: **133**
- อื่นๆ (On Process/Done/Waiting): 0

**สินค้าที่ถูกขอมากที่สุดเดือนนี้:**
| สินค้า | คำขอ | อนุมัติ | ปฏิเสธ |
|---|---|---|---|
| Refresh Wipes | 133 | 52 | 81 |
| Interior wipes | 73 | 32 | 41 |
| Interior | 17 | 6 | 11 |
| Reflex | 14 | 9 | 5 |
| Sugar | 12 | 9 | 3 |
| Beach | 1 | 1 | 0 |

**7 วันล่าสุด (09/09 - 15/09):** 103 คำขอ (เดิม 51 ก่อนหน้า)

ทุกเดือนก่อนหน้า (ต.ค.68 – ส.ค.69) ตรวจสอบกับชีตสดแล้ว **ตรงกันทุกจุด** ไม่พบความเปลี่ยนแปลงย้อนหลัง

## ⚠️ ข้อสังเกต
ระหว่าง `git commit` มีงาน auto-sync อีกงาน (น่าจะเป็น "Thursday affiliate sync" ที่ทำ VIDEOS/PRODUCTS GMV refresh) กำลังรันพร้อมกันและ `git add` ไฟล์ตัวเองค้างไว้ในเวลาเดียวกัน ทำให้ commit ของงานนี้ (80d3b62) พ่วงเอาการเปลี่ยนแปลงของ `WIBWUB_Affiliate_Dashboard.html` (PRODUCTS cr/vid, VIDEOS GMV), `WIBWUB_Dashboard.html`, และ `WIBWUB_Mobile.html` (AFI_GMV/NET/COMM, TK_FOL) ติดไปด้วย — ตรวจสอบเนื้อหาแล้วดูสมเหตุสมผล (ตัวเลข GMV/vid เพิ่มขึ้นตามปกติ ไม่มีข้อมูลแปลกปลอม) ไม่ใช่ข้อมูลเสีย เพียงแต่รวมอยู่ใน commit message ของงานนี้แทนที่จะเป็นของมันเอง ไม่ต้องแก้ไขอะไรเพิ่ม แต่แจ้งให้ทราบเผื่อเช็ค log

## ⚙️ ไฟล์ที่แก้ไข
- `WIBWUB_Affiliate_Dashboard.html` — SAMPLE_MONTHS['2026-09'], SAMPLE_PRODUCTS['2026-09'], SAMPLE_PRODUCTS_LAST7D (ช่วงที่ตั้งใจแก้)
- `sw.js` — v1122 → v1123

Commit: `80d3b62` "auto-update: คำขอสินค้า 2026-09-15"

**อย่าลืม double-click `push_now.command` เพื่อ deploy**
