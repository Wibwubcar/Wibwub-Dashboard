# WIBWUB Weekly Update — วันศุกร์ 4 ก.ย. 2569

Task: `wibwub-monday-update` · commit `2d600d0` · `sw.js` → `wibwub-v981`

---

## สรุปผล

| STEP | ผลลัพธ์ |
|---|---|
| M5 protection | ทำแล้ว **แต่ revert** — ดูหัวข้อ "ปัญหาที่พบ" ข้อ 1 |
| 1. Shipnity export | สำเร็จ — `Data Shipnity/Data_04-09-2026.xlsx` (3,494,023 B, 3,803 แถว, 01–04/09/2026) |
| 2. TikTok Affiliate export | **no-op** — ไม่มีข้อมูลใหม่ |
| 3. Top Products | สำเร็จ — อัปเดต Mobile + Dashboard |
| 4. Affiliate arrays | **no-op** — ข้อมูลล่าสุดอยู่แล้ว |
| 5. sw.js + commit | สำเร็จ — v980 → v981, commit `2d600d0`, regen `push_now.command` |

**ยังต้อง push เอง:** sandbox push ไม่ได้ (proxy 403) — ดับเบิลคลิก `push_now.command`

---

## STEP 3 — ผลการรวมข้อมูล Shipnity

รวม 99 ไฟล์ `.xlsx` ที่เป็น product-level, dedup ด้วย key `(เลขที่ออเดอร์, รหัสสินค้า, จำนวน)` → **223,818 แถว**

ยอดขายรายเดือน 2569 (บาท):

| ม.ค. | ก.พ. | มี.ค. | เม.ย. | พ.ค. | มิ.ย. | ก.ค. | ส.ค. | ก.ย. (1-4) |
|---|---|---|---|---|---|---|---|---|
| 9,072,564 | 7,594,735 | 7,213,504 | 7,368,461 | 8,101,284 | 7,788,602 | 8,697,335 | 9,899,337 | 1,118,160 |

กันยายน 1–4: **฿1,118,160 · 4,779 ชิ้น** กระจายช่องทาง Shopee ฿629,903 · TikTok ฿324,031 · Facebook ฿69,860 · Carcare ฿50,810 · Line Shopping ฿24,800 · อื่นๆ ฿11,157 · Lazada ฿5,099 · LINE OA ฿2,730 · Website ฿2,495

ข้อมูล ก.ย. อยู่ใน 3 ไฟล์ (`Data_02-09`, `Data_03-09`, `Data_04-09`) ไม่ใช่ไฟล์เดียว — ต้อง dedup ข้ามไฟล์ ไม่งั้นได้ ฿1,100,501 (ขาดไป ฿17,659)

### ไฟล์ที่แก้

**`WIBWUB_Mobile.html`**
- `ALL_PRODUCTS` — บวก delta ก.ย. เข้า `v`/`q` ทั้ง 15 รายการ (คง `mk`/`mkq` เดิม) ลำดับไม่เปลี่ยน
- `PROD_MO` — ต่อค่า ก.ย. เป็น index ที่ 9 ทุกรายการ (8 → 9 ค่า)
- `PROD_MO_LBL` — ต่อ `'ก.ย. (1-4)'`

**`WIBWUB_Dashboard.html`**
- KPI: ยอดขายรวม ฿65.49M → **฿66.61M** (ม.ค. – 4 ก.ย.), Wool Duster ฿5.98M/9,393 → **฿6.02M/9,459**, จำนวนชิ้น 254K → **259K**
- `pr_top10` — บวก delta ก.ย. แยกช่องทางทั้ง 9 dataset × 10 สินค้า
- `pr_channel` doughnut — บวก delta ก.ย. ของ Top 15
- ตารางสินค้าขายดี 15 แถว — บวก delta ก.ย. ทุกคอลัมน์ + หัวตาราง/คำอธิบายเปลี่ยนเป็น ม.ค.–4 ก.ย.

**หลักการที่ใช้:** พบว่า `ALL_PRODUCTS[i].v === sum(PROD_MO[i].mo)` เป๊ะ จึงใช้สูตร `v_new = v_old + sep_rev` แทนการเขียนทับด้วยตัวเลข recompute ทั้งก้อน (ตัวเลข ม.ค.–ส.ค. ที่ recompute ใหม่ต่างจากของเดิมเล็กน้อย — ถ้าเขียนทับจะทำให้ตัวเลขในอดีตขยับ)

---

## ปัญหาที่พบ (SKILL.md ควรแก้)

**1. กฎ M5 protection ผิดทิศทางในเดือนนี้ — ทำแล้วต้อง revert**

กฎบอกให้ขยาย `M5` ให้ยาวเท่าเลขเดือนปัจจุบัน (9) แต่ **array ข้อมูลยอดขายทุกตัวยังยาว 8** (`SH_REV`, `TK_REV`, `LZ_REV`, `SH_ORD`, `TK_AFI`, … ~33 arrays) เพราะ sales sync ยังไม่ได้ ingest เดือน ก.ย.

ถ้าปล่อยไว้จะเกิด:
- คอลัมน์ ก.ย. ว่างในทุกกราฟที่ใช้ `labels: M5`
- `mtdCoverageLabel()` แสดง "ก.ย. = MTD ถึง 31 ส.ค." ซึ่งคือ stale-label bug ที่ skill `wibwub-avoid-stale-hardcoded-labels` มีไว้กันโดยเฉพาะ

