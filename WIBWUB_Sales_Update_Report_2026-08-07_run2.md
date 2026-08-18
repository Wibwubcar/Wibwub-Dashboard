# WIBWUB Sales Sheet Update — 2026-08-07 (extra run)

## Result: bug fix committed — no new month data (August still incomplete in all 3 sheets)

## What happened
Found `WIBWUB_Dashboard.html` and `WIBWUB_Mobile.html` in a **corrupted, uncommitted state** on disk:
`M5` had 8 elements (`"ส.ค."` appended) and `SH_ADS` had 8 elements (165149.67 appended), while
`SH_REV`/`TK_REV`/`LZ_REV`/`SH_ORD`/etc. still had 7. This is exactly the documented array-length-mismatch
bug (charts read `M5[7]` against `undefined` data). The stray `165149.67` value traces to the *Shopee Ads*
spend total for Aug 1-7 in `data Ads/WIBWUB_Ads_Dashboard.html` (a different, unrelated dashboard that a
concurrent task was legitimately updating) — it looks like it leaked into the wrong file/array during an
earlier partial run.

**Fix:** reverted `M5` and `SH_ADS` back to 7 elements in both files (matching all other sales arrays).

## Sheet check (last cumulative row per platform, ยอดประจำปี tables)
| แหล่ง | เดือนล่าสุดที่มีข้อมูลครบ | เดือน ส.ค. 2026 |
|---|---|---|
| Shopee | 01-31/07/26 → 5,923,704 / ads 942,122.40 / fee 1,774,741.72 / order 10,511 (cancel 5.34%) | มีแค่ 01-05/08/26 (ยังไม่ครบเดือน) |
| Lazada | 01-31/07/26 → 95,770.98 / ads 9,710 / fee 16,914.09 / cost% 30.99 | มีแค่ 01-05/08/26 (ยังไม่ครบเดือน) |
| TikTok | 01-31/07/26 → 2,089,005.47 / ads 508,456.37 / commission 613,482.79 / order 10,094 | มีแค่ 01-05/08/26 (ยังไม่ครบเดือน) |

All three platforms' July cumulative figures were re-verified against the current arrays (index 6) and
match exactly — no drift, no new data to push this run.

## Committed
`de1ea80` — "fix: revert corrupted Aug stub in M5/SH_ADS (sales arrays) — Aug data incomplete in sheets,
cache bump v597" — 3 files (`WIBWUB_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js`).
Branch is 1 commit ahead of `origin/main`. A `push_now.command` already exists (created by a concurrent
Ads Dashboard task run) and will push this commit along with its own when the user runs it.

## Next run
Watch for all three platforms' `01-XX/08/26` row to reach a full month before adding "ส.ค." to
`M5`/`MONTH_LABELS_FULL`/`MONTH_LABELS_SHORT`/`MP_MONTH_BOUNDS` — push label + real values into every
array together, per STEP 3B.
