# WIBWUB Weekly Monday Update — 2026-06-29 (automated, no user present)

## Status: data updated & committed locally ✅ — push to GitHub PENDING ⚠️

## What was done
- **Step 1 — Shipnity**: Downloaded product-level purchase data (1 มิ.ย.–29 มิ.ย.) → `Data Shipnity/Data_มิถุนายน.xlsx` (23 MB).
- **Step 2 — Affiliate**: Downloaded TikTok Affiliate **Transaction Analysis** (1–27 มิ.ย., latest available) → `Data Affiliate/Transaction_Analysis_Creator_List_20260601-20260627.xlsx`.
- **Step 3 — Top Products (ภาพรวมธุรกิจ)**: Updated `ALL_PRODUCTS` (totals v/q) and `PROD_MO` (June column) for all 15 products in `WIBWUB_Mobile.html`; updated headline KPI in `WIBWUB_Dashboard.html` (Wool Duster → ฿5.16M · 8,065 ชิ้น).
- **Step 4 — Affiliate arrays**: June figures written consistently to both dashboards.
- **Step 5 — sw.js + commit**: Cache version bumped; data committed locally as `28af2b8`.

## Key June figures published
| Metric | Value |
|---|---|
| Top product (Wool Duster) total | ฿5,156,807 · 8,065 ชิ้น |
| Affiliate GMV (1–27 มิ.ย.) | ฿550,142 |
| Affiliate Net | ฿542,744 |
| Affiliate Commission | ฿68,304 |
| Affiliate Creators | 355 |

## Autonomous decisions (no user to confirm)
1. **Dashboard 9-channel platform breakdown chart NOT modified.** The stacked per-platform Top-Products chart/table in `WIBWUB_Dashboard.html` needs platform-split data that isn't in the Shipnity-only export. Only the headline KPI text was updated. Recompute that chart separately if needed.
2. **Affiliate data conflict detected & reconciled.** A parallel write (Drive-synced or concurrent run) had overwritten `WIBWUB_Mobile.html` affiliate lines and `sw.js` with alternative figures (GMV ฿553,845 / Net ฿545,656 / Comm ฿68,654, cache v259), leaving Mobile inconsistent with the Affiliate Dashboard (฿550,142). I **standardized everything on the verified 1–27 export figures (฿550,142…)** that trace directly to the file downloaded this session, so both dashboards now match. If a fresher (e.g. 1–28) affiliate pull is preferred, re-run with that range.

## ⚠️ Remaining manual step — PUBLISH
The push to GitHub could **not** be completed automatically:
- The sandbox has no network route to GitHub.
- `push_now.command` couldn't be auto-triggered (desktop-control approval requires a person, and none was present).
- The Google Drive filesystem also left an unremovable git lock that blocks further commits from the sandbox (it does **not** affect the user's native shell).

**To publish: double-click `push_now.command`.** It clears the locks, commits any remaining working-tree changes, and pushes. The correct data is already committed locally (`28af2b8`) and present in the dashboard files, so the live site will update on push.
