#!/usr/bin/env python3
"""อัปเดตข้อมูล Affiliate ใน WIBWUB_Affiliate_Dashboard.html + WIBWUB_Mobile.html

ใช้ process_affiliate() ของ wibwub_update.py เป็นตัวคำนวณ — ห้าม reimplement

เหตุผล (บั๊กที่ task prompt เก่าทำไว้ และ process_affiliate แก้ไปแล้ว):
  · ไฟล์ใน Data Affiliate/ มี 2 รูปแบบที่ "ตำแหน่งคอลัมน์ไม่เหมือนกัน"
      Creator_List_*            : returns = col21, commission = col7
      Transaction_Analysis_*    : returns = col4,  commission = col21
    พรอมป์เก่า hardcode col 1/2/10 ให้ทั้งสองแบบ -> commission กลายเป็นจำนวนโชว์เคส
    (เลขหลักหน่วย) และ net สูงกว่า gmv หรือติดลบ · ตัวจริงใช้ find_col() จับจากชื่อ header
  · ต้องกรองเฉพาะไฟล์ที่ชื่อมี 'Creator_List' — โฟลเดอร์มี Product_List / Video_List /
    Live_List / Core_Metrics / WIBWUB_KOL_Tracker ปนอยู่ ถ้า glob *.xlsx จะอ่านผิดไฟล์
  · ต้องเลือกไฟล์ตามช่วงวันที่ในชื่อไฟล์ (overlap กับเดือนมากสุด) ไม่ใช่ mtime ใหม่สุด
    ไม่งั้นไฟล์เดือน ส.ค. ที่เพิ่งโหลดจะไปลงช่อง ต.ค.

ใช้:  python3 scripts/affiliate_update.py [--dry-run]
exit: 0 = อัปเดตแล้ว · 10 = ไม่มีอะไรเปลี่ยน · 2 = ไม่ผ่านด่านตรวจ (ไม่เขียนไฟล์)
"""
import sys, json, argparse, re
from pathlib import Path

def _find_base():
    """ไล่ขึ้นจากตำแหน่งไฟล์นี้จนเจอโฟลเดอร์ All — ดูจาก marker sw.js + .git

    ห้ามฝังพาธ Mac ตายตัว: งานตั้งเวลาฝั่ง local รันในแซนด์บ็อกซ์ที่ mount โฟลเดอร์ All
    ไว้คนละที่ (/sessions/<ชื่อ>/mnt/All) และชื่อเซสชันเปลี่ยนทุกรอบ (24 ต.ค. 69)
    """
    p = Path(__file__).resolve()
    for d in (p, *p.parents):
        if (d / 'sw.js').is_file() and (d / '.git').exists():
            return d
    raise SystemExit(f'หาโฟลเดอร์ All ไม่เจอ — ไล่ขึ้นจาก {p} แล้วไม่เจอโฟลเดอร์ที่มีทั้ง '
                     'sw.js และ .git · ห้ามเดาพาธ ให้ตรวจว่าสคริปต์ยังอยู่ในโฟลเดอร์ All หรือไม่')


BASE = _find_base()
AFF = BASE / 'WIBWUB_Affiliate_Dashboard.html'
MOB = BASE / 'WIBWUB_Mobile.html'
# ชื่ออาเรย์ที่ต้องตรงกันระหว่าง 2 หน้า (Affiliate Dashboard -> Mobile)
PAIRS = [('AF_GMV', 'AFI_GMV'), ('AF_NET', 'AFI_NET'), ('AF_COM', 'AFI_COMM')]


def W_bump():
    """bump sw.js — ใช้ scripts/bump_sw.py ตรง ๆ ไม่ต้อง import wibwub_update ทั้งก้อน"""
    import subprocess
    subprocess.run([sys.executable, str(BASE / 'scripts' / 'bump_sw.py')], check=False)


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def arr(path, name):
    m = re.search(r'const\s+' + name + r'\s*=\s*\[([^\]]*)\]', Path(path).read_text(encoding='utf-8'))
    if not m: return None
    try: return [float(x) for x in m.group(1).split(',') if x.strip()]
    except ValueError: return None


