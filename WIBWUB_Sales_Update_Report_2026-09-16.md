# WIBWUB Sales Update Report — 2026-09-16 (scheduled run)

## สรุป
ตรวจสอบข้อมูลจาก Google Sheets ทั้ง 3 sheet (Shopee / TikTok / Lazada) แล้วเทียบกับค่าปัจจุบันใน `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html` — **ไม่มีข้อมูลใหม่ ข้ามการอัปเดตและ commit** (เหมือนผลตรวจของรัน 2026-09-15)

## ข้อมูลล่าสุดที่พบใน Sheets (September, row สุดท้าย ยังคงเป็น 01-13/09/26 ทั้ง 3 sheet)

| Platform | ยอดขาย | ยอดใช้ ads | ค่าธรรมเนียม/คอม | Order | ยกเลิก order |
|---|---|---|---|---|---|
| Shopee | ฿3,326,267 | 542,141.58 | 996,549.59 | 5,857 | 324 (5.53%) |
| TikTok | ฿1,424,369.56 | 374,134.99 | 409,641.33 | 6,041 | 401 |
| Lazada | ฿59,719.97 | 3,470 | 12,547.48 | — | — |

## เทียบกับค่าในไฟล์ (index 8 = กันยายน, ตรวจทั้ง WIBWUB_Dashboard.html และ WIBWUB_Mobile.html)

- `SH_REV[8]` = 3326267 ✅ ตรงกับ Sheet
- `TK_REV[8]` = 1424369.56 ✅ ตรงกับ Sheet
- `LZ_REV[8]` = 59719.97 ✅ ตรงกับ Sheet
- `SH_ORD[8]`=5857, `SH_CANCEL_PCT[8]`=5.53, `SH_ADS[8]`=542141.58, `SH_FEE[8]`=996549.59 ✅ ตรงหมด
- `LZ_ADS[8]`=3470, `LZ_FEE[8]`=12547.48, `LZ_COUPON[8]`=1140, `LZ_COST_PCT[8]`=28.73 ✅ ตรงหมด

Sheet ต้นทาง (Shopee/TikTok/Lazada) ยังไม่มีแถวใหม่กว่า 01-13/09/26 ในทั้ง 3 sheet ณ ตอนรันนี้ — พนักงานยังไม่ได้อัปเดตข้อมูลรอบถัดไป

## Array Integrity Check (STEP 0 protection)

`M5` / `SH_REV` / `TK_REV` / `LZ_REV` ใน **ทั้งสองไฟล์** — length ตรงกันทุกตัว = 9 เดือน (ม.ค.–ก.ย. 2569) ไม่มี mismatch ระหว่าง label array กับ data array

## Git

- ไม่มีการแก้ไข `WIBWUB_Dashboard.html` / `WIBWUB_Mobile.html` ในรันนี้ → **ไม่ commit** (ไม่มีอะไรเปลี่ยน)
- `sw.js` ไม่ถูก bump (ไม่มีการเปลี่ยนแปลง dashboard ที่ต้องเคลียร์ cache)
- พบ working-tree changes ที่ค้างจากงานอื่น (ไม่เกี่ยวกับ sales): `data content/Followers_wibwubcar.zip`, `push_now.command`, `scripts/auto_push.log`, `tiktok_product_daily_new.json`, และไฟล์ report/markdown อื่นๆ ที่ untracked — ไม่แตะต้องเพราะไม่ใช่ scope ของงานนี้

## ข้อเสนอแนะ

พนักงานยังไม่ได้เพิ่มแถวใหม่ใน Google Sheet (Shopee/TikTok/Lazada) หลัง 01-13/09/26 — รอบถัดไปจะดึงข้อมูลใหม่อัตโนมัติเมื่อมีการอัปเดตแถวใหม่ในทุก sheet
