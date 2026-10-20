#!/usr/bin/env python3
"""อัปเดต SALES arrays (Shopee / TikTok / Lazada) ใน WIBWUB_Dashboard.html + WIBWUB_Mobile.html

ใช้ process_sales() ของ wibwub_update.py เป็นตัวคำนวณ — ห้าม reimplement
เพราะตัวจริงมีด่านกันข้อมูลหายที่เขียนเองแล้วมักลืม:
  · months_shrunk  — ถ้ารอบนี้ได้เดือนน้อยกว่าเดิม ให้ข้ามทั้งไฟล์ (เคยเกิดจริง)
  · per-array length guard
  · zero-merge guard — ถ้าค่าใหม่เป็น 0 แต่ค่าเดิมไม่ใช่ 0 ให้คงค่าเดิมไว้
    (กัน fetch ล้มบางส่วนแล้วเขียน 0 ทับยอดจริง)

สิ่งที่ "ห้ามแตะ" และสคริปต์นี้ไม่แตะ:
  · TOTAL_REV / TOTAL_ORD — เป็น derived const ใน JS ไม่ใช่ data array
    (Dashboard รวม 6 ช่องทาง SH+TK+LZ+FB+LINE+WEB · Mobile รวม 10 ช่องทาง)
    ถ้าเขียนทับเป็น literal array ยอดจะหายและสูตรจะพังถาวร
  · MP_DATE_MAX / MP_MONTH_BOUNDS — หน้าเว็บคำนวณเองจาก MTD_COVERAGE แล้ว

ใช้:  python3 scripts/sales_update.py [--dry-run]
exit: 0 = อัปเดตแล้ว · 10 = ไม่มีอะไรเปลี่ยน · 2 = ไม่ผ่านด่านตรวจ (ไม่เขียนไฟล์)
"""
import sys, json, argparse, re
from pathlib import Path

BASE = Path('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com'
            '/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All')
PAGES = ['WIBWUB_Dashboard.html', 'WIBWUB_Mobile.html']
# อาเรย์ที่ process_sales() คืนมาและ update_html() เขียน
WATCH = ['SH_REV', 'TK_REV', 'LZ_REV', 'SH_ORD', 'TK_ORD', 'LZ_ORD']


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def arrays(path):
    """อ่านค่าอาเรย์ปัจจุบันจากหน้าเว็บ เพื่อเทียบก่อน/หลัง"""
    t = Path(path).read_text(encoding='utf-8')
    out = {}
    for k in WATCH:
        m = re.search(r'const\s+' + k + r'\s*=\s*\[([^\]]*)\]', t)
        if m:
            try: out[k] = [float(x) for x in m.group(1).split(',') if x.strip()]
            except ValueError: pass
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true', help='คำนวณและตรวจอย่างเดียว ไม่เขียนไฟล์')
    a = ap.parse_args()

    if not BASE.exists(): die('BASE ไม่พบ — Google Drive ยังไม่ sync?', str(BASE))
    for p in PAGES:
        if not (BASE / p).exists(): die('ไม่พบไฟล์', p)

    sys.path.insert(0, str(BASE))
    try:
        import wibwub_update as W
    except Exception as e:
        die('import wibwub_update ไม่สำเร็จ', f'{type(e).__name__}: {e}')

    before = {p: arrays(BASE / p) for p in PAGES}

    try:
        sheets = W.read_sheets()
        sales = W.process_sales(sheets)
    except SystemExit as e:
        die('read_sheets/process_sales ออกกลางคัน (ดู stderr ด้านบน)', f'exit={e.code}')
    except Exception as e:
        die('process_sales ล้มเหลว', f'{type(e).__name__}: {e}')
    if not sales: die('process_sales() คืนค่าว่าง')

    # ── ด่านตรวจก่อนเขียน ────────────────────────────────────────────────────
    n = {k: len(v) for k, v in sales.items() if isinstance(v, list)}
    if not n: die('ไม่มีอาเรย์ใน sales')
    months = max(n.values())
    if months < 1 or months > 12: die('จำนวนเดือนผิดปกติ', months)
    prev_months = max((len(v) for v in before[PAGES[0]].values()), default=0)
    if prev_months and months < prev_months:
        die('เดือนหดลง — อาจดึงชีตไม่ครบ ไม่เขียนทับ', f'{prev_months} -> {months}')
    for k in ('SH_REV', 'TK_REV'):
        v = sales.get(k) or []
        if not v or all((x or 0) == 0 for x in v): die(f'{k} เป็น 0 ทั้งหมด', v[:3])
    # ยอดเดือนล่าสุดต้องไม่ลดลงจากที่อยู่ในหน้า (ยอดสะสมรายเดือนมีแต่เพิ่ม)
    drops = []
    for k in WATCH:
        old, new = before[PAGES[0]].get(k), sales.get(k)
        if old and new and len(new) >= len(old):
            for i, o in enumerate(old):
                # ค่าใหม่เป็น 0 = ชีตยังไม่กรอก -> zero-merge guard ใน update_html คงค่าเดิมไว้ ไม่ใช่ข้อมูลหาย
                if o and new[i] and new[i] < o * 0.98:
                    drops.append(f'{k}[{i}] {o} -> {new[i]}')
    if drops: die('ค่าลดลงผิดปกติ (ยอดสะสมไม่ควรลด) — ไม่เขียนทับ', drops[:8])

    summary = {'months': months, 'arrays': n,
               'latest': {k: (sales.get(k) or [None])[-1] for k in WATCH if sales.get(k)}}

    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **summary}, ensure_ascii=False))
        return 0

    W.update_html(sales, None, None, None)      # เขียนเฉพาะส่วน sales (ส่วนอื่นเป็น None จึงถูกข้าม)

    # ── ช่องทาง Shipnity (FB/LINE/CARE/...) ให้สดพร้อมกับ sales ทุกรอบ ──────
    # ไม่งั้นกลางสัปดาห์ยอดรวมจะเอียง: SH/TK/LZ เดินหน้าวันละ 2 รอบ แต่ช่องทางอื่น
    # อัปเดตแค่วันจันทร์ · ใช้ cache จึงไม่ช้า (รอบที่ไม่มีไฟล์ Shipnity ใหม่ <1 วิ)
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from ship_cache import load_shipnity
        import shipnity_update as S
        raw = load_shipnity()
        if raw:
            asof = S._asof((BASE / PAGES[0]).read_text(encoding='utf-8'))
            S.write_channels(raw, asof)
            S.write_coverage(raw, asof)
            summary['channels_asof'] = asof
    except Exception as e:                   # ช่องทางล้มต้องไม่ทำให้ sales ล้มด้วย
        summary['channels_error'] = f'{type(e).__name__}: {e}'

    after = {p: arrays(BASE / p) for p in PAGES}
    changed = after != before
    if changed: W.bump_sw()
    summary['changed_files'] = [p for p in PAGES if after[p] != before[p]]
    print(json.dumps({'status': 'UPDATED' if changed else 'NO_CHANGE', **summary}, ensure_ascii=False))
    return 0 if changed else 10


if __name__ == '__main__':
    sys.exit(main())
