# ✅ WIBWUB Affiliate Update — 9 ก.ย. 2026 (scheduled: wibwub-thursday-affiliate)

📅 **ช่วงข้อมูล:** 1/9/2026 – 7/9/2026
(7 ก.ย. คือวันล่าสุดที่ TikTok เปิดให้เลือก — 8–10 ก.ย. ยังเป็นสีเทา, หน้าเพจระบุ "อัปเดตเมื่อ: 7 ก.ย. 2026")

## 📁 ไฟล์ที่ย้ายแล้ว

| Tab | ปลายทาง | ขนาด |
|---|---|---|
| ครีเอเตอร์ | `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260901-20260907.xlsx` | 404,798 B |
| สินค้า | `Data Affiliate/สินค้า/Transaction_Analysis_Product_List_20260901-20260907.xlsx` | 19,264 B |
| วีดีโอ | `Data Affiliate/วีดีโอ/Transaction_Analysis_Video_List_20260901-20260907.xlsx` | 873,799 B |
| ไลฟ์สตรีม | `Data Affiliate/ไลฟ์สตรีม/Transaction_Analysis_Live_List_20260901-20260907.xlsx` | 41,774 B |

หมายเหตุ: LaunchAgent `com.wibwub.download-mover` ย้าย + เปลี่ยนชื่อไฟล์ให้อัตโนมัติภายใน ~5 วิ ทำให้ STEP 3 ไม่ต้อง `cp` เอง

## 📊 ตัวเลข ก.ย. 2026 (1–7)

- **GMV:** ฿453,876 (เดิม ฿376,196)
- **Net:** ฿445,389 (เดิม ฿369,183)
- **Commission:** ฿51,320 (เดิม ฿42,741)
- **👥 Creators:** 350 คน (เดิม 314)

ตรวจสอบตรงกับ KPI บนหน้าเว็บ TikTok (GMV ฿453,876 / 350 creators)

## 🛒 Products — อัปเดต `cr` / `vid` (6 จาก 7 รายการ)

| สินค้า | cr | vid |
|---|---|---|
| Refresh Leather Wipes | 48 → 184 | 105 → 146 |
| Interior wipes | 25 → 87 | 73 → 83 |
| Sugar | 21 → 82 | 25 → 37 |
| CLEANER | 5 → 16 | 3 → 7 |
| Interior | 5 → 22 | 22 → 31 |
| Visible | 1 → 3 | 7 → 8 |
| Refresh | 3 (ไม่เปลี่ยน) | 8 (ไม่เปลี่ยน) |

รวม cr = 397

## 🎬 VIDEOS

อัปเดต **113** รายการ, เพิ่มใหม่ **80** รายการ (รวม **8,162** รายการ)
GMV ก.ย. จาก VIDEOS รวม ฿367,864 — เป็นส่วนย่อยของ ฿453,876 ที่สมเหตุสมผล (ส่วนที่เหลือมาจาก LIVE / showcase)

## ⚙️ ไฟล์ที่แก้ไข

- `WIBWUB_Affiliate_Dashboard.html` — `AF_MO` / `AF_GMV` / `AF_NET` / `AF_COM` / `AF_CR` (index สุดท้าย = ก.ย., เขียนทับในตำแหน่งเดิม ไม่แตะเดือนก่อนหน้า) + ข้อความ KPI hardcode 5 จุด "1-6" → "1-7"
- `WIBWUB_Mobile.html` — `AFI_MONTHS` / `AFI_GMV` / `AFI_NET` / `AFI_COMM` + mks-grid บรรทัด 391
- `sw.js` — **v1058 → v1059**
- `push_now.command` — สร้างใหม่ + `chmod +x`

Backup: `.bak_20260909_thu_run` (ก่อน STEP 4), `.bak_videos_20260909_run` (ก่อน STEP 5B)
git diff: 338/13,146 บรรทัด (~2.6%) ใน Affiliate + 10 บรรทัดใน Mobile — ผ่านเกณฑ์ความปลอดภัย

## ⚠️ ข้อสังเกต / จุดที่ต่างจาก task file

1. **STEP 4 column index ใน task file ไม่ตรงกับไฟล์จริง** — ไฟล์ครีเอเตอร์มี 22 คอลัมน์และ header 2 แถว; ที่ถูกคือ col[1]=GMV, col[4]=การคืนเงิน, col[21]=ค่าคอมมิชชั่นโดยประมาณ, data เริ่ม `iloc[2:]` (task file ระบุ col[2]/col[10] และ `iloc[1:]`) → แก้โดยหาคอลัมน์จากชื่อ header แทนตำแหน่ง
2. **STEP 5 สะกดคำผิด** — task file ค้นหา `'วีดีโอ'` (วี) แต่ header ในไฟล์ export ใช้ `'วิดีโอ'` (วิ) จึงไม่มีทาง match → แก้โดยระบุคอลัมน์ตรง ๆ (col 19 = ครีเอเตอร์ที่มียอดขาย, col 9 = วิดีโอ)
3. **การ map ชื่อสินค้าต้องเป็นแบบ first-match-wins ตามลำดับในตาราง** — ถ้าใช้ exclusion rule จะทำให้ "WIBWUB Refresh Leather Cleaner" หลุด map (cr รวมจะเหลือ 379 แทน 397)
4. **VIDEOS 27 รายการมี `product:'Unknown'`** — เป็นวิดีโอใหม่ที่ product_id ยังไม่มีใน mapping
5. **Commission ในไฟล์ (฿51,320) ต่างจาก KPI บนหน้าเว็บเล็กน้อย (฿51,172.97)** — ใช้ไฟล์เป็น source of truth ตาม task file
6. Panel ส่งออกค้างที่ "กำลังส่งออก" — ต้อง reload หน้าแล้วเปิด panel ใหม่จึงเห็นปุ่มดาวน์โหลด (date range ยังคงอยู่หลัง reload)

## 📌 ขั้นตอนถัดไป

**ดับเบิ้ลคลิก `push_now.command` เพื่อ push ขึ้น GitHub** (scheduled task ไม่ได้รับอนุญาตให้ push เอง)
