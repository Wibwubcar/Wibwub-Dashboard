#!/usr/bin/env python3
"""บอกงานตั้งเวลาว่ารอบนี้ต้องเปิด URL ไหนบ้าง + ช่วงวันที่ + เวลาเส้นตาย

ทำไมต้องเป็นสคริปต์ ไม่ใช่เขียน URL ไว้ในพรอมป์:
  · ช่วงวันที่เปลี่ยนทุกวัน และ "วันที่ 1 ของเดือน" ต้องคิดจากเมื่อวาน ไม่ใช่วันนี้
    (วันที่ 1 ต้องดึงของเดือนก่อนเพื่อปิดยอด ไม่ใช่ดึงเดือนใหม่ที่ยังว่าง)
  · งานตั้งเวลารันคำสั่ง shell ที่มีลูป/ตัวแปร/เงื่อนไขไม่ได้ (ติดกำแพงสิทธิ์)
    ตรรกะทุกอย่างจึงต้องอยู่ในสคริปต์ python แล้วเรียกด้วยพาธเต็ม

รอบไหนเป็นรอบไหน (ดูจากเวลาที่เริ่มรัน):
  · 08:00-09:59 = `morning`  รอบตั้งเวลาเช้า -> **ใช้เส้นตาย** (ค่าเริ่มต้น 08:50)
    เพราะงานสต๊อก 09:00 ใช้ในประชุม ถ้าส่วน Facebook ลากยาวจะไปเบียดจนโดนเตะทิ้ง
  · 18:00-21:59 = `evening`  รอบตั้งเวลาเย็น -> **ข้ามส่วน Facebook** (วันละรอบพอ)
  · นอกนั้น      = `manual`   คนกดเอง -> **ไม่ใช้เส้นตาย** ทำส่วน Facebook ได้เต็มที่
    (28 ต.ค. 69: ถ้าใช้เส้นตายกับรอบกดมือด้วย การกด Run now ตอนกลางวันจะข้ามส่วน
     Facebook ทั้งหมด หน้า Ads Manager ไม่ถูกเปิด ปุ่ม "อนุญาตเสมอ" ก็ไม่เด้ง
     แล้วงานตั้งเวลาจะไม่มีวันได้สิทธิ์โดเมน)

ใช้:  python3 scripts/ads/fb_plan.py [--deadline 08:50]
exit: 0 = ทำส่วน Facebook ต่อได้ · 3 = ให้ข้ามส่วน Facebook (เลยเส้นตาย หรือเป็นรอบเย็น)
"""
import sys, json, argparse
from datetime import date, datetime, timedelta

# (คีย์บัญชี, act id, business id) — คีย์ต้องตรงกับ ACC_LABEL ใน fb_daily.py
ACCOUNTS = [
    ('WibWub-AD-1', '465355531258126',  '2104658983166591'),
    ('AD-1',        '597632760310102',  '201710300222828'),
    ('AD-2',        '2771774829742992', '201710300222828'),
    ('AD3',         '2884723221808032', '201710300222828'),
    ('AD-4',        '361869315646318',  '201710300222828'),
]
# คอลัมน์ที่ต้องมี — 3 ตัวท้ายเพิ่มเมื่อ 28 ต.ค. 69 เพื่อให้ AD3 (CPAS) มีมูลค่าการซื้อ
# catalog_segment_value_omni_purchase_roas ขอมาได้แต่ค่าว่าง -> ไม่ใส่ ให้คำนวณ ROAS เอง
COLUMNS = ','.join([
    'name', 'delivery', 'objective', 'attribution_setting', 'results', 'cost_per_result',
    'budget', 'spend', 'impressions', 'reach', 'frequency', 'cpm', 'ctr',
    'inline_link_clicks', 'cost_per_inline_link_click', 'inline_link_click_ctr', 'cpc',
    'actions:onsite_conversion.messaging_conversation_started_7d',
    'actions:omni_purchase', 'purchase_roas:omni_purchase',
    'catalog_segment_actions:omni_purchase', 'catalog_segment_value:omni_purchase',
    'action_values:omni_purchase',
])
FILTER = 'campaign.impressions-NUMBER%1EGREATER_THAN%1E0'
BASE_URL = 'https://adsmanager.facebook.com/adsmanager/manage/campaigns'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--deadline', default='08:50', help='HH:MM — เลยเวลานี้ให้ข้ามส่วน Facebook')
    ap.add_argument('--today', default='', help='ทดสอบ: บังคับวันที่เป็น YYYY-MM-DD')
    ap.add_argument('--now', default='', help='ทดสอบ: บังคับเวลาเป็น HH:MM')
    a = ap.parse_args()

    today = date.fromisoformat(a.today) if a.today else date.today()
    # ช่วง = วันที่ 1 ของเดือนของ "เมื่อวาน" -> วันนี้
    # วันที่ 1: เมื่อวานอยู่เดือนก่อน จึงได้ช่วงที่ปิดยอดเดือนก่อนให้ครบ แล้วมี 1 วันของเดือนใหม่ติดมา
    y = today - timedelta(days=1)
    d_from, d_to = y.replace(day=1).isoformat(), today.isoformat()

    now = datetime.now()
    if a.now:
        h2, m2 = (int(x) for x in a.now.split(':'))
        now = now.replace(hour=h2, minute=m2, second=0)
    hh, mm = (int(x) for x in a.deadline.split(':'))

    # รอบไหน -> ตัดสินจากเวลาที่เริ่มรัน (ดูหัวไฟล์)
    if 8 <= now.hour < 10:
        rnd = 'morning'
    elif 18 <= now.hour < 22:
        rnd = 'evening'
    else:
        rnd = 'manual'
    past = (rnd == 'morning') and (now.hour, now.minute) >= (hh, mm)
    skip = past or rnd == 'evening'
    why = ('เลยเส้นตาย ' + a.deadline if past else
           'รอบเย็น — ส่วน Facebook ทำวันละรอบเดียวตอนเช้า' if rnd == 'evening' else '')

    out = {'from': d_from, 'to': d_to, 'now': now.strftime('%Y-%m-%d %H:%M:%S'),
           'round': rnd, 'deadline': a.deadline if rnd == 'morning' else None,
           'deadline_passed': past, 'skip_facebook': skip, 'reason': why,
           'accounts': [{'acc': k, 'id': i,
                         'url': f'{BASE_URL}?act={i}&business_id={b}&date={d_from}_{d_to}'
                                f'&time_breakdown=days_1&filter_set={FILTER}&columns={COLUMNS}'}
                        for k, i, b in ACCOUNTS]}
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 3 if skip else 0


if __name__ == '__main__':
    sys.exit(main())
