#!/usr/bin/env python3
"""Facebook Ads รายวัน — แหล่งความจริงเดียวของตัวเลข FB ทั้งระบบ

อ่าน  : data Ads/facebook/daily/FBD_*.csv  (1 ไฟล์ = 1 บัญชี · 1 แถว = 1 แคมเปญ x 1 วัน)
เขียน : data Ads/facebook/fb_daily.json                  <- marketing_update.py อ่านตัวนี้ (ads_fb)
        data Ads/WIBWUB_Ads_Dashboard.html บล็อก FB_ADS  <- ส่วน Facebook Ads บนหน้าเว็บ

ทำไมต้องมีไฟล์กลาง (27 ต.ค. 69):
  เดิม ads_fb ต้องกรอกมือใน mkt_manual.json ซึ่งไม่มีใครกรอก -> หน้า "การตลาด vs ยอดขาย"
  ขึ้น "รอข้อมูล" ทั้งเดือน ทั้งที่ไฟล์ CSV มีตัวเลขครบ และถ้ากรอกมือคู่กับหน้า Ads
  ก็จะมีตัวเลข FB 2 ชุดที่ไม่มีอะไรบังคับให้ตรงกัน

กติกาตัวเลข (อย่าเปลี่ยนโดยไม่อ่าน):
  · ค่าโฆษณา = คอลัมน์ "จำนวนเงินที่ใช้จ่ายไป (THB)" เท่านั้น ห้ามใช้ไฟล์ยอดรวม FB_*.csv
  · เป้าหมายของแคมเปญ = ค่าที่ "ไม่ว่าง" ของคอลัมน์ "ตัวระบุผลลัพธ์" ของแคมเปญนั้น
    (บางวันว่างเพราะวันนั้นไม่มีผลลัพธ์ ไม่ใช่เพราะเป้าหมายเปลี่ยน)
  · คลิกทั้งหมดไม่มีเป็นคอลัมน์นับ -> ถอดจาก CTR(ทั้งหมด)/100 x อิมเพรสชัน
    ตรวจแล้วปัดเป็นจำนวนเต็มพอดีทุกแถว (คลาดสูงสุด 0.0001) และ spend/clicks ตรงกับ
    คอลัมน์ CPC(ทั้งหมด) ทุกแถว
  · reach บวกข้ามวันไม่ได้ (คนเดิมถูกนับซ้ำ) -> เก็บรายวันไว้เฉย ๆ ให้หน้าเว็บคิด
    "ความถี่เฉลี่ยรายวัน" = Simp/Sreach แล้วเขียนหมายเหตุ ห้ามเอา reach ไปโชว์เป็นยอดรวม
  · CPM/CTR/CPC รายสัปดาห์ให้หน้าเว็บคิดจากผลรวมของสัปดาห์ ไม่ใช่เฉลี่ยค่ารายวัน
    (ค่าเฉลี่ยของอัตราส่วนไม่เท่ากับอัตราส่วนของผลรวม)

ใช้:  python3 scripts/ads/fb_daily.py [--dry-run]
exit: 0 = อัปเดตแล้ว · 10 = ไม่มีอะไรเปลี่ยน · 2 = ไม่ผ่านด่านตรวจ (ไม่เขียนไฟล์)
"""
import sys, re, csv, json, glob, argparse, subprocess
from pathlib import Path
from datetime import datetime, timedelta


def _find_base():
    """ไล่ขึ้นจากตำแหน่งไฟล์นี้จนเจอโฟลเดอร์ All — marker = sw.js + .git

    ห้ามฝังพาธ Mac ตายตัว: งานตั้งเวลาฝั่ง local รันในแซนด์บ็อกซ์ที่ mount โฟลเดอร์ All
    ไว้คนละที่ (/sessions/<ชื่อ>/mnt/All) และชื่อเซสชันเปลี่ยนทุกรอบ
    """
    p = Path(__file__).resolve()
    for d in (p, *p.parents):
        if (d / 'sw.js').is_file() and (d / '.git').exists():
            return d
    raise SystemExit(f'หาโฟลเดอร์ All ไม่เจอ — ไล่ขึ้นจาก {p} แล้วไม่เจอโฟลเดอร์ที่มีทั้ง '
                     'sw.js และ .git · ห้ามเดาพาธ')


BASE = _find_base()
SRC = BASE / 'data Ads' / 'facebook' / 'daily'
OUT = BASE / 'data Ads' / 'facebook' / 'fb_daily.json'
PAGE = BASE / 'data Ads' / 'WIBWUB_Ads_Dashboard.html'
START = '/* FB_ADS:AUTO-START */'
END = '/* FB_ADS:AUTO-END */'

