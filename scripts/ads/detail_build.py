#!/usr/bin/env python3
"""แปลงไฟล์รายงานโฆษณาเชิงลึกของ 4 ช่องทาง -> data Ads/ads_detail_{fb,tk,sh,lz}.json

หน้าที่เดียว: อ่านไฟล์ดิบที่งานตั้งเวลาโหลดมา แล้วเขียน JSON ให้หน้า Ads อ่าน
**ไม่เปิดเว็บ ไม่โหลดอะไรเอง ไม่ commit** — ของพวกนั้นเป็นหน้าที่ของพรอมป์

รูปแบบ JSON เหมือนกันทั้ง 4 ช่องทาง หน้าเว็บจะได้ใช้ตัวเรนเดอร์เดียว:
  channel/label · fetched_at · data_asof · range · caps · notes
  daily[]      {d, spend, imp, reach, clicks, msg, view, atc, checkout, orders, revenue}
  rows[]       {c:แคมเปญ, g:ชุดโฆษณา, a:แอด/สินค้า/คีย์เวิร์ด, d:วัน, + เมตริกชุดเดียวกัน}
  audience[]   {d, c, age, gender, + เมตริก}      (เฉพาะ fb/tk)
  placement[]  {d, c, p:ข้อความตำแหน่ง, + เมตริก} (เฉพาะ fb/tk)

กติกาตัวเลข (อย่าเปลี่ยนโดยไม่อ่าน):
  · **reach บวกข้ามวันไม่ได้** เก็บรายวันไว้เฉย ๆ ให้หน้าเว็บคิดความถี่ = Σimp ÷ Σreach
  · อัตราส่วน (CTR/CPC/CPM/ROAS) **ไม่เก็บลง JSON** ให้หน้าเว็บคิดจากผลรวม
    (ค่าเฉลี่ยของอัตราส่วน ≠ อัตราส่วนของผลรวม — กติกาเดียวกับ fb_daily.py)
  · ช่องไหนช่องทางนั้นไม่มีข้อมูลจริง ให้เป็น `null` **ห้ามเติม 0**
    (0 แปลว่า "วัดแล้วได้ศูนย์" ซึ่งคนละเรื่องกับ "ช่องทางนี้วัดไม่ได้")
  · **TikTok: ยอดรวมต้องมาจากระดับแคมเปญ** ระดับแอดขาดยอดของแอดที่ถูกลบ
    (29 ต.ค.–4 พ.ย. ระดับแอด 4,782.60 vs ระดับแคมเปญ 5,225.22) -> daily[] ของ tk
    จึงสร้างจากไฟล์ placement/audience ไม่ใช่จาก rows[]
  · **Lazada: ใช้ยอดขายระดับแคมเปญ** หน้า "รายงานข้อมูล" นับกว้างกว่าจึงสูงกว่า (บันทึกใน notes)

ชื่อครีเอเตอร์ TikTok ถูกแทนด้วยเลขคงที่ผ่าน detail_privacy.Masker ทุกรอบ
และก่อนเขียนไฟล์มีด่าน scan() ซ้ำอีกชั้น — เจอชื่อคน = ไม่เขียนไฟล์ ไม่ให้ commit

ใช้:  python3 scripts/ads/detail_build.py [--only fb,tk,sh,lz] [--probe] [--dry-run]
exit: 0 = เขียนแล้ว · 10 = ไม่มีไฟล์ดิบให้ทำ · 2 = ไม่ผ่านด่าน (ไม่เขียนอะไร)
"""
import sys, csv, json, glob, re, argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent))
from detail_privacy import BASE, Masker, scan          # noqa: E402

RAW = {'fb': BASE / 'data Ads' / 'facebook',
       'tk': BASE / 'data Ads' / 'TikTok',
       'sh': BASE / 'data Ads' / 'Shopee',
       'lz': BASE / 'data Ads' / 'Lazada'}
