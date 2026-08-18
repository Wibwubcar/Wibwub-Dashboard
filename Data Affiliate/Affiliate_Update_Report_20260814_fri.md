# WIBWUB Affiliate Update — 14 ส.ค. 2569 (ศุกร์)

**ช่วงข้อมูล:** 1/8/2026 – 11/8/2026
(TikTok อัปเดตข้อมูลถึง 11 ส.ค. เท่านั้น — 12–14 ส.ค. ยัง greyed out ในปฏิทิน)

## ไฟล์ที่ดาวน์โหลด + ย้ายแล้ว (LaunchAgent ย้ายอัตโนมัติทั้ง 4 ไฟล์)

| Tab | ไฟล์ | ปลายทาง |
|---|---|---|
| ครีเอเตอร์ | Transaction_Analysis_Creator_List_20260801-20260811.xlsx | Data Affiliate/ครีเอเตอร์/ |
| สินค้า | Transaction_Analysis_Product_List_20260801-20260811.xlsx | Data Affiliate/สินค้า/ |
| วีดีโอ | Transaction_Analysis_Video_List_20260801-20260811.xlsx | Data Affiliate/วีดีโอ/ |
| ไลฟ์สตรีม | Transaction_Analysis_Live_List_20260801-20260811.xlsx | Data Affiliate/ไลฟ์สตรีม/ |

## ตัวเลขเดือน ส.ค. (1–11)

| | เดิม | ใหม่ |
|---|---|---|
| GMV | ฿598,401 | **฿598,516** |
| Net GMV | ฿584,964 | **฿585,077** |
| Commission | ฿70,094 | **฿70,272** |
| Creators | 376 | 376 |

อัปเดตแล้วที่ index สุดท้ายของ AF_GMV / AF_NET / AF_COM / AF_CR (label `ส.ค. (1-11)`) และ AFI_GMV / AFI_NET / AFI_COMM (label `สค.69 (1-11)`) — ทั้งสอง label เป็นตัวสุดท้ายของ array อยู่แล้ว จึงเขียนทับเดือนเดิม ไม่มีการ append หรือแตะเดือนก่อนหน้า

## PRODUCTS cr/vid

Leather Wipes 36/32 → 32/28 · Interior Wipes 22/21 (ไม่เปลี่ยน) · Sugar 18/19 → 17/18 · Cleaner 7/8 → 6/7 · Interior 6/6 → 5/5 · Visible 2/2 (ไม่เปลี่ยน) · Refresh 0/0 (ไม่แตะ — ดูข้อ 3 ด้านล่าง)

## VIDEOS array — ไม่มีการเปลี่ยนแปลง (ตั้งใจ)

vid_id ในไฟล์วันนี้ 4,800 รายการ ตรงกับ dashboard 4,800/4,800 และค่า GMV รายคลิปเหมือนเดิมทุกตัว (0 updated, 0 new) เพราะช่วงข้อมูลเป็น 1–11 ส.ค. เท่ากับรอบเมื่อวาน — VIDEOS ยังเป็นข้อมูลล่าสุดอยู่แล้ว จึง **restore block เดิมกลับ** แทนการเขียนทับ (เหตุผลในข้อ 1)

## KPI strip ที่แก้เพิ่ม (ค้างมาตั้งแต่ 1 ส.ค.)

- Affiliate GMV (ส.ค. 1) ฿35.0K → **Affiliate GMV (ส.ค. 1-11) ฿598.5K**
- Net GMV ฿32.4K → **฿585.1K**
- ครีเอเตอร์ที่มียอด 45 → **376**
- ค่าคอมมิชชั่น ฿4.2K → **฿70.3K**
- อ้างอิงเดือน ก.ค. ปรับให้ตรงกับ array: Net ฿1,357K → ฿1,428K, Comm ฿170K → ฿169K

## sw.js

v660 → **v661**

---

# ⚠️ 3 เรื่องที่ต้องแก้ใน SKILL (พบวันนี้)

