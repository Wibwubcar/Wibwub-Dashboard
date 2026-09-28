# WIBWUB Sales Update Report — 2026-09-12 (run2)

## สรุป
รันตาม schedule "WIBWUB Sales Sheet Update — จันทร์+พฤหัส 09:30" ตรวจสอบ Google Sheets ทั้ง 3 sheet
(Shopee / TikTok / Lazada) เทียบกับค่าปัจจุบันใน `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html`

**ผลตรวจสอบ: ไม่มีข้อมูลใหม่ (No new data) — ข้าม commit**

หมายเหตุ: มีการรันของ task เดียวกันนี้ไปแล้วครั้งหนึ่งในวันนี้ (ดู `WIBWUB_Sales_Update_Report_2026-09-12.md`,
commit `5169494`) ซึ่งได้แก้ไข `SH_REV` เดือนกันยายนที่ผิดพลาดไปแล้ว การรันครั้งนี้เป็นการยืนยันซ้ำว่าข้อมูลใน Sheet
ยังตรงกับที่มีอยู่ในแดชบอร์ด ไม่มีการเปลี่ยนแปลงเพิ่มเติม

## STEP 0 — Array Integrity Check
ตรวจสอบความยาว array ในทั้งสองไฟล์ (M5, SH_REV, TK_REV, LZ_REV, SH_ORD, SH_CANCEL_PCT, SH_ADS, SH_FEE,
LZ_ADS, LZ_FEE, LZ_COUPON, LZ_COST_PCT) — **ทุกตัวมี 9 elements ตรงกันหมด ไม่มี mismatch**

## ข้อมูลล่าสุดจาก Sheets เทียบกับค่าในแดชบอร์ด (เดือนกันยายน 2569, index 8)

| Field | Sheet (ล่าสุด) | Dashboard ปัจจุบัน | ตรงกัน? |
|---|---|---|---|
| Shopee ยอดสุทธิ (01-06/09) | 1,212,856 | 1,212,856 | ✅ |
| Shopee ads | 202,487.77 | 202,487.77 | ✅ |
| Shopee fee | 363,371.66 | 363,371.66 | ✅ |
| Shopee orders | 2,231 | 2,231 | ✅ |
| Shopee cancel% | 5.647691618 → 5.65 | 5.65 | ✅ |
| TikTok ยอดสุทธิ (01-09/09) | 1,021,797.09 | 1,021,797.09 | ✅ |
| Lazada ยอดสุทธิ (01-06/09) | 15,785.40 | 15,785.40 | ✅ |
| Lazada ads | 1,550 | 1,550 | ✅ |
| Lazada fee | 2,788.63 | 2,788.63 | ✅ |
| Lazada coupon | 270 | 270 | ✅ |
| Lazada cost% | 29.19552244 → 29.20 | 29.20 | ✅ |

ทุกค่าตรงกันทั้งหมด — Sheet ยังไม่มีแถวใหม่เพิ่มเติมนับจากการรันครั้งก่อนหน้าในเช้าวันนี้

## Date Picker / KPI Text
ไม่มีการเปลี่ยนแปลง เนื่องจากไม่มีเดือนใหม่หรือค่าใหม่ที่ต้องอัปเดต

## Git
**ไม่มีการ commit** — ไม่มีการเปลี่ยนแปลงข้อมูลใน `WIBWUB_Dashboard.html` / `WIBWUB_Mobile.html` / `sw.js`
จากการรันครั้งนี้ (ตามกฎ "ข้อมูลเดือนนี้ไม่เปลี่ยนแปลงจากครั้งก่อน → log และ skip commit")
