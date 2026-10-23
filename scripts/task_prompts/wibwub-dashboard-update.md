---
name: wibwub-dashboard-update
description: อัปเดต WIBWUB Dashboard ทั้งหมด (Sales + Affiliate + TikTok + Ads) จาก Google Sheets ทุกวัน 09:00 และ 18:00 น.
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

## WIBWUB Dashboard Auto-Update Task

อัปเดต HTML Dashboard ทั้งหมดจาก Google Sheets + Excel files ทุกเที่ยง/เที่ยงคืน
ห้าม spawn subagents — ทำทุกอย่างใน Python/bash โดยตรง

---

## STEP 0 — หา paths (ทำก่อนทุกอย่าง)
```bash
ALL_MNT="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
OUTPUTS="/Users/thanasablilutanon/Library/Caches/wibwub-outputs"; mkdir -p "$OUTPUTS"
echo "ALL_MNT=$ALL_MNT"
echo "OUTPUTS=$OUTPUTS"
ls "$ALL_MNT" 2>/dev/null | head -20
```

**ถ้า ALL_MNT ว่าง = Google Drive ยังไม่ mount — ให้หยุดทันที อย่า fallback ไป Downloads เด็ดขาด**

## STEP 1 — ดาวน์โหลด Google Sheets

Call mcp__631cf5b2-d348-4eff-a244-06b07fea56f7__read_file_content สำหรับแต่ละ fileId:
- Shopee Sales: 10LrzWB8bbCO9FigCQFz5gZ3iSXMVhK0S → $OUTPUTS/shopee.txt
- TikTok Sales: 1k22c3PGY6aQjygAX6df_rQLR8aTzL-iz → $OUTPUTS/tiktok_sales.txt
- Lazada Sales: 1FxLAUiwabmNcBc3TA-bpHqg2MSK7uJ4U → $OUTPUTS/lazada.txt
- TikTok Content: 1OWZGQD1wHvIlLAAg_7rJ0CtL-X9vEx4py-cRp_e3NvQ → $OUTPUTS/tiktok_content.txt

จัดการ response:
- กรณี A (มี fileContent ใน response): เขียนลง txt โดยตรง
- กรณี B ("saved to /var/folders/..."): Read ไฟล์นั้น → json.load(f)['fileContent'] → เขียนลง txt

**หมายเหตุ:** Affiliate ไม่ได้ดาวน์โหลดจาก Google Sheets แล้ว — อ่านจาก xlsx ใน Data Affiliate/ โดยตรง (STEP 2 PART B)

## STEP 2 — Process Python (Sales + Affiliate + TikTok Content)

