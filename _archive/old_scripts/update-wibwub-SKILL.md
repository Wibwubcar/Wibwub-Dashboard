---
name: update-wibwub
description: >
  Use this skill whenever the user wants to sync new data into any WIBWUB dashboard or app.
  Triggers include: "update app", "update dashboard", "มีข้อมูลใหม่", "อัพเดทข้อมูล",
  "sync ข้อมูล", sharing a Google Sheet link with any sales/TikTok/affiliate data, sharing
  new Shipnity export files, asking why app/web data doesn't match the sheet, or any request
  to refresh WIBWUB content. This skill covers ALL files — Mobile PWA, Web Dashboard,
  Affiliate Dashboard, TikTok Dashboard — and ALL data sections: TikTok clips, sales arrays,
  affiliate GMV, ads ROAS, platform breakdown, top products (from Shipnity files), and all
  hardcoded KPI text. Always use this skill when the user mentions updating any part of the
  WIBWUB app or dashboards, even if they only mention one file — sync ALL files every time.
---

# WIBWUB Full Data Sync Skill

This skill guides you through syncing **all data** from the WIBWUB Google Sheets into the
Mobile PWA app (`WIBWUB_Mobile.html`) and bumping the service worker cache so installed
users get the update automatically.

**The most common mistake is updating TikTok clips but forgetting to update sales arrays,
KPI summary text, or the home hero section.** Follow every section, even if you think
it hasn't changed — verify by comparing the sheet with the current file.

---

## Google Sheets Data Sources (อ่านโดย Google Drive MCP — `mcp__claude_ai_Google_Drive__read_file_content`)

| แหล่งข้อมูล | File ID | อัปเดตทุก |
|---|---|---|
| **Shopee** | `10LrzWB8bbCO9FigCQFz5gZ3iSXMVhK0S` | จันทร์ 10 โมง |
| **Lazada** | `1FxLAUiwabmNcBc3TA-bpHqg2MSK7uJ4U` | จันทร์ 10 โมง |
| **TikTok** | `1k22c3PGY6aQjygAX6df_rQLR8aTzL-iz` | จันทร์ 10 โมง |
| **Affiliate** | `1FLmm9_fwZoNEG7VvHaQ4fvOVhqaRLDvF` | จันทร์ 10 โมง |
| **Social Media / Clips** | `1OWZGQD1wHvIlLAAg_7rJ0CtL-X9vEx4py-cRp_e3NvQ` | จันทร์ 10 โมง |

### วิธีดึงข้อมูลจาก Sheet (Column Mapping)

**Shopee** — Section `ยอดรายเดือน` — rows เป็น `01-DD/MM/YY`:
- ยอดขาย (col 1) → `SH_REV`
- ยอดใช้ ads (col 2) → `SH_ADS`
- ค่าธรรมเนียม (col 3) → `SH_FEE`
- ลูกค้าใหม่ (col 6) → `SH_NEW`
- ลูกค้าเก่า (col 7) → `SH_OLD`
- จำนวน order (col 8) → `SH_ORD`
- ยกเลิก order / จำนวน order × 100 → `SH_CANCEL` (%)
- ยอดรวมไลฟ์ → `SH_LIVE_TOTAL` (hardcoded)
- ใช้ Row สุดท้ายของเดือน: `01-31/01/26`, `01-28/02/26`, `01-31/03/26`, `01-30/04/26`, partial = row ล่าสุด

**Lazada** — Section `ยอดรายเดือน` — rows เป็น `01-DD/MM/YY`:
- ยอดขาย (col 1) → `LZ_REV`
- ยอดใช้ ads (col 2) → `LZ_ADS`
- ค่าธรรมเนียม+คูปอง / ยอดขาย (col 5) → `LZ_COST_PCT`
- จำนวน order (col 8) → `LZ_ORD`
- ยกเลิก order / จำนวน order × 100 → `LZ_CANCEL` (%)

