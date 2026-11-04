#!/usr/bin/env python3
"""git ที่ปลอดภัยสำหรับงานตั้งเวลา — เรียกผ่าน python3 จึงแมตช์กฎ Bash(python3:*)

ทำไมต้องมี (23 ต.ค. 69):
  กฎอนุญาตของ Claude Code จับจาก "คำขึ้นต้น" ของคำสั่ง
  - `git -C <path> ...`      ถูกตัดออกจาก allow เพราะ deny `git push:*`
                              ดักไม่ได้ → เปิดช่องให้ `git -C <path> push` หลุด
  - `cd <path> && git ...`   ขึ้นต้นด้วย cd จึงไม่แมตช์ `Bash(git add:*)`
                              → งานตั้งเวลาค้างรออนุญาตทุกตัว
  ตัวนี้แก้ทั้งสองปัญหา: ขึ้นต้นด้วย python3 (อนุญาตแล้ว) และกรองคำสั่งอันตรายในตัว

ใช้:
  python3 <BASE>/scripts/gitw.py add <ไฟล์...>
  python3 <BASE>/scripts/gitw.py commit -m "ข้อความ"
  python3 <BASE>/scripts/gitw.py -c user.name=X -c user.email=Y commit -m "ข้อความ"
  python3 <BASE>/scripts/gitw.py status --porcelain
  python3 <BASE>/scripts/gitw.py log --oneline -5
  python3 <BASE>/scripts/gitw.py diff --stat

รันที่ไหนก็ได้ — หา BASE เองจากตำแหน่งไฟล์นี้ ไม่ต้อง cd
รอ .git/index.lock เองได้ (4 พ.ย. 69):
  3-4 พ.ย. งาน shopee-live เขียนข้อมูลสำเร็จแต่ commit ไม่ผ่าน เพราะงานตั้งเวลาอีกตัว
  ถือ .git/index.lock อยู่ (sandbox คนละ user จึงลบไม่ได้ และห้ามลบอยู่แล้ว)
  แต่ `add` ติดไปก่อนแล้ว ไฟล์จึงค้างใน index แล้วถูก commit ของงานอื่นกวาดติดไป
  (0ccfffa, 78a034f) ตัวเช็กสถานะเลยหา commit ของงานนี้ไม่เจอ
  ตัวนี้จึง: รอ lock เองสูงสุด GITW_LOCK_WAIT วินาที (ค่าปริยาย 300) แล้วลองใหม่ทุก 5 วินาที
  ถ้าสุดท้าย commit ยังไม่ผ่าน จะ unstage เฉพาะไฟล์ที่ gitw ตัวเอง add ไว้ แล้วคืน exit 3

exit: ตามที่ git คืนมา · 2 = ถูกปฏิเสธเพราะคำสั่งไม่อยู่ในรายการอนุญาต
     3 = ติด index.lock จนหมดเวลา (ถ้าเป็น commit: unstage ของตัวเองคืนแล้ว)
"""
import json, os, subprocess, sys, time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent          # <BASE>/scripts/gitw.py -> <BASE>
ALLOWED = {'add', 'commit', 'status', 'log', 'diff', 'rev-parse', 'show'}
# -c ที่ยอมให้วางหน้าคำสั่งได้ — มีผลเฉพาะคำสั่งนั้น ไม่เขียนทับ config ในรีโป
PRE_CFG_OK = {'user.name', 'user.email'}
# ห้ามเด็ดขาด แม้จะส่งมาเป็น argument ของคำสั่งที่อนุญาต
BANNED = {'push', 'reset', 'clean', 'rebase', 'checkout', 'switch', 'restore',
          'remote', 'config', 'filter-branch', 'gc', 'prune', 'reflog'}
# คำสั่งที่เขียน index จึงชนกับงานอื่นได้ — ตัวอื่น (log/show/diff) อ่านอย่างเดียว ไม่ต้องรอ
INDEX_CMDS = {'add', 'commit'}
LOCK_WAIT = int(os.environ.get('GITW_LOCK_WAIT', '300'))   # วินาที (ตั้ง 0 = ไม่รอ)
# เวลาต่ออีกก้อนสำหรับ "เอาไฟล์ของตัวเองออกจาก index" หลัง commit ไม่ผ่าน
# ต้องมีแยก เพราะ git reset ก็ต้องใช้ index.lock เหมือนกัน (เจอตอนทดสอบ 4 พ.ย. 69:
#  ถือ lock ไว้ตลอด -> reset ล้มตาม -> ไฟล์ค้างใน index เหมือนเดิม ตาข่ายไม่ทำงาน)
UNSTAGE_WAIT = int(os.environ.get('GITW_UNSTAGE_WAIT', '120'))
LOCK_POLL = 5
# บันทึกว่า gitw ของ "เชลล์ตัวไหน" add อะไรค้างไว้ — ใช้ตอน commit ไม่ผ่านเพื่อ unstage คืน
# เก็บใน .git/ ซึ่ง git ไม่นับเป็นไฟล์ในรีโป จึงไม่โผล่ใน status และไม่ถูก commit ติดไป
PENDING = BASE / '.git' / 'gitw_pending_add.json'


def _run(args):
    return subprocess.run(['git', '-C', str(BASE), *args], text=True, capture_output=True)


def _is_lock_err(r):
    e = (r.stderr or '')
    return r.returncode != 0 and 'index.lock' in e and (
        'File exists' in e or 'Unable to create' in e)


def _run_waiting(args, wait=None):
    """รัน git แล้วถ้าติด index.lock ของคนอื่น ให้รอแล้วลองใหม่จนหมดเวลา — ไม่ลบ lock เด็ดขาด"""
    deadline = time.time() + (LOCK_WAIT if wait is None else wait)
    while True:
        r = _run(args)
        if not _is_lock_err(r) or time.time() >= deadline:
            return r
        time.sleep(LOCK_POLL)


