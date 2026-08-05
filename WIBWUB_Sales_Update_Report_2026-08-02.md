# WIBWUB Sales Sheet Update — 2026-08-02

## ผลลัพธ์: ไม่มีการเปลี่ยนแปลง (No new data — already up to date)

Task: WIBWUB Sales Sheet Update (Shopee / TikTok / Lazada → WIBWUB_Dashboard.html + WIBWUB_Mobile.html)

## ข้อมูลที่อ่านได้จาก Google Sheets (ยอดประจำปี — สะสมล่าสุด)

Re-fetched Shopee and Lazada "ยอดประจำปี 2026" tables fresh this run. Latest cumulative row for
July 2026 in **both** sheets is still **01-26/07/26** — no row past the 26th, and no August row yet.

| แหล่ง | ยอดขาย | Ads spend | ค่าธรรมเนียม/คอมมิชชั่น | คูปอง | order | ยกเลิก/cancel |
|---|---|---|---|---|---|---|
| Shopee (01-26/07/26) | 5,012,235 | 812,947.25 | 1,501,665.61 | — | 9,081 | 453 (4.99%) |
| Lazada (01-26/07/26) | 85,766.88 | 7,210 | 15,147.36 | 2,880 | — | — (29.43% cost) |
| TikTok | not directly re-verified this run — see note below | | | | | |

### TikTok note
`read_file_content` on the TikTok fileId again exceeded the tool's context limit (217k+ chars,
single unbroken line) and `download_file_content` (full xlsx export, ~6.18M base64 chars) also
couldn't be sliced — this sandbox has no reachable path to the host temp file the tool spills to,
and no jq/python access to the raw payload. A dedicated subagent confirmed via targeted
existence-checks that the live sheet's latest row is **01-26/07/26** (same cutoff as Shopee/Lazada,
no later date found) but could not extract the exact numeric values this way either.
`TK_REV[6]` already in both HTML files (1,803,127.22) matches the last positively-confirmed exact
value from a prior run's successful read (2026-07-31), and since Shopee/Lazada — freshly
re-verified today — are unchanged from that same 26/07 cutoff with no team activity in git log
since, it's reasonable to conclude TikTok is unchanged too.

Note: a stale local mirror `data content/ส่งเสริมการขายTIKTOK.xlsx` (last modified 2026-06-29) was
found in the workspace folder but was **not used** — it only has confirmed data through April 2026
and does not reflect the live sheet.

## เทียบกับค่าปัจจุบันในไฟล์ (index 6 = ก.ค. 2026)

- `SH_REV[6]`, `SH_FEE[6]`, `SH_ORD[6]`, `SH_CANCEL_PCT[6]` — ตรงกับ sheet เป๊ะ
- `SH_ADS[6]` = 972,772 in file vs 812,947.25 from the "ยอดประจำปี" table — left as-is, consistent
  with the prior run's documented decision (this field is sourced from a more complete ads report
  covering later than the 26th; overwriting would be a regression).
- `LZ_REV[6]`, `LZ_ADS[6]`, `LZ_FEE[6]`, `LZ_COUPON[6]`, `LZ_COST_PCT[6]` — ตรงกับ sheet เป๊ะ
- `TK_REV[6]` — ตรงกับค่าล่าสุดที่เคยยืนยันได้ (1,803,127.22)

No index-7 (August) entries exist yet in any revenue/order array in either file — correct, since no
August row has appeared in Shopee/Lazada sheets yet.

## M5 check
`const M5` in both files already lists 8 months (through ส.ค.), satisfying the protection rule
(count ≥ today.month = 8). No fix needed. Numeric arrays still correctly have 7 entries (Jan–Jul) —
this is expected and harmless per the note in the 2026-08-01 report; do not pre-fill index 7 until
real August data exists.

## Git / commit status
- No edits made to `WIBWUB_Dashboard.html`, `WIBWUB_Mobile.html`, or `sw.js` this run.
- No commit, no `push_now.command` created — nothing to push for this pipeline.

## Summary
- No new Shopee/TikTok/Lazada sales data found beyond what's already recorded for July 2026 (index 6, cutoff 01-26/07/26).
- No August 2026 data exists in the sheets yet.
- Files intentionally left untouched per the "no new data → skip" rule.
- Recommend a future run retry the TikTok annual-table read with a tool/environment that has a
  host-reachable path for jq/python slicing, to positively confirm TikTok numbers directly rather
  than via corroboration.
