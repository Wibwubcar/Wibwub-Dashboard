# TikTok Ads Download — 23 ก.ย. 2569 (รอบ 19:15 ICT)
📅 ช่วงข้อมูล: 01/09 – 23/09/2569 (23 ก.ย. เป็นข้อมูลบางส่วน)

✅ GMV Max: `Campaign overview data 20260901 - 20260923.xlsx`
   Total row: spend 634,060.82 / orders 11,224 / revenue 2,413,400.32 / ROI 3.81 / CPA 56.49
✅ Business Ads: `WIBWUBCAR-Campaign Report-2026-09-01 to 2026-09-23 (1915).xlsx`
   (ใส่ suffix เพราะชื่อเดิมมีไฟล์รอบเช้าอยู่แล้ว) Total of 97 results: spend 19,022.73 / imp 271,736 / clicks 3,372
   ผลรวม 6 แคมเปญที่มี spend = แถว Total ตรงทุกค่า

## Dashboard (WIBWUB_Ads_Dashboard.html)
- DATA_PERIODS.sep.tiktok: spend 653,083.55 (GMV Max + BizAds) · revenue 2,413,400.32 · orders 11,224 · ROAS 3.70 · CPA 58.19
- TK_BREAKDOWN.sep.gmvMax.total / bizAds.total + campaigns อัปเดต; gmvLive คงเดิม (0 = ยังไม่เก็บ)
- cover.tiktokPull + title ของ #ads-updated อัปเดต; ยอดใน .pb-sub คำนวณจาก DATA_PERIODS ตอนโหลดหน้าอยู่แล้ว
- node --check ผ่าน · sw.js → wibwub-v1222 · commit fb86e41
- Backup: WIBWUB_Ads_Dashboard.html.bak_20260923_tk_pm

## หมายเหตุ
- LaunchAgent ย้ายไฟล์จาก Downloads ไป `data Ads/TikTok/` ทันที (ก่อนที่ sandbox จะเห็น) → copy จากที่นั่นไปโฟลเดอร์ย่อยแทน
- Business Ads export: ใช้ More → Export data ("View report" เปิดแผงสรุป AI ไม่ใช่ export)
- Column layout ของ Business Ads เปลี่ยนจากที่ระบุไว้ใน task: [0]=name, [4]=spend, [7]=imp, [8]=clicks, ไม่มี Campaign ID
- ต้อง double-click `push_now.command` เพื่อ push
