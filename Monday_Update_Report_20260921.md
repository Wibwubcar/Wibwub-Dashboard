# WIBWUB Monday Weekly Update — 2026-09-21

## ✅ Completed

- **Protection check**: M5 month arrays in WIBWUB_Dashboard.html / WIBWUB_Mobile.html already correct (9 months = ก.ย.), no fix needed.
- **Affiliate GMV/Net/Commission**: Refreshed using TikTok Affiliate Center "ผลการดำเนินงาน" Core Stats export (period 1–19 ก.ย. 2569, GMT+7):
  - GMV: 1,262,337 → **1,334,858**
  - Net (after refunds ฿93,918): 1,243,069 → **1,240,941**
  - Commission: 139,343 → **147,107**
  - Label updated: "ก.ย. (1-18)" → **"ก.ย. (1-19)"**
  - Updated in both `WIBWUB_Affiliate_Dashboard.html` (AF_MO/AF_GMV/AF_NET/AF_COM) and `WIBWUB_Mobile.html` (AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM), plus the hardcoded KPI card text in both files.
  - JS syntax verified with `node -e "new Function(...)"` on both files — no errors.
- **sw.js**: bumped wibwub-v1190 → **wibwub-v1191**.
- **Git**: committed as `39e3b5a` (files: WIBWUB_Affiliate_Dashboard.html, WIBWUB_Mobile.html, sw.js). `push_now.command` already present in the folder — run it to push to origin (sandbox network can't push directly).

## ⚠️ Skipped / Incomplete

- **AF_CR (creator count)**: left unchanged at 737. TikTok's new UI no longer offers a reliable one-click export of the full per-creator list within the sandbox session — two export attempts (via the "ครีเอเตอร์" table's own export button) got stuck/cancelled without producing a downloadable file. The Core Stats export doesn't include a "creators with GMV>0" total for a custom date range. Recommend a manual check next run.
- **Shipnity Top Products (ภาพรวมธุรกิจ)**: skipped this round. Today's fresh Shipnity export (1–21 ก.ย.) got stuck at 100% and was ultimately cancelled without downloading. I could have used yesterday's Data_20-09-2026.xlsx (covers 1–20 ก.ย.) instead, but several SKU codes (notably the two "Reflex Ceramic Coating" variants) can't be reliably mapped to the existing canonical product labels without risking mismatched data, so I chose not to overwrite ALL_PRODUCTS/PROD_MO this round rather than risk corrupting the dashboard.
- **Note on concurrent edits**: WIBWUB_Affiliate_Dashboard.html was being actively modified by another automation while this task ran (PRODUCTS/VIDEOS arrays changed independently of my edits). The committed diff includes both my Affiliate GMV changes and those concurrent changes; I verified my specific target values are correct and intact before committing.

## Action needed
Run `push_now.command` in the WIBWUB folder to push commit `39e3b5a` to origin.
