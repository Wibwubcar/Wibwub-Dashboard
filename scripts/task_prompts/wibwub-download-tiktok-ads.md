---
name: wibwub-download-tiktok-ads
description: ดาวน์โหลด TikTok Ads data ทุกวัน 08:10/19:10 — GMV Max Campaign Overview + Business Ads Campaign Report
---

## WIBWUB TikTok Ads Download — ทุกวัน 08:10 / 19:10

โหลดไฟล์ดิบ 2 ชุดจาก TikTok Ads Manager เก็บเข้าโฟลเดอร์งาน (เป็นคลังย้อนหลัง
ไม่มีสคริปต์ไหนอ่านอัตโนมัติ — `wibwub-ads-daily` ดึงตัวเลขจาก API สดแยกต่างหาก)

| ชุด | ชื่อไฟล์ที่โหลดได้ | ปลายทาง |
|---|---|---|
| GMV Max Campaign overview | `Campaign overview data YYYYMMDD - YYYYMMDD.xlsx` | `data Ads/TikTok/GMV Max/` |
| Business Ads Campaign Report | `WIBWUBCAR-Campaign Report-YYYY-MM-01 to YYYY-MM-DD.xlsx` | `data Ads/TikTok/Business Ads/` |

BASE = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`

---

## 🚚 การย้ายไฟล์ — **ห้าม `cp` เอง**

launchd `com.wibwub.download-mover` (WatchPaths `~/Downloads`) ย้ายไฟล์ทั้ง 2 แบบ
เข้าโฟลเดอร์ปลายทางให้เองภายใน ~5 วินาที ผ่าน `scripts/wibwub_auto_move.sh`

> **บั๊กเดิม (แก้แล้ว 20 ต.ค. 2569):** พรอมป์เวอร์ชันก่อนสั่ง `cp` จาก `~/Downloads`
> หลังรอ 10 วินาที — ซึ่ง**แข่งกับ mover แล้วแพ้เกือบทุกครั้ง** ไฟล์ถูกย้ายไปแล้ว
> `cp` จึงหาไม่เจอและรายงาน "⛔ ไม่พบไฟล์" ทั้งที่โหลดสำเร็จ
> ซ้ำร้าย mover เดิมทิ้งไฟล์ไว้ที่ `data Ads/Tiktok/` (ราก) ไม่ใช่โฟลเดอร์ย่อย
> ตอนนี้ mover ย้ายเข้า `Business Ads/` และ `GMV Max/` ตรง ๆ แล้ว

**หน้าที่ของงานนี้คือ: กดโหลด → รอ → ตรวจว่าไฟล์โผล่ที่ปลายทาง** เท่านั้น
ชื่อซ้ำ mover จะต่อท้าย `__YYYYMMDD_HHMMSS` ให้เอง (ไม่เขียนทับ) — ไฟล์เหมือนกันทุกไบต์จะถูกเก็บเข้า archive/dup

---

## ⚠️ กฎ Chrome

- ก่อน `tabs_context_mcp` ครั้งแรก: `select_browser(deviceId="b75a6bb0-5b78-4e44-92a8-75224f1ce4ee")`
  (ถ้าไม่ connected → `list_connected_browsers` แล้วเลือกตัวที่ `osPlatform` = macOS / `isLocal:true` เท่านั้น ห้ามเลือก Windows)
- navigate ต้องอยู่ใน `browser_batch` เสมอ:
  `browser_batch([navigate(url=..., tabId=TAB), computer(wait 5), computer(screenshot)])`
- **UI สลับภาษาไทย/อังกฤษได้** ทุก selector ต้องจับทั้งสองภาษา ห้าม hardcode ภาษาเดียว

### Session check
Navigate `https://ads.tiktok.com/i18n/dashboard?aadvid=7229166192752148482`
ถ้า redirect ไปหน้า login → รายงาน "TikTok Ads session expired — ต้อง re-login" แล้ว**หยุด** (ห้ามพยายาม login เอง)

---

## 0. ข้ามรอบถ้าโหลดไว้แล้ว (idempotency)

งานรันวันละ 2 รอบ รอบเย็นควรโหลดทับเพราะข้อมูลเดินต่อ แต่ถ้าถูกสั่งรันซ้ำติด ๆ กัน
(retry / รันมือ) ให้ข้าม เพื่อไม่ให้ archive บวมด้วยไฟล์ `__stamp` ที่ต่างกันไม่กี่บาท

