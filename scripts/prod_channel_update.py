#!/usr/bin/env python3
"""กลุ่ม B — แหล่งข้อมูล "ตารางสินค้าขายดี แยกช่องทาง" ในหน้า WIBWUB_Dashboard.html

ที่มา (9 พ.ย. 69): ตารางนั้นเป็น <tr><td> พิมพ์มือ 15 แถว × 9 ช่องทาง ไม่มี id ไม่มี JS
ไม่มีอาเรย์ต้นทาง · ป้ายใต้หัวตารางบอกเองว่าคอลัมน์แยกช่องทาง "คำนวณจากไฟล์ Shipnity
ม.ค.–11 ก.ย. 69 เท่านั้น" และยอดรวมหยุดที่ 8 ต.ค. — ไม่มีสคริปต์ไหนแตะมาตั้งแต่นั้น

⚠️ รอบนี้ **อ่านอย่างเดียว** (--dry-run เท่านั้น) ไม่เขียนไฟล์ ไม่ commit ไม่แตะหน้าเว็บ
   โหมดเขียนเป็นงานกลุ่ม C ซึ่งผู้ใช้ยังไม่อนุมัติ

ทำไมไม่ parse .xlsx เอง
──────────────────────────────────────────────────────────────────────────────
`wibwub_update.process_shipnity()` รวมยอดเป็น agg[(วันที่, สินค้า, ช่องทาง)] อยู่แล้ว
พร้อม dedup (order_id, สินค้า) ที่กันไฟล์ export ซ้อนทับกัน และมี CHANNEL_MAP ของตัวเอง
ถ้าเขียนตัวอ่านใหม่ = มีกติกาสองชุดที่ไม่มีอะไรบังคับให้ตรงกัน (บั๊กคลาสเดิมของรีโปนี้)
จึง **import มาเรียก** · ถ้าดัชนีคอลัมน์ของ Shipnity เปลี่ยน ทั้งสองหน้าจะเปลี่ยนพร้อมกัน

ไม่ใช้ `Data Shipnity/Sales_Dashboard.html` (const RAW) เป็นแหล่ง เพราะไฟล์นั้นค้าง
ตั้งแต่ 2 พ.ย. 69 (date_max 2026-11-02) — สดน้อยกว่าไฟล์ .xlsx ที่มีถึงวันนี้

ใช้:  python3 scripts/prod_channel_update.py --dry-run [--top N] [--json ไฟล์]
exit: 0 = ด่านกระทบยอดผ่าน · 11 = ด่านไม่ผ่าน (รายงานแล้ว ไม่เขียนอะไร) · 1 = ผิดพลาด
"""
import argparse, importlib.util, json, re, sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PAGE = BASE / 'WIBWUB_Dashboard.html'

# คอลัมน์ของตารางในหน้าเว็บ (เรียงซ้าย->ขวาตามของจริง) -> ช่องทางของ Shipnity ที่รวมเข้าช่องนี้
# ชื่อช่องทางใน Shipnity มีตัวซ้ำความหมายกันเพราะ CHANNEL_MAP ไม่ได้ normalize ตัวพิมพ์ใหญ่
# ขีดล่าง ('LINE_OA' กับ 'Line OA' เป็นสองช่องแยกกันในข้อมูลจริง) — รวมให้ตรงนี้
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
# ตัวเลขในตารางปัจจุบันรวมพวกนี้ไว้ในคอลัมน์ "อื่นๆ" หรือไม่ ยังไม่รู้ (ตารางพิมพ์มือ)
# จึงรายงานทั้งสองแบบ แล้วให้ผู้ใช้ตัดสิน ⛔ ห้ามสคริปต์เลือกแทน
NON_SALE = ['เบิกของ', 'สินค้าสำหรับทำการตลาด', 'marketing']
# ── ด่านกระทบยอด: เทียบกับ "แหล่งเดียวกัน" เท่านั้น ─────────────────────────
# ด่านจริง (ต้องผ่าน): ยอดรายเดือน×ช่องทาง เทียบกับ const RAW ใน
#   Data Shipnity/Sales_Dashboard.html ซึ่งมาจาก process_shipnity() รอบก่อน
#   = พิสูจน์ว่าการรวมยอดของสคริปต์นี้ตรงกับไปป์ไลน์เดิมทุกบาท
# เกณฑ์แคบได้ (0.5%) เพราะเป็นแหล่งเดียวกัน · นับเฉพาะเดือนที่ RAW เก็บครบแล้ว
RAW_SRC = BASE / 'Data Shipnity' / 'Sales_Dashboard.html'
RAW_TOL = 0.005
# ⛔ ห้ามใช้ SH_REV/TK_REV/LZ_REV เป็นด่าน — ลองแล้ว 9 พ.ย. 69 ไม่ผ่านทุกเดือน
# เพราะคนละขอบเขต: อาเรย์พวกนั้นคือยอดจาก Seller Center ของแต่ละแพลตฟอร์ม
# ส่วนนี่คือยอดรายการสินค้าใน Shipnity (ผู้ใช้ยืนยันว่าสองหน้าไม่เท่ากันโดยตั้งใจ)
# Shopee ต่ำกว่าหน้าเว็บ 8-13% ทุกเดือน · Lazada ต่ำกว่า 16-26% · เป็นช่องว่างคงที่
# เก็บไว้เป็น "ข้อมูลประกอบ" เท่านั้น และดู**รูปร่าง**ของช่องว่างว่าเปลี่ยนผิดปกติไหม
INFO = {'Shopee': 'SH_REV', 'TikTok': 'TK_REV', 'Lazada': 'LZ_REV'}
TH_M = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
        'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']