```python
import re, json, os, csv, io, datetime
from collections import defaultdict

import subprocess
ALL_MNT = "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
OUTPUTS = "/Users/thanasablilutanon/Library/Caches/wibwub-outputs"
if not OUTPUTS: OUTPUTS = '/tmp'

# ตรวจ ALL_MNT ก่อน — ถ้าไม่มีให้หยุด
if not ALL_MNT or not os.path.exists(ALL_MNT):
    print('ERROR: ALL_MNT not found — Google Drive may not be mounted. Stopping.')
    exit(1)

def parse_num(s):
    if not s: return 0
    try: return float(re.sub(r'[฿,\s%]','',str(s)))
    except: return 0

# PART A: SALES DATA
shopee_monthly = {}
with open(f'{OUTPUTS}/shopee.txt') as f: text = f.read()
for m in re.finditer(r'01-(?:28|29|30|31)/(\d{2}/\d{2}),([\d,]+),([\d,]+\.?\d*),([\d,]+\.?\d*),[\d,]*\.?\d*,([\d.]+),([\d,]+),([\d,]+),([\d,]+),([\d,]+),([\d.]+)', text):
    key = m.group(1)
    shopee_monthly[key] = {'rev':parse_num(m.group(2)),'ads':parse_num(m.group(3)),'fee':parse_num(m.group(4)),'cancel_pct':float(m.group(5)),'ord':parse_num(m.group(8)),'cancel':parse_num(m.group(9))}
for m in re.finditer(r'(0[1-8]/25),([\d,]+),([\d,]+\.?\d*),([\d,]+\.?\d*),[\d,]*\.?\d*,([\d.]+),([\d,]+),([\d,]+),([\d,]+),([\d,]+),([\d.]+)', text):
    key = m.group(1)
    if key not in shopee_monthly:
        shopee_monthly[key] = {'rev':parse_num(m.group(2)),'ads':parse_num(m.group(3)),'fee':parse_num(m.group(4)),'cancel_pct':float(m.group(5)),'ord':parse_num(m.group(8)),'cancel':parse_num(m.group(9))}

tiktok_monthly = {}
with open(f'{OUTPUTS}/tiktok_sales.txt') as f: text = f.read()
for m in re.finditer(r'01-(?:28|29|30|31)/(\d{2}/\d{2}),([\d,]+\.?\d*),([\d,]+\.?\d*),([\d,]+\.?\d*),[\d,]*\.?\d*,([\d.]+),[^,]*,[^,]*,([\d,]+),([\d,]+),([\d.]+)', text):
    key = m.group(1)
    tiktok_monthly[key] = {'rev':parse_num(m.group(2)),'ads':parse_num(m.group(3)),'fee':parse_num(m.group(4)),'cancel_pct':float(m.group(5)),'ord':parse_num(m.group(6)),'cancel':parse_num(m.group(7))}

lazada_monthly = {}
with open(f'{OUTPUTS}/lazada.txt') as f: text = f.read()

ALL_MONTHS = ['01/25','02/25','03/25','04/25','05/25','06/25','07/25','08/25','09/25','10/25','11/25','12/25','01/26','02/26','03/26','04/26','05/26','06/26']
available = [m for m in ALL_MONTHS if m in shopee_monthly]
M_LABELS = {'01':'ม.ค.','02':'ก.พ.','03':'มี.ค.','04':'เม.ย.','05':'พ.ค.','06':'มิ.ย.','07':'ก.ค.','08':'ส.ค.','09':'ก.ย.','10':'ต.ค.','11':'พ.ย.','12':'ธ.ค.'}
YEAR_LABELS = {'25':'68','26':'69'}
def month_label(key):
    mm,yy=key.split('/'); return M_LABELS[mm]+YEAR_LABELS.get(yy,yy)
labels = [month_label(m) for m in available]; n = len(available)
results_sales = {
    'M4': labels,
    'SH_REV':  [int(shopee_monthly.get(m,{}).get('rev',0)) for m in available],
    'SH_ORD':  [int(shopee_monthly.get(m,{}).get('ord',0)) for m in available],
    'SH_CANCEL_PCT': [round(shopee_monthly.get(m,{}).get('cancel_pct',0),2) for m in available],
    'TK_REV':  [round(tiktok_monthly.get(m,{}).get('rev',0),2) for m in available],
    'TK_ORD':  [int(tiktok_monthly.get(m,{}).get('ord',0)) for m in available],
    'TK_CANCEL_PCT': [round(tiktok_monthly.get(m,{}).get('cancel_pct',0),2) for m in available],
    'TK_ADSSPEND': [int(tiktok_monthly.get(m,{}).get('ads',0)) for m in available],
    'TK_FEECOMM': [int(tiktok_monthly.get(m,{}).get('fee',0)) for m in available],
    'LZ_REV':  [int(lazada_monthly.get(m,{}).get('rev',0)) for m in available],
    'LZ_ORD':  [int(lazada_monthly.get(m,{}).get('ord',0)) for m in available],
    'LZ_COST_PCT': [round(lazada_monthly.get(m,{}).get('cost_pct',0),2) for m in available],
    'n_months': n, 'latest_month': labels[-1] if labels else '?'
}
with open(f'{OUTPUTS}/sales_results.json','w') as f: json.dump(results_sales, f, ensure_ascii=False)
print(f"Sales: {n} months, latest={results_sales['latest_month']}")

# PART B: AFFILIATE (อ่านจาก Data Affiliate/ xlsx — Net = GMV − returns จริง ไม่ใช่ copy ของ GMV)
import pandas as pd

AFI_DIR = f'{ALL_MNT}/Data Affiliate'
MONTH_ORDER = ['พย.68','ธค.68','มค.69','กพ.69','มีนา.69','เมษา.69','พค.69']

def detect_month_idx(fname):
    """แปลงชื่อไฟล์ → index ใน MONTH_ORDER (0=พย.68 … 6=พค.69)"""
    fn = fname.lower()
    if 'พย' in fn or 'nov' in fn: return 0
    if 'ธค' in fn or 'dec' in fn: return 1
    if 'มค' in fn or 'jan' in fn: return 2
    if 'กพ' in fn or 'feb' in fn: return 3
    if 'มีนา' in fn or 'mar' in fn: return 4
    if 'เมษา' in fn or 'apr' in fn: return 5
    if 'พค' in fn or 'may' in fn: return 6
    return None

# เก็บ per-creator per-month values
c_gmv  = defaultdict(lambda: [None]*len(MONTH_ORDER))
c_net  = defaultdict(lambda: [None]*len(MONTH_ORDER))
c_comm = defaultdict(lambda: [None]*len(MONTH_ORDER))

if os.path.exists(AFI_DIR):
    xlsx_files = sorted([f for f in os.listdir(AFI_DIR)
                         if f.endswith('.xlsx') and not f.startswith('~') and not f.startswith('.')])
    print(f'Data Affiliate: found {len(xlsx_files)} files: {xlsx_files}')
    for fname in xlsx_files:
        mi = detect_month_idx(fname)
        if mi is None:
            print(f'  WARNING: cannot detect month for {fname} — skipping'); continue
        try:
            df = pd.read_excel(f'{AFI_DIR}/{fname}', header=None)
            rows_read = 0
            for _, row in df.iterrows():
                # col 0=ชื่อ, 1=GMV, 2=returns, 10=commission
                name = str(row.iloc[0]).strip().lstrip('@') if pd.notna(row.iloc[0]) else ''
                if not name or name in ['nan','Creator','ชื่อครีเอเตอร์'] or name.startswith('Unnamed'): continue
                try:
                    gmv  = float(str(row.iloc[1]).replace(',','')) if len(row)>1 and pd.notna(row.iloc[1]) else 0
                    ret  = float(str(row.iloc[2]).replace(',','')) if len(row)>2 and pd.notna(row.iloc[2]) else 0
                    comm = float(str(row.iloc[10]).replace(',','')) if len(row)>10 and pd.notna(row.iloc[10]) else 0
                    net  = gmv - ret
                    if gmv > 0:
                        c_gmv[name][mi]  = int(gmv)
                        c_net[name][mi]  = int(net)
                        c_comm[name][mi] = int(comm)
                        rows_read += 1
                except: pass
            print(f'  {fname} (month idx {mi}={MONTH_ORDER[mi]}): {rows_read} creators')
        except Exception as e:
            print(f'  ERROR reading {fname}: {e}')

    # สร้าง creators list
    creators = []
    for name in set(c_gmv.keys()):
        mn = c_gmv[name]
        total = sum(v for v in mn if v)
        if total == 0: continue
        ma = sum(1 for v in mn if v and v > 0)
        creators.append({'n': name, 't': total, 'ma': ma, 'mn': mn})
    creators.sort(key=lambda x: -x['t'])

    # Aggregate monthly totals — GMV, Net, Commission แยกกัน
    gmvD  = [sum(c_gmv[c['n']][i]  or 0 for c in creators) for i in range(len(MONTH_ORDER))]
    netD  = [sum(c_net[c['n']][i]  or 0 for c in creators) for i in range(len(MONTH_ORDER))]
    commD = [sum(c_comm[c['n']][i] or 0 for c in creators) for i in range(len(MONTH_ORDER))]
    crD   = [sum(1 for c in creators if (c_gmv[c['n']][i] or 0) > 0) for i in range(len(MONTH_ORDER))]
    print(f'Affiliate totals: gmvD={gmvD}')
    print(f'                  netD={netD}')
    print(f'                 commD={commD}')
    print(f'                   crD={crD}')
else:
    print(f'WARNING: Data Affiliate/ not found at {AFI_DIR} — using zeros')
    creators = []
    gmvD = [0]*len(MONTH_ORDER); netD = [0]*len(MONTH_ORDER)
    commD = [0]*len(MONTH_ORDER); crD = [0]*len(MONTH_ORDER)

results_affil = {
    'months': MONTH_ORDER,
    'gmvD': gmvD, 'netD': netD, 'commD': commD, 'crD': crD,
    'creators': creators[:500], 'total_creators': len(creators)
}
with open(f'{OUTPUTS}/affil_results.json','w') as f: json.dump(results_affil, f, ensure_ascii=False)
print(f"Affiliate: {len(creators)} creators saved")

# PART C: TIKTOK CONTENT
with open(f'{OUTPUTS}/tiktok_content.txt') as f: text = f.read()
posts = []; reader2 = csv.reader(io.StringIO(text)); rows2 = list(reader2); hdr = None
for i2, row2 in enumerate(rows2):
    joined = ','.join(row2).lower()
    if ('view' in joined or 'วิว' in joined) and ('pillar' in joined or 'content' in joined):
        hdr = row2; data_start = i2+1; break
if hdr:
    def ci(kws):
        for j,h in enumerate(hdr):
            if any(k in h.lower().strip() for k in kws): return j
        return None
    c_lbl=ci(['วันที่','lbl','date']); c_day=ci(['day of week','dow']); c_month=ci(['month','เดือน'])
    c_pillar=ci(['pillar','category']); c_content=ci(['content','caption']); c_views=ci(['view','วิว'])
    c_eng=ci(['eng','engagement']); c_love=ci(['love','like']); c_comment=ci(['comment'])
    c_share=ci(['share']); c_save=ci(['save']); c_ret=ci(['ret','retention'])
    c_watch=ci(['watch']); c_er=ci(['er','rate']); c_url=ci(['url','tiktok.com'])
    for row2 in rows2[data_start:]:
        if len(row2) < 3: continue
        try:
            post = {'lbl':row2[c_lbl].strip() if c_lbl is not None and c_lbl<len(row2) else '','day':int(row2[c_day]) if c_day is not None and c_day<len(row2) and row2[c_day].strip().isdigit() else 0,'month':int(row2[c_month]) if c_month is not None and c_month<len(row2) and row2[c_month].strip().isdigit() else 0,'pillar':row2[c_pillar].strip() if c_pillar is not None and c_pillar<len(row2) else '','content':row2[c_content].strip() if c_content is not None and c_content<len(row2) else '','views':int(parse_num(row2[c_views])) if c_views is not None and c_views<len(row2) else 0,'eng':int(parse_num(row2[c_eng])) if c_eng is not None and c_eng<len(row2) else 0,'love':int(parse_num(row2[c_love])) if c_love is not None and c_love<len(row2) else 0,'comment':int(parse_num(row2[c_comment])) if c_comment is not None and c_comment<len(row2) else 0,'share':int(parse_num(row2[c_share])) if c_share is not None and c_share<len(row2) else 0,'save':int(parse_num(row2[c_save])) if c_save is not None and c_save<len(row2) else 0,'ret':float(parse_num(row2[c_ret])) if c_ret is not None and c_ret<len(row2) else 0,'watch':float(parse_num(row2[c_watch])) if c_watch is not None and c_watch<len(row2) else 0,'er':float(parse_num(row2[c_er])) if c_er is not None and c_er<len(row2) else 0,'url':row2[c_url].strip() if c_url is not None and c_url<len(row2) and row2[c_url].strip() else '#'}
            if post['views'] > 0 or post['lbl']: posts.append(post)
        except: pass
with open(f'{OUTPUTS}/tiktok_content_results.json','w') as f: json.dump(posts, f, ensure_ascii=False)
print(f"TikTok Content: {len(posts)} posts")
```

