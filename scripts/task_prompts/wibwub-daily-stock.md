---
name: wibwub-daily-stock
description: ดึงสต๊อกล่าสุดจาก Shipnity ทุกวัน 08:40/19:40 → อัปเดต Procurement_Dashboard.html → commit + push_now.command
---

<!-- LOCAL-OVERRIDE v1 -->
> **อ่านก่อน — ข้อนี้ทับคำสั่งที่ขัดกันในไฟล์นี้ทั้งหมด**
> ไฟล์นี้เขียนไว้ตอนรันบน Cowork cloud sandbox ตอนนี้ย้ายมารันบนเครื่อง Mac แล้ว
> - BASE / ALL_MNT = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All` · Downloads = `/Users/thanasablilutanon/Downloads` · OUTPUTS = `/Users/thanasablilutanon/Library/Caches/wibwub-outputs`
> - `git push` **ไม่ต้องทำ** และจะ**ไม่**เจอ error 403 แบบ sandbox — launchd `com.wibwub.autopush` push ให้เองทุก 2 นาที ข้ามทุกหัวข้อที่พูดถึง 403 / การสร้างหรือแก้ `push_now.command`
> - ที่ไหนเขียนว่า `mcp__workspace__bash` ให้ใช้ Bash tool ปกติแทน
> - อ่านไฟล์ในเครื่องใช้ Read/Bash ได้ตรง ๆ ไม่ต้องผ่าน connector
> - ถ้าขั้นไหนอ้าง path หรือเครื่องมือที่ไม่มีจริง: **หยุดและรายงาน ห้ามเดาทางเอง**

## WIBWUB Daily Stock Update — Shipnity Forecast

ดึงข้อมูลสต๊อกล่าสุดจาก Shipnity ผ่าน GraphQL API แล้วอัปเดต Procurement_Dashboard.html และ commit ขึ้น git ทุกวันเช้า

### BASE PATH
- Workspace: `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`
- Shell path: `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/`

### ⚠️ Chrome Navigation Rule — สำคัญมาก
ห้ามใช้ `navigate` แบบ standalone เด็ดขาด — จะค้างไม่ return ทำให้ task หยุดทำงาน
ต้องใช้ `browser_batch` ทุกครั้งที่ต้องการ navigate:
```
browser_batch([
  navigate(url="...", tabId=TAB_ID),
  computer(action="wait", duration=4, tabId=TAB_ID),
  computer(action="screenshot", tabId=TAB_ID)
])
```

---

## Step 1 — Navigate to Shipnity

1. ⚠️ **ต้องระบุ browser ที่ Mac เสมอ ห้ามปล่อยให้เลือกอัตโนมัติ** — ถ้ามีหลาย browser connected อาจไปรันบน PC โดยไม่ตั้งใจ:
   `select_browser(deviceId="b75a6bb0-5b78-4e44-92a8-75224f1ce4ee")` → `tabs_context_mcp(createIfEmpty=true)`
   (ถ้า deviceId นี้ไม่ connected แล้ว ให้เรียก `list_connected_browsers` ก่อน แล้วเลือกตัวที่ `osPlatform` เป็น macOS / `isLocal:true` เท่านั้น — ห้ามเลือก Windows/PC)

2. Navigate ด้วย browser_batch (ห้ามใช้ navigate standalone):
   - URL: `https://www.shipnity.com/product/p`
   - wait 4s → screenshot
   - ตรวจว่าหน้าโหลดปกติ ถ้าต้องการ login ให้หยุดและรายงาน "ต้องการ login Shipnity"

---

## Step 2 — Fetch all products via GraphQL (ดึงจนหมด)

⚠️ **กฎสำคัญ:** ต้องดึงจนได้สินค้าครบทุกตัว ห้ามหยุดที่หน้า 5 — Shipnity มีสินค้ามากกว่า 100 SKU
UV protect (SUVP*) อยู่หน้า 6+ ถ้าหยุดที่ 5 หน้าจะหายไปจาก Dashboard!

รันใน browser ทีละ page จนกว่าจะได้ผลว่างเปล่า:

