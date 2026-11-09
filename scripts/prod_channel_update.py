#!/usr/bin/env python3
"""แหล่งข้อมูล "ตารางสินค้าขายดี — แยกช่องทาง" + 2 กราฟข้างบนมัน ใน WIBWUB_Dashboard.html

ที่มา (9 พ.ย. 69): ของเดิมเป็นตัวเลขพิมพ์มือ 3 ก้อนที่ไม่มีสคริปต์ไหนแตะ
  · <tbody> 15 แถว × 9 ช่องทาง (ไม่มี id ไม่มี JS)         -> ค้างตั้งแต่ 23 ต.ค.
  · กราฟแท่ง `pr_top10` (Top 10 × 9 ช่องทาง)               -> ค้างตั้งแต่ 11 ก.ย.
  · กราฟโดนัท `pr_channel` (ยอดรายช่องทาง เฉพาะ Top 15)   -> ค้างตั้งแต่ 11 ก.ย.
ทั้งสามก้อนเป็น**ข้อเท็จจริงเดียวกัน** จึงรวมมาอ่านจาก `const PROD_CHANNEL` ตัวเดียว
(บั๊กคลาสเดิมของรีโปนี้คือข้อเท็จจริงเดียวถูกพิมพ์ไว้หลายที่แล้วไม่มีอะไรบังคับให้ตรงกัน)

แหล่งข้อมูล
──────────────────────────────────────────────────────────────────────────────
`--source raw` (ค่าตั้งต้น · ใช้ในรอบตั้งเวลา): อ่าน `const RAW` ใน
  `Data Shipnity/Sales_Dashboard.html` ซึ่ง `wibwub_update.process_shipnity()`
  เขียนไว้ในงาน "Shipnity รายสัปดาห์" รอบเดียวกัน -> เร็ว (ไม่ parse .xlsx) และ
  ตัวเลขมาจากไปป์ไลน์เดียวกันกับหน้า Shipnity โดยโครงสร้าง ไม่ใช่เพราะเราเทียบ
  ⛔ ห้ามเขียนตัวอ่าน .xlsx ชุดที่สอง — ดัชนีคอลัมน์/CHANNEL_MAP ต้องมีที่เดียว

`--source xlsx` (ตรวจสอบ): เรียก `process_shipnity()` เอง แล้ว**กระทบยอดกับ RAW**
  รายเดือน×ช่องทาง เกณฑ์ 0.5% = พิสูจน์ว่า RAW ยังตรงกับไฟล์ .xlsx จริง
  ช้า (~5 นาที เพราะอ่าน .xlsx บน Google Drive) จึงไม่ใช้ในรอบตั้งเวลา

⛔ ห้ามใช้ SH_REV/TK_REV/LZ_REV เป็นด่าน — ลองแล้ว 9 พ.ย. 69 ไม่ผ่านทุกเดือน
เพราะคนละขอบเขต: อาเรย์พวกนั้นคือยอดจาก Seller Center ของแต่ละแพลตฟอร์ม
ส่วนนี่คือยอดรายการสินค้าใน Shipnity (ผู้ใช้ยืนยันว่าสองหน้าไม่เท่ากันโดยตั้งใจ)
Shopee ต่ำกว่าหน้าเว็บ 8-13% ทุกเดือน · Lazada ต่ำกว่า 16-26% · เป็นช่องว่างคงที่
เก็บไว้เป็น "ข้อมูลประกอบ" เท่านั้น และดู**รูปร่าง**ของช่องว่างว่าเปลี่ยนผิดปกติไหม

ใช้:  python3 scripts/prod_channel_update.py --dry-run            (อ่าน RAW ไม่เขียน)
      python3 scripts/prod_channel_update.py --write              (เขียน + commit)
      python3 scripts/prod_channel_update.py --dry-run --source xlsx   (กระทบยอด)
exit: 0 = เขียนแล้ว/ด่านผ่าน · 10 = ไม่มีอะไรเปลี่ยน · 11 = ด่านไม่ผ่าน · 1 = ผิดพลาด
"""
import argparse, datetime, importlib.util, json, re, subprocess, sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PAGE = BASE / 'WIBWUB_Dashboard.html'
RAW_SRC = BASE / 'Data Shipnity' / 'Sales_Dashboard.html'
GITW = [sys.executable, str(BASE / 'scripts' / 'gitw.py')]

