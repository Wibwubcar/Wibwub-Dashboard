---
name: wibwub-fastmoss-competitor
description: ทุกวัน 08:05 — ดึงข้อมูล FastMoss ของ WIBWUB + munwow (cumulative + 28-day trend + top products) → อัปเดต WIBWUB_FastMoss_Competitor_Dashboard.html → commit + push_now.command
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


<!-- LOCAL-OVERRIDE v1 -->
> **อ่านก่อน — ข้อนี้ทับคำสั่งที่ขัดกันในไฟล์นี้ทั้งหมด**
> ไฟล์นี้เขียนไว้ตอนรันบน Cowork cloud sandbox ตอนนี้ย้ายมารันบนเครื่อง Mac แล้ว
> - BASE / ALL_MNT = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All` · Downloads = `/Users/thanasablilutanon/Downloads` · OUTPUTS = `/Users/thanasablilutanon/Library/Caches/wibwub-outputs`
> - `git push` **ไม่ต้องทำ** และจะ**ไม่**เจอ error 403 แบบ sandbox — launchd `com.wibwub.autopush` push ให้เองทุก 2 นาที ข้ามทุกหัวข้อที่พูดถึง 403 / การสร้างหรือแก้ `push_now.command`
> - ที่ไหนเขียนว่า `mcp__workspace__bash` ให้ใช้ Bash tool ปกติแทน
> - อ่านไฟล์ในเครื่องใช้ Read/Bash ได้ตรง ๆ ไม่ต้องผ่าน connector
> - ถ้าขั้นไหนอ้าง path หรือเครื่องมือที่ไม่มีจริง: **หยุดและรายงาน ห้ามเดาทางเอง**

## WIBWUB FastMoss Competitor Dashboard — Daily Update

Goal: scrape today's FastMoss shop-analytics numbers for WIBWUB and its competitor "munwow", then merge them into the WIBWUB_FastMoss_Competitor_Dashboard.html comparison dashboard so it always shows a fresh snapshot plus a growing history trend line. This is a fully self-contained task — you have no memory of any prior conversation, so follow every step below.

### Step 0 — Resolve paths

The Google Drive workspace folder is mounted into your bash sandbox under a session-specific path. Resolve it dynamically (do NOT hardcode a `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All` path from any old documentation — the `<name>` changes every session):

```bash
BASE="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
echo "BASE=$BASE"
ls "$BASE/fastmoss_history.json" "$BASE/fastmoss_update.py" "$BASE/WIBWUB_FastMoss_Competitor_Dashboard.html"
```

If any of those three files are missing, stop and report — something is wrong with the setup, don't try to recreate them from scratch.

### Step 1 — Open FastMoss via Claude in Chrome

⚠️ Chrome navigation rule: never call `navigate` standalone — it can hang and stall the whole task. Always wrap it in `browser_batch`:
```
browser_batch([
  navigate(url="...", tabId=TAB_ID),
  computer(action="wait", duration=4, tabId=TAB_ID),
  computer(action="screenshot", tabId=TAB_ID)
])
```

1. Always pin the browser explicitly — if multiple browsers are connected, picking the wrong one silently runs on the wrong machine: call `list_connected_browsers` first, then `select_browser` with the device whose `osPlatform` is macOS and `isLocal:true`. Then `tabs_context_mcp(createIfEmpty=true)`.
2. Navigate to WIBWUB's page: `https://www.fastmoss.com/th/shop-marketing/detail/7494549095358892612`
3. If the page asks you to log in, STOP and report "ต้องการ login FastMoss" — do not attempt to log in yourself.

### Step 2 — Read WIBWUB's numbers (⚠️ read this carefully — easy to get wrong)

FastMoss shop pages show TWO different classes of numbers that look similar but are NOT interchangeable:

- **(a) Header/profile stat cards near the top** = ALL-TIME CUMULATIVE totals (orders ever, sales ever, total lives/videos/creators ever tagged, country rank, category rank, rating, quality score, response rate, shipping rate, products active/total). Use `get_page_text` for these; they're usually present without scrolling.
- **(b) "แนวโน้มข้อมูล" (Data Trends) section**, further down the page, with its own 7/28/90/180-day tab selector and an explicit date-range label like "2026-07-30 → 2026-08-26". Make sure the "28 วัน" / 28-day tab is selected (it usually is by default), then scroll it into view and take a screenshot — `get_page_text` sometimes misses these numbers until they're actually scrolled into the viewport, so confirm the on-screen pixels via screenshot before trusting the number. Read: orders, sales, creators, lives, videos, products sold, and the exact date range shown.
- Do NOT substitute (a) for (b) or vice versa. A past run of this workflow mistakenly reported WIBWUB's cumulative header stats as if they were the 28-day trend — always double check you're reading the Data Trends section for the trend28d numbers, not the header.

