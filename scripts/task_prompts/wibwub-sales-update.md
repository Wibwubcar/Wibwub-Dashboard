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
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/sales_update.py" --dry-run
```

ตรวจด้วยตา: `months` ต้องไม่น้อยกว่ารอบก่อน · `latest.SH_REV` / `TK_REV` / `LZ_REV` ต้องสมเหตุสมผล
ถ้า `status` เป็น `ERROR` → **หยุดและรายงาน ห้ามแก้ตัวเลขเอง ห้ามเขียนวิธีอื่น**

ด่านที่สคริปต์จะปฏิเสธการเขียน: เดือนหดลง · `SH_REV`/`TK_REV` เป็น 0 ทั้งหมด ·
ค่าเดือนเก่าลดลงเกิน 2% (ยอดสะสมไม่ควรลด) · จำนวนเดือนผิดปกติ

### 2. รันจริง

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/sales_update.py"
```

exit `0` = อัปเดตแล้ว (bump sw.js ให้ด้วย) · `10` = ไม่มีอะไรเปลี่ยน · `2` = ไม่ผ่านด่าน ไม่ได้เขียนไฟล์

### 3. commit (เฉพาะตอน exit 0)

```bash
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" add WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
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