## STEP 3 — อัปเดต Main + Mobile + Affiliate + TikTok HTML

```python
import re, json, os, glob, subprocess

ALL_MNT = "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
OUTPUTS = "/Users/thanasablilutanon/Library/Caches/wibwub-outputs"
if not OUTPUTS: OUTPUTS='/tmp'
if not ALL_MNT or not os.path.exists(ALL_MNT):
    print('ERROR: ALL_MNT not found. Stopping.'); exit(1)

# A. Main Dashboard + Mobile — อัปเดตพร้อมกัน (ค่าต้องตรงกันทั้งสองไฟล์)
with open(f'{OUTPUTS}/sales_results.json') as f: d = json.load(f)

def replace_arr(html,name,values,qs=False):
    vs = json.dumps(values,ensure_ascii=False) if qs else '['+','.join(str(v) for v in values)+']'
    return re.sub(rf'(const {re.escape(name)}\s*=\s*)\[.*?\]',rf'\g<1>{vs}',html,flags=re.DOTALL)

SALES_ARRAYS = ['SH_REV','SH_ORD','SH_CANCEL_PCT','TK_REV','TK_ORD','TK_CANCEL_PCT',
                'TK_ADSSPEND','TK_FEECOMM','LZ_REV','LZ_ORD','LZ_COST_PCT']

for fname in ['WIBWUB_Dashboard.html', 'WIBWUB_Mobile.html']:
    fpath = f'{ALL_MNT}/{fname}'
    if not os.path.exists(fpath):
        print(f'⚠️ {fname} not found at {fpath}'); continue
    with open(fpath,'r',encoding='utf-8') as f: html = f.read(); orig = html
    if 'M4' in html:
        html = replace_arr(html,'M4',d['M4'],qs=True)
    for k in SALES_ARRAYS:
        if k in html:
            html = replace_arr(html,k,d[k])
    if html!=orig:
        with open(fpath,'w',encoding='utf-8') as f: f.write(html)
        print(f'✅ {fname} updated ({d["n_months"]} months)')
    else:
        print(f'ℹ️ {fname}: no change in sales arrays')

# B. Affiliate Dashboard
with open(f'{OUTPUTS}/affil_results.json') as f: d = json.load(f)
AFFIL = f'{ALL_MNT}/WIBWUB_Affiliate_Dashboard.html'
if os.path.exists(AFFIL):
    with open(AFFIL,'r',encoding='utf-8') as f: html = f.read(); orig = html
    months = d['months']
    for arr_name, values in [('gmvD',d['gmvD']),('netD',d['netD']),('commD',d['commD']),('crD',d['crD'])]:
        html = re.sub(rf'const {arr_name}\s*=\s*\[.*?\]', f'const {arr_name}=['+','.join(str(v) for v in values)+']', html)
    html = re.sub(r'const months\s*=\s*\[.*?\]', f'const months={json.dumps(months,ensure_ascii=False)}', html)
    raw_entries = []
    for c in d['creators']:
        mn_js = '['+','.join('null' if v is None else str(v) for v in c['mn'])+']'
        raw_entries.append(f'  {{n:"{c["n"]}",t:{c["t"]},ma:{c["ma"]},mn:{mn_js}}}')
    html = re.sub(r'const raw=\[[\s\S]*?\];','const raw=[\n'+',\n'.join(raw_entries)+'\n];',html)
    html = re.sub(r'const bLabels\s*=\s*\[.*?\]',f'const bLabels={json.dumps(["ทั้งหมด"]+months,ensure_ascii=False)}',html)
    if html!=orig:
        with open(AFFIL,'w',encoding='utf-8') as f: f.write(html)
        print(f'✅ Affiliate Dashboard updated ({len(d["creators"])} creators)')
    else:
        print(f'ℹ️ Affiliate Dashboard: no change')
else:
    print(f'⚠️ Affiliate not found at {AFFIL}')

# B2. Mobile — อัปเดต AFI arrays ให้ตรงกับ Affiliate Dashboard (ต้องทำทุกครั้งหลัง B)
MOBILE = f'{ALL_MNT}/WIBWUB_Mobile.html'
if os.path.exists(MOBILE):
    with open(MOBILE,'r',encoding='utf-8') as f: html = f.read(); orig = html
    for arr_name, values in [('AFI_GMV',d['gmvD']),('AFI_NET',d['netD']),('AFI_COMM',d['commD'])]:
        html = re.sub(rf'const {arr_name}\s*=\s*\[.*?\]',
                      f'const {arr_name}=['+','.join(str(v) for v in values)+']', html)
    if html!=orig:
        with open(MOBILE,'w',encoding='utf-8') as f: f.write(html)
        print(f'✅ Mobile AFI_GMV/AFI_NET/AFI_COMM updated')
        print(f'   AFI_GMV={d["gmvD"]}')
        print(f'   AFI_NET={d["netD"]}  ← ตรวจว่า NET ≤ GMV ทุกเดือน')
        print(f'   AFI_COMM={d["commD"]}')
    else:
        print(f'ℹ️ Mobile AFI arrays: no change')
else:
    print(f'⚠️ WIBWUB_Mobile.html not found at {MOBILE}')

# C. TikTok Content
with open(f'{OUTPUTS}/tiktok_content_results.json') as f: posts = json.load(f)
def js_str(v): return "'"+v.replace("'","\\'")+"'" if isinstance(v,str) else str(v)
entries = ['  {'+','.join(f'{k}:{js_str(p[k])}' for k in ['lbl','day','month','pillar','content','views','eng','love','comment','share','save','ret','watch','er','url'])+'}' for p in posts]
new_posts = 'ALL_POSTS = [\n'+',\n'.join(entries)+'\n]'
for TK in glob.glob(f'{ALL_MNT}/**/WIBWUB_TikTok_Dashboard_v7.html', recursive=True) + [f'{ALL_MNT}/WIBWUB_TikTok_Dashboard_v7.html']:
    if not os.path.exists(TK): continue
    with open(TK,'r',encoding='utf-8') as f: html = f.read(); orig = html
    html = re.sub(r'ALL_POSTS\s*=\s*\[[\s\S]*?\]', new_posts, html)
    if html!=orig:
        with open(TK,'w',encoding='utf-8') as f: f.write(html)
        print(f'✅ TikTok updated ({len(posts)} posts): {TK}')
```

