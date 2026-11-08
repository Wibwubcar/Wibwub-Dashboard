---
name: wibwub-download-orders-monday
description: ทุกวัน 08:35/19:35 (ชื่องานหลอก — ไม่ใช่เฉพาะวันจันทร์) — ส่วน A โหลด order Shopee/TikTok/Lazada/Line My Shop · ส่วน B ดึง Lazada · **เป็นตัวเขียน data Ads/ads_daily.json** (ads_daily_update.py) ซึ่งงานอื่นใช้ต่อ จึงต้องเสร็จก่อนรอบ sales-update 09:25
---
> ⛔ **ห้ามเรียกเครื่องมือขอสิทธิ์ลบไฟล์** (เช่น `allow_cowork_file_delete`)
> งานตั้งเวลาไม่มีคนกดอนุญาต เครื่องมือนี้จะค้างรอจนหมดรอบ — เกิดจริง 5 พ.ย. 69
> `wibwub-shopee-live-daily` เรียกเพื่อลบ `.git/HEAD.lock` ของตัวเอง แล้ว**ค้าง 81 นาที**
> (09:40 → 10:57) กินสล็อตงานพร้อมกัน 1 ใน 3 ไปเปล่า ๆ · ตอนนี้มี hook ตีกลับให้อัตโนมัติแล้ว
> ถ้าติด `.git/index.lock` หรือ `.git/HEAD.lock`: `gitw.py` รอให้แล้วสูงสุด 5 นาที
> **ห้ามลบ lock ของคนอื่น** ถ้าสุดท้ายยังไม่ผ่าน → **รายงานตรง ๆ** ว่ารอบนี้ข้อมูลเข้าไฟล์แล้ว
> แต่ยังไม่ได้ commit แล้วจบรอบ **ห้ามรอต่อ**

> 🔁 **ไฟล์นี้คือสำเนาของพรอมป์ตัวจริง** ที่ `~/Documents/Claude/Scheduled/wibwub-download-orders-monday/SKILL.md`
> (งาน local อ่านไฟล์นั้น ไม่ได้อ่านไฟล์นี้) · มีไว้ให้ git เก็บประวัติ
> **แก้ที่นี่แล้วไม่มีผล** — แก้ไฟล์ตัวจริงก่อน แล้วคัดลอกมาทับไฟล์นี้ในคอมมิตเดียวกัน


Download order export files from all 4 WIBWUB e-commerce platforms and save them to the correct folders. Complete all 4 platforms every time.

## ⚠️ Chrome Navigation Rule — สำคัญมาก
ห้ามใช้ `navigate` แบบ standalone เด็ดขาด — จะค้างไม่ return ทำให้ task หยุดทำงาน
ต้องใช้ `navigate` + `wait` ในคู่เสมอ:
```
navigate(url="...", tabId=TAB_ID)  # ผ่าน browser_batch หรือ standalone ก็ได้
computer(action="wait", duration=4, tabId=TAB_ID)
computer(action="screenshot", tabId=TAB_ID)
```

## ⚡ Session Recovery — ทำก่อนทุก platform
ถ้า page redirect ไปหน้า login ให้ทำตาม Recovery Steps ของแต่ละ platform ด้านล่างทันที อย่ายอมแพ้และ skip

## Save folder base
งานนี้รันบนเครื่อง Mac (ไม่ใช่แซนด์บ็อกซ์ Linux แล้ว) · cwd คือ `/Users/thanasablilutanon/Downloads`
พาธเต็มของโฟลเดอร์ปลายทาง — **ใช้พาธเต็มทุกคำสั่ง ห้ามใช้พาธ relative และห้ามใช้ `$BASE`**:

```
/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/data ยอดขาย plaform/
  ├── Shopee/
  ├── Tiktok/
  ├── Lazada/
  └── Line My Shop/
```

⛔ **พาธ `/sessions/<ชื่อ>/mnt/...` ในพรอมป์เก่าตายแล้ว** (แซนด์บ็อกซ์เดิม) ถ้าเจอที่ไหนอีกให้ถือว่าผิด

Use the Chrome MCP (`mcp__Claude_in_Chrome__*`) for all browser automation.
ไฟล์ที่โหลดเสร็จ **ไม่ต้อง `cp` เอง** 3 ใน 4 แพลตฟอร์ม — ดูหัวข้อ "กฎการย้ายไฟล์" ท้ายส่วน A

