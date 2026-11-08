---
name: wibwub-monday-update
description: ทุกวัน 10:35/21:35 — อัปเดต Top สินค้า (ALL_PRODUCTS + PROD_MO) ใน WIBWUB_Mobile.html จาก Shipnity
---
> ⛔ **ห้ามเรียกเครื่องมือขอสิทธิ์ลบไฟล์** (เช่น `allow_cowork_file_delete`)
> งานตั้งเวลาไม่มีคนกดอนุญาต เครื่องมือนี้จะค้างรอจนหมดรอบ — เกิดจริง 5 พ.ย. 69
> `wibwub-shopee-live-daily` เรียกเพื่อลบ `.git/HEAD.lock` ของตัวเอง แล้ว**ค้าง 81 นาที**
> (09:40 → 10:57) กินสล็อตงานพร้อมกัน 1 ใน 3 ไปเปล่า ๆ · ตอนนี้มี hook ตีกลับให้อัตโนมัติแล้ว
> ถ้าติด `.git/index.lock` หรือ `.git/HEAD.lock`: `gitw.py` รอให้แล้วสูงสุด 5 นาที
> **ห้ามลบ lock ของคนอื่น** ถ้าสุดท้ายยังไม่ผ่าน → **รายงานตรง ๆ** ว่ารอบนี้ข้อมูลเข้าไฟล์แล้ว
> แต่ยังไม่ได้ commit แล้วจบรอบ **ห้ามรอต่อ**

## 📂 ขั้น 0 — หาโฟลเดอร์ All ก่อนเสมอ (ทำก่อนทุกอย่าง)

พรอมป์นี้ถูกเรียกได้จาก **2 ฝั่ง** และโฟลเดอร์ All อยู่คนละที่กัน
จึง**ห้ามฝังพาธตายตัว** ให้หาด้วยคำสั่งนี้ทุกครั้ง แล้วใช้ผลลัพธ์เป็น `BASE`

```bash
python3 -c "
import glob, os
CAND = ['/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All',
        os.path.expanduser('~/mnt/All')] + sorted(glob.glob('/sessions/*/mnt/All'))
P = '/scripts/task_prompts/wibwub-monday-update.md'
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
> เกิดจริง 3–4 พ.ย. 69 กับ `wibwub-daily-stock`: stat บนโฟลเดอร์ Drive ตอบ **False** 5 รอบติด
> ทั้งที่ `open()` ไฟล์เดียวกันได้ปกติ → ต้องเปิดไฟล์จริงใน try/except OSError เท่านั้น
> และ**ทุกคำสั่ง shell ของรอบต้องเป็น `python3` ไม่ใช่แค่คำสั่งแรก**
รวมคำสั่งชั่วคราวที่คิดขึ้นเองตอนไล่หาสาเหตุกลางรอบด้วย (เกิดจริง 7 พ.ย. 69 รอบ 20:25
ของ `wibwub-tiktok-content`: 12 คำสั่งแรกผ่านหมด แล้วไปค้าง 48 นาทีที่คำสั่งที่ 13
ซึ่งขึ้นต้นด้วย `cd <สแครชแพด> &&` — ดูหัวข้อ "กฎคำสั่ง shell" ท้ายไฟล์) ห้ามเป็นลูป `for` ของ bash
> (สร้างกฎอนุญาตถาวรไม่ได้ → รอบค้างจนหมดเวลา)

- ได้ `BASE OK <พาธ>` → ใช้พาธ**ที่ด่านนี้คืนมา**เป็น `BASE` ในทุกคำสั่งถัดไป (เขียนพาธเต็มเสมอ)
- `⛔ ไม่พบ BASE` หรือ shell ตอบว่า `No folders are connected`
  → **หยุดทันที** รายงาน `❌ ล้มเหลว — เข้าโฟลเดอร์ All ไม่ได้` แล้วจบงาน ห้ามเดาพาธเอง
- พาธ `/sessions/<ชื่อ>/mnt/All` **ใช้ได้จริงและเป็นพาธเดียวที่เข้าถึงได้เมื่อรอบนั้นได้ Linux sandbox**
  (5 พ.ย. 69 `wibwub-thursday-affiliate` ล้มที่ขั้น 0 เพราะพรอมป์ห้ามใช้พาธนี้)
  **ห้ามฝังชื่อเซสชันตายตัว** — ชื่อเปลี่ยนทุกรอบ ให้ใช้ค่าที่ด่านข้างบนคืนมาเท่านั้น

---


## WIBWUB — Top สินค้าในหน้ามือถือ

BASE = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`

