---
name: wibwub-content-sheet
description: ทุกวัน 09:45/20:45 — เก็บตัวเลขคลิป TikTok (5 วินาทีแรก / วิว / ถูกใจ / คอมเมนต์ / แชร์ / บันทึก) ลงแท็บ CONTENT ของชีตคอนเทนต์ · เติมเฉพาะช่องว่าง ห้ามทับของเดิม
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


## WIBWUB — เติมตัวเลขคลิปลงชีต CONTENT

เป้าหมาย: ให้แท็บ CONTENT มีตัวเลขครบถึงคลิปล่าสุด โดย**ไม่แตะอะไรที่คนกรอกไว้แล้ว**

ชีต `1OWZGQD1wHvIlLAAg_7rJ0CtL-X9vEx4py-cRp_e3NvQ` แท็บ `CONTENT`

### 🚫 กฎเหล็ก — ผิดข้อไหนให้หยุดทันที

- **ห้ามแก้ค่าที่มีอยู่แล้ว** สคริปต์ข้ามช่องที่ไม่ว่างให้อยู่แล้ว ห้ามเขียนทับด้วยมือ
- **ห้ามแตะคอลัมน์ C, E, F, G, J** (Content Pillars / Target / Benefit / Caption / Feedback)
  เป็นงานจัดหมวดและเขียนเชิงกลยุทธ์ของทีม ไม่ใช่ข้อมูลที่ดึงมาได้
- **ห้ามแตะคอลัมน์ L, M, U** เป็นสูตร คำนวณเองจาก K/N/O/P
- **ห้ามลบแถว ห้ามเรียงใหม่ ห้ามแก้แท็บอื่น**

---

## ขั้นที่ 1 — ดูว่าต้องเติมอะไร

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/content/content_sheet_update.py" plan
```

ได้ `need_fill` (แถวที่มีลิงก์แต่ตัวเลขยังว่าง) และ `known_video_ids` (คลิปที่มีแถวแล้ว)

## ขั้นที่ 2 — หาคลิปที่ยังไม่มีในชีต

1. Chrome: `list_connected_browsers` → `select_browser` ตัว macOS
   (deviceId `b75a6bb0-5b78-4e44-92a8-75224f1ce4ee`) → `tabs_context_mcp(createIfEmpty=true)`
2. navigate `https://www.tiktok.com/tiktokstudio/content` รอ 9 วินาที
3. ดึง id ของคลิปในหน้า:
   ```js
   [...new Set([...document.querySelectorAll('a[href*="/video/"]')]
     .map(a=>(a.getAttribute('href')||'').split('/video/')[1]).filter(Boolean))]
   ```
4. เอา id ที่**ไม่อยู่ใน** `known_video_ids` มารวมกับ `need_fill` เป็นรายการที่ต้องเก็บ

> หน้ารายการโหลดมาแค่หน้าแรก (~7 รายการ) เลื่อนแล้วไม่โหลดเพิ่ม
> ไม่เป็นไร งานนี้รันวันละ 2 รอบ คลิปใหม่จะไม่มีทางหลุดเกินหน้าแรก

## ขั้นที่ 3 — เก็บตัวเลขทีละคลิป

ทำซ้ำสำหรับแต่ละ `<id>`:

1. navigate `https://www.tiktok.com/tiktokstudio/analytics/<id>?qa_enter_from=analytics`
2. รอ 9 วินาที
3. วางเนื้อหาไฟล์ `scripts/content/tt_content_collect.js` ใน `javascript_tool` **คัดลอกตรงตัว**
4. เก็บ JSON ที่คืนมา

> ⚠️ **ค่า "5 วินาทีแรก" ต้องให้สคริปต์ตั้ง `video.currentTime = 5` เท่านั้น**
> อย่าพยายามลาก slider ด้วยพิกัด อย่าอ่าน pixel จากกราฟมาคำนวณเอง
> (เคยลองแล้ว 22 ต.ค. 69 คำนวณได้ 23.9% ขณะที่ของจริง 22% — เพี้ยน 2 จุด)

