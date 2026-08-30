# WIBWUB Weekly Update — วันอาทิตย์ 30 ส.ค. 2569 (รอบ Monday-run)

Commit: `29e8b3e` · sw.js `wibwub-v894` → `wibwub-v895` · **ยังไม่ push** (รัน `push_now.command`)

## สรุปผล

| ขั้นตอน | ผล |
|---|---|
| 0. ตรวจ `M5` (protection) | ✅ ผ่าน — ทั้งสองไฟล์มี 8 entries ครบเดือน ส.ค. ไม่ต้องแก้ |
| 1. โหลด Shipnity purchase export | ✅ ได้ `Data Shipnity/Data_30-08-2026.xlsx` (30.6 MB, 32,647 แถว, 1–30 ส.ค.) |
| 2. โหลด TikTok Affiliate | ❌ **ล้มเหลว — session หมดอายุ** |
| 3. อัปเดต Top Products | ✅ เสร็จ (วิธี delta) |
| 4. อัปเดต Affiliate arrays | ⏭️ **ข้าม** (ไม่มีข้อมูลจากขั้นตอน 2) |
| 5. sw.js + git commit | ✅ commit แล้ว, regenerate `push_now.command` แล้ว |
| 6. ตรวจสอบ | ✅ ผ่านทุกข้อ |

## ⚠️ สิ่งที่ต้องทำด้วยมือ

1. **Login TikTok Affiliate ใหม่** — `https://affiliate.tiktok.com/insights/transaction-analysis?shop_region=TH&shop_id=7494549095358892612` เด้งไปหน้า login ทั้งรอบ 01:56 น. (ดู `Data Affiliate/Affiliate_Update_Report_20260830_sun_BLOCKED.md`) และรอบนี้ ตัวเลข Affiliate ทั้งหมดยังเป็นของ **27 ส.ค.** ไม่ได้ถูกแตะเลย — `AF_MO`/`AF_GMV`/`AF_NET`/`AF_COM`/`AF_CR` ใน `WIBWUB_Affiliate_Dashboard.html` และ `AFI_MONTHS`/`AFI_GMV`/`AFI_NET`/`AFI_COMM` ใน `WIBWUB_Mobile.html` คงเดิมทุกค่า
2. **Push** — ดับเบิลคลิก `push_now.command` (แซนด์บ็อกซ์ push ไม่ได้ proxy 403)

## วิธีคำนวณที่ใช้: delta ไม่ใช่คำนวณใหม่ทั้งหมด

พยายาม recompute ยอดสะสม ม.ค.–ส.ค. ใหม่ทั้งหมดจากไฟล์ Shipnity แล้ว **ไม่สามารถ reproduce ค่าเดิมได้** — ลองทั้ง ราคา×จำนวน แบบ dedup ออเดอร์, แบบไม่ dedup, และแบบเฉลี่ย `ยอดขายออเดอร์` ตามสัดส่วน ค่าที่ได้ต่ำกว่าค่าเดิมของเดือน ก.ค. อยู่ 1.6%–8.1% โดยอัตราส่วนไม่คงที่ แปลว่าสูตรที่ใช้สร้าง baseline เดิมไม่ตรงกับสูตรใดที่ทดลอง

จึงเลือกวิธี **delta**: สแกน `Data_29-08-2026.xlsx` และ `Data_30-08-2026.xlsx` ด้วยสูตรเดียวกันเป๊ะ แล้วเอาผลต่างไปบวกเข้ากับค่าเดิม → baseline ประวัติศาสตร์ไม่ถูกรบกวน และเดือน ม.ค.–ก.ค. ไม่ถูกแตะแม้แต่ตัวเดียว (ตรวจแล้ว)

**ผลต่างรวมทั้ง catalog (ยอดวันที่ 30 ส.ค.): +฿93,058 · +458 ชิ้น**
แยกช่องทาง: Shopee +฿45,224 · TikTok +฿40,499 · Facebook +฿6,513 · Lazada +฿822

### ผลต่างรายสินค้า (Top 15)

| # | สินค้า | Δ ยอดขาย | Δ จำนวน |
|---:|---|---:|---:|
| 1 | Wool Duster | +3,316 | +5 |
| 2 | Sugar 500ml | +21,426 | +62 |
| 3 | Interior 500ml | +4,907 | +14 |
| 4 | Refresh Wipes | +11,518 | +141 |
| 5 | Interior Wipes | +6,027 | +77 |
| 6 | Refresh 500ml | +2,876 | +8 |
| 7 | Spot 500ml | +3,216 | +8 |
| 8 | Perfect | +2,435 | +15 |
| 9 | Reflex 250ml | +1,883 | +5 |
| 10 | Tire&Trim 500ml | +2,793 | +6 |
| 11 | X-Glass | +1,604 | +4 |
| 12 | Sugar 3L | 0 | 0 |
| 13 | Martini | +2,061 | +15 |
| 14 | Quartz 1L | +1,998 | +9 |
| 15 | Mind 500ml | +781 | +2 |
| | **รวม Top 15** | **+66,841** | |