อัปเดต `ALL_PRODUCTS` (15 สินค้า) และ `PROD_MO` (ยอดรายเดือนต่อสินค้า) ใน `WIBWUB_Mobile.html`

> **งานนี้มี 2 หน้าที่: (ก) ดาวน์โหลดไฟล์ออเดอร์จาก Shipnity  (ข) อัปเดต Top สินค้า**
>
> ⚠️ **ขั้นดาวน์โหลด (ขั้นที่ 0 ข้างล่าง) เป็นทางสำรอง — เช็คก่อนแล้วข้ามได้ถ้าไฟล์มาแล้ว**
> ตั้งแต่ 27 ต.ค. 2569 คนที่ export เป็นหลักคือ `wibwub-daily-stock` (09:00/19:00 Step 0)
> เพราะงานนี้รัน 10:35 ซึ่งหลังการประชุม 09:00 ทำให้รอบเช้าของหน้าสต๊อกใช้ไฟล์เมื่อวานทุกวัน
> งานนี้ยังต้องเช็คและ export ให้ถ้าไฟล์ของวันนี้ยังไม่มา **ห้ามตัดขั้นนี้ออก**
> ไฟล์ `Data Shipnity/Data_DD-MM-YYYY.xlsx` ที่ได้จากขั้นนี้ถูกใช้ต่อโดย `update_stock.py`
> (sold7d/burn ในหน้าสต๊อก), `shipnity_update.py` และ `products_update.py`
> เคยมีข้อความเก่าบอกว่าขั้นนี้ย้ายไปงานอื่นแล้ว ซึ่ง**ไม่จริง** ทำให้ export หยุดไป
> 25–26 ต.ค. 69 แล้ว sold7d ต่ำกว่าจริง (SSUG010024 ได้ 550 ทั้งที่ของจริง 813)
>
> ส่วน*การคำนวณ*อื่นที่เคยอยู่ในพรอมป์เก่าย้ายไปที่อื่นหมดแล้วจริง (ขั้นดาวน์โหลดไม่ได้ย้ายไปด้วย):
> - Affiliate → `wibwub-thursday-affiliate` (`scripts/affiliate_update.py`)
> - Shipnity Sales_Dashboard + อาเรย์ช่องทาง → `wibwub-shipnity-monday`
> - ยอดขาย SH/TK/LZ → `wibwub-sales-update`
>
> **ห้ามเขียนสคริปต์อ่าน Excel เอง** ตัวคำนวณคือ `process_shipnity()` ผ่าน `scripts/products_update.py`

### ความหมายของฟิลด์ (สำคัญ)

| | |
|---|---|
| `v` | ยอดขายจริง — **เฉพาะแถวที่ราคา > 0** |
| `q` | จำนวนจริง |
| `mk` / `mkq` | งบการตลาด (ของแจก / ส่ง Influencer) — **carry over ไม่คำนวณใหม่** |

สคริปต์อัปเดตแค่ `v` / `q` / `PROD_MO` และคง `mk` / `mkq` ไว้ตามเดิม

---

## ขั้นตอน

### 0. ดาวน์โหลดไฟล์ออเดอร์จาก Shipnity (เช็คก่อน — ข้ามได้ถ้าไฟล์ของวันนี้มาแล้ว)

