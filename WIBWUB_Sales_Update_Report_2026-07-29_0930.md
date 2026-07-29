# WIBWUB Sales Sheet Update — 2026-07-29 (จันทร์+พฤหัส 09:30)

## ผลลัพธ์: ไม่มีการเปลี่ยนแปลง (No new data — already up to date)

อ่าน Shopee / TikTok / Lazada sheets สดจาก Google Drive — แถวสะสมล่าสุดของทั้ง 3 sheet ยังคงเป็น **01-26/07/26** เหมือนการตรวจครั้งก่อนหน้า (2026-07-28)

### ข้อมูลที่อ่านได้ (เดือน ก.ค. 2026, index 6, สะสมถึง 26/07/26)

| แหล่ง | ยอดขาย | Ads spend | ค่าธรรมเนียม/คอมมิชชั่น | orders | อื่นๆ |
|---|---|---|---|---|---|
| Shopee | 5,012,235 | 812,947.25 | 1,501,665.61 | 9,081 | cancel 453 (4.99%) |
| TikTok | 1,803,127.22 | 444,157.36 | 519,171.93 | 9,248 | ลูกค้าใหม่ 7,515 / เก่า 908 |
| Lazada | 85,766.88 | 7,210 | 15,147.36 | — | coupon 2,880, cost% 29.43 |

### ตรวจสอบไฟล์ (WIBWUB_Dashboard.html / WIBWUB_Mobile.html)

- M5 array: ครบ 7 เดือน (ม.ค.–ก.ค.) ✅
- ค่า index 6 (ก.ค.) ของทุก array ในสโคปงานนี้ ตรงกับข้อมูลชีตสดทุกตัว:
  SH_REV=5012235, SH_ORD=9081, SH_CANCEL_PCT=4.99, SH_ADS=812947, SH_FEE=1501665,
  TK_REV=1803127.22, LZ_REV=85766, LZ_ADS=7210, LZ_FEE=15147, LZ_COUPON=2880, LZ_COST_PCT=29.43
- TOTAL_REV / TOTAL_ORD คำนวณจาก JS (sum ของ array ข้างต้น) — ไม่ใช่ hardcoded array ไม่ต้องแก้

### Action taken

ไม่มีการเขียนไฟล์ dashboard, ไม่ bump sw.js, ไม่ commit ใหม่ — ตามกฎ "ข้อมูลเดือนนี้ไม่เปลี่ยนแปลงจากครั้งก่อน → log 'No new data' และ skip commit"
