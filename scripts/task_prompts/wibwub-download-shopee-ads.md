---
name: wibwub-download-shopee-ads
description: ทุกวัน 08:00/19:00 — โหลด Shopee Ads CSV → อัปเดต DATA_PERIODS.<เดือน>.shopee ใน Ads Dashboard
---

## WIBWUB — Shopee Ads รายวัน

BASE = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`

URL: `https://seller.shopee.co.th/portal/marketing/pas/index`
(ใช้ไม่ได้: `/portal/marketing/ads`, `/portal/download-centre`, `/portal/marketing/shopee-ads/report`)

---

## ขั้นที่ 1 — โหลด CSV ผ่าน API (ไม่ต้องกดปุ่มในหน้า)

1. Chrome: `list_connected_browsers` → `select_browser` deviceId `b75a6bb0-5b78-4e44-92a8-75224f1ce4ee` → `tabs_context_mcp(createIfEmpty=true)`
2. navigate ไป URL ข้างบน · ถ้าขึ้นหน้า login: **หยุดและรายงาน ห้ามกรอกรหัสผ่าน**

> 🚨 **ห้ามคลิกปุ่ม "ดาวน์โหลด" ของ Shopee ในหน้าเว็บ**
> ไม่ใช่เพราะ popup blocker (ข้อมูลเดิมผิด — ปุ่มทำงานปกติ) แต่เพราะ **Shopee ตั้งชื่อไฟล์
> เหมือนกันทุกครั้ง** (`ข้อมูล-Shopee-Ads-<from>-<to>.csv`) การกดปุ่มจะโหลดไฟล์ชื่อซ้ำ
> มาทับของรอบก่อนที่เนื้อหาต่างกัน — เกิดจริงเมื่อ 20 ต.ค. 2569 (ไฟล์ product-only
> ของรอบ 08:23 ถูกไฟล์ all-ads ทับ) ตอนนี้ `safe_mv()` ใน `wibwub_auto_move.sh`
> กันไม่ให้หายแล้ว แต่ก็ยังทำให้ไฟล์รกและชื่อไม่ตรงเนื้อหา

ยิง API ตรงใน `javascript_tool` (same-origin ไม่ต้องใช้ signature):

```
GET  /api/pas/v1/report/export_job/list_homepage_result/?page_number=1&page_size=10
     -> หา export_id ที่ status พร้อมแล้ว (fields: export_id, status, timestamp, file_name, progress)

POST /api/pas/v1/report/export_job/get_download_url/?SPC_CDS_VER=2
     body: {"export_id": <id>}
     -> คืน URL ไฟล์
```

(`direct_download` ที่พรอมป์เก่าพูดถึงตอบ 400 / `code 450` ใช้ไม่ได้)

ถ้ายังไม่มี export พร้อม ให้สั่งสร้างรายงานใหม่ในหน้า (เลือก **"ภาพรวมข้อมูลโฆษณา"**)
แล้วรอ ~10 วินาที · panel "รายงานล่าสุด" **เปิดเอง ไม่ต้องคลิกไอคอน "≡"**

3. โหลดไฟล์ด้วย Blob + `<a download>` และ **ตั้งชื่อให้ unique เสมอ**
   เช่น `shopee-ads-<from>-<to>-cpc-allads__<YYYYmmdd_HHMM>.csv`
4. ปิดแท็บด้วย `tabs_close_mcp`
5. หาไฟล์ (LaunchAgent `com.wibwub.download-mover` ย้ายให้ภายใน **~1 นาที** ไม่ใช่ 5–10 นาที):

```bash
ls -t /Users/thanasablilutanon/Downloads/*Shopee-Ads*.csv \
      "$BASE/data Ads/Shopee"/*Shopee-Ads*.csv 2>/dev/null | head -3
```

## ขั้นที่ 2 — อัปเดต Ads Dashboard

อ่าน CSV ล่าสุดใน `data Ads/Shopee/` — header จริงอยู่แถวที่มีคำว่า `ลำดับ` (skip 7 บรรทัดแรก)

คอลัมน์ (ตรวจแล้ว 20 ต.ค. ถูกทุกตัว):

