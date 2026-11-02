#!/usr/bin/env python3
"""อัปเดต ALL_PRODUCTS + PROD_MO ใน WIBWUB_Mobile.html จาก Shipnity

ใช้ process_shipnity() ของ wibwub_update.py เป็นตัวคำนวณ — ห้าม reimplement
(ไฟล์ใน Data Shipnity/ เป็น cumulative snapshot ที่ซ้อนทับกัน ต้อง dedup)

ความหมายของฟิลด์ (ตามคอมเมนต์ในหน้าเว็บเอง):
  v   = ยอดขายจริง — เฉพาะแถวที่ราคา > 0
  q   = จำนวนจริง
  mk  = งบการตลาด (ของแจก / ส่ง Influencer)   ← **carry over ไม่คำนวณใหม่**
  mkq = จำนวนงบการตลาด                          ← **carry over ไม่คำนวณใหม่**
สคริปต์นี้จึงอัปเดตแค่ v / q / PROD_MO และคง mk / mkq ไว้ตามเดิม

ชื่อสินค้าใน Shipnity ไม่เหมือนชื่อที่แสดงบนหน้าเว็บ จึงต้องมีตาราง NAME_MAP
ซึ่งตรวจสอบตัวเองได้: ผลรวมของ SKU ที่ map ต้องเข้าใกล้ค่าเดิมในหน้า (< 2%)
ถ้าห่างกว่านั้นแปลว่า map ผิดหรือมี SKU ใหม่ -> สคริปต์จะหยุด ไม่เขียนทับ

ใช้:  python3 scripts/products_update.py [--dry-run]
exit: 0 = อัปเดตแล้ว · 10 = ไม่มีอะไรเปลี่ยน · 2 = ไม่ผ่านด่านตรวจ (ไม่เขียนไฟล์)
"""
import sys, re, json, argparse
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
PAGE = BASE / 'WIBWUB_Mobile.html'

