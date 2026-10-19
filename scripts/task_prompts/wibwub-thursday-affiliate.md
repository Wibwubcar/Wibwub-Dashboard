---
name: wibwub-thursday-affiliate
description: ทุกวัน 08:50/19:50 — โหลด 4 ไฟล์ TikTok Affiliate (ครีเอเตอร์/สินค้า/วีดีโอ/ไลฟ์สตรีม) → ย้ายไปโฟล์เดอร์ → อัปเดต Dashboard
---

## WIBWUB Affiliate Auto-Update — ดาวน์โหลด 4 ไฟล์ + อัปเดต Dashboard

ดาวน์โหลด 4 ไฟล์ export จาก TikTok Affiliate Center แล้วย้ายไปโฟลเดอร์ที่ถูก จากนั้นอัปเดต dashboards ทั้งหมด

### Paths
- Shell base: /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/
- Data Affiliate root: /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Affiliate/
- Subfolders:
  - ครีเอเตอร์: /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Affiliate/ครีเอเตอร์/
  - สินค้า:     /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Affiliate/สินค้า/
  - วีดีโอ:     /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Affiliate/วีดีโอ/
  - ไลฟ์สตรีม:  /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Affiliate/ไลฟ์สตรีม/
- Downloads: /Users/thanasablilutanon/Downloads/

### วันที่
```python
from datetime import date
today = date.today()
first_of_month = today.replace(day=1)
month_num = today.month
month_idx = month_num - 1  # 0=Jan ... 5=Jun  — ⚠️ ใช้ได้เฉพาะ arrays ปกติเท่านั้น ห้ามใช้กับ AF_*/AFI_* (ดูคำเตือนใน STEP 4)
```

### ⚠️ Chrome Navigation Rule — สำคัญมาก
ห้ามใช้ `navigate` แบบ standalone เด็ดขาด — จะค้างไม่ return
ต้องใช้ `browser_batch` เสมอ:
```
browser_batch([
  navigate(url="...", tabId=TAB_ID),
  computer(action="wait", duration=4, tabId=TAB_ID),
  computer(action="screenshot", tabId=TAB_ID)
])
```

---

## STEP 1 — เปิดหน้าและตั้ง Date Range

1. ⚠️ **ต้องระบุ browser ที่ Mac เสมอ ห้ามปล่อยให้เลือกอัตโนมัติ** — ถ้ามีหลาย browser connected อาจไปรันบน PC โดยไม่ตั้งใจ:
   `select_browser(deviceId="b75a6bb0-5b78-4e44-92a8-75224f1ce4ee")` → `tabs_context_mcp(createIfEmpty=true)`
   (ถ้า deviceId นี้ไม่ connected แล้ว ให้เรียก `list_connected_browsers` ก่อน แล้วเลือกตัวที่ `osPlatform` เป็น macOS / `isLocal:true` เท่านั้น — ห้ามเลือก Windows/PC)

2. Navigate ด้วย browser_batch:
   - URL: `https://affiliate.tiktok.com/insights/transaction-analysis?shop_region=TH&shop_id=7494549095358892612`
   - wait 5s → screenshot ยืนยันหน้า "การวิเคราะห์ธุรกรรม" / "Transaction Analysis" โหลดแล้ว

3. Set date range เดือนปัจจุบัน:
   - คลิก date field → เลือก "กำหนดเอง"
   - Start = วันที่ 1 ของเดือน, End = วันล่าสุดที่ available (ถ้าวันนี้ greyed out → วันก่อน)
   - บันทึก end_date จริงที่ระบบยอมรับ

---

## STEP 2 — Export และดาวน์โหลด 4 ไฟล์ทีละ Tab

ทำซ้ำ 4 รอบ — แต่ละ tab มีปุ่ม "ส่งออก" ของตัวเอง
Export เป็น async queue: trigger → รอ → download จาก reports panel

### Tab 1: ครีเอเตอร์
1. ตรวจว่าอยู่ที่ tab **ครีเอเตอร์** (default) — ถ้าไม่ใช่ให้คลิก
2. Scroll หาปุ่ม **"ส่งออก"** เหนือตาราง → คลิก
3. รอ 60-90 วินาที
4. คลิกปุ่ม **"บันทึกการดาวน์โหลดไฟล์"** (document icon) → reports panel
5. หาไฟล์ล่าสุดที่สถานะ **"ดาวน์โหลด"** → คลิก ดาวน์โหลด
   - ถ้ายัง **"กำลังส่งออก"** → รออีก 30s แล้ว refresh panel

