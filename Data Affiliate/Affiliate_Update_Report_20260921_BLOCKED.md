# WIBWUB Affiliate Auto-Update — 2026-09-21 (BLOCKED)

## สถานะ: ❌ ไม่สำเร็จ — TikTok export download endpoint ตอบ 503 ต่อเนื่อง

## สิ่งที่ทำสำเร็จ
- เปิดหน้า TikTok Affiliate Center → Transaction Analysis ได้ปกติ (ล็อกอินอยู่)
- ตั้งช่วงวันที่แบบกำหนดเอง: 01/09/2026 – 19/09/2026 (19/09 คือวันล่าสุดที่ระบบมีข้อมูลให้เลือก, 20-21/09 ถูก disable)
- กด "ส่งออก" (Export) สำเร็จครบทั้ง 4 tab และระบบประมวลผลเสร็จ (ขึ้นเครื่องหมายถูกสีเขียวในรายการ "รายงานที่ส่งออก"):
  - ครีเอเตอร์ (Transaction_Analysis_Creator_List)
  - สินค้า (Transaction_Analysis_Product_List)
  - วีดีโอ (Transaction_Analysis_Video_List)
  - ไลฟ์สตรีม (Transaction_Analysis_Live_List)

## จุดที่ติดขัด
เมื่อกดปุ่ม "ดาวน์โหลด" สำหรับรายงานที่พร้อมแล้วทั้ง 4 ไฟล์ ระบบเรียก API:
```
GET /api/v1/oec/affiliate/compass/export_task/export?...task_id=...
```
และได้ **HTTP 503 (Service Unavailable) ทุกครั้ง** — ทดลองแล้วดังนี้:
- กดดาวน์โหลดซ้ำหลายรอบ ทั้ง 4 tab (รวม >10 ครั้ง)
- รอ 10-30 วินาทีระหว่างรอบ รวมเวลารอทั้งหมด >15 นาที
- Reload หน้าเว็บทั้งหน้าใหม่ทั้งหมด แล้วลองใหม่
- ลอง task_id ที่ต่างกัน (รายงานที่ export ใหม่จากรอบนี้) — ยัง 503 เหมือนเดิม

ตรวจสอบโฟลเดอร์ Downloads แล้ว — **ไม่มีไฟล์ .xlsx ใหม่เข้ามาเลย** ระหว่างรอบนี้ (ไฟล์ล่าสุดใน Downloads คือจากก่อนหน้า 14:39 ซึ่งเป็นคนละงาน)

สรุป: นี่คือปัญหาฝั่ง TikTok server (endpoint ส่งไฟล์ที่ export เสร็จแล้วล่ม) ไม่ใช่ปัญหาการ login/session/สิทธิ์ เพราะขั้นตอน export ทำงานได้ปกติ มีแค่ขั้นตอนดาวน์โหลดไฟล์ที่ export เสร็จแล้วเท่านั้นที่ล้มเหลว

## ผลกระทบ
- ไม่มีไฟล์ใหม่ให้ประมวลผล → **ไม่ได้แตะต้อง** WIBWUB_Affiliate_Dashboard.html และ WIBWUB_Mobile.html เลย (AF_GMV/AF_NET/AF_COM/AF_CR, AFI_GMV/AFI_NET/AFI_COMM, PRODUCTS cr/vid, VIDEOS array — ทั้งหมดคงค่าเดิมจากรอบก่อนหน้า ไม่มีการเขียนทับด้วยข้อมูลเก่า/ว่าง)
- ไม่ได้ bump sw.js และไม่ได้สร้าง push_now.command เพราะไม่มีอะไรเปลี่ยนแปลง

## แนะนำสำหรับรอบถัดไป
- ลองรันใหม่อีกครั้งในอีกสักพัก (อาจเป็น TikTok backend hiccup ชั่วคราว)
- ถ้ายัง 503 ต่อเนื่องหลายรอบติดกัน อาจต้องเข้าไปดาวน์โหลดด้วยมือผ่านเบราว์เซอร์ปกติ (ไม่ใช่ automation) เพื่อเช็คว่าปัญหาเกิดกับทุก session หรือเฉพาะ automation

---
*รันโดย scheduled task: wibwub-thursday-affiliate*
