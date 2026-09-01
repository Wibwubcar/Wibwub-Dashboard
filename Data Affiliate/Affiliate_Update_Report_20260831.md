# รายงานอัปเดต Affiliate — 31 ส.ค. 2569 (จันทร์)

รันอัตโนมัติโดย scheduled task `wibwub-thursday-affiliate` — ไม่มีผู้ใช้อยู่ระหว่างรัน

## ช่วงข้อมูล
1 ส.ค. 2569 – 28 ส.ค. 2569
(วันที่ 29–31 ยังเลือกไม่ได้ในหน้า TikTok — ระบบระบุ "อัปเดตเมื่อ: 28 ส.ค. 2026")

## ไฟล์ที่ดาวน์โหลดและจัดเก็บ
| แท็บ | ไฟล์ | ขนาด | ปลายทาง |
|---|---|---|---|
| ครีเอเตอร์ | Transaction_Analysis_Creator_List_20260801-20260828.xlsx | 635,675 B | Data Affiliate/ครีเอเตอร์/ |
| สินค้า | Transaction_Analysis_Product_List_20260801-20260828.xlsx | 19,421 B | Data Affiliate/สินค้า/ |
| วีดีโอ | Transaction_Analysis_Video_List_20260801-20260828.xlsx | 1,381,670 B | Data Affiliate/วีดีโอ/ |
| ไลฟ์สตรีม | Transaction_Analysis_Live_List_20260801-20260828.xlsx | 114,455 B | Data Affiliate/ไลฟ์สตรีม/ |

## ตัวเลขเดือน ส.ค. 69 (1–28)
| รายการ | ค่าเดิม | ค่าใหม่ |
|---|---|---|
| GMV | ฿1,452,748 → 1,526,372 | **฿1,526,564** |
| Net (หลังคืนสินค้า) | 1,502,226 | **฿1,502,415** |
| ค่าคอมมิชชั่น | 175,212 | **฿175,633** |
| ครีเอเตอร์ | 769 | **769** (ไม่เปลี่ยน) |

เทียบ ก.ค. 69 เต็มเดือน: GMV ฿1,452,748 — ส.ค. แซงแล้วทั้งที่เหลืออีก 3 วัน

## สิ่งที่แก้ไข
- `WIBWUB_Affiliate_Dashboard.html` — อัปเดต `AF_GMV` / `AF_NET` / `AF_COM` ที่ index สุดท้าย (label `"ส.ค. (1-28)"` มีอยู่แล้ว จึงเป็นการเขียนทับ ไม่ใช่ append) — 3 บรรทัด
- `sw.js` — bump cache `wibwub-v905` → `wibwub-v906`
- `push_now.command` — regenerate + chmod +x

## สิ่งที่ไม่ต้องแก้
- `WIBWUB_Mobile.html` — `AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM` และ KPI card ตรงกับข้อมูลใหม่อยู่แล้ว (1526564 / 1502415 / 175633 / 769 creators)
- `PRODUCTS` — ค่า `cr`/`vid` ทั้ง 7 รายการตรงกับ export ใหม่ทุกตัว
- `VIDEOS` — สคริปต์รวมข้อมูลรายงาน updated 0 / new 0 (ข้อมูลถึง 28 ส.ค. ไม่เปลี่ยนจากรอบก่อน) ยอดคงที่ 7,220 entries

## ตรวจสอบ
- `VIDEOS` eval ผ่าน: 7,220 entries, keys ครบ (creator, product, vid_id, caption, gmv, units, date, monthly)
- `git diff --stat` ของ `WIBWUB_Affiliate_Dashboard.html` = 3 insertions / 3 deletions เท่านั้น (ตรงกับที่ตั้งใจแก้)

## ⚠️ บั๊กใน SKILL.md ที่ต้องแก้ก่อนรันรอบหน้า

**1. STEP 4 — column index ของไฟล์ครีเอเตอร์ผิด**
สคริปต์ในสกิลใช้ returns = col 2, commission = col 10 และเริ่มอ่านที่แถวแรก → crash
`ValueError: could not convert string to float: 'GMV ที่เกิดจากลูกค้าที่แตะลิงก์...'`
ของจริง: ไฟล์มี header **2 แถว** (ข้อมูลเริ่มที่ `df.iloc[2:]`), GMV = col 1, returns = **col 4**, commission = **col 21**
ตรวจไฟล์ 20260827 แล้ว layout เหมือนกัน → เป็นความผิดพลาดเดิมในสกิล ไม่ใช่ TikTok เปลี่ยนรูปแบบ

**2. STEP 5 — การค้นหาคอลัมน์แบบ fuzzy ไม่เสถียร**
ยืนยันจากข้อมูลจริง: `vid` = **col 13** (วิดีโอที่มียอดขายเฉลี่ยรายวัน), `cr` = **col 19** (ครีเอเตอร์ที่มียอดขายเฉลี่ยรายวัน)
ควร hardcode index สองตัวนี้แทน fuzzy search

**3. STEP 5B — `date_label()` ใช้ convention ผิด → เขียนทับ label 280 บรรทัดโดยไม่มีข้อมูลใหม่เลย**
สกิลสร้าง label จาก "สองเดือนล่าสุดที่ active" แต่ convention จริงในไฟล์คือ "เดือนแรกที่ active – เดือนสุดท้ายที่ active"
ผลคือ entry ที่ active มิ.ย./ก.ค./ส.ค. ถูกเปลี่ยนจาก `'มิ.ย.–ส.ค.'` เป็น `'ก.ค.–ส.ค.'`
รอบนี้ restore จาก backup แล้ว (diff กลับจาก 280/280 → 3/3) แต่ **ถ้าไม่แก้ รอบหน้าจะพังซ้ำ**

## หมายเหตุการตัดสินใจ (ไม่มีคนยืนยัน)
- เลือกวันที่สิ้นสุดเป็น 28 ส.ค. เพราะ 29–31 ถูก disable ในปฏิทินของ TikTok
- แผงรายงานค้างที่ "กำลังส่งออก" ~3.5 นาที — แก้โดย reload หน้า (แผงไม่ refresh in place) แล้วปุ่ม "ดาวน์โหลด" จึงขึ้น
- ไม่ commit/push ให้ — เตรียม `push_now.command` ไว้ ต้องดับเบิลคลิกเองบนเครื่อง
