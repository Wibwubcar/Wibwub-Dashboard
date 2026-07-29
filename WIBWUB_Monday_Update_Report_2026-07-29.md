# WIBWUB Weekly Update — 29 กรกฎาคม 2569

Automated run of the `wibwub-monday-update` scheduled task (unattended, no live user this session).

## 1. M5 array protection check — ✅ already correct, no action needed

Verified `WIBWUB_Dashboard.html` / `WIBWUB_Mobile.html`: `M5` already had all 7 entries through July, no shrink/data-loss detected.

## 2. Shipnity Top Products / Sales data — ✅ done

- Downloaded a fresh export from Shipnity (date range 1–29 ก.ค. 2569, single-file xlsx) → `Data Shipnity/Data_29-07-2026.xlsx` (29,487 rows, confirmed date range 01/07–29/07/2026).
- `Data Shipnity/` has accumulated ~50 overlapping daily-snapshot exports across Jan–Jul (each snapshot is a cumulative month-to-date export, so same-month files are strict supersets of earlier same-month snapshots). Reprocessing all ~50 raw files (many 15–28MB) was impractically slow, so processing was restricted to one representative file per calendar month — verified by direct inspection that each selected file's internal date range cleanly and completely covers its month with no gaps or overlaps:
  - Jan → `Data_มกราคม.xlsx`, Feb → `Data_กุมภาพันธ์.xlsx`, Mar → `Data-มีนา.xlsx`, Apr → `Data_เมษา.xlsx`, May → `Data_พฤษภาคม.xlsx`, Jun → `Data_มิถุนายน.xlsx`, Jul → `Data_29-07-2026.xlsx` (this session's fresh export, most complete).
- Same column mapping, channel normalization, and `(order_id, product)` dedup logic as the canonical `wibwub_update.py` `process_shipnity()`.
- Result written to `Data Shipnity/Sales_Dashboard.html` (`const RAW`): 188 products, 31,889 product-day-channel lines, 1,324 order-day-channel groups, range **2026-01-01 → 2026-07-29**, total revenue **฿54,668,007** across **210,387** units.

## 3. TikTok Affiliate Transaction Analysis — ✅ done

- Downloaded Transaction Analysis Creator List export (custom range 01/07–27/07/2026, creator-list report) → `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260701-20260727.xlsx`.
- Processed all months' Creator_List files found under `Data Affiliate/` (best-overlap file picked per month, exact-header column matching, >10M outlier sanity guard) — same logic as `wibwub_update.py` `process_affiliate()`.
- 1,748 unique creators (GMV ≥ ฿1,000) across Mar–Jul. Jul (1–27) totals: GMV ฿1,329,672, Net ฿1,245,231, Commission ฿153,205 — consistent with the already-committed prior-run figures.
- Written to `WIBWUB_Affiliate_Dashboard.html` (`AF_MO`/`AF_GMV`/`AF_NET`/`AF_COM`/`AF_CR`, `CREATORS`, `CREATOR_MONTHS`) and `WIBWUB_Mobile.html` (`AFI_GMV`/`AFI_NET`/`AFI_COMM`). Also bumped the Affiliate iframe cache-bust in `WIBWUB_Dashboard.html`: `?v=282` → `?v=283`.

## 4. Cache version — ✅ done

`sw.js` bumped `wibwub-v492` → `wibwub-v493`.

## 5. Git commit — ✅ done, ⚠️ push needs manual trigger

- Staged and committed only the 5 intended files: `Data Shipnity/Sales_Dashboard.html`, `WIBWUB_Affiliate_Dashboard.html`, `WIBWUB_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js` — commit `9301dbd`, 752 insertions / 752 deletions. Left other unrelated in-progress/untracked files from concurrent automations untouched.
- Hit the same `.git/index.lock` contention seen in prior runs (this sandbox's mount of the Google-Drive-synced repo intermittently can't unlink freshly-created lock files for ~30–40s after creation) — resolved by removing the stale lock in an isolated step and retrying; committed successfully.
- **Did not push** (per task instructions — sandbox has no reliable path to push, and pushing must be a manual/human-triggered step). `push_now.command` already exists in the folder root; **run it** to push commit `9301dbd` (and any other pending local commits) to `origin/main`.

## Files changed (committed locally, not yet pushed)
- `Data Shipnity/Sales_Dashboard.html` — `RAW` (Shipnity lines/order_counts/products/channels, Jan 1–Jul 29)
- `WIBWUB_Affiliate_Dashboard.html` — `AF_MO`/`AF_GMV`/`AF_NET`/`AF_COM`/`AF_CR`, `CREATORS`, `CREATOR_MONTHS`
- `WIBWUB_Dashboard.html` — Affiliate iframe cache-bust `?v=282` → `?v=283`
- `WIBWUB_Mobile.html` — `AFI_GMV`/`AFI_NET`/`AFI_COMM`
- `sw.js` — cache version `v492` → `v493`
