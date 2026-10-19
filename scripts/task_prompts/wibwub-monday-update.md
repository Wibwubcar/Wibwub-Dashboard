---
name: wibwub-monday-update
description: ทุกวัน 09:10/20:10 — โหลด Shipnity + Affiliate แล้ว update ทุก dashboard (รันหลังสุด เพื่อรวมข้อมูลที่สดที่สุด)
---

<!-- LOCAL-OVERRIDE v1 -->
> **อ่านก่อน — ข้อนี้ทับคำสั่งที่ขัดกันในไฟล์นี้ทั้งหมด**
> ไฟล์นี้เขียนไว้ตอนรันบน Cowork cloud sandbox ตอนนี้ย้ายมารันบนเครื่อง Mac แล้ว
> - BASE / ALL_MNT = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All` · Downloads = `/Users/thanasablilutanon/Downloads` · OUTPUTS = `/Users/thanasablilutanon/Library/Caches/wibwub-outputs`
> - `git push` **ไม่ต้องทำ** และจะ**ไม่**เจอ error 403 แบบ sandbox — launchd `com.wibwub.autopush` push ให้เองทุก 2 นาที ข้ามทุกหัวข้อที่พูดถึง 403 / การสร้างหรือแก้ `push_now.command`
> - ที่ไหนเขียนว่า `mcp__workspace__bash` ให้ใช้ Bash tool ปกติแทน
> - อ่านไฟล์ในเครื่องใช้ Read/Bash ได้ตรง ๆ ไม่ต้องผ่าน connector
> - ถ้าขั้นไหนอ้าง path หรือเครื่องมือที่ไม่มีจริง: **หยุดและรายงาน ห้ามเดาทางเอง**

## WIBWUB Weekly Update — วันจันทร์

คุณคือ Claude ที่กำลังรัน automated weekly data update สำหรับ WIBWUB dashboards

### Workspace paths
- Shell base: /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/
- Data Shipnity: /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Shipnity/
- Data Affiliate: /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Affiliate/
- Downloads: /Users/thanasablilutanon/Downloads/

### ⚠️ Chrome Navigation Rule — สำคัญมาก
ห้ามใช้ `navigate` แบบ standalone เด็ดขาด — จะค้างไม่ return ทำให้ task หยุดทำงาน
ต้องใช้ `browser_batch` ทุกครั้งที่ต้องการ navigate:
```
browser_batch([
  navigate(url="...", tabId=TAB_ID),
  computer(action="wait", duration=4, tabId=TAB_ID),
  computer(action="screenshot", tabId=TAB_ID)
])
```

## 🛡️ CRITICAL PROTECTION — ทำก่อนทุก STEP

```python
import re
from datetime import date

today = date.today()
required_months = today.month
THAI_SHORT = ['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.']

for filepath in [
    '/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/WIBWUB_Dashboard.html',
    '/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/WIBWUB_Mobile.html'
]:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    m = re.search(r'const M5\s*=\s*\[(.*?)\]', html)
    if m:
        cnt = m.group(1).count('"') // 2 + m.group(1).count("'") // 2
        if cnt < required_months:
            correct = ', '.join([f'"{l}"' for l in THAI_SHORT[:required_months]])
            html = re.sub(r'const M5\s*=\s*\[.*?\]', f'const M5 = [{correct}]', html)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"🔧 FIXED M5 {cnt}→{required_months}: {filepath.split('/')[-1]}")
```

**กฎเหล็ก:** อัปเดตเฉพาะ index ของเดือนปัจจุบัน ห้ามสร้าง array ใหม่ทั้งหมด

---

### วันที่
```python
from datetime import date
today = date.today()
first_of_month = today.replace(day=1)
start_str = first_of_month.strftime('%Y-%m-%d')
end_str = today.strftime('%Y-%m-%d')
month_num = today.month
month_idx = month_num - 1
# Thai month names:
# 1=มกราคม 2=กุมภาพันธ์ 3=มีนาคม 4=เมษายน 5=พฤษภาคม 6=มิถุนายน
# 7=กรกฎาคม 8=สิงหาคม 9=กันยายน 10=ตุลาคม 11=พฤศจิกายน 12=ธันวาคม
```

---

## STEP 1: โหลดไฟล์ Shipnity ผ่าน Claude Chrome

1. ⚠️ **ต้องระบุ browser ที่ Mac เสมอ ห้ามปล่อยให้เลือกอัตโนมัติ** — ถ้ามีหลาย browser connected อาจไปรันบน PC โดยไม่ตั้งใจ:
   `select_browser(deviceId="b75a6bb0-5b78-4e44-92a8-75224f1ce4ee")` → `tabs_context_mcp(createIfEmpty=true)`
   (ถ้า deviceId นี้ไม่ connected แล้ว ให้เรียก `list_connected_browsers` ก่อน แล้วเลือกตัวที่ `osPlatform` เป็น macOS / `isLocal:true` เท่านั้น — ห้ามเลือก Windows/PC)

2. Navigate ด้วย browser_batch (ห้ามใช้ navigate standalone):
   - URL: `https://www.shipnity.com/data/c/purchase`
   - wait 4s → screenshot
   - ตรวจว่าหน้า "ประวัติ" โหลดขึ้นพร้อมตารางสินค้า (มีคอลัมน์ รหัสสินค้า / สินค้า / ราคา)

