# ✅ WIBWUB Affiliate Update — 2026-08-24 (จันทร์)
📅 ช่วงข้อมูล: 01/08/2026 – 22/08/2026 (23–24 ส.ค. ยังไม่เปิดให้เลือก)

## 📁 ไฟล์ที่ดาวน์โหลด + ย้ายแล้ว
| Tab | ไฟล์ | ปลายทาง |
|---|---|---|
| ครีเอเตอร์ | Transaction_Analysis_Creator_List_20260801-20260822.xlsx | Data Affiliate/ครีเอเตอร์/ |
| สินค้า | Transaction_Analysis_Product_List_20260801-20260822.xlsx | Data Affiliate/สินค้า/ |
| วีดีโอ | Transaction_Analysis_Video_List_20260801-20260822.xlsx | Data Affiliate/วีดีโอ/ |
| ไลฟ์สตรีม | Transaction_Analysis_Live_List_20260801-20260822.xlsx | Data Affiliate/ไลฟ์สตรีม/ |

## 📊 ตัวเลข ส.ค. (1–22)
- GMV: ฿1,172,768 (เดิม ฿1,120,368 → +฿52,400)
- Net GMV: ฿1,151,786
- Commission: ฿136,066
- Creators ที่มียอด: 612 (เดิม 583)

## 🔧 ที่แก้ในไฟล์
- `WIBWUB_Affiliate_Dashboard.html` — AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR index 7 (ส.ค.), label → "ส.ค. (1-22)", KPI ครีเอเตอร์ที่มียอด 612
- `WIBWUB_Mobile.html` — AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM index 9, KPI ฿1,172K · 612 creators · สค.69 (1-22)
- `PRODUCTS` cr/vid: Leather 39/36, Interior Wipes 23/22, Sugar 14/15, Cleaner 6/6, Interior 5/5, Visible 2/1 (Refresh ไม่มีในไฟล์ export รอบนี้ → คงค่าเดิม 4/4)
- `VIDEOS`: อัปเดต 71 รายการ, เพิ่มใหม่ 103 รายการ → รวม 6,610 (verify ด้วย node ผ่าน)
- `sw.js`: v807 → v808

## ⚠️ หมายเหตุการรันรอบนี้
- Column layout ของไฟล์ ครีเอเตอร์ เปลี่ยนจากที่ SKILL ระบุ: commission อยู่ **col 21** (ไม่ใช่ col 10) และมี header 2 แถว (ต้อง `iloc[2:]` ไม่ใช่ `iloc[1:]`) — ใช้ column ใหม่แล้วในรอบนี้
- ไฟล์ สินค้า: cr = col 19 (ครีเอเตอร์ที่มียอดขายเฉลี่ยรายวัน), vid = col 13 (วิดีโอที่มียอดขายเฉลี่ยรายวัน)
- `navigate` แบบ browser_batch ใช้ไม่ได้กับ tab ว่าง — ต้องเรียก navigate standalone ครั้งแรก

## 📌 ขั้นตอนถัดไป
ดับเบิ้ลคลิก `push_now.command` เพื่อ push ขึ้น GitHub
