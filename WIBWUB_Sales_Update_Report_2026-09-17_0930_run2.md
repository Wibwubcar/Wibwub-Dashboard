# WIBWUB Sales Update Report — 2026-09-17 (run 2)

## Result: TikTok updated · Shopee/Lazada unchanged

The 09:30 run found no new data. Re-checking later found TikTok's sheet has new September
entries; Shopee and Lazada are still at 01-13/09/26 (no change since the last sync).

| Platform | Latest sheet row | Status |
|---|---|---|
| Shopee | 01-13/09/26 | No new data — skipped (unchanged from prior sync) |
| Lazada | 01-13/09/26 | No new data — skipped (unchanged from prior sync) |
| TikTok | 01-16/09/26 (partial) | **Updated** — see reconciliation note below |

### TikTok reconciliation (judgment call — noted per autonomous-run instructions)

The TikTok "ยอดรายเดือน" sheet has two candidate September rows:
- **01-16/09/26**: REV / ADS / FEE / AFI / NET / ADSSPEND are populated (most current), but
  ORDER_COUNT, CANCELLED %, LIVE, NEW, OLD are blank for that row.
- **01-13/09/26**: all fields are populated, including ORDER_COUNT / CANCELLED % / LIVE / NEW / OLD.

Column mapping was empirically validated against known-correct July/August dashboard values
(index 5=REV, 6=ADS, 8=ADSSPEND, 10=FEECOMM, 12=LIVE, 15=NEW, 16=OLD, 17=ORDER_COUNT,
19=CANCELLED_PCT, 1=AFI, 3=NET) before extracting any numbers.

**Decision**: updated each field from the most recent row where that field is actually
populated — REV/ADS/FEE/AFI/NET/ADSSPEND from 01-16, and ORDER_COUNT/CANCELLED_PCT/LIVE/NEW/OLD
from 01-13 (Dashboard only; Mobile doesn't track LIVE/NEW/OLD/AFIPCT). TK_AFIPCT was
**recomputed** as AFI/REV from the same (01-16) row rather than carried over from 01-13, since
mixing an AFIPCT from one row with REV/AFI from another would be inconsistent.

`MTD_COVERAGE` (Dashboard) / `SALES_ASOF` (Mobile) were left at **2026-09-13** — the date
through which *all* TikTok fields are complete — rather than 09-16, to avoid the coverage label
overstating completeness of order/cancellation data. This is a judgment call; flagging it here
in case the intended convention is "most recent date with any data."

### Values applied (September / index 8)

| Field | Old | New | Source row |
|---|---|---|---|
| TK_REV | 1,424,369.56 | **1,757,913.04** | 01-16 |
| TK_ADSSPEND | 262,257 | **465,382.31** | 01-16 |
| TK_FEECOMM | 295,873 | **510,876.58** | 01-16 |
| TK_AFI | 526,014 | **1,055,400.72** | 01-16 |
| TK_NET | 517,038 | **1,039,624.10** | 01-16 |
| TK_ADS | 1,044,345 | **1,771,249.56** | 01-16 |
| TK_AFIPCT | 50.6% | **60.0%** | recomputed (AFI/REV, 01-16) |
| TK_ORD | 2,570 | **6,041** | 01-13 |
| TK_CANCEL_PCT | 6.26% | **6.64%** | 01-13 |
| TK_LIVE | 58,600 | **180,200** | 01-13 |
| TK_NEW | 1,676 | **4,408** | 01-13 |
| TK_OLD | 267 | **722** | 01-13 |

Applied as targeted single-index (`[8]`) edits in both `WIBWUB_Dashboard.html` and
`WIBWUB_Mobile.html` — no array was rebuilt, so all 8 prior months are untouched. All arrays
confirmed to still have 9 elements (Jan–Sep), matching `M5`.

Shopee (`SH_*`) and Lazada (`LZ_*`) arrays: **no changes** — confirmed unchanged since the
09:30 run.

### Hardcoded text / date picker
No hardcoded KPI text or date-picker consts needed updates. Header ranges, `rng-lbl`,
`kc-lbl`/`kc-val` totals, and the MTD coverage footnote all derive from `M5` / `TOTAL_REV` /
`MTD_COVERAGE` / `SALES_ASOF` dynamically (per the `wibwub-avoid-stale-hardcoded-labels`
convention already in place) — nothing to hand-edit. September was already the last month in
`M5`/`rangeEnd` from a prior run, so no new month/date-picker bounds were needed.

Note: the Mobile file's `CHANNELS` array (lifetime/all-time cumulative revenue per channel,
lines ~866–873) is a separate, static summary block unrelated to the monthly `ยอดขาย` arrays —
left untouched as out of scope for this sync.

### sw.js / git
- Bumped cache version: `wibwub-v1148` → `wibwub-v1149`.
- Attempted `git commit` directly from the sandbox for `WIBWUB_Dashboard.html`,
  `WIBWUB_Mobile.html`, `sw.js` — blocked by a stuck `.git/index.lock` that the sandbox cannot
  remove (`Operation not permitted`, likely a Google Drive sync artifact or contention with
  another concurrent scheduled task on this shared repo).
- Updated **`commit_and_push_sales_update.command`** in this folder with today's commit message
  and the correct 3 files. Double-click it on your Mac to clear the lock, commit, and push.

**Files modified this run**: `WIBWUB_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js`,
`commit_and_push_sales_update.command`.