def load_shipnity():
    """เรียก process_shipnity() ของ wibwub_update.py ตัวจริง (อ่าน .xlsx อย่างเดียว)"""
    spec = importlib.util.spec_from_file_location('_wu', BASE / 'wibwub_update.py')
    wu = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wu)
    raw = wu.process_shipnity()
    if not raw:
        print('⛔ process_shipnity() คืนค่าว่าง — อ่านไฟล์ Shipnity ไม่ได้', file=sys.stderr)
        sys.exit(1)
    return raw


def arr(html, name):
    """ดึงอาเรย์ตัวเลขชื่อ name จาก HTML (รูปแบบเดียวกับ extract_arr ของ wibwub_update)"""
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true', required=True,
                    help='โหมดเดียวที่มีในรอบนี้ — อ่านอย่างเดียว')
    ap.add_argument('--top', type=int, default=15,
                    help='จำนวนแถว (ของจริงในหน้าเว็บคือ 15 แถว ไม่ใช่ 12)')
    ap.add_argument('--json', default='', help='เขียนผลลัพธ์เป็น JSON ไว้ดู (นอกรีโป)')
    a = ap.parse_args()

    raw = load_shipnity()
    chan = raw['channels']
    prods = raw['products']
    # agg[สินค้า][คอลัมน์] = ยอด  ·  และ per_month[เดือน][คอลัมน์] = ยอด (ทุกสินค้า)
    col_of = {}
    for ci, cname in enumerate(chan):
        key = str(cname).lower().strip()
        col_of[ci] = 'อื่นๆ'
        for label, keys in COLS:
            if key in keys:
                col_of[ci] = label
                break
        else:
            if key in NON_SALE:
                col_of[ci] = '(ไม่ใช่การขาย)'
    labels = [c[0] for c in COLS] + ['อื่นๆ', '(ไม่ใช่การขาย)']

    per_prod = defaultdict(lambda: defaultdict(float))
    per_prod_q = defaultdict(int)
    per_month = defaultdict(lambda: defaultdict(float))
    for ln in raw['lines']:
        p = prods[ln['p']]
        c = col_of.get(ln['c'], 'อื่นๆ')
        per_prod[p][c] += ln['s']
        if c != '(ไม่ใช่การขาย)':
            per_prod_q[p] += ln['q']
        per_month[ln['d'][:7]][c] += ln['s']

    def sale_total(p):
        return sum(v for k, v in per_prod[p].items() if k != '(ไม่ใช่การขาย)')

    top = sorted(per_prod, key=sale_total, reverse=True)[:a.top]

    # ── ด่านกระทบยอด (แหล่งเดียวกัน) ─────────────────────────────────────────
    fails, recon = [], []
    rtxt = RAW_SRC.read_text(encoding='utf-8')
    rm = re.search(r'const RAW\s*=\s*(\{.*?\});', rtxt, re.S)
    if not rm:
        fails.append('หา const RAW ใน %s ไม่เจอ — ไม่มีอะไรให้กระทบยอด' % RAW_SRC.name)
        raw_cut = None
    else:
        RO = json.loads(rm.group(1))
        # เดือนสุดท้ายของ RAW ยังเก็บไม่ครบวัน (freeze กลางวัน) -> ตัดเดือนนั้นออก
        raw_cut = RO['date_max'][:7]
        old = defaultdict(float)
        for ln in RO['lines']:
            old[(ln['d'][:7], RO['channels'][ln['c']])] += ln['s']
        new_by_ch = defaultdict(float)
        for ln in raw['lines']:
            new_by_ch[(ln['d'][:7], chan[ln['c']])] += ln['s']
        for k in sorted(set(old) | set(new_by_ch)):
            if k[0] >= raw_cut:
                continue
            a_, b_ = old.get(k, 0.0), new_by_ch.get(k, 0.0)
            d = abs(a_ - b_) / max(a_, b_, 1.0)
            recon.append({'month': k[0], 'channel': k[1], 'raw': round(a_, 2),
                          'now': round(b_, 2), 'diff_pct': round(d * 100, 3)})
            if d > RAW_TOL:
                fails.append('%s %s ต่างจาก RAW %.2f%% (RAW %.0f vs รอบนี้ %.0f)'
                             % (k[1], k[0], d * 100, a_, b_))
        print('ด่านกระทบยอดกับ %s (แหล่งเดียวกัน · เกณฑ์ %.1f%% · เดือน %s ยังไม่ครบ ไม่นับ):'
              % (RAW_SRC.name, RAW_TOL * 100, raw_cut))
        print('   คู่ (เดือน × ช่องทาง) ที่ตรวจ %d คู่ · ไม่ผ่าน %d คู่'
              % (len(recon), sum(1 for r in recon if r['diff_pct'] > RAW_TOL * 100)))
        worst = sorted(recon, key=lambda r: -r['diff_pct'])[:3]
        for r in worst:
            print('   ต่างมากสุด: %-14s %s  %.3f%%' % (r['channel'], r['month'], r['diff_pct']))

    # ── ข้อมูลประกอบ: เทียบกับยอด Seller Center (ไม่ใช่ด่าน) ─────────────────
    html = PAGE.read_text(encoding='utf-8')
    m5 = arr(html, 'M5') or []
    months = sorted(per_month)
    cur = months[-1] if months else ''
    info = []
    for col, name in INFO.items():
        vals = arr(html, name)
        if vals is None:
            info.append({'channel': col, 'month': '-', 'note': 'หาอาเรย์ %s ไม่เจอ' % name})
            continue
        for mi, lbl in enumerate(m5):
            if mi >= len(vals):
                break
            ym = '2026-%02d' % (TH_M.index(lbl) + 1) if lbl in TH_M else None
            if not ym or ym not in per_month:
                continue
            ship, page = per_month[ym][col], float(vals[mi])
            gap = (ship - page) / page * 100 if page else 0.0
            info.append({'channel': col, 'month': lbl, 'shipnity': round(ship, 2),
                         'seller_center': round(page, 2), 'gap_pct': round(gap, 2),
                         'partial': ym == cur})

    # ── รายงาน ───────────────────────────────────────────────────────────────
    out = {'mode': 'dry-run', 'date_min': raw['date_min'], 'date_max': raw['date_max'],
           'products_total': len(prods), 'rows': a.top, 'raw_gate_cut': raw_cut,
           'channels_seen': chan, 'recon': recon, 'recon_failures': fails,
           'seller_center_gap': info,
           'table': [{'rank': i + 1, 'product': p,
                      'cols': {k: round(per_prod[p].get(k, 0.0), 2) for k in labels},
                      'total_sale': round(sale_total(p), 2),
                      'total_with_nonsale': round(sum(per_prod[p].values()), 2),
                      'qty': per_prod_q[p]} for i, p in enumerate(top)]}
    print('ช่วงข้อมูล Shipnity: %s → %s · สินค้า %d รายการ · %d แถวบนสุด'
          % (raw['date_min'], raw['date_max'], len(prods), a.top))
    print('ช่องทางที่เจอในข้อมูล -> คอลัมน์ในตาราง:')
    for ci, cname in enumerate(chan):
        print('   %-28s -> %s' % (cname, col_of[ci]))
    print('\nข้อมูลประกอบ (ไม่ใช่ด่าน) — Shipnity เทียบยอด Seller Center รายเดือน:')
    print('   ช่องว่างคงที่เป็นเรื่องปกติ (คนละขอบเขต) · ที่ต้องดูคือเดือนที่ช่องว่าง'
          '**เปลี่ยนรูปร่าง**')
    for col in INFO:
        rs = [r for r in info if r.get('channel') == col and 'gap_pct' in r]
        if rs:
            print('   %-7s ' % col + ' '.join('%s%+.0f%%' % (r['month'], r['gap_pct'])
                                              for r in rs))
    print('\n%d แถวบนสุด (ยอดขายไม่รวมช่องที่ไม่ใช่การขาย):' % a.top)
    for row in out['table']:
        print('   %2d. %-22s รวม %12.0f  จำนวน %7d  | %s'
              % (row['rank'], row['product'], row['total_sale'], row['qty'],
                 '  '.join('%s %.0f' % (k, v) for k, v in row['cols'].items() if v)))
    if a.json:
        Path(a.json).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
        print('\nเขียน JSON ไว้ที่', a.json)
    if fails:
        print('\n⛔ ด่านกระทบยอดไม่ผ่าน %d ข้อ — หยุด ไม่เขียนอะไรทั้งนั้น:' % len(fails),
              file=sys.stderr)
        for f in fails:
            print('   ·', f, file=sys.stderr)
        return 11
    print('\n✅ ด่านกระทบยอดผ่าน')
    return 0


if __name__ == '__main__':
    sys.exit(main())
