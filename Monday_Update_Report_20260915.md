# ✅ WIBWUB Weekly Update (wibwub-monday-update) — 15 ก.ย. 2569 (จันทร์) — สำเร็จบางส่วน

## สถานะ: STEP 0, 2, 4 สำเร็จ / STEP 1 (Shipnity) หยุด — Chrome download ไม่ลงดิสก์ / STEP 5 (commit) ค้าง — git lock

## สิ่งที่ทำสำเร็จ

- ✅ **Protection check (STEP 0)**: `M5` array ใน `WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html` มี 9 เดือน (ม.ค.–ก.ย.) ตรงกับเดือนปัจจุบัน — ไม่ต้องแก้ไข
- ✅ **STEP 2 — TikTok Affiliate Transaction Analysis**: session ยังไม่หมดอายุรอบนี้ (ต่างจากวันที่ 14 ก.ย.)
  แต่ URL ตรง `insights/transaction-analysis` ถูก redirect ไปหน้า "ผลการดำเนินงาน" ภาพรวมแทน (สินค้าถูกปรับโครงสร้างใหม่)
  → ใช้หน้าเก่า `affiliate.tiktok.com/data/creator-analysis` (ยังใช้งานได้ แม้จะแจ้งว่าใกล้ถูกเลิกใช้) แทน
  → ข้อมูลอัปเดตล่าสุดถึง 13 ก.ย. เท่านั้น (ปฏิทินล็อกวันหลังจากนั้น) จึงส่งออกช่วง 1–13 ก.ย. แทนที่จะเป็น 1–15 ก.ย.
  → ไฟล์ลงที่ `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260901-20260913.xlsx` (1.2MB, 14,517 ครีเอเตอร์)
  → หมายเหตุ: มีไฟล์ซ้ำอีก 3 ไฟล์ในโฟลเดอร์เดียวกันจากการกดดาวน์โหลดซ้ำระหว่างหาไฟล์ที่ถูกต้อง (ไม่ได้ลบเพราะนโยบายห้ามลบไฟล์ถาวร) — ลบเองได้ภายหลังหากต้องการ
- ✅ **STEP 4 — Affiliate arrays**: อัปเดต `AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR` (Affiliate Dashboard) และ
  `AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM` (Mobile) เป็น **ก.ย. (1-13)**: GMV ฿908,625 / Net ฿842,024 / Commission ฿101,829 / 568 ครีเอเตอร์
  → ตรวจสอบซ้ำเองด้วย Python (openpyxl) จากไฟล์ Creator_List ที่ดาวน์โหลดมาจริง: รวม GMV = 908,625.23, รวม commission = 101,829.35,
  จำนวนครีเอเตอร์ที่มี GMV>0 = 568 — **ตรงกันทุกตัวเลข**
  → หมายเหตุ: ตัวเลขเหล่านี้มีอยู่แล้วใน working tree ตอนที่ตรวจ (ยังไม่ commit) — ดูเหมือนมี automation รอบอื่นที่ทำงานคู่ขนานกันในช่วงเวลาเดียวกัน
  (พบ commit สดๆ จาก task อื่นหลายตัวระหว่างรอบนี้ เช่น TikTok followers, TikTok Ads, สต๊อก, คำขอสินค้า) — ตรวจสอบแล้วว่าตัวเลขถูกต้องจึงไม่แก้ซ้ำ

## สิ่งที่ถูกบล็อก

- ❌ **STEP 1 — Shipnity**: export ทั้งแบบแยกไฟล์ (20 หน้า) และไฟล์เดียว ล้วนแสดง "Download completed" ในหน้าเว็บ
  แต่ไฟล์จริงลงดิสก์แค่ **1 จาก ~20 หน้า** (`Data-Page-1_15-09-2026.xlsx`, 902KB) — ไฟล์ข้อมูลเต็มล่าสุดยังคงเป็น `Data_14-09-2026.xlsx` (17.3MB, 14 ก.ย.)
  → นี่คือปัญหา Chrome download ไม่ลงดิสก์แบบเดิม (ไม่ใช่ปัญหา login/session) — เกิดซ้ำ 2 ครั้งในรอบนี้ (split-mode และ single-file mode)
  → **STEP 3 (Top Products) จึงข้ามไปทั้งหมด** เพื่อไม่ให้ dashboard มีข้อมูลไม่ครบ
