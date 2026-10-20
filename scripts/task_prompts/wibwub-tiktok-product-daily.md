---
name: wibwub-tiktok-product-daily
description: ทุกวัน 08:45/19:45 — ดึงยอดขายระดับสินค้า TikTok Shop จาก Seller Center Compass (วันล่าสุด) → merge เข้า WIBWUB_Dashboard.html (TK_PROD_DATA) → ดึงยอดระดับ SKU/ตัวเลือกสินค้าด้วย (multi-day chunk) → merge เข้า TK_PROD_SKU → bump sw.js → commit + push_now.command
---

<!-- LOCAL-OVERRIDE v1 -->
> **อ่านก่อน — ข้อนี้ทับคำสั่งที่ขัดกันในไฟล์นี้ทั้งหมด**
> ไฟล์นี้เขียนไว้ตอนรันบน Cowork cloud sandbox ตอนนี้ย้ายมารันบนเครื่อง Mac แล้ว
> - BASE / ALL_MNT = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All` · Downloads = `/Users/thanasablilutanon/Downloads` · OUTPUTS = `/Users/thanasablilutanon/Library/Caches/wibwub-outputs`
> - `git push` **ไม่ต้องทำ** และจะ**ไม่**เจอ error 403 แบบ sandbox — launchd `com.wibwub.autopush` push ให้เองทุก 2 นาที ข้ามทุกหัวข้อที่พูดถึง 403 / การสร้างหรือแก้ `push_now.command`
> - ที่ไหนเขียนว่า `mcp__workspace__bash` ให้ใช้ Bash tool ปกติแทน
> - อ่านไฟล์ในเครื่องใช้ Read/Bash ได้ตรง ๆ ไม่ต้องผ่าน connector
> - ถ้าขั้นไหนอ้าง path หรือเครื่องมือที่ไม่มีจริง: **หยุดและรายงาน ห้ามเดาทางเอง**

Goal: keep BOTH the parent-product section ("🛒 สินค้าที่ขายได้ — TikTok Shop", the `TK_PROD_DATA` const) AND the SKU/variant-level breakdown (`TK_PROD_SKU` const, used by the "ตัวเลือกสินค้า" drill-down) in WIBWUB_Dashboard.html up to date, using TikTok Seller Center Compass as the source. Historically `TK_PROD_SKU` was left as an empty stub while `TK_PROD_DATA` kept getting updated daily, which caused the two to drift apart — the SKU breakdown totals stopped matching the parent product's real totals and confused the user ("ตัวเลือกสินค้าข้อมูลไม่ตรงกับความจริงของยอดรวม"). As of 2026-09-07 both are wired into this same daily task so they never drift again. `TK_PROD_DATA` shows GMV/orders/items_sold per product broken down by channel (self_live, self_video, affiliate, affiliate_live, affiliate_video, product_card). `TK_PROD_SKU` shows GMV/orders/items_sold per SKU/variant (e.g. "500 ml" vs "3 L") within each product.

File locations (host path — use Read/Write/Edit tools; for bash use the VM-mounted equivalent under /Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/):
- Dashboard: `.../claude/All/WIBWUB_Dashboard.html`
- Parent-level merge script: `.../claude/All/tiktok_product_merge.py` (already written and tested — do not rewrite it unless it's missing or broken)
- SKU-level merge script: `.../claude/All/tiktok_sku_merge.py` (already written and tested — do not rewrite it unless it's missing or broken)
- Service worker: `.../claude/All/sw.js`
- Push helper: `.../claude/All/push_now.command`

Step 1 — Determine the target date. Use "yesterday" relative to today (local time), as an ISO date string `YYYY-MM-DD`. Check the existing `TK_PROD_DATA.dates` array in WIBWUB_Dashboard.html (regex `const TK_PROD_DATA = ({.*?});` near the bottom `<script>` block) — if yesterday's date is already present, you can still re-fetch and overwrite it (the merge script is safe/idempotent per-date), but if the last several days are already missing/stale, fetch each missing date in turn rather than just yesterday.

Step 2 — Get the data via Claude-in-Chrome. There is no official public API for this — the working method (already proven in a prior session) is:
1. Navigate to TikTok Seller Center Compass (the seller's product-analytics page, e.g. https://seller-th.tiktok.com/compass/product-detail or similar — navigate to Compass > Product from the seller center nav if the direct URL doesn't load) and make sure you're logged in (the user's existing session/cookies should carry over; if a login wall appears, stop and tell the user to log in manually first).
2. Open the product-list view for a single day (yesterday's date) so the page fires its own request to `/api/v3/insights/seller/ttp/product/list`. Use `mcp__Claude_in_Chrome__read_network_requests` to capture that exact request (headers, query params, and POST body shape) — TikTok's own page already handles all anti-bot signing for this endpoint (unlike the SKU/variant-level v2 endpoint, which requires a signature we don't have), so replaying its own request structure works.
3. Once you have the real request shape from the network capture, use `mcp__Claude_in_Chrome__javascript_tool` to execute a same-origin `fetch()` (so cookies/auth carry over) against that endpoint with the date parameters adjusted to the target date(s), and parse the JSON response.
4. From the response, build a JS object matching this exact schema (one entry per date):
```json
{
  "YYYY-MM-DD": [
    {"pid": "...", "name": "...", "gmv": 0, "orders": 0, "sku_orders": 0, "items_sold": 0,
     "self_live": 0, "self_video": 0, "affiliate": 0, "affiliate_live": 0, "affiliate_video": 0, "product_card": 0},
    ...
  ]
}
```
Map the Compass response's fields onto these keys (field names in the TikTok UI are Thai/English mixed — gmv = total GMV for the product that day, self_live/self_video = GMV from the seller's own livestreams/videos, affiliate = total affiliate-driven GMV, affiliate_live/affiliate_video = the affiliate sub-breakdown, product_card = GMV from product-card/search placements). If a field genuinely isn't present in the response, default it to 0 rather than guessing.

Step 3 — Save that JSON to a temp file, e.g. `tiktok_product_daily_new.json` in the `All/` folder (via bash so it's in the same folder as the merge script).

Step 4 — Run the parent-level merge: `cd` into the `All/` folder (VM path) and run `python3 tiktok_product_merge.py tiktok_product_daily_new.json`. This merges the new date(s) into `TK_PROD_DATA` (dates/names/daily) inside WIBWUB_Dashboard.html, additive-only (never deletes existing dates), and auto-commits WIBWUB_Dashboard.html with a `WIBWUB Bot <marketingwibwub@gmail.com>` commit.

Step 5 — Also fetch and merge SKU/variant-level data (`TK_PROD_SKU`), in the same run, so it never falls behind `TK_PROD_DATA` again:
1. Determine a multi-day chunk ending yesterday. **The SKU-level endpoint (`/api/v2/insights/seller/ttp/product/sku/list`) rejects single-day ranges** (start===end fails with error code 98001021) and only returns ONE aggregate number per SKU for the whole range, not a true per-day breakdown. So pick a short window that ends at yesterday — e.g. if `TK_PROD_SKU`'s last date + 1 through yesterday is only 1 day, widen it to at least 2-3 days (going a bit further back is fine and harmless; the merge script overwrites/redistributes evenly across every date in the chunk, and re-running it for already-covered dates is safe/idempotent).
2. In Chrome, open the Compass product page and switch to its "ตาม SKU" / SKU/variant sub-view for that date range so the page fires its own request to `/api/v2/insights/seller/ttp/product/sku/list`. Capture the exact request (url + headers, which carry the anti-bot signature/msToken) via `mcp__Claude_in_Chrome__read_network_requests` — never hand-construct or guess a signature.
3. This endpoint paginates (10 SKUs per page, `body.request.list_control.pagination.page` starting at 0). To fetch all pages reliably via `mcp__Claude_in_Chrome__javascript_tool`:
   - Top-level `async () => {...}` expressions do NOT get awaited by the tool and return `{}` immediately. Instead: fire the async loop without awaiting (store progress/results into a `window.__skuPages` array and any error into `window.__skuError`), return a synchronous placeholder string like `"started"`, then poll `window.__skuPages.length` in a follow-up call (after a short `wait`) until it reaches `total_page` from the first response's `data.list_control.next_pagination`.
   - Replay each page with the captured `url`/`headers` verbatim and `credentials:'include'`, changing only `body.request.list_control.pagination.page`.
   - Never `JSON.stringify()` the full captured request/response object in one shot — including `url` or image fields (`product_image`/`sku_image`) triggers a `[BLOCKED: Cookie/query string data]` error from the tool. Only pull out specific plain fields you actually need (pid, sku_id, sku_property_value, gmv amount, orders, items_sold).
4. Once all pages are collected in `window.__skuPages`, flatten them client-side into simple records `{"pid","sid","prop","gmv","orders","items_sold"}` and build one combined JSON string. **Do not try to read large JSON (multi-KB) back through `javascript_tool` in text chunks** — outputs above roughly 1500-2000 characters can come back silently truncated even when the underlying JS string is correct. Instead, trigger a real browser download: build a `Blob` from the JSON string, `URL.createObjectURL()` it, create a hidden `<a download="...">` pointed at that URL, and `.click()` it. This saves the complete file to the user's real Downloads folder, which you can then read intact via `mcp__workspace__bash` (mounted at `/Users/thanasablilutanon/Downloads/`).
5. Wrap the flat array of records under a single chunk key `"STARTDATE_ENDDATE"` (e.g. `{"2026-09-08_2026-09-10": [...]}`) — this is the exact input shape `tiktok_sku_merge.py` expects — and save it to a file in the `All/` folder (e.g. `tiktok_sku_daily_new.json`).
6. Run `python3 tiktok_sku_merge.py tiktok_sku_daily_new.json`. This divides each numeric field evenly across every date in the chunk (since the API only gives a range total, not true per-day figures) and writes `TK_PROD_SKU[date] = {pid: [...]}` for each date, then auto-commits WIBWUB_Dashboard.html again.
   - **Known limitation, not a bug**: because a multi-day chunk's SKU total is spread evenly across its dates, a single day's `TK_PROD_SKU` entry will NOT exactly equal that same single day's real `TK_PROD_DATA` parent GMV (real daily parent sales fluctuate day-to-day; the averaged SKU figure doesn't). This was spot-checked on 2026-09-07: per-single-day mismatches were 20-50%, but summed back over the full chunk, SKU totals matched parent totals to within ~0.2% (rounding only). This is expected and acceptable — don't try to "fix" it by inventing a fake per-day split; just make sure the aggregate reconciles.

Step 6 — Bump the cache version in `sw.js` (e.g. `wibwub-v928` → `wibwub-v929`, always +1 from whatever is currently there — check the file first, don't assume a fixed number), then `git add sw.js && git commit -m "chore: bump sw.js cache version"` (separate commit, since both merge scripts only stage the dashboard HTML).

Step 7 — `git push origin main` will fail in this sandbox (proxy 403 — expected, not an error to report as a failure). Do NOT try to work around it. Instead, in your final summary, remind the user to double-click `push_now.command` on their real machine to publish the change to the live GitHub Pages dashboard, and mention the commit message(s) you just made so they know what's pending.

Important gotchas (from the skill history for this dashboard, same conventions apply here):
- Never guess/hardcode a msToken, sign, or anti-bot signature — only replay requests you've actually observed the live page make.
- If Compass's UI or API shape has changed since this task was written and you can't get a clean per-day per-product (or per-SKU) response after reasonable effort, stop and clearly report what you tried and what broke, rather than writing partial/malformed data into TK_PROD_DATA or TK_PROD_SKU.
- **ห้ามลบ `.git/*.lock` เอง** — มีงานตั้งเวลาอื่นรันพร้อมกันได้ ถ้า `git commit` ติด lock ให้รอ 20 วินาทีแล้วลองใหม่ สูงสุด 3 ครั้ง
- If fetching SKU-level data fails for any reason after reasonable effort (endpoint changed, no clean chunk available, etc.), don't let that block the parent-level (`TK_PROD_DATA`) update — commit that part and just report the SKU-level failure clearly, so daily parent-level freshness is never held hostage to the newer SKU step.

At the end, give a short Thai-language summary: which date(s) were added/updated for both TK_PROD_DATA and TK_PROD_SKU, how many products/SKUs, and remind the user about push_now.command.