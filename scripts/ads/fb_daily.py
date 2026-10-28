#!/usr/bin/env python3
"""Facebook Ads รายวัน — แหล่งความจริงเดียวของตัวเลข FB ทั้งระบบ

อ่าน  : data Ads/facebook/daily/FBD_*.csv  (1 ไฟล์ = 1 บัญชี · 1 แถว = 1 แคมเปญ x 1 วัน)
เขียน : data Ads/facebook/fb_daily.json   <- ไฟล์เดียว ผู้อ่าน 2 ราย:
          · marketing_update.py            (ads_fb ของหน้า "การตลาด vs ยอดขาย")
          · data Ads/WIBWUB_Ads_Dashboard_new.html  แท็บ Facebook (fetch ตอนเปิดหน้า)

28 ต.ค. 69 — เลิกฝังบล็อก FB_ADS ลง HTML:
  เดิมเขียนบล็อกลง `data Ads/WIBWUB_Ads_Dashboard.html` แต่ไฟล์นั้น **ไม่ได้ถูกฝัง
  ที่ไหนเลย** — `WIBWUB_Dashboard.html` ฝัง iframe ของ `WIBWUB_Ads_Dashboard_new.html`
  (คนละไฟล์) แท็บ Facebook จึงไม่เคยขึ้นให้ใครเห็นตั้งแต่ commit feaf8db
  ไฟล์ `_new` อ่านข้อมูลด้วย fetch อยู่แล้ว (ads_daily.json / ads_periods.json)
  จึงให้แท็บ Facebook อ่าน fb_daily.json ตรง ๆ ไม่ต้องมีขั้นฝังบล็อกอีก
  (ไฟล์เก่ายังมีคนใช้อยู่ในฐานะ "แหล่งข้อมูลรายเดือน": DATA_PERIODS/TK_BREAKDOWN
   ที่ scripts/ads/sync_periods.js แปลงเป็น ads_periods.json — ห้ามลบไฟล์นั้น)

ทำไมต้องมีไฟล์กลาง (27 ต.ค. 69):
  เดิม ads_fb ต้องกรอกมือใน mkt_manual.json ซึ่งไม่มีใครกรอก -> หน้า "การตลาด vs ยอดขาย"
  ขึ้น "รอข้อมูล" ทั้งเดือน ทั้งที่ไฟล์ CSV มีตัวเลขครบ และถ้ากรอกมือคู่กับหน้า Ads
  ก็จะมีตัวเลข FB 2 ชุดที่ไม่มีอะไรบังคับให้ตรงกัน

กติกาตัวเลข (อย่าเปลี่ยนโดยไม่อ่าน):
  · ค่าโฆษณา = คอลัมน์ "จำนวนเงินที่ใช้จ่ายไป (THB)" เท่านั้น ห้ามใช้ไฟล์ยอดรวม FB_*.csv
  · เป้าหมายของแคมเปญ = ค่าที่ "ไม่ว่าง" ของคอลัมน์ "ตัวระบุผลลัพธ์" ของแคมเปญนั้น
    (บางวันว่างเพราะวันนั้นไม่มีผลลัพธ์ ไม่ใช่เพราะเป้าหมายเปลี่ยน)
    ถ้ามีหลายแบบในแคมเปญเดียว ตัดสินด้วยค่าโฆษณา — ดูบล็อก "ตัดสินเป้าหมาย" ใน main()
  · คลิกทั้งหมดไม่มีเป็นคอลัมน์นับ -> ถอดจาก CTR(ทั้งหมด)/100 x อิมเพรสชัน
    ตรวจแล้วปัดเป็นจำนวนเต็มพอดีทุกแถว (คลาดสูงสุด 0.0001) และ spend/clicks ตรงกับ
    คอลัมน์ CPC(ทั้งหมด) ทุกแถว
  · reach บวกข้ามวันไม่ได้ (คนเดิมถูกนับซ้ำ) -> เก็บรายวันไว้เฉย ๆ ให้หน้าเว็บคิด
    "ความถี่เฉลี่ยรายวัน" = Simp/Sreach แล้วเขียนหมายเหตุ ห้ามเอา reach ไปโชว์เป็นยอดรวม
  · CPM/CTR/CPC รายสัปดาห์ให้หน้าเว็บคิดจากผลรวมของสัปดาห์ ไม่ใช่เฉลี่ยค่ารายวัน
    (ค่าเฉลี่ยของอัตราส่วนไม่เท่ากับอัตราส่วนของผลรวม)

กติกาไฟล์ใน data Ads/facebook/daily/ (28 ต.ค. 69):
  · ชื่อ `FBD_<บัญชี>_<id>_<from>_<to>.csv` · **1 บัญชี x 1 เดือน = 1 ไฟล์**
    (เดือน = เดือนของ `from`) ถ้ามีหลายใบของคู่เดียวกัน ใช้ใบที่ `to` ใหม่สุด
  · ก่อนหน้านี้อ่าน glob ทุกไฟล์แล้วบวกรวมกันหมด -> พอมีไฟล์ของบัญชีเดิม 2 ใบ
    (เช่น 01-26 กับ 01-29) ค่าโฆษณา 1-26 ถูกนับ 2 รอบ **และด่านเดิมจับไม่ได้**
    เพราะทั้ง days และ acc_days โตเท่ากัน ผลรวมจึงยังตรงกันเอง
  · ไฟล์คาบเดือน (เช่น 10-01_11-01 ที่ดึงวันที่ 1 พ.ย. เพื่อปิดยอดเดือน ต.ค.)
    ซ้อนกับไฟล์ของเดือนใหม่ -> **ตัดสินเป็น "รายวัน" ว่าวันนั้นเอาจากไฟล์ไหน**
    (เดือนของ `from` ตรงกับเดือนของวันนั้นก่อน แล้วค่อยดู `to` ใหม่สุด)
    แล้วเอา **ทุกแถว** ของวันนั้นจากไฟล์ที่เลือก
    ⚠️ ห้าม dedupe ระดับแถวด้วย (แคมเปญ, วัน) — ไฟล์จริงมีหลายแถวต่อแคมเปญต่อวัน
    (คนละชุดโฆษณา) เคยลองแล้วค่าโฆษณาหายไป 70,562 บาทจาก 292,512 โดยไม่มี error
  · ทุกบัญชีในเดือนเดียวกันต้องมี `to` ตรงกัน ไม่งั้นแปลว่าบัญชีใดบัญชีหนึ่ง
    โหลดไม่สำเร็จ แล้ววันท้าย ๆ จะขาดบัญชีนั้นแบบเงียบ ๆ -> หยุดทันที

ใช้:  python3 scripts/ads/fb_daily.py [--dry-run]
exit: 0 = อัปเดตแล้ว · 10 = ไม่มีอะไรเปลี่ยน · 2 = ไม่ผ่านด่านตรวจ (ไม่เขียนไฟล์)
"""
import sys, re, csv, json, glob, argparse, subprocess
from pathlib import Path
from datetime import datetime, timedelta


