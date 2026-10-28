#!/usr/bin/env python3
"""ตรวจว่างานตั้งเวลา "ยังทำงานอยู่จริง" ไหม — อ่านอย่างเดียว ไม่แตะทะเบียนงาน

ทำไมต้องมี (28 ต.ค. 69):
  งาน `wibwub-ads-daily` ("การตลาด vs ยอดขาย") ค้างสถานะ running ตั้งแต่ 26 ต.ค. 20:50
  ตัวจัดตารางจึงไม่ยิงรอบใหม่เลย — รอบ 27 ต.ค. เช้า/เย็น และ 28 ต.ค. เช้า หายไปทั้งหมด
  **37 ชั่วโมงโดยไม่มีใครรู้** กว่าจะจับได้ก็ตอนไล่ดู git log ด้วยมือ

ตรวจ 2 ฝั่งคนละวิธี เพราะเข้าถึงข้อมูลได้ไม่เท่ากัน:
  · ฝั่ง local — อ่าน `scheduled-tasks.json` ได้ตรง ๆ (lastRunAt / lastScheduledFor)
    เทียบกับรอบที่ควรจะยิงตาม cron
  · ฝั่ง code — **ไม่มีไฟล์ให้อ่าน** (`~/.claude/scheduled-tasks/<id>/` มีแค่ SKILL.md
    ส่วน lastRunAt/isRunning อยู่ในสโตร์ของแอป ต้องใช้ MCP) -> ตรวจจาก **ผลงานปลายทาง**
    ตาม `scripts/ops/task_expect.json` แทน ซึ่งจับได้ทุกสาเหตุ ไม่ใช่แค่เซสชันค้าง
    (งานถูกปิด · รันแล้วล้มเงียบ · กล่องขออนุญาตไม่มีคนกด · สมาชิกหมดอายุ)

ตรวจ `.git/*.lock` ค้างด้วย — งานตั้งเวลาฝั่ง local **ลบไฟล์ใน .git ไม่ได้**
(พิสูจน์แล้ว 28 ต.ค. 69: git ในแซนด์บ็อกซ์ขึ้น `unable to unlink '.git/objects/../tmp_obj_..':
Operation not permitted`) ทุกรอบที่ commit จึงทิ้ง lock ไว้ให้ฝั่ง Mac มาเก็บ
ถ้า lock ค้างนาน = ทุกงานหลังจากนั้น commit ไม่ได้ทั้งหมด

ใช้:  python3 scripts/ops/task_health.py [--json] [--grace-min 60] [--delay-min 20] [--lock-min 30]
exit: 0 = ปกติ · 3 = มี ⛔ (ให้ขึ้นบรรทัดแรกของรายงานรอบนั้น) · 2 = ตัวตรวจเองมีปัญหา
"""
import sys, json, re, glob, argparse, subprocess
from pathlib import Path
from datetime import datetime, timedelta


def _find_base():
    p = Path(__file__).resolve()
    for d in (p, *p.parents):
        if (d / 'sw.js').is_file() and (d / '.git').exists():
            return d
    raise SystemExit('หาโฟลเดอร์ All ไม่เจอ — ห้ามเดาพาธ')


BASE = _find_base()
EXPECT = BASE / 'scripts' / 'ops' / 'task_expect.json'
REG_GLOB = str(Path.home() / 'Library' / 'Application Support' / 'Claude' /
               'local-agent-mode-sessions' / '*' / '*' / 'scheduled-tasks.json')


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


# ── cron ─────────────────────────────────────────────────────────────────────
def _field(spec, lo, hi):
    """รองรับ * · a,b,c · a-b · */n (พอสำหรับ cron ที่ใช้จริงในบ้านนี้)"""
    out = set()
    for part in str(spec).split(','):
        step = 1
        if '/' in part:
            part, s = part.split('/', 1)
            step = int(s)
        if part in ('*', ''):
            a, b = lo, hi
        elif '-' in part:
            a, b = (int(x) for x in part.split('-', 1))
        else:
            a = b = int(part)
        out |= set(range(a, b + 1, step))
    return out


