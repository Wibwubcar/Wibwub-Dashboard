# รายงานอัปเดต Affiliate — 31 ส.ค. 2569 (รอบที่ 2)

รันอัตโนมัติโดย scheduled task `wibwub-thursday-affiliate` — ไม่มีผู้ใช้อยู่ระหว่างรัน

## ช่วงข้อมูล
1 ส.ค. 2569 – **29 ส.ค. 2569**
(หน้า TikTok ระบุ "อัปเดตเมื่อ: 29 ส.ค. 2026 0:00 (GMT+7:00)" — วันที่ 30–31 ยังถูก disable ในปฏิทิน)

## ไฟล์ที่ดาวน์โหลดและจัดเก็บ
| แท็บ | ไฟล์ | ขนาด | ปลายทาง |
|---|---|---|---|
| ครีเอเตอร์ | Transaction_Analysis_Creator_List_20260801-20260829.xlsx | 646,340 B | Data Affiliate/ครีเอเตอร์/ |
| สินค้า | Transaction_Analysis_Product_List_20260801-20260829.xlsx | 19,460 B | Data Affiliate/สินค้า/ |
| วีดีโอ | Transaction_Analysis_Video_List_20260801-20260829.xlsx | 1,399,089 B | Data Affiliate/วีดีโอ/ |
| ไลฟ์สตรีม | Transaction_Analysis_Live_List_20260801-20260829.xlsx | 117,824 B | Data Affiliate/ไลฟ์สตรีม/ |

ทั้ง 4 ไฟล์ถูกย้ายเข้าโฟลเดอร์ถูกต้องโดยอัตโนมัติแล้วผ่าน LaunchAgent `com.wibwub.download-mover` (scripts/wibwub_auto_move.sh) — STEP 3 จึงไม่ต้อง `cp` ซ้ำ

## STEP 4 — ตัวเลขเดือน ส.ค. 69 (1–29)
คำนวณจากไฟล์ครีเอเตอร์ (7,801 แถวข้อมูล):

| รายการ | ค่าที่คำนวณได้ | ค่าในไฟล์ dashboard | ผล |
|---|---|---|---|
| GMV | ฿1,603,562.27 | 1603562 | ✅ ตรง |
| การคืนเงิน | ฿25,085.19 | — | — |
| Net GMV | ฿1,578,477.08 | 1578477 | ✅ ตรง |
| ค่าคอมมิชชั่น | ฿184,714.82 | 184715 | ✅ ตรง |
| ครีเอเตอร์ที่มียอดขาย | 797 | 797 | ✅ ตรง |

**ไม่ต้องแก้อะไรใน STEP 4** — commit `20dd837` ("Affiliate GMV sync ส.ค. 1-28→1-29, sw v912") ได้ sync ชุดข้อมูล 1–29 ชุดเดียวกันนี้ไว้แล้ว
- `AF_MO` index สุดท้าย = `"ส.ค. (1-29)"` → เป็นการตรวจสอบทับ ไม่ใช่ append (ไม่มีเดือนก่อนหน้าถูกเขียนทับ)
- `AFI_MONTHS` index สุดท้าย = `'สค.69 (1-29)'` → `AFI_GMV/AFI_NET/AFI_COMM` ตรงกันทั้งหมด `WIBWUB_Mobile.html` จึงไม่ถูกแก้ไขรอบนี้

## STEP 5 — PRODUCTS (`cr` / `vid`)
เทียบกับไฟล์สินค้า 1–29 (vid = col 13, cr = col 19):

| สินค้า | เดิม | ใหม่ | หมายเหตุ |
|---|---|---|---|
| WIBWUB Refresh Leather Wipes | cr 41 / vid 39 | **cr 42** / vid 39 | +1 ครีเอเตอร์ |
| WIBWUB Sugar | cr 14 / vid 15 | **cr 15** / vid 15 | +1 ครีเอเตอร์ |
| WIBWUB Visible | cr 2 / vid 2 | cr 2 / **vid 1** | −1 วิดีโอ |
| Interior wipes · CLEANER · Interior · Refresh | — | ไม่เปลี่ยน | ตรงกับ export อยู่แล้ว |

KPI "ผ่าน X,XXX creators" — **ไม่มีในไฟล์เวอร์ชันนี้** ตัวเลข `1,597 unique creators` ที่ `#ck-gmv-s` ถูก render จาก JS (บรรทัด 11306) ไม่ใช่ค่า hardcode จึงไม่ต้องแก้

## STEP 5B — VIDEOS
รันด้วย `scripts/vid_merge.py` (สคริปต์ที่แก้บั๊ก `date_label()` ไว้แล้วจากรอบก่อน) ปรับ path เป็น session ปัจจุบัน

| รายการ | ค่า |
|---|---|
| แถวในไฟล์วีดีโอ | 6,976 |
| entries เดิม | 7,220 |
| อัปเดตค่า `aug` | **105** |
| entries ใหม่ | **93** |
| entries รวมหลังเขียน | **7,313** |

