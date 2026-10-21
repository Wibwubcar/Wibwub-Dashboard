#!/usr/bin/env python3
"""merge TikTok Shop LIVE รายวัน เข้า TK_LIVE_DAILY ใน WIBWUB_Dashboard.html

คู่กับ scripts/shopee_live_daily.py แต่ **ไม่ต้องโหลดไฟล์จากเว็บเลย** เพราะ
ข้อมูลที่ต้องใช้มีอยู่ในรีโปแล้วทั้งสองฝั่ง:

  ยอดขายไลฟ์ (gmv)      ← TK_PROD_DATA ในหน้าเดียวกัน (งาน wibwub-tiktok-product-daily
                           เติมให้ทุกวัน 08:45/19:45) = self_live + affiliate_live
                           ซึ่งคือสูตรเดิมที่ tiktok_live_daily_final.json ใช้
                           (source: tk_prod_data_selflive_afflive_sum)
  ค่าโฆษณาระหว่างไลฟ์   ← data Ads/ads_daily.json → tk_ads.live (งาน ads-daily เติมให้)
  (adsCost / adsRev)

ทำไมถึงต้องมีสคริปต์นี้: TK_LIVE_DAILY ค้างอยู่ที่ 1 ก.ย. 2569 เพราะเดิมทำด้วยมือ
ครั้งเดียวแล้วไม่มีงานตั้งเวลารับช่วง ต่างจาก SH_LIVE_DAILY ที่มีงานประจำ

กับดักที่ต้องรู้ (อย่าแก้ออก):
  · แถวใน TK_PROD_DATA เป็น array ตามลำดับคงที่
    [pid, gmv, orders, sku_orders, items_sold, self_live, self_video,
     affiliate, affiliate_live, affiliate_video, product_card]
    ยอดไลฟ์ = ดัชนี 5 (self_live) + 8 (affiliate_live) **ห้ามใช้ดัชนี 7 (affiliate)**
    เพราะ affiliate รวมวิดีโอด้วย จะเบิ้ล
  · ยอดโตขึ้นตามเวลา (ออเดอร์ทยอยยืนยัน) ค่าที่คำนวณใหม่อาจสูงกว่าที่เคยบันทึก
    เช่น 1 ก.ย. 15,057.53 -> 15,490.53 — อัปขึ้นได้ แต่ **ห้ามถอยลง**
  · adsCampaigns (จำนวนแคมเปญ) ไม่มีเก็บรายวันที่ไหน ads_daily.json มีแต่ยอดรวม
    จึงเขียน 0 ไว้ = "ไม่ทราบจำนวน" และหน้าเว็บเปลี่ยนไปใช้ adsCost>0 เป็นตัวตัดสิน
    ว่าวันนั้นมีโฆษณาหรือไม่ **ห้ามเดาใส่ 1**
  · TK_PROD_DATA เริ่ม 1 ส.ค. 2569 — วันก่อนหน้านั้นสร้างย้อนไม่ได้ด้วยวิธีนี้
    (ของเดิม เม.ย.-ก.ค. มาจาก Compass Live Analysis export เก็บไว้แล้ว ไม่ต้องแตะ)

ใช้:  python3 scripts/tiktok_live_daily.py [--dry-run] [--since YYYY-MM-DD]
exit: 0 = อัปเดตแล้ว · 10 = ไม่มีอะไรเปลี่ยน · 2 = ไม่ผ่านด่านตรวจ (ไม่เขียนไฟล์)
"""
import sys, re, json, argparse, subprocess, tempfile
import datetime as dt
from pathlib import Path

BASE = Path('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com'
            '/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All')
PAGE = BASE / 'WIBWUB_Dashboard.html'
ADS = BASE / 'data Ads' / 'ads_daily.json'
BKK = dt.timezone(dt.timedelta(hours=7))
I_SELF_LIVE, I_AFF_LIVE = 5, 8


def die(msg, detail=None):
    print(json.dumps({'status': 'ERROR', 'error': msg, 'detail': detail}, ensure_ascii=False))
    sys.exit(2)


