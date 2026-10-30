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
import sys, json, argparse, re, datetime as dt
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
PAGES = ['WIBWUB_Dashboard.html', 'WIBWUB_Mobile.html']
# อาเรย์ที่ process_sales() คืนมาและ update_html() เขียน
WATCH = ['SH_REV', 'TK_REV', 'LZ_REV', 'SH_ORD', 'TK_ORD', 'LZ_ORD']


# แถวในชีตยอดขายใช้รูปแบบ "01-DD/MM/YY" = ยอดสะสมตั้งแต่วันที่ 1 ถึง DD
# วันสุดท้ายของแถวล่างสุด = วันที่ข้อมูลในชีตไปถึง
ROW_RE = re.compile(r'^\s*0?1\s*-\s*(\d{1,2})/(\d{1,2})/(\d{2})\s*$')


TK_DATE_RE = re.compile(r'(\d{1,2})/(\d{1,2})/(\d{2})')


def tiktok_asof(rows):
    """ชีต TikTok เป็นรายวัน (DD/MM/YY ปี พ.ศ. 2 หลัก) ไม่ใช่ยอดสะสมแบบ Shopee/Lazada
    จึงต้องหาวันที่มากสุดจากทุกเซลล์"""
    best = None
    for r in rows or []:
        for c in (r or []):
            m = TK_DATE_RE.search(str(c or ''))
            if not m:
                continue
            d, mo, yy = int(m[1]), int(m[2]), int(m[3])
            if not (1 <= mo <= 12 and 1 <= d <= 31):
                continue
            y = 1957 + yy if yy >= 60 else 2000 + yy      # 69 = พ.ศ.2569 = ค.ศ.2026
            iso = f'{y}-{mo:02d}-{d:02d}'
            if best is None or iso > best:
                best = iso
    return best


def sheet_asof(rows):
    """วันสุดท้ายที่ชีตนี้มีข้อมูล (YYYY-MM-DD) — None ถ้าอ่านไม่ได้"""
    best = None
    for r in rows or []:
        m = ROW_RE.match(str((r or [''])[0] or ''))
        if not m:
            continue
        d, mo, yy = int(m[1]), int(m[2]), int(m[3])
        iso = f'20{yy:02d}-{mo:02d}-{d:02d}'
        if best is None or iso > best:
            best = iso
    return best


# ═════════════════════════════════════════════════════════════════════════════
# เติมยอดเดือนปัจจุบันจากข้อมูลหลังบ้าน (30 ต.ค. 69)
#
# ปัญหา: ทีมกรอกชีต Shopee/Lazada ทุกวันจันทร์ ยอดเดือนปัจจุบันบนหน้าเว็บจึงค้าง
#        ทั้งสัปดาห์ ทั้งที่ data Ads/ads_daily.json มียอดจริงรายวันอยู่แล้ว
# กติกา: ชีตเป็นหลักเสมอ · เติมเฉพาะ "วันหลัง sheet_asof ของแพลตฟอร์มนั้น"
#        · เฉพาะเดือนปัจจุบัน · พอทีมกรอกชีตวันจันทร์ ค่าชีตจะแทนที่ส่วนที่เติมเอง
#        · TikTok ไม่เติมยอดขาย/ออเดอร์ (ชีตกรอกเกือบรายวัน และหลังบ้านต่างจากชีต)
# ═════════════════════════════════════════════════════════════════════════════
BF_MAP = {'shopee': ('sh_real', 'SH_REV', 'SH_ORD', 'Shopee'),
          'lazada': ('lz_real', 'LZ_REV', 'LZ_ORD', 'Lazada')}
BF_TOL = 0.01          # ช่วงที่มีทั้งชีตและหลังบ้านต้องต่างกันไม่เกิน 1%


def _daysum(days, key, field, lo, hi):
    """รวมค่าจาก ads_daily ช่วง [lo, hi] · คืน (ผลรวม, วันที่มีคีย์, วันที่ขาดคีย์)"""
    tot, have, miss = 0.0, [], []
    for d in sorted(days):
        if not (lo <= d <= hi):
            continue
        v = (days[d] or {}).get(key)
        if not isinstance(v, dict) or v.get(field) is None:
            miss.append(d); continue
        tot += v[field] or 0
        have.append(d)
    return tot, have, miss


