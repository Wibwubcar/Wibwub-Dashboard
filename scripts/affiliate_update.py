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

def _find_base():
    """ไล่ขึ้นจากตำแหน่งไฟล์นี้จนเจอโฟลเดอร์ All — ดูจาก marker sw.js + .git

    ห้ามฝังพาธ Mac ตายตัว: งานตั้งเวลาฝั่ง local รันในแซนด์บ็อกซ์ที่ mount โฟลเดอร์ All
    ไว้คนละที่ (/sessions/<ชื่อ>/mnt/All) และชื่อเซสชันเปลี่ยนทุกรอบ (24 ต.ค. 69)
    """
    p = Path(__file__).resolve()
    for d in (p, *p.parents):
        if (d / 'sw.js').is_file() and (d / '.git').exists():
            return d
    raise SystemExit(f'หาโฟลเดอร์ All ไม่เจอ — ไล่ขึ้นจาก {p} แล้วไม่เจอโฟลเดอร์ที่มีทั้ง '
                     'sw.js และ .git · ห้ามเดาพาธ ให้ตรวจว่าสคริปต์ยังอยู่ในโฟลเดอร์ All หรือไม่')


BASE = _find_base()
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


# ── PRODUCTS[].vid — จำนวนวิดีโอขายสินค้าจากครีเอเตอร์ ────────────────────────
# ที่มา: คอลัมน์ "วิดีโอ" ของ Transaction_Analysis_Product_List_<ช่วง>.xlsx
# จับคู่ด้วย "รหัสสินค้า" (ฟิลด์ id ใน PRODUCTS) ไม่ใช่ชื่อ — ชื่อในไฟล์เป็นชื่อไทย
# คนละชุดกับชื่อบนหน้า (เช่น id 1729451577908759108 = "เคลือบสีคาร์นัวบา" = WIBWUB Sugar)
#
# 28 ต.ค. 69: ก่อนมีสคริปต์นี้ vid ถูกใส่ด้วยมือ และ 2 ตัวสร้างกลับจากไฟล์ไม่ได้เลย
# (Leather Wipes 670 แต่ไฟล์ให้ 644 · Interior 173 แต่ไฟล์ให้ 172 — ไล่ทั้ง 131 ไฟล์
# ก็ไม่มีไฟล์ไหนให้ 670/173) ผู้ใช้ยืนยันว่า 1 รหัส = 1 สินค้า ไม่มีการรวมกลุ่ม
# -> ยึดคอลัมน์ "วิดีโอ" ของรหัสเดียวเท่านั้น ห้ามบวกหลายรหัสเข้าด้วยกัน
PROD_DIR = BASE / 'Data Affiliate' / 'สินค้า'
PL_RE = re.compile(r'^Transaction_Analysis_Product_List_(\d{8})-(\d{8})')
VID_HDR, ID_HDR = 'วิดีโอ', 'รหัสสินค้า'


def pick_product_list():
    """ไฟล์ Product_List ของช่วงล่าสุด — เรียงตาม (วันสิ้นสุด, วันเริ่ม, mtime)

    ต้อง match ตั้งแต่ต้นชื่อ: โฟลเดอร์มีไฟล์ `_WRONG_RANGE_ignore_...` ปนอยู่
    และมีไฟล์ซ้ำทั้งแบบ ` (1)` และแบบ `__<stamp>` ที่ mover เติมกันชื่อชน
    """
    best = None
    for fp in PROD_DIR.glob('Transaction_Analysis_Product_List_*.xlsx'):
        if fp.name.startswith(('~', '.')):
            continue
        m = PL_RE.match(fp.name)
        if not m:
            continue
        key = (m.group(2), m.group(1), fp.stat().st_mtime)
        if best is None or key > best[0]:
            best = (key, fp, m.group(1), m.group(2))
    return best


