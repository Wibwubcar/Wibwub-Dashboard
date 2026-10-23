---
name: wibwub-shipnity-monday
description: อัปเดต Top สินค้าขายดี (Sales_Dashboard.html) จาก Excel ใน Data Shipnity ทุกวันจันทร์ 10:00 น.
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


## WIBWUB Shipnity Weekly Update — ทุกวันจันทร์ 10:00 น.

งานนี้อัปเดต **2 ส่วน** จาก Excel ใน `Data Shipnity/`:
1. `Data Shipnity/Sales_Dashboard.html` — Top สินค้าขายดี
2. **อาเรย์ยอดขายรายช่องทางใน `WIBWUB_Dashboard.html` + `WIBWUB_Mobile.html`**
   (`FB_REV`, `LINE_REV`, `CARE_REV`, `WEB_REV`, `MKT_REV`, `POS_REV`, `BEUK_REV`, `FB_ORD`, `LINE_ORD`)
   Shipnity เป็นแหล่งเดียวของช่องทางเหล่านี้ — ก่อน 20 ต.ค. 2569 ไม่มีงานไหนเขียนเลย
   ค่าจึงค้างซ้ำเดิมตั้งแต่ มิ.ย. และสองหน้าโชว์ไม่ตรงกัน (ยอดรวม ต.ค. ต่างกัน 334,351 บาท)
   สคริปต์เขียนค่าเดียวกันลงทั้ง 2 หน้าทุกรอบ และ **ตัดข้อมูลที่ `SALES_ASOF` เสมอ**
   เพื่อให้ยอดรวมเดือนล่าสุดไม่คาบเกี่ยวคนละวันกับ Shopee/TikTok/Lazada
พนักงาน upload ไฟล์ใหม่ก่อน 10:00 น. ทุกวันจันทร์

BASE = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`

> **ห้ามเขียนสคริปต์อ่าน Excel เอง** — ตัวคำนวณจริงคือ `process_shipnity()` ใน `wibwub_update.py`
> เหตุผล: ไฟล์ใน `Data Shipnity/` เป็น **cumulative snapshot รายวันที่ซ้อนทับกัน**
> (ไฟล์วันที่ 29 มีทุกแถวของวันที่ 28 อยู่แล้ว) ถ้ารวมตรง ๆ จะนับซ้ำหลายสิบรอบ
> ต้อง dedup ด้วย `(order_id, ชื่อสินค้า)` และ RAW ต้องมี `channels` / `products` /
> `order_counts` ครบตามที่ JS ในหน้าเว็บอ้าง ไม่งั้นหน้าเว็บพังทันที
> (เวอร์ชันเก่าของไฟล์นี้เคย inline สคริปต์เองแล้วได้ 2.4M lines / HTML 400 MB — ถูกถอดออกแล้ว)

---

## ขั้นตอน

### 1. ดูก่อนว่าจะได้อะไร (ไม่เขียนไฟล์)

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/shipnity_update.py" --dry-run
```

ใช้เวลาราว 1–2 นาที (ไฟล์ ~160 ไฟล์) จะได้ JSON เช่น:
`{"status":"DRY_RUN","lines":44216,"order_counts":1862,"products":217,"channels":17,"date_min":"2026-01-01","date_max":"2026-10-19","raw_mb":2.26,"page_mb_before":2.11}`

ตรวจด้วยตา: `date_max` ควรเป็นวันล่าสุดที่มีไฟล์ · `lines` ควรอยู่หลักหมื่น ไม่ใช่หลักล้าน · `raw_mb` ควรใกล้ `page_mb_before`
· `asof` ต้องตรงกับ `SALES_ASOF` ในหน้า · `channels_changed` บอกว่าอาเรย์ไหนในหน้าไหนจะเปลี่ยน
ถ้า `status` เป็น `ERROR` → **หยุดและรายงาน** ห้ามแก้ตัวเลขเองหรือเขียนวิธีอื่น

### 2. รันจริง

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/shipnity_update.py"
```

exit code: `0` = อัปเดตแล้ว (bump sw.js ให้ด้วย) · `10` = ไม่มีอะไรเปลี่ยน · `2` = ไม่ผ่านด่านตรวจ ไม่ได้เขียนไฟล์

สคริปต์จะไม่ยอมเขียนทับถ้า: ขาดคีย์ที่ JS ต้องใช้ · `lines` > 500,000 · `date_min` < 2020 · `date_max` < `date_min` · RAW > 20 MB

### 3. commit (เฉพาะตอน exit 0)

```bash
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" add "Data Shipnity/Sales_Dashboard.html" WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
    commit -m "auto-update: Shipnity Top สินค้าขายดี $(date +%Y-%m-%d)"
```

ไม่ต้อง `git push` — launchd `com.wibwub.autopush` push ให้เองภายใน 2 นาที

---

## RULES

- ทำทุกอย่างใน bash/python ห้าม spawn subagents
- ตัวเลขทุกตัวให้สคริปต์คำนวณ ห้ามคิดเอง ห้ามกรอกค่าสมมุติ
- ถ้า dry-run หรือรันจริงได้ `ERROR` / exit 2: หยุดและรายงาน **ห้ามหาทางอ้อม ห้าม reimplement**
- ถ้าต้องแก้วิธีคำนวณ ให้แก้ `process_shipnity()` ใน `wibwub_update.py` ที่เดียว อย่าแก้ที่ไฟล์นี้
- การ map ช่องทาง -> อาเรย์ อยู่ใน `CH_ARRAYS` / `CH_ORDERS` ของ `scripts/shipnity_update.py`
  (`LINE_REV` = Line OA + Line Shopping · `BEUK_REV` = เบิกของ · `CARE_REV` = Carcare)
- **ห้ามแก้อาเรย์ช่องทางด้วยมือ** ให้สคริปต์เขียนเท่านั้น ไม่งั้นสองหน้าจะหลุดจากกันอีก

## สรุปท้ายรอบ (สั้น ๆ ภาษาไทย)

ช่วงวันที่ที่ครอบคลุม (`date_min` → `date_max`), `asof` ที่ใช้ตัด, จำนวน lines / order_counts / products,
ขนาดหน้าก่อน-หลัง, อาเรย์ช่องทางที่เปลี่ยน + ยอด FB/LINE/CARE ของเดือนล่าสุด,
commit id หรือ "ไม่มีข้อมูลใหม่", และ error ถ้ามี

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