def prev_fire(cron, now, back_days=70):   # 70 วัน เพื่อให้ cron รายเดือน (เช่น `0 9 5 * *`) หาเจอ
    """เวลาที่ cron ควรยิงล่าสุด (<= now) · None ถ้าไม่เจอในช่วงที่ไล่ย้อน"""
    try:
        m, h, dom, mon, dow = cron.split()
    except ValueError:
        return None
    M, H = _field(m, 0, 59), _field(h, 0, 23)
    DOM, MON = _field(dom, 1, 31), _field(mon, 1, 12)
    DOW = {d % 7 for d in _field(dow, 0, 7)}
    dom_any, dow_any = str(dom).strip() == '*', str(dow).strip() == '*'
    t = now.replace(second=0, microsecond=0)
    for _ in range(back_days * 24 * 60):
        if t.minute in M and t.hour in H and t.month in MON:
            cd = (t.weekday() + 1) % 7          # python จันทร์=0 -> cron อาทิตย์=0
            # cron มาตรฐาน: ถ้าจำกัดทั้ง dom และ dow ให้ถือว่า "อย่างใดอย่างหนึ่ง"
            ok = (t.day in DOM) if dow_any else (cd in DOW) if dom_any else \
                 (t.day in DOM or cd in DOW)
            if ok:
                return t
        t -= timedelta(minutes=1)
    return None


def iso(s):
    if not s: return None
    try:
        return datetime.fromisoformat(str(s).replace('Z', '+00:00')).astimezone().replace(tzinfo=None)
    except ValueError:
        return None


def hrs(a, b):
    return round((a - b).total_seconds() / 3600, 1)


# ── ฝั่ง local ───────────────────────────────────────────────────────────────
def check_local(now, grace_min, delay_min):
    # เครื่องนี้มีทะเบียนมากกว่า 1 ไฟล์ (คนละ workspace) — เอาเฉพาะอันที่เป็นงาน WIBWUB
    # ไม่งั้นจะไปตรวจงานของโปรเจกต์อื่น (เจอจริง: drhybrid-dashboard-monthly-update)
    out, reg, skipped = [], None, []
    for f in sorted(glob.glob(REG_GLOB)):
        try:
            d = json.loads(Path(f).read_text(encoding='utf-8'))
        except Exception:
            continue
        ts = d.get('scheduledTasks') or []
        mine = [x for x in ts if 'wibwub' in (x.get('filePath') or '').lower()]
        if not mine:
            if ts: skipped.append(Path(f).parts[-3][:8])
            continue
        if reg is None or len(mine) > len(reg):
            reg = mine
    if skipped:
        out.append({'lv': 'ℹ️', 'task': '(ทะเบียนอื่น)',
                    'msg': f'ข้ามทะเบียนของ workspace อื่น {len(skipped)} ไฟล์ — ไม่ใช่งาน WIBWUB'})
    if reg is None:
        return [{'lv': '⛔', 'task': '(ทะเบียนงาน local)',
                 'msg': 'อ่าน scheduled-tasks.json ไม่ได้ — ตรวจฝั่ง local ไม่ได้ทั้งหมด'}]
    for t in reg:
        if not t.get('enabled'):
            continue
        name = (t.get('filePath') or '').split('/Scheduled/')[-1].split('/')[0] or t.get('id')
        cron, last = t.get('cronExpression', ''), iso(t.get('lastRunAt'))
        exp = prev_fire(cron, now)
        if exp is None:
            out.append({'lv': '⛔', 'task': name, 'msg': f'อ่าน cron ไม่ออก: {cron}'}); continue
        if last is None:
            out.append({'lv': '⛔', 'task': name, 'msg': 'ไม่เคยมีบันทึกการรัน'}); continue
        late = (now - exp).total_seconds() / 60
        if last < exp and late > grace_min:
            out.append({'lv': '⛔', 'task': name,
                        'msg': f'รอบ {exp.strftime("%d %b %H:%M")} ไม่ได้รัน '
                               f'(รอบล่าสุด {last.strftime("%d %b %H:%M")} · ค้าง {hrs(now, last)} ชม.)'})
            continue
        sch = iso(t.get('lastScheduledFor'))
        if sch and (last - sch).total_seconds() / 60 > delay_min:
            out.append({'lv': '⚠️', 'task': name,
                        'msg': f'รอบล่าสุดเริ่มช้า {round((last - sch).total_seconds() / 60)} นาที '
                               f'(ตั้งไว้ {sch.strftime("%H:%M")} เริ่มจริง {last.strftime("%H:%M")}) '
                               f'— น่าจะติดเพดาน 3 งานพร้อมกัน'})
        else:
            out.append({'lv': '✅', 'task': name,
                        'msg': f'รอบล่าสุด {last.strftime("%d %b %H:%M")}'})
    return out


