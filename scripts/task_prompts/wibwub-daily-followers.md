---
name: wibwub-daily-followers
description: ดาวน์โหลด TikTok Followers จาก TikTok Studio ทุกวัน 09:00/20:00 → อัปเดต soc_follow chart + Mobile KPI → commit
---
> ⚠️ ไฟล์นี้ไม่มีงานไหนใช้อยู่ (ณ 29 ต.ค. 69) — ตัวจริงอยู่ที่ `~/Documents/Claude/Scheduled/wibwub-daily-followers/SKILL.md` · ห้ามแก้ที่นี่โดยคิดว่ามีผล


## 📂 ขั้น 0 — หาโฟลเดอร์ All ก่อนเสมอ (ทำก่อนทุกอย่าง)

พรอมป์นี้ถูกเรียกได้จาก **2 ฝั่ง** และโฟลเดอร์ All อยู่คนละที่กัน
จึง**ห้ามฝังพาธตายตัว** ให้หาด้วยคำสั่งนี้ทุกครั้ง แล้วใช้ผลลัพธ์เป็น `BASE`

```bash
for d in "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" "$HOME/mnt/All" /sessions/*/mnt/All; do [ -d "$d/scripts" ] && echo "$d" && break; done
```

- ได้พาธมา → ใช้เป็น `BASE` ในทุกคำสั่งถัดไป (เขียนพาธเต็มเสมอ ห้ามใช้ตัวแปร shell)
- **ไม่เจอ** หรือ shell ตอบว่า `No folders are connected`
  → **หยุดทันที** รายงานว่า `❌ ล้มเหลว — เข้าโฟลเดอร์ All ไม่ได้` แล้วจบงาน
  ห้ามเดาพาธเอง ห้ามไปใช้ `~/Downloads` แทน

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
    # count=1 สำคัญ: มี "TK Followers" 2 ที่ (บรรทัด ~394 การ์ด mks, ~1637 การ์ด kc)
    # ที่สองไม่มี mks-sub ของตัวเอง ถ้าไม่จำกัดจำนวน DOTALL จะวิ่งไปทับ '+it.d+' ใน mksRatio()
    mobile = re.sub(r'(TK Followers.*?mks-sub">)[^<]+(</div>)', rf'\g<1>{delta_str}\g<2>', mobile, count=1, flags=re.DOTALL)
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
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" add WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" commit -m "auto-update: TikTok followers $(date +%Y-%m-%d) — ${latest_count} followers"
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

## 🚨 ทำงานไม่ได้ = ต้องรายงานว่าล้มเหลว ห้ามขึ้นว่าสำเร็จ

**กรณีที่ถือว่าล้มเหลว**

1. **เข้าโฟลเดอร์ All ไม่ได้** (ขั้น 0 ไม่เจอพาธ)
2. **เปิดเว็บไม่ได้** — `navigate`/`browser_batch` คืนข้อความใดข้อความหนึ่งนี้
   - `The approval prompt for this browser action went unanswered for 5 minutes` (กล่องขออนุญาตไม่มีคนกด)
   - `Navigation to this domain is not allowed` (สิทธิ์โดเมนถูกปฏิเสธ)
   - `Tab ... is not in Claude's tab group` / เชื่อมต่อส่วนขยายไม่ได้
3. **สคริปต์ที่พรอมป์ระบุหายหรือพัง**

**สิ่งที่ต้องทำเมื่อล้มเหลว**

1. **ลองครั้งเดียวพอ ห้ามวนลองซ้ำ** — เคยเสียเวลา 5 นาทีต่อหนึ่งเว็บโดยไม่ได้อะไร
   (22 ต.ค. 69 งาน HR ลองทั้ง `browser_batch` และ `javascript_tool` ตรงไปที่แท็บที่ล็อกอินค้างอยู่
   ก็โดนกล่องเดียวกันทั้งคู่ — แท็บที่เปิดค้างไว้ช่วยไม่ได้)