**TikTok** — Section `ยอดรายเดือน` — rows เป็น `01-DD/MM/YY`:
- ยอด Afi (col 1) → `TK_AFI`
- ยอดหลังหัก (col 3) → `TK_NET`
- ยอดขาย (col 5) → `TK_REV`
- ยอดจาก Ads (col 6) → `TK_ADS`
- ยอดใช้จ่าย Ads+GMV (col 8) → `TK_ADSSPEND`
- ค่าธรรมเนียม+ค่าคอม Afi (col 9) → `TK_FEECOMM`
- ยอด Live รวม (col 11) → `TK_LIVE`
- ลูกค้าใหม่ (col 14) → `TK_NEW`
- ลูกค้าเก่า (col 15) → `TK_OLD`
- จำนวน order (col 16) → `TK_ORD`
- TK_AFIPCT = TK_AFI / TK_REV × 100
- TK_CANCEL = ยกเลิก order / จำนวน order × 100
- **สำคัญ**: ใช้ row เดียวกันทั้งหมด — อย่าผสม snapshot ต่างวัน

**Affiliate** — Sheet `1FLmm9_fwZoNEG7VvHaQ4fvOVhqaRLDvF` gid=332180206 — ข้อมูล creator ระดับรายคน
- อ่านผ่าน Chrome fetch (ไม่ใช้ read_file_content เพราะ sheet ใหญ่เกินไป):
  ```javascript
  const csv = await fetch('https://docs.google.com/spreadsheets/d/1FLmm9_fwZoNEG7VvHaQ4fvOVhqaRLDvF/export?format=csv&gid=332180206').then(r=>r.text());
  ```
- โครงสร้าง CSV: col[0]=Creator name, col[1]=GMV (฿xxx,xxx.xx), col[2]=คืนเงิน, col[3]=NET GMV, col[4]=commission
- col[1] คือ GMV เดือนปัจจุบัน — sum ทุก row ควรตรงกับ AFI_GMV ของเดือนนั้น (ตรวจสอบก่อน)
- gmvD / AFI_GMV → ยอด GMV รวมทุก creator ต่อเดือน (array 7 ค่า index 0=พ.ย.68 → 6=พ.ค.69)
- netD / AFI_NET → NET GMV (หลังหักคืน)
- commD / AFI_COMM → ค่าคอมมิชชั่น
- crD → จำนวน creator ที่ active ต่อเดือน

**CREATORS array index mapping:** mn[0]=พ.ย.68, mn[1]=ธ.ค.68, mn[2]=ม.ค.69, mn[3]=ก.พ.69, mn[4]=มี.ค.69, mn[5]=เม.ย.69, mn[6]=พ.ค.69

**Social Media / TikTok Clips** — อ่านจาก tab **CONTENT** ใน sheet `1OWZGQD1wHvIlLAAg_7rJ0CtL-X9vEx4py-cRp_e3NvQ`:
- กรอง Status = 'Post' เท่านั้น (ข้ามแถวที่ยังไม่โพสต์)
- col[0]=DATE, col[2]=Content Pillars, col[3]=Content, col[8]=Link คลิปลงช่อง (URL)
- col[10]=5 Sec Retention%, col[11]=Avg Watch%, col[15]=Views
- col[16]=Likes, col[17]=Comments, col[18]=Shares, col[19]=Saves
- eng = col[16]+col[17]+col[18]+col[19] (คำนวณเอง)
- er = round((eng/views)×100, 2 decimal)
- ใช้สร้าง ALL_POSTS array ใน Mobile dashboard — **automated ได้ทั้งหมด ไม่ต้อง manual**
- หมายเหตุ: `data content/Tiktok stat_WIBWUB.xlsx` คือ backup local เท่านั้น ไม่ใช่ source หลัก

**TK Followers** — อ่านจากโฟลเดอร์ `data content/` (ไม่ใช่ Google Sheets):
- โครงสร้าง: `data content/Followers_wibwubcar (1)/Followers_wibwubcar (N)/FollowerHistory.xlsx`
- แต่ละ zip = 1 เดือน เรียงตามลำดับ (1)=ม.ค., (2)=ก.พ., (3)=มี.ค., (4)=เม.ย., (5)=พ.ค.…
- ใช้ **row สุดท้าย** ของ zip ล่าสุด = followers ปัจจุบัน
- ตรวจสอบด้วย: `ls "data content/Followers_wibwubcar (1)/"` → หา zip ล่าสุด
- TK Followers hardcoded ใน Mobile: `26.2K` = ค่าสุดท้าย ÷ 1000 (1 decimal)
- `+XK จาก ม.ค.` = followers ล่าสุด − followers สิ้น ม.ค. ÷ 1000 (round)

---

## File Paths

