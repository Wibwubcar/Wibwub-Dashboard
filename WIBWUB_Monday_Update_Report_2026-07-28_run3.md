# WIBWUB Weekly Update — 28 กรกฎาคม 2569 (continuation run)

Automated continuation of the `wibwub-monday-update` scheduled task. This picks up after an earlier run today got Shipnity Top Products committed but left the Affiliate step blocked by a TikTok 503 outage.

## 1. Shipnity sales data — ✅ already up to date, no action needed

Checked `WIBWUB_Dashboard.html` / `WIBWUB_Mobile.html`: Top Products totals (฿54.64M / 212,160 pcs, through 28 ก.ค.) were already committed and pushed by an earlier automation run today (commit `41e8a21`/`6e13d63`). No re-download or recompute needed this run.

## 2. TikTok Affiliate data — ✅ done (via legacy "ครีเอเตอร์" page, Core_Stats export)

- The old `transaction-analysis` URL now hard-redirects to a new **"ผลการดำเนินงาน" (Performance)** page — the deprecation flagged in earlier reports has completed for that specific URL.
- The legacy **"ครีเอเตอร์" (Creator)** page under การวิเคราะห์ is still live and still exports successfully. Set date range to 01/07–27/07/2026 and found a same-day queued export (`Core_Stats_20260701-20260727_...`, generated 08:57 this morning) already sitting in the reports panel — downloaded it directly, no new export/wait needed.
- **Format note:** this export is a single-row shop-wide summary (GMV, LIVE GMV, video GMV, product-card GMV, units sold, commission, refund GMV, etc.) — not the old 12-column per-creator `Transaction_Analysis_Creator_List` file. It does not include a per-creator row count, so **`AF_CR`/creator-count was left unchanged** (688) — no reliable source for it this run.
- Computed: GMV ฿1,329,841.65, refund GMV ฿84,532.12 → **Net = ฿1,245,309.53**, commission ฿153,498.56.
- These numbers are very close to (slightly higher than, as expected for fresher same-day data) the already-committed Jul(1-27) figures — confirms this file is measuring the same thing the prior methodology used, just via a different report name post-TikTok redesign.
- Per the rolling-window rule: the "ก.ค. (1-27)" label was already the last entry in both `AF_MO` (Affiliate_Dashboard) and the equivalent index in `AFI_MONTHS` (Mobile) — **overwrote the last index only**, did not touch any earlier month:
  - `AF_GMV`/`AFI_GMV` last: 1,329,672 → **1,329,842**
  - `AF_NET`/`AFI_NET` last: 1,245,231 → **1,245,310**
  - `AF_COM`/`AFI_COMM` last: 153,205 → **153,499**
  - Also fixed a label lag in `AFI_MONTHS` on Mobile — it still read "(1-26)" while the data was already through the 27th; updated to "(1-27)" to match `AF_MO`.

## 3. Cache version — ✅ done

`sw.js` bumped `wibwub-v486` → `wibwub-v487`.

## 4. Git commit — ✅ done, ⚠️ push needs manual trigger

- Staged only the 3 intended files (`WIBWUB_Mobile.html`, `WIBWUB_Affiliate_Dashboard.html`, `sw.js`) — 8 insertions / 8 deletions, all attributable to the changes above. Left all the other unrelated in-progress/untracked files from concurrent automations untouched.
- Hit the same `.git/index.lock` contention as the earlier run today (other automations committing concurrently); retried and succeeded on the first clean window — commit `1d8bf3e`.
- **Push failed as expected** — sandbox network proxy returns HTTP 403 to github.com (documented sandbox limitation, not an error to fix). `push_now.command` in the folder root was already correctly configured as a push-only script from an earlier fix; **double-click it** to push commit `1d8bf3e` (and any other pending local commits) to origin/main.

## Files changed (committed locally, not yet pushed)
- `WIBWUB_Affiliate_Dashboard.html` — `AF_GMV`, `AF_NET`, `AF_COM` (last index only)
- `WIBWUB_Mobile.html` — `AFI_MONTHS` (label fix), `AFI_GMV`, `AFI_NET`, `AFI_COMM` (last index only)
- `sw.js` — cache version v486 → v487
