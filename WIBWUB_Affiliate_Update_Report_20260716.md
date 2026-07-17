# WIBWUB Affiliate Auto-Update Report — 16 กรกฎาคม 2026 (Scheduled Task)

## สรุปสิ่งที่อัปเดต

### 1. Export ข้อมูลจาก TikTok Affiliate Center
- **ครีเอเตอร์**: ดาวน์โหลดสำเร็จ `Creator_List_20260701-20260715_20260716023923.xlsx` (ช่วง 1-15 ก.ค., 11,724 แถว, 24 คอลัมน์) ผ่านปุ่ม "ส่งออก" ระดับตาราง (ไม่ใช่ปุ่ม KPI บนสุดที่ให้ไฟล์ Core_Stats รูปแบบผิด) ไฟล์ถูก LaunchAgent ย้ายเข้า `Data Affiliate/ครีเอเตอร์/` อัตโนมัติ
- **สินค้า**: ⚠️ **พบปัญหาใหม่** — หน้า Product Analytics คืนค่า `503 Service Unavailable` จาก endpoint ดาวน์โหลดไฟล์ export ซ้ำๆ ทั้งจากไฟล์ export เดิมและ export ใหม่ที่สั่งซ้ำ (ยืนยันผ่าน network log 4 ครั้ง กับ export job คนละ ID) — เป็นปัญหาฝั่งเซิร์ฟเวอร์ TikTok ไม่ใช่ปัญหาไฟล์ค้าง จึงใช้ข้อมูลสำรองที่มีอยู่แล้วในโฟลเดอร์แทน: `ListProducts_2026-07-01-2026-07-14_ALLPlan_20260715025548.xlsx` (ช่วง 1-14 ก.ค., ข้อมูลเก่ากว่า 1 วัน)
- **วีดีโอ/ไลฟ์สตรีม**: ⚠️ **ยังหาไม่พบ** หน้า export ในเมนู TikTok ที่ปรับดีไซน์ใหม่ (เหมือนรอบที่แล้ว) — ไม่มีปุ่ม Video/Live List ในทั้ง Performance, Insights, Creator Outreach — ไฟล์ล่าสุดที่มียังคงเป็นของวันที่ 14 ก.ค. (`Data Affiliate/วีดีโอ/` และ `Data Affiliate/ไลฟ์สตรีม/`)

### 2. อัปเดตยอด Creator (AF_GMV/AF_NET/AF_COM/AF_CR) — ก.ค. (1-15)
Overwrite index ล่าสุด (เดือน ก.ค. เดิมอยู่แล้ว) ใน `WIBWUB_Affiliate_Dashboard.html` และ `WIBWUB_Mobile.html`:

| | เดิม (1-14) | ใหม่ (1-15) |
|---|---|---|
| GMV | 673,195 | 728,951 |
| NET | 656,656 | 685,454 |
| COM | 12,269 ⚠️(ค่าผิดตกค้างจากรอบก่อน) | 83,768 (แก้ไขแล้ว) |
| Creators | 402 | 435 |

ยอด commission ที่คำนวณได้ (83,768.33) ตรงกับตัวเลข KPI card บนหน้าเว็บสด — ยืนยันความถูกต้องแล้ว

### 3. แก้บั๊ก PRODUCTS array (cr/vid) ที่ถูก revert ผิดจากรอบเช้า
พบว่า commit `dc8e0d9` (09:02 เช้าวันนี้ — จาก task อื่น ไม่ใช่ task นี้) ได้เขียนทับค่า cr/vid ของสินค้า 7 ตัวใน `WIBWUB_Affiliate_Dashboard.html` กลับไปเป็นค่าเก่า/ผิดที่ต่ำกว่าความจริงมาก ตรวจสอบกับไฟล์ ListProducts (1-14 ก.ค.) แล้วพบว่าค่าที่ถูกต้องตรงกับค่าก่อนถูก revert เป๊ะ จึงแก้กลับ:

