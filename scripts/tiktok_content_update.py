#!/usr/bin/env python3
"""อัปเดต ALL_POSTS (คลิป TikTok) ใน WIBWUB_TikTok_Dashboard_v7.html + WIBWUB_Mobile.html

ใช้ process_tiktok_content() ของ wibwub_update.py — ห้าม reimplement
อ่านชีต CONTENT ผ่าน service account (ไม่ต้องใช้เบราว์เซอร์)

บั๊กที่เคยเกิดและ guard ที่กันไว้แล้ว (ดูสกิล wibwub-tiktok-social-charts-known-bugs):
  · ถ้า day/month พาร์สไม่ออกเกือบทุกแถว (ชีตเปลี่ยนโครงสร้าง) ห้ามเขียนทับ ALL_POSTS
    ไม่งั้นกราฟ Social ทุกอันจะว่างเปล่า — update_html() เช็คให้แล้วและจะข้ามรอบนั้น
  · regex ต้องแมตช์ถึง "];" ไม่ใช่ "]" ตัวแรก เพราะ content บางอันมี ']' อยู่ในสตริง

ใช้:  python3 scripts/tiktok_content_update.py [--dry-run]
exit: 0 = อัปเดตแล้ว · 10 = ไม่มีอะไรเปลี่ยน · 2 = ไม่ผ่านด่านตรวจ (ไม่เขียนไฟล์)
"""
import sys, re, json, argparse
from pathlib import Path

BASE = Path('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com'
            '/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All')
PAGES = ['WIBWUB_TikTok_Dashboard_v7.html', 'WIBWUB_Mobile.html']


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def count_posts(p):
    t = Path(p).read_text(encoding='utf-8')
    m = re.search(r'ALL_POSTS\s*=\s*\[([\s\S]*?)\]\s*;', t)
    if not m: return None
    return len(re.findall(r'\{lbl:', m.group(1)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    for p in PAGES:
        if not (BASE / p).exists(): die('ไม่พบไฟล์', p)
    before = {p: count_posts(BASE / p) for p in PAGES}

    sys.path.insert(0, str(BASE))
    try:
        import wibwub_update as W
    except Exception as e:
        die('import wibwub_update ไม่สำเร็จ', f'{type(e).__name__}: {e}')

    try:
        sheets = W.read_sheets()
    except SystemExit as e:
        die('read_sheets ออกกลางคัน (ดู stderr)', f'exit={e.code}')
    rows = sheets.get('content') or []
    if len(rows) < 20: die('ชีต CONTENT สั้นผิดปกติ — ไม่เขียนทับ', len(rows))

    posts = W.process_tiktok_content(rows)
    if not posts: die('process_tiktok_content() คืนค่าว่าง')

    # ── ด่านตรวจ ────────────────────────────────────────────────────────────
    n = len(posts)
    old = max((v for v in before.values() if v), default=0)
    if old and n < old * 0.9:
        die('จำนวนคลิปหดลงเกิน 10% — อาจอ่านชีตไม่ครบ ไม่เขียนทับ', f'{old} -> {n}')
    zero_day = sum(1 for p in posts if not (p.get('month') or 0))
    if n and zero_day / n > 0.3:
        die('คลิปที่พาร์สเดือนไม่ออกเกิน 30% — ชีตน่าจะเปลี่ยนโครงสร้าง '
            '(บั๊กที่เคยทำกราฟ Social ว่างทั้งหน้า)', f'{zero_day}/{n}')

    summary = {'posts': n, 'zero_month': zero_day, 'before': before,
               'months': sorted({p['month'] for p in posts if p.get('month')})}
    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **summary}, ensure_ascii=False)); return 0

    W.update_html(None, None, posts, None)      # เขียนเฉพาะส่วน TikTok content
    after = {p: count_posts(BASE / p) for p in PAGES}
    summary['after'] = after
    changed = after != before
    if changed: W.bump_sw()
    print(json.dumps({'status': 'UPDATED' if changed else 'NO_CHANGE', **summary}, ensure_ascii=False))
    return 0 if changed else 10


if __name__ == '__main__':
    sys.exit(main())
