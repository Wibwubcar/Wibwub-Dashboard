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
from detail_privacy import BASE, Masker, scan, names   # noqa: E402

RAW = {'fb': BASE / 'data Ads' / 'facebook',
       'tk': BASE / 'data Ads' / 'TikTok',
       'sh': BASE / 'data Ads' / 'Shopee',
       'lz': BASE / 'data Ads' / 'Lazada'}
LABEL = {'fb': 'Facebook', 'tk': 'TikTok', 'sh': 'Shopee', 'lz': 'Lazada'}
OUT = BASE / 'data Ads'
METRICS = ['spend', 'imp', 'reach', 'clicks', 'msg', 'view', 'atc', 'checkout',
           'orders', 'revenue']


# ช่องทางที่สั่งรายงาน **ทีละวัน** — รอบที่ได้ไม่ครบต้องไม่ลบวันเก่าทิ้ง
# ช่องทางที่ "หนึ่งแถว = หนึ่งวัน" จึงสะสมย้อนหลังได้ (ผู้ใช้สั่งให้ครบทุกช่องทาง 6 พ.ย. 69)
#
# `lz` ไม่อยู่ในนี้โดยเจตนา: รายงาน Lazada ไม่คืนคอลัมน์วันที่ หนึ่งแถวคือ **ยอดรวมของทั้งช่วง**
# (ฟิลด์ `span`) ถ้าเอามา merge ตามวัน ช่วงที่คาบกันจะถูกบวกซ้ำ · วิธีย้อนหลังของ Lazada
# คือ export ช่วงยาว (รองรับ 90 วันต่อไฟล์) แล้วใช้ไฟล์ช่วงใหม่สุดใบเดียวตามเดิม
MERGE_BY_DAY = ('sh', 'tk', 'fb')
MERGE_PARTS = ('rows', 'audience', 'placement')
KEEP_DAYS = 70          # ต้องครอบ "เดือนก่อน" ทั้งเดือน + เดือนนี้ (31+31 = 62 วัน) เผื่อ 8 วัน


