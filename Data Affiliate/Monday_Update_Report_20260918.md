# WIBWUB Weekly Monday Update — 2026-09-18

## Status: PARTIAL — Top Products updated, Affiliate BLOCKED

## 1. Shipnity export (already done before this run)
- `Data Shipnity/Data_กันยายน.xlsx` (= `Data_18-09-2026.xlsx`) confirmed product-level, 23,253 rows, dates 2026-09-01 → 2026-09-18 (day 18 only partial, pulled ~02:55, 223 order lines / ฿60,609).

## 2. Top Products — updated in both files
Files: `WIBWUB_Mobile.html` (`ALL_PRODUCTS`, `PROD_MO`, `PROD_MO_LBL`), `WIBWUB_Dashboard.html` (Top-15 table `รวม`/`จำนวน` columns, KPI row, subtitle dates).

**Method / judgment call:** I could NOT safely reverse-engineer the exact historical product-grouping methodology from raw monthly Shipnity files. Testing a straightforward code-based grouping (product code, e.g. `SSUG010024`=Sugar 500ml) against the already-trusted Aug-2026 figures showed a systematic ~10% gap I could not explain from the exported columns (probably return/cancellation handling not visible in this export). Recomputing full Jan–Aug from scratch risked corrupting validated numbers, so I did NOT touch Jan–Aug.

Instead I validated the same code-based grouping against the previous run's Sep(1-17) figures — gap was only ~0.2–4.8% (small, expected MTD noise) — so I trusted it for an incremental delta: computed revenue/qty for **Sep 18 only** (per product, price>0 filter, deduped on order#+code+qty) and added that delta on top of the existing Sep(1-17)/cumulative numbers. This keeps 8 months of trusted history untouched and only extends the most recent day using a validated-consistent method.

Net effect: all 15 products' totals nudged up slightly (day-18 was only a few hours of data, ~฿60.6K company-wide); ranking order unchanged. Dashboard's per-channel breakdown (Shopee/TikTok/etc. columns, `pr_top10`/`pr_channel` charts) was left untouched/stale (frozen at ~11 Sep), consistent with the prior Monday run's own documented convention.

`mk`/`mkq` (marketing giveaway) fields carried over unchanged, also per established convention.

KPI updates: ยอดขายรวม ฿72.19M→฿72.25M, best seller Sugar ฿6.44M/20,888→฿6.45M/20,911, date labels 17→18 ก.ย. throughout the products section.

## 3. sw.js
Bumped `wibwub-v1158` → `wibwub-v1159` (+1, since Mobile/Dashboard changed). Note: v1158 already reflected a prior concurrent session's unrelated affiliate-array edit that was pre-staged when I started.

## 4. push_now.command
Found already at `All/push_now.command` (not on a Desktop mount — no `/sessions/.../mnt/Desktop/` exists in this sandbox, so the Desktop-specific step from the instructions was skipped as directed). Refreshed its header comment/date and simplified it to a plain `git push origin main` (removed a stale hardcoded `git add`/`commit` line referencing yesterday's affiliate message, since add/commit is already handled per-run).

## 5. Git
- Committed as `a3710b8` on `main`: "auto-update: Monday 2026-09-18 — Shipnity Top Products refresh (Mobile ALL_PRODUCTS/PROD_MO + Dashboard top-products table, ม.ค.–18 ก.ย. 2569); sw.js v1159; refresh push_now.command" — 5 files changed.
- **Anomaly to flag:** `git status` showed heavy concurrent activity in this shared repo (many report `.md` files from other runs today, repeated `.git/index.lock` contention from what appears to be a live concurrent process). `WIBWUB_Affiliate_Dashboard.html` had pre-existing **staged** changes (small AFI_GMV/NET/COMM corrections, not authored by me, not touched by me) already sitting in the git index before I started. Since I only `git add`ed my own 4 files and then ran `git commit`, that pre-staged Affiliate file was swept into my commit as a side effect of shared index state — not something I edited or reviewed. Flagging for visibility; no action taken on affiliate content per scope rules.
- Did NOT `git push` (per rules — proxy blocks it). User/local push script must run `push_now.command`.
- `Data_กันยายน.xlsx` is `.gitignore`'d (`*.xlsx`), same as all other raw Shipnity exports — not added to git, by design.

## 6. BLOCKED — TikTok Affiliate Transaction Analysis
Not touched this run (out of scope + blocked): TikTok's export API returned persistent 503s, and the Chrome extension connection was fully lost mid-task ("No tab group exists for this session") — unrecoverable without the user reconnecting Chrome. As a result, affiliate GMV/Net/Commission arrays in `WIBWUB_Affiliate_Dashboard.html` and `WIBWUB_Mobile.html` (`AF_MO`/`AF_GMV`/`AF_NET`/`AF_COM`/`AF_CR`, `AFI_MONTHS`/`AFI_GMV`/`AFI_NET`/`AFI_COMM`) were **not** updated by me this run. Most recent affiliate data on file covers only through ~Sep 14–16, 2026 (per existing/pre-staged values).

## Files touched
- `WIBWUB_Mobile.html`
- `WIBWUB_Dashboard.html`
- `sw.js`
- `push_now.command`