| File | Local Path (for Read/Edit) |
|---|---|
| Mobile PWA | `…/All/WIBWUB_Mobile.html` |
| Web Dashboard | `…/All/WIBWUB_Dashboard.html` |
| Affiliate Dashboard | `…/All/WIBWUB_Affiliate_Dashboard.html` |
| TikTok Dashboard | `…/All/WIBWUB_TikTok_Dashboard_v7.html` |
| Service Worker | `…/All/sw.js` |

Full prefix: `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/`

**GitHub Pages URLs:**
- Mobile App: https://thanasab.github.io/Wibwub-Dashboard/WIBWUB_Mobile.html
- Web Dashboard: https://thanasab.github.io/Wibwub-Dashboard/WIBWUB_Dashboard.html
- Affiliate Dashboard: https://thanasab.github.io/Wibwub-Dashboard/WIBWUB_Affiliate_Dashboard.html
- Root (redirects to Mobile): https://thanasab.github.io/Wibwub-Dashboard/

**GitHub repo:** `thanasab/Wibwub-Dashboard` (branch: main)

---

## Step 0 — Read the Current File First

Before making any edits, read WIBWUB_Mobile.html (full file). Locate the `<script>` block
(around line 391) and note the current values of every data array so you know exactly
what has changed vs. the sheet.

---

## Step 1 — Parse Google Sheet Data

The Google Sheet "Tiktok stat_WUBWUB" is connected via Google Drive MCP. Read whichever
sheets are relevant. Key tabs:

| Sheet / Tab | Data |
|---|---|
| TikTok stat | Clips: date, pillar, content, views, likes, comments, shares, saves, 5s retention%, avg watch time% |
| Sales / ยอดขาย | Monthly revenue by platform (Shopee, TikTok, Lazada), orders, cancel%, ads spend, ROAS |
| Affiliate | Monthly GMV per creator, total GMV/NET/commission |
| Products | Top products by revenue and quantity |

---

## Step 2 — TikTok Clips (ALL_POSTS array)

### 2a. Identify new clips
Compare sheet clip list vs current ALL_POSTS. A clip is new if its TikTok URL or
date+content combo doesn't exist yet.

### 2b. Build each entry
```javascript
{lbl:'DAY',m:MONTH_NUM,pillar:'PILLAR',c:'CONTENT',views:VIEWS,eng:ENG,ret:RET,watch:WATCH,er:ER,url:'TIKTOK_URL'},
```
- `lbl` = day as string; two clips same day → `'8(1)'` and `'8(2)'`
- `m` = month integer: 3=มีนาคม, 4=เมษายน, 5=พฤษภาคม, 6=มิถุนายน …
- `eng` = likes + comments + shares + saves (CALCULATE THIS — do not copy from sheet)
- `er` = round((eng / views) × 100, 2 decimal places)
- `ret` = 5s retention as integer (e.g. 19, not 0.19)
- `watch` = avg watch time % as float, 1 decimal (e.g. 12.6)

**Pillar mapping:**
```
KNOWLEDGE/Knowledge → 'Knowledge'    REVIEW/Review → 'Review'
TESTIMONIAL         → 'Review'       SALES/Sale    → 'Sale'
LIFESTYLE/Lifestyle → 'Lifestyle'    BRAND EXPERT  → 'Brand Expert'
INTERVIEW/Interview → 'Interview'    AWARENESS     → 'Awareness'
(anything else)     → 'Other'
```

### 2c. Insert clips in chronological order within their month.

### 2d. Update TikTok month tab labels
In `<div class="mtabs" id="tt-mo-tabs">`, update clip count in parentheses:
```html
<div class="mtab" onclick="setTT(5,this)">พ.ค. (11)</div>
```

### 2e. Update TikTok Content Summary KPI cards
In Marketing → Overview, find the kgrid with clip count cards and update count + views:
```html
<div class="kc-val" style="font-size:15px">11</div>
<div class="kc-sub">26.2K views</div>
```
Views = sum of all views for that month, formatted as `K` with 1 decimal (e.g. `26.2K`).

---

## Step 3 — Sales Data Arrays

Arrays are 0-indexed: index 0 = ม.ค., 1 = ก.พ., 2 = มี.ค., 3 = เม.ย., 4 = พ.ค., …

