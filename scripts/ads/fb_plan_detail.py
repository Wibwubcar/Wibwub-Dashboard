#!/usr/bin/env python3
"""URL ของรายงาน Facebook ระดับลึก — ระดับแอด + breakdown อายุ/เพศ และ ตำแหน่งโฆษณา

ต่างจาก `fb_plan.py` (ของเดิม ห้ามแก้ — งาน 08:15 ใช้อยู่ทุกวัน) ตรงที่ตัวนั้นให้
URL **ระดับแคมเปญ** อย่างเดียว ไฟล์นี้ให้ 3 ชุดที่หน้า Ads Dashboard ตัวใหม่ต้องใช้

พารามิเตอร์ที่เจอจากของจริง (5 พ.ย. 69 · ผู้ใช้อนุญาตให้เปิดดรอปดาวน์ "ข้อมูลแยกย่อย"
ครั้งเดียวเพื่ออ่านค่า — หลังจากนี้ **ห้ามกดปุ่มนี้อีก ให้สั่งผ่าน URL เท่านั้น**):

  ระดับรายงาน (path)      /adsmanager/manage/campaigns | /adsets | /ads
  แยกตามวัน               time_breakdown=days_1
  อายุ / เพศ               demographics_breakdown=age,gender
  ตำแหน่งโฆษณา            impression_breakdown=device_platform,platform_position,publisher_platform
  ประเทศ                   geography_breakdown=country        (ยังไม่ได้ใช้)

⚠️ กติกาที่พิสูจน์มาแล้ว ห้ามเดาใหม่:
  · ชื่อ token ของ Ads Manager ใช้**ชื่อเก่า**: `campaign_group_name` = ชื่อแคมเปญ ·
    `campaign_name` = ชื่อ**ชุดโฆษณา** · `name` = ชื่อโฆษณา
    (`adset_name` / `ad_name` / `ad_id` ไม่มีจริง ขอไปก็เงียบหายไม่มี error)
  · `demographics_breakdown` กับ `impression_breakdown` **ใช้พร้อมกันไม่ได้**
    หน้าเว็บขึ้นว่า "ไม่สามารถใช้ข้อมูลแยกย่อยนี้ร่วมกับข้อมูลแยกย่อยที่คุณเลือกได้"
    จึงต้องโหลดคนละใบ
  · `impression_breakdown` ต้องใส่ **ครบ 3 ค่า** ตามลำดับข้างบน ใส่ 2 ค่าถูกเมินทั้งพารามิเตอร์
  · ระดับแอดให้ลำดับชั้นครบในไฟล์เดียว (แคมเปญ/ชุดโฆษณา/แอด) ไม่ต้อง join กับระดับอื่น
    ยอดรวมตรงกันเป๊ะกับระดับชุดโฆษณา (13,072.58 ทั้งคู่ ทดสอบ AD-1 1–4 พ.ย. 69)
    ส่วนไฟล์ breakdown ต่างจากระดับแอด 0.07 บาท เพราะปัดทศนิยมรายแถว — ปกติ ไม่ใช่บั๊ก
  · FB ตัดช่วงให้ถึง**เมื่อวาน**เสมอ (ขอ 1–5 ได้ 1–4) และ **แก้ตัวเลขย้อนหลัง**
    (3 พ.ย. ขยับ 3,222.93 -> 3,232.32 ภายในวันเดียว) จึงต้องดึงทับย้อนหลัง
    **อย่างน้อย 7 วันทุกรอบ** ห้าม append วันใหม่อย่างเดียว

ใช้:  python3 scripts/ads/fb_plan_detail.py [--levels ad,age_gender,placement] [--today YYYY-MM-DD]
exit: 0 เสมอ (ตัวตัดสินว่ารอบนี้ทำหรือข้าม ยังเป็นหน้าที่ของ fb_plan.py เหมือนเดิม)
"""
import sys, json, argparse
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fb_plan import ACCOUNTS, BASE_URL                      # noqa: E402  ห้ามก๊อปรายชื่อบัญชี

# ต้องดึงทับย้อนหลังกี่วันเป็นอย่างน้อย (ดูหัวไฟล์ — FB แก้ตัวเลขย้อนหลัง)
MIN_LOOKBACK_DAYS = 7

# คอลัมน์ร่วมของทุกระดับ — ชุดนี้ export ออกมาครบจริงทุกตัว (ทดสอบ 5 พ.ย. 69)
METRICS = [
    'spend', 'impressions', 'reach', 'frequency', 'cpm',
    'clicks', 'ctr', 'cpc', 'inline_link_clicks',
    'actions:onsite_conversion.messaging_conversation_started_7d',
    'actions:omni_view_content', 'actions:omni_add_to_cart',
    'actions:omni_initiated_checkout', 'actions:omni_purchase',
    'action_values:omni_purchase', 'purchase_roas:omni_purchase',
    'catalog_segment_actions:omni_purchase', 'catalog_segment_value:omni_purchase',
]
# ยอดดูเนื้อหา/ใส่ตะกร้า/เริ่มชำระเงิน ขอมาได้แต่ **ว่างเกือบทั้งหมด** เพราะแคมเปญเป็นแบบ
# ข้อความ/มีส่วนร่วม ไม่มี pixel บนเว็บตัวเอง -> Funnel ของ FB ทำได้แค่ เห็น -> คลิก -> ซื้อ
# เก็บคอลัมน์ไว้เฉย ๆ ถ้าวันหนึ่งมีแคมเปญเว็บไซต์จะได้มีข้อมูลเอง **ห้ามเติมเลขเองเมื่อว่าง**

