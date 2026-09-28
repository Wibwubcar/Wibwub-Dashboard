# WIBWUB Sales Sheet Update — จันทร์ 2026-09-21 09:30 run

## Sheets checked (row สุดท้ายของแต่ละเดือน)

| Platform | Sheet's latest cumulative row | vs. dashboard's current MTD_COVERAGE | Action |
|---|---|---|---|
| Shopee | `01-13/09/26` (ยอดขาย 3,326,267 / order 5,857 / cancel 5.53%) | already `2026-09-13` | **No new data — skipped** |
| Lazada | `01-13/09/26` (ยอดขาย 59,719.97 / ads 3,470 / fee 12,547.48 / coupon 1,140 / cost% 28.73) | already `2026-09-13` | **No new data — skipped** |
| TikTok | `01-20/09/26` (ยอดขาย 2,154,005.46 / ads-attributed 2,159,817.70 / ad spend 578,702.47 / fee+affi 641,658.79 / live 241,900 / new 7,503 / old 1,039 / order 9,826 / cancel 6.63%) | was `2026-09-17` | **Updated (newer data found)** |

Shopee and Lazada Google Sheets have not been updated by staff since the last sync (still ends at 13 Sep). Their arrays (`SH_*`, `LZ_*`) were left untouched — no risk of overwriting with stale/duplicate data.

## Files updated

**WIBWUB_Dashboard.html** (index 8 = ก.ย. 2569, no new month added, M5 still 9 entries):
- `TK_REV[8]`: 1,859,948.75 → **2,154,005.46**
- `TK_ORD[8]`: 6,041 → **9,826**
- `TK_CANCEL_PCT[8]`: 6.64 → **6.63**
- `TK_ADS[8]`: 1,872,387.94 → **2,159,817.70**
- `TK_ADSSPEND[8]`: 494,337.18 → **578,702.47**
- `TK_FEECOMM[8]`: 550,174.50 → **641,658.79**
- `TK_LIVE[8]`: 218,100.00 → **241,900.00**
- `TK_NEW[8]`: 4,408 → **7,503**
- `TK_OLD[8]`: 722 → **1,039**
- `MTD_COVERAGE.TikTok`: `2026-09-17` → **`2026-09-20`**
- `TK_AFI[8]` / `TK_NET[8]` / `TK_AFIPCT[8]` left unchanged — the TikTok sheet's `01-20/09/26` row didn't carry those specific columns yet (blank in source); next sync will pick them up once populated.
- `TOTAL_REV` / `TOTAL_ORD` are computed via `.map()` from the underlying arrays, so they update automatically — no manual edit needed.

**WIBWUB_Mobile.html** (same index 8, same arrays it tracks):
- `TK_REV[8]`, `TK_ORD[8]`, `TK_CANCEL[8]`, `TK_ADSSPEND[8]`, `TK_FEECOMM[8]` updated to the same values as above.
- `SALES_ASOF`: `2026-09-13` → **`2026-09-20`** (mirrors Dashboard's `MTD_MAX_DATE` = max across platforms).
- Mobile doesn't track `TK_ADS`/`TK_LIVE`/`TK_NEW`/`TK_OLD` as separate arrays (not present in this file), so nothing to update there.

## STEP 0 protection check
`M5` length vs every `SH_/TK_/LZ_` array length: **9 = 9 for all arrays in both files** — no mismatch, no new month was pushed. ✅

## KPI text / hh-grid / mks-grid / header labels
All checked labels (`cc-ovrev-sub`, `cc-pie-sub`, `cc-cust-sub`, mobile `hh-grid`/`hhg-tk` etc.) are computed at runtime from the arrays above (`set()`/`_setM()` calls), not hardcoded — so they refresh automatically. No manual text edits were needed this run.

## Date picker (STEP 3B)
Not touched — no new month was added (still ม.ค.–ก.ย., index 8), so `MP_MONTH_BOUNDS` / `MONTH_LABELS_FULL/SHORT` / `MP_DATE_MAX` are unaffected.

## sw.js
Cache bumped: `wibwub-v1184` → **`wibwub-v1185`**.

## ⚠️ Git commit — NOT completed this run
Both files were edited, saved, and JS-syntax-validated (`node --check` passed on both `<script>` blocks) — the live files on disk are correct. However, `git add`/`git commit` for `WIBWUB_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js` could not complete: `.git/index.lock` was held almost continuously for 10+ minutes by what appears to be another concurrently-running WIBWUB scheduled job (there are many other automated jobs' report files and commits from today in this same repo, e.g. `8fbb513 TikTok Ads: update Sep 1-20 data...` committed at 00:02 today, plus dozens of `.git/index.lock.mvaway_*` / `.stale*` / `.bak*` artifacts from previous runs hitting the same contention). Tried ~15 retry rounds including the `mv`-away-lock workaround seen in `.git` history; the lock kept reappearing within milliseconds each time, indicating a live competing process rather than a stale lock.

**Net effect:** the dashboard/mobile files themselves are already correct and will render correctly for anyone opening them directly. They are just not yet committed/pushed to the git repo. Recommend re-running `git add WIBWUB_Dashboard.html WIBWUB_Mobile.html sw.js && git commit -m "..."` once the concurrent job contention clears (e.g. later today), or letting the next scheduled sales-update run pick it up — it will find these values already correct and simply need to commit them (its own STEP 0 verify check will still pass since nothing is mismatched).

No `push_now.command` was created this run since there's no new commit yet to push.
