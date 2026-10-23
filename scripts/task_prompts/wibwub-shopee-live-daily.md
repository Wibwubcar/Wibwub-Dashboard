---
name: wibwub-shopee-live-daily
description: ทุกวัน 08:37/19:37 — ดึง Shopee Live รายวัน → merge SH_LIVE_DAILY ใน WIBWUB_Dashboard.html
---

## 📂 ขั้น 0 — หาโฟลเดอร์ All ก่อนเสมอ (ทำก่อนทุกอย่าง)

พรอมป์นี้ถูกเรียกได้จาก **2 ฝั่ง** และโฟลเดอร์ All อยู่คนละที่กัน
จึง**ห้ามฝังพาธตายตัว** ให้หาด้วยคำสั่งนี้ทุกครั้ง แล้วใช้ผลลัพธ์เป็น `BASE`

```bash
for d in "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" "$HOME/mnt/All" /sessions/*/mnt/All; do [ -d "$d/scripts" ] && echo "$d" && break; done
```

- ได้พาธมา → ใช้เป็น `BASE` ในทุกคำสั่งถัดไป (เขียนพาธเต็มเสมอ ห้ามใช้ตัวแปร shell)
- **ไม่เจอ** หรือ shell ตอบว่า `No folders are connected`
  → **หยุดทันที** รายงานว่า `❌ ล้มเหลว — เข้าโฟลเดอร์ All ไม่ได้` แล้วจบงาน
  ห้ามเดาพาธเอง ห้ามไปใช้ `~/Downloads` แทน

---


## WIBWUB — Shopee Live รายวัน

อัปเดตส่วน "📺 ยอดขายไลฟ์สดรายวัน — Shopee Live" (`SH_LIVE_DAILY`) ใน `WIBWUB_Dashboard.html`

> **ห้ามเขียนสคริปต์อ่าน CSV/คำนวณเอง** ตัวจริงคือ `scripts/shopee_live_daily.py`
> ซึ่งรู้จักกับดักของ export นี้แล้ว (คอลัมน์คู่แฝด, ค่าที่ยังไม่ยืนยัน, ไฟล์เก่าทับไฟล์ใหม่)

---

## ขั้นที่ 1 — โหลด CSV ของ "เมื่อวาน"

1. Chrome: `list_connected_browsers` → `select_browser` deviceId `b75a6bb0-5b78-4e44-92a8-75224f1ce4ee` → `tabs_context_mcp(createIfEmpty=true)`
2. navigate ไป `https://seller.shopee.co.th/creator-center/insight/live`
   (**ไม่ใช่** `/datacenter/live` — path นั้น 404) · รอ 9 วินาที
   ถ้าขึ้นหน้า login: **หยุดและรายงาน ห้ามกรอกรหัสผ่าน**
3. อยู่ที่แท็บ **"ข้อมูลโดยรวม"** · ตรวจ 2 ช่องนี้ด้วย `zoom` ก่อนโหลดเสมอ:
   - `ระยะเวลาเก็บข้อมูล` = **วันเดียว ของเมื่อวาน** (รูปแบบ `DD-MM-YYYY`)
   - `ประเภทคำสั่งซื้อ` = **"คำสั่งซื้อที่ยืนยันแล้ว"**

   > 🚨 ถ้าเป็น **ช่วงวันที่ (range)** ค้างจากแท็บอื่น ทุกช่องจะโชว์ `-` ซึ่งดูเหมือน "ไม่มีไลฟ์"
   > แต่จริง ๆ คือดึงผิด — **ต้องเลือกวันเดี่ยวเสมอ** (สคริปต์มีด่านกันเขียน 0 ทับอีกชั้น)

4. กด **"ดาวน์โหลดข้อมูล"** (มุมขวาของแถบวันที่) รอ 8 วินาที
5. ปิดแท็บด้วย `tabs_close_mcp`
6. ย้ายไฟล์เข้าโฟลเดอร์เก็บ (launchd `com.wibwub.download-mover` อาจย้ายออกจาก Downloads แล้ว):

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/collect_download.py" "overview-v2_1d_*.csv" "data ยอดขาย plaform/Shopee Live"
```

สคริปต์มองทั้ง `~/Downloads`, `downloads_archive/` (mover ย้ายไฟล์ออกจาก Downloads
ภายในไม่กี่วินาที) และโฟลเดอร์ปลายทาง แล้วหยิบไฟล์ใหม่สุด
`status` ที่ควรได้คือ `COPIED` หรือ `ALREADY_THERE`
ถ้าได้ `NOT_FOUND` หรือ `TOO_OLD` = รอบนี้โหลดไม่สำเร็จ **ให้หยุดและรายงาน
ห้ามเอาไฟล์ของเมื่อวานไปใช้แทน** (สคริปต์กันไว้ด้วยเกณฑ์อายุ 30 นาที)

ชื่อไฟล์จะเป็น `overview-v2_1d_<YYYY-MM-DD>_*.csv` — ตรวจว่าวันที่ในชื่อไฟล์คือเมื่อวานจริง

## ขั้นที่ 2 — ดูก่อนว่าจะเปลี่ยนอะไร

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/shopee_live_daily.py" "data ยอดขาย plaform/Shopee Live/" --dry-run
```

