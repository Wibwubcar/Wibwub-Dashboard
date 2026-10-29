---
name: wibwub-sales-update
description: ทุกวัน 09:25/20:25 (งานฝั่ง code ตั้งแต่ 29 ต.ค. 69) — อ่านชีตยอดขาย Shopee/TikTok/Lazada ผ่าน service account → อัปเดต SALES arrays + MTD_COVERAGE ใน Dashboard + Mobile
---

## ขั้น 0 — ไม่มีขั้นหาโฟลเดอร์ ห้ามใช้ shell ค้นหา

`sales_update.py` หาโฟลเดอร์ All เองจากตำแหน่งไฟล์ (marker `sw.js` + `.git`)
จึงไม่ต้องหาพาธ ไม่ต้องตั้งตัวแปร **คำสั่ง shell แรกของรอบต้องขึ้นต้นด้วย `python3` เสมอ**

**ห้ามรันลูป `for` / `[ -d ... ]` / ตั้งตัวแปร `BASE=` / `cd` เพื่อหาพาธ** — คำสั่งผสมแบบนั้น
สร้างกฎอนุญาตถาวรไม่ได้ จึงเด้งกล่องขออนุญาตที่ไม่มีคนกดแล้วค้างทั้งรอบ

ถ้าคำสั่ง `python3` ตอบว่าไม่พบไฟล์ ให้ลองพาธสำรอง
`~/mnt/All/scripts/sales_update.py` **หนึ่งครั้ง** ถ้ายังไม่ได้ → หยุดและรายงานว่าล้มเหลว
ห้ามเดาพาธเอง ห้ามใช้พาธ `/sessions/<ชื่อ>/mnt/...` ที่ฝังไว้ในเอกสารเก่า

> **เกิดจริง 28 ต.ค. 69 20:31 (งาน HR) และ 26/28 ต.ค. (งาน ads-daily):** ขั้น 0 แบบลูป
> ทำให้รอบนั้นค้างที่คำสั่งแรกโดยไม่มีใครรู้ · งานนี้ย้ายมาฝั่ง code เมื่อ 29 ต.ค. 69
> จึงตัดลูปออกทั้งหมด ไม่ต้องหวังให้เอเจนต์ "ข้าม" เอง

---


## WIBWUB — อัปเดตยอดขายรายเดือนจาก Google Sheets

โฟลเดอร์ All (ใช้เขียนพาธเต็มในคำสั่ง **ห้ามทำเป็นตัวแปร shell**):
`/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`

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
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" add WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
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