# คอลัมน์ของตารางในหน้าเว็บ (เรียงซ้าย->ขวาตามของจริง) -> ช่องทางของ Shipnity ที่รวมเข้าช่องนี้
# ชื่อช่องทางใน Shipnity มีตัวซ้ำความหมายกันเพราะ CHANNEL_MAP ไม่ได้ normalize ตัวพิมพ์ใหญ่
# ขีดล่าง ('LINE_OA' กับ 'Line OA' เป็นสองช่องแยกกันในข้อมูลจริง) — รวมให้ตรงนี้
# ผู้ใช้สั่ง 9 พ.ย. 69: แก้ที่ต้นทาง wibwub_update.py เป็นงานแยกทีหลัง รวมที่ชั้นนี้ไปก่อน
COLS = [
    ('Shopee',    ['shopee']),
    ('TikTok',    ['tiktok', 'tiktokshop']),
    ('Lazada',    ['lazada']),
    ('Facebook',  ['facebook', 'fb']),
    ('Line Shop', ['line shopping', 'line_shopping']),
    ('LINE OA',   ['line oa', 'line_oa']),
    ('Website',   ['website']),
    ('Carcare',   ['carcare']),
]
# ช่องทางที่ "ไม่ใช่การขาย" — ของแจก/ตัวอย่างการตลาด/เบิกภายใน
# ผู้ใช้ตัดสิน 9 พ.ย. 69: **ไม่นับเป็นยอดขาย** และไม่รวมในคอลัมน์ "อื่นๆ"
# แสดงยอดรวมไว้ในป้ายใต้ตารางอย่างเดียว เพื่อไม่ให้ดูเหมือนข้อมูลหาย
NON_SALE = ['เบิกของ', 'สินค้าสำหรับทำการตลาด', 'marketing']   # เทียบแบบ lower()
# ป้ายที่เอาไปแสดงบนหน้าเว็บ — ต้องสะกดตามที่ Shipnity ใช้จริง ไม่ใช่คีย์ตัวพิมพ์เล็ก
NON_SALE_LABELS = ['เบิกของ', 'สินค้าสำหรับทำการตลาด', 'Marketing']
OTHER = 'อื่นๆ'
NONSALE_COL = '(ไม่ใช่การขาย)'

# ชื่อสินค้าใน Shipnity -> ป้ายที่ใช้บนหน้าเว็บ (ของเดิมในตารางพิมพ์มือ)
# ⛔ ถ้ามีสินค้าใหม่ติด 15 อันดับแรก สคริปต์จะย่อชื่อให้เองแบบ "Sugar 500ml"
#    แล้ว**รายงานว่าย่อเอง** ให้คนมาเติมแมปตรงนี้ ไม่ใช่ปล่อยให้ชื่อดิบขึ้นหน้าเว็บ
NAME_MAP = {
    'Sugar (Sugar-500ml+Spray)': 'Sugar 500ml',
    'Sugar (Sugar-3L แถมขวดสเปรย์)': 'Sugar 3L',
    'Wool duster-ไม้ปัดขนแกะ': 'Wool Duster',
    'Refresh wipes': 'Refresh Wipes',
    'Interior (Interior-500ml+Spray)': 'Interior 500ml',
    'Interior wipes': 'Interior Wipes',
    'Spot (Spot-500ml)': 'Spot 500ml',
    'Refresh (Refresh-500ml+หัวโฟม สีขาว)': 'Refresh 500ml',
    'Perfect': 'Perfect',
    'Reflex (Reflex-250ml+Spray)': 'Reflex 250ml',
    'Reflex (Reflex-500ml+Spray)': 'Reflex 500ml',
    'Xglass (Xglass-100ml)': 'X-Glass 100ml',
    'Tire&trim gel (Tire&trim gel-500ml)': 'Tire&Trim 500ml',
    'Martini': 'Martini',
    'Quartz shampoo (Quartz shampoo-1L)': 'Quartz Shampoo 1L',
}

RAW_TOL = 0.005        # เกณฑ์กระทบยอด xlsx vs RAW (แหล่งเดียวกัน จึงแคบได้)
RAW_MAX_AGE_DAYS = 10  # RAW เขียนทุกวันจันทร์ -> เก่าเกิน 10 วัน = งานรายสัปดาห์ไม่ได้รัน
TOP_SHARE_MIN = 0.40   # 15 แถวบนต้องกินยอดอย่างน้อยเท่านี้ของยอดรวมทั้งหมด (จริง ~60%)
INFO = {'Shopee': 'SH_REV', 'TikTok': 'TK_REV', 'Lazada': 'LZ_REV'}
TH_M = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
        'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']


