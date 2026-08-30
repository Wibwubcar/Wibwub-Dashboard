# WIBWUB Weekly Update — 29 ส.ค. 2569 (เสาร์, อัตโนมัติ)

Commit `21932f9` — auto-update: Saturday 2026-08-29 weekly run
sw.js: `wibwub-v882` → `wibwub-v883`
**ยังไม่ push** (sandbox โดน proxy HTTP 403) → ดับเบิลคลิก `push_now.command`

> ⚠️ **STEP 1 ล้มเหลว** — Shipnity export ค้างทั้ง 2 ครั้ง (ครั้งแรก 53.97% ครั้งที่สอง 28.57%) ตามกติกา "retry 1 ครั้ง แล้ว log error" จึงหยุดและใช้ข้อมูลเดิมของวันที่ 28 ส.ค. ต่อ ผลคือ STEP 3 (Top Products) เป็น no-op

---

## STEP 0 — M5 protection
`const M5` ทั้ง `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html` = 8 label (ม.ค.–ส.ค.) ตรงกับเดือนปัจจุบัน (8) → **ไม่แก้**

## STEP 1 — Shipnity ❌ ล้มเหลว

ตั้งช่วง **1 ส.ค. 2569 ~ 29 ส.ค. 2569** สำเร็จ, filter "สินค้าในออเดอร์" คงเดิม, กด ส่งออกข้อมูล → `.xlsx` → ไฟล์เดียว → Export File

| ครั้ง | ความคืบหน้า | ผล |
|---|---|---|
| 1 | 0 → 3 → 22 → 41 → **53.97%** แล้วค้าง 10+ นาที | กด "หยุดทั้งหมด" ยกเลิก |
| 2 (retry) | 1.59 → 9.52 → 23.81 → **28.57%** แล้วค้าง ~10 นาที | ยอมแพ้ตามกติกา |

- ไม่มีไฟล์ใหม่ลงใน `Downloads` และ `Data Shipnity/` (ล่าสุดยังเป็น `Data_สิงหาคม.xlsx` / `Data_28-08-2026.xlsx` 29.1 MB ลงวันที่ 28 ส.ค. 13:28)
- ปล่อย job ครั้งที่ 2 ค้างไว้ในเบราว์เซอร์ — ถ้ามันเสร็จเองภายหลัง LaunchAgent `com.wibwub.download-mover` จะย้ายไฟล์ให้อัตโนมัติ แล้วรอบหน้าจะหยิบไปใช้ได้เลย
- **สาเหตุที่น่าจะเป็น:** ไฟล์ export ขนาด ~29 MB / 31,000+ แถว ฝั่ง Shipnity ประมวลผลช้าผิดปกติในช่วงเวลานี้ (ทั้ง 2 ครั้งค้างคนละจุด = ไม่ใช่ bug ที่แถวใดแถวหนึ่ง)

## STEP 2 — TikTok Affiliate ✅

- ปฏิทินยังเลือกได้ถึง **26 ส.ค.** เท่านั้น (27–29 ยังเป็นสีเทา — TikTok ยังไม่ปล่อยข้อมูล) → ช่วง 01/08/2026–26/08/2026
- panel "รายงาน" ค้างที่ "กำลังส่งออก" 5+ นาที และไม่ auto-refresh → อ่านชื่อไฟล์ในตารางด้วย JS แล้วโหลดรายงานที่พร้อมแล้วของวันเดียวกันแทน (task file อนุญาต)
- ได้ `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260801-20260826.xlsx` — **7,443 แถวข้อมูล**

## STEP 3 — Top Products ⏭️ no-op

ไม่มีไฟล์ Shipnity ใหม่ → **ไม่แตะ** `ALL_PRODUCTS` / `PROD_MO` (Mobile) และตาราง/กราฟ Top Products (Dashboard)
ค่าปัจจุบันยังเป็น baseline **1–28 ส.ค. เต็มวัน** จากรอบ 28 ส.ค. run 2 (commit `d96e24b`) ซึ่งถูกต้องอยู่ — ยืนยันว่า `git status` ของ `WIBWUB_Mobile.html` และ `WIBWUB_Dashboard.html` สะอาด ไม่มีการแก้ค้างไว้

## STEP 4 — Affiliate arrays ✅ (ยืนยันแล้ว ค่าตรง ไม่ต้องแก้เพิ่ม)

ตรวจ label ก่อนเขียนตามกติกา: `AF_MO[-1]` = `"ส.ค. (1-26)"`, `AFI_MONTHS[-1]` = `'สค.69 (1-26)'` → เป็นเดือนปัจจุบันแล้ว = **กรณีเขียนทับ index สุดท้าย ไม่ append**

คำนวณใหม่จากไฟล์จริง (map ด้วย **ชื่อคอลัมน์**):

```
GMV = 1,426,449   Net = 1,403,152   Comm = 163,882   Creators = 718   Returns = 23,298
```

ค่านี้ **ตรงกับที่อยู่ในไฟล์แล้วทุกตัว** (รอบเช้า 09:12 ICT เขียนไว้แต่ยังไม่ commit) จึงไม่ต้องแก้ตัวเลขซ้ำ — งานรอบนี้คือ **commit ของที่ค้างอยู่**

