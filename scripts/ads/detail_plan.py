#!/usr/bin/env python3
"""ตัดสินว่ารอบนี้ทำส่วน B (แอดละเอียด) หรือไม่ + คืนช่วงวันที่

ทำไมต้องเป็นสคริปต์ ไม่ใช่เขียนเวลาไว้ในพรอมป์ (บทเรียนจาก fb_plan.py 28 ต.ค. 69):
  เอเจนต์เอาเวลาปัจจุบันไปเทียบกับตัวเลขในพรอมป์เองแล้วข้ามงานผิด ๆ
  ถ้าจะเปลี่ยนกติกา **แก้ที่ไฟล์นี้ที่เดียว**

งานแม่คือ `wibwub-samp-request-sync` ซึ่งยิง 11:05 และ 22:05
ส่วน B ทำ **วันละรอบเดียวตอนเช้า** (ผู้ใช้กำหนด 5 พ.ย. 69) รอบ 22:05 จึงข้าม
**ยกเว้นรอบเช้าไม่สำเร็จ** — ถ้าผลงานเก่ากว่า STALE_HOURS รอบเย็นจะตามเก็บให้ (8 พ.ย. 69)
  8 พ.ย. 69 รอบ 11:05 หายไปตอนเน็ตหลุด (09:39-11:07) รอบตามเก็บ 12:43 เริ่มทำส่วน B จริง
  แต่ตายกลางทางตอนเน็ตหลุดรอบสอง (12:46-14:20) ได้ไฟล์มา 1 จาก 13 ใบ
  กติกาเดิมห้ามรอบเย็นแบบไม่มีเงื่อนไข ข้อมูลจึงค้างทั้งวันโดยไม่มีทางตามเก็บ

ช่วงวันที่: ย้อนหลัง LOOKBACK วันถึง "เมื่อวาน"
  · Facebook ให้ข้อมูลถึงเมื่อวานเท่านั้น และแก้ตัวเลขย้อนหลัง
  · Shopee ปิดยอดของวันปัจจุบันช้า ดึงวันนี้มาจะได้เลขที่เปลี่ยนอีกตอนเย็น
  → เอาแค่ถึงเมื่อวานทุกช่องทาง ให้ทุกช่องทางมีขอบเดียวกัน

ใช้:  python3 scripts/ads/detail_plan.py [--now HH:MM] [--today YYYY-MM-DD]
exit: 0 = ทำส่วน B ต่อ · 3 = ข้ามรอบนี้
"""
import sys, json, argparse
from datetime import date, datetime, timedelta
from pathlib import Path

LOOKBACK = 7          # ดึงทับย้อนหลังกี่วัน (ผู้ใช้กำหนดอย่างน้อย 7)
# ผลงานเก่ากว่านี้ (ชั่วโมง) = รอบเช้าของวันนี้ไม่สำเร็จ -> ให้รอบเย็นตามเก็บ
# 20 ชม. เลือกให้ > ระยะ 11:05 ของสองวันติด (24 ชม.) ไม่ได้ จึงต้องน้อยกว่า 24
# และต้องมากกว่าระยะ 11:05 -> 22:05 ของวันเดียวกัน (11 ชม.) เพื่อไม่ให้รอบเย็น
# ทำซ้ำในวันที่รอบเช้าสำเร็จปกติ · 20 ชม. อยู่กลางช่วง 11-24 พอดี
STALE_HOURS = 20
# งานแม่ (wibwub-samp-request-sync) ยิง 11:05 กับ 22:05 — บวกหน่วงของฝั่ง local 1–8 นาที
# รอบเช้า = ทำ · รอบเย็น = ข้าม (วันละรอบเดียว) · **นอกสองช่วงนี้ = คนกดเอง -> ทำเสมอ**
#
# ทำไมรอบกดเองต้องทำ: ต้องเปิดหน้าเว็บจริงครั้งแรกเพื่อให้กล่อง "อนุญาตเสมอ" เด้ง
# ไม่งั้นรอบตั้งเวลาจะไม่มีสิทธิ์โดเมนตลอดไป (บทเรียนเดียวกับ fb_plan.py 28 ต.ค. 69:
# ตอนนั้นรอบกดเองถูกข้ามด้วยเส้นตาย หน้า Ads Manager เลยไม่เคยถูกเปิด)
# 5 พ.ย. 69 เกิดซ้ำ: กด Run now 20:45 แล้วส่วน B ข้าม สิทธิ์โดเมนจึงยังไม่ได้
MORNING_H = (11, 12)  # ชั่วโมงของรอบเช้าตามตาราง
EVENING_H = (22, 23)  # ชั่วโมงของรอบเย็นตามตาราง