### Tab 2: สินค้า
6. คลิก tab **"สินค้า"** → รอ 3s → screenshot
7. ปุ่ม "ส่งออก" → คลิก → รอ 60-90s → download จาก reports panel

### Tab 3: วีดีโอ
8. คลิก tab **"วีดีโอ"** → รอ 3s → screenshot
9. ปุ่ม "ส่งออก" → คลิก → รอ 60-90s → download จาก reports panel

### Tab 4: ไลฟ์สตรีม
10. คลิก tab **"ไลฟ์สตรีม"** → รอ 3s → screenshot
11. ปุ่ม "ส่งออก" → คลิก → รอ 60-90s → download จาก reports panel

> ถ้า panel มีไฟล์ same-day ที่พร้อมอยู่แล้ว → ดาวน์โหลดได้เลย ไม่ต้อง export ใหม่

---

## STEP 3 — ย้ายไฟล์ไปโฟลเดอร์ที่ถูกต้อง (ย้าย ไม่ใช่ copy)

```bash
# ตรวจ Downloads ก่อน
ls -lt /Users/thanasablilutanon/Downloads/*.xlsx 2>/dev/null | head -10

# ฟังก์ชั่น move_latest: หาไฟล์ใหม่สุดใน Downloads ที่ match pattern แล้วย้ายไป target folder
# ไฟล์ที่โหลดมาชื่อต่างกันตาม tab ที่ส่งออก — ตรวจ timestamp เพื่อแยกแต่ละไฟล์

# Tab ครีเอเตอร์ (Transaction_Analysis_Creator_List_*)
CREATOR_FILE=$(ls -t /Users/thanasablilutanon/Downloads/Transaction_Analysis_Creator_List_*.xlsx 2>/dev/null | head -1)
if [ -n "$CREATOR_FILE" ]; then
  cp "$CREATOR_FILE" "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Affiliate/ครีเอเตอร์/"
  echo "✅ ครีเอเตอร์: $(basename $CREATOR_FILE) → Data Affiliate/ครีเอเตอร์/"
fi

# Tab สินค้า (Transaction_Analysis_Product_List_* หรือชื่อคล้ายกัน)
PRODUCT_FILE=$(ls -t /Users/thanasablilutanon/Downloads/*.xlsx 2>/dev/null | head -1)
if [ -n "$PRODUCT_FILE" ] && [ "$PRODUCT_FILE" != "$CREATOR_FILE" ]; then
  cp "$PRODUCT_FILE" "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Affiliate/สินค้า/"
  echo "✅ สินค้า: $(basename $PRODUCT_FILE) → Data Affiliate/สินค้า/"
fi
```

**⚠️ หมายเหตุ:** ชื่อไฟล์ขึ้นอยู่กับ TikTok — ตรวจด้วย `ls -lt Downloads/*.xlsx` ก่อนย้าย
แล้วจับคู่ตาม timestamp (ไฟล์ใหม่สุด = tab ล่าสุดที่ download) ย้ายตามลำดับที่โหลด:
1. ไฟล์ที่โหลดจาก Tab ครีเอเตอร์ → `Data Affiliate/ครีเอเตอร์/`
2. ไฟล์ที่โหลดจาก Tab สินค้า → `Data Affiliate/สินค้า/`
3. ไฟล์ที่โหลดจาก Tab วีดีโอ → `Data Affiliate/วีดีโอ/`
4. ไฟล์ที่โหลดจาก Tab ไลฟ์สตรีม → `Data Affiliate/ไลฟ์สตรีม/`

ใช้ `mv` (move) เสมอ — ห้ามใช้ `cp` (copy)

---

## STEP 4 — Process ไฟล์ ครีเอเตอร์ → อัปเดต Affiliate arrays

