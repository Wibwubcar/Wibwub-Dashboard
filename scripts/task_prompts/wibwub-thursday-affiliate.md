---
name: wibwub-thursday-affiliate
description: ทุกวัน 08:50/19:50 — โหลดไฟล์ TikTok Affiliate → อัปเดต Affiliate Dashboard + Mobile
---

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


## WIBWUB — อัปเดตข้อมูล Affiliate

BASE = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All`

อัปเดต `AF_MO / AF_GMV / AF_NET / AF_COM / AF_CR / CREATORS / CREATOR_MONTHS` ใน
`WIBWUB_Affiliate_Dashboard.html` และ `AFI_GMV / AFI_NET / AFI_COMM` ใน `WIBWUB_Mobile.html`

> **ห้ามเขียนสคริปต์อ่าน xlsx เอง** ตัวคำนวณจริงคือ `process_affiliate()` ใน `wibwub_update.py`
>
> เหตุผล — พรอมป์เวอร์ชันเก่า hardcode คอลัมน์ `1/2/10` ให้ทุกไฟล์ แต่ไฟล์มี **2 รูปแบบ
> ที่ตำแหน่งคอลัมน์ไม่เหมือนกัน**:
> - `Creator_List_*` : returns = col21 · commission = col7
> - `Transaction_Analysis_Creator_List_*` : returns = col4 · commission = col21
>
> ผลคือ commission ไปอ่านคอลัมน์ "จำนวนโชว์เคส" (เลขหลักหน่วย) และ net สูงกว่า gmv หรือติดลบ
> ตัวจริงใช้ `find_col()` จับจากชื่อ header จึงถูกทั้งสองแบบ
> และต้องกรองเฉพาะไฟล์ชื่อมี `Creator_List` (โฟลเดอร์มี Product_List / Video_List /
> Live_List / Core_Metrics / WIBWUB_KOL_Tracker ปนอยู่) แล้วเลือกไฟล์ที่ช่วงวันที่
> **overlap กับเดือนมากสุด** ไม่ใช่ mtime ใหม่สุด

---

## ขั้นที่ 1 — โหลดไฟล์ใหม่จาก TikTok Affiliate (ถ้ามี)

1. Chrome: `list_connected_browsers` → `select_browser` deviceId `b75a6bb0-5b78-4e44-92a8-75224f1ce4ee` → `tabs_context_mcp(createIfEmpty=true)`
2. โหลด **Creator List** ของเดือนปัจจุบันจาก TikTok Affiliate (Transaction Analysis → Creator)
   ถ้าขึ้นหน้า login: **หยุดและรายงาน ห้ามกรอกรหัสผ่าน**
3. ปิดแท็บด้วย `tabs_close_mcp`
4. ย้ายไฟล์เข้าที่ (launchd `com.wibwub.download-mover` อาจย้ายให้แล้ว):

```bash
ls -lt "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Affiliate"/*Creator_List*.xlsx | head -3
```

ถ้าไม่มีไฟล์ใหม่ก็ **ไม่เป็นไร** — ขั้นถัดไปจะคำนวณจากไฟล์ที่มีอยู่และจบด้วย `NO_CHANGE`

## ขั้นที่ 2 — ดูก่อนว่าจะเปลี่ยนอะไร

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/affiliate_update.py" --dry-run
```

ตรวจด้วยตา: `latest_month` ควรเป็นเดือนปัจจุบัน · `AF_GMV` ไม่ควรต่ำกว่า `current_page.AF_GMV`
· `AF_NET` ต้อง ≤ `AF_GMV` · `AF_COM` ควรเป็นหลักแสน ไม่ใช่หลักหน่วย

ด่านที่สคริปต์จะปฏิเสธการเขียน: net > gmv · net ติดลบ · commission เล็กผิดปกติ ·
เดือนหดลง · GMV เดือนเก่าลดเกิน 2%
ถ้า `status` เป็น `ERROR` → **หยุดและรายงาน ห้ามแก้ตัวเลขเอง**

## ขั้นที่ 3 — รันจริง

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/affiliate_update.py"
```

exit `0` = อัปเดต + bump sw.js แล้ว · `10` = ไม่มีอะไรเปลี่ยน · `2` = ไม่ผ่านด่าน
ดู `mobile_mismatch` ต้องเป็น `[]` (ค่าใน Mobile ตรงกับ Affiliate Dashboard)

## ขั้นที่ 4 — VIDEOS (ถ้ามีไฟล์วีดีโอใหม่)

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/vid_merge.py"
```

อ่านจาก `Data Affiliate/วีดีโอ/` แล้ว merge เข้า `const VIDEOS` ในหน้า Affiliate
(พรอมป์เก่าคัดลอกโค้ดตัวนี้มาทั้งก้อน — ใช้ไฟล์จริงแทน อย่า inline)

## ขั้นที่ 5 — commit (เฉพาะตอนมีอะไรเปลี่ยน)

```bash
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" add WIBWUB_Affiliate_Dashboard.html WIBWUB_Mobile.html sw.js "Data Affiliate"
python3 "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/scripts/gitw.py" -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" \
    commit -m "auto-update: Affiliate $(date +%Y-%m-%d)"
```

ไม่ต้อง `git push` — launchd `com.wibwub.autopush` push ให้เองภายใน 2 นาที
ถ้า git ติด `index.lock`: รอ 20 วินาทีแล้วลองใหม่ สูงสุด 3 ครั้ง **ห้ามลบ lock ของคนอื่น**

---

## RULES

- ตัวเลขทุกตัวให้สคริปต์คำนวณ ห้ามคิดเอง ห้ามกรอกค่าสมมุติ
- `grep -oP`, `sed -i "s/.../"`, `find -newermt` เป็น GNU-only **พังบน macOS** ห้ามใช้
- ถ้าต้องแก้วิธีคำนวณ ให้แก้ `process_affiliate()` ใน `wibwub_update.py` ที่เดียว
- **ห้ามแก้อาเรย์ด้วยมือ** ให้สคริปต์เขียนเท่านั้น ไม่งั้น Affiliate Dashboard กับ Mobile จะหลุดจากกัน

## สรุปท้ายรอบ (สั้น ๆ ภาษาไทย)

เดือนล่าสุด + GMV / Net / Commission / จำนวนครีเอเตอร์, จำนวน creator ในตาราง,
`mobile_mismatch` ว่าง/ไม่ว่าง, VIDEOS ที่เพิ่ม (ถ้ารัน), commit id หรือ "ไม่มีข้อมูลใหม่", error ถ้ามี

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

# 🚩 ขั้นที่มีเฉพาะใน SKILL.md — ย้ายเข้ามา 26 ต.ค. 2569

สามขั้นข้างล่างเคยอยู่ใน SKILL.md ของงาน local ที่เดียว พรอมป์ใน repo ไม่มี
ทำให้ "ขั้นที่ 1 — โหลดไฟล์ใหม่" ข้างบนโหลดมาแค่ Creator List แค่ไฟล์เดียว
แต่ "ขั้นที่ 4 — VIDEOS" กลับต้องใช้ไฟล์แท็บ "วีดิโอ" ที่ไม่เคยโหลด
และการอัปเดต `PRODUCTS[].cr / .vid` ก็หายไปทั้งขั้น

**หมายเหตุ 2 ข้อ**
1. STEP 3 ของ SKILL.md (คำสั่งย้ายไฟล์จาก Downloads ด้วยมือ) **ไม่ได้ย้ายมา**
   เพราะ launchd `com.wibwub.download-mover` ย้ายให้เองใน 5 วินาที และกฎของรีโปคือ **ห้าม `cp`/`mv` เอง**
2. โค้ด STEP 5 ข้างล่างคือโค้ด inline ที่ยกมาตามเดิม (แก้เฉพาะพาธ `/sessions/` → พาธจริง)
   ยัง**ไม่มีสคริปต์รองรับ** ต่างจากขั้นอื่นที่มี `affiliate_update.py` / `vid_merge.py`
   ถ้าค่า `cr`/`vid` ออกมาเพี้ยน → **หยุดรายงาน ห้ามเดาค่าเอง**

---

## STEP 1 — เปิดหน้าและตั้ง Date Range

1. ⚠️ **ต้องระบุ browser ที่ Mac เสมอ ห้ามปล่อยให้เลือกอัตโนมัติ** — ถ้ามีหลาย browser connected อาจไปรันบน PC โดยไม่ตั้งใจ:
   `select_browser(deviceId="b75a6bb0-5b78-4e44-92a8-75224f1ce4ee")` → `tabs_context_mcp(createIfEmpty=true)`
   (ถ้า deviceId นี้ไม่ connected แล้ว ให้เรียก `list_connected_browsers` ก่อน แล้วเลือกตัวที่ `osPlatform` เป็น macOS / `isLocal:true` เท่านั้น — ห้ามเลือก Windows/PC)

2. Navigate ด้วย browser_batch:
   - URL: `https://affiliate.tiktok.com/insights/transaction-analysis?shop_region=TH&shop_id=7494549095358892612`
   - wait 5s → screenshot ยืนยันหน้า "การวิเคราะห์ธุรกรรม" / "Transaction Analysis" โหลดแล้ว

3. Set date range เดือนปัจจุบัน:
   - คลิก date field → เลือก "กำหนดเอง"
   - Start = วันที่ 1 ของเดือน, End = วันล่าสุดที่ available (ถ้าวันนี้ greyed out → วันก่อน)
   - บันทึก end_date จริงที่ระบบยอมรับ

---

## STEP 2 — Export และดาวน์โหลด 4 ไฟล์ทีละ Tab

ทำซ้ำ 4 รอบ — แต่ละ tab มีปุ่ม "ส่งออก" ของตัวเอง
Export เป็น async queue: trigger → รอ → download จาก reports panel

### Tab 1: ครีเอเตอร์
1. ตรวจว่าอยู่ที่ tab **ครีเอเตอร์** (default) — ถ้าไม่ใช่ให้คลิก
2. Scroll หาปุ่ม **"ส่งออก"** เหนือตาราง → คลิก
3. รอ 60-90 วินาที
4. คลิกปุ่ม **"บันทึกการดาวน์โหลดไฟล์"** (document icon) → reports panel
5. หาไฟล์ล่าสุดที่สถานะ **"ดาวน์โหลด"** → คลิก ดาวน์โหลด
   - ถ้ายัง **"กำลังส่งออก"** → รออีก 30s แล้ว refresh panel

### Tab 2: สินค้า
6. คลิก tab **"สินค้า"** → รอ 3s → screenshot
7. ปุ่ม "ส่งออก" → คลิก → รอ 60-90s → download จาก reports panel

### Tab 3: วีดีโอ
8. คลิก tab **"วีดีโอ"** → รอ 3s → screenshot
9. ปุ่ม "ส่งออก" → คลิก → รอ 60-90s → download จาก reports panel

### Tab 4: ไลฟ์สตรีม
10. คลิก tab **"ไลฟ์สตรีม"** → รอ 3s → screenshot
11. ปุ่ม "ส่งออก" → คลิก → รอ 60-90s → download จาก reports panel

> ถ้า panel มีไฟล์ same-day ที่พร้อมอยู่แล้ว → ดาวน์โหลดได้เลย ไม่ต้อง export ใหม่

---


---

## STEP 5 — Process ไฟล์ สินค้า → อัปเดต PRODUCTS cr/vid

```python
PROD_DIR = '/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/Data Affiliate/สินค้า/'
prod_files = sorted(glob.glob(PROD_DIR + '*.xlsx'), key=os.path.getmtime, reverse=True)
if not prod_files:
    print("WARNING: ไม่พบไฟล์ในโฟลเดอร์สินค้า — ข้ามขั้นตอนนี้")
else:
    df_prod = pd.read_excel(prod_files[0], header=None)
    
    # หา header row ที่มีชื่อ column
    header_idx = 0
    for i, row in df_prod.iterrows():
        row_str = ' '.join(str(v) for v in row.values if pd.notna(v))
        if 'สินค้า' in row_str or 'GMV' in row_str or 'ครีเอเตอร์' in row_str:
            header_idx = i
            break
    
    df_prod = pd.read_excel(prod_files[0], header=header_idx)
    print(f"Columns: {list(df_prod.columns)}")
    
    # หา columns สำคัญ (ชื่อ column อาจต่างกันตามเวอร์ชัน TikTok)
    # ค้นหา: product name, ครีเอเตอร์ที่มียอดขาย, วีดีโอ
    cols = {str(c).lower(): i for i, c in enumerate(df_prod.columns)}
    
    # สร้าง product cr/vid dict
    prod_data = {}
    for _, row in df_prod.iterrows():
        name = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ''
        if not name or name == 'nan': continue
        # ค้นหา cr column (ครีเอเตอร์ที่มียอดขาย)
        cr_val = 0
        vid_val = 0
        for col_name, col_idx in cols.items():
            if 'ครีเอเตอร์' in col_name and 'ขาย' in col_name:
                cr_val = int(pd.to_numeric(row.iloc[col_idx], errors='coerce') or 0)
            elif 'วีดีโอ' in col_name or 'video' in col_name:
                vid_val = int(pd.to_numeric(row.iloc[col_idx], errors='coerce') or 0)
        prod_data[name] = {'cr': cr_val, 'vid': vid_val}
    
    print(f"Products found: {list(prod_data.items())[:5]}")
```

**Mapping TikTok product name → PRODUCTS[].name (fuzzy keyword):**
| Keyword | PRODUCTS[].name |
|---|---|
| Leather | WIBWUB Refresh Leather Wipes |
| interior wipe (case-insensitive) | WIBWUB Interior wipes |
| Sugar | WIBWUB Sugar |
| CLEANER | WIBWUB CLEANER |
| Interior (ไม่มี "wipe") | WIBWUB Interior |
| Refresh (ไม่มี "Leather") | WIBWUB Refresh |
| Visible | WIBWUB Visible |

**อัปเดต `WIBWUB_Affiliate_Dashboard.html`:**
- `PRODUCTS` array: แก้เฉพาะ `cr` และ `vid` fields (ห้ามแก้ gmv, units, monthly, ret)
- KPI strip สินค้า tab: `ผ่าน X,XXX creators` = รวม cr ทุกสินค้า

---