## ไฟล์ที่แก้

**`WIBWUB_Mobile.html`**
- `ALL_PRODUCTS` — `v`/`q` ทั้ง 15 รายการ (Wool Duster ยอดสะสมขึ้นเป็น ฿5,955,571 / 9,350 ชิ้น)
- `PROD_MO` — เขียนทับ **เฉพาะ index 7 (ส.ค.)** เท่านั้น; comment `Aug(1-29)` → `Aug(1-30)`
- `PROD_MO_LBL` — `'ส.ค. (1-28)'` → `'ส.ค. (1-30)'` (label ค้างมาจากรอบก่อน)
- header `data-updated` → `30 ส.ค. 2569`

**`WIBWUB_Dashboard.html`**
- KPI: ยอดขายรวม `฿64.77M` → `฿64.86M`; สินค้าขายดีสุด `฿5.95M · 9,345` → `฿5.96M · 9,350`
- ตาราง Top 15: คอลัมน์ `รวม (฿)` + `จำนวน` ครบทุกแถว, คอลัมน์ช่องทางเฉพาะแถวที่ค่าปัดเศษเปลี่ยน
- แถว `รวมทั้งหมด`: Shopee `฿21.96M*`, TikTok `฿8.98M*`, Lazada `฿405K*`, Facebook `฿6.18M*`, รวม `฿64.86M`, จำนวน `257,235`
- chart `pr_top10` — Shopee/TikTok/Facebook/Lazada datasets
- chart `pr_channel` — Shopee 21,824,791 · Facebook 6,164,391 · TikTok 8,876,862 · Lazada 404,432
- label วันที่ `29 ส.ค.` → `30 ส.ค.` ทุกจุด (0 จุดค้าง)

**`sw.js`** `wibwub-v894` → `wibwub-v895`
**`push_now.command`** เขียนใหม่ — เพิ่มการลบ `maintenance.lock` + `tmp_obj_*` และ `git reset --mixed` ก่อน push

**ไม่แตะ:** `WIBWUB_Affiliate_Dashboard.html`

## ข้อจำกัดที่ยอมรับในรอบนี้

- ตาราง Dashboard เก็บค่าแบบปัดเศษ (฿X.XXM/฿XXXK) ทำให้ไม่รู้ค่าจริงระดับหลักหน่วย — แถวที่ 11–15 (X-Glass, Sugar 3L, Martini, Quartz, Mind) จึงอัปเดตเฉพาะ `รวม`/`จำนวน` ส่วนคอลัมน์แยกช่องทางปล่อยไว้ (คลาดเคลื่อน ≤ ฿1.5K ต่อช่อง) แถว 1–10 อัปเดตครบเพราะมีค่าเต็มจาก `pr_top10`
- ค่า `฿64.86M` และ `฿945K` (X-Glass Shopee) มาจากการสมมติจุดกึ่งกลางของช่วงปัดเศษเดิม ±฿1K
- จำนวนแถวที่สแกนรอบนี้ (32,269 → 32,647) ต่างจากที่บันทึกไว้รอบก่อนเล็กน้อย เพราะรอบนี้ใช้สูตรเดียวกันกับทั้งสองไฟล์โดยไม่กรองวันที่ซ้ำ — ผลต่างจึงยัง self-consistent

## ปัญหาเชิงเทคนิคที่เจอ (ไว้แก้ skill)

1. **path ในไฟล์ task เป็นของ session เก่า** — `/sessions/hopeful-serene-fermi/mnt/...` ไม่มีจริง ต้องแมปเป็น `/sessions/<session ปัจจุบัน>/mnt/...` ทุกครั้ง ควรแก้ SKILL.md ให้ไม่ hardcode ชื่อ session
2. **`browser_batch` error "Can't interact with browser internal pages"** เมื่อแท็บที่ active เป็น `chrome://newtab/` — แก้ด้วยการเรียก `navigate` เดี่ยวๆ ก่อนหนึ่งครั้ง (ขัดกับที่ SKILL.md เตือนว่า navigate เดี่ยวจะค้าง — รอบนี้ไม่ค้าง)
3. **แซนด์บ็อกซ์ commit ไม่ได้เพราะ `.git/index.lock` ค้างและลบไม่ได้** (Operation not permitted บน Google Drive mount) — แก้ด้วย `export GIT_INDEX_FILE=<outputs>/gitindex` แล้ว `cp .git/index` ไปใช้แทน commit ผ่านได้ปกติ
4. **date picker Shipnity เด้งปิดเมื่อคลิกซ้ำ** — ใช้ชิป "เดือนนี้" แทนการเลือกวันทีละวัน
