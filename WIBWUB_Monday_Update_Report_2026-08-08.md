# WIBWUB Weekly Update — 2026-08-08 (automated run)

## Step 0 — M5 protection
Checked month-label arrays in WIBWUB_Dashboard.html and WIBWUB_Mobile.html. Already correct (7 elements). No fix needed.

## Step 1 — Shipnity export (BLOCKED)
Attempted all three export modes (แยกไฟล์, แยกเวิร์กชีต, ไฟล์เดียว) multiple times. Every attempt either produced an incomplete file or the browser connection dropped mid-download (confirmed via filesystem polling — no complete file landed). This far exceeds the "retry once" guidance, so I stopped rather than keep guessing. Only a partial file remains (`Data Shipnity/Data-Page-1_08-08-2026.xlsx`, ~500 of an estimated 4,000+ rows) — **not used** for any dashboard update.

## Step 2 — TikTok Affiliate export (SUCCESS)
Initial attempt hit the wrong page (old "ครีเอเตอร์" analysis view → `Core_Stats_*.xlsx`, a known-bad format per existing `_WRONG_FORMAT_ignore_` files in the folder). Corrected to the new "ผลการดำเนินงาน" → รายละเอียด → ครีเอเตอร์ export, which produces the correct `Transaction_Analysis_Creator_List_*.xlsx` format.

Downloaded: `Transaction_Analysis_Creator_List_20260801-20260806.xlsx` (Aug 1–6, 2026 — TikTok's own data lag means Aug 7–8 aren't selectable yet). Auto-moved to `Data Affiliate/ครีเอเตอร์/`.

## Step 3 — Top Products (SKIPPED)
Skipped this run because Shipnity data (Step 1) was incomplete — recomputing Top 15 from partial data risked showing wrong numbers. `ALL_PRODUCTS` left untouched.

## Step 4 — Affiliate arrays (UPDATED)
Parsed the Aug 1–6 Transaction Analysis file (4,186 creator rows; GMV col, Returns col, Commission col identified by header, not fixed index — the file's actual column layout differs from the original 12-column spec, so column matching was done by header text instead of position). Totals:

| Metric | Value |
|---|---|
| GMV | 312,344 |
| Returns | 5,597 |
| Net (GMV − Returns) | 306,748 |
| Commission | 36,260 |
| Active creators (GMV > 0) | 240 |

Commission-to-GMV ratio (11.6%) matches the prior "ส.ค. (1-5)" entry exactly, confirming the column mapping is correct.

Applied the rolling-window rule: since the existing last index was "ส.ค. (1-5)" (same month), it was **overwritten** (not appended) with the Aug 1–6 totals, in both:
- `WIBWUB_Affiliate_Dashboard.html` (AF_MO/AF_GMV/AF_NET/AF_COM/AF_CR)
- `WIBWUB_Mobile.html` (AFI_MONTHS/AFI_GMV/AFI_NET/AFI_COMM)

No earlier months were touched.

## Step 5 — Cache bump + commit
- `sw.js`: `wibwub-v609` → `wibwub-v610`
- Committed (hash `645fa42`): `WIBWUB_Affiliate_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js`
- The sandbox cannot push directly (proxy returns HTTP 403). **Double-click `push_now.command` in the folder to push this commit.**

## Not touched this run
Shopee/Shipnity stock and Top Products data — blocked by Step 1's export failure, left as-is rather than guessed.
