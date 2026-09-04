# Monday Update Report — 2026-09-03 (รอบบ่าย/เย็น)

Scheduled task: `wibwub-monday-update` · รอบที่สองของวัน (รอบเช้าจบไปแล้วที่ commit `bcc3c61`)
Commit รอบนี้: **`5c6855b`** · sw.js **v968 → v969**
Session mount: `/sessions/loving-awesome-fermat/mnt/` (runbook ยังชี้ที่ `hopeful-serene-fermi` ที่ตายแล้ว)

---

## สรุปสั้น

พบ **regression สำคัญ**: ตัวเลข Affiliate เดือน ส.ค. ที่รอบเช้าแก้ถูกต้องแล้ว ถูก commit `c9df6c2` ("auto: update 2026-09-03 18:22") เขียนกลับเป็นค่าเก่าที่ผิด รอบนี้กู้คืนแล้วและยืนยันตัวเลขกับไฟล์ export ต้นทางแบบตรงตัว

ดาวน์โหลดข้อมูลใหม่สำเร็จทั้งสองแหล่ง (Shipnity + TikTok Affiliate) แต่ **ไม่ append เดือน ก.ย. เข้ากราฟ** เพราะรูปแบบ export ของ TikTok เปลี่ยน metric ไปแล้ว (เหตุผลละเอียดด้านล่าง) — เข้าเกณฑ์ "ไม่แน่ใจ → หยุดและ log" ของ runbook ข้อ 5

---

## 1. Regression: ตัวเลข Affiliate ส.ค. ถูกเขียนทับ (แก้แล้ว)

รอบเช้า commit `bcc3c61` แก้ค่า ส.ค. เป็น GMV 1,730,879 / NET 1,701,979 / COMM 199,254 ถูกต้อง
ต่อมา commit `c9df6c2` เขียนกลับเป็น 1,730,666 / 1,701,769 / 198,783 (ค่าเก่าที่ผิด) ทั้งใน `WIBWUB_Mobile.html` และ `WIBWUB_Affiliate_Dashboard.html`

`c9df6c2` แก้ `WIBWUB_Affiliate_Dashboard.html` ไป **2,216 บรรทัด** พร้อมกัน — ลักษณะของการ regenerate ไฟล์ทั้งก้อนจากค่าที่ค้างอยู่ใน context ไม่ใช่การอ่านจาก export ล่าสุด ตรวจแล้วว่า**ไม่มี script ไหน hardcode ค่าเก่า** (grep `1730666|1701769|198783` ใน `*.py` `*.sh` `*.json` = ไม่พบ) ดังนั้นน่าจะมาจาก session อื่นที่ทำงานทับกัน

### ยืนยันตัวเลขจาก export ต้นทาง

คำนวณใหม่จาก `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260801-20260831.xlsx`:

| ตัวชี้วัด | คำนวณได้ | ที่กู้คืนลงไฟล์ |
|---|---|---|
| GMV (`GMV จากครีเอเตอร์`) | 1,730,879 | 1,730,879 ✅ |
| การคืนเงิน | 28,900 | — |
| NET (GMV − คืนเงิน) | 1,701,979 | 1,701,979 ✅ |
| ค่าคอมมิชชั่นโดยประมาณ | 199,254 | 199,254 ✅ |
| ครีเอเตอร์ที่มี GMV > 0 | 853 | 853 (ไม่แตะ) ✅ |

ตรงเป๊ะทุกตัว

### สิ่งที่แก้

- `WIBWUB_Affiliate_Dashboard.html` บรรทัด 12043–12045 → `AF_GMV` / `AF_NET` / `AF_COM` (index สุดท้าย = ส.ค. เท่านั้น)
- `WIBWUB_Mobile.html` บรรทัด 880–882 → `AFI_GMV` / `AFI_NET` / `AFI_COMM` (index สุดท้ายเท่านั้น)
- ไม่แตะ `AF_MO` / `AFI_MONTHS` / `AF_CR` · ไม่แตะเดือนก่อนหน้า · ไม่เปลี่ยนความยาว array

### ⚠️ ข้อควรระวัง — จะเกิดซ้ำได้อีก

การแก้รอบนี้ **จะถูกเขียนทับอีก** ถ้ามี session/auto-update ตัวถัดไป regenerate ไฟล์จากค่าที่ค้างใน context
**ข้อเสนอ:** ย้าย `AF_GMV`/`AF_NET`/`AF_COM`/`AFI_*` ออกไปเป็นไฟล์ JSON แยก (เช่น `affiliate_monthly.json`) ที่มีเจ้าของชัดเจน แล้วให้ dashboard `fetch()` มาใช้ จะตัดปัญหา array ถูกเขียนทับจาก session อื่นได้ถาวร

