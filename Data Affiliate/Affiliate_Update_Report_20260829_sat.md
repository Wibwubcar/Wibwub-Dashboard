# รายงานอัปเดต WIBWUB Affiliate — เสาร์ 29 ส.ค. 2569

## ช่วงข้อมูล
1–26 ส.ค. 2569 (TikTok เลือกได้ล่าสุดถึง 26 ส.ค. — วันที่ 27–29 ยังเป็นสีเทา, header ระบุ "อัปเดตเมื่อ: 26 ส.ค. 2026")
เป็นช่วงเดียวกับรอบวันศุกร์ที่ 28 ส.ค. แต่ TikTok ปรับตัวเลขย้อนหลังขึ้นเล็กน้อย

## ตัวเลขหลัก (ส.ค. 1–26)
| รายการ | ค่า | เทียบรอบก่อน |
|---|---|---|
| GMV | ฿1,426,449 | +182 |
| Net (หลังคืนเงิน) | ฿1,403,152 | +182 |
| ค่าคอมมิชชั่น | ฿163,882 | +386 |
| ครีเอเตอร์ที่มียอดขาย | 718 | ไม่เปลี่ยน |
| ยอดคืนเงิน | ฿23,298 | — |
| แถวในไฟล์ครีเอเตอร์ | 7,443 | — |

## ไฟล์ที่ดาวน์โหลด (4 ไฟล์ เข้าโฟลเดอร์ถูกต้องทั้งหมด)
- `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260801-20260826.xlsx`
- `Data Affiliate/สินค้า/Transaction_Analysis_Product_List_20260801-20260826.xlsx`
- `Data Affiliate/วีดีโอ/Transaction_Analysis_Video_List_20260801-20260826.xlsx`
- `Data Affiliate/ไลฟ์สตรีม/Transaction_Analysis_Live_List_20260801-20260826.xlsx`

LaunchAgent `com.wibwub.download-mover` ย้ายไฟล์ออกจาก Downloads ให้อัตโนมัติเรียบร้อย — Downloads สะอาด

## สิ่งที่แก้ในไฟล์
**WIBWUB_Affiliate_Dashboard.html** (index สุดท้ายของ rolling window = ส.ค.)
- `AF_GMV` ...,1452748,**1426449**
- `AF_NET` ...,1428498,**1403152**
- `AF_COM` ...,169224,**163882**
- `AF_CR` = 718 (เท่าเดิม ไม่ต้องแก้)
- `PRODUCTS` — ตรวจแล้ว `cr`/`vid` ตรงกับไฟล์สินค้าทั้ง 7 รายการ ไม่มีการแก้
- `VIDEOS` — 7,038 entries, updated 0 / new 0 (ข้อมูลตรงกับ export อยู่แล้ว)
- KPI "ผ่าน 718 creators · ส.ค. 1-26" ถูกต้องอยู่แล้ว

**WIBWUB_Mobile.html**
- `AFI_GMV` / `AFI_NET` / `AFI_COMM` index สุดท้าย (`สค.69 (1-26)`) อัปเดตตรงกัน
- KPI card `฿1,426K · 718 creators` ถูกต้องอยู่แล้ว

**sw.js** — `wibwub-v880` → `wibwub-v881`
**push_now.command** — regenerate + chmod +x

Backup: `WIBWUB_Affiliate_Dashboard.html.bak_20260829_run`, `WIBWUB_Mobile.html.bak_20260829_run`

## ผลตรวจสอบ (verify ก่อน commit)
```
WIBWUB_Affiliate_Dashboard.html | 6 +++---
WIBWUB_Mobile.html              | 6 +++---
sw.js                           | 2 +-
3 files changed, 7 insertions(+), 7 deletions(-)
```
เปลี่ยนเฉพาะ 7 บรรทัดที่ตั้งใจแก้ — ต่ำกว่าเกณฑ์ 50% มาก
`node` eval ผ่านทั้ง `VIDEOS` (7,038), `PRODUCTS`, `AFI_*`

## บั๊กที่เจอและแก้ไปแล้ว (สำคัญ — ควรอัปเดตใน skill)
1. **`vid_merge.py` เขียน label `date:` ผิด** — ฟังก์ชัน `date_label()` ใช้ "สองเดือนสุดท้าย" แต่ของจริงในไฟล์ใช้ "เดือนแรก–เดือนสุดท้าย" ที่มียอด ทำให้ครั้งแรกเขียนทับ 178 entries เป็น `ก.ค.–ส.ค.` แทน `มิ.ย.–ส.ค.` (ตรวจ HEAD แล้ว 146/146 entries ที่มี 3 เดือนขึ้นไปใช้ first–last ทั้งหมด) → แก้กลับหมดแล้ว และแก้ `vid_merge.py` (สำเนาเก็บไว้ที่ `All/scripts/vid_merge.py`)
2. **`navigate` แบบ standalone ใช้ได้ปกติ ไม่ค้าง** — ตรงกันข้ามกับที่ skill เตือน; กลับกันคือ `navigate` ใน `browser_batch` จะ error "Can't interact with browser internal pages" ถ้า tab อยู่ที่ `chrome://newtab`
3. **คอลัมน์ไฟล์ครีเอเตอร์ไม่ตรงกับ skill** — skill ระบุ returns=col2, orders=col3, commission=col10 แต่ export เวอร์ชันนี้เป็น GMV=col1, คืนเงิน=col4, คอมมิชชั่น=col21 → ต้องอ้างอิงด้วย "ชื่อหัวคอลัมน์" ไม่ใช่ index
4. **`PRODUCTS.cr`/`vid` มาจากคอลัมน์ค่าเฉลี่ยรายวัน** (`ครีเอเตอร์ที่มียอดขายเฉลี่ยรายวัน` / `วิดีโอที่มียอดขายเฉลี่ยรายวัน`) ไม่ใช่คอลัมน์ `วิดีโอ` ดิบ
5. **แถวแรกของไฟล์สินค้าเป็นแถวคำอธิบาย** ต้อง `.iloc[1:]`
6. **Reports panel ไม่รีเฟรชเอง** — สถานะค้างที่ "กำลังส่งออก" ~8 นาที ต้อง reload หน้า (F5) ถึงจะเห็นไฟล์พร้อมโหลด

## ขั้นตอนถัดไป
ดับเบิลคลิก **`push_now.command`** เพื่อ push ขึ้น GitHub (ยังไม่ได้ push ตามที่ระบุใน task)
