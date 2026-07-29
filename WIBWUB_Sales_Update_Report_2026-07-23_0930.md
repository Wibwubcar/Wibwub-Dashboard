# WIBWUB Sales Sheet Update — พฤหัส 23 ก.ค. 2026 (automated run)

## สรุป: ข้อมูลตรงกันหมดแล้ว — ไม่มี commit ใหม่ (sheet ยังไม่มีข้อมูลใหม่กว่าเมื่อวาน)

---

## STEP 1 — อ่าน Google Sheets

- Shopee: แถวล่าสุด `01-19/07/26` — ยอดขาย 3,789,950 / ads 606,406.44 / fee 1,135,469.02 / order 6,883 / cancel 321 (4.66%)
- TikTok: แถวล่าสุด `01-19/07/26` — ยอดขาย 1,358,229.08 / ads(GMV) 1,337,558.33 / ads+GMV spend 332,929.94 / fee+comm 354,806.12 / order 7,336
- Lazada: แถวล่าสุด `01-19/07/26` — ยอดขาย 58,344.78 / ads 4,350 / fee 10,304.62 / coupon 2,160 / cost% 28.82

ทั้ง 3 sheet ยังไม่มีแถวใหม่กว่า `01-19/07/26` (เหมือนรอบเมื่อวาน 22 ก.ค. — พนักงานยังไม่ได้อัปเดตข้อมูลรอบใหม่)

## STEP 2 — เทียบกับ arrays ใน Dashboard/Mobile (index 6 = ก.ค.)

ตรวจแล้วทุกค่าตรงกับ sheet เป๊ะ (ไม่มี delta):

- `SH_REV[6]=3789950`, `SH_ORD[6]=6883`, `SH_ADS[6]=606406`, `SH_FEE[6]=1135469`, `SH_CANCEL_PCT[6]=4.66`
- `TK_REV[6]=1358229.08`
- `LZ_REV[6]=58345`, `LZ_ADS[6]=4350`, `LZ_FEE[6]=10305`, `LZ_COUPON[6]=2160`, `LZ_COST_PCT[6]=28.82`

M5 = 7 labels (ม.ค.–ก.ค.) ตรงกับเดือนปัจจุบันแล้วทั้งสองไฟล์ — ไม่ต้องแก้

git log ล่าสุด (`d8531a6`) เป็นการอัปเดตของ workflow อื่น (Monday business overview) ที่รันหลังจาก sales sync commit เดิม (`3988f00 auto: update 2026-07-22 18:24`) — arrays ยอดขายยังคงค่าที่ถูกต้องอยู่

## STEP 3–6: ข้าม (ไม่มีข้อมูลใหม่ให้อัปเดต)

- ไม่แก้ arrays / hardcoded KPI text / date picker (ไม่มี delta)
- ไม่ bump sw.js / ไม่ commit / ไม่ push ซ้ำ