3. Set date range:
   - คลิก calendar icon ถัดจาก "วันที่สร้าง: วันที่ทั้งหมด" (มุมบนขวา)
   - เลือก "กำหนดเอง" → set start = วันที่ 1 ของเดือน, end = วันนี้ → Apply

4. ตรวจว่า filter "สินค้าในออเดอร์" ยังเลือกอยู่ (default) — ถ้าไม่ใช่ให้คลิกเลือก

5. คลิก **"ส่งออกข้อมูล"** (ปุ่มมุมขวาบน มีไอคอน download)

6. รอ 5 วินาที แล้วเช็ค Downloads:
   ```bash
   ls -lt /Users/thanasablilutanon/Downloads/*.xlsx 2>/dev/null | head -5
   ```

7. **ย้าย** (ไม่ใช่ copy) ไปที่ Data Shipnity/ — เพื่อไม่ให้ Downloads เต็ม:
   ```bash
   LATEST=$(ls -t /Users/thanasablilutanon/Downloads/*.xlsx 2>/dev/null | head -1)
   MONTH_NAME="มิถุนายน"   # เปลี่ยนตาม month_num ปัจจุบัน
   cp "$LATEST" "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Shipnity/Data_${MONTH_NAME}.xlsx"
   # rm disabled — cleanup_downloads.command จัดการแทน
   echo "Moved: Data_${MONTH_NAME}.xlsx (ลบต้นฉบับจาก Downloads แล้ว)"
   ```

---

## STEP 2: โหลดไฟล์ Affiliate ผ่าน Claude Chrome

> ⚠️ ต้องใช้ **Transaction Analysis** เท่านั้น (ไม่ใช่ Creator List)
> Transaction Analysis = ออเดอร์ที่ settle แล้ว → ตรงกับตัวเลขในหน้า TikTok Affiliate Center

1. Navigate ด้วย browser_batch (ห้ามใช้ navigate standalone):
   - URL: `https://affiliate.tiktok.com/insights/transaction-analysis?shop_region=TH&shop_id=7494549095358892612`
   - wait 4s → screenshot
   - ตรวจว่าหน้า "Transaction Analysis" / "การวิเคราะห์ธุรกรรม" โหลดขึ้น
   - ถ้ามี deprecation banner ให้ dismiss แล้วทำต่อ

2. Set date range (กำหนดเอง):
   - start = วันที่ 1 ของเดือน
   - end = วันล่าสุดที่ available (ถ้าวันนี้ greyed out ให้เลือกวันก่อนหน้า)

3. Scroll ลงหาตาราง creator list → คลิก **"ส่งออก"** เหนือตาราง

4. รอ 60-90 วินาที (export เป็น async queue)

5. คลิกปุ่ม **"บันทึกการดาวน์โหลดไฟล์"** (document icon) เพื่อเปิด reports panel

6. หาไฟล์ `Transaction_Analysis_Creator_List_...` ที่สถานะ **"ดาวน์โหลด"** → คลิก ดาวน์โหลด
   - ถ้า panel มีไฟล์ same-day พร้อมแล้ว ดาวน์โหลดได้เลย ไม่ต้อง export ใหม่

7. **ย้าย** (ไม่ใช่ copy) ไปที่ Data Affiliate/ — เพื่อไม่ให้ Downloads เต็ม:
   ```bash
   LATEST=$(ls -t /Users/thanasablilutanon/Downloads/Transaction_Analysis_Creator_List_*.xlsx 2>/dev/null | head -1)
   cp "$LATEST" "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Affiliate/"
   # rm disabled — cleanup_downloads.command จัดการแทน
   echo "Moved: $(basename $LATEST) (ลบต้นฉบับจาก Downloads แล้ว)"
   ```