⚠️ **ต้องระบุ browser ที่ Mac เสมอ ห้ามปล่อยให้เลือกอัตโนมัติ** — ก่อนเริ่ม platform แรก:
`select_browser(deviceId="b75a6bb0-5b78-4e44-92a8-75224f1ce4ee")` แล้วค่อย `tabs_context_mcp(createIfEmpty=true)`
(ถ้า deviceId นี้ไม่ connected แล้ว ให้เรียก `list_connected_browsers` ก่อน แล้วเลือกตัวที่ `osPlatform` เป็น macOS / `isLocal:true` เท่านั้น — ห้ามเลือก Windows/PC)

---

## Platform 1 — Shopee
URL: https://seller.shopee.co.th/portal/sale/order

### Session Check
ถ้า page URL ยังเป็น `/sale/order` = session OK
ถ้า redirect ไปหน้าอื่น = session expired → navigate ไปที่ https://seller.shopee.co.th แล้วรอ 5 วินาที แล้ว navigate กลับ

### Steps
1. Navigate to: https://seller.shopee.co.th/portal/sale/order
2. Wait 5 seconds → screenshot
3. Click tab "ทั้งหมด" (use find tool with query "ทั้งหมด tab")
4. Click "ส่งออก" dropdown
5. Select "ส่งออกรายการสั่งซื้อ" → "ทั้งหมด"
6. Set date range: **วันที่ 1 ของเดือนปัจจุบัน → วันนี้** — ต้องตั้งค่าเองทุกครั้ง
   > **ห้ามรับช่วงวันที่ default ที่ Shopee ตั้งมาให้** แม้มันจะ "ครอบเดือนนี้อยู่แล้ว"
   > เกิดจริง 4 พ.ย. 69 รอบเช้า: รับ default มา (5 ต.ค.–4 พ.ย. = 31 วัน) Shopee จึง
   > **หั่นไฟล์เป็น `_part_1_of_3` … `_part_3_of_3` แล้วห่อเป็น .zip** ได้
   > `Order.all.order_creation_date.20261005_20261104.zip` แทนไฟล์ .xlsx เดี่ยว
   > ตัวย้ายยังพาเข้าโฟลเดอร์ให้ (กฎ `Order.all.*` ครอบทั้ง .zip) แต่คนที่เปิดไฟล์ต่อ
   > ต้องแตก zip เองและเปิด 3 ไฟล์ ไม่ใช่รูปแบบที่รอบอื่น ๆ ส่งมา
   > ถ้าได้ไฟล์ .zip มา: **ไม่ต้องโหลดใหม่** (ข้อมูลครบ) แค่รายงานว่าช่วงวันที่หลุดเป็น default
7. Click Export → wait for download
8. Click download link when ready

File: ZIP named `Order.all.YYYYMMDD_YYYYMMDD.zip`
ตัวย้ายอัตโนมัติพาเข้าโฟลเดอร์ Shopee ให้เอง (กฎ `Order.all.*`) — **ห้าม cp** แค่ตรวจว่าถึงจริง:
```bash
python3 -c "
import glob, os, time
d = glob.glob('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/data ยอดขาย plaform/Shopee/Order.all.*')
f = max(d, key=os.path.getmtime) if d else None
age = (time.time() - os.path.getmtime(f))/60 if f else None
print('ไฟล์ล่าสุด:', os.path.basename(f) if f else 'ไม่มี', '| อายุ %.0f นาที' % age if age is not None else '')
print('OK' if age is not None and age < 15 else 'ยังไม่ถึง — รอ 10 วิแล้วตรวจอีกครั้ง')
"
```
ถ้ายังไม่ถึงหลังตรวจซ้ำ 2 ครั้ง ให้ cp เองจาก `/Users/thanasablilutanon/Downloads` (ตัวย้ายอาจไม่ทำงาน) แล้วรายงานว่าต้อง cp เอง

---

## Platform 2 — TikTok Shop
URL: https://seller-th.tiktok.com/order/list?tab=all

