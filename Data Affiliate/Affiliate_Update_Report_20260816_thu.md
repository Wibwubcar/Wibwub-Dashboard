# WIBWUB Affiliate Auto-Update — 2026-08-16 (thursday run)

ช่วงข้อมูล: **1–14 ส.ค. 2026** (TikTok อัปเดตล่าสุดถึง 14 ส.ค. — วันที่ 15 ยังถูกล็อกอยู่)

## สรุปผล

📊 GMV: ฿746,906   Net: ฿729,931   Comm: ฿87,959
👥 Creators: 434
🎬 VIDEOS: อัปเดต 65 รายการ, เพิ่มใหม่ 104 รายการ (รวม 5,618)
⚙️ sw.js: v692 → v693
📌 ดับเบิ้ลคลิก push_now.command เพื่อ push ขึ้น GitHub

### เทียบกับรอบก่อน (1–13 ส.ค.)

| ตัวเลข | 1–13 ส.ค. | 1–14 ส.ค. | เปลี่ยน |
|---|---|---|---|
| GMV | 699,495 | 746,906 | +47,411 |
| Net | 683,618 | 729,931 | +46,313 |
| Commission | 82,404 | 87,959 | +5,555 |
| Creators | 409 | 434 | +25 |

## ไฟล์ที่ดาวน์โหลด (4 ไฟล์ ครบ)

- `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260801-20260814.xlsx` (5,839 แถว)
- `Data Affiliate/สินค้า/Transaction_Analysis_Product_List_20260801-20260814.xlsx` (74 แถว)
- `Data Affiliate/วีดีโอ/Transaction_Analysis_Video_List_20260801-20260814.xlsx`
- `Data Affiliate/ไลฟ์สตรีม/Transaction_Analysis_Live_List_20260801-20260814.xlsx`

ไฟล์ถูกย้ายเข้าโฟลเดอร์ย่อยโดย LaunchAgent `com.wibwub.download-mover` อัตโนมัติ (ไม่ได้ค้างใน Downloads)

## ที่แก้ในไฟล์

**WIBWUB_Affiliate_Dashboard.html**

- KPI strip: `409` → `434`, ป้าย `ส.ค. 1-13` → `ส.ค. 1-14`
- `AF_MO` index 7: `ส.ค. (1-13)` → `ส.ค. (1-14)` — **เขียนทับ index สุดท้าย ไม่ append** (เดือน ส.ค. มีอยู่แล้ว)
- `AF_GMV / AF_NET / AF_COM / AF_CR` index 7 อัปเดตตามตัวเลขข้างบน เดือนก่อนหน้าไม่ถูกแตะ
- `PRODUCTS` แก้เฉพาะ `cr` / `vid`:
  - Refresh Leather Wipes 37→33 / 34→30
  - Interior Wipes 22→21 / 21→21
  - Sugar 17→16 / 17→17
  - Cleaner 7→6 / 8→7
  - Interior 6→5 / 6→5
  - Refresh 0/0 และ Visible 2/2 — ไม่เปลี่ยน (ไม่มีแถวตรงกันในไฟล์สินค้า)
- `VIDEOS` 5,514 → 5,618 รายการ

**WIBWUB_Mobile.html**

- KPI: `฿699K` → `฿747K`, `409 creators · สค.69 (1-13)` → `434 creators · สค.69 (1-14)`
- `AFI_MONTHS` index 9 → `สค.69 (1-14)`; `AFI_GMV / AFI_NET / AFI_COMM` index 9 อัปเดต

**sw.js** — `wibwub-v692` → `wibwub-v693`
**push_now.command** — เขียนใหม่ (add เฉพาะ Affiliate Dashboard + Mobile + sw.js)

## การตัดสินใจที่ทำเองระหว่างรัน (ควรรู้ไว้)

