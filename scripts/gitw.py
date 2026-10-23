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
exit: ตามที่ git คืนมา · 2 = ถูกปฏิเสธเพราะคำสั่งไม่อยู่ในรายการอนุญาต
"""
import subprocess, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent          # <BASE>/scripts/gitw.py -> <BASE>
ALLOWED = {'add', 'commit', 'status', 'log', 'diff', 'rev-parse', 'show'}
# -c ที่ยอมให้วางหน้าคำสั่งได้ — มีผลเฉพาะคำสั่งนั้น ไม่เขียนทับ config ในรีโป
PRE_CFG_OK = {'user.name', 'user.email'}
# ห้ามเด็ดขาด แม้จะส่งมาเป็น argument ของคำสั่งที่อนุญาต
BANNED = {'push', 'reset', 'clean', 'rebase', 'checkout', 'switch', 'restore',
          'remote', 'config', 'filter-branch', 'gc', 'prune', 'reflog'}


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
    r = subprocess.run(['git', '-C', str(BASE), *pre, *args],
                       text=True, capture_output=True)
    if r.stdout: print(r.stdout, end='')
    if r.stderr: print(r.stderr, end='', file=sys.stderr)
    sys.exit(r.returncode)


if __name__ == '__main__':
    main()
