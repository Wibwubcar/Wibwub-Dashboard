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
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" add WIBWUB_Mobile.html sw.js
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
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
