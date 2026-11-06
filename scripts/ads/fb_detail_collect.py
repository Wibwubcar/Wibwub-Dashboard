#!/usr/bin/env python3
"""ย้ายไฟล์ export **ระดับลึก** ของ Facebook จาก Downloads เข้า facebook/detail_raw/

ต่างจาก `fb_collect.py` (ของงาน 08:15 ห้ามแก้) 3 อย่าง:
  · ปลายทางคือ `data Ads/facebook/detail_raw/` ไม่ใช่ `facebook/daily/`
  · ชื่อไฟล์เป็น `WIBWUB-auto-fb-<บัญชี>-<ระดับ>-<from>_<to>.csv` ซึ่ง
    `detail_build.py` ใช้แยกระดับ (`ad` / `age_gender` / `placement`)
  · **ไม่ลบไฟล์เก่าในปลายทางเลย** — ชั้นนี้ต้องสะสมหลายช่วงไว้ด้วยกัน
    (ไฟล์ ต.ค. + ไฟล์ พ.ย. อยู่คู่กัน) การกันนับซ้ำทำที่ชั้นแถวใน detail_build.read_many()

ทำไมต้องมีสคริปต์: Ads Manager ตั้งชื่อไฟล์เอง (เช่น `Wi-Wu-AD-1-_-_-1-_._.-2026-...csv`)
ตั้งชื่อตอนโหลดไม่ได้ และ download-mover จับได้เฉพาะชื่อที่ขึ้นต้น `WIBWUB-auto-fb-`
ถ้าปล่อยให้พรอมป์ `mv` เอง จะพลาดได้หลายแบบและแข่งกับ mover (ซึ่งแพ้ประจำ)

ด่านที่ต้องผ่านก่อนคัดลอก:
  · ไฟล์ต้องใหม่กว่า `--after` (เวลาที่จดไว้ **ก่อน** กดปุ่ม export ของใบนั้น)
  · ขนาดไฟล์ต้องนิ่งแล้ว (กันอ่านไฟล์ที่ยังโหลดไม่จบ)
  · ต้องมีคอลัมน์ `เริ่มการรายงาน` และคอลัมน์เฉพาะของระดับนั้น
  · ทุกวันในไฟล์ต้องอยู่ในช่วง `--from`..`--to` ที่สั่งดึง
  · sha256 ซ้ำกับไฟล์ที่เคยหยิบ = ปฏิเสธ (กันหยิบใบเดิมซ้ำเมื่อ export ไม่สำเร็จ)

ใช้:  python3 scripts/ads/fb_detail_collect.py --acc AD-1 --level ad \
          --from 2026-10-01 --to 2026-10-29 --after "2026-11-06 11:50:00"
exit: 0 = คัดลอกแล้ว · 2 = ไม่ผ่านด่าน (ไม่คัดลอกอะไร)
"""
import sys, csv, json, time, hashlib, argparse, shutil, io
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fb_daily import BASE                                   # noqa: E402

