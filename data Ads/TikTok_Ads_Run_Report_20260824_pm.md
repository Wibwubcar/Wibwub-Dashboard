# TikTok Ads Download — 24 ส.ค. 2569 (รอบ 19:20 ICT)

📅 ช่วงข้อมูล: 01/08/2569 – 24/08/2569 (⚠️ 24 ส.ค. ยังไม่เต็มวัน)

## สถานะการดาวน์โหลดไฟล์

⛔ **GMV Max — ดาวน์โหลดไม่สำเร็จ**
⛔ **Business Ads — ดาวน์โหลดไม่สำเร็จ**

Session TikTok Ads ยัง login อยู่ปกติ (Dashboard โหลดได้ ไม่ redirect ไป login) และหน้า
GMV Max / Campaigns แสดงข้อมูลช่วง 1–24 ส.ค. ครบถ้วน แต่ **ไฟล์ export ไม่ตกลง Downloads เลย**

สาเหตุที่ยืนยันได้จาก network log: ปุ่ม export ของ GMV Max ยิงงานสร้างไฟล์สำเร็จ แต่ URL
ไฟล์ปลายทางของ TikTok คืน **HTTP 503**:

```
GET https://ads.tiktok.com/wsos_v2/statistics/object/wsos6a8c3601b1984b15?expire=1787577539...
→ 503
```

`download_task/query` วนถามสถานะไม่จบ (poll ค้าง) ลองกด export ซ้ำ 4 ครั้ง (ทั้งคลิกจริงและ
คลิกผ่าน JS) ผลเหมือนเดิมทุกครั้ง ฝั่ง Business Ads กด More → Export data ก็ไม่มีไฟล์ตกเช่นกัน
สรุปว่าเป็นปัญหาฝั่ง service ของ TikTok ไม่ใช่ session หมดอายุ

**ไฟล์ล่าสุดที่ยังมีในโฟลเดอร์ (จากรอบ 01:26 ICT วันนี้):**
- `data Ads/TikTok/GMV Max/Campaign overview data 20260801 - 20260824.xlsx`
- `data Ads/TikTok/Business Ads/WIBWUBCAR-Campaign Report-2026-08-01 to 2026-08-24.xlsx`

## ข้อมูลที่ใช้แทน — อ่านตรงจากหน้าเว็บ

เพื่อไม่ให้ Dashboard ค้างข้อมูลเก่า จึงอ่านตัวเลขตรงจาก UI ของ TikTok Ads Manager แทน
แล้วตรวจสอบความสอดคล้องภายในก่อนนำไปใช้

### GMV Max Overview (UTC+07:00 Asia/Bangkok, 2026-08-01 → 2026-08-24)

| ตัวชี้วัด | ค่า |
|---|---|
| Cost | 494,633.86 THB |
| SKU orders | 8,978 |
| Cost per order | 55.09 THB |
| Gross revenue | 1,822,243.24 THB |
| ROI | 3.68 |

ตรวจสอบ: 494,633.86 ÷ 8,978 = 55.09 ✓ · 1,822,243.24 ÷ 494,633.86 = 3.68 ✓

เทียบกับ snapshot xlsx รอบ 01:26 น. (478,533.10 / 8,701 / 1,764,388.51) ส่วนต่าง
+16,100.76 spend, +277 orders, +57,854.73 revenue คือยอดที่วิ่งเพิ่มระหว่างวันของ 24 ส.ค.
ซึ่งสมเหตุสมผล

### Business Ads — Campaign table (Aug 1 → Aug 24, 92 แคมเปญ)

| แคมเปญ | Spend | Impressions | Clicks | CPM | CTR |
|---|---|---|---|---|---|
| C-Ads TOP CREATOR | 12,296.80 | 173,180 | 4,822 | 71.01 | 2.78% |
| CAds-Sugar | 355.77 | 6,168 | 128 | 57.68 | 2.08% |
| **รวม (Total of 92)** | **12,652.57** | **179,348** | **4,950** | **70.55** | **2.76%** |

มีแค่ 2 จาก 92 แคมเปญที่มี spend