### Session Check + Recovery
1. Navigate to URL, wait 5s, take screenshot
2. Check page text with get_page_text:
   - ถ้ามี "จัดการคำสั่งซื้อ" หรือ "WIBWUBCAR" = session OK
   - ถ้ามี "เข้าสู่ระบบ" หรือ "login" = session expired

### Recovery Steps (ถ้า session หมด)
Navigate to https://seller-th.tiktok.com/ แล้วรอ 10 วินาที — ถ้า TikTok Shop ใช้ cookie เดียวกับ TikTok Ads ที่ login อยู่ จะ auto-login
ถ้าไม่ได้ → navigate ไปที่ https://seller-th.tiktok.com/ → find "เข้าสู่ระบบ" button → คลิก → รอ

### Steps (หลัง session OK)
1. Click เมนูซ้าย "จัดการคำสั่งซื้อ" ถ้าไม่เห็นรายการ
2. Click tab "ทั้งหมด" 
3. Click "ดาวน์โหลด" button (top-right area, ไม่ใช่ "ส่งออก"):
   ```javascript
   // หา ดาวน์โหลด button
   const btn = Array.from(document.querySelectorAll('button'))
     .find(b => (b.textContent||'').trim().includes('ดาวน์โหลด') && 
                 b.getBoundingClientRect().top > 0);
   if (btn) btn.click();
   ```
4. Dialog เปิด → เลือก "คำสั่งซื้อที่กรอง" → เลือก Excel
5. Click "ส่งออก" ใน dialog
6. รอ progress circle เปลี่ยนเป็น "ดาวน์โหลด" (สีแดง) ใน Export History
7. Click "ดาวน์โหลด" button ใน history row

File: `ทั้งหมด คำสั่งซื้อ-YYYY-MM-DD-HH_MM.xlsx`
ตัวย้ายอัตโนมัติพาเข้าโฟลเดอร์ Tiktok ให้เอง (กฎ `*คำสั่งซื้อ*.xlsx`) — **ห้าม cp** แค่ตรวจ:
```bash
python3 -c "
import glob, os, time
d = glob.glob('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/data ยอดขาย plaform/Tiktok/*คำสั่งซื้อ*.xlsx')
f = max(d, key=os.path.getmtime) if d else None
age = (time.time() - os.path.getmtime(f))/60 if f else None
print('ไฟล์ล่าสุด:', os.path.basename(f) if f else 'ไม่มี')
print('OK' if age is not None and age < 15 else 'ยังไม่ถึง')
"
```

---

## Platform 3 — Lazada
URL: https://sellercenter.lazada.co.th/apps/order/list?status=all

Lazada uses queue-based export — trigger, then do Line My Shop, then come back.

### Session Check + Recovery
1. Navigate to URL, wait 5s
2. Check URL after navigation:
   - ถ้า URL เป็น `/apps/order/list` = session OK
   - ถ้า redirect ไป `/apps/seller/login` = session expired → Recovery

### Recovery Steps (ถ้า session หมด)
```javascript
// ตรวจ URL ปัจจุบัน
window.location.href
```
ถ้าเป็น login page → หา "เข้าสู่ระบบ" button (credentials อยู่ใน browser แล้ว):
```javascript
// Click เข้าสู่ระบบ — browser จะ autofill user/pass
const loginBtn = Array.from(document.querySelectorAll('button'))
  .find(b => b.type === 'submit' || b.textContent.trim() === 'เข้าสู่ระบบ');
if (loginBtn) loginBtn.click();
```
Wait 5s → navigate กลับไปที่ order list URL

### Steps (หลัง session OK)
1. Export (JS):
```javascript
// Step 1: Open dropdown
const exportBtn = Array.from(document.querySelectorAll('button'))
  .find(b => b.textContent.trim() === 'ส่งออก');
exportBtn.click();
```
```javascript
// Step 2: Click Export All
const exportAll = Array.from(document.querySelectorAll('li, a, div, span, button'))
  .find(el => el.textContent.trim() === 'Export All' && el.offsetParent !== null);
exportAll.click();
```
2. Confirm dialog: find "ยืนยัน" button → click
3. **Do NOT wait** — proceed to Line My Shop immediately

