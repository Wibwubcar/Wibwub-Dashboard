#!/usr/bin/env python3
"""อัปเดต Data Shipnity/Sales_Dashboard.html จาก Excel ใน Data Shipnity/

ใช้ process_shipnity() ของ wibwub_update.py เป็นตัวคำนวณ — ห้าม reimplement
เพราะไฟล์ใน Data Shipnity/ เป็น cumulative snapshot รายวันที่ซ้อนทับกัน
ต้อง dedup ด้วย (order_id, ชื่อสินค้า) ไม่งั้นนับซ้ำหลายสิบรอบ
และ RAW ต้องมี channels / products / order_counts ครบตามที่ JS ในหน้าเว็บอ้าง

ใช้:  python3 scripts/shipnity_update.py [--dry-run]
exit: 0 = อัปเดตแล้ว · 10 = ไม่มีอะไรเปลี่ยน · 2 = ข้อมูลไม่ผ่านด่านตรวจ (ไม่เขียนไฟล์)
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
PAGE = BASE / 'Data Shipnity' / 'Sales_Dashboard.html'

# คีย์ที่ JS ในหน้าเว็บอ้างผ่าน RAW.* — ขาดตัวใดตัวหนึ่งหน้าเว็บพังทันที
REQUIRED = {'date_min', 'date_max', 'channels', 'products', 'lines', 'order_counts'}

# ── อาเรย์ยอดขายรายช่องทางใน WIBWUB_Dashboard.html / WIBWUB_Mobile.html ──────
# Shipnity เป็นแหล่งเดียวของช่องทางเหล่านี้ (ไม่มีใน Google Sheets)
# ก่อน 20 ต.ค. 2569 ไม่มีงานไหนเขียนเลย -> ค่าค้างซ้ำเดิมตั้งแต่ มิ.ย. และสองหน้าไม่ตรงกัน
MAIN_PAGES = ['WIBWUB_Dashboard.html', 'WIBWUB_Mobile.html']
# ⚠️ ชื่อช่องทางใน Shipnity สะกดไม่เหมือนกันหลายแบบ (คนกรอก/ระบบเปลี่ยน)
# 'Line OA' (เว้นวรรค) กับ 'LINE_OA' (ขีดล่าง) เป็นคนละสตริง — เดิม map แค่ตัวแรก
# ทำให้ยอด LINE_OA 449,137 บาท (ทั้งปี 69) หายไปจาก TOTAL_REV เงียบ ๆ
# แก้ 20 ต.ค. 2569 พร้อมใส่ด่านตรวจ unmapped ด้านล่างเพื่อไม่ให้เกิดซ้ำ
CH_ARRAYS = {                      # ชื่ออาเรย์ -> ช่องทางใน Shipnity ที่รวมเข้าด้วยกัน
    'FB_REV':   ['Facebook'],
    'LINE_REV': ['Line OA', 'Line Shopping', 'LINE_OA', 'LINE_SHOPPING'],
    'CARE_REV': ['Carcare'],
    'WEB_REV':  ['Website'],
    'MKT_REV':  ['Marketing', 'สินค้าสำหรับทำการตลาด'],
    'POS_REV':  ['POS'],
    'BEUK_REV': ['เบิกของ'],
    'OTH_REV':  ['Makro pro', 'Other', 'instagram'],
}
# ช่องทางฝั่งแพลตฟอร์ม — มีอาเรย์ของตัวเองจากแหล่งอื่น (ads_daily) ไม่เอาของ Shipnity
PLATFORM_CH = {'Shopee', 'TikTok', 'Lazada'}
CH_ORDERS = {                      # ออเดอร์รายช่องทาง — TOTAL_ORD รวมครบ 10 ช่องทางเท่า TOTAL_REV
    'FB_ORD':   ['Facebook'],
    'LINE_ORD': ['Line OA', 'Line Shopping', 'LINE_OA', 'LINE_SHOPPING'],
    'WEB_ORD':  ['Website'],
    'CARE_ORD': ['Carcare'],
    'MKT_ORD':  ['Marketing', 'สินค้าสำหรับทำการตลาด'],
    'BEUK_ORD': ['เบิกของ'],
    'POS_ORD':  ['POS'],
    'OTH_ORD':  ['Makro pro', 'Other', 'instagram'],
}


def _asof(html):
    """วันสุดท้ายที่ฝั่ง Sales (Shopee/TikTok/Lazada) ครอบถึง — ตัด Shipnity ให้เท่ากัน
    ไม่งั้นยอดรวมเดือนล่าสุดจะคาบเกี่ยวคนละวัน (Shipnity มักมีข้อมูลล่วงหน้า 1 วัน)"""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from ship_cache import sales_asof
    return sales_asof()


def channel_months(raw, asof):
    """ยอดขาย/ออเดอร์รายเดือนต่อช่องทาง จาก order_counts (ระดับออเดอร์ dedup แล้ว)"""
    CH = raw['channels']; agg = {}
    for o in raw['order_counts']:
        d = o['d']
        if asof and d > asof: continue
        mo = d[:7]
        agg.setdefault(mo, {}).setdefault(CH[o['c']], {'r': 0.0, 'n': 0})
        agg[mo][CH[o['c']]]['r'] += o['r']; agg[mo][CH[o['c']]]['n'] += o['n']
    return agg


def write_coverage(raw, asof, dry=False):
    """บอกบนหน้าเว็บว่าช่องทางฝั่ง Shipnity ครอบถึงวันไหน

    ช่องทาง Shipnity อัปเดตคนละความถี่กับ Shopee/TikTok/Lazada (ไฟล์มาจากคน export เอง)
    ถ้าวันไหนไม่มีไฟล์ใหม่ ยอดช่องทางจะค้างโดยไม่มีใครรู้ — คีย์นี้ทำให้เห็นทันที
    mtdCoverageLabel() ในหน้าเว็บวนอ่าน MTD_COVERAGE เองจึงโชว์ให้อัตโนมัติ
    (MTD_MAX_DATE ใช้ค่า max จึงไม่ถูกดึงลงถ้า Shipnity ตามหลัง)
    """
    ship = min(x for x in (raw['date_max'], asof) if x) if asof else raw['date_max']
    fp = BASE / 'WIBWUB_Dashboard.html'
    t = fp.read_text(encoding='utf-8')
    m = re.search(r"(const MTD_COVERAGE\s*=\s*\{)([^}]*)(\})", t)
    if not m: return None, False
    body = m.group(2)
    if re.search(r"Shipnity\s*:", body):
        new = re.sub(r"(Shipnity\s*:\s*')[^']*(')", lambda z: z.group(1) + ship + z.group(2), body)
    else:
        new = body.rstrip().rstrip(',') + f", Shipnity:'{ship}' "
    if new == body: return ship, False
    if not dry: fp.write_text(t[:m.start(2)] + new + t[m.end(2):], encoding='utf-8')
    return ship, True


def check_unmapped(agg):
    """ช่องทางที่มียอดแต่ไม่ได้ map ไว้ = ยอดหายจาก TOTAL_REV เงียบ ๆ -> หยุดทันที

    เคยเกิดจริง: 'LINE_OA' กับ 'Makro pro' ไม่อยู่ใน CH_ARRAYS เลยหายไปจากยอดรวม
    ตั้งแต่ ม.ค. 69 โดยไม่มีใครรู้ เพราะหน้าเว็บไม่ได้บอกว่ามีช่องทางที่ไม่ถูกนับ
    """
    mapped = {c for v in CH_ARRAYS.values() for c in v} | PLATFORM_CH
    bad = {}
    for mo, chans in agg.items():
        for c, v in chans.items():
            if c not in mapped and (v.get('r') or 0) > 0:
                bad[c] = round(bad.get(c, 0) + v['r'], 2)
    if bad:
        die('มีช่องทางใน Shipnity ที่ยังไม่ได้ map — ยอดจะหายจาก TOTAL_REV '
            'ให้เพิ่มเข้า CH_ARRAYS/CH_ORDERS ก่อน', bad)


def write_channels(raw, asof, dry=False):
    """เขียนอาเรย์ช่องทางลงทั้ง 2 หน้าให้ค่าตรงกัน — คืน (report, changed)"""
    agg = channel_months(raw, asof)
    check_unmapped(agg)
    rep, changed = {}, False
    for page in MAIN_PAGES:
        fp = BASE / page
        if not fp.exists(): die('ไม่พบไฟล์', page)
        t0 = t = fp.read_text(encoding='utf-8')
        m5 = re.search(r'const\s+M5\s*=\s*\[([^\]]*)\]', t)
        if not m5: die('ไม่พบ M5 (ชื่อเดือน)', page)
        nmo = len([x for x in m5.group(1).split(',') if x.strip()])
        yr = max(agg)[:4] if agg else None
        mos = [f'{yr}-{i:02d}' for i in range(1, nmo + 1)]
        for name, chans in {**CH_ARRAYS, **CH_ORDERS}.items():
            key = 'n' if name.endswith('_ORD') else 'r'
            vals = [round(sum(agg.get(mo, {}).get(c, {}).get(key, 0) for c in chans), 2) for mo in mos]
            vals = [int(v) if v == int(v) else v for v in vals]
            pat = re.compile(r'(const\s+' + name + r'\s*=\s*\[)([^\]]*)(\])')
            mm = pat.search(t)
            if not mm: continue                      # อาเรย์นี้ไม่มีในหน้านี้ -> ข้าม
            old = [x.strip() for x in mm.group(2).split(',') if x.strip()]
            if len(old) != nmo:
                die(f'{name} ใน {page} ยาว {len(old)} ไม่เท่า M5 ({nmo}) — ไม่เขียนทับ')
            new = ','.join(str(v) for v in vals)
            if mm.group(2).strip() != new:
                rep.setdefault(page, {})[name] = {'old': old, 'new': [str(v) for v in vals]}
                t = t[:mm.start(2)] + new + t[mm.end(2):]
        if t != t0:
            changed = True
            if not dry: fp.write_text(t, encoding='utf-8')
    return rep, changed


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true', help='คำนวณและตรวจอย่างเดียว ไม่เขียนไฟล์')
    a = ap.parse_args()

    if not BASE.exists():       die('BASE ไม่พบ — Google Drive ยังไม่ sync?', str(BASE))
    if not PAGE.exists():       die('ไม่พบ Sales_Dashboard.html', str(PAGE))

    sys.path.insert(0, str(BASE))
    try:
        import wibwub_update as W
    except Exception as e:
        die('import wibwub_update ไม่สำเร็จ', f'{type(e).__name__}: {e}')

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from ship_cache import load_shipnity
    raw = load_shipnity(verbose=True)       # อ่าน Excel ~2 นาที / cache hit <1 วิ
    if not raw:
        die('process_shipnity() คืน None — ดู stderr ด้านบน')

    # ── ด่านตรวจ: ยอมให้พังดีกว่าเขียนข้อมูลเสียทับ dashboard ───────────────
    missing = REQUIRED - set(raw)
    if missing:                 die('RAW ขาดคีย์ที่ JS ต้องใช้', sorted(missing))

    n_lines, n_oc = len(raw['lines']), len(raw['order_counts'])
    if n_lines == 0:            die('lines ว่าง')
    if n_lines > 500_000:       die('lines เยอะผิดปกติ — น่าจะ dedup ไม่ทำงาน', n_lines)
    if not raw['date_min'] or raw['date_min'] < '2020-01-01':
        die('date_min เพี้ยน (น่าจะมี date cell เสียหลุดเข้ามา)', raw['date_min'])
    if raw['date_max'] < raw['date_min']:
        die('date_max < date_min', [raw['date_min'], raw['date_max']])

    prev = PAGE.read_text(encoding='utf-8')
    size_mb = round(len(json.dumps(raw, ensure_ascii=False, separators=(',', ':'))) / 1e6, 2)
    if size_mb > 20:            die('RAW ใหญ่ผิดปกติ — ไม่เขียนทับ', f'{size_mb} MB')

    summary = {'lines': n_lines, 'order_counts': n_oc, 'products': len(raw['products']),
               'channels': len(raw['channels']), 'date_min': raw['date_min'],
               'date_max': raw['date_max'], 'raw_mb': size_mb,
               'page_mb_before': round(len(prev) / 1e6, 2)}

    asof = _asof((BASE / MAIN_PAGES[0]).read_text(encoding='utf-8'))
    summary['asof'] = asof

    if a.dry_run:
        rep_ch, ch_changed = write_channels(raw, asof, dry=True)
        ship, _ = write_coverage(raw, asof, dry=True)
        summary['shipnity_coverage'] = ship
        summary['channels_changed'] = {pg: {k: f"{v['old'][-1]} -> {v['new'][-1]}" for k, v in d.items()}
                                       for pg, d in rep_ch.items()}
        print(json.dumps({'status': 'DRY_RUN', **summary}, ensure_ascii=False))
        return 0

    changed = W.update_html(None, None, None, raw) or PAGE.read_text(encoding='utf-8') != prev
    rep_ch, ch_changed = write_channels(raw, asof)
    ship, cov_changed = write_coverage(raw, asof)
    summary['shipnity_coverage'] = ship
    ch_changed = ch_changed or cov_changed
    summary['channels_changed'] = {pg: sorted(d) for pg, d in rep_ch.items()}
    changed = changed or ch_changed
    if changed:
        W.bump_sw()
    summary['page_mb_after'] = round(len(PAGE.read_text(encoding='utf-8')) / 1e6, 2)
    print(json.dumps({'status': 'UPDATED' if changed else 'NO_CHANGE', **summary}, ensure_ascii=False))
    return 0 if changed else 10


if __name__ == '__main__':
    sys.exit(main())
