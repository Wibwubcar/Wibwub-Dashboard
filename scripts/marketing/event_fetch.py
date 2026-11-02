#!/usr/bin/env python3
"""ดึงค่าใช้จ่ายงาน Event จากชีต "Annual Budget 2026" แท็บ `MKT Event`

ทำไมต้องมี: ช่อง Event ของเมนู "การตลาด vs ยอดขาย" เคยกรอกมือใน
`data Ads/mkt_manual.json` ซึ่งไม่มีใครกรอกจริงเลยตั้งแต่เปิดหน้า -> หน้าเว็บขึ้น
"รอข้อมูล" มาตลอด · ย้ายมาอ่านจากชีตที่ทีมใช้จริง ให้เป็น **แหล่งเดียว** แบบเดียวกับ KOL

กติกาที่ผู้ใช้กำหนด (2 พ.ย. 69)
  · ยึด **วันที่จ่าย** เป็นวันของค่าใช้จ่าย (ทีมจะเพิ่มคอลัมน์ "วันที่จ่าย" ต่อท้ายแถวแต่ละงาน
    · ยังไม่จ่าย = เว้นว่าง · จ่ายหลายงวด = แยกแถว)
  · ยอดที่นับ = ช่อง **Actual** ของแถวที่ "มีวันที่จ่าย" เท่านั้น
  · แถวที่มีงบแต่ไม่มีวันที่ = "งบรอจ่าย" แสดงแยก **ไม่นับเข้ายอด**
  · อ่านเฉพาะ "แถวงาน" — ข้ามแถว Total / Total Expense / Actually
  · **คอลัมน์วันที่จ่ายยังไม่มี -> ไม่เดาวันที่** คืน days ว่าง หน้าเว็บขึ้น "รอข้อมูล" ตามเดิม

โครงชีต (เลย์เอาต์ที่รองรับ — ตรวจจากหัวตารางเอง ไม่ฝังเลขคอลัมน์)
  แบ่งเป็นบล็อกรายไตรมาส `Q2 2026` / `Q3 2026` / `Q4 2026`
  แต่ละบล็อกมีแถวชื่อเดือน (ภาษาไทย 3 เดือน) แล้วแถวหัว `Budget | Actual` ต่อเดือน
  คอลัมน์ A = ชื่องาน · B = งบรวมของงาน · ท้ายสุด = Total Actual

⛔ repo เป็น public + GitHub Pages เสิร์ฟหน้าเว็บสาธารณะ
   -> ไฟล์ที่ commit (`data Ads/event_daily.json`) เก็บ **ยอดรวมเท่านั้น**
   ชื่องาน/งบรายงานอยู่ใน `data Ads/event_rows_private.json` ซึ่ง **ห้าม commit**
   (รูปแบบเดียวกับ kol_fetch.py — ดูเหตุผลที่หัวไฟล์นั้น)

ใช้:  python3 scripts/marketing/event_fetch.py [--json-only]
exit: 0 = เขียนไฟล์แล้ว · 2 = ไม่ผ่านด่านตรวจ (ไม่เขียนไฟล์)
"""
import sys, re, json, argparse, subprocess
from datetime import datetime
from pathlib import Path


def _find_base():
    p = Path(__file__).resolve()
    for d in (p, *p.parents):
        if (d / 'sw.js').is_file() and (d / '.git').exists():
            return d
    raise SystemExit('หาโฟลเดอร์ All ไม่เจอ — ห้ามเดาพาธ')


BASE = _find_base()
OUT = BASE / 'data Ads' / 'event_daily.json'          # commit ได้ — ยอดรวมเท่านั้น
PRIV = BASE / 'data Ads' / 'event_rows_private.json'  # ห้าม commit — ชื่องาน + งบรายงาน
SHEET_ID = '1qOGnN2fgoVM93Ky26utRVFu_fVrtaVXr0J3cDTMEZmA'
TAB = 'MKT Event'
SA = Path.home() / 'wibwub-service-account.json'

