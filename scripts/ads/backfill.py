#!/usr/bin/env python3
"""ดึงข้อมูล Ads ย้อนหลัง (ม.ค.–ส.ค. 69) เข้า data Ads/ads_daily.json

**แยกจาก ads_daily_update.py โดยตั้งใจ** — ตัวนั้นงานตั้งเวลาใช้ทุกวัน ห้ามไปแก้
ความต่างสำคัญ: ตัวนี้ **ห้ามเขียนทับวันที่มีข้อมูลอยู่แล้ว** (ก.ย.–ต.ค. ที่ดึงมาแล้ว)
ส่วน ads_daily_update.py merge ตั้งใจให้เขียนทับได้ เพราะยอด "ยืนยันแล้ว" ขยับย้อนหลัง 3 วัน

ใช้:
  python3 backfill.py status                 → เดือนไหนมีกี่วัน ขาดเดือนไหนบ้าง
  python3 backfill.py guard [--minutes 30]   → ปลอดภัยที่จะดึงไหม (งานตั้งเวลาใกล้/กำลังรัน)
  python3 backfill.py merge work/*.json      → เขียนเฉพาะวันที่ยังไม่มี
  python3 backfill.py camp work/tk_camp.json → เพิ่มแคมเปญเดือนเก่า (ไม่ทับเดือนที่มีแล้ว)
  python3 backfill.py report                 → ยอดรวมรายเดือนทั้งปี (ไว้ใส่สรุปตอนเช้า)
exit 10 = ไม่มีอะไรใหม่ · exit 2 = ไม่ผ่านด่านตรวจ/ไม่ปลอดภัย
"""
import json, os, sys, datetime, glob, argparse, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ALL = os.path.abspath(os.path.join(HERE, '..', '..'))
DAILY = os.path.join(ALL, 'data Ads', 'ads_daily.json')
TKC = os.path.join(ALL, 'data Ads', 'ads_tk_campaigns.json')

# ตารางงานตั้งเวลา (ชั่วโมง:นาที เวลาไทย) — คัดจาก list_scheduled_tasks 20 ต.ค. 2569
# ถ้าเพิ่ม/ย้ายงาน ต้องมาแก้ที่นี่ด้วย ไม่งั้น guard จะบอกว่าปลอดภัยทั้งที่ไม่ใช่
# (ตัดรอบ HR 22:00 ออกแล้ว 20 ต.ค. 69 — ใกล้รอบปิดวัน 23:57 เกินไป เหลือ HR 6 เวลา/วัน)
SCHEDULE = ['08:00', '08:05', '08:10', '08:20', '08:30', '08:37', '08:40', '08:45', '08:50',
            '09:00', '09:10', '09:25', '09:30', '09:47', '10:00', '10:10', '10:30', '12:00',
            '17:30', '18:30', '19:00', '19:10', '19:20', '19:30', '19:37', '19:40',
            '19:45', '19:50', '20:00', '20:10', '20:25', '20:47', '21:10', '23:50']
JITTER_MIN = 15      # งานมี jitter สุ่มได้ถึง ~13 นาที เผื่อไว้ 15
SESS = os.path.expanduser('~/.claude/projects')


def die(msg, detail=None, code=2):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(code)


def load():
    return json.load(open(DAILY, encoding='utf-8'))


def bkk_now():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=7)


