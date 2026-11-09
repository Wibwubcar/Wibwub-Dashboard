"""ทดสอบ commit_own_hunks ในรีโปจำลอง — เงื่อนไขที่ผู้ใช้สั่งไว้ 9 พ.ย. 69

(ก) มีการแก้ของงานอื่นค้างใน "ไฟล์เดียวกัน" -> หลังรันต้องยังค้างอยู่ ไม่ถูก commit
(ข) commit ได้เฉพาะบรรทัด SAMPLE_* ของตัวเอง
(ค) hunk ที่มีบรรทัดอื่นปน (perf ใน SAMPLE_MONTHS) -> ข้ามและรายงาน
(ง) ไฟล์ของงานอื่นที่ staged ค้างใน index จริง -> ต้องยังค้าง ไม่ถูก commit
(จ) ไม่มีอะไรค้างใน index หลังรัน (ห้าม stage ทิ้ง)
(ฉ) รอบที่สองต้องคืน CLEAN (ไม่ commit ซ้ำ)

รัน:  python3 scripts/ops/test_own_hunks.py      (ไม่แตะรีโปจริงเลย ใช้ tempdir)
⛔ ต้องรันทุกครั้งที่แก้ scripts/ops/commit_own_hunks.py หรือ SAMP_REGIONS
"""
import json, os, shutil, subprocess, sys, tempfile

# หาโฟลเดอร์ All จากที่ไฟล์นี้วางอยู่ ไม่ฮาร์ดโค้ดพาธ — ไฟล์นี้อยู่ที่ scripts/ops/
# ⛔ ห้ามใช้ os.getcwd() เพราะ cwd ของงานตั้งเวลาคือ ~/Downloads ไม่ใช่รีโป
BASE_REAL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ok = True


def chk(name, got, want):
    global ok
    if got != want:
        ok = False
        print('  ✗', name, '| ได้', repr(got)[:160], '| ควรได้', repr(want)[:160])


def raw(tmp, *a):
    return subprocess.run(['git', '-C', tmp, *a], capture_output=True, text=True)


PAGE = 'WIBWUB_Affiliate_Dashboard.html'
REGIONS = [
    {"re": r"const SAMPLE_MONTHS = \[\n.*?\n\];", "need": r"funnel:",
     "only": r"funnel:\{[^}]*\}"},
    {"re": r"const SAMPLE_LAST7D = \{.*?\n\};"},
    {"re": r"const SAMPLE_DATA_ASOF = '[^']*';"},
]


def page(asof, f1, p1, f2, p2, r7, other):
    """รูปแบบเหมือนไฟล์จริง: funnel (ของ samp) กับ perf (ของ affiliate) อยู่บรรทัดเดียวกัน
    และ SAMPLE_DATA_ASOF อยู่ติดกับ const ของงานอื่นพอดี (บังคับให้ต้องหั่น hunk)"""
    return (
        "<html><script>\n"
        "const SAMPLE_MONTHS = [\n"
        "  {key:'2026-10', label:'x', funnel:%s, perf:%s},\n"
        "  {key:'2026-11', label:'y', funnel:%s, perf:%s},\n"
        "];\n"
        "const SAMPLE_LAST7D = {\n  key:'last7d', req:%s\n};\n"
        "const SAMPLE_DATA_ASOF = '%s';\n"
        "const CREATOR_MONTHS = [%s];\n"
        "</script></html>\n" % (f1, p1, f2, p2, r7, asof, other))


tmp = tempfile.mkdtemp(prefix='ownhunks')
os.makedirs(os.path.join(tmp, 'scripts', 'ops'))
shutil.copy(os.path.join(BASE_REAL, 'scripts', 'gitw.py'), os.path.join(tmp, 'scripts'))
shutil.copy(os.path.join(BASE_REAL, 'scripts', 'ops', 'commit_own_hunks.py'),
            os.path.join(tmp, 'scripts', 'ops'))
MOD = os.path.join(tmp, 'scripts', 'ops', 'commit_own_hunks.py')

V1 = page('01/11/2026', '{req:1}', '{gmv:10}', '{req:2}', '{gmv:20}', '3', '1')
open(os.path.join(tmp, PAGE), 'w').write(V1)
open(os.path.join(tmp, 'sw.js'), 'w').write('wibwub-v1\n')
open(os.path.join(tmp, 'other.json'), 'w').write('{"a":1}\n')
raw(tmp, 'init', '-q'); raw(tmp, 'config', 'user.email', 't@t'); raw(tmp, 'config', 'user.name', 't')
raw(tmp, 'add', '-A'); raw(tmp, 'commit', '-qm', 'init')
HEAD0 = raw(tmp, 'rev-parse', 'HEAD').stdout.strip()

# งานเรา (samp) เขียน SAMPLE_DATA_ASOF + funnel  /  งานอื่นเขียน perf + CREATOR_MONTHS ในไฟล์เดียวกัน
# ของเรา: funnel เดือน ต.ค. · req ใน LAST7D · SAMPLE_DATA_ASOF
# ของงานอื่น: perf เดือน พ.ย. (บรรทัดเดียวกับ funnel ที่เราก็แก้ด้วย) · CREATOR_MONTHS
open(os.path.join(tmp, PAGE), 'w').write(
    page('06/11/2026', '{req:9}', '{gmv:10}', '{req:8}', '{gmv:99}', '7', '1,2,3'))
