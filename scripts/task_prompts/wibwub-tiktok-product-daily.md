---
name: wibwub-tiktok-product-daily
description: ทุกวัน 09:55/20:55 — ยอดขายระดับสินค้า + SKU จาก TikTok Compass → TK_PROD_DATA / TK_PROD_SKU
---
> ⛔ **ห้ามเรียกเครื่องมือขอสิทธิ์ลบไฟล์** (เช่น `allow_cowork_file_delete`)
> งานตั้งเวลาไม่มีคนกดอนุญาต เครื่องมือนี้จะค้างรอจนหมดรอบ — เกิดจริง 5 พ.ย. 69
> `wibwub-shopee-live-daily` เรียกเพื่อลบ `.git/HEAD.lock` ของตัวเอง แล้ว**ค้าง 81 นาที**
> (09:40 → 10:57) กินสล็อตงานพร้อมกัน 1 ใน 3 ไปเปล่า ๆ · ตอนนี้มี hook ตีกลับให้อัตโนมัติแล้ว
> ถ้าติด `.git/index.lock` หรือ `.git/HEAD.lock`: `gitw.py` รอให้แล้วสูงสุด 5 นาที
> **ห้ามลบ lock ของคนอื่น** ถ้าสุดท้ายยังไม่ผ่าน → **รายงานตรง ๆ** ว่ารอบนี้ข้อมูลเข้าไฟล์แล้ว
> แต่ยังไม่ได้ commit แล้วจบรอบ **ห้ามรอต่อ**
> ✅ **ไฟล์นี้คือตัวจริง** — ตั้งแต่ 6 พ.ย. 69 `~/Documents/Claude/Scheduled/wibwub-tiktok-product-daily/SKILL.md`
> เป็น**สำเนาตรงทุกไบต์**ของไฟล์นี้ (`skill_sync` โหมด `copy` เฝ้าให้) แก้ที่นี่แล้ว**ต้องคัดลอกทับตัวจริงด้วย**
> ก่อนหน้านี้ตัวจริงเป็นพรอมป์คนละชุด (20 KB ภาษาอังกฤษ) ที่ยังสั่ง push ด้วยมือและให้ผู้ใช้
> ดับเบิลคลิกสคริปต์ช่วย push เอง ทั้งที่ launchd `com.wibwub.autopush` ทำให้อยู่แล้ว
> — การแก้ในรีโปจึงไม่มีผลกับรอบจริงเลย (ตัวตรวจ `skill_sync` มีมาร์กเกอร์จับแพทเทิร์นนี้แล้ว)


## 📂 ขั้น 0 — หาโฟลเดอร์ All ก่อนเสมอ (ทำก่อนทุกอย่าง)

พรอมป์นี้ถูกเรียกได้จาก **2 ฝั่ง** และโฟลเดอร์ All อยู่คนละที่กัน
จึง**ห้ามฝังพาธตายตัว** ให้หาด้วยคำสั่งนี้ทุกครั้ง แล้วใช้ผลลัพธ์เป็น `BASE`

**ทุกคำสั่ง shell ของรอบต้องขึ้นต้นด้วย `python3` เสมอ — ไม่ใช่แค่คำสั่งแรก**
รวมคำสั่งชั่วคราวที่คิดขึ้นเองตอนไล่หาสาเหตุกลางรอบด้วย (เกิดจริง 7 พ.ย. 69 รอบ 20:25
ของ `wibwub-tiktok-content`: 12 คำสั่งแรกผ่านหมด แล้วไปค้าง 48 นาทีที่คำสั่งที่ 13
ซึ่งขึ้นต้นด้วย `cd <สแครชแพด> &&` — ดูหัวข้อ "กฎคำสั่ง shell" ท้ายไฟล์)

