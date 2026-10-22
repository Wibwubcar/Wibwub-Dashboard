# ✅ WIBWUB Affiliate Update — 2 ต.ค. 2569 (09:05, scheduled: wibwub-thursday-affiliate)

📅 ช่วงข้อมูล: 1/9 – 29/9/2569 — TikTok อัปเดตข้อมูลถึง 29 ก.ย. 0:00; ทุกวันของ ต.ค. ยัง greyed out → ไม่มีข้อมูลเดือน ต.ค. ให้ดึง จึงอัปเดตเดือน ก.ย. (index สุดท้าย) แทน ไม่ได้เพิ่มเดือน ต.ค.

## 📁 ไฟล์ (export ใหม่ 02 ต.ค. 08:58 → LaunchAgent ย้ายจาก Downloads อัตโนมัติ)
- ครีเอเตอร์/ ← Transaction_Analysis_Creator_List_20260901-20260929.xlsx
- สินค้า/     ← Transaction_Analysis_Product_List_20260901-20260929.xlsx
- วีดีโอ/     ← Transaction_Analysis_Video_List_20260901-20260929.xlsx
- ไลฟ์สตรีม/ ← Transaction_Analysis_Live_List_20260901-20260929.xlsx
(ชื่อซ้ำกับไฟล์ export วันที่ 1 ต.ค. → ถูกเขียนทับด้วยไฟล์ใหม่ ช่วงข้อมูลเท่าเดิม)

## 📊 ก.ย. (1-28) → (1-29)
- GMV ฿1,996,363 → ฿2,124,239 · Net ฿1,960,601 → ฿2,086,608 · Comm ฿220,981 → ฿235,155 · Creators 1,031 → 1,072
- อัปเดต AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR และ AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM/AFI_CR (index สุดท้าย = ก.ย.)
- ตรวจวิธีคำนวณกับไฟล์ 1-28 แล้วได้ตรงกับค่าเดิมใน dashboard ทุกตัว; GMV ตรงกับหน้า TikTok (฿2,124,238.60)
- ใช้คอลัมน์ตามชื่อหัวตาราง (GMV / การคืนเงิน / ค่าคอมมิชชั่นโดยประมาณ) ข้ามแถวคำอธิบาย — index ใน task file ใช้กับ export รูปแบบใหม่ไม่ได้

## 🛒 PRODUCTS vid (map ตามรหัสสินค้า)
- Leather Wipes 528→552 · Interior wipes 265→277 · Sugar 237→242 · CLEANER 31→32 · Interior 109→112 · Visible 23→24
- `cr` ไม่แตะ (export มีแต่ "ครีเอเตอร์ที่มียอดขายเฉลี่ยรายวัน" ไม่มียอดรวม) เหมือน run ก่อน ๆ

## 🎬 VIDEOS (monthly key = sep)
- อัปเดต 140 รายการ, เพิ่มใหม่ 94 รายการ (รวม 10,200) — parse ครบ 10,106/10,106 entry เดิม, node eval ผ่าน, diff ~3% ของไฟล์, ไม่มี 'Unknown' ใหม่
- ใช้ key `sep` (เดือนของข้อมูล) ไม่ใช่ `oct` ตาม date.today() — ไม่งั้นยอด ก.ย. จะไปลงช่อง ต.ค.

## ⚙️ sw.js: v1366 → v1367
📌 ดับเบิ้ลคลิก push_now.command เพื่อ commit + push (WIBWUB_Affiliate_Dashboard.html, WIBWUB_Mobile.html, sw.js)
