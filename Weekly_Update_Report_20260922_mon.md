# WIBWUB Weekly Update — วันจันทร์ 22 ก.ย. 2569

## สรุปผล: สำเร็จทั้งหมด ✅

### STEP 1 — Shipnity Export
- ดาวน์โหลดสำเร็จ (ใช้เวลานานผิดปกติ ~3-4 นาทีต่อรอบ export ต้องลองใหม่ 3 รอบเพราะ dialog ค้างที่ 100% แล้วไม่ trigger auto-download ในสอง attempt แรก — attempt ที่ 3 สำเร็จ)
- ไฟล์บันทึกที่: `Data Shipnity/Data_22-09-2026.xlsx` (29,178 ออเดอร์, ครอบคลุม 1-22 ก.ย. 2569)
- หมายเหตุ: Chrome ในเซสชันนี้ตั้งค่าดาวน์โหลดตรงเข้าโฟลเดอร์ปลายทางอยู่แล้ว (ไม่ผ่าน Downloads/) ตรวจสอบไฟล์ผ่าน bash เจอที่ path ปลายทางถูกต้อง

### STEP 2 — Affiliate Transaction Analysis
- ดาวน์โหลดสำเร็จ: `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260901-20260920.xlsx`
- ช่วงวันที่: 1-20 ก.ย. 2569 (20 ก.ย. คือวันล่าสุดที่ TikTok มีข้อมูลพร้อม ณ ตอนรัน — 21-22 ก.ย. ยัง grey out)
- ⚠️ รูปแบบไฟล์เปลี่ยนจาก 12 คอลัมน์ (ตามที่ระบุใน skill) เป็น **22 คอลัมน์** พร้อม header 2 แถว — ปรับ mapping ใหม่: GMV=col[1], การคืนเงิน=col[4], ค่าคอมมิชชั่น=col[21] (ตรวจสอบ column header ทุกตัวแล้วยันยันถูกต้อง, ยอดรวมตรงกับหน้า TikTok Affiliate Center: GMV ฿1,426,508 ≈ 1,426,507.83 ที่แสดงบนหน้าเว็บ)

### STEP 3 — ภาพรวมธุรกิจ / Top Products (จาก Shipnity)
- ใช้ไฟล์รายเดือนล่าสุด 1 ไฟล์/เดือน (Data_มกราคม.xlsx ... Data_สิงหาคม.xlsx + Data_22-09-2026.xlsx) แทนการไล่ไฟล์รายวันทั้งหมด 150+ ไฟล์ (ซ้ำซ้อนเพราะแต่ละไฟล์รายวันเป็น cumulative snapshot ของเดือนนั้น)
- อัปเดต `ALL_PRODUCTS` ใน WIBWUB_Mobile.html (v/q ของสินค้า Top 15 ทั้งหมด, ยอด ม.ค.–22 ก.ย.)
- อัปเดต `PROD_MO` คอลัมน์ ก.ย. (index สุดท้าย) เป็นยอด 1-22 ก.ย. เต็ม (เดิมมีแค่ 1-18 ก.ย.)
- อัปเดตตาราง Top Products ใน WIBWUB_Dashboard.html — แก้เฉพาะคอลัมน์ "รวม (฿)" และ "จำนวน" (คอลัมน์ breakdown ราย platform ไม่แตะ ตามธรรมเนียมเดิมที่ระบุว่า "channel split not recomputed after 11 ก.ย.")
- อันดับสินค้าทั้ง 15 รายการไม่เปลี่ยนแปลง (ลำดับเดิมยังตรงกับยอดใหม่)
- mk/mkq (งบการตลาด) คงค่าเดิมตามกฎ ไม่ recompute

### STEP 4 — Affiliate Arrays
- `WIBWUB_Affiliate_Dashboard.html`: อัปเดต index สุดท้าย (ก.ย.) จาก "(1-19)" → "(1-20)"
  - AF_GMV: 1,334,642 → 1,426,508
  - AF_NET: 1,241,216 → 1,404,445
  - AF_COM: 146,703 → 156,889
  - AF_CR (creators): 771 → 811
- `WIBWUB_Mobile.html`: อัปเดตชุดเดียวกันใน AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM (index สุดท้าย)

### STEP 5 — sw.js + Git
- 🛡️ M5 protection check: ผ่าน (ทั้ง 2 ไฟล์มี M5 ครบ 9 เดือนอยู่แล้ว ไม่ต้องแก้)
- Bump sw.js: v1209 → **v1210**
- Commit: `edef7a7 auto-update: Monday 2026-09-22 — Shipnity + Affiliate + ภาพรวมธุรกิจ` (4 files changed)
- ⚠️ พบ `.git/index.lock` ค้างจาก process อื่นที่รันคู่ขนานอยู่ในrepo เดียวกัน (เห็น commit อื่นๆ auto-update หลายตัวแทรกเข้ามาระหว่างรัน) — รอ lock คลายแล้ว commit สำเร็จปกติ
- สร้าง `push_now.command` ไว้แล้ว — รอ user กดเพื่อ push ขึ้น GitHub

## สิ่งที่ควรทราบ / Follow-up
1. **Affiliate file format เปลี่ยนจาก 12 → 22 คอลัมน์** ควรอัปเดต skill ให้ตรงกับ format ปัจจุบัน (เหมือนที่เคยเกิดกับปัญหาชื่อตัวแปร gmvD/netD เมื่อ 2026-07-06)
2. Shipnity export ใช้เวลานานผิดปกติ (~3-4 นาที/ครั้ง, บางรอบ export เสร็จ 100% แต่ไม่ auto-download ต้องลองใหม่) — ควรจับตาดูว่าเป็นปัญหาที่ฝั่ง Shipnity หรือ browser session
3. ข้อมูล Affiliate เป็นช่วง 1-20 ก.ย. (ไม่ใช่ 1-22) เพราะ TikTok ยังไม่มีข้อมูล settle สำหรับ 21-22 ก.ย. ณ เวลาที่รัน — รอบถัดไปจะได้ข้อมูลที่สมบูรณ์กว่า