- ⚠️ **STEP 5 — git commit**: `sw.js` ถูก bump เป็น `wibwub-v1115` โดยรอบนี้ แต่ระหว่างรอ commit มี automation อื่นที่รันคู่ขนานกัน
  bump มันต่อเป็น `wibwub-v1116` ซ้ำ (repo นี้มีหลาย schedule เขียนพร้อมกันจริง — เห็น commit สดๆ จาก TikTok followers, TikTok Ads,
  Stock forecast, คำขอสินค้า ระหว่างรอบนี้) — ปล่อยไว้ตามนั้นเพราะเลขสูงกว่าถูกต้องกว่าอยู่แล้ว
  → `git add` ไฟล์ที่แก้ (`WIBWUB_Affiliate_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js`) สำเร็จและอยู่ใน staged index แล้ว
  → **แต่ `git commit` ล้มเหลวทุกครั้งติดต่อกัน (ลองรวมกว่า 120 ครั้ง ในช่วง ~2 นาที)** ด้วย error `.git/index.lock` ซ้ำๆ
  แม้จะเช็คก่อนทุกครั้งว่าไฟล์ lock หายไปแล้วก็ตาม — และเคยเจอ error ระดับลึกกว่านั้นด้วย เช่น
  `unable to unlink .git/objects/xx/tmp_obj_...: Operation not permitted` ซึ่งบ่งชี้ว่าปัญหาจริงๆ อาจไม่ใช่แค่ lock ค้างธรรมดา
  แต่เป็นความไม่เข้ากันระหว่าง git (ที่ต้องสร้าง/ลบไฟล์ temp บ่อยๆ) กับกลไก sync ของ Google Drive บนโฟลเดอร์นี้ที่มีหลาย
  automation เขียนพร้อมกันอย่างหนักช่วงเวลานี้ (มี commit อื่นสำเร็จ 5 ครั้งขึ้นไปในช่วงเวลาเดียวกัน แสดงว่า repo ใช้งานได้
  แต่ contention สูงมากจนรอบนี้ไม่ผ่านสักครั้ง)
  → **ไม่มีข้อมูลสูญหาย** — ไฟล์ยังอยู่ใน staged index ของ git พร้อม commit ทันทีที่ลองใหม่แล้วผ่าน (อาจแค่ต้องรอช่วงที่ automation อื่นเบาลง)

## ที่ต้องทำ (ต้องมีคนที่เครื่อง Mac)

1. **แก้ git lock ค้าง**: ดับเบิลคลิก `fix_git_locks.command` ในโฟลเดอร์ `claude/All` (มีอยู่แล้ว) หรือลบ `.git/index.lock` ด้วยตนเอง
   จากนั้นรัน `git commit -m "auto-update: Monday 2026-09-15 — TikTok Affiliate Creator List refresh (Sep 1-13)"` ในโฟลเดอร์ `claude/All`
   (ไฟล์ที่แก้ไขถูก stage ไว้แล้ว: `WIBWUB_Affiliate_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js`)
2. **ตรวจสอบ Chrome download settings บน Mac**: ปัญหา "Download completed แต่ไฟล์ไม่ลงดิสก์" เกิดกับ Shipnity 2 ครั้งติดกันในรอบนี้
   (เกิดปัญหาคล้ายกันมาแล้วก่อนหน้านี้ในสัปดาห์) — ตรวจว่า Chrome มี prompt "Save As" ค้างอยู่ หรือมีการบล็อก multiple downloads หรือไม่
3. หลังแก้ทั้งสองข้อแล้ว รัน schedule นี้ใหม่เพื่อดึง Shipnity ให้ครบ (15 ก.ย.) และอัปเดต Top Products
4. (ไม่เร่งด่วน) ลบไฟล์ Creator_List ที่ซ้ำ 3 ไฟล์ใน `Data Affiliate/ครีเอเตอร์/` (มี timestamp suffix ต่างกัน แต่เนื้อหาเหมือนกันหมด)