---

## 2. Shipnity (Step 1) — สำเร็จ

`Data Shipnity/Data_03-09-2026.xlsx` · 3,137,457 bytes · 20 คอลัมน์ตรงตาม runbook · 3,423 แถว (dedup แล้ว 3,413)

> ไฟล์นี้ทับไฟล์ของรอบเช้า (2,489,036 bytes @ 02:23) — รอบเช้าเก็บได้แค่ 2 วันครึ่ง รอบนี้ครบ 3 วันเต็ม

### ยอดขาย ก.ย. MTD (1–3 ก.ย.) = **฿990,967**

(รอบเช้ารายงาน ฿784,516 — เพิ่มขึ้นเพราะ 03/09 กลายเป็นวันเต็ม)

| วันที่ | ยอดขาย |
|---|---|
| 01/09 | ฿374,396 |
| 02/09 | ฿308,418 |
| 03/09 | ฿308,154 |

### แยกตามช่องทาง

| ช่องทาง | ยอดขาย |
|---|---|
| Shopee | 554,710 |
| Tiktok | 283,962 |
| facebook | 55,705 |
| Carcare | 50,810 |
| Line Shopping | 24,045 |
| FACEBOOK | 9,738 |
| Lazada | 4,900 |
| WEBSITE | 2,495 |
| POS | 2,309 |
| สินค้าสำหรับทำการตลาด | 1,328 |
| LINE_OA | 900 |
| Makro pro | 65 |

> หมายเหตุ: `facebook` และ `FACEBOOK` เป็นสองค่าแยกกันในข้อมูลต้นทาง (รวมกัน = 65,443) ควรทำ normalize ตัวพิมพ์ที่ต้นทาง Shipnity

### Top 15 สินค้า ก.ย. 1–3 (ยอดขาย / จำนวน)

| # | สินค้า | ยอดขาย | ชิ้น |
|---|---|---|---|
| 1 | Sugar 500ml | 120,175 | 346 |
| 2 | Refresh wipes | 103,083 | 1,267 |
| 3 | Interior 500ml | 51,417 | 146 |
| 4 | Interior wipes | 49,077 | 636 |
| 5 | Anna nano diamond | 42,960 | 24 |
| 6 | Wool duster | 39,635 | 63 |
| 7 | Spot 500ml | 39,234 | 99 |
| 8 | Refresh 500ml | 30,210 | 85 |
| 9 | Quartz shampoo 1L | 27,031 | 74 |
| 10 | Tire & trim gel | 25,532 | 53 |
| 11 | Xglass 100ml | 25,003 | 66 |
| 12 | Perfect | 24,386 | 151 |
| 13 | Reflex 250ml | 23,331 | 56 |
| 14 | Reflex 500ml | 18,448 | 28 |
| 15 | Monster | 16,303 | 20 |

---

## 3. TikTok Affiliate (Step 2) — ดาวน์โหลดสำเร็จ แต่รูปแบบเปลี่ยน

ไฟล์ใหม่: `Data Affiliate/ครีเอเตอร์/Creator_List_20260901-20260902_20260903151601.xlsx` · 369,112 bytes · 4,373 แถว

ช่วงข้อมูลที่เลือกได้: **1–2 ก.ย. เท่านั้น** (3 ก.ย. ขึ้นไปยังเป็นสีเทา เลือกไม่ได้)

### ตัวเลข ก.ย. 1–2 (คำนวณจากไฟล์ ตรงกับ KPI บนหน้าเว็บเป๊ะ)

| ตัวชี้วัด | ค่า |
|---|---|
| GMV จากแอฟฟิลิเอต | ฿111,391.33 |
| GMV ของการคืนเงิน | ฿4,369.88 |
| NET | ฿107,021.45 |
| ค่าคอมมิชชั่นโดยประมาณ | ฿12,423.99 |
| ครีเอเตอร์ที่มี GMV > 0 | 138 (จาก 4,373 ราย) |
| สินค้าที่ขายได้ | 633 |

### 🛑 ทำไมไม่ append เดือน ก.ย. เข้ากราฟ

รูปแบบ export **เปลี่ยน metric ไปแล้ว** ไม่ใช่แค่เปลี่ยนชื่อคอลัมน์:

| | ไฟล์ ส.ค. (Transaction Analysis) | ไฟล์ ก.ย. (Creator List ใหม่) |
|---|---|---|
| จำนวนคอลัมน์ | 22 | 24 |
| แถว header | 2 (ต้อง `.iloc[2:]`) | 1 |
| คอลัมน์ GMV | `GMV จากครีเอเตอร์` | `GMV จากแอฟฟิลิเอต` |
| คอลัมน์คืนเงิน | `การคืนเงิน` | `GMV ของการคืนเงินจากแอฟฟิลิเอต` |
| นิยาม | ยอดที่ settled | attribution 7 วัน ยังไม่หักยกเลิก |