### 1. `esc()` ใน STEP 5B ทำ backslash เพิ่มเป็นเท่าตัวทุกรอบ

caption ที่มี emoji escape (`\ud83d`) ถูก `.replace('\\','\\\\')` ทุกครั้งที่ script รัน → backslash เพิ่มขึ้นเรื่อย ๆ ตัวอย่างจริงวันนี้:

- ก่อนรัน: `...หายไปในพริบตา\\\\\\\\\\\\\\\\ud83d...` (16 backslash)
- หลังรัน: 32 backslash

เป็นการ corrupt สะสม ทุกครั้งที่ schedule ทำงาน ไม่ว่าจะมีข้อมูลใหม่หรือไม่ **วันนี้ผมเขียน VIDEOS block เดิมกลับไปแล้ว จึงไม่มีความเสียหายเพิ่ม** แต่ backslash ที่สะสมมาจากรอบก่อน ๆ ยังค้างอยู่ในไฟล์

แนะนำ: อ่าน caption กลับมาแบบ unescape ก่อน แล้วค่อย escape รอบเดียว หรือดีกว่านั้นคือ **อย่าแตะ field caption เลย** ถ้าไม่มี caption ใหม่

เพิ่มเติม: script ยัง rewrite ทั้ง block ทุกครั้ง (2,851/8,873 บรรทัด = 32% ของไฟล์) แม้ไม่มีข้อมูลเปลี่ยน — ควร skip การเขียนไฟล์เมื่อ `updated == 0 and new == 0`

### 2. Column index ใน STEP 4 ผิด (ยังไม่เคยถูกจับได้)

SKILL ระบุ `col[2]=returns, col[10]=commission` แต่ layout จริงของ Transaction_Analysis_Creator_List วันนี้คือ:

- `col[1]` = GMV จากครีเอเตอร์ ✅
- `col[2]` = GMV ที่มาจาก LIVE (**ไม่ใช่** returns)
- `col[4]` = การคืนเงิน ← returns ตัวจริง
- `col[10]` = CTOR (**sum = 0** — ไม่ใช่ commission)
- `col[21]` = ค่าคอมมิชชั่นโดยประมาณ ← commission ตัวจริง

นอกจากนี้ header กินสองแถว (แถว 0 ชื่อคอลัมน์ / แถว 1 คำอธิบาย) — `df.iloc[1:]` ตาม SKILL จะเหลือแถวคำอธิบายปนมา ต้องใช้ `df.iloc[2:]`

รอบนี้ผมใช้ col 1/4/21 และ skip 2 แถว ผลลัพธ์ตรงกับค่าที่มีอยู่เดิม (376 creators ตรงเป๊ะ, GMV ต่างกัน 115 บาทจาก data revision ปกติ) ยืนยันว่า mapping ใหม่ถูก

### 3. `WIBWUB Refresh` ไม่เคยถูก map

แถว `น้ำยาทำความสะอาดเบาะหนังรถยนต์ ... (WIBWUB Refresh Leather Cleaner)` มี GMV ฿25,351 ในเดือน ส.ค. แต่ใน PRODUCTS ตัว `WIBWUB Refresh` มี `aug:0, cr:0, vid:0` — แปลว่า mapping table ("Refresh ที่ไม่มี Leather") จับสินค้านี้ไม่ได้ เพราะชื่อจริงมีคำว่า Leather อยู่ด้วย

รอบนี้ผมไม่แตะ เพราะถ้าใส่ cr/vid เข้าไปโดยที่ gmv รายเดือนยังเป็น 0 ตัวเลขจะขัดกันเอง — ต้องให้ยืนยันก่อนว่า `WIBWUB Refresh` = Refresh Leather Cleaner ใช่หรือไม่ ถ้าใช่ ควรแก้ mapping table เป็นจับจาก `(WIBWUB ...)` ในวงเล็บแทน keyword แบบ fuzzy

---

📌 **ดับเบิ้ลคลิก `push_now.command` เพื่อ push ขึ้น GitHub**