**รูปแบบไฟล์:** `Transaction_Analysis_Creator_List_YYYYMMDD-YYYYMMDD_TIMESTAMP.xlsx` (12 columns)

---

## STEP 3: อัปเดต ภาพรวมธุรกิจ (Top Products จาก Shipnity)

เฉพาะไฟล์ product-level เท่านั้น (col[1] มีชื่อสินค้าจริง ไม่ใช่ numeric ID หรือว่าง)

```python
import openpyxl
from collections import defaultdict
import os

BASE = '/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Shipnity/'

def is_product_level(ws):
    for row in ws.iter_rows(min_row=2, max_row=5, values_only=True):
        if row[1] and not str(row[1]).replace('.','').isdigit():
            return True
    return False

prod_total = defaultdict(lambda: {'revenue': 0, 'qty': 0})
prod_month = defaultdict(lambda: defaultdict(lambda: {'revenue': 0, 'qty': 0}))
seen = set()

for fname in sorted(os.listdir(BASE)):
    if not fname.endswith('.xlsx'): continue
    wb = openpyxl.load_workbook(BASE+fname, read_only=True, data_only=True)
    ws = wb.active
    if not is_product_level(ws):
        wb.close()
        continue
    # หาเดือนจาก col[19]
    month = None
    for row in ws.iter_rows(min_row=2, max_row=10, values_only=True):
        if row[19]:
            d = str(row[19])
            if '/' in d:
                month = int(d.split('/')[1])
            elif '-' in d:
                month = int(d.split('-')[1])
            break
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row[4] or not row[1]: continue
        key = (str(row[4]), str(row[0]), int(row[3] or 0))
        if key in seen: continue
        seen.add(key)
        rev = (row[2] or 0) * (row[3] or 0)
        qty = int(row[3] or 0)
        prod_total[str(row[1])]['revenue'] += rev
        prod_total[str(row[1])]['qty'] += qty
        if month:
            prod_month[str(row[1])][month]['revenue'] += rev
            prod_month[str(row[1])][month]['qty'] += qty
    wb.close()

top15 = sorted(prod_total.items(), key=lambda x: x[1]['revenue'], reverse=True)[:15]
print("Top 15:", [(n, v['revenue']) for n,v in top15])
```

อัปเดต:
- `ALL_PRODUCTS` ใน `WIBWUB_Mobile.html`
- Top Products chart + table ใน `WIBWUB_Dashboard.html`

---

## STEP 4: อัปเดต Affiliate arrays

Transaction Analysis ใช้ format 12 คอลัมน์เสมอ:
- col[1] = GMV จากครีเอเตอร์
- col[2] = การคืนเงิน (returns)
- col[10] = ค่าคอมมิชชั่นโดยประมาณ

```python
import pandas as pd, os, glob

DATA_DIR = '/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Affiliate/'
# Transaction Analysis files only
files = sorted(glob.glob(DATA_DIR + 'Transaction_Analysis_Creator_List_*.xlsx'),
               key=os.path.getmtime, reverse=True)
if not files:
    raise FileNotFoundError("ไม่พบไฟล์ Transaction_Analysis_Creator_List_*.xlsx")
filepath = files[0]
print(f"Using: {os.path.basename(filepath)}")

df = pd.read_excel(filepath, header=None)
df = df.iloc[1:]

def parse_num(val):
    if val is None or str(val).strip() in ('','None','nan'): return 0.0
    return float(str(val).replace(',','').replace('฿','').strip() or 0)

# Transaction Analysis 12-column format
df['gmv_n']  = df[1].apply(parse_num)   # GMV จากครีเอเตอร์
df['ret_n']  = df[2].apply(parse_num)   # การคืนเงิน
df['comm_n'] = df[10].apply(parse_num)  # ค่าคอมมิชชั่น
df['net_n']  = df['gmv_n'] - df['ret_n']

total_gmv    = round(df['gmv_n'].sum())
total_net    = round(df['net_n'].sum())
total_comm   = round(df['comm_n'].sum())
num_creators = len(df[df['gmv_n'] > 0])
print(f"GMV={total_gmv:,}  Net={total_net:,}  Comm={total_comm:,}  Creators={num_creators}")
```

### ⚠️ ชื่อตัวแปรจริง (แก้ 2026-07-06 — ชื่อเดิม gmvD/netD/commD/crD/months/bLabels/raw ไม่มีอยู่แล้วในไฟล์จริง ทำให้ step นี้ no-op เงียบ ๆ มานาน ต้องใช้ชื่อด้านล่างเท่านั้น)