series `AF_GMV` / `AFI_GMV` ทั้งหมด (มี.ค.–ส.ค.) สร้างจาก metric **`GMV จากครีเอเตอร์`** การ append ค่าจาก metric อีกตัวเข้าไปในกราฟเดียวกันจะทำให้เทรนด์เพี้ยนโดยที่ดูไม่ออก และไม่มีไฟล์ Creator_List ของเดือนเต็มไหนให้ cross-check ว่าสอง metric นี้ห่างกันเท่าไหร่

เข้าเกณฑ์ runbook ข้อ 5 ตรงตัว: **"ถ้าไม่แน่ใจ หยุดและ log"** → เลย log ไว้ ไม่เดา

นอกจากนี้ 2 วันจาก 30 วัน (6.7%) ต่อท้ายเดือนเต็ม จะแสดงเป็นแท่งเตี้ยที่อ่านผิดเป็น GMV ร่วงได้

**ทางแก้ที่แนะนำ:** ดึง Creator_List ของ ส.ค. ทั้งเดือนมาเทียบกับ 1,730,879 ก่อน ถ้าตัวเลขใกล้กันก็ย้าย series ไปใช้ metric ใหม่ได้ทั้งชุด ถ้าห่างมากต้องแยก series

---

## 4. Step 0 (M5 protection) — ข้ามอีกครั้งโดยเจตนา (รอบที่ 5)

Script ใน runbook ใช้ `required_months = today.month` = 9 แต่ `SH_REV` / `TK_REV` / `LZ_REV` และ array อื่นอีกราว 20 ตัวยังยาว 8 → ยืด `M5` เป็น 9 จะได้ `undefined` ที่ index 8 ทุกกราฟ

ตรวจแล้วรอบนี้: `M5` = `SH_REV` = `TK_REV` = `LZ_REV` = `PROD_MO_LBL` = **8 ทุกตัว** สอดคล้องกันดีอยู่แล้ว ไม่ต้องแก้

**Bug ใน runbook (ยังไม่ถูกแก้ 5 รอบติด):** เปลี่ยน `required_months = today.month` → `required_months = len(SH_REV)`

---

## 5. Step 3 (Top Products) — ข้ามโดยเจตนา

`ALL_PRODUCTS` (15 รายการ ยอดสะสม lifetime), `PROD_MO` (array ละ 8 ช่อง), `PROD_MO_LBL` (8 ช่อง) ผูกกับหน้าต่าง 8 เดือนของ `M5` แบบแข็ง

การ append เดือน ก.ย. ต้องแก้ `M5` + `SH_REV`/`TK_REV`/`LZ_REV` + array อีกราว 20 ตัวพร้อมกันแบบ lockstep ซึ่ง runbook ไม่ได้เขียนวิธีไว้ และ ก.ย. มีข้อมูล Shipnity แค่ 3 วัน ช่องทางอื่นยังไม่ sync → ข้ามเหมือน 3 รอบก่อน

---

## 6. Runbook drift ที่เจอใหม่รอบนี้

1. **URL ตาย** — `insights/transaction-analysis` redirect ไปหน้า "ผลการดำเนินงาน" แล้ว ตัว export ครีเอเตอร์ย้ายไป `https://affiliate.tiktok.com/data/creator-analysis?shop_region=TH&shop_id=7494549095358892612` (เมนูซ้าย: การวิเคราะห์ → ครีเอเตอร์)
2. **หน้านั้นขึ้นป้าย deprecation** — "อัปเกรดการวิเคราะห์แล้ว — หน้านี้จะเลิกใช้งานเร็วๆ นี้" ต้องหาที่ดึง export ใหม่ก่อนหน้านี้จะปิด
3. **ชื่อไฟล์เปลี่ยน** — จาก `Transaction_Analysis_Creator_List_*` เป็น `Creator_List_*` (script ที่ match ด้วย prefix เดิมจะหาไม่เจอ)
4. **โครงไฟล์เปลี่ยน** — 24 คอลัมน์ / header 1 แถว (ดูตารางเทียบข้อ 3)
5. **path ใน runbook ตายแล้ว** — ชี้ `/sessions/hopeful-serene-fermi/mnt/` ควรเปลี่ยนไปอ่าน mount path จาก env แทน hardcode
6. **`DATA_DIR` ผิด** — ต้องเป็น `Data Affiliate/ครีเอเตอร์/` (บันทึกไว้แล้วรอบเช้า ยังไม่ถูกแก้)
7. **คำเตือน "`navigate` ห้ามเรียกเดี่ยว จะ hang" ไม่จริง** — เรียกเดี่ยวแล้วคืนค่าปกติ และเป็น**วิธีเดียว**ที่ออกจากหน้า `chrome://` ได้ เพราะ `browser_batch` จะ pre-check URL ของ tab ปัจจุบันแล้ว reject ทั้ง batch ("Can't interact with browser internal pages")