# ชื่อบนหน้าเว็บ -> ชื่อสินค้าใน Shipnity (รวมหลาย SKU ได้)
# หมายเหตุ: X-Glass นับเฉพาะ 100ml เท่านั้น — คอมเมนต์เก่าในหน้าเว็บเขียนว่า "100ml+1L"
# แต่ตัวเลขจริงตรงกับ 100ml อย่างเดียว (1L แถมขวด 234,751 ไม่เคยถูกนับ)
NAME_MAP = {
    'Sugar สเปรย์แวกซ์เคลือบสีรถ':          ['Sugar (Sugar-500ml+Spray)'],
    'Wool Duster ไม้ปัดฝุ่นขนแกะ':           ['Wool duster-ไม้ปัดขนแกะ'],
    'Interior สเปรย์ทำความสะอาดภายในรถ':    ['Interior (Interior-500ml+Spray)'],
    'Refresh Wipes ทิชชู่เปียกเบาะหนัง':     ['Refresh wipes'],
    'Interior Wipe ทิชชู่เปียกภายในรถ':      ['Interior wipes'],
    'Spot Clean น้ำยาขจัดคราบน้ำ':           ['Spot (Spot-500ml)'],
    'Refresh สเปรย์โฟมทำความสะอาด':          ['Refresh (Refresh-500ml+หัวโฟม สีขาว)'],
    'Perfect ผ้าไมโครไฟเบอร์ BOA 500gsm':    ['Perfect'],
    'X-Glass Shield น้ำยาเคลือบกระจก':       ['Xglass (Xglass-100ml)'],
    'Reflex Ceramic Coating สเปรย์เคลือบสี': ['Reflex (Reflex-250ml+Spray)'],
    'Tire & Trim เจลเคลือบพลาสติกและยาง':    ['Tire&trim gel (Tire&trim gel-500ml)'],
    'Martini ผ้าเช็ดน้ำยาเคลือบสี':          ['Martini'],
    'Sugar สเปรย์แวกซ์ขนาด 3L':              ['Sugar (Sugar-3L แถมขวดสเปรย์)'],
    'Quartz Shampoo น้ำยาล้างรถ 1L':         ['Quartz shampoo (Quartz shampoo-1L)'],
    'Reflex Ceramic Coating ขนาด 500ml':     ['Reflex (Reflex-500ml+Spray)'],
}


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    if not PAGE.exists(): die('ไม่พบ WIBWUB_Mobile.html')
    html = PAGE.read_text(encoding='utf-8')

    mA = re.search(r'(const ALL_PRODUCTS\s*=\s*\[)([\s\S]*?)(\n\];)', html)
    mP = re.search(r'(const PROD_MO\s*=\s*\[)([\s\S]*?)(\n\];)', html)
    if not mA: die('ไม่พบ ALL_PRODUCTS')
    cur = re.findall(r"\{n:'([^']+)',\s*v:([\d.]+),\s*q:(\d+),\s*mk:(\d+),\s*mkq:(\d+)\}", mA.group(2))
    if not cur: die('parse ALL_PRODUCTS ไม่ได้')
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from ship_cache import sales_asof
    asof = sales_asof()

    sys.path.insert(0, str(BASE))
    try:
        import wibwub_update as W
    except Exception as e:
        die('import wibwub_update ไม่สำเร็จ', f'{type(e).__name__}: {e}')
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from ship_cache import load_shipnity
    raw = load_shipnity(verbose=True)
    if not raw: die('process_shipnity() คืน None')

    P = raw['products']
    tot, mon = {}, {}
    for l in raw['lines']:
        if (l.get('s') or 0) <= 0: continue        # v นับเฉพาะแถวที่ราคา > 0
        if asof and l['d'] > asof: continue
        n = P[l['p']]
        t = tot.setdefault(n, {'v': 0.0, 'q': 0})
        t['v'] += l['s']; t['q'] += l.get('q') or 0
        mon.setdefault(n, {}).setdefault(l['d'][:7], 0.0)
        mon[n][l['d'][:7]] += l['s']

    # ── เดือนที่จะแสดง: derive จากข้อมูลจริง ห้ามตรึงปี/เดือน ────────────
    # ของเดิมเป็น ['2026-01'..'2026-10'] ตายตัว -> พ.ย. ไม่ขึ้น และปี 2570 พังทั้งก้อน
    # ต้องต่อเนื่องไม่มีช่องว่าง เพราะ PROD_MO เป็นอาเรย์ที่ index ต้องตรงกับป้ายเดือน
    seen = sorted({m for d in mon.values() for m in d})
    if not seen: die('ไม่มีข้อมูลรายเดือนจาก Shipnity')
    hi = (asof or seen[-1])[:7]
    months = []
    y, mth = int(seen[0][:4]), int(seen[0][5:7])
    while '%04d-%02d' % (y, mth) <= hi:
        months.append('%04d-%02d' % (y, mth))
        y, mth = (y + 1, 1) if mth == 12 else (y, mth + 1)

    unknown = [n for n in NAME_MAP for x in NAME_MAP[n] if x not in tot]
    if unknown: die('ชื่อสินค้าใน NAME_MAP ไม่มีใน Shipnity แล้ว — ตรวจ map', unknown)

    # ── ด่านตรวจ NAME_MAP ────────────────────────────────────────────────
    # v เป็นยอด "สะสมทั้งปีถึง asof" ของเดิมจึงเทียบยอดสะสมรอบนี้ (ถึง 25 ต.ค.)
    # กับยอดสะสมรอบก่อน (ถึง 18 ต.ค.) ซึ่งเป็นคนละช่วงเวลา -> ยอดขายที่เกิดขึ้นจริง
    # ระหว่างนั้นถูกนับเป็น "ผิดปกติ" ทุกครั้ง (1 พ.ย. 69 ตีกลับ 15/15 สินค้า
    # ทั้งที่ส่วนต่างเท่ากับยอดขาย 19-25 ต.ค. พอดีทุกตัว)
    # เปลี่ยนมาเทียบ "เดือนที่ปิดแล้ว" จาก PROD_MO บนหน้าเว็บแทน — ช่วงเดียวกันเป๊ะ
    # และยังจับ map ผิด/SKU ใหม่ได้เหมือนเดิม ส่วนเดือนปัจจุบันยังโตอยู่จึงไม่เอามาเทียบ
    old_mo = {}
    if mP:
        for mm in re.finditer(r"\{n:'([^']+)',\s*mo:\[([^\]]*)\]\}", mP.group(2)):
            old_mo[mm.group(1)] = [None if x.strip() in ('null', '') else float(x)
                                   for x in mm.group(2).split(',')]
    cur_mon = (asof or '')[:7]

    rows, warn, shrink = [], [], []
    for n, v_old, q_old, mk, mkq in cur:
        src = NAME_MAP.get(n)
        if not src: die(f'ไม่มี NAME_MAP สำหรับ "{n}" — เพิ่ม map ก่อน')
        v = round(sum(tot[x]['v'] for x in src), 2)
        q = sum(tot[x]['q'] for x in src)
        # (ก) ช่วงเดียวกัน: ผลรวมเดือนที่ปิดแล้ว ต้องตรงกับที่หน้าเว็บมีอยู่
        prev = old_mo.get(n)
        if prev:
            closed = [m for m in months if m != cur_mon]
            new_closed = sum(sum(mon.get(x, {}).get(m, 0) for x in src) for m in closed)
            old_closed = sum(prev[i] or 0 for i, m in enumerate(months)
                             if i < len(prev) and m != cur_mon)
            if old_closed:
                d = abs(new_closed - old_closed) / old_closed * 100
                if d > 2:
                    warn.append(f'{n}: เดือนที่ปิดแล้ว {old_closed:,.0f} -> {new_closed:,.0f} ({d:+.1f}%)')
        # (ข) ยอดสะสมห้ามหดลง (ของเดิมได้ผลนี้มาฟรีจากการเทียบยอดสะสม)
        if float(v_old) and v < float(v_old) * 0.98:
            shrink.append(f'{n}: {float(v_old):,.0f} -> {v:,.0f}')
        rows.append({'n': n, 'v': int(v) if v == int(v) else v, 'q': q, 'mk': int(mk), 'mkq': int(mkq)})
    if warn: die('ยอดเดือนที่ปิดแล้วต่างจากหน้าเว็บเกิน 2% — น่าจะ map ผิดหรือมี SKU ใหม่ ไม่เขียนทับ', warn)
    if shrink: die('ยอดสะสมลดลงเกิน 2% — น่าจะอ่านไฟล์ไม่ครบ ไม่เขียนทับ', shrink)

    rows.sort(key=lambda r: -r['v'])
    pm = [{'n': r['n'], 'mo': [round(sum(mon.get(x, {}).get(m, 0) for x in NAME_MAP[r['n']])) for m in months]}
          for r in rows]

    # ── ป้ายชื่อเดือนต้องยาวเท่า PROD_MO เสมอ ───────────────────────────
    # PROD_MO_LBL เป็นค่าตายตัวที่ไม่มีสคริปต์ไหนเขียน (ค้างที่ 'ต.ค. (1-18)')
    # ถ้าอาเรย์ข้อมูลยาวขึ้นแต่ป้ายไม่ตาม กราฟจะเลื่อนชื่อเดือนผิดทั้งแถว
    TH = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
          'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
    multi_year = len({m[:4] for m in months}) > 1
    labels = []
    for m in months:
        lbl = TH[int(m[5:7]) - 1] + (' %s' % (int(m[:4]) + 543 - 2500) if multi_year else '')
        if m == cur_mon and asof:
            lbl += ' (1-%d)' % int(asof[8:10])
        labels.append(lbl)
    newL = ','.join("'%s'" % x for x in labels)

    newA = '\n' + ',\n'.join(
        "  {n:'%s', v:%s, q:%d, mk:%d, mkq:%d}" % (r['n'], r['v'], r['q'], r['mk'], r['mkq']) for r in rows)
    newP = '\n' + ',\n'.join(
        "  {n:'%s', mo:[%s]}" % (p['n'], ', '.join(str(x) for x in p['mo'])) for p in pm)

    summary = {'asof': asof, 'products': len(rows), 'months': len(months),
               'top3': [(r['n'][:28], r['v']) for r in rows[:3]],
               'reordered': [r['n'][:28] for i, r in enumerate(rows) if cur[i][0] != r['n']]}
    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **summary}, ensure_ascii=False)); return 0

    out = html[:mA.start(2)] + newA + html[mA.end(2):]
    if mP:
        mP2 = re.search(r'(const PROD_MO\s*=\s*\[)([\s\S]*?)(\n\];)', out)
        out = out[:mP2.start(2)] + newP + out[mP2.end(2):]
    out = re.sub(r'const PROD_MO_LBL\s*=\s*\[[^\]]*\]',
                 lambda _: 'const PROD_MO_LBL=[' + newL + ']', out, count=1)
    if out == html:
        print(json.dumps({'status': 'NO_CHANGE', **summary}, ensure_ascii=False)); return 10

    import subprocess, tempfile
    js = Path(tempfile.gettempdir()) / 'wibwub_prod_check.js'
    js.write_text('\n;\n'.join(re.findall(r'<script[^>]*>([\s\S]*?)</script>', out)), encoding='utf-8')
    r = subprocess.run(['node', '--check', str(js)], capture_output=True, text=True)
    if r.returncode: die('node --check ไม่ผ่าน', r.stderr[:300])
    PAGE.write_text(out, encoding='utf-8')
    W.bump_sw()
    print(json.dumps({'status': 'UPDATED', **summary}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
