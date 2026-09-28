# WIBWUB Daily TikTok Followers — 9 ก.ย. 2026

## สรุป
ไม่มีข้อมูลใหม่ให้อัปเดต — dashboard ทั้งสองไฟล์ตรงกับข้อมูลล่าสุดของ TikTok อยู่แล้ว ไม่ได้แก้ไฟล์ ไม่ได้ bump sw.js ไม่ได้ commit

ข้อมูลวันสุดท้ายที่ TikTok ปิดยอดแล้ว (status 1) คือ **7 ก.ย. 2026 = 29,075 followers** ซึ่งเป็นค่าเดียวกับที่รอบวันที่ 8 ก.ย. เขียนลงไปแล้ว TikTok ยัง lag 2 วันเหมือนเดิม

## ค่าที่ตรวจสอบแล้วว่าถูกต้อง
- `WIBWUB_Dashboard.html` → `soc_follow` TikTok: `[23.404, 24.192, 24.967, 25.59, 26.339, 27.083, 27.834, 28.684, 29.075]`
- `WIBWUB_Dashboard.html` → `FOL_DATA` กันยายน 2569: start 28,684 → end 29,075, net +391 (+1.36%), รายวัน 1–7 ก.ย. ตรงกับ API ทุกค่า
- `WIBWUB_Mobile.html` → `TK_FOL` ปิดท้ายที่ 29,075, `mks-val` = 29.1K, `mks-sub` = +5.7K จาก ม.ค.

ยอดปลายเดือนจาก API ตรงกับ dashboard ครบทุกเดือน: ม.ค. 23,404 · ก.พ. 24,192 · มี.ค. 24,967 · เม.ย. 25,590 · พ.ค. 26,339 · มิ.ย. 27,083 · ก.ค. 27,834 · ส.ค. 28,684

## ปัญหาที่เจอ (เดิมซ้ำ) และวิธีแก้ที่ใช้รอบนี้
ปุ่ม "ดาวน์โหลดข้อมูล" ในหน้า TikTok Studio ยัง **ไม่ trigger การดาวน์โหลดไฟล์จริง** — กดสำเร็จ (dialog ปิด, เลือก CSV ได้) แต่ไม่มีไฟล์ตกลงใน Downloads เลย ตรงกับที่บันทึกไว้ใน `update_followers_api.py` และ `update_followers_api_20260830.py`

รอบนี้ดึงข้อมูลจาก insight API แทน และหา **endpoint/parameter ที่แน่นอนได้แล้ว** ควรใช้เป็นทางหลักในรอบถัดไป (เร็วกว่าและไม่ต้องพึ่งปุ่มดาวน์โหลด):

```
GET /tiktok/v1/analytics/insights/
    ?type_requests=[{"insight_type":160,"data_date_range":<R>}]
    &time_offset=25200&is_dark_mode=false
```

รันด้วย `fetch(..., {credentials:'include'})` จากในหน้า tiktok.com ที่ล็อกอินแล้ว

- `insight_type: 160` = `analytics_follower_total_followers` (ยอด follower สะสมรายวัน)
- `data_date_range`: `1` = 7 วัน, `2` = 28 วัน, `3` = 60 วัน, `4` = 365 วัน (ไม่ใช่จำนวนวันตรงๆ — ส่ง 60 จะได้แค่ 7 วัน)
- response: `analytics_follower_total_followers.list.value[]` แต่ละตัวมี `value` (ยอดสะสม) และ `message.timestamp` (UTC midnight — บวก 25200 ก่อนแปลงเป็นวันที่ไทย) กับ `message.status` (1 = ปิดยอดแล้ว, 2 = ยังไม่ final)

หมายเหตุอื่นที่เจอระหว่างทาง:
- `insight_type` แบบ string (`"follower_num_history"`) ที่ script เก่าเคยใช้ **ใช้ไม่ได้แล้ว** — API ตอบ `status_code: 5 Invalid parameters` ต้องใช้เลข 160
- การคลิกด้วยพิกัดใน Chrome MCP: พิกัดที่ tool รับเป็น CSS px แต่ screenshot ถูกสเกลขึ้น ~1.164 เท่า ต้องหารก่อนเสมอ ไม่งั้นคลิกผิดปุ่ม (รอบนี้เผลอเปิด dialog ดาวน์โหลดแทนที่จะเปิด date picker)