# ── guard ───────────────────────────────────────────────────────────────────
def cmd_guard(a):
    now = bkk_now()
    nxt = []
    for t in SCHEDULE:
        h, m = map(int, t.split(':'))
        w = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if w < now: w += datetime.timedelta(days=1)
        nxt.append((int((w - now).total_seconds() // 60), t))
    nxt.sort()
    mins, when = nxt[0]
    # งานที่เพิ่งเริ่ม (ภายใน JITTER_MIN นาทีที่ผ่านมา) อาจยังรันค้างอยู่
    running = []
    for t in SCHEDULE:
        h, m = map(int, t.split(':'))
        w = now.replace(hour=h, minute=m, second=0, microsecond=0)
        age = (now - w).total_seconds() / 60
        if 0 <= age <= a.busy: running.append(t)
    # เช็คจากของจริงด้วย: ไฟล์ session ของงานตั้งเวลาถูกเขียนอยู่หรือไม่
    live = []
    for p in glob.glob(os.path.join(SESS, '*', '*.jsonl')):
        try: age = (datetime.datetime.now().timestamp() - os.path.getmtime(p)) / 60
        except OSError: continue
        if age < 3: live.append(os.path.basename(p)[:8])
    ok = mins >= a.minutes and not running
    out = {'status': 'OK' if ok else 'WAIT', 'now': now.strftime('%Y-%m-%d %H:%M'),
           'next_task_in_min': mins, 'next_task_at': when,
           'maybe_running': running, 'sessions_written_last_3min': live,
           'need_free_min': a.minutes}
    if live and ok:
        out['status'] = 'WARN'
        out['note'] = 'ไม่มีงานตามตาราง แต่มี session เขียนไฟล์อยู่ — อาจเป็นเซสชันคน'
    print(json.dumps(out, ensure_ascii=False))
    return 0 if ok else 2


# ── status / report ─────────────────────────────────────────────────────────
def months_of(d):
    mo = {}
    for k, v in d['days'].items():
        m = mo.setdefault(k[:7], {'days': 0, 'lz': 0})
        m['days'] += 1
        if 'lz_real' in v: m['lz'] += 1
    return dict(sorted(mo.items()))


def cmd_status(a):
    d = load(); mo = months_of(d)
    want = [f'2026-{i:02d}' for i in range(1, 11)]
    import calendar
    rows = []
    for m in want:
        y, mm = int(m[:4]), int(m[5:7])
        full = calendar.monthrange(y, mm)[1]
        got = mo.get(m, {'days': 0, 'lz': 0})
        rows.append({'month': m, 'days': got['days'], 'in_month': full,
                     'lz_days': got['lz'], 'missing': full - got['days']})
    print(json.dumps({'status': 'OK', 'file_range': [min(d['days']), max(d['days'])],
                      'coverage': d.get('coverage'), 'months': rows}, ensure_ascii=False, indent=1))
    return 0


def cmd_report(a):
    d = load(); out = []
    for m, _ in months_of(d).items():
        ds = [v for k, v in d['days'].items() if k.startswith(m)]
        lz = [x for x in ds if 'lz_real' in x]
        out.append({'month': m, 'days': len(ds),
                    'sh_real': round(sum(x['sh_real']['gmv'] for x in ds), 2),
                    'sh_spend': round(sum(sum(t['spend'] for t in x['sh_ads'].values()) for x in ds), 2),
                    'tk_real': round(sum(x['tk_real']['gmv'] for x in ds), 2),
                    'tk_spend': round(sum(sum(t['spend'] for t in x['tk_ads'].values()) for x in ds), 2),
                    'lz_days': len(lz),
                    'lz_real': round(sum(x['lz_real']['gmv'] for x in lz), 2),
                    'lz_spend': round(sum(x['lz_ads']['spend'] for x in lz), 2)})
    print(json.dumps({'status': 'OK', 'months': out}, ensure_ascii=False, indent=1))
    return 0


# ── merge (เฉพาะวันใหม่) ────────────────────────────────────────────────────
# วันที่ร้านปิดตามแผน — ยอด 0 เป็นข้อมูลจริง ไม่ใช่ดึงพลาด ห้ามไปดึงซ้ำ
CLOSED = {'2026-02-19': 'ปิดร้านออนไลน์ เอาท์ติ้งบริษัท',
          '2026-02-20': 'ปิดร้านออนไลน์ เอาท์ติ้งบริษัท'}

NEED = ('sh_real', 'sh_ads', 'tk_real', 'tk_ads')
OPT = ('lz_real', 'lz_ads')
# ค่าโฆษณา Shopee ย้อนได้แค่ ~185 วัน (หน้าต่างกลิ้ง เลื่อนขึ้นวันละวัน) ส่วนยอดขายจริง
# + TikTok + Lazada ย้อนได้ถึง ม.ค. ถ้าจะเติมวันเก่ากว่าหน้าต่างนั้นต้องยอมให้ขาด sh_ads
# --allow-no-sh-ads = วันไหนไม่มี sh_ads ให้เขียนโดย "ไม่ใส่คีย์" (เหมือน lz_* ก่อน ก.ย.)
# ห้ามเติม 0 เพราะจะกลายเป็น "ลงโฆษณา 0 บาท" ซึ่งผิด


def cmd_merge(a):
    parts = {}
    for p in a.files:
        o = json.load(open(p, encoding='utf-8')); parts[o['kind']] = o['data']
    miss = [k for k in NEED if k not in parts]
    if miss: die('ขาดชุดบังคับ', miss)
    bad = [k for k in parts if k not in NEED + OPT]
    if bad: die('ชุดที่ไม่รู้จัก', bad)
    has_lz = any(k in parts for k in OPT)
    if has_lz and not all(k in parts for k in OPT):
        die('ถ้าจะใส่ Lazada ต้องให้ทั้ง lz_real และ lz_ads')

    core = tuple(k for k in NEED if not (a.allow_no_sh_ads and k == 'sh_ads'))
    dates = sorted(set.intersection(*[set(parts[k]) for k in core]))
    gaps = sorted(set().union(*[set(parts[k]) for k in core]) - set(dates))
    # ปกติห้ามให้ชุดใดชุดหนึ่งขาดวัน (กันเขียนวันไม่ครบ) แต่ตอน backfill ย้อนหลัง
    # แต่ละแหล่งย้อนได้ไม่เท่ากันโดยธรรมชาติ เช่น ค่าโฆษณา Shopee ย้อนได้แค่ ~6 เดือน
    # (หน้าต่างกลิ้ง เลื่อนขึ้นวันละวัน) ส่วนยอดขายจริงย้อนได้ถึง ม.ค.
    # --intersect = ยอมรับ แล้วเขียนเฉพาะวันที่ "ทุกชุดมีครบ" เท่านั้น ที่เหลือรายงานทิ้ง
    if gaps and not a.intersect:
        die('บางชุดขาดวันที่ — ห้ามเขียนข้อมูลไม่ครบ (ถ้าตั้งใจ ให้ใส่ --intersect)',
            {'ขาด': len(gaps), 'ตัวอย่าง': gaps[:5] + (['...'] if len(gaps) > 5 else []),
             'จะเขียนได้': f'{dates[0]} → {dates[-1]} ({len(dates)} วัน)' if dates else 'ไม่มีเลย'})
    dropped = gaps
    yest = (bkk_now().date() - datetime.timedelta(days=1)).isoformat()

    d = load(); have = set(d['days'])
    skipped_exist, skipped_future, added, warn = [], [], [], []
    no_sh_ads = []
    for dt in dates:
        if dt > yest: skipped_future.append(dt); continue
        if dt in have:                       # ★ หัวใจของสคริปต์นี้: ห้ามแตะของเดิม
            skipped_exist.append(dt); continue
        e = {'sh_real': {'gmv': int(round(parts['sh_real'][dt]['gmv'])),
                         'orders': int(parts['sh_real'][dt]['orders'])},
             'tk_real': {'gmv': round(float(parts['tk_real'][dt]['gmv']), 2),
                         'orders': int(parts['tk_real'][dt]['orders'])},
             'tk_ads': {k: {'gmv': round(float(parts['tk_ads'][dt][k]['gmv']), 2),
                            'spend': round(float(parts['tk_ads'][dt][k]['spend']), 2),
                            'orders': int(parts['tk_ads'][dt][k]['orders'])}
                        for k in ('product', 'live')}}
        if dt in parts['sh_ads']:
            e['sh_ads'] = {k: {f: int(parts['sh_ads'][dt][k][f])
                               for f in ('gmv_broad', 'gmv_direct', 'spend', 'orders')}
                           for k in ('product', 'search', 'live')}
        else:
            no_sh_ads.append(dt)
        if has_lz and dt in parts['lz_real'] and dt in parts['lz_ads']:
            e['lz_real'] = {'gmv': round(float(parts['lz_real'][dt]['gmv']), 2),
                            'orders': int(parts['lz_real'][dt]['orders'])}
            e['lz_ads'] = {f: (int(parts['lz_ads'][dt][f]) if f in ('orders', 'imp', 'clicks')
                               else round(float(parts['lz_ads'][dt][f]), 2))
                           for f in ('spend', 'revenue', 'orders', 'imp', 'clicks')}
        for sec in e.values():
            vals = sec.values() if all(isinstance(x, dict) for x in sec.values()) else [sec]
            for v in vals:
                if any(isinstance(x, (int, float)) and x < 0 for x in v.values()):
                    die('ค่าติดลบ', dt)
        if e['sh_real']['gmv'] == 0 and e['tk_real']['gmv'] == 0:
            warn.append(f'{dt} ยอดขายจริงเป็น 0 ทั้งสองแพลตฟอร์ม — ' +
                        (CLOSED[dt] + ' (ยืนยันแล้วว่าปกติ)' if dt in CLOSED else 'ตรวจสอบ'))
        d['days'][dt] = e; added.append(dt)

    summary = {'added': len(added), 'added_range': [added[0], added[-1]] if added else None,
               'skipped_exist': len(skipped_exist), 'skipped_future': skipped_future,
               'no_sh_ads': len(no_sh_ads),
               'no_sh_ads_range': [no_sh_ads[0], no_sh_ads[-1]] if no_sh_ads else None,
               'dropped_incomplete': len(dropped),
               'dropped_range': [dropped[0], dropped[-1]] if dropped else None,
               'warnings': warn}
    if not added:
        print(json.dumps({'status': 'NO_NEW', **summary}, ensure_ascii=False)); return 10
    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **summary}, ensure_ascii=False)); return 0

    d['days'] = dict(sorted(d['days'].items()))
    last = max(d['days'])
    cov = {'shopee': last, 'tiktok': last}
    lzd = [k for k, v in d['days'].items() if 'lz_real' in v]
    if lzd: cov['lazada'] = max(lzd)
    d['coverage'] = cov
    shutil.copy2(DAILY, DAILY + '.bak')
    tmp = DAILY + '.tmp'
    json.dump(d, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.replace(tmp, DAILY)
    print(json.dumps({'status': 'UPDATED', **summary, 'file_range': [min(d['days']), last]},
                     ensure_ascii=False))
    return 0


def cmd_fill_lz(a):
    """เติม lz_real/lz_ads ให้วันที่มีอยู่แล้วแต่ขาดคีย์ Lazada

    ทำไมต้องมีคำสั่งแยก: `merge` ถูกออกแบบให้ "ห้ามแตะวันที่มีข้อมูลแล้ว" เด็ดขาด
    จึงเติมคีย์ที่ขาดให้วันเดิมไม่ได้ ซึ่งเป็นสิ่งที่ถูกต้องสำหรับ merge
    แต่รอบ backfill 18 เม.ย.-31 ส.ค. (ทำเมื่อ 20 ต.ค.) merge ไปโดยไม่มีไฟล์ Lazada
    ทำให้ 136 วันนั้นขาด lz_* ทั้งที่ ม.ค.-17 เม.ย. และ ก.ย.-ต.ค. มี
    = หน้าเว็บมีช่องว่าง Lazada กลางปีทั้งที่ข้อมูลมีอยู่ในไฟล์ backfill

    คำสั่งนี้แคบที่สุดเท่าที่จะทำได้: **เพิ่มได้เฉพาะคีย์ที่ยังไม่มี**
    ถ้าวันไหนมี lz_real หรือ lz_ads อยู่แล้วจะข้ามทั้งวัน ไม่เขียนทับอะไรเลย
    และไม่แตะคีย์อื่น (sh_*, tk_*) แม้แต่ตัวเดียว
    """
    parts = {}
    for p in a.files:
        o = json.load(open(p, encoding='utf-8')); parts[o['kind']] = o['data']
    if set(parts) != {'lz_real', 'lz_ads'}:
        die('ต้องให้ไฟล์ lz_real และ lz_ads เท่านั้น', sorted(parts))

    d = load()
    yest = (bkk_now().date() - datetime.timedelta(days=1)).isoformat()
    filled, skip_have, skip_nodata, untouched = [], [], [], []
    for dt in sorted(d['days']):
        v = d['days'][dt]
        if 'lz_real' in v or 'lz_ads' in v: skip_have.append(dt); continue
        if dt > yest: continue
        if dt not in parts['lz_real'] or dt not in parts['lz_ads']:
            skip_nodata.append(dt); continue
        lr, la = parts['lz_real'][dt], parts['lz_ads'][dt]
        vals = [lr['gmv'], lr['orders']] + [la[f] for f in ('spend', 'revenue', 'orders', 'imp', 'clicks')]
        if any(x < 0 for x in vals): die('ค่าติดลบ', dt)
        v['lz_real'] = {'gmv': round(float(lr['gmv']), 2), 'orders': int(lr['orders'])}
        v['lz_ads'] = {f: (int(la[f]) if f in ('orders', 'imp', 'clicks') else round(float(la[f]), 2))
                       for f in ('spend', 'revenue', 'orders', 'imp', 'clicks')}
        filled.append(dt)

    summary = {'filled': len(filled),
               'filled_range': [filled[0], filled[-1]] if filled else None,
               'gmv': round(sum(d['days'][x]['lz_real']['gmv'] for x in filled), 2),
               'orders': sum(d['days'][x]['lz_real']['orders'] for x in filled),
               'spend': round(sum(d['days'][x]['lz_ads']['spend'] for x in filled), 2),
               'skipped_มีอยู่แล้ว': len(skip_have),
               'skipped_ไม่มีข้อมูล': len(skip_nodata)}
    if not filled:
        print(json.dumps({'status': 'NO_NEW', **summary}, ensure_ascii=False)); return 10
    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **summary}, ensure_ascii=False)); return 0

    lzd = [k for k, v in d['days'].items() if 'lz_real' in v]
    d['coverage']['lazada'] = max(lzd)
    shutil.copy2(DAILY, DAILY + '.bak')
    tmp = DAILY + '.tmp'
    json.dump(d, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.replace(tmp, DAILY)
    print(json.dumps({'status': 'UPDATED', **summary}, ensure_ascii=False))
    return 0


def cmd_camp(a):
    new = json.load(open(a.file, encoding='utf-8'))['data']
    cur = json.load(open(TKC, encoding='utf-8')) if os.path.exists(TKC) else {}
    box = cur.get('months') if isinstance(cur, dict) and 'months' in cur else cur
    added = []
    for m, v in new.items():
        if m in box:                          # ห้ามทับเดือนที่มีแล้ว
            continue
        box[m] = v; added.append(m)
    if not added:
        print(json.dumps({'status': 'NO_NEW', 'months_present': sorted(box)}, ensure_ascii=False))
        return 10
    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', 'would_add': added}, ensure_ascii=False)); return 0
    shutil.copy2(TKC, TKC + '.bak')
    json.dump(cur, open(TKC, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps({'status': 'UPDATED', 'added': added}, ensure_ascii=False))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    s = ap.add_subparsers(dest='cmd', required=True)
    g = s.add_parser('guard'); g.add_argument('--minutes', type=int, default=30)
    g.add_argument('--busy', type=int, default=JITTER_MIN); g.set_defaults(fn=cmd_guard)
    s.add_parser('status').set_defaults(fn=cmd_status)
    s.add_parser('report').set_defaults(fn=cmd_report)
    m = s.add_parser('merge'); m.add_argument('files', nargs='+')
    m.add_argument('--dry-run', action='store_true')
    m.add_argument('--allow-no-sh-ads', action='store_true', dest='allow_no_sh_ads',
                   help='ยอมให้บางวันไม่มีค่าโฆษณา Shopee (เกินหน้าต่าง 185 วัน) '
                        'วันนั้นจะไม่มีคีย์ sh_ads ไม่ใช่ 0')
    m.add_argument('--intersect', action='store_true',
                   help='ยอมให้แต่ละชุดมีช่วงวันไม่เท่ากัน เขียนเฉพาะวันที่ทุกชุดมีครบ')
    m.set_defaults(fn=cmd_merge)
    fl = s.add_parser('fill-lz', help='เติม lz_real/lz_ads ให้วันที่ขาด (ไม่เขียนทับของเดิม)')
    fl.add_argument('files', nargs='+'); fl.add_argument('--dry-run', action='store_true')
    fl.set_defaults(fn=cmd_fill_lz)

    c = s.add_parser('camp'); c.add_argument('file')
    c.add_argument('--dry-run', action='store_true'); c.set_defaults(fn=cmd_camp)
    a = ap.parse_args()
    sys.exit(a.fn(a))


if __name__ == '__main__':
    main()
