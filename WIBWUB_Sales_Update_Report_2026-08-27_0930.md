# WIBWUB Sales Sheet Update — 27 ส.ค. 2569 09:30

**ผลลัพธ์: No new data — ไม่มีการแก้ไขไฟล์ ไม่ commit**

## STEP 0 — Integrity check (verify-only)

| ไฟล์ | M5 | SH_REV | สถานะ |
|---|---|---|---|
| WIBWUB_Dashboard.html | 8 | 8 | ✅ ตรงกัน |
| WIBWUB_Mobile.html | 8 | 8 | ✅ ตรงกัน |

ทุก data array (SH_REV, TK_REV, LZ_REV, SH_ORD, SH_ADS, SH_FEE, LZ_ADS, LZ_FEE,
LZ_COUPON, LZ_COST_PCT, SH_CANCEL/SH_CANCEL_PCT) มี 8 elements เท่ากันหมดทั้ง 2 ไฟล์
ไม่มีอาการ label เกินค่าจริงแบบบั๊ก 2026-08-03

## STEP 1 — Row สุดท้ายของแต่ละ Sheet

ทั้งสาม sheet ยังหยุดอยู่ที่งวด **01-23/08/26** เท่ากับรอบก่อน — พนักงานยังไม่ได้เติมงวดใหม่

| Sheet | Row สุดท้าย | ยอดสุทธิ | อื่นๆ |
|---|---|---|---|
| Shopee | 01-23/08/26 | 4,787,148 | 8,361 orders · ยกเลิก 514 (6.15%) · fee 1,434,148 · ads 866,977 (รวม FB C-pass) |
| TikTok | 01-23/08/26 | 1,790,219.03 | 8,575 orders · ยกเลิก 572 (6.67%) · ads+GMV 473,046.74 · ค่าคอม 516,909.24 |
| Lazada | 01-23/08/26 | 84,993.69 | ads 9,730 · fee 15,010.82 · coupon 2,250 · cost 31.76% |

## STEP 2–3B — เทียบกับ arrays ปัจจุบัน (index 7 = ส.ค.)

ทุกค่าตรงกับ sheet อยู่แล้ว → ไม่ต้องเขียนทับ

`SH_REV[7]=4787148` ✅ · `TK_REV[7]=1790219.03` ✅ · `LZ_REV[7]=84993.69` ✅ ·
`SH_ORD[7]=8361` ✅ · `SH_CANCEL_PCT[7]=6.15` ✅ · `SH_FEE[7]=1434148` ✅ ·
`LZ_ADS[7]=9730` ✅ · `LZ_FEE[7]=15010.82` ✅ · `LZ_COUPON[7]=2250` ✅ · `LZ_COST_PCT[7]=31.76` ✅

Date picker: `MP_MONTH_BOUNDS` ส.ค. = `2026-08-01 → 2026-08-23` ตรงกับข้อมูลจริง,
`rangeEnd = 7`, footnote "ส.ค. = MTD ถึง 23 ส.ค." ถูกต้อง — ไม่มีเดือนใหม่ ไม่ต้องแก้

## ⚠️ ข้อสังเกต — SH_ADS ไม่ได้เขียนทับโดยตั้งใจ

`SH_ADS[7] = 796,207.17` ในแดชบอร์ด มาจาก **Shopee Ads report (1–26 ส.ค.)** ที่ sync ไว้เมื่อ
26 ส.ค. เย็น (commit `382a2ca`) ส่วนตัวเลข 866,977 ใน Sheet คือ **ads รวม Facebook C-pass +
Shopee C-pass ของงวด 1–23 ส.ค.** ซึ่งเป็นคนละนิยาม และเป็นช่วงวันที่สั้นกว่า
จึงคงค่าจาก Ads report ไว้ ไม่เขียนทับด้วยค่าจาก Sheet

## STEP 4 — Commit

ข้าม ตามกฎ "ข้อมูลเดือนนี้ไม่เปลี่ยนแปลงจากครั้งก่อน → skip commit"
`git status` ของ WIBWUB_Dashboard.html / WIBWUB_Mobile.html / sw.js สะอาด ไม่มี diff
sw.js ยังเป็นเวอร์ชันเดิม (v838) ไม่ได้ bump

**รอบถัดไป:** เมื่อ Sheet มีงวด 01-31/08/26 (หรือ 01-26/08/26) ครบทั้งสามแพลตฟอร์ม
ค่อยอัปเดต index 7 พร้อมกันทุก array
