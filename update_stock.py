#!/usr/bin/env python3
"""
update_stock.py — อัปเดต Procurement_Dashboard.html ด้วยข้อมูลสต๊อกล่าสุดจาก Shipnity
รับ input จาก Data Shipnity/stock_snapshot.json (stock/avail/reserved)
และ Data Shipnity/Data_DD-MM-YYYY.xlsx (order-level, ใช้คำนวณ sold7d/sold14d/burn)
Usage: python3 update_stock.py

สถานะ (status) ใหม่ 4 ระดับ อิงจาก "วันคงเหลือ" (avail ÷ burn):
  urgent (หมดเร็วมาก) <=7 วัน, low (ใกล้หมด) 8-14 วัน,
  watch (เริ่มตึง) 15-30 วัน, ok (ปกติ) >30 วัน, oos (หมดสต๊อก) avail<=0
Burn/วัน = sold7d ÷ 7 (ยอดขาย 7 วันล่าสุดเท่านั้น ไม่ใช่ค่าเฉลี่ย 6 เดือนแบบเดิม)
"""

import glob, json, os, re, sys
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).parent
SNAPSHOT = BASE / "Data Shipnity" / "Stock" / "stock_snapshot.json"
DASHBOARD = BASE / "Procurement_Dashboard.html"
SHIPNITY_DIR = BASE / "Data Shipnity"

# ─── อ่าน snapshot จาก Shipnity ─────────────────────────────────────────────
if not SNAPSHOT.exists():
    print(f"❌ ไม่พบ {SNAPSHOT}")
    sys.exit(1)

with open(SNAPSHOT, encoding="utf-8") as f:
    raw = json.load(f)

# ตรวจความสดของ snapshot (ไฟล์นี้ export มือจาก Shipnity ไม่มี LaunchAgent อัตโนมัติ)
snapshot_mtime = datetime.fromtimestamp(SNAPSHOT.stat().st_mtime)
snapshot_date = snapshot_mtime.date()
stale_days = (datetime.now().date() - snapshot_date).days
if stale_days >= 1:
    print(f"⚠️  stock_snapshot.json เก่าแล้ว {stale_days} วัน (แก้ไขล่าสุด {snapshot_mtime.strftime('%d/%m/%Y %H:%M')}) — กรุณา export ใหม่จาก Shipnity")

# สร้าง lookup ด้วย code (SKU)
raw_list = raw["products"] if isinstance(raw, dict) and "products" in raw else raw
ship_map = {p["code"]: p for p in raw_list if isinstance(p,dict) and p.get("code")}
print(f"📦 Shipnity stock: {len(ship_map)} SKUs")

# ─── หาไฟล์ order-level ล่าสุด (Data_DD-MM-YYYY.xlsx เท่านั้น — ห้ามใช้ Data-Page-1_*  ───
# เพราะ Data-Page-1_* เป็น export แค่หน้าแรก (~500 แถวล่าสุด) ไม่ใช่ยอดสะสมทั้งเดือน
order_files = sorted(
    glob.glob(str(SHIPNITY_DIR / "Data_[0-9][0-9]-[0-9][0-9]-*.xlsx")),
    key=os.path.getmtime, reverse=True
)

sold7_map, sold14_map = {}, {}
if not order_files:
    print("⚠️  ไม่พบไฟล์ Data_DD-MM-YYYY.xlsx ใน Data Shipnity/ — จะข้ามการคำนวณ sold7d/sold14d/burn (ใช้ค่าเดิม)")
