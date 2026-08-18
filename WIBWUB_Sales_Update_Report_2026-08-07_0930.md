# WIBWUB Sales Sheet Update — 2026-08-07 09:30

## Result: no update — August 2026 data incomplete (TikTok has no row yet)

## Sheet check (last cumulative row per platform, ยอดประจำปี tables)

| แหล่ง | เดือนล่าสุดที่มีข้อมูลครบ | เดือน ส.ค. มีข้อมูลหรือไม่ |
|---|---|---|
| Shopee | 01-31/07/26 → 5,923,704 / ads 942,122.40 / fee 1,774,741.72 / order 10,511 (cancel 5.34%) | มีแล้ว: 01-05/08/26 → 915,507 / ads 119,320.69 / fee 274,285.90 / order 1,552 (cancel 6.70%) |
| Lazada | 01-31/07/26 → 95,770.98 / ads 9,710 / fee 16,914.09 / cost% 30.99 | มีแล้ว: 01-05/08/26 → 6,852.00 / ads 1,510 / fee 1,210.99 / coupon 180 / cost% 42.34 |
| TikTok | 01-31/07/26 → 2,089,005.47 / ads 508,456.37 / commission 613,482.79 / order 10,094 | **ยังไม่มี** — ไม่พบ row `01-XX/08/26` ในชีท |

**เนื่องจาก TikTok ยังไม่มีข้อมูลเดือน ส.ค. — ข้ามการเพิ่ม label เดือนใหม่ทั้งหมด** (ตามกฎ: ต้องมีข้อมูลจริงครบทุก
แหล่งก่อนถึงจะ push label + ค่าใหม่พร้อมกันได้ ไม่งั้นจะเกิด array length mismatch แบบเดียวกับบั๊กที่เจอเมื่อ 3/6 ส.ค.)

## Protection check (STEP 0)
`M5` / `SH_REV` / `TK_REV` / `LZ_REV` / `SH_ORD` / `SH_CANCEL_PCT` / `SH_ADS` / `SH_FEE` / `LZ_ADS` / `LZ_FEE` /
`LZ_COUPON` / `LZ_COST_PCT` / `MONTH_LABELS_FULL` / `MONTH_LABELS_SHORT` / `MP_MONTH_BOUNDS` — all report
count=7 in both `WIBWUB_Dashboard.html` and `WIBWUB_Mobile.html`. No mismatch. `rangeEnd=6` in Dashboard,
matches July as latest month.

Index 6 (July) values verified to match sheet totals above exactly for Shopee/TikTok/Lazada revenue and
orders — no drift since the 2026-08-06 run.

## Committed
No file changes made — nothing to commit or push this run.

## Next run
Watch for TikTok's `01-XX/08/26` row to appear. Once it does, add "ส.ค." to `M5`/`MONTH_LABELS_FULL`/
`MONTH_LABELS_SHORT`/`MP_MONTH_BOUNDS` and push real August values into every array (SH/TK/LZ REV, ORD,
ADS, FEE, CANCEL_PCT, COUPON, COST_PCT) together in the same run, per STEP 3B.
