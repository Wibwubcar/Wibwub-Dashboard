# WIBWUB Weekly Update — 2026-07-29 (21:51 ICT run)

Scheduled task: wibwub-monday-update. Ran unattended; no dashboard files ended up changed this cycle. Summary below with reasoning for each step.

## STEP 1 — M5 / month-array protection check
`WIBWUB_Dashboard.html` and `WIBWUB_Mobile.html` both already had 7 entries in `M5` (matching the current month, July). No corruption found, no fix needed.

## STEP 2 — Shipnity purchase/order export
Export attempted via Chrome automation. The newly-triggered download did not appear promptly in the Downloads folder, so the run initially fell back to the existing `Data Shipnity/Data_29-07-2026.xlsx` (28.4MB, 29,959 line items) — which, on closer check, turned out to already be a same-day file newer than the one used in this morning's earlier commit (`9301dbd`, 03:28 UTC). So today's dataset is in hand, just not freshly re-verified against a brand-new export.

## STEP 3 — TikTok Affiliate Transaction Analysis export
Set the table's custom date range to 01/07/2026–28/07/2026 and clicked "ส่งออก". The export request completed successfully and appeared in the reports panel (รายงานที่ส่งออก). However, **every download attempt (5 retries across ~3 minutes) returned HTTP 503** from TikTok's own API:
```
GET .../export_task/export?...task_id=01KYQ53RFT4T843CQCR3KVJ2R8v2 → 503
GET .../export_task/export?...task_id=01KYNX5F2WFWXR703W15MFB1K6v2 → 503
```
Confirmed via network request inspection (not a Downloads-folder sync issue this time — the API call itself is failing). This looks like a transient TikTok-side outage on the export/download endpoint. **No new creator-list file was obtained this run.**

## STEP 4 — Top Products (ALL_PRODUCTS / PROD_MO)
Current data in `WIBWUB_Mobile.html` is already through **Jul 28** (one day stale) per the in-file comment. I did not recompute this array this cycle: there's no verified script in the repo that maps the raw Shipnity line-item export to `ALL_PRODUCTS`/`PROD_MO` (the existing `wibwub_update.py` only builds the separate Sales_Dashboard view, and git history shows the last commit touching Shipnity "product data" was actually just a tie-break reorder of affiliate creator rows, not a real ALL_PRODUCTS recompute). Hand-rolling the marketing-giveaway exclusion / SKU-to-name logic from scratch risked posting wrong revenue numbers to a live dashboard, so I left it untouched rather than guess.

## STEP 5 — Affiliate GMV/Net/Commission/Creator arrays
Blocked by the same TikTok 503 outage as Step 3 — no fresher data available. Confirmed via `git log` that `AF_MO/AF_GMV/AF_NET/AF_COM` (Affiliate Dashboard) and `AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM` (Mobile) already reflect data through **Jul 27**, committed earlier today at 03:28 UTC (`9301dbd`). That's the most recent period anyone has successfully processed. No changes made; no historical months touched.

## STEP 6 — sw.js version bump / git commit
No dashboard HTML/JS files changed this run (see Steps 4–5), so per the instructions ("bump whenever dashboard HTML changes") there's nothing to bump or commit. `sw.js` stays at `wibwub-v496`. `git status` shows only pre-existing, unrelated local changes (`push_now.command`, a Followers zip) left over from an earlier session — not touched, not part of this cycle.

## Bottom line
No production dashboard files were modified this run. The two real blockers were: (1) TikTok's affiliate export-download API returning 503 consistently, and (2) no safe, verified way to recompute Top Products from the raw Shipnity export without risking bad numbers on a live dashboard. Both are documented above for whoever picks this up next — worth a manual retry on the TikTok export later today, and worth writing/vetting a proper ALL_PRODUCTS-from-Shipnity script before automating that step further.