**0.0 เช็คก่อนทุกครั้ง ห้าม export ทับ**

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/stock/wait_shipnity_export.py" --max-wait-min 0 --fresh-min 240
```

- `exit 0` (`status: FOUND`) → `wibwub-daily-stock` export ให้แล้วในรอบนี้
  **ข้ามขั้น 0.1–0.2 ทั้งหมด** ไปทำ "Top สินค้า" ต่อเลย แล้วรายงานว่า
  `ดาวน์โหลด Shipnity: ข้าม — daily-stock ทำให้แล้ว (<ชื่อไฟล์> <เวลา>)`
  เหตุผลที่ต้องข้าม: ไฟล์ 33 MB ใช้เวลา export ราว 10 นาที และโหลดซ้ำไม่ได้อะไรเพิ่ม
- `exit 3` (`status: TIMEOUT`) → ไฟล์ของวันนี้ยังไม่มา **ให้ทำขั้น 0.1 ต่อตามปกติ**
  นี่คือกรณีที่รอบ 09:00 ของ daily-stock ล้ม งานนี้คือตัวสำรองที่กู้ให้

**0.1 สั่ง export (ทำเฉพาะเมื่อขั้น 0.0 ได้ exit 3)**

```
select_browser(deviceId ที่ osPlatform เป็น macOS) → tabs_context_mcp(createIfEmpty=true)
browser_batch([ navigate("https://www.shipnity.com/data/c/purchase"), wait 6, screenshot ])
```

1. ตรวจว่าหน้า "ประวัติ" โหลดขึ้น และตัวกรองซ้ายบนเป็น **"สินค้าในออเดอร์"**
   ถ้าเจอหน้า login: **หยุดและรายงานว่าล้มเหลว ห้ามกรอกรหัสผ่าน**
2. กดปุ่มช่วงวันที่มุมขวาบน (ป้าย "วันที่สร้าง") แล้วกดปุ่มลัด **"เดือนนี้"**
   ยืนยันว่าป้ายเปลี่ยนเป็น `1 <เดือน> <ปี> ~ 31 <เดือน> <ปี>` และตารางมีข้อมูลขึ้นมา
3. กด **"ส่งออกข้อมูล"** (ปุ่มขวาบน)
4. ⚠️ **ในกล่อง Export ต้องเลือก "ไฟล์เดียว" เสมอ**
   ค่าเริ่มต้นคือ **"แยกไฟล์"** 500 แถว/ไฟล์ ซึ่งจะได้ `Data-Page-1_*.xlsx` ที่เป็นไฟล์หลอก
   (มีแค่ ~500 แถวล่าสุด) ถ้าใช้ไฟล์นั้น sold7d/sold14d/burn ของทุก SKU จะผิดแบบไม่มี error
5. กด **Export File** แล้ว **รอจนขึ้น 100%** — ไฟล์ ~33 MB ใช้เวลาราว **10 นาที**
   ห้ามปิดแท็บก่อนเสร็จ ระหว่างรอให้ใช้สคริปต์รอ (รอจนไฟล์เข้าหรือครบ 20 นาที)
   ```bash
   python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/stock/wait_shipnity_export.py" --max-wait-min 20
   ```
   **ห้ามใช้ `find ... -newermt "today"`** — `find` บนเครื่องนี้คือ `bfs` ซึ่งตอบ
   `Invalid timestamp` แล้วคืน exit 0 ทำให้เข้าใจผิดว่า "ไม่พบไฟล์"
   และ `ls` กับ glob ที่ไม่แมตช์จะล้มทั้งคำสั่งเพราะ zsh nomatch
6. download-mover จะย้ายไฟล์เข้า `Data Shipnity/` ให้เองภายใน 5 วินาที **ห้าม cp/mv เอง**

**ด่านตรวจก่อนไปขั้นถัดไป**

```bash
python3 - "$BASE" <<'PY'
import sys, os, glob, datetime as dt
base = sys.argv[1]
fs = glob.glob(os.path.join(base, "Data Shipnity", "Data_[0-9][0-9]-[0-9][0-9]-*.xlsx"))
if not fs:
    print("FAIL ไม่พบไฟล์ Data_DD-MM-YYYY.xlsx เลย"); sys.exit(1)
