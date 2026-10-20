---
name: wibwub-monday-update
description: ทุกวัน 09:10/20:10 — อัปเดต Top สินค้า (ALL_PRODUCTS + PROD_MO) ใน WIBWUB_Mobile.html จาก Shipnity
---

## WIBWUB — Top สินค้าในหน้ามือถือ

BASE = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`

อัปเดต `ALL_PRODUCTS` (15 สินค้า) และ `PROD_MO` (ยอดรายเดือนต่อสินค้า) ใน `WIBWUB_Mobile.html`

> **งานนี้เหลือแค่ส่วนสินค้าแล้ว** — ส่วนอื่นที่เคยอยู่ในพรอมป์เก่าย้ายไปที่อื่นหมด:
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

### 1. ดูก่อนว่าจะเปลี่ยนอะไร

```bash
python3 "$BASE/scripts/products_update.py" --dry-run
```

ใช้ cache ของ Shipnity (`scripts/ship_cache.py`) — รอบที่ไม่มีไฟล์ใหม่ใน `Data Shipnity/`
จะเสร็จใน <1 วินาที ถ้ามีไฟล์ใหม่จะคำนวณใหม่ ~6 นาที

ตรวจด้วยตา: `asof` ต้องเป็นวันเดียวกับ `SALES_ASOF` · `products` = 15 ·
`reordered` บอกว่าอันดับสินค้าสลับที่ไหนบ้าง (ปกติได้ ถ้าสลับเยอะผิดปกติให้ดูก่อน)

ด่านที่สคริปต์จะปฏิเสธการเขียน: ยอดสินค้าใดต่างจากเดิมเกิน **2%** (แปลว่า `NAME_MAP`
ผิดหรือมี SKU ใหม่) · ชื่อใน `NAME_MAP` หายไปจาก Shipnity · `node --check` ไม่ผ่าน

### 2. รันจริง + commit

```bash
python3 "$BASE/scripts/products_update.py"
```

exit `0` = อัปเดต + bump sw.js · `10` = ไม่มีอะไรเปลี่ยน · `2` = ไม่ผ่านด่าน

```bash
git -C "$BASE" add WIBWUB_Mobile.html sw.js
git -C "$BASE" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
    commit -m "auto-update: Top สินค้า $(date +%Y-%m-%d)"
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
