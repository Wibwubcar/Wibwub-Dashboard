---
name: wibwub-shopee-live-daily
description: ทุกวัน 08:37/19:37 — ดึงข้อมูล Shopee Live ใหม่จาก Seller Centre → merge เข้า SH_LIVE_DAILY ใน WIBWUB_Dashboard.html → bump sw.js → commit + push_now.command
---

งาน: อัปเดตข้อมูล Shopee Live รายวัน (ส่วน "📺 ยอดขายไลฟ์สดรายวัน — Shopee Live" ใน WIBWUB_Dashboard.html ที่ใช้ SH_LIVE_DAILY เป็น data source, mirror โครงสร้างเดียวกับ TK_LIVE_DAILY)

Base folder: /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All
ไฟล์หลัก: WIBWUB_Dashboard.html, sw.js

## Step 1 — อ่านสถานะปัจจุบัน
Read WIBWUB_Dashboard.html, หา `const SH_LIVE_DAILY = {...}` (อยู่หลัง `tklInit(); tklRender();`)
- `SH_LIVE_DAILY.dates` = array วันที่ต่อเนื่อง (ISO string) ตั้งแต่ 2026-04-01
- `SH_LIVE_DAILY.daily[date]` = `{gmv, orders, viewers, newFollowers}` — วันที่ไม่มีไลฟ์ค่าจะเป็น 0 ทั้งหมด
- หา `lastDate` = ตัวสุดท้ายใน `dates` array — นี่คือจุดที่ต้องดึงข้อมูลต่อ (ตั้งแต่ lastDate+1 ถึงวันนี้)
- ถ้า lastDate เท่ากับหรือมากกว่าวันนี้แล้ว → ข้อมูลอัปเดตล่าสุดแล้ว ไม่ต้องทำอะไรต่อ จบงานเลย

## Step 2 — ดึงข้อมูล Shopee Live ใหม่ผ่าน Chrome
ใช้ Chrome MCP (`mcp__Claude_in_Chrome__*`) — ก่อนเริ่มต้อง `select_browser` เลือก browser บน Mac จริงเสมอ (ห้ามปล่อยเลือกอัตโนมัติ), แล้ว `tabs_context_mcp(createIfEmpty=true)` เหมือน task อื่นๆ ของ WIBWUB (ดู wibwub-download-orders-monday เป็นตัวอย่าง pattern การเช็ค session/recovery)

Shopee Seller Centre → เครื่องมือไลฟ์ (Live tools) / Data Center Live Analysis:
1. Navigate ไปที่ https://seller.shopee.co.th (หรือเมนู "เครื่องมือไลฟ์" ในหน้า Seller Centre) → wait 5s → screenshot
2. ถ้า redirect ไปหน้า login = session หมด → แจ้งใน completion report ว่าต้อง login Shopee ใน Claude Chrome เอง แล้วหยุดงาน (ห้ามพยายาม login เอง)
3. หาเมนู "ไลฟ์" หรือ "Live" → "ข้อมูลวิเคราะห์" / "Live Analysis" หรือหน้ารายงานสรุปไลฟ์แต่ละครั้ง (เดิมเคยอยู่ที่ Data Center > Live) — ใช้ `find`/`get_page_text` สำรวจถ้าตำแหน่งเมนูเปลี่ยน
4. ตั้งช่วงวันที่: lastDate+1 ถึงวันนี้ (ถ้าเป็นวันเดียวกับ lastDate อยู่แล้ว ให้ลองรวมวันปัจจุบันด้วยเผื่อมีไลฟ์เพิ่ม)
5. กด Export / ส่งออกรายงาน (CSV) ของทุกไลฟ์ในช่วงนั้น → รอดาวน์โหลด
   ⚠️ ถ้าเจอ Chrome popup "Allow multiple automatic downloads" ให้แจ้งใน completion report ว่าต้องกด Allow เองครั้งนี้ (auto-click ไม่ได้) แล้วลอง export ใหม่อีกครั้งหลัง user กดอนุญาต