```python
import pandas as pd, os, glob

CREATOR_DIR = '/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Affiliate/ครีเอเตอร์/'
files = sorted(glob.glob(CREATOR_DIR + '*.xlsx'), key=os.path.getmtime, reverse=True)
filepath = files[0]
print(f"Using: {os.path.basename(filepath)}")

df = pd.read_excel(filepath, header=None)
df = df.iloc[1:]  # skip header row

def parse_num(val):
    if val is None or str(val).strip() in ('','None','nan'): return 0.0
    return float(str(val).replace(',','').replace('฿','').strip() or 0)

# Transaction Analysis ครีเอเตอร์ format:
# col[0]=creator, col[1]=GMV, col[2]=returns, col[3]=orders, col[10]=commission
df['gmv_n']  = df[1].apply(parse_num)
df['ret_n']  = df[2].apply(parse_num)
df['comm_n'] = df[10].apply(parse_num)
df['net_n']  = df['gmv_n'] - df['ret_n']

total_gmv    = round(df['gmv_n'].sum())
total_net    = round(df['net_n'].sum())
total_comm   = round(df['comm_n'].sum())
num_creators = len(df[df['gmv_n'] > 0])
print(f"GMV={total_gmv:,}  Net={total_net:,}  Comm={total_comm:,}  Creators={num_creators}")
```

### ⚠️ ชื่อตัวแปรจริง (แก้ 2026-07-06 — ชื่อเดิม gmvD/netD/commD/crD ไม่มีอยู่จริงในไฟล์ ทำให้ step นี้ no-op เงียบ ๆ มานาน)

- `WIBWUB_Affiliate_Dashboard.html` → arrays จริงคือ `AF_MO` (label เดือน), `AF_GMV`, `AF_NET`, `AF_COM`, `AF_CR` — **ไม่ใช่** gmvD/netD/commD/crD
- `WIBWUB_Mobile.html` → arrays จริงคือ `AFI_MONTHS` (label เดือน), `AFI_GMV`, `AFI_NET`, `AFI_COMM`

### ⚠️ Layout เป็น "rolling window" ไม่ใช่ index ตายตัว — ห้ามใช้ `month_idx = today.month - 1` กับ arrays พวกนี้

ตัวอย่างจริง (ก.ค. 2569): `AFI_MONTHS=['พย.68','ธค.68','มค.69','กพ.69','มีนา.69','เมษา.69','พค.69','มิย.69','กค.69']`
— index สุดท้ายไม่ได้แปลว่า index 6 = ก.ค. เสมอไป (สูตร month-1 ตรง ๆ เคยเกือบทำข้อมูลเดือน พ.ค. หาย)

**วิธีที่ถูกต้องทุกครั้งที่จะแก้ arrays พวกนี้:**
1. อ่าน label array ปัจจุบัน (`AF_MO`, `AFI_MONTHS`) ก่อนเสมอ
2. หา label ของเดือนที่กำลังประมวลผลรอบนี้ (เช่น "ก.ค." / "กค.69")
3. ถ้า label นั้นเป็น**ตัวสุดท้าย**ของ array อยู่แล้ว → แก้ค่าที่ index สุดท้าย (เดือนเดิม ข้อมูลใหม่กว่า/ครบกว่าเดิม)
4. ถ้า label นั้น**ยังไม่มี** → **append** ต่อท้ายทุก array พร้อมกัน (label + GMV + NET + COMM/COM + CR) ห้าม insert แทรกกลางหรือ rebuild array ใหม่ทั้งหมด
5. ห้ามเขียนทับเดือนก่อนหน้าเด็ดขาด — ถ้าไม่แน่ใจ index ไหนคือเดือนปัจจุบัน ให้ **หยุดและ log** แทนการเดา

**อัปเดต `WIBWUB_Affiliate_Dashboard.html`:**
- `AF_GMV` (index เดือนปัจจุบันตามกฎ append/overwrite ด้านบน) = total_gmv
- `AF_NET` (เดียวกัน) = total_net
- `AF_COM` (เดียวกัน) = total_comm
- `AF_CR` (เดียวกัน) = num_creators
- KPI overview strip: ครีเอเตอร์ที่ Active = num_creators

**อัปเดต `WIBWUB_Mobile.html`:**
- `AFI_GMV` (index เดือนปัจจุบันตามกฎ append/overwrite ด้านบน) = total_gmv
- `AFI_NET` (เดียวกัน) = total_net
- `AFI_COMM` (เดียวกัน) = total_comm
- hardcoded mks-grid KPI: `฿{round(total_gmv/1000)}K`