MONTHS_TH = {'มกราคม': 1, 'กุมภาพันธ์': 2, 'มีนาคม': 3, 'เมษายน': 4, 'พฤษภาคม': 5,
             'มิถุนายน': 6, 'กรกฎาคม': 7, 'สิงหาคม': 8, 'กันยายน': 9, 'ตุลาคม': 10,
             'พฤศจิกายน': 11, 'ธันวาคม': 12}
# แถวสรุปที่ต้องข้าม — เทียบแบบ normalize ช่องว่าง + ตัวพิมพ์
SKIP_ROWS = {'total', 'total expense', 'actually', 'actual', 'sum', 'รวม'}
QUARTER = re.compile(r'^Q([1-4])\s*(\d{4})$')
PAY_DATE_HDR = 'วันที่จ่าย'


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail},
                     ensure_ascii=False))
    sys.exit(2)


def norm(s):
    return re.sub(r'\s+', ' ', (s or '')).strip()


def num(s):
    """'104,000.00' -> 104000.0 · ว่าง/ไม่ใช่เลข -> None"""
    t = norm(s).replace(',', '').replace('฿', '')
    if not t or t in ('-', '—'):
        return None
    try:
        return float(t)
    except ValueError:
        return None


def parse_date(s):
    """คืน YYYY-MM-DD · รับ d/m/yyyy, d/m/yy (พ.ศ. หรือ ค.ศ.), yyyy-mm-dd"""
    t = norm(s)
    if not t:
        return None
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', t):
        return t
    m = re.fullmatch(r'(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})', t)
    if not m:
        return None
    d, mo, y = (int(x) for x in m.groups())
    if y < 100:
        y += 2500 if y >= 60 else 2000      # 69 -> 2569 · 26 -> 2026
    if y > 2400:
        y -= 543                            # พ.ศ. -> ค.ศ.
    try:
        return datetime(y, mo, d).strftime('%Y-%m-%d')
    except ValueError:
        return None


