---
name: wibwub-download-shopee-ads
description: ทุกวัน 08:00/19:00 — โหลด Shopee Ads CSV → อัปเดต DATA_PERIODS.<เดือน>.shopee ใน Ads Dashboard
---

## 📂 ขั้น 0 — หาโฟลเดอร์ All ก่อนเสมอ (ทำก่อนทุกอย่าง)

พรอมป์นี้ถูกเรียกได้จาก **2 ฝั่ง** และโฟลเดอร์ All อยู่คนละที่กัน
จึง**ห้ามฝังพาธตายตัว** ให้หาด้วยคำสั่งนี้ทุกครั้ง แล้วใช้ผลลัพธ์เป็น `BASE`

```bash
for d in "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" "$HOME/mnt/All" /sessions/*/mnt/All; do [ -d "$d/scripts" ] && echo "$d" && break; done
```

- ได้พาธมา → ใช้เป็น `BASE` ในทุกคำสั่งถัดไป (เขียนพาธเต็มเสมอ ห้ามใช้ตัวแปร shell)
- **ไม่เจอ** หรือ shell ตอบว่า `No folders are connected`
  → **หยุดทันที** รายงานว่า `❌ ล้มเหลว — เข้าโฟลเดอร์ All ไม่ได้` แล้วจบงาน
  ห้ามเดาพาธเอง ห้ามไปใช้ `~/Downloads` แทน

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

**สั่ง export เองเสมอ อย่าใช้ของเก่าใน list** — ของเดิมมักเป็นรอบเช้า ข้อมูลค้างหลายชั่วโมง:

```
POST /api/pas/v1/report/export_job/trigger/?SPC_CDS_VER=2
     body: {"language":"th","report_type":"new_cpc_homepage__overall",
            "start_time":<epoch 1 ของเดือน 00:00>,"end_time":<epoch วันนี้ 23:59:59>}
     -> {"data":{"export_id":<id>}}  แล้ว poll list_homepage_result จน status=="success" (~10–30 วิ)
```

> 🚨 **`report_type` ต้องเป็น `new_cpc_homepage__overall` เท่านั้น** (all-CPC = 42 แคมเปญ)
> เมนู **"ภาพรวมข้อมูลโฆษณา"** ในหน้าเว็บยิง `product_homepage_v2__overall` ซึ่งเป็น
> **product-only = 38 แคมเปญ** ตัวเลขต่ำกว่าจริง (20 ต.ค. 69 รอบเย็น: product-only
> spend 7.4 แสน vs all-CPC 8.31 แสน) — พลาดมาแล้วเพราะพรอมป์เดิมสั่งให้กดเมนูนี้
> เช็กเร็ว ๆ: นับแถวใน CSV ถ้าไม่ใช่ ~42 และไม่มีแถว "โฆษณาร้านค้า"/"โฆษณาคำค้นหา" = ผิดชุด

(ถ้าจำเป็นต้องกดในหน้าจริง ๆ: panel "รายงานล่าสุด" **เปิดเอง ไม่ต้องคลิกไอคอน "≡"**)

3. โหลดไฟล์ด้วย Blob + `<a download>` และ **ตั้งชื่อให้ unique เสมอ**
   เช่น `ข้อมูล-Shopee-Ads-<from>-<to>-cpc-allads__<YYYYmmdd_HHMM>.csv`
   > ⚠️ **ต้องขึ้นต้นด้วย `ข้อมูล-Shopee-Ads-` เท่านั้น** — `wibwub_auto_move.sh` แมตช์
   > `"$DL"/ข้อมูล-Shopee-Ads-*.csv` แบบ case-sensitive ชื่ออย่าง `shopee-ads-...`
   > (ตัวอย่างเดิมในพรอมป์นี้ ผิด — แก้ 21 ต.ค. 69) จะค้างใน ~/Downloads ตลอดไป
   > mover ไม่ย้ายให้ แล้วขั้นที่ 2 จะหาไฟล์ใน `data Ads/Shopee/` ไม่เจอ
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
   - นับเฉพาะแถวที่ `spend > 0` · `all` = เรียง spend มาก→น้อย · `top5` = 5 ตัวแรกของ `all`
     · `worst5` = roas น้อย→มาก 5 ตัว
   - `roas=revenue/spend`, `ctr=clicks/imp*100`, `cvr=orders/clicks*100`, `cpa=spend/orders` (คำนวณเอง ไม่อ่าน col 27)
   - **รูปแบบตัวเลขต่างกันระหว่างระดับ** ระดับบนสุดใช้ `%.2f` ทุกตัว · ในแต่ละแคมเปญ
     `spend`/`revenue` ใช้ `%.2f` แต่ `roas`/`ctr`/`cvr`/`cpa` ใช้ `repr(round(x,2))`
     (เช่น `cpa:45.5`, `roas:0.0`) และ `cpa:0` (int) เมื่อ `orders==0`
   - generator มีอยู่แล้ว **ไม่ต้องเขียนใหม่**: `scripts/ads/shopee_block_from_csv.py`
     (สร้าง 21 ต.ค. 69 · ยืนยัน byte-identical กับบล็อก 21/10 08:06 และ 19:50)
     ```
     python3 "<BASE>/scripts/ads/shopee_block_from_csv.py" <csv> --check <ไฟล์บล็อกเดิม> --out <ไฟล์บล็อกใหม่>
     ```
   - **ตรวจ generator ก่อนใช้**: รัน generator กับ CSV ของรอบก่อน แล้วเทียบ byte-identical
     กับบล็อก `shopee:{...}` ที่อยู่ในไฟล์จริง (`--check` รายงาน `identical` + `first_diff_at`)
     ถ้าไม่ตรง = generator ผิด อย่าเขียนทับ