### Come back after Line My Shop — check Export History:
```javascript
// Click Export → Export History
const exportBtn = Array.from(document.querySelectorAll('button'))
  .find(b => b.textContent.trim() === 'ส่งออก');
exportBtn.click();
// Then click Export History in dropdown
const hist = Array.from(document.querySelectorAll('li,a,div,span'))
  .find(el => el.textContent.trim() === 'Export History' && el.offsetParent);
if (hist) hist.click();
```
```javascript
// Get download links
const links = Array.from(document.querySelectorAll('a'))
  .filter(a => a.textContent.trim() === 'Download Result File');
links.map(a => a.href) // index 0 = newest
```
Navigate directly to the CDN URL: `https://sg-test-11.slatic.net/other/batch/[HASH].xlsx`

File: ชื่อเป็น hash 32 ตัว เช่น `d46d670c5df0a375877f08a63e3726af.xlsx`

⚠️ **แพลตฟอร์มเดียวที่ต้อง cp เอง** — ตัวย้ายอัตโนมัติรู้จักแค่ชื่อ `Lazada_Orders_*.xlsx`
ไฟล์ชื่อ hash จึงค้างใน Downloads ตลอด

> **เกิดจริง 1–2 พ.ย. 69 — ไฟล์รอบเช้าหายเพราะรอบเย็นเขียนทับ ไม่ใช่รอบเช้าพลาด**
> ตรวจ audit ของรอบจริงแล้ว: 1 พ.ย. รอบเช้า **คัดลอกสำเร็จ** (9,053,348B เวลา 08:48)
> แต่รอบเย็น 19:47 รัน `cp … Lazada_Orders_20261101.xlsx` **ชื่อเดิมซ้ำ** ไฟล์เช้าจึงถูกทับ
> (2 พ.ย. เหมือนกันเป๊ะ) วันที่เห็นครบทั้งสองรอบ เช่น 30–31 ต.ค. คือวันที่ลงท้าย `_1948`/`_2221`
> **บรรทัด `if os.path.exists(out)` ข้างล่างคือตัวกันเรื่องนี้ ห้ามตัดออก และห้ามกลับไปใช้ `cp` เปล่า ๆ**
> ข้อมูลไม่หาย (ไฟล์เป็นยอดสะสม รอบเย็นครอบรอบเช้า 100%) แต่สแนปช็อตรอบเช้าหาย
เลือกไฟล์ด้วย**แพทเทิร์น hash + อายุไฟล์** ห้ามใช้ `ls -t *.xlsx | grep -v` แบบเดิม — มันคว้าไฟล์อะไรก็ได้ที่เพิ่งโหลด:
```bash
python3 -c "
import glob, os, re, shutil, time
from datetime import datetime
DL  = '/Users/thanasablilutanon/Downloads'
DST = '/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/data ยอดขาย plaform/Lazada'
pat = re.compile(r'^[0-9a-f]{32}( \(\d+\))?\.xlsx$')
c = [f for f in glob.glob(DL + '/*.xlsx')
     if pat.match(os.path.basename(f)) and (time.time() - os.path.getmtime(f)) < 1800]
if not c:
    print('⛔ ไม่พบไฟล์ Lazada ชื่อ hash ที่โหลดใน 30 นาทีล่าสุด — อย่าคัดลอกไฟล์อื่นมาแทน')
    raise SystemExit(1)
src = max(c, key=os.path.getmtime)
out = os.path.join(DST, 'Lazada_Orders_%s.xlsx' % datetime.now().strftime('%Y%m%d'))
if os.path.exists(out):
    out = out[:-5] + '_' + datetime.now().strftime('%H%M') + '.xlsx'
shutil.copy2(src, out)
print('✅ Lazada:', os.path.basename(src), '->', os.path.basename(out),
      '| %.1f MB' % (os.path.getsize(out)/1e6))
"
```
ไฟล์ hash ต้นฉบับยังค้างใน Downloads ได้ ไม่ต้องลบ (ตัวย้ายจะเก็บให้ภายหลัง)

---

## Platform 4 — Line My Shop
URL: https://oaplus.line.biz/channels/5000113570/e-commerce/report

Channel ID = 5000113570 (also the file password)

### ⚡ สำคัญ: Domain นี้ใช้งานได้ใน Claude Chrome ถ้า session ยังอยู่
### Session Check + Recovery
1. Navigate to https://oaplus.line.biz/channels/5000113570/e-commerce/report
2. Wait 5s → screenshot
3. Check page title/content:
   - ถ้ามี "รายงาน" หรือ "WIBWUB.CAR" = session OK ✅
   - ถ้า redirect ไป `access.line.me` = session expired → Recovery

