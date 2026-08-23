# Affiliate Auto-Update — 22 ส.ค. 2026 (สคีเมา: wibwub-thursday-affiliate)

ช่วงข้อมูล: **1–19 ส.ค. 2026** (TikTok Affiliate Center อัปเดตล่าสุดถึง 19 ส.ค. 2026 0:00 GMT+7 — วันที่ 20–22 ยังเลือกไม่ได้)

## ไฟล์ที่ดาวน์โหลด (STEP 2–3)

| แท็บ | ไฟล์ | ขนาด | ปลายทาง |
|---|---|---|---|
| ครีเอเตอร์ | Transaction_Analysis_Creator_List_20260801-20260819.xlsx | 564,842 B | Data Affiliate/ครีเอเตอร์/ |
| สินค้า | Transaction_Analysis_Product_List_20260801-20260819.xlsx | 19,537 B | Data Affiliate/สินค้า/ |
| วีดีโอ | Transaction_Analysis_Video_List_20260801-20260819.xlsx | 1,206,423 B | Data Affiliate/วีดีโอ/ |
| ไลฟ์สตรีม | Transaction_Analysis_Live_List_20260801-20260819.xlsx | 77,987 B | Data Affiliate/ไลฟ์สตรีม/ |

LaunchAgent `com.wibwub.download-mover` ย้ายไฟล์ออกจาก Downloads ให้เองครบทั้ง 4 ไฟล์ ไม่ต้อง `cp` เอง

## STEP 4 — ครีเอเตอร์

จาก 6,594 แถว:

| ตัวชี้วัด | ส.ค. 1–19 | ก.ค. เต็มเดือน |
|---|---|---|
| GMV | ฿1,023,630 | ฿1,452,748 |
| Net GMV | ฿1,004,422 | ฿1,428,498 |
| ค่าคอมมิชชั่น | ฿119,922 | ฿169,224 |
| ครีเอเตอร์ที่มียอด | 541 | 720 |

อัปเดตแล้ว: `AF_MO`/`AF_GMV`/`AF_NET`/`AF_COM`/`AF_CR` (Affiliate Dashboard) และ `AFI_MONTHS`/`AFI_GMV`/`AFI_NET`/`AFI_COMM` (Mobile) — เขียนทับสมาชิกตัวสุดท้าย (ส.ค.) ไม่แตะเดือนก่อนหน้า

KPI strip หน้าภาพรวมที่ค้างอยู่ที่ "ส.ค. 1-17" ถูกอัปเดตเป็น 1-19 ทั้งชุด รวมถึงบรรทัด note ด้านบนที่ยังเขียนว่า "อัปเดตล่าสุดถึง 1 ส.ค. 2026"

Live GMV (จากไฟล์ไลฟ์สตรีม): **฿71,263 / 421 sessions** (ตัวเลขเดิมบนหน้าเว็บคือ ฿37.7K/365 sessions ซึ่งเป็นข้อมูล มิ.ย.+ก.ค. ค้างไว้ — แก้ให้เป็นของ ส.ค. 1-19 แล้ว)

## STEP 5 — สินค้า

แก้เฉพาะ `cr` / `vid` ใน `PRODUCTS` ตามกติกา (ไม่แตะ gmv/units/monthly/ret) — เปลี่ยน 2 จุด:

- WIBWUB Refresh Leather Wipes: `vid` 34 → **35**
- WIBWUB Interior wipes: `cr` 22 → **23**

อีก 5 สินค้าค่าเท่าเดิม (Sugar 15/16, CLEANER 6/7, Interior 5/5, Refresh 3/4, Visible 2/2)

หมายเหตุ: ไฟล์ปัจจุบันไม่มีข้อความ "ผ่าน X,XXX creators" แบบ hardcode แล้ว — KPI strip แท็บสินค้าคำนวณจาก `PRODUCTS` ใน JS จึงอัปเดตเอง

## STEP 5B — วีดีโอ

Parse ผ่าน `zipfile` + regex (ไฟล์เป็น inlineStr XML, openpyxl อ่านไม่ได้)

- export rows: **5,915** (ไม่ใช่ 0 → ผ่านเงื่อนไข safety)
- entries เดิม: 6,167 → ปัจจุบัน **6,304**
- อัปเดตค่า `aug`: **90** entries
- เพิ่มใหม่: **137** entries
- ไม่เปลี่ยน: 5,688