- `WIBWUB_Affiliate_Dashboard.html` → arrays จริงคือ `AF_MO` (label เดือน), `AF_GMV`, `AF_NET`, `AF_COM`, `AF_CR` — **ไม่ใช่** gmvD/netD/commD/crD/raw
- `WIBWUB_Mobile.html` → arrays จริงคือ `AFI_MONTHS` (label เดือน), `AFI_GMV`, `AFI_NET`, `AFI_COMM`

### ⚠️ Layout เป็น "rolling window" ไม่ใช่ index ตายตัว — ห้ามใช้ `month_idx = today.month - 1` ตรง ๆ กับ array พวกนี้

ตัวอย่างจริง (ก.ค. 2569): `AFI_MONTHS=['พย.68','ธค.68','มค.69','กพ.69','มีนา.69','เมษา.69','พค.69','มิย.69','กค.69']`
— index สุดท้ายของ array ไม่ได้แปลว่า index 6 = ก.ค. เสมอไป (สูตร month-1 ตรง ๆ จะทับเดือนผิด และเคยเกือบทำข้อมูลเดือน พ.ค. หายมาแล้ว)

**วิธีที่ถูกต้องทุกครั้งที่จะแก้ arrays พวกนี้:**
1. อ่าน label array ปัจจุบัน (`AF_MO` ใน Affiliate_Dashboard, `AFI_MONTHS` ใน Mobile) ก่อนเสมอ
2. หา label ของเดือนที่กำลังประมวลผลรอบนี้ (เช่น "ก.ค." / "กค.69")
3. ถ้า label นั้น **มีอยู่แล้วเป็นตัวสุดท้าย** ของ array → แก้ค่าที่ index สุดท้ายนั้น (เดือนเดิม แค่ข้อมูลใหม่กว่า/ครบกว่าเดิม)
4. ถ้า label นั้น **ยังไม่มีอยู่ใน array เลย** → **append** ค่าใหม่ต่อท้ายทุก array พร้อมกัน (label + GMV + NET + COMM/COM + CR) ห้าม insert แทรกกลางหรือ rebuild ทั้ง array ใหม่
5. ห้ามเขียนทับเดือนก่อนหน้าโดยเด็ดขาดไม่ว่ากรณีใด — ถ้าไม่แน่ใจว่า index ไหนคือเดือนปัจจุบัน ให้ **หยุดและ log** แทนที่จะเดา/คำนวณเอง
6. ถ้าข้อมูลเดือนใหม่ยังมีแค่บางวัน (ไม่ครบเดือน) ยังอัปเดต/append ได้ตามปกติ แต่ให้ log ไว้ว่าเป็นข้อมูลบางส่วน — ตัวเลขจะถูกแก้ไขให้ครบขึ้นในรอบถัดไปที่ label เดือนเดิมยังเป็นตัวสุดท้าย (ตามข้อ 3)

อัปเดต:
- `WIBWUB_Affiliate_Dashboard.html` → `AF_MO`, `AF_GMV`, `AF_NET`, `AF_COM`, `AF_CR` (ตามกฎ append/overwrite ด้านบน)
- `WIBWUB_Mobile.html` → `AFI_MONTHS`, `AFI_GMV`, `AFI_NET`, `AFI_COMM` (ตามกฎ append/overwrite ด้านบน)

---

## STEP 5: Bump sw.js + Git commit

```bash
CURRENT=$(grep -oP "wibwub-v\K[0-9]+" /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/sw.js)
NEW=$((CURRENT + 1))
sed -i "s/wibwub-v${CURRENT}/wibwub-v${NEW}/" /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/sw.js

cd /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All
rm -f .git/index.lock .git/HEAD.lock
git add WIBWUB_Mobile.html WIBWUB_Dashboard.html WIBWUB_Affiliate_Dashboard.html sw.js
git commit -m "auto-update: Monday $(date +%Y-%m-%d) — Shipnity + Affiliate + ภาพรวมธุรกิจ"
echo "✅ Committed — รอ user กด push_now.command"

# สร้าง push_now.command (sandbox push ติด proxy HTTP 403 ไม่ push เอง)
cat > "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/push_now.command" << 'EOF'
#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
EOF
chmod +x "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/push_now.command"
```

---

## หากมีข้อผิดพลาด
- Chrome ไม่ connected → log "Chrome not available" และหยุด
- Login หมดอายุ → log "Session expired — re-login required" และหยุด
- Download ไม่พบไฟล์ → retry 1 ครั้ง แล้ว log error
- navigate ค้าง → ตรวจสอบว่าใช้ browser_batch ไม่ใช่ navigate standalone

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