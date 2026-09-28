# WIBWUB Weekly Update — วันจันทร์ 7 ก.ย. 2569

รันอัตโนมัติโดย scheduled task `wibwub-monday-update` · ไม่มีคนดูแลระหว่างรัน

**สรุป:** STEP 1 และ STEP 3 สำเร็จ (ข้อมูล Shipnity ถึงวันที่ 6 ก.ย. เข้าแดชบอร์ดแล้ว) · STEP 2 และ STEP 4 ถูกบล็อกเพราะ TikTok Affiliate session หมดอายุ · STEP 5 ทำได้ครึ่งเดียว — stage ไฟล์แล้วแต่ commit ไม่ผ่านเพราะมี stale `.git/index.lock` ที่ sandbox ลบไม่ได้ จึงย้ายคำสั่ง commit ไปไว้ใน `push_now.command` ให้เครื่อง Mac รันแทน

---

## STEP 0 — CRITICAL PROTECTION (M5)

ตรวจแล้ว **ไม่ต้องแก้อะไร** ทั้งสองไฟล์: `len(M5) == len(SH_REV) == 8` ทั้งใน `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html`

สำคัญ: สคริปต์ป้องกัน M5 ตามที่ runbook เขียนไว้ **จะทำแดชบอร์ดพังถ้ารันจริง** เพราะมันใช้ `required_months = today.month` (= 9) ซึ่งจะยืด `M5` เป็น 9 ช่อง ขณะที่ array ข้อมูลคู่ขนานอีก ~25 ตัว (`SH_REV`, `TK_REV`, `LZ_REV`, …) ยังยาว 8 ช่อง เงื่อนไขที่ถูกต้องคือ `required_months = len(SH_REV)` — ประเด็นนี้ค้างมา **5 รอบแล้ว** และยังไม่ได้แก้ใน runbook

`M5`, `MTD_COVERAGE`, `SH_REV`, `TK_REV` ยืนยันว่า byte-identical กับก่อนรัน

## STEP 1 — Shipnity export ✅

ดึงผ่าน Claude-in-Chrome สำเร็จ → `Data Shipnity/Data_07-09-2026.xlsx` (6,482,847 bytes, 7,105 แถว)

จำนวนแถวรายวัน: 01/09 = 1,204 · 02/09 = 1,144 · 03/09 = 1,139 · 04/09 = 1,105 · 05/09 = 1,114 · 06/09 = 1,204 · 07/09 = 194 (ไม่ครบวัน)

**หมายเหตุการทำงาน:** date picker ของ Shipnity กดด้วยพิกัดไม่ได้ (element โปร่งใส คลิกทะลุไปโดนตาราง) ต้องใช้ `find` เพื่อเอา element ref แล้วยืนยันด้วย JS ว่า `input-78 == "1 ก.ย. 2569 ~ 30 ก.ย. 2569"` และปุ่มส่งออก `disabled:false` ก่อนกด

## STEP 2 — TikTok Affiliate export ❌ BLOCKED

`affiliate.tiktok.com/data/creator-analysis`, `/insights/transaction-analysis` และ `/connection/creator` ทั้งหมด redirect ไปหน้า `seller.tiktok.com` เวอร์ชัน US ที่ยังไม่ล็อกอิน ส่วน `seller.tiktok.com/homepage?shop_region=TH` คืน 404

**Session expired — re-login required.** หยุดตาม error handling ที่ runbook กำหนด การ re-login ต้องกรอกรหัสผ่าน ซึ่งเป็นสิ่งที่ทำแทนไม่ได้ — ต้องให้คนล็อกอินเองแล้วสั่งรันใหม่

## STEP 3 — Top Products ✅

### วิธีที่เลือก: ใส่ delta เฉพาะวันที่ 6 ก.ย. (ไม่ rebuild ใหม่ทั้งก้อน)

รอบก่อนครอบคลุมถึง 5 ก.ย. ไฟล์ใหม่เพิ่มวันที่ 6 มาเต็มวัน (วันที่ 7 ไม่ครบวัน จึงตัดออกตามธรรมเนียมเดิมที่นับเฉพาะวันที่จบแล้ว) จึงคำนวณเฉพาะยอดวันที่ 6 ด้วย dedupe key `(เลขที่ออเดอร์, รหัสสินค้า, จำนวน)` แล้วบวกเข้าไป

