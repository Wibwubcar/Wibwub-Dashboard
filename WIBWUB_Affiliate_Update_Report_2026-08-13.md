# ✅ รายงานการอัปเดตข้อมูล Affiliate (WIBWUB) — 13 ส.ค. 2026 (scheduled: wibwub-thursday-affiliate)

## ช่วงวันที่ข้อมูล
1–11 สิงหาคม 2026 (GMT+7)

## ไฟล์ที่ดาวน์โหลดและย้ายสำเร็จ
ทั้ง 4 ไฟล์ดาวน์โหลดสำเร็จและถูก auto-move เข้าโฟลเดอร์ที่ถูกต้องแล้ว:
- `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260801-20260811.xlsx` (451,837 bytes)
- `Data Affiliate/สินค้า/Transaction_Analysis_Product_List_20260801-20260811.xlsx` (18,946 bytes)
- `Data Affiliate/วีดีโอ/Transaction_Analysis_Video_List_20260801-20260811.xlsx` (929,537 bytes, 4,800 แถวมี vid_id)
- `Data Affiliate/ไลฟ์สตรีม/Transaction_Analysis_Live_List_20260801-20260811.xlsx` (48,693 bytes)

## ⚠️ พบและแก้ปัญหา schema drift (STEP 4 — ครีเอเตอร์)
ไฟล์ครีเอเตอร์รอบนี้มี **2 แถว header** (แถวชื่อ column + แถวคำอธิบายยาว) ไม่ใช่ 1 แถวตามที่ script เดิมสมมติ และตำแหน่งคอลัมน์จริงต่างจากที่ hardcode ไว้ในไฟล์งาน (col[2]=returns, col[10]=commission แบบเดิม → ที่จริงคือ col[4]=returns, col[21]=commission) ตรวจสอบจาก header row จริงแล้วแก้ไขให้ถูกต้อง ยืนยันผลด้วยการเทียบ delta กับค่าที่บันทึกไว้เดิม (สมเหตุสมผล ไม่กระโดดผิดปกติ)

## สรุปตัวเลข (ครีเอเตอร์ — อัปเดตแล้ว)
- **GMV**: ฿598,516 (เดิม ฿484,852)
- **Net GMV**: ฿585,077 (เดิม ฿474,423)
- **Commission**: ฿70,272 (เดิม ฿56,606)
- **ครีเอเตอร์ที่ active** (GMV>0): 376 ราย (เดิม 321 ราย)
- Label: "ส.ค. (1-9)" → **"ส.ค. (1-11)"** — overwrite ค่าเดิมของเดือน ส.ค. ตามกฎ rolling-window (label ตรงกับช่วงข้อมูลปัจจุบัน จึงไม่ append)
- อัปเดตทั้ง `WIBWUB_Affiliate_Dashboard.html` (AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR) และ `WIBWUB_Mobile.html` (AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM + KPI strip "฿599K · 376 creators")

## PRODUCTS (cr/vid) — ⏭️ ข้าม ไม่อัปเดตรอบนี้
ปัญหาเดิมยังคงอยู่ต่อเนื่อง (บันทึกตั้งแต่ 1, 6, 8, 10, 12 ส.ค.): คอลัมน์ "วิดีโอ"/"ไลฟ์สตรีม" ในไฟล์สินค้าเป็นตัวเลขเฉพาะช่วงวันที่ที่เลือกเท่านั้น ไม่ใช่สะสม ในขณะที่ `cr`/`vid` ใน PRODUCTS array เป็นตัวเลขสะสม — ไม่มีสูตรแปลงที่ชัดเจน จึงยังคง**ไม่แตะ** field นี้

## 🎬 VIDEOS array — ✅ อัปเดตสำเร็จ (ครั้งแรกที่ merge สำเร็จ หลังข้ามมา 2 รอบก่อนหน้า)
**ตรวจ raw-vs-stored GMV consistency ก่อนตัดสินใจ:** สุ่มเทียบ vid_id ที่มีทั้งใน raw data และใน VIDEOS array (1,953 รายการ overlap, 362 รายการมีค่า `monthly.aug > 0` ให้เทียบ) — median ratio = **1.00**, mean = **1.06**, 92.8% ของรายการอยู่ในช่วง ±20% ของ 1.0 ซึ่งดีขึ้นมากจากปัญหาที่บันทึกไว้ในรายงาน 12 ส.ค. (ratio 1.5x–10x ไม่คงที่) → สรุปว่าปัญหาการคำนวณ attribution ของ TikTok ได้รับการแก้ไข/เสถียรแล้ว จึง**ดำเนินการ merge ตาม STEP 5B**

