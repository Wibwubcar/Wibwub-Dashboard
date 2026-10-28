#!/usr/bin/env python3
"""ย้ายไฟล์ export ของ Facebook Ads จาก Downloads เข้า data Ads/facebook/daily/

ทำไมต้องมีสคริปต์นี้ (28 ต.ค. 69):
  · download-mover **ไม่มีกฎของ Facebook** และตั้งไม่ได้ด้วย เพราะชื่อไฟล์ที่ Ads Manager
    ส่งออก (เช่น "WibWub AD 1-แคมเปญ-....csv") ไม่ได้บอกว่าเป็นบัญชีไหนในแบบที่
    mover แยกได้ และต้องเปลี่ยนชื่อเป็น FBD_<บัญชี>_<id>_<from>_<to>.csv ก่อน
  · ถ้าปล่อยให้พรอมป์ mv เอง จะพลาดได้หลายแบบ (ไฟล์เก่าค้าง ชื่อผิด ช่วงวันที่ผิด)
    และไฟล์เก่าที่ค้างจะทำให้ fb_daily.py นับซ้ำ -> ค่าโฆษณาพุ่งเป็นเท่าตัวเงียบ ๆ

กติกา:
  · ชื่อไฟล์ใช้ **ช่วงที่สั่งดึง** (--from/--to) ไม่ใช่ min/max ของข้อมูล เพราะบางบัญชี
    ไม่มียอดวันท้าย ๆ ถ้าตั้งชื่อตามข้อมูลจริง `to` ของ 5 บัญชีจะไม่ตรงกัน
    แล้วไปติดด่านของ fb_daily.py
  · ลบไฟล์เก่าของ **บัญชีเดียวกัน + เดือนเดียวกัน** เท่านั้น — ห้ามลบข้ามเดือน
    (เดือนก่อน ๆ ต้องเก็บไว้ ไม่งั้นยอดย้อนหลังหาย)

ใช้:  python3 scripts/ads/fb_collect.py --acc AD-1 --id 597632760310102 \\
          --from 2026-10-01 --to 2026-10-28 [--max-age-min 30] [--dry-run]
exit: 0 = ย้ายแล้ว · 2 = ไม่ผ่านด่านตรวจ (ไม่ย้ายอะไร)
"""
import sys, csv, json, re, argparse, shutil
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fb_daily import BASE, SRC, COL, ACC_LABEL          # noqa: E402  ใช้ชุดเดียวกัน ห้ามก๊อป

DL = Path.home() / 'Downloads'
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def read_csv(fp):
    try:
        with open(fp, encoding='utf-8-sig', newline='') as fh:
            return list(csv.DictReader(fh))
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--acc', required=True, help='คีย์บัญชี เช่น AD-1 / WibWub-AD-1')
    ap.add_argument('--id', required=True, help='เลขบัญชีโฆษณา (act=...)')
    ap.add_argument('--from', dest='d_from', required=True)
    ap.add_argument('--to', dest='d_to', required=True)
    ap.add_argument('--downloads', default=str(DL))
    ap.add_argument('--max-age-min', type=int, default=30,
                    help='ไฟล์ต้องเพิ่งถูกสร้างไม่เกินกี่นาที กันหยิบไฟล์ของรอบก่อน')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    if a.acc not in ACC_LABEL:
        die('ไม่รู้จักคีย์บัญชีนี้ — ต้องเพิ่มใน ACC_LABEL ของ fb_daily.py ก่อน',
            {'acc': a.acc, 'ที่รู้จัก': sorted(ACC_LABEL)})
    for d in (a.d_from, a.d_to):
        if not DATE_RE.match(d): die('รูปแบบวันที่ต้องเป็น YYYY-MM-DD', d)
    if a.d_from > a.d_to: die('--from ต้องไม่เกิน --to', [a.d_from, a.d_to])
    if not a.id.isdigit(): die('--id ต้องเป็นตัวเลขล้วน', a.id)

    dl = Path(a.downloads)
    if not dl.is_dir(): die('ไม่พบโฟลเดอร์ Downloads', str(dl))
    cutoff = datetime.now() - timedelta(minutes=a.max_age_min)

    # ── หาไฟล์ที่ "หน้าตาเป็น export ของ Ads Manager" ────────────────────────
    need = set(COL.values())
    cands, rejected = [], []
    for fp in dl.glob('*.csv'):
        if fp.name.startswith(('~', '.')): continue
        mt = datetime.fromtimestamp(fp.stat().st_mtime)
        if mt < cutoff:
            continue
        rows = read_csv(fp)
        if not rows:
            rejected.append({'file': fp.name, 'เหตุผล': 'อ่านไม่ได้หรือไม่มีแถว'}); continue
        miss = [c for c in need if c not in rows[0]]
        if miss:
            rejected.append({'file': fp.name, 'เหตุผล': 'ขาดคอลัมน์', 'missing': miss[:4]}); continue
        cands.append((mt, fp, rows))
    if not cands:
        die('ไม่พบไฟล์ export ของ Facebook Ads ใน Downloads ที่ใหม่พอ — '
            'export อาจยังไม่เสร็จหรือถูกย้ายไปแล้ว **ห้ามเดาว่าสำเร็จ**',
            {'downloads': str(dl), 'อายุไม่เกิน(นาที)': a.max_age_min,
             'ไฟล์ที่ไม่ผ่าน': rejected[:5]})
    cands.sort(key=lambda x: x[0])
    mt, fp, rows = cands[-1]

    # ── ตรวจเนื้อใน ─────────────────────────────────────────────────────────
    dates = sorted({(r[COL['d']] or '').strip() for r in rows})
    bad = [d for d in dates if not DATE_RE.match(d)]
    if bad: die('มีวันที่ผิดรูปแบบในไฟล์', {'file': fp.name, 'bad': bad[:3]})
    out_of = [d for d in dates if d < a.d_from or d > a.d_to]
    if out_of:
        die('ไฟล์มีวันที่อยู่นอกช่วงที่สั่งดึง — น่าจะหยิบไฟล์ผิดใบ หรือตั้งช่วงวันที่ผิด',
            {'file': fp.name, 'ช่วงที่สั่ง': [a.d_from, a.d_to], 'นอกช่วง': out_of[:5]})
    spend = round(sum(float((r[COL['spend']] or '0').replace(',', '') or 0) for r in rows), 2)

    dest = SRC / f'FBD_{a.acc}_{a.id}_{a.d_from}_{a.d_to}.csv'
    SRC.mkdir(parents=True, exist_ok=True)
    # ลบได้เฉพาะไฟล์เก่าของบัญชีเดียวกัน + เดือนเดียวกัน (เดือน = เดือนของ from)
    mo = a.d_from[:7]
    old = [p for p in SRC.glob(f'FBD_{a.acc}_*.csv')
           if p != dest and re.match(rf'^FBD_{re.escape(a.acc)}_\d+_{re.escape(mo)}-\d\d_', p.name)]

    info = {'source': fp.name, 'modified': mt.strftime('%Y-%m-%d %H:%M'),
            'rows': len(rows), 'days_in_file': len(dates),
            'span_in_file': [dates[0], dates[-1]] if dates else None,
            'range_requested': [a.d_from, a.d_to], 'spend_in_file': spend,
            'dest': dest.name, 'จะลบไฟล์เก่าเดือนเดียวกัน': [p.name for p in old]}
    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **info}, ensure_ascii=False)); return 0

    shutil.move(str(fp), str(dest))
    for p in old:
        p.unlink()
    print(json.dumps({'status': 'MOVED', **info}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
