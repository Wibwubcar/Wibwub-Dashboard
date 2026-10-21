---
name: wibwub-shopee-live-daily
description: ทุกวัน 08:37/19:37 — ดึง Shopee Live รายวัน → merge SH_LIVE_DAILY ใน WIBWUB_Dashboard.html
---

## WIBWUB — Shopee Live รายวัน

BASE = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`

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
D="$BASE/data ยอดขาย plaform/Shopee Live"
F=$(ls -t /Users/thanasablilutanon/Downloads/overview-v2_1d_*.csv \
          "$BASE/downloads_archive"/overview-v2_1d_*.csv 2>/dev/null | head -1)
[ -z "$F" ] && { echo "ไม่พบไฟล์ CSV ที่โหลดมา"; exit 1; }
cp "$F" "$D/" && echo "เก็บแล้ว: $(basename "$F")"
```

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
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" add WIBWUB_Dashboard.html sw.js "data ยอดขาย plaform/Shopee Live/"
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
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