1. **คอลัมน์ไฟล์ครีเอเตอร์ในสคริปต์เดิมไม่ตรงกับไฟล์จริง** — ไฟล์มี header 2 แถว (แถว 0 ชื่อคอลัมน์, แถว 1 คำอธิบาย) ข้อมูลจึงเริ่มที่ `iloc[2:]` ไม่ใช่ `[1:]` และคอลัมน์จริงคือ col0=ชื่อครีเอเตอร์, col1=GMV, col4=การคืนเงิน, col21=ค่าคอมมิชชั่น (ของเดิมระบุ col2/col10 ซึ่งผิด) — ใช้ค่าที่อ่านจาก header จริง

2. **ตัวจับคอลัมน์สินค้าแบบ fuzzy ใช้ไม่ได้** — header สะกด `วิดีโอ` แต่สคริปต์ค้นหา `วีดีโอ` ทำให้ได้ vid=0 เงียบ ๆ จึงเลือกคอลัมน์ตรง ๆ: col19 = ครีเอเตอร์ที่มียอดขายเฉลี่ยรายวัน (→ cr), col13 = วิดีโอที่มียอดขายเฉลี่ยรายวัน (→ vid) ตรวจย้อนกับค่าเก่าใน HTML แล้วว่าตรงคอนเวนชันเดิม

3. **การจับคู่ชื่อสินค้าใช้ชื่ออังกฤษในวงเล็บแบบตรงตัว** — ก่อนหน้านี้เงื่อนไข `'cleaner' in name` ไปเข้า "Refresh Leather Cleaner" แทน "WIBWUB Cleaner" จึงเปลี่ยนมาแมตช์ชื่อในวงเล็บแบบเป๊ะ

4. **ไฟล์วีดีโอเป็น inlineStr XML** — openpyxl อ่านไม่ออก ใช้ zipfile + regex อ่าน sheet XML ตรง ๆ (คอลัมน์ A=title B=video_id C=post_date D=link E=creator F=product_id G=GMV)

5. **มีวีดีโอ 37 รายการที่ `product:'Unknown'`** — product_id ของรายการเหล่านี้ไม่เคยปรากฏใน VIDEOS เดิม จึงเดาชื่อสินค้าไม่ได้ ปล่อยเป็น Unknown ไว้ก่อน ไม่ได้เดามั่ว

6. **การเชื่อมเบราว์เซอร์** — batch `navigate` จากแท็บ `chrome://newtab/` ล้มเหลว ต้องยิง navigate เดี่ยว ๆ ก่อน; และ panel รายงานค้างที่ "กำลังส่งออก" ~3 นาทีโดยไม่รีเฟรชเอง ต้อง reload หน้าแล้วเปิด panel ใหม่ ทั้ง 4 ไฟล์จึงขึ้นปุ่มดาวน์โหลด

7. **WIBWUB_Mobile.html มีการแก้ค้างจากรอบก่อน** (`ALL_PRODUCTS`, `prod-mo-tabs`, `prod-sub`) ที่ไม่ได้เกิดจากรอบนี้ — `push_now.command` add ทั้งไฟล์ จึงจะถูก commit ไปด้วยตามพฤติกรรมเดิม

8. **การแก้ Dashboard ถูก commit ไปแล้ว** โดย commit `89027e4` (auto push ตอน 15:36) ก่อนที่รอบนี้จะจบ ตอนนี้เหลือ `sw.js` v693 ที่ยังไม่ commit — รัน push_now.command เพื่อ commit + push ทั้งหมด (ตอนนี้ local ahead origin/main อยู่ 1 commit)

## การตรวจสอบ

- `node eval` แปลง `VIDEOS` (5,618) และ `PRODUCTS` (7) ผ่าน ไม่มี syntax error
- git diff = 181 เพิ่ม / 77 ลบ จาก 9,239 บรรทัด (~2.8% — ต่ำกว่าเกณฑ์ abort 50% มาก)
- diff นอกเหนือจาก VIDEOS มีเฉพาะบรรทัด KPI, 5 บรรทัด PRODUCTS และ 5 บรรทัด `AF_*` ตามที่ตั้งใจ
- อ่านค่ากลับจากไฟล์จริงหลังแก้ ทั้ง `AF_*` และ `AFI_*` ตรงกันทุกตัว
