# WIBWUB Weekly Update — วันจันทร์ 4 ส.ค. 2026

## สรุปผล
รันอัตโนมัติสำเร็จทุก step หลัก มี commit เรียบร้อย (`82ab83a`) — รอ user กด `push_now.command` เพื่อ push ขึ้น GitHub

---

## STEP 0 — Protection (M5)
ตรวจแล้ว WIBWUB_Dashboard.html และ WIBWUB_Mobile.html — `M5` array มีครบ 8 เดือนอยู่แล้ว (ไม่ต้องแก้)

## STEP 1 — Shipnity Export
โหลดข้อมูล purchase เดือนสิงหาคม (1-4 ส.ค.) ผ่าน Chrome สำเร็จ → บันทึกเป็น `Data Shipnity/Data_04-08-2026.xlsx` และ `Data_สิงหาคม.xlsx` (2,975 แถว)

## STEP 2 — Affiliate Transaction Analysis Export
โหลด Transaction Analysis creator list ผ่าน Chrome สำเร็จ — วันที่ 3-4 ส.ค. ยัง greyed out ในปฏิทิน TikTok (ข้อมูลยังไม่ finalize) จึงใช้ช่วง 1-2 ส.ค. ตามกฎ fallback ใน SKILL.md → บันทึก `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260801-20260802.xlsx` (1,794 creator rows)

## STEP 3 — Top Products (ภาพรวมธุรกิจ)
คำนวณ Top 15 จากไฟล์ Shipnity 8 ไฟล์ month-alias (ม.ค.-ส.ค.) — **ขาด `Data_มีนา.xlsx`** (ไม่มีไฟล์นี้ในโฟลเดอร์รอบนี้ ต่างจากรายงานสัปดาห์ก่อนที่มีครบ 8 ไฟล์) ได้ 7/8 ไฟล์ รวม 162,949 order-lines, 192 สินค้า

อันดับ 1: Wool duster-ไม้ปัดขนแกะ (rev 4,601,402 / qty 7,230)
อันดับ 2: Sugar (Sugar-500ml+Spray) (rev 4,087,360 / qty 13,722)

**🚫 ข้าม:** ไม่เขียนทับ `ALL_PRODUCTS` (WIBWUB_Mobile.html) และ Top Products chart (WIBWUB_Dashboard.html) — ตามแนวทางเดียวกับรายงาน 1 ส.ค. และ 3 ส.ค. เพราะ `ALL_PRODUCTS` มีฟิลด์ `mk`/`mkq` (ยอดขายจาก marketplace อื่น) ที่ข้อมูล Shipnity อย่างเดียวไม่มี การเขียนทับจะทำให้ข้อมูล marketplace หายไป บันทึกผลลัพธ์ไว้อ้างอิงที่ `top15_products_2026-08-04.json` แทน

## STEP 4 — Affiliate Arrays
ไฟล์จริงเป็น format 22 คอลัมน์ (ไม่ใช่ 12 คอลัมน์ตามที่ SKILL.md สมมติไว้) — map คอลัมน์จาก header จริง: col1=GMV จากครีเอเตอร์, col4=การคืนเงิน, col21=ค่าคอมมิชชั่นโดยประมาณ

Label เดือนปัจจุบัน "ส.ค. (1-2)" มีอยู่แล้วเป็น index สุดท้ายของทั้ง `AF_MO`/`AFI_MONTHS` → **แก้ค่าที่ index เดิม** (ไม่ append ไม่แตะเดือนก่อนหน้า) ตามกฎ rolling-window:

| | เดิม | ใหม่ |
|---|---|---|
| GMV | 82,634 | 82,646 |
| NET | 75,867 | 82,106 |
| Commission | 10,008 | 10,040 |
| Creators | 76 | 76 |

หมายเหตุ: NET เปลี่ยนมากกว่ารายการอื่น เพราะคำนวณใหม่จากสูตร GMV − การคืนเงิน (การคืนเงินรอบนี้ต่ำมาก ~540 บาท) ให้ค่าที่สอดคล้องกับข้อมูลจริงมากกว่าค่าเดิม — ตัวเลข creator count (76) ตรงกับค่าเดิมเป๊ะ ยืนยันว่าสูตรถูกต้อง

อัปเดตไฟล์: `WIBWUB_Affiliate_Dashboard.html`, `WIBWUB_Mobile.html`

## STEP 5 — sw.js + Git Commit
- Bump cache version: `wibwub-v555` → `wibwub-v556`
- เจอปัญหา `.git/index.lock`/`HEAD.lock` ค้าง (ปัญหาเรื้อรังของ Google-Drive-mounted repo) — แก้โดย rename lock file ในโฟลเดอร์เดียวกันผ่าน Python (`os.rename`) แทนการลบ เพราะ `rm`/`mv`/`os.remove` ทั้งหมดล้มเหลวด้วย "Operation not permitted" บน mount นี้
- Commit สำเร็จ: `82ab83a` — "auto-update: Monday 2026-08-04 — Shipnity + Affiliate + ภาพรวมธุรกิจ"
- ไฟล์ที่เปลี่ยน: `WIBWUB_Mobile.html`, `WIBWUB_Dashboard.html`, `WIBWUB_Affiliate_Dashboard.html`, `sw.js` (9 insertions, 9 deletions)
- `push_now.command` มีอยู่แล้วและถูกต้อง — **รอ user ดับเบิลคลิกเพื่อ push**

---

## ⚠️ สิ่งที่ต้องตรวจสอบ/ทำต่อ
1. **กดรัน `push_now.command`** เพื่อ push commit ขึ้น GitHub (sandbox push เองไม่ได้ ติด proxy)
2. **ไฟล์ `Data_มีนา.xlsx` หาย** จาก `Data Shipnity/` — ถ้ามีไฟล์ backup ควรใส่กลับเข้าโฟลเดอร์ เพื่อให้ Top 15 products ครบทุกเดือนในรอบถัดไป
3. Top Products (ภาพรวมธุรกิจ) ยังไม่อัปเดตต่อเนื่องเป็นสัปดาห์ที่ 3 แล้ว — ถ้าต้องการให้อัปเดตจริง ต้องมีข้อมูล marketplace (mk/mkq) แยกมาผสานด้วย ไม่ใช่แค่ Shipnity อย่างเดียว
