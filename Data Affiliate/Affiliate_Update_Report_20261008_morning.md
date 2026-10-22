# WIBWUB Affiliate Update — 2026-10-08 (morning, scheduled)

📅 ช่วงข้อมูล: 1/10 – 5/10/2026 (TikTok อัปเดตล่าสุด 5 ต.ค. 0:00 — ยังไม่มีข้อมูลใหม่กว่านี้)

## ไฟล์ที่ได้ (LaunchAgent ย้ายจาก Downloads อัตโนมัติ)
- ครีเอเตอร์/ ← Transaction_Analysis_Creator_List_20261001-20261005.xlsx
- สินค้า/ ← Transaction_Analysis_Product_List_20261001-20261005.xlsx (+ "(1)" ซ้ำ)
- วีดีโอ/ ← Transaction_Analysis_Video_List_20261001-20261005 (2).xlsx (+ "(1)" ซ้ำ)
- ไลฟ์สตรีม/ ← Transaction_Analysis_Live_List_20261001-20261005.xlsx (+ "(1)" ซ้ำ)

## ผลลัพธ์
- GMV ฿616,124 · Net ฿606,030 · Comm ฿64,467 · Creators 424 — **ตรงกับค่าใน AF_*/AFI_* (ต.ค. 1-5) อยู่แล้ว → ไม่ได้แก้**
- Products cr/vid: ข้อมูลต้นทางเหมือนรอบก่อน → ไม่ได้แก้
- VIDEOS: อัปเดต 0, เพิ่มใหม่ 0 (รวม 10,808) → ไม่ได้แก้ (สคริปต์จะเปลี่ยนแค่ label date ของ 133 แถวที่ GMV=0 จาก 'ต.ค.' เป็น '' จึง revert ไว้)
- sw.js: v1482 → v1483
- push_now.command: เขียนใหม่ให้มี git add + commit + push (ไฟล์เดิมมีแค่ push แต่ WIBWUB_Affiliate_Dashboard.html ยังมีการแก้ไขค้างจากรอบเมื่อคืนที่ยังไม่ commit)

## ⚠️ หมายเหตุ
- คอลัมน์ในไฟล์ครีเอเตอร์เปลี่ยนจากที่ STEP 4 ระบุ: returns = col[4] (การคืนเงิน), commission = col[21] (ค่าคอมมิชชั่นโดยประมาณ), และ row 2 เป็นแถวคำอธิบาย ต้อง skip 2 แถว — ควรอัปเดต task file
- ไฟล์สินค้าไม่มีคอลัมน์ "ครีเอเตอร์…ขาย" แบบยอดรวม (มีแต่ค่าเฉลี่ยรายวัน) — logic STEP 5 จะ match ได้ไม่ถูก
- 📌 ดับเบิ้ลคลิก push_now.command เพื่อ push ขึ้น GitHub
