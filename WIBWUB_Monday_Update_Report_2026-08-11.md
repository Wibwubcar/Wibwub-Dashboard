# WIBWUB Weekly Update — 2026-08-11

Automated run of "wibwub-monday-update." Two of the four data-dependent steps hit hard blockers this run; no dashboard files were edited.

## Task 1 — M5 protection check
Verified `M5` month-label array in `WIBWUB_Dashboard.html` and `WIBWUB_Mobile.html`. Length correct (8 Thai months through August). No fix needed.

## Task 2 — Shipnity purchase export (BLOCKED, partial data only)
Set date range to Aug 1–11, exported via Shipnity's UI (default split mode, 500 rows/file, 7 pages). All 7 pages showed "Download completed" in Shipnity's own UI, but only page 1 (`Data-Page-1_11-08-2026.xlsx`, 501 rows) actually landed in `Data Shipnity/` — pages 2–7 vanished (not in Downloads, not as partial/.crdownload files, not after 40s+ waits). Reproduced twice. Also tried: single consolidated-file export (hung indefinitely at 100%, never completed — likely a Shipnity server-side issue), raising the 500-row-per-file slider (unresponsive to clicks), and chunking to a 2-day range (still produced 3 files, same multi-file loss).

**Likely root cause:** the local Downloads-folder file-mover (`com.wibwub.download-mover` LaunchAgent) appears to only reliably relocate one file when several downloads land in a short window; the rest are lost before ever reaching Google Drive or Downloads. This is outside what Chrome automation can fix.

**Result:** only the most recent ~500 order line items (page 1) are available, not the full Aug 1–11 dataset.

## Task 3 — TikTok Affiliate export (BLOCKED — not authenticated)
`affiliate.tiktok.com` and `seller.tiktok.com` redirected to the public marketing homepage. `seller-th.tiktok.com` redirected to an explicit login page requiring phone number + password. No valid logged-in session was found in the browser profile. Per policy, I never enter credentials — this needs a manual login by you before this step can run.

## Tasks 4–5 — Top Products / Affiliate arrays: skipped
Both were skipped rather than run on bad data:
- Top Products needs the full Shipnity order set; only ~500 of the most recent rows are available, which would skew rankings.
- Affiliate arrays need the TikTok export, which never happened.

No edits were made to `ALL_PRODUCTS`, the Top Products chart/table, or any `AF_*`/`AFI_*` arrays.

## Task 6 — Cache bump / commit: skipped
Nothing new to commit since no dashboard data changed. Note: `sw.js` is already at `wibwub-v634` from a separate same-day "Sales from Sheets" automation — unrelated to this task. Git also shows uncommitted changes from other concurrent scheduled tasks (Shopee zip exports, `push_now.command`, `auto_push.log`); left untouched to avoid interfering with those.

## What's needed to unblock next run
1. Someone should check the download-mover script/LaunchAgent — it's losing files when multiple downloads fire close together (confirmed across 4 separate attempts today).
2. Log into TikTok Seller Center (`seller-th.tiktok.com`) in the browser profile used by this automation, so future runs have a valid session.

No files were modified in this run other than this report and the single Shipnity page already retained in `Data Shipnity/`.