# ชื่อบัญชีที่ผู้ใช้เรียก -> ใช้ในตารางบนหน้าเว็บ (คีย์ = ส่วนที่ 2 ของชื่อไฟล์ FBD_<คีย์>_<id>_...)
ACC_LABEL = {'WibWub-AD-1': 'WibWub AD 1', 'AD-1': 'AD 1', 'AD-2': 'AD 2',
             'AD3': 'AD3 (CPAS)', 'AD-4': 'AD 4'}
# ตัวระบุผลลัพธ์ -> (คีย์สั้น, ป้ายบนหน้าเว็บ, ป้ายของ "ผลลัพธ์", ป้ายของ "ต้นทุนต่อผลลัพธ์")
GOALS = {
    'actions:onsite_conversion.messaging_conversation_started_7d':
        ('msg', 'ข้อความ', 'แชทที่เริ่มขึ้น', 'ต้นทุนต่อแชท'),
    'actions:onsite_conversion.purchase':
        ('purchase', 'ยอดซื้อ (บนเพจ)', 'ยอดซื้อ', 'ต้นทุนต่อออเดอร์'),
    'catalog_segment_actions:omni_purchase':
        ('omni', 'ยอดขาย CPAS (Shopee)', 'ยอดซื้อ', 'ต้นทุนต่อออเดอร์'),
    'actions:onsite_conversion.lead_grouped':
        ('lead', 'ลูกค้าเป้าหมาย', 'lead', 'ต้นทุนต่อ lead'),
}
COL = {
    'd': 'เริ่มการรายงาน', 'camp': 'ชื่อแคมเปญ', 'deliv': 'การแสดงแคมเปญ',
    'obj': 'วัตถุประสงค์', 'res': 'ผลลัพธ์', 'ind': 'ตัวระบุผลลัพธ์',
    'spend': 'จำนวนเงินที่ใช้จ่ายไป (THB)', 'imp': 'อิมเพรสชัน', 'reach': 'การเข้าถึง',
    'ctr_all': 'CTR (ทั้งหมด)', 'lclicks': 'การคลิกลิงก์แบบอินไลน์ในโฆษณา',
    'msg': 'การสนทนาผ่านการส่งข้อความที่เริ่มขึ้น', 'purch': 'การซื้อ',
    'roas': 'ROAS (ผลตอบแทนจากค่าใช้จ่ายในการโฆษณา) ของการซื้อ',
}
# ตัวเลขรายวันที่บวกข้ามวัน/ข้ามบัญชีได้ (reach ไม่อยู่ในนี้โดยเจตนา — ดูหัวไฟล์)
SUM_KEYS = ['spend', 'imp', 'clicks', 'lclicks', 'msg', 'purch', 'omni', 'lead', 'reach_d']


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def num(x):
    s = str(x or '').strip().replace(',', '')
    if not s: return 0.0
    try: return float(s)
    except ValueError: die('คอลัมน์ตัวเลขอ่านไม่ได้', s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    files = sorted(glob.glob(str(SRC / 'FBD_*.csv')))
    if not files: die('ไม่พบไฟล์ FBD_*.csv', str(SRC))

    accounts, camps, acc_days, days = [], {}, {}, {}
    seen_goal = {}          # (acc, campaign) -> ตัวระบุผลลัพธ์ที่ไม่ว่าง
    rows_all = []
    for fp in files:
        parts = Path(fp).stem.split('_')
        if len(parts) < 3: die('ชื่อไฟล์ไม่ตรงแพทเทิร์น FBD_<บัญชี>_<id>_<from>_<to>.csv', Path(fp).name)
        key, acct_id = parts[1], parts[2]
        with open(fp, encoding='utf-8-sig', newline='') as fh:
            rows = list(csv.DictReader(fh))
        if not rows: die('ไฟล์ว่าง', Path(fp).name)
        miss = [c for c in COL.values() if c not in rows[0]]
        if miss: die('ไฟล์ขาดคอลัมน์ที่ต้องใช้', {'file': Path(fp).name, 'missing': miss})
        accounts.append({'key': key, 'label': ACC_LABEL.get(key, key),
                         'id': acct_id, 'file': Path(fp).name, 'rows': len(rows)})
        for r in rows:
            rows_all.append((key, r))
            ind = (r[COL['ind']] or '').strip()
            if ind:
                if ind not in GOALS:
                    die('เจอตัวระบุผลลัพธ์ที่ยังไม่รู้จัก — ต้องเพิ่มใน GOALS ก่อน',
                        {'file': Path(fp).name, 'ind': ind})
                k = (key, r[COL['camp']])
                if seen_goal.get(k, ind) != ind:
                    die('แคมเปญเดียวมีตัวระบุผลลัพธ์ 2 แบบ — ต้องตัดสินใจก่อนว่าจะใช้อันไหน',
                        {'camp': k, 'a': seen_goal[k], 'b': ind})
                seen_goal[k] = ind

    # ── ประกอบรายวัน + รายแคมเปญ ────────────────────────────────────────────
    for key, r in rows_all:
        d = (r[COL['d']] or '').strip()
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', d):
            die('วันที่ในคอลัมน์ "เริ่มการรายงาน" ผิดรูปแบบ', d)
        imp = num(r[COL['imp']])
        goal = seen_goal.get((key, r[COL['camp']]), '')
        gk = GOALS[goal][0] if goal else 'none'
        # คลิกทั้งหมด: ไม่มีคอลัมน์นับ ถอดจาก CTR(ทั้งหมด) (ตรวจแล้วเป็นจำนวนเต็มพอดี)
        clicks = round(num(r[COL['ctr_all']]) / 100 * imp)
        res = num(r[COL['res']])
        rec = {'spend': num(r[COL['spend']]), 'imp': imp, 'clicks': clicks,
               'lclicks': num(r[COL['lclicks']]), 'msg': num(r[COL['msg']]),
               'purch': num(r[COL['purch']]),
               # ยอดซื้อ CPAS เกิดที่ Shopee ไม่โผล่ในคอลัมน์ "การซื้อ" ต้องแยกเก็บ
               'omni': res if gk == 'omni' else 0.0,
               'lead': res if gk == 'lead' else 0.0,
               'reach_d': num(r[COL['reach']])}
        for bucket in (days.setdefault(d, dict.fromkeys(SUM_KEYS, 0.0)),
                       acc_days.setdefault(key, {}).setdefault(d, dict.fromkeys(SUM_KEYS, 0.0))):
            for k in SUM_KEYS: bucket[k] += rec[k]
        c = camps.setdefault((key, r[COL['camp']]), {
            'acc': key, 'name': r[COL['camp']], 'goal': gk,
            'goal_label': GOALS[goal][1] if goal else 'ไม่มีผลลัพธ์ในรายงาน',
            'obj': r[COL['obj']], 'deliv': r[COL['deliv']], 'res': 0.0, 'roas_days': [],
            'mo': {}, **dict.fromkeys(SUM_KEYS, 0.0)})
        c['res'] += res
        c['deliv'] = r[COL['deliv']] or c['deliv']
        for k in SUM_KEYS: c[k] += rec[k]
        # รายเดือน: ตัวเลือกช่วงวันที่ของหน้านี้เลือกเป็น "เดือน" ตารางบัญชี/แคมเปญ
        # จึงต้องมีรายเดือนให้บวก ไม่งั้นพอมีข้อมูลเดือนถัดไปตารางจะโชว์ยอดรวมทุกเดือน
        # ทั้งที่ผู้ใช้เลือกเดือนเดียว (บั๊กแบบเดียวกับที่เคยเจอใน period picker)
        mo = c['mo'].setdefault(d[:7], dict.fromkeys(SUM_KEYS + ['res'], 0.0))
        mo['res'] += res
        for k in SUM_KEYS: mo[k] += rec[k]
        if r[COL['roas']].strip(): c['roas_days'].append(num(r[COL['roas']]))

    for c in camps.values():
        # ROAS: FB ส่งมาเป็นอัตราส่วนรายวัน ไม่มีมูลค่าการซื้อให้บวก -> ได้แค่ค่าเฉลี่ยถ่วง
        # ด้วยค่าโฆษณาไม่ได้ จึงเก็บเป็น "เฉลี่ยของวันที่มีค่า" + จำนวนวัน ให้หน้าเว็บบอกตรง ๆ
        c['roas'] = round(sum(c['roas_days']) / len(c['roas_days']), 4) if c['roas_days'] else None
        c['roas_n'] = len(c['roas_days'])
        del c['roas_days']
        for k in SUM_KEYS + ['res']: c[k] = round(c[k], 2)
        c['mo'] = {m: [round(v[k], 2) for k in SUM_KEYS + ['res']] for m, v in sorted(c['mo'].items())}

    for bucket in (days, *acc_days.values()):
        for d in bucket:
            for k in SUM_KEYS: bucket[d][k] = round(bucket[d][k], 2)

    dates = sorted(days)
    tot = {k: round(sum(days[d][k] for d in dates), 2) for k in SUM_KEYS}

    # ── ด่านตรวจ ────────────────────────────────────────────────────────────
    miss_d = [d for d in dates if not days[d]['spend'] and not days[d]['imp']]
    gap = [str(x) for x in _gaps(dates)]
    acc_sum = round(sum(v['spend'] for dd in acc_days.values() for v in dd.values()), 2)
    if abs(acc_sum - tot['spend']) > 0.01:
        die('ผลรวมรายบัญชีไม่เท่าผลรวมรายวัน', {'acc': acc_sum, 'day': tot['spend']})
    camp_sum = round(sum(c['spend'] for c in camps.values()), 2)
    if abs(camp_sum - tot['spend']) > 0.01:
        die('ผลรวมรายแคมเปญไม่เท่าผลรวมรายวัน', {'camp': camp_sum, 'day': tot['spend']})

    data = {
        'generated': datetime.now().astimezone().isoformat(timespec='seconds'),
        'from': dates[0], 'to': dates[-1], 'days_n': len(dates),
        'accounts': accounts, 'goals': {v[0]: {'label': v[1], 'res': v[2], 'cpr': v[3]}
                                        for v in GOALS.values()},
        'keys': SUM_KEYS, 'camp_keys': SUM_KEYS + ['res'],
        'months': sorted({d[:7] for d in dates}),
        'days': {d: [days[d][k] for k in SUM_KEYS] for d in dates},
        'acc_days': {a: {d: [v[k] for k in SUM_KEYS] for d, v in sorted(dd.items())}
                     for a, dd in acc_days.items()},
        'camps': sorted(camps.values(), key=lambda c: -c['spend']),
        'total': tot,
    }

    summary = {'from': dates[0], 'to': dates[-1], 'days': len(dates),
               'spend_total': tot['spend'],
               'spend_by_account': {a['label']: round(sum(v['spend'] for v in acc_days[a['key']].values()), 2)
                                    for a in accounts},
               'chats': tot['msg'], 'purchases_onsite': tot['purch'], 'purchases_cpas': tot['omni'],
               'leads': tot['lead'], 'campaigns': len(camps),
               'วันที่ขาดช่วง': gap, 'วันที่ไม่มียอดเลย': miss_d,
               'size_kb': round(len(json.dumps(data, ensure_ascii=False)) / 1024, 1)}

    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **summary}, ensure_ascii=False, indent=1)); return 0

    changed = []
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    # เทียบแบบ "ถอด generated ออกแล้วเทียบโครงสร้าง" — ไฟล์เขียนด้วย indent แต่ blob เป็น
    # compact ถ้าเทียบเป็นสตริงตรง ๆ จะไม่เท่ากันทุกครั้ง แล้ว commit ไฟล์เปล่าทุกรอบ
    try:
        old = json.loads(OUT.read_text(encoding='utf-8')) if OUT.exists() else None
    except Exception:
        old = None
    if old is not None: old.pop('generated', None)
    cmp_new = {k: v for k, v in data.items() if k != 'generated'}
    if old != cmp_new:
        OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
        changed.append(OUT.name)

    if not PAGE.exists(): die('ไม่พบไฟล์', str(PAGE))
    t = PAGE.read_text(encoding='utf-8')
    if START not in t or END not in t:
        die(f'ไม่พบบล็อก {START} ใน {PAGE.name} — ต้องเพิ่มบล็อกในหน้าเว็บก่อน')
    block = START + '\nconst FB_ADS = ' + blob + ';\n' + END
    new = re.sub(re.escape(START) + r'[\s\S]*?' + re.escape(END), lambda _: block, t)
    if _strip_gen(new) != _strip_gen(t):
        PAGE.write_text(new, encoding='utf-8'); changed.append(PAGE.name)

    print(json.dumps({'status': 'UPDATED' if changed else 'NO_CHANGE',
                      'changed': changed, **summary}, ensure_ascii=False))
    return 0 if changed else 10


def _strip_gen(s):
    """ตัด generated ออกก่อนเทียบ — ไม่งั้นรันซ้ำจะนับว่าเปลี่ยนทุกครั้งแล้ว commit เปล่า"""
    return re.sub(r'"generated"\s*:\s*"[^"]*"', '', s)


def _gaps(dates):
    out, cur = [], datetime.strptime(dates[0], '%Y-%m-%d').date()
    have = set(dates)
    last = datetime.strptime(dates[-1], '%Y-%m-%d').date()
    while cur <= last:
        if cur.isoformat() not in have: out.append(cur.isoformat())
        cur += timedelta(days=1)
    return out


if __name__ == '__main__':
    sys.exit(main())