def read_vid_map(fp):
    """{รหัสสินค้า: จำนวนวิดีโอ} จาก sheet1.xml

    openpyxl อ่านไฟล์ export ชุดนี้ได้ 1 คอลัมน์ 0 แถว (dimension ในไฟล์ผิด)
    จึงต้องแกะ xml เองแบบเดียวกับ scripts/vid_merge.py · ค่าเป็น inline string
    (<is><t>) ไม่มี sharedStrings · แถว 1 = header, แถว 2 = คำอธิบายคอลัมน์ (ไม่ใช่ข้อมูล)
    """
    import zipfile
    with zipfile.ZipFile(fp) as zf:
        xml = zf.open('xl/worksheets/sheet1.xml').read().decode('utf-8', 'replace')
    row_re = re.compile(r'<row r="(\d+)"[^>]*>(.*?)</row>', re.DOTALL)
    cell_re = re.compile(r'<c r="([A-Z]+)(\d+)"[^>]*>(?:<is><t[^>]*>(.*?)</t></is>|<v>(.*?)</v>)?</c>')
    rows = {}
    for rn, body in row_re.findall(xml):
        cells = {}
        for col, _, s, v in cell_re.findall(body):
            cells[col] = (s if s else v) or ''
        rows[int(rn)] = cells
    if not rows:
        die('อ่าน Product_List ไม่ได้ (ไม่มีแถวเลย)', fp.name)
    hdr = rows.get(1) or {}
    cols = {}
    for col, val in hdr.items():
        v = val.strip()
        if v in (VID_HDR, ID_HDR) and v not in cols:
            cols[v] = col
    miss = [h for h in (VID_HDR, ID_HDR) if h not in cols]
    if miss:
        die('Product_List ไม่มีคอลัมน์ที่ต้องใช้ — รูปแบบไฟล์เปลี่ยน',
            {'ขาด': miss, 'ไฟล์': fp.name, 'header': sorted(hdr.values())})
    out = {}
    for rn in sorted(rows):
        if rn <= 2:                      # 1 = header · 2 = คำอธิบาย
            continue
        c = rows[rn]
        pid = (c.get(cols[ID_HDR]) or '').strip()
        raw = (c.get(cols[VID_HDR]) or '').strip().replace(',', '')
        if not pid:
            continue
        if not re.fullmatch(r'\d+(\.0+)?', raw):
            continue                     # ช่องว่าง/ค่าไม่ใช่ตัวเลข = ไม่นับ ห้ามเดาเป็น 0
        out.setdefault(pid, int(float(raw)))
    return out


def write_vid(dry):
    """เขียน vid ของทุกรายการใน PRODUCTS — ไม่ครบ = หยุด ไม่เขียนทับบางส่วน"""
    best = pick_product_list()
    if not best:
        die('ไม่พบไฟล์ Transaction_Analysis_Product_List_<YYYYMMDD>-<YYYYMMDD>.xlsx',
            str(PROD_DIR))
    _, fp, d0, d1 = best
    vmap = read_vid_map(fp)
    t = AFF.read_text(encoding='utf-8')
    m = re.search(r'const PRODUCTS = \[\n(.*?\n)\];', t, re.DOTALL)
    if not m:
        die('หา const PRODUCTS ใน Affiliate Dashboard ไม่เจอ')
    block = m.group(1)
    rows = [ln for ln in block.split('\n') if ln.strip().startswith('{')]
    noid, nofile, changes = [], [], []
    new = block
    for ln in rows:
        nm = re.search(r"name:'([^']*)'", ln)
        pid = re.search(r"id:'(\d+)'", ln)
        vid = re.search(r"vid:(\d+)", ln)
        name = nm.group(1) if nm else '(ไม่มี name)'
        if not pid:
            noid.append(name); continue
        if pid.group(1) not in vmap:
            nofile.append({'name': name, 'id': pid.group(1)}); continue
        if not vid:
            noid.append(name + ' (ไม่มีช่อง vid)'); continue
        want = vmap[pid.group(1)]
        if int(vid.group(1)) != want:
            changes.append({'name': name, 'จาก': int(vid.group(1)), 'เป็น': want})
            new = new.replace(ln, ln[:vid.start()] + f'vid:{want}' + ln[vid.end():], 1)
    # ── ด่าน: ขาดรหัส หรือหารหัสในไฟล์ไม่เจอ = หยุด ห้ามเขียน 0 ──────────────
    if noid or nofile:
        die('มีรายการใน PRODUCTS ที่จับคู่รหัสสินค้าไม่ได้ — ไม่เขียน vid เลย '
            '(ห้ามเขียน 0 แทน) ให้เติม id ใน PRODUCTS หรือหาไฟล์ที่มีรหัสนั้น',
            {'ไม่มี id บนหน้า': noid, 'หารหัสในไฟล์ไม่เจอ': nofile,
             'ไฟล์': fp.name, 'รหัสในไฟล์': len(vmap)})
    info = {'file': fp.name, 'range': f'{d0}-{d1}', 'products': len(rows),
            'ids_in_file': len(vmap), 'changes': changes}
    if changes and not dry:
        AFF.write_text(t[:m.start(1)] + new + t[m.end(1):], encoding='utf-8')
    return info


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

    summary['vid'] = write_vid(a.dry_run)

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
    changed = after != before or bool(summary['vid']['changes'])
    if changed: W.bump_sw()
    print(json.dumps({'status': 'UPDATED' if changed else 'NO_CHANGE', **summary}, ensure_ascii=False))
    return 0 if changed else 10


if __name__ == '__main__':
    sys.exit(main())