def grab(html, name):
    m = re.search(r'const ' + name + r'\s*=\s*(\{[\s\S]*?\});', html)
    if not m: die(f'ไม่พบ {name} ในหน้าเว็บ')
    try: return json.loads(m.group(1)), m
    except json.JSONDecodeError as e: die(f'{name} ไม่ใช่ JSON ที่อ่านได้', str(e))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--since', help='คำนวณใหม่ตั้งแต่วันนี้ (ปกติ: ทุกวันที่ TK_PROD_DATA มี)')
    a = ap.parse_args()

    if not PAGE.exists(): die('ไม่พบ WIBWUB_Dashboard.html')
    html = PAGE.read_text(encoding='utf-8')
    prod, _ = grab(html, 'TK_PROD_DATA')
    cur, m_live = grab(html, 'TK_LIVE_DAILY')
    dates, daily = cur['dates'], cur['daily']

    if not ADS.exists(): die('ไม่พบ data Ads/ads_daily.json')
    ads = json.load(open(ADS, encoding='utf-8'))['days']

    pdaily = prod.get('daily') or {}
    if not pdaily: die('TK_PROD_DATA ไม่มี daily — งาน tiktok-product-daily อาจยังไม่เคยรัน')

    y = (dt.datetime.now(BKK).date() - dt.timedelta(days=1)).isoformat()
    added, changed, skipped, refused = [], [], [], []

    for d in sorted(pdaily):
        if a.since and d < a.since: continue
        if d > y: skipped.append(f'{d} (ยังไม่จบวัน)'); continue
        rows = pdaily[d]
        if not rows: skipped.append(f'{d} (TK_PROD_DATA ไม่มีแถว)'); continue
        bad = [r for r in rows if len(r) <= I_AFF_LIVE]
        if bad: die('แถวใน TK_PROD_DATA สั้นกว่าที่คาด — รูปแบบเปลี่ยน',
                    {'วันที่': d, 'ความยาวแถว': len(bad[0])})
        gmv = round(sum((r[I_SELF_LIVE] or 0) + (r[I_AFF_LIVE] or 0) for r in rows), 2)
        lv = ((ads.get(d, {}).get('tk_ads') or {}).get('live') or {})
        n = {'gmv': gmv,
             'adsCost': round(float(lv.get('spend') or 0), 2),
             'adsRev': round(float(lv.get('gmv') or 0), 2),
             'adsCampaigns': 0}      # ไม่มีข้อมูลจำนวนแคมเปญรายวัน — ห้ามเดา
        o = daily.get(d)
        # ยอดไลฟ์โตขึ้นตามเวลา ค่าใหม่ที่ต่ำกว่าเดิม = ข้อมูลต้นทางถอย ให้ข้าม
        if o and o.get('gmv') and n['gmv'] < o['gmv'] - 0.01:
            skipped.append(f'{d} (ค่าใหม่ต่ำกว่าเดิม {n["gmv"]} < {o["gmv"]})'); continue
        # ห้ามเขียน 0 ทับวันที่เคยมียอด
        if o and o.get('gmv') and not n['gmv']:
            refused.append(f'{d}: เดิม gmv {o["gmv"]} แต่คำนวณใหม่เป็น 0'); continue
        # ค่าโฆษณาของ เม.ย.-ส.ค. มาจากแหล่งอื่น (export แคมเปญรายไลฟ์) ซึ่งตัวเลข
        # ไม่ตรงกับ ads_daily.json เป๊ะ ๆ เช่น 15 ส.ค. 585.62 vs 185.62
        # นั่นคือ "คนละแหล่ง" ไม่ใช่ "ข้อมูลอัปเดต" → ห้ามเอาทับของเดิม
        # เติมได้เฉพาะวันที่ยังว่างทั้งสามช่อง (= ไม่เคยมีข้อมูลโฆษณา)
        if o and (o.get('adsCost') or o.get('adsRev') or o.get('adsCampaigns')):
            for k in ('adsCost', 'adsRev', 'adsCampaigns'): n[k] = o[k]
        if o is None: daily[d] = n; added.append(d)
        elif o != n: daily[d] = n; changed.append(f'{d}: {o} -> {n}')

    if refused: die('คำนวณใหม่ได้ 0 ทับวันที่เคยมียอด — ไม่เขียน', refused)

    allv = sorted(set(dates) | set(daily))
    if allv:
        s, e = dt.date.fromisoformat(allv[0]), dt.date.fromisoformat(allv[-1])
        full = [(s + dt.timedelta(days=i)).isoformat() for i in range((e - s).days + 1)]
        for d in full:
            daily.setdefault(d, {'gmv': 0, 'adsCost': 0, 'adsRev': 0, 'adsCampaigns': 0})
    else:
        full = []
    if len(full) < len(dates): die('จำนวนวันหดลง — ไม่เขียนทับ', f'{len(dates)} -> {len(full)}')

    out = {'dates': full, 'daily': {d: daily[d] for d in full}}
    summary = {'added': added, 'changed': changed, 'skipped': skipped[-5:],
               'skipped_n': len(skipped), 'days': len(full),
               'range': [full[0], full[-1]] if full else None,
               'live_days': sum(1 for d in full if daily[d].get('gmv')),
               'gmv_total': round(sum(daily[d].get('gmv') or 0 for d in full), 2)}

    if a.dry_run:
        print(json.dumps({'status': 'DRY_RUN', **summary}, ensure_ascii=False)); return 0
    if not added and not changed:
        print(json.dumps({'status': 'NO_CHANGE', **summary}, ensure_ascii=False)); return 10

    new_html = (html[:m_live.start(1)]
                + json.dumps(out, ensure_ascii=False, separators=(',', ':'))
                + html[m_live.end(1):])
    js = Path(tempfile.gettempdir()) / 'wibwub_tklive_check.js'
    js.write_text('\n;\n'.join(re.findall(r'<script[^>]*>([\s\S]*?)</script>', new_html)),
                  encoding='utf-8')
    r = subprocess.run(['node', '--check', str(js)], capture_output=True, text=True)
    if r.returncode: die('node --check ไม่ผ่าน', r.stderr[:300])
    PAGE.write_text(new_html, encoding='utf-8')

    sw = BASE / 'sw.js'; t = sw.read_text(encoding='utf-8')
    v = int(re.search(r'wibwub-v(\d+)', t).group(1))
    sw.write_text(re.sub(r'wibwub-v\d+', f'wibwub-v{v+1}', t), encoding='utf-8')
    summary['sw'] = f'v{v} -> v{v+1}'
    print(json.dumps({'status': 'UPDATED', **summary}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
