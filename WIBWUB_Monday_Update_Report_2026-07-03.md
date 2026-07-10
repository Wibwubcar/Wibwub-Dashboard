# WIBWUB Weekly Update — ศุกร์ 3 ก.ค. 2569 (automated run)

**สรุป: ดึงข้อมูลใหม่ + เซฟไฟล์เรียบร้อย แต่ "ยังไม่แก้ dashboard / ไม่ push" รอบนี้ — เพราะยังไม่ถึงเวลาเปิดเดือนกรกฎาคม (มีข้อมูลแค่ 1 วัน + ไฟล์ platform sales ยังไม่มา)**

---

## ✅ สิ่งที่ทำสำเร็จรอบนี้ (non-destructive)

1. **Shipnity export (STEP 1)** — ตั้งช่วง 1–3 ก.ค. 2569, filter "สินค้าในออเดอร์", export ไฟล์เดียว
   - เซฟ: `Data Shipnity/Data_03-07-2026.xlsx` และ `Data Shipnity/Data_กรกฎาคม.xlsx` (2,096 แถว)
2. **Affiliate Transaction Analysis (STEP 2)** — TikTok Affiliate → Creator List
   - เซฟ: `Data Affiliate/Transaction_Analysis_Creator_List_20260701-20260701.xlsx`
   - ตัวเลข **1 ก.ค.**: GMV **฿30,570** · Net **฿30,384** · ค่าคอม **฿3,812** · 61 creators (95 แถว)

## ⛔ สิ่งที่ "ไม่ทำ" รอบนี้ และเหตุผล

### 1) ข้อมูลกรกฎาคมยังมีแค่วันเดียว
- หน้า TikTok Affiliate ระบุ **"อัปเดตเมื่อ 1 ก.ค. 2026 0:00"** — date picker เลือกได้แค่ **1 ก.ค.** (วันที่ 2–3 เป็นสีเทา)
- Export จึงได้ช่วง `20260701-20260701` = ข้อมูลวันเดียว ยังไม่พอเปิด slot เดือนใหม่

### 2) M5 guard: แก้แล้ว "revert กลับ" เพื่อกันไม่ให้ dashboard พัง
- Protection script บังคับให้ `M5` มี 7 เดือน (เพิ่ม "ก.ค.") — ทำไปแล้วตอนต้น
- **แต่** array ข้อมูล SALES ทุกตัวใน `WIBWUB_Dashboard.html` + `WIBWUB_Mobile.html` ยังมีแค่ **6 ช่อง (ม.ค.–มิ.ย.)**: `SH_REV, TK_REV, LZ_REV, FB_REV, LINE_REV, TOTAL_REV, SH_ORD, ...` (~25 arrays)
- render loop วนตาม `M5.length` → ถ้า M5=7 แต่ data=6 จะได้ `SH_REV[6]=undefined` → กราฟ ก.ค. โชว์ **"฿undefined" / NaN%** ทั้ง Mobile และ Dashboard
- ไฟล์ platform sales (Shopee zip / Lazada / TikTok / Line) **ไม่ได้อยู่ใน scope ของ task จันทร์นี้** และยังไม่มีข้อมูล ก.ค. → เติม array ให้ครบ 7 ไม่ได้
- **จึง revert `M5` กลับเป็น 6 เดือน** ทั้ง 2 ไฟล์ → dashboard กลับสู่สถานะ "มิ.ย. ครบ" ที่ consistent ตามเดิม (git ยืนยัน HTML ไม่มี diff)

### 3) Affiliate arrays: ยังไม่เปิด slot กรกฎาคม (structural change — รอยืนยัน)
ยืนยันซ้ำคำเตือนจากรอบ 2 ก.ค.:
- Layout เป็น rolling window ไม่ตรงกับสูตร `month_idx = month-1`:
  - `AFI_MONTHS=['พย.68','ธค.68','มค.69','กพ.69','มีนา.69','เมษา.69','พค.69','มิย.69']` → **index 7 = มิ.ย. 2026**
  - ก.ค. ต้องเป็น **index 8 (append)** ไม่ใช่ index 6 (ถ้าใช้สูตรตรง ๆ จะ**ทับ พ.ค.**)
- `WIBWUB_Affiliate_Dashboard.html` ใช้ `CREATOR_MONTHS` เป็น window **4 ช่อง/creator** (~110 creators) — คนละขนาดกับ Mobile (8) และ `PROD_MO` (6)
- การเปิดเดือนใหม่ต้องขยายพร้อมกันหลาย array คนละ layout → เป็น structural change เสี่ยงสูง **ทำแบบ unattended ไม่ปลอดภัย**

## 📊 สถานะ dashboard ปัจจุบัน (ตรวจแล้ว = ปัจจุบัน, ไม่พัง)
- SALES + Affiliate = "มิ.ย. 2569 ครบ" (Affiliate มิ.ย.: GMV ฿642,490 / Net ฿632,313 / Comm ฿79,284)
- ไม่มี HTML diff ค้าง → **ไม่ bump sw.js / ไม่ commit / ไม่สร้าง push** (ไม่มีอะไรจะ push)

## ▶️ ขั้นถัดไป (เมื่อพร้อมทำ July rollover เต็ม)
ต้องทำพร้อมกันในรอบเดียว (แนะนำยืนยันก่อน):
1. รอ TikTok Affiliate มีข้อมูล ก.ค. หลายวัน + ดาวน์โหลดไฟล์ platform sales เดือน ก.ค. (Shopee/Lazada/TikTok/Line)
2. **Append index 6** ให้ทุก SALES calendar array (SH_REV…TOTAL_ORD, TK_AFI, TK_NET ฯลฯ) แล้วค่อยปล่อย `M5`=7
3. **Append index 8** ให้ `AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM` (Mobile) — ห้ามใช้ index 6
4. ขยาย `CREATOR_MONTHS` (Affiliate_Dashboard, window 4) + `PROD_MO` (window 6) ตาม layout จริงของแต่ละตัว
5. Bump sw.js → commit → สร้าง push_now.command

---
*ไฟล์ข้อมูลดิบรอบนี้เซฟไว้ครบใน Data Shipnity/ และ Data Affiliate/ พร้อมใช้ตอน rollover*