```bash
BASE="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
TODAY=$(date +%Y-%m-%d)
for d in "$BASE/data Ads/TikTok/Business Ads" "$BASE/data Ads/TikTok/GMV Max"; do
  n=$(find "$d" -maxdepth 1 -type f -newermt "$TODAY 00:00" 2>/dev/null | wc -l | tr -d ' ')
  # find -newermt บน macOS บางเครื่องคืนค่าว่าง → เช็คซ้ำด้วย mtime ของไฟล์ล่าสุด
  latest=$(ls -t "$d" | head -1)
  echo "$d → วันนี้ $n ไฟล์ · ล่าสุด: $latest"
done
```
ถ้าทั้งสองโฟลเดอร์มีไฟล์ของ **ชั่วโมงนี้** อยู่แล้ว → รายงาน "ข้ามรอบ (โหลดไปแล้ว)" แล้วจบ

---

## PART 1 — GMV Max Campaign overview

### 1.1 คำนวณวันที่

```python
from datetime import datetime, timedelta, timezone
tz = timezone(timedelta(hours=7))
now = datetime.now(tz)
first = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
today0 = now.replace(hour=0, minute=0, second=0, microsecond=0)
start_ms = int(first.timestamp() * 1000)
end_ms   = int((today0 + timedelta(hours=23, minutes=59, seconds=59)).timestamp() * 1000)
```

> **บั๊กเดิม:** สูตรเก่าใช้ `today.timestamp() + 23ชม.59น.` โดย `today` เป็น**เวลาปัจจุบัน**
> ไม่ใช่เที่ยงคืน → ถ้ารันหลัง 00:01 end จะข้ามไปวันถัดไป ได้ไฟล์ชื่อ
> `... - 20261021` ทั้งที่วันนี้คือ 20 (เห็นจริงในไฟล์ `Campaign overview data 20261001 - 20261021.xlsx`)
> ต้อง normalize เป็นเที่ยงคืนก่อนเสมอ และสูตรเก่ายัง `- 7*3600000` ที่ start เกินมาอีก (timestamp เป็น UTC อยู่แล้ว)

### 1.2 เปิดหน้า

`https://ads.tiktok.com/i18n/gmv-max/dashboard?aadvid=7229166192752148482&oec_seller_id=7494549095358892612&bc_id=7229165256428240898&type=product&list_start_date={start_ms}&list_end_date={end_ms}`

รอ 5 วิ → screenshot → ยืนยันว่าช่วงวันที่บนหน้าตรงกับที่ขอ (ถ้าไม่ตรง ให้รายงานแล้วหยุด ห้ามโหลดข้อมูลผิดช่วง)

### 1.3 กดปุ่มส่งออก

```javascript
const L = ['ส่งออกข้อมูล','ส่งออก','Export data','Export','ดาวน์โหลด','Download'];
const b = Array.from(document.querySelectorAll('button,[role="button"],a'))
  .find(e => L.some(x => (e.textContent||'').trim().includes(x)) && e.offsetParent);
b ? (b.click(), 'clicked: ' + b.textContent.trim()) : 'NOT FOUND';
```
ถ้าได้ `NOT FOUND` → ใช้ `find` tool ด้วยคำว่า `Export` และ `ส่งออก` ก่อน แล้วค่อย fallback ไปหาปุ่มมุมขวาบนของตาราง

### 1.4 ตรวจผล (รอ 20 วิ)

```bash
ls -lt "$BASE/data Ads/TikTok/GMV Max/" | head -3
```
ต้องเห็นไฟล์ `Campaign overview data {YYYYMMDD} - {YYYYMMDD}.xlsx` ที่ mtime เป็นเวลานี้

---

## PART 2 — Business Ads Campaign Report

### 2.1 เปิดหน้า Campaign

`https://ads.tiktok.com/i18n/manage/campaign?aadvid=7229166192752148482&st={YYYY-MM-01}&et={YYYY-MM-DD}`
(`et` = **วันนี้** ตามเขตเวลาไทย — ใช้ `today0` จากข้อ 1.1 ห้ามบวก 1 วัน)

รอ 5 วิ → screenshot

### 2.2 กด **“… More” (เพิ่มเติม) → “Export data” (ส่งออกข้อมูล)**