# ── PRODUCTS[].vid — จำนวนวิดีโอขายสินค้าจากครีเอเตอร์ ────────────────────────
# ที่มา: คอลัมน์ "วิดีโอ" ของ Transaction_Analysis_Product_List_<ช่วง>.xlsx
# จับคู่ด้วย "รหัสสินค้า" (ฟิลด์ id ใน PRODUCTS) ไม่ใช่ชื่อ — ชื่อในไฟล์เป็นชื่อไทย
# คนละชุดกับชื่อบนหน้า (เช่น id 1729451577908759108 = "เคลือบสีคาร์นัวบา" = WIBWUB Sugar)
#
# 28 ต.ค. 69: ก่อนมีสคริปต์นี้ vid ถูกใส่ด้วยมือ และ 2 ตัวสร้างกลับจากไฟล์ไม่ได้เลย
# (Leather Wipes 670 แต่ไฟล์ให้ 644 · Interior 173 แต่ไฟล์ให้ 172 — ไล่ทั้ง 131 ไฟล์
# ก็ไม่มีไฟล์ไหนให้ 670/173) ผู้ใช้ยืนยันว่า 1 รหัส = 1 สินค้า ไม่มีการรวมกลุ่ม
# -> ยึดคอลัมน์ "วิดีโอ" ของรหัสเดียวเท่านั้น ห้ามบวกหลายรหัสเข้าด้วยกัน
PROD_DIR = BASE / 'Data Affiliate' / 'สินค้า'
PL_RE = re.compile(r'^Transaction_Analysis_Product_List_(\d{8})-(\d{8})')
VID_HDR, ID_HDR = 'วิดีโอ', 'รหัสสินค้า'


def pick_product_list():
    """ไฟล์ Product_List ของช่วงล่าสุด — เรียงตาม (วันสิ้นสุด, วันเริ่ม, mtime)

    ต้อง match ตั้งแต่ต้นชื่อ: โฟลเดอร์มีไฟล์ `_WRONG_RANGE_ignore_...` ปนอยู่
    และมีไฟล์ซ้ำทั้งแบบ ` (1)` และแบบ `__<stamp>` ที่ mover เติมกันชื่อชน
    """
    best = None
    for fp in PROD_DIR.glob('Transaction_Analysis_Product_List_*.xlsx'):
        if fp.name.startswith(('~', '.')):
            continue
        m = PL_RE.match(fp.name)
        if not m:
            continue
        key = (m.group(2), m.group(1), fp.stat().st_mtime)
        if best is None or key > best[0]:
            best = (key, fp, m.group(1), m.group(2))
    return best


def read_vid_map(fp):
    """{รหัสสินค้า: จำนวนวิดีโอ} จาก sheet1.xml

    openpyxl อ่านไฟล์ export ชุดนี้ได้ 1 คอลัมน์ 0 แถว (dimension ในไฟล์ผิด)
    จึงต้องแกะ xml เองแบบเดียวกับ scripts/vid_merge.py · ค่าเป็น inline string
    (<is><t>) ไม่มี sharedStrings · แถว 1 = header, แถว 2 = คำอธิบายคอลัมน์ (ไม่ใช่ข้อมูล)
    """
    import zipfile
    with zipfile.ZipFile(fp) as zf:
        xml = zf.open('xl/worksheets/sheet1.xml').read().decode('utf-8', 'replace')
    row_re = re.compile(r'<row r="(\d+)"[^>]*>(.*?)</row>', re.DOTALL)
    cell_re = re.compile(r'<c r="([A-Z]+)(\d+)"[^>]*>(?:<is><t[^>]*>(.*?)</t></is>|<v>(.*?)</v>)?</c>')
    rows = {}
    for rn, body in row_re.findall(xml):
        cells = {}
        for col, _, s, v in cell_re.findall(body):
            cells[col] = (s if s else v) or ''
        rows[int(rn)] = cells
    if not rows:
        die('อ่าน Product_List ไม่ได้ (ไม่มีแถวเลย)', fp.name)
    hdr = rows.get(1) or {}
    cols = {}
    for col, val in hdr.items():
        v = val.strip()
        if v in (VID_HDR, ID_HDR) and v not in cols:
            cols[v] = col
    miss = [h for h in (VID_HDR, ID_HDR) if h not in cols]
    if miss:
        die('Product_List ไม่มีคอลัมน์ที่ต้องใช้ — รูปแบบไฟล์เปลี่ยน',
            {'ขาด': miss, 'ไฟล์': fp.name, 'header': sorted(hdr.values())})
    out = {}
    for rn in sorted(rows):
        if rn <= 2:                      # 1 = header · 2 = คำอธิบาย
            continue
        c = rows[rn]
        pid = (c.get(cols[ID_HDR]) or '').strip()
        raw = (c.get(cols[VID_HDR]) or '').strip().replace(',', '')
        if not pid:
            continue
        if not re.fullmatch(r'\d+(\.0+)?', raw):
            continue                     # ช่องว่าง/ค่าไม่ใช่ตัวเลข = ไม่นับ ห้ามเดาเป็น 0
        out.setdefault(pid, int(float(raw)))
    return out