| Array | Description |
|---|---|
| `SH_REV` | Shopee revenue per month |
| `TK_REV` | TikTok Shop revenue per month |
| `LZ_REV` | Lazada revenue per month |
| `SH_ORD` | Shopee orders per month |
| `TK_ORD` | TikTok orders per month |
| `LZ_ORD` | Lazada orders per month |
| `SH_CANCEL` | Shopee cancel % |
| `TK_CANCEL` | TikTok cancel % |
| `LZ_CANCEL` | Lazada cancel % |
| `SH_ADS` | Shopee ads spend |
| `SH_FEE` | Shopee platform fee |
| `TK_ADSSPEND` | TikTok ads spend |
| `TK_FEECOMM` | TikTok fee+commission |
| `TK_AFI` | TikTok affiliate GMV per month |
| `TK_NET` | TikTok NET revenue |
| `LZ_COST_PCT` | Lazada total cost % |
| `LZ_ADS` | Lazada ads spend |
| `TOTAL_REV` | Total revenue all platforms |
| `TOTAL_ORD` | Total orders all platforms |

Compare every value with the sheet and update anything that changed.
To add a new month: append to EVERY array + add to `const M5=[...]` + add month tab buttons.

---

## Step 4 — CHANNELS Array

```javascript
const CHANNELS=[
  {n:'Shopee',v:CUMULATIVE_SH_TOTAL,color:'#ee4d2d'},
  ...
];
```
Update each `v` with the cumulative total from ม.ค. through the latest month.
Keep sorted by `v` descending.

---

## Step 5 — Affiliate Data

```javascript
const AFI_MONTHS=[...];   // month labels
const AFI_GMV=[...];      // GMV per month
const AFI_NET=[...];      // NET per month
const AFI_COMM=[...];     // commission per month
```
Append new month data if available.

Also update `CREATORS` array — each creator:
```javascript
{n:"username", t:TOTAL_GMV, ma:MONTHS_ACTIVE, mn:[mo1,mo2,...,null,...]},
```
- `mn` length must equal number of months (currently 7)
- `mn[6]` = current month (พ.ค.) GMV — อ่านจาก Affiliate Sheet col[1]
- `t` = sum(mn[]) recalculate ทุกครั้ง
- `ma` = จำนวนเดือนที่ mn[i] != null
- Keep sorted by `t` descending, keep top 40

**วิธี update CREATORS ทีละ step (JavaScript ใน Chrome):**
```javascript
// 1. Parse affiliate sheet
const csv = await fetch('https://docs.google.com/spreadsheets/d/1FLmm9_fwZoNEG7VvHaQ4fvOVhqaRLDvF/export?format=csv&gid=332180206').then(r=>r.text());
function parseCSVRow(row) {
  const result=[]; let cur='', inQ=false;
  for(let i=0;i<row.length;i++){const ch=row[i];if(ch==='"'){inQ=!inQ;}else if(ch===','&&!inQ){result.push(cur.trim());cur='';}else{cur+=ch;}}
  result.push(cur.trim()); return result;
}
const lines = csv.split('\n').filter(l=>l.trim());
const mayMap = {};
lines.slice(1).forEach(l=>{
  const r=parseCSVRow(l);
  const name=r[0]?.trim();
  const gmv=parseFloat(r[1]?.replace(/[฿,]/g,''));
  if(name && !isNaN(gmv) && gmv>0) mayMap[name]=Math.round(gmv);
});
// Verify: Object.values(mayMap).reduce((s,v)=>s+v,0) should equal AFI_GMV[currentMonthIdx]

// 2. Update existing CREATORS (already parsed into window._parsedCreators)
window._parsedCreators.forEach(cr=>{
  cr.mn[6]=mayMap[cr.n]||null;
  cr.t=cr.mn.reduce((s,v)=>s+(v||0),0);
  cr.ma=cr.mn.filter(v=>v!=null).length;
});

// 3. Add top new creators not already in list
const existingNames=new Set(window._parsedCreators.map(c=>c.n));
const top40May=Object.entries(mayMap).sort((a,b)=>b[1]-a[1]).slice(0,40).map(e=>e[0]);
const newOnes=top40May.filter(n=>!existingNames.has(n)).slice(0,10).map(n=>({
  n, t:mayMap[n], ma:1, mn:[null,null,null,null,null,null,mayMap[n]]
}));
const combined=[...window._parsedCreators,...newOnes].sort((a,b)=>b.t-a.t).slice(0,40);
```

---

## Step 6 — Products (ALL_PRODUCTS) — from Data Shipnity files

