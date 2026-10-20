#!/usr/bin/env python3
"""cache ผลของ process_shipnity() — อ่าน Excel 161 ไฟล์ใช้เวลา ~2 นาที

ใช้เมื่อหลายงานต้องการข้อมูล Shipnity ชุดเดียวกันในวันเดียวกัน
(shipnity-monday, products, และ sales-update ที่เรียกส่วนช่องทางรายวัน)

cache key = ชื่อไฟล์ + mtime + size ของ **ทุกไฟล์** ใน Data Shipnity/*.xlsx
ไฟล์ใหม่เข้าวันละ ~2 รอบ (คน export เอง) รอบที่ไม่มีไฟล์ใหม่จะได้ cache ทันที
ถ้ามีไฟล์ใหม่แม้ไฟล์เดียว key เปลี่ยน -> คำนวณใหม่ทั้งชุด (ถูกต้องเสมอ)

ใช้ในโค้ด:  from ship_cache import load_shipnity;  raw = load_shipnity()
CLI:        python3 scripts/ship_cache.py [--refresh]   (อุ่น cache ไว้ล่วงหน้า)
"""
import sys, json, hashlib, glob, os
from pathlib import Path

BASE = Path('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com'
            '/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All')
CACHE = Path.home() / 'Library' / 'Caches' / 'wibwub-outputs' / 'shipnity_cache.json'


def sales_asof():
    """วันสุดท้ายที่ฝั่ง Sales (Shopee/TikTok/Lazada) ครอบถึง

    SALES_ASOF อยู่ใน WIBWUB_Mobile.html (ไม่ใช่ Dashboard — เคยหาผิดไฟล์มาแล้ว)
    สำรอง: ค่าสูงสุดใน MTD_COVERAGE ของ Dashboard
    """
    import re
    m = re.search(r"SALES_ASOF\s*=\s*'(\d{4}-\d{2}-\d{2})'",
                  (BASE / 'WIBWUB_Mobile.html').read_text(encoding='utf-8'))
    if m: return m.group(1)
    m = re.search(r'const MTD_COVERAGE\s*=\s*\{([^}]*)\}',
                  (BASE / 'WIBWUB_Dashboard.html').read_text(encoding='utf-8'))
    if m:
        ds = re.findall(r"'(\d{4}-\d{2}-\d{2})'", m.group(1))
        if ds: return max(ds)
    return None


def fingerprint():
    """ลายนิ้วมือของทุกไฟล์ใน Data Shipnity — เปลี่ยนเมื่อมีไฟล์เพิ่ม/แก้/ลบ"""
    files = sorted(f for f in glob.glob(str(BASE / 'Data Shipnity' / '*.xlsx'))
                   if not os.path.basename(f).startswith('~'))
    h = hashlib.sha256()
    for f in files:
        st = os.stat(f)
        h.update(f'{os.path.basename(f)}|{int(st.st_mtime)}|{st.st_size}\n'.encode())
    return h.hexdigest(), len(files)


def load_shipnity(refresh=False, verbose=False):
    fp, n = fingerprint()
    if not refresh and CACHE.exists():
        try:
            c = json.loads(CACHE.read_text(encoding='utf-8'))
            if c.get('fingerprint') == fp:
                if verbose: print(f'cache hit ({n} ไฟล์)', file=sys.stderr)
                return c['raw']
        except Exception:
            pass                      # cache เสีย -> คำนวณใหม่
    sys.path.insert(0, str(BASE))
    import wibwub_update as W
    raw = W.process_shipnity()
    if not raw: return None
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    tmp = CACHE.with_suffix('.tmp')
    tmp.write_text(json.dumps({'fingerprint': fp, 'files': n, 'raw': raw},
                              ensure_ascii=False), encoding='utf-8')
    tmp.replace(CACHE)
    if verbose: print(f'cache miss -> คำนวณใหม่ ({n} ไฟล์)', file=sys.stderr)
    return raw


if __name__ == '__main__':
    import time
    t = time.time()
    raw = load_shipnity(refresh='--refresh' in sys.argv, verbose=True)
    fp, n = fingerprint()
    print(json.dumps({'status': 'OK' if raw else 'ERROR', 'files': n,
                      'date_min': raw and raw['date_min'], 'date_max': raw and raw['date_max'],
                      'lines': raw and len(raw['lines']), 'secs': round(time.time() - t, 1),
                      'cache': str(CACHE)}, ensure_ascii=False))