---

## STEP 5 — Process ไฟล์ สินค้า → อัปเดต PRODUCTS cr/vid

```python
PROD_DIR = '/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Affiliate/สินค้า/'
prod_files = sorted(glob.glob(PROD_DIR + '*.xlsx'), key=os.path.getmtime, reverse=True)
if not prod_files:
    print("WARNING: ไม่พบไฟล์ในโฟลเดอร์สินค้า — ข้ามขั้นตอนนี้")
else:
    df_prod = pd.read_excel(prod_files[0], header=None)
    
    # หา header row ที่มีชื่อ column
    header_idx = 0
    for i, row in df_prod.iterrows():
        row_str = ' '.join(str(v) for v in row.values if pd.notna(v))
        if 'สินค้า' in row_str or 'GMV' in row_str or 'ครีเอเตอร์' in row_str:
            header_idx = i
            break
    
    df_prod = pd.read_excel(prod_files[0], header=header_idx)
    print(f"Columns: {list(df_prod.columns)}")
    
    # หา columns สำคัญ (ชื่อ column อาจต่างกันตามเวอร์ชัน TikTok)
    # ค้นหา: product name, ครีเอเตอร์ที่มียอดขาย, วีดีโอ
    cols = {str(c).lower(): i for i, c in enumerate(df_prod.columns)}
    
    # สร้าง product cr/vid dict
    prod_data = {}
    for _, row in df_prod.iterrows():
        name = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ''
        if not name or name == 'nan': continue
        # ค้นหา cr column (ครีเอเตอร์ที่มียอดขาย)
        cr_val = 0
        vid_val = 0
        for col_name, col_idx in cols.items():
            if 'ครีเอเตอร์' in col_name and 'ขาย' in col_name:
                cr_val = int(pd.to_numeric(row.iloc[col_idx], errors='coerce') or 0)
            elif 'วีดีโอ' in col_name or 'video' in col_name:
                vid_val = int(pd.to_numeric(row.iloc[col_idx], errors='coerce') or 0)
        prod_data[name] = {'cr': cr_val, 'vid': vid_val}
    
    print(f"Products found: {list(prod_data.items())[:5]}")
```

**Mapping TikTok product name → PRODUCTS[].name (fuzzy keyword):**
| Keyword | PRODUCTS[].name |
|---|---|
| Leather | WIBWUB Refresh Leather Wipes |
| interior wipe (case-insensitive) | WIBWUB Interior wipes |
| Sugar | WIBWUB Sugar |
| CLEANER | WIBWUB CLEANER |
| Interior (ไม่มี "wipe") | WIBWUB Interior |
| Refresh (ไม่มี "Leather") | WIBWUB Refresh |
| Visible | WIBWUB Visible |

**อัปเดต `WIBWUB_Affiliate_Dashboard.html`:**
- `PRODUCTS` array: แก้เฉพาะ `cr` และ `vid` fields (ห้ามแก้ gmv, units, monthly, ret)
- KPI strip สินค้า tab: `ผ่าน X,XXX creators` = รวม cr ทุกสินค้า

---

## STEP 5B — Process ไฟล์ วีดีโอ → merge เข้า VIDEOS array (สำคัญ — ห้ามข้าม)

⚠️ **ก่อน 2026-07-20 step นี้ไม่มีอยู่** — ไฟล์วีดีโอถูกดาวน์โหลด/ย้ายเข้าโฟลเดอร์ทุกวันแต่ไม่เคยถูกประมวลผลเข้า Dashboard เลย
ต่างจาก Tab ครีเอเตอร์/สินค้า (STEP 4/5) ที่มีสคริปต์อัปเดตอัตโนมัติอยู่แล้ว — นี่คือช่องโหว่ที่ทำให้ VIDEOS array ค้างข้อมูลเก่าเป็นสัปดาห์ ต้องรันทุกครั้งที่ schedule นี้ทำงาน

ไฟล์ TikTok video export เป็น **inlineStr XML format** — `openpyxl` อ่านไม่ได้ (`max_row=1` ว่างเปล่า) ต้อง parse raw XML ด้วย `zipfile` + regex

