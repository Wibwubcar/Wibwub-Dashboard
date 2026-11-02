---
name: wibwub-download-tiktok-ads
description: ดาวน์โหลด TikTok Ads data ทุกวัน 08:10/19:10 — GMV Max Campaign Overview + Business Ads Campaign Report
---

> 🔁 **ไฟล์นี้คือสำเนาของพรอมป์ตัวจริง** ที่ `~/Documents/Claude/Scheduled/wibwub-download-tiktok-ads/SKILL.md`
> (งาน local อ่านไฟล์นั้น · ไม่มีสคริปต์หรืองานไหนอ่านไฟล์นี้) · มีไว้ให้ git เก็บประวัติ
> **แก้ที่นี่แล้วไม่มีผล** — แก้ไฟล์ตัวจริงก่อน แล้วคัดลอกมาทับไฟล์นี้ในคอมมิตเดียวกัน
> เวอร์ชันเก่าที่ยาวกว่า (302 บรรทัด) ซึ่งไม่ตรงกับของที่รันอยู่ ดูได้จาก git history และไฟล์ .bak-2026-11-02-mirror


## WIBWUB TikTok Ads Download — ทุกวัน 08:25 / 19:25

ดาวน์โหลด TikTok Ads data 2 ประเภทและบันทึกไปยังโฟลเดอร์งาน

### Paths (พาธเต็มเท่านั้น ห้ามใช้พาธ relative / `$BASE`)
- GMV Max folder: `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/data Ads/TikTok/GMV Max/`
- Business Ads folder: `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/data Ads/TikTok/Business Ads/`
- Downloads: `/Users/thanasablilutanon/Downloads/`

⛔ พาธ `/sessions/<ชื่อ>/mnt/...` ของแซนด์บ็อกซ์เดิม **ตายแล้ว** เจอที่ไหนให้ถือว่าผิด
⛔ **ไม่ต้อง `cp` ไฟล์ทั้งสองชนิด** — LaunchAgent `com.wibwub.download-mover` มีกฎครบแล้ว
   (`Campaign overview data *.xlsx` → GMV Max · `WIBWUBCAR-Campaign Report-*.xlsx` → Business Ads)
   และย้ายให้ภายใน ~5 วินาที · `cp` ในพรอมป์แข่งกับตัวย้ายแล้วมักแพ้ จนรายงานผิดว่า "ไม่พบไฟล์"
   หน้าที่ของรอบนี้คือ **ตรวจว่าไฟล์ถึงโฟลเดอร์ปลายทางจริง**

### ⚠️ Chrome Navigation Rule
ต้องใช้ browser_batch ทุกครั้ง ห้าม navigate standalone:
```
browser_batch([navigate(url="...", tabId=TAB), computer(action="wait", duration=5, tabId=TAB), computer(action="screenshot", tabId=TAB)])
```

### ⚠️ ต้องระบุ browser ที่ Mac เสมอ ห้ามปล่อยให้เลือกอัตโนมัติ
ก่อน tabs_context_mcp ครั้งแรก: `select_browser(deviceId="b75a6bb0-5b78-4e44-92a8-75224f1ce4ee")`
(ถ้า deviceId นี้ไม่ connected แล้ว ให้เรียก `list_connected_browsers` ก่อน แล้วเลือกตัวที่ `osPlatform` เป็น macOS / `isLocal:true` เท่านั้น — ห้ามเลือก Windows/PC)

---

## 🛡️ Session Check ก่อนทำทุกอย่าง
Navigate ไปที่ https://ads.tiktok.com/i18n/dashboard?aadvid=7229166192752148482
- ถ้าเห็น Dashboard = session OK
- ถ้า redirect ไป login = session expired → log แล้วหยุด รายงาน "TikTok Ads session expired"

---

## PART 1 — GMV Max Campaign Overview

### เป้าหมาย
ดาวน์โหลด Campaign overview data (daily totals: spend, orders, revenue) สำหรับเดือนปัจจุบัน

### ขั้นตอน
1. คำนวณวันที่:
```python
from datetime import datetime, timedelta, timezone
tz_th = timezone(timedelta(hours=7))
today = datetime.now(tz_th)
first = today.replace(day=1)
# Unix ms สำหรับ URL params
start_ms = int(first.timestamp() * 1000 - 7*3600000)  # UTC
end_ms = int(today.timestamp() * 1000 + (23*3600 + 59*60)*1000)
```

2. Navigate ไป GMV Max ด้วย date params:
URL: `https://ads.tiktok.com/i18n/gmv-max/dashboard?aadvid=7229166192752148482&oec_seller_id=7494549095358892612&bc_id=7229165256428240898&type=product&list_start_date={start_ms}&list_end_date={end_ms}`

