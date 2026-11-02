---
name: wibwub-ads-daily
description: ทุกวัน 09:45/20:45 — ขั้น 8 เดิมของ Ads รายวัน: kol_fetch.py + event_fetch.py + marketing_update.py → หน้า "การตลาด vs ยอดขาย" · ไม่ใช้เบราว์เซอร์ จึงรันบนฝั่ง code ได้ และไม่นับในเพดาน 3 งานพร้อมกันของฝั่ง local · รันหลังงาน local "โหลด order+Lazada+Ads" (จบ ~09:28) และ "ยอดขายจากชีต" (จบ ~09:38) · พรอมป์เลิกใช้ cd แล้วตั้งแต่ 24 ต.ค. ทุกคำสั่งขึ้นต้นด้วย python3 พาธเต็ม (ทดสอบรอบจริง 22:59 ผ่าน commit 51eec9e)
---

อ่านไฟล์นี้ด้วย Read tool เพื่อดูรายละเอียดขั้นตอน (อ่านเฉพาะหัวข้อ "ขั้น 8" เท่านั้น):

/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/task_prompts/ads_daily.md

งานนี้ทำ **เฉพาะขั้น 8** ของไฟล์นั้น (เมนู "การตลาด vs ยอดขาย") เท่านั้น
ขั้น 1-7 (ดึง Shopee/TikTok/Lazada + merge + commit ไฟล์ Ads) เป็นหน้าที่ของงาน local
"โหลด order ทุกแพลตฟอร์ม" รอบ 08:35/19:35 แล้ว **ห้ามทำซ้ำ ห้ามเปิดเบราว์เซอร์**
ถ้าคิดว่าต้องเปิด Chrome แปลว่าอ่านผิด ให้อ่านใหม่

## 🚫 กฎคำสั่ง shell — ผิดข้อนี้งานจะค้างตลอดไป

**ห้ามใช้ `cd` เด็ดขาด ไม่ว่าจะเป็น `cd X && ...` หรือ `cd X` บรรทัดเดียว**
คำสั่งที่ขึ้นต้นด้วย `cd` ไม่แมตช์กฎอนุญาต `Bash(python3:*)` จึงเด้งกล่องขออนุญาตที่ไม่มีใครกด
แล้วงานจะค้างไปเรื่อย ๆ (เกิดจริง 24 ต.ค. 69 รอบ 20:47 ค้าง 1 ชม. 45 นาที)

**ทุกคำสั่งต้องขึ้นต้นด้วย `python3` แล้วตามด้วยพาธเต็มในเครื่องหมายคำพูด**
สคริปต์ทุกตัวหาโฟลเดอร์ All เองจากตำแหน่งไฟล์ จึงไม่ต้อง cd เข้าไปก่อน

## ขั้นตอน

ตั้ง BASE ไว้อ่านง่าย (ใช้แทนในคำสั่งข้างล่าง ห้ามใช้ cd)

BASE = /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All

### 1. เช็คว่าต้นทางอัปเดตแล้วหรือยัง

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/ads/ads_daily_update.py" state
```

ดูค่า `last` — ถ้าเป็นวันก่อนเมื่อวาน แปลว่างาน local ยังไม่ได้รันหรือรันไม่สำเร็จ
ให้รายงานว่า "ต้นทางยังไม่อัปเดต (ads_daily.json ถึงแค่ <วันที่>)" แล้วทำขั้น 2-3 ต่อได้เลย

### 2. ดึงยอด KOL + ค่า Event แล้วรวมผล

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/marketing/kol_fetch.py"
```

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/marketing/event_fetch.py"
```

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/marketing/marketing_update.py"
```

**รันทีละคำสั่ง ห้ามเอามาต่อกันด้วย `&&` หรือ `;`**