```python
import zipfile, re, json, os, glob
from collections import Counter
from datetime import date

VID_DIR = '/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Affiliate/วีดีโอ/'
HTML = '/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/WIBWUB_Affiliate_Dashboard.html'

vid_files = sorted(glob.glob(VID_DIR + '*.xlsx'), key=os.path.getmtime, reverse=True)
if not vid_files:
    print("WARNING: ไม่พบไฟล์ในโฟลเดอร์วีดีโอ — ข้าม STEP 5B")
else:
    fpath = vid_files[0]
    print("Using:", os.path.basename(fpath))

    zf = zipfile.ZipFile(fpath)
    content = zf.open('xl/worksheets/sheet1.xml').read().decode('utf-8', errors='replace')
    row_pattern = re.compile(r'<row r="(\d+)"[^>]*>(.*?)</row>', re.DOTALL)
    cell_pattern = re.compile(r'<c r="([A-Z]+)(\d+)"[^>]*>(?:<is><t[^>]*>(.*?)</t></is>|<v>(.*?)</v>)?</c>')

    def col_to_idx(col):
        idx = 0
        for ch in col:
            idx = idx * 26 + (ord(ch) - ord('A') + 1)
        return idx - 1

    def parse_thb(s):
        if not s:
            return 0.0
        s = s.replace('฿', '').replace(',', '').strip()
        try:
            return float(s)
        except:
            return 0.0

    rows = {}
    for rm in row_pattern.finditer(content):
        rnum = int(rm.group(1))
        if rnum < 3:
            continue
        rowdata = {}
        for cm in cell_pattern.finditer(rm.group(2)):
            col, r, tv, nv = cm.groups()
            idx = col_to_idx(col)
            val = tv if tv is not None else nv
            if val is not None:
                val = val.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&apos;', "'")
            rowdata[idx] = val
        if rowdata:
            rows[rnum] = rowdata

    # col layout: A=title B=vid_id C=post_date D=link E=creator F=product_id G=GMV
    new_data = {}
    for r in rows.values():
        vid_id = r.get(1)
        if not vid_id:
            continue
        new_data[vid_id] = {
            'creator': r.get(4, ''),
            'product_id': r.get(5, ''),
            'gmv': parse_thb(r.get(6)),
        }
    print("parsed video rows:", len(new_data))

    with open(HTML, encoding='utf-8') as fh:
        html = fh.read()
    m = re.search(r'const VIDEOS = \[(.*?)\n\];', html, re.DOTALL)
    block = m.group(1)

    # ตรวจ schema key ของ monthly{} จาก entry แรก (เช่น mar,apr,may,jun,jul)
    first_monthly = re.search(r'monthly:\{([a-z:,\d.]+)\}', block)
    schema_keys = re.findall(r'([a-z]+):', first_monthly.group(1)) if first_monthly else []

    MONTH_KEY = {1: 'jan', 2: 'feb', 3: 'mar', 4: 'apr', 5: 'may', 6: 'jun',
                 7: 'jul', 8: 'aug', 9: 'sep', 10: 'oct', 11: 'nov', 12: 'dec'}
    THAI = {'jan': 'ม.ค.', 'feb': 'ก.พ.', 'mar': 'มี.ค.', 'apr': 'เม.ย.', 'may': 'พ.ค.', 'jun': 'มิ.ย.',
            'jul': 'ก.ค.', 'aug': 'ส.ค.', 'sep': 'ก.ย.', 'oct': 'ต.ค.', 'nov': 'พ.ย.', 'dec': 'ธ.ค.'}
    cur_key = MONTH_KEY[date.today().month]

    if cur_key not in schema_keys:
        print(f"เดือนใหม่ '{cur_key}' ยังไม่มีใน monthly schema ({schema_keys}) → เพิ่ม key ใหม่ค่า 0 ให้ทุก entry อัตโนมัติ")
        last_key = schema_keys[-1]
        block, n = re.subn(r"(" + last_key + r":[\d.]+)\}", r"\1," + cur_key + r":0}", block)
        print(f"extended {n} entries with key '{cur_key}'")
        schema_keys.append(cur_key)

    entry_re = re.compile(
        r"\{creator:'(?P<creator>[^']*)',product:'(?P<product>[^']*)',vid_id:'(?P<vid_id>[^']*)',"
        r"caption:'(?P<caption>[^']*)',gmv:(?P<gmv>[\d.]+),units:(?P<units>[\d.]+),date:'(?P<date>[^']*)',"
        r"monthly:\{" + ",".join(f"{k}:(?P<{k}>[\\d.]+)" for k in schema_keys) + r"\}\}"
    )
    existing = []
    for em in entry_re.finditer(block):
        d = em.groupdict()
        for k in ['gmv', 'units'] + schema_keys:
            d[k] = float(d[k])
        existing.append(d)
    print("parsed existing VIDEOS entries:", len(existing))

    if not existing:
        print("⚠️ STOP: entry_re ไม่ match เลย (schema เปลี่ยนไปจากที่คาด) — ห้ามเขียนทับ ให้แจ้ง user แทน")
    else:
        vid_to_product = {e['vid_id']: e['product'] for e in existing}
        existing_vids = set(vid_to_product)

        # product_id -> product name (จาก vid_id ที่มีอยู่ทั้งสองฝั่ง)
        pid_to_names = {}
        for vid, rec in new_data.items():
            if vid in vid_to_product:
                for pid in (rec.get('product_id') or '').split(','):
                    pid = pid.strip()
                    if pid:
                        pid_to_names.setdefault(pid, Counter())[vid_to_product[vid]] += 1
        pid_to_name = {p: c.most_common(1)[0][0] for p, c in pid_to_names.items()}

        def date_label(e):
            active = [k for k in schema_keys if e[k] > 0]
            if not active:
                return ''
            if len(active) == 1:
                return THAI[active[0]]
            last2 = active[-2:]
            idx2 = [schema_keys.index(k) for k in last2]
            if idx2[1] - idx2[0] == 1:
                return f"{THAI[last2[0]]}–{THAI[last2[1]]}"
            return THAI[active[-1]]

        updated = 0
        for e in existing:
            vid = e['vid_id']
            if vid in new_data:
                newgmv = round(new_data[vid]['gmv'])
                if newgmv != e[cur_key]:
                    updated += 1
                e[cur_key] = newgmv
            e['gmv'] = sum(e[k] for k in schema_keys)
            e['date'] = date_label(e)
        print("updated current-month (", cur_key, ") values:", updated)

        min_gmv = min(e['gmv'] for e in existing)
        new_only = [v for v in new_data if v not in existing_vids]
        candidates = sorted(
            ({**new_data[v], 'vid_id': v} for v in new_only if new_data[v]['gmv'] >= min_gmv),
            key=lambda x: -x['gmv']
        )

        new_entries = []
        for c in candidates:
            name = None
            for p in (c.get('product_id') or '').split(','):
                p = p.strip()
                if p in pid_to_name:
                    name = pid_to_name[p]
                    break
            name = name or 'Unknown'
            monthly = {k: 0.0 for k in schema_keys}
            monthly[cur_key] = round(c['gmv'])
            new_entries.append({
                'creator': c['creator'], 'product': name, 'vid_id': c['vid_id'],
                'caption': '', 'gmv': round(c['gmv']), 'units': 0.0,
                'date': THAI[cur_key], **{k: monthly[k] for k in schema_keys}
            })
        print("new video entries added:", len(new_entries))

        def esc(s):
            return s.replace('\\', '\\\\').replace("'", "\\'")

        def fmt(e):
            monthly_str = ",".join(f"{k}:{round(e[k])}" for k in schema_keys)
            return "  {creator:'%s',product:'%s',vid_id:'%s',caption:'%s',gmv:%d,units:%d,date:'%s',monthly:{%s}}" % (
                esc(e['creator']), esc(e['product']), e['vid_id'], esc(e['caption']),
                round(e['gmv']), round(e['units']), e['date'], monthly_str
            )

        lines = [fmt(e) for e in existing] + [fmt(e) for e in new_entries]
        new_block = "const VIDEOS = [\n" + ",\n".join(lines) + ",\n];"
        old_block_full = "const VIDEOS = [" + block + "\n];" if cur_key in schema_keys else None

        # ถ้ามีการ extend schema ด้านบน ให้ match แบบกว้างแทน (block ถูกแก้ไปแล้ว)
        html2 = re.sub(r'const VIDEOS = \[.*?\n\];', lambda _: new_block, html, count=1, flags=re.DOTALL)
        assert html2 != html, "เขียนทับ VIDEOS array ไม่สำเร็จ — หยุด ห้าม push"

        with open(HTML, 'w', encoding='utf-8') as fh:
            fh.write(html2)
        print("TOTAL VIDEOS entries written:", len(lines), "| updated:", updated, "| new:", len(new_entries))
```

