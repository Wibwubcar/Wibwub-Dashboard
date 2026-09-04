# WIBWUB Monday Update — 1 ก.ย. 2569

**สถานะ: สำเร็จบางส่วน** — Shipnity/Top Products อัปเดตครบ · Affiliate ติด blocker ที่ต้องให้คนตัดสินใจ

Commit: `b1faca7` · sw.js `wibwub-v922` → `wibwub-v923`

---

## สรุปสิ่งที่ทำ

### STEP 0 — M5 guard: **ข้าม โดยตั้งใจ**

สคริปต์ตามตัวอักษรจะเติม `"ก.ย."` เข้า `M5` (ตอนนี้ยาว 8 = ม.ค.–ส.ค.) เพราะวันนี้เดือน 9
แต่ array ข้อมูลทุกตัวที่คู่กับ M5 ยังยาว 8 ทั้งหมด:

```
SH_REV/TK_REV/LZ_REV/SH_ORD/TK_ORD/LZ_ORD  = length 8
MTD_COVERAGE = { Shopee:'2026-08-30', TikTok:'2026-08-30', Lazada:'2026-08-30' }
```

ถ้าเติม `ก.ย.` ตอนนี้ จะได้ label ที่ขัดแย้งตัวเอง —
*"ม.ค. – ก.ย. 2569 (ข้อมูลจริง) · ก.ย. = MTD ถึง 30 ส.ค."* — บวกกับคอลัมน์กันยายนว่างเปล่าทุกกราฟ

**จึงไม่เติม** จะเติม `ก.ย.` พร้อมกับตอนที่มีข้อมูล Shopee/TikTok/Lazada ของกันยายนจริง (รอบหน้า 7 ก.ย.)

### STEP 1 — Shipnity export: **สำเร็จ**

**เบี่ยงจาก runbook โดยตั้งใจ:** ดึงช่วง **1–31 ส.ค. 2569** แทน 1–1 ก.ย.

เหตุผล: `Data_31-08-2026.xlsx` ถูกโหลดตอน 31 ส.ค. 14:13 → ตกออเดอร์เย็นวันนั้นทั้งหมด
กันยายนมีข้อมูลแค่ ~1 วัน ซึ่งรอบหน้า (7 ก.ย. ครอบคลุม 1–7 ก.ย.) จะเก็บให้อยู่แล้ว

ผลการ re-export → `Data Shipnity/Data_01-09-2026.xlsx`:

| | เดิม (Data_31-08) | ใหม่ (Data_01-09) | ส่วนต่าง |
|---|---|---|---|
| แถว (dedup) | 34,684 | 34,876 | **+192** |
| ยอดขาย | ฿9,486,546 | ฿9,534,047 | **+฿47,501** |
| จำนวนชิ้น | 43,474 | 43,723 | +249 |

*วิธี dedup: key = (เลขที่ออเดอร์, รหัสสินค้า, จำนวน) · revenue = ราคา × จำนวน — ตรวจสอบแล้วว่า reproduce ตัวเลข ฿9,486,546 ของรายงาน 31 ส.ค. ได้ตรงทุกหลัก*

### STEP 2 + STEP 4 — Affiliate: **BLOCKER — ต้องให้คนตัดสินใจ**

**หน้า TikTok Transaction Analysis ถูกถอดออกจากระบบแล้ว**

- `/insights/transaction-analysis` → redirect ไปหน้า "Performance"
- `/data/transaction-analysis` → redirect เหมือนกัน
- ไม่มีลิงก์ใน sidebar แล้ว (ตรวจด้วย find)
- หน้า Creator Analysis ขึ้น banner แจ้ง deprecation

runbook เตือนไว้ชัดว่า **ห้ามใช้ Creator List ปกติแทน** ("Transaction Analysis = ออเดอร์ที่ settle แล้ว → ตรงกับตัวเลขในหน้า TikTok Affiliate Center") การเอาตัวเลขจาก Creator List มาใส่จะทำให้ `AF_GMV` เพี้ยน จึง**ไม่แตะ array affiliate เลย**