Top product rankings come from the **Data Shipnity** folder (NOT from Google Sheet):
```
Workspace: All/Data Shipnity/
Files:  Data_มกราคม.xlsx     → January
        Data_15-05-2026.xlsx → February (ชื่อหลอก — จริงๆ เป็นข้อมูลก.พ. อย่าเปลี่ยนเป็น 5!)
        Data-มีนา.xlsx        → March
        Data_เมษา.xlsx        → April
        Data_25-05-2026.xlsx → May (cumulative ม.ค.–25 พ.ค. supersedes Data_พฤษภา + Data_18-05)
        Data_[DATE].xlsx     → ไฟล์ใหม่สุด — ตรวจ date range ใน column วันที่สร้าง (index 19) ก่อน
```

⚠️ **Shipnity export เป็น CUMULATIVE** — ไฟล์ใหม่สุดของช่วงเดียวกัน = แทนที่ไฟล์เก่าทั้งหมด
ห้ามรวม Data_พฤษภา + Data_18-05-2026 + Data_25-05-2026 พร้อมกัน (จะนับซ้ำ!)
ใช้ `ls -lt "Data Shipnity/"` เช็คไฟล์ล่าสุดก่อนเสมอ

Always aggregate ONLY non-overlapping files and deduplicate using `(order_id, sku, qty)` as dedup key:
```python
# col[0]=รหัสสินค้า  col[1]=สินค้า  col[2]=ราคา  col[3]=จำนวน  col[4]=เลขที่ออเดอร์
seen = set()
prod = defaultdict(lambda: {'revenue': 0, 'qty': 0})
for row in all_rows_from_all_files:
    key = (row[4], row[0], row[3])   # order_id + sku + qty
    if key in seen: continue
    seen.add(key)
    prod[str(row[1])]['revenue'] += (row[2] or 0) * (row[3] or 0)
    prod[str(row[1])]['qty'] += int(row[3] or 0)
# Sort by revenue desc, take top 15, use clean display names
```

Update `ALL_PRODUCTS` sorted by `v` descending:
```javascript
const ALL_PRODUCTS=[
  {n:"Product Name", v:TOTAL_REVENUE, q:TOTAL_QUANTITY},
  ...
];
```

---

## Step 6b — Social Media & KPI Stats (Home mks-grid — easily forgotten!)

The 4 KPI boxes in `.mks-grid` are **hardcoded text** — update on every sync:

| Box | Formula |
|---|---|
| Affiliate GMV | `sum(AFI_GMV)` → format `฿X.XXM`; update creator count & months |
| Ads ROAS | `(ΣSH_REV + ΣTK_REV) / (ΣSH_ADS + ΣTK_ADSSPEND)` → format `X.XX×` |
| TikTok Clips | count `ALL_POSTS.length` after clip additions; update month range if new month added |
| TK Followers | อ่านจาก `data content/Followers_wibwubcar (1)/Followers_wibwubcar (N)/FollowerHistory.xlsx` row สุดท้าย |

Example (update these values):
```html
<div class="mks-val">฿3.41M</div><div class="mks-sub">40 creators · 7 เดือน</div>
<div class="mks-val">5.88×</div><div class="mks-sub">Shopee+TikTok</div>
<div class="mks-val">48 คลิป</div><div class="mks-sub">มี.ค.–พ.ค. 2569</div>
<div class="mks-val">128K</div><div class="mks-sub">+12K จาก ม.ค.</div>
```

---

## Step 7 — Hardcoded KPI Text (CRITICAL — easily forgotten)

These values are NOT generated from JS arrays. Find and update each one:

### Home hero section
```html
<div class="hh-lbl">ยอดขายรวม ม.ค.–พ.ค. 2569</div>
<div class="hh-val">฿35.2M</div>
<div class="hh-sub">62,197 unique orders · AOV ฿566</div>
```
Also the 3 platform boxes inside `hh-grid`.

### Home KPI boxes (mks-grid)
```
Affiliate GMV total · creator count + months
Ads ROAS combined
TikTok clip total count + month range
TK Followers
```

### Sales Overview KPI strip (initSalesOv function)
```html
฿35.2M total · 62,197 orders · ฿566 AOV · 131K line items
```

### Marketing Overview KPI strip (m-sv-0)
```html
Affiliate GMV รวม · Affiliate NET รวม · Shopee ROAS เฉลี่ย · TikTok ROAS เฉลี่ย
```

### Combined Ads section (a-cb panel)
```html
฿26.27M Revenue SH+TK · 5.88× ROAS Combined
```

### Header date range
```html
<div>ม.ค. – พ.ค. 2569</div>
```
Update if a new month was added.

