# WIBWUB Sales Update Report — 2026-09-16 (scheduled run, run2)

## สรุป
ตรวจสอบข้อมูลจาก Google Sheets ทั้ง 3 sheet (Shopee / TikTok / Lazada) แล้วเทียบกับค่าปัจจุบันใน `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html` อีกครั้ง — **ไม่มีข้อมูลใหม่ ข้ามการอัปเดตและ commit** (ผลตรงกับรันก่อนหน้าของวันนี้ `WIBWUB_Sales_Update_Report_2026-09-16.md`)

## ข้อมูลล่าสุดที่พบใน Sheets (row สุดท้ายของเดือนกันยายน ยังคงเป็น 01-13/09/26 ทั้ง 3 sheet)

| Platform | ยอดขาย | ยอดใช้ ads | ค่าธรรมเนียม/คอม | Order | ยกเลิก order % |
|---|---|---|---|---|---|
| Shopee | ฿3,326,267 | 542,141.58 | 996,549.59 | 5,857 | 5.53% (324) |
| TikTok | ฿1,424,369.56 | 374,134.99 (ยอดใช้จ่าย Ads+GMV) | 409,641.33 | — | — |
| Lazada | ฿59,719.97 | 3,470 | 12,547.48 | คูปอง 1,140 / cost% 28.73 | — |

## เทียบกับค่าใน index 8 (กันยายน) — ทั้ง WIBWUB_Dashboard.html และ WIBWUB_Mobile.html

- `M5` / `MONTH_LABELS_FULL` / `MONTH_LABELS_SHORT` = 9 elements (ม.ค.–ก.ย.) — ตรงกับ data arrays ทุกตัว (9 elements) ✅ ไม่มี mismatch
- `SH_REV[8]`=3326267, `SH_ORD[8]`=5857, `SH_CANCEL_PCT[8]`=5.53, `SH_ADS[8]`=542141.58, `SH_FEE[8]`=996549.59 → ตรงกับ Sheet ทั้งหมด ✅
- `TK_REV[8]`=1424369.56 → ตรงกับ Sheet (ยอดขาย) ✅
- `LZ_REV[8]`=59719.97, `LZ_ADS[8]`=3470, `LZ_FEE[8]`=12547.48, `LZ_COUPON[8]`=1140, `LZ_COST_PCT[8]`=28.73 → ตรงกับ Sheet ทั้งหมด ✅
- `rangeEnd`=8, `MP_DATE_MAX` และ footnote "ม.ค. – 14 ก.ย. 2569" ยังสอดคล้องกับข้อมูลที่มี (ไม่ต้องแก้)

Sheet ต้นทางทั้ง 3 (Shopee/TikTok/Lazada) ยังไม่มีแถวใหม่กว่า 01-13/09/26 ณ เวลาที่รันนี้ — พนักงานยังไม่ได้อัปเดตข้อมูลรอบถัดไปหลังจากรันก่อนหน้า

## Git

- ไม่มีการแก้ไข `WIBWUB_Dashboard.html` / `WIBWUB_Mobile.html` ในรันนี้ → **ไม่ commit**
- `sw.js` ไม่ถูก bump
- ไม่แตะไฟล์อื่นที่ค้างอยู่ใน working tree (ไม่ใช่ scope ของงานนี้)

## ข้อเสนอแนะ

รอ Sheet มีแถวใหม่กว่า 01-13/09/26 ก่อน — รอบถัดไป (Monday/Thursday 09:30) จะดึงและอัปเดตอัตโนมัติเมื่อพนักงานเพิ่มข้อมูลใหม่
