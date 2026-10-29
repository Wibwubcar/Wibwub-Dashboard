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
import sys, io, json, re, glob, argparse, subprocess
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


# ═════════════════════════════════════════════════════════════════════════════
# ชั้นสถานะรายงาน (29 ต.ค. 69) — อ่านไฟล์เซสชันจริง แล้วเขียน task_health.json
# ให้หน้า Dashboard อ่าน · ผู้ใช้มองไม่เห็นเซสชันของงานตั้งเวลาในแอป จึงต้องมีหน้านี้
#
# ⚠️ รันได้จากงานฝั่ง code เท่านั้น — ฝั่ง local อยู่ในแซนด์บ็อกซ์ อ่าน
#    ~/Library/Application Support ไม่ได้ · อ่านไม่ได้ต้องขึ้น "ตรวจไม่ได้" ห้ามขึ้น "ปกติ"
# ⚠️ repo เป็นสาธารณะ — JSON ที่เขียนออกไปห้ามมีพาธในเครื่อง session id ชื่อบัญชี อีเมล
# ═════════════════════════════════════════════════════════════════════════════
SESS_CODE = str(Path.home() / 'Library' / 'Application Support' / 'Claude' /
                'claude-code-sessions' / '*' / '*' / 'local_*.json')
SESS_LOCAL = str(Path.home() / 'Library' / 'Application Support' / 'Claude' /
                 'local-agent-mode-sessions' / '*' / '*' / 'local_*.json')
PROJ_GLOB = str(Path.home() / '.claude' / 'projects' / '*')

NOT_STARTED_MIN = 20      # งาน local เริ่มช้าได้ถึง ~15 นาทีเป็นปกติ (วัดจริง 29 ต.ค. 69)
SILENT_MIN = 15           # เซสชันเงียบเกินเท่านี้ + ผลงานยังไม่ออก = ค้าง
STALE_HOURS = 14          # task_health.json เก่ากว่านี้ = ตัวตรวจเองไม่ได้รัน


def _ms(v):
    try:
        return datetime.fromtimestamp(float(v) / 1000)
    except (TypeError, ValueError):
        return None


def load_sessions(pattern):
    """{taskId: [เซสชันเรียงจากเก่าไปใหม่]} · (None, เหตุผล) ถ้าอ่านไม่ได้"""
    files = glob.glob(pattern)
    if not files:
        return None, 'ไม่พบไฟล์เซสชัน (อ่านโฟลเดอร์ไม่ได้ หรือรันจากฝั่ง local)'
    by = {}
    for f in files:
        try:
            d = json.loads(Path(f).read_text(encoding='utf-8'))
        except Exception:
            continue
        tid = d.get('scheduledTaskId')
        if not tid:
            continue
        by.setdefault(tid, []).append(d)
    for v in by.values():
        v.sort(key=lambda x: x.get('createdAt') or 0)
    return by, None


ERR_PATS = ('"status": "ERROR"', '\\"status\\": \\"ERROR\\"',
            '"status":"ERROR"', '\\"status\\":\\"ERROR\\"')


def _transcript(sess):
    """พาธบันทึกของเซสชัน · ฝั่ง code = ~/.claude/projects/<โปรเจกต์>/<cliSessionId>.jsonl
    ฝั่ง local = <workspace>/<8 ตัวแรกของ sessionId>/audit.jsonl"""
    cli = sess.get('cliSessionId')
    if cli:
        g = glob.glob(str(Path(PROJ_GLOB) / (cli + '.jsonl')))
        if g:
            return g[0]
    # sessionId มาเป็น 'local_<uuid>' — โฟลเดอร์ audit ใช้ 8 ตัวแรกของ uuid ไม่ใช่ของทั้งก้อน
    sid = (sess.get('sessionId') or '').replace('local_', '', 1)[:8]
    if sid:
        for f in glob.glob(SESS_LOCAL):
            cand = Path(f).parent / sid / 'audit.jsonl'
            if cand.exists():
                return str(cand)
    return None


