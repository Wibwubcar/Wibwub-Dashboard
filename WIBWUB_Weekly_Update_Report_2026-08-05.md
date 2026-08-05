# WIBWUB Weekly Update — 5 ส.ค. 2026

## สรุปผล
รันอัตโนมัติ — Shipnity export สำเร็จ, Affiliate export ติด session expired (ข้าม), ไม่มีการแก้ไข dashboard HTML ในรอบนี้ จึงไม่มี commit ใหม่

---

## STEP 0 — Protection (M5)
ตรวจ `M5` ใน `WIBWUB_Dashboard.html`/`WIBWUB_Mobile.html` — มีแค่ 7 เดือน (ม.ค.–ก.ค.) ยังไม่มี ส.ค.

**ไม่แก้ตามสูตร auto-fix ใน SKILL** เพราะ M5 ผูกกับ data arrays รายเดือนอีกจำนวนมาก (SH_REV, TK_REV, LZ_REV, SH_ORD, TK_ORD, LZ_ORD ฯลฯ) ซึ่งทุกตัวมี 7 ค่าเท่ากันพอดี (เดือนที่ปิดรอบแล้ว) — การเติม label "ส.ค." เข้า M5 โดยไม่มีข้อมูลยอดขายแพลตฟอร์ม (Shopee/TikTok/Lazada) เดือนสิงหาคมที่ปิดรอบมาคู่กัน จะทำให้ label กับ data array ยาวไม่เท่ากันและ chart พัง ข้อมูลแพลตฟอร์มเหล่านี้ไม่ได้อยู่ใน scope ของงานสัปดาห์นี้ (Shipnity + Affiliate) — ปล่อยให้ระบบอื่นที่จัดการ platform sales อัปเดตแทนเมื่อเดือนสิงหาคมปิดรอบ

## STEP 1 — Shipnity Export
Export ผ่าน Chrome สำเร็จ: ช่วงวันที่ 1–5 ส.ค. 2569 → บันทึกเป็น `Data Shipnity/Data_05-08-2026.xlsx` และอัปเดต `Data_สิงหาคม.xlsx` (3.89MB)

## STEP 2 — Affiliate Transaction Analysis Export
**ติดปัญหา: Session expired** — เข้า `affiliate.tiktok.com/insights/transaction-analysis` แล้วถูก redirect ไปหน้า marketing (`seller.tiktok.com/us`) พร้อมปุ่ม "Log in" แทนที่จะเป็นหน้า Transaction Analysis ตามกฎใน SKILL.md ("Login หมดอายุ → log และหยุด") จึงหยุดขั้นตอนนี้โดยไม่ export ใหม่ — **ต้อง re-login เข้า TikTok Affiliate Center ในเบราว์เซอร์ก่อนรันครั้งถัดไป**

## STEP 3 — Top Products (ภาพรวมธุรกิจ)
คำนวณ Top 15 จากไฟล์ Shipnity ครบ 8/8 ไฟล์ (พบไฟล์ `Data-มีนา.xlsx` ที่ตั้งชื่อด้วยขีดกลางแทนขีดล่าง — เป็นสาเหตุที่รายงานสัปดาห์ก่อนนับว่า "ขาด" ไฟล์นี้) รวม 186,433 order-lines, 192 สินค้า

อันดับ 1: Wool duster-ไม้ปัดขนแกะ (rev 5,598,925 / qty 8,769)
อันดับ 2: Sugar (Sugar-500ml+Spray) (rev 4,715,037 / qty 15,798)
อันดับ 3: Interior (Interior-500ml+Spray) (rev 3,666,664 / qty 10,618)

**🚫 ข้าม:** ไม่เขียนทับ `ALL_PRODUCTS` (Mobile) และ Top Products chart (Dashboard) — เหตุผลเดิมต่อเนื่องจาก 3 สัปดาห์ก่อน: `ALL_PRODUCTS` มีฟิลด์ `mk`/`mkq` (ยอดขาย marketplace อื่น) ที่ข้อมูล Shipnity อย่างเดียวไม่มี ผลลัพธ์บันทึกไว้ที่ `top15_products_2026-08-05.json`

## STEP 4 — Affiliate Arrays
**ข้าม** — ไม่มีข้อมูล Transaction Analysis ใหม่เนื่องจาก session expired (ดู STEP 2) ไม่แตะ `AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR` หรือ `AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM` ในรอบนี้ — ค่าปัจจุบันยังเป็นของรอบ 4 ส.ค. (ข้อมูลถึง 1-2 ส.ค.)

## STEP 5 — sw.js + Git Commit
**ข้าม** — ไม่มีการแก้ไข `WIBWUB_Mobile.html`, `WIBWUB_Dashboard.html`, หรือ `WIBWUB_Affiliate_Dashboard.html` ในรอบนี้ (ทุก step หลักที่แก้ไฟล์ถูกข้ามด้วยเหตุผลข้างต้น) จึงไม่ bump cache version และไม่สร้าง commit ใหม่

---

## ⚠️ สิ่งที่ต้องตรวจสอบ/ทำต่อ
1. **Re-login TikTok Affiliate Center** ในเบราว์เซอร์ที่เชื่อมต่อ (Browser 1 / macOS) ก่อนรันรอบถัดไป ไม่เช่นนั้น Affiliate arrays จะค้างข้อมูลเก่าต่อไปเรื่อยๆ
2. **ไฟล์ `Data-มีนา.xlsx`** ควร rename เป็น `Data_มีนา.xlsx` (ขีดล่าง) เพื่อให้ script อัตโนมัติในอนาคตหาไฟล์เจอโดยไม่ต้องพึ่ง manual list แบบที่ใช้ในรอบนี้
3. **Top Products ยังไม่อัปเดตต่อเนื่องเป็นสัปดาห์ที่ 4 แล้ว** เพราะข้อมูล marketplace (mk/mkq) ไม่มีมาผสาน — ถ้าต้องการให้ Top Products อัปเดตจริง ต้องมีไฟล์ยอดขาย Shopee/Lazada/TikTok อื่นๆ ป้อนเข้ามาด้วย
4. **M5/platform arrays (SH_REV ฯลฯ)** ยังไม่มีเดือนสิงหาคม — รอข้อมูลยอดขายแพลตฟอร์มเดือนนี้ปิดรอบก่อนจึงจะเติมได้อย่างปลอดภัย
