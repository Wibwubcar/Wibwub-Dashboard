---
name: wibwub-fastmoss-competitor
description: ทุกวัน 08:05 — ดึงข้อมูล FastMoss ของ WIBWUB + munwow (cumulative + 28-day trend + top products) → อัปเดต WIBWUB_FastMoss_Competitor_Dashboard.html → commit + push_now.command
---

<!-- LOCAL-OVERRIDE v1 -->
> **อ่านก่อน — ข้อนี้ทับคำสั่งที่ขัดกันในไฟล์นี้ทั้งหมด**
> ไฟล์นี้เขียนไว้ตอนรันบน Cowork cloud sandbox ตอนนี้ย้ายมารันบนเครื่อง Mac แล้ว
> - BASE / ALL_MNT = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All` · Downloads = `/Users/thanasablilutanon/Downloads` · OUTPUTS = `/Users/thanasablilutanon/Library/Caches/wibwub-outputs`
> - `git push` **ไม่ต้องทำ** และจะ**ไม่**เจอ error 403 แบบ sandbox — launchd `com.wibwub.autopush` push ให้เองทุก 2 นาที ข้ามทุกหัวข้อที่พูดถึง 403 / การสร้างหรือแก้ `push_now.command`
> - ที่ไหนเขียนว่า `mcp__workspace__bash` ให้ใช้ Bash tool ปกติแทน
> - อ่านไฟล์ในเครื่องใช้ Read/Bash ได้ตรง ๆ ไม่ต้องผ่าน connector
> - ถ้าขั้นไหนอ้าง path หรือเครื่องมือที่ไม่มีจริง: **หยุดและรายงาน ห้ามเดาทางเอง**

## WIBWUB FastMoss Competitor Dashboard — Daily Update

Goal: scrape today's FastMoss shop-analytics numbers for WIBWUB and its competitor "munwow", then merge them into the WIBWUB_FastMoss_Competitor_Dashboard.html comparison dashboard so it always shows a fresh snapshot plus a growing history trend line. This is a fully self-contained task — you have no memory of any prior conversation, so follow every step below.

### Step 0 — Resolve paths

The Google Drive workspace folder is mounted into your bash sandbox under a session-specific path. Resolve it dynamically (do NOT hardcode a `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All` path from any old documentation — the `<name>` changes every session):

```bash
BASE="/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
echo "BASE=$BASE"
ls "$BASE/fastmoss_history.json" "$BASE/fastmoss_update.py" "$BASE/WIBWUB_FastMoss_Competitor_Dashboard.html"
```

If any of those three files are missing, stop and report — something is wrong with the setup, don't try to recreate them from scratch.

### Step 1 — Open FastMoss via Claude in Chrome

⚠️ Chrome navigation rule: never call `navigate` standalone — it can hang and stall the whole task. Always wrap it in `browser_batch`:
```
browser_batch([
  navigate(url="...", tabId=TAB_ID),
  computer(action="wait", duration=4, tabId=TAB_ID),
  computer(action="screenshot", tabId=TAB_ID)
])
```

1. Always pin the browser explicitly — if multiple browsers are connected, picking the wrong one silently runs on the wrong machine: call `list_connected_browsers` first, then `select_browser` with the device whose `osPlatform` is macOS and `isLocal:true`. Then `tabs_context_mcp(createIfEmpty=true)`.
2. Navigate to WIBWUB's page: `https://www.fastmoss.com/th/shop-marketing/detail/7494549095358892612`
3. If the page asks you to log in, STOP and report "ต้องการ login FastMoss" — do not attempt to log in yourself.

### Step 2 — Read WIBWUB's numbers (⚠️ read this carefully — easy to get wrong)

FastMoss shop pages show TWO different classes of numbers that look similar but are NOT interchangeable:

