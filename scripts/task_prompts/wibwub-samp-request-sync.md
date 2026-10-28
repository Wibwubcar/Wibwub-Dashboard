---
name: wibwub-samp-request-sync
description: ทุกวัน 09:35/20:35 — ดึงชีต "ขอสินค้า" มาอัปเดตแท็บ คำขอสินค้า ใน WIBWUB_Affiliate_Dashboard.html
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


## WIBWUB Affiliate — sync แท็บ "คำขอสินค้า" จากชีตสด

BASE = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`

พนักงานเพิ่มแถวในชีตตลอดวัน งานนี้ต้องรันทุกรอบ **ห้ามข้ามเพราะคิดว่า "ไม่น่ามีอะไรใหม่"**

> **ห้ามเขียนสคริปต์อ่าน/คำนวณเอง** ตัวคำนวณจริงคือ `scripts/affiliate/samp_update.py`
> มันจัดการครบทั้ง `SAMPLE_MONTHS` (req/appr/shipped/posted/clips/waiting), `SAMPLE_LAST7D`,
> `SAMPLE_PRODUCTS`, `SAMPLE_PRODUCTS_LAST7D`, `SAMPLE_POSTWAIT`, `SAMPLE_DATA_ASOF`
> และ `node --check` ก่อนเขียนไฟล์
> เวอร์ชันเก่าของพรอมป์นี้เคยบรรยายคอลัมน์เองแล้ว**ผิด** (ใส่คอลัมน์ `NO.` ที่ไม่มีจริง
> ทำให้ index เลื่อนทั้งแถว → อ่านวันที่ไม่ได้ → ล้างข้อมูลทั้งเดือนเป็น 0) จึงถอดออกทั้งหมด

---

## ขั้นที่ 1 — ดึงชีตเป็น CSV ลงดิสก์

ชีต **"Top 30 Affiliate"** · fileId `1EYzinmagF1iTXgKe7PNU5SVD9WcTvHhuO054aWKITxg` · แท็บ **"ขอสินค้า"** · gid `1644804644`

> 🚨 **ต้องใช้ `export?format=csv` เท่านั้น ห้ามใช้ `gviz/tq?tqx=out:csv`**
> `gviz` เคารพ filter view ของชีต — ทดสอบเมื่อ 20 ต.ค. ได้กลับมาแค่ **304 แถว (21 ก.ย.–19 ต.ค.)**
> ขณะที่ `export` ได้ครบ **2,647 แถว (21 ต.ค. 2025–19 ต.ค. 2026)** ถ้าใช้ gviz ข้อมูลเดือนเก่าจะหายหมด
> และ **ห้ามดึงผ่าน `get_values` แล้วเขียนไฟล์เอง** — 2,600+ แถวเปลืองมากและเสี่ยงตกหล่น

1. Chrome: `list_connected_browsers` → `select_browser` deviceId `b75a6bb0-5b78-4e44-92a8-75224f1ce4ee` → `tabs_context_mcp(createIfEmpty=true)`
2. `navigate` ไป URL นี้ตรง ๆ (Chrome จะโหลดไฟล์เอง — **อย่าใช้ `fetch` จะติด CORS**):
   `https://docs.google.com/spreadsheets/d/1EYzinmagF1iTXgKe7PNU5SVD9WcTvHhuO054aWKITxg/export?format=csv&gid=1644804644`
   รอ 8 วินาที · ถ้าขึ้นหน้า login: **หยุดและรายงาน ห้ามกรอกรหัสผ่าน**
3. ปิดแท็บที่เปิดด้วย `tabs_close_mcp`
4. หาไฟล์แล้วคัดลอกไปที่ work (ไฟล์ชื่อ `Top 30 Affiliate  - ขอสินค้า.csv`
   และ launchd `com.wibwub.download-mover` อาจย้ายออกจาก Downloads แล้ว):

```bash
mkdir -p "$BASE/scripts/affiliate/work"
F=$(ls -t /Users/thanasablilutanon/Downloads/*ขอสินค้า*.csv \
          "$BASE/downloads_archive"/*ขอสินค้า*.csv 2>/dev/null | head -1)
[ -z "$F" ] && { echo "ไม่พบไฟล์ CSV ที่โหลดมา"; exit 1; }
cp "$F" "$BASE/scripts/affiliate/work/samp.csv"
python3 -c "
import csv,sys
r=list(csv.reader(open('$BASE/scripts/affiliate/work/samp.csv',encoding='utf-8-sig')))
print('แถวดิบ',len(r))
sys.exit(0 if len(r)>=2000 else 1)"
```

ถ้าหาไฟล์ไม่เจอ หรือแถวดิบน้อยกว่า 2,000: **หยุดและรายงาน ห้ามเดาข้อมูล**
(สคริปต์มีด่านของตัวเองอีกชั้น — ถ้าแถวที่มีวันที่ < 500 มันจะ die เอง)

## ขั้นที่ 2 — ดูก่อนว่าจะเปลี่ยนอะไร

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/affiliate/samp_update.py" scripts/affiliate/work/samp.csv --dry
```

ตรวจด้วยตา: `rows` ควรใกล้เคียงหรือมากกว่ารอบก่อน · `latest_row` ควรเป็นวันนี้หรือเมื่อวาน ·
`this_month.req` ไม่ควรลดลง · ถ้า `status` เป็น `ERROR` → **หยุดและรายงาน**

## ขั้นที่ 3 — รันจริง

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/affiliate/samp_update.py" scripts/affiliate/work/samp.csv
```

exit `0` = อัปเดต + commit แล้ว · `10` = ไม่มีอะไรเปลี่ยน · อื่น ๆ = error

