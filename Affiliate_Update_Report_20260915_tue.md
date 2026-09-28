# ✅ WIBWUB Affiliate Update — 15 ก.ย. 2026 (scheduled: wibwub-thursday-affiliate)

📅 **ช่วงข้อมูล:** 1/9/2026 – 13/9/2026 (ครีเอเตอร์/สินค้า) · 1/9/2026 – 12/9/2026 (วีดีโอ — ไฟล์ที่มีอยู่ครอบคลุมถึง 12 ก.ย. เท่านั้น)

## 📁 ไฟล์ที่ย้ายแล้ว (auto-mover)

| Tab | ปลายทาง | ขนาด |
|---|---|---|
| ครีเอเตอร์ | `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260901-20260913.xlsx` | 1,208,884 B (14,517 rows × 24 cols) |
| สินค้า | `Data Affiliate/สินค้า/Transaction_Analysis_Product_List_20260901-20260914.xlsx` | (72 rows × 12 cols) |
| วีดีโอ | `Data Affiliate/วีดีโอ/Transaction_Analysis_Video_List_20260901-20260912.xlsx` | 1,057,548 B (5,266 rows × 24 cols) |

หมายเหตุ: ต้องแก้ไข retry การ export ครีเอเตอร์ 2 รอบ — ดูหัวข้อ "ข้อสังเกต" ด้านล่าง

## 📊 ตัวเลข ก.ย. 2026 (1–13)

- **GMV:** ฿908,625 (เดิม ฿829,411 ที่ 1-12)
- **Net:** ฿842,024 (เดิม ฿817,577)
- **Commission:** ฿101,829 (เดิม ฿93,068)
- **👥 Creators (GMV>0):** 568 คน (เดิม 535 คน)

ตรวจสอบตรงกับไฟล์ Core_Stats (aggregate) แยกต่างหาก: GMV=908,625.23 / Commission=101,829.35 / Refund=66,601.69 — ตรงกันทุกจุด

## 🛒 Products — อัปเดต `vid` (6 จาก 7 รายการ, `cr` ข้ามเนื่องจากคอลัมน์ไม่มีในไฟล์ export ปัจจุบัน)

| สินค้า | vid (เดิม → ใหม่) |
|---|---|
| Refresh Leather Wipes | 170 → 203 |
| Interior wipes | 108 → 125 |
| Sugar | 86 → 102 |
| CLEANER | 13 → 14 |
| Interior | 45 → 50 |
| Refresh | 8 (ไม่เปลี่ยน) |
| Visible | 11 → 13 |

## 🎬 VIDEOS array

- **อัปเดต GMV เดือน ก.ย. ของวีดีโอเดิม:** 3,847 รายการ
- **เพิ่มวีดีโอใหม่:** 5 รายการ (อีก 58 รายการที่พบใหม่มี GMV เดือนนี้ = 0 จึงข้าม ไม่เพิ่มเข้า array)
- **รวมทั้งหมดหลังอัปเดต:** 8,513 รายการ (เดิม 8,508)
- GMV รวมจากไฟล์วีดีโอที่ map เข้าสินค้าได้: ฿547,705 จาก 3,910 แถว (เป็นส่วนหนึ่งของ GMV รวม ฿908,625 — ส่วนที่เหลือมาจากไลฟ์สตรีม/showcase/สินค้าที่ไม่ track เป็นรายตัว)

## ⚙️ ไฟล์ที่แก้ไข