| Array | index สุดท้าย |
|---|---:|
| `AF_GMV` / `AFI_GMV` | 1,426,449 |
| `AF_NET` / `AFI_NET` | 1,403,152 |
| `AF_COM` / `AFI_COMM` | 163,882 |
| `AF_CR` | 718 |

KPI card ที่ hardcode ไว้ตรงกันหมด: `฿1426.4K` · `฿1403.2K` · `718` · `฿163.9K`

## STEP 5 — sw.js + commit ✅

- `sw.js`: `wibwub-v882` → **`wibwub-v883`**
- commit `21932f9` — 2 ไฟล์เปลี่ยนจริง (`WIBWUB_Affiliate_Dashboard.html` + `sw.js`), 6 insertions / 6 deletions
  (`WIBWUB_Mobile.html` และ `WIBWUB_Dashboard.html` add เข้าไปด้วยตามกติกา แต่ไม่มี diff → ไม่เกิด empty commit)
- เขียน `push_now.command` ใหม่ + `chmod +x` — เพิ่มการล้าง `maintenance.lock` และ `tmp_obj_*` ที่ sandbox ลบไม่ได้ (Google Drive mount ไม่ยอม unlink)

## Verification ✅

- `node --check` บน JS ที่ extract จากทั้ง 3 dashboard + `sw.js` → **ผ่านทั้งหมด**
- ความยาว array: `M5` = 8 ทั้งสองไฟล์ · `AF_*` = 8 ทุกตัว · `AFI_*` = 10 ทุกตัว
- `git diff HEAD~1 HEAD -- WIBWUB_Mobile.html` = **ว่าง** → ยืนยันว่าไม่มีเดือนไหนถูกเขียนทับ และ `PROD_MO` ไม่ถูกแตะ
- working tree ของ 4 ไฟล์หลัก = สะอาดหลัง commit

---

## ⚠️ ข้อสังเกต / สิ่งที่ตัดสินใจเอง

1. **task ชื่อ "monday-update" แต่รันวันเสาร์ 29 ส.ค.** และวันนี้มีรอบ affiliate รันไปแล้วช่วงเช้า (09:12 ICT, sw.js v880→v881, ต่อมามี job อื่นดันขึ้นเป็น v882) — จึงระวังไม่ให้ commit ซ้ำ: ตรวจ `git status` ก่อน แล้ว commit เฉพาะส่วนที่ค้างจริง
2. **STEP 1 ล้มเหลว → STEP 3 ข้าม** เลือกไม่คำนวณ Top Products ใหม่จากไฟล์ 28 ส.ค. เพราะจะได้ค่าเท่าเดิมเป๊ะ (ไฟล์เดียวกับที่ baseline ใช้อยู่) = แก้ไปก็ไม่มีอะไรเปลี่ยน แต่เสี่ยงพลาดจากสูตรที่ยังไม่ตรง 100%
3. **สูตร Top Products ยังไม่ตรงกับ baseline 100%** — ยังต้องใช้วิธี delta ต่อไป **ควรบันทึกสูตรทางการลงใน skill `update-wibwub`** (แจ้งเป็นรอบที่ 3 แล้ว)
4. **Task file ระบุคอลัมน์ไฟล์ Affiliate ผิด** — ระบุ GMV=col1, คืนเงิน=col2, คอมมิชชั่น=col10 แต่ไฟล์จริงมี **22 คอลัมน์** (คืนเงิน=**col4**, คอมมิชชั่น=**col21**) ต้อง map ด้วยชื่อคอลัมน์เท่านั้น (แจ้งซ้ำเป็นรอบที่ 5)
5. **Task file บอกว่า `navigate` เดี่ยวจะค้าง ต้องใช้ `browser_batch`** — ของจริง **ตรงข้าม**: `browser_batch` + navigate จะ error `"Can't interact with browser internal pages"` ถ้าแท็บอยู่บน `chrome://newtab` ต้องยิง `navigate` เดี่ยวก่อน แล้วค่อยใช้ batch (แจ้งซ้ำเป็นรอบที่ 2) — **ควรแก้ task file**
6. **ปฏิทิน Shipnity ต้องคลิก 2 ครั้ง** ครั้งแรกแค่ focus ช่อง ครั้งที่สองถึงเปิด popup
7. **`rm` บน Google Drive mount ทำไม่ได้** (Operation not permitted) — ไฟล์ซ้ำ `Transaction_Analysis_Creator_List_20260801-20260826 (1).xlsx` ยังค้างอยู่ใน `Data Affiliate/ครีเอเตอร์/` (ข้อมูลเหมือนกันเป๊ะ ไม่กระทบการคำนวณ) ถ้าอยากลบต้องลบบนเครื่อง
8. **push ทำจาก sandbox ไม่ได้** (proxy HTTP 403) — ต้องรัน `push_now.command` บนเครื่อง

## ➡️ สิ่งที่ควรทำรอบหน้า

- ลอง export Shipnity ใหม่ (ช่วง 1–30 ส.ค. หรือ 1–31 ส.ค.) แล้วค่อยอัปเดต Top Products ทีเดียว — ตอนนี้ค้างข้อมูลวันที่ 29 ส.ค. อยู่ 1 วัน
- ถ้ายัง export ไม่ผ่านอีก อาจต้องลองแบ่งช่วงเป็น 2 ก้อน (1–15 / 16–31) เพื่อลดขนาดไฟล์ต่อครั้ง
