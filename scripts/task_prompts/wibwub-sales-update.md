---
name: wibwub-sales-update
description: ทุกวัน 08:30/19:30 — อ่าน Google Sheets (Shopee/TikTok/Lazada) อัปเดตหน้า ยอดขาย ใน Dashboard + Mobile
---

<!-- LOCAL-OVERRIDE v1 -->
> **อ่านก่อน — ข้อนี้ทับคำสั่งที่ขัดกันในไฟล์นี้ทั้งหมด**
> ไฟล์นี้เขียนไว้ตอนรันบน Cowork cloud sandbox ตอนนี้ย้ายมารันบนเครื่อง Mac แล้ว
> - BASE / ALL_MNT = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All` · Downloads = `/Users/thanasablilutanon/Downloads` · OUTPUTS = `/Users/thanasablilutanon/Library/Caches/wibwub-outputs`
> - `git push` **ไม่ต้องทำ** และจะ**ไม่**เจอ error 403 แบบ sandbox — launchd `com.wibwub.autopush` push ให้เองทุก 2 นาที ข้ามทุกหัวข้อที่พูดถึง 403 / การสร้างหรือแก้ `push_now.command`
> - ที่ไหนเขียนว่า `mcp__workspace__bash` ให้ใช้ Bash tool ปกติแทน
> - อ่านไฟล์ในเครื่องใช้ Read/Bash ได้ตรง ๆ ไม่ต้องผ่าน connector
> - ถ้าขั้นไหนอ้าง path หรือเครื่องมือที่ไม่มีจริง: **หยุดและรายงาน ห้ามเดาทางเอง**

## WIBWUB Sales Sheet Update — จันทร์+พฤหัส 09:30

อ่าน Google Sheets ทั้ง 3 sheet (Shopee / TikTok / Lazada) หลังพนักงานอัปเดตข้อมูลแล้ว
แล้วอัปเดตหน้า **ยอดขาย > ยอดขาย & รายได้ / Shopee / TikTokShop / Lazada**
ใน WIBWUB_Dashboard.html และ WIBWUB_Mobile.html

---

## 🛡️ CRITICAL PROTECTION — ต้องทำก่อน write ทุกครั้ง

**⚠️ ประวัติบั๊ก (2026-08-03): ห้ามทำแบบเดิมเด็ดขาด** — เวอร์ชันก่อนหน้าของ STEP 0 นี้เคยเพิ่ม
label เดือนใหม่เข้า `M5` โดยอิงจาก `today.month` เพียงอย่างเดียว โดยไม่เช็คว่า SH_REV/TK_REV/LZ_REV
ฯลฯ มีค่าจริงของเดือนนั้นหรือยัง ผลคือ `M5` มี 8 elements (รวม "ส.ค.") แต่ SH_REV/TK_REV/LZ_REV
มีแค่ 7 elements (ถึง ก.ค.) ทำให้กราฟเดือนล่าสุดว่าง/พัง — **ห้ามเพิ่ม label ใน M5 (หรือ
MONTH_LABELS_FULL/MONTH_LABELS_SHORT/MP_MONTH_BOUNDS) เดี่ยวๆ โดยไม่เพิ่มค่าจริงลงทุก data array
ในการรันเดียวกันเด็ดขาด**

**กฎใหม่:** STEP 0 มีหน้าที่แค่ **ตรวจสอบและเตือน** (verify-only) ไม่ใช่แก้ไขไฟล์ การเพิ่มเดือนใหม่
(ทั้ง label และค่าจริง) ต้องเกิดพร้อมกันใน STEP 2 เท่านั้น หลังจากยืนยันแล้วว่า Sheet ต้นทางมีข้อมูล
เดือนนั้นจริง (มี row สุดท้ายของเดือนนั้นแล้ว)

```python
import re
from datetime import date

today = date.today()

for filepath in [
    '/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/WIBWUB_Dashboard.html',
    '/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/WIBWUB_Mobile.html'
]:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # ตรวจว่า M5 กับ SH_REV/TK_REV/LZ_REV มีจำนวน elements ตรงกันหรือไม่ (แค่ log ห้ามแก้ไฟล์ตรงนี้)
    m5 = re.search(r'const M5\s*=\s*\[(.*?)\]', html)
    shrev = re.search(r'const SH_REV\s*=\s*\[(.*?)\]', html)
    if m5 and shrev:
        m5_count = len([x for x in m5.group(1).split(',') if x.strip()])
        sh_count = len([x for x in shrev.group(1).split(',') if x.strip()])
        if m5_count != sh_count:
            print(f"⚠️ MISMATCH in {filepath.split('/')[-1]}: M5 has {m5_count} months, SH_REV has {sh_count} — "
                  f"DO NOT blindly pad M5. Investigate and fix both together in STEP 2, using verified sheet data only.")
        else:
            print(f"✅ M5/SH_REV length OK in {filepath.split('/')[-1]}: {m5_count} months")
