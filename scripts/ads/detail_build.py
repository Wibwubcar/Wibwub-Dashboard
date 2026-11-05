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

ใช้:  python3 scripts/ads/detail_build.py [--only fb,tk,sh,lz] [--probe] [--dry-run] [--fresh]
exit: 0 = เขียนแล้ว · 10 = ไม่มีไฟล์ดิบให้ทำ · 2 = ไม่ผ่านด่าน (ไม่เขียนอะไร)
"""
import sys, csv, json, glob, re, argparse
from pathlib import Path
from datetime import datetime, timedelta

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


# ช่องทางที่สั่งรายงาน **ทีละวัน** — รอบที่ได้ไม่ครบต้องไม่ลบวันเก่าทิ้ง
MERGE_BY_DAY = ('sh',)
KEEP_DAYS = 30          # เก็บย้อนหลังกี่วันในไฟล์ JSON


def merge_by_day(fp, rows):
    """รวมแถวของรอบนี้กับของเดิม: วันที่รอบนี้ได้ = ใช้ของใหม่ทับทั้งวัน

    5 พ.ย. 69 รอบ 21:00: Lazada ติด CAPTCHA ได้แค่ 29 ต.ค. ใบเดียว ถ้าเขียนทับตรง ๆ
    ข้อมูล 1–4 พ.ย. ที่มีอยู่จะหายทั้งก้อน — ผู้ใช้สั่งว่าให้ "ใช้ข้อมูลเดิม" แทน
    คืน (แถวที่รวมแล้ว, วันที่ยืมของเดิมมา)
    """
    new_days = {r['d'] for r in rows}
    try:
        old = json.loads(fp.read_text(encoding='utf-8')).get('rows', [])
    except (OSError, ValueError):
        return rows, []
    out = rows + [r for r in old if r.get('d') and r['d'] not in new_days]
    cut = (datetime.strptime(max(r['d'] for r in out), '%Y-%m-%d')
           - timedelta(days=KEEP_DAYS - 1)).strftime('%Y-%m-%d')
    out = [r for r in out if r['d'] >= cut]
    return out, sorted({r['d'] for r in out} - new_days)


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


# ──────────────── เลือกไฟล์ดิบ (ชื่อไฟล์ทนทั้ง `-` และ `_`) ────────────────
# 5 พ.ย. 69 รอบ 21:00: พรอมป์ตั้งชื่อ `WIBWUB-auto-fb-AD-1-ad-2026-10-29_2026-11-05.csv`
# แต่ glob เดิมหา `*_ad_*.csv` จึงไม่เจอไฟล์เลยทั้งรอบ (โหลดครบแต่ build ว่าง)
# แก้ที่ฝั่งอ่าน ไม่ใช่ฝั่งตั้งชื่อ — ชื่อไฟล์เปลี่ยนรูปได้อีกในอนาคต
STAMP = re.compile(r'(?:__\d{8}_\d{6}|\s*\(\d+\))$')


def _norm(s):
    """ชื่อไฟล์ -> ตัวพิมพ์เล็ก คั่นด้วย `_` ตัวเดียว (`-`/ช่องว่าง/`_` ถือว่าเท่ากัน)"""
    return re.sub(r'[-_\s]+', '_', str(s).strip().lower())


def _base(p):
    """ชื่อฐานสำหรับจับไฟล์ซ้ำ — ตัดรอยกันชื่อซ้ำของตัวย้ายและวันที่ท้ายชื่อออก

    `WIBWUB-auto-fb-AD-1-ad-2026-10-29_2026-11-05`      -> wibwub_auto_fb_ad_1_ad
    `Tiktok Ads_..._20261029-20261104__20261105_211305`  -> tiktok_ads_..._wibwubcar
    """
    s = _norm(STAMP.sub('', p.stem))
    while re.search(r'_\d+$', s):
        s = re.sub(r'_\d+$', '', s)
    return s


def by_level(paths, levels, per_account=False):
    """จัดไฟล์เข้าระดับตามคำในชื่อ แล้วเหลือ **ใบใหม่สุดของแต่ละกลุ่ม** ใบเดียว

    `levels` ต้องเรียงจากเฉพาะเจาะจงไปกว้าง: ไฟล์ `..._AD-1_age_gender_...` มีคำว่า
    `_ad_` ติดมาจากชื่อบัญชีด้วย ถ้าเช็ค 'ad' ก่อนจะถูกจัดเป็นระดับแอดผิด ๆ

    ด่านไฟล์ซ้ำ (ผู้ใช้สั่ง 5 พ.ย. 69): วัน/ระดับ/บัญชีเดียวกันมีได้หลายใบ —
    ไฟล์ของรอบก่อน ไฟล์ `(1)` ของเบราว์เซอร์ และไฟล์ที่ตัวย้ายเติม stamp กันชื่อซ้ำ
    ถ้าอ่านทุกใบ ยอดจะถูกนับซ้ำเงียบ ๆ (TikTok เคยได้ 10,450.44 แทน 5,225.22)
    """
    best = {}
    for p in sorted(paths):
        s = _norm(p.stem)
        lv = next((name for name, rx in levels if re.search(rx, s)), None)
        if not lv:
            continue
        k = (lv, _base(p)) if per_account else (lv,)
        if k not in best or p.stat().st_mtime > best[k].stat().st_mtime:
            best[k] = p
    out = {}
    for k in sorted(best):
        out.setdefault(k[0], []).append(best[k])
    return out


def newest_per_day(paths, day_of):
    """วันเดียวกันเอาใบใหม่สุด — สำหรับช่องทางที่สั่งรายงานทีละวัน (Shopee/Lazada)"""
    best = {}
    for p in sorted(paths):
        d = day_of(p)
        if not d:
            continue
        if d not in best or p.stat().st_mtime > best[d].stat().st_mtime:
            best[d] = p
    return [(d, best[d]) for d in sorted(best)]


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


# ระดับของไฟล์ FB — เรียง placement -> age_gender -> ad (ดูเหตุผลใน by_level)
FB_LV = [('placement', r'placement'), ('agegender', r'age_?gender'),
         ('ad', r'_ad_\d|_ad$')]


def build_fb(src):
    rows, aud, pla = [], [], []
    f = by_level(src.glob('*.csv'), FB_LV, per_account=True)   # FB มี 5 บัญชี
    for p in f.get('ad', []):
        for r in csv.DictReader(p.open(encoding='utf-8-sig')):
            d = (r.get('เริ่มการรายงาน') or '').strip()
            if not d:
                continue
            rows.append(dict(lv='ad', c=r.get('ชื่อแคมเปญ') or '(ไม่มีชื่อแคมเปญ)',
                             g=r.get('ชื่อชุดโฆษณา') or '', a=r.get('ชื่อโฆษณา') or '',
                             d=d, **fb_metrics(r)))
    for p in f.get('agegender', []):
        for r in csv.DictReader(p.open(encoding='utf-8-sig')):
            d = (r.get('เริ่มการรายงาน') or '').strip()
            if d:
                aud.append(dict(d=d, c=r.get('ชื่อแคมเปญ') or '', age=r.get('อายุ') or '',
                                gender=r.get('เพศ') or '', **fb_metrics(r)))
    for p in f.get('placement', []):
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


# TikTok มีบัญชีเดียว (WIBWUBCAR) และรายงาน 1 ใบครอบทั้งช่วง -> ระดับละใบใหม่สุดใบเดียว
TK_LV = [('placement', r'placement'), ('audience', r'audience'), ('ad', r'ad_daily')]


def build_tk(src):
    mask = Masker()
    rows, aud, pla = [], [], []
    f = by_level(src.glob('*.csv'), TK_LV)
    for p in f.get('ad', []):
        for r in csv.DictReader(p.open(encoding='utf-8-sig')):
            d = (r.get('By Day') or '').strip()
            if not d or d == '-':
                continue
            rows.append(dict(lv='ad', c=mask.mask(r.get('Campaign name') or ''),
                             g=mask.mask(r.get('Ad group name') or ''),
                             a=mask.mask_ad(r.get('Ad name') or ''),
                             d=d, **tk_metrics(r)))
    for p in f.get('audience', []):
        for r in csv.DictReader(p.open(encoding='utf-8-sig')):
            d = (r.get('By Day') or '').strip()
            if d and d != '-':
                aud.append(dict(d=d, c=mask.mask(r.get('Campaign name') or ''),
                                age=r.get('Age') or '', gender=r.get('Gender') or '',
                                **tk_metrics(r)))
    for p in f.get('placement', []):
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
    s = p.stem
    if re.search(r'\d{8}[-_]\d{8}$', s) or re.search(r'\d{8}[-_]\d{1,2}$', s):
        return None          # ไฟล์ช่วงหลายวัน (`..._20261101-20261105` / `..._20261101-05`)
    m = re.search(r'[-_](\d{4})(\d{2})(\d{2})$', s)
    return '-'.join(m.groups()) if m else None


# ชนิดรายงาน Shopee: คีย์เวิร์ด/แคมเปญ = new_cpc_homepage__detail · GMV Max = product_gms__homepage
SH_LV = [('kw', r'keyword|new_cpc'), ('gms', r'gms')]


def _sh_pick(src):
    """คืน [((วัน, ชนิด), ไฟล์)] — วัน+ชนิดเดียวกันเอาใบใหม่สุดใบเดียว"""
    best = {}
    for p in sorted(src.glob('*.csv')):
        n = _norm(p.stem)
        kind = next((k for k, rx in SH_LV if re.search(rx, n)), None)
        d = _sh_day(p)
        if not kind or not d:
            continue
        k = (d, kind)
        if k not in best or p.stat().st_mtime > best[k].stat().st_mtime:
            best[k] = p
    return [(k, best[k]) for k in sorted(best)]


def build_sh(src):
    rows = []
    for (d, kind), p in _sh_pick(src):
        head, body = _sh_read(p)
        if not head:
            continue
        idx = {k: head.index(c) for k, c in SH_COL.items() if c in head}
        gms = kind == 'gms'
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
def _lz_span(p):
    """ช่วงวันของไฟล์ Lazada จากชื่อไฟล์ -> (from, to) หรือ None

    `WIBWUB-auto-lazada-2026-10-30__2026-11-05.json` -> ('2026-10-30', '2026-11-05')
    `WIBWUB-auto-lazada-20261029.json` (แบบเก่า วันเดียว) -> ('2026-10-29', '2026-10-29')
    """
    s = re.sub(r'[^0-9_]', '', p.stem)
    m = re.search(r'(\d{8})__(\d{8})$', s)
    if m:
        a, b = m.group(1), m.group(2)
        return ('%s-%s-%s' % (a[:4], a[4:6], a[6:]), '%s-%s-%s' % (b[:4], b[4:6], b[6:]))
    d = _sh_day(p)
    return (d, d) if d else None


def build_lz(src):
    """Lazada ยิง 1 ครั้งต่อช่วง -> ได้ **ยอดรวมของทั้งช่วง ไม่ใช่รายวัน**

    5 พ.ย. 69: เดิมวนยิงทีละวัน (70 คำขอ/รอบ) แล้วติด CAPTCHA ตั้งแต่วันที่ 2
    ผู้ใช้สั่งให้ยิงช่วงเดียว · endpoint ไม่คืนคอลัมน์วันที่ จึงเก็บเป็นแถวของช่วง
    และ **ไม่สร้าง daily[]** (ห้ามหารเฉลี่ยรายวันเอง — ดู main())

    ไฟล์ใหม่สุดใบเดียวเท่านั้น: รอบที่ติด CAPTCHA จะไม่มีไฟล์ใหม่ สคริปต์จึงใช้
    ไฟล์ของรอบก่อนต่อเอง = "ใช้ข้อมูลเดิม" ตามที่ผู้ใช้สั่ง (ดู data_asof ในรายงาน)
    """
    rows = []
    cand = [(p, _lz_span(p)) for p in sorted(src.glob('*.json'))]
    for p, sp in cand:
        if not sp:
            print('ข้าม %s — อ่านช่วงวันจากชื่อไฟล์ไม่ได้ '
                  '(ต้องลงท้าย -YYYYMMDD__YYYYMMDD)' % p.name, file=sys.stderr)
    ok = [(p, sp) for p, sp in cand if sp]
    ok.sort(key=lambda x: x[0].stat().st_mtime)
    for p, sp in ok[-1:]:
        try:
            data = json.loads(p.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            continue
        d = sp[1]
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
                                 d=d, span='%s..%s' % sp, **m))
    notes = ['Lazada ไม่มีข้อมูลกลุ่มผู้ชม ตำแหน่งโฆษณา และคีย์เวิร์ด',
             'ตัวเลขของ Lazada เป็น **ยอดรวมของทั้งช่วง ไม่ใช่รายวัน** — รายงานของ Lazada '
             'ไม่คืนคอลัมน์วันที่ และการยิงทีละวันทำให้ติด CAPTCHA · '
             'ยอดรายวันของ Lazada มาจากไฟล์ export ของแท็บโฆษณาคนละใบ '
             '(จึงมีกราฟรายวัน แต่ตารางรายสินค้าเป็นยอดของทั้งช่วง)',
             'ยอดขายที่ใช้เป็นยอดระดับแคมเปญ — หน้า "รายงานข้อมูล" ของ Lazada '
             'นับยอดขายแบบกว้างกว่า ตัวเลขจึงสูงกว่า',
             'ไม่มี Reach และ Frequency จึงใช้เกณฑ์ "เปลี่ยนชิ้นงาน" ไม่ได้']
    return rows, [], [], notes


# คอลัมน์ของไฟล์ export แท็บ GMV Max / Storewide Overview ของ Lazada
LZ_DAILY_COL = {'spend': 'ค่าใช้จ่าย', 'revenue': ('รายได้', 'ยอดรายได้'),
                'orders': 'คำสั่งซื้อ', 'imp': 'การแสดงผล', 'clicks': 'คลิก'}


def lz_daily(src):
    """รายวันของ Lazada — จากไฟล์ export ของแท็บโฆษณา (ครอบได้ 90 วันต่อไฟล์)

    ทำไมต้องมีไฟล์นี้: endpoint `adgroupList`/`newCampaignList` **ไม่คืนคอลัมน์วันที่**
    คืนแต่ยอดรวมของช่วง · เดิมแก้ด้วยการยิงทีละวันแล้วติด CAPTCHA (5 พ.ย. 69)
    ไฟล์ export ใบเดียวให้รายวันครบ ไม่ต้องยิงถี่
    ตรวจแล้ว 5 พ.ย. 69: ตรงกับ `lz_ads` ใน ads_daily.json ทุกวัน (169.95 / 202.0 / 206.3)

    คืน [] ถ้าไม่มีไฟล์ — หน้าเว็บจะขึ้นว่า Lazada ไม่มีรายวัน ดีกว่าเดาตัวเลข
    """
    xs = sorted(src.glob('*.xlsx'), key=lambda p: p.stat().st_mtime)
    if not xs:
        return []
    try:
        import openpyxl
    except ImportError:
        print('ข้ามรายวันของ Lazada — ไม่มี openpyxl ในเครื่องนี้', file=sys.stderr)
        return []
    import warnings
    out = []
    for p in xs[-1:]:                      # ใบใหม่สุดใบเดียว (กันไฟล์รอบก่อนนับซ้ำ)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            ws = openpyxl.load_workbook(p, read_only=False).worksheets[0]
        grid = [[c for c in r] for r in ws.iter_rows(values_only=True)]
        hi = next((i for i, r in enumerate(grid)
                   if r and any(str(c).strip() == 'วันที่' for c in r if c is not None)), None)
        if hi is None:
            print('ข้าม %s — ไม่เจอหัวตาราง "วันที่"' % p.name, file=sys.stderr)
            continue
        head = [str(c).strip() if c is not None else '' for c in grid[hi]]
        idx = {}
        for k, names in LZ_DAILY_COL.items():
            for nm in ((names,) if isinstance(names, str) else names):
                if nm in head:
                    idx[k] = head.index(nm); break
        for r in grid[hi + 1:]:
            if not r or r[0] is None:
                continue
            ds = re.sub(r'[^0-9]', '', str(r[0]))
            if len(ds) != 8:
                continue
            m = blank()
            for k, i in idx.items():
                m[k] = num(r[i]) if i < len(r) else None
            out.append(dict(d='%s-%s-%s' % (ds[:4], ds[4:6], ds[6:]), **m))
    return rows_to_daily(out) if out else []


BUILD = {'fb': build_fb, 'tk': build_tk, 'sh': build_sh, 'lz': build_lz}
# ช่องทางที่สร้าง daily[] จากไฟล์ของตัวเอง ไม่ใช่จากผลรวมของ rows[]
DAILY_FROM = {'lz': lz_daily}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default='fb,tk,sh,lz')
    ap.add_argument('--probe', action='store_true',
                    help='อ่านจาก detail_probe/ แทน detail_raw/ (ใช้ตอนทดสอบ)')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--fresh', action='store_true',
                    help='ไม่ยืมวันเก่าจากไฟล์เดิม (ใช้ตอนข้อมูลเดิมผิดและต้องล้าง)')
    a = ap.parse_args()

    sub = 'detail_probe' if a.probe else 'detail_raw'
    wrote, empty = [], []
    for ch in [x.strip() for x in a.only.split(',') if x.strip()]:
        src = RAW[ch] / sub
        rows, aud, pla, notes = BUILD[ch](src) if src.is_dir() else ([], [], [], [])
        if not rows:
            empty.append(ch)
            continue
        fp = OUT / f'ads_detail_{ch}.json'
        borrowed = []
        if ch in MERGE_BY_DAY and not a.fresh:
            rows, borrowed = merge_by_day(fp, rows)
        days = sorted({r['d'] for r in rows})
        # Lazada: แถวเป็นยอดของทั้งช่วง ช่วงจริงอยู่ที่ฟิลด์ span ไม่ใช่ที่ d
        span = next((r['span'] for r in rows if r.get('span')), None)
        rng = ({'from': span.split('..')[0], 'to': span.split('..')[1]} if span
               else {'from': days[0], 'to': days[-1]})
        # แหล่งของยอดรวมรายวัน ต้องเป็น "ชั้นบนสุดของช่องทางนั้น" ชั้นเดียว
        # ไม่งั้นแคมเปญกับลูกของมันจะถูกบวกซ้ำ (Shopee เคยได้ 89,381 แทน 31,342)
        if ch == 'tk':
            top = pla or aud or rows          # ระดับแคมเปญ — ระดับแอดขาดแอดที่ถูกลบ
        elif ch == 'sh':
            # แคมเปญโฆษณาค้นหา **ไม่มีแถวระดับแคมเปญของตัวเอง** มีแต่แถวคีย์เวิร์ด
            # (ตรวจแล้ว 5 พ.ย. 69: ชื่อแคมเปญของแถว kw ไม่ซ้ำกับแถว camp เลย)
            # ดังนั้น camp + kw = ยอดจริงพอดี ส่วน prod เป็นลูกของแคมเปญ GMV Max จึงไม่บวก
            top = [r for r in rows if r.get('lv') in ('camp', 'kw')]
        elif ch == 'lz':
            top = []                          # rows[] เป็นยอดของทั้งช่วง ห้ามเอามาทำรายวัน
        else:
            top = rows                        # fb = ระดับแอด
        daily = DAILY_FROM[ch](src) if ch in DAILY_FROM else rows_to_daily(top)
        doc = {'channel': ch, 'label': LABEL[ch],
               'fetched_at': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
               'data_asof': days[-1], 'range': rng,
               'caps': {'audience': bool(aud), 'placement': bool(pla),
                        'funnel': [k for k in ('imp', 'clicks', 'msg', 'view', 'atc',
                                               'checkout', 'orders')
                                   if any(r.get(k) is not None for r in rows)]},
               'notes': notes, 'daily': daily, 'rows': rows,
               'audience': aud, 'placement': pla}
        if borrowed:
            notes = notes + ['รอบนี้ไม่ได้ข้อมูลของวัน %s จึงใช้ของรอบก่อน'
                             % ', '.join(borrowed)]
            doc['notes'] = notes
            print('   %s: ใช้ข้อมูลเดิมของวัน %s (รอบนี้ไม่ได้)'
                  % (ch, ', '.join(borrowed)), file=sys.stderr)
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
