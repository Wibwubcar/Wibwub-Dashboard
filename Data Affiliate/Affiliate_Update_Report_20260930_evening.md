# ✅ WIBWUB Affiliate Update — 30 ก.ย. 2569 (21:30, scheduled: wibwub-thursday-affiliate)

📅 ช่วงข้อมูล: 1/9 – 28/9/2569 (TikTok อัปเดตข้อมูลถึง 28 ก.ย. 0:00 — 29–30 ก.ย. ยัง greyed out)

## 📁 ไฟล์ (export ใหม่ แล้ว LaunchAgent ย้ายจาก Downloads อัตโนมัติ)
- ครีเอเตอร์/ ← Transaction_Analysis_Creator_List_20260901-20260928.xlsx
- สินค้า/     ← Transaction_Analysis_Product_List_20260901-20260928.xlsx
- วีดีโอ/     ← Transaction_Analysis_Video_List_20260901-20260928.xlsx
- ไลฟ์สตรีม/ ← Transaction_Analysis_Live_List_20260901-20260928.xlsx

## 📊 ก.ย. (1-28)
- GMV ฿1,996,363 · Net ฿1,960,601 · Comm ฿220,981 · Creators 1,031
- AF_* / AFI_* มีค่าชุดนี้อยู่แล้ว (run ก่อนหน้าวันนี้เขียนไว้แต่ยังไม่ commit) → ตรวจแล้วตรงทุกตัว ไม่ต้องแก้เพิ่ม
- ใช้ index คอลัมน์ตามชื่อหัวตาราง (GMV=col1, คืนเงิน=col4, ค่าคอม=col21, ข้ามแถวคำอธิบาย) — index ใน task file (2/10) ใช้กับ export รูปแบบใหม่ไม่ได้แล้ว

## 🛒 PRODUCTS vid (map ตามรหัส SKU)
- Leather Wipes 516→528 · Sugar 233→237 · Interior wipes 258→265 · Interior 106→109 (CLEANER 31, Visible 23 ไม่เปลี่ยน)
- `cr` ไม่แตะ — export ไม่มีคอลัมน์ "ครีเอเตอร์ที่มียอดขาย" แบบยอดรวม (มีแต่ค่าเฉลี่ยรายวัน) เหมือน run ก่อน ๆ

## 🎬 VIDEOS
- อัปเดต 102 รายการ, เพิ่มใหม่ 71 รายการ (รวม 10,106) — parse ครบ 10,035/10,035 entry เดิม, node eval ผ่าน, diff ~1.7% ของไฟล์
- 71 รายการใหม่บางส่วนมี product = 'Unknown' (map รหัสสินค้าไม่ได้) — รวมทั้ง array มี 'Unknown' 35 รายการ

## ⚙️ sw.js: v1333 → v1334
📌 ดับเบิ้ลคลิก push_now.command เพื่อ push (WIBWUB_Affiliate_Dashboard.html, WIBWUB_Mobile.html, sw.js)

## ⚠️ ควรทราบ
- Export จาก TikTok ค้างสถานะ "กำลังส่งออก" จนกว่าจะ reload หน้า — หลัง reload ไฟล์พร้อมดาวน์โหลดทันที
- push_now.command เดิม (ของ run สต๊อก) ถูกเขียนทับตาม task — commit สต๊อกนั้นเสร็จไปแล้ว (b20a71c) แต่ `Data Shipnity/stock/stock_snapshot.json` และไฟล์อื่นที่ไม่เกี่ยวยังมีการแก้ที่ยังไม่ commit