def write_vid(dry):
    """เขียน vid ของทุกรายการใน PRODUCTS — ไม่ครบ = หยุด ไม่เขียนทับบางส่วน"""
    best = pick_product_list()
    if not best:
        die('ไม่พบไฟล์ Transaction_Analysis_Product_List_<YYYYMMDD>-<YYYYMMDD>.xlsx',
            str(PROD_DIR))
    _, fp, d0, d1 = best
    vmap = read_vid_map(fp)
    t = AFF.read_text(encoding='utf-8')
    m = re.search(r'const PRODUCTS = \[\n(.*?\n)\];', t, re.DOTALL)
    if not m:
        die('หา const PRODUCTS ใน Affiliate Dashboard ไม่เจอ')
    block = m.group(1)
    rows = [ln for ln in block.split('\n') if ln.strip().startswith('{')]
    noid, nofile, changes = [], [], []
    new = block
    for ln in rows:
        nm = re.search(r"name:'([^']*)'", ln)
        pid = re.search(r"id:'(\d+)'", ln)
        vid = re.search(r"vid:(\d+)", ln)
        name = nm.group(1) if nm else '(ไม่มี name)'
        if not pid:
            noid.append(name); continue
        if pid.group(1) not in vmap:
            nofile.append({'name': name, 'id': pid.group(1)}); continue
        if not vid:
            noid.append(name + ' (ไม่มีช่อง vid)'); continue
        want = vmap[pid.group(1)]
        if int(vid.group(1)) != want:
            changes.append({'name': name, 'จาก': int(vid.group(1)), 'เป็น': want})
            new = new.replace(ln, ln[:vid.start()] + f'vid:{want}' + ln[vid.end():], 1)
    # ── ด่าน: ขาดรหัส หรือหารหัสในไฟล์ไม่เจอ = หยุด ห้ามเขียน 0 ──────────────
    if noid or nofile:
        die('มีรายการใน PRODUCTS ที่จับคู่รหัสสินค้าไม่ได้ — ไม่เขียน vid เลย '
            '(ห้ามเขียน 0 แทน) ให้เติม id ใน PRODUCTS หรือหาไฟล์ที่มีรหัสนั้น',
            {'ไม่มี id บนหน้า': noid, 'หารหัสในไฟล์ไม่เจอ': nofile,
             'ไฟล์': fp.name, 'รหัสในไฟล์': len(vmap)})
    info = {'file': fp.name, 'range': f'{d0}-{d1}', 'products': len(rows),
            'ids_in_file': len(vmap), 'changes': changes}
    if changes and not dry:
        AFF.write_text(t[:m.start(1)] + new + t[m.end(1):], encoding='utf-8')
    return info


# ── AF_LIVE — Live GMV จากครีเอเตอร์ รายเดือน ────────────────────────────────
# เดิมเป็น AF_LIVE_MANUAL กรอกมือ แล้วค้างที่ ก.ย. 2569 สองเดือน (เจอ 27 พ.ย. 69)
# ที่มา: TK_PROD_DATA ใน WIBWUB_Dashboard.html — daily[วัน] = list ของอาเรย์ต่อสินค้า
#        ดัชนี 8 = affiliate_live · ห้ามใช้ 7 (affiliate รวม) · 5 = ไลฟ์ของร้านเอง
# sessions: นับ "ID ของ LIVE" ไม่ซ้ำ จากไฟล์ Transaction_Analysis_Live_List_<ช่วง>.xlsx
# ด่าน: GMV ในไฟล์ไลฟ์สตรีม ต้องตรงกับผลรวมดัชนี 8 ช่วงวันเดียวกัน ต่างไม่เกิน 1 บาท
DASH = BASE / 'WIBWUB_Dashboard.html'
LIVE_DIR = BASE / 'Data Affiliate' / 'ไลฟ์สตรีม'
LL_RE = re.compile(r'^Transaction_Analysis_Live_List_(\d{8})-(\d{8})')
TH_MO = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
         'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
AFF_LIVE_IDX = 8
LIVE_ID_HDR = 'ID ของ LIVE'


def read_const_obj(path, name):
    """อ่าน `const <name> = {...};` ด้วยการนับปีกกา

    ห้ามใช้ regex `const X = (\{.*?\});` — แบบ non-greedy หยุดที่ `};` ของ const
    ข้างเคียง (24 พ.ย. 69 อ่าน TK_PROD_SKU ผิดไป 2 เดือน แล้วรายงานผิดให้ผู้ใช้)
    """
    t = Path(path).read_text(encoding='utf-8')
    i = t.find('const %s = ' % name)
    if i < 0:
        return None
    j = t.find('{', i)
    if j < 0:
        return None
    depth = 0
    for k in range(j, len(t)):
        if t[k] == '{':
            depth += 1
        elif t[k] == '}':
            depth -= 1
            if depth == 0:
                return json.loads(t[j:k + 1])
    return None