# ── ฝั่ง code ────────────────────────────────────────────────────────────────
def _git_last(pattern):
    r = subprocess.run(['git', '-C', str(BASE), 'log', '-1', '--format=%ct',
                        '--extended-regexp', f'--grep={pattern}'],
                       capture_output=True, text=True)
    s = r.stdout.strip()
    return datetime.fromtimestamp(int(s)) if s.isdigit() else None


def check_code(now):
    out = []
    try:
        cfg = json.loads(EXPECT.read_text(encoding='utf-8'))['code_tasks']
    except Exception as e:
        return [{'lv': '⛔', 'task': '(task_expect.json)',
                 'msg': f'อ่านไม่ได้: {type(e).__name__} — ตรวจฝั่ง code ไม่ได้ทั้งหมด'}]
    for tid, c in cfg.items():
        label, kind, maxh = c.get('label', tid), c.get('kind'), c.get('max_age_hours', 24)
        seen = None
        if kind == 'git_grep':
            seen = _git_last(c['pattern'])
        elif kind in ('mtime', 'regex_date'):
            fp = BASE / c['file']
            if not fp.exists():
                lv = '⚠️' if c.get('optional_file') else '⛔'
                out.append({'lv': lv, 'task': label, 'msg': f'ไม่พบไฟล์ {c["file"]}'}); continue
            if kind == 'mtime':
                seen = datetime.fromtimestamp(fp.stat().st_mtime)
            else:
                m = re.search(c['pattern'], fp.read_text(encoding='utf-8'))
                if not m:
                    out.append({'lv': '⛔', 'task': label,
                                'msg': f'หาแพทเทิร์นใน {c["file"]} ไม่เจอ — รูปแบบไฟล์อาจเปลี่ยน'}); continue
                seen = datetime.strptime(m.group(1), '%Y-%m-%d')
        elif kind == 'none':
            out.append({'lv': 'ℹ️', 'task': label,
                        'msg': 'ตรวจจากไฟล์ไม่ได้ — ' + c.get('note', '')[:90]}); continue
        else:
            out.append({'lv': '⛔', 'task': label, 'msg': f'kind ไม่รู้จัก: {kind}'}); continue
        if seen is None:
            out.append({'lv': '⛔', 'task': label, 'msg': 'ไม่พบหลักฐานว่าเคยมีผลงานเลย'}); continue
        age = hrs(now, seen)
        lv = '⛔' if age > maxh else '✅'
        # git_grep: ไม่มี commit ไม่ได้แปลว่าไม่ได้รัน (NO_CHANGE ก็ไม่ commit) -> เขียนให้ตรง
        tail = (' — ไม่มีผลงาน อาจรันแล้วแต่ไม่มีข้อมูลใหม่ ให้ไปดูว่างานยังรันอยู่ไหมก่อนสรุป'
                if lv == '⛔' and kind == 'git_grep' else '')
        out.append({'lv': lv, 'task': label,
                    'msg': f'ผลงานล่าสุด {seen.strftime("%d %b %H:%M")} ({age} ชม. · เกณฑ์ {maxh}){tail}'})
    return out