⚠️ **กฎสำคัญ:** ต้องดึง `subproducts` ด้วยเสมอ — SKUs จริง (เช่น SUVP000002) ซ่อนอยู่ใน subproducts ของ parent ไม่ใช่ top-level products!
ถ้าไม่ดึง subproducts จะได้แค่ 82 parent → ขาด SKU ตกหล่นหลายตัว (UV protect, Visible, Beach ฯลฯ)

```javascript
// ดึงทุกหน้า + subproducts (ครบ 193 SKUs)
let allProducts = [], page = 1;
while (true) {
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/api/graphql', false);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.withCredentials = true;
  xhr.send(JSON.stringify({
    query: `{ products(page: ${page}) { nodes { ... on Product { code name total reserved available subproducts { code name total reserved available } } } } }`
  }));
  const d = JSON.parse(xhr.responseText);
  const nodes = d.data.products.nodes;
  if (!nodes || nodes.length === 0) break;
  allProducts = allProducts.concat(nodes);
  page++;
  if (page > 20) break; // safety cap
}
window.__allProducts = allProducts;

// Flatten parents + subproducts → stock map
// ⚠️ บางครั้ง Shipnity มี SKU code เดียวกันปรากฏซ้ำ 2 record (เช่น เป็น subproduct
// ของ family group หนึ่ง + เป็น standalone top-level product อีกอัน) — เจอเคสจริงกับ
// SSUG050024 "Sugar 5L" เมื่อ 17 ส.ค. 2569: subproduct ใต้ "Sugar" family มีค่าค้าง
// (avail:0, total ผิดปกติ) ในขณะที่ตัว standalone product มีค่าจริงที่ active อยู่
// (avail:14) — ถ้า overwrite ตามลำดับ parent ที่ดึงมาเฉยๆ (last-write-wins) จะได้ค่า
// ที่ไม่แน่นอนและอาจดรอปค่าที่ถูกต้องไปโดยไม่รู้ตัว
// แก้โดย: เมื่อเจอ code ซ้ำและค่าไม่ตรงกัน ให้เลือก record ที่มี available สูงกว่าเสมอ
// (ถือว่า record ที่มี available>0 คือตัวที่ active จริง ส่วนตัวที่ 0 มักเป็น record
// เก่า/ค้างที่ไม่ได้ใช้ขายจริงแล้ว)
const stockMap = {};
const conflicts = [];
function setStock(code, name, total, reserved, available) {
  const entry = {code, name, total: total||0, reserved: reserved||0, available: available||0};
  const existing = stockMap[code];
  if (existing && (existing.total !== entry.total || existing.reserved !== entry.reserved || existing.available !== entry.available)) {
    conflicts.push({code, kept: existing.available >= entry.available ? existing : entry, dropped: existing.available >= entry.available ? entry : existing});
    if (entry.available > existing.available) stockMap[code] = entry; // เก็บตัวที่ available สูงกว่า
    return;
  }
  stockMap[code] = entry;
}
for (const p of allProducts) {
  if (p.code) setStock(p.code, p.name, p.total, p.reserved, p.available);
  if (p.subproducts) {
    for (const s of p.subproducts) {
      if (s.code) setStock(s.code, s.name, s.total, s.reserved, s.available);
    }
  }
}
window.__stockMap = stockMap;
window.__stockConflicts = conflicts;
if (conflicts.length) console.warn(`⚠️ ${conflicts.length} SKU code conflict(s) — ตรวจ window.__stockConflicts ก่อนบันทึก`, conflicts);

// Export as lines: code|stock|reserved|avail  (stock = available + reserved)
const lines = Object.values(stockMap).map(p =>
  `${p.code}|${p.available + p.reserved}|${p.reserved}|${p.available}`
).join('\n');
window.__stockLines = lines;
`✅ ${Object.keys(stockMap).length} SKUs across ${page-1} pages`
```

จากนั้นดึงข้อมูลทั้งหมด (อาจต้องดึงหลายช่วงถ้า output truncated):
```javascript
window.__stockLines.split('\n').slice(0, 70).join('\n')
// แล้วตามด้วย slice(70), slice(140) ฯลฯ จนครบ
```