newest = max(fs, key=os.path.getmtime)
d = dt.date.fromtimestamp(os.path.getmtime(newest))
ok = d == dt.date.today()
print(("OK " if ok else "FAIL ") + os.path.basename(newest) + " ลงวันที่ " + d.isoformat())
sys.exit(0 if ok else 1)
PY
```

ได้ `FAIL` → **ขึ้นต้นรายงานด้วย `❌ ล้มเหลว — export Shipnity ไม่สำเร็จ`**
บอกด้วยว่าไฟล์ล่าสุดที่มีคือวันไหน **ห้ามเขียนว่าสำเร็จเด็ดขาด**
ทำขั้นที่ 1–2 ต่อได้ (Top สินค้ายังคำนวณจากไฟล์เก่าได้) แต่ต้องรายงานว่าส่วนดาวน์โหลดล้มเหลว

### 1. ดูก่อนว่าจะเปลี่ยนอะไร

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/products_update.py" --dry-run
```

ใช้ cache ของ Shipnity (`scripts/ship_cache.py`) — รอบที่ไม่มีไฟล์ใหม่ใน `Data Shipnity/`
จะเสร็จใน <1 วินาที ถ้ามีไฟล์ใหม่จะคำนวณใหม่ ~6 นาที

ตรวจด้วยตา: `asof` ต้องเป็นวันเดียวกับ `SALES_ASOF` · `products` = 15 ·
`reordered` บอกว่าอันดับสินค้าสลับที่ไหนบ้าง (ปกติได้ ถ้าสลับเยอะผิดปกติให้ดูก่อน)

ด่านที่สคริปต์จะปฏิเสธการเขียน: ยอดสินค้าใดต่างจากเดิมเกิน **2%** (แปลว่า `NAME_MAP`
ผิดหรือมี SKU ใหม่) · ชื่อใน `NAME_MAP` หายไปจาก Shipnity · `node --check` ไม่ผ่าน

### 2. รันจริง + commit

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/products_update.py"
```

exit `0` = อัปเดต + bump sw.js · `10` = ไม่มีอะไรเปลี่ยน · `2` = ไม่ผ่านด่าน

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" add WIBWUB_Mobile.html sw.js
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
    commit -m "auto-update: Top สินค้า <วันที่วันนี้ เช่น 2026-11-04>"
```

ไม่ต้อง `git push` — launchd `com.wibwub.autopush` push ให้เองภายใน 2 นาที

---

## RULES

- ตัวเลขทุกตัวให้สคริปต์คำนวณ ห้ามคิดเอง ห้ามกรอกค่าสมมุติ
- **ห้ามแก้ `mk` / `mkq`** — เป็นค่าที่คนกรอก ไม่ได้มาจาก Shipnity
- ชื่อสินค้าใน Shipnity ≠ ชื่อบนหน้าเว็บ · ตาราง map อยู่ที่ `NAME_MAP` ใน `scripts/products_update.py`
  ถ้ามีสินค้าใหม่ติด Top 15 ต้องเพิ่ม map ก่อน สคริปต์จะ error บอกเอง
- `grep -oP`, `sed -i "s/.../"` เป็น GNU-only **พังบน macOS** ห้ามใช้

## สรุปท้ายรอบ (สั้น ๆ ภาษาไทย)

`asof` ที่ใช้, Top 3 สินค้า + ยอด, สินค้าที่สลับอันดับ, commit id หรือ "ไม่มีข้อมูลใหม่", error ถ้ามี

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