LABEL = {'fb': 'Facebook', 'tk': 'TikTok', 'sh': 'Shopee', 'lz': 'Lazada'}
OUT = BASE / 'data Ads'
METRICS = ['spend', 'imp', 'reach', 'clicks', 'msg', 'view', 'atc', 'checkout',
           'orders', 'revenue']


def num(v, default=None):
    """'1,234.5' / 'THB 578.25' / '3.36%' / '-' -> float (หรือ default)"""
    if v is None:
        return default
    s = str(v).strip().replace(',', '').replace('THB', '').replace('%', '').strip()
    if s in ('', '-', 'nan', 'None'):
        return default
    try:
        return float(s)
    except ValueError:
        return default


def blank():
    return {k: None for k in METRICS}


def add(dst, src):
    """บวกเมตริกแบบไม่ทำให้ None กลายเป็น 0"""
    for k in METRICS:
        v = src.get(k)
        if v is None:
            continue
        dst[k] = v if dst.get(k) is None else dst[k] + v


def rows_to_daily(rows):
    out = {}
    for r in rows:
        d = out.setdefault(r['d'], blank())
        add(d, r)
    return [dict(d=k, **v) for k, v in sorted(out.items())]


# ───────────────────────── Facebook ─────────────────────────
FB_COL = {'spend': 'จำนวนเงินที่ใช้จ่ายไป (THB)', 'imp': 'อิมเพรสชัน', 'reach': 'การเข้าถึง',
          'clicks': 'จำนวนคลิก (ทั้งหมด)', 'msg': 'การสนทนาผ่านการส่งข้อความที่เริ่มขึ้น',
          'view': 'ยอดดูเนื้อหา', 'atc': 'การหยิบใส่รถเข็น', 'checkout': 'การเริ่มต้นชำระเงิน',
          'orders': 'การซื้อ', 'revenue': 'ค่าคอนเวอร์ชั่นการซื้อ'}


def fb_metrics(r):
    m = blank()
    for k, col in FB_COL.items():
        m[k] = num(r.get(col))
    return m


def build_fb(src):
    rows, aud, pla = [], [], []
    for p in sorted(src.glob('*_ad_*.csv')):
        for r in csv.DictReader(p.open(encoding='utf-8-sig')):
            d = (r.get('เริ่มการรายงาน') or '').strip()
            if not d:
                continue
            rows.append(dict(lv='ad', c=r.get('ชื่อแคมเปญ') or '(ไม่มีชื่อแคมเปญ)',
                             g=r.get('ชื่อชุดโฆษณา') or '', a=r.get('ชื่อโฆษณา') or '',
                             d=d, **fb_metrics(r)))
    for p in sorted(src.glob('*_agegender_*.csv')) + sorted(src.glob('*_camp_agegender_*.csv')):
        for r in csv.DictReader(p.open(encoding='utf-8-sig')):
            d = (r.get('เริ่มการรายงาน') or '').strip()
            if d:
                aud.append(dict(d=d, c=r.get('ชื่อแคมเปญ') or '', age=r.get('อายุ') or '',
                                gender=r.get('เพศ') or '', **fb_metrics(r)))
    for p in sorted(src.glob('*placement*.csv')):
        for r in csv.DictReader(p.open(encoding='utf-8-sig')):
            d = (r.get('เริ่มการรายงาน') or '').strip()
            if d:
                where = ' / '.join(x for x in (r.get('แพลตฟอร์ม'), r.get('ตำแหน่งโฆษณา'),
                                               r.get('แพลตฟอร์มอุปกรณ์')) if x)
                pla.append(dict(d=d, c=r.get('ชื่อแคมเปญ') or '', p=where, **fb_metrics(r)))
    notes = ['ใส่ตะกร้าและเริ่มชำระเงินไม่มีข้อมูล เพราะแคมเปญเป็นแบบข้อความ/มีส่วนร่วม '
             'ไม่มี pixel บนเว็บของร้าน — Funnel จึงเป็น เห็น → คลิก → ทักแชท → ซื้อ',
             'Facebook แก้ตัวเลขย้อนหลังได้ จึงดึงทับย้อนหลัง 7 วันทุกรอบ '
             'และให้ข้อมูลถึงเมื่อวานเท่านั้น']
    return rows, aud, pla, notes


