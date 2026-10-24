#!/usr/bin/env python3
"""bump cache version ใน sw.js — ใช้แทน sed

เหตุผล: `sed -i "s/.../"` เป็น GNU syntax · BSD sed บน macOS กิน pattern เป็น
backup suffix แล้ว error "unterminated substitute pattern" แต่สคริปต์ส่วนใหญ่
ไม่มี `set -e` และ echo ว่าสำเร็จอยู่ดี -> sw.js ไม่ถูก bump ทั้งที่ dashboard
อัปเดตแล้ว ผู้ใช้จึงเห็นข้อมูลเก่าจาก PWA cache (เกิดจริง 3 ครั้ง 19-20 ต.ค. 2569)

ใช้:  python3 scripts/bump_sw.py        -> พิมพ์ "wibwub-v1767 -> wibwub-v1768"
exit: 0 = สำเร็จ · 1 = หาเลขเวอร์ชันไม่เจอ (ไม่แตะไฟล์)
"""
import re, sys
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
SW = BASE / 'sw.js'

t = SW.read_text(encoding='utf-8')
m = re.search(r'wibwub-v(\d+)', t)
if not m:
    print('ERROR: หา wibwub-v<N> ใน sw.js ไม่เจอ — ไม่แตะไฟล์', file=sys.stderr)
    sys.exit(1)
old = int(m.group(1))
SW.write_text(re.sub(r'wibwub-v\d+', f'wibwub-v{old + 1}', t), encoding='utf-8')
# อ่านกลับมายืนยันจริง ไม่เชื่อว่าเขียนสำเร็จเฉย ๆ
got = int(re.search(r'wibwub-v(\d+)', SW.read_text(encoding='utf-8')).group(1))
if got != old + 1:
    print(f'ERROR: bump ไม่สำเร็จ (ยังเป็น v{got})', file=sys.stderr); sys.exit(1)
print(f'wibwub-v{old} -> wibwub-v{got}')
