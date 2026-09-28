# ✅⚠️ WIBWUB Weekly Update (wibwub-monday-update) — 15 ก.ย. 2569 (จันทร์) — รอบที่ 2 — สำเร็จบางส่วน (ซ้ำ)

## สถานะ: Protection check OK / Affiliate arrays อัปเดตแล้ว (โดย automation คู่ขนาน) / Shipnity ยังบล็อกเหมือนรอบแรก / ไม่มีอะไรต้อง commit เพิ่มจากรอบนี้

หมายเหตุ: นี่คือการรัน `wibwub-monday-update` **รอบที่ 2 ในวันเดียวกัน** (ดู `Monday_Update_Report_20260915.md` สำหรับรอบแรก) — ผลลัพธ์ยืนยันปัญหาเดิมซ้ำอีกครั้ง

## สิ่งที่ตรวจสอบ/ทำสำเร็จ

- ✅ **Protection check**: `M5` array ใน `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html` มี 9 เดือน (ม.ค.–ก.ย.) ตรงกับเดือนปัจจุบัน — ไม่ต้องแก้ไข
- ✅ **Affiliate arrays**: พบว่าถูกอัปเดตแล้วโดย automation คู่ขนานอื่น (scheduled task อื่น รัน commit `5a3fe3d` เวลา 18:04 น.) —
  `AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR` ใน `WIBWUB_Affiliate_Dashboard.html` เป็น **ก.ย. (1-13)**: GMV ฿908,468, ตรวจสอบแล้วสมเหตุสมผลเทียบกับตัวเลขที่ automation อื่นยืนยันไว้ (฿908,625 — ต่างกันเล็กน้อยจาก rounding/รอบ export ที่ต่างกัน) — **ไม่แก้ไขซ้ำ** เพื่อไม่ให้ทับข้อมูลที่ถูกต้องอยู่แล้ว

## สิ่งที่ถูกบล็อกอีกครั้ง

- ❌ **Shipnity export — ไฟล์ไม่ลงดิสก์ (ซ้ำเป็นครั้งที่ 3 ของวันนี้)**:
  1. ตั้งช่วงวันที่ 1–15 ก.ย. 2569 ในหน้า `shipnity.com/data/c/purchase` สำเร็จ
  2. ลอง export แบบ **"ไฟล์เดียว" (single file)** 2 รอบ — ทั้ง 2 รอบ progress bar ขึ้นถึง **100%** ในหน้าเว็บ (ใช้เวลา generate ~4-5 นาที/รอบ เพราะข้อมูล 1-15 ก.ย. ขนาดใหญ่)
  3. รอบแรกที่ 100% ไปคลิกปุ่ม X (ปิด dialog) โดยเข้าใจผิดว่าจะ trigger download — กลับกลายเป็นสถานะ **"Cancelled"** ในแผง export history แทน (บทเรียน: ปุ่ม X = ยกเลิก ไม่ใช่ปิด/ดาวน์โหลด)
  4. รอบสองปล่อยให้ค้างที่ 100% โดยไม่แตะอะไรเลย รอเพิ่ม 15+ วินาที — **ไฟล์ก็ยังไม่ลงใน Downloads folder เช่นกัน**
  5. ตรวจ `read_network_requests` ไม่พบ request ที่มี `.xlsx` เลยตลอดช่วงที่ export อยู่ที่ 100% — บ่งชี้ว่า download ไม่ได้ถูก trigger จริงในระดับ browser (ไม่ใช่แค่ปัญหา save location)
  → ไฟล์ Shipnity ล่าสุดในดิสก์ยังคงเป็น `Data_14-09-2026.xlsx` (17.3MB, 14 ก.ย.) เหมือนก่อนรอบนี้ทุกประการ
  → **STEP 3 (Top Products) ข้ามอีกครั้ง** เพื่อไม่ให้ dashboard มีข้อมูลไม่ครบ (เหมือนรอบแรก)

## Git

- ไม่มีการเปลี่ยนแปลงใดจากรอบนี้ที่ต้อง commit (Shipnity/Top Products ไม่สำเร็จ, Affiliate ถูก commit ไปแล้วโดย automation อื่น)
- พบว่ามีไฟล์ `WIBWUB_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js` (v1121) ถูก **stage ไว้แล้ว** (`git add`) จาก automation อื่น (TikTok followers, 29.482→29.5) แต่ยังไม่ commit — **ไม่ได้แตะต้อง** เพราะไม่ใช่ขอบเขตของ task นี้ และเสี่ยงชนกับ automation ที่เป็นเจ้าของการเปลี่ยนแปลงจริง ปล่อยให้ task นั้น commit เอง

## ที่ต้องทำ (ต้องมีคนที่เครื่อง Mac)

1. **ตรวจสอบ Chrome download settings บน Mac อย่างจริงจัง** — ปัญหา "export ขึ้น 100% แต่ไฟล์ไม่ลงดิสก์" เกิดซ้ำ **3 ครั้งติดต่อกัน** ในวันนี้ (รอบแรก 2 ครั้ง + รอบนี้ 2 ครั้ง = รวม 4 ครั้ง) ทั้งแบบ split-mode และ single-file mode
   - ตรวจว่ามี prompt "Save As" หรือ "Allow multiple downloads?" ค้างอยู่เบื้องหลังหรือไม่ (native dialog ที่ระบบอัตโนมัติมองไม่เห็นผ่านหน้าเว็บ)
   - ตรวจ Chrome Settings → Downloads → ตำแหน่งที่บันทึกไฟล์ และ "ถามก่อนดาวน์โหลดทุกไฟล์เสมอ" (ถ้าเปิดอยู่ ให้ปิด เพื่อให้ดาวน์โหลดอัตโนมัติ)
   - ตรวจว่า Chrome บล็อก pop-up/download จากโดเมน shipnity.com หรือไม่
2. เมื่อแก้ปัญหาแล้ว รัน schedule นี้ใหม่เพื่อดึง Shipnity ให้ครบ (1–15 ก.ย.) และอัปเดต Top Products