### Data coverage footnotes
Search for strings like `"* พ.ค. 2569 ข้อมูล 1–13 พ.ค."` and update date ranges.

---

## Step 8 — Bump Service Worker Cache

In `sw.js`, increment the cache version number:
```javascript
const CACHE = 'wibwub-v5';  // was v4, now v5
```
Always increment by 1. This triggers automatic refresh for all PWA users.

---

## Step 9 — Verification Checklist

Before saving, verify:
- [ ] ALL_POSTS: new clips added, chronological order, eng/er calculated correctly
- [ ] TikTok tab labels: clip count in parentheses updated
- [ ] TikTok Content Summary KPI: count + views updated
- [ ] All 19 sales arrays: values match sheet
- [ ] CHANNELS: cumulative totals updated, sorted by v desc
- [ ] Affiliate arrays + CREATORS updated
- [ ] ALL_PRODUCTS updated (Shipnity files aggregated + deduplicated, sorted by revenue)
- [ ] Home KPI boxes: Clips count, Affiliate GMV, Ads ROAS, TK Followers updated
- [ ] Home hero text updated (revenue, orders, AOV, platform totals)
- [ ] Home KPI boxes updated (clips count, affiliate GMV, ROAS)
- [ ] Sales overview KPI strip updated
- [ ] Marketing overview KPI strip updated
- [ ] sw.js cache version bumped
- [ ] No JS syntax errors (no trailing commas on last array element in older browsers)

---

## Step 10 — Push to GitHub (via Claude in Chrome — NO lock files)

**⚠️ NEVER use `git add/commit/push` from bash sandbox** — Google Drive FUSE mount สร้าง lock files ที่ลบไม่ได้จาก Linux sandbox และ bash sandbox ไม่มี network access ไป api.github.com

**⚠️ NEVER ใช้ `btoa(unescape(encodeURIComponent(content)))` — จะทำให้ Thai text พัง!**

**ใช้ GitHub API ผ่าน Claude in Chrome แทนทุกครั้ง:**

### 1. Init helpers ใน Chrome tab (ครั้งเดียวต่อ session):
```javascript
const TOKEN = "YOUR_GITHUB_TOKEN_HERE";
const REPO  = "thanasab/Wibwub-Dashboard";

window.ghApi = async (method, path, data) => {
  const r = await fetch(`https://api.github.com${path}`, {
    method, headers:{'Authorization':`token ${TOKEN}`,'Content-Type':'application/json','User-Agent':'WIBWUB'},
    body: data ? JSON.stringify(data) : undefined
  });
  if (!r.ok) throw new Error(`${r.status} ${await r.text()}`);
  return r.json();
};

// ✅ CORRECT: base64 → bytes → TextDecoder (preserves Thai)
window.ghGetFileAtCommit = async (path, ref) => {
  const d = await window.ghApi('GET', `/repos/${REPO}/contents/${encodeURIComponent(path)}?ref=${ref}`);
  const binary = atob(d.content.replace(/\n/g,''));
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return { sha: d.sha, content: new TextDecoder('utf-8').decode(bytes) };
};

// ✅ CORRECT: TextEncoder → bytes → base64 (preserves Thai)
window.ghPushText = async (path, text, sha, msg) => {
  const bytes = new TextEncoder().encode(text);
  let bin = '';
  bytes.forEach(b => bin += String.fromCharCode(b));
  return window.ghApi('PUT', `/repos/${REPO}/contents/${encodeURIComponent(path)}`, {
    message: msg, content: btoa(bin), sha, branch: 'main'
  });
};

window.ghGetSha = async (path) => {
  const d = await window.ghApi('GET', `/repos/${REPO}/contents/${encodeURIComponent(path)}?ref=main`);
  return d.sha;
};
```

### 2. Push แต่ละไฟล์ (pattern มาตรฐาน):
```javascript
// ใช้ promise chain เพราะ await ใช้ได้แค่ใน async function
window.ghGetFileAtCommit('FILENAME.html', 'main')
  .then(r => {
    let c = r.content;
    c = c.replace('OLD_VALUE', 'NEW_VALUE');
    return window.ghPushText('FILENAME.html', c, r.sha, 'commit message');
  })
  .then(r => { window._pushResult = r.commit?.sha?.slice(0,7); })
  .catch(e => { window._pushErr = e.message; });
