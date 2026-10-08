# TikTok Ads Download — 2 ต.ค. 2569 (รอบเช้า 08:12 ICT)
📅 ช่วงข้อมูล: 01/10 – 02/10/2026 (2 ต.ค. ยังเป็นข้อมูลระหว่างวัน)

✅ GMV Max: Campaign overview data 20261001 - 20261002.xlsx
   Total row: spend 46,255.45 / 778 orders / revenue 162,986.50 / ROI 3.52 / CPA 59.45
✅ Business Ads: WIBWUBCAR-Campaign Report-2026-10-01 to 2026-10-02.xlsx
   97 campaigns (2 with spend); sum == "Total of 97 results": spend 1,232.32 / imp 15,160 / clicks 291
   (C-Ads TOP CREATOR 645.05 · 18.09.26/Followerพี่เป๊ก 587.27)

Dashboard:
- อัปเดตแล้วโดย session คู่ขนาน (commit 5005e6f, 08:14) — ตัวเลขตรงกับที่รอบนี้คำนวณเองทุกค่า
  DATA_PERIODS.oct.tiktok spend 47,487.77 / rev 162,986.50 / orders 778 / ROAS 3.43 / CPA 61.04; cover.tiktokDay=2
- รอบนี้จึงไม่แก้ไฟล์ซ้ำ / ไม่ commit ซ้ำ; ตรวจ node --check ผ่าน

หมายเหตุ:
- Business Ads export ไม่มีคอลัมน์ Campaign ID แล้ว — แถวรวมคือ "Total of 97 results", คอลัมน์ [4]=spend [7]=impressions [8]=clicks (ต่างจากที่ระบุใน task)
- ไฟล์ทั้งสองถูก LaunchAgent ย้ายจาก Downloads อัตโนมัติ (มีสำเนาที่ data Ads/TikTok/ ด้วย)
- schedule นี้ดูเหมือนถูกรันซ้ำ 2 session พร้อมกัน — ควรตรวจว่ามี scheduled task ซ้ำหรือไม่
- push ต้อง double-click push_now.command บน Mac
