# ✅ รายงานการอัปเดตข้อมูล Affiliate (WIBWUB) — 10 ส.ค. 2026 (scheduled: wibwub-thursday-affiliate)

## ช่วงวันที่ข้อมูล
1–8 สิงหาคม 2026 (GMT+7) — 8 ส.ค. คือวันล่าสุดที่ TikTok มีข้อมูลให้ export

## ไฟล์ที่ดาวน์โหลดและย้ายสำเร็จ
ทั้ง 4 ไฟล์ดาวน์โหลดสำเร็จ (หลังเจอ HTTP 503 ชั่วคราวจากปุ่ม "ดาวน์โหลด" 2-3 ครั้งแรก แต่ retry แล้วผ่าน) และถูก auto-move เข้าโฟลเดอร์ที่ถูกต้องแล้ว:
- `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260801-20260808.xlsx`
- `Data Affiliate/สินค้า/Transaction_Analysis_Product_List_20260801-20260808.xlsx`
- `Data Affiliate/วีดีโอ/Transaction_Analysis_Video_List_20260801-20260808.xlsx`
- `Data Affiliate/ไลฟ์สตรีม/Transaction_Analysis_Live_List_20260801-20260808.xlsx`

## สรุปตัวเลข (ครีเอเตอร์ — อัปเดตแล้ว)
- **GMV**: ฿425,770 (เดิม ฿371,392)
- **Net GMV** (GMV − การคืนเงิน): ฿417,097 (เดิม ฿364,238)
- **Commission**: ฿49,554 (เดิม ฿42,954)
- **ครีเอเตอร์ที่ active**: 293 ราย (เดิม 266 ราย)
- Label เปลี่ยนจาก "ส.ค. (1-7)" → "ส.ค. (1-8)" — overwrite ค่าเดิมของเดือน ส.ค. ตามกฎ rolling-window (label เดิมตรงกับเดือนปัจจุบัน จึงไม่ append รายการใหม่)
- อัปเดตทั้ง `WIBWUB_Affiliate_Dashboard.html` (AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR) และ `WIBWUB_Mobile.html` (AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM + การ์ด KPI หน้าแรก ฿371.5K→฿426K)

## PRODUCTS (cr/vid) — ⏭️ ข้าม ไม่อัปเดตรอบนี้
ตรวจสอบแล้วพบว่า logic การคำนวณ `cr`/`vid` ยังไม่ชัดเจน (สะสมข้ามสัปดาห์ vs รายช่วงวันที่) — ปัญหาเดียวกับที่ถูกบันทึกไว้แล้วในรายงานก่อนหน้า (1 ส.ค., 6 ส.ค.) จึง**ไม่แตะ** field นี้ต่อเนื่อง เพื่อไม่ให้ข้อมูลเพี้ยน ค่า cr/vid ปัจจุบันในไฟล์ยังคงเดิมทุกตัว

## VIDEOS array — ⏭️ ข้าม ไม่อัปเดตรอบนี้
เปิดไฟล์วิดีโอด้วย openpyxl ได้ปกติ (ไม่ติดปัญหา inlineStr รอบนี้) และ match ด้วย `vid_id` กับ array เดิมได้หลายรายการ (ผ่าน safety check ≠ 0) แต่ก่อน merge ได้สุ่มตรวจ 4 รายการเทียบ GMV ดิบจากไฟล์กับค่า `monthly.aug` ที่บันทึกไว้ในระบบ พบว่า **ตัวเลขไม่สอดคล้องกันอย่างมีนัยสำคัญ** (ค่าดิบสูงกว่าค่าที่บันทึกไว้ 2-5 เท่า ไม่มีอัตราส่วนคงที่ที่อธิบายได้) — ไม่มีสูตรแปลงที่มั่นใจได้ จึง**ไม่เขียนทับ** `VIDEOS` array ในรอบนี้ เพื่อป้องกันข้อมูลผิดพลาด **แนะนำให้ตรวจสอบด้วยตนเอง** ว่า TikTok เปลี่ยนวิธีคำนวณ GMV ต่อวิดีโอหรือไม่ (เช่น attribution window เปลี่ยน)

## sw.js
Bump cache version: `wibwub-v627` → **`wibwub-v628`**

## push_now.command
สร้าง/แก้ไขสคริปต์ที่ root ของโฟลเดอร์แล้ว (`push_now.command`) — แก้ให้ทำ `git add` + `git commit` + `git pull --no-edit` + `git push` ครบ (ของเดิมมีแค่ `git push` ลอยๆ ซึ่งจะไม่ push อะไรเลยเพราะยังไม่ได้ commit)

**⚠️ ยังไม่ได้ push ขึ้น GitHub — กรุณาดับเบิลคลิก `push_now.command` เพื่อ commit และ push การเปลี่ยนแปลงรอบนี้**

## ตรวจสอบความถูกต้อง
- คำนวณตัวเลข GMV/Net/Commission/ครีเอเตอร์ ด้วย pandas จากไฟล์ดิบโดยตรง (ไม่ได้อ่านจากหน้าเว็บ)
- Cross-check สูตรกับข้อมูลสัปดาห์ก่อน (ไฟล์ Aug 1-7): คำนวณได้ GMV=371,472 / Net=364,319 / Comm=43,076 / CR=266 เทียบกับค่าที่บันทึกไว้เดิมในระบบ (371,392/364,238/42,954/266) — ใกล้เคียงกันมาก (ต่างกัน <0.3%, CR ตรงเป๊ะ) ยืนยันว่าสูตรถูกต้อง
- ตรวจ JS syntax ผ่าน `node --check` ทั้ง `WIBWUB_Affiliate_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js` — ไม่มี error
- ตรวจ `git diff` แล้วว่ามีการเปลี่ยนแปลงเฉพาะ array ที่ตั้งใจแก้ (AF_*/AFI_*/sw.js) ไม่กระทบ PRODUCTS/VIDEOS หรือไฟล์อื่นที่ไม่เกี่ยวข้อง

---
*รายงานสร้างโดยระบบอัตโนมัติ (scheduled task: wibwub-thursday-affiliate)*
