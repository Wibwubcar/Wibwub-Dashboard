#!/usr/bin/env python3
"""รอไฟล์ออเดอร์ Shipnity ที่ export สดในรอบนี้

ใช้ใน wibwub-daily-stock หลังสั่ง "ส่งออกข้อมูล" บนหน้า Shipnity แล้ว
ไฟล์ ~34 MB ใช้เวลาสร้างราว 10 นาที แล้ว download-mover ย้ายเข้า
Data Shipnity/ ให้เองภายใน 5 วินาที

ทำไมไม่ใช้ find
  find บนเครื่องนี้คือ bfs ซึ่งไม่รับ -newermt "today" (Invalid timestamp)
  และ zsh nomatch ทำให้ ls กับ glob ที่ไม่แมตช์ล้มทั้งคำสั่ง

ทำไมตัดสินจาก mtime ไม่ใช่ชื่อไฟล์
  รอบ 19:00 จะได้ชื่อซ้ำกับรอบเช้า download-mover จึงต่อ __<stamp> ให้
  (safe_mv ใน scripts/wibwub_auto_move.sh — ไม่เขียนทับ)
  ถ้าเช็คแค่ว่า "มีไฟล์ Data_<วันนี้>" รอบเย็นจะผ่านทันทีเพราะไฟล์เช้ายังอยู่
  แล้วเราจะไม่รู้เลยว่า export รอบเย็นล้ม

exit code
  0  เจอไฟล์สด        -> รัน update_stock.py ต่อได้เลย
  3  ครบเวลาแล้วไม่มา  -> ไม่ใช่ error ให้รัน update_stock.py ด้วยไฟล์เดิมต่อ
                         (STOCK_DATA_WARN จะขึ้นป้ายเตือนเอง) แล้วรายงาน
                         "⚠️ export ไม่สำเร็จ" ห้ามข้ามรอบ
  2  หาโฟลเดอร์ All ไม่เจอ
"""
import argparse, glob, json, os, sys, time
from datetime import datetime
from pathlib import Path

PATTERN = "Data_[0-9][0-9]-[0-9][0-9]-*.xlsx"   # ห้ามกว้างกว่านี้ Data-Page-1_* คือไฟล์หลอก 500 แถว


def _find_base():
    p = Path(__file__).resolve()
    for d in (p, *p.parents):
        if (d / 'sw.js').is_file() and (d / '.git').exists():
            return d
    raise SystemExit(f'หาโฟลเดอร์ All ไม่เจอ — ไล่ขึ้นจาก {p} แล้วไม่พบโฟลเดอร์ที่มีทั้ง sw.js และ .git')


def newest_fresh(d, fresh_sec):
    now = time.time()
    best = None
    for f in glob.glob(os.path.join(d, PATTERN)):
        try:
            m = os.path.getmtime(f)
        except OSError:
            continue
        if now - m <= fresh_sec and (best is None or m > best[0]):
            best = (m, f)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-wait-min', type=float, default=20.0,
                    help='รอสูงสุดกี่นาที (ค่าเริ่มต้น 20)')
    ap.add_argument('--fresh-min', type=float, default=35.0,
                    help='ถือว่า "สด" ถ้า mtime ใหม่กว่านี้กี่นาที (ค่าเริ่มต้น 35)')
    ap.add_argument('--poll-sec', type=float, default=30.0)
    a = ap.parse_args()

    try:
        base = _find_base()
    except SystemExit as e:
        print(json.dumps({"status": "NO_BASE", "msg": str(e)}, ensure_ascii=False))
        return 2

    d = base / "Data Shipnity"
    fresh_sec = a.fresh_min * 60
    deadline = time.time() + a.max_wait_min * 60
    t0 = time.time()

    while True:
        hit = newest_fresh(str(d), fresh_sec)
        if hit:
            m, f = hit
            print(json.dumps({
                "status": "FOUND",
                "file": os.path.basename(f),
                "mtime": datetime.fromtimestamp(m).strftime("%Y-%m-%d %H:%M:%S"),
                "size_mb": round(os.path.getsize(f) / 1048576, 2),
                "waited_min": round((time.time() - t0) / 60, 1),
            }, ensure_ascii=False))
            return 0
        if time.time() >= deadline:
            break
        time.sleep(min(a.poll_sec, max(1.0, deadline - time.time())))

    allf = sorted(glob.glob(os.path.join(str(d), PATTERN)), key=os.path.getmtime)
    last = os.path.basename(allf[-1]) if allf else None
    last_m = (datetime.fromtimestamp(os.path.getmtime(allf[-1])).strftime("%Y-%m-%d %H:%M:%S")
              if allf else None)
    print(json.dumps({
        "status": "TIMEOUT",
        "waited_min": round((time.time() - t0) / 60, 1),
        "newest_on_disk": last,
        "newest_mtime": last_m,
        "msg": "ไม่มีไฟล์ export สดเข้ามา — ให้รัน update_stock.py ด้วยไฟล์เดิมต่อ "
               "แล้วรายงาน ⚠️ export ไม่สำเร็จ ห้ามข้ามรอบ",
    }, ensure_ascii=False))
    return 3


if __name__ == "__main__":
    sys.exit(main())
