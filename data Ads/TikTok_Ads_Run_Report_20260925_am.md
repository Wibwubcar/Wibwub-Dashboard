# TikTok Ads Download — 25 ก.ย. 2569 (รอบ 08:20 ICT เช้า)
📅 ช่วงข้อมูล: 01/09 – 25/09/2569 (25 ก.ย. เป็นข้อมูลบางส่วน)

✅ GMV Max: `Campaign overview data 20260901 - 20260926.xlsx` (คัดลอกไว้ที่ `TikTok/GMV Max/Campaign overview data 20260901 - 20260926 (0814).xlsx`)
   Total row: spend 674,434.27 / orders 11,876 / revenue 2,539,568.41 / ROI 3.77 / CPA 56.79
✅ Business Ads: `WIBWUBCAR-Campaign Report-2026-09-01 to 2026-09-25.xlsx` (คัดลอกไว้ที่ `TikTok/Business Ads/WIBWUBCAR-Campaign Report-2026-09-01 to 2026-09-25 (0816).xlsx`)
   Total of 97 results: spend 20,777.48 / imp 287,968 / clicks 3,575 (ผลรวม 6 แคมเปญที่มี spend = แถว Total ตรงทุกค่า — verified)

## Dashboard (WIBWUB_Ads_Dashboard.html)
- DATA_PERIODS.sep.tiktok: spend 695,211.75 · revenue 2,539,568.41 · orders 11,876 · ROAS 3.65 · CPA 58.54
- TK_BREAKDOWN.sep.gmvMax.total / bizAds.total + campaigns อัปเดต; gmvLive คงเดิม (0 = ยังไม่เก็บ, ไม่ถูกบวกซ้ำ)
- cover: tiktokDay 24 → 25, tiktokPull → 08:20 น.; shopeeDay/shopeePull ไม่แตะ (schedule นี้ไม่ได้ดึง Shopee)
- #ads-updated title prepend + AUDIT NOTE comments ใน gmvMax/bizAds เพิ่มแล้ว
- node --check ผ่านทั้งสองครั้ง (dry-run + ไฟล์จริง) · sw.js → wibwub-v1246
- Backup: WIBWUB_Ads_Dashboard.html.bak_20260925_tk

## หมายเหตุ
- Session TikTok Ads OK (ไม่ expired)
- LaunchAgent com.wibwub.download-mover ย้ายทั้ง 2 ไฟล์จาก Downloads เข้า `data Ads/TikTok/` ให้อัตโนมัติก่อนตรวจพบด้วยซ้ำ (ไม่ต้อง mv เอง) แล้ว copy ต่อเข้าโฟลเดอร์ย่อย GMV Max/ และ Business Ads/
- ไม่พบ .git lock ค้างจากรอบก่อน — คอมมิตได้ปกติ, push ต้องให้ user double-click `push_now.command`
