---
name: update-wibwub
description: >
  Use this skill whenever the user wants to sync new data into any WIBWUB dashboard or app.
  Triggers include: "update app", "update dashboard", "มีข้อมูลใหม่", "อัพเดทข้อมูล",
  "sync ข้อมูล", sharing a Google Sheet link with any sales/TikTok/affiliate data,
  sharing new Shipnity export files, sharing new platform order files (Shopee zip, Lazada
  xlsx, TikTok xlsx, Line My Shop xlsx), asking why app/web data doesn't match the sheet,
  or any request to refresh WIBWUB content. This skill covers ALL files — Mobile PWA,
  Web Dashboard, Affiliate Dashboard, TikTok Dashboard, Platform Analytics Dashboard —
  and ALL data sections: TikTok clips, sales arrays, affiliate GMV, ads ROAS, platform
  breakdown, top products (from all 5 platforms + Shipnity other channels), and all
  hardcoded KPI text. Always use this skill when the user mentions updating any part of
  the WIBWUB app or dashboards, even if they only mention one file — sync ALL files every time.
---

# WIBWUB Full Data Sync Skill

This skill guides syncing **all data** from official sources into **all WIBWUB files**
simultaneously — Mobile PWA, Web Dashboard, Ads Dashboard, Affiliate Dashboard, TikTok
Dashboard, Platform Analytics Dashboard.

---

## CRITICAL: Mistakes That Already Happened (อย่าทำซ้ำเด็ดขาด)

### ผิดพลาด #1: อัปเดตแค่ไฟล์เดียว — ห้ามเด็ดขาด
**กฎหลัก:** ทุกครั้งที่มีการอัปเดตข้อมูลใดๆ ต้องอัปเดตทั้ง Web และ Mobile พร้อมกันเสมอ ไม่มีข้อยกเว้น

| ส่วนข้อมูล | Web (WIBWUB_Dashboard.html) | Mobile (WIBWUB_Mobile.html) |
|---|---|---|
| Sales arrays | SH_REV, TK_REV, LZ_REV, ... | arrays เดียวกัน — ต้องตรงกัน |
| Affiliate | (อยู่ใน Affiliate Dashboard แยก) | AFI_GMV, AFI_NET, AFI_COMM |
| Social followers | soc_follow chart datasets | hardcoded KPI ใน mks-grid |
| Top Products | chart + table | ALL_PRODUCTS array |
| Hardcoded KPI text | hh-grid, sales KPI strip | mks-grid, hero values |

WIBWUB_Mobile.html และ WIBWUB_Dashboard.html มี arrays เดียวกัน แก้หนึ่งต้องแก้อีกอัน
ห้ามบอกว่าอัปเดตเสร็จแล้วถ้ายังไม่ครบทุกไฟล์

### ผิดพลาด #2: อ่านยอด TikTok/Lazada จาก row ที่ไม่ใช่ row สุดท้าย
Google Sheet มีหลาย rows ต่อเดือน (01-10/05, 01-13/05, 01-17/05...)
ยอดจริงคือ row สุดท้ายเท่านั้น เช่น "01-17/05/26" = ยอดสะสมถึง 17 พ.ค.
row กลางๆ คือยอดบางส่วน ใช้ไม่ได้

### ผิดพลาด #3: Data_15-05-2026.xlsx เป็นข้อมูลเดือนกุมภาพันธ์ ไม่ใช่พฤษภาคม
ชื่อไฟล์หลอก ต้องอ่าน column วันที่สร้าง (index 19) จากข้อมูลจริงเสมอ
ไฟล์นี้มีวันที่ 28/02/2026 = เดือน 2 (กุมภาพันธ์) อย่าเปลี่ยนเป็น 5!

### ผิดพลาด #4: ลืมเช็คไฟล์ Shipnity ใหม่ก่อน aggregate
ทำ ls -lt เช็ค Data Shipnity/ ก่อนทุกครั้ง
ไฟล์ที่ modified ล่าสุดที่ยังไม่ได้รวม = delta ที่ต้องเพิ่ม

### ผิดพลาด #5: pointRadius array สั้นกว่า data array
5 เดือน = pointRadius: [3,3,3,3,6] ไม่ใช่ [3,3,3,6]
ทุกครั้งที่เพิ่มเดือนใหม่ต้องเพิ่ม 3 ใน pointRadius ทุกจุด

### ผิดพลาด #6: ลืม bump sw.js cache version
ต้อง +1 ทุกครั้งที่แก้ไขไฟล์ใดก็ตาม ไม่งั้น PWA ไม่ refresh

### ผิดพลาด #7: Sales arrays มี 9 elements แต่ M5 มีแค่ 5 labels — root cause ของ data มั่ว
**อาการ:** Dashboard แสดงยอดเดือนกันยา-มกรา แทนที่จะเป็น ม.ค.-พ.ค. เพราะ labels มีแค่ 5 แต่ arrays มี 9
**สาเหตุ:** wibwub_update.py ไม่ได้ filter เฉพาะปีปัจจุบัน ทำให้ `available` รวมทุกเดือนตั้งแต่ Sep 2025
**แก้ใน wibwub_update.py:** เพิ่ม `current_yr = datetime.now().year % 100` แล้ว filter:
```python
available = [m for m in ALL_MONTHS if m in sh_data and m.endswith(f"/{current_yr}")]
```
**แก้ใน Dashboard/Mobile:** ตัด arrays ให้เหลือแค่ค่า Jan–May 2026 (5 ตัวสุดท้าย)
กฎ: จำนวน elements ใน arrays ต้องเท่ากับจำนวน labels ใน M5 เสมอ

### ผิดพลาด #8: wibwub_update.py อัปเดต M4 แทน M5
wibwub_update.py ใช้ variable `M4` ผิด ต้องเปลี่ยนเป็น `M5` ทุกจุด
ตรวจก่อนรันทุกครั้งว่า `const M5 = {` อยู่ใน Dashboard และ script อัปเดต M5 ไม่ใช่ M4

### ผิดพลาด #9: TK_CANCEL_PCT ไม่ใช่ cancel% ของ TikTok — ห้ามใส่ใน SALES_ARRS
TikTok Sheet col 5 = Gross GMV (ตัวเลขใหญ่มาก ~1.5M) ไม่ใช่ cancel%
ใน wibwub_update.py ห้ามมี `TK_CANCEL_PCT` ใน SALES_ARRS เด็ดขาด
Mobile ใช้ `SH_CANCEL` (array แยก = Shopee cancel% จริงๆ) ส่วน Dashboard ใช้ `SH_CANCEL_PCT` = cost% จาก col 5

