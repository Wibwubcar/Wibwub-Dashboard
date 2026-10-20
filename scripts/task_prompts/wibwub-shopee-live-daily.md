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
cd "$BASE" && python3 scripts/shopee_live_daily.py "data ยอดขาย plaform/Shopee Live/" --dry-run
```

ดูที่ `added` ควรมีวันเมื่อวาน · `skipped` ที่ขึ้นว่า "ไฟล์เก่ากว่า" เป็นเรื่องปกติ
(ยอด "ยืนยันแล้ว" โตขึ้นตามเวลา สคริปต์จะไม่ถอยค่าที่ matured แล้ว)
ถ้า `status` เป็น `ERROR` → **หยุดและรายงาน ห้ามแก้ตัวเลขเอง**

## ขั้นที่ 3 — รันจริง + commit

```bash
cd "$BASE" && python3 scripts/shopee_live_daily.py "data ยอดขาย plaform/Shopee Live/"
```

exit `0` = อัปเดต + bump sw.js แล้ว · `10` = ไม่มีอะไรเปลี่ยน (ไม่ต้อง commit) · `2` = ไม่ผ่านด่าน

เฉพาะตอน exit 0:

```bash
git -C "$BASE" add WIBWUB_Dashboard.html sw.js "data ยอดขาย plaform/Shopee Live/"
git -C "$BASE" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
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

**ห้ามใส่ `cd` ไว้ในคำสั่งเดียวกับ `git` เด็ดขาด** ไม่ว่าจะเชื่อมด้วย `&&` `;` หรือขึ้นบรรทัดใหม่
ตัวตรวจความปลอดภัยจะหยุดงานแล้วรอคนกดอนุญาต ("changes directory before running git,
which can execute untrusted hooks") ซึ่งงานตั้งเวลาไม่มีคนนั่งกด = ค้างทั้งรอบ

| ❌ ห้าม | ✅ ใช้แบบนี้ |
|---|---|
| `cd "$BASE" && git status` | `git -C "$BASE" status` |
| `cd "$BASE"` ขึ้นบรรทัดใหม่แล้วตามด้วย `git ...` | `git -C "$BASE" ...` |
| `cd "$BASE" && python3 x.py; git status` | แยกเป็น 2 คำสั่ง · ใช้ `python3 "$BASE/x.py"` และ `git -C "$BASE" status` |

เรียกสคริปต์ด้วย path เต็มเสมอ (`python3 "$BASE/scripts/..."`) จะได้ไม่ต้อง `cd`
ถ้าจำเป็นต้อง `cd` จริง ๆ (เช่นสคริปต์อ่าน path สัมพัทธ์) **ห้ามมี `git` อยู่ในคำสั่งนั้น**
