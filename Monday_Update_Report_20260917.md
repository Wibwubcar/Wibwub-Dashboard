# WIBWUB Weekly Update — 17 ก.ย. 2569 (วันจันทร์, unattended run)

## สรุปผล
✅ เสร็จสมบูรณ์ทุก step — commit แล้ว รอ user กด `push_now.command` เพื่อ push ขึ้น GitHub

## STEP 1 — Shipnity export
- ไฟล์ใหม่: `Data_17-09-2026.xlsx` → คัดลอกเป็น `Data Shipnity/Data_กันยายน.xlsx`
- Aggregate ทั้งหมด 113 ไฟล์ (product-level 112, order-level skip 1: `Data_07-08-2026_export.xlsx`) — ไม่มี error

## STEP 2 — Affiliate export
- ไฟล์ใหม่: `Transaction_Analysis_Creator_List_20260901-20260914.xlsx`
- ⚠️ หมายเหตุ: ไฟล์ที่ export ได้ยัง cover ช่วง 1-14 ก.ย. เท่านั้น (เหมือนรอบที่แล้ว) ไม่ใช่ 1-17 — น่าจะเป็นเพราะ TikTok Affiliate settle ข้อมูลช้ากว่าปัจจุบันหลายวัน ตัวเลขที่ได้ใกล้เคียงของเดิมมาก (GMV ต่างกัน ~166 บาท) จึงถือว่าเป็นข้อมูลเดือนเดิมที่ครบขึ้นเล็กน้อย → overwrite ตาม rule ข้อ 3 ไม่ได้ append เดือนใหม่

## STEP 3 — Top Products (Shipnity)
อัปเดต `ALL_PRODUCTS` + `PROD_MO` ใน `WIBWUB_Mobile.html` และตาราง/KPI ใน `WIBWUB_Dashboard.html` เป็นข้อมูลสะสม ม.ค.–17 ก.ย. 2569

| # | สินค้า | ยอดขายใหม่ | จำนวน |
|---|---|---|---|
| 1 | Sugar สเปรย์แวกซ์เคลือบสีรถ | ฿6.44M | 20,888 |
| 2 | Wool Duster ไม้ปัดฝุ่นขนแกะ | ฿6.17M | 9,690 |
| 3 | Interior สเปรย์ทำความสะอาดภายในรถ | ฿4.60M | 13,245 |
| 4 | Refresh Wipes | ฿3.78M | 47,840 |
| 5 | Interior Wipe | ฿3.20M | 43,603 |
| 6 | Refresh สเปรย์โฟม | ฿2.74M | 7,617 |
| 7 | Spot Clean | ฿2.65M | 7,006 |
| 8 | Perfect ผ้าไมโครไฟเบอร์ | ฿2.09M | 13,602 |
| 9 | Reflex Ceramic Coating สเปรย์ | ฿1.85M | 4,775 |
| 10 | X-Glass Shield (ขยับขึ้นจาก #11) | ฿1.74M | 4,670 |
| 11 | Tire & Trim (ขยับลงจาก #10) | ฿1.73M | 3,782 |
| 12 | Martini | ฿1.64M | 12,999 |
| 13 | Sugar 3L | ฿1.62M | 1,354 |
| 14 | Quartz Shampoo 1L | ฿1.52M | 6,245 |
| 15 | Reflex Ceramic Coating 500ml | ฿1.43M | 2,204 |

ยอดขายรวม (ทุกสินค้า ไม่ใช่แค่ Top 15): ฿72.19M · 290K ชิ้น

⚠️ **ไม่ได้ recompute รอบนี้ (flagged ตามที่ตกลงไว้):**
- `mk`/`mkq` (งบการตลาด/ของแจก) ใน `ALL_PRODUCTS` — carry over ค่าเดิมจากรอบก่อน เพราะ giveaway rows มีราคา=0 คำนวณ value ไม่ได้จาก aggregation script ปัจจุบัน
- คอลัมน์แยกช่องทาง (Shopee/TikTok/Lazada/ฯลฯ) ในตาราง `WIBWUB_Dashboard.html` — ยังเป็นข้อมูลถึง 11 ก.ย. เท่านั้น (ตามที่ comment เดิมในไฟล์ระบุไว้อยู่แล้วจากรอบก่อน) มีการอัปเดตแค่คอลัมน์ "รวม (฿)" และ "จำนวน" ต่อสินค้าเป็นยอดใหม่ถึง 17 ก.ย. — คอลัมน์ช่องทางจึงไม่ sum ตรงกับยอดรวมพอดี (เป็นความคลาดเคลื่อนที่ทราบอยู่แล้ว)
- Sidebar chart `pr_top10`/`pr_channel` (stacked bar + doughnut) — ไม่ได้แตะ ยังเป็นข้อมูลเดิมถึง 11 ก.ย.

## STEP 4 — Affiliate arrays
Overwrite index สุดท้าย (เดือน ก.ย.) ใน `WIBWUB_Affiliate_Dashboard.html` (`AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR`) และ `WIBWUB_Mobile.html` (`AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM`) — ไม่ได้ append เดือนใหม่ ไม่ได้แตะเดือนก่อนหน้า

| | เดิม (1-14 ก.ย. รอบก่อน) | ใหม่ (1-14 ก.ย. รอบนี้) |
|---|---|---|
| GMV | ฿977,710 | ฿977,876 |
| Net | ฿963,636 | ฿963,802 |
| Commission | ฿109,052 | ฿109,374 |
| Creators | 603 | 603 |

⚠️ พบว่า column mapping ในไฟล์ task เดิม (col[2]=คืนเงิน, col[10]=ค่าคอม) **ไม่ตรงกับไฟล์จริง** — ไฟล์ export ปัจจุบันมี 22 คอลัมน์ และมี header 2 แถว (แถวชื่อคอลัมน์ + แถวคำอธิบาย tooltip) ไม่ใช่ 12 คอลัมน์แถวเดียวตามที่ระบุไว้ ใช้ column จริงที่ตรวจสอบแล้ว: col[1]=GMV, col[4]=การคืนเงิน, col[21]=ค่าคอมมิชชั่นโดยประมาณ, skip 2 แถวแรก (header + description)

## STEP 5 — sw.js + git commit
- Bump: `wibwub-v1145` → `wibwub-v1146`
- Commit: `97bfdd9` — "auto-update: Monday 2026-09-17 — Shipnity Top Products + Affiliate + sw.js bump" (4 ไฟล์: WIBWUB_Mobile.html, WIBWUB_Dashboard.html, WIBWUB_Affiliate_Dashboard.html, sw.js)
- `push_now.command` มีอยู่แล้วและถูกต้องตรงตาม template — **ยังไม่ push**, รอ user double-click ไฟล์นี้ที่เครื่องจริงเพื่อ push ขึ้น GitHub

## Verification
- ตรวจ M5 protection: ผ่าน (ไม่ต้องแก้)
- ตรวจ array element count ตรงกับ label count ทุก array ที่แก้
- ตรวจ git diff เฉพาะ 4 ไฟล์ที่ตั้งใจแก้ ไม่มีไฟล์อื่นหลุดเข้ามา
- ไม่มีการเขียนทับเดือน/ข้อมูลก่อนหน้าใน rolling-window arrays