### ผิดพลาด #10: Shipnity ไฟล์ใหม่ format เปลี่ยนเป็น order-level — ใช้ Top Products ไม่ได้
ไฟล์เก่า (Data_มกราคม, Data_15-05-2026/กุมภา, Data-มีนา, Data_เมษา): product-level = มีชื่อสินค้า ใช้ aggregate Top Products ได้
ไฟล์ใหม่ (Data_พฤษภา, Data_18-05-2026, Data_กุมภา2, Data_01-06-2026 และหลังจากนี้): order-level = ไม่มีชื่อสินค้า ใช้ Top Products ไม่ได้
ถ้า col[1] ว่างเปล่าหรือเป็น numeric ID = order-level → ข้ามไฟล์นั้นสำหรับ Top Products

### ผิดพลาด #11: git push จาก bash sandbox ล้มเหลว (HTTP 403 proxy)
bash sandbox route GitHub HTTPS ผ่าน proxy ที่ block outbound → ได้รับ "HTTP 403 from proxy after CONNECT"
ห้ามเสียเวลา config proxy หรือ SSH ใน sandbox
**วิธีแก้:** สร้าง `push_now.command` ใน workspace แล้วให้ user double-click รันบนเครื่องจริง:
```bash
#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-.../All"
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
```

### ผิดพลาด #12: Lazada + TikTok ไฟล์ใหญ่ใช้ inlineStr XML — openpyxl คืน 1 row
**Lazada** (~87MB) และ **TikTok** (~122MB) ใช้ format `<is><t>...</t></is>` แทน shared strings
openpyxl.load_workbook จะ return max_row=1 และ data ว่างเปล่า
**วิธีแก้:** ต้องอ่าน raw XML ด้วย regex streaming จาก zipfile:
```python
import zipfile, re

with zipfile.ZipFile(filepath) as zf:
    # TikTok ใช้ sheet2.xml, Lazada ใช้ sheet1.xml
    sheet_name = 'xl/worksheets/sheet2.xml'  # หรือ sheet1.xml
    with zf.open(sheet_name) as f:
        content = f.read().decode('utf-8', errors='replace')

# หาทุก cell ที่มี <is><t>
cells = re.findall(r'<c r="([A-Z]+)(\d+)"[^>]*><is><t[^>]*>(.*?)</t></is></c>', content)
```

### ผิดพลาด #13: TikTok sheet XML — each cell เป็น separate `<row>` element
TikTok sheet XML format: แต่ละ cell อยู่ใน `<row r="N">` ของตัวเอง (ไม่ group cells ไว้ใน row เดียวกัน)
```xml
<row r="5"><c r="A5"><is><t>val_a</t></is></c></row>
<row r="5"><c r="B5"><is><t>val_b</t></is></c></row>
```
ต้องรวม cells ด้วย row number ก่อน แล้วค่อย build row dict:
```python
from collections import defaultdict
row_cells = defaultdict(dict)
for col_letter, row_num, val in cells:
    col_idx = col_letter_to_idx(col_letter)  # A=0, B=1, ...
    row_cells[int(row_num)][col_idx] = val
```

---

## Official Data Sources

### ยอดขาย (Sales) — อ่านผ่าน Google Drive MCP

| Platform | Google Sheet URL | สิ่งที่ต้องอ่าน |
|---|---|---|
| Shopee | https://docs.google.com/spreadsheets/d/10LrzWB8bbCO9FigCQFz5gZ3iSXMVhK0S/edit?gid=1820466351 | ยอดสุทธิ, orders, cancel%, ads, fee |
| Lazada | https://docs.google.com/spreadsheets/d/1FxLAUiwabmNcBc3TA-bpHqg2MSK7uJ4U/edit?gid=1032656124 | ยอดสุทธิ, ads, fee, coupon, cost% |
| TikTok | https://docs.google.com/spreadsheets/d/1k22c3PGY6aQjygAX6df_rQLR8aTzL-iz/edit?gid=150856480 | ยอดสุทธิ, ads, commission |

กฎ: ใช้ ROW สุดท้ายของแต่ละเดือนเท่านั้น

### Social Media
- Facebook/IG/YouTube: https://docs.google.com/spreadsheets/d/1OWZGQD1wHvIlLAAg_7rJ0CtL-X9vEx4py-cRp_e3NvQ/edit?gid=1242793042

### Affiliate
- ไฟล์ xlsx ใน `Data Affiliate/` folder (Transaction_Analysis_Creator_List_YYYYMMDD-YYYYMMDD.xlsx)
- Net GMV = GMV จากครีเอเตอร์ − การคืนเงิน (คำนวณเอง — ไม่มีคอลัมน์ Net ในไฟล์โดยตรง)

### TikTok Clips
- TikTok sheet เดียวกัน (gid=150856480) หรือ tab clip stats แยก

### Top Products & Ads (ไม่ได้มาจาก Google Sheet)
- **Top Products (Mobile/Web Dashboard):** Shipnity xlsx files ใน Data Shipnity/ เท่านั้น (product-level files)
- **Top Products (Platform Analytics):** ไฟล์ order-level จากทุก platform — ดู Step 8D
- Ads Dashboard: อ่านไฟล์ล่าสุดใน data Ads/ (ดู Step 8)

---

## File Paths

Base: /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All
Shell base: /sessions/hopeful-serene-fermi/mnt/All/

| File | Filename |
|---|---|
| Mobile PWA | WIBWUB_Mobile.html |
| Web Dashboard | WIBWUB_Dashboard.html |
| Affiliate Dashboard | WIBWUB_Affiliate_Dashboard.html |
| TikTok Dashboard | WIBWUB_TikTok_Dashboard_v7.html |
| Ads Dashboard | data Ads/WIBWUB_Ads_Dashboard.html |
| **Platform Analytics** | **WIBWUB_Platform_Analytics.html** |
| Service Worker | sw.js |
| Shipnity Data | Data Shipnity/ |
| Sales Dashboard | Data Shipnity/Sales_Dashboard.html |
| **Aggregation Script** | **outputs/aggregate_all_v2.py** (sandbox only) |
| **Platform Data Cache** | **outputs/products_combined.json** (sandbox only) |