```bash
python3 -c "
import glob, os
CAND = ['/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All',
        os.path.expanduser('~/mnt/All')] + sorted(glob.glob('/sessions/*/mnt/All'))
P = '/scripts/task_prompts/wibwub-tiktok-product-daily.md'
for B in CAND:
    try:
        open(B + P).read(1)
        print('BASE OK', B)
        break
    except OSError as e:
        print('ไม่ได้', B, type(e).__name__)
else:
    print('⛔ ไม่พบ BASE')
"
```

> ⛔ **ห้ามเช็ค BASE ด้วย `os.path.isdir` / `os.path.isfile` / `[ -d ... ]` / `[ -f ... ]`**
> stat บนโฟลเดอร์ Drive ตอบ **False** หลอกได้ (เกิดจริง 3–4 พ.ย. 69 กับ `wibwub-daily-stock`
> ล้ม 4 รอบติด) ให้ **เปิดไฟล์จริง** แล้วรับ `OSError` แทน
> **ห้ามใช้ลูป `for` ของ bash หรือตั้งตัวแปร `BASE=`** — ตัวแยกคำสั่งอ่านไม่ออก
> แล้วเด้งกล่องขออนุญาตที่ไม่มีคนกด (รอบนั้นค้างทั้งรอบ)

- ได้พาธมา → ใช้เป็น `BASE` ในทุกคำสั่งถัดไป (เขียนพาธเต็มเสมอ ห้ามใช้ตัวแปร shell)
- **ไม่เจอ** หรือ shell ตอบว่า `No folders are connected`
  → **หยุดทันที** รายงานว่า `❌ ล้มเหลว — เข้าโฟลเดอร์ All ไม่ได้` แล้วจบงาน
  ห้ามเดาพาธเอง ห้ามไปใช้ `~/Downloads` แทน

---


## WIBWUB — ยอดขายระดับสินค้า/SKU จาก TikTok Compass

BASE = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`

เป้าหมาย: เติมข้อมูล **ของเมื่อวาน** ลง `TK_PROD_DATA` และ `TK_PROD_SKU` ใน `WIBWUB_Dashboard.html`

> **สคริปต์ merge เขียนไว้แล้ว ห้ามเขียนใหม่** — `tiktok_product_merge.py` / `tiktok_sku_merge.py`
> หน้าที่ของรอบนี้คือ "ดึงข้อมูลให้ได้" แล้วส่งไฟล์ JSON ให้สคริปต์ merge

---

## ⚠️ วิธีที่ **ใช้ไม่ได้** (อย่าเสียเวลาลอง)

ทดสอบแล้วเมื่อ 20 ต.ค. 2569 — ทั้ง 3 วิธีนี้ตายหมด:

| วิธี | ทำไมไม่ได้ |
|---|---|
| `read_network_requests` เพื่อดู POST body | **คืนแค่ url/method/status ไม่มี body** จับ request shape ไม่ได้ |
| patch `window.fetch` / `XMLHttpRequest` เพื่อดัก request | **ถูก safety classifier บล็อก** (`Permission ... denied by the auto mode classifier`) |
| สแกน JS bundle ด้วย `performance.getEntriesByType('resource')` | ถูกบล็อกเหมือนกัน |

**ไม่ต้องไปค้นหา request shape ใหม่** — shape ที่ถูกต้องอยู่ข้างล่างนี้แล้ว

---

## ขั้นที่ 1 — เปิดหน้า Compass

1. Chrome: `list_connected_browsers` → `select_browser` deviceId `b75a6bb0-5b78-4e44-92a8-75224f1ce4ee` → `tabs_context_mcp(createIfEmpty=true)`
2. navigate ไป **`https://seller-th.tiktok.com/compass/product-analysis`**
   (**ไม่ใช่** `/compass/product-detail` — path นั้น redirect ไป data-overview)
   ถ้าขึ้นหน้า login: **หยุดและรายงาน ห้ามกรอกรหัสผ่าน**

## ขั้นที่ 2 — ดึงระดับสินค้า (parent)