DEST = BASE / 'data Ads' / 'facebook' / 'detail_raw'
LEDGER = Path(__file__).resolve().parent / 'work' / 'fb_detail_used.json'
DAY_COL = 'เริ่มการรายงาน'
NEED = {'ad': ['ชื่อโฆษณา', 'ชื่อแคมเปญ', 'ชื่อชุดโฆษณา'],
        'age_gender': ['อายุ', 'เพศ'],
        'placement': ['ตำแหน่งโฆษณา']}


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def stable(p, tries=10):
    """รอจนขนาดไฟล์ไม่เปลี่ยน — ไฟล์ที่ยังโหลดไม่จบจะอ่านได้ไม่ครบ"""
    last = -1
    for _ in range(tries):
        s = p.stat().st_size
        if s == last and s > 0:
            return True
        last = s
        time.sleep(1)
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--acc', required=True, help='คีย์บัญชี เช่น AD-1 / WibWub-AD-1')
    ap.add_argument('--level', required=True, choices=sorted(NEED))
    ap.add_argument('--from', dest='d_from', required=True)
    ap.add_argument('--to', dest='d_to', required=True)
    ap.add_argument('--after', default='', help='"YYYY-MM-DD HH:MM:SS" เวลาก่อนกด export')
    ap.add_argument('--downloads', default=str(Path.home() / 'Downloads'))
    ap.add_argument('--retry', type=int, default=6,
                    help='ยังไม่เจอไฟล์ใหม่ ให้รอแล้วลองใหม่กี่รอบ (รอบละ 6 วิ) '
                         'Ads Manager เตรียมไฟล์ช้าได้ถึง ~1 นาทีสำหรับรายงานที่แตกย่อย')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    cutoff = datetime.strptime(a.after, '%Y-%m-%d %H:%M:%S') if a.after else None
    dl = Path(a.downloads)
    used = {}
    if LEDGER.exists():
        try:
            used = json.loads(LEDGER.read_text(encoding='utf-8'))
        except ValueError:
            used = {}

    cand, rejected = [], []
    for attempt in range(max(1, a.retry)):
        cand = []
        for p in dl.glob('*.csv'):
            mt = datetime.fromtimestamp(p.stat().st_mtime)
            if cutoff and mt <= cutoff:
                continue
            cand.append((mt, p))
        if cand:
            break
        time.sleep(6)
    if not cand:
        die('ไม่พบไฟล์ .csv ใหม่กว่า --after ใน Downloads — รอบนี้ export ไม่สำเร็จ',
            {'after': a.after, 'downloads': str(dl), 'รอไปแล้ว_วินาที': 6 * a.retry})
    cand.sort(reverse=True)

    for mt, p in cand:
        if not stable(p):
            rejected.append({'file': p.name, 'เหตุผล': 'ขนาดไฟล์ยังไม่นิ่ง'}); continue
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        if digest in used:
            rejected.append({'file': p.name, 'เหตุผล': 'เคยหยิบไฟล์นี้ไปแล้ว'}); continue
        with io.open(p, encoding='utf-8-sig', newline='') as fh:
            rows = list(csv.DictReader(fh))
        if not rows:
            rejected.append({'file': p.name, 'เหตุผล': 'ไฟล์ว่าง'}); continue
        miss = [c for c in [DAY_COL] + NEED[a.level] if c not in rows[0]]
        if miss:
            rejected.append({'file': p.name, 'เหตุผล': 'ขาดคอลัมน์ ' + ', '.join(miss)}); continue
        days = sorted({(r.get(DAY_COL) or '').strip() for r in rows} - {''})
        out = [d for d in days if d < a.d_from or d > a.d_to]
        if out:
            rejected.append({'file': p.name, 'เหตุผล': 'มีวันนอกช่วงที่สั่ง: ' + ', '.join(out[:3])})
            continue
        break
    else:
        die('ไม่มีไฟล์ไหนผ่านด่านตรวจ', {'ไฟล์ที่ไม่ผ่าน': rejected[:5]})

    spend_col = next((c for c in rows[0] if 'จำนวนเงินที่ใช้จ่าย' in c), None)
    spend = round(sum(float((r.get(spend_col) or '0').replace(',', '') or 0)
                      for r in rows), 2) if spend_col else None
    dest = DEST / f'WIBWUB-auto-fb-{a.acc}-{a.level}-{a.d_from}_{a.d_to}.csv'
    info = {'source': p.name, 'sha256': digest[:12],
            'modified': mt.strftime('%Y-%m-%d %H:%M:%S'),
            'rows': len(rows), 'days_in_file': len(days),
            'span_in_file': [days[0], days[-1]] if days else None,
            'range_requested': [a.d_from, a.d_to], 'spend_in_file': spend,
            'dest': dest.name, 'ไฟล์ที่ไม่ผ่านด่าน': rejected[:3]}
    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **info}, ensure_ascii=False)); return 0

    DEST.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(p), str(dest))      # **ไม่ลบไฟล์เก่าในปลายทาง** — ชั้นนี้ต้องสะสม
    used[digest] = {'acc': a.acc, 'level': a.level, 'src': p.name,
                    'at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(used, ensure_ascii=False, indent=1), encoding='utf-8')
    try:
        p.unlink()
        info['ต้นทางใน Downloads'] = 'ลบแล้ว'
    except OSError as e:
        info['ต้นทางใน Downloads'] = 'ลบไม่ได้ (%s) — ไม่ใช่ error จดสมุดแล้ว' % type(e).__name__
    print(json.dumps({'status': 'COPIED', **info}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
