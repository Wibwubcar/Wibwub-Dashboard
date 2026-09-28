# WIBWUB Sales Update Report — 2026-09-20 (09:30 run)

## Result: Fixed a stale-data bug carried over from the 2026-09-19 run

## STEP 0 — Array-length verification (verify-only)

`M5` and all sales arrays (`SH_REV`, `TK_REV`, `LZ_REV`, `SH_ORD`, `SH_CANCEL_PCT`, `SH_ADS`,
`SH_FEE`, `LZ_ADS`, `LZ_FEE`, `LZ_COUPON`, `LZ_COST_PCT`, `TK_AFI`, `TK_NET`, `TK_ADS`,
`TK_AFIPCT`, `TK_ADSSPEND`, `TK_FEECOMM`, `TK_LIVE`, etc.) all have 9 elements (Jan–Sep) in both
`WIBWUB_Dashboard.html` and `WIBWUB_Mobile.html`. No length mismatch — safe to proceed.

## STEP 1 — Source sheet check (last row of each month)

| Platform | Latest sheet row | Key figures |
|---|---|---|
| Shopee | 01-13/09/26 | Rev 3,326,267 / Ads 542,141.58 / Fee 996,549.59 / Ord 5,857 / Cancel% 5.53 |
| Lazada | 01-13/09/26 | Rev 59,719.97 / Ads 3,470 / Fee 12,547.48 / Coupon 1,140 / Cost% 28.73 |
| TikTok | 01-17/09/26 | Sales(ยอดขาย) 1,859,948.75 / Afi 1,140,248.32 / Net(หลังหัก) 1,122,613.16 / Ads-attributed sales 1,872,387.94 / Ads spend 494,337.18 / Fee+Comm 550,174.50 / Live 218,100.00 (order/cancel/new/old columns for this row are still blank in the sheet — kept at the 01-13 row's values: Ord 6,041 / Cancel% 6.64 / New 4,408 / Old 722) |

Shopee and Lazada figures were already identical to what's in the dashboard — no change needed
for those two platforms.

## Bug found and fixed — TikTok array desync

The 2026-09-19 run (commit `f82c5e0`, titled "TK_REV MTD through 17 Sep") only advanced
`TK_REV[8]` to the newer 01-17 sheet row, but left `TK_AFI`, `TK_NET`, `TK_ADS`, `TK_AFIPCT`,
`TK_ADSSPEND`, `TK_FEECOMM`, and `TK_LIVE` (Dashboard) at the older 01-16 row's values. That left
September's TikTok figures internally inconsistent (revenue from one date, fees/ads/live from
an earlier date) in both dashboards.

Fixed this run — synced all of these to the 01-17/09/26 row in both files:

| Array | Old (01-16 row) | New (01-17 row) |
|---|---|---|
| TK_AFI[8] | 1,055,400.72 | 1,140,248.32 |
| TK_NET[8] | 1,039,624.10 | 1,122,613.16 |
| TK_ADS[8] (Dashboard only) | 1,771,249.56 | 1,872,387.94 |
| TK_AFIPCT[8] (Dashboard only) | 60.0 | 60.4 |
| TK_ADSSPEND[8] | 465,382.31 | 494,337.18 |
| TK_FEECOMM[8] | 510,876.58 | 550,174.50 |
| TK_LIVE[8] (Dashboard only) | 180,200 | 218,100.00 |

`TK_ORD`, `TK_CANCEL_PCT`, `TK_NEW`, `TK_OLD` were left unchanged (6,041 / 6.64 / 4,408 / 722) —
the sheet's 01-17 row still has blank order/cancellation/customer columns, so the 01-13 row
remains the latest available data for those fields. No hardcoded KPI text duplicated the old
TikTok numbers, so no text edits were needed. `MTD_COVERAGE` (TikTok: 2026-09-17) was already
correct.

## STEP 3B — Date picker

Not applicable — no new month was added (still Jan–Sep, idx 0-8).

## STEP 4 — sw.js / git

- Bumped `sw.js` cache version: `wibwub-v1170` → `wibwub-v1171`.
- Committed `WIBWUB_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js` as commit `0d489c1`.
- **Note:** `WIBWUB_Mobile.html` had an unrelated, already-in-progress Affiliate GMV update
  sitting uncommitted in the working tree (mks-grid card + `AFI_GMV`/`AFI_NET`/`AFI_COMM`
  arrays, "กย.69 (1-17)" → "(1-18)"). That wasn't part of this task, so it was reverted in the
  file before committing and is still sitting uncommitted in the working tree for whichever
  process owns it to commit separately — it was not lost.
- **Also note:** `git add` for this commit unexpectedly swept in `Data Shipnity/stock/stock_snapshot.json`
  (a small pre-existing staged change from another automation, 2 lines). It's legitimate data,
  just bundled into this commit's history rather than its own — flagging for visibility, no
  action taken since rewriting history wasn't safe to do unattended.
- Sandbox can't push directly (proxy blocks it) — `push_now.command` was regenerated in the
  folder; run it locally to push commit `0d489c1` to `origin/main`.

**Files modified this run**: `WIBWUB_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js`.
