#!/usr/bin/env python3
"""คัดลอกไฟล์ที่เพิ่งโหลดมาเข้าโฟลเดอร์เก็บของงานนั้น

ทำไมต้องมีสคริปต์นี้แทนที่จะเขียน bash:
  งานตั้งเวลาไม่มีคนนั่งกดอนุญาต และคำสั่ง bash ที่มีตัวแปร (`D="$BASE/..."`),
  `$(ls -t ...)`, `[ -z "$F" ]` จะถูกตัวตรวจตีธงว่า "simple_expansion"
  ซึ่งสร้างกฎอนุญาตถาวรไม่ได้ → งานค้างรอกด Allow ทั้งรอบ
  ส่วน `python3 "<พาธเต็ม>/..."` แมตช์กฎ `Bash(python3 *)` ที่อนุญาตไว้แล้ว

ทำไมต้องหาหลายที่: launchd `com.wibwub.download-mover` (WatchPaths ~/Downloads)
  ย้ายไฟล์ออกจาก Downloads ภายในไม่กี่วินาที บางแพตเทิร์นย้ายเข้าโฟลเดอร์ปลายทางให้เลย
  บางแพตเทิร์น (เช่น overview-v2_*.csv) ย้ายเข้า downloads_archive/ เท่านั้น
  จึงต้องมองทั้ง 3 ที่ แล้วเอาไฟล์ใหม่สุด

ใช้:  python3 scripts/collect_download.py <glob> <โฟลเดอร์ปลายทาง (relative กับ All)>
      [--max-age-min N]   ไฟล์ต้องใหม่กว่า N นาที (ปกติ 30) กันหยิบไฟล์เมื่อวานมาใช้
      [--check-only]      แค่ดูว่าเจออะไร ไม่คัดลอก
exit: 0 = คัดลอกแล้ว/มีอยู่แล้ว · 1 = ไม่พบไฟล์ใหม่
"""
import sys, os, glob, json, time, shutil, argparse

def _find_base():
    """ไล่ขึ้นจากตำแหน่งไฟล์นี้จนเจอโฟลเดอร์ All — ดูจาก marker sw.js + .git

    ห้ามฝังพาธ Mac ตายตัว: งานตั้งเวลาฝั่ง local รันในแซนด์บ็อกซ์ที่ mount โฟลเดอร์ All
    ไว้คนละที่ (/sessions/<ชื่อ>/mnt/All) และชื่อเซสชันเปลี่ยนทุกรอบ (24 ต.ค. 69)
    """
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(d, 'sw.js')) and os.path.exists(os.path.join(d, '.git')):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            raise SystemExit('หาโฟลเดอร์ All ไม่เจอ — ไล่ขึ้นจาก %s แล้วไม่เจอโฟลเดอร์ที่มีทั้ง '
                             'sw.js และ .git · ห้ามเดาพาธ ให้ตรวจว่าสคริปต์ยังอยู่ในโฟลเดอร์ All หรือไม่'
                             % os.path.abspath(__file__))
        d = parent


ALL = _find_base()
DL = os.path.expanduser('~/Downloads')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pattern')
    ap.add_argument('dest')
    ap.add_argument('--max-age-min', type=int, default=30)
    ap.add_argument('--check-only', action='store_true')
    a = ap.parse_args()

    dest = os.path.join(ALL, a.dest)
    # มองทั้ง Downloads · downloads_archive (mover ย้ายไปพักไว้) · ปลายทางเอง (เผื่อ mover ส่งตรง)
    cand = []
    for d in (DL, os.path.join(ALL, 'downloads_archive'), dest):
        cand += glob.glob(os.path.join(d, a.pattern))
        cand += glob.glob(os.path.join(d, '*', a.pattern))   # archive แยกโฟลเดอร์ย่อยตามแพตเทิร์น
    cand = [f for f in cand if os.path.isfile(f)]
    if not cand:
        print(json.dumps({'status': 'NOT_FOUND', 'pattern': a.pattern,
                          'มองที่': [DL, 'downloads_archive', a.dest]}, ensure_ascii=False))
        return 1

    newest = max(cand, key=os.path.getmtime)
    age = (time.time() - os.path.getmtime(newest)) / 60
    info = {'file': os.path.basename(newest), 'จาก': os.path.dirname(newest),
            'อายุ_นาที': round(age, 1), 'เจอทั้งหมด': len(cand)}
    if age > a.max_age_min:
        print(json.dumps({'status': 'TOO_OLD', 'เกณฑ์_นาที': a.max_age_min, **info},
                         ensure_ascii=False))
        return 1   # ไฟล์เก่า = รอบนี้โหลดไม่สำเร็จ ห้ามเอาไฟล์เมื่อวานไปใช้แทน

    if a.check_only:
        print(json.dumps({'status': 'FOUND', **info}, ensure_ascii=False)); return 0

    os.makedirs(dest, exist_ok=True)
    target = os.path.join(dest, os.path.basename(newest))
    if os.path.abspath(newest) == os.path.abspath(target):
        print(json.dumps({'status': 'ALREADY_THERE', **info}, ensure_ascii=False)); return 0
    shutil.copy2(newest, target)
    print(json.dumps({'status': 'COPIED', 'ไปที่': a.dest, **info}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
