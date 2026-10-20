#!/usr/bin/env python3
"""merge Shopee Live รายวัน (overview-v2) เข้า SH_LIVE_DAILY ใน WIBWUB_Dashboard.html

ที่มาของไฟล์: Shopee Seller Centre → Marketing Centre → Live&Video → แท็บ "ข้อมูลโดยรวม"
(/creator-center/insight/live) → กด "ดาวน์โหลดข้อมูล" **ทีละ 1 วัน**
ได้ไฟล์ชื่อ `overview-v2_1d_<YYYY-MM-DD>_*.csv`

กับดักที่เคยทำพัง (อย่าแก้ออก):
  · CSV มีคอลัมน์คู่แฝด "(คำสั่งซื้อที่เกิดขึ้น)" vs "(คำสั่งซื้อที่ยืนยันแล้ว)"
    ต้องใช้ **ที่ยืนยันแล้ว** เท่านั้น
  · ผู้ชมต้องใช้ "ผู้ชมทั้งหมด" ไม่ใช่ "ผู้ชมที่มีส่วนร่วม"
  · ผู้ติดตามใหม่ชื่อเต็มคือ "ผู้ติดตามใหม่จาก Live" (ไม่มีคอลัมน์ชื่อ "ผู้ติดตามใหม่")
  · ห้ามใช้ export แบบรายไลฟ์ (sc_live_stream_list_export*) มารวมกันเอง —
    ไฟล์นั้นไม่มีคอลัมน์ผู้ติดตาม และ overview-v2 เป็นยอดรวมรายวันอยู่แล้ว (รวมซ้ำ = เบิ้ล)
  · ถ้าเผลอเหลือ date range ค้างจากแท็บอื่น ทุกช่องจะเป็น "-" ซึ่งดูเหมือนไม่มีไลฟ์
    สคริปต์จะไม่ยอมเขียน 0 ทับวันที่เคยมียอด

ใช้:  python3 scripts/shopee_live_daily.py <csv|dir> [...] [--dry-run]
exit: 0 = อัปเดตแล้ว · 10 = ไม่มีอะไรเปลี่ยน · 2 = ไม่ผ่านด่านตรวจ (ไม่เขียนไฟล์)
"""
import sys, re, csv, json, argparse, datetime as dt
from pathlib import Path

BASE = Path('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com'
            '/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All')
PAGE = BASE / 'WIBWUB_Dashboard.html'
BKK = dt.timezone(dt.timedelta(hours=7))
COLS = {                      # ชื่อคอลัมน์เต็ม (เอา match แรกเท่านั้น — ชื่อซ้ำมีจริงในไฟล์)
    'gmv':          'ยอดขาย(คำสั่งซื้อที่ยืนยันแล้ว)',
    'orders':       'คำสั่งซื้อ(คำสั่งซื้อที่ยืนยันแล้ว)',
    'viewers':      'ผู้ชมทั้งหมด',
    'newFollowers': 'ผู้ติดตามใหม่จาก Live',
}


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def num(v):
    s = str(v or '').strip()
    if s in ('', '-', '—'): return 0
    s = re.sub(r'[฿,\s%]', '', s)
    try: return float(s)
    except ValueError: return 0