# งานอื่น stage ไฟล์ของมันค้างไว้ใน index จริง (เคส "staged ค้างถูกกวาด")
open(os.path.join(tmp, 'other.json'), 'w').write('{"a":2}\n')
raw(tmp, 'add', 'other.json')

r = subprocess.run([sys.executable, MOD, PAGE, json.dumps(REGIONS)],
                   cwd=tmp, capture_output=True, text=True)
out = json.loads(r.stdout)
chk('(ข) สถานะ COMMITTED', out.get('status'), 'COMMITTED')
chk('(ค) ข้าม 2 บรรทัดที่มีของงานอื่นปน', len(out.get('hunks_skipped', [])), 2)
chk('(ค) commit 3 บรรทัดของเรา', out.get('hunks_mine'), 3)
chk('(ข) commit เฉพาะไฟล์หน้านี้', raw(tmp, 'show', '--format=', '--name-only', 'HEAD').stdout.split(), [PAGE])
chk('HEAD ขยับ 1 commit', raw(tmp, 'rev-list', '--count', HEAD0 + '..HEAD').stdout.strip(), '1')

# เนื้อ commit: ต้องมี SAMPLE_* ใหม่ และต้องยังเป็นค่าเก่าของงานอื่น
body = raw(tmp, 'show', 'HEAD:' + PAGE).stdout
chk('(ข) SAMPLE_DATA_ASOF ใหม่เข้า commit', "SAMPLE_DATA_ASOF = '06/11/2026'" in body, True)
chk('(ข) funnel ที่ perf ไม่เปลี่ยน -> เข้า commit', 'funnel:{req:9}' in body, True)
chk('(ข) req ใน LAST7D เข้า commit', 'req:7' in body, True)
chk('(ค) บรรทัดที่ perf เปลี่ยนด้วย -> ยังเป็นค่าเก่าทั้งบรรทัด',
    "funnel:{req:2}, perf:{gmv:20}" in body, True)
chk('(ก) CREATOR_MONTHS ของงานอื่นยังเป็นค่าเก่า', 'CREATOR_MONTHS = [1]' in body, True)

# ของงานอื่นต้องยังค้างใน working tree
wt = raw(tmp, 'diff', '--name-only').stdout.split()
chk('(ก) หน้านี้ยังมีของงานอื่นค้างอยู่', PAGE in wt, True)
dif = raw(tmp, 'diff', '-U0', '--', PAGE).stdout     # -U0: ไม่เอาบรรทัด context มาปน
chk('(ก) ของค้างคือ perf ของงานอื่น', 'perf:{gmv:99}' in dif, True)
chk('(ก) ของค้างคือ CREATOR_MONTHS', 'CREATOR_MONTHS = [1,2,3]' in dif, True)
chg = [l for l in dif.split('\n')
       if l.startswith(('+', '-')) and not l.startswith(('+++', '---'))]
chk('(ก) เหลือค้าง 2 บรรทัดเก่า + 2 บรรทัดใหม่', len(chg), 4)
chk('(ก) ของเราไม่ค้างแล้ว', any('SAMPLE_DATA_ASOF' in l for l in chg), False)
chk('(ก) funnel ที่ commit แล้วไม่ค้างซ้ำ', any('req:9' in l for l in chg), False)
chk('(ก) LAST7D ที่ commit แล้วไม่ค้างซ้ำ', any('req:7' in l for l in chg), False)

# index จริงต้องไม่ถูกแตะ: other.json ยัง staged อยู่ และไม่ได้เข้า commit
chk('(ง) other.json ยัง staged ค้างอยู่', raw(tmp, 'diff', '--cached', '--name-only').stdout.strip(), 'other.json')
chk('(จ) หน้านี้ไม่ค้างใน index', PAGE in raw(tmp, 'diff', '--cached', '--name-only').stdout, False)

# รอบสอง: ของเราไม่มีอะไรใหม่ แต่ของงานอื่นยังค้าง -> ต้องไม่ commit ซ้ำ
r2 = subprocess.run([sys.executable, MOD, PAGE, json.dumps(REGIONS)],
                    cwd=tmp, capture_output=True, text=True)
o2 = json.loads(r2.stdout)
chk('(ฉ) รอบสองไม่ commit ซ้ำ', o2.get('status'), 'NO_OWN_HUNKS')
chk('(ฉ) HEAD ไม่ขยับเพิ่ม', raw(tmp, 'rev-list', '--count', HEAD0 + '..HEAD').stdout.strip(), '1')

print('ผ่านทั้งหมด' if ok else 'ไม่ผ่าน')
if not ok:
    print('--- stdout รอบแรก:', r.stdout[:900]); print('--- stderr:', r.stderr[:600])
shutil.rmtree(tmp, ignore_errors=True)
sys.exit(0 if ok else 1)