def tk_live_by_month():
    """{'2026-11': {'gmv': float, 'd0': 'YYYY-MM-DD', 'd1': ...}} จาก TK_PROD_DATA ดัชนี 8"""
    tk = read_const_obj(DASH, 'TK_PROD_DATA')
    if not tk or not tk.get('daily'):
        die('อ่าน TK_PROD_DATA ใน WIBWUB_Dashboard.html ไม่ได้')
    out = {}
    for d, rows in tk['daily'].items():
        if not isinstance(rows, list):
            continue
        g = 0.0
        for r in rows:
            if isinstance(r, list) and len(r) > AFF_LIVE_IDX:
                try:
                    g += float(r[AFF_LIVE_IDX] or 0)
                except (TypeError, ValueError):
                    pass
        e = out.setdefault(d[:7], {'gmv': 0.0, 'd0': d, 'd1': d})
        e['gmv'] += g
        e['d0'] = min(e['d0'], d)
        e['d1'] = max(e['d1'], d)
    return out


def read_live_file(fp):
    """(จำนวน LIVE ไม่ซ้ำ, ผลรวม GMV) — แกะ sheet1.xml เองแบบเดียวกับ read_vid_map()"""
    import zipfile
    with zipfile.ZipFile(fp) as zf:
        xml = zf.open('xl/worksheets/sheet1.xml').read().decode('utf-8', 'replace')
    row_re = re.compile(r'<row r="(\d+)"[^>]*>(.*?)</row>', re.DOTALL)
    cell_re = re.compile(r'<c r="([A-Z]+)(\d+)"[^>]*>(?:<is><t[^>]*>(.*?)</t></is>|<v>(.*?)</v>)?</c>')
    rows = {}
    for rn, body in row_re.findall(xml):
        rows[int(rn)] = {c: ((s if s else v) or '') for c, _, s, v in cell_re.findall(body)}
    hdr = rows.get(1) or {}
    id_col = next((c for c, v in hdr.items() if v.strip() == LIVE_ID_HDR), None)
    gmv_col = next((c for c, v in hdr.items() if v.strip().startswith('GMV')), None)
    if not id_col or not gmv_col:
        die('ไฟล์ไลฟ์สตรีมไม่มีคอลัมน์ที่ต้องใช้ — รูปแบบไฟล์เปลี่ยน',
            {'ไฟล์': fp.name, 'header': sorted(hdr.values())[:30]})
    ids, tot = set(), 0.0
    for rn in sorted(rows):
        if rn <= 2:                      # 1 = header · 2 = คำอธิบาย
            continue
        c = rows[rn]
        lid = (c.get(id_col) or '').strip()
        if not lid:
            continue
        ids.add(lid)
        raw = re.sub(r'[฿,\s]', '', (c.get(gmv_col) or ''))
        try:
            tot += float(raw)
        except ValueError:
            pass
    return len(ids), tot


def write_af_live(dry):
    """เขียน const AF_LIVE ในหน้า Affiliate — ไม่ผ่านด่าน = หยุด ไม่เขียน"""
    by = tk_live_by_month()
    if len(by) < 2:
        die('TK_PROD_DATA มีไม่ถึง 2 เดือน — คำนวณ AF_LIVE ไม่ได้', sorted(by))
    keys = sorted(by)
    cur, prev = by[keys[-1]], by[keys[-2]]

    def lbl(k, e):
        return '%s %d-%d' % (TH_MO[int(k[5:7]) - 1], int(e['d0'][8:]), int(e['d1'][8:]))

    # ── ด่าน: เทียบกับไฟล์ไลฟ์สตรีมของช่วงเดียวกัน (ต่างไม่เกิน 1 บาท) ──────
    want = cur['d0'].replace('-', '') + '-' + cur['d1'].replace('-', '')
    fp = None
    for f in LIVE_DIR.glob('Transaction_Analysis_Live_List_*.xlsx'):
        if f.name.startswith(('~', '.')):
            continue
        m = LL_RE.match(f.name)
        if m and '%s-%s' % (m.group(1), m.group(2)) == want:
            if fp is None or f.stat().st_mtime > fp.stat().st_mtime:
                fp = f
    if fp is None:
        die('ไม่พบไฟล์ไลฟ์สตรีมของช่วงเดียวกับ TK_PROD_DATA — ยังไม่เขียน AF_LIVE '
            '(ต้องโหลดไฟล์ช่วงนี้ก่อน หรือรอ TK_PROD_DATA ตามให้ทัน)',
            {'ต้องการช่วง': want, 'โฟลเดอร์': str(LIVE_DIR)})
    sessions, file_gmv = read_live_file(fp)
    if abs(file_gmv - cur['gmv']) > 1:
        die('GMV ไลฟ์จากไฟล์ไม่ตรงกับ TK_PROD_DATA ดัชนี 8 — ไม่เขียน AF_LIVE',
            {'ไฟล์': fp.name, 'จากไฟล์': round(file_gmv, 2),
             'จาก TK_PROD_DATA': round(cur['gmv'], 2),
             'ต่าง': round(file_gmv - cur['gmv'], 2)})

    blk = ("const AF_LIVE = {asof:'%s', gmv:%d, sessions:%d,\n"
           "                 prev_asof:'%s', prev_gmv:%d};"
           % (lbl(keys[-1], cur), round(cur['gmv']), sessions,
              lbl(keys[-2], prev), round(prev['gmv'])))
    t = AFF.read_text(encoding='utf-8')
    m = re.search(r"const AF_LIVE = \{[^}]*\};", t, re.DOTALL)
    if not m:
        die('หา const AF_LIVE ในหน้า Affiliate ไม่เจอ')
    changed = m.group(0) != blk
    if changed and not dry:
        AFF.write_text(t[:m.start()] + blk + t[m.end():], encoding='utf-8')
    return {'asof': lbl(keys[-1], cur), 'gmv': round(cur['gmv']), 'sessions': sessions,
            'prev_asof': lbl(keys[-2], prev), 'prev_gmv': round(prev['gmv']),
            'live_file': fp.name, 'gate_diff': round(file_gmv - cur['gmv'], 2),
            'changed': changed}