| สินค้า | cr ผิด→ถูก | vid ผิด→ถูก |
|---|---|---|
| Leather Wipes | 30→160 | 43→84 |
| Interior Wipes | 23→119 | 30→51 |
| Sugar | 13→65 | 42→74 |
| Cleaner | 8→37 | 7→11 |
| Interior | 5→30 | 24→43 |
| Refresh | 0→29 | 0→21 |
| Visible | 1→9 | 1→7 |

(field อื่น เช่น gmv/units/monthly/ret ไม่ถูกแตะ — นอกสโคป, และไม่พบ PRODUCTS array ใน WIBWUB_Mobile.html จึงไม่มีอะไรต้องแก้ที่นั่น)

### 4. Cache version + Git
- Bump `sw.js`: `wibwub-v389` → `wibwub-v390`
- พบ `push_now.command` ถูกย่อ (ขาด `git add -A` + `git commit`) **เป็นครั้งที่ 3 ติดต่อกันในรอบวันที่ต่างกัน** — คืนค่าให้ครบ add+commit+push อีกครั้ง (ปัญหานี้เกิดซ้ำบ่อยมาก ควรตรวจสอบต้นตอ)
- **รอบนี้ sandbox commit สำเร็จ** (`git add -A` + `git commit` ผ่านได้จริง แม้จะมี warning `.git/index.lock`/`.git/objects/*/tmp_obj_*` ไม่สามารถลบได้) → commit `a348f62 "WIBWUB affiliate auto-update 2026-07-16_0305"` ถูกสร้างในเครื่อง sandbox แล้ว
- **แต่ `git push` ยังทำไม่ได้จาก sandbox**: fail ด้วย `403 from proxy` (ข้อจำกัด network ของ sandbox ไม่ใช่ปัญหา repo) — **ยังต้องดับเบิลคลิก `push_now.command`** เพื่อ push ขึ้น GitHub จากเครื่องจริง (รอบนี้ script จะเจอว่า commit มีอยู่แล้วและจะ push ให้เลย ไม่ต้อง commit ซ้ำ)

### 5. Cleanup ไฟล์ใน Downloads
เปลี่ยนชื่อไฟล์ผิดรูปแบบ/ซ้ำที่เกิดจากการลองหลายรอบวันนี้ ให้ขึ้นต้นด้วย `_WRONG_FORMAT_ignore_` และ `_DUP_ignore_` เพื่อไม่ให้ปนกับไฟล์ที่ใช้งานจริง

## หมายเหตุ / ประเด็นที่ควรแจ้งทีม
1. **หน้า Product Analytics ของ TikTok Affiliate Center ใช้งานไม่ได้ชั่วคราว** (503 ที่ endpoint ดาวน์โหลดไฟล์ export) — ควรลองรันใหม่ในรอบถัดไป ถ้ายัง 503 อาจต้องแจ้ง TikTok Support
2. **วีดีโอ/ไลฟ์สตรีม export หายไปจาก TikTok UI ใหม่ต่อเนื่องเป็นวันที่ 2** — ควรพิจารณาหาวิธีอื่น (เช่น ติดต่อ TikTok support ถามตำแหน่งฟีเจอร์ใหม่) เพราะข้อมูลค้างที่ 14 ก.ค. มาหลายวันแล้ว
3. **`push_now.command` ถูกย่อซ้ำเป็นครั้งที่ 3** — น่าจะมีกระบวนการ/task อื่นเขียนทับไฟล์นี้โดยไม่ตั้งใจ ควรตรวจสอบ
4. **พบบั๊ก cross-task**: task อื่น (ไม่ใช่ affiliate) เขียนทับ PRODUCTS cr/vid ผิดพลาดตอนเช้า — เป็นสัญญาณว่าอาจมี task/skill อื่นที่แก้ไฟล์เดียวกันโดยไม่ได้ตั้งใจ ควรตรวจสอบขอบเขตของแต่ละ scheduled task ให้ชัดเจนขึ้น
