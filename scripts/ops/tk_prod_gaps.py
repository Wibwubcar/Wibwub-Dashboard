#!/usr/bin/env python3
"""
tk_prod_gaps.py — หา "วันที่ขาด" ของ TK_PROD_DATA เพื่อให้รอบ
wibwub-tiktok-product-daily ดึงย้อนได้เองในรอบเดียว

ทำไมต้องมีไฟล์นี้: พรอมป์ของงานตั้งเวลาเขียนลูป bash / ตั้งตัวแปร shell ไม่ได้
(เด้งกล่องขออนุญาตที่ไม่มีคนกด แล้วค้างทั้งรอบ) ตรรกะวนหาวันจึงต้องอยู่ในไฟล์ python
แล้วเรียกด้วย `python3 "<พาธเต็ม>/scripts/ops/tk_prod_gaps.py"` คำสั่งเดียว

กฎที่ยึด (ผู้ใช้อนุมัติ 24 พ.ย. 69):
- เพดาน 3 วันต่อรอบ (ปรับด้วย --max ได้ แต่ค่าเริ่มต้นคือ 3)
- เรียงเก่า → ใหม่ เพื่อให้ merge ต่อวันเรียงตามจริง
- วันที่ยัง "ไม่มี tk_real" ใน data Ads/ads_daily.json ให้ **ข้าม** ไม่ใช่ล้ม
  (ด่าน GMV ต้องมี tk_real เป็นตัวเทียบ ถ้าไม่มีก็ตรวจไม่ได้)
- ไม่ย้อนเกินวันแรกที่ TK_PROD_DATA มีข้อมูล และไม่แตะวันนี้ (ข้อมูลยังไม่นิ่ง)

⚠️ อ่าน const ด้วยการนับวงเล็บปีกกา **ไม่ใช่ regex `\\{.*?\\};`** — regex แบบนั้น
หยุดที่ `};` ตัวแรกที่เจอ ซึ่งอาจเป็นของ const ข้างเคียง 24 พ.ย. 69 มันทำให้อ่าน
TK_PROD_SKU ได้เป็น 2026-09-09 ทั้งที่ค่าจริงคือ 2026-11-10 แล้วสรุปผิดไปหนึ่งรอบ

exit code: 0 เสมอ (ทั้งกรณีมีวันที่ขาดและไม่มี) เพื่อไม่ให้รอบตั้งเวลาสะดุด
อ่านผลจากบรรทัดที่ขึ้นต้นด้วย GAPS / NO_GAPS
"""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))          # <BASE>/scripts/ops
BASE = os.path.dirname(os.path.dirname(HERE))              # <BASE>
DASHBOARD = os.path.join(BASE, "WIBWUB_Dashboard.html")
ADS_DAILY = os.path.join(BASE, "data Ads", "ads_daily.json")


def read_const(html, name):
    """อ่าน `const <name> = {...};` ด้วยการนับปีกกา คืน dict หรือ None"""
    i = html.find("const %s = " % name)
    if i < 0:
        return None
    j = html.find("{", i)
    if j < 0:
        return None
    depth = 0
    for k in range(j, len(html)):
        c = html[k]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return json.loads(html[j:k + 1])
    return None


def tk_prod_dates():
    with open(DASHBOARD, encoding="utf-8") as f:
        html = f.read()
    obj = read_const(html, "TK_PROD_DATA")
    if obj is None:
        sys.exit("⛔ ไม่พบ const TK_PROD_DATA ใน WIBWUB_Dashboard.html")
    return sorted(obj.get("dates") or [])


def tk_real_days():
    with open(ADS_DAILY, encoding="utf-8") as f:
        days = json.load(f)["days"]
    return {d for d, v in days.items() if isinstance(v, dict) and v.get("tk_real")}


def main():
    argv = sys.argv[1:]
    mx = 3
    for i, a in enumerate(argv):
        if a == "--max" and i + 1 < len(argv):
            mx = int(argv[i + 1])
    have = tk_prod_dates()
    if not have:
        sys.exit("⛔ TK_PROD_DATA ว่าง — ผิดปกติ หยุดก่อน")
    real = tk_real_days()
    first, last = have[0], have[-1]
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    haveset = set(have)
    gaps, skipped = [], []
    d = yesterday
    floor = datetime.date.fromisoformat(first)
    while d >= floor and len(gaps) < mx:
        iso = d.isoformat()
        if iso not in haveset:
            if iso in real:
                gaps.append(iso)
            else:
                skipped.append(iso)          # ไม่มี tk_real → ตรวจด่าน GMV ไม่ได้
        d -= datetime.timedelta(days=1)
    gaps.sort()                               # เก่า → ใหม่

    print("TK_PROD_DATA: %d วัน  %s → %s" % (len(have), first, last))
    print("tk_real ใน ads_daily.json: ถึง %s" % max(real) if real else "tk_real: ไม่มีเลย")
    if skipped:
        print("ข้าม (ยังไม่มี tk_real): %s" % ",".join(sorted(skipped)))
    if gaps:
        print("GAPS %s" % ",".join(gaps))
        print("→ ดึง %d วัน เรียงเก่าไปใหม่ (เพดาน %d วัน/รอบ)" % (len(gaps), mx))
    else:
        print("NO_GAPS")
        print("→ ไม่มีวันที่ต้องดึงย้อน ทำรอบปกติของเมื่อวานได้เลย")
    print(json.dumps({"gaps": gaps, "skipped": sorted(skipped),
                      "tk_prod_last": last, "max": mx}, ensure_ascii=False))


if __name__ == "__main__":
    main()