2. ปิดแท็บที่เปิดไว้ด้วย `tabs_close_mcp`
3. จบงานโดยขึ้นต้นบรรทัดแรกด้วย
   `❌ ล้มเหลว — <สาเหตุสั้น ๆ> ไม่ได้ข้อมูลใหม่รอบนี้`
   แล้วบอกด้วยว่าข้อมูลล่าสุดในไฟล์อยู่ถึงวันไหน

**ห้ามทำเด็ดขาด**

- ❌ ห้ามหันไปใช้ไฟล์เก่าแล้วรายงานว่า "สำเร็จ" — ถ้าดึงของใหม่ไม่ได้ ถือว่าล้มเหลว
- ❌ ห้ามเขียน ✅ หรือคำว่า "เสร็จ/สำเร็จ/OK" เมื่อขั้นใดขั้นหนึ่งข้างบนไม่ผ่าน
- ❌ ห้ามเดาตัวเลข หรือคัดลอกตัวเลขจากรอบก่อนมาใส่

> ใช้ไฟล์เดิมได้เฉพาะกรณีที่พรอมป์ระบุไว้ชัดเจนว่าเป็นทางสำรองที่ยอมรับได้
> (เช่น ads-daily ใช้ `work/*.json` ที่ครอบช่วง `from→to` พอดี) และต้อง**รายงานตรง ๆ
> ว่ารอบนี้ใช้ของเดิม ไม่ได้ดึงใหม่**

---

## 🚫 กฎคำสั่ง shell (ทุกงาน — รวมคำสั่งที่คิดขึ้นเองระหว่างรัน)

งานตั้งเวลา **ไม่มีคนนั่งกดอนุญาต** ถ้าคำสั่งไม่แมตช์กฎที่อนุญาตไว้แล้ว
(`Bash(python3 *)` / `Bash(git *)` / `Bash(ls *)` ฯลฯ) งานจะค้างทั้งรอบ
สังเกตง่าย ๆ: ถ้ากล่องขออนุญาตมีแค่ปุ่ม **"Allow once"** โดยไม่มี "Always allow"
แปลว่าคำสั่งนั้นสร้างกฎถาวรไม่ได้ จะถามใหม่ทุกครั้งตลอดไป

**เขียนคำสั่งให้เรียบง่ายที่สุด — 1 คำสั่ง = 1 โปรแกรม + พาธเต็ม**

| ❌ ห้าม | เหตุผลที่โดนถาม | ✅ ใช้แบบนี้ |
|---|---|---|
| `git ...` ทุกรูปแบบ | `git -C` เปิดช่องให้ push หลุด · `cd ... && git` ขึ้นต้นด้วย cd จึงไม่แมตช์กฎ `Bash(git add:*)` → งานค้างรออนุญาต | `python3 "<BASE>/scripts/gitw.py" add/commit/status/log` |
| `cd "<path>" && python3 x.py` | ขึ้นต้นด้วย cd ไม่แมตช์ `Bash(python3 *)` | `python3 "<path เต็ม>/x.py"` |
| `BASE="..."` แล้วใช้ `$BASE` | ตัวแปร = simple_expansion สร้างกฎถาวรไม่ได้ | เขียนพาธเต็มตรง ๆ ทุกครั้ง |
| `for d in ...; do ... done` / `if [ ... ]` | ลูป/เงื่อนไขใน bash ก็เข้าข่ายเดียวกัน | ย้ายตรรกะไปไว้ในสคริปต์ python แล้วเรียกไฟล์นั้น |
| `cmd1; cmd2; cmd3` ต่อกันยาว ๆ | คำสั่งผสมแมตช์กฎไม่ได้ | แยกเป็นคนละคำสั่ง |

