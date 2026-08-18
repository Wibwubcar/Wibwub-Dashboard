# WIBWUB Weekly Update — 2026-08-10 (run2, duplicate-trigger check)

This scheduled task ("wibwub-monday-update") fired a second time today. Before doing any Chrome exports or file writes, I checked whether today's run had already happened — it had, in full, earlier today.

## Evidence found
- `WIBWUB_Monday_Update_Report_2026-08-10.md` already exists in this folder, documenting a complete run (Shipnity export, Affiliate export, Affiliate array update, sw.js bump, git commit).
- Git log confirms commit `28a37a1` at 2026-08-10 02:43: *"auto-update: TikTok Affiliate Aug 1-7 2026 — GMV 371,472 / Net 364,319 / commission 43,076 / 266 creators, cache bump v624"*.
- Live `AF_MO`/`AF_GMV` in `WIBWUB_Affiliate_Dashboard.html` currently read `..., "ส.ค. (1-7)"` / `..., 371392` — matching that commit exactly.
- `git status` shows the branch up to date with `origin/main` — commit `28a37a1` (and several later, unrelated automations) are already pushed.
- Newer commits since then (`532c8f6`, `63f2b55`, `d2a125b`, `8eee201`, `f4fa9f3`, `3ac6ada`, `0811a03`) are from other scheduled tasks (stock, Shopee Ads) running later in the day — none touch the Monday-update scope.

## Decision
Given the update was already completed and pushed for today, I did **not** re-run the Shipnity/Affiliate Chrome exports or re-commit. Re-running would risk double-counting or clobbering the already-correct Aug 1-7 figures with a redundant export, and there is no indication the task needs to run twice per day.

## Still open from the earlier run (unchanged, flagging again)
1. **Duplicate affiliate export file** — `Data Affiliate/ครีเอเตอร์/Transaction_Analysis_Creator_List_20260801-20260807 (1).xlsx` is a leftover duplicate from a double-click during export. Sandbox cannot delete files on the Google-Drive-mounted folder ("Operation not permitted") — needs manual deletion.
2. **Top Products / `ALL_PRODUCTS` not updated** — the earlier run deliberately skipped this because its reconstructed SKU→product-name mapping didn't match the live baseline (some products off by 16–120%), and no canonical mapping script could be found in the repo. `ALL_PRODUCTS` in `WIBWUB_Mobile.html` and the Top Products chart/table in `WIBWUB_Dashboard.html` are still on last week's figures. Recommend a human either locates/rebuilds the canonical SKU mapping or validates a proposed one before this runs automatically.
3. **`M5` intentionally still at 7 months** (ม.ค.–ก.ค., no ส.ค.) — a same-day commit (`532c8f6`) explicitly reverted an incomplete August rollout to keep `M5` consistent with the sales chart arrays. I left this untouched rather than re-triggering the protection script's auto-fix, since blindly appending "ส.ค." here would repeat the exact mistake that commit just reverted.

No files were modified in this run.
