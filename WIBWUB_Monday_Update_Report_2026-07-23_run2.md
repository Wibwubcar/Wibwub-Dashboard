# WIBWUB Weekly Update — รันที่ 2 วันพฤหัสบดี 23 ก.ค. 2569 (รันอัตโนมัติ, wibwub-monday-update)

**สรุปสั้น**: พบว่างานหลักของ task นี้ (Top Products + Affiliate arrays + sw.js bump + commit) **ทำสำเร็จไปแล้วในรันก่อนหน้าของวันนี้** (commit `4485e49`, ดู `WIBWUB_Monday_Update_Report_2026-07-23.md`) จึงไม่ทำซ้ำ เพื่อลดความเสี่ยงชนกับบอทอื่นที่กำลังแก้ไฟล์เดียวกันอยู่ (พบการแก้ไข PRODUCTS/VIDEOS ใน Affiliate Dashboard ที่ยังไม่ commit จาก task อื่นระหว่างรันนี้) รันนี้จึงเน้นตรวจสอบสถานะและ export ข้อมูลสำรองเพิ่มเติมเท่านั้น

---

## ✅ สิ่งที่ทำในรันนี้

### 1. Re-export ข้อมูล Shipnity (เพิ่ม 1 วัน)
- Export ใหม่ผ่าน Chrome จนได้ `Data_23-07-2026.xlsx` (23.6MB) บันทึกอัตโนมัติลง `Data Shipnity/` (ครอบคลุมถึง 23 ก.ค. เทียบกับรันก่อนที่ใช้ข้อมูลถึง 22 ก.ค.)
- **ไม่ได้นำมารัน pipeline คำนวณ Top Products ใหม่** เพราะข้อมูลเพิ่มแค่ 1 วัน มูลค่าเพิ่มต่ำ และมีบอทอื่นกำลังแก้ไฟล์ dashboard เดียวกันอยู่พร้อมกัน (เสี่ยง race condition สูงกว่าประโยชน์ที่ได้)

### 2. พยายาม re-export TikTok Affiliate Creator List
- วินิจฉัยพบว่าปุ่ม "ดาวน์โหลด" บนรายการเก่าในหน้า export list ยิง request ไปที่ task_id เดิมที่เสีย (`01KY7HZTBK9GA6E87GC93FJA8Cv2`) แล้วได้ **HTTP 503** ทุกครั้ง ยืนยันด้วย network request inspection
- แก้โดยกดปุ่ม "ส่งออก" ใหม่ในตารางเพื่อสร้าง export task ใหม่จริง — task ใหม่ (รายการที่ 25) ขึ้นสถานะ "กำลังส่งออก" แต่ยัง**ไม่เสร็จหลังรอ 100+ วินาที**
- ไม่ block งานหลักเพราะตัวเลข Affiliate ของวันนี้ถูกอัปเดตจากไฟล์ export ที่สำเร็จแล้วในรันก่อนหน้า (Creator_List ถึง 22 ก.ค.)

### 3. ตรวจสอบสถานะ Git
- ยืนยันว่า commit `4485e49` (Monday update, ข้อมูล 1-22 ก.ค.) มีอยู่ใน local history จริง และยัง**ไม่ได้ push**
- พบว่า origin/main **diverged** จาก local ตั้งแต่ commit `afb1e47`: origin มี commit `6f0bb51` (ข้อความเดียวกันแต่ข้อมูลเป็นเวอร์ชันเก่ากว่า 1-21 ก.ค.) ส่วน local มี `4485e49` (ข้อมูลใหม่กว่า 1-22 ก.ค.) ตามด้วย commit อื่นอีก 3 ตัวจากบอทอื่น (`08b961f`, `e199d36`, `e841939`)
- Sandbox push ไม่ได้อยู่แล้ว (403 จาก proxy) — และครั้งนี้ **push ตรงๆ จะ fail เพราะ non-fast-forward** (ประวัติแยกสาขาจริง ไม่ใช่แค่ sandbox push ไม่ได้เฉยๆ เหมือนที่เข้าใจก่อนหน้า)
- `push_now.command` ปัจจุบันมีแค่ `git push` ธรรมดา — **จะ fail** ถ้ารันตอนนี้โดยไม่ pull/merge ก่อน

---

## ⛔ สิ่งที่ทำไม่ได้ / ต้องทำต่อ (สำคัญ)

1. **ต้อง pull/merge ก่อน push**: รัน `push_now.command` ตอนนี้จะ push ล้มเหลว เพราะ origin มี commit ที่ local ไม่มี (`6f0bb51`) ต้องเปิด Terminal บนเครื่องจริงแล้วรัน `git pull --rebase` (หรือ merge) ก่อน push เพื่อรวมประวัติทั้งสองสาย — แนะนำให้ตรวจ diff ของ `WIBWUB_Affiliate_Dashboard.html`/`WIBWUB_Mobile.html` ตอน merge ด้วยความระมัดระวัง เพราะ origin `6f0bb51` มีตัวเลข Affiliate เก่ากว่า (1-21) ในขณะที่ local `4485e49` ใหม่กว่า (1-22) — ต้องเลือกเก็บเวอร์ชันใหม่กว่า ไม่ใช่ auto-merge เฉยๆ
2. TikTok export ใหม่ (รายการ 25) ยังไม่เสร็จตอนจบรันนี้ — ยังไม่ได้ไฟล์มาเก็บใน `Data Affiliate/`
3. มีไฟล์ที่ยังไม่ commit จากบอทอื่น (`WIBWUB_Affiliate_Dashboard.html`, `WIBWUB_Mobile.html` มี PRODUCTS/VIDEOS ที่ต่างจาก HEAD) — ไม่ได้แตะต้องตามหลัก "ไม่ยุ่งงานนอกขอบเขตของ task นี้"

---

## 📊 สถานะปัจจุบัน
- ข้อมูล Top Products และ Affiliate arrays: อัปเดตล่าสุดถึง 1-22 ก.ค. (commit `4485e49`, ยังไม่ push)
- sw.js: v452 (ถูกบอทอื่น bump ต่อจาก v449 ไปแล้วหลายรอบ)
- Git: local (`e841939`) และ origin (`6f0bb51`) แยกสาขากันตั้งแต่ `afb1e47` — ต้อง merge ก่อน push

## ▶️ ขั้นถัดไป (แนะนำ)
1. เปิดเครื่องจริง รัน `git pull --rebase origin main` ใน repo แล้วแก้ conflict (ถ้ามี) โดยเลือกเก็บตัวเลข Affiliate เวอร์ชัน 1-22 ก.ค. (จาก local) ไม่ใช่ 1-21 (จาก origin) จากนั้นค่อยรัน `push_now.command`
2. ตรวจสอบว่า export TikTok รายการ 25 เสร็จหรือยัง แล้วดาวน์โหลดเก็บใน `Data Affiliate/` (ไม่จำเป็นเร่งด่วน เพราะข้อมูลหลักอัปเดตแล้ว)
3. พิจารณาจัด schedule บอทให้ไม่ทับเวลากัน — พบหลักฐานชัดเจนขึ้นว่ามีบอทอย่างน้อย 2 ตัว (Monday update + Affiliate/Products update) แก้ไฟล์เดียวกันพร้อมกันจนเกิด git divergence จริง ไม่ใช่แค่ index.lock ชั่วคราวแล้ว