## STEP 4 — UPDATE ADS DASHBOARD

```python
import openpyxl, csv, re, json, os, glob, subprocess
from collections import defaultdict

ALL_MNT = "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
ADS_DIR = f'{ALL_MNT}/data Ads'
ADS_HTML = f'{ADS_DIR}/WIBWUB_Ads_Dashboard.html'

if not os.path.exists(ADS_DIR):
    print(f'⚠️ data Ads folder not found at {ADS_DIR}')
else:
    def parse_num(v):
        if v is None: return 0
        try: return float(re.sub(r'[฿,\s%]','',str(v)))
        except: return 0

    shopee_camps = {}; sh_total = {'spend':0,'rev':0,'orders':0,'imp':0,'clicks':0}
    for fp in sorted(glob.glob(f'{ADS_DIR}/ข้อมูล-Shopee-Ads-*.csv')):
        with open(fp, encoding='utf-8-sig') as f: rows = list(csv.reader(f))
        hdr_i = next((i for i,r in enumerate(rows) if len(r)>5 and 'ชื่อโฆษณา' in str(r)), None)
        if hdr_i is None: continue
        for r in rows[hdr_i+1:]:
            if len(r)<25 or not r[1]: continue
            name=r[1].strip(); spend=parse_num(r[24]); rev=parse_num(r[22]); orders=parse_num(r[14])
            imp=parse_num(r[11]); clicks=parse_num(r[12])
            ctr=parse_num(r[13].replace('%','')) if r[13] else 0
            cvr=parse_num(r[16].replace('%','')) if r[16] else 0
            if name not in shopee_camps: shopee_camps[name]={'spend':0,'rev':0,'orders':0,'imp':0,'clicks':0,'ctr_list':[],'cvr_list':[]}
            shopee_camps[name]['spend']+=spend; shopee_camps[name]['rev']+=rev; shopee_camps[name]['orders']+=orders
            shopee_camps[name]['imp']+=imp; shopee_camps[name]['clicks']+=clicks
            if ctr>0: shopee_camps[name]['ctr_list'].append(ctr)
            if cvr>0: shopee_camps[name]['cvr_list'].append(cvr)
            sh_total['spend']+=spend; sh_total['rev']+=rev; sh_total['orders']+=orders; sh_total['imp']+=imp; sh_total['clicks']+=clicks

    sh_roas=sh_total['rev']/sh_total['spend'] if sh_total['spend'] else 0
    sh_ctr=sh_total['clicks']/sh_total['imp']*100 if sh_total['imp'] else 0
    sh_cvr=sh_total['orders']/sh_total['clicks']*100 if sh_total['clicks'] else 0
    sh_cpa=sh_total['spend']/sh_total['orders'] if sh_total['orders'] else 0
    sh_list=[]
    for name,d in shopee_camps.items():
        s=d['spend']; r=d['rev']; o=d['orders']
        roas=r/s if s else 0; cpa=s/o if o else 0
        ctr=sum(d['ctr_list'])/len(d['ctr_list']) if d['ctr_list'] else 0
        cvr=sum(d['cvr_list'])/len(d['cvr_list']) if d['cvr_list'] else 0
        if s>0 or r>0: sh_list.append({'name':name,'spend':round(s),'revenue':round(r),'roas':round(roas,2),'ctr':round(ctr,2),'cvr':round(cvr,2),'cpa':round(cpa)})
    sh_list.sort(key=lambda x:-x['spend'])
    sh_top5=sorted([c for c in sh_list if c['spend']>0],key=lambda x:-x['roas'])[:5]
    sh_worst5=sorted([c for c in sh_list if c['spend']>0],key=lambda x:x['roas'])[:5]

    def read_product(path):
        wb=openpyxl.load_workbook(path,data_only=True); ws=wb.active; camps={}
        for i,row in enumerate(ws.iter_rows(values_only=True)):
            if i==0: continue
            if not row[0]: continue
            name=str(row[0]).strip(); spend=parse_num(row[10]); orders=parse_num(row[11]); rev=parse_num(row[13])
            imp=parse_num(row[15]); clicks=parse_num(row[16])
            ctr_v=(parse_num(row[17]) if row[17] else 0)*100; cvr_v=(parse_num(row[18]) if row[18] else 0)*100
            if name not in camps: camps[name]={'spend':0,'orders':0,'rev':0,'imp':0,'clicks':0,'ctr_list':[],'cvr_list':[]}
            camps[name]['spend']+=spend; camps[name]['orders']+=orders; camps[name]['rev']+=rev
            camps[name]['imp']+=imp; camps[name]['clicks']+=clicks
            if ctr_v>0: camps[name]['ctr_list'].append(ctr_v)
            if cvr_v>0: camps[name]['cvr_list'].append(cvr_v)
        wb.close(); return camps

    def read_live(path):
        wb=openpyxl.load_workbook(path,data_only=True); ws=wb.active; camps={}
        for i,row in enumerate(ws.iter_rows(values_only=True)):
            if i==0: continue
            if not row or not row[3]: continue
            name=str(row[3]).strip(); spend=parse_num(row[5]); orders=parse_num(row[7]); rev=parse_num(row[10])
            if name not in camps: camps[name]={'spend':0,'orders':0,'rev':0,'imp':0,'clicks':0,'ctr_list':[],'cvr_list':[]}
            camps[name]['spend']+=spend; camps[name]['orders']+=orders; camps[name]['rev']+=rev
        wb.close(); return camps

    tk_camps={}
    def merge_into(dst,src):
        for name,d in src.items():
            if name not in dst: dst[name]={'spend':0,'orders':0,'rev':0,'imp':0,'clicks':0,'ctr_list':[],'cvr_list':[]}
            for k in ['spend','orders','rev','imp','clicks']: dst[name][k]+=d.get(k,0)
            dst[name]['ctr_list']+=d.get('ctr_list',[]); dst[name]['cvr_list']+=d.get('cvr_list',[])

    for fp in sorted(glob.glob(f'{ADS_DIR}/creative data for product campaigns*.xlsx')): merge_into(tk_camps, read_product(fp))
    for fp in sorted(glob.glob(f'{ADS_DIR}/livestream data for live campaigns*.xlsx')): merge_into(tk_camps, read_live(fp))

    tk_total={'spend':0,'rev':0,'orders':0,'imp':0,'clicks':0}
    for d in tk_camps.values():
        for k in ['spend','rev','orders','imp','clicks']: tk_total[k]+=d.get(k,0)
    tk_roas=tk_total['rev']/tk_total['spend'] if tk_total['spend'] else 0
    tk_ctr=tk_total['clicks']/tk_total['imp']*100 if tk_total['imp'] else 0
    tk_list=[]
    for name,d in tk_camps.items():
        s=d['spend']; r=d['rev']; o=d['orders']
        roas=r/s if s else 0; cpa=s/o if o else 0
        ctr=sum(d['ctr_list'])/len(d['ctr_list']) if d['ctr_list'] else 0
        cvr=sum(d['cvr_list'])/len(d['cvr_list']) if d['cvr_list'] else 0
        tk_list.append({'name':name,'spend':round(s),'revenue':round(r),'roas':round(roas,2),'ctr':round(ctr,2),'cvr':round(cvr,2),'cpa':round(cpa)})
    tk_list.sort(key=lambda x:-x['spend'])
    tk_top5=sorted([c for c in tk_list if c['spend']>0],key=lambda x:-x['roas'])[:5]
    tk_worst5=sorted([c for c in tk_list if c['spend']>0],key=lambda x:x['roas'])[:5]

    def fmtc(c): return '{'+','.join(f'{k}:{json.dumps(v,ensure_ascii=False) if isinstance(v,str) else v}' for k,v in c.items())+'}'
    with open(ADS_HTML,'r',encoding='utf-8') as f: html=f.read()
    new_block = f"""const DATA = {{
  shopee: {{spend:{round(sh_total['spend'])},revenue:{round(sh_total['rev'])},clicks:{round(sh_total['clicks'])},imp:{round(sh_total['imp'])},orders:{round(sh_total['orders'])},roas:{round(sh_roas,2)},ctr:{round(sh_ctr,2)},cvr:{round(sh_cvr,2)},cpa:{round(sh_cpa)},top5:[{','.join(fmtc(c) for c in sh_top5)}],worst5:[{','.join(fmtc(c) for c in sh_worst5)}],all:[{','.join(fmtc(c) for c in sh_list)}]}},
  tiktok: {{spend:{round(tk_total['spend'])},revenue:{round(tk_total['rev'])},clicks:{round(tk_total['clicks'])},imp:{round(tk_total['imp'])},orders:{round(tk_total['orders'])},roas:{round(tk_roas,2)},ctr:{round(tk_ctr,2)},cvr:{round(tk_cvr,2)},cpa:{round(round(tk_total['spend']/tk_total['orders'],2) if tk_total['orders'] else 0)},top5:[{','.join(fmtc(c) for c in tk_top5)}],worst5:[{','.join(fmtc(c) for c in tk_worst5)}],all:[{','.join(fmtc(c) for c in tk_list)}]}}
}};"""
    html_new = re.sub(r'const DATA\s*=\s*\{[\s\S]*?\};\s*\n\s*const addedEntries', new_block+'\n\nconst addedEntries', html)
    if html_new!=html:
        with open(ADS_HTML,'w',encoding='utf-8') as f: f.write(html_new)
        print(f'✅ Ads Dashboard updated')
    else:
        print('⚠️ Ads Dashboard: no change')
```

