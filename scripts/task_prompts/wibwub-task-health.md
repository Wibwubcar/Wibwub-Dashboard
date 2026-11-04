---
name: wibwub-task-health
description: ทุกชั่วโมง 08:00–23:00 — เขียน scripts/ops/task_health.json ให้หน้า Dashboard อ่าน
---

## 📂 ขั้น 0 — ไม่มีขั้นหาโฟลเดอร์ ห้ามใช้ shell ค้นหา

สคริปต์หาโฟลเดอร์ All เองจากตำแหน่งไฟล์ (marker `sw.js` + `.git`)
จึง**ไม่ต้องหา `BASE` ก่อน** ให้เขียนพาธเต็มในคำสั่ง `python3` ได้เลย

**ห้ามรันลูป `for` / `[ -d ... ]` / ตั้งตัวแปร `BASE=` / `cd` เพื่อหาพาธ**
**คำสั่ง shell แรกของรอบต้องขึ้นต้นด้วย `python3` เสมอ**

ถ้าคำสั่ง `python3` ตอบว่าไม่พบไฟล์ ให้ลองพาธสำรองที่ขึ้นต้นด้วย `~/mnt/All/` **หนึ่งครั้ง**
ถ้ายังไม่ได้ → **หยุดทันที** รายงานว่า `❌ ล้มเหลว — เข้าโฟลเดอร์ All ไม่ได้` แล้วจบงาน

---

## WIBWUB — สถานะงานอัตโนมัติ (task_health.json)

BASE = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`

**ไม่ต้องใช้เบราว์เซอร์ ไม่ต้องใช้ชีต** — อ่านไฟล์เซสชันในเครื่องอย่างเดียว

> แยกออกมาเป็นงานของตัวเองเมื่อ 3 พ.ย. 69 — ก่อนหน้านั้นเป็น "ขั้นที่ 2"
> ของงาน `wibwub-hr-attendance-1200-2200` จึงรีเฟรชแค่วันละ 3 ครั้ง (10:30/20:30/00:30)
> ผู้ใช้เห็นหน้าสถานะค้างที่สแนปช็อตเก่าแล้วเข้าใจผิดว่างานตั้งเวลาพัง
>
> **ต้องรันจากงานฝั่ง code เท่านั้น** — ฝั่ง local อยู่ในแซนด์บ็อกซ์ อ่านไฟล์เซสชันใน
> `~/Library/Application Support` ไม่ได้ จะได้ผล "ตรวจไม่ได้" ทุกแถว

---

## ขั้นตอน

### 1. เขียนสถานะ

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/ops/task_health.py" --write-json
```

- exit `0` = ไม่มีงานค้าง · exit `3` = มี ⛔ หรืออ่านบางส่วนไม่ได้
- **exit 3 ไม่ใช่ความผิดพลาดของรอบนี้** ให้เอาบรรทัดสรุปที่มันพิมพ์ออกมาขึ้นรายงานแล้วทำงานต่อ
- **ห้ามไปหยุดหรือแก้งานที่ค้างเอง** งานนี้รายงานอย่างเดียว
- ถ้าคำสั่งนี้ล้ม ให้รายงานว่าเขียนสถานะไม่ได้ **ห้ามข้ามเงียบ ๆ**

### 2. commit

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" add scripts/ops/task_health.json
```

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" commit -m "auto-update: สถานะงานอัตโนมัติ <วันที่วันนี้ เช่น 2026-11-04>"
```

- **ข้อความ commit ใช้ `$(date +%Y-%m-%d)` เท่านั้น ห้ามเติมเวลา `%H:%M` และห้ามมีช่องว่าง
  escape (`\ `) ใน `$( )`** — เกิดจริง 3 พ.ย. 69 19:12: รอบแรกของงานนี้ใช้
  `$(date +%Y-%m-%d\ %H:%M)` แล้วเด้งกล่องขออนุญาตที่ไม่มีคนกด **ค้าง 4 ชั่วโมง**
  และทำให้รอบ 20:00/21:00/22:00/23:00 ถูกข้ามทั้งหมด
  (พรอมป์อื่นทุกตัวใช้ `$(date +%Y-%m-%d)` เปล่า ๆ และผ่านมาตลอด)
  เวลาที่ตรวจอยู่ในฟิลด์ `checked_at` ของ JSON แล้ว ไม่ต้องใส่ในข้อความ commit
- **add แล้วต้อง commit คำสั่งถัดไปทันที** ไม่งั้นงานอื่นจะกวาด index ไปใช้
  (เกิดจริงรอบ 19:12: add ไปแล้วแต่ commit ค้าง ไฟล์จึงถูกงาน ads-daily 19:47 พาไป commit)
- **add เฉพาะ `scripts/ops/task_health.json` ไฟล์เดียว** ห้าม `add -A` — ไฟล์ dirty อื่นในรีโป
  เป็นของงานอื่นที่ยังทำไม่เสร็จ
- ถ้าไม่มีอะไรเปลี่ยน commit จะคืน exit 1 พร้อม "nothing to commit" → ถือว่าปกติ ไม่ใช่ error
- ไม่ต้อง `git push` — launchd `com.wibwub.autopush` push ให้เองภายใน 2 นาที
- ถ้า git ติด index.lock: รอ 20 วินาทีแล้วลองใหม่ สูงสุด 3 ครั้ง **ห้ามลบ lock ของคนอื่น**

---

## RULES

- ตัวเลขและสถานะทุกตัวให้สคริปต์คำนวณ **ห้ามแก้ JSON ด้วยมือ ห้ามกรอกค่าสมมุติ**
- ถ้าเกณฑ์ตัดสินผิด (เช่นงานที่จบแล้วขึ้นว่าค้าง) ให้แก้ `scripts/ops/task_health.py`
  หรือ `scripts/ops/task_expect.json` ที่เดียว **แล้วทำสำเนา `.bak-<วันที่>-<เรื่อง>` ก่อนแก้**
  (`.bak*` อยู่ใน .gitignore ไม่เข้า repo)
- `grep -oP`, `sed -i "s/.../"` เป็น GNU-only **พังบน macOS** ห้ามใช้
- งานนี้ซ้อนกับ "ขั้นที่ 2" ของ `wibwub-hr-attendance-1200-2200` ที่ยังเรียกสคริปต์เดียวกัน
  อยู่โดยตั้งใจ (กันกรณีงานนี้ไม่ได้รัน + ครอบรอบ 00:30 ที่อยู่นอกช่วง 08:00–23:00)
  เขียนไฟล์เดียวกันซ้ำไม่เสียหาย

## สรุปท้ายรอบ (สั้น ๆ ภาษาไทย)

`checked_at` · counts (stop/warn/ok/sheet_wait/gaps) · รายชื่อแถวที่เป็น ⛔ หรือ ⚠️
พร้อมเหตุผลสั้น ๆ · ช่วงที่ไม่มีงานไหนเริ่มเลย (gaps) ถ้ามี · commit id หรือ "ไม่มีอะไรเปลี่ยน"

**ถ้ามีแถว ⛔ ให้ขึ้นบรรทัดแรกของรายงานด้วย `⛔ <ชื่องาน> — <เหตุผล>`** เพื่อให้เห็นทันที
