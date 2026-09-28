# WIBWUB Weekly Update — 2026-09-25 (ศุกร์ เช้า)

## สถานะรวม: ⏸️ ไม่มีการเปลี่ยนแปลงไฟล์ dashboard ใดๆ ในรอบนี้ (ทั้ง Shipnity และ Affiliate ไม่มีข้อมูลใหม่ที่ดึงได้สำเร็จ)

## ✅ Protection Check
- ตรวจ `const M5` ใน WIBWUB_Dashboard.html และ WIBWUB_Mobile.html: มี 9 เดือนแล้ว (ตรงกับเดือนปัจจุบัน = กันยายน) — ไม่ต้องแก้ไข

## ❌ STEP 1 — Shipnity Export ล้มเหลวทั้งหมด (บั๊กเดิมที่เคยเจอ 22 ก.ย. แต่รอบนี้หนักกว่าเดิม)
- ตั้งช่วงวันที่ 1-30 ก.ย. 2569 (เดือนนี้) ผ่านปุ่ม preset "เดือนนี้" สำเร็จ
- ลองโหมด **"ไฟล์เดียว"**: ระบบขึ้นแถบสถานะไล่ไปจนถึง 100% และขึ้นข้อความ "Download completed" (ใช้เวลา ~3 นาที) — **แต่ไม่มีไฟล์ Data_25-09-2026.xlsx ปรากฏใน Downloads เลย** แม้รออีก 10+ นาทีหลังจากนั้น
- ลองโหมด **"แยกไฟล์"** (rows/file = 1000 ซึ่งเป็นค่าสูงสุดที่ slider อนุญาต): ระบบสร้างไฟล์ Data-Page-1 ถึง Data-Page-11 ต่อเนื่องกัน แต่ละไฟล์ขึ้น "Download completed" ในหน้าเว็บ — **แต่ไม่มีไฟล์ Data-Page-*_25-09-2026.xlsx ไฟล์ใดปรากฏใน Downloads เลยแม้แต่ไฟล์เดียว** (ตรวจด้วย `find` ทั้งโฟลเดอร์ Downloads หลายรอบ)
- สังเกต: ไฟล์อื่นที่ระบบ/สคริปต์อัตโนมัติตัวอื่นดาวน์โหลดในช่วงเวลาใกล้เคียงกัน (เช่น tiktok_sku_daily_new, tiktok_product_daily_new เวลา 02:13-02:17 UTC) **สามารถลง Downloads ได้ตามปกติ** — แปลว่า Downloads folder / mount ใช้งานได้ปกติ ปัญหาจำกัดอยู่ที่การดาวน์โหลดจากหน้า Shipnity export โดยเฉพาะ
- ข้อสงสัย (ยังไม่ยืนยัน เพราะเครื่องมือที่มีไม่สามารถเห็น browser-level permission prompt ที่อยู่นอกเนื้อหาเพจได้): Chrome อาจ block การดาวน์โหลดจากโดเมน shipnity.com ไว้ (เช่น prompt "shipnity.com wants to download multiple files" ที่ต้องกด Allow ด้วยมือ) ซึ่ง automation ผ่านหน้าเว็บอย่างเดียวมองไม่เห็นและกดยืนยันเองไม่ได้
- **ยังไม่มีข้อมูล Shipnity เดือน ก.ย. (เต็มเดือน) ใหม่ — ต้องแก้ปัญหา download permission ก่อน แล้วรันใหม่ในรอบถัดไป**
- ยกเลิก export ที่ค้างอยู่แล้ว (กดปิด dialog)

## ⏭️ STEP 2 — Affiliate (Transaction Analysis): ไม่มีข้อมูลใหม่ (ไม่ใช่ error)
- เข้าหน้า TikTok Affiliate Center → ผลการดำเนินงาน ได้ปกติ ล็อกอินอยู่
- หน้า Performance แสดง "อัปเดตเมื่อ: 22 ก.ย. 2026" — ตรงกับผลตรวจของรอบเช้าวันนี้ (Affiliate_Update_Report_20260925_am.md) ที่พบว่า TikTok ยังไม่ปล่อยข้อมูลหลัง 22 ก.ย.
- ไฟล์ Transaction_Analysis_Creator_List_20260901-20260922.xlsx ที่มีอยู่แล้ว sync เข้า dashboard ครบแล้วตั้งแต่เมื่อวาน — **ไม่ได้ export ซ้ำ** เพราะจะได้ไฟล์ซ้ำโดยไม่มีข้อมูลใหม่

## ⏸️ STEP 3-5 — ข้าม (ไม่มีข้อมูลใหม่ให้ประมวลผล)
ไม่ได้แตะ WIBWUB_Mobile.html, WIBWUB_Dashboard.html, WIBWUB_Affiliate_Dashboard.html, sw.js — ไม่มีการเปลี่ยนแปลงใดๆ ไม่มีการ commit

## แนะนำสำหรับรอบถัดไป / สิ่งที่ต้องการความช่วยเหลือจากผู้ใช้
1. **ตรวจสอบ Chrome download permission สำหรับ shipnity.com บน Mac เครื่องนี้** — อาจต้องเข้า Settings → Privacy and security → Site settings → shipnity.com → Automatic downloads → Allow (หรือลองกด export ด้วยตัวเองสักครั้งเพื่อ trigger permission prompt แล้วกด Allow)
2. ลองรัน Shipnity export ใหม่หลังแก้ permission แล้ว
3. Affiliate: รอรอบบ่าย/เย็นตามคำแนะนำเดิม น่าจะเห็นข้อมูลถึง 23-24 ก.ย.

---
*รันโดย scheduled task: WIBWUB Weekly Update (วันจันทร์ prompt, รันจริงวันศุกร์ 25 ก.ย. 2569 09:16 ICT)*