**Platform raw data folders:**
| Platform | Folder | Format |
|---|---|---|
| Shopee | `data ยอดขาย plaform/shopee/` | zip files, each containing xlsx |
| Lazada | `data ยอดขาย plaform/Lazada/` | single large xlsx (~87MB, inlineStr) |
| TikTok | `data ยอดขาย plaform/tiktok shop/` | xlsx (~122MB, inlineStr, sheet2.xml) |
| Line My Shop | `data ยอดขาย plaform/Line my shop/` | ECMA-376 encrypted xlsx (password=5000113570) |

---

## Step 0 — เช็คไฟล์ใหม่ใน Data Shipnity (ทำก่อนเสมอ)

```bash
ls -lt "/sessions/hopeful-serene-fermi/mnt/All/Data Shipnity/"
```
ไฟล์ที่ modified ล่าสุดที่ยังไม่เคยรวม = delta ที่ต้องเพิ่ม

---

## Step 1 — อ่านไฟล์ปัจจุบันก่อนแก้

Read WIBWUB_Mobile.html + WIBWUB_Dashboard.html
บันทึกค่าปัจจุบันของทุก array เพื่อเปรียบเทียบกับข้อมูลใหม่

---

## Step 2 — Shipnity Month Mapping (ตรวจก่อนทุกครั้ง)

ห้ามเชื่อชื่อไฟล์ ต้องตรวจ column วันที่สร้าง (index 19):
```python
wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
ws = wb.active
dates = [str(row[19]) for i,row in enumerate(ws.iter_rows(min_row=2, values_only=True))
         if row[19] and i < 500]
print(f"{filepath}: {min(dates)} -> {max(dates)}")
```

Confirmed mapping (อย่าเปลี่ยน):
- Data_มกราคม.xlsx      = เดือน 1
- Data_15-05-2026.xlsx  = เดือน 2 (กุมภาพันธ์) ชื่อหลอก อย่าใส่ 5!
- Data-มีนา.xlsx         = เดือน 3
- Data_เมษา.xlsx         = เดือน 4
- Data_พฤษภา.xlsx       = เดือน 5 (พ.ค. 1-14)
- Data_18-05-2026.xlsx  = เดือน 5 (พ.ค. 15-17)
- ไฟล์ใหม่สุด           = ตรวจ date ก่อน map

---

## Step 3 — Aggregate Top Products

```python
import openpyxl
from collections import defaultdict

BASE = '/sessions/hopeful-serene-fermi/mnt/All/Data Shipnity/'

file_month = {
    'Data_มกราคม.xlsx':    1,
    'Data_15-05-2026.xlsx': 2,  # กุมภาพันธ์ ห้ามเปลี่ยนเป็น 5
    'Data-มีนา.xlsx':       3,
    'Data_เมษา.xlsx':       4,
    'Data_พฤษภา.xlsx':     5,
    'Data_18-05-2026.xlsx': 5,
    # เพิ่มไฟล์ใหม่จาก Step 0 ตรงนี้
}

seen = set()
prod_total = defaultdict(lambda: {'revenue': 0, 'qty': 0})
prod_month = defaultdict(lambda: defaultdict(lambda: {'revenue': 0, 'qty': 0}))

for fname, month in file_month.items():
    wb = openpyxl.load_workbook(BASE+fname, read_only=True, data_only=True)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row[4] or not row[1]: continue
        key = (str(row[4]), str(row[0]), int(row[3] or 0))
        if key in seen: continue
        seen.add(key)
        rev = (row[2] or 0) * (row[3] or 0)
        qty = int(row[3] or 0)
        prod_total[str(row[1])]['revenue'] += rev
        prod_total[str(row[1])]['qty']     += qty
        prod_month[str(row[1])][month]['revenue'] += rev
        prod_month[str(row[1])][month]['qty']     += qty
    wb.close()

# ALL_PRODUCTS (Mobile) = top 15 cumulative ม.ค.-ปัจจุบัน
top15 = sorted(prod_total.items(), key=lambda x: x[1]['revenue'], reverse=True)[:15]

# Web Dashboard chart+table = top 10 by 3-month total (มี.ค.+เม.ย.+พ.ค.)
def three_rev(n): return sum(prod_month[n][m]['revenue'] for m in [3,4,5])
top10_3mo = sorted([n for n,_ in top15], key=three_rev, reverse=True)[:10]
```

---

## Step 4 — Sales Arrays

Arrays 0-indexed: [ม.ค., ก.พ., มี.ค., เม.ย., พ.ค., ...]

SH_REV, TK_REV, LZ_REV, SH_ORD, SH_CANCEL/SH_CANCEL_PCT,
SH_ADS, SH_FEE, SH_NEW, SH_OLD,
LZ_ADS, LZ_FEE, LZ_COUPON, LZ_COST_PCT,
TOTAL_REV, TOTAL_ORD

แก้ WIBWUB_Mobile.html และ WIBWUB_Dashboard.html พร้อมกัน ค่าต้องตรงกัน

---

## Step 5 — CHANNELS Array (Mobile)

v = ยอดสะสม ม.ค. ถึงเดือนล่าสุด เรียง descending

---

## Step 6 — TikTok Clips (ALL_POSTS)

{lbl:'DAY', m:MONTH_NUM, pillar:'PILLAR', c:'CONTENT', views:V, eng:E, ret:R, watch:W, er:ER, url:'URL'}
eng = likes + comments + shares + saves (คำนวณเอง ห้าม copy จาก sheet)
er = round((eng/views)*100, 2 decimal)
อัปเดตทั้ง Mobile และ WIBWUB_TikTok_Dashboard_v7.html

---

## Step 7 — Hardcoded KPI Text (ลืมบ่อย)

ค่าพวกนี้ไม่คำนวณจาก JS ต้องแก้ text โดยตรง:
- Home hero: ยอดขายรวม, orders, AOV
- hh-grid: ยอดแต่ละ platform
- mks-grid: Affiliate GMV, Ads ROAS, TikTok Clips count, TK Followers
- Sales overview KPI strip
- Marketing overview KPI strip
- Combined Ads section
- Data coverage footnotes (เช่น "พ.ค. 1-17 พ.ค.")
- Header date range ทุกไฟล์: "ม.ค. – พ.ค. 2569"

---

## Step 8 — Ads Dashboard

### แหล่งข้อมูล Ads (อ่านไฟล์ล่าสุดในโฟลเดอร์ `data Ads/`)

```bash
# หาไฟล์ล่าสุดก่อนเสมอ
ls -lt "/sessions/hopeful-serene-fermi/mnt/All/data Ads/"
```

