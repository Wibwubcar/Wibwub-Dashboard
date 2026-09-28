# WIBWUB Weekly Update (wibwub-monday-update) — 27 ก.ย. 2569 20:15–20:50

## Protection: M5 มี 9 เดือนทั้ง Dashboard + Mobile — ไม่ต้องแก้

## STEP 1 Shipnity ✅
- Export 1–30 ก.ย. (preset "เดือนนี้"), ไฟล์เดียว .xlsx → ไฟล์ลง Downloads และ auto-mover ย้ายเข้า Data Shipnity/Data_27-09-2026.xlsx (32.2MB, ข้อมูลถึง 27/09 20:12) — **ปัญหาดาวน์โหลดไม่ลงเมื่อ 25–26 ก.ย. หายแล้ว**
- copy เป็น Data_กันยายน.xlsx ด้วย (ทับของเดิม 25 ก.ย.)

## STEP 2 Affiliate ⏭️ ไม่มีข้อมูลใหม่
- หน้า Performance ยังแสดงข้อมูลถึง 25 ก.ย. — ไฟล์ Transaction_Analysis_Creator_List_20260901-20260925.xlsx มีอยู่แล้ว (GMV 1,777,507 / 955 creators ตรงกับ AF_GMV/AFI_GMV) → ไม่ export ซ้ำ ไม่แก้ arrays

## STEP 3 Top Products ✅
- Recompute เฉพาะ ก.ย. (1–27) จากไฟล์ ก.ย. ทุกไฟล์ใน Data Shipnity (union, dedup order+sku+qty — วิธีเดียวกับรอบ 25 ก.ย.) ม.ค.–ส.ค. คงเดิม
- ALL_PRODUCTS v = v เดิม − ก.ย.เดิม + ก.ย.ใหม่; q บวก delta; PROD_MO[ก.ย.] + label "ก.ย. (1-27)"
- Dashboard: ตาราง 15 สินค้า (คอลัมน์ รวม/จำนวน), KPI ยอดรวม ฿74.85M → ฿75.38M, ชิ้น 300K → 303K, Sugar 500ml ฿6.83M · 21,870 ชิ้น
- ลำดับ Top 15 ไม่เปลี่ยน; คอลัมน์แยกช่องทาง/กราฟ pr_top10, pr_channel ยังเป็นข้อมูลเดิม (ม.ค.–11/14 ก.ย.) เหมือนรอบก่อน

## STEP 5 ✅ sw.js v1280 → v1281, commit e412171 — รอกด push_now.command
- หมายเหตุ: WIBWUB_Affiliate_Dashboard.html มีการแก้ไขค้าง (uncommitted) จาก automation อื่น — ไม่ได้ commit รวมในรอบนี้