สถานะปัจจุบันยังถูกต้องอยู่ — label ท้ายสุดคือ `ส.ค. (1-29)` ซึ่งตรงกับข้อมูลชุดล่าสุดที่มี:

```js
AF_MO  = [..., "ก.ค. (1-31)", "ส.ค. (1-29)"]   // WIBWUB_Affiliate_Dashboard.html
AFI_MONTHS = [..., 'กค.69 (1-31)', 'สค.69 (1-29)']  // WIBWUB_Mobile.html
```

**ต้องตัดสินใจ:** หา export ทดแทนใน TikTok Seller Center รุ่นใหม่ (หน้า Performance / Affiliate Center) แล้วอัปเดต STEP 2 ของ runbook — งานนี้ทำอัตโนมัติต่อไม่ได้จนกว่าจะรู้ว่า export ไหนคือ settled orders

### STEP 3 — Top Products: **สำเร็จ**

ยืนยันการจับกลุ่ม SKU ก่อนแก้: 15 ชื่อสินค้าใน `ALL_PRODUCTS` map **1:1** กับ 15 SKU
ขนาด 3L/5L นับแยกกลุ่มจริงตามคอมเมนต์ในไฟล์ — `SRFX030003` (Reflex 3L), `SSUG050024` (Sugar 5L), `SRFX110003` (Reflex 500ml) **ไม่ได้** รวมเข้ากลุ่มไหน

ตรวจด้วย invariant: `sum(PROD_MO['Reflex'].mo) = 1,711,458 = ALL_PRODUCTS['Reflex'].v` และ Aug = 189,874 ≈ `SRFX000003` เดี่ยว (ไม่ใช่ 000003+110003 = ~408K)

**ใช้วิธีบวก delta ไม่ใช่ทับค่า** เพราะยอด single-SKU เดือน ส.ค. ไม่ตรงกับ `PROD_MO[7]` เป๊ะ และเพี้ยนคนละทาง (Wool Duster ไฟล์สูงกว่า 592 · Sugar ไฟล์ต่ำกว่า 16,201) แปลว่า `PROD_MO[7]` ไม่ใช่ตัวเลข single-SKU ล้วน การบวกส่วนต่างจึงปลอดภัยกว่า

| สินค้า | Δ ยอดขาย | Δ ชิ้น |
|---|---|---|
| Refresh Wipes | +7,733 | +93 |
| Sugar 500ml | +6,401 | +18 |
| Interior 500ml | +3,408 | +9 |
| Interior Wipes | +3,398 | +45 |
| Spot 500ml | +3,015 | +8 |
| Tire & Trim | +2,024 | +4 |
| X-Glass | +1,886 | +5 |
| Refresh 500ml | +1,820 | +5 |
| Perfect | +1,619 | +8 |
| Martini | +1,432 | +11 |
| Quartz 1L | +1,067 | +4 |
| Reflex 250ml | +1,041 | +3 |
| Wool Duster / Sugar 3L / Mind | 0 | 0 |
| **รวม 15 สินค้า** | **+34,844** | |

**ไฟล์ที่แก้:**

`WIBWUB_Mobile.html`
- `ALL_PRODUCTS` — บวก delta ที่ `v` และ `q` (12 รายการ)
- `PROD_MO` — บวก delta ที่ **index 7 เท่านั้น** (index 0–6 เหมือนเดิมทุก byte — verify ด้วย git diff แล้ว)
- คอมเมนต์ `Aug(1-30)` → `Aug(1-31)`

