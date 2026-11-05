---
name: wibwub-ads-detail
description: ส่วน B ของงาน local wibwub-samp-request-sync (11:05 รอบเช้ารอบเดียว) — โหลดรายงานโฆษณาเชิงลึก 4 ช่องทาง → ads_detail_*.json
---

# ═══════════ ส่วน B — แอดละเอียด 4 ช่องทาง ═══════════

> 🔒 **กฎเหล็กของส่วนนี้ อ่านก่อนเปิดหน้าเว็บทุกครั้ง**
>
> - **โหลดรายงานอย่างเดียว ห้ามกดปุ่มอื่นใด** ในหน้าโฆษณาของทุกช่องทาง
>   ห้ามแก้แคมเปญ งบ ราคาประมูล สถานะ ROAS เป้าหมาย หรือสร้างอะไรใหม่
> - **ป๊อปอัปให้ปิดด้วย X หรือ Escape เท่านั้น** ห้ามกด "เข้าร่วมเลย" / "เติมยอด" /
>   "เพิ่มงบประมาณ" / "รับทราบ" · ป๊อปอัปไม่บล็อก fetch ถ้าปิดไม่ได้ก็ดึงข้อมูลต่อได้
> - **ห้ามแตะเรื่องเงินทุกชนิด** ยอดคงเหลือในบัญชีแอดติดลบเป็นเรื่องปกติ **ปล่อยไว้**
>   ห้ามเติมเงิน ห้ามเปิดเติมเงินอัตโนมัติ
> - **ห้ามกรอกรหัสผ่าน** ถ้าหลุดหน้า login ให้หยุดช่องทางนั้นแล้วรายงาน ทำช่องทางถัดไปต่อ
> - รายงาน TikTok 3 ชุดที่สร้างไว้แล้ว **ห้ามสร้างใหม่ ห้ามแก้ ห้ามเปิด Scheduled running**
>   ถ้าหาไม่เจอให้หยุดแล้วแจ้ง **ห้ามสร้างซ้ำ**

> ⛔ **ส่วน B ล้ม ห้ามทำให้ส่วน A ขึ้นว่าล้มเหลว** — รายงานแยกหัวข้อเสมอ
> ส่วน A (คำขอสินค้า) จบแล้วถือว่าสำเร็จของมันเอง

## B0 — ทำต่อเมื่อส่วน A จบแล้ว และเฉพาะรอบเช้า

```bash
python3 "<BASE>/scripts/ads/detail_plan.py"
```

- `skip: true` (exit 3) → **ข้ามส่วน B ทั้งหมด** รายงาน `ℹ️ ข้ามส่วน B — <reason>` แล้วจบ
  (รอบ 22:05 เป็นรอบข้ามเสมอ งานนี้ทำวันละรอบเดียว)
- `skip: false` (exit 0) → ทำต่อ · ใช้ `from`/`to` ที่มันคืนมา **ย้อนหลัง 7 วันเสมอ**
  เพราะ Facebook แก้ตัวเลขย้อนหลัง และ Shopee ปิดยอดของวันปัจจุบันช้า

## B1 — Facebook (5 บัญชี × 3 ระดับ)

```bash
python3 "<BASE>/scripts/ads/fb_plan_detail.py" --levels ad,age_gender,placement
```

เปิด `urls.<ระดับ>` ของแต่ละบัญชีแล้วกด **ดรอปดาวน์ข้างปุ่ม export → "ส่งออกเป็น .csv"**
(2 คลิกนี้เท่านั้นที่อนุญาตในหน้า Ads Manager)

ไฟล์ที่ได้ชื่อซ้ำกันทุกบัญชี ให้ `fb_collect.py` จัดการเหมือนงาน 08:15 ไม่ได้ —
ส่วนนี้ให้ **ตั้งชื่อตอนโหลดเอง** เป็น `WIBWUB-auto-fb-<บัญชี>-<ระดับ>-<from>_<to>.csv`
ตัวย้ายจะพาไป `data Ads/facebook/detail_raw/` ให้เอง

## B2 — TikTok (เปิดรายงานที่มีอยู่ + export เท่านั้น)

| รายงาน | reportId |
|---|---|
| `WIBWUB auto – ad daily` | 7704617861406916628 |
| `WIBWUB auto – audience daily` | 7704621165457145877 |
| `WIBWUB auto – placement daily` | 7704624169216327700 |

เปิด `https://ads.tiktok.com/i18n/reporting/pivot/table/edit?reportId=<id>&aadvid=7229166192752148482`
→ ปุ่ม **Export** → ตั้งชื่อ `WIBWUB-auto-ad-daily` / `-audience-daily` / `-placement-daily` → **CSV**

ช่วงของรายงานตั้งเป็น **Last 7 days** ไว้แล้ว ไม่ต้องแตะตัวเลือกวันที่