- `WIBWUB_Affiliate_Dashboard.html` — `AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR` (index สุดท้าย ก.ย. 1-13), `PRODUCTS[].vid` ×6, `VIDEOS[]` (3,847 update + 5 เพิ่ม), หัวข้อ/แถบ KPI hardcode 6 จุด (hdr-badge, overview note, kstrip ×4) "1-12"/"1-11" → "1-13"
- `WIBWUB_Mobile.html` — `AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM` (เพิ่ม index ก.ย. 1-13), mks-grid บรรทัด 391
- `sw.js` — v1115 → v1116
- `push_now.command` — อัปเดตให้รวม `git add` + `git commit` ด้วย (ดูข้อสังเกต #4)

Backup: `/tmp/WIBWUB_Affiliate_Dashboard.html.bak_videos_20260915` (ก่อนแก้ VIDEOS array)
git diff (unstaged view): 199 บรรทัดใน Affiliate + 10 บรรทัดใน Mobile + 2 ใน sw.js — ตรวจสอบ JS syntax ผ่าน `node -e` ทุก array ที่แก้ (VIDEOS, PRODUCTS, AF_*, AFI_*) ไม่มี error, gmv/monthly-sum ตรงกันทุกแถว

## ⚠️ ข้อสังเกต / จุดที่ต่างจาก run ก่อนหน้า

1. **TikTok Affiliate Center อัปเกรดฟอร์แมต export ครีเอเตอร์แล้ว** — จาก 22 คอลัมน์/2-header-row (สัปดาห์ก่อน) เป็น 24 คอลัมน์/1-header-row ตอนนี้ ("อัปเกรดการวิเคราะห์แล้ว") ต้อง map คอลัมน์ใหม่ทั้งหมดโดยใช้ชื่อคอลัมน์แทนตำแหน่ง และ cross-validate กับไฟล์ Core_Stats เพื่อยืนยันความถูกต้อง (ตรงกันทุกจุด)
2. **Date range ไม่คงอยู่หลัง reload หน้า** (ต่างจากรายงานสัปดาห์ก่อนที่ระบุว่าคงอยู่) — หลัง reload ต้องตั้งช่วงวันที่ใหม่ทุกครั้งผ่าน "กำหนดเอง"
3. **ปุ่ม export ซ้อนกัน 2 จุด** บนหน้าครีเอเตอร์ — ปุ่มบนสุด (KPI) ให้ไฟล์ Core_Stats เล็กที่ผิด ปุ่มที่ถูกต้องอยู่เหนือตารางรายครีเอเตอร์ (ต้อง scroll ลง) ต้องใช้ 2 รอบกว่าจะได้ไฟล์ถูกต้อง แก้ไฟล์ปลายทางด้วย `cp -f` ทับเนื้อหา เนื่องจาก `rm` บนไฟล์ที่ mount จาก Google Drive ให้ error "Operation not permitted"
4. **`git commit` (ไม่ใช่แค่ `push`) ก็ทำจาก sandbox ไม่ได้เช่นกัน** ในรันนี้ — พบ `.git/index.lock` ค้างอยู่และลบไม่ได้ (permission บน Google Drive mount) จึงย้าย `git add` + `git commit` เข้าไปอยู่ใน `push_now.command` ด้วย (เดิมมีแค่ `git push`) ผู้ใช้ต้องรันสคริปต์นี้เพื่อทั้ง commit และ push
5. **รหัสสินค้า (product ID) ของสินค้า "Refresh Leather Wipes" และ "Refresh"** ไม่มีอยู่ในไฟล์ export สินค้าปัจจุบันเลย (ถูกถอดออกจากแคตตาล็อก/export) — แก้ปัญหาโดย derive product-ID → ชื่อสินค้า mapping จากข้อมูล VIDEOS array เดิมที่มีอยู่แล้ว (cross-reference vid_id เดิม กับ รหัสสินค้า ในไฟล์ใหม่) แทนการพึ่งพาไฟล์แคตตาล็อกสินค้าอย่างเดียว ทำให้ครอบคลุมสินค้าครบทั้ง 7 รายการ (ก่อนแก้ไขจะขาด 2 รายการนี้ไปเกือบ 1,200 แถว)
6. **แถวที่มีหลาย รหัสสินค้า คั่นด้วยคอมมา (วีดีโอโปรโมทหลายสินค้า) ถูกข้ามทั้งหมด** เพื่อความปลอดภัย ไม่สุ่มแบ่ง GMV ให้สินค้าใดสินค้าหนึ่ง (ประมาณ 1,355 แถวจาก 5,265 แถว)
7. **cr ของสินค้ายังคงข้ามเช่นเดิม** — คอลัมน์ "ครีเอเตอร์ที่มียอดขาย" ไม่มีในไฟล์ export สินค้ารูปแบบปัจจุบัน (ยืนยันซ้ำจากข้อสรุปสัปดาห์ก่อน)

## 📌 ขั้นตอนถัดไป

**ดับเบิ้ลคลิก `push_now.command` เพื่อ commit + push ขึ้น GitHub** (ทั้ง commit และ push ทำจาก sandbox ไม่ได้ในรันนี้ — scheduled task ไม่ได้รับอนุญาตให้ push อยู่แล้ว และ index.lock ทำให้ commit ก็ทำจาก sandbox ไม่ได้ด้วย)