### Recovery Steps (ถ้า session หมด)
Tab 1415001339 (LINE Login tab) มักจะเปิดอยู่แล้วในกลุ่ม Claude Chrome
Navigate tab นั้นไปที่ https://access.line.me → รอ user login (หรือถ้ามี auto-login จะเข้าเองเลย)
แล้ว navigate tab ใหม่ไปที่ https://oaplus.line.biz/channels/5000113570/e-commerce/report

หรือสร้าง tab ใหม่:
```python
# tabs_create_mcp() แล้ว navigate ไปที่ URL
```
ถ้า session ยังไม่กลับมา → แจ้ง user ว่าต้อง login LINE ใน Claude Chrome tab แล้วรัน schedule ใหม่

### Steps (หลัง session OK)
1. คำนวณวันที่:
```python
from datetime import datetime, timedelta
today = datetime.now()
start = today - timedelta(days=87)  # 87 วัน = ไม่เกิน 90
start_str = start.strftime("%d/%m/%Y")
# เช่น "05/04/2026"
```

2. Click start date field (find tool: "วันที่เริ่ม" หรือ triple_click ที่ field แรก)
3. พิมพ์ start date ใหม่ (เช่น "05/04/2026") → Enter
4. Calendar จะเปิด → navigate ไปเดือนที่ถูกต้อง (กดลูกศรซ้าย) แล้วคลิกวันที่
5. Find "ดาวน์โหลด" button → click (ref-based)
6. ถ้ามี confirmation dialog (>30 วัน) → find "ดาวน์โหลด" blue button → click

File: `Order Report YYYYMMDD.xlsx` (password-encrypted, password = 5000113570)
ตัวย้ายอัตโนมัติพาเข้าโฟลเดอร์ Line My Shop ให้เอง (กฎ `Order Report *.xlsx`) — **ห้าม cp** แค่ตรวจ:
```bash
python3 -c "
import glob, os, time
d = glob.glob('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/data ยอดขาย plaform/Line My Shop/Order Report *.xlsx')
f = max(d, key=os.path.getmtime) if d else None
age = (time.time() - os.path.getmtime(f))/60 if f else None
print('ไฟล์ล่าสุด:', os.path.basename(f) if f else 'ไม่มี')
print('OK' if age is not None and age < 15 else 'ยังไม่ถึง')
"
```
(ชื่อ `LineMyShop_Orders_*.xlsx` ในโฟลเดอร์เป็นของเก่าสมัยยัง cp เอง ไม่ต้องสร้างใหม่)

---

## Summary Table
| Platform | URL | Format | Recovery |
|---|---|---|---|
| Shopee | seller.shopee.co.th | ZIP | Auto via cookies |
| TikTok | seller-th.tiktok.com | .xlsx | Navigate homepage |
| Lazada | sellercenter.lazada.co.th | .xlsx | Click login btn (browser autofill) |
| Line My Shop | oaplus.line.biz | .xlsx encrypted (pw=5000113570) | Needs manual LINE login if expired |

## Completion Report
After all platforms done:
- ✅ Shopee: [filename] (covers YYYY/MM/DD–DD)
- ✅ TikTok: [filename]
- ✅ Lazada: [filename]
- ✅ Line My Shop: [filename]
- ⛔ [platform]: session expired — [action taken]


## ⚠️ กฎการย้ายไฟล์จาก Downloads (สำคัญมาก)

**ตัวย้ายอัตโนมัติเป็นเจ้าของการจัดไฟล์ ไม่ใช่พรอมป์นี้** — LaunchAgent `com.wibwub.download-mover`
เฝ้า `~/Downloads` อยู่ตลอด พอไฟล์โหลดเสร็จจะ **ย้าย** เข้าโฟลเดอร์งานเองภายใน ~5 วินาที