**กฎความปลอดภัย:**
- ถ้า `entry_re` match ได้ 0 รายการ → **ห้ามเขียนทับไฟล์เด็ดขาด** ให้ log warning ใน report แล้วข้าม STEP 6/push สำหรับไฟล์นี้ (schema อาจเปลี่ยนไปจากที่ script คาดไว้ ต้องให้ user ตรวจ manual)
- ตรวจ `git diff --stat WIBWUB_Affiliate_Dashboard.html` หลังรัน ถ้าบรรทัดเปลี่ยนเกิน ~50% ของทั้งไฟล์ (ผิดปกติมาก) → หยุด อย่า commit
- Verify ก่อน commit เสมอ: `node -e "const h=require('fs').readFileSync('WIBWUB_Affiliate_Dashboard.html','utf8'); eval('['+h.match(/const VIDEOS = \[([\s\S]*?)\n\];/)[1]+']')"` ต้องไม่ throw error

**อัปเดต `push_now.command`** (STEP 6) ให้ commit ครอบคลุมไฟล์นี้ด้วย (มีอยู่แล้วใน `git add`)

---

## STEP 6 — Bump sw.js + สร้าง push_now.command

```bash
CURRENT=$(grep -oP "wibwub-v\K[0-9]+" /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/sw.js)
NEW=$((CURRENT + 1))
sed -i "s/wibwub-v${CURRENT}/wibwub-v${NEW}/" /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/sw.js
echo "sw.js: v$CURRENT → v$NEW"

cat > "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/push_now.command" << 'EOF'
#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock
git add WIBWUB_Affiliate_Dashboard.html WIBWUB_Mobile.html sw.js
git commit -m "auto-update: Affiliate $(date +%Y-%m-%d)"
git push && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
EOF
chmod +x "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/push_now.command"
```

