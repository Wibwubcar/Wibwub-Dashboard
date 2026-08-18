TikTok Ads Download — 11/08/2569

📅 ช่วงข้อมูล: 01/08 – 11/08

✅ GMV Max: Campaign overview data 20260801 - 20260811.xlsx (สเปนด์ 218,480.80 บาท / 4,022 ออเดอร์ / ยอดขาย 837,366.11 บาท / ROI 3.83)

✅ Business Ads: WIBWUBCAR-Campaign Report-2026-08-01 to 2026-08-11.xlsx (สเปนด์ 5,214.42 บาท / อิมเพรสชัน 79,779 / คลิก 2,870, แคมเปญ "C-Ads TOP CREATOR" เท่านั้นที่มีสเปนด์)

หมายเหตุ:
- อัปเดต WIBWUB_Ads_Dashboard.html แล้ว: DATA_PERIODS.aug.tiktok (สเปนด์รวม 223,695.22 / ยอดขาย 837,366.11 / 4,022 ออเดอร์ / ROAS 3.74 / CPA 55.62), TK_BREAKDOWN.aug.gmvMax และ .bizAds, badge #ads-updated, ป้าย pb-sub และ ADS_PERIOD_DEFS.aug (TikTok ครบ 1-11 แล้ว)
- ตรวจสอบความสอดคล้องแล้ว: tiktok.spend = gmvMax.spend + bizAds.spend, tiktok.revenue/orders = gmvMax (gmvLive ไม่มีข้อมูลเดือนนี้)
- ตรวจ JS ด้วย node --check ผ่าน, bump sw.js เป็น wibwub-v636
- ปุ่ม "View report" เปิดพาเนล "Generate a reporting summary" (Beta) แทนการดาวน์โหลดตรง — ใช้เมนู More → Export data แทน จึงได้ไฟล์ครบตามชื่อเดิม
- ⚠️ Git commit ทำไม่สำเร็จ: .git/index.lock ค้างอยู่ในสภาพแวดล้อม sandbox (ลบ/rename ไม่ได้ — permission denied แม้เป็นไฟล์ของตัวเอง) เป็นปัญหาเดิมที่เคยเกิดซ้ำหลายรอบก่อนหน้านี้ (พบไฟล์ index.lock.bak/.stale/.old หลายสิบไฟล์จากรันก่อนๆ) ไฟล์ WIBWUB_Ads_Dashboard.html และ sw.js ถูกบันทึกลงดิสก์ถูกต้องแล้ว แต่ยังไม่ได้ commit เข้า git — รอ auto-push script ฝั่ง Mac รอบถัดไป หรือผู้ใช้กด push_now.command เอง