## STEP 5 — UPDATE SALES DASHBOARD

```python
import openpyxl, datetime, re, json, os, glob, subprocess
from collections import defaultdict

ALL_MNT = "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
SHIP_DIR = f'{ALL_MNT}/Data Shipnity'
SALES_HTML = f'{SHIP_DIR}/Sales_Dashboard.html'

if not os.path.exists(SHIP_DIR):
    print(f'⚠️ Data Shipnity folder not found at {SHIP_DIR}')
else:
    def parse_date(v):
        if v is None: return None
        if isinstance(v,(datetime.datetime,datetime.date)):
            dt=v if isinstance(v,datetime.datetime) else datetime.datetime.combine(v,datetime.time())
            return dt.strftime('%Y-%m-%d')
        s=str(v).strip()
        for fmt in ['%d/%m/%Y %H:%M','%d/%m/%Y','%Y-%m-%d %H:%M:%S','%Y-%m-%d']:
            try: return datetime.datetime.strptime(s,fmt).strftime('%Y-%m-%d')
            except: pass
        return None

    def parse_num(v):
        if v is None: return 0
        try: return float(re.sub(r'[฿,\s]','',str(v)))
        except: return 0

    CHANNEL_MAP={'tiktok':'TikTok','tiktokshop':'TikTok','shopee':'Shopee','facebook':'Facebook','fb':'Facebook','lazada':'Lazada','line oa':'Line OA','line shopping':'Line Shopping','carcare':'Carcare','marketing':'Marketing','pos':'POS','website':'Website','เบิกของ':'เบิกของ'}
    CHANNELS=["Carcare","Facebook","Lazada","Line OA","Line Shopping","Marketing","POS","Shopee","TikTok","Website","เบิกของ"]
    CH_IDX={c.lower():i for i,c in enumerate(CHANNELS)}
    def norm_channel(raw):
        if not raw: return 'Other'
        r=str(raw).lower().strip()
        return CHANNEL_MAP.get(r,raw.strip())

    files=[f for f in glob.glob(f'{SHIP_DIR}/*.xlsx') if not os.path.basename(f).startswith('~')]
    agg=defaultdict(lambda:{'q':0,'s':0.0}); product_set=set()
    for fp in sorted(files):
        wb=openpyxl.load_workbook(fp,data_only=True); ws=wb.active
        for i,row in enumerate(ws.iter_rows(values_only=True)):
            if i==0: continue
            if not row or all(c is None for c in row[:6]): continue
            date_val=None
            for di in [19,12,11]:
                if di<len(row) and row[di]:
                    d=parse_date(row[di])
                    if d: date_val=d; break
            if not date_val: continue
            name=str(row[1]).strip() if row[1] else ''
            if not name: continue
            rev=parse_num(row[5]) if len(row)>5 else 0
            qty=int(parse_num(row[3])) if len(row)>3 and row[3] else 1
            ch_raw=str(row[15]).strip() if len(row)>15 and row[15] else ''
            channel=norm_channel(ch_raw)
            if rev<=0: continue
            key=(date_val,name,channel); agg[key]['q']+=qty; agg[key]['s']+=rev; product_set.add(name)
        wb.close()

    products=sorted(product_set); PROD_IDX={p:i for i,p in enumerate(products)}
    lines=[]
    for (date,prod,ch),vals in sorted(agg.items()):
        p_i=PROD_IDX.get(prod); ch_lower=ch.lower(); c_i=CH_IDX.get(ch_lower)
        if c_i is None: c_i=len(CHANNELS); CHANNELS.append(ch); CH_IDX[ch_lower]=c_i
        if p_i is None: continue
        lines.append({'d':date,'p':p_i,'c':c_i,'q':vals['q'],'s':round(vals['s'],2)})
    lines.sort(key=lambda x:x['d'])
    raw={'date_min':lines[0]['d'] if lines else '','date_max':lines[-1]['d'] if lines else '','channels':CHANNELS,'products':products,'lines':lines}
    raw_js=json.dumps(raw,ensure_ascii=False,separators=(',',':'))
    with open(SALES_HTML,'r',encoding='utf-8') as f: html=f.read()
    html_new=re.sub(r'const RAW\s*=\s*\{[\s\S]*?\};',f'const RAW = {raw_js};',html)
    if html_new!=html:
        with open(SALES_HTML,'w',encoding='utf-8') as f: f.write(html_new)
        print(f'✅ Sales Dashboard updated: {len(lines)} lines, {raw["date_min"]} to {raw["date_max"]}')
    else:
        print('⚠️ Sales Dashboard: no change')
```