def backfill_current_month(sales, asof_ch, today=None):
    """เติม SH_/LZ_ ของเดือนปัจจุบันจาก ads_daily.json · คืน (รายงาน, วันที่ใหม่รายช่อง)"""
    rep = {'filled': {}, 'skipped': {}, 'checks': {}}
    per_ch_new = {}
    fp = BASE / 'data Ads' / 'ads_daily.json'
    if not fp.exists():
        rep['skipped']['ทั้งหมด'] = 'ไม่พบ data Ads/ads_daily.json'
        return rep, per_ch_new
    try:
        days = (json.loads(fp.read_text(encoding='utf-8')) or {}).get('days') or {}
    except (ValueError, OSError) as e:
        rep['skipped']['ทั้งหมด'] = 'อ่าน ads_daily.json ไม่ได้: %s' % type(e).__name__
        return rep, per_ch_new

    today = today or dt.date.today()
    mon = today.strftime('%Y-%m')
    # ด่าน: ถ้าไฟล์ยังไม่มี "เมื่อวาน" แปลว่างานที่เขียนไฟล์นี้ยังไม่ได้รัน -> ไม่เติม
    yday = (today - dt.timedelta(days=1)).isoformat()
    if yday not in days:
        rep['skipped']['ทั้งหมด'] = 'ads_daily.json ยังไม่มีวันที่ %s — ไม่เติม' % yday
        return rep, per_ch_new

    first = mon + '-01'
    last_in_file = max([d for d in days if d.startswith(mon)] or [''])
    for ch, (key, rev_k, ord_k, label) in BF_MAP.items():
        asof = asof_ch.get(ch)
        if not asof or not asof.startswith(mon):
            rep['skipped'][label] = 'ไม่มี sheet_asof ของเดือนนี้'; continue
        # ── ด่าน 1%: ช่วงที่มีทั้งชีตและหลังบ้าน (1..asof) ต้องตรงกัน
        # ถ้าชีตไม่มีค่าเลยในเดือนนี้ (เช่น Lazada ออเดอร์ที่ทีมกรอกเฉพาะแถวปิดเดือน)
        # จะเทียบช่วงทับซ้อนของเดือนนี้ไม่ได้ -> ใช้ "เดือนที่ปิดแล้วล่าสุด" เป็นด่านแทน
        # และต้องเอายอดหลังบ้าน **ทั้งเดือน** มาใช้ ไม่ใช่บวกเฉพาะวันหลัง asof
        # (ไม่งั้นจะได้ยอดไม่ครบเดือน แล้วด่าน "ห้ามลด" จะตีกลับ — เจอจริง 30 ต.ค. 69
        #  LZ_ORD 53 -> 13 เพราะบวกแค่วันที่ 26-27)
        ok, whole = {}, {}
        prev_mon = (dt.date.fromisoformat(first) - dt.timedelta(days=1)).strftime('%Y-%m')
        for field, arr_k in (('gmv', rev_k), ('orders', ord_k)):
            arr = sales.get(arr_k) or []
            sheet_val = arr[-1] if arr else None
            if sheet_val:
                back, _, _ = _daysum(days, key, field, first, asof)
                diff = abs(back - sheet_val) / sheet_val
                ok[field] = diff <= BF_TOL
                rep['checks']['%s %s' % (label, field)] = {
                    'ช่วงเทียบ': '%s..%s' % (first[-2:], asof[-2:]),
                    'ชีต': round(sheet_val, 2), 'หลังบ้าน': round(back, 2),
                    'ต่าง%': round(diff * 100, 2), 'ผ่าน': ok[field]}
            else:
                prev_sheet = arr[-2] if len(arr) >= 2 else None
                prev_back, _, _ = _daysum(days, key, field, prev_mon + '-01', prev_mon + '-31')
                if not prev_sheet or not prev_back:
                    ok[field] = False
                    rep['checks']['%s %s' % (label, field)] = {
                        'ช่วงเทียบ': prev_mon, 'ผ่าน': False,
                        'เหตุผล': 'ชีตเดือนนี้ว่าง และเทียบเดือนที่ปิดแล้วไม่ได้'}
                else:
                    diff = abs(prev_back - prev_sheet) / prev_sheet
                    ok[field] = diff <= BF_TOL
                    whole[field] = True      # ชีตว่าง -> ต้องใช้ยอดหลังบ้านทั้งเดือน
                    rep['checks']['%s %s' % (label, field)] = {
                        'ช่วงเทียบ': prev_mon + ' (เดือนที่ปิดแล้ว)',
                        'ชีต': round(prev_sheet, 2), 'หลังบ้าน': round(prev_back, 2),
                        'ต่าง%': round(diff * 100, 2), 'ผ่าน': ok[field],
                        'หมายเหตุ': 'ชีตเดือนนี้ว่าง -> ใช้ยอดหลังบ้านทั้งเดือน'}
        # ── เติมวันหลัง asof
        nxt = (dt.date.fromisoformat(asof) + dt.timedelta(days=1)).isoformat()
        if nxt > last_in_file:
            rep['skipped'][label] = 'ไม่มีวันใหม่กว่าชีต (ชีตถึง %s)' % asof; continue
        def _span(field):
            lo = first if whole.get(field) else nxt
            return _daysum(days, key, field, lo, last_in_file)
        add_rev, have, _ = _span('gmv')
        if not have:
            rep['skipped'][label] = 'ไม่มีคีย์ %s หลังวันที่ %s' % (key, asof); continue
        done = {}
        if ok.get('gmv'):
            base_rev = 0 if whole.get('gmv') else (sales[rev_k][-1] or 0)
            sales[rev_k][-1] = round(base_rev + add_rev, 2)
            done['ยอดขาย'] = round(add_rev, 2)
        else:
            rep['skipped']['%s ยอดขาย' % label] = 'ด่าน 1% ไม่ผ่าน — ใช้ชีตอย่างเดียว'
        add_ord, have_o, _ = _span('orders')
        if ok.get('orders') and add_ord:
            base_ord = 0 if whole.get('orders') else (sales[ord_k][-1] or 0)
            sales[ord_k][-1] = int(base_ord + add_ord)
            done['ออเดอร์'] = int(add_ord)
        elif add_ord:
            rep['skipped']['%s ออเดอร์' % label] = 'ด่าน 1% ไม่ผ่าน — ใช้ชีตอย่างเดียว'
        if done:
            done['ช่วงที่เติม'] = '%s..%s' % (have[0][-2:], have[-1][-2:])
            rep['filled'][label] = done
            per_ch_new[label] = have[-1]
    return rep, per_ch_new


