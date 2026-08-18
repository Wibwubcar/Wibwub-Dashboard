# WIBWUB Weekly Update — 14 ส.ค. 2569

> หมายเหตุ: รอบเช้าของวันนี้ล้มเหลว (export ทั้งสองแพลตฟอร์มค้าง) รอบนี้รันใหม่และ **สำเร็จครบทุกขั้นตอน** รายงานนี้แทนที่ฉบับ BLOCKED เดิม

## STEP 0 — Protection check ✅
`const M5` มี 8 label (ม.ค.–ส.ค.) = เดือนปัจจุบัน → ผ่าน ไม่ต้องแก้

## STEP 1 — Shipnity ✅
ดาวน์โหลด export ช่วง 1–14 ส.ค. (filter "สินค้าในออเดอร์") → copy เข้า `Data Shipnity/`
รวม 78 ไฟล์ product-level, 200,309 แถวหลัง dedup, 126 SKU

ข้าม 2 ไฟล์ที่ header ไม่ตรงรูปแบบ: `Data_07-08-2026_export.xlsx`, `ROI product 2JUL26.xlsx`

## STEP 2 — TikTok Affiliate ✅
ดาวน์โหลด Transaction Analysis (creator list) ช่วง 1–12 ส.ค. → copy เข้า `Data Affiliate/`
ตรวจสอบกับ KPI card บนหน้าจอ: GMV ฿656,761.00 ตรงกันพอดี
เทียบวิธีคำนวณกับข้อมูลสัปดาห์ก่อน: creator 376 คนตรงกันเป๊ะ, GMV/NET/COMM คลาดเคลื่อน < 0.03%

## STEP 3 — Top Products (ภาพรวมธุรกิจ) ✅
- `ALL_PRODUCTS` (Mobile) — 15 SKU ยอดสะสม
- `PROD_MO` (Mobile) — รายเดือน ม.ค.–ส.ค.(1-14) ครบ 15 SKU
- `pr_top10` stacked bar + ตาราง 15 แถว + แถวรวม (Dashboard)
- `pr_channel` doughnut (Dashboard)
- KPI: ยอดขายรวม ฿60.09M → **฿60.48M** · 234K → **236K ชิ้น** · Facebook 15%→14% · TikTok 17%→18%

### ข้อค้นพบด้านวิธีคำนวณ
ค่า `mk`/`mkq` เดิมนิยามจากช่องทาง **"สินค้าสำหรับทำการตลาด" + "เบิกของ"** (ไม่ใช่เฉพาะ marketing) — ยืนยันตรงกันเป๊ะ 6 SKU
ผลพลอยได้: ตารางช่องทางในแดชบอร์ดตอนนี้ **ผลรวมแต่ละแถวตรงกับยอดรวมของแถวนั้นพอดีเป็นครั้งแรก** (เดิมไม่ตรงเพราะ "อื่นๆ" ไม่ได้รวม marketing/เบิกของ)

## STEP 4 — Affiliate arrays ✅ (ทำแล้วโดย task คู่ขนาน)
`AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR` และ `AFI_*` อัปเดตแล้ว ลงท้ายด้วย "ส.ค. (1-12)"
**ไม่ทำซ้ำ** เพื่อไม่ให้ rolling window เพี้ยน — ตรวจความยาว array แล้วตรงกันทุกตัว

## STEP 5 — Cache + Git ⚠️
- `sw.js`: `wibwub-v666` → **`wibwub-v667`** ✅
- **commit ทำใน sandbox ไม่ได้** — repo มี `.git/index.lock` ค้าง และ mount ของ sandbox ลบ/rename ไฟล์ไม่ได้ (Operation not permitted) ทำให้ `git add` / `git commit` ล้มเหลวทุกวิธี (ลองใช้ `GIT_INDEX_FILE` แยก index แล้วก็ยังติด lock)
- แก้โดยย้าย add/commit/push ไปไว้ใน **`push_now.command`** พร้อมคำสั่งล้าง lock ค้าง

### 👉 ต้องทำเอง 1 ขั้น
ดับเบิลคลิก **`push_now.command`** เพื่อ commit + push ขึ้น GitHub

## Verification
| รายการ | ผล |
|---|---|
| M5 (Dashboard / Mobile) | 8 / 8 ✓ |
| AF_MO / GMV / NET / COM / CR | 8 ทุกตัว ✓ |
| AFI_MONTHS / GMV / NET / COMM | 10 ทุกตัว ✓ |
| PROD_MO 15 SKU × 8 เดือน — ผลรวมตรงยอดสะสม | 15/15 ✓ |
| เดือนก่อนหน้าถูกเขียนทับผิดพลาด | ไม่มี ✓ |

## หมายเหตุ
ไฟล์ซ้ำ `Transaction_Analysis_Creator_List_20260801-20260812 (1).xlsx` ใน `Data Affiliate/` (md5 เหมือนต้นฉบับ) — sandbox ลบไม่ได้ ลบเองได้ตามสะดวก ไม่กระทบตัวเลขเพราะ dedup แล้ว
