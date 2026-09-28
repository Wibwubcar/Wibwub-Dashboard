# WIBWUB Affiliate Auto-Update — 7 ก.ย. 2026 (รอบเย็น)

**สถานะ: สำเร็จครบทุก STEP** · ช่วงข้อมูล **1–5 ก.ย. 2026** (ขยายจากรอบก่อนที่ครอบคลุมถึง 4 ก.ย.)

## STEP 1–2 — ดึงข้อมูลจาก TikTok Affiliate Center
Session ใช้งานได้ปกติ (ไม่ต้อง re-login) วันล่าสุดที่เลือกได้คือ 5 ก.ย. 2026 ("อัปเดตเมื่อ: 5 ก.ย. 2026 0:00") ตั้งช่วงวันที่บน date picker ตัวที่สอง (แถบ "รายละเอียด") ซึ่งเป็นตัวที่ควบคุมการ export จริง แล้ว export ครบทั้ง 4 แท็บ

พบว่าแผงรายงานที่ส่งออกไม่รีเฟรชสถานะเอง ต้อง reload หน้าเว็บก่อนสถานะจึงเปลี่ยนจาก "กำลังส่งออก" เป็น "ดาวน์โหลด" — บันทึกไว้เป็นขั้นตอนมาตรฐานของรอบถัดไป

## STEP 3 — ย้ายไฟล์
LaunchAgent `com.wibwub.download-mover` ย้ายไฟล์ทั้ง 4 เข้าโฟลเดอร์ปลายทางอัตโนมัติแล้ว

| แท็บ | ไฟล์ | ขนาด |
|---|---|---|
| ครีเอเตอร์ | Transaction_Analysis_Creator_List_20260901-20260905.xlsx | 349,377 B |
| สินค้า | Transaction_Analysis_Product_List_20260901-20260905.xlsx | 19,064 B |
| วีดีโอ | Transaction_Analysis_Video_List_20260901-20260905.xlsx | 779,111 B |
| ไลฟ์สตรีม | Transaction_Analysis_Live_List_20260901-20260905.xlsx | 33,306 B |

## STEP 4 — ครีเอเตอร์ → AF_* / AFI_*

| ตัวชี้วัด | 1–4 ก.ย. (รอบก่อน) | 1–5 ก.ย. (รอบนี้) |
|---|---|---|
| GMV | 226,511 | **301,201** |
| Net GMV | 223,095 | **296,810** |
| Commission | 25,565 | **34,008** |
| Creators | 214 | **268** |

ใช้กฎ label-based: label เดิมของ index สุดท้ายคือ "ก.ย. (1-4)" ซึ่งเป็นเดือนเดียวกัน จึง **เขียนทับ index สุดท้าย** (ไม่ append) — เดือนก่อนหน้าไม่ถูกแตะต้อง ตัวเลขตรงกับ KPI บนหน้าจอ (฿301,200.97 / คืนเงิน ฿4,391.47)

อัปเดต label และข้อความ KPI ทั้งหมดจาก "ก.ย. 1-4" → "ก.ย. 1-5" ทั้งใน `WIBWUB_Affiliate_Dashboard.html` และ `WIBWUB_Mobile.html` (การ์ด mks-grid: ฿227K/214 creators → ฿301K/268 creators)

## STEP 5 — สินค้า → PRODUCTS (แก้เฉพาะ cr / vid)

| สินค้า | cr | vid |
|---|---|---|
| Refresh Leather Wipes | 47 | 90 |
| Interior Wipes | 24 | 53 |
| Sugar | 20 | 23 |
| Cleaner | 5 | 3 |
| Interior | 5 | 19 |
| Refresh | 3 | 8 |
| Visible | 1 | 7 |
| **รวม** | **105** | **203** |

`gmv`, `units`, `monthly`, `ret` ไม่ถูกแก้ไข

**หมายเหตุ/การตัดสินใจ:** KPI strip ของแท็บสินค้าในไฟล์ปัจจุบันคำนวณแบบ dynamic (`kk-prod-active`, `kk-prod-top-gmv` ฯลฯ มีค่าเริ่มต้นเป็น "–") ไม่มีข้อความ hardcode รูปแบบ "ผ่าน X,XXX creators" ตามที่ task file ระบุ จึงไม่มีอะไรต้องแก้ในส่วนนี้ — ค่าจะอัปเดตเองจาก PRODUCTS

Schema ของไฟล์ export ต่างจากที่ task file เขียนไว้ (มี 2 แถวหัวตาราง ต้องเริ่มอ่านข้อมูลแถวที่ 3 และ resolve คอลัมน์ด้วยชื่อหัวตารางภาษาไทยแทน index ตายตัว) ปรับสคริปต์แล้ว

## STEP 5B — วีดีโอ → VIDEOS

- อ่าน 3,911 แถวจาก inlineStr XML (zipfile + regex)
- entry เดิมที่ parse ได้: **7,912** (ผ่านเกณฑ์ความปลอดภัย — ไม่ใช่ 0 จึงเขียนทับได้)
- อัปเดตค่าเดือน `sep`: **123 รายการ**
- เพิ่ม entry ใหม่: **81 รายการ**
- **รวม 7,993 entries** · GMV เดือน ก.ย. จากวีดีโอรวม ฿243,278

## STEP 6 — Cache & push
`sw.js`: `wibwub-v1023` → **`wibwub-v1024`** · เขียน `push_now.command` ใหม่ให้ commit ไฟล์ affiliate/mobile/sw.js ของรอบนี้

## STEP 8 — ตรวจสอบ
`node` parse `VIDEOS` (7,993) และ `PRODUCTS` ได้สำเร็จ ไม่มี syntax error · `git diff --stat` ของ `WIBWUB_Affiliate_Dashboard.html` = 775 บรรทัด สอดคล้องกับ 123 update + 81 entry ใหม่ ไม่มีความผิดปกติ

**ค้างรอผู้ใช้:** ยังไม่ได้ push ขึ้น git — ดับเบิลคลิก `push_now.command` เพื่อ deploy