**ถ้าต้องมีตรรกะ (วนลูป / เช็คเงื่อนไข / ประกอบพาธ): เขียนเป็นสคริปต์ python
ไว้ใน `scripts/` แล้วเรียกด้วยพาธเต็ม** เช่น `python3 "<path เต็ม>/scripts/ads/check_downloads.py" tiktok`
วิธีนี้ทั้งอ่านง่ายกว่า ทดสอบแยกได้ และไม่ติดกำแพงสิทธิ์

---
---

# 🔁 งานนี้มี 2 ส่วน — เพิ่มส่วน B เมื่อ 24 ต.ค. 2569

ทุกอย่างข้างบนคือ **ส่วน A (TikTok Followers)** ทำทุกรอบเหมือนเดิมทุกประการ ห้ามข้าม
**ส่วน B ทำเฉพาะทุก 5 วัน** (เช็คก่อนตามขั้น B0) · ส่วนไหนล้มก็ทำอีกส่วนต่อ · **รายงานแยก 2 หัวข้อ**

เหตุผล: งานชีตคอนเทนต์ฝั่ง code ใช้ Chrome ซึ่งรันในรอบตั้งเวลาไม่ได้ตั้งแต่เวอร์ชัน 2.1.308
งานนี้มีโดเมน `www.tiktok.com` อยู่แล้ว จึงย้าย **เฉพาะท่อนเก็บตัวเลขคลิป** มาไว้ด้วยกัน
ส่วนท่อนเขียนลงชีตยังอยู่ฝั่ง code เพราะต้องใช้ไฟล์กุญแจ service account ที่ `~/` ซึ่งแซนด์บ็อกซ์นี้เข้าไม่ถึง

## ขั้น B0 — วันนี้ต้องทำส่วน B ไหม

**เงื่อนไขต้องตรงกับ cron ของงานฝั่ง code เป๊ะ ๆ** งานนั้นใช้ `50 10 */5 * *` ซึ่งยิงเฉพาะ
**วันที่ 1, 6, 11, 16, 21, 26, 31 ของเดือน** ถ้าส่วน B ใช้เกณฑ์อื่น (เช่น นับอายุไฟล์)
วันจะเลื่อนออกจากกัน แล้วฝั่ง code จะเจอ clips.json เก่าเกิน 180 นาที → exit 3 ทุกรอบ

```bash
for d in "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All" "$HOME/mnt/All" /sessions/*/mnt/All; do
  [ -f "$d/scripts/content/content_sheet_update.py" ] && BASE="$d" && break
done
echo "BASE=$BASE"
[ -z "$BASE" ] && echo "หาโฟลเดอร์ All ไม่เจอ — หยุดส่วน B รายงาน" && exit 0

# ใช้ python3 ตัดสิน จะได้ไม่ต้องพึ่งไวยากรณ์ date/stat ที่ต่างกันระหว่าง macOS กับ Linux
python3 - "$BASE" <<'PY'
import sys, os, datetime as dt
base = sys.argv[1]
today = dt.date.today()
if (today.day - 1) % 5 != 0:
    print(f"วันนี้วันที่ {today.day} ไม่ใช่รอบ (รอบคือ 1,6,11,16,21,26,31) -> ข้ามส่วน B")
    sys.exit(1)
f = os.path.join(base, "scripts/content/work/clips.json")
if os.path.exists(f) and dt.date.fromtimestamp(os.path.getmtime(f)) == today:
    print("วันนี้เก็บไปแล้ว (clips.json ลงวันที่วันนี้) -> ข้ามส่วน B รอบนี้")
    sys.exit(1)
print(f"วันนี้วันที่ {today.day} เป็นรอบ และยังไม่ได้เก็บ -> ทำส่วน B")
PY
[ $? -ne 0 ] && exit 0
```

ด่านที่สองกันไม่ให้รอบเย็น (20:45) เก็บซ้ำหลังรอบเช้า (09:45) ทำไปแล้ว
แต่ถ้ารอบเช้าล้ม รอบเย็นจะได้ทำแทน ซึ่งยังทันงานฝั่ง code รอบถัดไป