> ⚠️ **ยอดวิวเกิน ~100K หน้าเว็บย่อเป็น "232K"** ไม่มีเลขเต็มที่ไหนเลย
> สคริปต์แปลงให้เป็น 232000 ตามที่ตกลงกับผู้ใช้ 22 ต.ค. 69 และตั้ง `views_approx: true`
> ให้รายงานด้วยว่าแถวไหนเป็นเลขปัด

รวม JSON ทุกคลิปเป็น list แล้วบันทึกด้วย heredoc เป็น
`scripts/content/work/clips.json`

## ขั้นที่ 4 — เขียนลงชีต

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/content/content_sheet_update.py" write --in "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/content/work/clips.json" --dry-run
```

ดูผล `DRY_RUN` ก่อนว่า `added` / `filled` สมเหตุสมผล แล้วค่อยรันซ้ำ**โดยตัด `--dry-run` ออก**

exit 0 = เขียนแล้ว · 10 = ไม่มีอะไรต้องเขียน (ปกติ ไม่ใช่ error) · 2 = ผิดพลาด ไม่ได้เขียนอะไรเลย

## ขั้นที่ 5 — ปิดแท็บ

`tabs_close_mcp` ทุกแท็บที่เปิด

## ถ้าเจอกล่องขออนุญาตเบราว์เซอร์ (เกิดบ่อยมากตั้งแต่ย้ายมารันบนแอป)

ถ้า `navigate` / `browser_batch` คืนข้อความทำนองว่า
*"The approval prompt for this browser action went unanswered for 5 minutes
and this run looks unattended"* แปลว่าไม่มีคนกดอนุญาต

**ลองครั้งเดียวพอ แล้วจบงานทันที ห้ามวนลองซ้ำ** — เคยเสียเวลาไป 10 นาที/รอบ
โดยไม่ได้อะไรเลย (งาน HR 22 ต.ค. 69 ลองทั้ง browser_batch และ javascript_tool
ตรงไปที่แท็บที่ล็อกอินค้างอยู่ ก็โดนกล่องเดียวกันทั้งคู่)

รายงานว่า `⚠️ ติดกล่องขออนุญาตเบราว์เซอร์ ไม่ได้เก็บข้อมูลรอบนี้`
แล้วจบงาน **ไม่ถือเป็น error** — ชีตไม่เสียหาย รอบหน้าเก็บต่อได้เพราะเติมเฉพาะช่องว่างอยู่แล้ว

## ถ้าเจอหน้า login TikTok

**ห้ามกรอกรหัสผ่าน ห้ามกดเข้าสู่ระบบ** ให้เปิดหน้า login ค้างไว้ แล้วรายงานว่า
`⚠️ TikTok Studio login หลุด — เปิดหน้า login ค้างไว้ให้แล้ว` จบงาน ไม่ถือเป็น error

## สรุปท้ายรอบ (สั้น ๆ ภาษาไทย)

เติมไปกี่ช่อง / เพิ่มแถวใหม่กี่แถว (วันที่อะไรบ้าง) / คลิปล่าสุดในชีตคือวันที่เท่าไร /
แถวไหนที่ยอดวิวเป็นเลขปัดจากแพลตฟอร์ม

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

**เขียนคำสั่งให้เรียบง่ายที่สุด — 1 คำสั่ง = 1 โปรแกรม + พาธเต็ม**

| ❌ ห้าม | เหตุผลที่โดนถาม | ✅ ใช้แบบนี้ |
|---|---|---|
| `cd "<path>" && git status` | cd + git = ตัวตรวจตีธง | `cd "<path เต็ม>" && git status` |
| `cd "<path>" && python3 x.py` | ขึ้นต้นด้วย cd ไม่แมตช์ `Bash(python3 *)` | `python3 "<path เต็ม>/x.py"` |
| `BASE="..."` แล้วใช้ `$BASE` | ตัวแปร = simple_expansion | เขียนพาธเต็มตรง ๆ ทุกครั้ง |
| `for ...; do ... done` / `if [ ... ]` | ลูป/เงื่อนไขเข้าข่ายเดียวกัน | ย้ายตรรกะไปไว้ในสคริปต์ python |
| `cmd1; cmd2; cmd3` | คำสั่งผสมแมตช์กฎไม่ได้ | แยกเป็นคนละคำสั่ง |