# ───────────────────────── TikTok ─────────────────────────
TK_COL = {'spend': 'Spend', 'imp': 'Impressions', 'reach': 'Reach',
          'clicks': 'Clicks (destination)', 'view': 'Product page views (Shop)',
          'atc': 'Adds to cart (Shop)', 'checkout': 'Checkouts initiated (Shop)',
          'orders': 'Purchases (Shop)', 'revenue': 'Gross revenue (Shop)'}


def tk_metrics(r):
    m = blank()
    for k, col in TK_COL.items():
        m[k] = num(r.get(col))
    return m


def build_tk(src):
    mask = Masker()
    rows, aud, pla = [], [], []
    for p in sorted(src.glob('*ad_daily*.csv')):
        for r in csv.DictReader(p.open(encoding='utf-8-sig')):
            d = (r.get('By Day') or '').strip()
            if not d or d == '-':
                continue
            rows.append(dict(lv='ad', c=mask.mask(r.get('Campaign name') or ''),
                             g=mask.mask(r.get('Ad group name') or ''),
                             a=mask.mask_ad(r.get('Ad name') or ''),
                             d=d, **tk_metrics(r)))
    for p in sorted(src.glob('*audience*.csv')):
        for r in csv.DictReader(p.open(encoding='utf-8-sig')):
            d = (r.get('By Day') or '').strip()
            if d and d != '-':
                aud.append(dict(d=d, c=mask.mask(r.get('Campaign name') or ''),
                                age=r.get('Age') or '', gender=r.get('Gender') or '',
                                **tk_metrics(r)))
    for p in sorted(src.glob('*placement*.csv')):
        for r in csv.DictReader(p.open(encoding='utf-8-sig')):
            d = (r.get('By Day') or '').strip()
            if d and d != '-':
                pla.append(dict(d=d, c=mask.mask(r.get('Campaign name') or ''),
                                p=r.get('Placement') or '', **tk_metrics(r)))
    n = mask.save()
    notes = ['ยอดรวมรายวันของ TikTok มาจากรายงานระดับแคมเปญ — ยอดรวมรายแอดจะต่ำกว่า '
             'เพราะแอดที่ถูกลบไม่ปรากฏย้อนหลัง (29 ต.ค.–4 พ.ย. ต่างกัน 442.62 บาท)',
             'ยอดซื้อและ ROAS ระดับแอดไม่มีข้อมูล — ยอดขายของ TikTok มาทาง GMV Max '
             'ซึ่งเป็นรายงานคนละชุด · Funnel จึงจบที่ ใส่ตะกร้า',
             'ชื่อแอดที่ตั้งตามชื่อครีเอเตอร์ถูกแทนด้วยเลขคงที่']
    if n:
        notes.append(f'รอบนี้พบครีเอเตอร์ใหม่ {n} ราย ออกเลขให้อัตโนมัติแล้ว')
    return rows, aud, pla, notes


# ───────────────────────── Shopee ─────────────────────────
SH_COL = {'spend': 'ค่าโฆษณา', 'imp': 'การมองเห็น', 'clicks': 'จำนวนคลิก',
          'orders': 'การสั่งซื้อ', 'revenue': 'ยอดขาย'}


def _sh_read(p):
    rows = list(csv.reader(p.open(encoding='utf-8-sig')))
    hi = next((i for i, r in enumerate(rows) if r and r[0] == 'ลำดับ'), None)
    if hi is None:
        return None, []
    return rows[hi], rows[hi + 1:]


def _sh_day(p):
    """วันของไฟล์ — ต้องลงท้ายด้วย `_YYYYMMDD` เท่านั้น

    ต้องผูกกับท้ายชื่อแบบเคร่งครัด ไม่งั้นไฟล์ช่วง `..._20261101-05.csv` จะถูกอ่าน
    เป็นข้อมูลของวันที่ 1 พ.ย. ทั้งก้อน (ยอด 5 วันไปกองที่วันเดียว) แบบไม่มี error
    """
    m = re.search(r'_(\d{4})(\d{2})(\d{2})$', p.stem)
    return '-'.join(m.groups()) if m else None