def session_facts(sess, now):
    """ข้อเท็จจริงที่อ่านได้จริงของเซสชันหนึ่งรอบ — ไม่เดาสถานะ

    **ไม่มีสัญญาณ "จบแล้ว" ที่เชื่อถือได้ฝั่ง code** — บันทึกของฝั่งนั้นไม่มี event
    `result` แบบฝั่ง local (ตรวจแล้ว 29 ต.ค. 69: มีแต่ assistant/api-request/cost-state)
    และ `isRunning` อยู่ในสโตร์ของแอป อ่านจากสคริปต์ไม่ได้
    จึงใช้ "เงียบนานแค่ไหน" คู่กับ "ผลงานปลายทางออกหรือยัง" ตัดสินแทน ตามที่ผู้ใช้กำหนด
    """
    la = _ms(sess.get('lastActivityAt'))
    f = {'silent_min': round((now - la).total_seconds() / 60) if la else None,
         'has_result': None, 'has_error': None, 'ended_with_text': None}
    p = _transcript(sess)
    if not p:
        return f
    try:
        txt = io.open(p, encoding='utf-8', errors='replace').read()
    except OSError:
        return f
    f['has_result'] = ('"type": "result"' in txt) or ('"type":"result"' in txt)
    f['has_error'] = any(e in txt for e in ERR_PATS)
    # สัญญาณ "รอบนี้จบแล้ว" ที่เชื่อได้ที่สุด = ข้อความ assistant ก้อนสุดท้ายเป็น text
    # (รายงานปิดท้าย) ไม่ใช่ tool_use ที่ค้างรออนุญาต
    #   ตรวจกับเหตุการณ์จริง 28 ต.ค. 69: HR 20:30 ที่ค้าง -> ['tool_use'] ไม่มี text
    #   ส่วน tiktok-content / tiktok-live รอบเดียวกันที่จบปกติ -> ['text']
    # ข้อจำกัด: รอบที่ถูกสั่งหยุดจะได้เขียนรายงานตอนถูกหยุด ย้อนหลังจึงดูเหมือนจบปกติ
    # (ads-daily 28 ต.ค. 20:45) — ตอนค้างอยู่จริงยังไม่มี text ตัวตรวจจึงจับได้ในเวลาจริง
    last = None
    for line in txt.split('\n'):
        if '"assistant"' not in line:
            continue
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get('type') == 'assistant':
            last = o
    if last is not None:
        cs = (last.get('message') or {}).get('content') or []
        f['ended_with_text'] = any(c.get('type') == 'text' and (c.get('text') or '').strip()
                                   for c in cs)
    return f


def artifact_age(cfg, now):
    """(อายุเป็นชั่วโมง, ข้อความเวลา, datetime ของผลงาน) · (None, เหตุผล, None) ถ้าตรวจไม่ได้"""
    kind = cfg.get('kind')
    if kind == 'git_grep':
        seen = _git_last(cfg['pattern'])
    elif kind in ('mtime', 'regex_date'):
        fp = BASE / cfg['file']
        if not fp.exists():
            return None, 'ไม่พบไฟล์ผลงาน', None
        if kind == 'mtime':
            seen = datetime.fromtimestamp(fp.stat().st_mtime)
        else:
            m = re.search(cfg['pattern'], fp.read_text(encoding='utf-8'))
            seen = datetime.strptime(m.group(1), '%Y-%m-%d') if m else None
    else:
        return None, 'งานนี้ไม่มีผลงานปลายทางให้ตรวจ', None
    if seen is None:
        return None, 'ไม่พบหลักฐานผลงาน', None
    return hrs(now, seen), seen.strftime('%d %b %H:%M'), seen


DESC_TIME = re.compile(r'[0-2]?\d:[0-5]\d')


def desc_vs_cron(prompt_file, cron):
    """เทียบเวลาใน description ของไฟล์พรอมป์กับ cron จริง"""
    fp = BASE / 'scripts' / 'task_prompts' / prompt_file if prompt_file else None
    if not fp or not fp.exists():
        return None, 'ไม่มีไฟล์พรอมป์ให้เทียบ'
    desc = None
    for line in fp.read_text(encoding='utf-8', errors='replace').split('\n')[:12]:
        if line.startswith('description:'):
            desc = line[12:].strip(); break
    if not desc:
        return None, 'ไม่มี description ให้เทียบ'
    got = set(DESC_TIME.findall(desc))
    if not got:
        return None, 'description ไม่ได้ระบุเวลา'
    try:
        mi, hh = cron.split()[0], cron.split()[1]
        want = {'%02d:%02d' % (int(h), int(m))
                for h in hh.split(',') if h.isdigit()
                for m in mi.split(',') if m.isdigit()}
    except Exception:
        return None, 'อ่าน cron ไม่ออก'
    if not want:
        return None, 'cron ไม่ใช่รูปแบบที่เทียบได้'
    return (got == want), '%s vs cron %s' % ('/'.join(sorted(got)), '/'.join(sorted(want)))


