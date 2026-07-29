# WIBWUB Sales Sheet Update — 2026-07-28 08:38 ICT (อังคาร, off-cycle check)

## ผลลัพธ์: ไม่มีการเปลี่ยนแปลง (No new data — already up to date)

อ่าน Shopee / TikTok / Lazada sheets สดจาก Google Drive แล้ว — แถวสะสมล่าสุดของทั้ง 3 sheet คือ **01-26/07/26** (ยังไม่มีแถวใหม่หลังจากนี้)

### ข้อมูลที่อ่านได้ (เดือน ก.ค. 2026, index 6, สะสมถึง 26/07/26)

| แหล่ง | ยอดขาย | Ads spend | ค่าธรรมเนียม/คอมมิชชั่น | orders | อื่นๆ |
|---|---|---|---|---|---|
| Shopee | 5,012,235 | 812,947.25 | 1,501,665.61 | 9,081 | ลูกค้าใหม่ 5,761, เก่า 2,110, cancel 453, cancel% 4.99 |
| TikTok | 1,803,127.22 | 444,157.36 | 519,171.93 | 9,248 | ลูกค้าใหม่ 7,515, เก่า 908, cancel order 663 |
| Lazada | 85,766.88 | 7,210 | 15,147.36 | — | coupon 2,880, cost% 29.43 |

### ตรวจสอบไฟล์ (WIBWUB_Dashboard.html / WIBWUB_Mobile.html)

- M5 array: ครบ 7 เดือน (ม.ค.–ก.ค.) ✅
- ตรวจ index 6 (ก.ค.) ของทุก array ที่เกี่ยวกับ Shopee/TikTok/Lazada ในทั้ง 2 ไฟล์ — **พบว่าไฟล์ถูกอัปเดตด้วยข้อมูลชุดนี้แล้ว** (ตรงกับข้อมูลชีตสดทุกตัวเป๊ะ):
  SH_REV=5012235, SH_ORD=9081, SH_CANCEL_PCT=4.99, SH_ADS=812947, SH_FEE=1501665,
  TK_REV=1803127.22, TK_ADSSPEND=444157, TK_FEECOMM=519171,
  LZ_REV=85766, LZ_ADS=7210, LZ_FEE=15147, LZ_COUPON=2880, LZ_COST_PCT=29.43
- ตรวจ git: commit `c68f951 auto-update: sales from Sheets 2026-07-27 — SH/TK/LZ arrays` มีข้อมูลชุดนี้อยู่แล้ว, `git diff` ต่อ WIBWUB_Dashboard.html / WIBWUB_Mobile.html / sw.js = ว่างเปล่า, และ `HEAD == origin/main` — คือ push ไปแล้วเรียบร้อย

### Action taken

ไม่มีการเขียนไฟล์ dashboard, ไม่ bump sw.js, ไม่ commit ใหม่ (ไม่มีอะไรให้ commit) — ตามกฎ *"ข้อมูลเดือนนี้ไม่เปลี่ยนแปลงจากครั้งก่อน → log 'No new data' และ skip commit"* ข้อมูลถูกซิงค์ครบแล้วจากรอบก่อนหน้า (27 ก.ค.)
