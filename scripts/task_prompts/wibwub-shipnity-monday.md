---
name: wibwub-shipnity-monday
description: อัปเดต Top สินค้าขายดี (Sales_Dashboard.html) จาก Excel ใน Data Shipnity ทุกวันจันทร์ 10:00 น.
---

## WIBWUB Shipnity Weekly Update — ทุกวันจันทร์ 10:00 น.

อัปเดต `Data Shipnity/Sales_Dashboard.html` ด้วยข้อมูลล่าสุดจาก Excel files ใน Data Shipnity folder
พนักงานจะ upload ไฟล์ใหม่ก่อน 10:00 น. ทุกวันจันทร์

ทำทุกอย่างใน Python/bash — ห้าม spawn subagents เด็ดขาด
**ห้าม hardcode session name — ใช้ find เท่านั้น**

---

## STEP 0 — หา paths แบบ dynamic (ทำก่อนทุกอย่าง)

```bash
ALL_MNT="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
OUTPUTS="/Users/thanasablilutanon/Library/Caches/wibwub-outputs"; mkdir -p "$OUTPUTS"
echo "ALL_MNT=$ALL_MNT"
echo "OUTPUTS=$OUTPUTS"

if [ -z "$ALL_MNT" ]; then
  echo "ERROR: All/ folder not found — Google Drive may not be mounted. Stopping."
  exit 1
fi

ls "$ALL_MNT/Data Shipnity/" 2>/dev/null | head -20
```

---

## STEP 1 — อ่าน Excel files ด้วย openpyxl

```python
import openpyxl, os, re, json, datetime, subprocess
from collections import defaultdict

# Dynamic path — ห้าม hardcode session name
ALL_MNT = "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"

OUTPUTS = "/Users/thanasablilutanon/Library/Caches/wibwub-outputs"
if not OUTPUTS: OUTPUTS = '/tmp'

if not ALL_MNT or not os.path.exists(ALL_MNT):
    print('ERROR: All/ not found — stopping.')
    exit(1)

SHIPNITY_DIR = f'{ALL_MNT}/Data Shipnity'
if not os.path.exists(SHIPNITY_DIR):
    print(f'ERROR: {SHIPNITY_DIR} not found — stopping.')
    exit(1)

xlsx_files = sorted([
    f for f in os.listdir(SHIPNITY_DIR)
    if f.endswith('.xlsx') and not f.startswith('~') and not f.startswith('.')
])
print(f'Found {len(xlsx_files)} Excel files: {xlsx_files}')

if not xlsx_files:
    print('WARNING: No xlsx files found — stopping.')
    exit(0)

lines_data = []
orders_dict = {}

for fname in xlsx_files:
    fpath = os.path.join(SHIPNITY_DIR, fname)
    try:
        wb = openpyxl.load_workbook(fpath, read_only=True, data_only=True)
        ws = wb.active
        header_read = False
        row_count = 0
        for row in ws.iter_rows(values_only=True):
            if not header_read:
                header_read = True
                continue
            try:
                sku      = str(row[0] or '').strip()
                name     = str(row[1] or '').strip()
                qty      = int(row[3] or 0)
                order_id = str(row[4] or '').strip()
                revenue  = float(row[5] or 0)
                shipping = float(row[6] or 0)
                channel  = str(row[15] or 'Shipnity').strip()
                price    = float(row[2] or 0)

                raw_date = row[12] if row[12] else row[19]
                if raw_date is None: continue
                if isinstance(raw_date, (datetime.datetime, datetime.date)):
                    d_str = raw_date.strftime('%Y-%m-%d')
                else:
                    parts = str(raw_date).strip().split(' ')[0].split('/')
                    if len(parts) == 3:
                        d_str = f'{parts[2][:4]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}'
                    else: continue

                if not sku or not order_id: continue
                lines_data.append({'d':d_str,'sku':sku,'name':name,'qty':qty,'price':round(price,2),'revenue':round(revenue,2),'shipping':round(shipping,2),'channel':channel,'order_id':order_id})
                if order_id not in orders_dict:
                    orders_dict[order_id] = {'d':d_str,'order_id':order_id,'channel':channel,'revenue':round(revenue,2),'shipping':round(shipping,2)}
                row_count += 1
            except: pass
        wb.close()
        print(f'  {fname}: {row_count} line items')
    except Exception as e:
        print(f'  ERROR reading {fname}: {e}')

if not lines_data:
    print('WARNING: No data found — aborting.')
    exit(0)

date_min = min(l['d'] for l in lines_data)
date_max = max(l['d'] for l in lines_data)
print(f'Total: {len(lines_data)} lines, {len(orders_dict)} orders, {date_min} → {date_max}')

result = {'lines':lines_data,'orders':list(orders_dict.values()),'date_min':date_min,'date_max':date_max}
with open(f'{OUTPUTS}/shipnity_results.json','w',encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, separators=(',',':'))
print('Saved shipnity_results.json')
```

---

## STEP 2 — อัปเดต Sales_Dashboard.html

```python
import re, json, os, subprocess

ALL_MNT = "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
OUTPUTS = "/Users/thanasablilutanon/Library/Caches/wibwub-outputs"
if not OUTPUTS: OUTPUTS='/tmp'

with open(f'{OUTPUTS}/shipnity_results.json',encoding='utf-8') as f: d=json.load(f)

SALES_HTML = f'{ALL_MNT}/Data Shipnity/Sales_Dashboard.html'
with open(SALES_HTML,'r',encoding='utf-8') as f: html=f.read()
original = html

raw_obj = {'date_min':d['date_min'],'date_max':d['date_max'],'lines':d['lines'],'orders':d['orders']}
raw_json = json.dumps(raw_obj, ensure_ascii=False, separators=(',',':'))
html = re.sub(r'const RAW\s*=\s*\{[\s\S]*?\};', f'const RAW = {raw_json};', html)

if html != original:
    with open(SALES_HTML,'w',encoding='utf-8') as f: f.write(html)
    print(f'✅ Sales_Dashboard.html updated — {len(d["lines"])} lines, {len(d["orders"])} orders')
    print(f'   Date range: {d["date_min"]} → {d["date_max"]}')
else:
    print('WARNING: No changes made — check RAW pattern')
```

---

## STEP 3 — CLEANUP + VERIFY

```python
import re, json, os, subprocess

ALL_MNT = "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
OUTPUTS = "/Users/thanasablilutanon/Library/Caches/wibwub-outputs"
if not OUTPUTS: OUTPUTS='/tmp'

# Verify
SALES = f'{ALL_MNT}/Data Shipnity/Sales_Dashboard.html'
with open(SALES) as f: html = f.read()
m = re.search(r'date_min[\"\':].*?([0-9]{4}-[0-9]{2}-[0-9]{2})', html)
if m: print(f'✅ Verified: date_min={m.group(1)}')
else: print('❌ Could not verify')

# Cleanup temp
for tmp in ['shipnity_results.json']:
    fp = f'{OUTPUTS}/{tmp}'
    if os.path.exists(fp): os.remove(fp); print(f'🗑️ cleaned {tmp}')
```

---

## RULES
- ห้าม spawn subagents
- **ห้าม hardcode session name — ใช้ subprocess find เสมอ**
- **ถ้า ALL_MNT ไม่พบ → หยุดทันที อย่า fallback ไป Downloads**
- ถ้าไม่พบ xlsx files ให้ log แล้วหยุด อย่า overwrite ด้วยข้อมูลว่าง
- On error: log แล้วทำต่อ ห้าม abort กลางคัน
- Date format ใน Excel: DD/MM/YYYY HH:MM → แปลงเป็น YYYY-MM-DD