ในไฟล์เองมีคอมเมนต์ยืนยันอยู่แล้ว (`WIBWUB_Dashboard.html:1685`):
> `// index อ้างอิง array M5 ซึ่งยังจบที่ ส.ค. — ก.ย. จะเพิ่มเมื่อ sales sync มีข้อมูลเดือน ก.ย.`

**จึง revert M5 กลับเป็น 8 entries ทั้งสองไฟล์** (net change = 0)

**เสนอแก้กฎเป็น:** ขยาย `M5` ก็ต่อเมื่อ `SH_REV.length >= เลขเดือนปัจจุบัน` เท่านั้น — คือให้ label ตาม data ไม่ใช่ตามปฏิทิน

**2. path ใน SKILL.md เป็น hard-code ของ session เก่า**

SKILL.md เขียน `/sessions/hopeful-serene-fermi/mnt/...` แต่ session นี้คือ `/sessions/brave-intelligent-euler/mnt/...` — ต้องแปลทุก path เอง ควรเปลี่ยนเป็น relative หรือระบุให้หา mount path ก่อน

**3. Shipnity export เป็น 2 ขั้น — SKILL.md บอกแค่ขั้นเดียว**

กด "ส่งออกข้อมูล" **ไม่ได้ทำให้ไฟล์ถูกดาวน์โหลด** แต่เปิด modal ที่ต้องทำต่อ:
1. เลือก radio **"ไฟล์เดียว"** (~810, 343) — default คือ "แยกไฟล์" 500 แถว/ไฟล์
2. กด **"Export File"** (~968, 558)
3. รอ ~50 วิ (12.5% → 50% → "Download completed")

ครั้งแรกได้ไฟล์ผิด `e8112e9946b60447d252a30b5e68d819.xlsx` (7,864,387 B, มีคอลัมน์เดียวคือ `orderItemId`) — เป็นไฟล์ขยะที่หลุดออกมาตอนกดปุ่มแรก

**4. date picker ของ Shipnity มี quirk**

- ไอคอนปฏิทิน (1489, 173) เป็น **toggle** — กดซ้ำจะปิด
- กดวันที่รายวันแล้ว panel ปิดโดยไม่ apply
- **ใช้ปุ่ม "เดือนนี้" (~1387, 663) แทน** → apply "1 ก.ย. 2569 ~ 30 ก.ย. 2569" ทันที
- ต้อง screenshot ก่อนคลิกทุกครั้ง เพราะ panel fade-in

**5. STEP 2 (TikTok Affiliate) เป็น no-op จริง — ไม่ใช่ error**

หน้า Transaction Analysis ขึ้น "อัปเดตเมื่อ: 1 ก.ย. 2026 0:00", ปฏิทินเดือน ก.ย. เลือกได้แค่วันที่ 01 (02–05 เป็นสีเทา) ไฟล์ 01/09 ดึงไปแล้วตอน 02:00 วันนี้ และ `AF_*`/`AFI_*` มีตัวเลข ก.ย. (1-2) ที่ใหม่กว่าอยู่แล้ว → STEP 2 และ STEP 4 ข้ามได้ถูกต้อง

SKILL.md ควรระบุ exit condition นี้ไว้ ไม่งั้นรอบต่อไปจะพยายาม export ซ้ำ

**6. background process ตายระหว่าง bash call**

ทั้ง `nohup ... &` และ `setsid nohup ... & disown` หยุดทำงานทันทีที่ call จบ — ต้องเขียนสคริปต์แบบ chunked (`agg_chunk.py start count`) + pickle state file แล้วเรียกหลายรอบ

**7. เบ็ดเตล็ด**

- `/tmp/agg_state.pkl` เก่าเป็นของ `nobody:nogroup` ลบไม่ได้ → ใช้ชื่อใหม่
- bash timeout 45 วิ → chunk ละ 20 ไฟล์
- `sed -n '959,980p'` บนไฟล์ HTML ระเบิด token limit (บรรทัดยาวมาก) → ใช้ `python3 -c` regex extract แทน
- `.git` มี lock/tmp object ที่ลบไม่ได้ (Operation not permitted) แต่ commit สำเร็จ — warning ไม่เป็นปัญหา

---

## Verification

- `node -e "new Function(script)"` — script ทั้ง 3 ก้อนในทั้งสองไฟล์ parse ผ่าน ไม่มี syntax error
- `ALL_PRODUCTS.length === PROD_MO.length === 15`, `PROD_MO[i].mo.length === 9` ทุกรายการ
- `ALL_PRODUCTS[i].v === sum(PROD_MO[i].mo)` ทุกรายการ (ผิดพลาด ≤ 2 บาทจากการปัดเศษเดิม)
- `ALL_PRODUCTS` เรียงจากมากไปน้อยถูกต้อง — ลำดับเดิมไม่สลับ
- `M5.length === 8` ทั้งสองไฟล์ = เท่ากับ array ข้อมูลทุกตัว
- ไม่มีเดือนก่อนหน้าถูกเขียนทับ — ทุกการแก้เป็นการ **บวก** หรือ **ต่อท้าย** เท่านั้น
- `PROD_MO_LBL` แยกอิสระจาก `M5` (คนละ array) จึงเพิ่ม ก.ย. ได้โดยไม่กระทบกราฟ platform
