# WIBWUB Daily TikTok Followers — 21 ก.ย. 2026

## สรุป
**อัปเดตสำเร็จ**

ปุ่ม "ดาวน์โหลดข้อมูล" (ทั้ง XLSX และ CSV) บน TikTok Studio ล้มเหลวแบบเงียบอีกครั้ง (dialog ปิดตามปกติ แต่ไม่มีไฟล์ปรากฏใน Downloads เลย แม้ลองซ้ำ 3 รอบ พร้อมยืนยันด้วย network log ว่ามีแค่ analytics/tracking request ไม่มี request ดาวน์โหลดไฟล์จริง) — จึงใช้วิธีดึงข้อมูลตรงจาก TikTok Studio insight API (`/aweme/v2/data/insight/` กับ `insigh_type:"follower_num_history"`) ผ่าน `javascript_tool` แทน (เป็น API เดียวกับที่หน้าเว็บใช้เรนเดอร์กราฟ ใช้ session cookie เดิม ไม่ต้องผ่าน download manager)

ข้อมูลล่าสุดที่ TikTok sync เสร็จคือ **19 กันยายน = 29,614 followers** (มี lag 2 วันตามปกติของ TikTok — ข้อมูลของ 20-21 ก.ย. ยังเป็น "pending" ในระบบ)

- `WIBWUB_Dashboard.html` → TikTok data array เดือนกันยายน (index 8) = `29.594` → `29.614` ✅
- `WIBWUB_Dashboard.html` → `FOL_DATA` เดือนกันยายน: เพิ่มวันที่ 18 ก.ย. (val 29,614), end 29,594→29,614, net +910→+930 คน, pct 3.17%→3.24% ✅
  - หมายเหตุ: label วันในไฟล์ (`FOL_DATA.days`) ที่ผ่านมามี offset ช้ากว่าวันที่จริง 1 วัน (ค่าที่ label ว่า "17 ก.ย." ตรงกับข้อมูลจริงของวันที่ 18 ก.ย. ตาม insight API) — รอบนี้คงรูปแบบเดิมไว้เพื่อความต่อเนื่องของอนุกรมข้อมูล (เพิ่ม label "18 ก.ย." ต่อจาก "17 ก.ย." เดิม, ค่า 29,614)
- `WIBWUB_Mobile.html` → TK Followers = 29.6K (ไม่เปลี่ยนจากรอบก่อน เพราะปัดเศษทศนิยม 1 ตำแหน่งเท่าเดิม), delta +6.2K จาก ม.ค. (คำนวณจาก end ม.ค. 23,404 เดิม) — ไม่มี diff
- `sw.js` → bump cache version `wibwub-v1187` → `wibwub-v1188` ✅
- `push_now.command` → สร้าง/อัปเดตให้พร้อมกด push ✅
- Git commit `1e76696` — "auto-update: TikTok followers 2026-09-21 — 29,614 followers (via insight API, CSV download unavailable)" (2 ไฟล์เปลี่ยน: WIBWUB_Dashboard.html, sw.js)
- ตรวจ JS syntax ของทั้งสองไฟล์ด้วย `node --check` ผ่านทั้งคู่ ✅

## รายละเอียดทางเทคนิค — ปัญหาการดาวน์โหลด CSV
คลิก "ดาวน์โหลดข้อมูล" → เลือก CSV → คลิก "ดาวน์โหลด" (ยืนยันด้วย ref-based click ผ่าน accessibility tree ไม่ใช่แค่ coordinate click) ทำซ้ำ 3 รอบ — dialog ปิดปกติทุกครั้งแต่ไม่มีไฟล์ `Followers_wibwubcar*` ใหม่ปรากฏใน Downloads (ตรวจสอบด้วย `find -newermt` เทียบ timestamp ละเอียด) ตรวจ network log ระหว่างคลิกพบแค่ `async_tasks/icon_info`, `mon.tiktokv.com` (tracking), `mssdk` (anti-bot) — ไม่มี request ที่คืนไฟล์จริง ⇒ สรุปว่าปัญหาเดิมซ้ำ (บันทึกไว้ในรายงานรอบก่อนๆ เช่นกัน)

**Workaround ที่ใช้ (รอบนี้ — เปลี่ยนวิธีจากรอบก่อน):**
แทนที่จะ hook `URL.createObjectURL` + parse ZIP ด้วยมือ ใช้วิธีเรียก insight API ตรง (`fetch` ด้วย `credentials:'include'` ในหน้า TikTok Studio ที่ login อยู่แล้ว) ดึง `follower_num_history` ย้อนหลังได้ถึง 265 วัน (ครอบคลุมตั้งแต่ ธ.ค. 2568 ถึงปัจจุบัน) เร็วและง่ายกว่าวิธี ZIP-parse มาก แนะนำให้ใช้เป็น default workflow ต่อไป:
```js
fetch("https://www.tiktok.com/aweme/v2/data/insight/?...&type_requests=[{\"insigh_type\":\"follower_num_history\",\"days\":60,\"end_days\":1}]", {credentials:'include'})
```

## ข้อเสนอแนะ
1. ปัญหาการดาวน์โหลดไฟล์จาก TikTok Studio ยังคงเกิดซ้ำทุกรอบติดต่อกันหลายวันแล้ว — ควรปรับ SKILL ให้ข้ามขั้นตอนคลิกปุ่มดาวน์โหลดไปเลย แล้วเรียก insight API ตรงตั้งแต่ต้น (เร็วกว่า, เสถียรกว่า, ไม่ต้องพึ่ง Downloads folder)
2. TikTok API มี data lag 2 วันเสมอ (วันนี้ 21 ก.ย. แต่ข้อมูลล่าสุดคือ 19 ก.ย.) — พฤติกรรมปกติ ไม่ใช่บั๊ก
3. สังเกตว่า `FOL_DATA.days` label ในไฟล์มี offset ช้ากว่าวันที่จริง 1 วันมาสักระยะ (ไม่ทราบจุดเริ่มต้นที่คลาดเคลื่อน) — ไม่กระทบความถูกต้องของยอดรวม/เทรนด์ แต่ถ้าต้องการแก้ให้ตรงปฏิทินจริง ควรรีเซ็ต baseline ใหม่ทั้งเดือนแทนการแก้ปลายทางอย่างเดียว (มีความเสี่ยงทำให้อนุกรมข้อมูลไม่ต่อเนื่อง)
