#!/usr/bin/env python3
"""สร้างข้อมูล **รายวัน** ของเมนู "การตลาด vs ยอดขาย" ลง Dashboard + Mobile

หน้าเว็บคำนวณทุกตัวเลขเองจากข้อมูลรายวันชุดนี้ ตามช่วงวันที่ผู้ใช้เลือก
สคริปต์นี้จึงมีหน้าที่แค่ "รวมแหล่งข้อมูลให้เป็นรายวันที่เชื่อถือได้"

แหล่งข้อมูล (ไฮบริด — ตั้งใจให้ตรงกับหน้าอื่นของ Dashboard)
  · ยอดขาย Shopee/TikTok/Lazada : `data Ads/ads_daily.json` (sh_real/tk_real/lz_real)
      รวมทั้งเดือนแล้วได้เท่ากับ SH_REV / LZ_REV บนหน้าเว็บเป๊ะ ๆ
      -> จึงมีรายวันเฉพาะตั้งแต่ 2026-09-01 (วันแรกของ ads_daily.json)
  · ยอดขายช่องทางที่เหลือ        : Shipnity รายวัน (Facebook, Line, Carcare, Website,
      Marketing, POS, เบิกของ, อื่น ๆ) — map ตาม CH_ARRAYS ของ shipnity_update.py
      ที่เดียว ไม่ก๊อปมาเขียนใหม่ (เคยมีบั๊ก LINE_OA หายไปจากยอดรวม)
  · ค่าโฆษณา                      : `data Ads/ads_daily.json`
  · KOL                           : `data Ads/kol_monthly.json` (จาก kol_fetch.py)
  · Facebook Ads / Event          : ยังไม่มีข้อมูล -> หน้าเว็บขึ้น "รอข้อมูล" และ
      **ไม่นับเป็น 0** ในสูตร % ต่อยอดขาย

⚠️ ชีต KOL มีข้อมูลส่วนบุคคล — ไฟล์นี้อ่านแค่ `kol_monthly.json` ซึ่งมีเฉพาะ
   วันที่ / ยอดเงิน / ชื่อช่อง (handle) / แคมเปญ / สถานะ
   ห้ามดึงชีตตรงจากที่นี่ และห้ามให้ชื่อจริง เลขบัญชี เลขบัตร ที่อยู่ เบอร์โทร หลุดเข้ามา

ใช้:  python3 scripts/marketing/marketing_update.py [--dry-run]
exit: 0 = อัปเดตแล้ว · 10 = ไม่มีอะไรเปลี่ยน · 2 = ไม่ผ่านด่านตรวจ (ไม่เขียนไฟล์)
"""
import sys, re, json, argparse, subprocess
from pathlib import Path

BASE = Path('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com'
            '/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All')
ADS = BASE / 'data Ads' / 'ads_daily.json'
KOL = BASE / 'data Ads' / 'kol_monthly.json'
# ค่าการตลาดที่ยังไม่มีระบบดึงอัตโนมัติ (Event, Facebook Ads) — กรอกมือ ไฟล์อาจยังว่าง
MANUAL = BASE / 'data Ads' / 'mkt_manual.json'
MANUAL_KEYS = ['ads_fb', 'event']
# อัตราค่าธรรมเนียมแพลตฟอร์ม — ผู้ใช้กำหนดเป็นอัตราคงที่ แก้ที่ไฟล์นี้ได้เลย
# ส่งขึ้นหน้าเว็บเป็น fee_rates แล้วหน้าเว็บคูณกับยอดขายรายวันเอง
# เก็บเป็น "อัตรา" ไม่ใช่ "ยอดเงิน" เพราะยอดขายรายวันเปลี่ยนได้ทีหลัง (ออเดอร์ยกเลิก/ยืนยันเพิ่ม)
# ถ้าเก็บยอดเงินไว้จะค้างเป็นค่าเก่าโดยไม่มีใครรู้
FEE = BASE / 'data Ads' / 'platform_fee.json'
PAGES = ['WIBWUB_Dashboard.html', 'WIBWUB_Mobile.html']
START = '/* MKT_SPEND:AUTO-START */'
END = '/* MKT_SPEND:AUTO-END */'

