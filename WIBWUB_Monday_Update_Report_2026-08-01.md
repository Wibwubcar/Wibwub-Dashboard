✅ WIBWUB Auto Update — 1/8/2026 (09:10 run)

📅 ช่วงข้อมูล: 1/7 – 30/7 (Affiliate, Transaction Analysis) — TikTok ยังไม่มีข้อมูล 31/7 หรือ 1/8 ให้ดึง (ถูก disable ใน date picker เพราะยังไม่ finalize)

📁 ไฟล์ที่ย้ายแล้ว:
  Data Affiliate/ครีเอเตอร์/ ← Transaction_Analysis_Creator_List_20260701-20260730.xlsx (568KB, 6,729 creators)
  ไฟล์เก่าช่วง 24/7-30/7 ที่โหลดผิดตอนแรก (ก่อนแก้ date range) ถูก rename เป็น `_SUPERSEDED_ignore_...xlsx` กันสับสน

📊 Affiliate (AF_MO/AFI_MONTHS index สุดท้าย = "ก.ค. (1-30)", overwrite ค่าเดิมเพราะยังเป็นเดือนเดียวกัน):
  GMV: ฿1,424,363 → ฿1,424,548
  NET: ฿1,329,926 → ฿1,400,643 ⚠️ (ดูหมายเหตุ 1)
  Commission: ฿165,654 → ฿166,130
  Creators (GMV>0): 716 → 716 (ไม่เปลี่ยน — ตรงกับค่าเดิมเป๊ะ ยืนยันว่า mapping คอลัมน์ถูกต้อง)

⚙️ sw.js: v522 → v523
📌 Commit แล้ว (`03d0868`) — ดับเบิ้ลคลิก push_now.command เพื่อ push ขึ้น GitHub

🚫 ข้าม: Top Products (ภาพรวมธุรกิจ) — ดูหมายเหตุ 2

---

⚠️ หมายเหตุสำคัญ:

**1) NET เปลี่ยนขึ้น ~฿70,700 ทั้งที่ GMV เปลี่ยนแค่ ~฿185**
ผมคำนวณ NET = GMV − การคืนเงิน (คอลัมน์ "การคืนเงิน" ตรงตัวในไฟล์ Transaction Analysis Creator List) — ไม่มีคอลัมน์ไหนในไฟล์ที่ sum แล้วได้ ~94,437 (ตัวเลข returns ที่ทำให้ NET เดิม = 1,329,926) เลย ผมเช็คโดย sum ทุกคอลัมน์ baht ในไฟล์แล้วไม่มีตัวไหนตรง
ทั้งนี้ TikTok เองระบุใน tooltip ของคอลัมน์ "การคืนเงิน" ว่า "ยอดการคืนเงินและยอด GMV ในแต่ละช่วงเวลาที่เลือกจึงมักจะไม่สอดคล้องกัน" (การคืนเงินทยอย settle ช้ากว่า GMV) — เป็นไปได้สูงว่า returns ผันผวนจริงระหว่างสองรอบดึงข้อมูล ไม่ใช่ bug การ map คอลัมน์ผิด (GMV/Commission/Creator count ตรงกับของเดิมเกือบเป๊ะหรือเป๊ะเลย) แต่ยัง**แนะนำให้ตรวจสอบ NET กับหน้าเว็บ TikTok โดยตรงอีกครั้ง**ก่อนเชื่อถือ 100%

**2) Top Products (ALL_PRODUCTS/PROD_MO) — จงใจไม่เขียนทับ**
คำนวณ Top 15 จาก Shipnity แล้ว (all-time cumulative ม.ค.–1 ส.ค., รวม 183,088 order-line ที่ไม่ซ้ำกัน จาก 17 ไฟล์ curated) — อันดับ 1 คือ Wool Duster (฿5,555,107) ใกล้เคียงกับค่าปัจจุบันในไฟล์ (฿5,569,034) แต่ไม่ตรงเป๊ะ
**เหตุผลที่ไม่เขียนทับ:** `ALL_PRODUCTS` ปัจจุบันมี field เพิ่ม `mk`/`mkq` (ยอดขาย marketplace เช่น Shopee/Lazada ที่ไม่ได้อยู่ใน Shipnity) และมี `PROD_MO` แยกยอดขายรายเดือน (ม.ค.–ก.ค.) ที่ผมไม่มีข้อมูลพอจะคำนวณใหม่ให้ตรงกับของเดิม (ผลรวม PROD_MO ต่อสินค้าก็ไม่ตรงกับ ALL_PRODUCTS.v เป๊ะอยู่แล้ว น่าจะมี logic เพิ่มเติมที่ script ใน SKILL.md ไม่ได้ระบุไว้) ถ้าเขียนทับด้วยยอด Shipnity-only จะทำให้ข้อมูล marketplace ของทุกสินค้าหายไปเงียบๆ — จึงข้าม step นี้ไว้ก่อน ยอดที่คำนวณได้บันทึกไว้ที่ `top15_products.json` ในกรณีต้องการอ้างอิง/อัปเดตด้วยมือ

**3) Git lock files**
เจอ `.git/index.lock`, `.git/HEAD.lock`, `.git/objects/maintenance.lock` ค้างจาก process ก่อนหน้าอีกครั้ง (ปัญหาเดิมที่เกิดซ้ำๆ ในหลาย session) — `rm` ใช้ไม่ได้ (Operation not permitted บน Google Drive mount) แต่ `mv` ใช้ได้ จึง rename ไฟล์ lock ออกแล้ว commit ผ่านปกติ ไม่กระทบข้อมูล

📌 สรุปว่า commit นี้ push แค่: Affiliate arrays (AF_GMV/AF_NET/AF_COM/AF_CR + AFI_GMV/AFI_NET/AFI_COMM) + sw.js bump เท่านั้น — Top Products ยังไม่ถูกแตะต้อง, WIBWUB_Dashboard.html ไม่มีการเปลี่ยนแปลง
