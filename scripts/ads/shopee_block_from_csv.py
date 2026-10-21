#!/usr/bin/env python3
"""สร้างบล็อก `shopee:{...}` ของ DATA_PERIODS.<เดือน> จาก CSV รายงาน Shopee Ads

ใช้:  python3 scripts/ads/shopee_block_from_csv.py <csv path> [--check <ไฟล์บล็อกเดิม>]

ที่มาของรูปแบบตัวเลข (ห้ามเปลี่ยน — ไฟล์จริงถูกเขียนด้วยกติกานี้มาตลอด):
  ระดับบนสุด  spend/revenue = %.2f · orders/imp/clicks = int · roas/ctr/cvr/cpa = %.2f
  ในแคมเปญ    spend/revenue = %.2f · roas/ctr/cvr/cpa = repr(round(x,2)) (เช่น 6.5, 0.0)
              และ cpa = 0 (int) เมื่อ orders == 0

คอลัมน์ (ยืนยันกับ header row ทุกครั้ง ไม่ hardcode เฉย ๆ):
  11 imp · 12 clicks · 16 orders · 24 revenue · 26 spend
"""
import argparse, csv, io, json, os, sys

COLS = {'imp': 11, 'clicks': 12, 'orders': 16, 'revenue': 24, 'spend': 26}
HDR = {'imp': 'การมองเห็น', 'clicks': 'จำนวนคลิก', 'orders': 'การสั่งซื้อ',
       'revenue': 'ยอดขาย', 'spend': 'ค่าโฆษณา'}


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail},
                     ensure_ascii=False))
    sys.exit(2)


def num(s):
    s = (s or '').strip().replace(',', '')
    if not s or s == '-':
        return 0.0
    return float(s)


def read_csv(path):
    rows = list(csv.reader(io.StringIO(
        io.open(path, encoding='utf-8-sig', errors='replace').read())))
    hi = next((i for i, r in enumerate(rows) if r and r[0].strip() == 'ลำดับ'), None)
    if hi is None:
        die('ไม่พบ header row ที่มีคำว่า "ลำดับ"', path)
    hdr = [c.strip() for c in rows[hi]]
    for k, idx in COLS.items():
        if len(hdr) <= idx or hdr[idx] != HDR[k]:
            die('คอลัมน์ไม่ตรงกับที่คาด — รูปแบบรายงานเปลี่ยน',
                {'key': k, 'index': idx, 'expect': HDR[k],
                 'got': hdr[idx] if len(hdr) > idx else None})
    period = next((r[1].strip() for r in rows[:hi]
                   if r and r[0].strip() == 'ระยะเวลา'), None)
    camps = []
    for r in rows[hi + 1:]:
        if not r or not r[0].strip().isdigit():
            continue
        c = {k: num(r[i]) for k, i in COLS.items()}
        c['name'] = r[1].strip()
        camps.append(c)
    return period, hdr, camps


def derive(c):
    spend, rev = c['spend'], c['revenue']
    orders, clicks, imp = c['orders'], c['clicks'], c['imp']
    return {
        'name': c['name'], 'spend': spend, 'revenue': rev,
        'orders': int(orders), 'imp': int(imp), 'clicks': int(clicks),
        'roas': rev / spend if spend else 0.0,
        'ctr': clicks / imp * 100 if imp else 0.0,
        'cvr': orders / clicks * 100 if clicks else 0.0,
        'cpa': spend / orders if orders else None,
    }


def camp_js(d):
    name = d['name'].replace('\\', '\\\\').replace('"', '\\"')
    r2 = lambda x: repr(round(x, 2))
    cpa = '0' if d['cpa'] is None else r2(d['cpa'])
    return ('{name:"%s",spend:%.2f,revenue:%.2f,orders:%d,imp:%d,clicks:%d,'
            'roas:%s,ctr:%s,cvr:%s,cpa:%s}'
            % (name, d['spend'], d['revenue'], d['orders'], d['imp'],
               d['clicks'], r2(d['roas']), r2(d['ctr']), r2(d['cvr']), cpa))


def build(camps):
    rows = [derive(c) for c in camps if c['spend'] > 0]
    allr = sorted(rows, key=lambda d: -d['spend'])
    top5 = allr[:5]
    worst5 = sorted(rows, key=lambda d: d['roas'])[:5]

    spend = sum(d['spend'] for d in rows)
    rev = sum(d['revenue'] for d in rows)
    orders = sum(d['orders'] for d in rows)
    imp = sum(d['imp'] for d in rows)
    clicks = sum(d['clicks'] for d in rows)
    head = ('shopee:{spend:%.2f,revenue:%.2f,orders:%d,imp:%d,clicks:%d,'
            'roas:%.2f,ctr:%.2f,cvr:%.2f,cpa:%.2f'
            % (spend, rev, orders, imp, clicks,
               rev / spend if spend else 0.0,
               clicks / imp * 100 if imp else 0.0,
               orders / clicks * 100 if clicks else 0.0,
               spend / orders if orders else 0.0))
    lst = lambda xs: '[' + ','.join(camp_js(d) for d in xs) + ']'
    block = (head + ',top5:' + lst(top5) + ',worst5:' + lst(worst5)
             + ',all:' + lst(allr) + '}')
    totals = {'campaigns': len(rows), 'spend': round(spend, 2),
              'revenue': round(rev, 2), 'orders': orders, 'imp': imp,
              'clicks': clicks, 'roas': round(rev / spend, 2) if spend else 0}
    return block, totals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv')
    ap.add_argument('--check', help='ไฟล์ที่เก็บบล็อกเดิม — เทียบ byte-identical')
    ap.add_argument('--out', help='เขียนบล็อกที่สร้างได้ลงไฟล์นี้')
    a = ap.parse_args()
    if not os.path.isfile(a.csv):
        die('ไม่พบไฟล์ CSV', a.csv)
    period, hdr, camps = read_csv(a.csv)
    block, totals = build(camps)
    rep = {'status': 'OK', 'csv': os.path.basename(a.csv), 'period': period,
           'rows_in_csv': len(camps), 'totals': totals, 'block_len': len(block)}
    if a.check:
        old = io.open(a.check, encoding='utf-8').read().strip()
        rep['check_file'] = os.path.basename(a.check)
        rep['identical'] = (old == block)
        if not rep['identical']:
            n = min(len(old), len(block))
            i = next((i for i in range(n) if old[i] != block[i]), n)
            rep['first_diff_at'] = i
            rep['old_at_diff'] = old[max(0, i - 60):i + 60]
            rep['new_at_diff'] = block[max(0, i - 60):i + 60]
    if a.out:
        io.open(a.out, 'w', encoding='utf-8').write(block)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