> **บั๊กเดิมข้อใหญ่ที่สุด:** พรอมป์เก่าสั่งกด **“ดูรายงาน” / “View report”**
> ปุ่มนั้น**ไม่ใช่ export** — มันเปิดพาเนลสรุปของ AI ที่ไม่มีปุ่มดาวน์โหลดไฟล์
> ปุ่มส่งออกจริงอยู่ใน **เมนู “… More” มุมขวาบนของแถบตาราง** (แถวเดียวกับ “View report”)
> รายการในเมนูเรียงว่า: Export/Import · Label · Automated rules · **Export data** · Keyboard shortcuts
> **ต้องเลือกรายการที่ 4 “Export data” เท่านั้น** — “Export/Import” (รายการแรก) คือการนำเข้า/ส่งออก
> *โครงสร้างแคมเปญ* ไม่ใช่ตัวเลขผลลัพธ์

```javascript
// ขั้นที่ 1 — เปิดเมนู More
const more = Array.from(document.querySelectorAll('button,[role="button"],span,div'))
  .filter(e => e.offsetParent && /^(More|เพิ่มเติม|\.\.\. ?More)$/.test((e.textContent||'').trim()))
  .pop();
more ? (more.click(), 'opened') : 'MORE NOT FOUND';
```
รอ 1 วิ แล้ว:
```javascript
// ขั้นที่ 2 — เลือก "Export data" (ห้ามจับ "Export/Import" ซึ่งขึ้นต้นด้วย Export เหมือนกัน)
const OK  = ['Export data','ส่งออกข้อมูล'];
const BAD = ['Export/Import','ส่งออก/นำเข้า','นำเข้า'];
const it = Array.from(document.querySelectorAll('[role="menuitem"],li,div,span'))
  .filter(e => e.offsetParent)
  .find(e => { const t=(e.textContent||'').trim();
               return OK.some(x=>t===x||t.startsWith(x)) && !BAD.some(x=>t.includes(x)); });
it ? (it.click(), 'export clicked') : 'EXPORT ITEM NOT FOUND';
```

### 2.3 รอไฟล์ (async — ไม่ใช่ดาวน์โหลดทันที)

หลังกด จะมีป้าย **“Exporting data”** โผล่มุมขวาบนของ header พร้อมสปินเนอร์
เบื้องหลังเป็น 2 จังหวะ (ตรวจยืนยันแล้วจาก network เมื่อ 20 ต.ค. 2569):

1. `POST /api/v4/i18n/statistics/op/campaign/task_create/real_time/?aadvid=...` → คืน `download_id` + `status:"PENDING"`
2. `POST /api/v4/i18n/statistics/reporting/task_query/?aadvid=...` โพลซ้ำจน `status:"SUCCESS"`
   แล้วคืน `data.url` เป็นลิงก์ signed (`ads.tiktok.com/wsos_v2/statistics/object/...&expire=&sign=`)
   เบราว์เซอร์ดาวน์โหลดจากลิงก์นั้นเอง

ปกติเสร็จใน 5–15 วินาที **ให้รออย่างน้อย 20 วินาที** ก่อนสรุปว่าไม่สำเร็จ
ลิงก์มีอายุ ~1 ชั่วโมง (`expire`) — ถ้าจะ retry ให้กด export ใหม่ ไม่ต้องไปงมลิงก์เดิม

### 2.4 ตรวจผล

```bash
ls -lt "$BASE/data Ads/TikTok/Business Ads/" | head -3
```
ต้องเห็น `WIBWUBCAR-Campaign Report-{YYYY-MM-01} to {YYYY-MM-DD}.xlsx` mtime เป็นเวลานี้
ถ้ายังไม่มี รอเพิ่มอีก 15 วิ แล้วตรวจซ้ำ 1 ครั้ง ก่อนรายงานว่าไม่สำเร็จ

---

## PART 3 — อัปเดต Ads Dashboard

ทำต่อทันทีเมื่อได้ไฟล์ใหม่ ห้ามจบงานแค่ download
(เดิม schedule นี้โหลดไฟล์อย่างเดียว ไม่เคย parse → Dashboard ค้างข้อมูลเก่าแม้โหลดไฟล์ใหม่ทุกวัน)

