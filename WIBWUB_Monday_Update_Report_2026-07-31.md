# WIBWUB Weekly Update — 31 กรกฎาคม 2569 (2026-07-31)

Automated run of the `wibwub-monday-update` scheduled task. Note: an earlier attempt of this same task on 31/7 hit blockers on both data sources (download-permission block on Shipnity, expired TikTok login) and made zero edits — see the superseded version of this note. This later run retried after those conditions cleared and **succeeded** on both data sources; the summary below reflects the final, committed state.

## 0. M5 protection check — ✅ done
Thai month-array length already matched current month (7) in both `WIBWUB_Dashboard.html` and `WIBWUB_Mobile.html`. No fix needed.

## 1. Shipnity sales data — ✅ done
- July export (`Data_กรกฎาคม.xlsx`, product-level, Jul 1–31) obtained and placed in `Data Shipnity/`.
- Aggregated **all 59** product-level Shipnity files on disk (Jan–Jul, cumulative, deduped on `(order#, product code, qty)`) via a checkpointed script (openpyxl processing exceeded the single bash call's time budget, so it ran across 3 resumable passes with a pickle checkpoint).
- Updated Top 15 by revenue in `ALL_PRODUCTS` and `PROD_MO` (July index only — Jan–Jun left untouched) in `WIBWUB_Mobile.html`, and the KPI cards, table rows (รวม(฿)/จำนวน columns only), grand-total row, and "last updated" date in `WIBWUB_Dashboard.html`.
- New grand total: ฿55.84M / 216,264 pcs (was ฿54.64M / 212,160). Top product Wool Duster: ฿5.57M / 8,724 pcs.
- Per-channel breakdown columns and the `pr_top10`/`pr_channel` chart canvases were **not** touched — no channel-level source data was recomputed this run (same limitation as prior runs).

## 2. TikTok Affiliate data — ✅ done
- Exported/downloaded `Transaction_Analysis_Creator_List_20260701-20260730.xlsx` (Jul 1–30, latest settled range; the 31st wasn't yet available) from the **Transaction Analysis** page (confirmed correct source, not Creator List page).
- **Format drift note**: the export is now **22 columns**, not the 12 columns documented in the task's SKILL.md. Mapped fields by header name instead of trusting the stale positional indices: `GMV จากครีเอเตอร์` (GMV), `การคืนเงิน` (returns), `ค่าคอมมิชชั่นโดยประมาณ` (commission, last column). Computed GMV matched the previously-committed value exactly (฿1,424,548), confirming this mapping is consistent with how the last successful run computed it.
- Computed: GMV ฿1,424,548 (unchanged) · NET ฿1,400,643 (was ฿1,330,017 — more returns settled since) · Commission ฿166,130 (was ฿165,964) · Creators 716.
- **Flagged and corrected a data anomaly**: the previously-committed creator count for July was 17,493 — inconsistent with every other month (398–558 range), almost certainly a column-mapping bug from an earlier run. Recomputed as 716 (count of creators with GMV > 0), consistent with the historical pattern.
- Updated in place at the existing last index (label unchanged: "ก.ค. (1-30)" / "กค.69 (1-30)") — no new month appended, no historical months touched: `AF_GMV/AF_NET/AF_COM/AF_CR` in `WIBWUB_Affiliate_Dashboard.html`, `AFI_GMV/AFI_NET/AFI_COMM` in `WIBWUB_Mobile.html`.

## 3. Cache version — ✅ done
`sw.js` bumped `wibwub-v519` → `wibwub-v520`.

## 4. Git commit — ✅ done
- Minor lock-file contention (`.git/objects/*/tmp_obj_*`, `.git/index.lock`) from concurrent automations; git recovered on its own and the commit succeeded.
- `81584d2 — auto-update: Monday 2026-07-31 — Shipnity + Affiliate + ภาพรวมธุรกิจ` (4 files changed: `WIBWUB_Mobile.html`, `WIBWUB_Dashboard.html`, `WIBWUB_Affiliate_Dashboard.html`, `sw.js`).
- `push_now.command` regenerated (executable) — push was not executed from the sandbox (blocked by proxy); run the script locally to push.

## Files changed (committed)
- `WIBWUB_Mobile.html` — `ALL_PRODUCTS`, `PROD_MO` (Jul), `AFI_GMV/NET/COMM` (Jul)
- `WIBWUB_Dashboard.html` — Top Products KPI card, table, footnote
- `WIBWUB_Affiliate_Dashboard.html` — `AF_GMV/NET/COM/CR` (Jul)
- `sw.js` — cache version v519 → v520

## Open items for next run
- Per-channel product breakdown and Top Products chart canvases remain unverified/stale — needs a dedicated data source not produced by this run's aggregation script.
- A pre-existing mismatched-header table in `WIBWUB_Dashboard.html`'s overview section (~line 597) — labeled as an order list but showing product-revenue data — noticed but out of scope for this run; flagging for review.
- TikTok's Transaction Analysis export format changed from 12 to 22 columns since the task instructions were written — the instructions' hardcoded column indices are now stale; this run used header-name matching instead. Worth updating the SKILL.md to avoid relying on positional indices going forward.
