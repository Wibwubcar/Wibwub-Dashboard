#!/usr/bin/env python3
"""สร้างข้อมูลเมนู "การตลาด vs ยอดขาย" ลง WIBWUB_Dashboard.html + WIBWUB_Mobile.html

รวมค่าการตลาดทุกช่องทางเทียบกับยอดขายรวมรายเดือน

แหล่งข้อมูล
  · Ads Shopee / TikTok / Lazada : `data Ads/ads_daily.json` (รวม spend รายวัน -> รายเดือน)
  · KOL                          : `data Ads/kol_monthly.json` (สร้างโดย kol_fetch.py)
  · ยอดขายรวม                    : TOTAL_REV ในหน้าเว็บ = ผลรวมอาเรย์ช่องทางทั้ง 10 ตัว
  · Facebook Ads / Event         : **ยังไม่มีข้อมูล** -> null = "รอข้อมูล"

กฎที่ตกลงไว้ (ห้ามเปลี่ยนโดยไม่ถาม)
  · ช่องที่ยังไม่มีข้อมูลเป็น null **ห้ามนับเป็น 0** ในสูตร % ต่อยอดขาย
    หน้าเว็บจะขึ้นหมายเหตุว่า % ที่เห็นยังไม่รวม Facebook / Event
  · KOL นับเฉพาะ Status=Done ตามวันที่ทำจ่าย · ยอด "รอจ่าย" แสดงเป็นหมายเหตุแยก
  · ทุกเดือนตัดข้อมูลที่ `asof` เดียวกับฝั่งยอดขาย (SALES_ASOF) ไม่ให้คาบเกี่ยวคนละวัน

⚠️ ชีต KOL มีข้อมูลส่วนบุคคล — ที่นี่อ่านเฉพาะ `kol_monthly.json` ซึ่งเป็นผลรวมรายเดือน
   ห้ามดึงชีตตรงจากไฟล์นี้ และห้ามใส่ชื่อ/เลขบัญชีลงหน้าเว็บหรือ commit เด็ดขาด

**เพิ่มเดือนย้อนหลัง**: แก้ `MONTHS` ด้านล่างให้มีเดือนที่ต้องการ (ต้องมีใน ads_daily.json)
แล้วรันสคริปต์ใหม่ — ไม่ต้องแตะ HTML

ใช้:  python3 scripts/marketing/marketing_update.py [--dry-run] [--all-months]
exit: 0 = อัปเดตแล้ว · 10 = ไม่มีอะไรเปลี่ยน · 2 = ไม่ผ่านด่านตรวจ (ไม่เขียนไฟล์)
"""
import sys, re, json, argparse
from pathlib import Path

BASE = Path('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com'
            '/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All')
ADS = BASE / 'data Ads' / 'ads_daily.json'
KOL = BASE / 'data Ads' / 'kol_monthly.json'
PAGES = ['WIBWUB_Dashboard.html', 'WIBWUB_Mobile.html']

# เดือนที่จะแสดงบนหน้าเว็บ — เพิ่มย้อนหลังได้ที่นี่ที่เดียว (เรียงเก่า -> ใหม่)
MONTHS = ['2026-10']

TH_MON = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
          'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
REV_ARRAYS = ['SH_REV', 'TK_REV', 'LZ_REV', 'FB_REV', 'LINE_REV',
              'WEB_REV', 'CARE_REV', 'MKT_REV', 'BEUK_REV', 'POS_REV']
START = '/* MKT_SPEND:AUTO-START */'
END = '/* MKT_SPEND:AUTO-END */'


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def arr(text, name):
    m = re.search(r'const\s+' + name + r'\s*=\s*\[([^\]]*)\]', text)
    if not m: return None
    try: return [float(x) for x in m.group(1).split(',') if x.strip()]
    except ValueError: return None


def th_label(ym):
    y, m = ym.split('-')
    return f'{TH_MON[int(m) - 1]} {int(y) + 543 - 2500:02d}'      # 2026-10 -> 'ต.ค. 69'