def build_sh(src):
    rows = []
    for p in sorted(src.glob('*keywords*.csv')) + sorted(src.glob('*gms*.csv')):
        d = _sh_day(p)
        if not d:
            continue
        head, body = _sh_read(p)
        if not head:
            continue
        idx = {k: head.index(c) for k, c in SH_COL.items() if c in head}
        gms = 'gms' in p.stem
        for r in body:
            if len(r) < 3:
                continue
            m = blank()
            for k, i in idx.items():
                m[k] = num(r[i]) if i < len(r) else None
            name = r[1]
            if gms:
                # แถวแรกของไฟล์ GMV Max คือ **ยอดรวมทั้งร้าน** (รหัสสินค้า = '-')
                # ถ้าเก็บไปด้วยจะกลายเป็นนับซ้ำกับผลรวมของสินค้า 53 รายการข้างล่าง
                # และซ้ำกับแถว "GMV Max ร้านค้า" ในไฟล์คีย์เวิร์ดอีกชั้น
                if len(r) > 2 and str(r[2]).strip() in ('-', ''):
                    continue
                rows.append(dict(lv='prod', c='GMV Max ร้านค้า', g='', a=name, d=d, **m))
            else:
                kw = r[9] if len(r) > 9 else ''
                is_kw = kw not in ('-', '', 'เลือกอัตโนมัติ', 'ทั้งหมด')
                rows.append(dict(lv='kw' if is_kw else 'camp',
                                 c=name, g='คีย์เวิร์ด' if is_kw else '',
                                 a=kw if is_kw else name, d=d, **m))
    notes = ['Shopee ไม่มีข้อมูลกลุ่มผู้ชมและตำแหน่งโฆษณา',
             'รายงานของ Shopee ไม่มีคอลัมน์วันที่ จึงต้องสั่งทีละวัน — วันที่มาจากชื่อไฟล์',
             'ตัวเลขของวันปัจจุบันยังไม่ปิด ดึงเวลาต่างกันจะได้คนละค่า (เช้า 09:21 vs เย็น '
             'ต่างกัน 14,256 บาท) ไม่ใช่บั๊ก']
    return rows, [], [], notes


