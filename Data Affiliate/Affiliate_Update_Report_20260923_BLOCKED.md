# WIBWUB Affiliate Auto-Update — 2026-09-23 (BLOCKED)

## สถานะ: ❌ ไม่สำเร็จ — TikTok export download endpoint ตอบ 503 ต่อเนื่องเป็นวันที่ 3 ติดต่อกัน

## สิ่งที่ทำสำเร็จ
- เลือก browser macOS (deviceId b75a6bb0-...) ถูกต้องตามกฎ ไม่ได้หลุดไป PC
- เปิดหน้า TikTok Affiliate Center → ผลการดำเนินงาน → รายละเอียด (Transaction Analysis) ได้ปกติ ล็อกอินอยู่
- ตั้งช่วงวันที่แบบกำหนดเอง: **01/09/2026 – 20/09/2026** (20/09 คือวันล่าสุดที่ระบบมีข้อมูลให้เลือก, 21-23/09 ถูก disable ในปฏิทิน)
- กด "ส่งออก" ครบทั้ง 4 tab สำเร็จ ระบบขึ้นสถานะสำเร็จในแผง "รายงานที่ส่งออก" (13 → เพิ่มรายการใหม่ทุก tab):
  - ครีเอเตอร์ (Transaction_Analysis_Creator_List) — export เสร็จ พร้อมดาวน์โหลด (ส่งออกเมื่อ 23 ก.ย. 09:01–09:05 AM)
  - สินค้า (Transaction_Analysis_Product_List) — export triggered สำเร็จ
  - วีดีโอ (Transaction_Analysis_Video_List) — export triggered สำเร็จ
  - ไลฟ์สตรีม (Transaction_Analysis_Live_List) — export triggered สำเร็จ

## จุดที่ติดขัด

กดปุ่ม "ดาวน์โหลด" สำหรับรายงานที่พร้อมแล้ว (แท็บครีเอเตอร์) — ระบบเรียก API:
```
GET /api/v1/oec/affiliate/compass/export_task/export?...task_id=...
```
และได้ **HTTP 503 (Service Unavailable) ทุกครั้ง** — ยืนยันด้วย network request log โดยตรง ทดลองแล้วดังนี้:
- task_id ใหม่ที่ export วันนี้ (`01M35ZVNNWV3E6PW2CSWV3729Gv2`) — **503 ซ้ำ 5 ครั้ง** ห่างกันด้วย wait 3-10 วินาที รวมถึงหลัง reload หน้าเว็บเต็มรูปแบบ 1 ครั้ง
- task_id เก่าจากเมื่อวาน 22 ก.ย. 11:57PM (`01M34Z42VDTKJCJ39Z6BQS4Z8Nv2`) — **503 เช่นกัน** → ยืนยันว่าปัญหาไม่ได้จำกัดแค่ task ใหม่ของวันนี้ แต่เป็น endpoint ดาวน์โหลดล่มทั้งระบบ (เหมือนรอบ 21-22 ก.ย.)
- ตรวจโฟลเดอร์ Downloads หลังทุกครั้งที่กด — **ไม่มีไฟล์ Transaction_Analysis_*.xlsx ใหม่เข้ามาเลย**

## สรุป

นี่คือปัญหาฝั่ง TikTok server เหมือนรอบ 2026-09-21 และ 2026-09-22 (endpoint ส่งไฟล์ export ล่ม/503) และเกิดซ้ำเป็น **วันที่ 3 ติดต่อกัน** ไม่ใช่ปัญหา login/session/สิทธิ์ เพราะ:
- หน้าเว็บโหลดและแสดงข้อมูลได้ปกติ (ยอด GMV, รายชื่อครีเอเตอร์/สินค้า/วีดีโอ/ไลฟ์ ขึ้นในตารางปกติ)
- ปุ่ม export กดได้ครบทั้ง 4 tab ระบบขึ้นสถานะสำเร็จ ("ดาวน์โหลด" พร้อมกด ไม่ใช่ "กำลังส่งออก")
- มีแค่ endpoint ดาวน์โหลดไฟล์ที่ export เสร็จแล้วเท่านั้นที่ 503 — ทั้งไฟล์ใหม่ (วันนี้) และไฟล์เก่า (เมื่อวาน)

## ผลกระทบ
- ไม่มีไฟล์ใหม่ให้ประมวลผล → **ไม่ได้แตะต้อง** WIBWUB_Affiliate_Dashboard.html และ WIBWUB_Mobile.html เลย (AF_GMV/AF_NET/AF_COM/AF_CR, AFI_GMV/AFI_NET/AFI_COMM, PRODUCTS cr/vid, VIDEOS array — ทั้งหมดคงค่าเดิมจากรอบก่อนหน้า ไม่มีการเขียนทับด้วยข้อมูลเก่า/ว่าง)
- ไม่ได้ bump sw.js (ยังเป็น wibwub-v1215) และไม่ได้สร้าง push_now.command เพราะไม่มีอะไรเปลี่ยนแปลง

## ⚠️ ควรยกระดับ — ปัญหาต่อเนื่อง 3 วันติด

นี่เป็นรอบที่ 3 ติดต่อกัน (21, 22, 23 ก.ย.) ที่ endpoint `export_task/export` ตอบ 503 คงที่ ทำให้ข้อมูล Affiliate Dashboard ค้างที่ช่วง 1–19 ก.ย. มาตั้งแต่รอบ 2026-09-19/20 โดยไม่มีการอัปเดตใหม่เลย

**แนะนำ:**
- ควรแจ้ง TikTok Shop Partner Support โดยตรงเรื่อง endpoint `export_task/export` ตอบ 503 ต่อเนื่อง 3 วัน แทนที่จะรอให้หายเอง
- ลองดาวน์โหลดด้วยมือผ่านเบราว์เซอร์ปกติ (ไม่ใช่ automation) เพื่อเช็คว่าปัญหาเกิดกับทุก session/ทุกบัญชี หรือเฉพาะ session นี้
- ถ้ายัง 503 ต่อเนื่องในรอบถัดไปอีก (วันที่ 4) ควรพิจารณาหาช่องทางอื่น (เช่น TikTok Seller Center API โดยตรง หรือติดต่อ TikTok ผ่านช่องทางอื่น) เพราะ Dashboard จะยิ่งค้างข้อมูลนานขึ้นเรื่อยๆ

---
*รันโดย scheduled task: wibwub-thursday-affiliate*
