# WIBWUB Affiliate Auto-Update — รายงานสรุป (รอบบ่าย)

**วันที่รัน:** เสาร์ 15 ส.ค. 2026 (รอบที่ 2 ของวัน)
**ช่วงข้อมูล:** 1–13 ส.ค. 2026 — TikTok ขยับ "อัปเดตเมื่อ" เป็น 13 ส.ค. 2026 0:00 (GMT+7) แล้ว จึงดึงได้เพิ่มอีก 1 วันจากรอบเช้า (1–12)

## STEP 1–3: ดาวน์โหลดไฟล์
Export ครบ 4 tab แล้วดาวน์โหลดจาก reports panel — LaunchAgent `com.wibwub.download-mover` ย้ายเข้าโฟลเดอร์ปลายทางให้อัตโนมัติ

| Tab | ไฟล์ | ขนาด | ปลายทาง |
|---|---|---|---|
| ครีเอเตอร์ | Transaction_Analysis_Creator_List_20260801-20260813.xlsx | 468,138 B | Data Affiliate/ครีเอเตอร์/ |
| สินค้า | Transaction_Analysis_Product_List_20260801-20260813.xlsx | 19,023 B | Data Affiliate/สินค้า/ |
| วีดีโอ | Transaction_Analysis_Video_List_20260801-20260813.xlsx | 1,021,025 B | Data Affiliate/วีดีโอ/ |
| ไลฟ์สตรีม | Transaction_Analysis_Live_List_20260801-20260813.xlsx | 54,552 B | Data Affiliate/ไลฟ์สตรีม/ |

## STEP 4: ตัวเลข Affiliate (rolling window — เขียนทับ index สุดท้าย = ส.ค.)

| ค่า | เดิม (1-12) | ใหม่ (1-13) | เปลี่ยน |
|---|---|---|---|
| GMV | 656,761 | **699,495** | +42,734 |
| NET | 641,279 | **683,618** | +42,339 |
| Commission | 77,399 | **82,404** | +5,005 |
| Creators | 393 | **409** | +16 |

- `WIBWUB_Affiliate_Dashboard.html` → AF_GMV / AF_NET / AF_COM / AF_CR (index 7 = ตัวสุดท้าย), label `AF_MO` เปลี่ยน "ส.ค. (1-12)" → "ส.ค. (1-13)"
- `WIBWUB_Mobile.html` → AFI_GMV / AFI_NET / AFI_COMM (index 9 = ตัวสุดท้าย), label "สค.69 (1-12)" → "สค.69 (1-13)"
- ตรวจแล้ว: array ยาว 8 (dashboard) / 10 (mobile) เท่ากับ label array, label สุดท้ายตรงกับเดือนที่กำลังประมวลผล → เขียนทับถูกช่อง ไม่ทับเดือนก่อนหน้า
- KPI: dashboard "ครีเอเตอร์ที่มียอด" 393 → 409 · mobile mks-grid "฿657K / 393 creators" → **฿699K / 409 creators**

Column mapping ที่ใช้ (ยืนยันจาก header จริงอีกครั้ง ไม่ตรงกับที่ SKILL.md ระบุ):
GMV=col1, การคืนเงิน=col4, คำสั่งซื้อ=col5, ค่าคอมมิชชั่น=col21, ข้อมูลเริ่ม `.iloc[2:]`

## STEP 5: PRODUCTS cr/vid
ไฟล์สินค้า 72 รายการ (vid=col13 "วิดีโอที่มียอดขายเฉลี่ยรายวัน", cr=col19 "ครีเอเตอร์ที่มียอดขายเฉลี่ยรายวัน")

เปลี่ยนแปลง 1 รายการ: **WIBWUB Sugar** vid 18 → 17 (cr คงที่ 17)
ที่เหลือเท่าเดิม: Leather Wipes 32/29 · Interior wipes 22/21 · CLEANER 6/7 · Interior 5/5 · Visible 2/2
**WIBWUB Refresh คง 0/0** — สินค้าที่ควรจับคู่ชื่อจริงคือ "WIBWUB Refresh Leather Cleaner" (4/4) แต่ชื่อมีคำว่า Leather จึงถูกกฎ mapping ของ skill ("Refresh ที่ไม่มี Leather") ตัดออก เหมือนทุกรอบก่อนหน้า — **ควรแก้กฎ mapping ใน skill** ถ้าต้องการให้สินค้านี้มีตัวเลข

## STEP 5B: VIDEOS array
- ไฟล์วีดีโอ parse ได้ **5,070 แถว** (zipfile + regex เพราะเป็น inlineStr XML)
- entries เดิม 5,398 → **5,514** (แก้ค่าเดือน ส.ค. 76 รายการ, เพิ่มใหม่ 116 รายการ)
- เขียนแบบ line-level: แตะเฉพาะบรรทัดที่ค่า `aug` เปลี่ยนจริง + ต่อท้ายรายการใหม่ บรรทัดอื่นคงเดิม verbatim (กันปัญหา backslash escape สะสม และ diff บวมที่เคยเจอรอบก่อน)
- ตรวจ `node eval` ผ่านไม่ error · aug > 0 = **427 คลิป** · GMV ส.ค. รวมจากวีดีโอ = **575,795**
- diff รวม: +205 / −89 บรรทัด จากไฟล์ 9,123 บรรทัด (≈3%) — ต่ำกว่า threshold 50% มาก ปลอดภัย commit
- product 'Unknown' 36 → 37 (เพิ่ม 1 จากคลิปใหม่ที่ product_id ยังไม่มีคู่เทียบ)

## STEP 6: Cache & push
- `sw.js`: wibwub-v678 → **wibwub-v679**
- เขียน `push_now.command` ใหม่ (add 3 ไฟล์ + commit "auto-update: Affiliate 2026-08-15 (1-13 Aug)" + push) chmod +x แล้ว

## หมายเหตุการรัน browser
- URL `insights/transaction-analysis` redirect ไปหน้า "ผลการดำเนินงาน" — ตาราง Transaction Analysis อยู่ในส่วน "รายละเอียด" ท้ายหน้าเดียวกัน (ไม่มีเมนู sidebar แยก) ต้อง `find` + `scroll_to` ลงไป
- tab ตั้งต้นที่ chrome://newtab ทำให้ browser_batch error → เรียก `navigate` เดี่ยว 1 ครั้งก่อน (ไม่ hang)
- trigger export ทั้ง 4 tab รวดเดียวแล้วค่อย reload หน้าเพื่อดาวน์โหลด เร็วกว่ารอทีละ tab (panel ไม่ poll เอง ต้อง reload)
- reports panel filter ตาม tab ที่เปิดอยู่ ต้องสลับ tab ก่อนกดไอคอน "บันทึกการดาวน์โหลดไฟล์" ทุกครั้ง

## ต้องทำต่อ
ดับเบิลคลิก `push_now.command` เพื่อ push ขึ้น GitHub
