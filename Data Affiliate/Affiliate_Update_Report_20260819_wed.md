# รายงานอัปเดต Affiliate — พุธ 19 ส.ค. 2569

**ช่วงข้อมูล:** 1–17 ส.ค. 2569 (ปฏิทิน TikTok ปิดวันที่ 18–19 → เลือกได้ถึง 17)

## ไฟล์ที่ดาวน์โหลด (4/4 ครบ)
| Tab | ไฟล์ | ขนาด |
|---|---|---|
| ครีเอเตอร์ | Transaction_Analysis_Creator_List_20260801-20260817.xlsx | 524 KB |
| สินค้า | Transaction_Analysis_Product_List_20260801-20260817.xlsx | 19 KB |
| วีดีโอ | Transaction_Analysis_Video_List_20260801-20260817.xlsx | 1.13 MB |
| ไลฟ์สตรีม | Transaction_Analysis_Live_List_20260801-20260817.xlsx | 68 KB |

ทุกไฟล์ถูกย้ายเข้าโฟลเดอร์ย่อยของ `Data Affiliate/` เรียบร้อยโดย LaunchAgent อัตโนมัติ

## ตัวเลขที่อัปเดต (ส.ค. 1-17)
| ตัวชี้วัด | ส.ค. 1-17 | ก.ค. เต็มเดือน |
|---|---|---|
| Affiliate GMV | ฿902,978 | ฿1,452,748 |
| Net GMV (หลังคืนเงิน) | ฿884,466 | ฿1,428,498 |
| ค่าคอมมิชชั่น | ฿106,107 | ฿169,224 |
| ครีเอเตอร์ที่มียอด | 491 | 720 |
| ยอดคืนเงิน | ฿18,512 | — |

ข้อมูลจาก 6,322 แถว / 22 คอลัมน์ (ข้าม header 2 แถว)

## ไฟล์ที่แก้ไข
- `WIBWUB_Affiliate_Dashboard.html` — AF_MO / AF_GMV / AF_NET / AF_COM / AF_CR + KPI strip + PRODUCTS + VIDEOS
- `WIBWUB_Mobile.html` — AFI_MONTHS / AFI_GMV / AFI_NET / AFI_COMM + mks-grid
- `sw.js` — v730 → **v731**

## STEP 5B — VIDEOS array (ทำครบแล้ว)
- อ่านไฟล์วีดีโอ 5,620 แถว
- Parse entry เดิมได้ 5,878/5,878 รายการ (ครบ 100% — ผ่านเกณฑ์ความปลอดภัย)
- อัปเดตค่า `aug` ของวิดีโอเดิม: **90 รายการ**
- เพิ่มวิดีโอใหม่: **149 รายการ** → รวม **6,027 entries**
- GMV วิดีโอเดือน ส.ค.: ฿698,748 → **฿749,782**
- Verify ด้วย `node eval` ผ่าน ไม่มี error
- ✅ ไม่มี caption ตัวไหนยาวขึ้นเลย (0 รายการ) และไม่มี double-backslash — bug `esc()` ไม่กลับมาแล้ว (แก้โดยไม่ส่ง caption ที่ parse จาก HTML เดิมเข้า `esc()` ซ้ำ)

**Top 5 วิดีโอ ส.ค.**
1. papajate — Refresh Leather Wipes ฿68,941
2. noonjourneyyy — Refresh Leather Wipes ฿49,149
3. .namoshop125 — Sugar ฿44,380
4. .namoshop125 — Sugar ฿42,382
5. fahareejun — Refresh Leather Wipes ฿26,977

## STEP 5 — PRODUCTS
อัปเดตเฉพาะ `cr` / `vid` ตามกฎ (ไม่แตะ gmv/units/monthly/ret)
- WIBWUB Refresh Leather Wipes: cr 36, vid 33

## ⚠️ เรื่องที่ต้องรู้ / ต้องตัดสินใจ
1. **เปลี่ยน label จาก "1-18" เป็น "1-17"** — ค่าเดิมบน dashboard (GMV ฿959,972) มาจาก export คนละฟอร์แมต (24 คอลัมน์ `Creator_List`) ซึ่งนิยาม "การคืนเงิน" ต่างกันมาก (สูงกว่าประมาณ 2.9 เท่า) ทำให้ NET ไม่ต่อเนื่องกับเดือนก่อน ๆ รอบนี้ใช้ฟอร์แมตเดิม 22 คอลัมน์เพื่อให้เทียบกับ มิ.ย./ก.ค. ได้ ตัวเลขจึงต่ำลงแต่ **สอดคล้องกันทั้งชุด** และปรับ label เป็น 1-17 ให้ตรงข้อมูลจริง (ของเดิม label กับข้อมูลไม่ตรงกันอยู่แล้ว — Desktop เขียน 1-18 แต่ Mobile เขียน 1-16)
2. **`WIBWUB Refresh` ใน PRODUCTS ยังไม่ได้แก้** — SKILL.md ให้จับคู่ชื่อที่มี "Refresh" แต่ไม่มี "Leather" ซึ่งในไฟล์มีแค่ "WIBWUB Refresh Leather Cleaner" (cr 3 / vid 4) ส่วน dashboard ถือค่า 4/4 อยู่ เนื่องจากไม่ชัดว่าเป็นสินค้าตัวเดียวกัน **จึงเว้นไว้ ไม่แก้** — รอยืนยันการจับคู่
3. **ไฟล์ไลฟ์สตรีม** ดาวน์โหลดและเก็บเข้าโฟลเดอร์แล้ว แต่ SKILL.md ยังไม่มี step ประมวลผล — ยังไม่ถูกนำเข้า dashboard
4. **Reports panel ของ TikTok ไม่ refresh เอง** — ต้องกด reload หน้า (cmd+r) หลังรอ export ~2-3 นาที ปุ่มดาวน์โหลดถึงจะขึ้น (ปัญหาเดิมซ้ำทุกสัปดาห์)
5. **คอลัมน์ในไฟล์ครีเอเตอร์ต่างจากที่ SKILL.md ระบุ** — ของจริงคือ col 4 = การคืนเงิน, col 21 = ค่าคอมมิชชั่น (SKILL.md เขียน col 2 / col 10 ซึ่งผิด) ควรแก้ SKILL.md

## Git
Commit `17b19a7` เรียบร้อย (3 ไฟล์ +387 / -238)
**ยังไม่ push** — ต้องดับเบิลคลิก `push_now.command` เพื่อ push ขึ้น GitHub
