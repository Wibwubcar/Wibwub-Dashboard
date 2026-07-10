# WIBWUB Affiliate Auto-Update — 26 มิ.ย. 2026

**ช่วงข้อมูล:** 1–23 มิ.ย. 2026 (วันที่ 24 ในตารางยังว่าง จึงใช้ถึง 23 เป็นวันล่าสุด)
**สถานะ:** สำเร็จ (รันอัตโนมัติ ไม่มีผู้ใช้อยู่)

## ตัวเลขหลัก (Affiliate, 1–23 มิ.ย.)
| ตัวชี้วัด | ค่า |
|---|---|
| GMV | ฿436,626 |
| Net GMV | ฿429,316 |
| Commission | ฿54,274 |
| Creators | 308 |

## ไฟล์ที่ดาวน์โหลด & ย้ายเข้าโฟลเดอร์ (Data Affiliate)
- ครีเอเตอร์ → `Transaction_Analysis_Creator_List_20260601-20260623_260626.xlsx` (582 แถว)
- สินค้า → `Transaction_Analysis_Product_List_20260601-20260623.xlsx` (46 สินค้า)
- วีดีโอ → `Transaction_Analysis_Video_List_20260601-20260623_260626.xlsx`
- ไลฟ์สตรีม → `Transaction_Analysis_Live_List_20260601-20260623.xlsx`

## การแก้ไฟล์
**WIBWUB_Affiliate_Dashboard.html**
- AF_MO ป้ายเดือน มิ.ย. → "มิ.ย. (1-23)"
- AF_GMV/NET/COM/CR idx5 → 436626 / 429316 / 54274 / 308
- PRODUCTS cr/vid (เฉพาะ 2 ฟิลด์นี้ ไม่แตะ gmv/units/monthly/ret):
  Leather Wipes 7/7 · Interior Wipes 18/82 · Sugar 10/186 · Cleaner 8/53 · Interior 4/182 · Refresh 3/28 · Visible 2/12

**WIBWUB_Mobile.html**
- AFI_GMV/NET/COMM idx7 (มิย.69) → 436626 / 429316 / 54274
  (เดือนก่อนหน้าเป็น 0 อยู่แล้วตามโครงสร้างเดิม — ไม่มีข้อมูลหาย)

**sw.js** — cache `wibwub-v243` → `wibwub-v244`
**push_now.command** — อัปเดต commit message + git add 3 ไฟล์ (Affiliate, Mobile, sw.js)

## ขั้นตอนถัดไป (ต้องทำเอง)
ดับเบิลคลิก `push_now.command` เพื่อ commit + push ขึ้น GitHub (Wibwub-Dashboard) ให้เว็บ/แอปอัปเดต

## หมายเหตุ / การตัดสินใจอัตโนมัติ
- ใช้คอลัมน์ cr = "ครีเอเตอร์ที่มียอดขายเฉลี่ยรายวัน" (col9), vid = "วิดีโอ" (col13) ตรงกับ convention เดิม (ตรวจ Sugar/Interior/Cleaner/Visible ค่าเดิมตรงกัน)
- จับคู่สินค้าด้วยชื่อภาษาอังกฤษในวงเล็บแบบตรงตัว ทั้ง 7 รายการ
- ไม่แตะ KPI สะสมหลายเดือน (active creators 1,168 / ฿2,668K) เพราะคำนวณจาก export เดือนเดียวไม่ได้
- สำรองไฟล์ไว้แล้ว: `*.bak_20260626_025057`
- ไฟล์ต้นทางใน Downloads ลบไม่ได้ (ข้อจำกัด sandbox) — ไม่กระทบผลลัพธ์