def detail_age_hours():
    """อายุผลงานส่วน B เป็นชั่วโมง จาก `fetched_at` ใน `data Ads/ads_detail_sh.json`

    ใช้ไฟล์ Shopee เป็นตัวชี้วัดตัวเดียว ให้ตรงกับการ์ด "แอดละเอียด 11:05"
    ใน task_expect.json ที่วัดจากไฟล์เดียวกัน (ถ้าเปลี่ยนที่นี่ ต้องเปลี่ยนที่นั่นด้วย)

    คืน `None` เมื่ออ่านไม่ได้ — ผู้เรียก**ต้องถือว่าไม่รู้แล้วใช้กติกาเดิม (รอบเย็นข้าม)**
    ห้ามเดาว่า "อ่านไม่ได้ = เก่า" เพราะจะทำให้รอบเย็นเปิดเบราว์เซอร์ทำงานซ้ำทุกคืน
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from detail_privacy import BASE          # ตัวหาโฟลเดอร์ All ตัวเดียวกับสคริปต์พี่น้อง
        fp = BASE / 'data Ads' / 'ads_detail_sh.json'
        got = json.loads(fp.read_text(encoding='utf-8')).get('fetched_at')
        when = datetime.fromisoformat(str(got))
        return (datetime.now() - when).total_seconds() / 3600.0
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--now', default='')
    ap.add_argument('--today', default='')
    ap.add_argument('--age-hours', type=float, default=None, dest='age_hours',
                    help='บังคับอายุผลงานส่วน B (ชั่วโมง) — สำหรับทดสอบเท่านั้น')
    a = ap.parse_args()

    age = a.age_hours
    today = date.fromisoformat(a.today) if a.today else date.today()
    now = datetime.now()
    if a.now:
        h, m = (int(x) for x in a.now.split(':'))
        now = now.replace(hour=h, minute=m)

    if MORNING_H[0] <= now.hour < MORNING_H[1]:
        rnd, skip, why = 'morning', False, ''
    elif EVENING_H[0] <= now.hour < EVENING_H[1]:
        age = a.age_hours if a.age_hours is not None else detail_age_hours()
        if age is not None and age >= STALE_HOURS:
            rnd, skip, why = 'evening-catchup', False, ''
        else:
            rnd, skip, why = 'evening', True, 'รอบเย็น — ส่วน B ทำวันละรอบเดียวตอนเช้า'
    else:
        rnd, skip, why = 'manual', False, ''
    to = today - timedelta(days=1)
    frm = to - timedelta(days=LOOKBACK - 1)
    out = {'skip': skip, 'reason': why, 'round': rnd,
           'detail_age_hours': None if age is None else round(age, 1),
           'from': frm.isoformat(), 'to': to.isoformat(),
           'days': [(frm + timedelta(days=i)).isoformat() for i in range(LOOKBACK)],
           'note': 'ทุกช่องทางเอาถึงเมื่อวานเท่านั้น — FB ไม่ให้ข้อมูลวันนี้ '
                   'และ Shopee ยังปิดยอดวันนี้ไม่เสร็จ'}
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 3 if out['skip'] else 0


if __name__ == '__main__':
    sys.exit(main())
