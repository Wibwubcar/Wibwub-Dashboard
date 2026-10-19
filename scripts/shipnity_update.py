#!/usr/bin/env python3
"""อัปเดต Data Shipnity/Sales_Dashboard.html จาก Excel ใน Data Shipnity/

ใช้ process_shipnity() ของ wibwub_update.py เป็นตัวคำนวณ — ห้าม reimplement
เพราะไฟล์ใน Data Shipnity/ เป็น cumulative snapshot รายวันที่ซ้อนทับกัน
ต้อง dedup ด้วย (order_id, ชื่อสินค้า) ไม่งั้นนับซ้ำหลายสิบรอบ
และ RAW ต้องมี channels / products / order_counts ครบตามที่ JS ในหน้าเว็บอ้าง

ใช้:  python3 scripts/shipnity_update.py [--dry-run]
exit: 0 = อัปเดตแล้ว · 10 = ไม่มีอะไรเปลี่ยน · 2 = ข้อมูลไม่ผ่านด่านตรวจ (ไม่เขียนไฟล์)
"""
import sys, json, argparse
from pathlib import Path

BASE = Path('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com'
            '/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All')
PAGE = BASE / 'Data Shipnity' / 'Sales_Dashboard.html'

# คีย์ที่ JS ในหน้าเว็บอ้างผ่าน RAW.* — ขาดตัวใดตัวหนึ่งหน้าเว็บพังทันที
REQUIRED = {'date_min', 'date_max', 'channels', 'products', 'lines', 'order_counts'}


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true', help='คำนวณและตรวจอย่างเดียว ไม่เขียนไฟล์')
    a = ap.parse_args()

    if not BASE.exists():       die('BASE ไม่พบ — Google Drive ยังไม่ sync?', str(BASE))
    if not PAGE.exists():       die('ไม่พบ Sales_Dashboard.html', str(PAGE))

    sys.path.insert(0, str(BASE))
    try:
        import wibwub_update as W
    except Exception as e:
        die('import wibwub_update ไม่สำเร็จ', f'{type(e).__name__}: {e}')

    raw = W.process_shipnity()
    if not raw:
        die('process_shipnity() คืน None — ดู stderr ด้านบน')

    # ── ด่านตรวจ: ยอมให้พังดีกว่าเขียนข้อมูลเสียทับ dashboard ───────────────
    missing = REQUIRED - set(raw)
    if missing:                 die('RAW ขาดคีย์ที่ JS ต้องใช้', sorted(missing))

    n_lines, n_oc = len(raw['lines']), len(raw['order_counts'])
    if n_lines == 0:            die('lines ว่าง')
    if n_lines > 500_000:       die('lines เยอะผิดปกติ — น่าจะ dedup ไม่ทำงาน', n_lines)
    if not raw['date_min'] or raw['date_min'] < '2020-01-01':
        die('date_min เพี้ยน (น่าจะมี date cell เสียหลุดเข้ามา)', raw['date_min'])
    if raw['date_max'] < raw['date_min']:
        die('date_max < date_min', [raw['date_min'], raw['date_max']])

    prev = PAGE.read_text(encoding='utf-8')
    size_mb = round(len(json.dumps(raw, ensure_ascii=False, separators=(',', ':'))) / 1e6, 2)
    if size_mb > 20:            die('RAW ใหญ่ผิดปกติ — ไม่เขียนทับ', f'{size_mb} MB')

    summary = {'lines': n_lines, 'order_counts': n_oc, 'products': len(raw['products']),
               'channels': len(raw['channels']), 'date_min': raw['date_min'],
               'date_max': raw['date_max'], 'raw_mb': size_mb,
               'page_mb_before': round(len(prev) / 1e6, 2)}

    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **summary}, ensure_ascii=False))
        return 0

    changed = W.update_html(None, None, None, raw) or PAGE.read_text(encoding='utf-8') != prev
    if changed:
        W.bump_sw()
    summary['page_mb_after'] = round(len(PAGE.read_text(encoding='utf-8')) / 1e6, 2)
    print(json.dumps({'status': 'UPDATED' if changed else 'NO_CHANGE', **summary}, ensure_ascii=False))
    return 0 if changed else 10


if __name__ == '__main__':
    sys.exit(main())