**เหตุผลที่ไม่ rebuild:** ได้ลอง rebuild เต็ม ม.ค.–ก.ย. จากไฟล์ Shipnity ทุกไฟล์แล้ว อันดับสินค้าตรงกันเป๊ะ แต่ตัวเลขสะสมทุกตัวต่ำกว่าที่แดชบอร์ดแสดงอยู่ราว 1–2% (เช่น Wool Duster rebuild 5,987,714 vs. ของจริง 6,037,049) เป็น offset เชิงระบบที่อธิบายไม่ได้ น่าจะมาจากออเดอร์ที่ถูกยกเลิกแล้วหายไปจากไฟล์ export รุ่นหลัง — พบหลักฐานว่าข้อมูล Shipnity **เปลี่ยนย้อนหลังได้จริง** (ไฟล์วันที่ 6 ให้ยอด `<=04` = 48,684 ซึ่งน้อยกว่าไฟล์วันที่ 5 ที่ให้ 49,864) การเขียนทับด้วย rebuild จะเท่ากับแก้ตัวเลข 8 เดือนย้อนหลังแบบเงียบ ๆ และผิดกฎเหล็ก *"ห้ามสร้าง array ใหม่ทั้งหมด"*

### ยอดวันที่ 6 ก.ย. ที่บวกเข้าไป

1,201 แถว (หลัง dedupe) · **฿332,943** · **1,526 ชิ้น**

แยกช่องทาง: Shopee 161,260 · TikTok 142,543 · Facebook 19,714 · Line Shopping 5,454 · Lazada 3,972

### ไฟล์ที่แก้

**`WIBWUB_Mobile.html`** (backup: `WIBWUB_Mobile.html.bak_20260907`)

- `ALL_PRODUCTS` — บวก `v` และ `q` ให้ครบทั้ง 15 รายการ
- `PROD_MO` — บวกเฉพาะ `mo[8]` (ก.ย.) ของทั้ง 15 รายการ ดัชนี 0–7 (ม.ค.–ส.ค.) ไม่แตะเลย
- `PROD_MO_LBL` — `'ก.ย. (1-5)'` → `'ก.ย. (1-6)'`

**`WIBWUB_Dashboard.html`** (backup: `WIBWUB_Dashboard.html.bak_20260907`)

- กราฟ `pr_top10` — บวก delta รายช่องทางเข้า Shopee / TikTok / Facebook / Line Shopping
- โดนัท `pr_channel` — บวกยอดรวมเฉพาะ Top 15: Shopee +86,881 · TikTok +108,499 · Facebook +16,553 · Line Shopping +2,694
- ตาราง 13 คอลัมน์ — คอลัมน์ รวม/จำนวน อัปเดตครบ 15 แถว, คอลัมน์รายช่องทางของแถว 1–10 สร้างใหม่จากค่าใน `pr_top10`, แถวรวมท้ายตาราง `฿65.57M / 260,410` → `฿65.90M / 261,936`
- KPI — `฿66.91M` → `฿67.24M` · `260K ชิ้น` → `262K ชิ้น` · `฿6.04M · 9,479 ชิ้น` → `฿6.05M · 9,497 ชิ้น`
- ป้ายวันที่ `5 ก.ย.` → `6 ก.ย.` ทั้ง 9 จุด (เว้นกราฟ follower รายวัน `1–5 ก.ย.` ซึ่งเป็นคนละชุดข้อมูล)

## STEP 4 — Affiliate arrays ❌ BLOCKED

ไม่แตะ `WIBWUB_Affiliate_Dashboard.html` และ `AFI_*` ใน `WIBWUB_Mobile.html` เลย เพราะไม่มีข้อมูลใหม่จาก STEP 2 — ยืนยันด้วย byte-comparison ว่า `AF_MO`/`AF_GMV`/`AF_NET`/`AF_COM`/`AF_CR` (len 9) และ `AFI_MONTHS`/`AFI_GMV`/`AFI_NET`/`AFI_COMM` (len 11) เหมือนเดิมทุกไบต์

ค่าล่าสุดยังคงเป็น **ก.ย. (1-3)** — เก่ากว่าฝั่ง Shipnity อยู่ 3 วัน

## STEP 5 — sw.js + commit ⚠️ ทำได้บางส่วน

- `sw.js` — บัมพ์เป็น `wibwub-v1005` แล้วมี automation ตัวอื่นบัมพ์ต่อเป็น `wibwub-v1006` ระหว่างที่รันอยู่ ผลลัพธ์ยังถูกต้อง (สูงกว่า v1004 → cache invalidate ได้)
- `git add WIBWUB_Dashboard.html sw.js` — **สำเร็จ** (stage ไว้แล้ว)
- `git commit` — **ไม่สำเร็จ** มี `.git/index.lock` ค้างตั้งแต่ 01:35 และ sandbox ลบไม่ได้ (`Operation not permitted`) ลอง retry 4 รอบก็ยังไม่หาย
- `push_now.command` — เขียนใหม่แล้ว ใส่ทั้ง `rm -f .git/index.lock`, `git add`, `git commit` และ `git push` ครบ