def check_locks(now, lock_min):
    """`.git/*.lock` ค้าง = ทุกงานหลังจากนั้น commit ไม่ได้

    ไม่ลบให้ — หน้าที่ลบเป็นของฝั่ง Mac (launchd) เพราะแซนด์บ็อกซ์ของงานตั้งเวลา
    ไม่มีสิทธิ์ลบไฟล์ใน .git · ตัวตรวจนี้แค่บอกว่ามีค้างอยู่
    """
    g = BASE / '.git'
    out = []
    try:
        locks = sorted(g.rglob('*.lock'))
    except Exception as e:
        return [{'lv': '⛔', 'task': '(.git lock)', 'msg': f'อ่าน .git ไม่ได้: {type(e).__name__}'}]
    old = []
    for p in locks:
        try:
            age = (now - datetime.fromtimestamp(p.stat().st_mtime)).total_seconds() / 60
        except OSError:
            continue
        if age > lock_min:
            old.append(f'{p.relative_to(g)} ({age:.0f} นาที)')
    if old:
        out.append({'lv': '⛔', 'task': '(.git lock ค้าง)',
                    'msg': 'ค้างอยู่ ' + ' · '.join(old[:4]) +
                           ' — ทุกงานที่ commit หลังจากนี้จะล้มจนกว่าจะถูกลบ '
                           '(ฝั่ง Mac เท่านั้นที่ลบได้ · งานตั้งเวลาลบเองไม่ได้)'})
    # เศษ tmp_obj_* ที่ git ในแซนด์บ็อกซ์ลบไม่ได้ — ไม่บล็อกงาน แต่โตวันละ ~100 ไฟล์
    try:
        tmp = list(g.glob('objects/*/tmp_obj_*'))
    except Exception:
        tmp = []
    if len(tmp) > 1500:
        mb = sum(p.stat().st_size for p in tmp) / 1024 / 1024
        out.append({'lv': '⚠️', 'task': '(.git objects)',
                    'msg': f'เศษไฟล์ tmp_obj_* {len(tmp)} ไฟล์ ({mb:.0f} MB) — ไม่บล็อกงาน '
                           'แต่ควรให้ฝั่ง Mac กวาดทิ้ง'})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--grace-min', type=int, default=60,
                    help='รอบที่เลยเวลามาแล้วเกินกี่นาทีจึงถือว่า "ไม่ได้รัน"')
    ap.add_argument('--delay-min', type=int, default=20,
                    help='เริ่มช้ากว่าที่ตั้งไว้กี่นาทีจึงเตือน')
    ap.add_argument('--lock-min', type=int, default=30,
                    help='.git/*.lock ค้างเกินกี่นาทีจึงถือว่าเป็นปัญหา')
    a = ap.parse_args()
    now = datetime.now()
    rows = check_locks(now, a.lock_min) + check_local(now, a.grace_min, a.delay_min) + check_code(now)
    bad = [r for r in rows if r['lv'] == '⛔']
    warn = [r for r in rows if r['lv'] == '⚠️']
    info = [r for r in rows if r['lv'] == 'ℹ️']
    if a.json:
        print(json.dumps({'checked_at': now.strftime('%Y-%m-%d %H:%M'),
                          'problems': len(bad), 'warnings': len(warn), 'rows': rows},
                         ensure_ascii=False, indent=1))
    else:
        for r in bad + warn + info:
            print(f'{r["lv"]} {r["task"]} — {r["msg"]}')
        if not bad and not warn and not info:
            print(f'✅ งานตั้งเวลาทุกตัวปกติ ({len(rows)} งาน)')
        elif not bad:
            print(f'(ไม่มีงานค้าง · {len(rows)} งาน)')
    return 3 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