---

## STEP 7 — Report สรุป

```
✅ WIBWUB Affiliate Update — {today}
📅 ช่วงข้อมูล: 1/{month_num} – {end_date}

📁 ไฟล์ที่ย้ายแล้ว:
  ครีเอเตอร์/ ← {creator_filename}
  สินค้า/     ← {product_filename}
  วีดีโอ/     ← {video_filename}
  ไลฟ์สตรีม/ ← {live_filename}

📊 GMV: ฿{total_gmv:,}  Net: ฿{total_net:,}  Comm: ฿{total_comm:,}
👥 Creators: {num_creators}
🛒 Products cr/vid updated
🎬 VIDEOS: อัปเดต {updated} รายการ, เพิ่มใหม่ {new_count} รายการ (รวม {total_videos})
⚙️ sw.js: v{old} → v{new}
📌 ดับเบิ้ลคลิก push_now.command เพื่อ push ขึ้น GitHub
```

---

## หากมีข้อผิดพลาด
- Chrome ไม่ connected → log "Chrome not available" และหยุด
- Session expired → log "Re-login required" และหยุด
- ไฟล์ tab ใดไม่ดาวน์โหลดได้ → บันทึก error, ข้ามไปทำ tab ต่อไป, แจ้งใน report
- ชื่อไฟล์ไม่ตรงกับ pattern → ใช้ `ls -lt Downloads/*.xlsx` ดู timestamp แล้ว mv ตามลำดับเวลา
- navigate ค้าง → ต้องใช้ browser_batch เท่านั้น ห้าม navigate standalone
- STEP 5B (VIDEOS) parse ไม่ match / schema ผิดปกติ → ห้ามเขียนทับไฟล์ แจ้งใน report ว่า "VIDEOS array ต้องตรวจ manual" แล้วข้าม commit ส่วนนี้ (ส่วนครีเอเตอร์/สินค้ายัง commit ได้ตามปกติ)

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