**ข้อสังเกตสำคัญ:**
- `available` = คงเหลือ (ใช้เป็น avail ใน Dashboard)
- `reserved` = จอง
- `available + reserved` = สต๊อก (ตัวเลขในคอลัมน์ "สต๊อก" บน Shipnity)
- ครบ ~193 SKUs จาก 5 หน้า (82 parents × multiple subproducts)
- ถ้า `window.__stockConflicts.length > 0` หลังรัน Step 2 ให้ตรวจดูก่อนเซฟ — มี SKU code
  ที่ปรากฏซ้ำ 2 record ขึ้นไป (สคริปต์เลือก record ที่ available สูงกว่าให้อัตโนมัติแล้ว
  แต่ควร spot-check ว่าเลือกถูกจริง โดยเทียบกับหน้า UI ค้นหา SKU นั้นตรงๆ)
- **เคสที่เจอแล้ว:**
  - `SSUG050024` ("Sugar 5L") มี 2 record ซ้ำ — subproduct ใต้ family "Sugar"
    (ค้าง avail:0) กับ standalone product (avail จริง 14) — แก้แล้ว 17 ส.ค. 2569
  - `EFOM000001` ("Foam cannon") มี 2 record ซ้ำ — top-level product จริงที่ active
    (total:545, reserved:2, avail:543) กับ subproduct เสียชื่อ "ค่าเริ่มต้น" (default
    value) ที่มีค่า avail ติดลบ (total:0, reserved:2, avail:-2) — เจอและแก้แล้ว
    17 ส.ค. 2569 เช่นกัน ด้วย dedup logic เดียวกัน (script เลือก 543 ถูกต้องอัตโนมัติ)
  - ตรวจ full catalog ครบทั้ง 190 SKU / 5 หน้าแล้วเมื่อ 17 ส.ค. 2569 (ผ่าน
    `window.__stockConflicts`) — พบแค่ 2 เคสนี้เท่านั้น ไม่มี SKU อื่นที่มี code ซ้ำ
  - ถ้าเจอ SKU อื่นแบบเดียวกันอีกในอนาคต ให้ยืนยันด้วยการค้นหาชื่อสินค้าในช่องค้นหา
    หน้า Shipnity แล้วดูว่ามีกี่แถวที่โชว์ code ซ้ำกัน ก่อนเชื่อผลจากสคริปต์เสมอ

---

## Step 3 — Save stock_snapshot.json

⚠️ **สำคัญมาก — path ต้องตรงกับที่ update_stock.py อ่านจริง:**
`update_stock.py` อ่านจาก `Data Shipnity/Stock/stock_snapshot.json` (มี subfolder "stock" — ไม่ใช่ root ของ "Data Shipnity")
ถ้าเซฟผิด path (เช่น root "Data Shipnity/stock_snapshot.json") ไฟล์จะไม่ถูกอ่านเลย
update_stock.py จะเจอ snapshot เก่าค้างและ auto-flag "⚠️ ข้อมูลเก่า N วัน" ทั้งที่เพิ่งดึงข้อมูลสดมา — เคยเกิดบั๊คนี้มาแล้วเมื่อ 2026-07-19 ทำให้ Forecast ค้างที่วันที่ 18 ก.ค. ทั้งที่ auto-commit รันไปแล้ว

สร้างไฟล์ `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Shipnity/stock/stock_snapshot.json` จากข้อมูลที่ได้ (ใช้ path นี้เท่านั้น):

```python
import json
from datetime import datetime
from pathlib import Path

# ใส่ข้อมูลที่ได้จาก Step 2
sku_lines = """... (ข้อมูล SKU จาก browser)"""
parent_lines = """... (ข้อมูล parent จาก browser)"""

products = []
for line in sku_lines.strip().split('\n'):
    if not line.strip(): continue
    parts = line.split('|')
    if len(parts) >= 4:
        products.append({"code":parts[0],"total":int(parts[1]),"reserved":int(parts[2]),"available":int(parts[3]),"sold":int(parts[4]) if len(parts)>4 else 0})

for line in parent_lines.strip().split('\n'):
    if not line.strip(): continue
    parts = line.split('|')
    if len(parts) >= 4:
        products.append({"code":parts[0],"total":int(parts[1]),"reserved":int(parts[2]),"available":int(parts[3]),"sold":0})

out = {"fetched_at": datetime.now().isoformat(), "products": products}
Path("/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Shipnity/stock/stock_snapshot.json").write_text(
    json.dumps(out, ensure_ascii=False), encoding='utf-8'
)
print(f"✅ Saved {len(products)} products")
```

