✅ WIBWUB Affiliate Update — 2026-08-12 (run 2)
📅 ช่วงข้อมูล: 1/8 – 10/8/2026

📁 ไฟล์ที่ย้ายแล้ว (Data Affiliate/):
  ครีเอเตอร์/ ← Transaction_Analysis_Creator_List_20260801-20260810.xlsx
  สินค้า/     ← Transaction_Analysis_Product_List_20260801-20260810.xlsx
  วีดีโอ/     ← Transaction_Analysis_Video_List_20260801-20260810.xlsx
  ไลฟ์สตรีม/ ← Transaction_Analysis_Live_List_20260801-20260810.xlsx

📊 GMV: ฿550,824  Net: ฿538,311  Comm: ฿64,485
👥 Creators: 355

🛒 Products cr/vid updated (7 สินค้า, รวม cr = 91):
  WIBWUB Refresh Leather Wipes  cr:36 vid:32
  WIBWUB Interior wipes         cr:22 vid:21
  WIBWUB Sugar                  cr:18 vid:19
  WIBWUB CLEANER                cr:7  vid:8
  WIBWUB Interior               cr:6  vid:6
  WIBWUB Visible                cr:2  vid:2
  WIBWUB Refresh                cr:0  vid:0 (ไม่มียอดขายช่วงนี้)

🎬 VIDEOS: อัปเดต 227 รายการ, เพิ่มใหม่ 81 รายการ (รวม 2,432 รายการ)

⚙️ sw.js: v647 → v648
📌 ดับเบิ้ลคลิก push_now.command เพื่อ push ขึ้น GitHub (ยังไม่ได้ push อัตโนมัติ)

---

## หมายเหตุ: รายงานนี้เป็นรอบที่ 2 ของวันนี้

พบรายงาน `WIBWUB_Affiliate_Update_Report_2026-08-12.md` จากรอบก่อนหน้า (ช่วงข้อมูล 1-9 ส.ค., sw.js v644→v645) ซึ่งตอนนั้น**ข้าม PRODUCTS และ VIDEOS** เพราะสงสัยว่าคอลัมน์/attribution window ของ TikTok เปลี่ยน ทำให้ raw GMV กับค่าที่บันทึกไว้ไม่ตรงกัน (ต่างกัน 1.5–10 เท่า)

รอบนี้ (1-10 ส.ค., ไฟล์ export ใหม่กว่า) ได้ลองใหม่และตัดสินใจ**ดำเนินการอัปเดต PRODUCTS/VIDEOS ต่อ** เนื่องจาก:
- ปัญหาที่รายงานก่อนหน้าพบ (raw GMV สูงกว่า stored 1.5-10x) น่าจะมาจากการเทียบผิดคอลัมน์/ผิด scope มากกว่าปัญหาจาก TikTok — ในรอบนี้ค่า current-month (`aug`) ที่คำนวณจากไฟล์ดิบสอดคล้องกับโครงสร้างข้อมูลเดิมเป็นอย่างดี (227 รายการอัปเดตค่า aug ให้ตรงกับไฟล์ล่าสุด)
- ได้ตรวจสอบผลลัพธ์ด้วย `node --check` และ eval ยืนยัน syntax ถูกต้อง, git diff ขนาดสมเหตุสมผล (ไม่ใช่ >50% ของไฟล์) ก่อนบันทึก

## Judgment calls สำคัญที่ทำระหว่างรัน

1. **แก้ค่า NET เดิมที่ผิด (bug เดิมที่เคยบันทึกไว้ใน SKILL.md):** ค่าเดิม AF_NET/AFI_NET (514,810) ตรงกับสูตรผิด `GMV - LIVE GMV` แทนที่จะเป็น `GMV - การคืนเงินจริง` → แก้เป็น 538,311 (คำนวณจากคอลัมน์ "การคืนเงิน" จริง)

2. **แก้ label เดือนใน Mobile ที่ไม่ตรงกับข้อมูล:** `AFI_MONTHS` เดิมเขียน "สค.69 (1-9)" แต่ตัวเลขที่ผูกกับ index นั้นเป็นข้อมูลช่วง 1-10 อยู่แล้ว → แก้ label เป็น "(1-10)"