def _find_base():
    """ไล่ขึ้นจากตำแหน่งไฟล์นี้จนเจอโฟลเดอร์ All — marker = sw.js + .git

    ห้ามฝังพาธ Mac ตายตัว: งานตั้งเวลาฝั่ง local รันในแซนด์บ็อกซ์ที่ mount โฟลเดอร์ All
    ไว้คนละที่ (/sessions/<ชื่อ>/mnt/All) และชื่อเซสชันเปลี่ยนทุกรอบ
    """
    p = Path(__file__).resolve()
    for d in (p, *p.parents):
        if (d / 'sw.js').is_file() and (d / '.git').exists():
            return d
    raise SystemExit(f'หาโฟลเดอร์ All ไม่เจอ — ไล่ขึ้นจาก {p} แล้วไม่เจอโฟลเดอร์ที่มีทั้ง '
                     'sw.js และ .git · ห้ามเดาพาธ')


BASE = _find_base()
SRC = BASE / 'data Ads' / 'facebook' / 'daily'
OUT = BASE / 'data Ads' / 'facebook' / 'fb_daily.json'
# ไม่มีพาธ HTML แล้ว — หน้าเว็บ fetch ไฟล์ json เอง (ดูหัวไฟล์)

# ชื่อบัญชีที่ผู้ใช้เรียก -> ใช้ในตารางบนหน้าเว็บ (คีย์ = ส่วนที่ 2 ของชื่อไฟล์ FBD_<คีย์>_<id>_...)
ACC_LABEL = {'WibWub-AD-1': 'WibWub AD 1', 'AD-1': 'AD 1', 'AD-2': 'AD 2',
             'AD3': 'AD3 (CPAS)', 'AD-4': 'AD 4'}
