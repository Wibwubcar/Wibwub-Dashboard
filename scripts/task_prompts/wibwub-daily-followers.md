---
name: wibwub-daily-followers
description: ดาวน์โหลด TikTok Followers จาก TikTok Studio ทุกวัน 09:00/20:00 → อัปเดต soc_follow chart + Mobile KPI → commit
---

<!-- LOCAL-OVERRIDE v1 -->
> **อ่านก่อน — ข้อนี้ทับคำสั่งที่ขัดกันในไฟล์นี้ทั้งหมด**
> ไฟล์นี้เขียนไว้ตอนรันบน Cowork cloud sandbox ตอนนี้ย้ายมารันบนเครื่อง Mac แล้ว
> - BASE / ALL_MNT = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All` · Downloads = `/Users/thanasablilutanon/Downloads` · OUTPUTS = `/Users/thanasablilutanon/Library/Caches/wibwub-outputs`
> - `git push` **ไม่ต้องทำ** และจะ**ไม่**เจอ error 403 แบบ sandbox — launchd `com.wibwub.autopush` push ให้เองทุก 2 นาที ข้ามทุกหัวข้อที่พูดถึง 403 / การสร้างหรือแก้ `push_now.command`
> - ที่ไหนเขียนว่า `mcp__workspace__bash` ให้ใช้ Bash tool ปกติแทน
> - อ่านไฟล์ในเครื่องใช้ Read/Bash ได้ตรง ๆ ไม่ต้องผ่าน connector
> - ถ้าขั้นไหนอ้าง path หรือเครื่องมือที่ไม่มีจริง: **หยุดและรายงาน ห้ามเดาทางเอง**

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

> 🚨 **ต้องใช้ "60 วันล่าสุด" เท่านั้น ห้ามใช้ 28 / 365 / กำหนดเอง เด็ดขาด**
> export ของ TikTok **ติดป้ายวันที่ไม่เหมือนกันตามช่วงที่เลือก** — ไฟล์ 365 วันช้ากว่าไฟล์ 60 วัน
> 1 วันทุกแถว (เคยเทียบแล้ว ซ้อนกัน 59 วัน ตรงกัน 0 วัน) ถ้าเผลอใช้คนละช่วงแล้วเอามาต่อกัน
> ข้อมูลจะเหลื่อมและกราฟจะขาดช่วง (บั๊กที่เกิดจริงกับ ส.ค./ก.ย. 2569 — แก้เมื่อ 20 ต.ค.)
> ถ้าหน้าเว็บไม่มีตัวเลือก "60 วัน" ให้ **หยุดและรายงาน ห้ามเลือกช่วงอื่นแทน**

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

## Step 4B — ด่านตรวจความต่อเนื่อง (ทำทุกครั้ง ห้ามข้าม)

หลังรัน `update_followers.py` และ **ก่อน** commit ให้ตรวจว่า `start` ของทุกเดือนใน `FOL_DATA`
เท่ากับ `end` ของเดือนก่อนหน้า และ `end` ของแต่ละเดือนตรงกับ `TK_FOL` ใน `WIBWUB_Mobile.html`:

```bash
cd "$BASE" && python3 - <<'EOF'
import re,sys
d=open('WIBWUB_Dashboard.html',encoding='utf-8').read()
seg=d[d.find('const FOL_DATA'):]
ent=[]
for m in re.finditer(r"\{label:'([^']+)',start:(\d+),end:(\d+)",seg):
    ent.append((m.group(1),int(m.group(2)),int(m.group(3))))
    if m.group(1).startswith('ตุลาคม') or len(ent)>=24: break
bad=[]
for i in range(1,len(ent)):
    if ent[i][1]!=ent[i-1][2]:
        bad.append(f"{ent[i][0]}: start={ent[i][1]} แต่ {ent[i-1][0]} end={ent[i-1][2]}")
tk=[int(x) for x in re.search(r'const TK_FOL = \[([^\]]*)\]',
      open('WIBWUB_Mobile.html',encoding='utf-8').read()).group(1).split(',')]
for i,(lab,s,e) in enumerate(ent):
    if i<len(tk) and tk[i]!=e: bad.append(f"{lab}: Dashboard end={e} แต่ Mobile TK_FOL={tk[i]}")
