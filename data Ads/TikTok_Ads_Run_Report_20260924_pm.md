# TikTok Ads Download — 24 ก.ย. 2569 (รอบ 19:12 ICT)
📅 ช่วงข้อมูล: 01/09 – 24/09/2569 (24 ก.ย. เป็นข้อมูลบางส่วน)

✅ GMV Max: `Campaign overview data 20260901 - 20260924 (1912).xlsx`
   Total row: spend 662,463.50 / orders 11,710 / revenue 2,503,082.03 / ROI 3.78 / CPA 56.57
✅ Business Ads: `WIBWUBCAR-Campaign Report-2026-09-01 to 2026-09-24 (1913).xlsx`
   Total of 97 results: spend 20,189.16 / imp 283,273 / clicks 3,518 (ผลรวม 6 แคมเปญที่มี spend = แถว Total ตรงทุกค่า)

## Dashboard (WIBWUB_Ads_Dashboard.html)
- DATA_PERIODS.sep.tiktok: spend 682,652.66 · revenue 2,503,082.03 · orders 11,710 · ROAS 3.67 · CPA 58.30
- TK_BREAKDOWN.sep.gmvMax.total / bizAds.total + campaigns อัปเดต; gmvLive คงเดิม (0 = ยังไม่เก็บ)
- cover: tiktokPull → 19:12; shopeeDay 23 → 24 (ข้อมูล Shopee ใน DATA_PERIODS ครอบคลุม 1-24 แล้วจากรอบ 19:03 แต่ cover ยังค้างที่ 23)
- #ads-updated title + static fallback text อัปเดต
- node --check ผ่าน · sw.js → wibwub-v1239 · commit 41cd48d
- Backup: WIBWUB_Ads_Dashboard.html.bak_20260924_tk_pm

## ⚠️ ต้องทำเอง
- git ทิ้ง `.git/HEAD.lock` ไว้ (sandbox ลบไม่ได้ และคำขอสิทธิ์ลบถูกปฏิเสธอัตโนมัติเพราะเป็นรอบ schedule) → ลบไฟล์นี้ก่อน git ครั้งถัดไป แล้ว double-click `push_now.command`