def build_status(now):
    """รวมทุกอย่างเป็นแถวพร้อมขึ้นหน้าเว็บ — ห้ามใส่ข้อมูลที่ระบุตัวตน/พาธ"""
    rows, unreadable = [], []
    code_sess, err_c = load_sessions(SESS_CODE)
    if err_c:
        unreadable.append('เซสชันฝั่ง code: ' + err_c)
    local_sess, err_l = load_sessions(SESS_LOCAL)
    if err_l:
        unreadable.append('เซสชันฝั่ง local: ' + err_l)

    try:
        cfg_all = json.loads(EXPECT.read_text(encoding='utf-8'))
        code_cfg = cfg_all['code_tasks']
    except Exception as e:
        code_cfg = {}
        unreadable.append('task_expect.json: %s' % type(e).__name__)

    # ── ทะเบียนงาน local ────────────────────────────────────────────────────
    reg = None
    for f in sorted(glob.glob(REG_GLOB)):
        try:
            d = json.loads(Path(f).read_text(encoding='utf-8'))
        except Exception:
            continue
        mine = [x for x in (d.get('scheduledTasks') or [])
                if 'wibwub' in (x.get('filePath') or '').lower()]
        if mine and (reg is None or len(mine) > len(reg)):
            reg = mine
    if reg is None:
        unreadable.append('ทะเบียนงาน local: อ่านไม่ได้')

    def mk(name, side, cron, last_run, sched, sess_list, acfg, prompt_file):
        r = {'name': name, 'side': side, 'cron': cron}
        # ตัดเซสชันที่เกิดหลังเวลาที่กำลังตรวจทิ้ง เพื่อให้ --at ย้อนหลังได้จริง
        sess_list = [x for x in sess_list if (_ms(x.get('createdAt')) or now) <= now]
        if last_run and last_run > now:
            last_run = _ms(sess_list[-1].get('createdAt')) if sess_list else None
        exp = prev_fire(cron, now) if cron else None
        r['last_round'] = last_run.strftime('%d %b %H:%M') if last_run else '—'
        # ผลงานปลายทาง
        age, when, art_at = (None, None, None)
        if acfg:
            age, when, art_at = artifact_age(acfg, now)
        r['data_asof'] = when if when else '—'
        maxh = (acfg or {}).get('max_age_hours')
        # รอบล่าสุดเริ่มหรือยัง
        started = bool(last_run and exp and last_run >= exp)
        late_min = round((now - exp).total_seconds() / 60) if exp else None
        sess = sess_list[-1] if sess_list else None
        fct = session_facts(sess, now) if sess else {'silent_min': None,
                                                     'has_result': None, 'has_error': None}
        silent = fct['silent_min']
        r['silent_min'] = silent if silent is not None else ''
        # "ผลงานออกแล้ว" ต้องหมายถึง **ออกสำหรับรอบนี้** คือใหม่กว่าเวลาที่รอบเริ่ม
        # ไม่ใช่แค่ "ยังไม่เกิน max_age_hours" — เกณฑ์ชั่วโมงมักยาวกว่าระยะห่างระหว่างรอบ
        # จึงมองไม่เห็นรอบที่ค้าง (28 ต.ค. 69: HR 20:30 ค้าง แต่ hr_state.json ของรอบ 10:30
        # ยังอายุแค่ 11 ชม. < เกณฑ์ 16 ชม. ตัวตรวจเลยขึ้นว่าปกติทั้งที่งานค้างอยู่)
        done_this_round = (art_at is not None and last_run is not None
                           and art_at >= last_run - timedelta(minutes=2))
        fresh = (maxh is not None and age is not None and age <= maxh)
        # ── ตัดสินสถานะ ──
        # หมายเหตุสำคัญ (29 ต.ค. 69): สัญญาณที่เชื่อได้มีแค่ 2 อย่างคือ "เวลาเริ่มรอบ"
        # (จากทะเบียน/ไฟล์เซสชัน) กับ "ผลงานปลายทาง" (task_expect.json)
        #   · ฝั่ง code ไม่มี event `result` ในบันทึกเลย
        #   · ฝั่ง local มี `result` บ้างไม่มีบ้าง — ใช้ชี้ขาดไม่ได้
        #   · `status: ERROR` ในบันทึกเป็นสัญญาณระดับ **ขั้นตอน** ไม่ใช่ระดับรอบ
        #     (29 ต.ค. download-shopee-ads และ tiktok-product-daily มีขั้นที่ล้มแต่รอบนั้น
        #      ทำงานต่อจนมีผลงานออกมาจริง) จึงยกเป็น ⚠️ ไม่ใช่ ⛔ เว้นแต่ผลงานไม่ออกด้วย
        if not started and exp is not None:
            if late_min is not None and late_min > NOT_STARTED_MIN:
                r.update(level='⛔', status='ไม่เริ่ม',
                         note='เลยเวลาที่ตั้งไว้ %d นาทีแล้วยังไม่มีรอบใหม่' % late_min)
            else:
                r.update(level='⏳', status='ยังไม่ถึงรอบ / กำลังเริ่ม',
                         note='งานฝั่ง local เริ่มช้าได้ถึง ~15 นาทีเป็นปกติ')
        elif silent is not None and silent <= SILENT_MIN:
            r.update(level='⏳', status='กำลังรัน', note='เริ่มแล้ว เพิ่งมีความเคลื่อนไหว')
        elif fct.get('ended_with_text') is False:
            r.update(level='⛔', status='ค้าง',
                     note='เซสชันเงียบมา %s นาที และรอบนี้ยังไม่ได้เขียนรายงานปิดท้าย '
                          '(ค้างกลางคำสั่ง)' % silent)
        elif acfg and acfg.get('kind') == 'none':
            r.update(level='⚠️', status='ตรวจผลงานไม่ได้',
                     note=(acfg.get('note') or 'งานนี้ไม่มีผลงานปลายทางในเครื่องให้ตรวจ')[:90])
        elif acfg and age is None:
            r.update(level='⚠️', status='ตรวจผลงานไม่ได้', note=when or 'อ่านผลงานปลายทางไม่ได้')
        elif acfg and not fresh:
            r.update(level='⚠️', status='ข้อมูลค้าง',
                     note='งานรันผ่าน แต่ผลงานไม่ขยับมา %.0f ชม. (เกณฑ์ %d)' % (age, maxh))
        elif fct.get('ended_with_text') is None:
            r.update(level='⚠️', status='ตรวจไม่ได้',
                     note='อ่านบันทึกของรอบล่าสุดไม่ได้ — ไม่ยืนยันว่าปกติ')
        elif fct.get('has_error'):
            r.update(level='⚠️', status='มีขั้นที่ล้ม',
                     note='รอบล่าสุดมีขั้นที่คืน status ERROR — รอบอาจทำต่อจนจบได้ ให้เปิดดูรายงานรอบนั้น')
        else:
            r.update(level='✅', status='ปกติ',
                     note='รอบล่าสุดเริ่มตามเวลา' + (' และผลงานออกแล้ว' if acfg else ''))
        # ล้ม/ค้าง 2 รอบติดขึ้นไป → ยกขึ้นบนสุด · ดูเฉพาะรอบใน 3 วันล่าสุด
        # (กันไปนับรอบเก่าตอนงานยังปิดอยู่ แบบที่เจอกับ sales-update ฝั่ง code)
        recent = [x for x in sess_list[-6:]
                  if (_ms(x.get('createdAt')) or now) > now - timedelta(days=3)]
        if len(recent) >= 2:
            bad = 0
            for s2 in reversed(recent):
                if session_facts(s2, now).get('has_error'):
                    bad += 1
                else:
                    break
            if bad >= 2:
                if r['level'] not in ('⛔',):
                    r['level'] = '⚠️'
                r['status'] = 'ล้มติดกัน %d รอบ' % bad
                r['repeat'] = bad
                r['note'] = ('รอบล่าสุด %d รอบติดกันมีขั้นที่คืน status ERROR '
                             '— ซ้ำแบบนี้มักไม่ใช่เหตุบังเอิญ' % bad)
        # description vs cron
        if prompt_file and cron:
            okd, detail = desc_vs_cron(prompt_file, cron)
            if okd is False:
                r['desc_mismatch'] = detail
        return r

    # ฝั่ง local
    for t in (reg or []):
        if not t.get('enabled'):
            continue
        name = (t.get('filePath') or '').split('/Scheduled/')[-1].split('/')[0] or t.get('id')
        pf = None
        try:
            txt = Path(t['filePath']).read_text(encoding='utf-8', errors='replace')
            m = re.findall(r'task_prompts/([A-Za-z0-9_\-]+\.md)', txt)
            pf = m[0] if m else None
        except Exception:
            pass
        rows.append(mk(name, 'local', t.get('cronExpression', ''),
                       iso(t.get('lastRunAt')), iso(t.get('lastScheduledFor')),
                       (local_sess or {}).get(t.get('id'), []), None, pf))
    # ฝั่ง code
    for tid, c in code_cfg.items():
        sl = (code_sess or {}).get(tid, [])
        last = _ms(sl[-1].get('createdAt')) if sl else None
        rows.append(mk(c.get('label', tid), 'code', c.get('cron', ''), last, None, sl, c,
                       tid + '.md'))

    order = {'⛔': 0, '⚠️': 1, '⏳': 2, '✅': 3}
    rows.sort(key=lambda r: (order.get(r['level'], 9), r['name']))
    return rows, unreadable


