# WIBWUB Sales Sheet Update — 30 ส.ค. 2569 (รอบที่ 2)

**ผลลัพธ์: No new data — ไม่แก้ไขไฟล์ ไม่ bump sw.js ไม่ commit**

รอบนี้เป็นการรันซ้ำหลังรอบ 09:30 ของวันเดียวกัน ผลสรุปตรงกัน: พนักงานยังไม่ได้เติม row รอบใหม่ใน sheet ทั้ง 3 ตัว

---

## STEP 0 — ตรวจความยาว array (verify-only, ไม่แก้ไฟล์)

ผ่านทั้งสองไฟล์ ไม่มี mismatch — ทุก array มี 8 elements ตรงกับ M5

| ไฟล์ | M5 | SH_REV | TK_REV | LZ_REV | MONTH_LABELS_FULL/SHORT | MP_MONTH_BOUNDS |
|---|---|---|---|---|---|---|
| WIBWUB_Dashboard.html | 8 | 8 | 8 | 8 | 8 / 8 | 8 |
| WIBWUB_Mobile.html | 8 | 8 | 8 | 8 | (ไม่มีในไฟล์นี้) | (ไม่มีในไฟล์นี้) |

เดือน ส.ค. (index 7) มีค่าจริงครบแล้ว → ไม่ต้อง push label เดือนใหม่ ไม่แตะ M5 / MONTH_LABELS_* / MP_MONTH_BOUNDS

---

## STEP 1 — row สุดท้ายของ ส.ค. 2569 ในแต่ละ Sheet

| Sheet | row สุดท้าย | ยอดขาย | เทียบรอบ 09:30 |
|---|---|---|---|
| Shopee | `01-23/08/26` | 4,787,148 | เท่าเดิม |
| TikTok | `01-26/08/26` | 2,057,387.59 | เท่าเดิม |
| Lazada | `01-23/08/26` | 84,993.69 | เท่าเดิม |

ยังไม่มี row `01-30/08/26` ในทั้ง 3 sheet

---

## STEP 2 — เทียบค่าใน dashboard กับ sheet (index 7 = ส.ค.)

| Array | ค่าในไฟล์ | ค่าใน Sheet | ตรงกัน |
|---|---|---|---|
| SH_REV | 4,787,148 | 4,787,148 | ✅ |
| SH_ORD | 8,361 | 8,361 | ✅ |
| SH_CANCEL_PCT | 6.15 | 6.1476 | ✅ (ปัดเศษ) |
| SH_FEE | 1,434,148 | 1,434,148 | ✅ |
| SH_NEW / SH_OLD | 5,214 / 1,873 | 5,214 / 1,873 | ✅ |
| SH_ADS | 929,927.64 | 866,977 | ⚠️ ดูหมายเหตุ |
| TK_REV | 2,057,387.59 | 2,057,387.59 | ✅ |
| TK_ORD | 9,846 | 9,846 | ✅ |
| TK_CANCEL | 6.53 | 6.5306 | ✅ |
| TK_AFI / TK_NET | 1,375,920 / 1,352,971 | 1,375,920.38 / 1,352,971.16 | ✅ |
| TK_ADS / TK_ADSSPEND | 2,020,799 / 549,245 | 2,020,798.51 / 549,244.94 | ✅ |
| TK_LIVE / TK_FEECOMM | 230,100 / 620,547 | 230,100.00 / 620,546.69 | ✅ |
| TK_AFIPCT / TK_NEW / TK_OLD | 65.8 / 7,855 / 971 | 65.76 / 7,855 / 971 | ✅ |
| LZ_REV | 84,993.69 | 84,993.69 | ✅ |
| LZ_ADS / LZ_FEE / LZ_COUPON | 9,730 / 15,010.82 / 2,250 | เท่ากันทุกตัว | ✅ |
| LZ_COST_PCT | 31.76 | 31.7563 | ✅ |

**ไม่มี array ใดถูกแก้ไข**

### ⚠️ หมายเหตุ SH_ADS — ตั้งใจไม่ทับ
`SH_ADS[7] = 929,927.64` สูงกว่าเลขใน Shopee sheet (866,977 ณ 23 ส.ค.) เพราะมาจากคนละสายงาน:

- `a9ce132 — Shopee Ads: refresh Aug data (30/08/2026 19:11 pull)`
- ก่อนหน้านั้น `adc6252 — sync 1-30 Aug 2026 (43 campaigns, ฿909,740.33 / ROAS 6.86)`

คือข้อมูล ads ดึงตรงจากระบบ Shopee Ads ถึง **30 ส.ค.** ซึ่งใหม่กว่า sheet (ถึง 23 ส.ค.) → เขียนทับด้วยเลขจาก sheet จะเป็นการถอยข้อมูลกลับ 7 วัน จึงเว้นไว้

รอบ 09:30 ค่านี้ยังเป็น 909,740.33 — เปลี่ยนเป็น 929,927.64 จาก commit `a9ce132` ตอน 19:11 ยืนยันว่า array นี้ถูก own โดย workflow Shopee Ads ไม่ใช่ workflow นี้

---

## STEP 3 / 3B — Label และ date picker

ตรวจแล้วถูกต้อง ไม่ต้องแก้:

- `MTD_COVERAGE = { Shopee:'2026-08-23', TikTok:'2026-08-26', Lazada:'2026-08-23' }` — ตรงกับ row สุดท้ายจริงทั้ง 3 sheet
- `MP_MONTH_BOUNDS` ตัวสุดท้ายถูก patch ตอน runtime ด้วย `MP_MONTH_BOUNDS[len-1].e = MTD_MAX_DATE` (บรรทัด 1648) → ไม่ใช่ hardcode ที่ค้าง
- `MP_DATE_MAX` derive จาก `_now` · `rangeEnd = 7` ถูกต้องสำหรับ ส.ค.
- `MONTH_LABELS_FULL` / `MONTH_LABELS_SHORT` = 8 ตัว ตรงกับ M5

---

## STEP 4 — Commit

**Skip ตามสเปค** ("ข้อมูลเดือนนี้ไม่เปลี่ยนแปลงจากครั้งก่อน → log No new data และ skip commit")

- ไม่ bump `sw.js` (คงที่ `wibwub-v898`)
- `origin/main..HEAD` ว่าง — ไม่มี commit ค้างที่ยังไม่ push
- ไม่ต้องกด `push_now.command` รอบนี้

ไฟล์ที่ค้างใน `git status` (`Followers_wibwubcar.zip`, `push_now.command`, `scripts/auto_push.log`, Shopee order zip) เป็นของ workflow อื่น — ไม่แตะ

---

## ต้องทำต่อ

ให้พนักงานเติม row `01-30/08/26` ในทั้ง 3 sheet (Shopee / TikTok / Lazada) แล้วรอบถัดไปจะ sync ให้อัตโนมัติ