- **(a) Header/profile stat cards near the top** = ALL-TIME CUMULATIVE totals (orders ever, sales ever, total lives/videos/creators ever tagged, country rank, category rank, rating, quality score, response rate, shipping rate, products active/total). Use `get_page_text` for these; they're usually present without scrolling.
- **(b) "แนวโน้มข้อมูล" (Data Trends) section**, further down the page, with its own 7/28/90/180-day tab selector and an explicit date-range label like "2026-07-30 → 2026-08-26". Make sure the "28 วัน" / 28-day tab is selected (it usually is by default), then scroll it into view and take a screenshot — `get_page_text` sometimes misses these numbers until they're actually scrolled into the viewport, so confirm the on-screen pixels via screenshot before trusting the number. Read: orders, sales, creators, lives, videos, products sold, and the exact date range shown.
- Do NOT substitute (a) for (b) or vice versa. A past run of this workflow mistakenly reported WIBWUB's cumulative header stats as if they were the 28-day trend — always double check you're reading the Data Trends section for the trend28d numbers, not the header.

Also find the Top 5 best-selling products for the current 28-day window (name, orders, sales for each) — usually in a "สินค้าขายดี" / top products section on the same page.

Record: category %, price range, and "listed since" date too if visible (used for the shop meta card, rarely changes).

### Step 3 — Repeat Step 1-2 for munwow

URL: `https://www.fastmoss.com/th/shop-marketing/detail/7494636213512539066`

### Step 4 — Write the snapshot JSON and run the updater

Write a JSON file (e.g. `/tmp/fastmoss_snapshot.json`) shaped exactly like this (use today's actual date and the real numbers you just read):

```json
{
  "date": "YYYY-MM-DD",
  "shops": {
    "wibwub": {
      "cumulative": {"orders_total":.., "sales_total":.., "products_active":.., "products_total":.., "country_rank":.., "category_rank":.., "rating":.., "overall_good_pct":.., "quality_score":.., "response_rate_24h":.., "shipping_rate_48h":..},
      "trend28d": {"range":"YYYY-MM-DD → YYYY-MM-DD", "orders":.., "sales":.., "creators":.., "lives":.., "videos":.., "products_sold":..},
      "top_products": [{"name":.., "orders":.., "sales":..}, ...up to 5]
    },
    "munwow": { ... same shape ... }
  }
}
```

Then run:
```bash
cd "$BASE"
python3 fastmoss_update.py --snapshot /tmp/fastmoss_snapshot.json
```
This script merges the snapshot into `fastmoss_history.json` (overwriting today's entry if you re-run it — safe to retry), regenerates the dashboard's embedded data, and commits both files plus the dashboard HTML with author "WIBWUB Bot <marketingwibwub@gmail.com>". It will also attempt `git push`, which is expected to fail from the sandbox (HTTP 403 proxy) — that's normal, not an error.

If the script errors with "Unknown shop key", it means the FastMoss competitor set has changed — do not invent a fix, just report the error.

### Step 5 — Validate before trusting it

```bash
cd "$BASE"
python3 -c "
import re
html = open('WIBWUB_FastMoss_Competitor_Dashboard.html', encoding='utf-8').read()
m = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
open('/tmp/fm_check.js','w',encoding='utf-8').write(m.group(1))
"
node --check /tmp/fm_check.js && echo "JS_OK"
```
If this fails, the merge broke something — do not leave the commit in place silently; report the failure clearly.

### Step 6 — Report

Summarize in Thai: today's date, WIBWUB vs munwow's 28-day orders/sales, and remind that `push_now.command` still needs to be double-clicked on the user's Mac for the change to actually reach GitHub Pages (sandbox git push always fails — expected).

### Notes
- If FastMoss's page layout has visibly changed (missing "แนวโน้มข้อมูล" section, different card labels, etc.), stop and report rather than guessing at numbers.
- Never hand-edit WIBWUB_FastMoss_Competitor_Dashboard.html's data directly — always go through fastmoss_update.py so fastmoss_history.json (the source of truth) and the dashboard never drift apart.