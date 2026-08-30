# WIBWUB Sales Sheet Update — 30 ส.ค. 2569 (09:30)

**ผลลัพธ์: No new data — ไม่มีการแก้ไขไฟล์ และไม่ commit**

---

## STEP 0 — ตรวจความยาว array (verify-only)

ผ่านทั้งสองไฟล์ ไม่มี mismatch:

| ไฟล์ | M5 | SH_REV | TK_REV | LZ_REV | array อื่นทั้งหมด |
|---|---|---|---|---|---|
| WIBWUB_Dashboard.html | 8 | 8 | 8 | 8 | 8 (รวม MONTH_LABELS_FULL/SHORT) |
| WIBWUB_Mobile.html | 8 | 8 | 8 | 8 | 8 |

เดือน ส.ค. (index 7) มีค่าจริงครบอยู่แล้ว — ไม่ต้อง push label เดือนใหม่ และไม่ได้แตะ M5 / MONTH_LABELS_* / MP_MONTH_BOUNDS

---

## STEP 1 — row สุดท้ายของ ส.ค. 2569 ในแต่ละ Sheet

| Sheet | row สุดท้าย | ยอดขาย | เทียบกับรอบก่อน (27 ส.ค. รอบเย็น) |
|---|---|---|---|
| Shopee | `01-23/08/26` | 4,787,148 | เท่าเดิม — ไม่มี row ใหม่ |
| TikTok | `01-26/08/26` | 2,057,387.59 | เท่าเดิม — ไม่มี row ใหม่ |
| Lazada | `01-23/08/26` | 84,993.69 | เท่าเดิม — ไม่มี row ใหม่ |

พนักงานยังไม่ได้เติมข้อมูลรอบสัปดาห์ล่าสุด (คาดว่า row ถัดไปคือ `01-30/08/26`) ในทั้ง 3 sheet

---

## STEP 2 — เทียบค่าใน dashboard กับ sheet ทีละ array (index 7 = ส.ค.)

| Array | ค่าในไฟล์ | ค่าใน Sheet | ตรงกัน |
|---|---|---|---|
| SH_REV | 4,787,148 | 4,787,148 | ✅ |
| SH_ORD | 8,361 | 8,361 | ✅ |
| SH_CANCEL_PCT | 6.15 | 6.1476 | ✅ (ปัดเศษ) |
| SH_FEE | 1,434,148 | 1,434,148 | ✅ |
| SH_ADS | 909,740.33 | 866,977 | ⚠️ ดูหมายเหตุ |
| TK_REV | 2,057,387.59 | 2,057,387.59 | ✅ |
| TK_ORD | 9,846 | 9,846 | ✅ |
| TK_CANCEL / _PCT | 6.53 | 6.5306 | ✅ |
| TK_AFI / TK_NET | 1,375,920 / 1,352,971 | 1,375,920.38 / 1,352,971.16 | ✅ |
| TK_ADS / TK_ADSSPEND | 2,020,799 / 549,245 | 2,020,798.51 / 549,244.94 | ✅ |
| TK_LIVE / TK_FEECOMM | 230,100 / 620,547 | 230,100.00 / 620,546.69 | ✅ |
| TK_AFIPCT / TK_NEW / TK_OLD | 65.8 / 7,855 / 971 | 65.76 / 7,855 / 971 | ✅ |
| LZ_REV | 84,993.69 | 84,993.69 | ✅ |
| LZ_ADS / LZ_FEE / LZ_COUPON | 9,730 / 15,010.82 / 2,250 | เท่ากันทุกตัว | ✅ |
| LZ_COST_PCT | 31.76 | 31.7563 | ✅ |

**ไม่มี array ใดถูกแก้ไข**

### ⚠️ หมายเหตุ SH_ADS
`SH_ADS[7] = 909,740.33` สูงกว่าเลขใน Shopee sheet (866,977 ณ 23 ส.ค.) เพราะมาจาก commit คนละสายงาน:
`adc6252 — Shopee Ads: sync 1-30 Aug 2026 (43 campaigns, spend ฿909,740.33 / ROAS 6.86)`
คือข้อมูล ads ถึง **30 ส.ค.** จากระบบ Shopee Ads โดยตรง ซึ่งใหม่กว่าและละเอียดกว่า sheet (ถึง 23 ส.ค. เท่านั้น)
→ **ตั้งใจไม่ทับค่านี้ด้วยเลขจาก sheet** เพราะจะเป็นการถอยข้อมูลกลับไป 7 วัน

---

## STEP 3 / 3B — Label และ date picker

ตรวจแล้วถูกต้องอยู่แล้ว ไม่ต้องแก้:
- `MTD_COVERAGE = { Shopee:'2026-08-23', TikTok:'2026-08-26', Lazada:'2026-08-23' }` — ตรงกับ row สุดท้ายจริงของทั้ง 3 sheet
- `MTD_MAX_DATE` และ `MP_MONTH_BOUNDS` เดือนสุดท้าย derive จาก `MTD_COVERAGE` (ไม่ hardcode)
- `MP_DATE_MAX` derive จาก `_now` · `rangeEnd = 7` ถูกต้องสำหรับ ส.ค.
- `MONTH_LABELS_FULL` / `MONTH_LABELS_SHORT` = 8 ตัว ตรงกับ M5

---

## STEP 4 — Commit

**Skip ตามสเปค** ("ข้อมูลเดือนนี้ไม่เปลี่ยนแปลงจากครั้งก่อน → log No new data และ skip commit")
- ไม่ bump `sw.js` (คงที่ `wibwub-v891`)
- `git status` สะอาด · ไม่มี commit ค้างที่ยังไม่ push (`origin/main..HEAD` ว่าง)
- ไม่ต้องกด `push_now.command` รอบนี้

---

## ต้องทำต่อ

ให้พนักงานเติม row `01-30/08/26` ในทั้ง 3 sheet (Shopee / TikTok / Lazada) แล้วรอบถัดไปจะ sync ให้อัตโนมัติ
