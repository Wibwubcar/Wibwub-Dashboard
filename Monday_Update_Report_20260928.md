# WIBWUB Weekly Update (wibwub-monday-update) — 28 ก.ย. 2569 (จันทร์) 09:13–09:50

## Protection: M5 มี 9 เดือนทั้ง Dashboard + Mobile (ก.ย. = เดือน 9) — ไม่ต้องแก้

## STEP 1 Shipnity ✅
- ใช้ preset "เดือนนี้" (1–30 ก.ย. 2569), ไฟล์เดียว .xlsx → `Data_28-09-2026.xlsx` (32.7MB, 35,273 แถว, ข้อมูลถึง 28/09 09:12)
- Export ใช้เวลา ~15 นาที (progress ช้ากว่าปกติ) แต่ไฟล์ดาวน์โหลดสำเร็จ
- cp เข้า `Data Shipnity/Data_28-09-2026.xlsx` + `Data_กันยายน.xlsx` (ทับของเดิม)

## STEP 2 Affiliate ⏭️ ไม่มีข้อมูลใหม่
- หน้า Performance ยังระบุ "อัปเดตเมื่อ 25 ก.ย. 2026" → ข้อมูลเท่ากับไฟล์ `Transaction_Analysis_Creator_List_20260901-20260925.xlsx` ที่มีอยู่แล้ว (GMV 1,777,507 / 955 creators ตรงกับ AF_GMV/AFI_GMV) → ไม่ export ซ้ำ

## STEP 3 Top Products ✅
- วิธี: หาแถวใหม่ใน Data_28-09 ที่ไม่อยู่ในไฟล์ ก.ย. เดิมทุกไฟล์ (dedup order+sku+qty) → 516 แถว (27/09 20:15 – 28/09 09:12), ยอด ฿133,175 · 671 ชิ้น (ราคา>0)
- Map ตาม SKU หลักเข้า 15 กลุ่ม (X-Glass 1L ไม่นับรวม X-Glass 100ml เพราะแยกตามขนาด) แล้วบวกเข้า ก.ย. (ม.ค.–ส.ค. คงเดิม)
- Mobile: ALL_PRODUCTS v/q, PROD_MO[ก.ย.], label "ก.ย. (1-28)"
- Dashboard: ตาราง 15 สินค้า (รวม/จำนวน), KPI ฿75.38M → ฿75.51M, 303K → 304K ชิ้น, Sugar 500ml ฿6.84M · 21,907 ชิ้น
  - หมายเหตุ: KPI รวมคำนวณเป็น (ค่าที่แสดงเดิม + delta) เพราะไม่มีตัวเลขฐานแบบละเอียด — ตัวเลขประมาณการ ±0.01M / ±1K
- ลำดับ Top 15 ไม่เปลี่ยน; คอลัมน์แยกช่องทางยังเป็นข้อมูลเดิม (เหมือนรอบก่อน)

## STEP 4 Affiliate arrays ⏭️ ไม่แก้ (ไม่มีข้อมูลใหม่)

## STEP 5 ✅ sw.js v1294 → v1295, commit 2ca4869 — รอกด push_now.command
- ไม่ได้ commit `WIBWUB_Affiliate_Dashboard.html` เพราะมีการแก้ไขค้างจาก automation อื่น (ไม่ได้แก้ในรอบนี้)
- sandbox ลบ `.git/index.lock` / `HEAD.lock` ไม่ได้ — push_now.command จะลบให้ก่อน push
