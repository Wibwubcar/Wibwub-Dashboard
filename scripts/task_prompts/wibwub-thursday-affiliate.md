---
name: wibwub-thursday-affiliate
description: ทุกวัน 08:50/19:50 — โหลดไฟล์ TikTok Affiliate → อัปเดต Affiliate Dashboard + Mobile
---

## WIBWUB — อัปเดตข้อมูล Affiliate

BASE = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`

อัปเดต `AF_MO / AF_GMV / AF_NET / AF_COM / AF_CR / CREATORS / CREATOR_MONTHS` ใน
`WIBWUB_Affiliate_Dashboard.html` และ `AFI_GMV / AFI_NET / AFI_COMM` ใน `WIBWUB_Mobile.html`

> **ห้ามเขียนสคริปต์อ่าน xlsx เอง** ตัวคำนวณจริงคือ `process_affiliate()` ใน `wibwub_update.py`
>
> เหตุผล — พรอมป์เวอร์ชันเก่า hardcode คอลัมน์ `1/2/10` ให้ทุกไฟล์ แต่ไฟล์มี **2 รูปแบบ
> ที่ตำแหน่งคอลัมน์ไม่เหมือนกัน**:
> - `Creator_List_*` : returns = col21 · commission = col7
> - `Transaction_Analysis_Creator_List_*` : returns = col4 · commission = col21
>
> ผลคือ commission ไปอ่านคอลัมน์ "จำนวนโชว์เคส" (เลขหลักหน่วย) และ net สูงกว่า gmv หรือติดลบ
> ตัวจริงใช้ `find_col()` จับจากชื่อ header จึงถูกทั้งสองแบบ
> และต้องกรองเฉพาะไฟล์ชื่อมี `Creator_List` (โฟลเดอร์มี Product_List / Video_List /
> Live_List / Core_Metrics / WIBWUB_KOL_Tracker ปนอยู่) แล้วเลือกไฟล์ที่ช่วงวันที่
> **overlap กับเดือนมากสุด** ไม่ใช่ mtime ใหม่สุด

---

## ขั้นที่ 1 — โหลดไฟล์ใหม่จาก TikTok Affiliate (ถ้ามี)

1. Chrome: `list_connected_browsers` → `select_browser` deviceId `b75a6bb0-5b78-4e44-92a8-75224f1ce4ee` → `tabs_context_mcp(createIfEmpty=true)`
2. โหลด **Creator List** ของเดือนปัจจุบันจาก TikTok Affiliate (Transaction Analysis → Creator)
   ถ้าขึ้นหน้า login: **หยุดและรายงาน ห้ามกรอกรหัสผ่าน**
3. ปิดแท็บด้วย `tabs_close_mcp`
4. ย้ายไฟล์เข้าที่ (launchd `com.wibwub.download-mover` อาจย้ายให้แล้ว):

```bash
ls -lt "$BASE/Data Affiliate"/*Creator_List*.xlsx | head -3
```

ถ้าไม่มีไฟล์ใหม่ก็ **ไม่เป็นไร** — ขั้นถัดไปจะคำนวณจากไฟล์ที่มีอยู่และจบด้วย `NO_CHANGE`

## ขั้นที่ 2 — ดูก่อนว่าจะเปลี่ยนอะไร

```bash
cd "$BASE" && python3 scripts/affiliate_update.py --dry-run
```

ตรวจด้วยตา: `latest_month` ควรเป็นเดือนปัจจุบัน · `AF_GMV` ไม่ควรต่ำกว่า `current_page.AF_GMV`
· `AF_NET` ต้อง ≤ `AF_GMV` · `AF_COM` ควรเป็นหลักแสน ไม่ใช่หลักหน่วย

ด่านที่สคริปต์จะปฏิเสธการเขียน: net > gmv · net ติดลบ · commission เล็กผิดปกติ ·
เดือนหดลง · GMV เดือนเก่าลดเกิน 2%
ถ้า `status` เป็น `ERROR` → **หยุดและรายงาน ห้ามแก้ตัวเลขเอง**

## ขั้นที่ 3 — รันจริง

```bash
cd "$BASE" && python3 scripts/affiliate_update.py
```

exit `0` = อัปเดต + bump sw.js แล้ว · `10` = ไม่มีอะไรเปลี่ยน · `2` = ไม่ผ่านด่าน
ดู `mobile_mismatch` ต้องเป็น `[]` (ค่าใน Mobile ตรงกับ Affiliate Dashboard)

## ขั้นที่ 4 — VIDEOS (ถ้ามีไฟล์วีดีโอใหม่)

```bash
cd "$BASE" && python3 scripts/vid_merge.py
```

อ่านจาก `Data Affiliate/วีดีโอ/` แล้ว merge เข้า `const VIDEOS` ในหน้า Affiliate
(พรอมป์เก่าคัดลอกโค้ดตัวนี้มาทั้งก้อน — ใช้ไฟล์จริงแทน อย่า inline)

## ขั้นที่ 5 — commit (เฉพาะตอนมีอะไรเปลี่ยน)

```bash
cd "$BASE"
git add WIBWUB_Affiliate_Dashboard.html WIBWUB_Mobile.html sw.js "Data Affiliate"
git -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
    commit -m "auto-update: Affiliate $(date +%Y-%m-%d)"
```

ไม่ต้อง `git push` — launchd `com.wibwub.autopush` push ให้เองภายใน 2 นาที
ถ้า git ติด `index.lock`: รอ 20 วินาทีแล้วลองใหม่ สูงสุด 3 ครั้ง **ห้ามลบ lock ของคนอื่น**

---

## RULES

- ตัวเลขทุกตัวให้สคริปต์คำนวณ ห้ามคิดเอง ห้ามกรอกค่าสมมุติ
- `grep -oP`, `sed -i "s/.../"`, `find -newermt` เป็น GNU-only **พังบน macOS** ห้ามใช้
- ถ้าต้องแก้วิธีคำนวณ ให้แก้ `process_affiliate()` ใน `wibwub_update.py` ที่เดียว
- **ห้ามแก้อาเรย์ด้วยมือ** ให้สคริปต์เขียนเท่านั้น ไม่งั้น Affiliate Dashboard กับ Mobile จะหลุดจากกัน

## สรุปท้ายรอบ (สั้น ๆ ภาษาไทย)

เดือนล่าสุด + GMV / Net / Commission / จำนวนครีเอเตอร์, จำนวน creator ในตาราง,
`mobile_mismatch` ว่าง/ไม่ว่าง, VIDEOS ที่เพิ่ม (ถ้ารัน), commit id หรือ "ไม่มีข้อมูลใหม่", error ถ้ามี