| แพลตฟอร์ม | กฎในตัวย้าย | ต้อง cp เองไหม |
|---|---|---|
| Shopee | `Order.all.*` | ❌ ไม่ต้อง — ตรวจปลายทางพอ |
| TikTok | `*คำสั่งซื้อ*.xlsx` | ❌ ไม่ต้อง |
| Line My Shop | `Order Report *.xlsx` | ❌ ไม่ต้อง |
| **Lazada** | ไม่มีกฎ (ชื่อเป็น hash) | ✅ **ต้อง cp + เปลี่ยนชื่อเอง** |

⛔ **ห้าม `cp` ไฟล์ที่ตัวย้ายดูแลอยู่** — ตัวย้ายยิงภายใน 5 วิ `cp` ในพรอมป์จะแพ้เกือบทุกครั้ง
แล้วรายงานว่า "ไม่พบไฟล์" ทั้งที่โหลดสำเร็จ · ให้ตรวจที่**โฟลเดอร์ปลายทาง** ไม่ใช่ที่ Downloads
`mv`/`rm` ใน Downloads เป็นหน้าที่ของตัวย้าย พรอมป์นี้ไม่ต้องลบอะไรเลย

**Script ที่เกี่ยวข้อง (อยู่ใน All/scripts/):**
- `wibwub_auto_move.sh` — script ย้ายไฟล์ (ถูกเรียกโดย LaunchAgent)
- `com.wibwub.download-mover.plist` — LaunchAgent config (WatchPaths ~/Downloads)
---
---

# 🔁 งานนี้มี 3 ส่วน — เพิ่ม B และ C เมื่อ 24 ต.ค. 2569

ทุกอย่างข้างบนทั้งหมดคือ **ส่วน A (โหลด order 4 แพลตฟอร์ม)** ทำให้ครบเหมือนเดิมทุกประการ ห้ามข้าม
เสร็จแล้ว **ทำส่วน B ต่อ แล้วทำส่วน C** ตามลำดับนี้เท่านั้น (C กินผลของ B)

**ส่วนไหนล้มก็ทำส่วนถัดไปต่อ** อย่าหยุดทั้งงาน และ **รายงานแยกเป็น 3 หัวข้อเสมอ**

เหตุผลที่ย้ายมารวมที่นี่: ฝั่ง code เปิดเว็บในรอบตั้งเวลาไม่ได้ตั้งแต่เวอร์ชัน 2.1.308 (22 ต.ค. 69 20:32)
งานนี้เป็นงาน local ที่มีสิทธิ์โดเมนครบที่สุด (19 โดเมน) จึงยกงาน Ads มาไว้ด้วยกัน

## ขั้น 0 ร่วม — ยืนยันว่าโฟลเดอร์ All อยู่ที่เดิม

**ทุกคำสั่ง shell ของรอบต้องเป็น `python3` ไม่ใช่แค่คำสั่งแรก · ห้ามเป็นลูป `for` ของ bash**
รวมคำสั่งชั่วคราวที่คิดขึ้นเองตอนไล่หาสาเหตุกลางรอบด้วย (เกิดจริง 7 พ.ย. 69 รอบ 20:25
ของ `wibwub-tiktok-content`: 12 คำสั่งแรกผ่านหมด แล้วไปค้าง 48 นาทีที่คำสั่งที่ 13
ซึ่งขึ้นต้นด้วย `cd <สแครชแพด> &&` — ดูหัวข้อ "กฎคำสั่ง shell" ท้ายไฟล์) (ลูปทำให้รอบค้างจนหมดเวลา)
> ⛔ **ห้ามเช็ค BASE ด้วย `os.path.isdir` / `os.path.isfile` / `[ -d ... ]`**
> เกิดจริง 3–4 พ.ย. 69 กับ `wibwub-daily-stock`: stat ตอบ **False** 5 รอบติด
> ทั้งที่ `Grep`/`cat`/`python3 "<BASE>/scripts/..."` อ่านและรันไฟล์ในพาธเดียวกันได้ปกติ
> แปลว่า stat บนโฟลเดอร์ Google Drive เชื่อไม่ได้ (ไม่ใช่ว่า BASE หาย) — **ให้ลองเปิดไฟล์จริง**
> พาธสำรอง `/sessions/<ชื่อ>/mnt/All` **ยังไม่ตาย** และเป็นโฟลเดอร์เดียวกับ Drive จริง เขียนได้
> (ยืนยันด้วย commit `0fab409`) · ชื่อ `<ชื่อ>` เปลี่ยนทุกเซสชัน ห้ามฝังตายตัว ให้ใช้ glob หาเอง