print("ไม่ผ่าน:\n  "+"\n  ".join(bad) if bad else "ผ่าน: ทุกเดือนต่อเนื่องและตรงกับ Mobile")
sys.exit(1 if bad else 0)
EOF
```

ถ้า exit != 0 → **หยุดทันที ห้าม commit ห้ามแก้ตัวเลขเอง** ให้รายงานว่าเดือนไหนไม่ต่อเนื่อง
สาเหตุที่พบบ่อยคือใช้ export คนละช่วง (ดู Step 2) หรือสคริปต์เขียนทับเฉพาะเดือนปัจจุบัน

## Step 5 — Bump sw.js + Git commit

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/bump_sw.py"   # ห้ามใช้ sed -i — BSD sed บน macOS พังเงียบ ๆ (sw.js จะไม่ถูก bump)
echo "sw.js: v${CURRENT} → v${NEW}"

# Git commit (ไม่ push เอง — sandbox push ติด proxy HTTP 403)
# ห้ามลบ .git/*.lock — มีงานตั้งเวลาอื่นรันพร้อมกันได้ ถ้าติดให้รอ 20 วิแล้วลองใหม่ สูงสุด 3 ครั้ง
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" add WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js
git -C "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" commit -m "auto-update: TikTok followers $(date +%Y-%m-%d) — ${latest_count} followers"
echo "✅ Committed — autopush จะ push ให้เองใน 2 นาที"

```

## หมายเหตุ
- ไฟล์ zip ที่ download อาจชื่อ `Followers_wibwubcar (N).zip` หรือ `Followers_wibwubcar.zip`
- ถ้า download ไม่สำเร็จ ให้ลอง DOM scraping แทน: `document.body.innerText` หา "ผู้ติดตามทั้งหมด" แล้วดูค่าถัดไป
- ไฟล์ TikTok export มีข้อมูล 60 วันย้อนหลัง อัปเดตทุกวันจะได้ข้อมูล realtime
- **convention วันที่:** ยึดไฟล์ 60 วันเป็นหลักเสมอ · ถ้าจำเป็นต้องใช้ไฟล์ช่วงอื่นมาเติมย้อนหลัง
  ต้องเลื่อน +1 วัน (กฎที่ตรวจแล้ว: `ค่าวันที่ D ในไฟล์ 60 วัน = ค่าวันที่ D-1 ในไฟล์ 365 วัน` ตรง 60/60)
- `FOL_DATA[เดือน].start` = ยอดของวันสุดท้ายของเดือนก่อน (ไม่ใช่วันที่ 1 ของเดือนนั้น)
- ไม่ต้อง git push — launchd com.wibwub.autopush push ให้เองทุก 2 นาที
- navigate ค้าง → ตรวจสอบว่าใช้ browser_batch ไม่ใช่ navigate standalone

---

## 🚫 กฎคำสั่ง shell (ทุกงาน — รวมคำสั่งที่คิดขึ้นเองระหว่างรัน)

**ห้ามใส่ `cd` ไว้ในคำสั่งเดียวกับ `git` เด็ดขาด** ไม่ว่าจะเชื่อมด้วย `&&` `;` หรือขึ้นบรรทัดใหม่
ตัวตรวจความปลอดภัยจะหยุดงานแล้วรอคนกดอนุญาต ("changes directory before running git,
which can execute untrusted hooks") ซึ่งงานตั้งเวลาไม่มีคนนั่งกด = ค้างทั้งรอบ

| ❌ ห้าม | ✅ ใช้แบบนี้ |
|---|---|
| `cd "$BASE" && git status` | `git -C "$BASE" status` |
| `cd "$BASE"` ขึ้นบรรทัดใหม่แล้วตามด้วย `git ...` | `git -C "$BASE" ...` |
| `cd "$BASE" && python3 x.py; git status` | แยกเป็น 2 คำสั่ง · ใช้ `python3 "$BASE/x.py"` และ `git -C "$BASE" status` |

เรียกสคริปต์ด้วย path เต็มเสมอ (`python3 "$BASE/scripts/..."`) จะได้ไม่ต้อง `cd`
ถ้าจำเป็นต้อง `cd` จริง ๆ (เช่นสคริปต์อ่าน path สัมพัทธ์) **ห้ามมี `git` อยู่ในคำสั่งนั้น**
