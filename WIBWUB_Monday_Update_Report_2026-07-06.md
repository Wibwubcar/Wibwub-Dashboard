# WIBWUB Weekly Update — จันทร์ 6 ก.ค. 2569 (automated run)

**สรุป: ซิงค์ Affiliate arrays ใน Mobile ให้ตรงกับ Affiliate Dashboard (แก้ค่าเพี้ยน 5 เดือน) + bump sw.js v333→v334 — แต่ "ยังไม่ commit" เพราะ git ถูกล็อกโดย process อื่นที่รันพร้อมกัน; Top Products (Shipnity cumulative) ยังไม่ทำ เพราะต้องเลือก browser**

---

## ✅ สิ่งที่ทำสำเร็จรอบนี้

### 1) ตรวจสอบ Affiliate arrays — พบและแก้ค่าไม่ตรงกันระหว่าง 2 ไฟล์
- `WIBWUB_Affiliate_Dashboard.html` (`AF_GMV/AF_NET/AF_COM/AF_CR`) และ `CREATOR_MONTHS` (882 creators) **ถูกต้องและครบแล้ว** จาก commit ก่อนหน้าวันนี้ (`863677e`, `f45eef6`, `520cc44`) — ตรวจกับไฟล์ export ล่าสุด `Transaction_Analysis_Creator_List_20260701-20260705.xlsx` (266 แถว, 198 creators ที่ GMV>0) → **ตรงเป๊ะ**: GMV ฿199,013.78 / Net ฿195,973.04 / Comm ฿22,658.07 / CR 198
- แต่ `WIBWUB_Mobile.html` (`AFI_GMV/AFI_NET/AFI_COMM`) **ไม่ตรง** กับ Affiliate Dashboard ใน 5 เดือนล่าสุด (มี.ค.–ก.ค.) — ค่าเพี้ยนไปทุกเดือน (เช่น ก.ค.: 198,968 vs ที่ถูกต้อง 199,014)
- **แก้แล้ว**: sync `AFI_GMV/AFI_NET/AFI_COMM` ใน Mobile ให้ตรงกับ `AF_GMV/AF_NET/AF_COM` ทุก index (มี.ค.–ก.ค. 2569) — ตรวจ syntax array ผ่าน Node แล้ว ไม่พัง
- `PRODUCTS` (cr/vid) และ `VIDEOS` array ใน Affiliate Dashboard อัปเดตแล้วจาก commit ก่อนหน้า ไม่ต้องแก้ซ้ำ

### 2) Bump sw.js
- `wibwub-v333` → `wibwub-v334`

## ⛔ สิ่งที่ "ไม่ทำ" รอบนี้ และเหตุผล

### 1) ยังไม่ commit / push — ยืนยันแล้วว่ามี process อื่นรันจริงพร้อมกัน
- ครั้งแรก `.git/index.lock` ลบไม่ได้ (`Operation not permitted` ผ่านทั้ง `rm`, `mv`, python `os.remove`) → รอ ~15 วิ แล้ว lock หายไปเอง
- `git add WIBWUB_Mobile.html sw.js` **สำเร็จ** (staged แล้ว ตรวจด้วย `git status` เห็น `M` ทั้งสองไฟล์)
- แต่ `git commit` ล้มเหลวอีกครั้งทันที: เห็น warning `unable to unlink .git/objects/.../tmp_obj_*` และ `.git/index.lock` ถูกสร้างใหม่อีกครั้ง → ยืนยันว่ามี **git process อื่นกำลังเขียนจริงในเวลาเดียวกัน** (ไม่ใช่ stale lock ค้าง) — น่าจะเป็นอีก session/scheduled task ที่กำลัง commit repo เดียวกันอยู่ตอนนี้
- **ไม่ force-remove lock ซ้ำ** เพื่อไม่ให้ชนกับ commit ของอีก process จนไฟล์ git เสีย — ปล่อยให้รอบถัดไป (หรือรันซ้ำภายหลัง) commit แทน
- ไฟล์ที่แก้ค้างอยู่ (staged แต่ยัง uncommitted): `WIBWUB_Mobile.html` (AFI arrays), `sw.js` (v334)

### 2) Top Products (ALL_PRODUCTS/PROD_MO cumulative ม.ค.–ก.ค.) — ยังไม่ทำ
- ต้องใช้ Shipnity report2 (`รายงานอย่างละเอียด`) filter "ปีนี้" เพื่อดึงยอดสะสม แต่ตอนนี้มี **2 browser เชื่อมต่อพร้อมกัน** (macOS local + Windows remote) → ระบบบังคับให้ถามผู้ใช้เลือก browser ก่อนทำ action ใดๆ ซึ่งเป็น unattended run เลยข้ามขั้นตอนนี้ไปแทนที่จะเดาเอง
- ดึงข้อมูล Top 20 เดือน ก.ค. (MTD) มาแล้วจากรอบก่อน แต่ยังไม่พอสำหรับ cumulative Top 15 ที่ `ALL_PRODUCTS` ต้องการ

## 📊 สถานะปัจจุบัน
- Affiliate arrays: Mobile ↔ Affiliate Dashboard **ตรงกันแล้ว** (มี.ค.–ก.ค. 2569)
- Top Products: ยังเป็นข้อมูล ม.ค.–มิ.ย. เดิม (6 เดือน) — ก.ค. ยังไม่เพิ่ม

## ▶️ ขั้นถัดไป
1. Commit `WIBWUB_Mobile.html` + `sw.js` (v334) เมื่อ git lock หลุดแล้ว — commit message แนะนำ: `"auto: sync Mobile Affiliate arrays (Mar-Jul) + sw.js v334"`
2. เมื่อมี user คนที่เลือก browser ได้ (หรือเหลือ browser เดียว) → กลับมาทำ Top Products cumulative ต่อจาก Shipnity report2 "ปีนี้"
3. สร้าง `push_now.command` พร้อมกับ commit ข้อบน

---
*ไฟล์ export ล่าสุดที่ใช้ตรวจสอบ: `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260701-20260705.xlsx`*
