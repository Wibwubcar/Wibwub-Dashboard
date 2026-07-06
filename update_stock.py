#!/usr/bin/env python3
"""
update_stock.py — อัปเดต Procurement_Dashboard.html ด้วยข้อมูลสต๊อกล่าสุดจาก Shipnity
รับ input จาก Data Shipnity/stock_snapshot.json
Usage: python3 update_stock.py
"""

import json, re, sys
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).parent
SNAPSHOT = BASE / "Data Shipnity" / "Stock" / "stock_snapshot.json"
DASHBOARD = BASE / "Procurement_Dashboard.html"

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
print(f"📦 Shipnity: {len(ship_map)} SKUs")

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
    if not ship:
        continue

    # อัปเดต stock fields จาก Shipnity
    p["stock"]    = (ship.get("available", 0) or 0) + (ship.get("reserved", 0) or 0)
    p["reserved"] = ship.get("reserved", 0) or 0
    p["avail"]    = ship.get("available", 0) or 0

    # คำนวณ days, stockout, status ใหม่
    burn = p.get("burn", 0) or 0
    avail = p["avail"]

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
        if days <= 0:
            p["status"] = "oos"
        elif days <= 20:
            p["status"] = "critical"
        elif days <= 45:
            p["status"] = "low"
        else:
            p["status"] = "ok"

    updated += 1

print(f"✅ อัปเดต {updated}/{len(products)} SKUs")

# ─── เช็ค SKU ที่มีใน Shipnity แต่ยังไม่ถูก track ใน Dashboard ─────────────────────
tracked_skus = {p.get("sku", "") for p in products}
missing_skus = [code for code in ship_map if code not in tracked_skus]
if missing_skus:
    print(f"⚠️  พบ {len(missing_skus)} SKU ใน Shipnity ที่ยังไม่มีใน PRODUCTS (ไม่ถูกอัปเดต): {', '.join(missing_skus[:20])}{' ...' if len(missing_skus) > 20 else ''}")

# ─── สถิติสรุป ─────────────────────────────────────────────────────────────────
critical = sum(1 for p in products if p["status"] == "critical")
low      = sum(1 for p in products if p["status"] == "low")
ok       = sum(1 for p in products if p["status"] == "ok")
oos      = sum(1 for p in products if p["status"] == "oos")
print(f"   🔴 วิกฤต: {critical}  🟡 เฝ้าระวัง: {low}  🟢 ปกติ: {ok}  ⬛ หมด: {oos}")

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