def write_backfill_label(filled):
    """เขียน MTD_BACKFILL ลงหน้าเว็บ — บอกว่าช่วงไหนของเดือนนี้มาจากหลังบ้าน

    เขียนทุกรอบรวมถึงตอนว่าง ({}) เพื่อให้ป้ายหายเองเมื่อทีมกรอกชีตตามทันแล้ว
    """
    TH = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
          'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
    mo = TH[dt.date.today().month - 1]
    parts = []
    for label, d in sorted((filled or {}).items()):
        span = d.get('ช่วงที่เติม')
        if span:
            a, b = span.split('..')
            parts.append("%s:'%s-%s %s'" % (label, int(a), int(b), mo))
    body = '{ ' + ', '.join(parts) + ' }' if parts else '{}'
    out = []
    for pg in PAGES:
        f = BASE / pg
        if not f.exists():
            continue
        h = f.read_text(encoding='utf-8')
        new = re.sub(r'const MTD_BACKFILL = \{[^}]*\};',
                     'const MTD_BACKFILL = %s;' % body, h, count=1)
        if new != h:
            f.write_text(new, encoding='utf-8'); out.append(pg)
    return {'label': body, 'pages': out}


def write_asof(asof, per_ch=None):
    """เขียน SALES_ASOF + MTD_COVERAGE ลงหน้าเว็บ — ขยับไปข้างหน้าเท่านั้น

    ทำไมต้องมี: หลังย้ายมาใช้สคริปต์ชุดใหม่ 19 ต.ค. 69 ไม่มีตัวไหนเขียนค่านี้อีกเลย
    ทุกตัวอ่านอย่างเดียว ค่าจึงค้างอยู่ที่ 2026-10-18 ถาวร และหน้า "การตลาด vs ยอดขาย"
    ใช้ค่านี้เป็นขอบของการกระทบยอด -> ป้าย "ยังไม่กระทบยอด" จะยาวขึ้นเรื่อย ๆ
    """
    # ⚠️ ต้องตรวจ "ห้ามถอยหลัง" ให้ครบทุกหน้า **ก่อน** เริ่มเขียน
    # เคยเขียนด่านไว้ในลูปแล้วเจอว่าเขียน Dashboard ไปแล้วค่อยหยุดที่ Mobile
    # ทำให้สองหน้าค่าไม่ตรงกันโดยไม่มีอะไรเตือน (เจอตอนทดสอบ 22 ต.ค. 69)
    cur = []
    for pg in PAGES:
        f = BASE / pg
        if not f.exists():
            continue
        m = re.search(r"SALES_ASOF\s*=\s*'(\d{4}-\d{2}-\d{2})'", f.read_text(encoding='utf-8'))
        if m:
            cur.append(m.group(1))
    if cur and asof < max(cur):          # ชีตอาจอ่านพลาดบางรอบ
        return {'skipped': f'{asof} เก่ากว่าค่าเดิม {max(cur)} — ไม่เขียน'}

    changed = []
    for pg in PAGES:
        f = BASE / pg
        if not f.exists():
            continue
        h = f.read_text(encoding='utf-8')
        new = h
        m = re.search(r"SALES_ASOF\s*=\s*'(\d{4}-\d{2}-\d{2})'", new)
        if m and asof != m.group(1):
            new = new[:m.start(1)] + asof + new[m.end(1):]
        # MTD_COVERAGE โชว์วันที่ของแต่ละช่องทาง — แต่ละชีตไปถึงคนละวันได้
        # (22 ต.ค. 69: Shopee/Lazada ถึง 18 แต่ TikTok ถึง 21)
        # ⚠️ แก้ทีละคีย์เท่านั้น ห้ามประกอบ dict ใหม่ทั้งก้อน — คีย์ Shipnity เป็นของ
        # shipnity_update.py ถ้าเขียนทับจะดึงวันของมันถอยหลังแบบเงียบ ๆ
        for k, v in (per_ch or {}).items():
            if not v:
                continue
            mk = re.search(r"(MTD_COVERAGE\s*=\s*\{[^}]*?" + k + r"\s*:\s*')(\d{4}-\d{2}-\d{2})",
                           new)
            if mk and v > mk.group(2):
                new = new[:mk.start(2)] + v + new[mk.end(2):]
        if new != h:
            f.write_text(new, encoding='utf-8')
            changed.append(pg)
    return {'asof': asof, 'pages': changed}


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
    ap.add_argument('--no-backfill', action='store_true',
                    help='ไม่ต้องเติมยอดเดือนปัจจุบันจากหลังบ้าน (ใช้ชีตอย่างเดียว)')
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

    # ── เติมยอดเดือนปัจจุบันจากหลังบ้าน (ก่อนด่านตรวจ เพื่อให้ด่าน "ห้ามลด" ตรวจค่าที่เติมแล้วด้วย)
    asof_pre = {k: sheet_asof(sheets.get(k)) for k in ('shopee', 'lazada')}
    asof_pre['tiktok'] = tiktok_asof(sheets.get('tiktok'))
    backfill, per_ch_bf = ({}, {}) if a.no_backfill else backfill_current_month(sales, asof_pre)

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

    # ── SALES_ASOF: ขอบ "กระทบยอดแล้ว" ที่หน้า การตลาด vs ยอดขาย ใช้ ─────────
    # อ่านวันสุดท้ายจากชีตเอง แทนที่จะปล่อยให้ค่าค้างอยู่กับที่
    asof_ch = asof_pre
    got = {k: v for k, v in asof_ch.items() if v}
    PER = {'shopee': 'Shopee', 'tiktok': 'TikTok', 'lazada': 'Lazada'}
    per_ch = {PER[k]: v for k, v in got.items() if k in PER}
    # MTD_COVERAGE รายช่องทาง = วันล่าสุดที่ "มีข้อมูล" ไม่ว่าจะมาจากชีตหรือหลังบ้าน
    # ส่วนวันของชีตล้วนเก็บแยกไว้ใน data Ads/sheet_asof.json ให้ตัวตรวจอ่าน
    for lbl, d_ in (per_ch_bf or {}).items():
        if d_ and d_ > per_ch.get(lbl, ''):
            per_ch[lbl] = d_
    if backfill:
        summary['backfill'] = backfill
        if not a.dry_run:
            summary['backfill']['label'] = write_backfill_label(backfill.get('filled'))
    summary['sheet_asof'] = asof_ch
    # เก็บ "วันสุดท้ายที่ชีตมีข้อมูล" แยกเป็นไฟล์ (30 ต.ค. 69)
    # ห้ามให้ตัวตรวจไปอ่าน MTD_COVERAGE แทน เพราะเมื่องาน "เติมยอดจากหลังบ้าน" เริ่มทำงาน
    # MTD_COVERAGE จะขยับทุกวันจาก ads_daily.json แม้ทีมจะยังไม่กรอกชีต -> ตัวตรวจจะสรุปผิด
    # ว่าทีมกรอกทัน (false negative ที่แย่กว่าเตือนเกิน) ไฟล์นี้เป็นของชีตล้วน ไม่ปนหลังบ้าน
    if not a.dry_run:
        try:
            (BASE / 'data Ads').mkdir(exist_ok=True)
            (BASE / 'data Ads' / 'sheet_asof.json').write_text(json.dumps(
                {'_note': 'วันสุดท้ายที่ชีตของแต่ละช่องทางมีข้อมูล — ของชีตล้วน '
                          'ไม่รวมข้อมูลหลังบ้าน เขียนโดย sales_update.py ทุกรอบที่รันจริง',
                 'shopee': asof_ch.get('shopee'), 'tiktok': asof_ch.get('tiktok'),
                 'lazada': asof_ch.get('lazada'),
                 'written_at': dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
                ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
            summary['sheet_asof_file'] = 'data Ads/sheet_asof.json'
        except OSError as e:
            summary['sheet_asof_file_error'] = f'{type(e).__name__}: {e}'
    if not got:
        summary['asof_note'] = 'อ่านวันที่จากชีตไม่ได้เลย — คง SALES_ASOF เดิมไว้'
    elif len(set(got.values())) > 1:
        # ชีตคนละวัน = ด่านตรวจของหน้าการตลาดจะเทียบไม่ตรงอยู่ดี ใช้ตัวเก่าสุดไว้ก่อน
        # แล้วรายงานให้คนไปกรอกชีตที่ตามหลังให้ทัน
        summary['asof_note'] = ('ชีตแต่ละช่องทางไปถึงคนละวัน ใช้วันเก่าสุด — '
                                'ควรกรอกชีตที่ตามหลังให้ทันกัน')
        summary['asof_write'] = write_asof(min(got.values()), per_ch) if not a.dry_run else 'dry-run'
    else:
        summary['asof_write'] = (write_asof(next(iter(got.values())), per_ch)
                                 if not a.dry_run else 'dry-run')

    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **summary}, ensure_ascii=False))
        return 0

    W.update_html(sales, None, None, None)      # เขียนเฉพาะส่วน sales (ส่วนอื่นเป็น None จึงถูกข้าม)

    # ── ช่องทาง Shipnity (FB/LINE/CARE/...) ให้สดพร้อมกับ sales ทุกรอบ ──────
    # ไม่งั้นกลางสัปดาห์ยอดรวมจะเอียง: SH/TK/LZ เดินหน้าวันละ 2 รอบ แต่ช่องทางอื่น
    # อัปเดตแค่วันจันทร์ · ใช้ cache จึงไม่ช้า (รอบที่ไม่มีไฟล์ Shipnity ใหม่ <1 วิ)
    ch_any = False
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from ship_cache import load_shipnity
        import shipnity_update as S
        raw = load_shipnity()
        if raw:
            asof = S._asof((BASE / PAGES[0]).read_text(encoding='utf-8'))
            rep_ch, ch_changed = S.write_channels(raw, asof)
            _, cov_changed = S.write_coverage(raw, asof)
            summary['channels_asof'] = asof
            summary['channels_changed'] = {pg: sorted(d) for pg, d in rep_ch.items()}
            ch_any = ch_changed or cov_changed
    except Exception as e:                   # ช่องทางล้มต้องไม่ทำให้ sales ล้มด้วย
        summary['channels_error'] = f'{type(e).__name__}: {e}'
        ch_any = False

    after = {p: arrays(BASE / p) for p in PAGES}
    changed = (after != before) or ch_any
    if changed: W.bump_sw()
    summary['changed_files'] = [p for p in PAGES if after[p] != before[p]]
    print(json.dumps({'status': 'UPDATED' if changed else 'NO_CHANGE', **summary}, ensure_ascii=False))
    return 0 if changed else 10


if __name__ == '__main__':
    sys.exit(main())