ดูที่ `added` ควรมีวันเมื่อวาน · `skipped` ที่ขึ้นว่า "ไฟล์เก่ากว่า" เป็นเรื่องปกติ
(ยอด "ยืนยันแล้ว" โตขึ้นตามเวลา สคริปต์จะไม่ถอยค่าที่ matured แล้ว)
ถ้า `status` เป็น `ERROR` → **หยุดและรายงาน ห้ามแก้ตัวเลขเอง**

## ขั้นที่ 3 — รันจริง + commit

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/shopee_live_daily.py" "data ยอดขาย plaform/Shopee Live/"
```

exit `0` = อัปเดต + bump sw.js แล้ว · `10` = ไม่มีอะไรเปลี่ยน (ไม่ต้อง commit) · `2` = ไม่ผ่านด่าน

เฉพาะตอน exit 0:

```bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" && git add WIBWUB_Dashboard.html sw.js "data ยอดขาย plaform/Shopee Live/"
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" && git -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
    commit -m "auto-update: Shopee Live รายวัน $(date +%Y-%m-%d)"
```

ไม่ต้อง `git push` — launchd `com.wibwub.autopush` push ให้เองภายใน 2 นาที
ถ้า git ติด `index.lock`: รอ 20 วินาทีแล้วลองใหม่ สูงสุด 3 ครั้ง **ห้ามลบ lock ของคนอื่น**

---

## RULES

- ตัวเลขทุกตัวให้สคริปต์คำนวณ ห้ามคิดเอง ห้ามกรอกค่าสมมุติ
- ห้ามใช้ export แบบรายไลฟ์ (`sc_live_stream_list_export*`) — ไม่มีคอลัมน์ผู้ติดตาม
  และ `overview-v2` เป็นยอดรวมรายวันอยู่แล้ว ถ้าเอามาบวกกันเองจะเบิ้ล
- `grep -oP`, `sed -i "s/.../"`, `find -newermt` เป็น GNU-only **พังบน macOS** ห้ามใช้
- ถ้าต้องแก้วิธีคำนวณหรือชื่อคอลัมน์ ให้แก้ `scripts/shopee_live_daily.py` ที่เดียว

## สรุปท้ายรอบ (สั้น ๆ ภาษาไทย)

วันที่เพิ่มเข้าไป + ยอดขาย/ออเดอร์/ผู้ชม/ผู้ติดตามใหม่ของวันนั้น,
จำนวนวันทั้งหมดและวันที่มีไลฟ์, รายการที่ถูกข้าม, commit id หรือ "ไม่มีข้อมูลใหม่", error ถ้ามี

---

## 🚨 ทำงานไม่ได้ = ต้องรายงานว่าล้มเหลว ห้ามขึ้นว่าสำเร็จ

**กรณีที่ถือว่าล้มเหลว**

1. **เข้าโฟลเดอร์ All ไม่ได้** (ขั้น 0 ไม่เจอพาธ)
2. **เปิดเว็บไม่ได้** — `navigate`/`browser_batch` คืนข้อความใดข้อความหนึ่งนี้
   - `The approval prompt for this browser action went unanswered for 5 minutes` (กล่องขออนุญาตไม่มีคนกด)
   - `Navigation to this domain is not allowed` (สิทธิ์โดเมนถูกปฏิเสธ)
   - `Tab ... is not in Claude's tab group` / เชื่อมต่อส่วนขยายไม่ได้
3. **สคริปต์ที่พรอมป์ระบุหายหรือพัง**

**สิ่งที่ต้องทำเมื่อล้มเหลว**

