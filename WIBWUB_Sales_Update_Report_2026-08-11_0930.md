# WIBWUB Sales Sheet Update — รายงานรอบ 2026-08-11 09:30

## สรุปผล
เพิ่มข้อมูลเดือน ส.ค. (index 7, ข้อมูลสะสมถึง 09/08/26) เข้า `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html` สำเร็จ — ครบทั้ง 3 platform (Shopee/TikTok/Lazada) ตาม CRITICAL PROTECTION rule (ทุก array อัปเดตพร้อมกันในรอบเดียว ไม่มี label ไม่ตรงกับข้อมูล)

## ข้อมูลที่ดึงจาก Sheets (แถวสุดท้ายของเดือน ส.ค., cumulative ถึง 09/08/26)
- **Shopee**: ยอดขาย ฿2,306,333 · 3,816 orders · ยกเลิก 6.29% · Ads ฿432,482.25 · ค่าธรรมเนียม ฿690,977.37 · ลูกค้าใหม่ 2,296 / เก่า 420
- **TikTok**: ยอดขาย ฿753,236.36 · Affiliate ฿371,472 · หลังหัก ฿364,318 · Ads(GMV) ฿702,364 · Ads Spend ฿183,806 · ค่าธรรมเนียม+คอม ฿226,430 · Affi% 48.37%
- **Lazada**: ยอดขาย ฿42,724.80 · Ads ฿4,290 · ค่าธรรมเนียม ฿7,546.13 · คูปอง ฿990 · Cost% 30.02%

หมายเหตุ: TikTok ไม่มีคอลัมน์ order/cancel/customer breakdown ในชีต, Lazada ยังไม่มี order/customer breakdown สำหรับ ส.ค. (คอลัมน์ G-K ว่าง) — ค่าที่ไม่มีแหล่งข้อมูล (TK_ORD, TK_CANCEL_PCT, TK_LIVE, TK_NEW/OLD, LZ_ORD, LZ_CANCEL_PCT, LZ_NEW/OLD) **carry-forward ค่าเดือน ก.ค.** เช่นเดียวกับ FB_REV/LINE_REV/WEB_REV/CARE_REV/MKT_REV/BEUK_REV/POS_REV ที่ไม่มีแหล่งข้อมูลในสโคปนี้อยู่แล้ว (ตามแนวทางเดิมของไฟล์)

## จุดที่แก้ไขเพิ่มเติมนอกเหนือจาก array append
1. **Date picker (STEP 3B)**: `MP_MONTH_BOUNDS`/`MONTH_LABELS_FULL`/`MONTH_LABELS_SHORT`/`rangeEnd` ใน Dashboard.html ขยายถึง ส.ค. (bound ถึง 2026-08-11); แก้ bound เดือน ก.ค. ที่ค้างเป็น `2026-07-27` (จากตอนยังไม่ครบเดือน) ให้ถูกต้องเป็น `2026-07-31`
2. **Highlight เดือนปัจจุบันในกราฟ**: พบ hardcode `i===6`/`idx===6` (ชี้ไปเดือน ก.ค.) กว่า 39 จุดในทั้งสองไฟล์ (สี highlight แท่งกราฟ, จุดกราฟเส้น, แถว `<tr class="hl">` ในตาราง) — แก้เป็น `i===7`/`idx===7` ทั้งหมดแล้ว (ไม่ทำแบบนี้จะทำให้กราฟยัง highlight เดือน ก.ค. แทนที่จะเป็น ส.ค.)
3. **Header/KPI text ที่เป็น hardcoded string** (ยืนยันแล้วว่าไม่ใช่ JS-computed จาก array — ต่างจาก `v-ov-*`/`v-sh-*`/`v-tk-*`/`v-lz-*` ที่เป็น JS-computed อยู่แล้วไม่ต้องแก้):
   - Dashboard.html: แทนที่ "ม.ค. – ก.ค. 2569" → "ม.ค. – ส.ค. 2569" ทั้ง 14 จุด (chart caption + mrange-label)
   - Mobile.html: `home-hero` (ยอดขายรวม, unique orders, AOV, Shopee/TikTok/Lazada breakdown) และ header date-range/`data-updated`, และ Sales-tab overview KPI card (`s-ov-kpi` template string) — คำนวณยอดรวม ม.ค.–ส.ค. ใหม่จาก array: รวม ฿59.8M (Shopee ฿37.8M / TikTok ฿10.5M / Lazada ฿980K), 124,156 unique orders, AOV ฿482