| Platform | ไฟล์ | Format |
|---|---|---|
| **Shopee** | `ข้อมูล-Shopee-Ads-DD_MM_YYYY-DD_MM_YYYY.csv` (ล่าสุด) | CSV, skip 7 header rows, header อยู่ที่ row 8 |
| **TikTok** | `creative data for product campaigns YYYY-MM-DD ~ YYYY-MM-DD.xlsx` (ล่าสุด) | xlsx, sheet="Data" |

**วิธีอ่าน Shopee CSV:**
```python
import csv, io
with open(SHOPEE_CSV, encoding='utf-8-sig') as f:
    lines = f.readlines()
header_idx = next(i for i,l in enumerate(lines) if 'ลำดับ' in l)
reader = csv.reader(io.StringIO(''.join(lines[header_idx:])))
headers = next(reader)
rows = [r for r in reader if r and r[0].strip() and r[0].isdigit()]
# col[24]=ค่าโฆษณา(spend), col[22]=ยอดขาย(rev), col[14]=orders, col[11]=imp, col[12]=clicks
```

**วิธีอ่าน TikTok xlsx:**
```python
import pandas as pd
df = pd.read_excel(TIKTOK_XLSX, sheet_name='Data')
# columns: ต้นทุน(spend), รายได้ขั้นต้น(revenue), คำสั่งซื้อ SKU(orders)
# ยอดการแสดงผลโฆษณาสินค้า(imp), ยอดการคลิกโฆษณาสินค้า(clicks)
```

**สิ่งที่ต้องอัปเดตใน `data Ads/WIBWUB_Ads_Dashboard.html`:**
1. `may.shopee` และ `may.tiktok`: spend, revenue, orders, imp, clicks, roas, ctr, cvr, cpa, top5, worst5, all campaigns
2. `all.shopee` และ `all.tiktok`: +delta จาก old May → new May
3. `ADS_PERIOD_SUMMARY`: อัปเดต may/all labels
4. HTML button labels `<span class="pb-sub">` (มี 2 จุด)
5. `SH_ADS[4]` ใน WIBWUB_Dashboard.html และ WIBWUB_Mobile.html (= Shopee spend ใหม่)

**หมายเหตุ:** Shopee revenue ใน may section ใช้ SH_REV[4] (ยอดขายรวม) ไม่ใช่ยอด ads-attributed

---

## Step 8B — Affiliate Data

**โครงสร้างโฟลเดอร์ (ไฟล์แยกตาม tab):**
```bash
ls -lt "/sessions/hopeful-serene-fermi/mnt/All/Data Affiliate/ครีเอเตอร์/"
# ไฟล์รูปแบบ: Transaction_Analysis_Creator_List_YYYYMMDD-YYYYMMDD.xlsx
# ใช้ไฟล์ที่ครอบคลุมช่วงวันล่าสุดของเดือนปัจจุบัน
```

**หมายเหตุ:** ไฟล์ถูกแยกไว้ในโฟลเดอร์ย่อยตาม tab ที่ export:
- `Data Affiliate/ครีเอเตอร์/` — Transaction_Analysis_Creator_List_*.xlsx
- `Data Affiliate/สินค้า/` — Transaction_Analysis_Product_List_*.xlsx (หรือชื่อคล้ายกัน)
- `Data Affiliate/วีดีโอ/` — video performance exports
- `Data Affiliate/ไลฟ์สตรีม/` — livestream exports

**คอลัมน์ในไฟล์ (header row=0, data row=1+):**
- col 0: Creator name
- col 1: GMV จากครีเอเตอร์
- col 2: การคืนเงิน
- col 10: ค่าคอมมิชชั่นโดยประมาณ

**Net GMV = GMV − การคืนเงิน** (คำนวณเองเสมอ — ไม่มีคอลัมน์ Net ในไฟล์)

**วิธีอ่านและคำนวณ:**
```python
import pandas as pd

def parse_thb(val):
    if not val: return 0.0
    return float(str(val).replace('฿','').replace(',','').strip() or 0)

import glob, os

CREATOR_DIR = '/sessions/hopeful-serene-fermi/mnt/All/Data Affiliate/ครีเอเตอร์/'
files = sorted(glob.glob(CREATOR_DIR + '*.xlsx'), key=os.path.getmtime, reverse=True)
if not files:
    raise FileNotFoundError("ไม่พบไฟล์ใน Data Affiliate/ครีเอเตอร์/")
filepath = files[0]
print(f"Using: {os.path.basename(filepath)}")

df = pd.read_excel(filepath, header=None)
df = df.iloc[1:]  # skip header row

# Transaction Analysis ครีเอเตอร์ format:
# col[0]=creator, col[1]=GMV, col[2]=returns, col[3]=orders, col[10]=commission
df['gmv_n']  = df[1].apply(parse_thb)
df['ret_n']  = df[2].apply(parse_thb)
df['net_n']  = df['gmv_n'] - df['ret_n']   # ← NET = GMV - คืนเงิน
df['comm_n'] = df[10].apply(parse_thb)

total_gmv  = round(df['gmv_n'].sum())
total_net  = round(df['net_n'].sum())
total_comm = round(df['comm_n'].sum())
num_creators = len(df[df['gmv_n'] > 0])
```

**Array mapping:**
| Array | ตัวแปรใน HTML | คำนวณจาก |
|---|---|---|
| GMV รายเดือน | `gmvD` / `AFI_GMV` | sum(gmv_n) |
| Net GMV | `netD` / `AFI_NET` | sum(gmv_n - ret_n) |
| ค่าคอม | `commD` / `AFI_COMM` | sum(comm_n) |
| จำนวน Creator | `crD` | len(df) |

**ไฟล์ที่ต้องอัปเดต (ทั้งสองไฟล์พร้อมกัน):**
1. `WIBWUB_Affiliate_Dashboard.html` → แก้ `gmvD`, `netD`, `commD`, `crD`, และ `raw[]` (ตาราง creator รายคน)
2. `WIBWUB_Mobile.html` → แก้ `AFI_GMV`, `AFI_NET`, `AFI_COMM`

**กฎ raw[]:** mn[] values = GMV per creator per month (ไม่ใช่ net), format:
```js
{n:"creator_name", t:total_gmv, ma:active_months, mn:[nov,dec,jan,feb,mar,apr,may]}
```
เพิ่มเฉพาะ creator ที่ GMV > 1,000 บาท เพื่อไม่ให้ array ใหญ่เกินไป

**ตรวจ KPI ใน Affiliate Dashboard header ด้วย:**
- `af-kpi-gmv` = GMV รวมทุกเดือน
- `af-kpi-net` = Net GMV รวม
- `af-kpi-comm` = ค่าคอมรวม + avg %
- `af-kpi-best` = เดือนที่ net GMV สูงสุด