## STEP 6 — BUMP SW.JS CACHE VERSION

```python
import re, os, subprocess

ALL_MNT = "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
SW = f'{ALL_MNT}/sw.js'

if os.path.exists(SW):
    with open(SW,'r',encoding='utf-8') as f: content = f.read()
    m = re.search(r"const CACHE = 'wibwub-v(\d+)'", content)
    if m:
        old_v = int(m.group(1))
        new_v = old_v + 1
        new_content = content.replace(f"'wibwub-v{old_v}'", f"'wibwub-v{new_v}'")
        with open(SW,'w',encoding='utf-8') as f: f.write(new_content)
        print(f'✅ sw.js cache bumped: wibwub-v{old_v} → wibwub-v{new_v}')
    else:
        print('⚠️ sw.js: CACHE version pattern not found')
else:
    print(f'⚠️ sw.js not found at {SW}')
```

## STEP 7 — VERIFY
```bash
python3 -c "
import re, os, subprocess
ALL_MNT = "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
print(f'ALL_MNT={ALL_MNT}')
checks = {'Dashboard':f'{ALL_MNT}/WIBWUB_Dashboard.html','Mobile':f'{ALL_MNT}/WIBWUB_Mobile.html','Affiliate':f'{ALL_MNT}/WIBWUB_Affiliate_Dashboard.html','TikTok':f'{ALL_MNT}/WIBWUB_TikTok_Dashboard_v7.html','Ads':f'{ALL_MNT}/data Ads/WIBWUB_Ads_Dashboard.html','Sales':f'{ALL_MNT}/Data Shipnity/Sales_Dashboard.html','sw.js':f'{ALL_MNT}/sw.js'}
for name,path in checks.items():
    if not os.path.exists(path): print(f'MISSING {name}: {path}'); continue
    with open(path,encoding='utf-8') as f: h=f.read()
    if name=='Ads': m=re.search(r'spend:(\d+)',h); print(f'OK {name}: spend={m.group(1) if m else \"?\"}')
    elif name=='Sales': m=re.search(r'date_min.{1,5}([0-9-]{10}).{1,30}date_max.{1,5}([0-9-]{10})',h); print(f'OK {name}: {m.group(1) if m else \"?\"} to {m.group(2) if m else \"?\"}')
    elif name=='sw.js': m=re.search(r\"const CACHE = '(wibwub-v\d+)'\",h); print(f'OK {name}: {m.group(1) if m else \"?\"}')
    elif name=='Affiliate':
        mg=re.search(r'const gmvD=\[([^\]]+)\]',h); mn=re.search(r'const netD=\[([^\]]+)\]',h)
        print(f'OK {name}: gmvD=[{mg.group(1) if mg else \"?\"}]'); print(f'   Affiliate: netD=[{mn.group(1) if mn else \"?\"}] ← ตรวจว่า Net ≤ GMV')
    elif name=='Mobile':
        m=re.search(r'const AFI_NET=\[([^\]]+)\]',h); print(f'OK {name}: AFI_NET=[{m.group(1) if m else \"?\"}]')
    else:
        m=re.search(r'const SH_REV\s*=\s*\[([^\]]+)\]',h)
        if m: print(f'OK {name}: {len(m.group(1).split(\",\"))} months SH_REV')
        else: print(f'OK {name}: updated')
"
```