# ── PRODUCTS[].monthly / .ret — เขียนใหม่จากไฟล์ Product_List เต็มเดือน ──────
# 27 พ.ย. 69: ค่าเดิมกรอกมือและ "คนละนิยามในแต่ละเดือน" — รวมทุกสินค้าต่อเดือน
# เทียบ AF_GMV ได้ 9%(ส.ค.) ถึง 90%(พ.ค.) → เติมเดือนใหม่ต่อท้ายจะอ่านเป็นโตพรวด
# ที่มาใหม่: คอลัมน์ "GMV จากครีเอเตอร์" (monthly) และ "การคืนเงิน" (ret)
# จับคู่ด้วย "รหัสสินค้า" = PRODUCTS[].id เหมือน vid
# เงื่อนไขไฟล์: ต้องขึ้นวันที่ 1 และ d0/d1 เดือนเดียวกัน (กันไฟล์คร่อมเดือนลงช่องผิด)
# ด่าน: ผลรวม GMV ทุกสินค้าในไฟล์ เทียบ AF_GMV เดือนนั้น ต่างเกิน 2% = ข้ามเดือนนั้น
GMV_HDR, RET_HDR = 'GMV จากครีเอเตอร์', 'การคืนเงิน'
MO_KEYS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
           'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
GATE_PCT = 0.02


def _money(x):
    return float(re.sub(r'[฿,\s]', '', x or '') or 0)


def read_prod_money(fp):
    """{รหัสสินค้า: (gmv, ret)} — แกะ sheet1.xml เองแบบเดียวกับ read_vid_map()"""
    import zipfile
    with zipfile.ZipFile(fp) as zf:
        xml = zf.open('xl/worksheets/sheet1.xml').read().decode('utf-8', 'replace')
    row_re = re.compile(r'<row r="(\d+)"[^>]*>(.*?)</row>', re.DOTALL)
    cell_re = re.compile(r'<c r="([A-Z]+)(\d+)"[^>]*>(?:<is><t[^>]*>(.*?)</t></is>|<v>(.*?)</v>)?</c>')
    rows = {}
    for rn, body in row_re.findall(xml):
        rows[int(rn)] = {c: ((s if s else v) or '') for c, _, s, v in cell_re.findall(body)}
    hdr = rows.get(1) or {}
    cols = {}
    for col, val in hdr.items():
        v = val.strip()
        if v in (GMV_HDR, RET_HDR, ID_HDR) and v not in cols:
            cols[v] = col
    miss = [h for h in (GMV_HDR, RET_HDR, ID_HDR) if h not in cols]
    if miss:
        die('Product_List ไม่มีคอลัมน์เงินที่ต้องใช้ — รูปแบบไฟล์เปลี่ยน',
            {'ขาด': miss, 'ไฟล์': fp.name, 'header': sorted(hdr.values())[:30]})
    out = {}
    for rn in sorted(rows):
        if rn <= 2:
            continue
        c = rows[rn]
        pid = (c.get(cols[ID_HDR]) or '').strip()
        if pid:
            out[pid] = (_money(c.get(cols[GMV_HDR])), _money(c.get(cols[RET_HDR])))
    return out