### บันทึกเทคนิค: date picker ของ Shipnity

คลิกด้วยพิกัดไม่ได้ผล (picker เรนเดอร์โปร่งแสงทับตารางข้างหลัง คลิกทะลุลงตาราง) ต้องใช้ `find` เอา element ref มาคลิก — ref `ปุ่ม "เดือนนี้"` แล้วยืนยันด้วย JS ว่า `input-78` = `"1 ก.ย. 2569 ~ 30 ก.ย. 2569"` และปุ่ม export `disabled:false` ก่อนกด

### บันทึกเทคนิค: คิว export ของ TikTok

รอบแรกคิวขึ้น "กำลังส่งออก" ค้าง ~2.5 นาที แล้ว**reload หน้าเว็บ ทำให้คิวหายทั้งหมด** (panel ขึ้น "รายงานที่ส่งออก (0)")
แต่จริงๆ ไฟล์ export **สำเร็จแล้ว** — เห็นในรอบ retry ว่ามีไฟล์ `Creator_List_20260901-20260902_20260903151601.xlsx` รออยู่
**บทเรียน: ห้าม reload หน้าระหว่างรอ export** ให้ปิด-เปิด panel "บันทึกการดาวน์โหลดไฟล์" เพื่อ refresh สถานะแทน

---

## 7. Step 5 — commit แล้ว รอ push

```
5c6855b  Weekly update 2026-09-03 (pm): restore August affiliate totals
         reverted by c9df6c2 (GMV 1,730,879 / NET 1,701,979 / COMM 199,254,
         verified vs Transaction Analysis export); bump sw cache v969
```

ไฟล์ที่ commit: `WIBWUB_Affiliate_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js` (3 files, +7 −7)

**push ยังไม่ได้ทำ** — sandbox ติด proxy HTTP 403 ตามที่ runbook ระบุ
👉 **ต้องรัน `push_now.command` เองเพื่อ deploy** (ไฟล์มีอยู่และถูกต้องแล้ว ไม่ต้องแก้)

---

## 8. Verification

- ✅ `AF_MO`/`AF_GMV`/`AF_NET`/`AF_COM`/`AF_CR` = 8 ทุกตัว (ความยาวไม่เปลี่ยน)
- ✅ `AFI_MONTHS`/`AFI_GMV`/`AFI_NET`/`AFI_COMM` = 10 ทุกตัว (ความยาวไม่เปลี่ยน)
- ✅ `M5`/`SH_REV`/`TK_REV`/`LZ_REV` = 8 ทั้งใน Dashboard และ Mobile
- ✅ `PROD_MO_LBL` = 8 สอดคล้องกับ `M5`
- ✅ diff ที่ commit = 7 บรรทัดเท่านั้น ไม่มีเดือนก่อนหน้าถูกแตะ
- ✅ ตัวเลข ส.ค. ที่กู้คืน ตรงกับที่คำนวณจาก export ต้นทางทั้ง 4 ตัว
- ✅ ตัวเลข ก.ย. 1–2 ที่คำนวณจากไฟล์ ตรงกับ KPI บนหน้า TikTok เป๊ะ (GMV 111,391.33 / COMM 12,423.99)

---

## สิ่งที่ควรทำต่อ (เรียงตามความสำคัญ)

1. **รัน `push_now.command`** เพื่อ deploy commit `5c6855b`
2. **แก้ต้นเหตุ regression** — ย้าย affiliate monthly arrays ออกเป็น JSON แยก ไม่ให้ session อื่น regenerate ทับได้
3. **ดึง Creator_List ของ ส.ค. เต็มเดือน** มาเทียบกับ 1,730,879 เพื่อตัดสินใจว่าจะย้าย series ไป metric ใหม่หรือแยก series
4. **แก้ runbook** ทั้ง 7 ข้อในหัวข้อ 6 โดยเฉพาะ `required_months = len(SH_REV)` (ค้าง 5 รอบ) และ URL/ชื่อไฟล์/โครงคอลัมน์ของ TikTok
5. **normalize ตัวพิมพ์ช่องทาง** ที่ต้นทาง Shipnity (`facebook` vs `FACEBOOK`)
6. **หาที่ดึง affiliate export ตัวใหม่** ก่อนหน้า `creator-analysis` ถูกปิด