1. **ลองครั้งเดียวพอ ห้ามวนลองซ้ำ** — เคยเสียเวลา 5 นาทีต่อหนึ่งเว็บโดยไม่ได้อะไร
   (22 ต.ค. 69 งาน HR ลองทั้ง `browser_batch` และ `javascript_tool` ตรงไปที่แท็บที่ล็อกอินค้างอยู่
   ก็โดนกล่องเดียวกันทั้งคู่ — แท็บที่เปิดค้างไว้ช่วยไม่ได้)
2. ปิดแท็บที่เปิดไว้ด้วย `tabs_close_mcp`
3. จบงานโดยขึ้นต้นบรรทัดแรกด้วย
   `❌ ล้มเหลว — <สาเหตุสั้น ๆ> ไม่ได้ข้อมูลใหม่รอบนี้`
   แล้วบอกด้วยว่าข้อมูลล่าสุดในไฟล์อยู่ถึงวันไหน

**ห้ามทำเด็ดขาด**

- ❌ ห้ามหันไปใช้ไฟล์เก่าแล้วรายงานว่า "สำเร็จ" — ถ้าดึงของใหม่ไม่ได้ ถือว่าล้มเหลว
- ❌ ห้ามเขียน ✅ หรือคำว่า "เสร็จ/สำเร็จ/OK" เมื่อขั้นใดขั้นหนึ่งข้างบนไม่ผ่าน
- ❌ ห้ามเดาตัวเลข หรือคัดลอกตัวเลขจากรอบก่อนมาใส่

> ใช้ไฟล์เดิมได้เฉพาะกรณีที่พรอมป์ระบุไว้ชัดเจนว่าเป็นทางสำรองที่ยอมรับได้
> (เช่น ads-daily ใช้ `work/*.json` ที่ครอบช่วง `from→to` พอดี) และต้อง**รายงานตรง ๆ
> ว่ารอบนี้ใช้ของเดิม ไม่ได้ดึงใหม่**
---

## 🚫 กฎคำสั่ง shell (ทุกงาน — รวมคำสั่งที่คิดขึ้นเองระหว่างรัน)

งานตั้งเวลา **ไม่มีคนนั่งกดอนุญาต** ถ้าคำสั่งไม่แมตช์กฎที่อนุญาตไว้แล้ว
(`Bash(python3 *)` / `Bash(git *)` / `Bash(ls *)` ฯลฯ) งานจะค้างทั้งรอบ
สังเกตง่าย ๆ: ถ้ากล่องขออนุญาตมีแค่ปุ่ม **"Allow once"** โดยไม่มี "Always allow"
แปลว่าคำสั่งนั้นสร้างกฎถาวรไม่ได้ จะถามใหม่ทุกครั้งตลอดไป

**เขียนคำสั่งให้เรียบง่ายที่สุด — 1 คำสั่ง = 1 โปรแกรม + พาธเต็ม**

| ❌ ห้าม | เหตุผลที่โดนถาม | ✅ ใช้แบบนี้ |
|---|---|---|
| `git -C "<path>" ...` | **ห้ามใช้** — กฎ deny จับจากคำขึ้นต้น `git push` จึงกัน `git -C <path> push` ไม่ได้ = เปิดช่องให้ push หลุด | `cd "<path เต็ม>" && git status` |
| `cd "<path>" && python3 x.py` | ขึ้นต้นด้วย cd ไม่แมตช์ `Bash(python3 *)` | `python3 "<path เต็ม>/x.py"` |
| `BASE="..."` แล้วใช้ `$BASE` | ตัวแปร = simple_expansion สร้างกฎถาวรไม่ได้ | เขียนพาธเต็มตรง ๆ ทุกครั้ง |
| `for d in ...; do ... done` / `if [ ... ]` | ลูป/เงื่อนไขใน bash ก็เข้าข่ายเดียวกัน | ย้ายตรรกะไปไว้ในสคริปต์ python แล้วเรียกไฟล์นั้น |
| `cmd1; cmd2; cmd3` ต่อกันยาว ๆ | คำสั่งผสมแมตช์กฎไม่ได้ | แยกเป็นคนละคำสั่ง |

**ถ้าต้องมีตรรกะ (วนลูป / เช็คเงื่อนไข / ประกอบพาธ): เขียนเป็นสคริปต์ python
ไว้ใน `scripts/` แล้วเรียกด้วยพาธเต็ม** เช่น `python3 "<path เต็ม>/scripts/ads/check_downloads.py" tiktok`
วิธีนี้ทั้งอ่านง่ายกว่า ทดสอบแยกได้ และไม่ติดกำแพงสิทธิ์