**Hardcoded ใน Mobile (mks-grid):**
```html
<div class="mks-val">฿XXX K</div>  <!-- Affiliate GMV ล่าสุด -->
```

---

---

## Step 8B-2 — Affiliate สินค้า Tab: ครีเอเตอร์/วีดีโอ รายสินค้า (จากไฟล์ Export)

ข้อมูล `cr` (ครีเอเตอร์ที่มียอดขาย) และ `vid` (วีดีโอ) รายสินค้ามาจาก **ไฟล์ Export ของ tab สินค้า** ที่โหลดมาไว้ใน `Data Affiliate/สินค้า/` — ห้ามใช้ Chrome DOM scraping

```bash
ls -lt "/sessions/hopeful-serene-fermi/mnt/All/Data Affiliate/สินค้า/"
```

```python
import pandas as pd, glob, os

PROD_DIR = '/sessions/hopeful-serene-fermi/mnt/All/Data Affiliate/สินค้า/'
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
    cols = {str(c).lower(): i for i, c in enumerate(df_prod.columns)}
    
    prod_data = {}
    for _, row in df_prod.iterrows():
        name = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ''
        if not name or name == 'nan': continue
        cr_val = 0
        vid_val = 0
        for col_name, col_idx in cols.items():
            if 'ครีเอเตอร์' in col_name and ('ขาย' in col_name or 'active' in col_name):
                cr_val = int(pd.to_numeric(row.iloc[col_idx], errors='coerce') or 0)
            elif 'วีดีโอ' in col_name or 'video' in col_name:
                vid_val = int(pd.to_numeric(row.iloc[col_idx], errors='coerce') or 0)
        prod_data[name] = {'cr': cr_val, 'vid': vid_val}
    
    print(f"Products found: {list(prod_data.items())[:5]}")
```

**Product name → PRODUCTS[].name mapping (fuzzy keyword):**
| Keyword ใน TikTok name | PRODUCTS[].name |
|---|---|
| Leather | WIBWUB Refresh Leather Wipes |
| interior wipe (case-insensitive) | WIBWUB Interior wipes |
| Sugar | WIBWUB Sugar |
| CLEANER | WIBWUB CLEANER |
| Interior (ไม่มี "wipe") | WIBWUB Interior |
| Refresh (ไม่มี "Leather") | WIBWUB Refresh |
| Visible | WIBWUB Visible |

สินค้าที่ไม่ปรากฏในไฟล์ (ไม่มียอดเดือนนี้) → ใส่ `cr:0, vid:0`

**อัปเดต `PRODUCTS` array ใน `WIBWUB_Affiliate_Dashboard.html`:**
- แก้เฉพาะ `cr` และ `vid` fields — ห้ามแก้ gmv, units, monthly, ret
- ค่าเป็น snapshot ของเดือนปัจจุบัน (จะถูก overwrite ทุกรอบ)

**ตรวจ KPI strip สินค้า tab ด้วย (hardcoded):**
- `ผ่าน X,XXX creators` = รวม cr ของทุกสินค้าที่มี cr > 0

**หมายเหตุ:** ถ้ายังไม่มีไฟล์ใน `Data Affiliate/สินค้า/` → ข้ามขั้นตอนนี้ โดยไม่ต้องใช้ Chrome scraping ทดแทน ไฟล์จะถูกโหลดโดย task `wibwub-thursday-affiliate` ที่รันทุกวัน 09:30 และ 19:30

---

## Step 8B-3 — Affiliate วีดีโอ Tab: อัปเดต VIDEOS array

ไฟล์ export วีดีโออยู่ใน `Data Affiliate/วีดีโอ/` — ใช้อัปเดต monthly GMV ใน `VIDEOS` array และเพิ่มวีดีโอใหม่ที่ยังไม่มีใน array

```bash
ls -lt "/sessions/hopeful-serene-fermi/mnt/All/Data Affiliate/วีดีโอ/"
```

```python
import pandas as pd, glob, os, re

VID_DIR = '/sessions/hopeful-serene-fermi/mnt/All/Data Affiliate/วีดีโอ/'
vid_files = sorted(glob.glob(VID_DIR + '*.xlsx'), key=os.path.getmtime, reverse=True)
if not vid_files:
    print("WARNING: ไม่พบไฟล์ในโฟลเดอร์วีดีโอ — ข้ามขั้นตอนนี้")
else:
    df_vid = pd.read_excel(vid_files[0], header=None)
    
    # หา header row
    header_idx = 0
    for i, row in df_vid.iterrows():
        row_str = ' '.join(str(v) for v in row.values if pd.notna(v))
        if 'วีดีโอ' in row_str or 'GMV' in row_str or 'video' in row_str.lower():
            header_idx = i
            break
    
    df_vid = pd.read_excel(vid_files[0], header=header_idx)
    print(f"Columns: {list(df_vid.columns)}")
    
    # Parse: ต้องการ vid_id, creator, product, GMV สำหรับเดือนปัจจุบัน
    def parse_num(val):
        if val is None or str(val).strip() in ('','None','nan'): return 0
        return int(float(str(val).replace(',','').replace('฿','').strip() or 0))
    
    vid_data = []
    for _, row in df_vid.iterrows():
        row_vals = row.values.tolist()
        if not any(row_vals): continue
        
        # หา vid_id จาก URL หรือ column ที่มีเลข 19 หลัก
        vid_id = ''
        creator = ''
        product = ''
        gmv = 0
        
        for val in row_vals:
            s = str(val) if pd.notna(val) else ''
            # ดึง video ID จาก TikTok URL หรือตัวเลข 19 หลัก
            m = re.search(r'\b(\d{19})\b', s)
            if m: vid_id = m.group(1)
            # URL pattern
            mu = re.search(r'video/(\d+)', s)
            if mu: vid_id = mu.group(1)
        
        # columns ตาม index (ตรวจด้วย print Columns ด้านบน)
        cols_lower = {str(c).lower(): i for i, c in enumerate(df_vid.columns)}
        for col_name, col_idx in cols_lower.items():
            if 'creator' in col_name or 'ครีเอเตอร์' in col_name:
                creator = str(row.iloc[col_idx]) if pd.notna(row.iloc[col_idx]) else ''
            elif 'product' in col_name or 'สินค้า' in col_name:
                product = str(row.iloc[col_idx]) if pd.notna(row.iloc[col_idx]) else ''
            elif 'gmv' in col_name:
                gmv = parse_num(row.iloc[col_idx])
        
        if vid_id and gmv > 0:
            vid_data.append({'vid_id': vid_id, 'creator': creator, 'product': product, 'gmv': gmv})
    
    print(f"Videos found: {len(vid_data)}")
    for v in vid_data[:5]:
        print(f"  {v['creator']} | {v['product']} | ฿{v['gmv']:,} | {v['vid_id']}")
```

