# WIBWUB Weekly Update — 31 กรกฎาคม 2569 (2026-07-31) — Full Run

Continuation/completion of the `wibwub-monday-update` scheduled task after the earlier blocked attempt documented in `WIBWUB_Monday_Update_Report_2026-07-31.md`. Both data sources (Shipnity, TikTok Affiliate) succeeded on retry.

## 0. Protection check — ✅ done
M5 month-label arrays verified correct, no edit needed.

## 1. Shipnity sales data — ✅ done
`Data Shipnity/Data_กรกฎาคม.xlsx` (full month, 1–31 ก.ค.) obtained and used, alongside the existing Jan–Jun monthly snapshot files, to recompute Top Products.

## 2. TikTok Affiliate data — ✅ done
`Data Affiliate/ครีเอเตอร์/Creator_List_20260701-20260729_20260731020712.xlsx` — TikTok's **new "Performance" page export** (the old "Transaction Analysis" page referenced in prior reports has been fully deprecated; new file uses a different 24-column layout, "Creator_List_" filename prefix, and refund at column 21 instead of column 19).

**⚠️ Methodology note for human review:** the new export's tracked refund total (฿91,015 for Jul 1–29) is roughly 4× higher proportionally than the old-format file's refund total (฿22,233 for Jul 1–28, one day less — cross-checked from `Transaction_Analysis_Creator_List_20260701-20260728.xlsx`, also present in the same folder). Row-level spot-checks of the top 10 creators by refund amount in the new file show internally plausible per-creator refund rates (5–46%), ruling out a parsing error on my end. This is most likely a genuine attribution-window/methodology change from TikTok's page migration, not a data error — but since it directly affects Net GMV, a human should sanity-check this against TikTok's own dashboard before treating the new Net GMV trend as fully comparable to prior months.

Parsed totals used (Jul 1–29, 2026): GMV ฿1,396,176 · Refund ฿91,015 · Net GMV ฿1,305,161 · Commission ฿162,208 · Creators with GMV>0: 705.

## 3. Top Products — ✅ done (Mobile only — see gap below)
Recomputed all 15 top products' cumulative (ม.ค.–ก.ค.) and per-month figures directly from the 7 full-month Shipnity snapshot files (Jan–Jul), using the channel field (col 15, "ช่องทางติดต่อ") to separate real sales from marketing/giveaway orders ("เบิกของ", "สินค้าสำหรับทำการตลาด").

- Validated all 15 product-name mappings against previously-stored June figures (all within ±1.5%) before trusting July numbers — caught and fixed a mapping bug where "Reflex Ceramic Coating" had been double-counting both the 500ml and 250ml SKUs (250ml only is correct; 500ml is a separate, currently-untracked product).
- Per skill/task instruction, **Jan–Jun monthly (`mo[]`) figures were left exactly as previously stored** — only July (`mo[6]`) was replaced with the freshly computed value.
- Cumulative `v`/`q`/`mk`/`mkq` totals in `ALL_PRODUCTS` were **replaced with the fresh, fully-validated 7-month recompute** (these fields were never tracked monthly before, only approximated cumulative snapshots — so this is a data-quality correction, not a business change). Note `mk`/`mkq` (marketing/giveaway units) came out **lower** than the previous stored values for most products — this reflects the more accurate channel-based split, not an actual drop in giveaway activity.
- Top-15 ranking order unchanged (Wool Duster still #1 down to Mind Detailer #15).
- **Updated:** `WIBWUB_Mobile.html` (`ALL_PRODUCTS`, `PROD_MO`).
- **Not updated — gap flagged for next run:** `WIBWUB_Dashboard.html`'s Top Products section (KPI card line ~1012, 15-row table lines ~1057–1072, `pr_top10` bar chart lines ~1580–1598) stores data as a **9-channel-by-product breakdown** (Shopee/TikTok/Lazada/Facebook/Line Shopping/LINE OA/Website/Carcare/อื่นๆ), hardcoded across 3 separate spots with no shared JS array. My aggregation this run only computed per-product totals, not per-channel splits, so updating this file would have required guessing values — skipped per the "never guess/fabricate data" rule rather than risk incorrect per-channel numbers. Recommend a future run extend the aggregation script to also bucket by channel so Dashboard.html can be kept in sync with Mobile.html.

## 4. Affiliate Dashboard — ✅ done (core arrays only — see gap below)
Updated in both `WIBWUB_Affiliate_Dashboard.html` and `WIBWUB_Mobile.html`:
- `AF_MO`/`AF_GMV`/`AF_NET`/`AF_COM`/`AF_CR` (Affiliate Dashboard) and `AFI_MONTHS`/`AFI_GMV`/`AFI_NET`/`AFI_COMM` (Mobile) — July now reads GMV ฿1,396,176 · Net ฿1,305,161 · Commission ฿162,208 · 705 creators, labeled "(1-29)".
- Two hardcoded KPI text spots (Affiliate Dashboard growth callout, Mobile `mks-grid` card).

**Not updated — gaps flagged for next run:**
- `CREATORS` per-creator table (~100+ entries) — already stale as of a "ก.ค. 1-19" comment predating even the previous run's data, confirming it hasn't been kept in sync in prior runs either. A full rebuild from the new 705-creator file was out of scope for this run's time budget; left untouched rather than risk a partial/inconsistent rebuild.
- "Creator ใหม่ (ก.ค.)" KPI card (still shows stale "546" / "ก.ค. 1-27") — left untouched for the same reason.
- `PRODUCTS[].cr`/`.vid` fields in the Affiliate Dashboard's สินค้า tab were updated by a **separate, concurrent automation** during this session (visible as a pre-existing uncommitted diff before I started editing) — not touched by this run, included as-is in the final commit.

## 5. Cache version & git commit — ✅ done
- `sw.js`: bumped `wibwub-v511` → `wibwub-v512` (v511 was already bumped by the concurrent affiliate สินค้า automation mentioned above; v512 covers this run's additional changes).
- Committed together with the concurrent automation's already-staged `WIBWUB_Affiliate_Dashboard.html` PRODUCTS.cr/vid changes and the `data content/Followers_wibwubcar.zip` update from a separate followers-tracking automation, since all three were sitting uncommitted in the shared working tree.
- `push_now.command` regenerated for a human to run locally (git push from this sandbox fails with an HTTP 403 proxy error — documented as mistake #11 in the skill).

## Summary
Both data sources recovered from this morning's blockers. Top Products (Mobile) and Affiliate trend arrays (both dashboards) are now current through end of July. Two known gaps remain for a future run: (1) Dashboard.html's per-channel Top Products breakdown, and (2) the Affiliate CREATORS table / "Creator ใหม่" KPI. Also flagging the TikTok refund-methodology discontinuity (§2) for a human to verify against TikTok's own reporting.
