# WIBWUB Weekly Update — ศุกร์ 3 ก.ค. 2569 (continuation run, บ่าย)

**สรุป: Chrome ไม่ได้เชื่อมต่อ → ไม่ export ข้อมูลใหม่ แต่พบและแก้บั๊กข้อมูลสูญหายใน Affiliate arrays (Mobile) ที่เกิดจาก commit ก่อนหน้าในวันนี้ → แก้แล้ว commit แล้ว (ยังไม่ push)**

## สถานะที่ตรวจพบตอนเริ่ม
- `list_connected_browsers` คืนค่าว่าง → Chrome ไม่พร้อม → **ข้าม STEP 1 (Shipnity) และ STEP 2 (Affiliate export)** ตามกฎ error handling ของ task
- ข้อมูล 1 ก.ค. ที่ export ไว้แล้วจากรอบเช้า (GMV ฿30,570 / Net ฿30,384 / Comm ฿3,812 / 61 creators) ยังใช้ได้ ไม่ต้อง export ซ้ำ

## 🐛 บั๊กที่พบ: ข้อมูลเดือน เม.ย.–พ.ค. หายจาก `WIBWUB_Mobile.html`
ตรวจ git history พบว่า commit `bd654c8` (15:00 น. วันนี้, ก่อนรอบนี้) แก้ `AFI_GMV/AFI_NET/AFI_COMM` จาก 8 ช่องเหลือ 7 ช่อง โดย**ลบข้อมูลเดือน เม.ย. และ พ.ค. ทิ้งไปเลย** (724,337 / 951,325 GMV) แทนที่ด้วยค่า มิ.ย.+ก.ค.1 วัน แต่ `AFI_MONTHS` (label) ไม่ได้ถูกแก้ ยังมี 8 ช่องเดิม → เกิด array length mismatch (8 label vs 7 data) และข้อมูล 2 เดือนหายจริง

**แก้ไขแล้ว:**
- คืนค่า เม.ย. (GMV 724,337 / NET 708,947 / COMM 69,235) และ พ.ค. (GMV 951,325 / NET 937,364 / COMM 105,035) กลับเข้า array
- เพิ่ม ก.ค. เป็น index ใหม่ (index 8) ตามที่ควรจะเป็น: GMV 30,570 / NET 30,384 / COMM 3,812 (ข้อมูล 1 ก.ค. วันเดียว)
- เพิ่ม label `'กค.69'` ต่อท้าย `AFI_MONTHS` ให้ครบ 9 ช่อง ตรงกับ data
- Bump `sw.js` wibwub-v311 → v312, commit `be92860`

## ⚠️ พบบั๊กเพิ่ม (ยังไม่แก้ — นอก scope ของ task นี้)
`WIBWUB_Dashboard.html` และ `WIBWUB_Mobile.html` มี `M5 = 7 เดือน` (ม.ค.–ก.ค., ถูกต้องตามวันที่ปัจจุบัน) **แต่** array ข้อมูลยอดขายแพลตฟอร์มยังไม่ครบตาม:
- `SH_REV`, `TK_REV`, `LZ_REV`, `SH_ORD` → มีแค่ **5 ช่อง** (ขาด มิ.ย.+ก.ค.)
- `FB_REV`, `LINE_REV`, `TOTAL_REV`, `TOTAL_ORD`, `TK_AFI`, `TK_NET` → มีแค่ **6 ช่อง** (ขาด ก.ค.)

ผลคือกราฟ/การ์ดยอดขายบางส่วนจะโชว์ `฿undefined`/`NaN` สำหรับเดือนที่ขาด — **นี่คือบั๊ก live อยู่ตอนนี้** ไม่ได้แก้ในรอบนี้เพราะ:
1. ต้องใช้ไฟล์ยอดขายแพลตฟอร์ม (Shopee/Lazada/TikTok/Line) ซึ่งไม่ได้อยู่ใน scope ของ task "จันทร์" นี้ (เป็นของ `update-wibwub` skill/task อื่น)
2. ไม่มีข้อมูลดิบพอจะเติมให้ถูกต้อง — เติมมั่วเสี่ยงข้อมูลผิด

**แนะนำ:** รัน task/skill ที่รับผิดชอบยอดขายแพลตฟอร์ม (Shopee/Lazada/TikTok/Line) เพื่อเติม 1-2 เดือนที่ขาดให้ `SH_REV`...`TK_NET` ครบตาม `M5`

## ยังไม่ push
Commit `be92860` พร้อม push แล้ว — รอ user กด `push_now.command` (มีอยู่แล้วในโฟลเดอร์ ไม่ต้องสร้างใหม่)

## ไฟล์ที่แก้
- `WIBWUB_Mobile.html` (AFI arrays)
- `sw.js` (v311→v312)
- Backup ก่อนแก้: `WIBWUB_Mobile.html.bak_20260703_continuation_fix`