# ช่องทางฝั่ง Shipnity -> คีย์ที่ใช้บนหน้าเว็บ (ชื่ออาเรย์เดิมใน CH_ARRAYS)
SHIP_KEYS = [('fb', 'FB_REV'), ('line', 'LINE_REV'), ('care', 'CARE_REV'),
             ('web', 'WEB_REV'), ('mkt', 'MKT_REV'), ('pos', 'POS_REV'),
             ('beuk', 'BEUK_REV'), ('oth', 'OTH_REV')]
# ลำดับตัวเลขในแต่ละวัน (ย่อให้ไฟล์เล็ก — หน้าเว็บอ่านลำดับจาก MKT_SPEND.keys)
DAY_KEYS = ['sh', 'tk', 'lz'] + [k for k, _ in SHIP_KEYS] + \
           ['ads_sh', 'ads_tk', 'ads_lz', 'kol'] + MANUAL_KEYS


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def arr(text, name):
    m = re.search(r'const\s+' + name + r'\s*=\s*\[([^\]]*)\]', text)
    if not m: return None
    try: return [float(x) for x in m.group(1).split(',') if x.strip()]
    except ValueError: return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    for p in (ADS, KOL):
        if not p.exists(): die('ไม่พบไฟล์แหล่งข้อมูล', str(p))
    ads_raw = json.loads(ADS.read_text(encoding='utf-8'))
    kol_raw = json.loads(KOL.read_text(encoding='utf-8'))
    days_ads = ads_raw.get('days') or {}
    if not days_ads: die('ads_daily.json ไม่มี days')

    pages = {}
    for p in PAGES:
        fp = BASE / p
        if not fp.exists(): die('ไม่พบไฟล์', p)
        pages[p] = fp.read_text(encoding='utf-8')
    dash = pages['WIBWUB_Dashboard.html']

    m = re.search(r"SALES_ASOF\s*=\s*'([\d-]{10})'", pages['WIBWUB_Mobile.html'])
    if not m: die('ไม่พบ SALES_ASOF ใน WIBWUB_Mobile.html')
    asof = m.group(1)

    # ── Shipnity รายวัน (ใช้ CH_ARRAYS ตัวจริง ไม่ reimplement) ───────────────
    sys.path.insert(0, str(BASE / 'scripts'))
    try:
        from ship_cache import load_shipnity
        import shipnity_update as SU
    except Exception as e:
        die('import ship_cache/shipnity_update ไม่สำเร็จ', f'{type(e).__name__}: {e}')
    raw = load_shipnity(verbose=False)
    if not raw: die('load_shipnity คืน None')
    CH = raw['channels']
    ship = {}
    for o in raw['order_counts']:
        d = o['d']
        if d > asof: continue
        s = ship.setdefault(d, {})
        c = CH[o['c']]
        s[c] = s.get(c, 0.0) + o['r']

    # ── ค่าใช้จ่ายที่กรอกมือ (Event / Facebook Ads) ──────────────────────────
    man = {}
    if MANUAL.exists():
        try:
            man = (json.loads(MANUAL.read_text(encoding='utf-8')).get('days') or {})
        except Exception as e:
            die('อ่าน mkt_manual.json ไม่ได้ (JSON เสีย?)', f'{type(e).__name__}: {e}')
        for d, v in man.items():
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', d):
                die('วันที่ใน mkt_manual.json ผิดรูปแบบ ต้องเป็น YYYY-MM-DD', d)
            for k, x in (v or {}).items():
                if k not in MANUAL_KEYS:
                    die('คีย์ที่ไม่รู้จักใน mkt_manual.json — ใช้ได้เฉพาะ ' + ', '.join(MANUAL_KEYS),
                        {d: k})
                if not isinstance(x, (int, float)) or x < 0:
                    die('ยอดใน mkt_manual.json ต้องเป็นตัวเลขไม่ติดลบ', {d: {k: x}})

    # ── KOL รายวัน ───────────────────────────────────────────────────────────
    kol_rows = [r for r in (kol_raw.get('rows') or []) if r.get('d')]
    kol_day = {}
    for r in kol_rows:
        if r['st'] == 'done' and r['d'] <= asof:
            kol_day[r['d']] = round(kol_day.get(r['d'], 0.0) + r['amt'], 2)

    # ── ประกอบรายวัน ────────────────────────────────────────────────────────
    # เดิมตรึงไว้ที่ 2026-09-01 เพราะ ads_daily.json เริ่มเดือน ก.ย.
    # ตอนนี้ปล่อยตามไฟล์จริง เพื่อให้ backfill ย้อนหลังโผล่บนหน้าเองโดยไม่ต้องแก้โค้ดอีก
    d0 = min(days_ads)
    dates = sorted(d for d in days_ads if d0 <= d <= asof)
    if not dates: die('ไม่มีวันในช่วงที่ใช้ได้', {'ads_from': min(days_ads), 'asof': asof})

    rows = {}
    for d in dates:
        v = days_ads[d]
        s = ship.get(d, {})
        rec = [round((v.get('sh_real', {}) or {}).get('gmv', 0) or 0, 2),
               round((v.get('tk_real', {}) or {}).get('gmv', 0) or 0, 2),
               round((v.get('lz_real', {}) or {}).get('gmv', 0) or 0, 2)]
        for _, name in SHIP_KEYS:
            rec.append(round(sum(s.get(c, 0) for c in SU.CH_ARRAYS[name]), 2))
        rec += [round(sum((v.get('sh_ads', {}).get(x, {}) or {}).get('spend', 0) or 0
                          for x in ('product', 'search', 'live')), 2),
                round(sum((v.get('tk_ads', {}).get(x, {}) or {}).get('spend', 0) or 0
                          for x in ('product', 'live')), 2),
                round((v.get('lz_ads', {}) or {}).get('spend', 0) or 0, 2),
                kol_day.get(d, 0.0)]
        rec += [round(float((man.get(d) or {}).get(k, 0) or 0), 2) for k in MANUAL_KEYS]
        rows[d] = rec

    # ── ด่านตรวจ: รวมรายวันของเดือนล่าสุดต้องเท่าอาเรย์รายเดือนบนหน้าเว็บ ────
    checks, idx = {}, int(asof[5:7]) - 1
    for key, name in [('sh', 'SH_REV'), ('lz', 'LZ_REV')] + SHIP_KEYS:
        page_v = (arr(dash, name) or [0] * 12)[idx]
        day_v = round(sum(rows[d][DAY_KEYS.index(key)] for d in dates if d[:7] == asof[:7]), 2)
        checks[name] = {'page': page_v, 'daily': day_v, 'diff': round(day_v - page_v, 2)}
        if page_v and abs(day_v - page_v) > max(1.0, abs(page_v) * 0.001):
            die(f'รายวันรวมแล้วไม่เท่า {name} บนหน้าเว็บ — แหล่งข้อมูลไม่ตรงกัน', checks[name])
    # TikTok ต่างได้บ้าง (ads_daily เป็นยอดก่อนหักยกเลิก · TK_REV หักแล้ว) แต่ไม่เกิน 3%
    tk_page = (arr(dash, 'TK_REV') or [0] * 12)[idx]
    tk_day = round(sum(rows[d][1] for d in dates if d[:7] == asof[:7]), 2)
    checks['TK_REV'] = {'page': tk_page, 'daily': tk_day, 'diff': round(tk_day - tk_page, 2)}
    if tk_page and abs(tk_day - tk_page) > abs(tk_page) * 0.03:
        die('ยอด TikTok รายวันต่างจาก TK_REV เกิน 3%', checks['TK_REV'])

    cov = {'sales': asof, 'shopee': (ads_raw.get('coverage') or {}).get('shopee'),
           'tiktok': (ads_raw.get('coverage') or {}).get('tiktok'),
           'lazada': (ads_raw.get('coverage') or {}).get('lazada'),
           'shipnity': max((d for d in ship), default=None),
           'kol': max((r['d'] for r in kol_rows if r['st'] == 'done'), default=None),
           'kol_fetched': kol_raw.get('fetched_at')}

    # หมวดที่ยังไม่มีข้อมูลเลยในช่วงนี้ -> หน้าเว็บขึ้น "รอข้อมูล" และไม่นับเป็น 0
    # พอ mkt_manual.json มียอดจริง คีย์นั้นจะหลุดออกจาก missing เอง ไม่ต้องแก้โค้ดหน้าเว็บ
    missing = [k for k in MANUAL_KEYS
               if sum(r[DAY_KEYS.index(k)] for r in rows.values()) <= 0]
    man_out = {k: round(sum(r[DAY_KEYS.index(k)] for r in rows.values()), 2) for k in MANUAL_KEYS}

    fee_cfg = json.load(open(FEE, encoding='utf-8')) if FEE.exists() else {}
    fee_rates = fee_cfg.get('rates') or {}
    bad = [k for k in fee_rates if k not in DAY_KEYS]
    if bad:
        die('platform_fee.json มีคีย์ที่ไม่ใช่ช่องทางยอดขาย', bad)
    # อัตราเขียนได้ 2 แบบ: ตัวเลขเดียว (คงที่) หรือ list ของ {from, rate} (เปลี่ยนตามวันที่)
    for k, v in fee_rates.items():
        if isinstance(v, (int, float)):
            if not 0 <= v < 1:
                die('อัตราค่าธรรมเนียมต้องอยู่ระหว่าง 0-1 (0.30 = 30%)', {k: v})
            continue
        if not isinstance(v, list) or not v:
            die('อัตราต้องเป็นตัวเลข หรือ list ของ {from, rate}', {k: v})
        prev = ''
        for s in v:
            if not isinstance(s, dict) or 'from' not in s or 'rate' not in s:
                die('ทุกช่วงต้องมี from และ rate', {k: s})
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(s['from'])):
                die('from ต้องเป็น YYYY-MM-DD', {k: s})
            if not 0 <= s['rate'] < 1:
                die('rate ต้องอยู่ระหว่าง 0-1', {k: s})
            if s['from'] <= prev:
                die('ช่วงอัตราต้องเรียงจากเก่าไปใหม่ ห้ามซ้ำ', {k: s['from']})
            prev = s['from']

    # ค่าการตลาดที่คิดจากอัตรา (คอมแอฟฟิลิเอต ฯลฯ) — base ต้องเป็นช่องทางยอดขายจริง
    mkt_rates = fee_cfg.get('marketing_rates') or {}
    for k, b in mkt_rates.items():
        if b.get('base') not in DAY_KEYS:
            die('marketing_rates.base ต้องเป็นช่องทางยอดขาย', {k: b.get('base')})
        if not isinstance(b.get('rates'), list) or not b['rates']:
            die('marketing_rates ต้องมี rates เป็น list ของ {from, rate}', k)

    data = {'asof': asof, 'from': dates[0], 'to': dates[-1], 'keys': DAY_KEYS,
            'days': rows, 'kol': kol_rows, 'cov': cov,
            'tiers_unmapped': kol_raw.get('tiers_unmapped') or [],
            'fee_rates': fee_rates, 'fee_labels': fee_cfg.get('labels') or {},
            'mkt_rates': mkt_rates,
            'missing': missing}

    tot = {k: round(sum(r[i] for r in rows.values()), 2) for i, k in enumerate(DAY_KEYS)}
    summary = {'asof': asof, 'range': f'{dates[0]} → {dates[-1]}', 'days': len(dates),
               'checks_vs_page': checks, 'totals_whole_range': tot,
               'kol_rows': len(kol_rows), 'tiers_unmapped': data['tiers_unmapped'],
               'manual': man_out, 'still_missing': missing,
               'manual_file': str(MANUAL.relative_to(BASE)),
               'size_kb': round(len(json.dumps(data, ensure_ascii=False)) / 1024, 1)}

    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **summary}, ensure_ascii=False, indent=1)); return 0

    block = (START + '\nconst MKT_SPEND = ' +
             json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n' + END)
    changed = False
    for p, t in pages.items():
        if START not in t or END not in t:
            die(f'ไม่พบบล็อก {START} ใน {p} — รัน marketing_section.py ก่อน')
        new = re.sub(re.escape(START) + r'[\s\S]*?' + re.escape(END), lambda _: block, t)
        if new != t:
            (BASE / p).write_text(new, encoding='utf-8'); changed = True
    notes = []
    if changed:
        r = subprocess.run([sys.executable, str(BASE / 'scripts' / 'bump_sw.py')],
                           capture_output=True, text=True)
        notes.append(r.stdout.strip() if r.returncode == 0
                     else f'bump_sw ไม่สำเร็จ: {r.stderr.strip()[:120]}')
    print(json.dumps({'status': 'UPDATED' if changed else 'NO_CHANGE', **summary,
                      'notes': notes}, ensure_ascii=False))
    return 0 if changed else 10


if __name__ == '__main__':
    sys.exit(main())
