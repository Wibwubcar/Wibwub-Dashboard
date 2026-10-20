#!/usr/bin/env python3
"""ดึงค่าโฆษณา Shopee **รายเดือน** จากไฟล์ CSV ที่เก็บไว้ใน data Ads/Shopee/

ทำไมต้องมีไฟล์นี้:
  API ของ Shopee (`get_time_graph`) ย้อนได้แค่ ~6 เดือนแบบหน้าต่างกลิ้ง
  (ทดสอบแล้ว 20 ต.ค. 69: เก่าสุดคือ 18 เม.ย. · 17 เม.ย. ตอบ code 5 invalid request)
  แต่ในโฟลเดอร์มีไฟล์ export เก่าเก็บไว้ ซึ่งมียอดของ ม.ค.–มี.ค. 69 อยู่

ข้อจำกัดสำคัญ: ไฟล์พวกนี้เป็น **รายงานรายแคมเปญของทั้งช่วง** (1 แถว = 1 แคมเปญ)
  ไม่มีแถวรายวัน -> ได้แค่ยอดรวมรายเดือน **ใช้แทนข้อมูลรายวันไม่ได้**
  หน้าเว็บจึงต้องแยกแสดงและบอกให้ชัดว่าเดือนนั้นเป็นยอดรวม ไม่ใช่รายวัน

ใช้:  python3 scripts/ads/shopee_monthly_from_csv.py [--dry-run]
ออก:  data Ads/shopee_ads_monthly.json
"""
import csv, io, json, re, sys, glob, os, argparse, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ALL = os.path.abspath(os.path.join(HERE, '..', '..'))
SRC = os.path.join(ALL, 'data Ads', 'Shopee')
OUT = os.path.join(ALL, 'data Ads', 'shopee_ads_monthly.json')
COL_SPEND, COL_GMV = 24, 22          # ค่าโฆษณา · ยอดขาย (ตรวจจากหัวตารางทุกครั้ง)


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def read_report(path):
    """คืน (ช่วงวันที่, จำนวนแคมเปญ, ค่าโฆษณา, ยอดขาย) — None ถ้าไม่ใช่รูปแบบที่รองรับ"""
    try:
        rows = list(csv.reader(io.StringIO(
            io.open(path, encoding='utf-8-sig', errors='replace').read())))
    except Exception:
        return None
    hi = next((i for i, r in enumerate(rows) if r and r[0] == 'ลำดับ'), None)
    if hi is None: return None
    hdr = rows[hi]
    # ยืนยันว่าคอลัมน์ยังอยู่ตำแหน่งเดิม ไม่งั้นข้ามไฟล์นี้ (ดีกว่าบวกเลขผิดช่อง)
    if len(hdr) <= COL_SPEND or hdr[COL_SPEND] != 'ค่าโฆษณา' or hdr[COL_GMV] != 'ยอดขาย':
        return None
    period = next((r[1] for r in rows[:hi] if r and r[0] == 'ระยะเวลา'), None)
    if not period: return None
    spend = gmv = 0.0; n = 0
    for r in rows[hi + 1:]:
        if not r or not r[0].isdigit(): continue
        try:
            spend += float(r[COL_SPEND] or 0); gmv += float(r[COL_GMV] or 0); n += 1
        except ValueError:
            continue
    return period, n, round(spend, 2), round(gmv, 2)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    if not os.path.isdir(SRC): die('ไม่พบโฟลเดอร์', SRC)

    best = {}      # 'YYYY-MM' -> dict
    skipped = 0
    for f in sorted(glob.glob(os.path.join(SRC, '*.csv'))):
        got = read_report(f)
        if not got: skipped += 1; continue
        period, n, spend, gmv = got
        m = re.match(r'(\d{2})/(\d{2})/(\d{4}) - (\d{2})/(\d{2})/(\d{4})$', period.strip())
        if not m: continue
        d1, m1, y1, d2, m2, y2 = m.groups()
        # เอาเฉพาะไฟล์ที่ครอบ "ทั้งเดือนพอดี" เดือนเดียว — ไฟล์ช่วงคร่อมเดือนแยกรายเดือนไม่ได้
        if (y1, m1) != (y2, m2) or d1 != '01': continue
        last = (datetime.date(int(y1), int(m1), 28) + datetime.timedelta(days=4))
        last = (last - datetime.timedelta(days=last.day)).day
        if int(d2) != last: continue
        key = f'{y1}-{m1}'
        rec = {'spend': spend, 'gmv': gmv, 'campaigns': n,
               'period': period.strip(), 'source': os.path.basename(f)}
        # ถ้ามีหลายไฟล์ของเดือนเดียวกัน เลือกไฟล์ที่มีแคมเปญมากสุด (ครบสุด)
        if key not in best or n > best[key]['campaigns']:
            best[key] = rec

    if not best: die('ไม่พบไฟล์ที่ครอบทั้งเดือนพอดีเลย')

    out = {'_คืออะไร': 'ค่าโฆษณา Shopee รายเดือน ดึงจากไฟล์ CSV เก่าใน data Ads/Shopee/',
           '_ข้อจำกัด': 'เป็นยอดรวมทั้งเดือน ไม่มีรายวัน — ใช้ได้เฉพาะตอนเลือกช่วงที่คลุมทั้งเดือน',
           '_ทำไมต้องมี': 'API Shopee ย้อนได้แค่ ~6 เดือน (เก่าสุด 18 เม.ย. 69 ตอนตรวจ 20 ต.ค.)',
           '_อัปเดตเมื่อ': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
           'months': dict(sorted(best.items()))}
    rep = {'status': 'DRY_RUN' if a.dry_run else 'OK', 'months': len(best),
           'skipped_files': skipped,
           'detail': {k: {'spend': v['spend'], 'campaigns': v['campaigns'], 'src': v['source'][:46]}
                      for k, v in sorted(best.items())}}
    if not a.dry_run:
        json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