`WIBWUB_Dashboard.html`
- ตาราง Top Products — คอลัมน์ รวม (฿) + จำนวน (12 แถว)
- แถวรวมทั้งหมด: ฿65.44M → **฿65.49M** · 259,838 → **260,087** ชิ้น
- KPI "ยอดขายรวม ม.ค.–ส.ค.": ฿65.44M → **฿65.49M**
- กราฟ `pr_top10` — dataset Shopee / TikTok / Facebook (คำนวณ delta แยกช่องทางจากคอลัมน์ `ช่องทางติดต่อ`)
- กราฟ `pr_channel` — Shopee 22,020,234→**22,038,221** · Facebook 6,196,501→**6,197,561** · TikTok 9,017,420→**9,033,217**
- คอมเมนต์ `(ม.ค.–30 ส.ค.)` → `(ม.ค.–31 ส.ค.)` ทั้ง 2 จุด

### STEP 5 — sw.js + commit: **สำเร็จ**

`wibwub-v922` → `wibwub-v923` · commit `b1faca7` (5 files, +66/−53)
มี warning `Operation not permitted` ตอน git cleanup temp objects (ข้อจำกัด sandbox↔macOS ตามปกติ) แต่ commit ผ่าน

---

## การตรวจสอบ

- ✅ `node --check` ผ่านทั้ง `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html`
- ✅ git diff ยืนยัน `PROD_MO` index 0–6 ไม่ถูกแตะ
- ✅ invariant `sum(PROD_MO[i].mo) == ALL_PRODUCTS[i].v` ยังคงอยู่ (คลาดเคลื่อน ±1 จาก rounding ที่มีมาก่อนแล้ว — สินค้าที่ delta = 0 ก็คลาด ±1 เหมือนเดิม)
- ✅ array length เดิมทุกตัว (M5 = 8, PROD_MO = 8 ช่อง, AF_* = 8, AFI_* = 10)
- ✅ ไม่มี label `1-30` / `30 ส.ค.` ค้างในส่วน Top Products แล้ว

## สิ่งที่ไม่ได้แก้ (ตั้งใจ) — ควรรู้ไว้

1. **คอลัมน์แยกช่องทางในตาราง Top Products (Shopee/TikTok/Lazada/…) ไม่ได้อัปเดต** — ตัวเลขในตารางกับใน `pr_top10` ไม่ตรงกันอยู่ก่อนแล้ว (เช่น Refresh Wipes TikTok: ตาราง ฿2.01M vs chart 2,003,735 = ฿2.00M) แปลว่าถูกคำนวณคนละรอบ/คนละวิธี ผมจึงไม่ regenerate ทับ เพราะจะทำให้ตัวเลขเปลี่ยนเกินกว่า delta จริง (delta = 0.07% ของยอดรวม) มีเชิงอรรถในหน้าเว็บระบุอยู่แล้วว่าคอลัมน์เหล่านี้เป็นค่าประมาณจาก 15 สินค้า

2. **`mk` / `mkq` ใน `ALL_PRODUCTS` ไม่ได้อัปเดต** — ไม่รู้ที่มาของตัวเลขชุดนี้ ไม่มีในไฟล์ Shipnity

3. **`SH_REV` / `TK_REV` / `LZ_REV` และ `MTD_COVERAGE` (2026-08-30) ไม่ได้อัปเดต** — มาจาก seller center ของแต่ละแพลตฟอร์ม ไม่ใช่ Shipnity คนละแหล่งข้อมูล

4. **มี diff แถมติดมาใน commit** — `WIBWUB_Mobile.html` มีการแก้ "TK Followers +6.0K จาก ม.ค." → "+5.2K" ค้างอยู่ใน working tree ก่อนผมเริ่ม (จาก `update_followers.py`) ถูก commit ไปพร้อมกัน

---

## ต้องทำต่อ

1. **หา export ทดแทน TikTok Transaction Analysis** แล้วแก้ STEP 2 ใน runbook — ค้างมา 1 รอบ (ข้อมูล affiliate ล่าสุดยังเป็น ส.ค. 1–29)
2. รอบ 7 ก.ย. → เติม `ก.ย.` เข้า M5 พร้อมข้อมูลแพลตฟอร์มจริง และดึง Shipnity 1–7 ก.ย.
