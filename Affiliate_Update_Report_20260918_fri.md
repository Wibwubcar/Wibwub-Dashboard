# WIBWUB Affiliate Dashboard Update — 2026-09-18 (Fri)

**Shop:** 7494549095358892612 (TH) | **Period covered:** Sep 1–16, 2026 (ก.ย. (1-16))

## Summary

| Metric | Previous | Updated | Δ |
|---|---|---|---|
| GMV | 1,140,058 | 1,140,248 | +190 |
| Net GMV | 1,057,329 | 1,057,024 | -305 |
| Commission | 125,843 | 126,202 | +359 |
| Creators (GMV>0) | 676 | 676 | 0 |

This period's label (ก.ย. (1-16)) already existed as the last entry in both dashboards, so this run **overwrote** that entry with refreshed totals rather than appending a new column (TikTok's export data for this range had settled/changed slightly since the last pull).

## Products (cr/vid updated, 7 matched)

| Product | cr | vid |
|---|---|---|
| WIBWUB Refresh Leather Wipes | 370 | 289 |
| WIBWUB Interior wipes | 169 | 148 |
| WIBWUB Sugar | 159 | 130 |
| WIBWUB CLEANER | 26 | 17 |
| WIBWUB Interior | 46 | 66 |
| WIBWUB Refresh | 0 | 0 |
| WIBWUB Visible | 9 | 15 |

61 other SKUs (non-WIBWUB-branded accessory/tool line items) did not match any keyword and were left untouched, consistent with SKILL.md's fuzzy-matching scope.

## Videos / Livestreams — SKIPPED (no new export)

TikTok's Affiliate Insights sidebar currently only exposes 5 sub-pages (Performance, Sample Analytics, Outreach, Product Analytics, Creator Analysis) — there is no dedicated Video Analysis or Livestream Analysis page in the current UI, so no export button could be found for either this run. Newest files on disk remain unchanged: Video_Analysis_Video_List_20260901-20260915.xlsx (Sep 17) and Transaction_Analysis_Live_List_20260906-20260912.xlsx (Sep 14). VIDEOS array was **not** modified this run — this gap should be flagged for a UI-path fix in the skill.

## Files updated

- `WIBWUB_Affiliate_Dashboard.html` — AF_GMV/AF_NET/AF_COM/AF_CR (index 8 overwritten), PRODUCTS[].cr/vid (7 rows)
- `WIBWUB_Mobile.html` — AFI_GMV/AFI_NET/AFI_COMM (index 10 overwritten)
- `sw.js` — cache version bumped v1157 → v1158

## Note on a false alarm this run

Early in the run, repeated `503` responses were observed on TikTok's `export/file` status-polling endpoint across multiple report IDs, which looked like a site-wide export outage. This was a red herring — the actual files had already downloaded successfully via a different code path and were auto-relocated into the correct `Data Affiliate/` subfolders by the local LaunchAgent within seconds, faster than the bash checks could catch them in Downloads. No blocker actually occurred for ครีเอเตอร์ or สินค้า.

## Action needed

**Push to GitHub:** `push_now.command` (in the All folder) has been updated to `git add` + `commit` + `push` the 3 changed files in one step — the sandbox couldn't commit directly this run (`.git/index.lock` unremovable due to filesystem permissions on the Drive-synced repo). Please double-click `push_now.command` to publish these changes.
