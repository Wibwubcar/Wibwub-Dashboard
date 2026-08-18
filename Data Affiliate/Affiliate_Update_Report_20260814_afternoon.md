# WIBWUB Affiliate Auto-Update — 14 ส.ค. 2569 (รอบบ่าย)

**สถานะ: สำเร็จ** — ข้อมูล TikTok อัปเดตถึง **12 ส.ค. 2026** (หน้าเว็บระบุ "อัปเดตเมื่อ: 12 ส.ค. 2026 0:00"; วันที่ 13–15 ยังเป็นสีเทา)

รอบนี้ได้ข้อมูลใหม่กว่ารอบเช้า (ซึ่งได้แค่ถึง 11 ส.ค.) จึงมีการเปลี่ยนแปลงจริงทุกส่วน

## STEP 1–3 — ดาวน์โหลดและจัดไฟล์

ตั้งช่วงวันที่ 01/08/2026 – 12/08/2026 แล้ว export ครบ 4 แท็บ ไฟล์ถูกจัดเข้าโฟลเดอร์เรียบร้อย

| แท็บ | ไฟล์ | ปลายทาง |
|---|---|---|
| ครีเอเตอร์ | Transaction_Analysis_Creator_List_20260801-20260812.xlsx | Data Affiliate/ครีเอเตอร์/ |
| สินค้า | Transaction_Analysis_Product_List_20260801-20260812.xlsx | Data Affiliate/สินค้า/ |
| วีดีโอ | Transaction_Analysis_Video_List_20260801-20260812.xlsx | Data Affiliate/วีดีโอ/ |
| ไลฟ์สตรีม | Transaction_Analysis_Live_List_20260801-20260812.xlsx | Data Affiliate/ไลฟ์สตรีม/ |

## STEP 4 — ตัวเลขภาพรวมเดือน ส.ค.

"ส.ค." เป็น label ตัวสุดท้ายของ array อยู่แล้ว จึง **เขียนทับตำแหน่งเดิม** ไม่ append และไม่แตะเดือนก่อนหน้า

| ค่า | เดิม (1-11 ส.ค.) | ใหม่ (1-12 ส.ค.) |
|---|---|---|
| GMV | 598,401 | **656,761** |
| Net (หลังคืนเงิน) | 584,964 | **641,279** |
| ค่าคอมมิชชั่น | 70,094 | **77,399** |
| ครีเอเตอร์ที่มียอด | 376 | **393** |

ตรวจสอบกับ KPI card บนหน้าเว็บ: GMV ฿656,761.00 (ตรงเป๊ะ), การคืนเงิน ฿15,481.61 vs คำนวณได้ 15,482 (ตรง), ค่าคอมมิชชั่น ฿77,338.57 vs 77,399 (ต่างจากการปัดเศษรายแถว รับได้)

อัปเดตแล้วทั้ง `WIBWUB_Affiliate_Dashboard.html` (AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR + KPI strip) และ `WIBWUB_Mobile.html` (AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM + mks-grid) โดย label เปลี่ยนเป็น "ส.ค. (1-12)" / "สค.69 (1-12)"

## STEP 5 — PRODUCTS (cr / vid)

เปลี่ยนแปลงจุดเดียว: **WIBWUB Refresh Leather Wipes vid 28 → 29** ที่เหลือเท่าเดิมทุกตัว (Interior Wipes 22/21, Sugar 17/18, Cleaner 6/7, Interior 5/5, Visible 2/2, Refresh 0/0) ไม่แตะ gmv/units/monthly/ret ตามกติกา

หมายเหตุ: KPI "ผ่าน X,XXX creators" ที่ SKILL สั่งให้อัปเดต **ไม่มีอยู่ในไฟล์ปัจจุบัน** (บรรทัด 272 เป็น "สินค้าที่ขายผ่าน Affiliate ... 7+") จึงข้ามขั้นตอนย่อยนี้

## STEP 5B — VIDEOS

parse ผ่าน zipfile+regex (ไฟล์เป็น inlineStr, openpyxl อ่านไม่ได้) ได้ 4,938 คลิป