def load_raw():
    """อ่าน const RAW จาก Data Shipnity/Sales_Dashboard.html (ผลงานของ process_shipnity)"""
    m = re.search(r'const RAW\s*=\s*(\{.*?\});',
                  RAW_SRC.read_text(encoding='utf-8'), re.S)
    if not m:
        print('⛔ หา const RAW ใน %s ไม่เจอ' % RAW_SRC.name, file=sys.stderr)
        sys.exit(1)
    R = json.loads(m.group(1))
    return {'channels': [str(c) for c in R['channels']], 'products': R['products'],
            'lines': R['lines'], 'date_min': R['date_min'], 'date_max': R['date_max']}


def load_xlsx():
    """เรียก process_shipnity() ของ wibwub_update.py ตัวจริง (อ่าน .xlsx อย่างเดียว)"""
    spec = importlib.util.spec_from_file_location('_wu', BASE / 'wibwub_update.py')
    wu = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wu)
    raw = wu.process_shipnity()
    if not raw:
        print('⛔ process_shipnity() คืนค่าว่าง — อ่านไฟล์ Shipnity ไม่ได้', file=sys.stderr)
        sys.exit(1)
    raw['channels'] = [str(c) for c in raw['channels']]
    return raw


def web_name(p):
    """ป้ายบนหน้าเว็บ · คืน (ชื่อ, ย่อเองไหม)"""
    if p in NAME_MAP:
        return NAME_MAP[p], False
    m = re.match(r'^(.+?)\s*\(\1[-\s]*([0-9]+(?:\.[0-9]+)?\s*(?:ml|ML|l|L))', p)
    if m:
        return '%s %s' % (m.group(1).strip(), m.group(2).replace(' ', '')), True
    return re.sub(r'\s*\(.*', '', p).strip() or p, True


def col_map(chan):
    """ดัชนีช่องทางของ Shipnity -> ชื่อคอลัมน์ในตาราง"""
    out = {}
    for ci, cname in enumerate(chan):
        key = str(cname).lower().strip()
        hit = OTHER
        for label, keys in COLS:
            if key in keys:
                hit = label
                break
        else:
            if key in NON_SALE:
                hit = NONSALE_COL
        out[ci] = hit
    return out


def aggregate(raw, top_n):
    """รวมยอดเป็นก้อนเดียวที่หน้าเว็บใช้ทั้งตารางและสองกราฟ"""
    chan, prods = raw['channels'], raw['products']
    cof = col_map(chan)
    cols = [c[0] for c in COLS] + [OTHER]

    per_prod = defaultdict(lambda: defaultdict(float))
    per_prod_q = defaultdict(int)
    nonsale = defaultdict(float)
    per_month = defaultdict(lambda: defaultdict(float))
    ch_all = defaultdict(float)
    for ln in raw['lines']:
        p, c = prods[ln['p']], cof.get(ln['c'], OTHER)
        if c == NONSALE_COL:
            nonsale[p] += ln['s']
            continue
        per_prod[p][c] += ln['s']
        per_prod_q[p] += ln['q']
        per_month[ln['d'][:7]][c] += ln['s']
        ch_all[c] += ln['s']

    def tot(p):
        return sum(per_prod[p].values())

    top = sorted(per_prod, key=tot, reverse=True)[:top_n]
    guessed, rows = [], []
    for p in top:
        n, g = web_name(p)
        if g:
            guessed.append((p, n))
        rows.append({'n': n, 'raw': p,
                     'v': [round(per_prod[p].get(c, 0.0), 2) for c in cols],
                     't': round(tot(p), 2), 'q': per_prod_q[p],
                     'x': round(nonsale.get(p, 0.0), 2)})
    ch_top = defaultdict(float)
    for p in top:
        for c, v in per_prod[p].items():
            ch_top[c] += v
    return {'cols': cols, 'rows': rows, 'per_prod': per_prod, 'per_month': per_month,
            'all_total': round(sum(tot(p) for p in per_prod), 2),
            'all_qty': sum(per_prod_q.values()),
            'top_total': round(sum(tot(p) for p in top), 2),
            'products_total': len(per_prod),
            'nonsale_total': round(sum(nonsale.values()), 2),
            'ch_all': {c: round(ch_all.get(c, 0.0), 2) for c in cols},
            'ch_top': {c: round(ch_top.get(c, 0.0), 2) for c in cols},
            'guessed': guessed}


