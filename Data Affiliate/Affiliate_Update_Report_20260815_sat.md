# WIBWUB Affiliate Auto-Update — รายงานสรุป
**วันที่รัน:** เสาร์ 15 ส.ค. 2026
**ช่วงข้อมูล:** 1–12 ส.ค. 2026 (TikTok อัปเดตล่าสุดถึง 12 ส.ค. 2026 0:00 GMT+7 — วันที่ 13–15 ยังเลือกไม่ได้)

## STEP 1–3: ดาวน์โหลดไฟล์
ดาวน์โหลดครบ 4 ไฟล์จาก Transaction Analysis และถูก LaunchAgent ย้ายเข้าโฟลเดอร์ปลายทางอัตโนมัติ (ไม่ต้อง cp เอง)

| Tab | ไฟล์ | ขนาด | ปลายทาง |
|---|---|---|---|
| ครีเอเตอร์ | Transaction_Analysis_Creator_List_20260801-20260812.xlsx | 465,128 B | Data Affiliate/ครีเอเตอร์/ |
| สินค้า | Transaction_Analysis_Product_List_20260801-20260812.xlsx | 18,981 B | Data Affiliate/สินค้า/ |
| วีดีโอ | Transaction_Analysis_Video_List_20260801-20260812.xlsx | 994,117 B | Data Affiliate/วีดีโอ/ |
| ไลฟ์สตรีม | Transaction_Analysis_Live_List_20260801-20260812.xlsx | 51,182 B | Data Affiliate/ไลฟ์สตรีม/ |

## STEP 4: อัปเดตตัวเลข Affiliate (rolling window — เขียนทับ index สุดท้าย = ส.ค.)

| ค่า | เดิม | ใหม่ | เปลี่ยน |
|---|---|---|---|
| GMV | 656,646 | **656,761** | +115 |
| NET | 641,163 | **641,279** | +116 |
| Commission | 77,211 | **77,399** | +188 |
| Creators | 393 | 393 | — |

- `WIBWUB_Affiliate_Dashboard.html` → AF_GMV / AF_NET / AF_COM (AF_CR ไม่เปลี่ยน)
- `WIBWUB_Mobile.html` → AFI_GMV / AFI_NET / AFI_COMM
- ตรวจแล้ว: ทุก array ยาว 8 (dashboard) / 10 (mobile) เท่ากับ label array, label สุดท้าย = "ส.ค. (1-12)" / "สค.69 (1-12)" → เขียนทับถูกช่อง ไม่ทับเดือนก่อนหน้า
- KPI การ์ดใน Mobile แสดง ฿657K อยู่แล้ว (round(656,761/1000) = 657) → ไม่ต้องแก้

## STEP 5: PRODUCTS cr/vid
7 รายการ — ค่าที่คำนวณได้ **เท่าเดิมทุกตัว**: 32/29, 22/21, 17/18, 6/7, 5/5, 0/0, 2/2
("WIBWUB Refresh" ไม่มี match ตามกฎ contains Refresh แต่ไม่ Leather → คง 0/0 เหมือนรอบก่อน)

## STEP 5B: VIDEOS array
- ไฟล์วีดีโอ 4,938 แถว (parse ผ่าน zipfile + regex เพราะเป็น inlineStr)
- เดิม 5,284 entries → ใหม่ **5,398 entries** (เพิ่ม 114, แก้ไข 0)
- ตรวจ: `node eval` ผ่านไม่ error, aug > 0 = 405 คลิป, รวม GMV ส.ค. = 537,564

## STEP 6: Cache & push
- `sw.js`: wibwub-v671 → **wibwub-v672**
- สร้าง `push_now.command` ใหม่ (add 3 ไฟล์ + commit "auto-update: Affiliate 2026-08-15 (sw.js v672)" + push) และ chmod +x แล้ว

## ⚠️ เรื่องที่ต้องรู้ / ตัดสินใจเองระหว่างรัน

**1. เลข column ใน SKILL.md ของไฟล์ครีเอเตอร์ผิด (ต้องแก้ skill)**
Skill ระบุ GMV=col2, returns=col3, commission=col10 — ใช้แล้วได้ NET=602,992 และ COMM=0 ซึ่งผิด
ค่าที่ถูกจากการอ่าน header จริง: **GMV=col1, returns=col4, orders=col5, commission=col21** (ข้อมูลเริ่ม `.iloc[2:]` เพราะแถว index 1 เป็นคำอธิบาย)
ผลลัพธ์จาก mapping ใหม่ตรงกับค่าของวันก่อนหน้าแบบสมเหตุสมผล (656,646 → 656,761) จึงยืนยันว่าถูก
ไฟล์สินค้าก็ไม่ได้ระบุ column ของ cr/vid ไว้ — reverse-engineer ได้ **vid=col13, cr=col19** และตรงกับค่าเดิมในแดชบอร์ดครบทั้ง 6 ตัวที่ match

**2. ต้องย้อนกลับการเขียนทับ VIDEOS ครั้งแรก**
สคริปต์ merge รอบแรกไป recompute field `date` ของ entry เก่าด้วย ทำให้ 2,845 บรรทัดเปลี่ยน (diff 5,810 บรรทัด = 64% ของไฟล์ → เกิน threshold 50% ที่ skill สั่งให้หยุด)
ตรวจแล้วพบ 2 ปัญหา: (ก) label `date` ของ entry เก่าถูกเปลี่ยน ซึ่งรอบก่อน ๆ ไม่เคยทำ (ข) มี 1 entry (vid 7615878290879941909) ที่ backslash ใน caption ถูก escape ซ้ำทุกครั้งที่เขียนไฟล์ — เป็น corruption แบบสะสม
จึงเขียน VIDEOS ใหม่โดย **คงบรรทัดเดิมทั้ง 5,284 บรรทัดแบบ verbatim + ต่อท้าย 114 บรรทัดใหม่เท่านั้น**
diff สุดท้าย: **+120 / -6 บรรทัด** ปลอดภัย commit ได้

**3. หมายเหตุการรัน browser**
- tab เริ่มต้นอยู่ที่ chrome://newtab ทำให้ `browser_batch` error → ต้องเรียก `navigate` เดี่ยว 1 ครั้งก่อน (ไม่ hang)
- panel รายงาน export ไม่ poll เอง ค้างที่ "กำลังส่งออก" 3+ นาที → แก้ด้วยการ reload หน้า
- scroll ธรรมดาได้ screenshot ค้าง → ต้องใช้ `find` หา ref แล้ว `scroll_to`

## สถานะไฟล์
แก้แล้ว 3 ไฟล์: `WIBWUB_Affiliate_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js` (+ `push_now.command`)
ยังไม่ commit/push จากใน sandbox — ให้ automation หรือรัน `push_now.command` เอง
