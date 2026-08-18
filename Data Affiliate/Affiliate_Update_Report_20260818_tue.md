# WIBWUB Affiliate Update — 2026-08-18 (Tuesday)

**ช่วงข้อมูล:** 01/08/2026 – 15/08/2026
TikTok ยังอัปเดตข้อมูลถึง 15 ส.ค. 0:00 เท่านั้น (16, 17, 18 ส.ค. ยัง greyed out ในปฏิทิน) — เป็นวันที่ 3 ติดต่อกันที่ข้อมูลไม่ขยับ

## ไฟล์ที่ดาวน์โหลด (LaunchAgent ย้ายอัตโนมัติจาก Downloads)
- ครีเอเตอร์/ ← Transaction_Analysis_Creator_List_20260801-20260815.xlsx (6,018 แถว)
- สินค้า/ ← Transaction_Analysis_Product_List_20260801-20260815.xlsx (72 แถว)
- วีดีโอ/ ← Transaction_Analysis_Video_List_20260801-20260815.xlsx (5,308 แถว)
- ไลฟ์สตรีม/ ← Transaction_Analysis_Live_List_20260801-20260815.xlsx

## ตัวเลขเดือน ส.ค. (1-15)
| | เดิมใน dashboard | ใหม่ |
|---|---|---|
| GMV | ฿793,677 | ฿793,803 |
| Net GMV | ฿776,700 | ฿776,827 |
| Commission | ฿93,238 | ฿93,464 |
| Creators | 459 | 459 |

TikTok ปรับข้อมูลย้อนหลังเล็กน้อย (+฿126 GMV, +฿226 commission)

## ไฟล์ที่แก้
- `WIBWUB_Affiliate_Dashboard.html` — AF_GMV/AF_NET/AF_COM (index สุดท้าย = "ส.ค. (1-15)"), VIDEOS array (normalize date label), แก้ caption corruption
- `WIBWUB_Mobile.html` — AFI_GMV/AFI_NET/AFI_COMM (index สุดท้าย = "สค.69 (1-15)")
- `sw.js` — v716 → v717

## PRODUCTS cr/vid
ไม่มีการเปลี่ยนแปลง — ตรงกับค่าใน dashboard อยู่แล้ว:
Leather Wipes 34/31 · Interior Wipes 22/21 · Sugar 16/16 · Cleaner 6/7 · Interior 5/5 · Refresh 0/0 · Visible 2/2

## VIDEOS
อัปเดต 0 รายการ · เพิ่มใหม่ 0 รายการ · รวม 5,732 รายการ (ส.ค. GMV รวม ฿655,325)
— ข้อมูลวีดีโอเหมือนเมื่อวานทุกประการ เพราะ TikTok ยังไม่ปล่อยข้อมูลวันใหม่

## ⚠️ Bug ที่พบและแก้แล้ว — caption backslash doubling (สำคัญ ควรแก้ใน SKILL.md)
ฟังก์ชั่น `esc()` ใน STEP 5B ทำ `.replace('\\','\\\\')` กับ caption ที่ **อ่านมาจาก HTML ซึ่ง escape ไว้แล้ว**
→ backslash เพิ่มเป็น 2 เท่าทุกครั้งที่ schedule รัน

หลักฐาน: caption ของ vid_id `7615878290879941909` (creator mycarnooknook)
เดิม `👀` (emoji 👀) กลายเป็น backslash ติดกัน **256 ตัว** ก่อนรันวันนี้ และ **512 ตัว** หลังรัน — คือ doubling มาแล้ว 9 รอบ

**แก้แล้ววันนี้:** ยุบ backslash run กลับเป็น 1 ตัว → caption กลับมาแสดง 👀 ถูกต้อง (ไฟล์เล็กลง 1,022 bytes)

**สิ่งที่ต้องแก้ใน SKILL.md STEP 5B:** entry ที่ parse มาจาก HTML เดิมเป็น source-form อยู่แล้ว **ห้ามส่งผ่าน `esc()` ซ้ำ** — ควร escape เฉพาะ entry ใหม่ที่มาจากไฟล์ xlsx เท่านั้น ถ้าไม่แก้ ปัญหานี้จะกลับมาและ backslash จะโตเป็น 1024, 2048, ... ทุกวัน

## หมายเหตุอื่น
- Column layout ไฟล์ ครีเอเตอร์ ยังต่างจากที่ SKILL.md ระบุ — ต้องใช้ index 4 (`การคืนเงิน`) และ 21 (`ค่าคอมมิชชั่นโดยประมาณ`) ไม่ใช่ 2/10
- ไฟล์ สินค้า: cr = index 19 (`ครีเอเตอร์ที่มียอดขายเฉลี่ยรายวัน`), vid = index 13 (`วิดีโอที่มียอดขายเฉลี่ยรายวัน`)
- Export panel ไม่ auto-refresh — ต้อง reload หน้าถึงจะเห็นปุ่ม "ดาวน์โหลด" (ใช้เวลา ~5 นาที)
- Verify ผ่าน: `node -e eval(VIDEOS)` → 5,732 entries, ไม่ throw

**ถัดไป:** ดับเบิ้ลคลิก `push_now.command` เพื่อ push ขึ้น GitHub