def write_status_json(now, path=None):
    rows, unreadable = build_status(now)
    data = {
        'checked_at': now.strftime('%Y-%m-%d %H:%M'),
        'unreadable': unreadable,
        'thresholds': {'not_started_min': NOT_STARTED_MIN, 'silent_min': SILENT_MIN,
                       'stale_hours': STALE_HOURS},
        'counts': {'stop': sum(1 for r in rows if r['level'] == '⛔'),
                   'warn': sum(1 for r in rows if r['level'] == '⚠️'),
                   'ok': sum(1 for r in rows if r['level'] == '✅')},
        'tasks': [{k: r.get(k, '') for k in
                   ('name', 'side', 'last_round', 'level', 'status', 'data_asof',
                    'silent_min', 'note', 'desc_mismatch')} for r in rows],
    }
    p = Path(path) if path else (BASE / 'scripts' / 'ops' / 'task_health.json')
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return data, p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--grace-min', type=int, default=60,
                    help='รอบที่เลยเวลามาแล้วเกินกี่นาทีจึงถือว่า "ไม่ได้รัน"')
    ap.add_argument('--delay-min', type=int, default=20,
                    help='เริ่มช้ากว่าที่ตั้งไว้กี่นาทีจึงเตือน')
    ap.add_argument('--lock-min', type=int, default=30,
                    help='.git/*.lock ค้างเกินกี่นาทีจึงถือว่าเป็นปัญหา')
    ap.add_argument('--write-json', action='store_true',
                    help='เขียน scripts/ops/task_health.json ให้หน้า Dashboard อ่าน '
                         '(ต้องรันจากงานฝั่ง code เท่านั้น ฝั่ง local อ่านไฟล์เซสชันไม่ได้)')
    ap.add_argument('--at', help='ทดสอบย้อนหลัง: สมมุติว่าตอนนี้คือเวลานี้ YYYY-MM-DDTHH:MM '
                                '(ใช้ตรวจเหตุการณ์ที่ผ่านมาแล้ว ไม่ใช้ในงานจริง)')
    a = ap.parse_args()
    now = datetime.fromisoformat(a.at) if a.at else datetime.now()
    if a.write_json:
        data, p = write_status_json(now)
        c = data['counts']
        print(json.dumps({'status': 'WROTE', 'file': p.name, 'checked_at': data['checked_at'],
                          'counts': c, 'unreadable': data['unreadable']}, ensure_ascii=False))
        return 3 if (c['stop'] or data['unreadable']) else 0
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