def payload(raw, ag):
    """ก้อน JSON ที่จะเขียนเป็น const PROD_CHANNEL (ไม่มีชื่อคน ไม่มีข้อมูลลูกค้า)"""
    return {
        'date_min': raw['date_min'], 'date_max': raw['date_max'],
        'generated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
        'src': RAW_SRC.name, 'cols': ag['cols'], 'rows': ag['rows'],
        'all_total': ag['all_total'], 'all_qty': ag['all_qty'],
        'top_total': ag['top_total'], 'products_total': ag['products_total'],
        'nonsale_total': ag['nonsale_total'], 'nonsale_labels': NON_SALE_LABELS,
        'ch_all': ag['ch_all'], 'ch_top': ag['ch_top'],
    }


def gates(raw, ag, pay):
    """ด่านก่อนเขียน — ทุกข้อเป็น "ของตัวเองเทียบของตัวเอง" ไม่พึ่งหน้าอื่น"""
    bad = []
    try:
        age = (datetime.date.today()
               - datetime.date.fromisoformat(raw['date_max'])).days
    except Exception as e:
        return ['อ่าน date_max ไม่ได้: %s' % e]
    if age > RAW_MAX_AGE_DAYS:
        bad.append('ข้อมูลเก่า %d วัน (date_max %s) เกินเกณฑ์ %d วัน — '
                   'งาน "Shipnity รายสัปดาห์" น่าจะไม่ได้รัน ยังไม่เขียนทับของเดิม'
                   % (age, raw['date_max'], RAW_MAX_AGE_DAYS))
    if len(ag['rows']) != 15:
        bad.append('ได้ %d แถว ไม่ใช่ 15 แถวตามของจริงบนหน้าเว็บ' % len(ag['rows']))
    for r in ag['rows']:
        if r['t'] <= 0 or r['q'] <= 0:
            bad.append('แถว %s ยอดหรือจำนวนเป็นศูนย์' % r['n'])
        s = round(sum(r['v']), 2)
        if abs(s - r['t']) > 1.0:
            bad.append('แถว %s ผลรวมคอลัมน์ %.2f ไม่เท่ากับยอดรวม %.2f' % (r['n'], s, r['t']))
    if len(set(r['n'] for r in ag['rows'])) != len(ag['rows']):
        bad.append('มีป้ายชื่อซ้ำกันในตาราง (แมปชื่อชนกัน)')
    if ag['all_total'] <= 0 or ag['top_total'] / ag['all_total'] < TOP_SHARE_MIN:
        bad.append('15 แถวบนกินยอดแค่ %.1f%% ของทั้งหมด ต่ำกว่าเกณฑ์ %.0f%%'
                   % (100 * ag['top_total'] / max(ag['all_total'], 1), TOP_SHARE_MIN * 100))
    cs = round(sum(ag['ch_all'].values()), 2)
    if abs(cs - ag['all_total']) > 1.0:
        bad.append('ยอดรายช่องทางรวม %.2f ไม่เท่ากับยอดรวมทั้งหมด %.2f' % (cs, ag['all_total']))
    return bad


def recon_vs_raw(ag_x, raw_x):
    """กระทบยอด xlsx vs RAW รายเดือน×ช่องทาง (ใช้เฉพาะ --source xlsx)"""
    R = load_raw()
    cof_r, cof_x = col_map(R['channels']), col_map(raw_x['channels'])
    cut = R['date_max'][:7]       # เดือนสุดท้ายอาจเก็บไม่ครบวัน -> ไม่นับ
    old, new = defaultdict(float), defaultdict(float)
    for ln in R['lines']:
        c = cof_r.get(ln['c'], OTHER)
        if c != NONSALE_COL:
            old[(ln['d'][:7], c)] += ln['s']
    for ln in raw_x['lines']:
        c = cof_x.get(ln['c'], OTHER)
        if c != NONSALE_COL:
            new[(ln['d'][:7], c)] += ln['s']
    rows, fails = [], []
    for k in sorted(set(old) | set(new)):
        if k[0] >= cut:
            continue
        a_, b_ = old.get(k, 0.0), new.get(k, 0.0)
        d = abs(a_ - b_) / max(a_, b_, 1.0)
        rows.append({'month': k[0], 'channel': k[1], 'raw': round(a_, 2),
                     'now': round(b_, 2), 'diff_pct': round(d * 100, 3)})
        if d > RAW_TOL:
            fails.append('%s %s ต่างจาก RAW %.2f%% (RAW %.0f vs .xlsx %.0f)'
                         % (k[1], k[0], d * 100, a_, b_))
    print('กระทบยอด .xlsx vs %s (เกณฑ์ %.1f%% · เดือน %s ยังไม่ครบ ไม่นับ): '
          '%d คู่ · ไม่ผ่าน %d คู่' % (RAW_SRC.name, RAW_TOL * 100, cut,
                                        len(rows), len(fails)))
    for r in sorted(rows, key=lambda r: -r['diff_pct'])[:3]:
        print('   ต่างมากสุด: %-14s %s  %.3f%%' % (r['channel'], r['month'], r['diff_pct']))
    return rows, fails