6. ไฟล์ที่โหลดมาจะอยู่ที่ `/Users/thanasablilutanon/Downloads/` — ใช้ `cp` ย้ายไปที่ `All/data ยอดขาย plaform/Shopee Live/` (สร้างโฟลเดอร์นี้ถ้ายังไม่มี) เพื่อเก็บ raw ไว้ตรวจสอบย้อนหลังได้

## Step 3 — Parse CSV และรวมยอดต่อวัน
คอลัมน์ในไฟล์ CSV ของ Shopee Live analysis (อิงจากตารางที่ใช้แสดงผลในหน้า dashboard):
- วันที่ไลฟ์ → ใช้ mapping เป็น key ISO date (YYYY-MM-DD)
- ยอดขาย (ยืนยันแล้ว) → `gmv`
- คำสั่งซื้อ → `orders`
- ผู้ชมทั้งหมด → `viewers`
- ผู้ติดตามใหม่ → `newFollowers`

ถ้าวันเดียวมีไลฟ์มากกว่า 1 รอบ ให้ **sum** ทั้ง 4 ค่าเข้าด้วยกันเป็นค่าของวันนั้นวันเดียว (เหมือนที่ backfill Apr–Sep ทำไว้)

## Step 4 — Merge เข้า SH_LIVE_DAILY
- ขยาย `SH_LIVE_DAILY.dates` ให้ต่อเนื่องทุกวันจาก lastDate+1 ถึงวันนี้ (รวมวันที่ไม่มีไลฟ์ด้วย โดยใส่ `{gmv:0,orders:0,viewers:0,newFollowers:0}`)
- ใส่ค่าจริงเฉพาะวันที่มีไลฟ์ (จาก Step 3)
- แก้ไฟล์ WIBWUB_Dashboard.html ด้วย Edit tool เท่านั้น (ห้าม regenerate ทั้งไฟล์)

## Step 5 — Validate
- Extract `<script>` blocks แล้วรัน `node --check` ต้องผ่านไม่มี syntax error
- เช็คว่า `SH_LIVE_DAILY.dates.length` ตรงกับจำนวนวันจริงระหว่างวันแรก (2026-04-01) ถึงวันสุดท้าย (ไม่มีวันขาด)

## Step 6 — Bump sw.js + Commit
1. เปิด sw.js, เพิ่มเลข version ใน `const CACHE = 'wibwub-vNNN';` ขึ้น 1
2. `cd` ไปที่ All folder แล้ว:
   ```bash
   git add WIBWUB_Dashboard.html sw.js
   git commit -m "Update Shopee Live daily data through <วันที่ล่าสุด>"
   ```
   **สำคัญ:** commit เฉพาะ WIBWUB_Dashboard.html และ sw.js เท่านั้น ห้ามรวมไฟล์อื่นที่อาจ modified จาก task อื่นๆ (เช่น report .md, push_now.command, vid_merge.py ฯลฯ)
3. อย่าพยายาม `git push` จาก sandbox — จะ fail ด้วย 403 proxy error เสมอ (เป็นเรื่องปกติ) ให้ผู้ใช้กด `push_now.command` เองบนเครื่องจริงแทน

## Completion Report (สรุปสั้นๆ)
- ✅ อัปเดต Shopee Live: [N] วันใหม่ที่มีไลฟ์ ([lastDate+1] ถึง [วันนี้]) ยอดขายรวมช่วงนี้ ฿[X]
- หรือ "ไม่มีข้อมูลใหม่ ข้อมูลอัปเดตล่าสุดแล้ว" ถ้า lastDate = วันนี้แล้ว
- ⛔ ถ้า session Shopee หมดหรือเจอ permission popup ที่ auto-click ไม่ได้ → แจ้งชัดเจนว่าต้องทำอะไรต่อ (login / กด Allow) แล้วรอบหน้าจะลองใหม่
- เตือนให้กด push_now.command เพื่อ publish ขึ้น GitHub Pages เสมอเมื่อมีการ commit