สคริปต์ bump `sw.js` และ commit ให้เอง **ไม่ต้อง `git push`** (launchd autopush ทำให้ภายใน 2 นาที)

ถ้าผลลัพธ์มี `commit: "SKIPPED: ... มีงานค้าง ..."` แปลว่ามีคนแก้ `WIBWUB_Affiliate_Dashboard.html`
ค้างไว้ก่อน สคริปต์เขียนข้อมูลใหม่ให้แล้วแต่ไม่ commit เพื่อไม่ให้กวาดงานคนอื่นเข้าไปด้วย
→ **ให้รายงาน ไม่ต้อง commit เอง**

---

## RULES

- ตัวเลขทุกตัวให้สคริปต์คำนวณ ห้ามคิดเอง ห้ามกรอกค่าสมมุติ
- **ห้ามลบ `.git/index.lock` หรือ `.git/HEAD.lock`** มีงานอื่นรันพร้อมกันได้ ถ้าติดให้รอแล้วลองใหม่
- ถ้าต้องแก้วิธีคำนวณ ให้แก้ `scripts/affiliate/samp_update.py` ที่เดียว อย่าแก้ที่ไฟล์นี้
- คอลัมน์สินค้าที่ใช้คือ **"สินค้าที่ Creator ขอ"** เท่านั้น ห้ามใช้ "สินค้าที่ให้"

## ขั้นที่ 4 — ตรวจสุขภาพงานตั้งเวลาทั้งระบบ (ทำทุกรอบ ไม่ว่าขั้นก่อนหน้าจะผ่านหรือไม่)

```bash
python3 "<BASE>/scripts/ops/task_health.py"
```

- **exit 3** = มีงานค้าง → เอาบรรทัด `⛔ …` ที่มันพิมพ์ออกมา **ขึ้นเป็นบรรทัดแรกสุดของรายงานรอบนี้**
  ก่อนหัวข้ออื่นทั้งหมด แล้วทำงานของตัวเองต่อตามปกติ
- **exit 0** = ปกติ ไม่ต้องเขียนอะไรเพิ่มในรายงาน (บรรทัด ℹ️ ไม่ใช่ปัญหา ไม่ต้องยก)
- **exit 2** = ตัวตรวจเองมีปัญหา ให้รายงาน 1 บรรทัดว่าตรวจไม่ได้เพราะอะไร

**ห้ามแก้อะไรเองตามผลที่ได้ ห้ามหยุดเซสชันของงานอื่น ห้าม enable/disable งาน** —
หน้าที่ของขั้นนี้คือ *บอก* เท่านั้น การลงมือเป็นของผู้ใช้

> ทำไมต้องมี: 28 ต.ค. 69 งาน `wibwub-ads-daily` ค้างสถานะ running ตั้งแต่ 26 ต.ค. 20:50
> ตัวจัดตารางจึงไม่ยิงรอบใหม่เลย หน้า "การตลาด vs ยอดขาย" หยุดอัปเดต **37 ชั่วโมง**
> โดยไม่มีใครรู้ กว่าจะจับได้ก็ตอนไล่ดู git log ด้วยมือ · งานนี้เป็นรอบท้ายสุดของเช้า
> จึงเหมาะเป็นจุดตรวจ (รายละเอียดเกณฑ์อยู่ใน `scripts/ops/task_expect.json` แก้ที่นั่นที่เดียว)

## สรุปท้ายรอบ (สั้น ๆ ภาษาไทย)

จำนวนแถวที่อ่านได้, วันที่ล่าสุดในชีต, คำขอ/อนุมัติ/โพสต์แล้ว ของเดือนนี้,
รอบ 7 วันล่าสุด, จำนวนที่รอโพสต์, สินค้าที่ถูกขอมากสุด 5 อันดับ,
commit id หรือ "ไม่มีข้อมูลใหม่" หรือเหตุผลที่ไม่ได้ commit, และ error ถ้ามี

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
| `git ...` ทุกรูปแบบ | `git -C` เปิดช่องให้ push หลุด · `cd ... && git` ขึ้นต้นด้วย cd จึงไม่แมตช์กฎ `Bash(git add:*)` → งานค้างรออนุญาต | `python3 "<BASE>/scripts/gitw.py" add/commit/status/log` |
| `cd "<path>" && python3 x.py` | ขึ้นต้นด้วย cd ไม่แมตช์ `Bash(python3 *)` | `python3 "<path เต็ม>/x.py"` |
| `BASE="..."` แล้วใช้ `$BASE` | ตัวแปร = simple_expansion สร้างกฎถาวรไม่ได้ | เขียนพาธเต็มตรง ๆ ทุกครั้ง |
| `for d in ...; do ... done` / `if [ ... ]` | ลูป/เงื่อนไขใน bash ก็เข้าข่ายเดียวกัน | ย้ายตรรกะไปไว้ในสคริปต์ python แล้วเรียกไฟล์นั้น |
| `cmd1; cmd2; cmd3` ต่อกันยาว ๆ | คำสั่งผสมแมตช์กฎไม่ได้ | แยกเป็นคนละคำสั่ง |

**ถ้าต้องมีตรรกะ (วนลูป / เช็คเงื่อนไข / ประกอบพาธ): เขียนเป็นสคริปต์ python
ไว้ใน `scripts/` แล้วเรียกด้วยพาธเต็ม** เช่น `python3 "<path เต็ม>/scripts/ads/check_downloads.py" tiktok`
วิธีนี้ทั้งอ่านง่ายกว่า ทดสอบแยกได้ และไม่ติดกำแพงสิทธิ์
