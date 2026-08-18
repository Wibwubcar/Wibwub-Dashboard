# WIBWUB Weekly Update (wibwub-monday-update) — 2026-08-07

รันแบบอัตโนมัติ ไม่มีผู้ใช้ควบคุมระหว่างรัน (scheduled task)

## ✅ สรุปผล

| งาน | สถานะ |
|---|---|
| ตรวจ M5 (label เดือน) ให้ตรงกับ array ยอดขาย | ✅ ตรวจแล้ว ถูกต้อง (8 ช่อง ม.ค.–ส.ค. ตรงกับ array อื่น) |
| Export Shipnity purchase history | ✅ ดาวน์โหลดสำเร็จ |
| Export TikTok Affiliate Creator List | ✅ ดาวน์โหลดสำเร็จ (6,087 ครีเอเตอร์) |
| คำนวณ Top 15 Products ใหม่จากไฟล์ Shipnity ทั้งหมด (dedup) | ✅ ประมวลผล 70 ไฟล์ครบ |
| อัปเดต `ALL_PRODUCTS` ใน WIBWUB_Mobile.html | ✅ อัปเดต 15 รายการ |
| อัปเดตตาราง/กราฟ Top Products ใน WIBWUB_Dashboard.html | ✅ อัปเดตยอดรวม+จำนวน (คงคอลัมน์แยกช่องทางไว้ตามธรรมเนียมเดิม) |
| อัปเดต Affiliate arrays (AF_*/AFI_*) — rolling window | ✅ overwrite index ล่าสุด (สค. 1-4 → 1-5) |
| Bump sw.js cache version | ✅ v592 → v593 |
| Git commit | ✅ commit `f38e036` |
| Git push | ⏳ sandbox push ไม่ได้ (403) — เตรียม `push_now.command` ให้ผู้ใช้กดเอง |

## 🐛 บั๊กที่พบและแก้ไขระหว่างทำงาน: ข้อมูลเดือนมกราคมหายจาก Top Products

ระหว่างรวมยอดขายจากไฟล์ Shipnity ทั้งหมด (70 ไฟล์) ด้วยสคริปต์ checkpoint/resume พบว่า `Data_มกราคม.xlsx` (~28,000 แถว) ถูกข้ามไปเงียบๆ เนื่องจากบั๊กในการ pickle/unpickle checkpoint (`defaultdict` ถูก unpickle กลับมาเป็น `dict` ธรรมดา ทำให้ชื่อสินค้าใหม่ที่ไม่เคยเจอมาก่อนโยน `KeyError` และไฟล์ทั้งไฟล์ถูกนับเป็น error)

**แก้โดย**: แก้สคริปต์ให้ rewrap เป็น `defaultdict` ทุกครั้งที่ resume จาก checkpoint แล้วรันคำนวณใหม่ทั้งหมดตั้งแต่ต้น (70 ไฟล์) เพื่อความชัวร์ — ยืนยันว่า `Data_มกราคม.xlsx` ถูกนับครบ 27,979 แถวในรอบใหม่ ผลลัพธ์สุดท้าย: ยอดขายรวม ฿57,594,371 / 223,846 ชิ้น / 196 SKU (เดิมก่อนแก้บั๊กจะขาดข้อมูล ม.ค. ไปทั้งเดือน)

## ค่าที่อัปเดต

**Top 15 Products** (v=ยอดขาย, q=จำนวน) — อันดับ 1-3: Wool Duster ฿5.65M/8,842 ชิ้น, Sugar 500ml ฿4.83M/16,141 ชิ้น, Interior 500ml ฿3.74M/10,820 ชิ้น (ครบ 15 รายการใน `ALL_PRODUCTS` และตาราง Dashboard)

**Affiliate (สค. 1-4 → 1-5)**: GMV 202,748 → 259,377 / NET 197,622 → 239,024 / Commission 23,115 → 30,138 / ครีเอเตอร์ที่มียอด 172 → 208 (คำนวณ NET = GMV − GMV คืนเงิน จากไฟล์ Creator List ที่ดาวน์โหลดใหม่)

## ⚠️ ปัญหาที่พบและยังไม่ได้แก้: WIBWUB_Affiliate_Dashboard.html มีการเปลี่ยนแปลงอื่นติดมาในคอมมิตเดียวกัน

ตอน `git add WIBWUB_Affiliate_Dashboard.html` ก่อน commit พบว่าไฟล์นี้มี diff ยาวผิดปกติ (4,576 บรรทัด แทนที่จะเป็นแค่ 5 array ที่ตั้งใจแก้) เมื่อตรวจสอบพบว่ามีการเปลี่ยนแปลงใน array `PRODUCTS` และ `VIDEOS` (เช่น ค่า `cr`/`vid` ของครีเอเตอร์บางคนลดลงมาก, ค่า `gmv` ในหลายวิดีโอมีทศนิยมเพิ่มขึ้น) ซึ่ง**ไม่ใช่การแก้ไขที่ทำในรอบนี้** — เป็นการเปลี่ยนแปลงที่ค้างอยู่ใน working tree (uncommitted) มาก่อนแล้ว จากกระบวนการอื่นที่ไม่เกี่ยวข้อง แล้วถูกเก็บติดไปพร้อมกันตอน commit นี้เพราะ `git add` ทั้งไฟล์

**การตัดสินใจ**: เลือกไม่ revert ส่วนนั้นออก เพราะเสี่ยงทำลายงานที่อีกกระบวนการหนึ่งทำค้างไว้โดยยังไม่ได้ commit (ไม่มีทางแยกได้ว่าอันไหนคือ "ของจริง" ที่ควรเก็บ) — ขอแจ้งให้ผู้ใช้ตรวจสอบ diff ของ `WIBWUB_Affiliate_Dashboard.html` เองก่อนกด `push_now.command` โดยเฉพาะส่วน `PRODUCTS`/`VIDEOS` arrays ว่าค่าที่เปลี่ยนนั้นถูกต้องตามที่ต้องการหรือไม่

ตรวจสอบ `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html` แล้ว — diff สะอาด ไม่มีการเปลี่ยนแปลงอื่นติดมา

## Git commit

Commit `f38e036c3251c08c41859c479f06ed8e8f0e7c17` — "auto-update: Monday 2026-08-07 — Shipnity Top Products + Affiliate GMV/Commission + cache bump" — แก้ 4 ไฟล์: `WIBWUB_Mobile.html`, `WIBWUB_Dashboard.html`, `WIBWUB_Affiliate_Dashboard.html`, `sw.js`

**ยังไม่ได้ push** — sandbox ไม่มีสิทธิ์ push โดยตรง (proxy บล็อก HTTP 403) กรุณาดับเบิลคลิก `push_now.command` ในโฟลเดอร์ All เพื่อ push ขึ้น origin/main (แนะนำให้ตรวจ diff ของ `WIBWUB_Affiliate_Dashboard.html` ตามหัวข้อด้านบนก่อน)

## ⚠️ รายการที่ควรตรวจสอบเพิ่มเติม (ไม่เร่งด่วน)

- ตรวจสอบ diff ของ `WIBWUB_Affiliate_Dashboard.html` ก่อน push (ดูหัวข้อด้านบน)
- ยอดขาย Shopee/TikTok-shop/Lazada เดือน ส.ค. (Google Sheets) ยังไม่ถูกดึงเข้า dashboard — นอกขอบเขตงานนี้
