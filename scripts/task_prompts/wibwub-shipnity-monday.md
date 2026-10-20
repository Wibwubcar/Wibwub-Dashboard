---
name: wibwub-shipnity-monday
description: อัปเดต Top สินค้าขายดี (Sales_Dashboard.html) จาก Excel ใน Data Shipnity ทุกวันจันทร์ 10:00 น.
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
python3 "$BASE/scripts/shipnity_update.py" --dry-run
```

ใช้เวลาราว 1–2 นาที (ไฟล์ ~160 ไฟล์) จะได้ JSON เช่น:
`{"status":"DRY_RUN","lines":44216,"order_counts":1862,"products":217,"channels":17,"date_min":"2026-01-01","date_max":"2026-10-19","raw_mb":2.26,"page_mb_before":2.11}`

ตรวจด้วยตา: `date_max` ควรเป็นวันล่าสุดที่มีไฟล์ · `lines` ควรอยู่หลักหมื่น ไม่ใช่หลักล้าน · `raw_mb` ควรใกล้ `page_mb_before`
· `asof` ต้องตรงกับ `SALES_ASOF` ในหน้า · `channels_changed` บอกว่าอาเรย์ไหนในหน้าไหนจะเปลี่ยน
ถ้า `status` เป็น `ERROR` → **หยุดและรายงาน** ห้ามแก้ตัวเลขเองหรือเขียนวิธีอื่น

### 2. รันจริง

```bash
python3 "$BASE/scripts/shipnity_update.py"
```

exit code: `0` = อัปเดตแล้ว (bump sw.js ให้ด้วย) · `10` = ไม่มีอะไรเปลี่ยน · `2` = ไม่ผ่านด่านตรวจ ไม่ได้เขียนไฟล์

สคริปต์จะไม่ยอมเขียนทับถ้า: ขาดคีย์ที่ JS ต้องใช้ · `lines` > 500,000 · `date_min` < 2020 · `date_max` < `date_min` · RAW > 20 MB

### 3. commit (เฉพาะตอน exit 0)

```bash
git -C "$BASE" add "Data Shipnity/Sales_Dashboard.html" WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js
git -C "$BASE" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
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

## 🚫 กฎคำสั่ง shell (ทุกงาน — รวมคำสั่งที่คิดขึ้นเองระหว่างรัน)

**ห้ามขึ้นต้นคำสั่งด้วย `cd` เด็ดขาด** — ทั้งกับ `git` และ `python3`

คำสั่งที่ขึ้นต้นด้วย `cd` ไม่แมตช์กฎที่อนุญาตไว้แล้ว (`Bash(python3 *)` / `Bash(git *)`)
จึงเด้งถามทุกครั้ง และถ้ามี `git` ร่วมด้วยจะโดนตัวตรวจตีธงซ้ำอีกชั้น
ตัวตรวจความปลอดภัยจะหยุดงานแล้วรอคนกดอนุญาต ("changes directory before running git,
which can execute untrusted hooks") ซึ่งงานตั้งเวลาไม่มีคนนั่งกด = ค้างทั้งรอบ

| ❌ ห้าม | ✅ ใช้แบบนี้ |
|---|---|
| `cd "$BASE" && git status` | `git -C "$BASE" status` |
| `cd "$BASE"` ขึ้นบรรทัดใหม่แล้วตามด้วย `git ...` | `git -C "$BASE" ...` |
| `cd "$BASE" && python3 x.py; git status` | แยกเป็น 2 คำสั่ง · ใช้ `python3 "$BASE/x.py"` และ `git -C "$BASE" status` |

เรียกสคริปต์ด้วย path เต็มเสมอ (`python3 "$BASE/scripts/..."`) จะได้ไม่ต้อง `cd`
ถ้าจำเป็นต้อง `cd` จริง ๆ (เช่นสคริปต์อ่าน path สัมพัทธ์) **ห้ามมี `git` อยู่ในคำสั่งนั้น**