**วิธีอัปเดต VIDEOS array ใน `WIBWUB_Affiliate_Dashboard.html`:**

1. **วีดีโอที่มีอยู่แล้ว** (จับคู่ด้วย `vid_id`) → อัปเดต `monthly.{month_key}` ด้วยยอด GMV ใหม่
2. **วีดีโอใหม่** (ไม่มีใน array) → เพิ่มเป็น entry ใหม่:
   ```js
   {creator:'CREATOR',product:'PRODUCT_FULL_NAME',vid_id:'VID_ID',caption:'',
    gmv:GMV_TOTAL,units:0,date:'มิ.ย.',
    monthly:{mar:0,apr:0,may:0,jun:GMV_THIS_MONTH}},
   ```
3. Product name mapping (ใช้ fuzzy match กับ PRODUCTS[].name เหมือน Step 8B-2)

**ตรวจ KPI strip วีดีโอ tab ด้วย (hardcoded):**
- `วีดีโอที่บันทึก N` = len(VIDEOS)
- `Top Video GMV` = max GMV video (เดือนปัจจุบัน)
- `Avg GMV/Video` = mean GMV ทุกวีดีโอ

---

## Step 8B-4 — Affiliate ไลฟ์สตรีม Tab: เก็บข้อมูล + แสดง KPI

```bash
ls -lt "/sessions/hopeful-serene-fermi/mnt/All/Data Affiliate/ไลฟ์สตรีม/"
```

```python
LIVE_DIR = '/sessions/hopeful-serene-fermi/mnt/All/Data Affiliate/ไลฟ์สตรีม/'
live_files = sorted(glob.glob(LIVE_DIR + '*.xlsx'), key=os.path.getmtime, reverse=True)
if not live_files:
    print("WARNING: ไม่พบไฟล์ ไลฟ์สตรีม — ข้ามขั้นตอนนี้")
else:
    df_live = pd.read_excel(live_files[0], header=None)
    # หา header row เหมือนเดิม
    header_idx = 0
    for i, row in df_live.iterrows():
        row_str = ' '.join(str(v) for v in row.values if pd.notna(v))
        if 'GMV' in row_str or 'ไลฟ์' in row_str or 'live' in row_str.lower():
            header_idx = i; break
    df_live = pd.read_excel(live_files[0], header=header_idx)
    print(f"Columns: {list(df_live.columns)}")
    print(df_live.head(3).to_string())
    
    # ดึง GMV รวมไลฟ์ + จำนวน session (ใช้ print ข้างต้นระบุ column ก่อน)
```

**Affiliate Dashboard ปัจจุบัน ยังไม่มี tab ไลฟ์สตรีม** — เมื่อดาวน์โหลดไฟล์ครั้งแรก ให้:
1. Print columns และ 5 แถวแรกเพื่อทำความเข้าใจ format
2. ดึง: total live GMV, จำนวน session, top creator by live GMV
3. อัปเดต KPI overview strip (tab-overview) เพิ่ม Live GMV ถ้ายังไม่มี
4. หรือรายงาน format ให้ user ตัดสินใจว่าจะเพิ่ม tab ไลฟ์สตรีมหรือไม่

**กฎ:** อย่าข้ามไฟล์นี้เงียบๆ — ถ้ามีไฟล์ให้อ่านและรายงาน format + summary ให้ user เสมอ แม้จะยังไม่มี section แสดงผลก็ตาม

## Step 8C — Social Media Followers

**แหล่งข้อมูล TikTok:** https://docs.google.com/spreadsheets/d/1OWZGQD1wHvIlLAAg_7rJ0CtL-X9vEx4py-cRp_e3NvQ/edit?gid=1242793042
(fileId = `1OWZGQD1wHvIlLAAg_7rJ0CtL-X9vEx4py-cRp_e3NvQ`)

แท็บที่ใช้: **"การวิเคราะห์"** (TikTok Analytics)
- คอลัมน์ `ผู้ติดตามสุทธิ` = net new followers per month
- คอลัมน์ `ยอดการดูโพสท์` = total views per month
- คอลัมน์ `ถูกใจ` = likes per month

**วิธีคำนวณยอด Followers สะสม:**
ยอดสะสมเดือน N = ยอดเริ่มต้น + Σ(ผู้ติดตามสุทธิ ม.ค. → เดือน N)
→ ใส่ใน `soc_follow` chart เป็นหน่วย K (เช่น 130000 → 130)

**ไฟล์ที่ต้องอัปเดต:**

1. **WIBWUB_Dashboard.html** — แก้ datasets ใน `new Chart('soc_follow',...)`:
```javascript
{label:'TikTok', data:[116,120,124,128,130], ...}     // ← อัปเดตตัวเลข
{label:'Facebook', data:[58,59,61,63,64], ...}         // ← ถ้ามีข้อมูล FB ใหม่
{label:'Instagram', data:[35,36,37,38,39], ...}        // ← ถ้ามีข้อมูล IG ใหม่
```

2. **WIBWUB_Mobile.html** — แก้ hardcoded KPI ใน mks-grid:
```html
<div class="mks-val">130K</div>    <!-- TK Followers เดือนล่าสุด -->
<div class="mks-sub">+14K จาก ม.ค.</div>  <!-- delta จาก ม.ค. -->
```
→ ตัวเลข `+XK จาก ม.ค.` = ผลรวม ผู้ติดตามสุทธิ ม.ค.–เดือนปัจจุบัน

**หมายเหตุ:** ถ้าชีตมีแท็บ Facebook / Instagram แยก ให้อ่านยอด followers รวมรายเดือนจากแต่ละแท็บ แล้วอัปเดต datasets ที่เกี่ยวข้องด้วย

---

## Step 8D — Platform Analytics Dashboard (WIBWUB_Platform_Analytics.html)

Dashboard นี้แสดง Top Products จากทุก 5 platform รวมถึง "Other" channels จาก Shipnity
ข้อมูลมาจาก raw order files โดยตรง — **ไม่ใช่ Google Sheets**

### แหล่งข้อมูลและ format

