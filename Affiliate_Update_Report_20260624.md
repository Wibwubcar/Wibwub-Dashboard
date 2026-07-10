# WIBWUB Affiliate Auto-Update — 24 มิ.ย. 2569

**ช่วงข้อมูล:** 1–23 มิ.ย. 2569 (TikTok Affiliate Transaction Analysis)
**Shop:** 7494549095358892612 (TH)

## ผล (June MTD)
- **GMV:** ฿436,626
- **Net (หลังคืน):** ฿429,317
- **Commission:** ฿54,274
- **ครีเอเตอร์มียอดขาย (GMV>0):** 308
- **ครีเอเตอร์ Active (≥฿1,000):** 66

## ไฟล์ที่ export + ย้ายเข้า Data Affiliate/
- ครีเอเตอร์/ → Creator_List_20260601-20260623.xlsx ✅ (ประมวลผล)
- สินค้า/ → Product_List_20260601-20260623.xlsx ✅ (ประมวลผล)
- วีดีโอ/ → Video_List_20260601-20260623.xlsx ✅ (เก็บไว้, ไม่มี target)
- ไลฟ์สตรีม/ → Live_List_20260601-20260623.xlsx ✅ (เก็บไว้, ไม่มี target)

## การแก้ไข Dashboard
**WIBWUB_Affiliate_Dashboard.html**
- CREATORS[] → regenerate 66 รายการ active
- CREATOR_MONTHS → อัปเดต jun (index 3) 209 คีย์
- PRODUCTS → อัปเดต monthly.jun + ret.jun 7 สินค้า
- badge → "1–23 มิ.ย. 2569 · อัปเดต 24 มิ.ย. 2569"; note + comment อัปเดต

**WIBWUB_Mobile.html**
- AFI_GMV/NET/COMM[7] = 436626 / 429317 / 54274
- home KPI → "308 creators · มิย.69"

**sw.js:** cache wibwub-v235 → **v236**

## Verify
- JS parse: Affiliate 2/2 scripts OK, Mobile 6/6 scripts OK (0 errors)
- CREATORS=66, CREATOR_MONTHS=209, ค่าทั้งหมดตรง

## ค้างทำ (manual)
git push จาก sandbox ถูก block (HTTP 403 proxy) → **double-click `push_now.command`** บนเครื่องจริงเพื่อ commit + push

## หมายเหตุการตัดสินใจ
- ใช้ date picker ส่วน Details (ถึง 23 มิ.ย.) เป็นช่วง export
- PRODUCTS/top-KPI cr/vid และ KPI "ครีเอเตอร์ Active 1,168" = cumulative → คงไว้ (ตาม precedent เมื่อวาน)
- CREATORS[] = active (GMV≥฿1,000); CREATOR_MONTHS jun = GMV รายคน (ปัด)