ยิง `fetch` same-origin ใน `javascript_tool` ตรง ๆ **ไม่ต้องใช้ signature/token**:

```
POST /api/v3/insights/seller/ttp/product/list
{"version":3,"request":{
  "time_descriptor":{"start":"YYYY-MM-DD","end":"YYYY-MM-DD"},
  "list_control":{"pagination":{"page":1,"size":30}}}}
```

กฎที่ต้องรู้ (เคยพลาดมาแล้วทุกข้อ):
- **`end` เป็น exclusive** — ข้อมูลวันเดียวคือ `start` = วันนั้น, `end` = วันถัดไป
- ต้องมี key `request` ครอบ ไม่งั้นได้ error `binding: expr_path=request`
- ฟิลด์ที่ใช้อยู่ใน `stats_v3.total`: `gmv`, `orders`, `sku_orders`, `items_sold`,
  `self_live_gmv`, `self_video_gmv`, `affiliate_gmv`
- **backend ตัดข้อมูลทิ้งแบบสุ่ม** — `size` > 50 คืน `items` ว่างทั้งที่ `code:0` ·
  `size:40` ได้ 34 แถว · `size:50` ได้ 24 แถว ทั้งที่ `total` บอก 74
- `rules:[{"field":"gmv","direction":2}]` ผ่าน validation และ server echo กลับ **แต่ไม่ sort จริง**
- ยิงถี่เกินไปได้ `code:429 rate limit exceeded` → **เว้น ≥ 2 วินาทีต่อ request**

**วิธีที่ใช้ได้:** ยิงซ้ำหลายรอบสลับ `size` (10/20/30/40) และ `page` (1..8) แล้ว **union ตาม `pid`**
หยุดเมื่อจำนวน pid ไม่เพิ่มแล้วติดกันหลายรอบ แล้วเทียบกับ `next_pagination.total`

## ขั้นที่ 3 — เซฟไฟล์ (ห้ามอ่านผ่าน javascript_tool)

ผลลัพธ์ JSON หลาย KB **อ่านกลับผ่าน `javascript_tool` จะถูกตัดเงียบ ๆ** (เกิน ~1,500–2,000 ตัวอักษร)
ให้ trigger download แทน:

```js
const a=document.createElement('a');
a.href=URL.createObjectURL(new Blob([JSON.stringify(out)],{type:'application/json'}));
a.download='tk_prod_YYYYMMDD.json'; document.body.appendChild(a); a.click();
```

แล้วอ่านไฟล์ด้วย **Bash tool** จาก `/Users/thanasablilutanon/Downloads/`
(launchd `com.wibwub.download-mover` อาจย้ายไป `downloads_archive/` ของ BASE แล้ว — หาทั้งสองที่)

## ขั้นที่ 4 — merge ระดับสินค้า

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/tiktok_product_merge.py" "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/tiktok_product_daily_new.json"
```

## ขั้นที่ 5 — ดึงระดับ SKU

Endpoint: `/api/v2/.../sku/list` — **ไม่ต้องใช้ signature เช่นกัน** แต่ **ต้องมี query params**:
`oec_seller_id`, `seller_id`, `aid=4068`, `app_name=i18n_ecom_shop`
ถ้าขาด params จะได้ `code=98001021 call downstream server error`
(**ไม่ใช่** เพราะ `start === end` อย่างที่พรอมป์เก่าเขียนไว้ผิด)

ห่อผลเป็น chunk key เดียว `"STARTDATE_ENDDATE"` แล้ว:

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/tiktok_sku_merge.py" "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/tiktok_sku_daily_new.json"
```

## ขั้นที่ 6 — ตรวจ + bump + commit

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/bump_sw.py"   # ห้ามใช้ sed -i — BSD sed บน macOS พังเงียบ ๆ
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" add WIBWUB_Dashboard.html sw.js tiktok_product_daily_new.json tiktok_sku_daily_new.json
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
    commit -m "auto: TikTok product/SKU <วันที่วันนี้ เช่น 2026-11-04>"