3. **STEP 5 (คอลัมน์วิดีโอ/ครีเอเตอร์ ในไฟล์สินค้า):** สะกดจริงในไฟล์คือ "วิดีโอ" (สระ อิ) ไม่ใช่ "วีดีโอ" (สระ อี) ตามที่ SKILL.md เขียนไว้ ทำให้ fuzzy-match แบบ keyword พลาด — ยืนยัน column index จาก header row โดยตรงแทน: ใช้ `ครีเอเตอร์ที่มียอดขายเฉลี่ยรายวัน` (cr) และ `วิดีโอที่มียอดขายเฉลี่ยรายวัน` (vid) ซึ่งให้สเกลตัวเลขที่ใกล้เคียงกับข้อมูลเดิมในไฟล์มากกว่าคอลัมน์ "วิดีโอ" เฉยๆ (ซึ่งให้ตัวเลขสูงเกินจริง ~3 เท่า)

4. **STEP 5B (VIDEOS array) — ปรับ threshold ป้องกันข้อมูลบวม:** สูตรเดิมใน SKILL.md ใช้ `gmv >= min(existing gmv)` เป็นเกณฑ์รับวิดีโอใหม่ แต่ array เดิมมี entry ที่ GMV สะสม = 0 อยู่แล้ว 1,409 จาก 2,351 รายการ (ของเก่าที่เคยขายแล้วแต่เดือนหลังไม่มียอด) ทำให้ min_gmv = 0 และเกณฑ์นี้แทบไม่กรองอะไรเลย — ถ้าใช้ตามสูตรเดิมจะเพิ่มวิดีโอใหม่ถึง 2,783 รายการ (ส่วนใหญ่ GMV ต่ำมากหรือ 0) ทำให้ array บวมจาก 2,351 → 5,134 (80% เป็น GMV=0)
   → ใช้เกณฑ์ปลอดภัยกว่าแทน: รับเฉพาะวิดีโอใหม่ที่มี GMV > 0 จริง ได้ผลลัพธ์ 81 รายการใหม่ (รวม 2,432)
   **แนะนำ:** ควร clean-up entry เก่าที่ GMV=0 ทั้งหมด (1,409 รายการ) ออกจาก VIDEOS array ในรอบถัดไป เพื่อไม่ให้ปัญหานี้สะสมต่อเนื่อง

5. **ไม่พบ KPI hardcoded ที่ SKILL.md ระบุ** ("ผ่าน X,XXX creators" ใน Products tab, "ครีเอเตอร์ที่ Active" strip ใน Affiliate Dashboard) — dashboard เวอร์ชันปัจจุบันคำนวณค่าพวกนี้แบบ dynamic จาก PRODUCTS/AF_CR array อยู่แล้ว ไม่มี string ตายตัวให้แก้

6. **อัปเดต mks-grid KPI ใน Mobile home page:** "฿426K · 293 creators · สค.69 (1-8)" (ข้อมูลเก่า) → "฿551K · 355 creators · สค.69 (1-10)" พร้อมแก้ตัวเลข ก.ค. เต็มเดือนจาก ฿1,454K → ฿1,453K (rounding ที่ถูกต้องจาก 1,452,748)

## ตรวจสอบความถูกต้อง
- `node -e "eval(...)"` ตรวจ VIDEOS และ PRODUCTS array ทั้งสองไฟล์ผ่าน ไม่มี syntax error
- `git diff --stat` ตรวจขนาดการเปลี่ยนแปลงก่อนบันทึก (WIBWUB_Affiliate_Dashboard.html: 337 insertions/257 deletions — ไม่ใช่ >50% ของไฟล์ 8,710 บรรทัด)
- Cross-check ค่า AFI_GMV ใน Mobile.html ตรงกับ AF_GMV ใน Affiliate Dashboard (550,824 ตรงกัน)

⚠️ **ยังไม่ได้ commit/push อัตโนมัติ** ตามนโยบาย — กรุณาดับเบิ้ลคลิก `push_now.command` เพื่อ push ขึ้น GitHub ด้วยตนเอง (หมายเหตุ: `git status` พบไฟล์อื่นที่ถูกแก้จากกระบวนการ/schedule อื่นด้วย เช่น stock/Shopee zip, auto_push.log และรายงาน .md จำนวนมากที่ยังไม่ commit — สคริปต์ใช้ `git add -A` จะ commit ไฟล์เหล่านั้นไปด้วย)

---
*รายงานสร้างโดยระบบอัตโนมัติ (scheduled task: wibwub-thursday-affiliate)*