else:
    order_file = order_files[0]
    print(f"🧾 ใช้ไฟล์ order-level: {os.path.basename(order_file)} (แก้ไขล่าสุด {datetime.fromtimestamp(os.path.getmtime(order_file)).strftime('%d/%m/%Y %H:%M')})")
    import openpyxl
    wb = openpyxl.load_workbook(order_file, read_only=True, data_only=True)
    ws = wb.active
    today_dt = datetime.now()
    d7_start  = (today_dt - timedelta(days=6)).date()   # ขาย 7 วันล่าสุด (รวมวันนี้)
    d14_start = (today_dt - timedelta(days=13)).date()  # ขาย 14 วันล่าสุด (รวมวันนี้)
    rows_seen = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or not row[0] or len(row) < 20:
            continue
        sku = str(row[0])
        qty = row[3] or 0
        created_raw = row[19]
        if not created_raw:
            continue
        try:
            if isinstance(created_raw, datetime):
                created_date = created_raw.date()
            else:
                created_date = datetime.strptime(str(created_raw).strip()[:16], "%d/%m/%Y %H:%M").date()
        except Exception:
            continue
        rows_seen += 1
        if created_date >= d14_start:
            sold14_map[sku] = sold14_map.get(sku, 0) + qty
            if created_date >= d7_start:
                sold7_map[sku] = sold7_map.get(sku, 0) + qty
    wb.close()
    print(f"   อ่าน {rows_seen} แถว → sold7d: {len(sold7_map)} SKU, sold14d: {len(sold14_map)} SKU")

# ─── อ่าน Procurement_Dashboard.html ─────────────────────────────────────────
html = DASHBOARD.read_text(encoding="utf-8")

# ดึง PRODUCTS array ปัจจุบัน
m = re.search(r'const PRODUCTS = (\[.*?\]);', html, re.DOTALL)
if not m:
    print("❌ ไม่พบ PRODUCTS array ใน Procurement_Dashboard.html")
    sys.exit(1)

products = json.loads(m.group(1))
today = datetime.now().date()
updated = 0

# ─── อัปเดตแต่ละ product ──────────────────────────────────────────────────────
for p in products:
    sku = p.get("sku", "")
    ship = ship_map.get(sku)

    # อัปเดต stock fields จาก Shipnity (ถ้ามี snapshot ของ SKU นี้)
    if ship:
        p["stock"]    = (ship.get("available", 0) or 0) + (ship.get("reserved", 0) or 0)
        p["reserved"] = ship.get("reserved", 0) or 0
        p["avail"]    = ship.get("available", 0) or 0
        updated += 1

    # อัปเดต sold7d/sold14d/burn จากไฟล์ order-level (ถ้ามี)
    if order_files:
        p["sold7d"]  = int(sold7_map.get(sku, 0))
        p["sold14d"] = int(sold14_map.get(sku, 0))
        p["burn"] = round(p["sold7d"] / 7, 2)

    # คำนวณ days, stockout, status ใหม่ (4 ระดับ: urgent/low/watch/ok/oos)
    burn = p.get("burn", 0) or 0
    avail = p.get("avail", 0) or 0

    if avail <= 0:
        p["days"] = 0
        p["stockout"] = today.strftime("%Y-%m-%d")
        p["status"] = "oos"
    elif burn <= 0:
        p["days"] = 999
        p["stockout"] = "2099-12-31"
        p["status"] = "ok"
    else:
        days = int(avail / burn)
        p["days"] = days
        stockout = today + timedelta(days=days)
        p["stockout"] = stockout.strftime("%Y-%m-%d")
        if days <= 7:
            p["status"] = "urgent"
        elif days <= 14:
            p["status"] = "low"
        elif days <= 30:
            p["status"] = "watch"
        else:
            p["status"] = "ok"

print(f"✅ อัปเดตสต๊อก {updated}/{len(products)} SKUs")

# ─── เช็ค SKU ที่มีใน Shipnity แต่ยังไม่ถูก track ใน Dashboard ─────────────────────
tracked_skus = {p.get("sku", "") for p in products}
missing_skus = [code for code in ship_map if code not in tracked_skus]
if missing_skus:
    print(f"⚠️  พบ {len(missing_skus)} SKU ใน Shipnity ที่ยังไม่มีใน PRODUCTS (ไม่ถูกอัปเดต): {', '.join(missing_skus[:20])}{' ...' if len(missing_skus) > 20 else ''}")