## STEP 6
- `sw.js` — bump cache `wibwub-v914` → **`wibwub-v915`**
- `push_now.command` — เขียนใหม่ให้ `git add` ทั้ง 3 ไฟล์ + commit + push, `chmod +x` แล้ว

## การตรวจสอบ
- `node` eval ผ่าน: VIDEOS = 7,313 entries, keys ครบ (creator/product/vid_id/caption/gmv/units/date/monthly), monthly keys = mar–aug
- ผลรวม `monthly.aug` = **1,342,852** · `monthly.jul` = 1,243,970 (สอดคล้องกับ ส.ค. แซง ก.ค.)
- `date` ว่างในรายการที่ gmv > 0: **0 รายการ** (ไม่มี regression ของ label)
- `git diff --stat` = 291 insertions / 198 deletions จาก ~11,600 บรรทัด ≈ **2.5%** — ต่ำกว่าเกณฑ์เตือน 50% มาก
- ตรวจ diff ด้วยตา: เปลี่ยนเฉพาะฟิลด์ `aug` และ `gmv` เท่านั้น — label เช่น `'มิ.ย.–ส.ค.'` คงเดิม (บั๊ก date_label ไม่กลับมา)
- ทั้งสองไฟล์ HTML จบด้วย `</html>` ครบถ้วน

## ⚠️ บั๊กใน SKILL.md ที่ยังไม่ได้แก้ (ซ้ำจากรายงานรอบก่อน)
1. **STEP 4 column index ผิด** — สกิลระบุ returns = col 2, orders = col 3, commission = col 10 และเริ่มที่ `df.iloc[1:]` ของจริงคือ header 2 แถว (`df.iloc[2:]`), GMV = col 1, refunds = **col 4**, orders = **col 5**, commission = **col 21** รอบนี้ใช้ index ที่ตรวจสอบเองแทน ถ้ารันตามสกิลตรง ๆ จะได้ค่าผิดแบบเงียบ ๆ (col 2 = LIVE GMV, col 10 = CTOR)
2. **STEP 5 fuzzy column search ไม่เสถียร** — ควร hardcode `vid` = col 13, `cr` = col 19
3. **STEP 5B `date_label()`** — สกิลใช้ "สองเดือนล่าสุด" แต่ convention จริงคือ "เดือนแรก–เดือนสุดท้ายที่ active" รอบนี้เลี่ยงได้เพราะใช้ `scripts/vid_merge.py` ที่แก้ไว้แล้ว **แต่ถ้าใครรันตามสกิลจะพังซ้ำ**
4. **`navigate` แบบ standalone** — สกิลห้ามใช้ แต่ของจริง `browser_batch` ที่มี `navigate` จะ error `"Can't interact with browser internal pages"` เมื่อ tab อยู่ที่ `chrome://newtab/` ต้องใช้ standalone `navigate` เพื่อ bootstrap ก่อน แล้วค่อยใช้ `browser_batch`
5. **path ใน SKILL.md hardcode `/sessions/hopeful-serene-fermi/`** — ต้อง remap เป็น session ปัจจุบันทุกครั้ง (รอบนี้ = `/sessions/funny-sleepy-keller/`)

## หมายเหตุการตัดสินใจ (ไม่มีคนยืนยัน)
- เลือกวันสิ้นสุด 29 ส.ค. เพราะ 30–31 ถูก disable ในปฏิทิน TikTok
- ต้องตั้งช่วงวันที่ **สองจุด** — picker ด้านบน (KPI) และ picker ในหัวข้อ "รายละเอียด" ที่คุมการ export หากตั้งเฉพาะอันบน export จะได้ default 7 วัน
- Trigger export ทั้ง 4 แท็บก่อน แล้วค่อยดาวน์โหลดทีเดียว เพื่อลดเวลารอ
- แผงรายงานค้างที่ "กำลังส่งออก" — แก้โดย reload หน้า (แผง cache ฝั่ง client ไม่ poll เอง)
- **ยังไม่ push** — `push_now.command` พร้อมแล้ว รอผู้ใช้รันเอง (การ push เป็นการเผยแพร่สาธารณะ จึงไม่ทำอัตโนมัติ)

## สรุปไฟล์ที่ถูกแก้
| ไฟล์ | การเปลี่ยนแปลง |
|---|---|
| `WIBWUB_Affiliate_Dashboard.html` | PRODUCTS 3 ค่า + VIDEOS (105 updated / 93 new) |
| `sw.js` | wibwub-v914 → v915 |
| `push_now.command` | regenerate + chmod +x |
| `WIBWUB_Mobile.html` | ไม่แก้ (ข้อมูลตรงอยู่แล้ว) |

Backup: `WIBWUB_Affiliate_Dashboard.html.bak_*_run`, `WIBWUB_Mobile.html.bak_*_run`
