---
name: wibwub-samp-request-sync
description: ทุกวัน 09:35/20:35 — ดึงข้อมูลสดจากชีต "ขอสินค้า" มาอัปเดตแท็บ คำขอสินค้า (SAMPLE_MONTHS + SAMPLE_PRODUCTS) ใน WIBWUB_Affiliate_Dashboard.html
---

<!-- LOCAL-OVERRIDE v1 -->
> **อ่านก่อน — ข้อนี้ทับคำสั่งที่ขัดกันในไฟล์นี้ทั้งหมด**
> ไฟล์นี้เขียนไว้ตอนรันบน Cowork cloud sandbox ตอนนี้ย้ายมารันบนเครื่อง Mac แล้ว
> - BASE / ALL_MNT = `/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All` · Downloads = `/Users/thanasablilutanon/Downloads` · OUTPUTS = `/Users/thanasablilutanon/Library/Caches/wibwub-outputs`
> - `git push` **ไม่ต้องทำ** และจะ**ไม่**เจอ error 403 แบบ sandbox — launchd `com.wibwub.autopush` push ให้เองทุก 2 นาที ข้ามทุกหัวข้อที่พูดถึง 403 / การสร้างหรือแก้ `push_now.command`
> - ที่ไหนเขียนว่า `mcp__workspace__bash` ให้ใช้ Bash tool ปกติแทน
> - อ่านไฟล์ในเครื่องใช้ Read/Bash ได้ตรง ๆ ไม่ต้องผ่าน connector
> - ถ้าขั้นไหนอ้าง path หรือเครื่องมือที่ไม่มีจริง: **หยุดและรายงาน ห้ามเดาทางเอง**

## WIBWUB Affiliate Dashboard — sync "คำขอสินค้า" (product-request) tab from the live sheet

Goal: refresh `SAMPLE_MONTHS` and `SAMPLE_PRODUCTS`/`SAMPLE_PRODUCTS_LAST7D` in `WIBWUB_Affiliate_Dashboard.html` (in the WIBWUB "All" Google Drive workspace folder) so the "คำขอสินค้า" tab reflects the latest rows a team member has added to the source Google Sheet today. This sheet gets new rows added by staff throughout the day, so this must run automatically — don't skip it just because "nothing seems new."

### Source

Google Sheet **"Top 30 Affiliate"**, fileId `1EYzinmagF1iTXgKe7PNU5SVD9WcTvHhuO054aWKITxg`, tab **"ขอสินค้า"**, gid `1644804644`.

### STEP 1 — Fetch the sheet live via Chrome

1. Select the Mac Chrome browser explicitly (never let it auto-pick — could run on the wrong device if multiple browsers are connected). Call `list_connected_browsers` and pick the entry with `osPlatform` macOS / `isLocal:true`, then `select_browser(deviceId=...)` → `tabs_context_mcp(createIfEmpty=true)`.
2. Navigate (via `browser_batch`, NEVER standalone `navigate` — it hangs) to any open tab, then run `javascript_tool` to fetch:
   ```js
   fetch('https://docs.google.com/spreadsheets/d/1EYzinmagF1iTXgKe7PNU5SVD9WcTvHhuO054aWKITxg/gviz/tq?tqx=out:csv&gid=1644804644', {credentials:'include'})
     .then(r => r.text()).then(t => { window.__sheetCsv = t; window.__sheetCsvLen = t.length; });
   ```
   Wait a couple seconds, then read `window.__sheetCsvLen` to confirm it fetched, then read `window.__sheetCsv` back out.
3. **Output truncation gotcha:** `javascript_tool` truncates returned strings at ~900-1000 chars. Read `window.__sheetCsv` back in ~900-char slices (`window.__sheetCsv.slice(0,900)`, `.slice(900,1800)`, etc. using `window.__sheetCsvLen` to know when to stop) across multiple calls and reconstruct the full CSV text yourself before parsing.
4. Parse the CSV with a proper quoted-field-aware parser (char-by-char state machine) — a naive `.split(',')`/`.split('\n')` will break on creator names or product lists that contain commas inside quotes.

### STEP 2 — Column layout (do not confuse col 4 and col 5)

`NO. | Date | Creator | url | สินค้าที่ Creator ขอ | สินค้าที่ให้ | Status | Category | GMV 1 เดือนล่าสุด | Top 3 สินค้าขายได้ 1 เดือนล่าสุด | ...`