# ตัวระบุผลลัพธ์ -> (คีย์สั้น, ป้ายบนหน้าเว็บ, ป้ายของ "ผลลัพธ์", ป้ายของ "ต้นทุนต่อผลลัพธ์")
GOALS = {
    'actions:onsite_conversion.messaging_conversation_started_7d':
        ('msg', 'ข้อความ', 'แชทที่เริ่มขึ้น', 'ต้นทุนต่อแชท'),
    'actions:onsite_conversion.purchase':
        ('purchase', 'ยอดซื้อ (บนเพจ)', 'ยอดซื้อ', 'ต้นทุนต่อออเดอร์'),
    'catalog_segment_actions:omni_purchase':
        ('omni', 'ยอดขาย CPAS (Shopee)', 'ยอดซื้อ', 'ต้นทุนต่อออเดอร์'),
    'actions:onsite_conversion.lead_grouped':
        ('lead', 'ลูกค้าเป้าหมาย', 'lead', 'ต้นทุนต่อ lead'),
}
COL = {
    'd': 'เริ่มการรายงาน', 'camp': 'ชื่อแคมเปญ', 'deliv': 'การแสดงแคมเปญ',
    'obj': 'วัตถุประสงค์', 'res': 'ผลลัพธ์', 'ind': 'ตัวระบุผลลัพธ์',
    'spend': 'จำนวนเงินที่ใช้จ่ายไป (THB)', 'imp': 'อิมเพรสชัน', 'reach': 'การเข้าถึง',
    'ctr_all': 'CTR (ทั้งหมด)', 'lclicks': 'การคลิกลิงก์แบบอินไลน์ในโฆษณา',
    'msg': 'การสนทนาผ่านการส่งข้อความที่เริ่มขึ้น', 'purch': 'การซื้อ',
    'roas': 'ROAS (ผลตอบแทนจากค่าใช้จ่ายในการโฆษณา) ของการซื้อ',
}
# คอลัมน์ "มีก็ใช้ ไม่มีก็ไม่พัง" — เพิ่งเพิ่มใน URL ตอน 28 ต.ค. 69 ไฟล์เก่ายังไม่มี
# · omni_act = จำนวนการซื้อ CPAS · omni_val = มูลค่าการซื้อ CPAS
# · pval     = มูลค่าการซื้อแบบปกติ (บนเพจ) — AD3 ว่าง แต่บัญชีอื่นน่าจะมี
# ทดสอบกับ export จริงของ AD3 1-27 ต.ค.: มูลค่า 1,190,237 / ค่าโฆษณา 48,570.98 = 24.51x
COL_OPT = {
    'omni_act': 'การซื้อสินค้าที่แชร์',
    'omni_val': 'ค่าคอนเวอร์ชั่นการซื้อสำหรับรายการที่แชร์เท่านั้น',
    'pval': 'ค่าคอนเวอร์ชั่นการซื้อ',
}
# คอลัมน์ `catalog_segment_value_omni_purchase_roas` ขอมาได้แต่ค่าออกมาว่างเปล่า
# (หัวคอลัมน์เป็น token ดิบด้วย) -> ROAS ต้องคำนวณเอง = Σมูลค่า ÷ Σค่าโฆษณา
# ตัวเลขรายวันที่บวกข้ามวัน/ข้ามบัญชีได้ (reach ไม่อยู่ในนี้โดยเจตนา — ดูหัวไฟล์)
SUM_KEYS = ['spend', 'imp', 'clicks', 'lclicks', 'msg', 'purch', 'omni', 'lead', 'reach_d',
            'omni_val', 'pval']


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def num(x):
    s = str(x or '').strip().replace(',', '')
    if not s: return 0.0
    try: return float(s)
    except ValueError: die('คอลัมน์ตัวเลขอ่านไม่ได้', s)


FNAME = re.compile(r'^FBD_(.+?)_(\d+)_(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})(?:__.*)?$')


def _days_between(a, b):
    out, cur = [], datetime.strptime(a, '%Y-%m-%d').date()
    last = datetime.strptime(b, '%Y-%m-%d').date()
    while cur <= last:
        out.append(cur.isoformat()); cur += timedelta(days=1)
    return out


