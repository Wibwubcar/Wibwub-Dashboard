# WIBWUB Affiliate Auto-Update — 10 ก.ย. 2026 (รอบเย็น) — ❌ BLOCKED

## สรุป
รันไม่สำเร็จ **ไม่ใช่เพราะสคริปต์หรือ session หมดอายุ** แต่เพราะ **TikTok Affiliate Center ตอบ HTTP 503 ที่ endpoint ดาวน์โหลดไฟล์ export** ทำให้ไม่ได้ไฟล์ทั้ง 4 ตัว
**ไม่มีไฟล์ใดถูกแก้ไข** — dashboards ยังคงข้อมูลเดิม (ก.ย. 1–7) จากรอบเช้า และ **ไม่ต้อง push**

## สิ่งที่ทำสำเร็จ
- เชื่อม Chrome ที่ Mac (deviceId b75a6bb0…) ได้ปกติ ไม่ต้อง re-login
- เปิดหน้า Transaction Analysis และตั้ง date range **01/09/2026 – 08/09/2026** สำเร็จ
  (ข้อมูลอัปเดตล่าสุดของ TikTok คือ 8 ก.ย. 2026 0:00 GMT+7 — วันที่ 09 เป็นต้นไป greyed out)
- กดปุ่ม "ส่งออก" ครบทั้ง 4 tab: ครีเอเตอร์ / สินค้า / วิดีโอ / ไลฟ์สตรีม
- ระบบ TikTok สร้าง export task ครบและขึ้นสถานะ "ดาวน์โหลด" (พร้อมโหลด) ในแผง "รายงานที่ส่งออก"

## สิ่งที่ล้มเหลว
กดปุ่ม "ดาวน์โหลด" ในแผงรายงาน → ไม่มีไฟล์ลง ~/Downloads เลย
ตรวจ network พบว่า request ตอบ **503** ทุกครั้ง:

```
GET https://affiliate.tiktok.com/api/v1/oec/affiliate/compass/export_task/export
    ?shop_region=TH&oec_seller_id=7494549095358892612&task_id=…
→ 503 Service Unavailable
```

ทดสอบแล้วยืนยันว่าเป็นฝั่ง TikTok:
- ลองซ้ำ 6 ครั้ง ห่างกันรวมประมาณ 12 นาที → 503 ทุกครั้ง
- ลอง task_id ต่างกัน 2 ตัว (01M25QVPW5W9RAGM7SV0NF9KHJv2 และ 01M25QSJKTNH4ZRS5AQYTVNNR8v2) → 503 ทั้งคู่
- reload หน้าใหม่ทั้งหน้าแล้วลองใหม่ → ยัง 503
- ไม่มี dialog / popup / captcha ขึ้นมาขวาง และ session ยัง login อยู่ปกติ

## สถานะ Dashboard ปัจจุบัน (ไม่เปลี่ยนแปลง)
| Array | ค่าเดือน ก.ย. (index สุดท้าย) |
|---|---|
| AF_MO | "ก.ย. (1-7)" |
| AF_GMV | 453,788 |
| AF_NET | 445,305 |
| AF_COM | 51,120 |
| AF_CR | 350 |
| AFI_MONTHS | "กย.69 (1-7)" |
| AFI_GMV | 453,788 |

sw.js: **wibwub-v1073** (ไม่ได้ bump)

## STEP ที่ข้าม
- STEP 3 ย้ายไฟล์ — ไม่มีไฟล์ให้ย้าย
- STEP 4 ครีเอเตอร์ → AF_*/AFI_* — ข้าม
- STEP 5 สินค้า → PRODUCTS cr/vid — ข้าม
- STEP 5B วีดีโอ → VIDEOS array — ข้าม (VIDEOS array ไม่ถูกแตะต้อง ปลอดภัย)
- STEP 6 bump sw.js / push_now.command — ข้าม (ไม่มีอะไรเปลี่ยน จึงไม่ต้อง push)

## ข้อดีสำหรับรอบถัดไป
export task ทั้ง 4 ตัวของช่วง **01/09–08/09** ถูกสร้างไว้แล้วและอยู่ในแผง "รายงานที่ส่งออก"
TikTok เก็บให้ **7 วัน** → รอบหน้าถ้า endpoint กลับมาปกติ **ไม่ต้อง export ใหม่** กดดาวน์โหลดจากแผงได้เลย

## ที่ต้องทำ
รอ TikTok แก้ endpoint แล้วรัน schedule นี้ใหม่ หรือกดดาวน์โหลดเองจากแผง "รายงานที่ส่งออก"
