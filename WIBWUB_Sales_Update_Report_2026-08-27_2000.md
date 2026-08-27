# WIBWUB Sales Sheet Update — 27 ส.ค. 2569 (รอบเย็น)

Commit: `8ee3bc2` · sw.js `wibwub-v851` → `wibwub-v852`

## STEP 0 — ตรวจความยาว array (verify-only)
ผ่านทั้งสองไฟล์: `M5` = 8 เดือน, `SH_REV`/`TK_REV`/`LZ_REV` และ array อื่นทั้งหมด = 8 เดือนเท่ากัน
ไม่มีการ pad label เดือนใหม่ และไม่ต้องเพิ่มเดือนใหม่ (ส.ค. มีอยู่แล้ว)

## STEP 1 — ข้อมูลจาก Google Sheets (row สุดท้ายของ ส.ค. 2569)

| Sheet | row สุดท้าย | ยอดขาย | สถานะ |
|---|---|---|---|
| Shopee | `01-23/08/26` | 4,787,148 | ไม่มีข้อมูลใหม่ — ตรงกับที่แดชบอร์ดมีอยู่แล้ว |
| TikTok | `01-26/08/26` | 2,057,387.59 | **มีข้อมูลใหม่** (เดิม `01-23/08/26` = 1,790,219.03) |
| Lazada | `01-23/08/26` | 84,993.69 | ไม่มีข้อมูลใหม่ — ตรงกับที่แดชบอร์ดมีอยู่แล้ว |

## STEP 2 — Arrays ที่อัปเดต (index 7 = ส.ค. เท่านั้น)

TikTok เท่านั้นที่เปลี่ยน (จาก row `01-26/08/26`):

| Array | เดิม | ใหม่ |
|---|---|---|
| TK_REV | 1,790,219.03 | 2,057,387.59 |
| TK_ORD | 8,575 | 9,846 |
| TK_CANCEL_PCT / TK_CANCEL | 6.67 | 6.53 |
| TK_AFI | 1,172,768 | 1,375,920 |
| TK_NET | 1,151,786 | 1,352,971 |
| TK_ADS | 1,743,949 | 2,020,799 |
| TK_LIVE | 195,400 | 230,100 |
| TK_AFIPCT | 65.5 | 65.8 |
| TK_NEW | 6,694 | 7,855 |
| TK_OLD | 867 | 971 |
| TK_ADSSPEND | 473,047 | 549,245 |
| TK_FEECOMM | 516,909 | 620,547 |

Shopee และ Lazada arrays ไม่ถูกแตะ (ค่าเดิมตรงกับ sheet แล้ว)

## STEP 3 / 3B — Label และ date picker
ตามหลัก `wibwub-avoid-stale-hardcoded-labels` — เปลี่ยน label ที่เคย hardcode ให้ derive จากข้อมูลจริงแทน:

WIBWUB_Dashboard.html
- เพิ่ม source of truth `MTD_COVERAGE = {Shopee:'2026-08-23', TikTok:'2026-08-26', Lazada:'2026-08-23'}` + `MTD_MAX_DATE` + `mtdCoverageLabel()` ไว้ติดกับ array ยอดขาย
- `cc-sub` ของกราฟ "ยอดขายรายเดือน แยก Platform" เดิมเขียนตายว่า "ส.ค. = MTD ถึง 23 ส.ค. (Shopee / TikTok / Lazada)" ตอนนี้ render เป็น
  `ม.ค. – ส.ค. 2569 (ข้อมูลจริง) · ส.ค. = MTD · Shopee ถึง 23 ส.ค. · TikTok ถึง 26 ส.ค. · Lazada ถึง 23 ส.ค.`
- `MP_MONTH_BOUNDS` เดือนสุดท้าย `e` derive จาก `MTD_MAX_DATE` (`2026-08-23` → `2026-08-26`) แทนค่าตายตัว
- `MP_DATE_MAX` derive จาก `_now` อยู่แล้ว · `rangeEnd = 7` ถูกต้อง · `MONTH_LABELS_FULL/SHORT` = 8 ตัว ถูกต้อง

WIBWUB_Mobile.html
- hero tiles Shopee/TikTok/Lazada ใส่ id แล้วให้ `initHome()` คำนวณจาก `SH_REV`/`TK_REV`/`LZ_REV` โดยตรง → TikTok `฿11.6M` → `฿11.8M` (Shopee `฿40.3M`, Lazada `฿1.02M` เท่าเดิม, format ตรงกับของเดิม)

## ไม่ได้แก้ (ตั้งใจ) — ต้องให้คนตัดสินใจ
1. **Mobile hero `฿62.0M` / `124,156 unique orders` / `AOV ฿484`** — ตัวเลขนี้ไม่ตรงกับผลรวมของ array ใดๆ ในไฟล์ (ผลรวม `TOTAL_REV` = ฿63.67M, `TOTAL_ORD` = 128,453) และคำว่า "unique orders" บ่งว่าเป็นตัวเลข dedupe จาก Shipnity คนละฐานกับ sheet ทั้ง 3 จึงไม่แก้เพื่อไม่ให้เปลี่ยนนิยาม metric โดยพลการ — **ขอให้ยืนยันว่าตัวเลขนี้มาจากไหน** แล้วค่อยทำให้ derive อัตโนมัติ
2. **`CHANNELS` array ใน Mobile** (Shopee 35,516,360 / TikTok 9,775,146 ฯลฯ) ไม่ตรงกับผลรวม `SH_REV`/`TK_REV` — น่าจะเป็นฐาน Shipnity เช่นกัน ไม่แตะ
3. **`SH_ADS[7] = 796,207.17`** ไม่ตรงกับตัวเลขใดใน Shopee sheet — row `01-23/08/26` มีแต่ ads รวม facebook C-pass = 866,977 (แถว 01-16 มีทั้ง Shopee-only 507,442 และรวม 683,132 แต่แถว 01-23 มีแค่ค่ารวม) ค่าปัจจุบันน่าจะเป็นค่าประมาณจากรอบก่อน — ปล่อยไว้เพราะ Shopee ไม่มีข้อมูลใหม่รอบนี้ แต่ควรตรวจสอบ
4. `PROD_MO_LBL` = `ส.ค. (1-23)` และ KPI `฿64.16M` ในหน้า Products มาจากไฟล์ Shipnity ไม่ใช่ sheet ทั้ง 3 — นอกขอบเขตงานนี้

## Verification
- แตก `<script>` ทุก block ของทั้งสองไฟล์ผ่าน `node --check` — ผ่านทั้งหมด
- ตรวจซ้ำความยาวทุก array = 8 ตรงกับ `M5`/`MONTH_LABELS_*`
- รัน `mtdCoverageLabel()` และ formatter ของ hero tiles ใน node เพื่อยืนยัน output จริง
- grep หา label เก่าที่ค้าง (`MTD ถึง 23`, `฿11.6M`) — ไม่เหลือ

## ต้องทำต่อ
Commit เรียบร้อยแล้ว แต่ sandbox push ไม่ได้ (proxy 403) — **ดับเบิลคลิก `push_now.command` บนเครื่อง Mac เพื่อ push ขึ้น origin/main**
