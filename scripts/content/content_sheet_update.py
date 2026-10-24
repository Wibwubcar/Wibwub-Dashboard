#!/usr/bin/env python3
"""เติมตัวเลขคลิป TikTok ลงแท็บ CONTENT — เติมเฉพาะช่องว่าง ห้ามทับของเดิม

ชีต: 1OWZGQD1wHvIlLAAg_7rJ0CtL-X9vEx4py-cRp_e3NvQ แท็บ CONTENT

คอลัมน์ที่งานนี้แตะได้เท่านั้น:
  K = 5 Sec Retention %      N = Avg. Duration (วินาที)
  O = Length (วินาที)        P = View
  Q = Love   R = Comment     S = Share   T = Save
แถวใหม่เพิ่ม A (วันที่) B ("Post") D (เนื้อหา) H (hashtags) I (ลิงก์) ให้ด้วย
**ไม่แตะ C/E/F/G/J เด็ดขาด** — เป็นงานจัดหมวด/เขียนเชิงกลยุทธ์ของทีม
**ไม่แตะ L/M/U** — เป็นสูตร คำนวณเองจาก K/N/O/P

ใช้:
  plan                 -> บอกว่าแถวไหนยังว่าง + คลิปไหนยังไม่มีแถว (อ่านอย่างเดียว)
  write --in <file>    -> เขียนจากไฟล์ JSON ที่ได้จาก tt_content_collect.js
  write --in <f> --dry-run

รูปแบบไฟล์ --in : list ของ object จาก tt_content_collect.js
  [{"video_id":"...","posted":"30/9/2026","len_sec":60,"ret5":"22%",
    "avg_watch":"7.94","views":1309,"likes":27,"comments":5,"shares":1,
    "saves":1,"views_approx":false,"caption":"...","hashtags":"#..."}]

exit: 0 = เขียนแล้ว · 10 = ไม่มีอะไรต้องเขียน · 2 = ผิดพลาด (ไม่เขียนอะไรเลย)
"""
import sys, json, argparse, re, time
from pathlib import Path

SHEET_ID = '1OWZGQD1wHvIlLAAg_7rJ0CtL-X9vEx4py-cRp_e3NvQ'
TAB = 'CONTENT'
SA = Path.home() / 'wibwub-service-account.json'
FIRST_ROW = 2                      # แถว 1 เป็นหัวตาราง

# ชื่อคอลัมน์ -> index (0-based) ตามหัวตารางจริง
COL = dict(A=0, B=1, C=2, D=3, E=4, F=5, G=6, H=7, I=8, J=9,
           K=10, L=11, M=12, N=13, O=14, P=15, Q=16, R=17, S=18, T=19, U=20)
FILL = ['K', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']       # ช่องตัวเลขที่เติมได้


def die(msg, detail=None, code=2):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(code)


def vid_of(url):
    """ดึง video id จากลิงก์ในคอลัมน์ I (รูปแบบลิงก์ไม่เหมือนกันทุกแถว บางอันมี query ต่อท้าย)"""
    m = re.search(r'/video/(\d+)', str(url or ''))
    return m.group(1) if m else None


def th_date(posted):
    """'30/9/2026' (ค.ศ.) -> '30/9/26' ตามรูปแบบที่ชีตใช้อยู่ (ปี 2 หลักของ ค.ศ.)"""
    m = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})$', str(posted or '').strip())
    if not m:
        return None
    d, mo, y = m.groups()
    return f'{int(d)}/{int(mo)}/{y[2:]}'


def open_sheet(write=False):
    if not SA.exists():
        die('ไม่พบ service account', str(SA))
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except Exception as e:
        die('import gspread/google-auth ไม่สำเร็จ', f'{type(e).__name__}: {e}')
    scope = 'https://www.googleapis.com/auth/spreadsheets'
    if not write:
        scope += '.readonly'
    cred = Credentials.from_service_account_file(str(SA), scopes=[scope])
    try:
        return gspread.authorize(cred).open_by_key(SHEET_ID).worksheet(TAB)
    except Exception as e:
        die('เปิดชีตไม่สำเร็จ — service account อาจยังไม่ได้รับสิทธิ์',
            f'{type(e).__name__}: {e}')


def read_rows(ws):
    vals = ws.get_values(f'A{FIRST_ROW}:U')
    out = []
    for i, r in enumerate(vals):
        r = list(r) + [''] * (21 - len(r))
        out.append({'row': FIRST_ROW + i, 'date': r[COL['A']].strip(),
                    'link': r[COL['I']].strip(), 'vid': vid_of(r[COL['I']]),
                    'cells': r})
    return out


def cmd_plan(a):
    rows = read_rows(open_sheet())
    used = [r for r in rows if r['date'] or r['link']]
    need, have = [], {}
    for r in used:
        if r['vid']:
            have[r['vid']] = r['row']
        empty = [c for c in FILL if not str(r['cells'][COL[c]]).strip()]
        if empty and r['vid']:
            need.append({'row': r['row'], 'date': r['date'],
                         'video_id': r['vid'], 'empty': empty})
    last = max([r['row'] for r in used], default=FIRST_ROW - 1)
    print(json.dumps({'status': 'OK', 'rows_used': len(used), 'last_row': last,
                      'next_free_row': last + 1, 'need_fill': need,
                      'known_video_ids': list(have)}, ensure_ascii=False))