```

ไม่ต้อง `git push` — launchd `com.wibwub.autopush` push ให้เองภายใน 2 นาที

---

## RULES

- **ห้ามลบ `.git/*.lock` ของคนอื่นทุกกรณี** และ **ห้ามวน retry เอง** — `gitw.py` รอ lock
  ให้สูงสุด 5 นาที และถ้าสุดท้าย commit ไม่ผ่านจะ unstage ไฟล์ของตัวเองคืนให้ (เนื้อไฟล์ไม่หาย)
  **exit 3 = ไม่ได้ commit** ให้รายงานตรง ๆ ว่ารอบนี้ข้อมูลเข้าไฟล์แล้วแต่ยังไม่ได้ commit
- ตัวเลขทุกตัวให้สคริปต์ merge คำนวณ ห้ามคิดเอง ห้ามกรอกค่าสมมุติ
- **ห้ามเขียนทับวันเดิมด้วยข้อมูลที่ได้น้อยกว่าเดิม** — backend ตัดข้อมูลสุ่ม
  ถ้ารอบนี้ได้สินค้าน้อยกว่าที่มีอยู่ ให้ข้ามและรายงาน
- จบงานปิดแท็บที่เปิดด้วย `tabs_close_mcp`
- บันทึก coverage % (unique pid เทียบ `next_pagination.total`) ลง commit message ทุกครั้ง
  เพื่อให้รู้ว่าวันไหน merge ของไม่ครบ

## สรุปท้ายรอบ (สั้น ๆ ภาษาไทย)

วันที่ดึง, จำนวนสินค้าที่ได้ / total ที่ backend บอก (coverage %), GMV รวม,
จำนวน SKU, reconcile SKU vs parent, commit id หรือ "ไม่มีข้อมูลใหม่", error ถ้ามี

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

> ⚠️ **กฎนี้ใช้กับคำสั่งที่คิดขึ้นเองตอนไล่หาสาเหตุด้วย** ไม่ใช่แค่คำสั่งที่พรอมป์เขียนไว้
>
> **เกิดจริง 7 พ.ย. 69 รอบ 20:25 ของ `wibwub-tiktok-content`:** 12 คำสั่งแรกขึ้นต้นด้วย
> `python3` อนุมัติเองใน 1 วินาทีทุกตัว แต่ตอนจะพิสูจน์วันที่ของคลิป เอเจนต์คิดคำสั่ง
> ชั่วคราวขึ้นเองเป็น `cd <สแครชแพด> && python3 -c "..."` → **ค้างรอกล่อง 48 นาที**
> แล้วถูกตีกลับ รอบนั้นจึงจบแบบไม่มีรายงานปิดท้าย และคลิปเดือน พ.ย. ไม่เข้าหน้าเว็บ

🚫 **ห้ามให้คำสั่งขึ้นต้นด้วย `cd` ทุกกรณี** แม้จะ `cd` ไปโฟลเดอร์ที่อนุญาตไว้แล้วก็ตาม
— ตัวเทียบกฎดูคำแรกของคำสั่ง พอคำแรกเป็น `cd` กฎ `Bash(python3 *)` ก็ไม่ถูกใช้

🚫 **ห้ามใช้โฟลเดอร์สแครชแพด** (`/private/tmp/claude-501/...`) วางสคริปต์ชั่วคราว
— พาธนั้นมี id ของเซสชันอยู่ จึง**เปลี่ยนทุกรอบ** สร้างกฎอนุญาตถาวรให้ไม่ได้เลย

✅ **ถ้าต้องเขียนอะไรทดลอง/ตรวจสอบชั่วคราว ให้เขียนเป็นไฟล์** ไว้ใน
`<BASE>/scripts/ops/work/` แล้วเรียกด้วยพาธเต็ม:
`python3 "<BASE>/scripts/ops/work/<ชื่อไฟล์>.py"` — โฟลเดอร์นี้อยู่ใน `.gitignore`
จึงไม่ติดขึ้นรีโปสาธารณะ และคำสั่งขึ้นต้นด้วย `python3` จึงผ่านกฎเดิมทันที

---
---

# 🚦 ด่านบังคับก่อน merge ระดับสินค้า — ผลรวม GMV ต้องเท่ากับ tk_real (เพิ่ม 27 ต.ค. 69)

**ผลรวม `gmv` ของทุกสินค้าในวันนั้น ต้องเท่ากับ `tk_real` ของวันเดียวกันใน `data Ads/ads_daily.json`**
(ตรวจย้อนหลัง 21–25 ต.ค. แล้ว ตรงกัน **100.0% ทุกวัน** ไม่ใช่ใกล้เคียง — ตรงถึงหลักสตางค์)

```bash
python3 -c "
import json,sys,re,io
f=sys.argv[1]; dt=sys.argv[2]
B='<BASE>'
rows=json.load(open(f))[dt]
g=sum(r['gmv'] for r in rows)
tr=json.load(open(B+'/data Ads/ads_daily.json'))['days'][dt]['tk_real']['gmv']
print('%s: %d สินค้า  GMV %.2f  tk_real %.2f  = %.2f%%'%(dt,len(rows),g,tr,g/tr*100))
sys.exit(0 if abs(g-tr)<1 else 1)
" tiktok_product_daily_new.json 2026-XX-XX
```

**ถ้าไม่ตรง = ดึงมาไม่ครบ ห้าม merge เด็ดขาด** ให้วนดึงเพิ่มจนครบ แล้วค่อย merge
ถ้าวนแล้วยังไม่ครบ ให้ **หยุด ไม่ต้องเขียนไฟล์** แล้วรายงานว่า
`❌ ดึงระดับสินค้าไม่ครบ — ได้ <n> สินค้า GMV <x> จาก <tk_real> (<%>) ข้ามการ merge`

เหตุผล: `next_pagination.total` คืน `null` ได้ (เจอจริง 27 ต.ค.) จึงใช้เป็นด่านไม่ได้
และ backend ตัดข้อมูลทิ้งแบบสุ่ม การ union ตาม pid อย่างเดียวจะ "นิ่ง" ที่ตัวเลขไม่ครบแล้วดูเหมือนจบ
เคสจริง 27 ต.ค. 69: ประกอบ request เองได้ 54 สินค้า / 82,845 ของวันที่ 26 (ของจริง ~131,690)
และทดสอบกับวันที่ 25 ที่รู้คำตอบ ก็ได้แค่ 66 / 100,597 เทียบกับไฟล์จริงของรอบ 26 ต.ค. 21:10
ที่ได้ **74 สินค้า / 132,767.93 ตรงเป๊ะ** — ถ้าไม่มีด่านนี้ ข้อมูลขาด 38% จะถูก commit แบบเงียบ ๆ

**เช็ค `TK_PROD_SKU` ด้วย:** ผลรวม GMV ระดับ SKU ของสินค้าหนึ่ง **ต้องไม่เกิน** GMV ระดับ parent
ถ้าเกิน แปลว่า merge ยัด chunk เดียวซ้ำให้ทุกวัน (เคยเกิด 19–21 ต.ค. 69)

---

# 🔁 งานนี้มี 2 ส่วน — เพิ่มส่วน B เมื่อ 24 ต.ค. 2569

ทุกอย่างข้างบนคือ **ส่วน A (TikTok สินค้า + SKU)** ทำให้ครบเหมือนเดิมทุกประการ ห้ามข้าม
เสร็จแล้วทำ **ส่วน B** ต่อ · **ส่วนไหนล้มก็ทำอีกส่วนต่อ** และ **รายงานแยก 2 หัวข้อเสมอ**

เหตุผล: ฝั่ง code เปิดเว็บในรอบตั้งเวลาไม่ได้ตั้งแต่เวอร์ชัน 2.1.308 (22 ต.ค. 69 20:32)
งานค่าธรรมเนียมใช้โดเมน `seller-th.tiktok.com` ตัวเดียว ซึ่งงานนี้มีสิทธิ์อยู่แล้ว จึงย้ายมารวมกัน
**ไม่ต้องขออนุญาตโดเมนเพิ่ม**

## ขั้น 0 — หาโฟลเดอร์ All

**ทุกคำสั่ง shell ของรอบต้องขึ้นต้นด้วย `python3` เสมอ — ไม่ใช่แค่คำสั่งแรก**
รวมคำสั่งชั่วคราวที่คิดขึ้นเองตอนไล่หาสาเหตุกลางรอบด้วย (เกิดจริง 7 พ.ย. 69 รอบ 20:25
ของ `wibwub-tiktok-content`: 12 คำสั่งแรกผ่านหมด แล้วไปค้าง 48 นาทีที่คำสั่งที่ 13
ซึ่งขึ้นต้นด้วย `cd <สแครชแพด> &&` — ดูหัวข้อ "กฎคำสั่ง shell" ท้ายไฟล์)

```bash
python3 -c "
import glob, os
CAND = ['/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All',
        os.path.expanduser('~/mnt/All')] + sorted(glob.glob('/sessions/*/mnt/All'))