def arr(html, name):
    m = re.search(r'const %s\s*=\s*\[([^\]]*)\]' % name, html)
    if not m:
        return None
    out = []
    for x in m.group(1).split(','):
        x = x.strip().strip("'\"")
        if not x:
            continue
        try:
            out.append(float(x))
        except ValueError:
            out.append(x)
    return out


def seller_center_info(ag, html):
    """ข้อมูลประกอบ (ไม่ใช่ด่าน) — ช่องว่าง Shipnity vs Seller Center รายเดือน"""
    m5, info = arr(html, 'M5') or [], []
    months = sorted(ag['per_month'])
    cur = months[-1] if months else ''
    for col, name in INFO.items():
        vals = arr(html, name)
        if vals is None:
            continue
        for mi, lbl in enumerate(m5):
            if mi >= len(vals) or lbl not in TH_M:
                continue
            ym = '2026-%02d' % (TH_M.index(lbl) + 1)
            if ym not in ag['per_month']:
                continue
            ship, page = ag['per_month'][ym][col], float(vals[mi])
            info.append({'channel': col, 'month': lbl, 'shipnity': round(ship, 2),
                         'seller_center': round(page, 2),
                         'gap_pct': round((ship - page) / page * 100 if page else 0.0, 2),
                         'partial': ym == cur})
    return info


def write_const(pay):
    """แทน const PROD_CHANNEL ในหน้าเว็บ · คืน True ถ้าเนื้อไฟล์เปลี่ยนจริง"""
    html = PAGE.read_text(encoding='utf-8')
    body = json.dumps(pay, ensure_ascii=False, separators=(',', ':'))
    new = 'const PROD_CHANNEL = %s;' % body
    pat = re.compile(r'const PROD_CHANNEL = \{.*?\};', re.S)
    if not pat.search(html):
        print('⛔ หา const PROD_CHANNEL ในหน้าเว็บไม่เจอ — ต้องใส่ที่ยึดก่อน '
              '(งานนี้แก้เฉพาะค่า ไม่สร้างโครงหน้าเว็บเอง)', file=sys.stderr)
        sys.exit(1)
    old = pat.search(html).group(0)
    # เทียบโดยไม่สน generated เพื่อไม่ให้ commit ทุกรอบที่ข้อมูลเหมือนเดิม
    strip = lambda s: re.sub(r'"generated":"[^"]*",?', '', s)
    if strip(old) == strip(new):
        return False
    out = pat.sub(lambda _: new, html, count=1)
    if len(out) < len(html) * 0.5:
        print('⛔ ไฟล์จะหดเกินครึ่ง — ไม่เขียน', file=sys.stderr)
        sys.exit(1)
    PAGE.write_text(out, encoding='utf-8')
    return True


