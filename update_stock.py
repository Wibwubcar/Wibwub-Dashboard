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
date_str = today.strftime("%d/%m/%Y")
html_new = re.sub(
    r'(อัปเดตล่าสุด:?\s*)[\d/]+',
    rf'\g<1>{date_str}',
    html_new
)
# ถ้าไม่มี badge ให้เพิ่ม
if date_str not in html_new and "table-note" in html_new:
    html_new = html_new.replace(
        '<div class="note" id="table-note"></div>',
        f'<div class="note" id="table-note">อัปเดตล่าสุด: {date_str} (Shipnity live)</div>'
    )

DASHBOARD.write_text(html_new, encoding="utf-8")
print(f"💾 บันทึก Procurement_Dashboard.html แล้ว")
print(f"📅 วันที่อัปเดต: {date_str}")