| index | ความหมาย |
|---|---|
| 11 | การมองเห็น (impression) |
| 12 | จำนวนคลิก |
| 16 | การสั่งซื้อ |
| 24 | ยอดขาย |
| 26 | ค่าโฆษณา |
| 27 | ROAS |

> **ใช้ยอด all-CPC ไม่ใช่ product-only** — แท็บ "โฆษณาสินค้า" บนหน้าเว็บจะโชว์เลขต่ำกว่า
> เพราะไม่รวม GMV Max และโฆษณาร้านค้า ถ้า cross-check แล้วไม่ตรงนี่คือสาเหตุ ไม่ใช่บั๊ก

1. Sum เป็นยอดรวมเดือนปัจจุบัน + สร้าง top5 / worst5 / all campaigns
2. **ถ้าค่าที่คำนวณได้เท่ากับของเดิมทุกตัว → หยุดตรงนี้** ไม่ต้องเขียน ไม่ bump sw.js ไม่ commit
   (รอบ 19:00 จะเจอเคสนี้บ่อยถ้า Shopee ยังไม่อัปเดตข้อมูล)
3. แก้ `DATA_PERIODS.<เดือน>.shopee` ใน `data Ads/WIBWUB_Ads_Dashboard.html`
   ไฟล์นี้ minified บรรทัดเดียวยาวมาก — ใช้ Python แทนที่ substring แบบ exact-match
   **อย่าใช้ Edit tool**
4. แก้ `SH_ADS[idx]` ใน `WIBWUB_Dashboard.html` + `WIBWUB_Mobile.html` ให้ตรงกับ spend เดือนปัจจุบัน
   `idx` นับจาก array **`M5` ซึ่งอยู่ใน `WIBWUB_Dashboard.html`** (ไม่มีใน Ads Dashboard)
5. แก้ badge `#ads-updated` และ `.pb-sub` ให้ตรงวันที่ข้อมูลจริง
6. ตรวจ + commit:

```bash
cd "$BASE"
python3 -c "
import re,io
h=io.open('data Ads/WIBWUB_Ads_Dashboard.html',encoding='utf-8').read()
io.open('/tmp/ads.js','w').write('\n'.join(re.findall(r'<script[^>]*>([\s\S]*?)</script>',h)))"
node --check /tmp/ads.js || exit 1
python3 scripts/bump_sw.py          # ห้ามใช้ sed -i — BSD sed บน macOS พังเงียบ ๆ
git add "data Ads/WIBWUB_Ads_Dashboard.html" WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js "data Ads/Shopee"
git -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
    commit -m "auto: Shopee Ads $(date +%Y-%m-%d)"
```

**`git add` ต้องระบุ path เฉพาะไฟล์เสมอ** — working tree มีงานค้างของคนอื่นอยู่ประจำ
ถ้า `git add -A` หรือ `git add .` จะกวาดเข้า commit หมด

ไม่ต้อง `git push` — launchd `com.wibwub.autopush` push ให้เองภายใน 2 นาที

---

## RULES

- **ห้ามลบ `.git/*.lock` เอง** — มี 18 งานรันสลับกัน ถ้าติดให้รอ 20 วิแล้วลองใหม่ สูงสุด 3 ครั้ง
- ตัวเลขทุกตัวให้สคริปต์คำนวณ ห้ามคิดเอง ห้ามกรอกค่าสมมุติ
- ตั้งชื่อไฟล์ที่โหลดให้ unique เสมอ (Shopee ตั้งชื่อซ้ำทุกครั้ง)
- `grep -oP`, `sed -i "s/.../"` เป็น GNU-only **พังบน macOS** ห้ามใช้

## สรุปท้ายรอบ (สั้น ๆ ภาษาไทย)

ชื่อไฟล์ที่โหลด + ช่วงวันที่ + จำนวนแคมเปญ, ยอด spend/revenue/orders เดือนนี้,
เปลี่ยนจากเดิมเท่าไร (หรือ "ไม่มีข้อมูลใหม่"), commit id, error ถ้ามี