**ต้องทำต่อ:** ดับเบิลคลิก `push_now.command` บนเครื่อง Mac เพื่อ commit + push

## STEP 6 — Verification ✅ ผ่านทั้งหมด

- `len(M5) == len(SH_REV) == 8` ทั้งสองไฟล์ · `M5` และ `MTD_COVERAGE` byte-identical
- `PROD_MO_LBL` = 9 ช่อง เท่ากับทุก `PROD_MO.mo`
- `PROD_MO` ดัชนี 0–7 (ม.ค.–ส.ค.) ไม่มีตัวไหนเปลี่ยน · ดัชนี 8 มีแต่เพิ่มขึ้น
- `pr_top10` = 9 dataset × 10 ค่า · ยอดรวมต่อสินค้าตรงกับ `ALL_PRODUCTS.v`
- `pr_channel` = 9 ค่า รวม 40,218,337 = 40,003,710 + 214,627 ✓
- `AF_*` len 9 และ `AFI_*` len 11 ไม่เปลี่ยน
- ตารางยังมี 15 แถวสินค้า · เหลือ `5 ก.ย.` แค่ 2 จุดตามที่ตั้งใจ

---

## ปัญหาที่ต้องแก้ (สะสมข้ามรอบ)

1. **สคริปต์ป้องกัน M5 ใน runbook ยังผิดอยู่** — ค้างมา 5 รอบ `required_months` ต้องมาจาก `len(SH_REV)` ไม่ใช่ `today.month` ถ้ามีใครรันตามตัวอักษรจริง ๆ กราฟจะพังทันที
2. **path ใน runbook ล้าสมัย** — เขียนว่า `/sessions/hopeful-serene-fermi/mnt/` แต่ของจริงคือ `/sessions/youthful-compassionate-faraday/mnt/` (เคยรายงานไปแล้วใน `Monday_Update_Report_20260903_pm.md` ข้อ 5) ควรให้ runbook ค้นหา mount เองแทนที่จะ hardcode
3. **`Data_30-06-2026.xlsx` ตั้งชื่อผิด** — ข้างในเป็นข้อมูล ก.พ./มี.ค. ไม่ใช่ มิ.ย. ต้องใช้ `Data_มิถุนายน.xlsx` แทนถึงจะได้เดือน 6 ครบ 30 วัน
4. **ตัวเลขในตาราง Top Products เคยเพี้ยนจากกราฟ** — ก่อนรอบนี้ คอลัมน์ Shopee ของ Wool Duster แสดง `฿3.86M` ขณะที่กราฟเก็บ 3,877,223 (`฿3.88M`) เพี้ยนแบบนี้ทั้งตารางประมาณ 0.4–1% รอบนี้สร้างคอลัมน์รายช่องทางของแถว 1–10 ใหม่จากกราฟแล้ว แต่แถว 11–15 ยังไม่มีแหล่งตัวเลขดิบให้เทียบ จึงยังค้างอยู่
5. **ตัวเลขรวมสามชุดไม่ตรงกัน** — KPI `฿66.91M`, แถวรวมในตาราง `฿65.57M` และ rebuild `฿66.72M` ต่างกันหมด ทั้งสามเดินหน้าด้วย delta เดียวกันในรอบนี้ แต่ควรหาว่าอันไหนคือตัวจริงแล้วปรับให้ตรงกัน
6. **มี automation อื่นรันทับกัน** — ระหว่างรอบนี้มี auto-push commit `1b6ab81` กวาด `WIBWUB_Mobile.html` ที่แก้ไว้ไปด้วย และมีตัวที่บัมพ์ `sw.js` เป็น v1006 ผลลัพธ์ไม่เสียหาย แต่ทำให้ commit ของงานนี้ไม่ครบก้อน และน่าจะเป็นต้นเหตุของ `index.lock` ที่ค้าง ควรใส่ mutex กันชนกัน
7. **`ALL_PRODUCTS.v` กับ `sum(PROD_MO.mo)` ต่างกัน ±1 ใน 8 รายการ** — เป็นเศษปัดที่มีมาก่อนหน้านี้แล้ว ยืนยันว่ารอบนี้ไม่ได้ทำให้แย่ลง แต่ควรเคลียร์