```

**กฎ:** อัปเดตเฉพาะ index ของเดือนปัจจุบัน — ห้ามสร้าง array ใหม่ทั้งหมด (จะทำให้เดือนก่อนหาย)
```python
# ✅ ถูก: อัปเดต index เดียว
array[month_idx] = new_value

# ❌ ผิด: สร้าง array ใหม่ทั้งหมด (ทำให้เดือนก่อนหาย!)
# array = [val1, val2, ...]
```

**กฎเพิ่มเดือนใหม่ (เช่น ส.ค.):** ต้องเช็คก่อนว่า Sheet ต้นทาง (Shopee/TikTok/Lazada — ดู STEP 1)
มี row สุดท้ายของเดือนใหม่แล้วจริงๆ (ไม่ใช่แค่ยังไม่มีเลย) ถ้ายังไม่มี → **ห้าม push label เดือนใหม่
เข้า M5/MONTH_LABELS_FULL/MONTH_LABELS_SHORT/MP_MONTH_BOUNDS เลย** ปล่อยไว้เป็นเดือนล่าสุดที่มีข้อมูลจริง
แล้ว log "เดือนนี้ยังไม่มีข้อมูลใน Sheet — ข้าม" ถ้ามีข้อมูลแล้ว → push label + ค่าจริงทุก array
(SH_REV, TK_REV, LZ_REV, SH_ORD, SH_CANCEL_PCT, SH_ADS, SH_FEE, LZ_ADS, LZ_FEE, LZ_COUPON,
LZ_COST_PCT, ฯลฯ) พร้อมกันในขั้นตอนเดียว รวมถึง MONTH_LABELS_FULL/SHORT และ MP_MONTH_BOUNDS ด้วย
(ดู STEP 3B) — ห้ามแก้แค่ M5 อย่างเดียว

---

---

### Workspace paths
- Shell base: /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/

---

## STEP 1: อ่าน Google Sheets ผ่าน Google Drive MCP

ใช้ `mcp__631cf5b2-d348-4eff-a244-06b07fea56f7__read_file_content` หรือ `download_file_content`

**Shopee Sheet:**
- fileId: `19P7945wP4mQI0zzWA3qgFsEFOd1VQOLctLfSM0TJMos`
- URL: https://docs.google.com/spreadsheets/d/19P7945wP4mQI0zzWA3qgFsEFOd1VQOLctLfSM0TJMos/edit?gid=1820466351
- อ่าน row สุดท้ายของแต่ละเดือน (row ล่าสุดคือยอดสะสมจริง)
- Columns: ยอดสุทธิ, orders, cancel%, ads spend, platform fee

**TikTok Sheet:**
- fileId: `1k22c3PGY6aQjygAX6df_rQLR8aTzL-iz`
- URL: https://docs.google.com/spreadsheets/d/1k22c3PGY6aQjygAX6df_rQLR8aTzL-iz/edit?gid=150856480
- อ่าน row สุดท้ายของแต่ละเดือน
- Columns: ยอดสุทธิ, ads spend, commission

**Lazada Sheet:**
- fileId: `1x8bbjZxgoQe6bT4s1_S8W2A9EONsI4bl4d4znwq9t7E`
- URL: https://docs.google.com/spreadsheets/d/1x8bbjZxgoQe6bT4s1_S8W2A9EONsI4bl4d4znwq9t7E/edit?gid=1032656124
- อ่าน row สุดท้ายของแต่ละเดือน
- Columns: ยอดสุทธิ, ads, fee, coupon, cost%

**กฎสำคัญ:** แต่ละ sheet มีหลาย row ต่อเดือน (เช่น 01-10/05, 01-17/05, 01-31/05)
ต้องใช้ **row สุดท้ายของแต่ละเดือนเท่านั้น** = ยอดสะสมจริง

---

## STEP 2: Map ข้อมูลเข้า arrays

Arrays indexed 0=ม.ค., 1=ก.พ., 2=มี.ค., 3=เม.ย., 4=พ.ค., 5=มิ.ย., ...

อัปเดตค่าเดือนปัจจุบัน (month_idx = today.month - 1):

**WIBWUB_Dashboard.html และ WIBWUB_Mobile.html — arrays ต้องตรงกัน:**

| Array | ที่มา |
|---|---|
| `SH_REV` | Shopee ยอดสุทธิ |
| `TK_REV` | TikTok ยอดสุทธิ |
| `LZ_REV` | Lazada ยอดสุทธิ |
| `SH_ORD` | Shopee orders |
| `SH_CANCEL` / `SH_CANCEL_PCT` | Shopee cancel% |
| `SH_ADS` | Shopee ads spend |
| `SH_FEE` | Shopee platform fee |
| `LZ_ADS` | Lazada ads |
| `LZ_FEE` | Lazada fee |
| `LZ_COUPON` | Lazada coupon |
| `LZ_COST_PCT` | Lazada cost% |
| `TOTAL_REV` | SH_REV + TK_REV + LZ_REV |
| `TOTAL_ORD` | total orders |

---

## STEP 3: อัปเดต hardcoded KPI text

หลังอัปเดต arrays แล้ว ต้องแก้ hardcoded text ที่ไม่คำนวณจาก JS ด้วย:

**WIBWUB_Dashboard.html:**
- hh-grid: ยอดแต่ละ platform เดือนปัจจุบัน
- Sales overview KPI strip
- Header date range: "ม.ค. – {เดือนปัจจุบัน} 2569"
- Data coverage footnote

**WIBWUB_Mobile.html:**
- Home hero: ยอดขายรวม, orders, AOV
- mks-grid: ยอด Shopee/TikTok/Lazada

---

## STEP 3B: อัปเดต Date Picker ใน WIBWUB_Dashboard.html

ทุกครั้งที่มีเดือนใหม่เพิ่มขึ้น (month_idx > 4 หรือ month_idx เพิ่มจากครั้งก่อน) ต้องอัปเดต:

```python
import re, calendar
from datetime import date