**Reconcile ผ่าน:** ผลรวม `monthly.aug` ใน `VIDEOS` = **฿849,754** ตรงกับผลรวมคอลัมน์ GMV ของไฟล์ export แบบเป๊ะ และไม่มี entry ไหนที่มี `aug > 0` แต่หายไปจาก export (stale = 0)

`gmv` คำนวณใหม่เป็น sum(monthly) ตามคอนเวนชันเดิม, `units` ของ entry เดิมไม่แตะ, `date` label recompute เฉพาะ entry ที่ยังไม่มี "ส.ค." และเพิ่งมียอดในเดือนนี้

## STEP 6 — sw.js

`wibwub-v769` → **`wibwub-v770`** · `push_now.command` มีอยู่แล้วและถูกต้อง ไม่ต้องสร้างใหม่

## การตรวจสอบ

- `node --check` ผ่านทุก script block: Affiliate Dashboard (1 block), Mobile (3 blocks)
- eval `VIDEOS` ใน node สำเร็จ: 6,304 entries, aug ฿849,754, gmv รวม ฿2,621,050

## ⚠️ สิ่งที่ต้องแก้ในไฟล์ skill

1. **STEP 4 อ่านคอลัมน์ผิด** — skill hardcode index ว่า returns = col[2], commission = col[10] แต่ export เวอร์ชันปัจจุบัน index 2 คือ "GMV ที่มาจาก LIVE" และ index 10 คือ "CTOR" ตัวจริงคือ `การคืนเงิน` (index 4) และ `ค่าคอมมิชชั่นโดยประมาณ` (index 21) — ควรเปลี่ยนไปอ้างชื่อคอลัมน์แทน index
2. **STEP 4 อ่าน header ผิด** — `pd.read_excel(header=None)` แล้ว `.iloc[1:]` ทำให้แถวคำอธิบายยาวๆ ค้างอยู่ในข้อมูลและ `float()` พัง ต้องใช้ `header=0` แล้ว `.iloc[1:]`
3. **STEP 5 ไม่ได้ระบุคอลัมน์** — ยืนยันแล้วว่า `cr` = `ครีเอเตอร์ที่มียอดขายเฉลี่ยรายวัน` และ `vid` = `วิดีโอที่มียอดขายเฉลี่ยรายวัน` (ไม่ใช่คอลัมน์ `วิดีโอ` ที่เป็นจำนวนคลิปทั้งหมด) — regression test กับไฟล์ 0818 ได้ค่าตรงกับ dashboard ทั้ง 7 สินค้า
4. **`navigate` แบบ standalone ใช้ได้** — skill เตือนว่าให้ห่อใน `browser_batch` เสมอ แต่จริงๆ กลับกัน: `browser_batch` ที่มี `navigate` จะพังถ้าแท็บอยู่บน `chrome://newtab/` ส่วน standalone `navigate` ทำงานได้ทันที
5. **path ใน skill เป็นของ session เก่า** (`/sessions/hopeful-serene-fermi/`) ควรเขียนเป็น path แบบ relative หรือ resolve จาก mount ปัจจุบัน

## 🔍 ข้อมูลที่แก้ย้อนหลัง

`AF_NET` ของ ส.ค. ที่บันทึกไว้เดิม (จากรอบ 1-18) คือ **904,366** แต่คำนวณใหม่จากไฟล์เดิมได้ **940,905** — ส่วนต่าง 36,539 ไม่ตรงกับผลรวมคอลัมน์ไหนในไฟล์เลย (`การคืนเงิน` จริง = 19,208) และ gap ratio 5.8% ผิดปกติเมื่อเทียบกับ ก.ค. (1.67%) จึงสรุปว่าค่าเดิมผิด และเขียนทับด้วยค่าที่คำนวณใหม่ (1,004,422 สำหรับช่วง 1-19)

## ❗ git commit ทำไม่สำเร็จ

sandbox เขียน `.git/index` ไม่ได้ (`Operation not permitted`) — ไฟล์บนดิสก์อัปเดตครบถูกต้องแล้ว แต่ยังไม่ถูก commit ต้องรอ cron `auto_push` ฝั่งเครื่อง หรือรัน `push_now.command` เอง
