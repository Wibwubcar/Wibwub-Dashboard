# WIBWUB Sales Sheet Update — 2026-08-02 (run 2)

## Result: no new sales data, one housekeeping fix applied

## Data check (ยอดประจำปี — latest cumulative row)

Re-read Shopee and Lazada "ยอดประจำปี 2026" tables fresh this run. Latest row for both is still
**01-26/07/26** — same cutoff as the 04:54 run earlier today. No row past July 26, no August row.

| แหล่ง | ยอดขาย | Ads | ค่าธรรมเนียม/คอมมิชชั่น | คูปอง | order | cancel |
|---|---|---|---|---|---|---|
| Shopee (01-26/07/26) | 5,012,235 | 812,947.25 | 1,501,665.61 | — | 9,081 | 453 (4.99%) |
| Lazada (01-26/07/26) | 85,766.88 | 7,210 | 15,147.36 | 2,880 | — | 29.43% cost |

Matches what's already in `SH_REV[6]`/`LZ_REV[6]` etc. in both dashboards exactly (SH_ADS[6] in-file
is 972,772 vs 812,947 in the annual table — left untouched per prior run's documented decision: the
in-file figure comes from a more complete ads report that already covers past the 26th).

### TikTok — still not directly re-verifiable
`read_file_content`/`download_file_content` on the TikTok sheet again exceeded this environment's
context/token limits (217k+ char single-line payload, 6.1MB base64 export) with no reachable path
for jq/python slicing, confirmed again via a dedicated subagent attempt. `TK_REV[6]` in both files
(1,803,127.22) is left as-is — unchanged since the last positively-confirmed read, consistent with
Shopee/Lazada showing no team activity past 26/07.

**Recommendation:** this TikTok sheet has grown too large for the current read tools to handle at
all. Worth asking the team to archive/trim old rows in that sheet, or set up a dedicated
narrower-range export, so future runs can positively confirm TikTok numbers instead of inferring.

## Fix applied: M5 label array

`const M5` in both `WIBWUB_Dashboard.html` and `WIBWUB_Mobile.html` only had 7 month labels
(ม.ค.–ก.ค.), one short of today's month count (8, since it's now August). Per the M5 protection
rule, added `"ส.ค."` as the 8th label in both files. This only adds a chart label — no data arrays
were touched, so no index-7 (August) entries were added to SH_REV/TK_REV/LZ_REV/etc. (correct, since
no August data exists in the sheets yet).

Date picker (`MP_MONTH_BOUNDS`, `MONTH_LABELS_FULL/SHORT`, `rangeEnd`) was left untouched — those
only need updating when a new *data* month is added, which didn't happen this run.

## Git / push
- Committed `WIBWUB_Dashboard.html`, `WIBWUB_Mobile.html`, `sw.js` (cache bumped v539→v540).
- Commit: `7b6a0e7 auto-update: M5 label fix (add ส.ค.) — 2026-08-02, no new SH/TK/LZ data this run`
- `push_now.command` already exists in the folder from a prior run — double-click it to push to
  `origin main` (sandbox can't push directly, HTTP 403 via proxy).

## Summary
- No new Shopee/Lazada/TikTok sales figures this run — same July 26 cutoff as the earlier run today.
- Fixed a real bug: M5 chart-label array was missing August, now fixed in both dashboards.
- TikTok sheet remains unreadable with current tools — flagged for follow-up.