def pick_files():
    """([(path, บัญชี, id, from, to)], [ไฟล์ที่ข้าม], {(บัญชี, วัน): path ที่เป็นเจ้าของวันนั้น})

    `__<stamp>` ท้ายชื่อมาจาก download-mover ตอนกันชื่อซ้ำ ไม่ใช่ส่วนของช่วงวันที่
    """
    best, skipped = {}, []
    for fp in sorted(glob.glob(str(SRC / 'FBD_*.csv'))):
        m = FNAME.match(Path(fp).stem)
        if not m:
            die('ชื่อไฟล์ไม่ตรงแพทเทิร์น FBD_<บัญชี>_<id>_<from>_<to>.csv', Path(fp).name)
        key, acct_id, f_from, f_to = m.groups()
        if f_from > f_to:
            die('ช่วงวันที่ในชื่อไฟล์กลับหัว', Path(fp).name)
        gk = (key, f_from[:7])          # 1 บัญชี x 1 เดือน = 1 ไฟล์
        cur, score = best.get(gk), (f_to, Path(fp).stat().st_mtime)
        if cur is None or score > cur[0]:
            if cur: skipped.append(Path(cur[1]).name)
            best[gk] = (score, fp, key, acct_id, f_from, f_to)
        else:
            skipped.append(Path(fp).name)
    if not best:
        die('ไม่พบไฟล์ FBD_*.csv', str(SRC))

    # ด่าน: เดือนเดียวกัน ทุกบัญชีต้องมี to ตรงกัน
    by_mo = {}
    for (key, mo), v in best.items():
        by_mo.setdefault(mo, {})[key] = v[5]
    for mo, accs in sorted(by_mo.items()):
        if len(set(accs.values())) > 1:
            die('เดือนเดียวกันแต่ช่วงวันที่ของแต่ละบัญชีไม่ตรงกัน — น่าจะมีบัญชีที่โหลดไม่สำเร็จ '
                'ให้โหลดบัญชีที่ค้างให้ครบก่อน (ถ้าปล่อยไว้ วันท้าย ๆ จะขาดบัญชีนั้นแบบเงียบ ๆ)',
                {'เดือน': mo, 'to ของแต่ละบัญชี': accs})

    # เจ้าของรายวัน: ไฟล์ที่เดือนของ from ตรงกับเดือนของวันนั้นก่อน แล้วค่อย to ใหม่สุด
    owner, oscore = {}, {}
    for _, fp, key, _, f_from, f_to in best.values():
        for d in _days_between(f_from, f_to):
            s = (1 if f_from[:7] == d[:7] else 0, f_to)
            if (key, d) not in oscore or s > oscore[(key, d)]:
                oscore[(key, d)] = s; owner[(key, d)] = fp
    out = [(v[1], v[2], v[3], v[4], v[5]) for v in sorted(best.values(), key=lambda v: (v[4], v[2]))]
    return out, sorted(skipped), owner


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    files, skipped, owner = pick_files()

    accounts, camps, acc_days, days = {}, {}, {}, {}
    seen_goal = {}          # (acc, campaign) -> ตัวระบุผลลัพธ์ที่ใช้เป็นเป้าหมาย
    ind_spend = {}          # (acc, campaign) -> {ตัวระบุ: ค่าโฆษณาของแถวที่มีตัวระบุนั้น}
    cpas_sum = {}           # (acc, campaign) -> จำนวนการซื้อ CPAS รวม (ใช้เดาเป้าหมาย)
    have_opt = {}           # ชื่อคอลัมน์ทางเลือก -> มีในไฟล์ไหม
    rows_all = []
    not_mine = 0            # แถวที่วันนั้นเป็นของไฟล์อื่น (ช่วงคาบเดือน)
    for fp, key, acct_id, f_from, f_to in files:
        with open(fp, encoding='utf-8-sig', newline='') as fh:
            rows = list(csv.DictReader(fh))
        if not rows: die('ไฟล์ว่าง', Path(fp).name)
        miss = [c for c in COL.values() if c not in rows[0]]
        if miss: die('ไฟล์ขาดคอลัมน์ที่ต้องใช้', {'file': Path(fp).name, 'missing': miss})
        for ok, oc in COL_OPT.items():
            have_opt[ok] = have_opt.get(ok, True) and (oc in rows[0])
        # 1 รายการ = 1 บัญชี ไม่ใช่ 1 ไฟล์ — ตั้งแต่ backfill ย้อนหลัง (28 ต.ค. 69)
        # บัญชีหนึ่งมีไฟล์เดือนละใบ ถ้า append ต่อไฟล์ accounts จะยาว 44 รายการ
        # แล้วหน้า Ads จะขึ้น "44 บัญชี" และวาดตารางซ้ำบัญชีเดิม 9-10 รอบ
        ac = accounts.setdefault(key, {'key': key, 'label': ACC_LABEL.get(key, key),
                                       'id': acct_id, 'files': [], 'rows': 0, 'months': []})
        ac['files'].append(Path(fp).name); ac['rows'] += len(rows); ac['months'].append(f_from[:7])
        for r in rows:
            d = (r[COL['d']] or '').strip()
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', d):
                die('วันที่ในคอลัมน์ "เริ่มการรายงาน" ผิดรูปแบบ', {'file': Path(fp).name, 'd': d})
            if not (f_from <= d <= f_to):
                die('ไฟล์มีแถวที่อยู่นอกช่วงวันที่ในชื่อไฟล์ — ชื่อไฟล์กับข้อมูลไม่ตรงกัน',
                    {'file': Path(fp).name, 'row_date': d})
            # วันนี้เป็นของไฟล์อื่น (ช่วงที่ 2 ไฟล์คาบกัน) -> ข้ามทั้งแถว ห้ามบวกซ้ำ
            if owner.get((key, d)) != fp:
                not_mine += 1
                continue
            rows_all.append((key, r))
            if COL_OPT['omni_act'] in r:
                k2 = (key, r[COL['camp']])
                cpas_sum[k2] = cpas_sum.get(k2, 0.0) + num(r[COL_OPT['omni_act']])
            ind = (r[COL['ind']] or '').strip()
            if ind:
                if ind not in GOALS:
                    die('เจอตัวระบุผลลัพธ์ที่ยังไม่รู้จัก — ต้องเพิ่มใน GOALS ก่อน',
                        {'file': Path(fp).name, 'ind': ind})
                k = (key, r[COL['camp']])
                e = ind_spend.setdefault(k, {})
                e[ind] = e.get(ind, 0.0) + num(r[COL['spend']])

    # ── ตัดสินเป้าหมายของแต่ละแคมเปญ ─────────────────────────────────────────
    # เดิมเจอตัวระบุ 2 แบบในแคมเปญเดียว = die ทันที ซึ่งถูกตอนมีข้อมูลเดือนเดียว
    # แต่พอ backfill ย้อน 10 เดือน (28 ต.ค. 69) เจอแคมเปญวัตถุประสงค์ "การมีส่วนร่วม"
    # ที่วันเดียวมี 2 ชุดโฆษณาให้ผลคนละแบบ (1 แชท + 1 การซื้อ จาก 4,288 บาททั้งเดือน)
    # — ไม่ใช่การเปลี่ยนเป้าหมาย แค่ผลพลอยได้ของแคมเปญที่ไม่ได้ยิงเพื่อคอนเวอร์ชั่น
    # กติกา: ตัวระบุที่กินค่าโฆษณา >= 80% ของแถวที่มีตัวระบุ = เป้าหมายของแคมเปญ
    #        ไม่ถึงนั้น = ไม่ชี้เป้าหมายเดียว ('none') ให้หน้าเว็บจัดลงกลุ่ม "อื่น ๆ"
    #        แต่ถ้าแคมเปญนั้นใช้เงินเกิน 20,000 บาท ให้หยุด — เงินระดับนั้นต้องมีคนดูก่อน
    mixed = []
    camp_spend_all = {}
    for key, r in rows_all:
        k = (key, r[COL['camp']])
        camp_spend_all[k] = camp_spend_all.get(k, 0.0) + num(r[COL['spend']])
    for k, e in ind_spend.items():
        top, tv = max(e.items(), key=lambda x: x[1])
        tot_i = sum(e.values())
        if len(e) == 1 or (tot_i and tv / tot_i >= 0.8):
            seen_goal[k] = top
            if len(e) > 1:
                mixed.append({'acc': k[0], 'camp': k[1], 'ใช้': top.split(':')[-1],
                              'สัดส่วน': round(tv / tot_i, 3),
                              'อื่น ๆ': {i.split(':')[-1]: round(v, 2) for i, v in e.items() if i != top}})
            continue
        if camp_spend_all.get(k, 0.0) > 20000:
            die('แคมเปญเดียวมีตัวระบุผลลัพธ์หลายแบบและใช้เงินเกิน 20,000 บาท — '
                'ต้องตัดสินใจก่อนว่าจะใช้อันไหน', {'camp': list(k), 'ค่าโฆษณา': round(camp_spend_all[k], 2),
                                                 'ตัวระบุ': {i.split(':')[-1]: round(v, 2) for i, v in e.items()}})
        mixed.append({'acc': k[0], 'camp': k[1], 'ใช้': 'none (ไม่ชี้เป้าหมายเดียว)',
                      'ค่าโฆษณา': round(camp_spend_all.get(k, 0.0), 2),
                      'ตัวระบุ': {i.split(':')[-1]: round(v, 2) for i, v in e.items()}})

    # ── ประกอบรายวัน + รายแคมเปญ ────────────────────────────────────────────
    for key, r in rows_all:
        d = (r[COL['d']] or '').strip()
        imp = num(r[COL['imp']])
        goal = seen_goal.get((key, r[COL['camp']]), '')
        gk = GOALS[goal][0] if goal else 'none'
        # แคมเปญ CPAS บางตัว "ตัวระบุผลลัพธ์" ว่างทุกวัน แต่มีการซื้อสินค้าที่แชร์จริง
        # (28 ต.ค. 69: 3 แคมเปญของ AD3 = 798 การซื้อ / 442,723 บาท ถูกขึ้นเป็น
        #  "ไม่มีผลลัพธ์ในรายงาน" ทั้งที่มีผลลัพธ์) -> เดาเป้าหมายจากคอลัมน์นี้แทน
        if gk == 'none' and cpas_sum.get((key, r[COL['camp']]), 0) > 0:
            gk, goal = 'omni', 'catalog_segment_actions:omni_purchase'
        oa = num(r[COL_OPT['omni_act']]) if COL_OPT['omni_act'] in r else None
        # คลิกทั้งหมด: ไม่มีคอลัมน์นับ ถอดจาก CTR(ทั้งหมด) (ตรวจแล้วเป็นจำนวนเต็มพอดี)
        clicks = round(num(r[COL['ctr_all']]) / 100 * imp)
        res = num(r[COL['res']])
        rec = {'spend': num(r[COL['spend']]), 'imp': imp, 'clicks': clicks,
               'lclicks': num(r[COL['lclicks']]), 'msg': num(r[COL['msg']]),
               'purch': num(r[COL['purch']]),
               # ยอดซื้อ CPAS เกิดที่ Shopee ไม่โผล่ในคอลัมน์ "การซื้อ" ต้องแยกเก็บ
               # มีคอลัมน์นับตรง ๆ ก็ใช้เลย แม่นกว่าการอ่าน "ผลลัพธ์" ตามเป้าหมาย
               'omni': (oa if oa is not None else (res if gk == 'omni' else 0.0)),
               'lead': res if gk == 'lead' else 0.0,
               'reach_d': num(r[COL['reach']]),
               'omni_val': num(r[COL_OPT['omni_val']]) if COL_OPT['omni_val'] in r else 0.0,
               'pval': num(r[COL_OPT['pval']]) if COL_OPT['pval'] in r else 0.0}
        for bucket in (days.setdefault(d, dict.fromkeys(SUM_KEYS, 0.0)),
                       acc_days.setdefault(key, {}).setdefault(d, dict.fromkeys(SUM_KEYS, 0.0))):
            for k in SUM_KEYS: bucket[k] += rec[k]
        c = camps.setdefault((key, r[COL['camp']]), {
            'acc': key, 'name': r[COL['camp']], 'goal': gk,
            'goal_label': GOALS[goal][1] if goal else 'ไม่มีผลลัพธ์ในรายงาน',
            'obj': r[COL['obj']], 'deliv': r[COL['deliv']], 'res': 0.0, 'roas_days': [],
            'mo': {}, 'dd': {}, **dict.fromkeys(SUM_KEYS, 0.0)})
        # แคมเปญ CPAS ที่ตัวระบุว่าง: "ผลลัพธ์" ก็ว่างตาม -> ใช้จำนวนการซื้อแทน
        # ⚠️ ต้องใช้ค่าเดียวกันทั้ง c / mo / dd ไม่งั้นยอดรวมของแคมเปญกับยอดที่หน้าเว็บ
        #    บวกจากรายวันจะไม่ตรงกัน (28 ต.ค. 69: เคยต่างกัน 2,061 vs 1,281)
        res_eff = oa if (oa is not None and gk == 'omni' and not res) else res
        c['res'] += res_eff
        c['deliv'] = r[COL['deliv']] or c['deliv']
        for k in SUM_KEYS: c[k] += rec[k]
        # รายเดือน: ตัวเลือกช่วงวันที่ของหน้านี้เลือกเป็น "เดือน" ตารางบัญชี/แคมเปญ
        # จึงต้องมีรายเดือนให้บวก ไม่งั้นพอมีข้อมูลเดือนถัดไปตารางจะโชว์ยอดรวมทุกเดือน
        # ทั้งที่ผู้ใช้เลือกเดือนเดียว (บั๊กแบบเดียวกับที่เคยเจอใน period picker)
        mo = c['mo'].setdefault(d[:7], dict.fromkeys(SUM_KEYS + ['res'], 0.0))
        mo['res'] += res_eff
        for k in SUM_KEYS: mo[k] += rec[k]
        # รายวันของแคมเปญ: หน้า _new เลือกช่วงเป็น "วันที่" ไม่ใช่ "เดือน" ถ้ามีแต่รายเดือน
        # ตารางบัญชี/แคมเปญจะคิดเต็มเดือนทั้งที่ผู้ใช้เลือก 7 วัน แล้วไม่ตรงกับการ์ดด้านบน
        dd = c['dd'].setdefault(d, dict.fromkeys(SUM_KEYS + ['res'], 0.0))
        dd['res'] += res_eff
        for k in SUM_KEYS: dd[k] += rec[k]
        if r[COL['roas']].strip(): c['roas_days'].append(num(r[COL['roas']]))

    both_val = []
    for c in camps.values():
        # ROAS แบบถูกต้อง = Σมูลค่าการซื้อ ÷ Σค่าโฆษณา (ถ่วงน้ำหนักจริง)
        # ใช้ได้ต่อเมื่อไฟล์มีคอลัมน์มูลค่า ถ้าไม่มีก็ถอยไปใช้ค่าเฉลี่ยรายวันแบบเดิม
        # ซึ่งถ่วงน้ำหนักไม่ได้ (ค่าเฉลี่ยของอัตราส่วน != อัตราส่วนของผลรวม)
        rev = round(c['omni_val'] + c['pval'], 2)
        if c['omni_val'] > 0 and c['pval'] > 0:
            both_val.append(c['name'])     # ถ้าเจอ อาจนับมูลค่าซ้ำ 2 คอลัมน์ ต้องดูก่อนเชื่อ
        c['rev'] = rev
        if rev > 0 and c['spend'] > 0:
            c['roas'] = round(rev / c['spend'], 4); c['roas_src'] = 'value'
        elif c['roas_days']:
            c['roas'] = round(sum(c['roas_days']) / len(c['roas_days']), 4); c['roas_src'] = 'avg'
        else:
            c['roas'] = None; c['roas_src'] = None
        c['roas_n'] = len(c['roas_days'])
        del c['roas_days']
        for k in SUM_KEYS + ['res']: c[k] = round(c[k], 2)
        if c['goal'] == 'none' and c['omni'] > 0:
            c['goal'] = 'omni'; c['goal_label'] = GOALS['catalog_segment_actions:omni_purchase'][1]
        c['mo'] = {m: [round(v[k], 2) for k in SUM_KEYS + ['res']] for m, v in sorted(c['mo'].items())}
        # วันที่ทุกค่าเป็น 0 ไม่ต้องเขียนลงไฟล์ — หน้าเว็บบวกเอา วันที่ไม่มีคีย์ = 0 อยู่แล้ว
        # (28 ต.ค. 69 หลัง backfill 10 เดือน: 7,812 จาก 22,426 วันเป็น 0 ล้วน เพราะแถว
        #  not_delivering ของชุดโฆษณาที่ปิดไปแล้ว ตัดออกได้ ~580 KB จาก 2.1 MB)
        c['dd'] = {d: r for d, r in ((d, [round(v[k], 2) for k in SUM_KEYS + ['res']])
                                     for d, v in sorted(c['dd'].items())) if any(r)}

    for bucket in (days, *acc_days.values()):
        for d in bucket:
            for k in SUM_KEYS: bucket[d][k] = round(bucket[d][k], 2)

    dates = sorted(days)
    tot = {k: round(sum(days[d][k] for d in dates), 2) for k in SUM_KEYS}

    # ── ด่านตรวจ ────────────────────────────────────────────────────────────
    miss_d = [d for d in dates if not days[d]['spend'] and not days[d]['imp']]
    gap = [str(x) for x in _gaps(dates)]
    acc_sum = round(sum(v['spend'] for dd in acc_days.values() for v in dd.values()), 2)
    if abs(acc_sum - tot['spend']) > 0.01:
        die('ผลรวมรายบัญชีไม่เท่าผลรวมรายวัน', {'acc': acc_sum, 'day': tot['spend']})
    camp_sum = round(sum(c['spend'] for c in camps.values()), 2)
    if abs(camp_sum - tot['spend']) > 0.01:
        die('ผลรวมรายแคมเปญไม่เท่าผลรวมรายวัน', {'camp': camp_sum, 'day': tot['spend']})
    # รายวันรายแคมเปญต้องบวกกลับได้เท่ารายวันรวมทุกวัน ไม่งั้นตารางในหน้าเว็บจะไม่ตรงการ์ด
    si = SUM_KEYS.index('spend')
    for d in dates:
        cd = round(sum(c['dd'][d][si] for c in camps.values() if d in c['dd']), 2)
        if abs(cd - days[d]['spend']) > 0.01:
            die('ค่าโฆษณารายวันของแคมเปญรวมไม่เท่ายอดรายวัน',
                {'วันที่': d, 'camp': cd, 'day': days[d]['spend']})

    data = {
        'generated': datetime.now().astimezone().isoformat(timespec='seconds'),
        'from': dates[0], 'to': dates[-1], 'days_n': len(dates),
        'accounts': sorted(accounts.values(), key=lambda a: a['key']), 'goals': {v[0]: {'label': v[1], 'res': v[2], 'cpr': v[3]}
                                        for v in GOALS.values()},
        'keys': SUM_KEYS, 'camp_keys': SUM_KEYS + ['res'],
        'has_value_cols': {k: bool(v) for k, v in have_opt.items()},
        'months': sorted({d[:7] for d in dates}),
        'days': {d: [days[d][k] for k in SUM_KEYS] for d in dates},
        'acc_days': {a: {d: [v[k] for k in SUM_KEYS] for d, v in sorted(dd.items())}
                     for a, dd in acc_days.items()},
        'camps': sorted(camps.values(), key=lambda c: -c['spend']),
        'total': tot,
    }

    summary = {'from': dates[0], 'to': dates[-1], 'days': len(dates),
               'spend_total': tot['spend'],
               'spend_by_account': {a['label']: round(sum(v['spend'] for v in acc_days[a['key']].values()), 2)
                                    for a in accounts.values()},
               'chats': tot['msg'], 'purchases_onsite': tot['purch'], 'purchases_cpas': tot['omni'],
               'มูลค่าการซื้อ CPAS': tot['omni_val'], 'มูลค่าการซื้อบนเพจ': tot['pval'],
               'ROAS ถ่วงน้ำหนัก': (round((tot['omni_val'] + tot['pval']) / tot['spend'], 2)
                                    if tot['spend'] and (tot['omni_val'] + tot['pval']) else None),
               'คอลัมน์มูลค่าที่พบ': {k: bool(v) for k, v in have_opt.items()},
               'แคมเปญที่มีมูลค่าทั้ง 2 คอลัมน์ (เสี่ยงนับซ้ำ)': both_val[:5],
               'แคมเปญที่มีตัวระบุผลลัพธ์หลายแบบ': mixed,
               'leads': tot['lead'], 'campaigns': len(camps),
               'วันที่ขาดช่วง': gap, 'วันที่ไม่มียอดเลย': miss_d,
               'ไฟล์ที่ใช้': [Path(f[0]).name for f in files],
               'ไฟล์ที่ข้าม (ใบเก่าของบัญชี x เดือนเดียวกัน)': skipped,
               'แถวที่ข้ามเพราะวันนั้นเป็นของไฟล์อื่น': not_mine,
               'size_kb': round(len(json.dumps(data, ensure_ascii=False)) / 1024, 1)}

    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **summary}, ensure_ascii=False, indent=1)); return 0

    changed = []
    # เทียบแบบ "ถอด generated ออกแล้วเทียบโครงสร้าง" — ไฟล์เขียนด้วย indent แต่ blob เป็น
    # compact ถ้าเทียบเป็นสตริงตรง ๆ จะไม่เท่ากันทุกครั้ง แล้ว commit ไฟล์เปล่าทุกรอบ
    try:
        old = json.loads(OUT.read_text(encoding='utf-8')) if OUT.exists() else None
    except Exception:
        old = None
    if old is not None: old.pop('generated', None)
    cmp_new = {k: v for k, v in data.items() if k != 'generated'}
    if old != cmp_new:
        OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
        changed.append(OUT.name)

    print(json.dumps({'status': 'UPDATED' if changed else 'NO_CHANGE',
                      'changed': changed, **summary}, ensure_ascii=False))
    return 0 if changed else 10


def _gaps(dates):
    out, cur = [], datetime.strptime(dates[0], '%Y-%m-%d').date()
    have = set(dates)
    last = datetime.strptime(dates[-1], '%Y-%m-%d').date()
    while cur <= last:
        if cur.isoformat() not in have: out.append(cur.isoformat())
        cur += timedelta(days=1)
    return out


if __name__ == '__main__':
    sys.exit(main())