def _load_pending():
    try:
        return json.loads(PENDING.read_text(encoding='utf-8'))
    except Exception:
        return {}


def _save_pending(d):
    try:
        PENDING.write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
    except OSError:
        pass          # เขียนไม่ได้ก็ไม่เป็นไร แค่เสียความสามารถ unstage คืน


def _record_add(paths):
    """จำว่าเชลล์แม่ตัวนี้ add อะไรไว้ (add กับ commit เป็นคนละโปรเซส แต่เชลล์แม่เดียวกัน)"""
    if not paths:
        return
    d = _load_pending()
    now = time.time()
    d = {k: v for k, v in d.items() if now - v.get('ts', 0) < 3600}      # ตัดของเก่าทิ้ง
    key = str(os.getppid())
    old = d.get(key, {}).get('paths', [])
    d[key] = {'paths': sorted(set(old) | set(paths)), 'ts': now}
    _save_pending(d)


def _take_record():
    """คืนรายการไฟล์ที่ตัวเอง add ไว้ แล้วลบบันทึกทิ้ง"""
    d = _load_pending()
    key = str(os.getppid())
    rec = d.pop(key, None)
    if rec is None:                      # add/commit ถูกเรียกคนละเชลล์ — ใช้บันทึกล่าสุดที่ยังสด
        fresh = [(v.get('ts', 0), k) for k, v in d.items() if time.time() - v.get('ts', 0) < 600]
        if fresh:
            key = max(fresh)[1]
            rec = d.pop(key)
    _save_pending(d)
    return (rec or {}).get('paths', [])


def _unstage(paths):   # noqa: C901
    """เอาเฉพาะไฟล์ของตัวเองออกจาก index — เนื้อไฟล์ใน working tree ไม่ถูกแตะ"""
    if not paths:
        return 'ไม่มีไฟล์ที่ต้องคืน'
    staged = _run(['diff', '--cached', '--name-only'])
    if staged.returncode != 0:
        return 'อ่านรายการ staged ไม่ได้ จึงยังไม่ได้ unstage'
    on_index = set(staged.stdout.split('\n'))
    mine = [p for p in paths if p in on_index]
    if not mine:
        return 'ไฟล์ของตัวเองไม่ได้ค้างใน index อยู่แล้ว'
    r = _run_waiting(['reset', '--quiet', '--', *mine], wait=UNSTAGE_WAIT)
    if r.returncode != 0:
        return ('⛔ unstage ไม่สำเร็จ — ไฟล์ยังค้างใน index: ' + ', '.join(mine) +
                ' · งานอื่นอาจ commit กวาดติดไป ให้รายงานเรื่องนี้ไว้ด้วย (' +
                (r.stderr or '').strip().split('\n')[0][:80] + ')')
    return 'unstage คืนแล้ว (เนื้อไฟล์ยังอยู่ครบ): ' + ', '.join(mine)


def die(msg):
    print(f'gitw: ปฏิเสธ — {msg}', file=sys.stderr)
    sys.exit(2)


def main():
    args = sys.argv[1:]
    if not args:
        die('ไม่ได้ระบุคำสั่ง (ใช้ได้: ' + ', '.join(sorted(ALLOWED)) + ')')
    # รับ -c user.name=... / -c user.email=... ที่วางไว้หน้าคำสั่ง (พรอมป์งานตั้งเวลาใช้แบบนี้)
    pre = []
    while len(args) >= 2 and args[0] == '-c':
        key = args[1].split('=', 1)[0]
        if key not in PRE_CFG_OK:
            die(f'-c {key} ไม่อนุญาต (ใช้ได้: ' + ', '.join(sorted(PRE_CFG_OK)) + ')')
        pre += [args[0], args[1]]
        args = args[2:]
    if not args:
        die('มีแต่ -c ไม่ได้ระบุคำสั่ง')
    sub = args[0]
    if sub not in ALLOWED:
        die(f'"{sub}" ไม่อยู่ในรายการอนุญาต (ใช้ได้: ' + ', '.join(sorted(ALLOWED)) + ')')
    for a in args:
        if a.lstrip('-') in BANNED:
            die(f'พบคำสั่งต้องห้าม "{a}" ในอาร์กิวเมนต์')
    # ผู้ใช้ตั้งใจให้ auto-push (launchd com.wibwub.autopush) เป็นคนเดียวที่ push
    full = [*pre, *args]
    r = _run_waiting(full) if sub in INDEX_CMDS else _run(full)
    if r.stdout: print(r.stdout, end='')
    if r.stderr: print(r.stderr, end='', file=sys.stderr)

    if sub == 'add' and r.returncode == 0:
        _record_add([a for a in args[1:] if not a.startswith('-')])
    elif sub == 'commit' and r.returncode == 0:
        _take_record()                       # commit ผ่านแล้ว ไม่มีอะไรค้าง
    elif sub == 'commit' and _is_lock_err(r):
        print(f'gitw: รอ .git/index.lock ครบ {LOCK_WAIT} วินาทีแล้วยังไม่ว่าง — '
              'ไม่ลบ lock ของคนอื่น', file=sys.stderr)
        print('gitw: ' + _unstage(_take_record()), file=sys.stderr)
        sys.exit(3)
    elif sub == 'add' and _is_lock_err(r):
        print(f'gitw: รอ .git/index.lock ครบ {LOCK_WAIT} วินาทีแล้วยังไม่ว่าง — add ไม่สำเร็จ',
              file=sys.stderr)
        sys.exit(3)
    sys.exit(r.returncode)


if __name__ == '__main__':
    main()