## B3 — Shopee (API ไม่ต้องกดปุ่มในหน้า)

ที่ `https://seller.shopee.co.th/portal/marketing/pas/index` ยิง same-origin ทีละวัน
(**ยิงพร้อมกันไม่ได้ ตัวที่ 2 จะตอบ `too many export requests`** ต้องรอให้ตัวแรกเสร็จก่อน)

```
POST /api/pas/v1/report/export_job/trigger/?SPC_CDS_VER=2
     {"language":"th","report_type":"<ชนิด>","start_time":<epoch 00:00 ของวันนั้น>,"end_time":<epoch 23:59:59 ของวันเดียวกัน>}
  -> poll /api/pas/v1/report/export_job/list_homepage_result/?page_number=1&page_size=5 จน status=="success"
  -> POST /api/pas/v1/report/export_job/get_download_url/?SPC_CDS_VER=2  {"export_id":<id>}
  -> โหลดด้วย Blob + <a download> ตั้งชื่อ WIBWUB-auto-shopee-<ชนิด>-<YYYYMMDD>.csv
```

ชนิดที่ต้องดึง **ทุกวันในช่วง**: `new_cpc_homepage__detail` (คีย์เวิร์ด + รายสินค้า) ·
`product_gms__homepage` (GMV Max รายสินค้า)

> ⚠️ **ชื่อไฟล์ห้ามขึ้นต้นด้วย `ข้อมูล-Shopee-Ads-`** ไม่งั้นตัวย้ายจะส่งไปปนกับงานรายวัน
> ⚠️ ต้องลงท้ายด้วย `_YYYYMMDD` ของวันเดียว — `detail_build.py` อ่านวันที่จากชื่อไฟล์

## B4 — Lazada (API ล้วน)

ที่ `https://sellercenter.lazada.co.th/sponsor/solutions/ads/smax/#!/home` ยิงทีละวัน

```
GET /sponsor/solutions/performance/newCampaignList.json?page=1&pageSize=100&campaignStatus=2&startDate=<d>&endDate=<d>&sceneId=<12020..12024>&attributionType=2
GET /sponsor/solutions/performance/adgroupList.json?adName=&startDate=<d>&endDate=<d>&adStatus=-1&page=1&pageSize=200&sortable=storeRevenue,desc&attributionType=2&sceneId=<id>
```

รวมผลเป็น `{<sceneId>:{camp:[...],ads:[...]}}` แล้วโหลดเป็น `WIBWUB-auto-lazada-<YYYYMMDD>.json`
(ชื่อสินค้าอยู่ที่ `adgroupName` **ไม่ใช่** `itemName` ซึ่งเป็น null เสมอ)

## B5 — สร้าง JSON + ด่านชื่อคน

```bash
python3 "<BASE>/scripts/ads/detail_build.py"
```

- exit 0 = เขียนครบและ**ผ่านด่านชื่อคนแล้ว** · exit 10 = ไม่มีไฟล์ดิบ · **exit 2 = เจอชื่อคน
  ไฟล์ถูกลบทิ้งแล้ว ห้าม commit** ให้รายงานว่าเจอที่ไหน
- สคริปต์แทนชื่อแอด TikTok ด้วยเลขคงที่ให้เองทุกรอบ ตารางจับคู่อยู่นอก git
  **ห้ามพิมพ์ชื่อจริงของครีเอเตอร์ลงรายงานท้ายรอบ**

## B6 — commit

```bash
python3 "<BASE>/scripts/bump_sw.py"
python3 "<BASE>/scripts/gitw.py" add "data Ads/ads_detail_fb.json" "data Ads/ads_detail_tk.json" "data Ads/ads_detail_sh.json" "data Ads/ads_detail_lz.json" "data Ads/WIBWUB_Ads_Dashboard_redesign.html" WIBWUB_Dashboard.html sw.js
python3 "<BASE>/scripts/gitw.py" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" commit -m "auto: แอดละเอียด 4 ช่องทาง <วันที่วันนี้แบบตัวอักษร เช่น 2026-11-06>"
```

ไฟล์ดิบใน `detail_raw/` ไม่เข้า git (`.gitignore` ครอบ `*.csv` อยู่แล้ว)

## สรุปส่วน B (ภาษาไทย)

ช่องทางไหนได้/ไม่ได้ · ช่วงวันที่ · จำนวนแถวของแต่ละช่องทาง · ค่าแอดรวมรายช่องทาง ·
ด่านชื่อคนผ่านหรือไม่ · commit id · ถ้าช่องทางไหนล้มให้บอกว่าข้อมูลเดิมอยู่ถึงวันไหน

**ห้ามเขียน ✅ ถ้ามีช่องทางใดล้ม** ให้ขึ้น `⚠️ ได้ N/4 ช่องทาง` แทน