2. **ถ้าค่าที่คำนวณได้เท่ากับของเดิมทุกตัว → หยุดตรงนี้** ไม่ต้องเขียน ไม่ bump sw.js ไม่ commit
   (รอบ 19:00 จะเจอเคสนี้บ่อยถ้า Shopee ยังไม่อัปเดตข้อมูล)
3. แก้ `DATA_PERIODS.<เดือน>.shopee` ใน `data Ads/WIBWUB_Ads_Dashboard.html`
   ไฟล์นี้ minified บรรทัดเดียวยาวมาก — ใช้ Python แทนที่ substring แบบ exact-match
   **อย่าใช้ Edit tool**
4. ~~แก้ `SH_ADS[idx]`~~ — **ข้ามข้อนี้** มีคอมเมนต์กำกับในไฟล์ทั้งสองว่า `SH_ADS` มาจาก
   Google Sheet (sales sync) ซึ่งกว้างกว่ายอด Ads portal **ห้าม overwrite ด้วย spend จากรายงานนี้**
   (ส.ค. 69: Sheet 1,185,609.37 vs Ads report 974,764.42) · รอบ 19–20 ต.ค. 69 ก็ข้ามเหมือนกัน
5. ~~แก้ badge `#ads-updated` / `.pb-sub` ด้วยมือ~~ — ทั้งคู่ derive จาก `DATA_PERIODS.oct.cover`
   แก้แค่ `cover.shopeeDay` + `cover.shopeePull` พอ (skill: wibwub-avoid-stale-hardcoded-labels)
6. ตรวจ + commit:

```bash
export BASE
python3 -c "
import re,io,os
h=io.open(os.environ['BASE']+'/data Ads/WIBWUB_Ads_Dashboard.html',encoding='utf-8').read()
io.open('/tmp/ads.js','w').write('\n'.join(re.findall(r'<script[^>]*>([\s\S]*?)</script>',h)))"
node --check /tmp/ads.js || exit 1
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/bump_sw.py"   # ห้ามใช้ sed -i — BSD sed บน macOS พังเงียบ ๆ
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" add "data Ads/WIBWUB_Ads_Dashboard.html" WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js "data Ads/Shopee"
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
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

---

## 🚨 ทำงานไม่ได้ = ต้องรายงานว่าล้มเหลว ห้ามขึ้นว่าสำเร็จ

**กรณีที่ถือว่าล้มเหลว**

1. **เข้าโฟลเดอร์ All ไม่ได้** (ขั้น 0 ไม่เจอพาธ)
2. **เปิดเว็บไม่ได้** — `navigate`/`browser_batch` คืนข้อความใดข้อความหนึ่งนี้
   - `The approval prompt for this browser action went unanswered for 5 minutes` (กล่องขออนุญาตไม่มีคนกด)
   - `Navigation to this domain is not allowed` (สิทธิ์โดเมนถูกปฏิเสธ)
   - `Tab ... is not in Claude's tab group` / เชื่อมต่อส่วนขยายไม่ได้
3. **สคริปต์ที่พรอมป์ระบุหายหรือพัง**

**สิ่งที่ต้องทำเมื่อล้มเหลว**