def merge_by_day(fp, parts):
    """รวมของรอบนี้กับของเดิมทีละส่วน: วันที่รอบนี้ได้ = ใช้ของใหม่ทับทั้งวัน

    5 พ.ย. 69 รอบ 21:00: Lazada ติด CAPTCHA ได้แค่ 29 ต.ค. ใบเดียว ถ้าเขียนทับตรง ๆ
    ข้อมูล 1–4 พ.ย. ที่มีอยู่จะหายทั้งก้อน — ผู้ใช้สั่งว่าให้ "ใช้ข้อมูลเดิม" แทน
    6 พ.ย. 69 ขยายให้ครอบ `audience`/`placement` ด้วย ไม่ใช่แค่ `rows` — ไม่งั้นส่วนเจาะ
    กลุ่มผู้ชมจะเหลือแค่ช่วงที่รอบล่าสุดดึงมา (7 วัน) ทั้งที่ rows ย้อนไปถึง 70 วัน

    `parts` = {ชื่อส่วน: แถวของรอบนี้} · คืน ({ชื่อส่วน: แถวที่รวมแล้ว}, วันที่ยืมของเดิมมา)
    วันตัดคิดจาก "วันใหม่สุดของทุกส่วนรวมกัน" ครั้งเดียว เพื่อให้ทุกส่วนตัดที่วันเดียวกัน
    """
    try:
        old = json.loads(fp.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return parts, []
    new_days = {r['d'] for v in parts.values() for r in v if r.get('d')}
    merged = {}
    for name, rows in parts.items():
        prev = old.get(name) or []
        merged[name] = rows + [r for r in prev if r.get('d') and r['d'] not in new_days]
    alld = {r['d'] for v in merged.values() for r in v if r.get('d')}
    if not alld:
        return parts, []
    cut = (datetime.strptime(max(alld), '%Y-%m-%d')
           - timedelta(days=KEEP_DAYS - 1)).strftime('%Y-%m-%d')
    for name in merged:
        merged[name] = [r for r in merged[name] if r.get('d') and r['d'] >= cut]
    kept = {r['d'] for v in merged.values() for r in v if r.get('d')}
    return merged, sorted(kept - new_days)


def drop_nulls(rows):
    """ตัดคีย์ที่เป็น null ออก — ลดขนาดไฟล์ ~30% โดยไม่เสียความละเอียด

    39% ของคีย์ในชั้นกลุ่มผู้ชมของ Facebook เป็น null (วัดจริง 6 พ.ย. 69) เพราะทุกแถว
    พาคีย์ตัววัดมาครบ 11 ตัวทั้งที่ช่องทางนั้นวัดได้ไม่กี่ตัว
    **ความหมายไม่เปลี่ยน**: หน้าเว็บเช็ค `v==null` ซึ่งเป็น true ทั้ง null และ undefined
    (ตรวจ dAdd() แล้ว) · คีย์ที่ "หายไป" จึงอ่านได้ว่า "วัดไม่ได้" เหมือนเดิม
    ห้ามเอาไปใช้แทนการเขียน 0 — 0 แปลว่าวัดแล้วได้ศูนย์ ซึ่งคนละความหมาย
    """
    return [{k: v for k, v in r.items() if v is not None} for r in rows]


# ───────── กลุ่มผู้ชม/ตำแหน่ง: รายสัปดาห์ (ผู้ใช้เลือก 6 พ.ย. 69) ─────────
# ที่มา: ถ้าเก็บรายวัน 62 วัน ไฟล์ Facebook จะโต ~18 MB (กลุ่มผู้ชม 10.4 + ตำแหน่ง 7.0)
# และหน้าเว็บโหลดไฟล์ทั้ง 4 ช่องทางพร้อมกันตอนเปิดหน้า แบบ no-store ทุกครั้ง
# รวมรายสัปดาห์แล้วเหลือ ~0.8 + 0.6 MB (-84%/-81%) · ชั้น rows ยังรายวันตามเดิม
WEEK_KEY = {'audience': ('c', 'age', 'gender'), 'placement': ('c', 'p')}


def week_start(d):
    """วันจันทร์ของสัปดาห์นั้น **แต่ไม่ให้คาบเดือน** — จันทร์อยู่เดือนก่อน ใช้วันที่ 1

    พรีเซ็ตหลักของหน้านี้คือ "เดือนนี้" / "เดือนก่อน" ถ้าถังสัปดาห์คาบสองเดือน
    การเลือกเดือนจะได้ยอดของเดือนอื่นปนมาทุกครั้ง แก้ไม่ได้ที่ฝั่งหน้าเว็บ
    """
    t = datetime.strptime(d, '%Y-%m-%d')
    w = t - timedelta(days=t.weekday())
    return max(w, t.replace(day=1)).strftime('%Y-%m-%d')


def to_weekly(rows, keyf):
    """รวมแถวรายวันเป็นรายสัปดาห์ · null ยังเป็น null (ไม่มีใครวัด ไม่ใช่ศูนย์)

    แต่ละถังพา `to` (วันสุดท้ายที่มีข้อมูลจริงในถัง) และ `n` (จำนวนวัน) มาด้วย
    หน้าเว็บใช้ `d`..`to` ตัดสินว่าถังนี้ทับช่วงที่เลือกไหม แบบเดียวกับ span ของ Lazada
    """
    agg = {}
    for r in rows:
        if not r.get('d'):
            continue
        k = (week_start(r['d']),) + tuple(r.get(f) for f in keyf)
        o = agg.get(k)
        if o is None:
            o = agg[k] = dict(zip(('d',) + keyf, k), _days=set(), **blank())
        o['_days'].add(r['d'])
        for m in METRICS:
            v = r.get(m)
            if v is None:
                continue
            o[m] = v if o[m] is None else o[m] + v
    out = []
    for o in agg.values():
        ds = o.pop('_days')
        o['to'], o['n'] = max(ds), len(ds)
        for m in METRICS:
            if o[m] is not None:
                o[m] = round(o[m], 6)
        out.append(o)
    return sorted(out, key=lambda x: (x['d'], -(x.get('spend') or 0)))


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


def all_by_level(paths, levels, per_account=False):
    """จัดไฟล์เข้าระดับ แล้วคืน **ทุกใบ** เรียงเก่า -> ใหม่ตาม mtime

    ต่างจาก by_level() ที่เหลือใบใหม่สุดใบเดียว — การเติมย้อนหลังต้องอ่านหลายใบ
    (ไฟล์ ต.ค. + ไฟล์ พ.ย. ของบัญชีเดียวกัน) ซึ่ง by_level() จะทิ้งใบเก่าทั้งใบ
    เพราะ _base() ตัดวันที่ท้ายชื่อออก ทำให้สองใบได้คีย์เดียวกัน
    การกันนับซ้ำย้ายไปอยู่ชั้นแถวแทน (ดู upsert()) ซึ่งกันได้ทั้ง
    ไฟล์ซ้ำเป๊ะ · ไฟล์ `(1)` ของเบราว์เซอร์ · และไฟล์ช่วงที่คาบกัน
    คืน {ระดับ: [พาธเรียงเก่า->ใหม่]} และกลุ่มบัญชีของแต่ละไฟล์ (per_account)
    """
    out = {}
    for p in sorted(paths, key=lambda x: (x.stat().st_mtime, x.name)):
        lv = next((name for name, rx in levels if re.search(rx, _norm(p.stem))), None)
        if lv:
            out.setdefault(lv, []).append(p)
    return out


def read_many(files, parse, key):
    """อ่านหลายไฟล์ — **ในไฟล์เดียวบวกรวม · ข้ามไฟล์ทับด้วยใบใหม่**

    ต้องแยกสองชั้น (เจอจริง 6 พ.ย. 69 ตอนทำด่านกระทบยอด):
      · **ในไฟล์เดียวกัน** รายงาน Facebook แตกแถวตาม `การแสดงโฆษณา`/`วัตถุประสงค์`
        ด้วย ad-day เดียวจึงมีได้หลายแถว (96 คีย์จาก 321) -> ต้อง **บวก**
        ถ้าทับจะหายวันละ ~2,700 บาทแบบไม่มี error (ยอดต่ำกว่า fb_daily ทุกวัน)
      · **ข้ามไฟล์** ช่วงที่คาบกันคือข้อมูลเดิมที่ดึงซ้ำ -> ต้อง **ทับด้วยใบใหม่**
        เพราะรอบรายวันดึงทับย้อนหลัง 7 วันทุกรอบ และ Facebook แก้ตัวเลขย้อนหลัง
        (ของเดิมกันนับซ้ำด้วยการเลือกไฟล์ใบใหม่สุดใบเดียว ซึ่งทำให้เติมย้อนหลังไม่ได้)

    `files` ต้องเรียงเก่า -> ใหม่ · `parse(p)` yield แถว · `key(p, row)` คืนตัวระบุ
    """
    out = {}
    for p in files:
        cur = {}
        for row in parse(p):
            k = key(p, row)
            o = cur.get(k)
            if o is None:
                cur[k] = row
                continue
            for m in METRICS:                     # แถวซ้ำในไฟล์เดียว = คนละส่วนของ ad-day
                v = row.get(m)
                if v is not None:
                    o[m] = v if o[m] is None else o[m] + v
        out.update(cur)                           # ใบใหม่ทับใบเก่าทั้งคีย์
    return list(out.values())


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
# ยอดขายของแคมเปญ CPAS อยู่คนละคอลัมน์ — ของที่ลูกค้าซื้อคือสินค้าที่แชร์ไป Shopee
# ไม่ใช่การซื้อบนเพจ ถ้าไม่อ่านคู่นี้ แคมเปญ CPAS จะขึ้น "รอยอด CPAS" ตลอดไป
# และ ROAS ของหน้า Ads จะหายไป 321,758 บาทใน 7 วัน (ตรวจ 6 พ.ย. 69)
FB_CPAS = {'orders': 'การซื้อสินค้าที่แชร์',
           'revenue': 'ค่าคอนเวอร์ชั่นการซื้อสำหรับรายการที่แชร์เท่านั้น'}


def fb_metrics(r):
    m = blank()
    for k, col in FB_COL.items():
        m[k] = num(r.get(col))
    # บวกรวมเป็น "ยอดซื้อที่ Facebook นับ" ชุดเดียว เหมือนการ์ดของหน้าเดิม (purch + omni)
    # แคมเปญหนึ่งมักมีด้านเดียว แต่ 6 แถวใน 7 วันมีทั้งสองจริง จึงต้องบวก ไม่ใช่เลือกอัน
    for k, col in FB_CPAS.items():
        v = num(r.get(col))
        if v is not None:
            m[k] = v if m[k] is None else m[k] + v
    return m


# ระดับของไฟล์ FB — เรียง placement -> age_gender -> ad (ดูเหตุผลใน by_level)
FB_LV = [('placement', r'placement'), ('agegender', r'age_?gender'),
         ('ad', r'_ad_\d|_ad$')]


def _fb_day(r):
    return (r.get('เริ่มการรายงาน') or '').strip()


def build_fb(src):
    f = all_by_level(src.glob('*.csv'), FB_LV, per_account=True)   # FB มี 5 บัญชี

    def ad_rows(p):
        for r in csv.DictReader(p.open(encoding='utf-8-sig')):
            if _fb_day(r):
                yield dict(lv='ad', c=r.get('ชื่อแคมเปญ') or '(ไม่มีชื่อแคมเปญ)',
                           g=r.get('ชื่อชุดโฆษณา') or '', a=r.get('ชื่อโฆษณา') or '',
                           d=_fb_day(r), **fb_metrics(r))

    def ag_rows(p):
        for r in csv.DictReader(p.open(encoding='utf-8-sig')):
            if _fb_day(r):
                yield dict(d=_fb_day(r), c=r.get('ชื่อแคมเปญ') or '',
                           age=r.get('อายุ') or '', gender=r.get('เพศ') or '',
                           **fb_metrics(r))

    def pl_rows(p):
        for r in csv.DictReader(p.open(encoding='utf-8-sig')):
            if _fb_day(r):
                where = ' / '.join(x for x in (r.get('แพลตฟอร์ม'), r.get('ตำแหน่งโฆษณา'),
                                               r.get('แพลตฟอร์มอุปกรณ์')) if x)
                yield dict(d=_fb_day(r), c=r.get('ชื่อแคมเปญ') or '', p=where,
                           **fb_metrics(r))

    rows = read_many(f.get('ad', []), ad_rows,
                     lambda p, r: (_base(p), r['d'], r['c'], r['g'], r['a']))
    aud = read_many(f.get('agegender', []), ag_rows,
                    lambda p, r: (_base(p), r['d'], r['c'], r['age'], r['gender']))
    pla = read_many(f.get('placement', []), pl_rows,
                    lambda p, r: (_base(p), r['d'], r['c'], r['p']))
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
    f = all_by_level(src.glob('*.csv'), TK_LV)

    def day(r):
        d = (r.get('By Day') or '').strip()
        return None if (not d or d == '-') else d

    def ad_rows(p):
        for r in csv.DictReader(p.open(encoding='utf-8-sig')):
            if day(r):
                yield dict(lv='ad', c=mask.mask(r.get('Campaign name') or ''),
                           g=mask.mask(r.get('Ad group name') or ''),
                           a=mask.mask_ad(r.get('Ad name') or ''),
                           d=day(r), **tk_metrics(r))

    def au_rows(p):
        for r in csv.DictReader(p.open(encoding='utf-8-sig')):
            if day(r):
                yield dict(d=day(r), c=mask.mask(r.get('Campaign name') or ''),
                           age=r.get('Age') or '', gender=r.get('Gender') or '',
                           **tk_metrics(r))

    def pl_rows(p):
        for r in csv.DictReader(p.open(encoding='utf-8-sig')):
            if day(r):
                yield dict(d=day(r), c=mask.mask(r.get('Campaign name') or ''),
                           p=r.get('Placement') or '', **tk_metrics(r))

    rows = read_many(f.get('ad', []), ad_rows, lambda p, r: (r['d'], r['c'], r['g'], r['a']))
    aud = read_many(f.get('audience', []), au_rows,
                    lambda p, r: (r['d'], r['c'], r['age'], r['gender']))
    pla = read_many(f.get('placement', []), pl_rows, lambda p, r: (r['d'], r['c'], r['p']))
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
            got, borrowed = merge_by_day(fp, {'rows': rows, 'audience': aud,
                                              'placement': pla})
            rows, aud, pla = got['rows'], got['audience'], got['placement']
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
        # หมายเหตุความครอบคลุมของ TikTok (ผู้ใช้สั่ง 6 พ.ย. 69) — เขียนจากข้อมูลจริง
        # ไม่ใช่วันที่ตายตัว เพราะสองชั้นนี้จะสะสมเองทุกวันจากนี้ไป
        if ch == 'tk':
            a_days = sorted({r['d'] for r in aud if r.get('d')})
            r_days = sorted({r['d'] for r in rows if r.get('d')})
            if a_days and r_days and a_days[0] > r_days[0]:
                d0 = '%s/%s/%s' % (a_days[0][8:10], a_days[0][5:7], a_days[0][:4])
                notes = notes + [
                    'กลุ่มผู้ชมและตำแหน่งของ TikTok มีข้อมูลตั้งแต่ %s เป็นต้นไปเท่านั้น '
                    '(รายงานชุดนี้ตั้งช่วงไว้ 7 วันล่าสุด ดึงย้อนหลังไม่ได้) '
                    'จะสะสมเพิ่มเองวันละวันจากนี้ไป — เลือกช่วงที่เก่ากว่านี้ '
                    'สองบล็อกนั้นจะว่างหรือไม่ครบช่วง' % d0,
                    'ชั้นรายแอดของเดือนก่อน ๆ ไม่ครบ 100% ของค่าโฆษณา — '
                    'แอดที่ถูกลบไปแล้วไม่ปรากฏในรายงานย้อนหลัง ยิ่งเดือนเก่ายิ่งหายมาก '
                    '(ต.ค. 69 ชั้นรายแอดครอบ ~63% ของค่าโฆษณาทั้งเดือน) '
                    'ใช้จัดอันดับและดูแนวโน้มได้ แต่ยอดรวมของช่องทางให้ยึดการ์ดด้านบน '
                    'ซึ่งมาจากรายงานระดับแคมเปญคนละชุด']
        # รวมรายสัปดาห์ **หลัง** merge — merge ต้องเทียบรายวันก่อน ไม่งั้นสัปดาห์ที่ยัง
        # ไม่ครบจะถูกถังใหม่ที่มีวันเดียวทับทั้งถัง (ข้อมูลหายแบบไม่มี error)
        aud_w, pla_w = to_weekly(aud, WEEK_KEY['audience']), to_weekly(pla, WEEK_KEY['placement'])
        doc = {'channel': ch, 'label': LABEL[ch],
               'fetched_at': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
               'data_asof': days[-1], 'range': rng,
               'caps': {'audience': bool(aud), 'placement': bool(pla),
                        # บอกหน้าเว็บว่าสองชั้นนี้เป็นรายสัปดาห์ ไม่ใช่รายวัน
                        'grain': {'rows': 'day', 'audience': 'week', 'placement': 'week'},
                        'funnel': [k for k in ('imp', 'clicks', 'msg', 'view', 'atc',
                                               'checkout', 'orders')
                                   if any(r.get(k) is not None for r in rows)]},
               'notes': notes, 'daily': daily, 'rows': drop_nulls(rows),
               'audience': drop_nulls(aud_w), 'placement': drop_nulls(pla_w)}
        if borrowed:
            # ย้อนหลังได้หลายสิบวัน ถ้าไล่ชื่อวันทั้งหมดจะยาวเกินอ่าน -> บอกเป็นช่วง + จำนวน
            span_txt = ('%s–%s (%d วัน)' % (borrowed[0], borrowed[-1], len(borrowed))
                        if len(borrowed) > 3 else ', '.join(borrowed))
            notes = notes + ['วันที่รอบนี้ไม่ได้ดึงใหม่ ใช้ของรอบก่อน: ' + span_txt]
            doc['notes'] = notes
            print('   %s: ใช้ข้อมูลเดิมของวัน %s (รอบนี้ไม่ได้ดึง)'
                  % (ch, span_txt), file=sys.stderr)
        if a.dry_run:
            print(f'{ch}: rows {len(rows)} · audience {len(aud)}→{len(aud_w)} สัปดาห์ '
                  f'· placement {len(pla)}→{len(pla_w)} สัปดาห์ '
                  f'· {days[0]}..{days[-1]} (dry-run ไม่เขียน)')
            continue
        fp.write_text(json.dumps(doc, ensure_ascii=False) + '\n', encoding='utf-8')
        wrote.append(fp)
        print(f'{ch}: เขียน {fp.name} · {fp.stat().st_size/1e6:.2f} MB · rows {len(rows)} '
              f'· audience {len(aud_w)} สัปดาห์ · placement {len(pla_w)} สัปดาห์ '
              f"· {rng['from']}..{rng['to']}")

    if empty:
        print('ไม่มีไฟล์ดิบให้ทำ: ' + ', '.join(empty))
    if not wrote:
        return 10 if not a.dry_run else 0

    # ด่านชื่อคน **2 ชั้น** (ผู้ใช้สั่ง 6 พ.ย. 69 หลังชื่อจริง 2 ชื่อหลุดเข้าไฟล์ TikTok)
    #   scan()  เดาจากคำนำหน้า — จับชื่อที่ยังไม่เคยเห็น
    #   names() เทียบกับตารางจับคู่ตัวจริง — จับ 100% สำหรับชื่อที่เคยออกเลขแล้ว
    # ชั้นที่ 2 คือชั้นที่จับของหลุดรอบนั้นได้ ส่วนชั้นแรกมองไม่เห็นเพราะเดาแบบเดียวกัน
    hits = scan([str(f) for f in wrote]) + \
        [(a, b, c) for a, b, c, _d in names([str(f) for f in wrote])]
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
