# WIBWUB Daily TikTok Followers — 21 ก.ย. 2026 (run 2)

## สรุป
**อัปเดตสำเร็จ** (แก้ไขทับข้อมูลที่ผิดพลาดจาก run แรกของวันนี้ด้วย)

## สิ่งที่เกิดขึ้น
1. ปุ่ม "ดาวน์โหลดข้อมูล" (XLSX และ CSV) บน TikTok Studio ล้มเหลวแบบเงียบอีกครั้ง — ลองซ้ำหลายรอบ (ทั้ง coordinate click และ ref-based click ผ่าน accessibility tree) dialog ปิดปกติทุกครั้งแต่ไม่มีไฟล์ `Followers_wibwubcar*` ใหม่ปรากฏใน Downloads เลย (ตรวจสอบละเอียดด้วย `os.scandir` เทียบ mtime) — ยืนยันปัญหาเดิมซ้ำเป็นวันที่ N แล้ว
2. **ความผิดพลาดที่เกิดขึ้นระหว่างทาง:** ก่อนพบวิธี insight API ได้ลอง fallback ไป scrape หน้าโปรไฟล์สาธารณะ (`tiktok.com/@wibwubcar`) แทน ได้ค่า `followerCount:29700` จาก `__UNIVERSAL_DATA_FOR_REHYDRATION__` แล้วอัปเดตไฟล์ทั้งหมดด้วยค่านี้ไปก่อน (commit `984ff4e`) — แต่ค่านี้เป็นตัวเลข "live" จากหน้าโปรไฟล์สาธารณะ ซึ่ง **ไม่ตรงกับ methodology เดิมที่ dashboard ใช้มาตลอด** (TikTok Studio insight API ที่มี sync lag ~1-2 วัน) ทำให้ series ไม่ต่อเนื่องและ mix แหล่งข้อมูลกัน
3. หลังจากนั้นพบว่ามี `Followers_Update_Report_20260921.md` จาก run ก่อนหน้าของวันนี้อยู่แล้ว ซึ่งใช้วิธี insight API (`/aweme/v2/data/insight/?...insigh_type:"follower_num_history"`) ได้สำเร็จ — จึงเรียก API เดิมซ้ำเพื่อดึงข้อมูลล่าสุด แล้ว **แก้ไข (amend) commit ให้ใช้ค่าที่ถูกต้องจาก insight API แทน** ค่าที่ scrape มาจากหน้าโปรไฟล์

## ข้อมูลจาก insight API (ล่าสุด)
เรียก `fetch("/aweme/v2/data/insight/?type_requests=[{insigh_type:'follower_num_history',days:60,end_days:1}]", {credentials:'include'})` บนหน้า TikTok Studio ที่ login อยู่ — ได้ array 60 วันย้อนหลัง คำนวณวันที่จาก `extra.now` (epoch) เทียบ Bangkok time:
- **19 ก.ย. 2026 = 29,661 followers** (ค่าล่าสุดที่ sync เสร็จ, status:0)
- **20 ก.ย. 2026 = pending** (status:2, ยังไม่ sync)
- ตรวจสอบย้อนหลังพบว่าค่าที่มีอยู่เดิมในไฟล์ (17 ก.ย.=29,594, 18 ก.ย.=29,614) ตรงกับค่าจาก API แบบไม่มี offset วันเลย — ข้อสังเกตเรื่อง "label offset 1 วัน" ในรายงานรอบก่อนน่าจะเป็นการวิเคราะห์ผิดพลาด ไม่ใช่บั๊กจริง

## ไฟล์ที่แก้ไข (ค่าสุดท้ายหลัง amend)
- `WIBWUB_Dashboard.html`:
  - KPI card "TikTok Followers": `29,363` → `29,661`, `↑ 2.37% จาก ส.ค. · ข้อมูล 12 ก.ย.` → `↑ 3.41% จาก ส.ค. · ข้อมูล 19 ก.ย.`
  - Chart.js `soc_follow` เดือนกันยายน (index 8): `29.614` → `29.661`
  - `FOL_DATA` เดือนกันยายน: เพิ่มวันที่ "19 ก.ย." (val 29,661) ต่อจาก "18 ก.ย." เดิม, end 29,614→29,661, net +930→+977 คน, pct 3.24%→3.41%
- `WIBWUB_Mobile.html`:
  - `TK_FOL` เดือนกันยายน (index 8): `29594` → `29661`
  - `.mks-val` "TK Followers": `29.6K` → `29.7K`, delta `+6.2K` → `+6.3K จาก ม.ค.` (ปัดทศนิยม 1 ตำแหน่งจาก 29,661 และ 29,661-23,404)
- `sw.js` → bump cache version `wibwub-v1196` → `wibwub-v1197`
- Bracket/brace sanity check ผ่าน (Python `{`/`}` และ `[`/`]` count เท่ากัน)
- Git commit `66d0124` (amended จาก `984ff4e`) — "auto-update: TikTok followers 2026-09-21 — 29,661 followers (19 ก.ย., via insight API — CSV/XLSX download still failing)"
- `push_now.command` → สร้าง/อัปเดตให้พร้อมกด push (ยังไม่ push — sandbox ติด proxy HTTP 403 ตามปกติ)

## ข้อเสนอแนะ
1. **ยืนยันซ้ำ**: ปัญหาการดาวน์โหลดไฟล์จาก TikTok Studio (XLSX/CSV) ล้มเหลวต่อเนื่องมาหลายวันแล้ว ควรอัปเดต SKILL ให้ข้ามขั้นตอนคลิกดาวน์โหลดไปเลย ใช้ insight API (`/aweme/v2/data/insight/`) เป็น default ตั้งแต่ต้น — เร็วกว่า เสถียรกว่า ไม่ต้องพึ่ง Downloads folder เลย
2. **ข้อควรระวัง**: อย่าใช้ตัวเลขจากหน้าโปรไฟล์สาธารณะ (`tiktok.com/@wibwubcar`, `followerCount` ใน `__UNIVERSAL_DATA_FOR_REHYDRATION__`) เป็นแหล่งข้อมูลสำหรับ dashboard เพราะเป็นคนละ methodology กับ insight API ที่ใช้มาตลอด (ไม่มี sync lag, อาจไม่ตรงกับซีรีส์ย้อนหลัง) — ใช้เฉพาะ insight API เท่านั้นเพื่อความต่อเนื่องของข้อมูล
3. TikTok insight API มี lag ปกติ ~1 วัน (วันนี้ 21 ก.ย. ข้อมูลล่าสุดที่ sync เสร็จคือ 19 ก.ย.) — ไม่ใช่บั๊ก
