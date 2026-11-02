#!/usr/bin/env python3
"""สร้างโครงเดือนใหม่ในหน้า Ads รายเดือน (DATA_PERIODS + TK_BREAKDOWN)

ใช้:  python3 scripts/ads/ensure_month.py [--month nov] [--shopee-day N] [--note "..."]
      ไม่ใส่ --month = เดือนปัจจุบัน

ทำไมต้องมี (2 พ.ย. 69): หน้า data Ads/WIBWUB_Ads_Dashboard.html เก็บข้อมูลรายเดือน
เป็นคีย์ 3 ตัวอักษร พอขึ้นเดือนใหม่แล้วไม่มีคีย์ งานที่ดึงข้อมูลมาได้จะเขียนลงไม่ได้
และต้องรอคนมาเติมมือ — เกิดจริงกับ wibwub-download-shopee-ads รอบ 2 พ.ย. 08:22
(ดึงครบ 41 แคมเปญแต่รายงานขึ้น ⛔ เพราะไม่มี DATA_PERIODS.nov)

กติกา:
  · มีคีย์อยู่แล้ว -> ไม่แตะไฟล์เลย (idempotent · เช็คด้วย md5 ได้)
  · ใส่เฉพาะ "โครงว่าง" ค่าเป็นศูนย์ ไม่เดาตัวเลข ให้ขั้นเขียนข้อมูลจริงทับทีหลัง
  · ปุ่มเลือกช่วงกับ entry ของ ADS_PERIOD_DEFS หน้าเว็บสร้างเอง (adsAutoMonths)
  · ห้ามแตะ _redesign / _new — สองไฟล์นั้นอ่าน ads_periods.json ที่ sync_periods.js สร้าง
"""
import argparse, datetime as dt, io, json, os, sys

MK = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
ADS_HTML = 'data Ads/WIBWUB_Ads_Dashboard.html'

ZERO_PLAT = ('{spend:0,revenue:0,orders:0,imp:0,clicks:0,roas:0,ctr:0,cvr:0,cpa:0,'
             'top5:[],worst5:[],all:[]}')
ZERO_TK = ('{\n      gmvLive: { total:{spend:0,orders:0,revenue:0,views:0,roi:0,cpa:0}, sessions:[] },\n'
           '      gmvMax: { total:{spend:0,orders:0,revenue:0,imp:0,clicks:0,roi:0,ctr:0,cvr:0,cpa:0},'
           ' top5:[], worst5:[], campaigns:[] },\n'
           '      bizAds: { total:{spend:0,imp:0,clicks:0,cpm:0,ctr:0}, campaigns:[] }\n    }')


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def base():
    d = os.path.abspath(os.path.dirname(__file__))
    while d != '/':
        if os.path.isfile(os.path.join(d, 'sw.js')):
            return d
        d = os.path.dirname(d)
    die('หา BASE ไม่เจอ (ไล่ขึ้นไม่พบ sw.js)')


def _insert(s, const_name, key, body):
    """ต่อคีย์ใหม่ท้าย object ของ const_name — คืน (ข้อความใหม่, สร้างไหม)"""
    i = s.find('const %s' % const_name)
    if i < 0:
        die('ไม่พบ %s' % const_name)
    if '\n  %s: {' % key in s[i:]:
        return s, False
    j = s.index('\n};', i)
    return s[:j] + ',\n  %s: %s' % (key, body) + s[j:], True


def ensure(key, shopee_day=0, note=''):
    fp = os.path.join(base(), ADS_HTML)
    if not os.path.isfile(fp):
        die('ไม่พบ ' + ADS_HTML)
    s0 = s = io.open(fp, encoding='utf-8').read()
    safe = (note or '').replace("'", '’').replace('\n', ' ')
    dp_body = ('{\n'
               '    /* โครงเดือนใหม่สร้างโดย scripts/ads/ensure_month.py */\n'
               "    cover:{ shopeeDay:%d, tiktokDay:0, shopeePull:'%s', tiktokPull:'' },\n"
               '    shopee:%s,\n    tiktok:%s\n  }') % (shopee_day, safe, ZERO_PLAT, ZERO_PLAT)
    s, made_dp = _insert(s, 'DATA_PERIODS', key, dp_body)
    s, made_tk = _insert(s, 'TK_BREAKDOWN', key, ZERO_TK)
    if s != s0:
        io.open(fp, 'w', encoding='utf-8').write(s)
    return {'month': key, 'DATA_PERIODS': 'สร้างใหม่' if made_dp else 'มีอยู่แล้ว',
            'TK_BREAKDOWN': 'สร้างใหม่' if made_tk else 'มีอยู่แล้ว',
            'file_changed': s != s0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--month', help="คีย์เดือน 3 ตัวอักษร เช่น nov (ไม่ใส่ = เดือนปัจจุบัน)")
    ap.add_argument('--shopee-day', type=int, default=0,
                    help='วันที่ข้อมูล Shopee ไปถึงในเดือนนี้ (ใส่ 0 ถ้ายังไม่รู้)')
    ap.add_argument('--note', default='', help='บันทึกลง cover.shopeePull')
    a = ap.parse_args()
    key = a.month or MK[dt.date.today().month - 1]
    if key not in MK:
        die('คีย์เดือนไม่ถูกต้อง', key)
    rep = ensure(key, a.shopee_day, a.note)
    print(json.dumps({'status': 'OK', **rep}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