1. **GMV Max overview**: แถวสุดท้ายเป็น `Total` (day/date = `-`) ซึ่งรวมทุกแถวไว้แล้ว
   **ใช้แถวนี้ตรง ๆ ห้าม sum เอง** (จะ double-count) — ดึง spend, orders, revenue, roi, cpa
2. **Business Ads report**: หลายแถวต่อ campaign ต่อวัน + แถวรวม (Campaign ID = `-`)
   aggregate เฉพาะ Campaign ID จริง แล้วเช็ค `sum(campaigns) == แถว '-'` ก่อนใช้
   คอลัมน์: `[2]`=spend · `[3]`=impressions · `[7]`=clicks(all)
3. TikTok revenue/orders รวม = **gmvMax + gmvLive เท่านั้น**
   (bizAds มีแค่ spend/imp/clicks เป็น impression-based ไม่มี revenue/orders)
4. แก้ `DATA_PERIODS.<เดือนปัจจุบัน>.tiktok` และ `TK_BREAKDOWN.<เดือนปัจจุบัน>.{gmvMax,gmvLive,bizAds}`
   ใน `data Ads/WIBWUB_Ads_Dashboard.html`
   ไฟล์นี้ minified บรรทัดเดียว → ใช้ Python แทนที่ substring แบบ exact-match **ห้ามใช้ Edit tool**
5. อัปเดต badge `#ads-updated` และ `.pb-sub` ให้ตรงวันข้อมูลล่าสุดจริงของทั้ง Shopee และ TikTok
6. ตรวจ + commit:

```bash
export BASE
python3 - <<'PY'
import re, os, subprocess, tempfile, pathlib
p = pathlib.Path(os.environ['BASE'])/'data Ads/WIBWUB_Ads_Dashboard.html'
js = pathlib.Path(tempfile.gettempdir())/'ads_check.js'
js.write_text('\n;\n'.join(re.findall(r'<script[^>]*>([\s\S]*?)</script>', p.read_text(encoding='utf-8'))), encoding='utf-8')
r = subprocess.run(['node','--check',str(js)], capture_output=True, text=True)
print('node --check', 'OK' if r.returncode==0 else 'FAIL\n'+r.stderr[:400])
PY
python3 "$BASE/scripts/bump_sw.py"   # ห้ามใช้ sed -i — BSD sed ต้องใส่ '' และเคยพังเงียบ ๆ มาแล้ว
git -C "$BASE" add "data Ads/WIBWUB_Ads_Dashboard.html" sw.js
git -C "$BASE" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
    commit -m "auto-update: TikTok Ads $(date +%Y-%m-%d)"
```

> ไฟล์ `.xlsx` **ไม่ต้อง `git add`** — `.gitignore` บรรทัดแรกคือ `*.xlsx` คำสั่ง add จึงเป็น no-op
> ไม่ต้อง `git push` — launchd `com.wibwub.autopush` push ให้เองใน 2 นาที (ไม่มี error 403 แบบ sandbox เดิม)

---

## RULES

- ทำทุกอย่างใน bash/python + Chrome tools ห้าม spawn subagents
- ห้าม `cp`/`mv`/`rm` ไฟล์ใน `~/Downloads` เอง — mover จัดการให้แล้ว
- ห้ามกด "เติมเงิน" / "เข้าร่วมแคมเปญ" / แก้ ROAS / แก้ budget ใด ๆ บนหน้า Ads
  ถ้ามีป๊อปอัปโผล่ ให้กด X ปิดอย่างเดียว
- ตัวเลขทุกตัวมาจากไฟล์จริง ห้ามกรอกค่าสมมุติ ถ้าหาไฟล์ไม่เจอให้รายงานว่าไม่เจอ
- session expired → รายงานแล้วหยุด ห้าม login เอง

## สรุปท้ายรอบ (สั้น ๆ ภาษาไทย)

```
TikTok Ads Download — {วันที่} {รอบเช้า/เย็น}
📅 ช่วงข้อมูล: 01/{เดือน} – {วันนี้}
✅/⛔ GMV Max: {ชื่อไฟล์ หรือ เหตุผลที่ไม่ได้}
✅/⛔ Business Ads: {ชื่อไฟล์ หรือ เหตุผลที่ไม่ได้}
📊 Dashboard: {commit id หรือ "ไม่มีข้อมูลใหม่"}
หมายเหตุ: {ปัญหาที่เจอ}
```