ได้ "ข้ามส่วน B" → รายงานว่าข้ามเพราะอะไร แล้วจบ


## ขั้น B1 — เก็บตัวเลขคลิป (ห้ามแตะชีต)

อ่านไฟล์นี้ด้วย Read tool แล้วทำตาม **เฉพาะขั้นที่ 2 และ 3 เท่านั้น**:

`$BASE/scripts/task_prompts/wibwub-content-sheet.md`

- **ข้ามขั้นที่ 1 (`plan`) และขั้นที่ 4 (`write`)** สองขั้นนั้นใช้ service account งานนี้รันไม่ได้
  ถ้าเผลอรันจะได้ `ไม่พบ service account` แล้วจบ
- ไม่ต้องรู้ว่าคลิปไหนมีในชีตแล้ว **ให้เก็บคลิปล่าสุดย้อนหลังราว 10–15 คลิป** พอ
  ท่อนเขียนชีตจะเติมเฉพาะช่องที่ยังว่างอยู่แล้ว เก็บเกินมาไม่เสียหาย
- จำนวนที่ต้องได้ต่อคลิป: **5 วินาทีแรก (%) · วิว · ถูกใจ · คอมเมนต์ · แชร์ · บันทึก**
- ⚠️ 5 วินาทีแรกต้องใช้วิธี `video.currentTime = 5` แล้วอ่านป้าย `0:05 (NN%)`
  **ลาก slider หรืออ่าน canvas ไม่ได้ผล**
- ⚠️ วิวที่เกินแสนหน้าเว็บย่อเป็น `232K` ให้บันทึกเป็นตัวเลขเต็ม **232000**
- ถ้าเจอหน้า login TikTok: หยุดส่วน B รายงาน **ห้ามกรอกรหัสผ่าน**

## ขั้น B2 — บันทึกไฟล์แล้ว commit

เขียนผลเป็น JSON array ลง `$BASE/scripts/content/work/clips.json` รูปแบบนี้

```json
[{"ok":true,"video_id":"76xxxxxxxxxxxxxxxxx","retention5":58,"views":232000,
  "likes":1234,"comments":56,"shares":78,"saves":90}]
```

แล้ว commit **เฉพาะไฟล์นี้ไฟล์เดียว**

```bash
python3 "$BASE/scripts/gitw.py" add scripts/content/work/clips.json
python3 "$BASE/scripts/gitw.py" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
    commit -m "content: เก็บตัวเลขคลิป TikTok $(date +%Y-%m-%d)"
```

**สำคัญ:** งานฝั่ง code "ชีตคอนเทนต์ TikTok" จะอ่านไฟล์นี้ตอน 10:50 และมีด่าน `--max-age-min 180`
ถ้าส่วน B ล้มหรือไม่ได้เขียนไฟล์ใหม่ ท่อนนั้นจะไม่เขียนชีตซ้ำด้วยของเก่า (exit 3) — ถือว่าถูกต้อง

จบส่วน B ให้ปิดแท็บ Chrome ที่เปิดด้วย `tabs_close_mcp`

---

# รูปแบบรายงานท้ายรอบ (ภาษาไทย แยก 2 หัวข้อ)

```
## A — TikTok Followers
<สำเร็จ/ล้มเหลว> · จำนวนผู้ติดตาม · commit id

## B — เก็บตัวเลขคลิป (ทุก 5 วัน)
<สำเร็จ/ข้าม เพราะยังไม่ถึงรอบ/ล้มเหลว> · จำนวนคลิปที่เก็บได้ · commit id
```

**ห้ามเขียน ✅ หรือคำว่าสำเร็จ ถ้าส่วนใดส่วนหนึ่งไม่ผ่าน** ให้ขึ้นต้นส่วนนั้นด้วย `❌ ล้มเหลว — <สาเหตุ>`