1. **ลองครั้งเดียวพอ ห้ามวนลองซ้ำ** — เคยเสียเวลา 5 นาทีต่อหนึ่งเว็บโดยไม่ได้อะไร
   (22 ต.ค. 69 งาน HR ลองทั้ง `browser_batch` และ `javascript_tool` ตรงไปที่แท็บที่ล็อกอินค้างอยู่
   ก็โดนกล่องเดียวกันทั้งคู่ — แท็บที่เปิดค้างไว้ช่วยไม่ได้)
2. ปิดแท็บที่เปิดไว้ด้วย `tabs_close_mcp`
3. จบงานโดยขึ้นต้นบรรทัดแรกด้วย
   `❌ ล้มเหลว — <สาเหตุสั้น ๆ> ไม่ได้ข้อมูลใหม่รอบนี้`
   แล้วบอกด้วยว่าข้อมูลล่าสุดในไฟล์อยู่ถึงวันไหน

**ห้ามทำเด็ดขาด**

- ❌ ห้ามหันไปใช้ไฟล์เก่าแล้วรายงานว่า "สำเร็จ" — ถ้าดึงของใหม่ไม่ได้ ถือว่าล้มเหลว
- ❌ ห้ามเขียน ✅ หรือคำว่า "เสร็จ/สำเร็จ/OK" เมื่อขั้นใดขั้นหนึ่งข้างบนไม่ผ่าน
- ❌ ห้ามเดาตัวเลข หรือคัดลอกตัวเลขจากรอบก่อนมาใส่

> ใช้ไฟล์เดิมได้เฉพาะกรณีที่พรอมป์ระบุไว้ชัดเจนว่าเป็นทางสำรองที่ยอมรับได้
> (เช่น ads-daily ใช้ `work/*.json` ที่ครอบช่วง `from→to` พอดี) และต้อง**รายงานตรง ๆ
> ว่ารอบนี้ใช้ของเดิม ไม่ได้ดึงใหม่**

---

## 🚫 กฎคำสั่ง shell (ทุกงาน — รวมคำสั่งที่คิดขึ้นเองระหว่างรัน)

งานตั้งเวลา **ไม่มีคนนั่งกดอนุญาต** ถ้าคำสั่งไม่แมตช์กฎที่อนุญาตไว้แล้ว
(`Bash(python3 *)` / `Bash(git *)` / `Bash(ls *)` ฯลฯ) งานจะค้างทั้งรอบ
สังเกตง่าย ๆ: ถ้ากล่องขออนุญาตมีแค่ปุ่ม **"Allow once"** โดยไม่มี "Always allow"
แปลว่าคำสั่งนั้นสร้างกฎถาวรไม่ได้ จะถามใหม่ทุกครั้งตลอดไป

**เขียนคำสั่งให้เรียบง่ายที่สุด — 1 คำสั่ง = 1 โปรแกรม + พาธเต็ม**

| ❌ ห้าม | เหตุผลที่โดนถาม | ✅ ใช้แบบนี้ |
|---|---|---|
| `git ...` ทุกรูปแบบ | `git -C` เปิดช่องให้ push หลุด · `cd ... && git` ขึ้นต้นด้วย cd จึงไม่แมตช์กฎ `Bash(git add:*)` → งานค้างรออนุญาต | `python3 "<BASE>/scripts/gitw.py" add/commit/status/log` |
| `cd "<path>" && python3 x.py` | ขึ้นต้นด้วย cd ไม่แมตช์ `Bash(python3 *)` | `python3 "<path เต็ม>/x.py"` |
| `BASE="..."` แล้วใช้ `$BASE` | ตัวแปร = simple_expansion สร้างกฎถาวรไม่ได้ | เขียนพาธเต็มตรง ๆ ทุกครั้ง |
| `for d in ...; do ... done` / `if [ ... ]` | ลูป/เงื่อนไขใน bash ก็เข้าข่ายเดียวกัน | ย้ายตรรกะไปไว้ในสคริปต์ python แล้วเรียกไฟล์นั้น |
| `cmd1; cmd2; cmd3` ต่อกันยาว ๆ | คำสั่งผสมแมตช์กฎไม่ได้ | แยกเป็นคนละคำสั่ง |

**ถ้าต้องมีตรรกะ (วนลูป / เช็คเงื่อนไข / ประกอบพาธ): เขียนเป็นสคริปต์ python
ไว้ใน `scripts/` แล้วเรียกด้วยพาธเต็ม** เช่น `python3 "<path เต็ม>/scripts/ads/check_downloads.py" tiktok`
วิธีนี้ทั้งอ่านง่ายกว่า ทดสอบแยกได้ และไม่ติดกำแพงสิทธิ์