- `kol_fetch.py` → exit 0 = อัปเดต · 10 = ยอดไม่เปลี่ยน (ทั้งคู่ผ่าน) · 2 = ไม่ผ่านด่าน ให้รายงาน
- `event_fetch.py` → exit 0 = เขียนไฟล์แล้ว (ดู `status`: `UPDATED` / `NO_CHANGE`) · 2 = ไม่ผ่านด่าน
  `"pay_date_col": false` = ชีต Annual Budget ยังไม่มีคอลัมน์ "วันที่จ่าย" **ไม่ใช่บั๊ก**
  ช่อง Event จะอยู่ใน `still_missing` ต่อไป หน้าเว็บขึ้น "รอข้อมูล" ตามที่ตกลงไว้
  ถ้า exit 2 ให้รายงานข้อความที่สคริปต์คืนมาตรง ๆ **ห้ามกรอกตัวเลข Event มือใน mkt_manual.json**
  (marketing_update.py จะตายทันทีถ้าเจอ)
- `marketing_update.py` → exit 0 = UPDATED · 10 = ไม่มีอะไรเปลี่ยน · 2 = ไม่ผ่านด่านเทียบรายช่องทาง
  ให้รายงานว่าช่องไหนต่างเท่าไร
- ถ้า exit 2 เพราะชีตยอดขายยังกรอกไม่ถึงวันล่าสุด **ไม่ใช่บั๊ก** ให้รายงานว่ารอคนกรอกชีต

### 3. commit ถ้ามีไฟล์เปลี่ยน

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" add "data Ads/kol_monthly.json" "data Ads/event_daily.json" WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js
```

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" commit -m "auto-update: การตลาด vs ยอดขาย"
```

`gitw.py` ทำงานในโฟลเดอร์ All ให้เองอยู่แล้ว ไม่ต้อง cd
auto-push (launchd com.wibwub.autopush) จะ push ให้เองภายใน 2 นาที **ไม่ต้อง git push**
ถ้าไม่มีอะไรเปลี่ยน ข้ามขั้นนี้ได้

## กติกา

- ตัวเลขทุกตัวให้สคริปต์คำนวณ **ห้ามคิดเองหรือแก้ไฟล์ JSON เอง**
- git add เฉพาะ 4 ไฟล์ข้างบน รีโปนี้มีงานอื่นทำงานพร้อมกัน ไฟล์ dirty ที่เหลือเป็นของคนอื่น **ห้าม commit ติดไปด้วย**
- ⚠️ ชีต KOL (1NEkm1bcHvXO0Ehs6cwaNDkBUUM1A9assALMp5V7S7lo) มีชื่อ-นามสกุล เลขบัตรประชาชน
  เลขบัญชีธนาคาร ที่อยู่ เบอร์โทร — `kol_fetch.py` อ่านแค่ 4 คอลัมน์และเขียนออกเป็นผลรวมรายเดือนเท่านั้น
  **ห้ามเปิดชีตนี้ด้วยวิธีอื่น ห้ามนำแถวรายบุคคลขึ้นหน้าเว็บ ห้าม commit อะไรที่มีข้อมูลส่วนบุคคล**
  ถ้า `kol_fetch.py` พัง: รายงานแล้วข้าม **ห้าม copy ตัวเลขจากชีตมาใส่มือ**
- ถ้าโฟลเดอร์ All เข้าไม่ถึง: หยุดและรายงานทันทีว่าล้มเหลว **ห้ามใช้ไฟล์เก่าแล้วบอกว่าสำเร็จ**

## รายงานท้ายรอบ (สั้น ๆ ภาษาไทย)

ads_daily.json ถึงวันไหน · ผล kol_fetch (ยอด KOL เดือนนี้) · ผล marketing_update (as-of วันไหน
ด่านเทียบรายช่องทางผ่านหรือไม่ ถ้าไม่ผ่านช่องไหนต่างเท่าไร) · commit id หรือ "ไม่มีอะไรเปลี่ยน" · error ถ้ามี