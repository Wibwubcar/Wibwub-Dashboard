# รายงานอัปเดต Affiliate — 30 ส.ค. 2026 (อาทิตย์) — ❌ หยุดกลางคัน

## สรุป
รอบนี้ **ไม่ได้ดาวน์โหลดหรืออัปเดตอะไรเลย** เพราะ **TikTok session หมดอายุ (Re-login required)**
ไม่มีการแก้ไขไฟล์ dashboard, sw.js หรือ push_now.command ใด ๆ

## สิ่งที่เกิดขึ้น
1. เชื่อมต่อ Chrome บน Mac สำเร็จ (deviceId `b75a6bb0-5b78-4e44-92a8-75224f1ce4ee`, macOS, isLocal)
2. Navigate ไป `https://affiliate.tiktok.com/insights/transaction-analysis?shop_region=TH&shop_id=7494549095358892612`
   → ถูก redirect ไป `https://seller.tiktok.com/` (หน้าการตลาด US แบบไม่ล็อกอิน มีปุ่ม **Log in / Join now** มุมขวาบน)
3. ลองซ้ำอีกครั้ง — ผลเหมือนเดิม
4. ลองอีก entry point `https://affiliate.tiktok.com/connection/creator?shop_region=TH` — redirect เหมือนกัน

สรุปได้ว่า cookie/session ของ TikTok Affiliate Center หมดอายุแล้ว ไม่ใช่ปัญหาชั่วคราวของหน้าเดียว

## ทำไมถึงไม่ทำ STEP 3-6 ต่อ
- ไม่มีไฟล์ใหม่เข้ามาใน Downloads เลย (ไฟล์ล่าสุดที่เกี่ยวข้องคือของรอบ 29 ส.ค.)
- ไฟล์ใหม่ที่สุดในโฟลเดอร์งานยังเป็นชุด **1–27 ส.ค.** ซึ่ง**ถูกประมวลผลเข้า dashboard ครบแล้ว**ตั้งแต่รอบ 29 ส.ค. (commit `b64afa3`)
- รันซ้ำจะเป็น no-op แต่มีความเสี่ยงทำ array เพี้ยนโดยไม่จำเป็น จึงข้ามทั้งหมด

## สถานะปัจจุบันของ dashboard (ตรวจแล้ว — ไม่ได้แตะ)
| รายการ | ค่า |
|---|---|
| `AFI_MONTHS` ตัวสุดท้าย | `สค.69 (1-27)` |
| ข้อมูล Affiliate ล่าสุดใน dashboard | 1–27 ส.ค. 2026 |
| `sw.js` | `wibwub-v892` |
| Affiliate commit ล่าสุด | `b64afa3` (29 ส.ค. รอบ 2) — push แล้ว |

`git status` มีของค้างอยู่ แต่**ไม่เกี่ยวกับงาน Affiliate**:
- `M push_now.command`, `M scripts/auto_push.log` — จากงาน stock/sales รอบเช้า
- `?? WIBWUB_Sales_Update_Report_2026-08-30_0930.md`
- `?? data ยอดขาย plaform/Shopee/Order.all.order_creation_date.20260731_20260830.zip`

## ต้องทำเอง ⚠️
1. เปิด Chrome → ไป `https://affiliate.tiktok.com/insights/transaction-analysis?shop_region=TH&shop_id=7494549095358892612`
2. **ล็อกอิน TikTok Affiliate Center ใหม่** (ผมทำแทนไม่ได้ — ห้ามกรอกรหัสผ่านแทนผู้ใช้)
3. เมื่อล็อกอินแล้ว สั่งรัน schedule นี้ใหม่ หรือบอกผมให้รันซ้ำ

หลังล็อกอินแล้ว ข้อมูล Affiliate จะขาดหายไป 2–3 วัน (28–29 ส.ค.) ซึ่งรอบถัดไปจะเก็บย้อนหลังให้ครบเองอยู่แล้ว
เพราะ export ใช้ช่วง 1 ส.ค. ถึงวันล่าสุดเสมอ ไม่ใช่ราย incremental