def read_rows():
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError as e:
        die('import gspread/google-auth ไม่สำเร็จ — ต้องรันด้วย python ที่ติดตั้งไว้ '
            '(เครื่องนี้คือ /usr/bin/python3)', str(e))
    if not SA.exists():
        die(f'ไม่พบไฟล์ service account ที่ {SA}')
    cred = Credentials.from_service_account_file(
        str(SA), scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    try:
        sh = gspread.authorize(cred).open_by_key(SHEET_ID)
    except Exception as e:
        die('เปิดชีต Annual Budget ไม่ได้ — ตรวจว่าแชร์ให้ service account แล้ว (Viewer พอ)',
            f'{type(e).__name__}: {e}')
    try:
        return sh.worksheet(TAB).get_all_values()
    except Exception as e:
        die(f'ไม่พบแท็บ "{TAB}" — ถ้าทีมเปลี่ยนชื่อแท็บ ให้แก้ค่า TAB ในสคริปต์',
            f'{type(e).__name__}: {e}')


def parse_blocks(rows):
    """คืน (events, blocks_seen, pay_col_found)

    events = [{'name', 'budget', 'cells': [{'ym','budget','actual'}], 'pay_dates': [...]}]
    """
    events, blocks, pay_found = [], [], False
    i = 0
    while i < len(rows):
        qm = next((QUARTER.match(norm(c)) for c in rows[i] if QUARTER.match(norm(c))), None)
        if not qm:
            i += 1
            continue
        year = int(qm.group(2))
        # แถวชื่อเดือน
        j, months = i + 1, {}
        while j < min(i + 6, len(rows)):
            found = {k: MONTHS_TH[norm(c)] for k, c in enumerate(rows[j])
                     if norm(c) in MONTHS_TH}
            if found:
                months = found
                break
            j += 1
        if not months:
            die('เจอหัวไตรมาสแต่หาแถวชื่อเดือนไม่เจอ — โครงชีตเปลี่ยน ให้ตรวจก่อนเชื่อตัวเลข',
                {'quarter': qm.group(0), 'row': i + 1})
        # แถวหัว Budget/Actual
        k = j + 1
        while k < min(j + 6, len(rows)):
            cells = [norm(c).lower() for c in rows[k]]
            if 'budget' in cells and 'actual' in cells:
                break
            k += 1
        else:
            die('หาแถวหัว Budget/Actual ไม่เจอ', {'quarter': qm.group(0)})
        hdr = [norm(c) for c in rows[k]]
        pay_cols = [c for c, h in enumerate(hdr) if PAY_DATE_HDR in h]
        if pay_cols:
            pay_found = True
        # จับคู่เดือน -> (คอลัมน์ Budget, คอลัมน์ Actual) จากหัวตารางจริง
        colmap = {}
        for col, mo in sorted(months.items()):
            b = col if hdr[col:col + 1] and hdr[col].lower() == 'budget' else None
            a = col + 1 if len(hdr) > col + 1 and hdr[col + 1].lower() == 'actual' else None
            if b is None or a is None:
                die('หัว Budget/Actual ไม่ตรงกับคอลัมน์ชื่อเดือน — โครงชีตเปลี่ยน',
                    {'quarter': qm.group(0), 'month': mo,
                     'hdr_รอบคอลัมน์นั้น': hdr[max(0, col - 1):col + 3]})
            colmap[mo] = (b, a)
        blocks.append({'quarter': qm.group(0), 'months': sorted(colmap),
                       'pay_date_cols': pay_cols})
        # แถวงาน
        r = k + 1
        while r < len(rows):
            name = norm(rows[r][0] if rows[r] else '')
            if not name:
                break
            if name.lower() in SKIP_ROWS:
                break
            ev = {'name': name, 'budget': num(rows[r][1] if len(rows[r]) > 1 else ''),
                  'cells': [], 'pay_dates': []}
            for mo, (bc, ac) in colmap.items():
                b = num(rows[r][bc]) if len(rows[r]) > bc else None
                a = num(rows[r][ac]) if len(rows[r]) > ac else None
                if b or a:
                    ev['cells'].append({'ym': '%04d-%02d' % (year, mo),
                                        'budget': b or 0.0, 'actual': a or 0.0})
            for pc in pay_cols:
                d = parse_date(rows[r][pc]) if len(rows[r]) > pc else None
                if d:
                    ev['pay_dates'].append(d)
            events.append(ev)
            r += 1
        i = r
    if not blocks:
        die('ไม่เจอหัวไตรมาส (Qn YYYY) เลยในแท็บนี้ — โครงชีตเปลี่ยน')
    return events, blocks, pay_found


def git_ignored(p):
    """(ignored, tracked) — เขียนไฟล์ private ต่อเมื่อ git ยืนยันว่า ignore แล้ว"""
    rel = str(p.relative_to(BASE))
    try:
        ig = subprocess.run(['git', 'check-ignore', '-q', rel], cwd=str(BASE),
                            capture_output=True).returncode == 0
        tr = subprocess.run(['git', 'ls-files', '--error-unmatch', rel], cwd=str(BASE),
                            capture_output=True).returncode == 0
    except Exception:
        return False, False
    return ig, tr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json-only', action='store_true',
                    help='พิมพ์ผลอย่างเดียว ไม่เขียนไฟล์ (ใช้ตรวจก่อนรันจริง)')
    a = ap.parse_args()

    events, blocks, pay_found = parse_blocks(read_rows())

    days, months, no_date_actual, no_actual_budget = {}, {}, {}, 0.0
    for ev in events:
        act = sum(c['actual'] for c in ev['cells'])
        bud = ev['budget'] or sum(c['budget'] for c in ev['cells'])
        for c in ev['cells']:
            if c['actual']:
                m = months.setdefault(c['ym'], {'actual': 0.0, 'budget': 0.0})
                m['actual'] += c['actual']
            if c['budget']:
                months.setdefault(c['ym'], {'actual': 0.0, 'budget': 0.0})['budget'] += c['budget']
        if ev['pay_dates'] and act:
            # จ่ายหลายงวด = แยกแถวตามกติกา -> แถวหนึ่งควรมีวันเดียว
            # ถ้ามีหลายวันในแถวเดียว ไม่หารเฉลี่ย (เดาไม่ได้) ให้ตีกลับ
            if len(ev['pay_dates']) > 1:
                die('แถวเดียวมีวันที่จ่ายหลายวัน — กติกาคือจ่ายหลายงวดต้องแยกแถว '
                    'สคริปต์ไม่หารเฉลี่ยให้', {'งาน': ev['name'], 'วันที่': ev['pay_dates']})
            days[ev['pay_dates'][0]] = round(days.get(ev['pay_dates'][0], 0.0) + act, 2)
        elif act:
            for c in ev['cells']:
                if c['actual']:
                    no_date_actual[c['ym']] = round(
                        no_date_actual.get(c['ym'], 0.0) + c['actual'], 2)
        if not act and bud:
            no_actual_budget += bud

    for m in months.values():
        m['actual'] = round(m['actual'], 2)
        m['budget'] = round(m['budget'], 2)

    status = 'OK' if pay_found else 'WAIT_PAY_DATE_COL'
    out = {
        'generated': datetime.now().strftime('%Y-%m-%dT%H:%M:%S+07:00'),
        'source': {'sheet': 'Annual Budget 2026', 'tab': TAB, 'id': SHEET_ID},
        'status': status,
        'has_pay_date_col': pay_found,
        'days': days,
        'months': months,
        'pending': {
            'actual_no_pay_date': no_date_actual,
            'budget_no_actual': round(no_actual_budget, 2),
        },
        'events_n': len(events),
        'blocks': blocks,
        'note': ('นับเฉพาะ Actual ของแถวที่มีวันที่จ่าย'
                 if pay_found else
                 'ยังไม่มีคอลัมน์ "วันที่จ่าย" ในชีต -> days ว่างโดยตั้งใจ '
                 'หน้าเว็บต้องขึ้น "รอข้อมูล" ห้ามเดาวันที่ · '
                 'ยอด Actual ที่มีอยู่แล้วรายงานไว้ใน pending.actual_no_pay_date'),
        'privacy': ('ชื่องานและงบรายงานอยู่ที่ data Ads/event_rows_private.json '
                    '(gitignored) — ไฟล์นี้เก็บยอดรวมเท่านั้นเพราะ repo เป็น public'),
    }

    # ด่านกันชื่องานหลุดเข้าไฟล์ที่ commit
    blob = json.dumps(out, ensure_ascii=False)
    for ev in events:
        if ev['name'] and ev['name'] in blob:
            die('พบชื่องาน Event ในไฟล์ที่จะ commit — repo เป็น public ห้ามส่งลงไป',
                ev['name'])

    priv = {'generated': out['generated'],
            'events': [{'name': e['name'], 'budget': e['budget'], 'cells': e['cells'],
                        'pay_dates': e['pay_dates']} for e in events]}

    if a.json_only:
        print(json.dumps({**out, '_preview': True}, ensure_ascii=False, indent=1))
        return 0

    prev = json.loads(OUT.read_text(encoding='utf-8')) if OUT.exists() else {}
    same = {k: v for k, v in prev.items() if k != 'generated'} == \
           {k: v for k, v in out.items() if k != 'generated'}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

    ignored, tracked = git_ignored(PRIV)
    if tracked:
        die('event_rows_private.json ถูก track อยู่ใน git — ให้ git rm --cached ก่อน')
    if ignored:
        PRIV.write_text(json.dumps(priv, ensure_ascii=False, indent=1) + '\n',
                        encoding='utf-8')
        priv_note = f'เขียนแล้ว {len(events)} งาน (gitignored)'
    else:
        priv_note = 'ไม่ได้เขียน — git ยังไม่ยืนยันว่าไฟล์นี้ถูก ignore'

    print(json.dumps({'status': 'NO_CHANGE' if same else 'UPDATED',
                      'pay_date_col': pay_found,
                      'days_with_amount': len(days),
                      'months': {k: v['actual'] for k, v in sorted(months.items())},
                      'pending': out['pending'],
                      'events_n': len(events),
                      'private': priv_note}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