today = date.today()
month_idx = today.month - 1  # 0-based

# สร้าง date range ถึงวันนี้
new_max = today.strftime('%Y-%m-%d')

# Thai month names (short)
THAI_SHORT = ['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.']
THAI_FULL_YEAR = [f'{m} 2569' for m in THAI_SHORT]

# สร้าง MONTH_BOUNDS ใหม่ทุกเดือน
bounds = []
for m in range(1, today.month + 1):
    last_day = today.day if m == today.month else calendar.monthrange(today.year, m)[1]
    bounds.append(f"{{s:'{today.year}-{m:02d}-01',e:'{today.year}-{m:02d}-{last_day:02d}'}}")
bounds_str = ','.join(bounds)

labels_full = str(THAI_FULL_YEAR[:today.month]).replace('"',"'")
labels_short = str(THAI_SHORT[:today.month]).replace('"',"'")

# อ่านไฟล์และแก้ค่า
with open('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/WIBWUB_Dashboard.html', 'r') as f:
    html = f.read()

html = re.sub(r"const MP_DATE_MAX = '[^']*';", f"const MP_DATE_MAX = '{new_max}';", html)
html = re.sub(r'const MP_MONTH_BOUNDS = \[[^\]]*\];', f'const MP_MONTH_BOUNDS = [{bounds_str}];', html)
html = re.sub(r"const MONTH_LABELS_FULL = \[[^\]]*\];", f"const MONTH_LABELS_FULL = {labels_full};", html)
html = re.sub(r"const MONTH_LABELS_SHORT = \[[^\]]*\];", f"const MONTH_LABELS_SHORT = {labels_short};", html)
html = re.sub(r"let rangeStart = 0, rangeEnd = \d+;", f"let rangeStart = 0, rangeEnd = {month_idx};", html)

with open('/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/WIBWUB_Dashboard.html', 'w') as f:
    f.write(html)
print(f"Date picker updated → MP_DATE_MAX={new_max}, rangeEnd={month_idx}")
```

---

## STEP 4: Bump sw.js + Git commit + Push

```bash
CURRENT=$(grep -oP "wibwub-v\K[0-9]+" /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/sw.js)
NEW=$((CURRENT + 1))
sed -i "s/wibwub-v${CURRENT}/wibwub-v${NEW}/" /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/sw.js

cd /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All
rm -f .git/index.lock .git/HEAD.lock
git add WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js
git commit -m "auto-update: sales from Sheets $(date +%Y-%m-%d) — SH/TK/LZ arrays"
```

หลัง commit แล้ว — สร้าง push_now.command (sandbox push ติด proxy HTTP 403 ไม่ push เอง):
```bash
echo "✅ Committed — รอ user กด push_now.command"
cat > "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/push_now.command" << 'EOF'
#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
EOF
chmod +x "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/push_now.command"
```

---

## หากมีข้อผิดพลาด
- Google Drive ไม่ตอบสนอง → log "Google Drive MCP unavailable" และ skip
- Sheet ยังไม่มีข้อมูลเดือนนี้ → ใช้ข้อมูลเดือนล่าสุดที่มี แล้ว log แจ้ง
- ข้อมูลเดือนนี้ไม่เปลี่ยนแปลงจากครั้งก่อน → log "No new data" และ skip commit