def read_csv(p):
    rows = list(csv.reader(open(p, encoding='utf-8-sig')))
    hdr = next((r for r in rows[:5] if 'ระยะเวลาเก็บข้อมูล' in [c.strip() for c in r]), None)
    if hdr is None: die('ไม่พบแถว header (ต้องมีคอลัมน์ "ระยะเวลาเก็บข้อมูล")', str(p))
    hdr = [c.strip() for c in hdr]
    idx = {}
    for k, name in COLS.items():
        if name not in hdr: die(f'ไม่พบคอลัมน์ "{name}" — ชีต/export เปลี่ยนรูปแบบ', str(p))
        idx[k] = hdr.index(name)          # match แรก
    di = hdr.index('ระยะเวลาเก็บข้อมูล')
    out = {}
    for r in rows[rows.index(hdr) + 1:]:
        if not r or len(r) <= di: continue
        m = re.match(r'(\d{2})-(\d{2})-(\d{4})$', str(r[di]).strip())
        if not m: continue
        d = f'{m[3]}-{m[2]}-{m[1]}'
        out[d] = {'gmv': round(num(r[idx['gmv']]), 2), 'orders': int(num(r[idx['orders']])),
                  'viewers': int(num(r[idx['viewers']])), 'newFollowers': int(num(r[idx['newFollowers']]))}
    if not out: die('ไม่พบแถวข้อมูลที่มีวันที่', str(p))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='+')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    files = []
    for p in a.paths:
        p = Path(p)
        files += sorted(p.glob('overview-v2_1d_*.csv'), key=lambda x: x.stat().st_mtime) if p.is_dir() else [p]
    if not files: die('ไม่พบไฟล์ CSV')

    new = {}
    for f in files: new.update(read_csv(f))

    if not PAGE.exists(): die('ไม่พบ WIBWUB_Dashboard.html')
    html = PAGE.read_text(encoding='utf-8')
    m = re.search(r'const SH_LIVE_DAILY\s*=\s*(\{[\s\S]*?\});', html)
    if not m: die('ไม่พบ SH_LIVE_DAILY ในหน้าเว็บ')
    cur = json.loads(m.group(1))
    dates, daily = cur['dates'], cur['daily']

    y = (dt.datetime.now(BKK).date() - dt.timedelta(days=1)).isoformat()
    added, changed, skipped, refused = [], [], [], []
    for d in sorted(new):
        if d > y: skipped.append(f'{d} (ยังไม่จบวัน)'); continue
        n, o = new[d], daily.get(d)
        # ห้ามเขียน 0 ทับวันที่เคยมียอด — อาการของ date range ค้าง/ดึงผิดวัน
        if o and o.get('gmv') and not n['gmv']:
            refused.append(f'{d}: เดิม gmv {o["gmv"]} แต่ไฟล์ใหม่เป็น 0'); continue
        # ยอด "ยืนยันแล้ว" โตขึ้นตามเวลา (ออเดอร์ทยอยยืนยัน) ไฟล์ที่โหลดเก่ากว่าจะต่ำกว่า
        # ถ้าค่าใหม่ต่ำกว่าเดิม = ไฟล์เก่า ให้ข้าม ไม่ถอยข้อมูลที่ matured แล้ว
        if o and (n['gmv'] < o.get('gmv', 0) or n['orders'] < o.get('orders', 0)):
            skipped.append(f'{d} (ไฟล์เก่ากว่า: gmv {n["gmv"]} < {o.get("gmv")})'); continue
        if o is None: daily[d] = n; added.append(d)
        elif o != n: daily[d] = n; changed.append(f'{d}: {o} -> {n}')

    if refused: die('ไฟล์ใหม่เป็น 0 ทับวันที่เคยมียอด — ไม่เขียน (เช็ค date range ในหน้าเว็บ)', refused)

    # เติมวันว่างระหว่างกลางให้ต่อเนื่อง แล้วเรียงใหม่
    allv = sorted(set(dates) | set(daily))
    if allv:
        s, e = dt.date.fromisoformat(allv[0]), dt.date.fromisoformat(allv[-1])
        full = [(s + dt.timedelta(days=i)).isoformat() for i in range((e - s).days + 1)]
        for d in full: daily.setdefault(d, {'gmv': 0, 'orders': 0, 'viewers': 0, 'newFollowers': 0})
    else:
        full = []
    if len(full) < len(dates): die('จำนวนวันหดลง — ไม่เขียนทับ', f'{len(dates)} -> {len(full)}')

    out = {'dates': full, 'daily': {d: daily[d] for d in full}}
    summary = {'files': len(files), 'added': added, 'changed': changed, 'skipped': skipped,
               'days': len(full), 'range': [full[0], full[-1]] if full else None,
               'live_days': sum(1 for d in full if daily[d].get('gmv'))}

    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **summary}, ensure_ascii=False)); return 0
    if not added and not changed:
        print(json.dumps({'status': 'NO_CHANGE', **summary}, ensure_ascii=False)); return 10

    new_html = html[:m.start(1)] + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + html[m.end(1):]
    import subprocess, tempfile
    js = Path(tempfile.gettempdir()) / 'wibwub_shlive_check.js'
    js.write_text('\n;\n'.join(re.findall(r'<script[^>]*>([\s\S]*?)</script>', new_html)), encoding='utf-8')
    r = subprocess.run(['node', '--check', str(js)], capture_output=True, text=True)
    if r.returncode: die('node --check ไม่ผ่าน', r.stderr[:300])
    PAGE.write_text(new_html, encoding='utf-8')

    sw = BASE / 'sw.js'; t = sw.read_text(encoding='utf-8')
    v = int(re.search(r'wibwub-v(\d+)', t).group(1))
    sw.write_text(re.sub(r'wibwub-v\d+', f'wibwub-v{v+1}', t), encoding='utf-8')
    summary['sw'] = f'v{v} -> v{v+1}'
    print(json.dumps({'status': 'UPDATED', **summary}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