Also find the Top 5 best-selling products for the current 28-day window (name, orders, sales for each) — usually in a "สินค้าขายดี" / top products section on the same page.

Record: category %, price range, and "listed since" date too if visible (used for the shop meta card, rarely changes).

### Step 3 — Repeat Step 1-2 for munwow

URL: `https://www.fastmoss.com/th/shop-marketing/detail/7494636213512539066`

### Step 4 — Write the snapshot JSON and run the updater

Write a JSON file (e.g. `/tmp/fastmoss_snapshot.json`) shaped exactly like this (use today's actual date and the real numbers you just read):

```json
{
  "date": "YYYY-MM-DD",
  "shops": {
    "wibwub": {
      "cumulative": {"orders_total":.., "sales_total":.., "products_active":.., "products_total":.., "country_rank":.., "category_rank":.., "rating":.., "overall_good_pct":.., "quality_score":.., "response_rate_24h":.., "shipping_rate_48h":..},
      "trend28d": {"range":"YYYY-MM-DD → YYYY-MM-DD", "orders":.., "sales":.., "creators":.., "lives":.., "videos":.., "products_sold":..},
      "top_products": [{"name":.., "orders":.., "sales":..}, ...up to 5]
    },
    "munwow": { ... same shape ... }
  }
}
```

Then run:
```bash
cd "$BASE"
python3 fastmoss_update.py --snapshot /tmp/fastmoss_snapshot.json
```
This script merges the snapshot into `fastmoss_history.json` (overwriting today's entry if you re-run it — safe to retry), regenerates the dashboard's embedded data, and commits both files plus the dashboard HTML with author "WIBWUB Bot <marketingwibwub@gmail.com>". It will also attempt `git push`, which is expected to fail from the sandbox (HTTP 403 proxy) — that's normal, not an error.

If the script errors with "Unknown shop key", it means the FastMoss competitor set has changed — do not invent a fix, just report the error.

### Step 5 — Validate before trusting it

```bash
cd "$BASE"
python3 -c "
import re
html = open('WIBWUB_FastMoss_Competitor_Dashboard.html', encoding='utf-8').read()
m = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
open('/tmp/fm_check.js','w',encoding='utf-8').write(m.group(1))
"
node --check /tmp/fm_check.js && echo "JS_OK"
```
If this fails, the merge broke something — do not leave the commit in place silently; report the failure clearly.

### Step 6 — Report

Summarize in Thai: today's date, WIBWUB vs munwow's 28-day orders/sales, and remind that `push_now.command` still needs to be double-clicked on the user's Mac for the change to actually reach GitHub Pages (sandbox git push always fails — expected).

### Notes
- If FastMoss's page layout has visibly changed (missing "แนวโน้มข้อมูล" section, different card labels, etc.), stop and report rather than guessing at numbers.
- Never hand-edit WIBWUB_FastMoss_Competitor_Dashboard.html's data directly — always go through fastmoss_update.py so fastmoss_history.json (the source of truth) and the dashboard never drift apart.

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

---
---

# 🔁 งานนี้มี 2 ส่วน — เพิ่มส่วน A (HR) เมื่อ 24 ต.ค. 2569

ทุกอย่างข้างบนคือ **ส่วน B (FastMoss คู่แข่ง)** ทำให้ครบเหมือนเดิมทุกประการ ห้ามข้าม
**ทำส่วน A ก่อนเสมอ แล้วค่อยทำส่วน B ต่อ**

เหตุผล: ฝั่ง code เปิดเว็บในรอบตั้งเวลาไม่ได้ตั้งแต่เวอร์ชัน 2.1.308 (22 ต.ค. 69 20:32)

---

# งานนี้มี 2 ส่วนที่แยกขาดจากกัน

**ทำส่วน A ก่อนเสมอ แล้วทำส่วน B ต่อ**
**ถ้าส่วน A ล้ม ให้ทำส่วน B ต่อ และถ้าส่วน B ล้ม ก็ไม่กระทบส่วน A ที่ทำไปแล้ว**
**รายงานผลแยกกันสองหัวข้อเสมอ ห้ามรวบเป็นอันเดียว**

---

# ส่วน A — HR เข้า-ออกงาน (ทำทุกรอบ)

อ่านไฟล์นี้ด้วย Read tool แล้วทำตามทุกขั้นตอนในไฟล์:

`$BASE/scripts/task_prompts/hr_attendance.md`

ใช้สกิล **wibwub-hr-attendance** เป็นคู่มือหลัก อ่านสกิลก่อนเริ่มทุกครั้ง

### ข้อยกเว้นของรอบนี้
**ข้ามขั้น Google Sheet ไปก่อน** (ขั้น 6 และ 7 ในไฟล์พรอมป์ — `hr_update.py sheet`, `sheet-done`, `get_values`)
ทำแค่ถึงขั้น commit พอ แล้วรายงานว่า "ยังไม่ได้เขียน Google Sheet (ตั้งใจข้าม)"
เหตุผล: ขั้นนั้นต้องคัดตารางเวลาจากผล API ลงไฟล์ด้วยมือ ซึ่งถ้าพลาดจะเขียนทับค่าเดิมในชีตเงินเดือน
จะเปิดใช้เมื่อผู้ใช้สั่งเท่านั้น

### กติกาประจำรอบ
- ห้อง Discord: เข้างาน https://discord.com/channels/1331888082802315295/1331888545253818400 · ออกงาน https://discord.com/channels/1331888082802315295/1331888567592550441 · การลา https://discord.com/channels/1331888082802315295/1331942184739667979 · รายงานการผลิต https://discord.com/channels/1331888082802315295/1392059303669792889
- Chrome: `list_connected_browsers` → `select_browser` ตัวที่ `osPlatform` เป็น macOS และ `isLocal:true` → `tabs_context_mcp(createIfEmpty=true)`
- ห้ามเรียก `navigate` เดี่ยว ให้ห่อใน `browser_batch([navigate, computer wait 6])` เสมอ
- ถ้า Discord ขึ้นหน้า login: **หยุดส่วน A รายงาน ห้ามกรอกรหัสผ่าน** แล้วไปทำส่วน B ต่อ
- **ก่อนรัน merge ต้องตรวจไฟล์ `work/*.txt` ด้วย SHA-256** เทียบกับฝั่งเบราว์เซอร์ (ส่งแฮชของไฟล์เข้าไปให้หน้าเว็บเทียบแล้วตอบ true/false) ถ้าไม่ตรงห้าม merge
- **ทางลัดที่ใช้ได้จริง:** ใบลาและรายงานการผลิตมักไม่เปลี่ยนหลายวันติด ให้แฮชข้อความในเบราว์เซอร์เทียบกับ `work/new_leave.txt` / `work/new_prod.txt` ที่มีอยู่ก่อน ถ้าตรงกันให้ใช้ไฟล์เดิมเลย ไม่ต้องคัดข้อความออกมาใหม่ทั้งก้อน
- ผลของ `javascript_tool` ถูกตัดที่ ~1000 ตัวอักษร และข้อความที่มีทั้ง `&` และ `=` จะถูกบล็อก — ถ้าเจอ ให้สลับเป็น `<EQ>` / `<AMP>` แล้วแทนกลับ ห้ามเดาเนื้อหา
- ตัวเลขทุกตัวให้สคริปต์คำนวณ ห้ามคิดเอง
- **ห้ามเพิ่มชื่อพนักงาน/ชื่อเล่น** ถ้าเจอ `unknown_names` ให้รายงานเฉย ๆ
- ห้ามเปลี่ยนกฎ OT/สาย ห้ามคัดลอกเงินเดือน เงินเบิก เลขบัญชี หรือยอดเงิน OT
- จบส่วน A ให้ปิดแท็บ Chrome ที่เปิดด้วย `tabs_close_mcp`
- auto-push (launchd com.wibwub.autopush) จะ push ให้เอง **ไม่ต้อง git push**

---

# รูปแบบรายงานท้ายรอบ (ภาษาไทย แยกสองหัวข้อ)

```
## A — HR
<สำเร็จ/ล้มเหลว> · ดึงตั้งแต่วันที่ N · เพิ่มเข้า X ออก Y · ใบลาใหม่ · รายงานการผลิตใหม่
ชื่อที่ไม่รู้จัก · ลืมเช็คเอาท์ · มาสายวันนี้ · OT รวมเดือนนี้ · commit id
(ยังไม่ได้เขียน Google Sheet — ตั้งใจข้าม)

## B — FastMoss
<สำเร็จ/ข้าม เพราะทำไปแล้ววันนี้/ล้มเหลว> · ยอด 28 วัน WIBWUB vs munwow (ออเดอร์/ยอดขาย) · commit id
```