---

## Step 4 — Run update_stock.py

```bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
python3 update_stock.py
```

ถ้า update_stock.py ไม่มี ให้ใช้ inline script นี้แทน:

```python
import json, re
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path("/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All")
raw = json.loads((BASE / "Data Shipnity/stock/stock_snapshot.json").read_text(encoding='utf-8'))
raw_list = raw["products"] if isinstance(raw, dict) and "products" in raw else raw
ship_map = {p["code"]: p for p in raw_list if isinstance(p, dict) and p.get("code")}

DASHBOARD = BASE / "Procurement_Dashboard.html"
html = DASHBOARD.read_text(encoding='utf-8')
m = re.search(r'const PRODUCTS = (\[.*?\]);', html, re.DOTALL)
products = json.loads(m.group(1))
today = datetime.now().date()

for p in products:
    ship = ship_map.get(p.get("sku",""))
    if not ship: continue
    p["stock"] = ship.get("total",0) or 0
    p["reserved"] = ship.get("reserved",0) or 0
    p["avail"] = ship.get("available",0) or 0
    burn = p.get("burn",0) or 0
    avail = p["avail"]
    if avail <= 0:
        p["days"] = 0; p["stockout"] = today.strftime("%Y-%m-%d"); p["status"] = "oos"
    elif burn <= 0:
        p["days"] = 999; p["stockout"] = "2099-12-31"; p["status"] = "ok"
    else:
        days = int(avail/burn); p["days"] = days
        p["stockout"] = (today+timedelta(days=days)).strftime("%Y-%m-%d")
        p["status"] = "oos" if days<=0 else "critical" if days<=20 else "low" if days<=45 else "ok"

new_json = json.dumps(products, ensure_ascii=False, separators=(',',':'))
html_new = re.sub(r'const PRODUCTS = \[.*?\];', f'const PRODUCTS = {new_json};', html, flags=re.DOTALL)
date_str = today.strftime("%d/%m/%Y")
html_new = re.sub(r'(id="table-note">)[^<]*', rf'\g<1>อัปเดตล่าสุด: {date_str} — Shipnity live', html_new)
DASHBOARD.write_text(html_new, encoding='utf-8')
print(f"✅ Updated Procurement_Dashboard.html — {date_str}")
```

---

## Step 5 — Bump sw.js + Git commit + สร้าง push_now.command

```bash
# Bump sw.js
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/bump_sw.py"   # ห้ามใช้ sed -i — BSD sed บน macOS พังเงียบ ๆ (sw.js จะไม่ถูก bump)
echo "sw.js: v${CURRENT} → v${NEW}"

# Git commit (ไม่ push เอง — sandbox push ติด proxy HTTP 403)
# ห้ามลบ .git/*.lock — มีงานตั้งเวลาอื่นรันพร้อมกันได้ ถ้าติดให้รอ 20 วิแล้วลองใหม่ สูงสุด 3 ครั้ง
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" add Procurement_Dashboard.html sw.js "Data Shipnity/stock_snapshot.json"
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" commit -m "auto-update: Stock forecast $(date +%Y-%m-%d) — Shipnity live"
echo "✅ Committed — รอ user กด push_now.command"

# สร้าง push_now.command
cat > "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/push_now.command" << 'EOF'
#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
# ห้ามลบ .git/*.lock — มีงานตั้งเวลาอื่นรันพร้อมกันได้ ถ้าติดให้รอ 20 วิแล้วลองใหม่ สูงสุด 3 ครั้ง
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
EOF
chmod +x "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/push_now.command"
```

---

## หมายเหตุ

- ถ้า Shipnity ต้องการ login: หยุดและรายงาน
- git push จาก sandbox จะล้มเหลว HTTP 403 (proxy) → commit ไว้แล้วรายงานให้ user กด push_now.command
- ไฟล์ที่อัปเดต: Procurement_Dashboard.html, sw.js, Data Shipnity/stock_snapshot.json
- navigate ค้าง → ตรวจสอบว่าใช้ browser_batch ไม่ใช่ navigate standalone