| Platform | ไฟล์ | Format พิเศษ |
|---|---|---|
| Shopee | `data ยอดขาย plaform/shopee/*.zip` → แต่ละ zip มี xlsx | shared strings ใน sheet2.xml, dedup ด้วย (order_id, sku) |
| TikTok | `data ยอดขาย plaform/tiktok shop/*.xlsx` | inlineStr, **sheet2.xml**, each cell = separate `<row>` element |
| Lazada | `data ยอดขาย plaform/Lazada/*.xlsx` (~87MB) | inlineStr, sheet1.xml |
| Line My Shop | `data ยอดขาย plaform/Line my shop/Order Report *.xlsx` | ECMA-376 Agile encrypted |
| Shipnity Other | `Data Shipnity/` (product-level files เท่านั้น) | col[15] channel filter |

### Line My Shop — Decrypt Logic (ECMA-376 Agile Encryption)

Password: **`5000113570`** (ชื่อโฟลเดอร์ Line my shop)

```python
import struct, hashlib, base64, zipfile, io
import xml.etree.ElementTree as ET
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypt_xlsx(filepath, password="5000113570"):
    """Full ECMA-376 Agile Encryption decryptor. Returns bytes of decrypted xlsx."""
    def read_ole(data, sn):
        # OLE2 compound document parser
        ss = 1 << struct.unpack_from('<H', data, 30)[0]
        mss = 1 << struct.unpack_from('<H', data, 32)[0]
        rds = struct.unpack_from('<I', data, 48)[0]
        msc = struct.unpack_from('<I', data, 56)[0]
        fat_s = [s for s in struct.unpack_from('<109I', data, 76) if s < 0xFFFFFFFC]
        fat = []
        for s in fat_s:
            fat += list(struct.unpack_from(f'<{ss//4}I', data, (s+1)*ss))
        def rc(s):
            r = b''
            while s < 0xFFFFFFFC:
                r += data[(s+1)*ss:(s+2)*ss]
                s = fat[s] if s < len(fat) else 0xFFFFFFFE
            return r
        dd = rc(rds)
        entries = {}
        for i in range(len(dd)//128):
            e = dd[i*128:(i+1)*128]
            nl = struct.unpack_from('<H', e, 64)[0]
            if not nl: continue
            name = e[:nl-2].decode('utf-16-le', errors='ignore')
            entries[name] = (struct.unpack_from('<I', e, 116)[0], struct.unpack_from('<I', e, 120)[0])
        ms_s = struct.unpack_from('<I', dd[:128], 116)[0]
        ms = rc(ms_s) if ms_s < 0xFFFFFFFC else b''
        mfs = struct.unpack_from('<I', data, 60)[0]
        mf = []
        if mfs < 0xFFFFFFFC:
            mfd = rc(mfs)
            mf = list(struct.unpack_from(f'<{len(mfd)//4}I', mfd))
        def rm(s, sz):
            r = b''
            while s < 0xFFFFFFFC:
                r += ms[s*mss:(s+1)*mss]
                s = mf[s] if s < len(mf) else 0xFFFFFFFE
            return r[:sz]
        if sn in entries:
            s, sz = entries[sn]
            return rm(s, sz) if sz < msc and ms else rc(s)[:sz]
        return None

    with open(filepath, 'rb') as f:
        raw = f.read()

    ei = read_ole(raw, 'EncryptionInfo')
    rx = ET.fromstring(ei[8:])
    ns = {'e': 'http://schemas.microsoft.com/office/2006/encryption',
          'p': 'http://schemas.microsoft.com/office/2006/keyEncryptor/password'}
    kd = rx.find('e:keyData', ns)
    pe = rx.find('.//p:encryptedKey', ns)
    ds  = base64.b64decode(kd.get('saltValue'))   # data salt
    kb  = int(kd.get('keyBits'))                  # AES-128 = 128
    es  = base64.b64decode(pe.get('saltValue'))   # encryptedKey salt
    sc  = int(pe.get('spinCount'))                # 100000 iterations
    ekv = base64.b64decode(pe.get('encryptedKeyValue'))
    pkb = int(pe.get('keyBits'))

    # Key derivation (SHA-1 based, sc spin rounds, then block key)
    h = hashlib.sha1(es + password.encode('utf-16-le')).digest()
    for i in range(sc):
        h = hashlib.sha1(struct.pack('<I', i) + h).digest()

    # Block key for encryptedKeyValue
    ENC_KEY_BLOCK = bytes([0x14, 0x6e, 0x0b, 0xe7, 0xab, 0xac, 0xd0, 0xd6])
    k = hashlib.sha1(h + ENC_KEY_BLOCK).digest()[:pkb//8]

    def aes_decrypt(key, iv, ct):
        ct += b'\x00' * ((-len(ct)) % 16)
        d = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()).decryptor()
        return d.update(ct) + d.finalize()

    # Decrypt the actual AES key
    ak = aes_decrypt(k, es, ekv)[:kb//8]

    # Decrypt package (4096-byte segments)
    ep  = read_ole(raw, 'EncryptedPackage')
    psz = struct.unpack_from('<Q', ep, 0)[0]
    epd = ep[8:]
    dec = b''
    for i in range(0, len(epd), 4096):
        iv = hashlib.sha1(ds + struct.pack('<I', i//4096)).digest()[:16]
        dec += aes_decrypt(ak, iv, epd[i:i+4096])
    return dec[:psz]

# Usage: ใช้ผล decrypt เป็น in-memory xlsx
decrypted_bytes = decrypt_xlsx(filepath)
wb = openpyxl.load_workbook(io.BytesIO(decrypted_bytes), read_only=True, data_only=True)
```

**Line My Shop columns (0-indexed):**
- col[1] = order_id
- col[3] = order_date ("YYYYMMDD HH:MM")
- col[22] = SKU (รหัสสินค้า)
- col[28] = product_name
- col[20] = price
- col[31] = qty
- col[39] = order_status

**Files:**
- `Order Report 20260616.xlsx` = ม.ค.–มี.ค. 2026 (1874 rows)
- `Order Report 20260616 (1).xlsx` = เม.ย.–มิ.ย. 2026 (1632 rows)

### Shipnity Channel Filter (Other)

```python
KEEP_CHANNELS = {"facebook", "FACEBOOK", "LINE_OA", "Carcare", "WEBSITE", "POS"}

# ข้าม channels เหล่านี้ (ใช้ platform files แทน):
# shopee, tiktok, lazada, line_shopping, เบิกของ, สินค้าสำหรับทำการตลาด
# ข้ามไฟล์ order-level (col[1] ว่าง หรือเป็น numeric)
```

