---
name: wibwub-daily-followers
description: ดาวน์โหลด TikTok Followers จาก TikTok Studio ทุกวัน 09:00/20:00 → อัปเดต soc_follow chart + Mobile KPI → commit + push_now.command
---

## WIBWUB Daily TikTok Followers Update

ดาวน์โหลดข้อมูล followers จาก TikTok Studio แล้วอัปเดต dashboard ทุกวัน

### BASE PATH
- Workspace: `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`
- Shell: `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/`
- Downloads: `/Users/thanasablilutanon/Downloads/`

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

## Step 1 — Navigate ไป TikTok Studio Followers

1. ⚠️ **ต้องระบุ browser ที่ Mac เสมอ ห้ามปล่อยให้เลือกอัตโนมัติ** — ถ้ามีหลาย browser connected อาจไปรันบน PC โดยไม่ตั้งใจ:
   `select_browser(deviceId="b75a6bb0-5b78-4e44-92a8-75224f1ce4ee")` → `tabs_context_mcp(createIfEmpty=true)`
   (ถ้า deviceId นี้ไม่ connected แล้ว ให้เรียก `list_connected_browsers` ก่อน แล้วเลือกตัวที่ `osPlatform` เป็น macOS / `isLocal:true` เท่านั้น — ห้ามเลือก Windows/PC)

2. Navigate ด้วย browser_batch (ห้ามใช้ navigate standalone):
   - URL: `https://www.tiktok.com/tiktokstudio/analytics/followers`
   - wait 3s → screenshot
   - ถ้า redirect ไป login page → หยุดและรายงาน "ต้องการ login TikTok Studio"

## Step 2 — เปลี่ยน Date Range เป็น 60 วัน

1. คลิกปุ่ม date range (มุมขวาบน แสดง "7 วันล่าสุด")
2. คลิก "60 วัน"
3. Wait 2 วินาที

## Step 3 — Download ไฟล์ CSV

1. คลิกปุ่ม "ดาวน์โหลดข้อมูล" (มุมขวาบน มีไอคอน ↓)
2. Dialog จะเปิด → คลิก radio button "CSV"
3. คลิก "ดาวน์โหลด"
4. Wait 3 วินาที → ไฟล์จะอยู่ใน Downloads เป็น `Followers_wibwubcar (N).zip`

## Step 4 — รัน update_followers.py

```bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
python3 update_followers.py
```

ถ้า script ไม่มี ให้รัน inline:
```python
import os, re, csv, zipfile, glob
from datetime import datetime
from pathlib import Path

BASE   = Path("/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All")
DL     = Path("/Users/thanasablilutanon/Downloads")

# หา zip ล่าสุด
all_zips = glob.glob(str(DL / "Followers_wibwubcar*.zip")) + \
           glob.glob(str(BASE / "data content/Followers_wibwubcar*.zip"))
if not all_zips: raise FileNotFoundError("ไม่พบ Followers zip")
zip_path = max(all_zips, key=os.path.getmtime)

# อ่าน CSV
rows = []
with zipfile.ZipFile(zip_path) as z:
    for name in z.namelist():
        if 'History' in name:
            data = z.read(name).decode('utf-8-sig')
            for i, line in enumerate(data.strip().split('\n')):
                if i == 0: continue
                parts = [p.strip().strip('"') for p in line.split(',')]
                if len(parts) >= 2 and parts[1].isdigit():
                    rows.append((parts[0], int(parts[1])))

latest_date, latest_count = rows[-1]
latest_k = round(latest_count / 1000, 3)
jan_count = next((c for d,c in rows if 'มกราคม' in d), None)
delta_str = f"+{round((latest_count-jan_count)/1000,1)}K จาก ม.ค." if jan_count else ""
cur_idx = datetime.now().month - 1

# อัปเดต Dashboard
dash = (BASE / "WIBWUB_Dashboard.html").read_text(encoding='utf-8')
def upd(html, val, idx):
    def rep(m):
        vals = [v.strip() for v in m.group(1).split(',')]
        while len(vals) <= idx: vals.append('null')
        vals[idx] = str(val)
        while vals and vals[-1] == 'null': vals.pop()
        return "{label:'TikTok',data:[" + ','.join(vals) + "]"
    return re.sub(r"\{label:'TikTok',data:\[([^\]]+)\]", rep, html)
(BASE / "WIBWUB_Dashboard.html").write_text(upd(dash, latest_k, cur_idx), encoding='utf-8')

# อัปเดต Mobile
mobile = (BASE / "WIBWUB_Mobile.html").read_text(encoding='utf-8')
disp_k = f"{latest_k:.1f}K"
mobile = re.sub(r'(TK Followers</div><div class="mks-val">)[^<]+(</div>)', rf'\g<1>{disp_k}\g<2>', mobile)
if delta_str:
    mobile = re.sub(r'(TK Followers.*?mks-sub">)[^<]+(</div>)', rf'\g<1>{delta_str}\g<2>', mobile, flags=re.DOTALL)
(BASE / "WIBWUB_Mobile.html").write_text(mobile, encoding='utf-8')
print(f"✅ Updated: {latest_count:,} followers ({latest_date})")
```

## Step 5 — Bump sw.js + Git commit + สร้าง push_now.command

```bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
CURRENT=$(grep -o 'wibwub-v[0-9]*' sw.js | head -1 | grep -o '[0-9]*')
NEW=$((CURRENT + 1))
sed -i "s/wibwub-v${CURRENT}/wibwub-v${NEW}/" sw.js
echo "sw.js: v${CURRENT} → v${NEW}"

# Git commit (ไม่ push เอง — sandbox push ติด proxy HTTP 403)
rm -f .git/index.lock .git/HEAD.lock
git add WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js
git commit -m "auto-update: TikTok followers $(date +%Y-%m-%d) — ${latest_count} followers"
echo "✅ Committed — รอ user กด push_now.command"

# สร้าง push_now.command
cat > "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/push_now.command" << 'EOF'
#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
EOF
chmod +x "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/push_now.command"
```

## หมายเหตุ
- ไฟล์ zip ที่ download อาจชื่อ `Followers_wibwubcar (N).zip` หรือ `Followers_wibwubcar.zip`
- ถ้า download ไม่สำเร็จ ให้ลอง DOM scraping แทน: `document.body.innerText` หา "ผู้ติดตามทั้งหมด" แล้วดูค่าถัดไป
- ไฟล์ TikTok export มีข้อมูล 60 วันย้อนหลัง อัปเดตทุกวันจะได้ข้อมูล realtime
- git push จาก sandbox จะล้มเหลว HTTP 403 (proxy) → commit ไว้แล้วรายงานให้ user กด push_now.command
- navigate ค้าง → ตรวจสอบว่าใช้ browser_batch ไม่ใช่ navigate standalone