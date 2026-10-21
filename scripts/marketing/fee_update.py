#!/usr/bin/env python3
"""เพิ่ม/ตรวจอัตราค่าธรรมเนียมแพลตฟอร์มใน data Ads/platform_fee.json

ทำไมต้องมี: Shopee และ TikTok ปรับค่าธรรมเนียมขึ้นเรื่อย ๆ (ปี 69 ขึ้นทั้งคู่
ช่วง พ.ค. และ ก.ค.) ถ้าไม่ตามอัปเดต ตัวเลข "ยอดขายหลังหักค่าธรรมเนียม" บนหน้า
"การตลาด vs ยอดขาย" จะค่อย ๆ ผิดมากขึ้นโดยไม่มีอะไรเตือน

คำสั่ง
  shopee --month YYYY-MM
      ถอดอัตรา Shopee จาก SH_FEE ÷ SH_REV ในหน้า WIBWUB_Dashboard.html
      (ฝ่ายบัญชีกรอกไว้อยู่แล้ว ไม่ต้องเปิดเบราว์เซอร์)

  tiktok --month YYYY-MM --revenue N --fee N [--aff N] [--aff-ads N]
      ใส่ยอดที่อ่านมาจากแผง "รายงานธุรกิจ" ของ TikTok Seller Center
      (ใช้ scripts/marketing/fee_scrape.js อ่านค่า)
      ถ้าใส่ --aff/--aff-ads ด้วย จะแยกค่าคอมแอฟฟิลิเอตออกมาเป็นอีกก้อน
      แล้วอัตราค่าธรรมเนียมจะเหลือเฉพาะส่วนที่ไม่ใช่ค่าคอม (กันนับซ้ำ)

  show
      แสดงอัตราปัจจุบันทั้งหมด

กฎ: ห้ามเขียนทับเดือนที่มีอยู่แล้ว ถ้าต้องแก้จริง ๆ ให้ใส่ --force
     (อัตราเก่าถูกใช้คำนวณย้อนหลังไปแล้ว การแก้เงียบ ๆ ทำให้ตัวเลขขยับโดยไม่มีใครรู้)
exit: 0 = เพิ่มแล้ว · 10 = มีอยู่แล้วและค่าตรงกัน (ไม่ต้องทำอะไร) · 2 = ไม่ผ่านด่าน
"""
import sys, re, json, argparse
from pathlib import Path

BASE = Path('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com'
            '/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All')
FEE = BASE / 'data Ads' / 'platform_fee.json'
PAGE = BASE / 'WIBWUB_Dashboard.html'
MKEYS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def load():
    if not FEE.exists(): die('ไม่พบ data Ads/platform_fee.json')
    return json.load(open(FEE, encoding='utf-8'))


def arr(name):
    """อ่าน const <name> = [...] จากหน้าเว็บ"""
    h = PAGE.read_text(encoding='utf-8')
    m = re.search(r'const ' + name + r'\s*=\s*\[([^\]]*)\]', h)
    if not m: die(f'ไม่พบ {name} ในหน้าเว็บ')
    return [float(x) for x in m.group(1).split(',')]


# ค่าคอมแอฟฟิลิเอตไม่ใช่ "ค่าธรรมเนียม" แต่เป็นค่าจ้างครีเอเตอร์ที่จ่ายผ่านแพลตฟอร์ม
# จึงเก็บแยกใน marketing_rates และให้หน้าเว็บวางไว้กลุ่มเดียวกับ KOL
MKT_RATE_META = {
    'aff_tk': {'base': 'tk', 'label': 'คอมแอฟฟิลิเอต TikTok', 'group': 'kol', 'color': '#c084fc'},
}


def put(cfg, key, month, rate, force, extra=None):
    """ใส่อัตราของเดือนนั้น — ห้ามทับของเดิม"""
    rate = round(rate, 5)
    if key in MKT_RATE_META:
        box = cfg.setdefault('marketing_rates', {}).setdefault(key, dict(MKT_RATE_META[key], rates=[]))
        return put_spec(box, 'rates', key, month, rate, force, extra, cfg)
    spec = cfg['rates'].get(key)
    if isinstance(spec, (int, float)):          # เดิมเป็นอัตราคงที่ -> แปลงเป็นช่วง
        spec = [{'from': '2026-01-01', 'rate': spec}]
    spec = spec or []
    frm = month + '-01'
    cur = next((s for s in spec if s['from'] == frm), None)
    if cur and not force:
        if abs(cur['rate'] - rate) < 1e-9:
            return False, f'{key} {month} มีอยู่แล้วและค่าตรงกัน ({rate*100:.3f}%)'
        die('เดือนนี้มีอัตราอยู่แล้วและค่าไม่ตรง — ห้ามเขียนทับเงียบ ๆ (ใส่ --force ถ้าตั้งใจ)',
            {'คีย์': key, 'เดือน': month, 'เดิม': cur['rate'], 'ใหม่': rate})
    if cur: cur['rate'] = rate
    else: spec.append({'from': frm, 'rate': rate})
    cfg['rates'][key] = squash(spec)
    if extra: cfg.setdefault('_บันทึก', {})[f'{key} {month}'] = extra
    return True, f'{key} {month} = {rate*100:.3f}%'


def squash(spec):
    """เรียงตามวันที่ แล้วตัดช่วงที่อัตราเท่ากับช่วงก่อนหน้าทิ้ง"""
    spec.sort(key=lambda s: s['from'])
    out = []
    for s in spec:
        if out and abs(out[-1]['rate'] - s['rate']) < 1e-9: continue
        out.append(s)
    return out