ผลการ merge:
- Entry เดิมที่ parse ได้: 2,432 รายการ (entry_re match ผ่าน — ไม่ใช่ 0 จึงปลอดภัยที่จะเขียนทับ)
- อัปเดตค่าเดือนปัจจุบัน (aug): **68 รายการ** เปลี่ยนแปลง
- เพิ่มรายการใหม่: **2,847 รายการ** (วิดีโอที่ยังไม่เคยอยู่ใน array และมี GMV ในช่วงนี้ ≥ threshold ขั้นต่ำที่มีอยู่เดิม ซึ่งเท่ากับ 0 — เพราะ STEP 5B เพิ่งเริ่มใช้งานจริงได้ครั้งแรกเมื่อรอบนี้ หลังจากที่ก่อนหน้านี้ข้ามมาตลอดเนื่องจากปัญหา consistency ยอดเก่าที่คั่งค้างจึงถูกเติมเข้ามาในรอบเดียว)
- รวมทั้งหมดหลัง merge: **5,279 รายการ**
- Git diff: 2,921 insertions / 74 deletions จากทั้งไฟล์ 8,855 บรรทัด (~33%) — **ต่ำกว่าเกณฑ์ 50%** ที่กำหนดให้หยุด จึงดำเนินการต่อได้
- ตรวจ JS syntax ด้วย `node -e` eval บน VIDEOS array จริง — ไม่มี error, อ่านค่าได้ครบ 5,279 entries

## sw.js
Bump cache version: `wibwub-v656` → **`wibwub-v657`**

## push_now.command
พบปัญหาเดิมซ้ำอีกครั้ง (เป็น push-only ไม่มี add+commit) — แก้ให้ทำ `git add -A` + `git commit` + `git pull --no-edit` + `git push` ครบในคลิกเดียว เหมือนที่แก้ไว้ในรายงานก่อนหน้า

**⚠️ ยังไม่ได้ push ขึ้น GitHub — กรุณาดับเบิลคลิก `push_now.command` เพื่อ commit และ push การเปลี่ยนแปลงรอบนี้** (หมายเหตุ: `git status` พบไฟล์อื่นที่ถูกแก้จากกระบวนการอื่นด้วย เช่น stock zip files, auto_push.log และรายงาน .md จำนวนมากที่ยังไม่ commit — สคริปต์ใช้ `git add -A` จะ commit ไฟล์เหล่านั้นไปด้วย)

## ตรวจสอบความถูกต้อง
- คำนวณ GMV/Net/Commission/ครีเอเตอร์ ด้วย pandas จากไฟล์ดิบโดยตรง หลังแก้ column index ให้ถูกต้องตาม header row จริง
- ตรวจ VIDEOS ก่อนตัดสินใจ merge: เทียบ raw GMV vs stored `monthly.aug` แบบละเอียดข้าม 1,953 vid_id ที่ overlap ก่อนสรุปว่าปัญหา consistency เดิมคลี่คลายแล้ว
- ตรวจ entry_re match ได้ 2,432 > 0 (ปลอดภัยที่จะเขียนทับ), ตรวจ diff % ต่ำกว่า 50%, ตรวจ JS syntax ผ่าน node eval
- ตรวจ HTML files ด้วย grep ยืนยันค่า AF_*/AFI_* และ sw.js version ถูกบันทึกจริงในไฟล์ทั้งสอง
- ตรวจไฟล์ในทุกโฟลเดอร์ Data Affiliate ด้วย `ls -la` ยืนยัน 4 ไฟล์ใหม่ (20260801-20260811) ถูกย้ายเข้าครบ

---
*รายงานสร้างโดยระบบอัตโนมัติ (scheduled task: wibwub-thursday-affiliate)*