- **updated 76 คลิป** (monthly.aug + units + gmv รวม)
- **เพิ่มใหม่ 5 คลิป** (คลิปที่มี GMV/units > 0 และยังไม่มีใน dashboard)
- รวม entries 5,279 → **5,284**
- ยอด aug รวมใน VIDEOS = 537,564 (เป็น subset ของ GMV รวม เพราะไม่รวมยอดจากไลฟ์/ช่องทางอื่น)

**แก้บั๊กจากรอบก่อน:** เขียนแบบแก้เฉพาะบรรทัดที่เปลี่ยน แทนการ regenerate ทั้ง block และ **ไม่แตะ field `caption` ของ entry เดิมเลย** จึงไม่มีปัญหา backslash สะสมจาก `esc()` อีก — diff รวมทั้งไฟล์อยู่แค่ 96 insertions / 91 deletions (~2% ของไฟล์) เทียบกับ 32% ในรอบก่อน

ตรวจสอบด้วย node: array parse ได้ 5,284 entries, `sum(monthly) === gmv` ครบทุกตัว (mismatch 0)

## STEP 6 — Cache

`sw.js` bump v665 → **v666**, regenerate `push_now.command` (chmod +x) ให้ commit ไฟล์ affiliate/mobile/sw.js

## ⚠️ เรื่องที่ยังต้องตัดสินใจ (ไม่ได้แก้เอง)

### 1. WIBWUB Refresh ยังแมปไม่ได้ — ตัวเลขเป็น 0 ทั้งที่มียอดขายจริง

สินค้าชื่อ "น้ำยาทำความสะอาดเบาะหนังรถยนต์ สูตร pH-Balance..." มียอด ส.ค. **฿27,359** (cr 4, vid 4) แต่ไม่แมปกับ entry ไหนเลย ขณะที่ `WIBWUB Refresh` ใน PRODUCTS ยังเป็น `aug:0, cr:0, vid:0`

ต้นเหตุคือกติกา fuzzy match ของ SKILL ("Refresh ที่ไม่มี Leather") ใช้ไม่ได้ เพราะชื่อจริงในไฟล์เป็นภาษาไทยล้วน ไม่มีคำว่า Refresh — **ต้องเพิ่ม mapping แบบระบุตรง ๆ ใน SKILL** ผมไม่แก้เองเพราะเป็นการเปลี่ยนกติกา ไม่ใช่ข้อมูล

### 2. สินค้าที่ยังไม่มีใน PRODUCTS แต่มียอด ส.ค.

WIBWUB Spot Clean ฿34,298 (5/5), WIBWUB Reflex V.2 ฿8,236, X-Glass Shield ฿4,609, Martini ฿4,537, BANYAKART ฿4,446 และ SKU ย่อยอีกราว 25 ตัว — ถ้าต้องการให้แสดงบน dashboard ต้องเพิ่ม entry ใหม่ (นอกขอบเขต STEP 5 ซึ่งอนุญาตแก้แค่ cr/vid)

### 3. PRODUCTS.monthly.aug ยังเป็นค่าเก่า

ค่าเช่น Leather Wipes `aug:48243` ไม่ตรงกับไฟล์ล่าสุด (฿210,320) เพราะ SKILL ห้ามแก้ field `monthly` — ถ้าต้องการให้กราฟรายเดือนของ tab สินค้าถูกต้อง ต้องแก้กติกาข้อนี้

### 4. ไฟล์ซ้ำใน Downloads

`Transaction_Analysis_Creator_List_20260801-20260812 (1).xlsx` หลุดเข้าโฟลเดอร์ ครีเอเตอร์/ ด้วย (เนื้อหาเหมือนกันทุกไบต์) ลบจาก sandbox ไม่ได้ (Operation not permitted) — ไม่กระทบผลลัพธ์ แต่ควรลบด้วยมือ

## ขั้นตอนถัดไป

รัน `push_now.command` เพื่อ commit + push ขึ้น production
