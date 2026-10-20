---
name: wibwub-sales-update
description: ทุกวัน 08:30/19:30 — อ่านชีตยอดขาย Shopee/TikTok/Lazada → อัปเดต SALES arrays ใน Dashboard + Mobile
---

## WIBWUB — อัปเดตยอดขายรายเดือนจาก Google Sheets

BASE = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`

**ไม่ต้องใช้เบราว์เซอร์เลย** — อ่านชีตผ่าน service account (`~/wibwub-service-account.json`)

> **ห้ามเขียนสคริปต์อ่านชีต/คำนวณเอง** ตัวคำนวณจริงคือ `process_sales()` ใน `wibwub_update.py`
> ซึ่งมีด่านกันข้อมูลหายที่เขียนเองแล้วมักลืม (months_shrunk, length guard, zero-merge guard)
>
> **ห้ามแตะเด็ดขาด:**
> - `TOTAL_REV` / `TOTAL_ORD` — เป็น **derived const ใน JS** ไม่ใช่ data array
>   (Dashboard รวม 6 ช่องทาง SH+TK+LZ+FB+LINE+WEB · Mobile รวม 10 ช่องทาง)
>   พรอมป์เวอร์ชันเก่าสั่งให้เขียนทับด้วยสูตร SH+TK+LZ ซึ่งจะทำยอด ต.ค. หายไป **902,653 บาท (11.5%)**
>   และทำลายสูตรถาวร
> - `MP_DATE_MAX` / `MP_MONTH_BOUNDS` — หน้าเว็บคำนวณเองจาก `MTD_COVERAGE` แล้ว

---

## ขั้นตอน

### 1. ดูก่อนว่าจะเปลี่ยนอะไร

```bash
python3 "$BASE/scripts/sales_update.py" --dry-run
```

ตรวจด้วยตา: `months` ต้องไม่น้อยกว่ารอบก่อน · `latest.SH_REV` / `TK_REV` / `LZ_REV` ต้องสมเหตุสมผล
ถ้า `status` เป็น `ERROR` → **หยุดและรายงาน ห้ามแก้ตัวเลขเอง ห้ามเขียนวิธีอื่น**

ด่านที่สคริปต์จะปฏิเสธการเขียน: เดือนหดลง · `SH_REV`/`TK_REV` เป็น 0 ทั้งหมด ·
ค่าเดือนเก่าลดลงเกิน 2% (ยอดสะสมไม่ควรลด) · จำนวนเดือนผิดปกติ

### 2. รันจริง

```bash
python3 "$BASE/scripts/sales_update.py"
```

exit `0` = อัปเดตแล้ว (bump sw.js ให้ด้วย) · `10` = ไม่มีอะไรเปลี่ยน · `2` = ไม่ผ่านด่าน ไม่ได้เขียนไฟล์

### 3. commit (เฉพาะตอน exit 0)

```bash
git -C "$BASE" add WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js
git -C "$BASE" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
    commit -m "auto-update: sales from Sheets $(date +%Y-%m-%d)"
```

ไม่ต้อง `git push` — launchd `com.wibwub.autopush` push ให้เองภายใน 2 นาที
ถ้า git ติด `index.lock`: รอ 20 วินาทีแล้วลองใหม่ สูงสุด 3 ครั้ง **ห้ามลบ lock ของคนอื่น**

---

## RULES

- ทำทุกอย่างใน bash/python ห้าม spawn subagents · ห้ามใช้เบราว์เซอร์
- ตัวเลขทุกตัวให้สคริปต์คำนวณ ห้ามคิดเอง ห้ามกรอกค่าสมมุติ
- `grep -oP`, `sed -i "s/.../"`, `find -newermt` เป็น **GNU-only พังบน macOS** ห้ามใช้
  (bump sw.js ให้สคริปต์ทำ อย่าเขียน sed เอง — พรอมป์เก่าพังตรงนี้และ echo ว่าสำเร็จทั้งที่ไม่ได้ทำ)
- ถ้าต้องแก้วิธีคำนวณหรือ ID ชีต ให้แก้ `wibwub_update.py` ที่เดียว อย่าแก้ที่ไฟล์นี้

## สรุปท้ายรอบ (สั้น ๆ ภาษาไทย)

จำนวนเดือนที่ได้, ยอดเดือนล่าสุดของ Shopee / TikTok / Lazada (ยอดขาย + ออเดอร์),
ไฟล์ที่เปลี่ยน, commit id หรือ "ไม่มีข้อมูลใหม่", และ error ถ้ามี

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