def ads_by_month(days):
    out = {}
    for d, v in days.items():
        o = out.setdefault(d[:7], {'sh': 0.0, 'tk': 0.0, 'lz': 0.0, 'days': 0,
                                   'first': d, 'last': d})
        o['sh'] += sum((v.get('sh_ads', {}).get(x, {}) or {}).get('spend', 0) or 0
                       for x in ('product', 'search', 'live'))
        o['tk'] += sum((v.get('tk_ads', {}).get(x, {}) or {}).get('spend', 0) or 0
                       for x in ('product', 'live'))
        o['lz'] += (v.get('lz_ads', {}) or {}).get('spend', 0) or 0
        o['days'] += 1
        o['first'] = min(o['first'], d); o['last'] = max(o['last'], d)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--all-months', action='store_true',
                    help='แสดงทุกเดือนที่มีข้อมูล (ไว้ดูตัวเลขตอน dry-run)')
    a = ap.parse_args()

    for p in (ADS, KOL):
        if not p.exists(): die('ไม่พบไฟล์แหล่งข้อมูล', str(p))
    ads_raw = json.loads(ADS.read_text(encoding='utf-8'))
    kol_raw = json.loads(KOL.read_text(encoding='utf-8'))
    ads = ads_by_month(ads_raw.get('days') or {})
    if not ads: die('ads_daily.json ไม่มี days')

    pages = {}
    for p in PAGES:
        fp = BASE / p
        if not fp.exists(): die('ไม่พบไฟล์', p)
        pages[p] = fp.read_text(encoding='utf-8')

    dash = pages['WIBWUB_Dashboard.html']
    m = re.search(r"SALES_ASOF\s*=\s*'([\d-]{10})'", pages['WIBWUB_Mobile.html'])
    if not m: die('ไม่พบ SALES_ASOF ใน WIBWUB_Mobile.html')
    asof = m.group(1)

    # ── ยอดขายรวมรายเดือน: ต้องตรงกันทั้ง 2 หน้า ไม่งั้นหยุด ───────────────
    revs = {}
    for p, t in pages.items():
        tot = None
        for n in REV_ARRAYS:
            v = arr(t, n)
            if v is None: die(f'ไม่พบอาเรย์ {n} ใน {p}')
            tot = v if tot is None else [x + y for x, y in zip(tot, v)]
        revs[p] = [round(x, 2) for x in tot]
    if revs[PAGES[0]] != revs[PAGES[1]]:
        die('TOTAL_REV สองหน้าไม่ตรงกัน — รัน shipnity_update.py ก่อน',
            {p: revs[p][-1] for p in PAGES})
    rev = revs[PAGES[0]]
    nmo = len(arr(dash, 'SH_REV') or [])

    want = sorted(ads) if a.all_months else MONTHS
    missing = [x for x in want if x not in ads]
    if missing: die('ไม่มีข้อมูล Ads ของเดือนที่ขอ — ดูช่วงใน ads_daily.json',
                    {'missing': missing, 'available': sorted(ads)})

    rows, notes = [], []
    for ym in want:
        o = ads[ym]
        idx = int(ym[5:7]) - 1                      # อาเรย์ยอดขายเริ่ม ม.ค. = index 0
        if ym[:4] != '2026' or idx >= nmo:
            die('เดือนนี้ยังไม่มีช่องในอาเรย์ยอดขายของหน้าเว็บ', ym)
        k = (kol_raw.get('months') or {}).get(ym) or {}
        kp = (kol_raw.get('pending') or {}).get(ym) or {}
        cov = min(o['last'], asof) if ym == asof[:7] else o['last']
        if o['last'] > asof:
            notes.append(f'{ym}: ข้อมูล Ads ถึง {o["last"]} แต่ตัดที่ {asof} ตาม SALES_ASOF')
        rows.append({
            'm': ym, 'label': th_label(ym), 'i': idx,
            'rev': rev[idx],
            'sh': round(o['sh'], 2), 'tk': round(o['tk'], 2), 'lz': round(o['lz'], 2),
            'fb': None, 'event': None,                      # ยังไม่มีข้อมูล
            'kol': round(k.get('amount', 0.0), 2), 'kol_n': k.get('n', 0),
            'kol_pending': round(kp.get('amount', 0.0), 2), 'kol_pending_n': kp.get('n', 0),
            'cov': cov, 'days': o['days'],
        })

    # ── ด่านตรวจ ────────────────────────────────────────────────────────────
    for r in rows:
        spend = r['sh'] + r['tk'] + r['lz'] + r['kol']
        if spend <= 0: die('ค่าการตลาดรวมเป็น 0 — แหล่งข้อมูลน่าจะหลุด', r['m'])
        if r['rev'] <= 0: die('ยอดขายรวมเป็น 0', r['m'])
        if spend > r['rev']: die('ค่าการตลาดสูงกว่ายอดขาย — ตรวจแหล่งข้อมูลก่อน',
                                 {'m': r['m'], 'spend': spend, 'rev': r['rev']})
        r['spend'] = round(spend, 2)
        r['pct'] = round(spend / r['rev'] * 100, 2)
        r['roi'] = round(r['rev'] / spend, 2)

    data = {'asof': asof, 'missing_sources': ['fb', 'event'],
            'kol_rule': kol_raw.get('rule', ''),
            'kol_fetched': kol_raw.get('fetched_at', ''),
            'ads_note': ads_raw.get('source_note', '')[:160],
            'months': rows}

    summary = {'asof': asof, 'months': [
        {'เดือน': r['label'], 'ครอบถึง': r['cov'], 'วัน': r['days'],
         'ยอดขาย': r['rev'], 'Shopee': r['sh'], 'TikTok': r['tk'], 'Lazada': r['lz'],
         'KOL': r['kol'], 'KOL รอจ่าย': r['kol_pending'],
         'ค่าการตลาดรวม': r['spend'], '%ต่อยอดขาย': r['pct'], 'ยอดขาย/ค่าการตลาด': r['roi']}
        for r in rows], 'notes': notes}

    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **summary}, ensure_ascii=False, indent=1))
        return 0

    block = (START + '\nconst MKT_SPEND = ' +
             json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n' + END)
    changed = False
    for p, t in pages.items():
        if START not in t or END not in t:
            die(f'ไม่พบบล็อก {START} ใน {p} — ต้องแทรก UI ก่อน (ดู marketing_section.py)')
        new = re.sub(re.escape(START) + r'[\s\S]*?' + re.escape(END), lambda _: block, t)
        if new != t:
            (BASE / p).write_text(new, encoding='utf-8'); changed = True
    if changed:
        # bump_sw.py ทำงานตอน import (ไม่มี main()) จึงต้องเรียกเป็น subprocess
        import subprocess
        r = subprocess.run([sys.executable, str(BASE / 'scripts' / 'bump_sw.py')],
                           capture_output=True, text=True)
        notes.append(r.stdout.strip() if r.returncode == 0
                     else f'bump_sw ไม่สำเร็จ: {r.stderr.strip()[:120]}')
    print(json.dumps({'status': 'UPDATED' if changed else 'NO_CHANGE', **summary},
                     ensure_ascii=False))
    return 0 if changed else 10


if __name__ == '__main__':
    sys.exit(main())