# ───────────────────────── Lazada ─────────────────────────
def build_lz(src):
    rows = []
    for p in sorted(src.glob('*.json')):
        try:
            data = json.loads(p.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            continue
        d = _sh_day(p) or ''
        for scene, v in data.items():
            camp = {}
            for c in v.get('camp', []):
                camp[c.get('campaignId')] = c.get('campaignName') or ''
            for a in v.get('ads', []):
                m = blank()
                m['spend'] = num(a.get('spendValue'), num(a.get('spend')))
                m['imp'] = num(a.get('impressionsValue'), num(a.get('impressions')))
                m['clicks'] = num(a.get('clicksValue'), num(a.get('clicks')))
                m['atc'] = num(a.get('storeA2cValue'), num(a.get('storeA2c')))
                m['orders'] = num(a.get('storeOrdersValue'), num(a.get('storeOrders')))
                m['revenue'] = num(a.get('storeRevenueValue'), num(a.get('storeRevenue')))
                rows.append(dict(lv='prod',
                                 c=a.get('campaignName') or camp.get(a.get('campaignId')) or '',
                                 g='', a=a.get('adgroupName') or str(a.get('itemId') or ''),
                                 d=d, **m))
    notes = ['Lazada ไม่มีข้อมูลกลุ่มผู้ชม ตำแหน่งโฆษณา และคีย์เวิร์ด',
             'ยอดขายที่ใช้เป็นยอดระดับแคมเปญ — หน้า "รายงานข้อมูล" ของ Lazada '
             'นับยอดขายแบบกว้างกว่า ตัวเลขจึงสูงกว่า',
             'ไม่มี Reach และ Frequency จึงใช้เกณฑ์ "เปลี่ยนชิ้นงาน" ไม่ได้']
    return rows, [], [], notes


BUILD = {'fb': build_fb, 'tk': build_tk, 'sh': build_sh, 'lz': build_lz}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default='fb,tk,sh,lz')
    ap.add_argument('--probe', action='store_true',
                    help='อ่านจาก detail_probe/ แทน detail_raw/ (ใช้ตอนทดสอบ)')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    sub = 'detail_probe' if a.probe else 'detail_raw'
    wrote, empty = [], []
    for ch in [x.strip() for x in a.only.split(',') if x.strip()]:
        src = RAW[ch] / sub
        rows, aud, pla, notes = BUILD[ch](src) if src.is_dir() else ([], [], [], [])
        if not rows:
            empty.append(ch)
            continue
        days = sorted({r['d'] for r in rows})
        # แหล่งของยอดรวมรายวัน ต้องเป็น "ชั้นบนสุดของช่องทางนั้น" ชั้นเดียว
        # ไม่งั้นแคมเปญกับลูกของมันจะถูกบวกซ้ำ (Shopee เคยได้ 89,381 แทน 31,342)
        if ch == 'tk':
            top = pla or aud or rows          # ระดับแคมเปญ — ระดับแอดขาดแอดที่ถูกลบ
        elif ch == 'sh':
            # แคมเปญโฆษณาค้นหา **ไม่มีแถวระดับแคมเปญของตัวเอง** มีแต่แถวคีย์เวิร์ด
            # (ตรวจแล้ว 5 พ.ย. 69: ชื่อแคมเปญของแถว kw ไม่ซ้ำกับแถว camp เลย)
            # ดังนั้น camp + kw = ยอดจริงพอดี ส่วน prod เป็นลูกของแคมเปญ GMV Max จึงไม่บวก
            top = [r for r in rows if r.get('lv') in ('camp', 'kw')]
        else:
            top = rows                        # fb = ระดับแอด · lz = ระดับสินค้า (ตรงกับแคมเปญ)
        daily = rows_to_daily(top)
        doc = {'channel': ch, 'label': LABEL[ch],
               'fetched_at': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
               'data_asof': days[-1], 'range': {'from': days[0], 'to': days[-1]},
               'caps': {'audience': bool(aud), 'placement': bool(pla),
                        'funnel': [k for k in ('imp', 'clicks', 'msg', 'view', 'atc',
                                               'checkout', 'orders')
                                   if any(r.get(k) is not None for r in rows)]},
               'notes': notes, 'daily': daily, 'rows': rows,
               'audience': aud, 'placement': pla}
        fp = OUT / f'ads_detail_{ch}.json'
        if a.dry_run:
            print(f'{ch}: rows {len(rows)} · audience {len(aud)} · placement {len(pla)} '
                  f'· {days[0]}..{days[-1]} (dry-run ไม่เขียน)')
            continue
        fp.write_text(json.dumps(doc, ensure_ascii=False) + '\n', encoding='utf-8')
        wrote.append(fp)
        print(f'{ch}: เขียน {fp.name} · rows {len(rows)} · audience {len(aud)} '
              f'· placement {len(pla)} · ถึง {days[-1]}')

    if empty:
        print('ไม่มีไฟล์ดิบให้ทำ: ' + ', '.join(empty))
    if not wrote:
        return 10 if not a.dry_run else 0

    hits = scan([str(f) for f in wrote])
    if hits:
        for f in wrote:
            f.unlink(missing_ok=True)
        print('⛔ ด่านชื่อคนไม่ผ่าน %d จุด — ลบไฟล์ที่เพิ่งเขียนแล้ว ห้าม commit' % len(hits))
        for h in hits[:10]:
            print('   ', h[0], '|', h[1], '|', h[2])
        return 2
    print('✅ ด่านชื่อคนผ่าน — commit ได้')
    return 0


if __name__ == '__main__':
    sys.exit(main())