# ─── สถิติสรุป ─────────────────────────────────────────────────────────────────
urgent = sum(1 for p in products if p["status"] == "urgent")
low    = sum(1 for p in products if p["status"] == "low")
watch  = sum(1 for p in products if p["status"] == "watch")
ok     = sum(1 for p in products if p["status"] == "ok")
oos    = sum(1 for p in products if p["status"] == "oos")
print(f"   🔴 หมดเร็วมาก(≤7d): {urgent}  🟡 ใกล้หมด(8-14d): {low}  🟠 เริ่มตึง(15-30d): {watch}  🟢 ปกติ(>30d): {ok}  ⬛ หมด: {oos}")

# ─── เขียนกลับ HTML ──────────────────────────────────────────────────────────
new_products_json = json.dumps(products, ensure_ascii=False, separators=(',', ':'))
html_new = re.sub(
    r'const PRODUCTS = \[.*?\];',
    f'const PRODUCTS = {new_products_json};',
    html, flags=re.DOTALL
)

# อัปเดต last_updated badge ใน header
# ใช้วันที่ของ "ข้อมูล" (snapshot_date) ไม่ใช่วันที่รันสคริปต์ — กันไม่ให้ badge โกหกว่าข้อมูลสดกว่าที่เป็นจริง
date_str = snapshot_date.strftime("%d/%m/%Y")
if stale_days >= 1:
    date_str += f" (⚠️ ข้อมูลเก่า {stale_days} วัน)"
html_new = re.sub(
    r'(อัปเดตล่าสุด:?\s*)[\d/]+(?:\s*\(⚠️[^)]*\))?',
    rf'\g<1>{date_str}',
    html_new
)
# ถ้าไม่มี badge ให้เพิ่ม
if snapshot_date.strftime("%d/%m/%Y") not in html_new and "table-note" in html_new:
    html_new = html_new.replace(
        '<div class="note" id="table-note"></div>',
        f'<div class="note" id="table-note">อัปเดตล่าสุด: {date_str} (Shipnity live)</div>'
    )

# อัปเดต header badge หลัก "อัปเดต D MMM YYYY" (พ.ศ., ตัวย่อไทย) — เคยเป็น static string ไม่เคยถูกแตะมาก่อน
thai_months = ['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.']
thai_date_str = f'{snapshot_date.day} {thai_months[snapshot_date.month-1]} {snapshot_date.year + 543}'
html_new = re.sub(
    r'(อัปเดต )\d{1,2} \S+ \d{4}',
    rf'\g<1>{thai_date_str}',
    html_new
)

DASHBOARD.write_text(html_new, encoding="utf-8")
print(f"💾 บันทึก Procurement_Dashboard.html แล้ว")
print(f"📅 วันที่ของข้อมูล (snapshot): {date_str}")

# ─── Git commit + push ────────────────────────────────────────────────────────
# สคริปต์นี้ไม่มี LaunchAgent ของตัวเอง (รันมือ/ผ่าน run_now.command เท่านั้น)
# และเดิม wibwub_update.py's git_push() ไม่ได้ add ไฟล์นี้เลย ทำให้ Procurement_Dashboard.html
# ไม่เคยถูก push ขึ้นเว็บจริง แม้จะอัปเดตในเครื่องแล้วก็ตาม — commit เองที่นี่กันพลาด
import subprocess
try:
    subprocess.run(["git", "add", "Procurement_Dashboard.html"], cwd=str(BASE), check=True, capture_output=True)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=str(BASE))
    if diff.returncode == 0:
        print("   Git: ไม่มีอะไรเปลี่ยน")
    else:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        subprocess.run(["git", "commit", "-m", f"auto: update stock {ts}",
                        "--author=WIBWUB Bot <marketingwibwub@gmail.com>"],
                       cwd=str(BASE), check=True, capture_output=True)
        r = subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE), capture_output=True, text=True)
        if r.returncode == 0:
            print("   ✅ Git pushed")
        else:
            print(f"   ❌ Git push failed: {r.stderr.strip()}")
except subprocess.CalledProcessError as e:
    print(f"   ❌ Git error: {e}")
except Exception as e:
    print(f"   ❌ Git error: {e}")