ตรวจสอบ: spend 12,296.80 + 355.77 = 12,652.57 ตรงกับแถว Total เป๊ะ ✓ ·
impressions 173,180 + 6,168 = 179,348 ตรงเป๊ะ ✓ · clicks คำนวณย้อนจาก spend ÷ CPC
(destination) แล้วเช็คกลับ: 12,652.57 ÷ 4,950 = 2.556 → ตรงกับ CPC รวม 2.56 ที่หน้าเว็บแสดง ✓

## การอัปเดต WIBWUB_Ads_Dashboard.html

แก้ไขแล้ว (backup: `WIBWUB_Ads_Dashboard.html.bak_20260824_tk2`):

- `TK_BREAKDOWN.aug.gmvMax.total` → 494,633.86 / 8,978 / 1,822,243.24 / roi 3.68 / cpa 55.09
- `TK_BREAKDOWN.aug.bizAds.total` + campaigns → 12,652.57 / 179,348 imp / 4,950 clicks / cpm 70.55 / ctr 2.76
  (ชื่อแคมเปญแก้ให้ตรงกับหน้าเว็บด้วย: "C-Ads TOP CREATOR", "CAds-Sugar" แทนของเดิม
  "C-Ads TOP  CREATOR", "Cpass-Sugar")
- `DATA_PERIODS.aug.tiktok` → spend 507,286.43 (= gmvMax 494,633.86 + bizAds 12,652.57),
  revenue 1,822,243.24, orders 8,978, roas 3.59, cpa 56.50
- `TK_BREAKDOWN.all.gmvMax` / `.bizAds` → บวก delta ของ ส.ค. เข้าไป
- คอมเมนต์ source ทุกจุด + tooltip `#ads-updated` → ระบุว่ารอบนี้อ่านจากหน้าเว็บ เพราะ export 503

> หมายเหตุที่รักษาไว้ตามเดิม: ตัวเลข GMV Max Overview เป็นระดับ **shop-level** และรวม LIVE GMV Max
> อยู่แล้ว จึงห้ามบวก `gmvLive` ทับเข้าไปอีก · bizAds เป็น impression-based ไม่มี revenue/orders
> จึงบวกเฉพาะ spend เข้า TikTok total

### Validation

`node --check` ผ่านทั้ง script block ของ Dashboard และ `sw.js`
เขียน harness ตรวจความสอดคล้องของตัวเลข 14 ข้อ — **ผ่านทั้งหมด** (tiktok.spend = gmvMax + bizAds,
revenue/orders = GMV Max อย่างเดียว, cpa/roi/roas/cpm/ctr คำนวณกลับได้ตรง,
sum(campaigns) = total ทุกตัว)

### Git

- `sw.js` cache `wibwub-v804` → `wibwub-v805`
- commit `f3467da` (`sw.js` + `data Ads/WIBWUB_Ads_Dashboard.html`)
- ⚠️ **ยังไม่ push** — ต้อง double-click `push_now.command` เอง

## สิ่งที่ควรทำต่อ

1. ถ้ารอบถัดไป (พฤหัส 27 ส.ค.) export ยังคืน 503 อยู่ แปลว่าไม่ใช่ปัญหาชั่วคราว —
   ควรพิจารณาให้ schedule ดึงตัวเลขจาก UI เป็นทางหลักไปเลย แล้วเก็บ xlsx เป็น optional
2. ค่า `TK_BREAKDOWN.all` เป็นยอด all-time (รวมแคมเปญปี 2024–2025) ไม่ใช่ผลรวม ม.ค.–ส.ค. 2569
   แต่ `ADS_PERIOD_DEFS.all` ใช้ keys `['jan'..'aug']` — สอง bucket นี้นิยามไม่ตรงกัน
   รอบนี้จึงบวกแบบ delta ไว้ก่อนตามแนวทางเดิม แต่ควรตัดสินใจให้ชัดว่าจะเอาแบบไหน
3. ตัวเลข 24 ส.ค. ยังไม่เต็มวัน — รอบพรุ่งนี้จะได้ยอดเต็ม
