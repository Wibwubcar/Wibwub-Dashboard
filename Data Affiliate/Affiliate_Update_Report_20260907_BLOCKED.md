# รายงานอัปเดต Affiliate — 7 ก.ย. 2026 (หยุดกลางทาง)

รันโดย scheduled task `wibwub-thursday-affiliate` (อัตโนมัติ)

## ❌ สถานะ: หยุดที่ STEP 1 — Re-login required

Chrome เชื่อมต่อได้ปกติ (Browser 1 / macOS / deviceId `b75a6bb0…`) แต่เมื่อ navigate ไปที่
`https://affiliate.tiktok.com/insights/transaction-analysis?shop_region=TH&shop_id=7494549095358892612`
ระบบ **redirect ออกไปหน้า marketing สาธารณะ `https://seller.tiktok.com/` (TikTok Shop US, มีปุ่ม "Log in" / "Join now")** ทั้งสองครั้งที่ลอง

แปลว่า **session TikTok Affiliate Center หมดอายุ / ถูก log out แล้ว** ไม่สามารถเข้าหน้า Transaction Analysis เพื่อ export ได้

ตามกฎใน SKILL.md ("Session expired → log 'Re-login required' และหยุด") จึงหยุดที่ STEP 1
และตามนโยบายความปลอดภัย ผมกรอกรหัสผ่าน/ล็อกอินแทนไม่ได้ — ต้องให้คุณล็อกอินเองก่อน

## สิ่งที่ต้องทำ

1. เปิด Chrome (เครื่อง Mac เดียวกัน) → ไปที่ https://affiliate.tiktok.com/ แล้วล็อกอินบัญชี WIBWUB
2. ยืนยันว่าเข้าหน้า "การวิเคราะห์ธุรกรรม" ได้และเห็นข้อมูลร้าน
3. สั่งรัน schedule นี้ใหม่ (หรือรอรอบถัดไป) — ทุก STEP จะทำงานต่อได้ตามปกติ

## ตรวจสอบสถานะข้อมูลปัจจุบัน (ยังปลอดภัย ไม่มีอะไรเสียหาย)

ไม่มีการแก้ไขไฟล์ใด ๆ ในรอบนี้ — ไม่ได้แตะ dashboard, ไม่ได้ bump sw.js, ไม่มี commit

ข้อมูลล่าสุดที่อยู่บนแดชบอร์ดตอนนี้ มาจากรอบวันที่ 6 ก.ย. (commit `380e95e`) ครอบคลุมถึง **1–3 ก.ย. 2026**

| Array | ค่าเดือน ก.ย. (index สุดท้าย) |
|---|---|
| `AF_MO` / `AFI_MONTHS` | "ก.ย. (1-3)" / "กย.69 (1-3)" |
| `AF_GMV` / `AFI_GMV` | 173,691 |
| `AF_NET` / `AFI_NET` | 171,874 |
| `AF_COM` / `AFI_COMM` | 19,536 |
| `AF_CR` | 178 |

ตรวจความสมบูรณ์แล้ว: `VIDEOS` array parse ผ่าน node ได้ปกติ **7,764 รายการ** ไม่มีความเสียหาย

ไฟล์ export ล่าสุดในโฟลเดอร์ (ครบทั้ง 4 tab) คือช่วง `20260901-20260903` ดาวน์โหลดเมื่อ 6 ก.ย. — ถูกประมวลผลเข้าแดชบอร์ดไปแล้วเรียบร้อย จึงไม่มีไฟล์ค้างที่ยังไม่ได้ใช้

**ช่องว่างข้อมูล:** ยังขาดวันที่ 4–6 ก.ย. (ต้อง export หลังล็อกอินใหม่)
