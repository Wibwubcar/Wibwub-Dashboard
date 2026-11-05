#!/usr/bin/env python3
"""ตัดสินว่ารอบนี้ทำส่วน B (แอดละเอียด) หรือไม่ + คืนช่วงวันที่

ทำไมต้องเป็นสคริปต์ ไม่ใช่เขียนเวลาไว้ในพรอมป์ (บทเรียนจาก fb_plan.py 28 ต.ค. 69):
  เอเจนต์เอาเวลาปัจจุบันไปเทียบกับตัวเลขในพรอมป์เองแล้วข้ามงานผิด ๆ
  ถ้าจะเปลี่ยนกติกา **แก้ที่ไฟล์นี้ที่เดียว**

งานแม่คือ `wibwub-samp-request-sync` ซึ่งยิง 11:05 และ 22:05
ส่วน B ทำ **วันละรอบเดียวตอนเช้า** (ผู้ใช้กำหนด 5 พ.ย. 69) รอบ 22:05 จึงข้าม

ช่วงวันที่: ย้อนหลัง LOOKBACK วันถึง "เมื่อวาน"
  · Facebook ให้ข้อมูลถึงเมื่อวานเท่านั้น และแก้ตัวเลขย้อนหลัง
  · Shopee ปิดยอดของวันปัจจุบันช้า ดึงวันนี้มาจะได้เลขที่เปลี่ยนอีกตอนเย็น
  → เอาแค่ถึงเมื่อวานทุกช่องทาง ให้ทุกช่องทางมีขอบเดียวกัน

ใช้:  python3 scripts/ads/detail_plan.py [--now HH:MM] [--today YYYY-MM-DD]
exit: 0 = ทำส่วน B ต่อ · 3 = ข้ามรอบนี้
"""
import sys, json, argparse
from datetime import date, datetime, timedelta

LOOKBACK = 7          # ดึงทับย้อนหลังกี่วัน (ผู้ใช้กำหนดอย่างน้อย 7)
MORNING = (5, 15)     # ชั่วโมงที่ถือว่าเป็น "รอบเช้า" — กว้างเผื่องานแม่เริ่มช้า


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--now', default='')
    ap.add_argument('--today', default='')
    a = ap.parse_args()

    today = date.fromisoformat(a.today) if a.today else date.today()
    now = datetime.now()
    if a.now:
        h, m = (int(x) for x in a.now.split(':'))
        now = now.replace(hour=h, minute=m)

    morning = MORNING[0] <= now.hour < MORNING[1]
    to = today - timedelta(days=1)
    frm = to - timedelta(days=LOOKBACK - 1)
    out = {'skip': not morning,
           'reason': '' if morning else 'รอบเย็น — ส่วน B ทำวันละรอบเดียวตอนเช้า',
           'round': 'morning' if morning else 'evening',
           'from': frm.isoformat(), 'to': to.isoformat(),
           'days': [(frm + timedelta(days=i)).isoformat() for i in range(LOOKBACK)],
           'note': 'ทุกช่องทางเอาถึงเมื่อวานเท่านั้น — FB ไม่ให้ข้อมูลวันนี้ '
                   'และ Shopee ยังปิดยอดวันนี้ไม่เสร็จ'}
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 3 if out['skip'] else 0


if __name__ == '__main__':
    sys.exit(main())
