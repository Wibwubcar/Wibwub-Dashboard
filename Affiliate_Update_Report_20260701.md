# รายงานอัปเดต Affiliate Dashboard — 1 ก.ค. 2569 (รันอัตโนมัติ)

## สรุป
งาน `wibwub-thursday-affiliate` รันอัตโนมัติวันพุธที่ 1 ก.ค. 2569 ดึงข้อมูล TikTok Affiliate Center และอัปเดตแดชบอร์ดสำหรับเดือน **มิ.ย. 2569 (1–29)**

> **หมายเหตุเรื่องช่วงวันที่:** TikTok มี data lag — วันที่ 30 มิ.ย. ถูกปิด (greyed out) วันล่าสุดที่เลือกได้คือ 29 มิ.ย. และแดชบอร์ดไม่มีช่อง "ก.ค." จึงปิดยอดเดือน มิ.ย. ด้วยข้อมูลที่ครบที่สุด (1–29) แทนที่ยอดเดิม (1–28)

## ไฟล์ที่ดาวน์โหลด (4 ไฟล์)
บันทึกไว้ที่ `Data Affiliate/` (สำเนาต้นฉบับยังอยู่ใน Downloads เพราะ mount เป็น read-only)

| ไฟล์ | ขนาด |
|---|---|
| Transaction_Analysis_Creator_List_20260601-20260629.xlsx | 45 KB |
| Transaction_Analysis_Product_...20260629.xlsx | 13 KB |
| Transaction_Analysis_Video_...20260629.xlsx | 151 KB |
| Transaction_Analysis_Live_...20260629.xlsx | 11 KB |

## ตัวเลขหลัก — มิ.ย. 2569 (1–29)
| ตัวชี้วัด | เดิม (1–28) | ใหม่ (1–29) |
|---|---|---|
| Affiliate GMV | ฿580,142 | **฿607,557** |
| Net GMV (หลังคืนเงิน) | ฿571,872 | **฿598,495** |
| ค่าคอมมิชชั่น | ฿71,879 | **฿75,273** |
| Returns | ฿8.3K | ฿9.1K |
| ครีเอเตอร์ที่มียอด (GMV>0) | 371 | **383** |
| ครีเอเตอร์ Active (GMV ≥ ฿1K) | 81 | **83** |

> ตรวจสอบกับ KPI บนหน้า TikTok: GMV ฿607,301 / Comm ฿75,273.49 / Returns ฿9,061 — ตรงกับค่าที่คำนวณจากไฟล์

## Product cr/vid ที่อัปเดต (7 รายการ)
| สินค้า | cr (ครีเอเตอร์เฉลี่ย/วัน) | vid (วิดีโอ) |
|---|---|---|
| Leather Wipes | 14 | 21 |
| Interior Wipes | 17 | 110 |
| Sugar | 10 | 218 |
| Cleaner | 7 | 71 |
| Interior | 4 | 195 |
| Refresh | 3 | 39 |
| Visible | 2 | 24 |

## ไฟล์ที่แก้ไข
- `WIBWUB_Affiliate_Dashboard.html` — trend arrays (AF_GMV/AF_NET/AF_COM/AF_CR index 5 = มิ.ย.), KPI cards, note, PRODUCTS cr/vid, DATA comment
- `WIBWUB_Mobile.html` — AFI_GMV/AFI_NET/AFI_COMM index 7 = มิ.ย.; การ์ด Affiliate GMV ฿2.91M → ฿2.94M
- `sw.js` — cache version wibwub-v298 → v299
- `push_now.command` — อัปเดต commit message + จัด git add ไฟล์ที่ถูกต้อง (สำรองไฟล์ .bak_20260701_024718_run ไว้แล้ว)

## ขั้นตอนถัดไป (ต้อง manual)
ดับเบิลคลิก **`push_now.command`** เพื่อ commit + push ขึ้น GitHub Pages (สคริปต์รันไม่ได้แบบอัตโนมัติในเซสชันนี้ — ต้องรันบนเครื่องผู้ใช้)

## ข้อสังเกต / การตัดสินใจอัตโนมัติ
- ค่าที่เป็น cumulative (เช่น "ผ่าน 1,168 creators", "663 creators" บนมือถือ) **ไม่แก้** เพราะไม่ใช่ตัวเลขรายเดือน
- ยังไม่รวมข้อมูล Livestream ในตัวเลข GMV (คงเดิมตามโครงสร้างแดชบอร์ด)
- ไฟล์ Video/Live ดาวน์โหลดเก็บไว้แล้ว แต่ยังไม่ได้ประมวลผลเข้าแดชบอร์ด (นอกขอบเขต STEP ปัจจุบัน)