def cmd_write(a):
    src = Path(a.input)
    # ด่านกันเขียนซ้ำด้วยไฟล์เก่า: ท่อนเก็บตัวเลขอยู่คนละงาน (local ผ่าน Chrome)
    # ถ้าท่อนนั้นล้ม ไฟล์เดิมจะยังอยู่ และงานนี้จะเขียนของเก่าซ้ำโดยไม่รู้ตัว (24 ต.ค. 69)
    if getattr(a, 'max_age_min', None):
        if not src.exists():
            die('ไม่พบไฟล์ --in', str(src), code=3)
        age = (time.time() - src.stat().st_mtime) / 60
        if age > a.max_age_min:
            die('ไฟล์ --in เก่าเกินกำหนด ไม่เขียนซ้ำ',
                f'{src.name} เก่า {age:.0f} นาที (จำกัด {a.max_age_min}) '
                f'— ให้งานที่เก็บตัวเลขคลิปรันใหม่ก่อน', code=3)
    try:
        items = json.loads(src.read_text(encoding='utf-8'))
    except Exception as e:
        die('อ่านไฟล์ --in ไม่ได้', f'{type(e).__name__}: {e}')
    if isinstance(items, dict):
        items = [items]
    items = [x for x in items if x.get('ok') is not False and x.get('video_id')]
    if not items:
        die('ไฟล์ --in ไม่มีคลิปที่ใช้ได้')

    ws = open_sheet(write=True)
    rows = read_rows(ws)
    by_vid = {r['vid']: r for r in rows if r['vid']}
    used = [r for r in rows if r['date'] or r['link']]
    next_free = max([r['row'] for r in used], default=FIRST_ROW - 1) + 1

    updates, added, filled, skipped = [], [], [], []
    for it in sorted(items, key=lambda x: (x.get('posted') or '')):
        vid = str(it['video_id'])
        tgt = by_vid.get(vid)
        if tgt is None:
            # คลิปใหม่ -> แถวใหม่ท้ายตาราง
            row = next_free
            next_free += 1
            d = th_date(it.get('posted'))
            if not d:
                skipped.append({'video_id': vid, 'why': 'อ่านวันที่โพสต์ไม่ได้'})
                continue
            updates += [(f'A{row}', d), (f'B{row}', 'Post')]
            if it.get('caption'):  updates.append((f'D{row}', it['caption']))
            if it.get('hashtags'): updates.append((f'H{row}', it['hashtags']))
            updates.append((f'I{row}', f"https://www.tiktok.com/@wibwubcar/video/{vid}"))
            cells = [''] * 21
            added.append({'row': row, 'date': d, 'video_id': vid})
        else:
            row, cells = tgt['row'], tgt['cells']

        val = {'K': it.get('ret5'), 'N': it.get('avg_watch'), 'O': it.get('len_sec'),
               'P': it.get('views'), 'Q': it.get('likes'), 'R': it.get('comments'),
               'S': it.get('shares'), 'T': it.get('saves')}
        wrote = []
        for c in FILL:
            if str(cells[COL[c]]).strip():
                continue                      # ⚠️ มีค่าอยู่แล้ว -> ข้าม ห้ามทับ
            v = val[c]
            if v is None or v == '':
                continue
            updates.append((f'{c}{row}', v))
            wrote.append(c)
        if wrote and tgt is not None:
            filled.append({'row': row, 'video_id': vid, 'cols': wrote})
        if it.get('views_approx'):
            skipped.append({'video_id': vid, 'why': 'ยอดวิวถูกแพลตฟอร์มย่อ (เช่น 232K) '
                                                    'ค่าที่เขียนเป็นเลขปัด ไม่ใช่เลขจริง'})

    if not updates:
        print(json.dumps({'status': 'NO_CHANGE', 'note': 'ทุกช่องมีข้อมูลอยู่แล้ว'},
                         ensure_ascii=False))
        sys.exit(10)

    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', 'cells': len(updates), 'added': added,
                          'filled': filled, 'notes': skipped,
                          'sample': updates[:12]}, ensure_ascii=False))
        return

    try:
        # ⚠️ ws.batch_update ของ gspread เติมชื่อแท็บให้เองแล้ว
        # ถ้าใส่ 'CONTENT!' ไปด้วยจะกลายเป็น 'CONTENT'!CONTENT!B153 แล้ว API ตีกลับ 400
        ws.batch_update([{'range': rng, 'values': [[v]]} for rng, v in updates],
                        value_input_option='USER_ENTERED')
    except Exception as e:
        die('เขียนชีตไม่สำเร็จ', f'{type(e).__name__}: {e}')
    print(json.dumps({'status': 'UPDATED', 'cells': len(updates), 'added': added,
                      'filled': filled, 'notes': skipped}, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('plan')
    w = sub.add_parser('write')
    w.add_argument('--in', dest='input', required=True)
    w.add_argument('--dry-run', action='store_true')
    w.add_argument('--max-age-min', type=int, dest='max_age_min')
    a = ap.parse_args()
    (cmd_plan if a.cmd == 'plan' else cmd_write)(a)


if __name__ == '__main__':
    main()