3. รอ 5 วินาที → หาปุ่ม download:
```javascript
// หา input fields เพื่อ verify date range
const inputs = Array.from(document.querySelectorAll('input[type="text"]'))
  .filter(e => e.getBoundingClientRect().top > 360 && e.getBoundingClientRect().top < 440);
inputs.map(e => e.value)
```

4. คลิกปุ่ม Download (ส่งออกข้อมูล) — หาจาก button ที่ pos บนขวา:
```javascript
const btn = Array.from(document.querySelectorAll('button,[role="button"]'))
  .find(b => b.getBoundingClientRect().top > 360 && b.getBoundingClientRect().top < 420 && b.getBoundingClientRect().left > 1150);
if (btn) btn.click();
```
หรือ find tool: "ส่งออกข้อมูล"

5. รอ 10 วินาที (ให้ตัวย้ายทำงาน) → **ตรวจที่โฟลเดอร์ปลายทาง ไม่ใช่ Downloads**:
```bash
python3 -c "
import glob, os, time
d = glob.glob('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/data Ads/TikTok/GMV Max/*Campaign overview data*.xlsx')
f = max(d, key=os.path.getmtime) if d else None
age = (time.time() - os.path.getmtime(f))/60 if f else None
print('ไฟล์ล่าสุด:', os.path.basename(f) if f else 'ไม่มี', '| %.0f นาที' % age if age is not None else '')
print('✅ GMV Max OK' if age is not None and age < 15 else '⛔ GMV Max: ยังไม่ถึงปลายทาง')
"
```
⛔ ถ้ายังไม่ถึง: ตรวจซ้ำอีกครั้งหลัง 10 วินาที · ยังไม่มาอีกให้ดูว่าไฟล์ค้างใน `/Users/thanasablilutanon/Downloads` ไหม
ถ้าค้างอยู่จริงให้ `cp` เอง **แล้วรายงานว่าตัวย้ายไม่ทำงาน** (เป็นเรื่องผิดปกติ ไม่ใช่ขั้นตอนปกติ)

---

## PART 2 — Business Ads Campaign Report

### เป้าหมาย
ดาวน์โหลด Campaign performance report (C-Ads campaigns spend/impressions/clicks)

### ขั้นตอน
1. Navigate ไป Campaign page:
URL: `https://ads.tiktok.com/i18n/manage/campaign?aadvid=7229166192752148482&st={YYYY-MM-01}&et={YYYY-MM-DD}`
(ใช้ first_of_month และ today)

2. รอ 5 วินาที → screenshot

3. คลิก "ดูรายงาน" (View Reports) จาก sidebar:
```javascript
const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('ดูรายงาน'));
if (btn) btn.click();
```

4. รอ dialog/panel เปิด → หาปุ่ม download Campaign Report:
   - ใช้ find tool: "download" หรือ "ดาวน์โหลด" ใน dialog
   - ถ้ามีหลาย format → เลือก Excel (.xlsx)

5. รอ 10 วินาที (ให้ตัวย้ายทำงาน) → **ตรวจที่โฟลเดอร์ปลายทาง**:
```bash
python3 -c "
import glob, os, time
d = glob.glob('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/data Ads/TikTok/Business Ads/WIBWUBCAR-Campaign Report-*.xlsx')
f = max(d, key=os.path.getmtime) if d else None
age = (time.time() - os.path.getmtime(f))/60 if f else None
print('ไฟล์ล่าสุด:', os.path.basename(f) if f else 'ไม่มี', '| %.0f นาที' % age if age is not None else '')
print('✅ Business Ads OK' if age is not None and age < 15 else '⛔ Business Ads: ยังไม่ถึงปลายทาง')
"
```
⛔ ยังไม่ถึง → เงื่อนไขเดียวกับ PART 1 (ตรวจซ้ำ แล้วค่อยดูว่าค้างใน Downloads ไหม)

---

## สรุปผล

```
TikTok Ads Download — {TODAY}
📅 ช่วงข้อมูล: 01/{MONTH} – {TODAY}

✅/⛔ GMV Max: {filename หรือ error}
✅/⛔ Business Ads: {filename หรือ error}

หมายเหตุ: {ถ้ามี session ปัญหา ฯลฯ}
```

## หากมีปัญหา
- Session expired → log "TikTok Ads session expired — re-login required" แล้วหยุด
- ไม่พบไฟล์หลัง download → retry 1 ครั้ง รอ 15 วินาที
- navigate ค้าง → ใช้ browser_batch เท่านั้น

## ⚠️ ขั้นตอนต่อ (สำคัญ — ห้ามข้าม): อัปเดต WIBWUB_Ads_Dashboard.html หลังดาวน์โหลด