### SKU Merge Strategy

SKU canonical ใช้ Shipnity เป็น master:
- **TikTok, Lazada, Line My Shop**: ใช้ Seller SKU ตรงๆ (match 100% กับ Shipnity SKU)
- **Shopee**: Parent SKU อาจว่าง หรือไม่ตรงทั้งหมด → fallback เป็น `SH_NAME_{product_name}`
- SKU format: ตัวอักษรใหญ่ตามด้วยตัวเลข เช่น `BWLD000001`, `SSUG010024`

### Aggregation Script

Script หลัก: `aggregate_all_v2.py` (เก็บใน sandbox outputs directory เท่านั้น)

```bash
# รัน script ใน subagent (ใช้เวลา > 45 วินาที sandbox timeout):
# spawn subagent พร้อม script path แทนที่จะรันตรงใน bash
```

Output: `products_combined.json`
```json
{
  "products": [
    {
      "sku": "BWLD000001",
      "name": "ไม้ปัดฝุ่นขนแกะแท้ (WIBWUB Wool Duster)",
      "total_rev": 4920382.0,
      "by_platform": {
        "Shopee":     {"total": 3052068.0, "monthly": {"01": 450000, "02": 380000, ...}},
        "TikTok":     {"total": 416654.0,  "monthly": {...}},
        "Lazada":     {"total": 39477.0,   "monthly": {...}},
        "LineMyShop": {"total": 105434.0,  "monthly": {...}},
        "Other":      {"total": 1306749.0, "monthly": {...}}
      }
    },
    ...
  ],
  "summary": {
    "total_revenue": 61426343.0,
    "by_platform": {
      "Shopee": 44100000.0,
      "Other":  8000000.0,
      "TikTok": 6500000.0,
      "LineMyShop": 2100000.0,
      "Lazada": 670000.0
    }
  }
}
```

### อัปเดต WIBWUB_Platform_Analytics.html

ไฟล์นี้มี JS arrays โดยตรงใน `<script>` block:

```javascript
// Platform overview arrays (6 months: Jan–Jun)
const LMS_REV = [289886,441204,401837,348105,379012,250745];
const LMS_ORD = [279,407,279,316,303,228];
const TOTAL_REV = 27522789;   // Shopee+TikTok+Lazada+LMS net (ไม่รวม Other)

// PRODUCTS array (top ~30 by total revenue, sorted desc)
const PRODUCTS = [
  {sku:"BWLD000001", n:"ชื่อสินค้า", t:TOTAL, s:SHOPEE, k:TIKTOK, l:LAZADA, lms:LMS, oth:OTHER},
  ...
];
```

**สิ่งที่ต้องอัปเดตเมื่อมีไฟล์ใหม่:**
1. รัน `aggregate_all_v2.py` ใหม่ (ผ่าน subagent) → ได้ `products_combined.json` ใหม่
2. อ่าน top 30 products จาก JSON
3. อัปเดต `PRODUCTS` array ใน HTML (ตัวเลข `t`, `s`, `k`, `l`, `lms`, `oth`)
4. อัปเดต `LMS_REV`, `LMS_ORD` จาก Line My Shop files ใหม่
5. อัปเดต `TOTAL_REV` = Shopee+TikTok+Lazada+LMS net รวม
6. อัปเดต `TOTAL_REV` hardcoded ใน `<div class="kpi-val">` (header KPIs)
7. อัปเดต footer date: "ข้อมูล ณ วันที่ DD เดือน YYYY"

**กฎ:** ตัวเลขใน PRODUCTS ใช้ยอด gross revenue จาก platform files (ไม่ใช่ net)
`TOTAL_REV` ใน header KPI = net revenue จาก Google Sheets (ตรงกับ SH_REV+TK_REV+LZ_REV+LMS_REV)

---

## Step 9 — Sales_Dashboard date_max

```bash
sed -i 's/"date_max":"OLD_DATE"/"date_max":"NEW_DATE"/' \
  "/sessions/hopeful-serene-fermi/mnt/All/Data Shipnity/Sales_Dashboard.html"
```

---

## Step 10 — pointRadius Check

Search "pointRadius" ทุกจุดในไฟล์ ตรวจว่าความยาว = จำนวนเดือน:
5 เดือน = [3,3,3,3,6]   6 เดือน = [3,3,3,3,3,6]

---

## Step 11 — Bump Service Worker

const CACHE = 'wibwub-vN';  // +1 ทุกครั้ง

---

## Step 12 — Verification Checklist

- [ ] Shopee/TikTok/Lazada arrays ตรงกันทั้ง Mobile + Web Dashboard
- [ ] TikTok/Lazada values มาจาก row สุดท้ายของ Google Sheet
- [ ] CHANNELS cumulative totals อัปเดต
- [ ] ALL_PRODUCTS รวมไฟล์ใหม่สุดจาก Step 0 แล้ว
- [ ] Top Products chart + table ใน Web Dashboard อัปเดต
- [ ] Hardcoded KPI text อัปเดตทุกจุด
- [ ] pointRadius ทุก array ยาวตรงกับ data
- [ ] Ads Dashboard: may + all + button labels อัปเดต
- [ ] Sales_Dashboard date_max อัปเดต
- [ ] TikTok clips อัปเดตทั้ง Mobile + TikTok Dashboard
- [ ] sw.js cache bumped +1
- [ ] Affiliate arrays ตรงกันทั้ง Affiliate Dashboard + Mobile (gmvD=AFI_GMV, netD=AFI_NET, commD=AFI_COMM)
- [ ] Social Media followers อัปเดตใน Dashboard (soc_follow chart) + Mobile (hardcoded KPI)
- [ ] TK Followers hardcoded text ใน Mobile (mks-val + mks-sub) ตรงกับ data
- [ ] Platform Analytics: PRODUCTS array อัปเดตจาก products_combined.json ใหม่
- [ ] Platform Analytics: LMS_REV/LMS_ORD + TOTAL_REV อัปเดต
- [ ] Platform Analytics: footer date อัปเดต
- [ ] ไม่มี JS syntax errors

---

## Step 13 — Git Push

```bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock
git add WIBWUB_Mobile.html WIBWUB_Dashboard.html WIBWUB_Affiliate_Dashboard.html \
        WIBWUB_TikTok_Dashboard_v7.html "data Ads/WIBWUB_Ads_Dashboard.html" \
        "Data Shipnity/Sales_Dashboard.html" WIBWUB_Platform_Analytics.html sw.js
git commit -m "update: sync data [DATE] — [description]"
git push
```
