# WIBWUB Weekly Auto-Update — พุธ 24 มิ.ย. 2569

## สรุป
รันอัตโนมัติ พบว่ารอบเช้า (08:00) อัปเดต Affiliate Dashboard ไปแล้วบางส่วน แต่ค่า
ใน WIBWUB_Mobile.html ยัง **ค้างเป็นค่าเก่า** (414,842) ไม่ตรงกับข้อมูลจริง → แก้ให้ถูกต้องแล้ว

## ข้อมูลที่ใช้
- Shipnity: `Data Shipnity/Data_มิถุนายน.xlsx` (24 มิ.ย. 01:37)
- Affiliate: `Transaction_Analysis_Creator_List_20260601-20260623.xlsx` (ย้ายเข้า Data Affiliate/ แล้ว)

## ตัวเลข Affiliate (1–23 มิ.ย.) — ตรวจซ้ำจากไฟล์ต้นทาง
- GMV: ฿436,626
- Net (หลังคืน): ฿429,316
- Commission: ฿54,274
- ครีเอเตอร์มียอดขาย: 308 · Active (≥฿1,000): 66

## การแก้ไข
- **WIBWUB_Mobile.html** → แก้ AFI_GMV/NET/COMM[7] = 436,626 / 429,316 / 54,274 (เดิมค้าง 414,842/406,742/51,177)
- **WIBWUB_Affiliate_Dashboard.html** → รอบเช้าอัปเดตไว้ถูกต้องแล้ว (badge 1–23 มิ.ย., 308 creators) คงไว้
- **sw.js** → v237 → **v238** (force cache refresh)

## ที่ตัดสินใจไม่แตะ
- **Top Products (Shipnity):** ข้อมูลล่าสุดต่างจากรอบ 23 มิ.ย. เพียง ~0.1–0.2% (เพิ่ม 1 วัน)
  แต่ ALL_PRODUCTS ใช้ "ชื่อที่จัดรูปแล้ว" ส่วน raw ในไฟล์เป็นรหัส (เช่น "Sugar (Sugar-500ml+Spray)")
  ไม่มี mapping table → ถ้าเขียนทับด้วยชื่อ raw จะทำให้ชื่อแย่ลงและกระทบ PROD arrays รายเดือน
  จึงคงค่าเดิม (refresh ล่าสุด 23 มิ.ย.) ไว้

## ค้างทำ (ต้องทำบนเครื่องจริง)
- **commit/push จาก sandbox ทำไม่ได้:**
  1) Google Drive mount ไม่อนุญาตให้ลบไฟล์ใน `.git` → ลบ `.git/index.lock` + `HEAD.lock` (ค้างจาก 23 มิ.ย.) ไม่ได้ → git commit ไม่ผ่าน
  2) git push ถูก proxy block (HTTP 403)
- **วิธีแก้:** ดับเบิลคลิก **`push_now.command`** บนเครื่อง Mac → จะ clear lock, add, commit, push ให้เอง
  (ไฟล์ที่แก้ทั้งหมดเซฟลงดิสก์/ซิงก์ Drive แล้ว พร้อม push)