**Root cause ของปัญหาเดิม (พบ 2026-07-30):** Schedule นี้ดาวน์โหลดไฟล์ดิบเข้า `data Ads/TikTok/{GMV Max,Business Ads}/`
เท่านั้น ไม่เคย parse/อัปเดต `data Ads/WIBWUB_Ads_Dashboard.html` เอง ทำให้ Dashboard ค้างข้อมูลเก่าแม้ดาวน์โหลดไฟล์ใหม่ทุกวัน
→ ทุกครั้งที่ดาวน์โหลดไฟล์ xlsx ใหม่เสร็จ ให้ทำต่อทันที ห้ามจบงานแค่ download:

1. **GMV Max Campaign overview**: ไฟล์ export มักมีแถวสุดท้ายเป็น "Total" (day/date = `-`) ที่เป็นผลรวมของทุกแถวก่อนหน้าอยู่แล้ว
   **ใช้แถว Total นี้ตรงๆ** ห้าม sum ทุกแถวเองอีกรอบ (จะ double-count) — ค่าที่ต้องดึง: spend, orders, revenue, roi, cpa
2. **Business Ads Campaign Report**: ไฟล์มีหลายแถวต่อ campaign ต่อวัน + แถวรวม (Campaign ID = `-`) เป็นผลรวม
   Aggregate ตาม Campaign ID จริงเท่านั้น (ไม่รวม key `-` เข้าไปใน list แคมเปญ) แล้วเช็คว่า sum(campaigns) == แถว `-` เพื่อ verify ก่อนใช้
   Column: `[2]`=spend, `[3]`=impressions, `[7]`=clicks(all)
3. รวม TikTok revenue/orders รวม = gmvMax + gmvLive เท่านั้น (bizAds มีแค่ spend/imp/clicks ไม่มี revenue/orders เพราะเป็น impression-based ไม่ใช่ product-sales)
4. **ก่อนเขียน ให้สร้างโครงเดือนก่อนเสมอ** (ขึ้นเดือนใหม่แล้วคีย์ยังไม่มี = เขียนไม่ได้
   เกิดจริงกับงาน Shopee Ads รอบ 2 พ.ย. 08:22 — ดึงข้อมูลได้แต่รายงานขึ้น ⛔):
   ```
   python3 "<BASE>/scripts/ads/ensure_month.py"
   ```
   ไม่ต้องใส่ `--month` (ใช้เดือนปัจจุบัน) · มีคีย์อยู่แล้วจะไม่แตะไฟล์เลย
5. แก้ `DATA_PERIODS.<เดือนปัจจุบัน>.tiktok` และ `TK_BREAKDOWN.<เดือนปัจจุบัน>.{gmvMax,gmvLive,bizAds}` ใน `data Ads/WIBWUB_Ads_Dashboard.html`
   (ไฟล์นี้ minified บรรทัดเดียวยาวมาก — ใช้ Python อ่าน/แทนที่ substring แบบ exact-match, ห้ามใช้ Edit tool บรรทัดปกติ)
6. อัปเดต badge `#ads-updated` และ `.pb-sub` labels ให้ตรงกับวันที่ข้อมูลล่าสุดจริงของทั้ง Shopee และ TikTok
7. Validate JS (`node --check` หลัง extract `<script>` blocks), bump `sw.js` cache version, `git add`+`git commit` (push ต้องให้ user double-click `push_now.command`)


## ⚠️ กฎการย้ายไฟล์จาก Downloads (สำคัญมาก)

**ปัญหา:** Sandbox (Linux) ลบไฟล์จาก Downloads ไม่ได้ — `mv` และ `rm` จาก Downloads ล้มเหลวด้วย "Operation not permitted"

**วิธีที่ถูกต้องสำหรับ sandbox:**
- ใช้ `cp` เพื่อ copy ไปยังโฟลเดอร์งาน (ทำได้ ✅)
- ห้ามใช้ `mv` หรือ `rm` กับไฟล์ใน Downloads จาก sandbox (ล้มเหลว ❌)

**ระบบย้ายอัตโนมัติ (ไม่ต้องทำอะไรเพิ่ม):**
มี macOS LaunchAgent `com.wibwub.download-mover` ทำงานอยู่เบื้องหลังตลอดเวลา
เมื่อ schedule cp ไฟล์ไปโฟลเดอร์งานแล้ว LaunchAgent จะ **mv (ย้าย)** ไฟล์ต้นฉบับออกจาก Downloads อัตโนมัติภายใน 5 วินาที
— ไม่ต้อง double-click อะไรทั้งนั้น ทุกอย่างเป็นอัตโนมัติ

**Script ที่เกี่ยวข้อง (อยู่ใน All/scripts/):**
- `wibwub_auto_move.sh` — script ย้ายไฟล์ (ถูกเรียกโดย LaunchAgent)
- `com.wibwub.download-mover.plist` — LaunchAgent config (WatchPaths ~/Downloads)