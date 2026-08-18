# WIBWUB Affiliate Update — 2026-08-17 (Monday)

**ช่วงข้อมูล:** 01/08/2026 – 15/08/2026 (TikTok อัปเดตข้อมูลถึง 15 ส.ค. 0:00 — 16-17 ส.ค. ยัง greyed out)

## ไฟล์ที่ดาวน์โหลด (LaunchAgent ย้ายอัตโนมัติ)
- ครีเอเตอร์/ ← Transaction_Analysis_Creator_List_20260801-20260815.xlsx (6,018 แถว)
- สินค้า/ ← Transaction_Analysis_Product_List_20260801-20260815.xlsx (72 แถว)
- วีดีโอ/ ← Transaction_Analysis_Video_List_20260801-20260815.xlsx (5,308 แถว)
- ไลฟ์สตรีม/ ← Transaction_Analysis_Live_List_20260801-20260815.xlsx

## ตัวเลขเดือน ส.ค. (1-15)
| | เดิม (1-14) | ใหม่ (1-15) |
|---|---|---|
| GMV | ฿746,785 | ฿793,803 |
| Net GMV | ฿729,810 | ฿776,827 |
| Commission | ฿87,753 | ฿93,464 |
| Creators | 434 | 459 |

## ไฟล์ที่แก้
- `WIBWUB_Affiliate_Dashboard.html` — AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR (index สุดท้าย = ส.ค.), KPI ครีเอเตอร์ที่มียอด 434→459, PRODUCTS cr/vid, VIDEOS array
- `WIBWUB_Mobile.html` — AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM, mks-grid KPI ฿747K→฿794K
- `sw.js` — v709 → v710

## PRODUCTS cr/vid (ค่าเฉลี่ยรายวัน)
Leather Wipes 34/31 · Interior Wipes 22/21 · Sugar 16/16 · Cleaner 6/7 · Interior 5/5 · Refresh 0/0 (ไม่มี match ตาม mapping) · Visible 2/2

## VIDEOS
อัปเดต 80 รายการ · เพิ่มใหม่ 114 รายการ · รวม 5,732 รายการ (ส.ค. GMV รวม ฿655,325)

## หมายเหตุ
- Column layout ของไฟล์ ครีเอเตอร์ เปลี่ยนจากที่ skill ระบุไว้ (col[2]=returns, col[10]=commission) — ตอนนี้ต้องอ่านตามชื่อ column: `การคืนเงิน` (index 4) และ `ค่าคอมมิชชั่นโดยประมาณ` (index 21) ควรอัปเดต SKILL.md
- Export ใช้เวลา ~8 นาที และ panel ไม่ auto-refresh ต้อง reload หน้าเพื่อดูสถานะล่าสุด

**ถัดไป:** ดับเบิ้ลคลิก `push_now.command` เพื่อ push ขึ้น GitHub