P = '/scripts/marketing/fee_update.py'
for B in CAND:
    try:
        open(B + P).read(1)
        print('BASE OK', B)
        break
    except OSError as e:
        print('ไม่ได้', B, type(e).__name__)
else:
    print('⛔ ไม่พบ BASE')
"
```

> ⛔ **ห้ามเช็ค BASE ด้วย `os.path.isdir` / `os.path.isfile` / `[ -d ... ]` / `[ -f ... ]`**
> stat บนโฟลเดอร์ Drive ตอบ **False** หลอกได้ (เกิดจริง 3–4 พ.ย. 69 กับ `wibwub-daily-stock`
> ล้ม 4 รอบติด) ให้ **เปิดไฟล์จริง** แล้วรับ `OSError` แทน
> **ห้ามใช้ลูป `for` ของ bash และห้ามตั้งตัวแปร `BASE=`** — ตัวแยกคำสั่งอ่านไม่ออก
> แล้วเด้งกล่องขออนุญาตที่ไม่มีคนกด (รอบนั้นค้างทั้งรอบ) · ได้พาธมาแล้วให้**เขียนพาธเต็ม
> ตรง ๆ ทุกคำสั่งถัดไป ห้ามใช้ `$BASE`**

ไม่เจอ → หยุดส่วน B แล้วรายงาน ห้ามเดาพาธ

---

# ส่วน B — อัตราค่าธรรมเนียมแพลตฟอร์ม

อ่านไฟล์นี้ด้วย Read tool แล้วทำตามทุกขั้นตอน (พาธเต็ม ห้ามใช้ `$BASE`):

`/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/task_prompts/wibwub-platform-fee-daily.md`

### กติกาสำคัญ
- **เดือนปัจจุบันต้องใส่ `--provisional` เสมอ** (ยอด settlement ยังไหลเข้าไม่ครบ)
  เดือนที่แล้วปิดยอดได้ตั้งแต่วันที่ 5 เป็นต้นไป ไม่ต้องใส่ธงนี้
- **ห้ามแก้อัตราของเดือนที่ปิดยอดไปแล้ว** ถ้าสคริปต์บอกว่าค่าไม่ตรง ให้รายงาน
  **ห้ามใส่ `--force` เอง** เพราะอัตราที่ปิดแล้วถูกใช้คำนวณย้อนหลังทั้งปี
- ด่าน `--range` ผ่านไม่ได้สำหรับเดือนปัจจุบัน เพราะ TikTok ปิดวันที่อนาคต เลือกเต็มเดือนไม่ได้
  → ต้องใช้ `--no-range-check` ตามที่พรอมป์ระบุ
- ตัวเลขทุกตัวต้องมาจากหน้าเว็บจริง **ห้ามเดาหรือประมาณเอง**
- ถ้าเจอหน้า login หรือสิทธิ์โดเมนถูกปฏิเสธ: หยุดส่วน B รายงาน **ห้ามกรอกรหัสผ่าน**
  อัตราเดิมในไฟล์จะยังอยู่ หน้าเว็บไม่พัง รอบพรุ่งนี้ค่อยลองใหม่
- จบส่วน B ให้ปิดแท็บ Chrome ที่เปิดในส่วนนี้ด้วย `tabs_close_mcp`
- git add เฉพาะไฟล์ที่พรอมป์ระบุ รีโปนี้มีงานอื่นทำงานพร้อมกัน ไฟล์ dirty ที่เหลือเป็นของคนอื่น
- auto-push จะ push ให้เอง **ไม่ต้อง git push**

---

# รีเฟรชการ์ดสถานะ (ทำท้ายรอบทุกครั้ง หลังจบทั้งส่วน A และ B)

```bash
python3 "<BASE>/scripts/ops/task_health.py" --refresh
```

- ทำให้การ์ดสถานะเห็นผลงานของรอบนี้**ทันที** ไม่ต้องรอตัวตรวจรอบถัดไป (ทุกชั่วโมงที่ :12)
  - เกิดจริง 6 พ.ย. 69: `sales-update` อ่านชีตใหม่ได้ถึง 5/11 ตอน 09:34 แต่การ์ดยังขึ้น
    "รอทีมกรอกชีต ค้าง 31/10" จนถึงรอบ 10:12 ผู้ใช้อ่านแล้วเข้าใจผิดว่างานยังไม่ได้รัน
- **ทำทุกครั้ง แม้รอบนี้ไม่มีอะไร commit** (ความสดของผลงานก็เป็นข้อมูลที่การ์ดใช้)
- **คำสั่งนี้คืน exit 0 เสมอ** ถ้าผลพิมพ์ว่า `"status": "SKIP"` หรือ `"NO_CHANGE"`
  ก็ไม่ใช่ความผิดพลาดของรอบนี้ ให้ไปต่อได้เลย
- ไม่ต้อง `git add` / commit ไฟล์สถานะ — งาน `wibwub-task-health` commit ให้เองทุกชั่วโมง
- ⛔ **ห้ามใช้ `--write-json` แทน** — ธงนั้นเขียนทับไฟล์ทั้งก้อน ถ้ารันจากแซนด์บ็อกซ์
  (งานฝั่ง local อ่านไฟล์เซสชันไม่ได้) จะทับสแนปช็อตที่ดีด้วยผลที่อ่านไม่ครบ ทุกแถวจะกลาย
  เป็น "ตรวจไม่ได้" · `--refresh` รู้จักแยกสองกรณีนี้ให้แล้ว

---

# รูปแบบรายงานท้ายรอบ (ภาษาไทย แยก 2 หัวข้อ)

```
## A — TikTok สินค้า + SKU
<สำเร็จ/ล้มเหลว> · วันที่ที่เพิ่ม/อัปเดต · จำนวนสินค้า/SKU · commit id

## B — อัตราค่าธรรมเนียม
<สำเร็จ/ล้มเหลว> · เดือนที่อัปเดต · อัตราที่ได้ · commit id
```

**ห้ามเขียน ✅ หรือคำว่าสำเร็จ ถ้าส่วนใดส่วนหนึ่งไม่ผ่าน** ให้ขึ้นต้นส่วนนั้นด้วย `❌ ล้มเหลว — <สาเหตุ>`
