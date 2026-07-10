# WIBWUB Weekly Update — Friday 26 Jun 2026

## Status: data updated & verified ✅ — push pending one manual step ⚠️

### What was updated
**Top Products (Shipnity ม.ค.–มิ.ย. 2569, cumulative through Jun 26)**
- `WIBWUB_Mobile.html` — `ALL_PRODUCTS` (15 SKUs, v/q) and `PROD_MO` (June column) refreshed.
- `WIBWUB_Dashboard.html` — KPI row, Top-10 stacked chart, channel doughnut, and full 15-row channel table regenerated.
- Best-seller: Wool Duster ฿5.12M · 8,011 ชิ้น. Grand total ฿46.1M · 173,224 ชิ้น (was ฿44.7M / 168K).
- Top channel: Shopee 59% · Facebook 16% · TikTok 16%.

**Affiliate (TikTok Transaction Analysis, Jun 1–23)**
- GMV ฿436,626 · Net ฿429,316 · Commission ฿54,274 · 308 creators (GMV>0).
- `WIBWUB_Mobile.html` `AFI_GMV/AFI_NET/AFI_COMM` (index 7 = มิย.69) updated.
- `WIBWUB_Affiliate_Dashboard.html` was already current (AF_GMV/NET/COM/CR last element matched) — no edit needed.

**Service worker**
- `sw.js` cache bumped `wibwub-v245` → `wibwub-v246`.

### Decisions made autonomously (unattended run)
- The TikTok affiliate export downloaded today (114701) was usable once parsed — values are ฿-formatted strings, not numbers; aggregation handles this. Figures match the prior same-day export, so data is stable for Jun 1–23 (TikTok lags ~2–3 days, so Jun 24–26 not yet final).
- Dashboard was previously "current to display precision" only — several rows had drifted enough to change the rounded display (e.g. Sugar 500ml ฿3.76M→฿3.78M, Xglass ฿964K→฿974K, all qty columns), so I regenerated the whole table/charts.
- Updated `push_now.command`: added `WIBWUB_Dashboard.html` to the staged files (the old script omitted it) and refreshed the commit message.

### ⚠️ Action required from you
The git commit + push could **not** run automatically:
- A stale `.git/index.lock` (dated Jun 23) blocks git, and the sandbox can't delete it.
- Screen-access approval for Finder timed out (nobody present to approve).

**`push_now.command` already handles the lock** (line 3 removes it). Just double-click **push_now.command** to commit and push. It will stage Affiliate_Dashboard, Mobile, Dashboard, and sw.js, then push to origin/main.

### Files changed
- WIBWUB_Mobile.html
- WIBWUB_Dashboard.html
- sw.js
- push_now.command (staging list + commit message)