- col 1 (Date) = `DD/MM/YYYY` in Buddhist era. Convert year: `if (yr > 2400) yr -= 543;`
- **col 4 "สินค้าที่ Creator ขอ" = the column to use for counting requests per product.** It's populated for both Approved and Rejected rows at similar rates (~80%).
- col 5 "สินค้าที่ให้" (what was shipped) — **do NOT use this for request counts.** It's only filled in on approval, so building per-product counts from it systematically undercounts/mislabels rejected requests. (This was a real bug shipped once and caught by the user — do not reintroduce it.)
- col 6 Status: `Approve`, `Reject`, `On Process`, `Done`, `Sent Product`, `Waiting`, or blank.

### STEP 3 — Recompute data

Bucket rows by month (`YYYY-MM` from col 1, after Buddhist→Gregorian conversion).

For `SAMPLE_MONTHS`: recompute `funnel.req` (count of rows) and `funnel.appr` (count where Status=='Approve') for the CURRENT month only (in-progress month, since past months are already finalized and confirmed — don't silently rewrite historical months; if a past month's row count changed, flag it in the report instead of overwriting).

For `SAMPLE_PRODUCTS[currentMonthKey]` and the `all`/`last7d` aggregates, rebuild using col 4:
```js
{
  total: N,
  unspecified: {c:N, appr:N, rej:N, other:N},   // rows where col4 is blank/"-"
  items: [ {n:'ProductName', c:N, appr:N, rej:N, other:N}, ... ]  // one per product name in col4
}
```
- `appr` = Status=='Approve' count, `rej` = Status=='Reject' count, `other` = everything else (On Process/Done/Sent Product/Waiting/blank).
- A request can list multiple products in col4 (comma-separated) — count it toward EACH product listed. `sum(items[].c)` can legitimately exceed `total`; this is expected and documented in the on-page note, don't dedupe it away.
- `SAMPLE_PRODUCTS_LAST7D` = rolling last-7-calendar-days window computed directly from the date column, independent of the monthly buckets.
- `SAMPLE_PRODUCTS['all']`/`productsByKey('all')` is computed on-the-fly in the JS itself (sums all monthly buckets) — you don't need to hardcode it, just make sure the per-month buckets are correct and that function will stay correct automatically.

### STEP 4 — Update the file

In `WIBWUB_Affiliate_Dashboard.html`:
- `SAMPLE_MONTHS` (~line 8773): update the CURRENT month's `funnel.req`/`funnel.appr` entry only. If the current month's key doesn't exist yet in the array, append a new entry (copy the shape of the last entry, mark `partial:true` with an updated date range like `"01/MM/YYYY - DD/MM/YYYY"` in `range` and `label`).
- `SAMPLE_PRODUCTS` (near `productsByKey`, ~line 8830): update/replace the current month's entry with the recomputed object from STEP 3.
- `SAMPLE_PRODUCTS_LAST7D`: replace with the freshly recomputed rolling-7-day object.
- Do not touch any other month's data.

### STEP 5 — Validate, bump cache, commit

1. Extract the `<script>` block from the HTML and run `node --check` on it (via bash) — must pass with no errors before proceeding.
2. Run `git diff --stat WIBWUB_Affiliate_Dashboard.html` — if the diff touches more than the SAMPLE_MONTHS/SAMPLE_PRODUCTS/SAMPLE_PRODUCTS_LAST7D regions, stop and do not commit; report the anomaly instead.
3. Bump `sw.js`: read current `const CACHE = 'wibwub-vNNN';`, increment by 1, write it back.
4. `git add WIBWUB_Affiliate_Dashboard.html sw.js` then commit with `git -c user.name="WIBWUB Bot" -c user.email="marketingwibwub@gmail.com" commit -m "auto-update: คำขอสินค้า $(date +%Y-%m-%d)"`.
5. Sandbox `git push` will fail with a 403 proxy error — this is expected, do not troubleshoot it. Make sure `push_now.command` exists in the workspace root and stages `WIBWUB_Affiliate_Dashboard.html sw.js` (create/refresh it if missing, following the pattern used by the other wibwub-* scheduled tasks).

### STEP 6 — Report

Short Thai summary: current month req/approve/reject totals, top products this month, whether any anomaly was flagged (e.g. row count for a past month changed, or diff looked too large to commit), sw.js version bump, and remind to double-click `push_now.command` to deploy.

### If something fails
- Chrome not connected / session expired → log it and stop, don't guess at data.
- CSV fetch returns much shorter than expected or header row doesn't match the expected columns → the sheet structure may have changed; stop and flag for manual review rather than writing bad data.
- `node --check` fails → do not commit; report the syntax issue instead.