```bash
python3 -c "
import glob
for B in ['/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All'] + sorted(glob.glob('/sessions/*/mnt/All')):
    try:
        open(B + '/sw.js').read(1)
        print('BASE OK', B)
        break
    except OSError as e:
        print('ไม่ได้', B, type(e).__name__)
else:
    print('⛔ ไม่พบ BASE')
"
```
- `BASE OK <พาธ>` → ใช้**พาธที่พิมพ์ออกมาตัวนั้น**เป็น `BASE` ในทุกคำสั่งถัดไป
- `⛔ ไม่พบ BASE` (เปิดไฟล์ไม่ได้ทุกพาธ) → หยุดส่วน B และ C แล้วรายงาน **ห้ามเดาพาธ ห้ามไปหาที่อื่น**

---

# ส่วน B — ดึง Lazada ล่วงหน้า (เก็บไว้ให้ส่วน C)

อ่านไฟล์นี้ด้วย Read tool แล้วทำตามทุกขั้นตอน:

`/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/task_prompts/wibwub-lazada-collect.md`

- โดเมน `sellercenter.lazada.co.th` อยู่ในรายการอนุญาตของงานนี้แล้ว ใช้ได้เลย
- ผลลัพธ์ต้องได้ `scripts/ads/work/lz_real.json` และ `work/lz_ads.json`
- **ห้ามกรอกรหัสผ่าน และห้ามกดปุ่มเข้าสู่ระบบ Lazada** แม้ช่องจะถูกกรอกไว้ให้แล้วก็ตาม
  ถ้าเจอหน้า login: หยุดส่วน B รายงาน แล้วไปทำส่วน C ต่อ (ส่วน C ทำงานได้โดยไม่มี Lazada)
- ป๊อปอัปบนหน้า Ads ให้กด X หรือ Escape ปิดเท่านั้น **ห้ามกด "เข้าร่วมเลย" / "เติมยอด" / เปลี่ยน ROAS**

---

# ส่วน C — Ads รายวัน (ยอดขายจริง vs ยอดจาก Ads)

อ่านไฟล์นี้ด้วย Read tool แล้วทำตามทุกขั้นตอน:

`/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/task_prompts/ads_daily.md`

### โดเมนที่ต้องใช้
| โดเมน | สถานะ |
|---|---|
| seller.shopee.co.th | ✅ มีแล้ว |
| seller-th.tiktok.com | ✅ มีแล้ว |
| sellercenter.lazada.co.th | ✅ มีแล้ว |
| **ads.tiktok.com** | ⚠️ ต้องกด "อนุญาตเสมอ" รอบแรก |

ถ้า `ads.tiktok.com` ถูกปฏิเสธ: ดึง `tk_ads` / `tk_camp` ไม่ได้ ให้รายงานตรง ๆ ว่าขาดสิทธิ์โดเมนนี้
**ห้ามวนลองซ้ำ** ลองครั้งเดียวพอ แล้วทำขั้นที่เหลือเท่าที่ทำได้

### ข้อควรระวังที่เคยพลาดมาแล้ว
- Lazada: ถ้าส่วน B สำเร็จ ไฟล์ `work/lz_*.json` จะสดใหม่ในรอบเดียวกัน **ใช้ได้เลย ไม่ต้องเปิด Lazada ซ้ำ**
  ถ้าส่วน B ล้ม ให้ตัด 2 ไฟล์ท้ายออกจากคำสั่ง merge แล้วรายงานว่า Lazada ไม่ได้อัปเดตรอบนี้
- Shopee ปิดยอดยืนยันช้า — ถ้าเจอ `code 60001 data isn't ready` แปลว่าวันนั้นยังไม่พร้อม **ไม่ใช่ error ของเรา**
  ให้รายงานว่าดึงได้ถึงวันไหน (รอบเช้า 08:20 ปกติพร้อมแล้ว)
- หน้า `ads.tiktok.com` เขียนทับ `window.fetch` ตอน bootstrap — วาง hook.js ครั้งเดียวแล้วรอหน้าโหลดจบ
  ถ้า `window.__cap` ยังว่าง ให้เช็ค `String(window.fetch).includes('__cap')` ว่าเป็น true ก่อน