def full_month_files():
    """{'oct': (path, d0, d1)} — เฉพาะไฟล์ที่ d0 เป็นวันที่ 1 และเดือนเดียวกับ d1"""
    best = {}
    for fp in PROD_DIR.glob('Transaction_Analysis_Product_List_*.xlsx'):
        if fp.name.startswith(('~', '.')):
            continue
        m = PL_RE.match(fp.name)
        if not m:
            continue
        d0, d1 = m.group(1), m.group(2)
        if d0[6:] != '01' or d0[:6] != d1[:6]:
            continue                      # ไฟล์ไม่เต็มเดือน หรือคร่อมเดือน
        key = MO_KEYS[int(d0[4:6]) - 1]
        cand = (d1, fp.stat().st_mtime)
        if key not in best or cand > (best[key][2], best[key][0].stat().st_mtime):
            best[key] = (fp, d0, d1)
    return best


def _set_month(block_line, field, mo, val):
    """คืนบรรทัดใหม่ที่ <field>:{...} มีคีย์ mo = val (เรียงตามปฏิทิน)"""
    m = re.search(field + r':\{([^}]*)\}', block_line)
    if not m:
        return None
    cur = dict((k, int(v)) for k, v in re.findall(r'(\w+):(-?\d+)', m.group(1)))
    cur[mo] = int(val)
    body = ','.join('%s:%d' % (k, cur[k]) for k in MO_KEYS if k in cur)
    return block_line[:m.start()] + '%s:{%s}' % (field, body) + block_line[m.end():]