LEVELS = {
    'ad': {
        'path': 'ads',
        'names': ['campaign_group_name', 'campaign_name', 'name', 'delivery', 'objective'],
        'extra': 'time_breakdown=days_1',
        'filter': 'ad.impressions-NUMBER%1EGREATER_THAN%1E0',
    },
    'adset': {
        'path': 'adsets',
        'names': ['campaign_group_name', 'name', 'delivery'],
        'extra': 'time_breakdown=days_1',
        'filter': 'adset.impressions-NUMBER%1EGREATER_THAN%1E0',
    },
    'age_gender': {
        'path': 'campaigns',
        'names': ['name'],
        'extra': 'time_breakdown=days_1&demographics_breakdown=age,gender',
        'filter': 'campaign.impressions-NUMBER%1EGREATER_THAN%1E0',
    },
    'placement': {
        'path': 'campaigns',
        'names': ['name'],
        'extra': ('time_breakdown=days_1&impression_breakdown='
                  'device_platform,platform_position,publisher_platform'),
        'filter': 'campaign.impressions-NUMBER%1EGREATER_THAN%1E0',
    },
}


def date_range(today):
    """ช่วงที่ต้องดึง = ครอบเดือนของเมื่อวาน และย้อนหลังอย่างน้อย MIN_LOOKBACK_DAYS วัน

    ต้นเดือน (เช่นวันที่ 3) ช่วง "ต้นเดือน -> วันนี้" สั้นกว่า 7 วัน จึงต้องถอยไปคาบเดือนก่อน
    ไม่งั้นตัวเลขวันท้าย ๆ ของเดือนก่อนที่ FB เพิ่งแก้จะค้างเป็นของเก่าตลอดไป
    """
    y = today - timedelta(days=1)
    month_start = y.replace(day=1)
    lookback = today - timedelta(days=MIN_LOOKBACK_DAYS)
    return min(month_start, lookback).isoformat(), today.isoformat()


def build(level, acc_id, business_id, d_from, d_to):
    cfg = LEVELS[level]
    cols = ','.join(cfg['names'] + METRICS)
    return (f"{BASE_URL.rsplit('/', 1)[0]}/{cfg['path']}"
            f'?act={acc_id}&business_id={business_id}&date={d_from}_{d_to}'
            f"&{cfg['extra']}&filter_set={cfg['filter']}&columns={cols}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--levels', default='ad,age_gender,placement',
                    help='คั่นด้วยจุลภาค: ' + ','.join(LEVELS))
    ap.add_argument('--today', default='', help='ทดสอบ: บังคับวันที่เป็น YYYY-MM-DD')
    # ช่วงเติมย้อนหลัง (6 พ.ย. 69) — **งานรายวันห้ามใส่สองธงนี้** ปล่อยให้ date_range()
    # คิดเองตามเดิม ไม่งั้นจะหลุดกติกา "ดึงทับย้อนหลังอย่างน้อย 7 วัน" ที่กันเลขค้าง
    ap.add_argument('--from', dest='frm', default='',
                    help='เติมย้อนหลัง: วันเริ่ม YYYY-MM-DD (ต้องใส่คู่กับ --to)')
    ap.add_argument('--to', dest='to', default='',
                    help='เติมย้อนหลัง: วันจบ YYYY-MM-DD (ต้องใส่คู่กับ --from)')
    a = ap.parse_args()

    levels = [x.strip() for x in a.levels.split(',') if x.strip()]
    bad = [x for x in levels if x not in LEVELS]
    if bad:
        print(json.dumps({'status': 'ERROR', 'error': 'ไม่รู้จักระดับ: ' + ', '.join(bad),
                          'detail': 'ที่มีให้: ' + ', '.join(LEVELS)}, ensure_ascii=False))
        return 2

    today = date.fromisoformat(a.today) if a.today else date.today()
    if bool(a.frm) != bool(a.to):
        print(json.dumps({'status': 'ERROR', 'error': 'ต้องใส่ --from และ --to คู่กัน',
                          'detail': 'ใส่มาข้างเดียวจะได้ช่วงที่ไม่ได้ตั้งใจ'},
                         ensure_ascii=False))
        return 2
    if a.frm:
        d_from, d_to = a.frm, a.to
        if d_from > d_to:
            print(json.dumps({'status': 'ERROR', 'error': '--from ต้องไม่เกิน --to'},
                             ensure_ascii=False))
            return 2
    else:
        d_from, d_to = date_range(today)
    out = {'from': d_from, 'to': d_to, 'lookback_days': MIN_LOOKBACK_DAYS,
           'manual_range': bool(a.frm),
           'levels': levels,
           'note': 'FB ให้ข้อมูลถึงเมื่อวานเท่านั้น และแก้ตัวเลขย้อนหลัง — ดึงทับทุกรอบ',
           'accounts': [{'acc': k, 'id': i,
                         'urls': {lv: build(lv, i, b, d_from, d_to) for lv in levels}}
                        for k, i, b in ACCOUNTS]}
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
