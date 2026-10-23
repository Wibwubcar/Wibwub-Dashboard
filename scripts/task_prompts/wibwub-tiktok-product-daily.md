---
name: wibwub-tiktok-product-daily
description: ทุกวัน 08:45/19:45 — ยอดขายระดับสินค้า + SKU จาก TikTok Compass → TK_PROD_DATA / TK_PROD_SKU
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
cd "$BASE" && python3 tiktok_product_merge.py tiktok_product_daily_new.json
```

## ขั้นที่ 5 — ดึงระดับ SKU

Endpoint: `/api/v2/.../sku/list` — **ไม่ต้องใช้ signature เช่นกัน** แต่ **ต้องมี query params**:
`oec_seller_id`, `seller_id`, `aid=4068`, `app_name=i18n_ecom_shop`
ถ้าขาด params จะได้ `code=98001021 call downstream server error`
(**ไม่ใช่** เพราะ `start === end` อย่างที่พรอมป์เก่าเขียนไว้ผิด)

ห่อผลเป็น chunk key เดียว `"STARTDATE_ENDDATE"` แล้ว:

```bash
cd "$BASE" && python3 tiktok_sku_merge.py tiktok_sku_daily_new.json
```

## ขั้นที่ 6 — ตรวจ + bump + commit

```bash
python3 scripts/bump_sw.py          # ห้ามใช้ sed -i — BSD sed บน macOS พังเงียบ ๆ
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" add WIBWUB_Dashboard.html sw.js tiktok_product_daily_new.json tiktok_sku_daily_new.json
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
    commit -m "auto: TikTok product/SKU $(date +%Y-%m-%d)"
```

ไม่ต้อง `git push` — launchd `com.wibwub.autopush` push ให้เองภายใน 2 นาที

---

## RULES

- **ห้ามลบ `.git/*.lock` เอง** — มีงานตั้งเวลาอื่นรันพร้อมกันได้ ถ้าติดให้รอ 20 วิแล้วลองใหม่ สูงสุด 3 ครั้ง
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
| `cd "<path>" && git status` | cd + git = ตัวตรวจตีธง (รัน hook ได้) | `git -C "<path เต็ม>" status` |
| `cd "<path>" && python3 x.py` | ขึ้นต้นด้วย cd ไม่แมตช์ `Bash(python3 *)` | `python3 "<path เต็ม>/x.py"` |
| `BASE="..."` แล้วใช้ `$BASE` | ตัวแปร = simple_expansion สร้างกฎถาวรไม่ได้ | เขียนพาธเต็มตรง ๆ ทุกครั้ง |
| `for d in ...; do ... done` / `if [ ... ]` | ลูป/เงื่อนไขใน bash ก็เข้าข่ายเดียวกัน | ย้ายตรรกะไปไว้ในสคริปต์ python แล้วเรียกไฟล์นั้น |
| `cmd1; cmd2; cmd3` ต่อกันยาว ๆ | คำสั่งผสมแมตช์กฎไม่ได้ | แยกเป็นคนละคำสั่ง |

**ถ้าต้องมีตรรกะ (วนลูป / เช็คเงื่อนไข / ประกอบพาธ): เขียนเป็นสคริปต์ python
ไว้ใน `scripts/` แล้วเรียกด้วยพาธเต็ม** เช่น `python3 "<path เต็ม>/scripts/ads/check_downloads.py" tiktok`
วิธีนี้ทั้งอ่านง่ายกว่า ทดสอบแยกได้ และไม่ติดกำแพงสิทธิ์
