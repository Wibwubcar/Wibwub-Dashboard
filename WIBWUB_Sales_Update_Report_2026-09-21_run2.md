# WIBWUB Sales Sheet Update — จันทร์ 2026-09-21 (run 2)

## Context
An earlier 09:30 run today already synced TikTok's core revenue/order fields to the sheet's
`01-20/09/26` row, but its commit failed on git lock contention and it left `TK_AFI`/`TK_NET`/
`TK_AFIPCT` unrefreshed (sheet had those columns blank at the time). This run re-checked all
three sheets from scratch.

## Sheets checked (row สุดท้ายของแต่ละเดือน)

| Platform | Sheet's latest cumulative row | vs. dashboard before this run | Action |
|---|---|---|---|
| Shopee | `01-20/09/26` — ยอดขาย 4,802,418 / ads 802,234.87 / fee 1,438,804.43 / order 8,456 / cancel 5.4754% | was `01-13/09/26` (3,326,267 / 5,857 orders) | **Updated** |
| Lazada | `01-20/09/26` — ยอดขาย 85,324.24 / ads 6,490 / fee 15,069.19 / coupon 1,980 / cost% 27.588% | was `01-13/09/26` (59,719.97) | **Updated** |
| TikTok | `01-20/09/26` — Afi 1,334,858.42 / Net 1,314,711.12 / Afi% 61.036% (Rev/Ord/Ads/Fee/Live/New/Old already synced by the 09:30 run) | Afi/Net/Afi% still at `01-17/09/26` values | **Updated (Afi/Net/Afi% only)** |

## STEP 0 protection check
`M5` and every `SH_/TK_/LZ_` array: **9 = 9** in both files before and after edit — no new month
pushed, no mismatch. ✅

## Files updated

**WIBWUB_Dashboard.html** (index 8 = ก.ย. 2569):
- `SH_REV[8]`: 3,326,267 → **4,802,418**
- `SH_ORD[8]`: 5,857 → **8,456**
- `SH_CANCEL_PCT[8]`: 5.53 → **5.48**
- `SH_FEE[8]`: 996,549.59 → **1,438,804.43**
- `SH_ADS[8]` left untouched (714,615.75) — already synced separately by the dedicated Shopee Ads
  download job (commit `6dc77c3`); file has an explicit comment warning not to overwrite it from
  this sheet.
- `LZ_REV[8]`: 59,719.97 → **85,324.24**
- `LZ_ADS[8]`: 3,470 → **6,490**
- `LZ_FEE[8]`: 12,547.48 → **15,069.19**
- `LZ_COUPON[8]`: 1,140 → **1,980**
- `LZ_COST_PCT[8]`: 28.73 → **27.59**
- `TK_AFI[8]`: 1,140,248.32 → **1,334,858.42**
- `TK_NET[8]`: 1,122,613.16 → **1,314,711.12**
- `TK_AFIPCT[8]`: 60.4 → **61.0**
- `MTD_COVERAGE`: `{Shopee:'2026-09-13', TikTok:'2026-09-20', Lazada:'2026-09-13'}` → **`{Shopee:'2026-09-20', TikTok:'2026-09-20', Lazada:'2026-09-20'}`**
- `TOTAL_REV`/`TOTAL_ORD` are `.map()`-derived — update automatically.

**WIBWUB_Mobile.html** (same index 8, same values):
- `SH_REV[8]`, `SH_ORD[8]`, `SH_CANCEL[8]`, `SH_FEE[8]`, `LZ_REV[8]`, `LZ_ADS[8]`, `LZ_COST_PCT[8]`,
  `TK_AFI[8]`, `TK_NET[8]` all updated to the same figures as above.
- Mobile doesn't track `LZ_FEE`/`LZ_COUPON`/`TK_AFIPCT` as separate arrays — nothing to update there.
- `SALES_ASOF` was already `'2026-09-20'` (max across platforms) — no change needed.

## KPI text / hh-grid / mks-grid / header labels
Checked for stale hardcoded figures (e.g. `3,326,267`, `59,719.97`, `5,857`) — none found outside
the arrays. Confirmed via source comments and prior reports that visible KPI labels are computed
at runtime from these arrays, not hardcoded.

## Date picker (STEP 3B)
Not touched — no new month was added (still ม.ค.–ก.ย., index 8).

## JS syntax check
`node --check` passed on all 3 inline `<script>` blocks in both files after editing.

## sw.js
Cache bumped: `wibwub-v1195` → **`wibwub-v1196`**.

## Git commit — ✅ completed this run
`.git/index.lock` blocked deletion the first few tries (sandbox can't `unlink()` files under
`.git/` on this Google-Drive-synced folder — same symptom as prior blocked runs), but a later
retry found the lock cleared and the commit went through:

```
f49a17e auto-update: sales from Sheets 2026-09-21 09:30 run2 — Shopee/Lazada extend 01-13->01-20/09,
        TikTok TK_AFI/TK_NET/TK_AFIPCT refined; sw.js bump
 4 files changed, 24 insertions(+), 24 deletions(-)
```

Note: the commit also swept in a 1-line change to `Data Shipnity/stock/stock_snapshot.json` that
another concurrent WIBWUB job had already staged in the shared index before this commit ran —
that's legitimate data from that other job, just bundled into this commit's message rather than
its own (a side effect of multiple scheduled jobs sharing one git index/working tree today).

## Push — ⚠️ blocked by sandbox proxy (expected)
`git push origin main` failed with `HTTP 403 from proxy` — this sandbox cannot reach GitHub
directly (documented, expected). Refreshed **`commit_and_push_sales_update.command`** in this
folder — double-click it on your Mac to push commit `f49a17e` (and it will no-op safely if
already pushed by another run).
