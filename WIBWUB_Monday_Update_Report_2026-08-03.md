✅ WIBWUB Monday Update — 3/8/2026 (09:32 run)

📅 ช่วงข้อมูล: 1/8 เท่านั้น (Affiliate, Transaction Analysis) — TikTok disable วันที่ 2-3 ส.ค. ในตัวเลือกช่วงวันที่กำหนดเอง เพราะข้อมูลยังไม่ finalize (เหมือนสัปดาห์ก่อนที่ 31/7-1/8 ก็ถูก disable เช่นกัน)

📁 ไฟล์ที่ดาวน์โหลด/ย้ายแล้ว:
  Data Shipnity/Data_03-08-2026.xlsx (1,633 rows, product-level) + alias Data_สิงหาคม.xlsx
  Data Affiliate/Transaction_Analysis_Creator_List_20260801-20260801.xlsx (110KB, 1,253 creators) — ย้ายจาก Data Affiliate/ครีเอเตอร์/ มาไว้ที่ root ด้วย

📊 Affiliate (AF_MO/AFI_MONTHS index สุดท้าย = "ส.ค. (1-1)" / "สค.69 (1)"):
  GMV: ฿35,041
  NET (GMV − การคืนเงิน): ฿34,679
  Commission: ฿4,219
  Creators (GMV>0): 45

  หมายเหตุ: ตอนเริ่ม task พบว่า WIBWUB_Affiliate_Dashboard.html และ WIBWUB_Mobile.html มีตัวเลขชุดนี้ **อยู่แล้ว** (ตรงกับที่ผมคำนวณเองจากไฟล์ export 100%) — คาดว่ามาจาก automation run อื่นที่ทำงานคู่ขนานกันในเช้าวันนี้ (เห็น commit auto-update หลายตัวใน git log ช่วงเวลาใกล้กัน) ผมจึงแค่ verify ตัวเลขให้ตรง ไม่ได้เขียนทับซ้ำ — WIBWUB_Mobile.html ถูก commit ไปแล้วก่อนหน้า (ไม่มีการเปลี่ยนแปลงค้างใน git status ตอนที่ผมเช็ค) ส่วน WIBWUB_Affiliate_Dashboard.html ยังค้างเป็น uncommitted change ผมจึง commit ให้พร้อมกับ sw.js

⚙️ sw.js: v544 → v545 (พบว่าถูกบัมป์ไว้แล้วเป็น uncommitted change ก่อนที่ผมจะเริ่ม step นี้ — ไม่ได้บัมป์ซ้ำ แค่ commit ให้)

📌 Commit แล้ว (`f0062a1`) — ดับเบิ้ลคลิก push_now.command เพื่อ push ขึ้น GitHub (ปรับสคริปต์ให้รวม WIBWUB_Dashboard.html ในลิสต์ add ด้วยแล้ว เผื่อรอบหน้ามีการแก้ Top Products)

🚫 ข้าม: Top Products (ภาพรวมธุรกิจ ALL_PRODUCTS/PROD_MO) — เหตุผลเดียวกับรอบ 1/8

---

⚠️ หมายเหตุสำคัญ:

**1) TikTok Affiliate date-range picker — แก้ปัญหาคลิกไม่ติด**
ปฏิทินแบบกำหนดเองใน "รายละเอียด → ครีเอเตอร์" คลิกวันที่ผ่าน screenshot coordinate ไม่ติดหลายรอบ (คลิกวันที่ 03 ส.ค. ไม่มีผลใดๆ) หลัง debug ด้วย JavaScript พบสาเหตุจริง: วันที่ 2-3 ส.ค. มี class `core-picker-cell-disabled` ในปฏิทิน (TikTok ปิดไม่ให้เลือกเพราะข้อมูลยังไม่ finalize) จึงไม่ใช่ปัญหา coordinate แต่เป็นเพราะวันนั้นเลือกไม่ได้จริงๆ แก้โดยดึงช่วง 1-1 ส.ค. (วันเดียวที่เปิดให้เลือกได้) แทน — ใช้วิธี dispatch MouseEvent ผ่าน JS โดยตรงบน element ที่ถูกต้อง (กรองด้วย bounding-rect ให้อยู่ในพื้นที่ปฏิทินที่มองเห็นจริง เพราะ DOM มี calendar panel ซ้อนซ่อนอยู่หลายชุดสำหรับ animation)

**2) Top Products (ALL_PRODUCTS/PROD_MO) — จงใจไม่เขียนทับ (เหมือนรอบ 1/8)**
คำนวณ Top 15 จาก Shipnity แล้ว (cumulative ม.ค.–3 ส.ค. รวม 184,479 order-line จาก 8 ไฟล์ month-alias) อันดับ 1 คือ Wool duster (฿5,579,523) ใกล้เคียงค่าปัจจุบันในไฟล์ (฿5,569,034) แต่ไม่ตรงเป๊ะ เหตุผลเดิม: `ALL_PRODUCTS` มี field `mk`/`mkq` (ยอดขาย marketplace) ที่ Shipnity ไม่มี ถ้าเขียนทับจะทำข้อมูล marketplace หายไปเงียบๆ บันทึกผลไว้ที่ `top15_products_2026-08-03.json` แทน

**3) Git lock files**
เจอ `.git/index.lock`, `.git/HEAD.lock`, `.git/objects/maintenance.lock`, `.git/objects/*/tmp_obj_*` ค้างซ้ำๆ เหมือนทุกสัปดาห์ (Google Drive mount ไม่ยอมให้ unlink) ใช้ `mv` แทน `rm` เพื่อเลี่ยงปัญหา — commit ผ่านสำเร็จ ไม่กระทบข้อมูล

**4) M5 label — ตรวจแล้วไม่ต้องแก้**
WIBWUB_Dashboard.html และ WIBWUB_Mobile.html มี M5 ครบถึง "ส.ค." อยู่แล้ว (แก้ไปตั้งแต่ 2 ส.ค.)

📌 สรุปว่า commit นี้ push แค่: WIBWUB_Affiliate_Dashboard.html + sw.js + top15_products_2026-08-03.json (reference only) — WIBWUB_Dashboard.html ไม่มีการเปลี่ยนแปลง, WIBWUB_Mobile.html ถูก commit ไปก่อนหน้าโดย process อื่นแล้ว