## STEP 8 — CLEANUP TEMP FILES

```python
import os, subprocess

OUTPUTS = "/Users/thanasablilutanon/Library/Caches/wibwub-outputs"
if OUTPUTS and os.path.exists(OUTPUTS):
    for tmp in ['shopee.txt','tiktok_sales.txt','lazada.txt','tiktok_content.txt',
                'sales_results.json','affil_results.json','tiktok_content_results.json']:
        fp = f'{OUTPUTS}/{tmp}'
        if os.path.exists(fp):
            os.remove(fp)
            print(f'🗑️ cleaned {tmp}')
print('✅ Cleanup done.')
```

## RULES
- ห้าม spawn subagents
- ใช้ subprocess.run find ค้นหา ALL_MNT ทุก step — ห้าม hardcode session name
- **ถ้า ALL_MNT ไม่พบ → หยุดทันที อย่า fallback ไป Downloads หรือ folder อื่นเด็ดขาด**
- **ห้ามบันทึกไฟล์ใดๆ ลง ~/Downloads** — ใช้ $OUTPUTS สำหรับ temp และ $ALL_MNT สำหรับ output เท่านั้น
- ถ้า Google Sheet response ถูก save ไว้ที่ /var/folders/... ให้ Read ไฟล์แล้วดึง fileContent
- **Affiliate: อ่านจาก Data Affiliate/ xlsx เท่านั้น — netD = GMV − returns ต่อ creator, ไม่ใช่ copy ของ GMV**
- **Dashboard + Mobile ต้องอัปเดตพร้อมกันทุก step (sales arrays ใน A, AFI arrays ใน B2)**
- Ads: glob ทุกไฟล์ใน folder ไม่ hardcode ชื่อไฟล์
- Sales: อ่าน xlsx ทุกไฟล์ใน Data Shipnity/ แล้ว aggregate
- sw.js: bump +1 ทุกครั้งที่รัน task (ไม่งั้น PWA ไม่ refresh)
- On error: log แล้วทำต่อ ห้าม abort

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
| `git -C "<path>" ...` | **ห้ามใช้** — กฎ deny จับจากคำขึ้นต้น `git push` จึงกัน `git -C <path> push` ไม่ได้ = เปิดช่องให้ push หลุด | `cd "<path เต็ม>" && git status` |
| `cd "<path>" && python3 x.py` | ขึ้นต้นด้วย cd ไม่แมตช์ `Bash(python3 *)` | `python3 "<path เต็ม>/x.py"` |
| `BASE="..."` แล้วใช้ `$BASE` | ตัวแปร = simple_expansion สร้างกฎถาวรไม่ได้ | เขียนพาธเต็มตรง ๆ ทุกครั้ง |
| `for d in ...; do ... done` / `if [ ... ]` | ลูป/เงื่อนไขใน bash ก็เข้าข่ายเดียวกัน | ย้ายตรรกะไปไว้ในสคริปต์ python แล้วเรียกไฟล์นั้น |
| `cmd1; cmd2; cmd3` ต่อกันยาว ๆ | คำสั่งผสมแมตช์กฎไม่ได้ | แยกเป็นคนละคำสั่ง |

**ถ้าต้องมีตรรกะ (วนลูป / เช็คเงื่อนไข / ประกอบพาธ): เขียนเป็นสคริปต์ python
ไว้ใน `scripts/` แล้วเรียกด้วยพาธเต็ม** เช่น `python3 "<path เต็ม>/scripts/ads/check_downloads.py" tiktok`
วิธีนี้ทั้งอ่านง่ายกว่า ทดสอบแยกได้ และไม่ติดกำแพงสิทธิ์
