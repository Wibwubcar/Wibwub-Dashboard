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
cd "$BASE" && python3 scripts/tiktok_content_update.py --dry-run
```

ตรวจด้วยตา: `posts` ไม่ควรน้อยกว่า `before` · `zero_month` ควรเป็น **0** ·
`months` ควรต่อเนื่องถึงเดือนปัจจุบัน

ด่านที่สคริปต์จะปฏิเสธการเขียน: จำนวนคลิปหดเกิน 10% · คลิปที่พาร์สเดือนไม่ออกเกิน 30% ·
ชีต CONTENT สั้นผิดปกติ (< 20 แถว)
ถ้า `status` เป็น `ERROR` → **หยุดและรายงาน ห้ามแก้ตัวเลขเอง**

### 2. รันจริง + commit

```bash
cd "$BASE" && python3 scripts/tiktok_content_update.py
```

exit `0` = อัปเดต + bump sw.js · `10` = ไม่มีอะไรเปลี่ยน · `2` = ไม่ผ่านด่าน

```bash
cd "$BASE"
git add WIBWUB_TikTok_Dashboard_v7.html WIBWUB_Mobile.html sw.js
git -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
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