def write_prod_monthly(dry, rebuild=False):
    """เขียน monthly/ret ของเดือนปัจจุบัน (หรือทุกเดือนที่มีไฟล์เต็ม ถ้า rebuild)"""
    files = full_month_files()
    if not files:
        return {'written': {}, 'skipped': [{'เหตุผล': 'ไม่พบไฟล์เต็มเดือนเลย'}], 'changes': []}
    af = arr(AFF, 'AF_GMV') or []
    targets = sorted(files, key=lambda k: MO_KEYS.index(k))
    if not rebuild:
        targets = targets[-1:]            # รอบปกติ = เดือนล่าสุดเท่านั้น

    t = AFF.read_text(encoding='utf-8')
    m = re.search(r'const PRODUCTS = \[\n(.*?\n)\];', t, re.DOTALL)
    if not m:
        die('หา const PRODUCTS ใน Affiliate Dashboard ไม่เจอ')
    block = m.group(1)
    written, skipped, changes = {}, [], []

    for mo in targets:
        fp, d0, d1 = files[mo]
        vals = read_prod_money(fp)
        idx = MO_KEYS.index(mo)
        want = af[idx] if idx < len(af) else None
        tot = sum(v[0] for v in vals.values())
        if not want:
            skipped.append({'เดือน': mo, 'เหตุผล': 'ไม่มี AF_GMV ให้เทียบ', 'ไฟล์': fp.name})
            continue
        diff = (tot - want) / want
        if abs(diff) > GATE_PCT:
            skipped.append({'เดือน': mo, 'เหตุผล': 'ไม่ผ่านด่าน %.0f%%' % (GATE_PCT * 100),
                            'ไฟล์': fp.name, 'ไฟล์รวม': round(tot), 'AF_GMV': round(want),
                            'ต่าง': '%+.2f%%' % (diff * 100)})
            continue
        # ── ทุกสินค้าในหน้าต้องมีในไฟล์ ไม่งั้นข้ามทั้งเดือน (ห้ามเขียน 0) ──
        lines = [ln for ln in block.split('\n') if ln.strip().startswith('{')]
        rows, missing = [], []
        for ln in lines:
            pid = re.search(r"id:'(\d+)'", ln)
            nm = re.search(r"name:'([^']*)'", ln)
            if not pid:
                missing.append(nm.group(1) if nm else '(ไม่มี name)')
                continue
            if pid.group(1) not in vals:
                missing.append('%s (%s)' % (nm.group(1) if nm else '?', pid.group(1)))
                continue
            rows.append((ln, nm.group(1) if nm else '?', vals[pid.group(1)]))
        if missing:
            skipped.append({'เดือน': mo, 'เหตุผล': 'จับคู่รหัสสินค้าไม่ครบ ไม่เขียนทั้งเดือน',
                            'ไฟล์': fp.name, 'ขาด': missing[:5]})
            continue
        for ln, name, (g, r) in rows:
            old_g = re.search(r'monthly:\{([^}]*)\}', ln)
            old_r = re.search(r'ret:\{([^}]*)\}', ln)
            prev_g = dict(re.findall(r'(\w+):(-?\d+)', old_g.group(1))).get(mo) if old_g else None
            prev_r = dict(re.findall(r'(\w+):(-?\d+)', old_r.group(1))).get(mo) if old_r else None
            new = _set_month(ln, 'monthly', mo, round(g))
            if new is None:
                skipped.append({'เดือน': mo, 'เหตุผล': 'ไม่มีช่อง monthly ในแถว', 'สินค้า': name})
                break
            new2 = _set_month(new, 'ret', mo, round(r))
            if new2 is None:
                skipped.append({'เดือน': mo, 'เหตุผล': 'ไม่มีช่อง ret ในแถว', 'สินค้า': name})
                break
            # gmv (ยอดสะสม ใช้ตอนกดปุ่ม "รวม") = ผลรวม monthly เสมอ
            # 27 พ.ย. 69: ก่อนเขียน monthly ใหม่ ค่าทั้งสองเกือบเท่ากันอยู่แล้ว
            # พอ monthly ถูกแก้ให้ถูกนิยาม gmv เดิมจะต่ำกว่า 3 เท่า ปุ่ม "รวม" เลยขัดกับรายเดือน
            mm2 = re.search(r'monthly:\{([^}]*)\}', new2)
            gm = re.search(r'gmv:(\d+)', new2)
            if not gm:
                skipped.append({'เดือน': mo, 'เหตุผล': 'ไม่มีช่อง gmv ในแถว', 'สินค้า': name})
                break
            tot_m = sum(int(v) for _k, v in re.findall(r'(\w+):(-?\d+)', mm2.group(1)))
            prev_gmv = int(gm.group(1))
            new2 = new2[:gm.start()] + 'gmv:%d' % tot_m + new2[gm.end():]
            if new2 != ln:
                changes.append({'เดือน': mo, 'สินค้า': name,
                                'monthly': [prev_g and int(prev_g), round(g)],
                                'ret': [prev_r and int(prev_r), round(r)],
                                'gmv': [prev_gmv, tot_m]})
            block = block.replace(ln, new2, 1)
        else:
            written[mo] = '1-%d' % int(d1[6:])
            continue
        break                              # เจอแถวพัง = หยุดทั้งหมด

    if not written:
        return {'written': {}, 'skipped': skipped, 'changes': []}

    t = t[:m.start(1)] + block + t[m.end(1):]
    # PROD_MO_SRC — เดือนที่เขียนใหม่แล้ว (เก็บของเดิมไว้ด้วย)
    ms = re.search(r'const PROD_MO_SRC = \{([^}]*)\};', t)
    if not ms:
        die('หา const PROD_MO_SRC ในหน้า Affiliate ไม่เจอ')
    cur = dict(re.findall(r'"(\w+)"\s*:\s*"([^"]*)"', ms.group(1)))
    cur.update(written)
    body = ', '.join('"%s": "%s"' % (k, cur[k]) for k in MO_KEYS if k in cur)
    t = t[:ms.start()] + 'const PROD_MO_SRC = {%s};' % body + t[ms.end():]
    if not dry:
        AFF.write_text(t, encoding='utf-8')
    return {'written': written, 'skipped': skipped, 'changes': changes}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--live-only', action='store_true',
                    help='เขียนเฉพาะ const AF_LIVE แล้วจบ (ไม่ซิงก์ AF_* ทั้งก้อน)')
    ap.add_argument('--rebuild-monthly', action='store_true',
                    help='เขียน monthly/ret ใหม่ทุกเดือนที่มีไฟล์เต็มเดือน แล้วจบ')
    a = ap.parse_args()

    for p in (AFF, MOB):
        if not p.exists(): die('ไม่พบไฟล์', p.name)

    if a.rebuild_monthly:
        info = write_prod_monthly(a.dry_run, rebuild=True)
        print(json.dumps({'status': 'DRY_RUN' if a.dry_run else
                          ('UPDATED' if info['written'] else 'NO_CHANGE'),
                          'prod_monthly': info}, ensure_ascii=False))
        if info['written'] and not a.dry_run: W_bump()
        return 0 if (info['written'] or a.dry_run) else 10

    if a.live_only:
        info = write_af_live(a.dry_run)
        print(json.dumps({'status': 'DRY_RUN' if a.dry_run else
                          ('UPDATED' if info['changed'] else 'NO_CHANGE'),
                          'af_live': info}, ensure_ascii=False))
        if info['changed'] and not a.dry_run: W_bump()
        return 0 if (info['changed'] or a.dry_run) else 10
    sys.path.insert(0, str(BASE))
    try:
        import wibwub_update as W
    except Exception as e:
        die('import wibwub_update ไม่สำเร็จ', f'{type(e).__name__}: {e}')

    before = {k: arr(AFF, k) for k, _ in PAIRS}
    before['AF_CR'] = arr(AFF, 'AF_CR')

    try:
        aff = W.process_affiliate()
    except SystemExit as e:
        die('process_affiliate ออกกลางคัน', f'exit={e.code}')
    except Exception as e:
        die('process_affiliate ล้มเหลว', f'{type(e).__name__}: {e}')
    if not aff: die('process_affiliate() คืนค่าว่าง (ดู stderr)')

    gmv, net, com, cr = aff.get('AF_GMV'), aff.get('AF_NET'), aff.get('AF_COM'), aff.get('AF_CR')
    mo = aff.get('AF_MO')
    for nm, v in (('AF_MO', mo), ('AF_GMV', gmv), ('AF_NET', net), ('AF_COM', com), ('AF_CR', cr)):
        if not v: die(f'{nm} ว่าง')
    if not (len(mo) == len(gmv) == len(net) == len(com) == len(cr)):
        die('ความยาวอาเรย์ไม่เท่ากัน', {'AF_MO': len(mo), 'AF_GMV': len(gmv), 'AF_NET': len(net),
                                        'AF_COM': len(com), 'AF_CR': len(cr)})

    # ── ด่านตรวจ ────────────────────────────────────────────────────────────
    old = before['AF_GMV']
    if old and len(gmv) < len(old):
        die('เดือนหดลง — อาจอ่านไฟล์ไม่ครบ ไม่เขียนทับ', f'{len(old)} -> {len(gmv)}')
    bad = [f'เดือน {mo[i]}: net {net[i]:,.0f} > gmv {gmv[i]:,.0f}' for i in range(len(gmv))
           if gmv[i] and net[i] > gmv[i] * 1.001]
    if bad: die('net สูงกว่า gmv — อ่านคอลัมน์ผิด (บั๊กเดิมของพรอมป์เก่า)', bad[:5])
    neg = [f'{mo[i]}: {net[i]}' for i in range(len(net)) if net[i] < 0]
    if neg: die('net ติดลบ — อ่านคอลัมน์ผิด', neg[:5])
    tiny = [f'เดือน {mo[i]}: com {com[i]:,.0f} เทียบ gmv {gmv[i]:,.0f}' for i in range(len(gmv))
            if gmv[i] > 100_000 and 0 < com[i] < 1_000]
    if tiny: die('commission เล็กผิดปกติ — น่าจะไปอ่านคอลัมน์จำนวนโชว์เคส', tiny[:5])
    if old:
        drops = [f'{mo[i]}: {old[i]:,.0f} -> {gmv[i]:,.0f}' for i in range(min(len(old), len(gmv)))
                 if old[i] and gmv[i] and gmv[i] < old[i] * 0.98]
        if drops: die('GMV เดือนเก่าลดลง (ยอดสะสมไม่ควรลด) — ไม่เขียนทับ', drops[:5])

    summary = {'months': len(mo), 'latest_month': mo[-1],
               'latest': {'AF_GMV': gmv[-1], 'AF_NET': net[-1], 'AF_COM': com[-1], 'AF_CR': cr[-1]},
               'creators': len(aff.get('CREATORS') or []),
               'creator_months': len(aff.get('CREATOR_MONTHS') or [])}

    summary['vid'] = write_vid(a.dry_run)
    summary['af_live'] = write_af_live(a.dry_run)
    summary['prod_monthly'] = write_prod_monthly(a.dry_run)

    if a.dry_run:
        summary['current_page'] = {k: (before[k][-1] if before.get(k) else None) for k in ('AF_GMV', 'AF_CR')}
        print(json.dumps({'status': 'DRY_RUN', **summary}, ensure_ascii=False)); return 0

    W.update_html(None, aff, None, None)        # เขียนเฉพาะส่วน affiliate

    # ตรวจหลังเขียน: ค่าใน Mobile ต้องตรงกับ Affiliate Dashboard
    mism = []
    for A, B in PAIRS:
        x, y = arr(AFF, A), arr(MOB, B)
        if not x or not y: continue
        n = min(len(x), len(y))          # AF_* เริ่ม ม.ค.69 · AFI_* เริ่ม พย.68 -> เทียบท้ายเท่าที่ซ้อนกัน
        if x[-n:] != y[-n:]:
            mism.append(f'{A}[-{n}:] != {B}[-{n}:] (ล่าสุด {x[-1]} vs {y[-1]})')
    summary['mobile_mismatch'] = mism
    after = {k: arr(AFF, k) for k in before}
    changed = (after != before or bool(summary['vid']['changes'])
               or summary['af_live']['changed']
               or bool(summary['prod_monthly']['changes']))
    if changed: W.bump_sw()
    print(json.dumps({'status': 'UPDATED' if changed else 'NO_CHANGE', **summary}, ensure_ascii=False))
    return 0 if changed else 10


if __name__ == '__main__':
    sys.exit(main())