def put_spec(box, field, key, month, rate, force, extra, cfg):
    spec = box.get(field) or []
    frm = month + '-01'
    cur = next((s for s in spec if s['from'] == frm), None)
    if cur and not force:
        if abs(cur['rate'] - rate) < 1e-9:
            return False, f'{key} {month} มีอยู่แล้วและค่าตรงกัน ({rate*100:.3f}%)'
        die('เดือนนี้มีอัตราอยู่แล้วและค่าไม่ตรง — ห้ามเขียนทับเงียบ ๆ (ใส่ --force ถ้าตั้งใจ)',
            {'คีย์': key, 'เดือน': month, 'เดิม': cur['rate'], 'ใหม่': rate})
    if cur: cur['rate'] = rate
    else: spec.append({'from': frm, 'rate': rate})
    box[field] = squash(spec)
    if extra: cfg.setdefault('_บันทึก', {})[f'{key} {month}'] = extra
    return True, f'{key} {month} = {rate*100:.3f}%'


def save(cfg):
    FEE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def cmd_shopee(a):
    cfg = load()
    y, m = a.month.split('-')
    if y != '2026': die('รองรับเฉพาะปี 2026 (อาเรย์ในหน้าเว็บเป็นรายเดือนของปีนั้น)')
    i = int(m) - 1
    rev, fee = arr('SH_REV'), arr('SH_FEE')
    if i >= len(rev) or not rev[i]: die('เดือนนี้ยังไม่มียอดขาย Shopee ในหน้าเว็บ', a.month)
    if not fee[i]: die('เดือนนี้ยังไม่ได้กรอกค่าธรรมเนียม Shopee (SH_FEE = 0) — รอฝ่ายบัญชีกรอกก่อน', a.month)
    changed, msg = put(cfg, 'sh', a.month, fee[i] / rev[i], a.force,
                       {'ยอดขาย': rev[i], 'ค่าธรรมเนียม': fee[i], 'ที่มา': 'SH_FEE/SH_REV'})
    if not changed:
        print(json.dumps({'status': 'NO_CHANGE', 'msg': msg}, ensure_ascii=False)); return 10
    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', 'msg': msg}, ensure_ascii=False)); return 0
    save(cfg); print(json.dumps({'status': 'UPDATED', 'msg': msg}, ensure_ascii=False)); return 0


def cmd_tiktok(a):
    cfg = load()
    if a.revenue <= 0: die('revenue ต้องมากกว่า 0')
    if not 0 < a.fee < a.revenue: die('fee ต้องมากกว่า 0 และน้อยกว่า revenue', {'fee': a.fee, 'revenue': a.revenue})
    aff = (a.aff or 0) + (a.aff_ads or 0)
    if aff > a.fee: die('ค่าคอมแอฟฟิลิเอตมากกว่าค่าธรรมเนียมรวม — อ่านตัวเลขผิดแน่', {'aff': aff, 'fee': a.fee})
    msgs = []
    # แยกค่าคอมแอฟฟิลิเอตออกเป็นอีกก้อน -> อัตราค่าธรรมเนียมต้องหักส่วนนั้นออก กันนับซ้ำ
    fee_rate = (a.fee - aff) / a.revenue if aff else a.fee / a.revenue
    ch, m = put(cfg, 'tk', a.month, fee_rate, a.force,
                {'รายได้': a.revenue, 'ค่าธรรมเนียมรวม': a.fee, 'คอมแอฟฟิลิเอต': aff,
                 'ที่มา': 'TikTok Seller Center > การเงิน > ธุรกรรม > รายงานธุรกิจ'})
    msgs.append(m); changed = ch
    if aff:
        ch2, m2 = put(cfg, 'aff_tk', a.month, aff / a.revenue, a.force)
        msgs.append(m2); changed = changed or ch2
    if not changed:
        print(json.dumps({'status': 'NO_CHANGE', 'msgs': msgs}, ensure_ascii=False)); return 10
    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', 'msgs': msgs}, ensure_ascii=False)); return 0
    save(cfg); print(json.dumps({'status': 'UPDATED', 'msgs': msgs}, ensure_ascii=False)); return 0


def cmd_show(a):
    cfg = load()
    out = {}
    for k, v in cfg['rates'].items():
        out[k] = f'{v*100:.3f}% คงที่' if isinstance(v, (int, float)) else \
                 [f"{s['from']} {s['rate']*100:.3f}%" for s in v]
    mkt = {k: [f"{s['from']} {s['rate']*100:.3f}%" for s in (b.get('rates') or [])]
           for k, b in (cfg.get('marketing_rates') or {}).items()}
    print(json.dumps({'status': 'OK', 'ค่าธรรมเนียม': out, 'ค่าการตลาดที่คิดจากอัตรา': mkt},
                     ensure_ascii=False, indent=1)); return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    s = ap.add_subparsers(dest='cmd', required=True)
    for name, fn in (('shopee', cmd_shopee), ('tiktok', cmd_tiktok)):
        p = s.add_parser(name)
        p.add_argument('--month', required=True, help='YYYY-MM')
        p.add_argument('--force', action='store_true')
        p.add_argument('--dry-run', action='store_true')
        p.set_defaults(fn=fn)
        if name == 'tiktok':
            p.add_argument('--revenue', type=float, required=True)
            p.add_argument('--fee', type=float, required=True)
            p.add_argument('--aff', type=float, default=0)
            p.add_argument('--aff-ads', type=float, default=0, dest='aff_ads')
    sh = s.add_parser('show'); sh.set_defaults(fn=cmd_show)
    a = ap.parse_args()
    if not re.match(r'^\d{4}-\d{2}$', getattr(a, 'month', '2026-01')):
        die('--month ต้องเป็น YYYY-MM')
    return a.fn(a)


if __name__ == '__main__':
    sys.exit(main())