- **ข้ามขั้น 8 ในไฟล์พรอมป์ (เมนู "การตลาด vs ยอดขาย") — ย้ายไปฝั่ง code แล้วเมื่อ 24 ต.ค. 69**
  ห้ามรัน `kol_fetch.py` และ `marketing_update.py` ในงานนี้ ให้จบที่ขั้น 7 (commit ไฟล์ Ads) พอ
  เหตุผล: `kol_fetch.py` ต้องใช้ไฟล์กุญแจ service account ที่ `~/wibwub-service-account.json`
  ซึ่งแซนด์บ็อกซ์ของงาน local มองไม่เห็น (รอบ 24 ต.ค. 08:50 จึงได้ exit 2) และกุญแจย้ายเข้า
  โฟลเดอร์ All ไม่ได้เพราะเป็น Google Drive ที่แชร์อยู่ · ขั้นนี้ไม่ต้องใช้เบราว์เซอร์
  จึงให้งานฝั่ง code `wibwub-ads-daily` รันแทนเวลา 09:15/20:15 ซึ่งอยู่หลังงานนี้จบพอดี
  ให้รายงานในหัวข้อ C ว่า "ขั้น 8 ข้ามโดยตั้งใจ — ฝั่ง code ทำต่อ 09:15/20:15"

---

# ⛔ บรรทัดแรกของรายงาน — ถ้า login หลุด ต้องบอกทันที (เพิ่ม 27 ต.ค. 69)

ถ้ารอบนี้มีโดเมนไหน **เด้งไปหน้าเข้าสู่ระบบ** ให้ขึ้นต้นรายงาน **บรรทัดแรกสุด** ด้วย

```
⛔ ต้อง login ใหม่: <โดเมน>[, <โดเมน>...]
```

ก่อนหัวข้อ A/B/C ทั้งหมด หลายโดเมนให้ใส่ในบรรทัดเดียวคั่นด้วยคอมมา
ยังทำส่วนที่เหลือให้ครบเหมือนเดิม แล้วค่อยรายงาน A/B/C ตามรูปแบบข้างล่าง

เหตุผล: 27 ต.ค. 69 รอบ 08:35 มี `seller-th.tiktok.com` + `sellercenter.lazada.co.th`
+ `oaplus.line.biz` หมดอายุพร้อมกัน รายงานเขียน ⛔ ไว้กลางหัวข้อ A/B/C ถูกต้องแล้ว
แต่กว่าจะเห็นก็ตอนบ่าย ทำให้ `tk_real` ของวันที่ 26 หายทั้งวัน และ `TK_PROD_DATA` ค้างตามไปด้วย
**cookie ของ 3 โดเมนนี้หมดอายุพร้อมกันได้ ให้ถือว่าเป็นเรื่องปกติที่ต้องรายงานให้เด่น ไม่ใช่เรื่องผิดปกติที่ต้องซ่อน**
ห้ามกรอกรหัสผ่านหรือกดปุ่มเข้าสู่ระบบเองทุกกรณี — รายงานอย่างเดียว

---

# รูปแบบรายงานท้ายรอบ (ภาษาไทย แยก 3 หัวข้อ)

```
## A — โหลด order
<สำเร็จ/ล้มเหลว> · Shopee / TikTok / Lazada / Line My Shop อันไหนได้อันไหนไม่ได้

## B — ดึง Lazada ล่วงหน้า
<สำเร็จ/ล้มเหลว> · ช่วงวันที่ · ไฟล์ work/lz_real.json + lz_ads.json

## C — Ads รายวัน
<สำเร็จ/ล้มเหลว> · ช่วงที่ดึง · วันที่เพิ่ม/เปลี่ยน · ยอดเดือนนี้ 3 แพลตฟอร์ม
· แคมเปญ GMV Max · commit id · "ขั้น 8 ข้ามโดยตั้งใจ — ฝั่ง code ทำต่อ 09:15/20:15"
```

**ห้ามเขียน ✅ หรือคำว่าสำเร็จ ถ้าส่วนใดส่วนหนึ่งไม่ผ่าน** ให้ขึ้นต้นส่วนนั้นด้วย `❌ ล้มเหลว — <สาเหตุ>`
