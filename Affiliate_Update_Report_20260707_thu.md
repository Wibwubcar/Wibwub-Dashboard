# WIBWUB Affiliate Auto-Update — Thursday 2026-07-07

## Summary
Partial success. 2 of 4 TikTok exports completed and applied; the ครีเอเตอร์ (Creator) and วีดีโอ (Video) exports for 2026-07-01–07-06 never finished processing on TikTok's side after 3 export attempts and ~20+ minutes of waiting, so those two updates are deferred to the next run.

## Files exported/downloaded
- ✅ **สินค้า (Product)** — `Transaction_Analysis_Product_List_20260701-20260706.xlsx` (moved to `Data Affiliate/สินค้า/`)
- ✅ **ไลฟ์สตรีม (Live)** — `Transaction_Analysis_Live_List_20260701-20260706.xlsx` (moved to `Data Affiliate/ไลฟ์สตรีม/`), found via the legacy "ผลการดำเนินงาน" page's "รายละเอียด" tabbed section
- ❌ **ครีเอเตอร์ (Creator)** — 3 export attempts (2 via new dedicated page, 1 via legacy page) all stuck at "กำลังส่งออก" (processing) and never completed. Likely a TikTok-side bottleneck given the 6,400-affiliate dataset size.
- ❌ **วีดีโอ (Video)** — 1 export attempt stuck at "กำลังส่งออก", never completed.

## Dashboard changes applied (WIBWUB_Affiliate_Dashboard.html)
Updated only the `cr` (creator count) and `vid` (video count) fields in the `PRODUCTS` array, per the Product export (fuzzy name-matched, 7/7 products found):

| Product | cr (old→new) | vid (old→new) |
|---|---|---|
| WIBWUB Refresh Leather Wipes | 27 → 82 | 28 → 31 |
| WIBWUB Interior wipes | 19 → 65 | 23 → 26 |
| WIBWUB Sugar | 10 → 42 | 26 → 28 |
| WIBWUB CLEANER | 8 → 28 | 6 → 6 |
| WIBWUB Interior | 5 → 20 | 18 → 18 |
| WIBWUB Refresh | 4 → 17 | 7 → 7 |
| WIBWUB Visible | 1 → 6 | 1 → 1 |

No other PRODUCTS fields (gmv/units/monthly/ret) were touched.

Also left the hardcoded "ผ่าน 1,168 creators" KPI text (line ~337) untouched — it does not correspond to the sum of the `cr` fields above (which is only 260), so its source is unclear and I did not want to guess.

## NOT updated this run (blocked)
- `AF_MO` / `AF_GMV` / `AF_NET` / `AF_COM` / `AF_CR` in WIBWUB_Affiliate_Dashboard.html
- `AFI_MONTHS` / `AFI_GMV` / `AFI_NET` / `AFI_COMM` in WIBWUB_Mobile.html
- `VIDEOS` array in WIBWUB_Affiliate_Dashboard.html

These all require the Creator and/or Video export files, which never finished downloading. **Next run should retry these exports first before anything else** — the Product/Live files may still be usable from today if TikTok returns the same date range, but Creator/Video need a fresh attempt.

## Live-stream (ไลฟ์สตรีม) data — inspected, not yet added to dashboard
The dashboard has no live-stream display section. Per the skill's instruction not to silently skip this, here are the summary stats extracted from the file (2026-07-01 to 2026-07-06, though it also includes a couple of live sessions from 06/28–06/29):
- 15 order-line rows across **7 unique live sessions**
- Total GMV from live: **฿9,192.31**
- Top creator by live GMV: **wanchai_4343** (฿4,742.64) vs ralph.detailing8 (฿4,449.67) — close
- Judgment call: did not add a new "Live" tab/section to the dashboard this run since that's a design decision (new UI section) rather than a data update — flagging here for a decision on whether/how to surface this going forward.

## Version bump
- `sw.js` cache version bumped: `wibwub-v340` → `wibwub-v341`

## Git
- Committed locally: `6ce400d auto: Thursday affiliate update 2026-07-07 - Product cr/vid + cache bump (Creator/Video exports pending)`
- **Not pushed** — bash sandbox cannot push directly (proxy blocks HTTPS). Run `push_now.command` in the `All` folder to push to GitHub.