def commit():
    """commit เฉพาะไฟล์ของตัวเองผ่าน gitw.py (ห้ามเรียก git ตรง ห้ามไม่ระบุ path)"""
    rel = PAGE.name
    r = subprocess.run(GITW + ['add', '--', rel], cwd=str(BASE),
                       capture_output=True, text=True)
    if r.returncode:
        return 'ADD_FAILED: ' + (r.stderr or r.stdout)[:200]
    msg = ('auto-update: ตารางสินค้าขายดีแยกช่องทาง %s'
           % datetime.date.today().isoformat())
    r = subprocess.run(GITW + ['-c', 'user.name=WIBWUB Bot',
                               '-c', 'user.email=marketingwibwub@gmail.com',
                               'commit', '-m', msg], cwd=str(BASE),
                       capture_output=True, text=True)
    if r.returncode:
        return 'COMMIT_FAILED(%d): %s' % (r.returncode, (r.stderr or r.stdout)[:200])
    sha = subprocess.run(GITW + ['rev-parse', '--short', 'HEAD'], cwd=str(BASE),
                         capture_output=True, text=True).stdout.strip()
    return sha


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--dry-run', action='store_true', help='อ่านอย่างเดียว ไม่เขียนไฟล์')
    g.add_argument('--write', action='store_true', help='เขียน const PROD_CHANNEL + commit')
    ap.add_argument('--source', choices=['raw', 'xlsx'], default='raw')
    ap.add_argument('--top', type=int, default=15, help='จำนวนแถว (ของจริง 15 แถว)')
    ap.add_argument('--no-commit', action='store_true', help='เขียนแต่ไม่ commit')
    ap.add_argument('--json', default='', help='เขียนผลลัพธ์เป็น JSON ไว้ดู (นอกรีโป)')
    a = ap.parse_args()

    raw = load_xlsx() if a.source == 'xlsx' else load_raw()
    ag = aggregate(raw, a.top)
    pay = payload(raw, ag)
    html = PAGE.read_text(encoding='utf-8')

    print('ช่วงข้อมูล %s → %s · สินค้า %d รายการ · %d แถวบนสุด (แหล่ง: %s)'
          % (raw['date_min'], raw['date_max'], ag['products_total'], a.top, a.source))
    print('ยอดขายรวมทุกสินค้า %.0f · 15 แถวบน %.0f (%.1f%%) · ไม่ใช่การขาย %.0f'
          % (ag['all_total'], ag['top_total'],
             100 * ag['top_total'] / max(ag['all_total'], 1), ag['nonsale_total']))
    print('ช่องทาง -> คอลัมน์:')
    cof = col_map(raw['channels'])
    for ci, cname in enumerate(raw['channels']):
        print('   %-28s -> %s' % (cname, cof[ci]))
    print('\n%d แถวบนสุด:' % a.top)
    for i, r in enumerate(ag['rows'], 1):
        print('   %2d. %-18s รวม %12.0f  จำนวน %7d  | %s'
              % (i, r['n'], r['t'], r['q'],
                 '  '.join('%s %.0f' % (c, v) for c, v in zip(ag['cols'], r['v']) if v)))
    if ag['guessed']:
        print('\n⚠️ ย่อชื่อให้เอง %d รายการ — ควรเติมใน NAME_MAP:' % len(ag['guessed']))
        for p, n in ag['guessed']:
            print('   %r -> %r' % (p, n))

    info = seller_center_info(ag, html)
    print('\nข้อมูลประกอบ (ไม่ใช่ด่าน) — Shipnity เทียบยอด Seller Center รายเดือน:')
    print('   ช่องว่างคงที่เป็นเรื่องปกติ (คนละขอบเขต) · ที่ต้องดูคือเดือนที่'
          'ช่องว่าง**เปลี่ยนรูปร่าง**')
    for col in INFO:
        rs = [r for r in info if r['channel'] == col]
        if rs:
            print('   %-7s ' % col + ' '.join('%s%+.0f%%' % (r['month'], r['gap_pct'])
                                              for r in rs))

    fails = gates(raw, ag, pay)
    recon = []
    if a.source == 'xlsx':
        recon, rf = recon_vs_raw(ag, raw)
        fails += rf

    if a.json:
        Path(a.json).write_text(json.dumps(
            {'payload': pay, 'guessed': ag['guessed'], 'seller_center_gap': info,
             'recon': recon, 'failures': fails}, ensure_ascii=False, indent=1),
            encoding='utf-8')
        print('\nเขียน JSON ไว้ที่', a.json)

    if fails:
        print('\n⛔ ด่านไม่ผ่าน %d ข้อ — หยุด ไม่เขียนอะไรทั้งนั้น:' % len(fails),
              file=sys.stderr)
        for f in fails:
            print('   ·', f, file=sys.stderr)
        return 11
    print('\n✅ ด่านผ่านทุกข้อ')

    if a.dry_run:
        print('(--dry-run: ไม่เขียนไฟล์)')
        return 0
    if not write_const(pay):
        print('ไม่มีอะไรเปลี่ยน — ไม่เขียน ไม่ commit')
        return 10
    print('เขียน const PROD_CHANNEL ลง %s แล้ว' % PAGE.name)
    if a.no_commit:
        print('(--no-commit: ไม่ commit)')
        return 0
    print('commit:', commit())
    return 0


if __name__ == '__main__':
    sys.exit(main())
