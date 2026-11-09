# -*- coding: utf-8 -*-
"""ทดสอบด่าน "ไฟล์ดิบ parse ได้ 0 แถว" + การอ่านหัวคอลัมน์สองภาษาของ detail_build.py

(ก) หัวคอลัมน์ที่ไม่รู้จักทั้งใบ -> ต้องได้ 0 แถว **และติดด่าน** พร้อมจำนวนบรรทัดที่ถูกต้อง
(ข) ไฟล์จริงใบล่าสุด (ตอนนี้หัวไทย) -> parse ได้ · ไม่ติดด่าน · วันสุดท้ายตรงกับในไฟล์เอง
(ค) ไฟล์ที่เหลือแต่แถวสรุป `ทั้งหมดจาก N ผลลัพธ์` -> 0 แถวแต่ **ห้ามติดด่าน**
    (นี่คือเหตุผลที่เกณฑ์ของด่านเป็น "บรรทัดข้อมูล > 1" ไม่ใช่ "> 0")

ที่มา: 7 พ.ย. 69 TikTok เปลี่ยนหัวคอลัมน์ export เป็นภาษาไทย (`By Day` -> `ตามวัน`)
ตัวอ่านได้ 0 แถวจากไฟล์ใหม่ทุกใบ แต่ไฟล์เก่ายัง parse ได้ rows จึงไม่ว่าง สคริปต์เลย
เขียนไฟล์และพิมพ์ว่าสำเร็จตามปกติ — ข้อมูล TikTok ค้างที่ 5 พ.ย. เงียบ ๆ 3 วัน

รัน:  python3 scripts/ads/test_parse_gate.py     (ไม่แตะไฟล์จริง ใช้ tempdir)
⛔ ต้องรันทุกครั้งที่แก้ตัวอ่านไฟล์ดิบใน detail_build.py (TK_ALIAS / tkget / tally /
   parse_failures / read_many / build_*) ไม่งั้นด่านอาจตายเงียบแบบเดิม
"""
import csv, importlib.util, shutil, sys, tempfile
from pathlib import Path

# หาโฟลเดอร์ All จากที่ไฟล์นี้วางอยู่ (scripts/ads/) ไม่ฮาร์ดโค้ดพาธ
# ⛔ ห้ามใช้ os.getcwd() — cwd ของงานตั้งเวลาคือ ~/Downloads ไม่ใช่รีโป
BASE = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('db', BASE / 'scripts/ads/detail_build.py')
db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db)

RAW = BASE / 'data Ads/TikTok/detail_raw'
ok = True


def chk(name, got, want):
    global ok
    if got != want:
        ok = False
        print('  ✗', name, '| ได้', repr(got)[:90], '| ควรได้', repr(want)[:90])


def run(lines, tag):
    """เรียก build_tk() ตัวจริงกับไฟล์จำลองใน tempdir · คืน (แถวที่ได้, ไฟล์ที่ติดด่าน)"""
    d = Path(tempfile.mkdtemp(prefix='pgate'))
    name = 'Tiktok Ads_WIBWUB-auto-ad-daily_%s_20261102-20261108.csv' % tag
    (d / name).write_text(''.join(lines), encoding='utf-8')
    del db.PARSE_LOG[:]
    rows = db.build_tk(d)[0]
    fails = db.parse_failures()
    shutil.rmtree(d, ignore_errors=True)
    return rows, fails


src = sorted(RAW.glob('*ad-daily_*.csv'), key=lambda p: p.stat().st_mtime)
src = [p for p in src if '-oct' not in p.name]
if not src:
    print('ข้ามการทดสอบ — ไม่มีไฟล์ดิบ *ad-daily_*.csv ให้ใช้เป็นตัวอย่าง')
    sys.exit(0)
SRC = src[-1]
raw = SRC.read_text(encoding='utf-8').splitlines(keepends=True)
head, body = raw[0], [x for x in raw[1:] if x.strip()]
print('ใช้ไฟล์ตัวอย่าง:', SRC.name)

# วันสุดท้ายที่ "ควรได้" อ่านจากไฟล์เอง ไม่ฮาร์ดโค้ด — ไฟล์ดิบหมุนทุกวัน
with SRC.open(encoding='utf-8-sig') as f:
    days = {(r.get('By Day') or r.get('ตามวัน') or '').strip()
            for r in csv.DictReader(f)}
want_last = max(d for d in days if d and d != '-')

# ── (ก) หัวที่ไม่รู้จักเลย ────────────────────────────────────────────────
bad = ','.join('COL%d' % i for i in range(head.count(',') + 1)) + '\n'
rows, fails = run([bad] + body, 'BAD')
chk('(ก) หัวแปลก -> 0 แถว', len(rows), 0)
chk('(ก) ติดด่าน 1 ใบ', len(fails), 1)
if fails:
    chk('(ก) ด่านรายงานจำนวนบรรทัดถูก', fails[0][1], len(body))

# ── (ข) ไฟล์จริงใบล่าสุด ──────────────────────────────────────────────────
rows, fails = run(raw, 'REAL')
chk('(ข) ไฟล์จริง parse ได้ครบทุกแถวที่มีวัน', len(rows) > 0, True)
chk('(ข) ไฟล์จริงไม่ติดด่าน', fails, [])
chk('(ข) วันสุดท้ายตรงกับในไฟล์', max(r['d'] for r in rows), want_last)
chk('(ข) ตัวเลขอ่านได้ (มี spend)', any(r.get('spend') for r in rows), True)

# ── (ค) เหลือแต่แถวสรุป ───────────────────────────────────────────────────
summ = [x for x in body if 'ทั้งหมดจาก' in x]
if summ:
    rows, fails = run([head] + summ, 'SUM')
    chk('(ค) แถวสรุปอย่างเดียว -> 0 แถว', len(rows), 0)
    chk('(ค) แต่ต้องไม่ติดด่าน', fails, [])
else:
    print('  ℹ️ ข้าม (ค) — ไฟล์ตัวอย่างใบนี้ไม่มีแถวสรุป "ทั้งหมดจาก N ผลลัพธ์"')

print('ผ่านทั้งหมด' if ok else 'ไม่ผ่าน')
sys.exit(0 if ok else 1)