// ดู result: window._pushResult หรือ window._pushErr
```

### 3. ลำดับการ push ไฟล์ทุก session:
1. `WIBWUB_Mobile.html`
2. `WIBWUB_Dashboard.html`
3. `WIBWUB_Affiliate_Dashboard.html`
4. `sw.js` — bump cache version ทุกครั้งที่ push ไฟล์อื่น

### 4. Bump sw.js:
```javascript
window.ghGetFileAtCommit('sw.js', 'main')
  .then(r => {
    const newSw = r.content.replace("'wibwub-vXX'", "'wibwub-vXY'"); // XX→XY +1
    return window.ghPushText('sw.js', newSw, r.sha, 'bump: sw.js cache vXY');
  })
  .then(r => { window._swResult = r.commit?.sha?.slice(0,7); });
// Current version after 24 May 2026 session: v17
```

---

## Common Mistakes

- **Using git from bash sandbox**: NEVER. Bash sandbox runs on Linux with Google Drive FUSE mount — git creates `.git/index.lock` or `.git/HEAD.lock` that can't be deleted → use GitHub API via Chrome browser (Step 10).
- **Wrong base64 encoding for Thai text**: NEVER use `btoa(unescape(encodeURIComponent(content)))` — this corrupts Thai characters. ALWAYS use `TextEncoder` to encode and `TextDecoder` to decode (see Step 10 helpers above). This was the root cause of a full-app garble bug on 24 May 2026.
- **Forgetting eng calculation**: `eng` = likes + comments + shares + saves. Always calculate.
- **Ignoring hardcoded text**: Home hero `฿35.2M` and KPI boxes are NOT from JS arrays.
- **Not bumping sw.js**: Without this, installed PWA users keep seeing stale data. Current version: v18 (after 25 May 2026). Always increment by 1.
- **Stale month range**: When adding a new month, update `ม.ค. – พ.ค. 2569` everywhere.
- **Wrong array index**: Month arrays are 0-based. New month always appends at the END.
- **Only updating clips**: Sales, affiliate, ROAS, products also need to be checked every sync.
- **Reading entire Affiliate Sheet via read_file_content**: Sheet is 500K+ chars and result goes to /var/folders (inaccessible from bash). Always use Claude in Chrome fetch CSV: `fetch('https://docs.google.com/spreadsheets/d/1FLmm9_fwZoNEG7VvHaQ4fvOVhqaRLDvF/export?format=csv&gid=332180206')`.
- **CREATORS sum not matching AFI_GMV**: After updating mn[6], verify sum of all creator mn[currentIdx] ≈ AFI_GMV[currentIdx]. Exact match expected since sheet exports all 403 active creators.
- **Forgetting WIBWUB_Dashboard.html and WIBWUB_Affiliate_Dashboard.html**: These files also contain `SH_ADS`, `TK_AFI`, `gmvD`, `netD`, `commD`, `crD` arrays — update ALL three HTML files, not just Mobile.
- **Restoring corrupted file**: If a file has garbled Thai after a push, fetch from the last good commit (before the corrupt push) using `ghGetFileAtCommit('file.html', 'COMMIT_SHA')`, re-apply data changes (numbers only), and re-push. Find last good commit via: `ghApi('GET', '/repos/thanasab/Wibwub-Dashboard/commits?path=FILENAME&per_page=10')`.

---

## Auto-Push Setup (ติดตั้งแล้ว 2026-06-01)

**macOS LaunchAgent** `com.wibwub.autopush` ทำงานทุก **3 นาที** โดยอัตโนมัติ
- Script: `~/.wibwub_autopush.sh`
- Plist: `~/Library/LaunchAgents/com.wibwub.autopush.plist`
- Log: `~/Library/Logs/wibwub_autopush.log`

ไฟล์ที่ auto-push จะ stage: `WIBWUB_Mobile.html`, `WIBWUB_Dashboard.html`, `WIBWUB_Affiliate_Dashboard.html`, `WIBWUB_TikTok_Dashboard_v7.html`, `data Ads/WIBWUB_Ads_Dashboard.html`, `Data Shipnity/Sales_Dashboard.html`, `sw.js`

**ไม่ต้องสั่ง git push อีกต่อไป** — แค่แก้ไฟล์แล้วรอ ≤3 นาที

ถ้า agent ดับ ให้ reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.wibwub.autopush.plist
launchctl load   ~/Library/LaunchAgents/com.wibwub.autopush.plist
```
