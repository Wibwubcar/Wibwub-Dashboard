#!/usr/bin/env python3
"""
diag_investigate.py — วินิจฉัยปัญหา:
1/2. Sales (Shopee/Lazada/TikTok) เดือนนี้ไม่ขึ้น + มิ.ย. หายเป็น 0
3/4. Affiliate เดือนนี้ไม่ขึ้น + ยอดรายครีเอเตอร์ไม่ตรง
5. สต๊อกไม่ตรงปัจจุบัน
ไม่แก้ไขไฟล์ใดๆ — อ่านอย่างเดียว
"""
import sys, os, re, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wibwub_update as w

print("="*70)
print("PART A — SALES SHEETS RAW DIAGNOSIS")
print("="*70)

sheets = w.read_sheets()

def show_sheet(name, ncols=12):
    rows = sheets.get(name, [])
    print(f"\n--- {name}: {len(rows)} rows total ---")
    print("Last 15 rows (col0 + col1..col3):")
    for row in rows[-15:]:
        if not row: continue
        c0 = row[0] if len(row) > 0 else ''
        c1 = row[1] if len(row) > 1 else ''
        c2 = row[2] if len(row) > 2 else ''
        print(f"  [{c0!r}] {c1!r} | {c2!r}")

    # replicate extract() regex logic, WITHOUT year filter, to see ALL keys found
    monthly = {}
    unmatched_recent = []
    for row in rows:
        if not row: continue
        d = str(row[0]).strip()
        m = re.match(r'01-(?:2[89]|3[01])/(\d{2})/(\d{2})$', d)
        if not m:
            m = re.match(r'01-\d{2}/(\d{2})/(\d{2})$', d)
            if not m:
                if d and re.search(r'\d{2}/\d{2}', d):
                    unmatched_recent.append(d)
                continue
        key = f'{m.group(1)}/{m.group(2)}'
        monthly[key] = row
    print(f"  Extracted month-keys (ALL years, no filter): {sorted(monthly.keys())}")
    if unmatched_recent:
        print(f"  แถวที่มี date-like text แต่ regex ไม่ match (โชว์ 10 ล่าสุด): {unmatched_recent[-10:]}")

for nm in ['shopee', 'lazada', 'tiktok']:
    show_sheet(nm)

current_yr = datetime.datetime.now().strftime('%y')
print(f"\ncurrent_yr filter ที่สคริปต์ใช้ = '{current_yr}' (ปีนี้ ค.ศ. {datetime.datetime.now().year})")

print("\n" + "="*70)
print("PART B — AFFILIATE FILE SELECTION DIAGNOSIS")
print("="*70)

AFI_DIR = w.BASE / 'Data Affiliate'
all_files = []
for root, _dirs, files in os.walk(AFI_DIR):
    for f in files:
        if f.endswith('.xlsx') and not f.startswith(('~', '.')) and 'Creator_List' in f:
            all_files.append(str(w.Path(root) / f))

def detect_mi(fname):
    m = re.search(r'(20\d{2})(\d{2})\d{2}', fname)
    if m:
        i = (int(m.group(1)) - 2025) * 12 + (int(m.group(2)) - 11)
        return i if i >= 0 else None
    return None

def idx_to_label(i):
    TH_ABBR = {1:'มค',2:'กพ',3:'มีนา',4:'เมษา',5:'พค',6:'มิย',
               7:'กค',8:'สค',9:'กย',10:'ตค',11:'พย',12:'ธค'}
    mo = (10 + i) % 12 + 1
    yr = 2025 + (10 + i) // 12
    return f'{TH_ABBR[mo]}.{(yr + 543) % 100:02d}'

by_month = {}
for fp in all_files:
    fname = os.path.basename(fp)
    mi = detect_mi(fname)
    by_month.setdefault(mi, []).append(fname)

print("ไฟล์ Creator_List ทั้งหมด แยกตามเดือนที่ detect ได้ (mi=index, ดูว่ามีไฟล์เดือนปัจจุบัน ก.ค. หรือไม่):")
for mi in sorted(k for k in by_month if k is not None):
    label = idx_to_label(mi)
    print(f"  mi={mi} ({label}): {len(by_month[mi])} ไฟล์")
    for fn in sorted(by_month[mi]):
        print(f"      - {fn}")
if None in by_month:
    print(f"  detect_mi ล้มเหลว (ไม่รู้เดือน) {len(by_month[None])} ไฟล์: {by_month[None]}")

today = datetime.date.today()
this_mi = (today.year - 2025) * 12 + (today.month - 11)
print(f"\nวันนี้ {today} → เดือนปัจจุบันควรเป็น mi={this_mi} ({idx_to_label(this_mi)})")
print(f"มีไฟล์สำหรับเดือนนี้หรือไม่: {'มี' if this_mi in by_month else 'ไม่มี — นี่คือสาเหตุที่เดือนนี้ไม่ขึ้น Dashboard'}")

print("\n" + "="*70)
print("PART C — STOCK / PROCUREMENT DIAGNOSIS")
print("="*70)
snap_path = w.BASE / 'Data Shipnity' / 'Stock' / 'stock_snapshot.json'
if snap_path.exists():
    mtime = datetime.datetime.fromtimestamp(snap_path.stat().st_mtime)
    print(f"stock_snapshot.json แก้ไขล่าสุด: {mtime}")
    with open(snap_path, encoding='utf-8') as f:
        raw = json.load(f)
    plist = raw['products'] if isinstance(raw, dict) and 'products' in raw else raw
    print(f"จำนวน SKU ใน snapshot: {len(plist)}")
    for p in plist[:3]:
        print(f"  ตัวอย่าง: {p}")
else:
    print(f"ไม่พบ {snap_path}")

dash_path = w.BASE / 'Procurement_Dashboard.html'
if dash_path.exists():
    html = dash_path.read_text(encoding='utf-8')
    m = re.search(r'const PRODUCTS = (\[.*?\]);', html, re.DOTALL)
    if m:
        products = json.loads(m.group(1))
        print(f"\nProcurement_Dashboard.html PRODUCTS: {len(products)} SKU")
        for p in products[:3]:
            print(f"  ตัวอย่าง: {p}")
    badge = re.search(r'อัปเดต[^<\"]{0,30}', html)
    if badge: print(f"badge: {badge.group(0)}")

print("\n" + "="*70)
print("DONE — ไม่มีการแก้ไขไฟล์ใดๆ ในการรันนี้")
print("="*70)
