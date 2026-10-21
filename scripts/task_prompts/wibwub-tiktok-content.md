---
name: wibwub-tiktok-content
description: ทุกวัน 09:25/20:25 — อ่านชีต CONTENT → อัปเดต ALL_POSTS ใน WIBWUB_TikTok_Dashboard_v7.html
---

## WIBWUB — คลิป TikTok (ALL_POSTS)

BASE = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`

**ไม่ต้องใช้เบราว์เซอร์** — อ่านชีต CONTENT ผ่าน service account (`~/wibwub-service-account.json`)

> งานนี้แยกออกมาจาก `wibwub-dashboard-update` ที่ถูกยุบ (20 ต.ค. 2569)
> ก่อนหน้านั้น `ALL_POSTS` **ไม่มีใครดูแลเลยตั้งแต่ 28 ก.ย.** ทั้งที่หน้า TikTok
> ยังอยู่ในเมนูหน้าหลัก
>
> **ห้ามเขียนสคริปต์อ่านชีตเอง** ตัวคำนวณคือ `process_tiktok_content()` ใน `wibwub_update.py`
> ซึ่งมี guard กันบั๊กที่เคยทำกราฟ Social ว่างทั้งหน้า (ดูสกิล
> `wibwub-tiktok-social-charts-known-bugs`) — ถ้าชีตเปลี่ยนโครงสร้างจน day/month
> พาร์สไม่ออก มันจะข้ามการเขียนแทนที่จะล้างข้อมูลทิ้ง

---

## ขั้นตอน

### 1. ดูก่อน

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/tiktok_content_update.py" --dry-run
```

ตรวจด้วยตา: `posts` ไม่ควรน้อยกว่า `before` · `zero_month` ควรเป็น **0** ·
`months` ควรต่อเนื่องถึงเดือนปัจจุบัน

ด่านที่สคริปต์จะปฏิเสธการเขียน: จำนวนคลิปหดเกิน 10% · คลิปที่พาร์สเดือนไม่ออกเกิน 30% ·
ชีต CONTENT สั้นผิดปกติ (< 20 แถว)
ถ้า `status` เป็น `ERROR` → **หยุดและรายงาน ห้ามแก้ตัวเลขเอง**

### 2. รันจริง + commit

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/tiktok_content_update.py"
```

exit `0` = อัปเดต + bump sw.js · `10` = ไม่มีอะไรเปลี่ยน · `2` = ไม่ผ่านด่าน

```bash
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" add WIBWUB_TikTok_Dashboard_v7.html WIBWUB_Mobile.html sw.js
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
    commit -m "auto-update: TikTok content $(date +%Y-%m-%d)"
```

ไม่ต้อง `git push` — launchd `com.wibwub.autopush` push ให้เองภายใน 2 นาที

---

## RULES

- ตัวเลขทุกตัวให้สคริปต์คำนวณ ห้ามคิดเอง · `eng` และ `er` คำนวณจาก love+comment+share+save
  ห้ามคัดลอกจากชีต (สคริปต์ทำให้แล้ว)
- ถ้าต้องแก้วิธีอ่านชีต ให้แก้ `process_tiktok_content()` ใน `wibwub_update.py` ที่เดียว
- `grep -oP`, `sed -i "s/.../"` เป็น GNU-only **พังบน macOS** ห้ามใช้
- ถ้ากราฟ Social ว่างเปล่าหลังรัน ให้อ่านสกิล `wibwub-tiktok-social-charts-known-bugs`
  ก่อนวินิจฉัยใหม่ — มีสาเหตุที่เคยเจอและแก้ไปแล้ว 2 ข้อบันทึกไว้

## สรุปท้ายรอบ (สั้น ๆ ภาษาไทย)

จำนวนคลิปก่อน/หลัง, เดือนที่มีข้อมูล, คลิปที่พาร์สเดือนไม่ออก (ควรเป็น 0),
commit id หรือ "ไม่มีข้อมูลใหม่", error ถ้ามี

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
