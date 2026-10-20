#!/usr/bin/env python3
"""อัปเดตข้อมูล Affiliate ใน WIBWUB_Affiliate_Dashboard.html + WIBWUB_Mobile.html

ใช้ process_affiliate() ของ wibwub_update.py เป็นตัวคำนวณ — ห้าม reimplement

เหตุผล (บั๊กที่ task prompt เก่าทำไว้ และ process_affiliate แก้ไปแล้ว):
  · ไฟล์ใน Data Affiliate/ มี 2 รูปแบบที่ "ตำแหน่งคอลัมน์ไม่เหมือนกัน"
      Creator_List_*            : returns = col21, commission = col7
      Transaction_Analysis_*    : returns = col4,  commission = col21
    พรอมป์เก่า hardcode col 1/2/10 ให้ทั้งสองแบบ -> commission กลายเป็นจำนวนโชว์เคส
    (เลขหลักหน่วย) และ net สูงกว่า gmv หรือติดลบ · ตัวจริงใช้ find_col() จับจากชื่อ header
  · ต้องกรองเฉพาะไฟล์ที่ชื่อมี 'Creator_List' — โฟลเดอร์มี Product_List / Video_List /
    Live_List / Core_Metrics / WIBWUB_KOL_Tracker ปนอยู่ ถ้า glob *.xlsx จะอ่านผิดไฟล์
  · ต้องเลือกไฟล์ตามช่วงวันที่ในชื่อไฟล์ (overlap กับเดือนมากสุด) ไม่ใช่ mtime ใหม่สุด
    ไม่งั้นไฟล์เดือน ส.ค. ที่เพิ่งโหลดจะไปลงช่อง ต.ค.

ใช้:  python3 scripts/affiliate_update.py [--dry-run]
exit: 0 = อัปเดตแล้ว · 10 = ไม่มีอะไรเปลี่ยน · 2 = ไม่ผ่านด่านตรวจ (ไม่เขียนไฟล์)
"""
import sys, json, argparse, re
from pathlib import Path

BASE = Path('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com'
            '/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All')
AFF = BASE / 'WIBWUB_Affiliate_Dashboard.html'
MOB = BASE / 'WIBWUB_Mobile.html'
# ชื่ออาเรย์ที่ต้องตรงกันระหว่าง 2 หน้า (Affiliate Dashboard -> Mobile)
PAIRS = [('AF_GMV', 'AFI_GMV'), ('AF_NET', 'AFI_NET'), ('AF_COM', 'AFI_COMM')]


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def arr(path, name):
    m = re.search(r'const\s+' + name + r'\s*=\s*\[([^\]]*)\]', Path(path).read_text(encoding='utf-8'))
    if not m: return None
    try: return [float(x) for x in m.group(1).split(',') if x.strip()]
    except ValueError: return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    for p in (AFF, MOB):
        if not p.exists(): die('ไม่พบไฟล์', p.name)
    sys.path.insert(0, str(BASE))
    try:
        import wibwub_update as W
    except Exception as e:
        die('import wibwub_update ไม่สำเร็จ', f'{type(e).__name__}: {e}')

    before = {k: arr(AFF, k) for k, _ in PAIRS}
    before['AF_CR'] = arr(AFF, 'AF_CR')

    try:
        aff = W.process_affiliate()
    except SystemExit as e:
        die('process_affiliate ออกกลางคัน', f'exit={e.code}')
    except Exception as e:
        die('process_affiliate ล้มเหลว', f'{type(e).__name__}: {e}')
    if not aff: die('process_affiliate() คืนค่าว่าง (ดู stderr)')

    gmv, net, com, cr = aff.get('AF_GMV'), aff.get('AF_NET'), aff.get('AF_COM'), aff.get('AF_CR')
    mo = aff.get('AF_MO')
    for nm, v in (('AF_MO', mo), ('AF_GMV', gmv), ('AF_NET', net), ('AF_COM', com), ('AF_CR', cr)):
        if not v: die(f'{nm} ว่าง')
    if not (len(mo) == len(gmv) == len(net) == len(com) == len(cr)):
        die('ความยาวอาเรย์ไม่เท่ากัน', {'AF_MO': len(mo), 'AF_GMV': len(gmv), 'AF_NET': len(net),
                                        'AF_COM': len(com), 'AF_CR': len(cr)})

    # ── ด่านตรวจ ────────────────────────────────────────────────────────────
    old = before['AF_GMV']
    if old and len(gmv) < len(old):
        die('เดือนหดลง — อาจอ่านไฟล์ไม่ครบ ไม่เขียนทับ', f'{len(old)} -> {len(gmv)}')
    bad = [f'เดือน {mo[i]}: net {net[i]:,.0f} > gmv {gmv[i]:,.0f}' for i in range(len(gmv))
           if gmv[i] and net[i] > gmv[i] * 1.001]
    if bad: die('net สูงกว่า gmv — อ่านคอลัมน์ผิด (บั๊กเดิมของพรอมป์เก่า)', bad[:5])
    neg = [f'{mo[i]}: {net[i]}' for i in range(len(net)) if net[i] < 0]
    if neg: die('net ติดลบ — อ่านคอลัมน์ผิด', neg[:5])
    tiny = [f'เดือน {mo[i]}: com {com[i]:,.0f} เทียบ gmv {gmv[i]:,.0f}' for i in range(len(gmv))
            if gmv[i] > 100_000 and 0 < com[i] < 1_000]
    if tiny: die('commission เล็กผิดปกติ — น่าจะไปอ่านคอลัมน์จำนวนโชว์เคส', tiny[:5])
    if old:
        drops = [f'{mo[i]}: {old[i]:,.0f} -> {gmv[i]:,.0f}' for i in range(min(len(old), len(gmv)))
                 if old[i] and gmv[i] and gmv[i] < old[i] * 0.98]
        if drops: die('GMV เดือนเก่าลดลง (ยอดสะสมไม่ควรลด) — ไม่เขียนทับ', drops[:5])

    summary = {'months': len(mo), 'latest_month': mo[-1],
               'latest': {'AF_GMV': gmv[-1], 'AF_NET': net[-1], 'AF_COM': com[-1], 'AF_CR': cr[-1]},
               'creators': len(aff.get('CREATORS') or []),
               'creator_months': len(aff.get('CREATOR_MONTHS') or [])}

    if a.dry_run:
        summary['current_page'] = {k: (before[k][-1] if before.get(k) else None) for k in ('AF_GMV', 'AF_CR')}
        print(json.dumps({'status': 'DRY_RUN', **summary}, ensure_ascii=False)); return 0

    W.update_html(None, aff, None, None)        # เขียนเฉพาะส่วน affiliate

    # ตรวจหลังเขียน: ค่าใน Mobile ต้องตรงกับ Affiliate Dashboard
    mism = []
    for A, B in PAIRS:
        x, y = arr(AFF, A), arr(MOB, B)
        if not x or not y: continue
        n = min(len(x), len(y))          # AF_* เริ่ม ม.ค.69 · AFI_* เริ่ม พย.68 -> เทียบท้ายเท่าที่ซ้อนกัน
        if x[-n:] != y[-n:]:
            mism.append(f'{A}[-{n}:] != {B}[-{n}:] (ล่าสุด {x[-1]} vs {y[-1]})')
    summary['mobile_mismatch'] = mism
    after = {k: arr(AFF, k) for k in before}
    changed = after != before
    if changed: W.bump_sw()
    print(json.dumps({'status': 'UPDATED' if changed else 'NO_CHANGE', **summary}, ensure_ascii=False))
    return 0 if changed else 10


if __name__ == '__main__':
    sys.exit(main())