4. **พบ array ที่พลาดไปตอนแรก**: `CARE_REV`/`MKT_REV`/`BEUK_REV`/`POS_REV` ใน Dashboard.html (มีเฉพาะใน Dashboard.html และ Mobile.html แต่ตอน inventory ครั้งแรกจับได้แค่ฝั่ง Mobile) ยังค้างที่ 7 elements — แก้โดย carry-forward ค่า ก.ค. (0 ทั้งหมดยกเว้น CARE_REV=86982) เป็น commit แยกหลังตรวจ verify ครบทุก array = 8 elements

## Out of scope (ไม่แตะ — ไม่มีข้อมูลในสโคปนี้)
- Shipnity top-products section (Dashboard.html) — sourced จากไฟล์ export แยก ไม่ใช่ 3 sheets นี้ ปัจจุบันระบุ "ม.ค.–ส.ค. 2569" อยู่แล้ว (อัปเดตจากรอบอื่น)
- mks-grid (Affiliate GMV/ROAS/TikTok Clips/Followers) ใน Mobile.html home — ไม่มีแหล่งข้อมูลจาก 3 sheets นี้

## Verification
- ทุก array ที่เกี่ยวข้องกับ sales (40 arrays ใน Dashboard.html, 30 ใน Mobile.html) ยืนยันความยาว = 8 elements ผ่าน script ตรวจสอบ
- Array อื่นที่ไม่ใช่ month-indexed (config/permission/affiliate/product/follower — นอกสโคป) ไม่ถูกแตะต้อง
- ตรวจสอบ diff stat: Dashboard.html (174 lines), Mobile.html (104 lines), sw.js (2 lines) — ตรงตามที่คาด ไม่มีการเปลี่ยนแปลงนอกสโคป

## ไฟล์ที่แก้ไข / Git
- `WIBWUB_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js` (cache `wibwub-v633` → `wibwub-v634`)
- Commit 1: `b140394` — array append + i===6→7 fix
- Commit 2: `1e9a323` — CARE_REV/MKT_REV/BEUK_REV/POS_REV fix (พบทีหลัง)
- **ยังไม่ push** (sandbox push ไม่ได้เนื่องจากข้อจำกัด proxy) — กรุณา double-click `push_now.command` ในโฟลเดอร์ All เพื่อ push ขึ้น GitHub
- หมายเหตุ: พบ `.git/index.lock`/`HEAD.lock` ค้างหลายรอบระหว่าง commit (filesystem permission quirk ของ Google Drive mount ตามที่เคยพบในรอบก่อนหน้า — ใช้ rename ได้ปกติ ไม่กระทบข้อมูล เพียงต้อง retry)

## แนะนำสำหรับรอบถัดไป
- ตรวจสอบว่า `CARE_REV`/`MKT_REV`/`BEUK_REV`/`POS_REV` ควรอยู่ใน official STEP2 array table ของ task instructions ด้วย (ปัจจุบันไม่ได้ระบุไว้ ทำให้พลาดในรอบนี้จนต้องแก้เพิ่ม)
- ทุกครั้งที่เพิ่มเดือนใหม่ ต้องเช็ค hardcode `i===N`/`idx===N` (current-month highlight) คู่กับ `rangeEnd`/`MP_MONTH_BOUNDS` เสมอ — ควรเพิ่มเป็น checklist item ถาวรใน task instructions
